from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings

class APIKeyAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Allow health checks or specific public routes
        if request.url.path in ["/", "/health", "/docs", "/openapi.json"]:
            return await call_next(request)

        api_key = request.headers.get("X-API-KEY")
        if not api_key or api_key != settings.API_KEY:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or missing API key"
            )
        
        return await call_next(request)

