import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    # API keys
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN", "")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

    # Models
    COPY_MODEL = os.getenv("COPY_MODEL", "claude-opus-4-8")
    STRATEGY_MODEL = os.getenv("STRATEGY_MODEL", "claude-haiku-4-5-20251001")
    # Voice assistant: fast + cheap tool-use model keeps spoken replies snappy.
    ASSISTANT_MODEL = os.getenv("ASSISTANT_MODEL", "claude-haiku-4-5-20251001")
    IMAGE_MODEL = os.getenv("IMAGE_MODEL", "black-forest-labs/flux-schnell")
    GEMINI_IMAGE_MODEL = os.getenv("GEMINI_IMAGE_MODEL", "gemini-2.5-flash-image")
    # Image backend: "auto" (gemini > replicate > placeholder) or force one.
    IMAGE_PROVIDER = os.getenv("IMAGE_PROVIDER", "auto")

    # Image generation resilience
    IMAGE_TIMEOUT = int(os.getenv("IMAGE_TIMEOUT", "180"))  # seconds per attempt
    IMAGE_RETRIES = int(os.getenv("IMAGE_RETRIES", "2"))  # retries after first attempt

    # Infra
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ugc.db")
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "storage")
    PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL", "").rstrip("/")
    CORS_ORIGINS = [
        o.strip()
        for o in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
        if o.strip()
    ]

    # Social publishing / paid campaign automation.
    # X requires an OAuth2 user access token with tweet.write/media.write scopes.
    X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN", "")
    X_API_BASE = os.getenv("X_API_BASE", "https://api.x.com/2").rstrip("/")

    # Instagram and Meta Ads use the Graph API.
    META_GRAPH_VERSION = os.getenv("META_GRAPH_VERSION", "v25.0")
    META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN", "")
    META_IG_USER_ID = os.getenv("META_IG_USER_ID", "")
    META_AD_ACCOUNT_ID = os.getenv("META_AD_ACCOUNT_ID", "")
    META_PAGE_ID = os.getenv("META_PAGE_ID", "")

    @property
    def has_anthropic(self) -> bool:
        return bool(self.ANTHROPIC_API_KEY)

    @property
    def has_replicate(self) -> bool:
        return bool(self.REPLICATE_API_TOKEN)

    @property
    def has_gemini(self) -> bool:
        return bool(self.GEMINI_API_KEY)

    @property
    def has_x(self) -> bool:
        return bool(self.X_ACCESS_TOKEN)

    @property
    def has_instagram(self) -> bool:
        return bool(self.META_ACCESS_TOKEN and self.META_IG_USER_ID)

    @property
    def has_meta_ads(self) -> bool:
        return bool(self.META_ACCESS_TOKEN and self.META_AD_ACCOUNT_ID)


settings = Settings()
