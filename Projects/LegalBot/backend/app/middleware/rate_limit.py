"""
Rate limiting middleware
"""
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from loguru import logger
import time
from collections import defaultdict

from app.core.config import settings


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Simple in-memory rate limiter
    In production, use Redis for distributed rate limiting
    """
    
    def __init__(self, app):
        super().__init__(app)
        self.requests = defaultdict(list)  # ip -> [timestamps]
    
    async def dispatch(self, request: Request, call_next):
        if not settings.RATE_LIMIT_ENABLED:
            return await call_next(request)
        
        # Get client IP
        client_ip = request.client.host
        
        # Clean old entries
        current_time = time.time()
        self.requests[client_ip] = [
            ts for ts in self.requests[client_ip]
            if current_time - ts < 60  # Keep last minute
        ]
        
        # Check rate limit
        if len(self.requests[client_ip]) >= settings.RATE_LIMIT_PER_MINUTE:
            logger.warning(f"Rate limit exceeded for {client_ip}")
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": "Too many requests. Please try again later."
                }
            )
        
        # Add current request
        self.requests[client_ip].append(current_time)
        
        return await call_next(request)
