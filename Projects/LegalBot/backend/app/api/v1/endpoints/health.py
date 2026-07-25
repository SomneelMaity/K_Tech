"""
Health check endpoints
"""
from fastapi import APIRouter
from datetime import datetime

from app.models.schemas import HealthResponse
from app.core.rag_engine import rag_engine

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Basic health check"""
    return HealthResponse(
        status="healthy",
        rag_engine="initialized" if rag_engine.initialized else "not initialized",
        segments_loaded=len(rag_engine.loaded_segments) if hasattr(rag_engine, 'loaded_segments') else 0
    )


@router.get("/ping")
async def ping():
    """Simple ping endpoint"""
    return {"ping": "pong", "timestamp": datetime.utcnow().isoformat()}
