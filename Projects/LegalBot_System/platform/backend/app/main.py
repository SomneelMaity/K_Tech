import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import settings
from .database import Base, engine, migrate
from .routers import chat, documents
from .middleware.safety import SafetyMiddleware

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
Base.metadata.create_all(bind=engine)
migrate()

app = FastAPI(
    title="LegalBot System API",
    description="AI-Powered Legal Assistant for Every Indian — RAG-grounded, multilingual.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SafetyMiddleware)

app.mount("/storage", StaticFiles(directory=settings.UPLOAD_DIR), name="storage")
app.include_router(chat.router)
app.include_router(documents.router)


@app.get("/api/health", response_model=None)
def health():
    return {
        "status": "ok",
        "llm_provider": settings.LLM_PROVIDER,
        "llm_configured": settings.has_llm,
        "chat_model": settings.CHAT_MODEL,
        "vector_store": settings.VECTOR_STORE,
        "bhashini_configured": settings.has_bhashini,
    }
