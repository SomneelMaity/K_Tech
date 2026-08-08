"""Voice assistant: a Claude tool-use loop that drives the app's own actions.

The frontend sends the spoken transcript (plus prior turns); Claude decides
which tools to call, we execute them against the same services the REST
routers use, and the final text reply is spoken aloud by the browser.
"""

import json
from typing import Any, Dict, List, Optional, Tuple

from fastapi import BackgroundTasks
from sqlalchemy.orm import Session

from ..config import settings
from ..database import SessionLocal
from ..models import Generation
from ..schemas import CampaignRequest
from . import copy_service, image_service, marketing_service, pipeline, platform_specs
from .llm import get_client

IN_FLIGHT = {"queued", "researching", "writing", "rendering"}

MAX_TOOL_ROUNDS = 8

SYSTEM_PROMPT = """\
You are Jarvis, the voice assistant for Faceless UGC Factory - an app that turns
a content idea into a ready-to-post social media asset (strategy angle, caption
with hook and hashtags, and an AI-generated image).

Your replies are read aloud by a speech synthesizer, so:
- Keep them short: one to three conversational sentences.
- Plain prose only. No markdown, no bullet points, no emojis, no URLs.
- Never read IDs, hashes, or file paths out loud.

You act on the user's spoken commands using your tools. Valid values:
- platform: instagram, tiktok, x, facebook, threads (default instagram)
- tone: friendly, professional, witty, bold, inspirational, casual (default friendly)
- image_style: photo, sketch, monochrome, 3d, cartoon, minimal (default photo)

Map natural speech to the closest valid value (e.g. "funny" -> witty,
"drawing" -> sketch). When the user references "my last post" or "the latest
one", call list_posts and use the most recent entry.

Creating a post kicks off a background pipeline that takes roughly 30 to 60
seconds - tell the user it's underway and that the screen will update, don't
pretend it's already finished. If a command is ambiguous, ask one short
clarifying question instead of guessing.
"""

TOOLS: List[Dict[str, Any]] = [
    {
        "name": "create_post",
        "description": (
            "Create a new social media post from an idea. Starts the background "
            "generation pipeline (strategy, copy, image). Returns the new post's "
            "id and status."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "idea": {"type": "string", "description": "The content idea, in the user's words."},
                "platform": {"type": "string", "enum": ["instagram", "tiktok", "x", "facebook", "threads"]},
                "tone": {"type": "string", "enum": ["friendly", "professional", "witty", "bold", "inspirational", "casual"]},
                "image_style": {"type": "string", "enum": ["photo", "sketch", "monochrome", "3d", "cartoon", "minimal"]},
            },
            "required": ["idea"],
        },
    },
    {
        "name": "list_posts",
        "description": "List the most recent posts, newest first, with id, idea, platform and status.",
        "input_schema": {
            "type": "object",
            "properties": {
                "limit": {"type": "integer", "description": "How many posts to return (default 5, max 20)."},
            },
        },
    },
    {
        "name": "get_post",
        "description": "Get the current status and content of one post by id.",
        "input_schema": {
            "type": "object",
            "properties": {"post_id": {"type": "string"}},
            "required": ["post_id"],
        },
    },
    {
        "name": "regenerate_copy",
        "description": "Rewrite the caption, hook and hashtags of a finished post, keeping its strategy angle.",
        "input_schema": {
            "type": "object",
            "properties": {"post_id": {"type": "string"}},
            "required": ["post_id"],
        },
    },
    {
        "name": "regenerate_image",
        "description": "Generate a new image for a post, optionally with a different style or prompt.",
        "input_schema": {
            "type": "object",
            "properties": {
                "post_id": {"type": "string"},
                "image_prompt": {"type": "string", "description": "Optional new text-to-image prompt."},
                "image_style": {"type": "string", "enum": ["photo", "sketch", "monochrome", "3d", "cartoon", "minimal"]},
            },
            "required": ["post_id"],
        },
    },
    {
        "name": "plan_campaign",
        "description": "Build a marketing campaign plan around a finished post.",
        "input_schema": {
            "type": "object",
            "properties": {
                "post_id": {"type": "string"},
                "goal": {"type": "string", "description": "Campaign goal, e.g. awareness, traffic, conversions."},
                "duration_days": {"type": "integer", "description": "Campaign length in days (3-90)."},
                "budget_level": {"type": "string", "description": "starter, growth, or scale."},
            },
            "required": ["post_id"],
        },
    },
]


def _summary(g: Generation) -> Dict[str, Any]:
    return {
        "id": g.id,
        "idea": g.idea,
        "platform": g.platform,
        "tone": g.tone,
        "image_style": g.image_style,
        "status": g.status,
        "hook": g.hook or "",
        "caption": (g.caption or "")[:280],
        "hashtags": g.hashtags or [],
        "has_image": bool(g.image_url),
        "has_campaign_plan": bool(g.campaign_plan),
        "error": g.error or "",
    }


async def _run_pipeline_bg(gid: str) -> None:
    # Background task: the request session is closed by now, use a fresh one.
    db = SessionLocal()
    try:
        g = db.get(Generation, gid)
        if g is not None:
            await pipeline.run_generation(g, db, "strategy")
    finally:
        db.close()


def _require_post(post_id: str, db: Session) -> Generation:
    g = db.get(Generation, post_id)
    if g is None:
        raise ValueError(f"No post found with id {post_id}. Use list_posts to find valid ids.")
    return g


def _require_finished(g: Generation) -> None:
    if g.status in IN_FLIGHT:
        raise ValueError("That post is still generating. Ask the user to wait a moment.")
    if g.status == "error":
        raise ValueError(f"That post failed at the {g.failed_stage or 'unknown'} stage: {g.error}")


async def _execute(
    name: str,
    args: Dict[str, Any],
    db: Session,
    background_tasks: BackgroundTasks,
) -> Tuple[Dict[str, Any], Optional[str]]:
    """Run one tool call. Returns (result payload, touched generation id)."""
    if name == "create_post":
        g = Generation(
            idea=args["idea"],
            platform=args.get("platform", "instagram"),
            tone=args.get("tone", "friendly"),
            image_style=args.get("image_style", "photo"),
            status="queued",
        )
        db.add(g)
        db.commit()
        db.refresh(g)
        background_tasks.add_task(_run_pipeline_bg, g.id)
        return _summary(g), g.id

    if name == "list_posts":
        limit = max(1, min(int(args.get("limit") or 5), 20))
        rows = (
            db.query(Generation)
            .order_by(Generation.created_at.desc())
            .limit(limit)
            .all()
        )
        return {"posts": [_summary(r) for r in rows]}, None

    if name == "get_post":
        g = _require_post(args["post_id"], db)
        return _summary(g), g.id

    if name == "regenerate_copy":
        g = _require_post(args["post_id"], db)
        _require_finished(g)
        copy = await copy_service.generate_copy(
            g.idea, g.platform, g.tone, g.image_style, g.angle or "", g.audience or ""
        )
        pipeline.apply_copy(g, copy)
        db.commit()
        db.refresh(g)
        return _summary(g), g.id

    if name == "regenerate_image":
        g = _require_post(args["post_id"], db)
        _require_finished(g)
        prompt = args.get("image_prompt") or g.image_prompt
        style = args.get("image_style") or g.image_style
        aspect = g.image_aspect or platform_specs.aspect_for(g.platform)
        g.image_prompt = prompt
        g.image_style = style
        g.image_aspect = aspect
        g.image_url = await image_service.generate_image(prompt, style, aspect)
        db.commit()
        db.refresh(g)
        return _summary(g), g.id

    if name == "plan_campaign":
        g = _require_post(args["post_id"], db)
        _require_finished(g)
        req = CampaignRequest(
            goal=args.get("goal") or "awareness",
            duration_days=max(3, min(int(args.get("duration_days") or 14), 90)),
            budget_level=args.get("budget_level") or "starter",
        )
        plan = await marketing_service.generate_campaign_plan(g, req)
        g.campaign_plan = plan.model_dump()
        db.commit()
        db.refresh(g)
        return {"post": _summary(g), "campaign_name": plan.campaign_name, "objective": plan.objective}, g.id

    raise ValueError(f"Unknown tool: {name}")


async def run_turn(
    messages: List[Dict[str, str]],
    db: Session,
    background_tasks: BackgroundTasks,
) -> Tuple[str, Optional[str]]:
    """Run one assistant turn. Returns (spoken reply, touched generation id)."""
    client = get_client()
    convo: List[Dict[str, Any]] = [
        {"role": m["role"], "content": m["content"]} for m in messages
    ]
    touched_id: Optional[str] = None

    for _ in range(MAX_TOOL_ROUNDS):
        resp = await client.messages.create(
            model=settings.ASSISTANT_MODEL,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=convo,
        )

        if resp.stop_reason != "tool_use":
            reply = "".join(b.text for b in resp.content if b.type == "text").strip()
            return reply or "Done.", touched_id

        convo.append({"role": "assistant", "content": resp.content})
        results = []
        for block in resp.content:
            if block.type != "tool_use":
                continue
            try:
                payload, gid = await _execute(block.name, dict(block.input), db, background_tasks)
                if gid:
                    touched_id = gid
                results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(payload),
                    }
                )
            except Exception as e:  # surface tool failures to the model, not as a 500
                results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps({"error": str(e)}),
                        "is_error": True,
                    }
                )
        convo.append({"role": "user", "content": results})

    return "Sorry, that took too many steps. Could you try a simpler request?", touched_id
