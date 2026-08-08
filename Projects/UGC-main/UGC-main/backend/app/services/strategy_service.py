"""Stage 1 of the pipeline: creative angle + target audience, via a fast Claude model."""

from ..config import settings
from ..schemas import StrategyOutput
from . import platform_specs
from .llm import get_client

SYSTEM = (
    "You are a senior social media strategist. Given a raw idea, you identify "
    "the single strongest creative angle and the specific audience it will "
    "resonate with. You are concrete and opinionated — never generic."
)


def _build_prompt(idea: str, platform: str, tone: str) -> str:
    return (
        f"Idea / product / topic:\n{idea}\n\n"
        f"Platform: {platform}\n"
        f"Desired tone: {tone}\n\n"
        f"{platform_specs.copy_constraints(platform)}\n\n"
        "Pick the single strongest angle for a post about this, and the "
        "specific audience it targets. The angle will be handed to a "
        "copywriter, so make it actionable."
    )


async def generate_strategy(idea: str, platform: str, tone: str) -> StrategyOutput:
    if not settings.has_anthropic:
        return _mock(idea)

    message = await get_client().messages.parse(
        model=settings.STRATEGY_MODEL,
        max_tokens=500,
        system=SYSTEM,
        messages=[{"role": "user", "content": _build_prompt(idea, platform, tone)}],
        output_format=StrategyOutput,
    )
    parsed = message.parsed_output
    if parsed is None:
        return _mock(idea)
    return parsed


def _mock(idea: str) -> StrategyOutput:
    """Used when no ANTHROPIC_API_KEY is set, so the app runs out of the box."""
    short = idea.strip().split("\n")[0][:80]
    return StrategyOutput(
        angle=f"[demo] Show the before/after of using: {short}",
        audience="[demo] People actively searching for this kind of solution",
    )
