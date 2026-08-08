import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import settings
from .database import Base, engine, migrate
from .routers import assistant, generations

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
Base.metadata.create_all(bind=engine)
migrate()

app = FastAPI(title="Faceless UGC Factory API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/storage", StaticFiles(directory=settings.UPLOAD_DIR), name="storage")
app.include_router(generations.router)
app.include_router(assistant.router)


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "anthropic_configured": settings.has_anthropic,
        "replicate_configured": settings.has_replicate,
        "copy_model": settings.COPY_MODEL,
        "image_model": settings.IMAGE_MODEL,
    }
