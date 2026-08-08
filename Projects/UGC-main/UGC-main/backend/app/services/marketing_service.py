"""Campaign planning for generated content."""

import logging
import re

from ..config import settings
from ..models import Generation
from ..schemas import (
    CampaignCalendarItem,
    CampaignChannel,
    CampaignExperiment,
    CampaignPlan,
    CampaignRequest,
)
from .llm import get_client

logger = logging.getLogger(__name__)

SYSTEM = (
    "You are a senior growth marketer who turns one generated social post into "
    "a practical campaign plan. You connect every recommendation to the post, "
    "the audience, and the selected campaign goal. Be specific, testable, and "
    "ready for a founder or marketer to execute. Keep every field concise so "
    "the full structured response fits without truncation."
)


def _slug(text: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return value[:48] or "ugc-campaign"


def _goal_context(goal: str) -> tuple[str, str, list[str]]:
    normalized = goal.lower()
    if normalized in {"lead", "leads", "lead generation"}:
        return (
            "Lead generation",
            "consideration",
            ["link clicks", "landing page conversion rate", "new leads", "cost per lead"],
        )
    if normalized in {"sales", "conversion", "conversions"}:
        return (
            "Sales conversion",
            "conversion",
            ["click-through rate", "conversion rate", "cost per acquisition", "return on ad spend"],
        )
    if normalized in {"retention", "community", "engagement"}:
        return (
            "Community engagement",
            "retention",
            ["comments", "shares", "saves", "returning profile visits"],
        )
    return (
        "Brand awareness",
        "awareness",
        ["reach", "impressions", "saves", "shares", "profile visits"],
    )


def _build_prompt(g: Generation, req: CampaignRequest) -> str:
    hashtags = " ".join(f"#{h}" for h in (g.hashtags or [])) or "none"
    variants = "\n".join(
        f"- {v.get('hook', '')}: {v.get('caption', '')[:180]}"
        for v in (g.variants or [])[:3]
    )
    if not variants:
        variants = "- No alternate variants available."

    return (
        "Create a campaign plan for this generated content.\n\n"
        f"Campaign goal: {req.goal}\n"
        f"Duration: {req.duration_days} days\n"
        f"Budget level: {req.budget_level}\n\n"
        f"Original idea:\n{g.idea}\n\n"
        f"Primary platform: {g.platform}\n"
        f"Tone: {g.tone}\n"
        f"Creative angle: {g.angle or 'not specified'}\n"
        f"Target audience: {g.audience or 'not specified'}\n\n"
        "Generated post:\n"
        f"Hook: {g.hook}\n"
        f"Caption: {g.caption}\n"
        f"Hashtags: {hashtags}\n\n"
        "Available copy variants:\n"
        f"{variants}\n\n"
        "Use these planning principles:\n"
        "- Treat the campaign as one strategic effort with multiple assets that ladder to one measurable goal.\n"
        "- Include a clear CTA and measurable KPI set tied to the funnel stage.\n"
        "- Recommend organic distribution, paid amplification, and creative testing.\n"
        "- Use multiple distinct creative variants, not tiny wording changes.\n"
        "- For short-form platforms, prioritize the hook and make the creative native to the platform.\n"
        "- Keep the launch plan realistic for a small team.\n\n"
        "Return a compact plan with exactly 4 calendar items, 3 channels, "
        "4 KPIs, 2 experiments, and 4 launch checklist items. Keep list items "
        "under 18 words and avoid long explanations."
    )


async def generate_campaign_plan(g: Generation, req: CampaignRequest) -> CampaignPlan:
    if not settings.has_anthropic:
        return _mock(g, req)

    try:
        message = await get_client().messages.parse(
            model=settings.STRATEGY_MODEL,
            max_tokens=5000,
            system=SYSTEM,
            messages=[{"role": "user", "content": _build_prompt(g, req)}],
            output_format=CampaignPlan,
        )
        parsed = message.parsed_output
        if parsed is not None:
            return parsed
    except Exception:
        logger.exception("Campaign plan generation failed; using deterministic fallback")

    return _mock(g, req)


def _mock(g: Generation, req: CampaignRequest) -> CampaignPlan:
    objective, stage, kpis = _goal_context(req.goal)
    hook = g.hook or (g.idea.strip().split("\n")[0][:80] or "Generated UGC post")
    audience = g.audience or "People already showing interest in this problem"
    cta = "Save this post and visit the offer page"
    if stage == "consideration":
        cta = "Join the waitlist"
    elif stage == "conversion":
        cta = "Start today"
    elif stage == "retention":
        cta = "Comment with your use case"

    secondary_platform = "email"
    if g.platform in {"instagram", "facebook"}:
        secondary_platform = "stories"
    elif g.platform == "tiktok":
        secondary_platform = "spark ads"
    elif g.platform in {"x", "threads"}:
        secondary_platform = "reply thread"

    calendar_days = [
        ("Day 1", g.platform, "Primary post", hook, cta),
        ("Day 2", secondary_platform, "Behind-the-scenes note", "Why this matters now", cta),
        ("Day 4", g.platform, "Variant repost", "Test a sharper hook against the original", cta),
        ("Day 7", "retargeting", "Paid amplification", "Promote the best early engagement angle", cta),
        (f"Day {min(req.duration_days, 12)}", "email or DM", "Follow-up asset", "Turn social engagement into a direct response", cta),
    ]

    return CampaignPlan(
        campaign_name=f"{objective}: {_slug(hook).replace('-', ' ').title()}",
        objective=f"Use the generated {g.platform} post to drive {objective.lower()} over {req.duration_days} days.",
        funnel_stage=stage,
        primary_audience=audience,
        positioning=g.angle or f"Show a clear before/after around {g.idea[:80]}",
        primary_cta=cta,
        organic_plan=[
            f"Publish the generated post on {g.platform} with the strongest hook as line one.",
            "Reply to every early comment within the first hour to compound reach.",
            "Repurpose the alternate hooks as follow-up posts instead of treating them as duplicates.",
            "Pin the clearest CTA comment or profile link so interested viewers have a next step.",
        ],
        paid_plan=[
            "Wait for the first organic signal before boosting; use the post with highest save/share or click rate.",
            "Run a small retargeting set against engagers and profile visitors.",
            "Refresh creative if reach or click-through declines for two consecutive checks.",
        ],
        channel_mix=[
            CampaignChannel(
                channel=g.platform,
                role="Primary discovery surface",
                action="Launch the generated creative and monitor hook retention signals.",
            ),
            CampaignChannel(
                channel=secondary_platform,
                role="Context and reminder layer",
                action="Reframe the same angle with a shorter proof point and CTA.",
            ),
            CampaignChannel(
                channel="retargeting",
                role="Conversion assist",
                action="Promote the winning hook to people who engaged but did not act.",
            ),
            CampaignChannel(
                channel="email or DM",
                role="Direct response capture",
                action="Send a concise follow-up built around the same promise and CTA.",
            ),
        ],
        content_calendar=[
            CampaignCalendarItem(
                day=day, channel=channel, asset=asset, message=message, cta=item_cta
            )
            for day, channel, asset, message, item_cta in calendar_days
        ],
        kpis=kpis,
        experiments=[
            CampaignExperiment(
                hypothesis="A problem-first hook will create more qualified engagement than a benefit-first hook.",
                variant_a=hook,
                variant_b=(g.variants or [{}])[-1].get("hook", "Use the most direct benefit as the first line"),
                metric="save/share rate",
            ),
            CampaignExperiment(
                hypothesis="A direct CTA will convert better after social proof appears in comments.",
                variant_a=cta,
                variant_b="Comment 'guide' for the next step",
                metric=kpis[-1],
            ),
        ],
        budget_note=(
            f"Budget level: {req.budget_level}. Start with a small boost only after organic proof, "
            "then shift spend toward the winning hook and audience."
        ),
        utm_campaign=_slug(f"{req.goal}-{g.platform}-{hook}"),
        launch_checklist=[
            "Confirm the destination link matches the promise in the caption.",
            "Prepare two alternate hooks before launch.",
            "Set UTM parameters before publishing.",
            "Check performance at 24 hours and 72 hours.",
            "Document the winning hook, CTA, and audience for the next generation.",
        ],
    )
