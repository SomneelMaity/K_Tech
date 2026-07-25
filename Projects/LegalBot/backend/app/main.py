"""
LegalBot FastAPI Main Application
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
import time

from app.core.config import settings
from app.core.rag_engine import rag_engine
from app.api.v1 import api_router
from app.middleware.safety import SafetyMiddleware
from app.middleware.rate_limit import RateLimitMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup
    logger.info("Starting LegalBot API...")
    
    # Initialize RAG engine
    logger.info("Initializing RAG engine...")
    await rag_engine.initialize()
    
    # Load vector stores for all segments
    logger.info("Loading knowledge base...")
    await rag_engine.load_all_segments()
    
    logger.info("LegalBot API started successfully!")
    
    yield
    
    # Shutdown
    logger.info("Shutting down LegalBot API...")
    await rag_engine.cleanup()
    logger.info("LegalBot API shutdown complete.")


# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    description="AI-Powered Legal Assistant for India - Breaking the justice gap",
    version=settings.API_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Add custom middleware
if settings.ENABLE_SAFETY_MIDDLEWARE:
    app.add_middleware(SafetyMiddleware)

if settings.RATE_LIMIT_ENABLED:
    app.add_middleware(RateLimitMiddleware)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred. Please try again later."
        }
    )


# Include API router
app.include_router(api_router, prefix=settings.API_PREFIX)


# Root endpoint
@app.get("/")
async def root():
    return {
        "name": "LegalBot API",
        "version": settings.API_VERSION,
        "status": "running",
        "docs": "/docs",
        "description": "AI-Powered Legal Assistant for India"
    }


# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "rag_engine": "initialized" if rag_engine.initialized else "not initialized",
        "segments_loaded": len(rag_engine.loaded_segments) if hasattr(rag_engine, 'loaded_segments') else 0
    }


# Ready check (for k8s)
@app.get("/ready")
async def ready_check():
    if not rag_engine.initialized:
        return JSONResponse(
            status_code=503,
            content={"status": "not ready", "reason": "RAG engine not initialized"}
        )
    
    return {"status": "ready"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
