from typing import List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import SessionLocal, get_db
from ..models import Generation
from ..schemas import (
    AutomationRequest,
    AutomationResult,
    CampaignRequest,
    GenerateRequest,
    GenerationOut,
    RegenerateImageRequest,
    UpdateGenerationRequest,
)
from ..services import (
    automation_service,
    copy_service,
    image_service,
    marketing_service,
    pipeline,
    platform_specs,
)

router = APIRouter(prefix="/api", tags=["generations"])

IN_FLIGHT = {"queued", "researching", "writing", "rendering"}


def _get_or_404(gid: str, db: Session) -> Generation:
    g = db.get(Generation, gid)
    if g is None:
        raise HTTPException(status_code=404, detail="Generation not found")
    return g


async def _run_pipeline(gid: str, from_stage: str = "strategy") -> None:
    # Background task: the request session is closed by now, use a fresh one.
    db = SessionLocal()
    try:
        g = db.get(Generation, gid)
        if g is not None:
            await pipeline.run_generation(g, db, from_stage)
    finally:
        db.close()


@router.post("/generate", response_model=GenerationOut, status_code=202)
async def generate(
    req: GenerateRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    g = Generation(
        idea=req.idea,
        platform=req.platform,
        tone=req.tone,
        image_style=req.image_style,
        status="queued",
    )
    db.add(g)
    db.commit()
    db.refresh(g)

    background_tasks.add_task(_run_pipeline, g.id)
    return GenerationOut.from_model(g)


@router.post("/generations/{gid}/retry", response_model=GenerationOut, status_code=202)
async def retry(
    gid: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)
):
    g = _get_or_404(gid, db)
    if g.status in IN_FLIGHT:
        raise HTTPException(status_code=409, detail="Generation is already running")
    from_stage = g.failed_stage if g.failed_stage in pipeline.STAGE_ORDER else "strategy"
    g.status = "queued"
    g.error = ""
    db.commit()
    db.refresh(g)

    background_tasks.add_task(_run_pipeline, gid, from_stage)
    return GenerationOut.from_model(g)


@router.get("/generations", response_model=List[GenerationOut])
def list_generations(db: Session = Depends(get_db)):
    rows = (
        db.query(Generation).order_by(Generation.created_at.desc()).limit(100).all()
    )
    return [GenerationOut.from_model(r) for r in rows]


@router.get("/generations/{gid}", response_model=GenerationOut)
def get_generation(gid: str, db: Session = Depends(get_db)):
    return GenerationOut.from_model(_get_or_404(gid, db))


@router.patch("/generations/{gid}", response_model=GenerationOut)
def update_generation(
    gid: str, req: UpdateGenerationRequest, db: Session = Depends(get_db)
):
    g = _get_or_404(gid, db)
    touched_copy = False
    if req.hook is not None:
        g.hook = req.hook
        touched_copy = True
    if req.caption is not None:
        g.caption = req.caption
        touched_copy = True
    if req.hashtags is not None:
        g.hashtags = req.hashtags
        touched_copy = True
    if touched_copy:
        g.campaign_plan = {}
    db.commit()
    db.refresh(g)
    return GenerationOut.from_model(g)


@router.post("/generations/{gid}/regenerate-copy", response_model=GenerationOut)
async def regenerate_copy(gid: str, db: Session = Depends(get_db)):
    g = _get_or_404(gid, db)
    # Reuse the stored angle so a rewrite keeps the winning strategy.
    copy = await copy_service.generate_copy(
        g.idea, g.platform, g.tone, g.image_style, g.angle or "", g.audience or ""
    )
    pipeline.apply_copy(g, copy)
    db.commit()
    db.refresh(g)
    return GenerationOut.from_model(g)


@router.post("/generations/{gid}/regenerate-image", response_model=GenerationOut)
async def regenerate_image(
    gid: str, req: RegenerateImageRequest, db: Session = Depends(get_db)
):
    g = _get_or_404(gid, db)
    prompt = req.image_prompt or g.image_prompt
    style = req.image_style or g.image_style
    aspect = g.image_aspect or platform_specs.aspect_for(g.platform)
    g.image_prompt = prompt
    g.image_style = style
    g.image_aspect = aspect
    g.image_url = await image_service.generate_image(prompt, style, aspect)
    db.commit()
    db.refresh(g)
    return GenerationOut.from_model(g)


@router.post("/generations/{gid}/campaign", response_model=GenerationOut)
async def generate_campaign(
    gid: str, req: Optional[CampaignRequest] = None, db: Session = Depends(get_db)
):
    g = _get_or_404(gid, db)
    if g.status in IN_FLIGHT:
        raise HTTPException(status_code=409, detail="Generation is still running")
    if g.status == "error":
        raise HTTPException(status_code=409, detail="Fix the generation before planning a campaign")

    plan = await marketing_service.generate_campaign_plan(g, req or CampaignRequest())
    g.campaign_plan = plan.model_dump()
    db.commit()
    db.refresh(g)
    return GenerationOut.from_model(g)


@router.post("/generations/{gid}/automation/launch", response_model=AutomationResult)
async def launch_automation(
    gid: str, req: AutomationRequest, db: Session = Depends(get_db)
):
    g = _get_or_404(gid, db)
    if g.status in IN_FLIGHT:
        raise HTTPException(status_code=409, detail="Generation is still running")
    if g.status == "error":
        raise HTTPException(status_code=409, detail="Fix the generation before launching")
    if not (g.hook or g.caption):
        raise HTTPException(status_code=409, detail="No generated content to publish")

    result = await automation_service.execute_automation(g, req)
    g.automation_runs = [result.model_dump()] + list(g.automation_runs or [])[:9]
    db.commit()
    return result
