"""Per-platform norms that drive copy constraints and image aspect ratio."""

from typing import TypedDict


class PlatformSpec(TypedDict):
    aspect_ratio: str
    max_chars: int
    hashtag_range: str
    norms: str


SPECS: dict[str, PlatformSpec] = {
    "instagram": {
        "aspect_ratio": "1:1",
        "max_chars": 2200,
        "hashtag_range": "8-12",
        "norms": (
            "Feed post. Hook must work as the first line before the fold. "
            "Line breaks between short paragraphs, emoji welcome in moderation, "
            "end with a CTA (save/share/comment)."
        ),
    },
    "tiktok": {
        "aspect_ratio": "9:16",
        "max_chars": 150,
        "hashtag_range": "3-6",
        "norms": (
            "Short caption; the hook doubles as on-screen overlay text, so keep "
            "it punchy and spoken-word natural. Caption complements, never "
            "repeats, the hook."
        ),
    },
    "x": {
        "aspect_ratio": "16:9",
        "max_chars": 280,
        "hashtag_range": "0-2",
        "norms": (
            "Single post, hard 280-character limit INCLUDING hashtags. No "
            "emoji spam, no engagement bait. Plain, sharp, quotable."
        ),
    },
    "facebook": {
        "aspect_ratio": "1:1",
        "max_chars": 600,
        "hashtag_range": "2-4",
        "norms": (
            "Conversational, slightly longer-form is fine. First sentence "
            "carries the post. Ask a question to drive comments."
        ),
    },
    "threads": {
        "aspect_ratio": "3:4",
        "max_chars": 500,
        "hashtag_range": "0-1",
        "norms": (
            "Hard 500-character limit. Casual, conversation-starter energy; "
            "hashtags are barely used on Threads, at most one topic tag."
        ),
    },
}

DEFAULT = SPECS["instagram"]


def spec_for(platform: str) -> PlatformSpec:
    return SPECS.get(platform, DEFAULT)


def aspect_for(platform: str) -> str:
    return spec_for(platform)["aspect_ratio"]


def copy_constraints(platform: str) -> str:
    s = spec_for(platform)
    return (
        f"Platform rules for {platform}:\n"
        f"- Caption max length: {s['max_chars']} characters (hard limit).\n"
        f"- Hashtag count: {s['hashtag_range']}.\n"
        f"- Norms: {s['norms']}"
    )
