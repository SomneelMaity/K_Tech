from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class StrategyOutput(BaseModel):
    """Structured output of the strategy stage."""

    angle: str = Field(
        description=(
            "The single strongest creative angle for this post, in one or two "
            "sentences. Concrete, not generic."
        )
    )
    audience: str = Field(
        description="The specific target audience this angle speaks to, in one sentence."
    )


class CopyVariant(BaseModel):
    hook: str = Field(
        description="A scroll-stopping first line / hook, max ~12 words."
    )
    caption: str = Field(
        description="The full post caption, engaging and within the platform's limits."
    )
    hashtags: List[str] = Field(
        description="Relevant hashtags WITHOUT the leading # symbol, count per platform norms."
    )


class CopyOutput(BaseModel):
    """Structured output Claude is forced to return for the copy stage."""

    variants: List[CopyVariant] = Field(
        description=(
            "Exactly 3 distinct copy variants for the same angle - different "
            "hooks and caption structures, not rewordings of each other."
        )
    )
    image_prompt: str = Field(
        description=(
            "A detailed, visual text-to-image prompt depicting the concept of "
            "this post. Describe subject, setting, mood, and composition. No text "
            "in the image."
        )
    )


class CampaignRequest(BaseModel):
    goal: str = "awareness"
    duration_days: int = Field(default=14, ge=3, le=90)
    budget_level: str = "starter"


class CampaignChannel(BaseModel):
    channel: str = Field(description="Distribution channel or placement.")
    role: str = Field(description="How this channel supports the campaign.")
    action: str = Field(description="Concrete action to take on this channel.")


class CampaignCalendarItem(BaseModel):
    day: str = Field(description="Relative day label, e.g. Day 1.")
    channel: str
    asset: str
    message: str
    cta: str


class CampaignExperiment(BaseModel):
    hypothesis: str
    variant_a: str
    variant_b: str
    metric: str


class CampaignPlan(BaseModel):
    campaign_name: str
    objective: str
    funnel_stage: str
    primary_audience: str
    positioning: str
    primary_cta: str
    organic_plan: List[str]
    paid_plan: List[str]
    channel_mix: List[CampaignChannel]
    content_calendar: List[CampaignCalendarItem]
    kpis: List[str]
    experiments: List[CampaignExperiment]
    budget_note: str
    utm_campaign: str
    launch_checklist: List[str]


class AutomationRequest(BaseModel):
    platforms: List[str] = Field(default_factory=lambda: ["x", "instagram"])
    daily_budget_usd: float = Field(default=10, ge=1, le=10000)
    duration_days: int = Field(default=14, ge=1, le=90)
    launch_paid: bool = False
    activate_paid: bool = False
    dry_run: bool = False
    destination_url: Optional[str] = None
    targeting_country: str = Field(default="US", min_length=2, max_length=2)


class AutomationStep(BaseModel):
    platform: str
    action: str
    status: str
    message: str
    external_id: str = ""
    url: str = ""
    details: Dict[str, Any] = Field(default_factory=dict)


class AutomationResult(BaseModel):
    id: str
    generation_id: str
    status: str
    summary: str
    request: AutomationRequest
    steps: List[AutomationStep]
    created_at: str


class GenerateRequest(BaseModel):
    idea: str = Field(min_length=1)
    platform: str = "instagram"
    tone: str = "friendly"
    image_style: str = "photo"


class RegenerateImageRequest(BaseModel):
    image_prompt: Optional[str] = None
    image_style: Optional[str] = None


class UpdateGenerationRequest(BaseModel):
    hook: Optional[str] = None
    caption: Optional[str] = None
    hashtags: Optional[List[str]] = None


class AssistantMessage(BaseModel):
    role: str = Field(pattern="^(user|assistant)$")
    content: str = Field(min_length=1)


class AssistantChatRequest(BaseModel):
    messages: List[AssistantMessage] = Field(min_length=1)


class AssistantChatResponse(BaseModel):
    reply: str
    generation_id: Optional[str] = None


class GenerationOut(BaseModel):
    id: str
    idea: str
    platform: str
    tone: str
    image_style: str
    angle: str
    audience: str
    hook: str
    caption: str
    hashtags: List[str]
    variants: List[CopyVariant]
    image_prompt: str
    image_url: str
    image_aspect: str
    campaign_plan: Optional[CampaignPlan]
    automation_runs: List[AutomationResult]
    status: str
    failed_stage: str
    error: str
    duration_ms: int
    created_at: str

    @classmethod
    def from_model(cls, g) -> "GenerationOut":
        campaign_plan = None
        if g.campaign_plan:
            try:
                campaign_plan = CampaignPlan(**g.campaign_plan)
            except (TypeError, ValueError):
                campaign_plan = None
        automation_runs = []
        for run in g.automation_runs or []:
            try:
                automation_runs.append(AutomationResult(**run))
            except (TypeError, ValueError):
                continue

        return cls(
            id=g.id,
            idea=g.idea,
            platform=g.platform,
            tone=g.tone,
            image_style=g.image_style,
            angle=g.angle or "",
            audience=g.audience or "",
            hook=g.hook or "",
            caption=g.caption or "",
            hashtags=g.hashtags or [],
            variants=[CopyVariant(**v) for v in (g.variants or [])],
            image_prompt=g.image_prompt or "",
            image_url=g.image_url or "",
            image_aspect=g.image_aspect or "1:1",
            campaign_plan=campaign_plan,
            automation_runs=automation_runs,
            status=g.status,
            failed_stage=g.failed_stage or "",
            error=g.error or "",
            duration_ms=g.duration_ms or 0,
            created_at=g.created_at.isoformat() if g.created_at else "",
        )
