"""Orchestrates the Content-to-Post pipeline: strategy -> copy -> image.

Runs as a background task. Status moves through
queued -> researching -> writing -> rendering -> complete, with `error` +
`failed_stage` set on any failure so a retry can resume from the failed
stage instead of re-paying for the ones that succeeded.
"""

import time

from sqlalchemy.orm import Session

from ..models import Generation
from . import copy_service, image_service, platform_specs, strategy_service

STAGE_ORDER = ("strategy", "copy", "image")

_STATUS_BY_STAGE = {
    "strategy": "researching",
    "copy": "writing",
    "image": "rendering",
}


def apply_copy(g: Generation, copy) -> None:
    """Write a CopyOutput onto the row; variant 0 is the default pick."""
    chosen = copy.variants[0]
    g.hook = chosen.hook
    g.caption = chosen.caption
    g.hashtags = chosen.hashtags
    g.variants = [v.model_dump() for v in copy.variants]
    g.image_prompt = copy.image_prompt
    g.campaign_plan = {}


async def _run_stage(g: Generation, stage: str) -> None:
    if stage == "strategy":
        strat = await strategy_service.generate_strategy(g.idea, g.platform, g.tone)
        g.angle = strat.angle
        g.audience = strat.audience
    elif stage == "copy":
        copy = await copy_service.generate_copy(
            g.idea, g.platform, g.tone, g.image_style, g.angle or "", g.audience or ""
        )
        apply_copy(g, copy)
    else:  # image
        g.image_aspect = platform_specs.aspect_for(g.platform)
        g.image_url = await image_service.generate_image(
            g.image_prompt, g.image_style, g.image_aspect
        )


async def run_generation(
    g: Generation, db: Session, from_stage: str = "strategy"
) -> Generation:
    start_idx = STAGE_ORDER.index(from_stage) if from_stage in STAGE_ORDER else 0
    started = time.perf_counter()
    stage = STAGE_ORDER[start_idx]
    try:
        for stage in STAGE_ORDER[start_idx:]:
            g.status = _STATUS_BY_STAGE[stage]
            db.commit()
            await _run_stage(g, stage)
            db.commit()
        g.status = "complete"
        g.failed_stage = ""
        g.error = ""
    except Exception as exc:  # noqa: BLE001 - surface any provider error to the UI
        g.status = "error"
        g.failed_stage = stage
        g.error = str(exc)

    g.duration_ms = (g.duration_ms or 0 if start_idx else 0) + int(
        (time.perf_counter() - started) * 1000
    )
    db.commit()
    db.refresh(g)
    return g
