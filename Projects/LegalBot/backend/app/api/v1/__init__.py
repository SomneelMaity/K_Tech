"""
API Router - v1
"""
from fastapi import APIRouter
from app.api.v1.endpoints import query, documents, segments, health

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(query.router, prefix="/query", tags=["Query"])
api_router.include_router(documents.router, prefix="/documents", tags=["Documents"])
api_router.include_router(segments.router, prefix="/segments", tags=["Segments"])
