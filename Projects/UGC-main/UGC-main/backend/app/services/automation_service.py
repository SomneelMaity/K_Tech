"""One-click social publishing and paid campaign activation."""

import datetime as dt
import json
import mimetypes
import os
import uuid
from typing import List, Optional
from urllib.parse import urljoin

import httpx

from ..config import settings
from ..models import Generation
from ..schemas import AutomationRequest, AutomationResult, AutomationStep


def _step(
    platform: str,
    action: str,
    status: str,
    message: str,
    external_id: str = "",
    url: str = "",
    details: Optional[dict] = None,
) -> AutomationStep:
    return AutomationStep(
        platform=platform,
        action=action,
        status=status,
        message=message,
        external_id=external_id,
        url=url,
        details=details or {},
    )


def _post_text(g: Generation) -> str:
    hashtags = " ".join(f"#{h}" for h in (g.hashtags or []))
    parts = [g.hook or "", g.caption or "", hashtags]
    return "\n\n".join(p for p in parts if p.strip())


def _x_text(g: Generation) -> str:
    text = _post_text(g).replace("\r\n", "\n").strip()
    if len(text) <= 280:
        return text
    hashtags = " ".join(f"#{h}" for h in (g.hashtags or [])[:2])
    base = "\n\n".join(p for p in [g.hook or "", g.caption or ""] if p.strip())
    room = 277 - len(hashtags)
    shortened = base[: max(room, 40)].rstrip()
    return f"{shortened}... {hashtags}".strip()


def _image_path(g: Generation) -> Optional[str]:
    if not g.image_url or not g.image_url.startswith("/storage/"):
        return None
    filename = g.image_url.removeprefix("/storage/")
    path = os.path.join(settings.UPLOAD_DIR, filename)
    return path if os.path.exists(path) else None


def _public_image_url(g: Generation) -> str:
    if not g.image_url:
        return ""
    if g.image_url.startswith(("http://", "https://")):
        return g.image_url
    if not settings.PUBLIC_BASE_URL:
        return ""
    return urljoin(f"{settings.PUBLIC_BASE_URL}/", g.image_url.lstrip("/"))


def _ad_account_path() -> str:
    ad_account = settings.META_AD_ACCOUNT_ID
    if not ad_account.startswith("act_"):
        ad_account = f"act_{ad_account}"
    return ad_account


async def _publish_x(g: Generation, req: AutomationRequest) -> AutomationStep:
    if req.dry_run:
        return _step("x", "publish_post", "skipped", "Dry run: X post was not published.")
    if not settings.X_ACCESS_TOKEN:
        return _step(
            "x",
            "publish_post",
            "blocked",
            "Missing X_ACCESS_TOKEN with OAuth2 user write scopes.",
        )

    headers = {"Authorization": f"Bearer {settings.X_ACCESS_TOKEN}"}
    media_ids: List[str] = []
    image_path = _image_path(g)

    async with httpx.AsyncClient(timeout=60) as client:
        if image_path:
            mime_type = mimetypes.guess_type(image_path)[0] or "image/png"
            with open(image_path, "rb") as f:
                files = {"media": (os.path.basename(image_path), f.read(), mime_type)}
            data = {"media_category": "tweet_image", "media_type": mime_type}
            upload = await client.post(
                f"{settings.X_API_BASE}/media/upload",
                headers=headers,
                data=data,
                files=files,
            )
            if upload.status_code >= 400:
                return _step(
                    "x",
                    "upload_media",
                    "error",
                    "X media upload failed.",
                    details={"status_code": upload.status_code, "body": upload.text[:500]},
                )
            media_id = (upload.json().get("data") or {}).get("id")
            if media_id:
                media_ids.append(media_id)

        payload = {"text": _x_text(g)}
        if media_ids:
            payload["media"] = {"media_ids": media_ids}
        post = await client.post(
            f"{settings.X_API_BASE}/tweets",
            headers={**headers, "Content-Type": "application/json"},
            json=payload,
        )
        if post.status_code >= 400:
            return _step(
                "x",
                "publish_post",
                "error",
                "X post failed.",
                details={"status_code": post.status_code, "body": post.text[:500]},
            )

    data = post.json().get("data") or {}
    post_id = data.get("id", "")
    return _step(
        "x",
        "publish_post",
        "success",
        "Published to X.",
        external_id=post_id,
        url=f"https://x.com/i/web/status/{post_id}" if post_id else "",
    )


async def _publish_instagram(g: Generation, req: AutomationRequest) -> AutomationStep:
    if req.dry_run:
        return _step(
            "instagram",
            "publish_media",
            "skipped",
            "Dry run: Instagram media was not published.",
        )
    if not settings.META_ACCESS_TOKEN or not settings.META_IG_USER_ID:
        return _step(
            "instagram",
            "publish_media",
            "blocked",
            "Missing META_ACCESS_TOKEN or META_IG_USER_ID.",
        )

    image_url = _public_image_url(g)
    if not image_url:
        return _step(
            "instagram",
            "publish_media",
            "blocked",
            "Instagram requires PUBLIC_BASE_URL or an already-public image_url.",
        )

    base = f"https://graph.facebook.com/{settings.META_GRAPH_VERSION}"
    async with httpx.AsyncClient(timeout=60) as client:
        container = await client.post(
            f"{base}/{settings.META_IG_USER_ID}/media",
            data={
                "image_url": image_url,
                "caption": _post_text(g),
                "access_token": settings.META_ACCESS_TOKEN,
            },
        )
        if container.status_code >= 400:
            return _step(
                "instagram",
                "create_media_container",
                "error",
                "Instagram media container creation failed.",
                details={"status_code": container.status_code, "body": container.text[:500]},
            )
        creation_id = container.json().get("id", "")
        published = await client.post(
            f"{base}/{settings.META_IG_USER_ID}/media_publish",
            data={"creation_id": creation_id, "access_token": settings.META_ACCESS_TOKEN},
        )
        if published.status_code >= 400:
            return _step(
                "instagram",
                "publish_media",
                "error",
                "Instagram publish failed.",
                external_id=creation_id,
                details={"status_code": published.status_code, "body": published.text[:500]},
            )

    media_id = published.json().get("id", "")
    return _step(
        "instagram",
        "publish_media",
        "success",
        "Published to Instagram.",
        external_id=media_id,
    )


async def _create_meta_paid_campaign(g: Generation, req: AutomationRequest) -> List[AutomationStep]:
    if not req.launch_paid:
        return [_step("meta_ads", "create_paid_campaign", "skipped", "Paid launch disabled.")]
    if req.dry_run:
        return [
            _step(
                "meta_ads",
                "create_paid_campaign",
                "skipped",
                f"Dry run: would set ${req.daily_budget_usd:.2f}/day for {req.duration_days} days.",
            )
        ]
    if not settings.META_ACCESS_TOKEN or not settings.META_AD_ACCOUNT_ID:
        return [
            _step(
                "meta_ads",
                "create_paid_campaign",
                "blocked",
                "Missing META_ACCESS_TOKEN or META_AD_ACCOUNT_ID.",
            )
        ]

    campaign_name = (
        (g.campaign_plan or {}).get("campaign_name")
        or g.hook
        or f"UGC Campaign {g.id[:8]}"
    )
    base = f"https://graph.facebook.com/{settings.META_GRAPH_VERSION}/{_ad_account_path()}"
    status = "ACTIVE" if req.activate_paid else "PAUSED"
    budget_cents = max(100, int(req.daily_budget_usd * 100))
    start = dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=10)
    end = start + dt.timedelta(days=req.duration_days)
    steps: List[AutomationStep] = []

    async with httpx.AsyncClient(timeout=60) as client:
        campaign = await client.post(
            f"{base}/campaigns",
            data={
                "name": campaign_name,
                "objective": "OUTCOME_TRAFFIC",
                "status": status,
                "special_ad_categories": json.dumps([]),
                "access_token": settings.META_ACCESS_TOKEN,
            },
        )
        if campaign.status_code >= 400:
            return [
                _step(
                    "meta_ads",
                    "create_campaign",
                    "error",
                    "Meta campaign creation failed.",
                    details={"status_code": campaign.status_code, "body": campaign.text[:500]},
                )
            ]
        campaign_id = campaign.json().get("id", "")
        steps.append(
            _step(
                "meta_ads",
                "create_campaign",
                "success",
                f"Created Meta campaign in {status.lower()} status.",
                external_id=campaign_id,
            )
        )

        adset = await client.post(
            f"{base}/adsets",
            data={
                "name": f"{campaign_name} - Broad {req.targeting_country.upper()}",
                "campaign_id": campaign_id,
                "daily_budget": str(budget_cents),
                "billing_event": "IMPRESSIONS",
                "optimization_goal": "LINK_CLICKS",
                "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
                "start_time": start.isoformat(),
                "end_time": end.isoformat(),
                "status": status,
                "targeting": json.dumps(
                    {
                        "geo_locations": {"countries": [req.targeting_country.upper()]},
                        "publisher_platforms": ["facebook", "instagram"],
                    }
                ),
                "access_token": settings.META_ACCESS_TOKEN,
            },
        )
        if adset.status_code >= 400:
            steps.append(
                _step(
                    "meta_ads",
                    "create_ad_set",
                    "error",
                    "Meta ad set creation failed after campaign creation.",
                    details={"status_code": adset.status_code, "body": adset.text[:500]},
                )
            )
            return steps

    adset_id = adset.json().get("id", "")
    steps.append(
        _step(
            "meta_ads",
            "create_ad_set",
            "success",
            f"Set daily budget to ${req.daily_budget_usd:.2f} for {req.duration_days} days.",
            external_id=adset_id,
            details={"daily_budget_cents": budget_cents, "status": status},
        )
    )
    if not settings.META_PAGE_ID or not req.destination_url:
        steps.append(
            _step(
                "meta_ads",
                "create_ad",
                "blocked",
                "Campaign and ad set created, but ad creative needs META_PAGE_ID and destination_url.",
            )
        )
        return steps

    link_data = {
        "message": _post_text(g)[:500],
        "link": req.destination_url,
        "name": (g.hook or campaign_name)[:80],
        "description": (g.caption or g.idea)[:120],
        "call_to_action": {
            "type": "LEARN_MORE",
            "value": {"link": req.destination_url},
        },
    }
    image_url = _public_image_url(g)
    if image_url:
        link_data["picture"] = image_url

    async with httpx.AsyncClient(timeout=60) as client:
        creative = await client.post(
            f"{base}/adcreatives",
            data={
                "name": f"{campaign_name} - Creative",
                "object_story_spec": json.dumps(
                    {
                        "page_id": settings.META_PAGE_ID,
                        "link_data": link_data,
                    }
                ),
                "access_token": settings.META_ACCESS_TOKEN,
            },
        )
        if creative.status_code >= 400:
            steps.append(
                _step(
                    "meta_ads",
                    "create_ad_creative",
                    "error",
                    "Meta ad creative creation failed.",
                    details={"status_code": creative.status_code, "body": creative.text[:500]},
                )
            )
            return steps
        creative_id = creative.json().get("id", "")
        steps.append(
            _step(
                "meta_ads",
                "create_ad_creative",
                "success",
                "Created Meta ad creative.",
                external_id=creative_id,
            )
        )

        ad = await client.post(
            f"{base}/ads",
            data={
                "name": f"{campaign_name} - Ad",
                "adset_id": adset_id,
                "creative": json.dumps({"creative_id": creative_id}),
                "status": status,
                "access_token": settings.META_ACCESS_TOKEN,
            },
        )
        if ad.status_code >= 400:
            steps.append(
                _step(
                    "meta_ads",
                    "create_ad",
                    "error",
                    "Meta ad creation failed after creative creation.",
                    details={"status_code": ad.status_code, "body": ad.text[:500]},
                )
            )
            return steps

    steps.append(
        _step(
            "meta_ads",
            "create_ad",
            "success",
            f"Created Meta ad in {status.lower()} status.",
            external_id=ad.json().get("id", ""),
        )
    )
    return steps


async def execute_automation(g: Generation, req: AutomationRequest) -> AutomationResult:
    steps: List[AutomationStep] = []
    selected = {p.lower() for p in req.platforms}

    if "x" in selected or "twitter" in selected:
        steps.append(await _publish_x(g, req))
    if "instagram" in selected:
        steps.append(await _publish_instagram(g, req))
    steps.extend(await _create_meta_paid_campaign(g, req))

    successes = sum(1 for s in steps if s.status == "success")
    blockers = sum(1 for s in steps if s.status == "blocked")
    errors = sum(1 for s in steps if s.status == "error")
    status = "success" if errors == 0 and blockers == 0 and successes else "partial"
    if errors and not successes:
        status = "error"
    if blockers and not successes and not errors:
        status = "blocked"
    if req.dry_run:
        status = "dry_run"

    return AutomationResult(
        id=uuid.uuid4().hex,
        generation_id=g.id,
        status=status,
        summary=f"{successes} succeeded, {blockers} blocked, {errors} errored.",
        request=req,
        steps=steps,
        created_at=dt.datetime.utcnow().isoformat(),
    )
