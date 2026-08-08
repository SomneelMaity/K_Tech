import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    LLM_PROVIDER: str = "gemini"
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    # Models
    CHAT_MODEL: str = os.getenv("CHAT_MODEL", "gemini-flash-latest")

    # RAG / Vector DB
    VECTOR_STORE: str = os.getenv("VECTOR_STORE", "chroma")
    CHROMA_PERSIST_DIR: str = os.getenv("CHROMA_PERSIST_DIR", "storage/chroma")
    KB_DIR: str = os.getenv("KB_DIR", "../../knowledge-base")

    # Language
    BHASHINI_API_KEY: str = os.getenv("BHASHINI_API_KEY", "")
    DEFAULT_LANGUAGE: str = os.getenv("DEFAULT_LANGUAGE", "en")

    # Infra
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./legalbot.db")
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "storage")
    CORS_ORIGINS: list[str] = [
        o.strip()
        for o in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
        if o.strip()
    ]

    # Document generation
    TEMPLATES_DIR: str = os.getenv("TEMPLATES_DIR", "app/templates")
    OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "storage/docs")

    @property
    def has_llm(self) -> bool:
        return bool(self.GEMINI_API_KEY)

    @property
    def has_bhashini(self) -> bool:
        return bool(self.BHASHINI_API_KEY)


settings = Settings()
