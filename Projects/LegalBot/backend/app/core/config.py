"""
Application Configuration
"""
from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    # API Configuration
    API_TITLE: str = "LegalBot API"
    API_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/legalbot"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # LLM Configuration
    LLM_PROVIDER: str = "openai"
    LLM_API_KEY: str = ""
    LLM_API_BASE: str = "https://api.openai.com/v1"
    LLM_MODEL: str = "gpt-4-turbo-preview"
    LLM_TEMPERATURE: float = 0.3
    LLM_MAX_TOKENS: int = 2048
    
    # Embeddings
    EMBEDDING_MODEL: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    EMBEDDING_DIMENSION: int = 768
    
    # Vector Database
    VECTOR_DB_TYPE: str = "faiss"
    VECTOR_DB_PATH: str = "./vector_store"
    FAISS_INDEX_TYPE: str = "IVFFlat"
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    
    # RAG Configuration
    RAG_TOP_K: int = 5
    RAG_SIMILARITY_THRESHOLD: float = 0.7
    RAG_RERANK: bool = True
    RAG_HYBRID_SEARCH: bool = True
    
    # Language & Translation
    BHASHINI_API_KEY: str = ""
    BHASHINI_API_URL: str = "https://dhruva-api.bhashini.gov.in/services"
    DEFAULT_LANGUAGE: str = "en"
    SUPPORTED_LANGUAGES: str = "en,hi,bn,te,mr,ta,gu,kn,ml,or,pa"
    
    # Speech
    SPEECH_PROVIDER: str = "bhashini"
    WHISPER_MODEL: str = "base"
    TTS_PROVIDER: str = "bhashini"
    
    # Document Generation
    DOC_GEN_FORMAT: str = "pdf,docx"
    TEMPLATE_DIR: str = "./app/templates"
    OUTPUT_DIR: str = "./generated_docs"
    MAX_DOC_SIZE_MB: int = 5
    
    # Safety & Moderation
    ENABLE_SAFETY_MIDDLEWARE: bool = True
    EMERGENCY_DETECTION: bool = True
    CONTENT_MODERATION: bool = True
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 20
    RATE_LIMIT_PER_HOUR: int = 200
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    CORS_ALLOW_CREDENTIALS: bool = True
    
    # Monitoring
    SENTRY_DSN: str = ""
    PROMETHEUS_ENABLED: bool = False
    
    # WhatsApp
    WHATSAPP_API_URL: str = ""
    WHATSAPP_API_TOKEN: str = ""
    WHATSAPP_PHONE_NUMBER_ID: str = ""
    WHATSAPP_VERIFY_TOKEN: str = ""
    
    # Analytics
    ENABLE_ANALYTICS: bool = True
    ANALYTICS_DB: str = "legalbot_analytics"
    
    # File Upload
    MAX_UPLOAD_SIZE_MB: int = 10
    ALLOWED_FILE_TYPES: str = "pdf,jpg,jpeg,png,docx"
    
    # Session
    SESSION_TIMEOUT_MINUTES: int = 60
    SESSION_CLEANUP_HOURS: int = 24
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    @property
    def supported_languages_list(self) -> List[str]:
        return [lang.strip() for lang in self.SUPPORTED_LANGUAGES.split(",")]
    
    @property
    def allowed_file_types_list(self) -> List[str]:
        return [ft.strip() for ft in self.ALLOWED_FILE_TYPES.split(",")]
    
    @property
    def doc_gen_formats_list(self) -> List[str]:
        return [fmt.strip() for fmt in self.DOC_GEN_FORMAT.split(",")]


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
