"""Stage 2 of the pipeline: copy variants + image prompt, via Claude."""

from ..config import settings
from ..schemas import CopyOutput, CopyVariant
from . import platform_specs
from .llm import get_client

SYSTEM = (
    "You are an expert short-form social media copywriter. You write "
    "thumb-stopping, native-feeling content that drives engagement without "
    "sounding like an ad or generic AI text. You follow platform constraints "
    "exactly and always lead with a strong hook."
)


def _build_prompt(
    idea: str,
    platform: str,
    tone: str,
    image_style: str,
    angle: str,
    audience: str,
) -> str:
    strategy = ""
    if angle:
        strategy = (
            f"Creative angle (already decided — write to it, don't re-decide):\n{angle}\n"
            f"Target audience: {audience}\n\n"
        )
    return (
        f"Create one social media post for {platform}.\n\n"
        f"Idea / product / topic:\n{idea}\n\n"
        f"{strategy}"
        f"Desired tone: {tone}\n"
        f"Intended image style: {image_style}\n\n"
        f"{platform_specs.copy_constraints(platform)}\n\n"
        "Produce:\n"
        "1. Exactly 3 distinct copy variants (hook + caption + hashtags each). "
        "Vary the hook mechanism across variants — e.g. question, bold claim, "
        "pattern interrupt — not rewordings of the same line.\n"
        "2. One detailed text-to-image prompt that visually captures the "
        "concept of the post (sent to an image generator; describe subject, "
        "setting, mood, composition; no text in the image)."
    )


async def generate_copy(
    idea: str,
    platform: str,
    tone: str,
    image_style: str,
    angle: str = "",
    audience: str = "",
) -> CopyOutput:
    if not settings.has_anthropic:
        return _mock(idea, platform, image_style)

    message = await get_client().messages.parse(
        model=settings.COPY_MODEL,
        max_tokens=3000,
        system=SYSTEM,
        messages=[
            {
                "role": "user",
                "content": _build_prompt(
                    idea, platform, tone, image_style, angle, audience
                ),
            }
        ],
        output_format=CopyOutput,
    )
    parsed = message.parsed_output
    if parsed is None or not parsed.variants:
        # Refusal or unparseable output — fall back so the pipeline still completes.
        return _mock(idea, platform, image_style)
    return parsed


def _mock(idea: str, platform: str, image_style: str) -> CopyOutput:
    """Used when no ANTHROPIC_API_KEY is set, so the app runs out of the box."""
    short = idea.strip().split("\n")[0][:80]
    caption = (
        f"[demo copy] {short}\n\n"
        "Add your ANTHROPIC_API_KEY to .env to generate real, on-brand "
        f"captions for {platform}. This is placeholder text so you can see "
        "the full flow."
    )
    return CopyOutput(
        variants=[
            CopyVariant(
                hook=f"Stop scrolling — here's why {short} matters 👀",
                caption=caption,
                hashtags=["ugc", "contentcreation", "marketing", "founders", "ai"],
            ),
            CopyVariant(
                hook=f"Nobody talks about this side of {short}",
                caption=caption,
                hashtags=["growth", "socialmedia", "creator", "startup"],
            ),
        ],
        image_prompt=(
            f"A clean, eye-catching {image_style} style visual representing: "
            f"{short}. Centered composition, vibrant, social-media ready, no text."
        ),
    )
