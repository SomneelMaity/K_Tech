"""Stage 3 of the pipeline: styled image.

The provider is auto-selected (see ``IMAGE_PROVIDER``):
  * **Pollinations** — free, no API key, no billing. Flux under the hood.
    This is the default when no paid key is configured.
  * **Gemini** — Google's native image model (requires billing; free tier
    does *not* include image generation).
  * **Flux on Replicate** — paid, ~$0.003/image.
  * an **SVG placeholder** as a last resort.
"""

import asyncio
import base64
import os
import uuid
from urllib.parse import quote

import httpx

from ..config import settings

STYLE_MODIFIERS = {
    "photo": "photorealistic, high detail, professional product photography, natural light",
    "sketch": "pencil sketch, hand-drawn line art, monochrome, cross-hatching",
    "monochrome": "black and white, high contrast monochrome, dramatic lighting",
    "3d": "stylized 3d render, octane, soft cinematic lighting, depth of field",
    "cartoon": "flat vector cartoon illustration, bold clean outlines, vibrant colors",
    "minimal": "minimalist, lots of negative space, muted palette, clean and modern",
}

# Placeholder canvas sizes per supported aspect ratio.
_PLACEHOLDER_DIMS = {
    "1:1": (768, 768),
    "9:16": (576, 1024),
    "16:9": (1024, 576),
    "3:4": (768, 1024),
    "4:5": (819, 1024),
}

# Pixel dimensions Pollinations should render per aspect ratio.
_POLLINATIONS_DIMS = {
    "1:1": (1024, 1024),
    "9:16": (768, 1365),
    "16:9": (1365, 768),
    "3:4": (768, 1024),
    "4:5": (896, 1120),
}

# Aspect ratios Gemini's image model accepts natively; the app's set is a subset.
_GEMINI_ASPECTS = {"1:1", "9:16", "16:9", "3:4", "4:3", "4:5", "5:4", "2:3", "3:2"}


def _full_prompt(image_prompt: str, image_style: str, aspect_ratio: str) -> str:
    modifier = STYLE_MODIFIERS.get(image_style, STYLE_MODIFIERS["photo"])
    return f"{image_prompt}. Visual style: {modifier}. {aspect_ratio} framing."


def _select_provider() -> str:
    """Resolve which backend to call from config + available keys."""
    choice = settings.IMAGE_PROVIDER.lower()
    if choice == "gemini":
        return "gemini" if settings.has_gemini else "pollinations"
    if choice == "replicate":
        return "replicate" if settings.has_replicate else "pollinations"
    if choice in ("pollinations", "placeholder"):
        return choice
    # auto: paid keys win if explicitly configured, else the free provider.
    if settings.has_replicate:
        return "replicate"
    if settings.has_gemini:
        return "gemini"
    return "pollinations"


def _run_pollinations(prompt: str, aspect_ratio: str) -> tuple[bytes, str]:
    """Free image generation — no key. Returns (image_bytes, extension)."""
    w, h = _POLLINATIONS_DIMS.get(aspect_ratio, _POLLINATIONS_DIMS["1:1"])
    url = f"https://image.pollinations.ai/prompt/{quote(prompt)}"
    params = {
        "width": w,
        "height": h,
        "nologo": "true",
        "model": "flux",
        # fresh seed each call so identical prompts don't return a cached image
        "seed": uuid.uuid4().int % 1_000_000,
    }
    with httpx.Client(timeout=settings.IMAGE_TIMEOUT, follow_redirects=True) as client:
        resp = client.get(url, params=params)
        resp.raise_for_status()
        content = resp.content
    ctype = resp.headers.get("content-type", "")
    if not content or not ctype.startswith("image"):
        raise RuntimeError(f"Pollinations returned non-image ({ctype or 'unknown'})")
    ext = "png" if "png" in ctype else "jpg"
    return content, ext


def _run_gemini(prompt: str, aspect_ratio: str) -> bytes:
    """Call Gemini's native image model over REST; return raw PNG bytes."""
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{settings.GEMINI_IMAGE_MODEL}:generateContent"
    )
    generation_config: dict = {"responseModalities": ["IMAGE"]}
    if aspect_ratio in _GEMINI_ASPECTS:
        generation_config["imageConfig"] = {"aspectRatio": aspect_ratio}
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": generation_config,
    }
    headers = {"x-goog-api-key": settings.GEMINI_API_KEY}

    with httpx.Client(timeout=settings.IMAGE_TIMEOUT) as client:
        resp = client.post(url, json=body, headers=headers)
        resp.raise_for_status()
        data = resp.json()

    for part in data.get("candidates", [{}])[0].get("content", {}).get("parts", []):
        inline = part.get("inlineData") or part.get("inline_data")
        if inline and inline.get("data"):
            return base64.b64decode(inline["data"])
    raise RuntimeError(f"Gemini returned no image data: {str(data)[:300]}")


def _run_replicate(prompt: str, aspect_ratio: str):
    import replicate

    os.environ["REPLICATE_API_TOKEN"] = settings.REPLICATE_API_TOKEN
    return replicate.run(
        settings.IMAGE_MODEL,
        input={
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "output_format": "png",
            "num_outputs": 1,
        },
    )


def _save_image(content: bytes, ext: str = "png") -> str:
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    fname = f"{uuid.uuid4().hex}.{ext}"
    path = os.path.join(settings.UPLOAD_DIR, fname)
    with open(path, "wb") as f:
        f.write(content)
    return f"/storage/{fname}"


async def _download(url: str) -> str:
    async with httpx.AsyncClient(timeout=120) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return _save_image(resp.content, "png")


async def generate_image(
    image_prompt: str, image_style: str, aspect_ratio: str = "1:1"
) -> str:
    provider = _select_provider()
    if provider == "placeholder":
        return _placeholder(image_style, aspect_ratio)

    prompt = _full_prompt(image_prompt, image_style, aspect_ratio)

    # Providers cold-start / rate-limit transiently; retry with backoff, and cap
    # each attempt so a stuck request errors the row instead of hanging forever.
    last_exc: Exception = RuntimeError("image generation failed")
    for attempt in range(settings.IMAGE_RETRIES + 1):
        try:
            if provider == "pollinations":
                content, ext = await asyncio.wait_for(
                    asyncio.to_thread(_run_pollinations, prompt, aspect_ratio),
                    timeout=settings.IMAGE_TIMEOUT,
                )
                return _save_image(content, ext)

            if provider == "gemini":
                content = await asyncio.wait_for(
                    asyncio.to_thread(_run_gemini, prompt, aspect_ratio),
                    timeout=settings.IMAGE_TIMEOUT,
                )
                return _save_image(content, "png")

            output = await asyncio.wait_for(
                asyncio.to_thread(_run_replicate, prompt, aspect_ratio),
                timeout=settings.IMAGE_TIMEOUT,
            )
            # Flux returns a list of file outputs; str() yields a downloadable URL.
            item = output[0] if isinstance(output, (list, tuple)) else output
            return await _download(str(item))
        except Exception as exc:  # noqa: BLE001 - retry any provider error
            last_exc = exc
            if attempt < settings.IMAGE_RETRIES:
                await asyncio.sleep(2 * (2**attempt))  # 2s, 4s, ...
    raise last_exc


def _placeholder(image_style: str, aspect_ratio: str = "1:1") -> str:
    """SVG placeholder — last-resort fallback."""
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    w, h = _PLACEHOLDER_DIMS.get(aspect_ratio, _PLACEHOLDER_DIMS["1:1"])
    fname = f"{uuid.uuid4().hex}.svg"
    path = os.path.join(settings.UPLOAD_DIR, fname)
    svg = (
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{w}' height='{h}'>"
        "<rect width='100%' height='100%' fill='#1f2937'/>"
        "<text x='50%' y='46%' fill='#9ca3af' font-family='sans-serif' "
        "font-size='34' text-anchor='middle'>Demo image</text>"
        "<text x='50%' y='56%' fill='#6b7280' font-family='sans-serif' "
        f"font-size='22' text-anchor='middle'>style: {image_style}</text>"
        "</svg>"
    )
    with open(path, "w") as f:
        f.write(svg)
    return f"/storage/{fname}"
