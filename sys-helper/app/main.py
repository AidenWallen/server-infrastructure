from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api import chat, server
from app.core.database import connect_to_mongo, close_mongo_connection
from app.core.security import APIKeyAuthMiddleware
from app.exceptions.handlers import global_exception_handler

# Database lifecycle events - Updated to use lifespan event handlers
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event
    await connect_to_mongo()
    yield
    # Shutdown event
    await close_mongo_connection()

app = FastAPI(
    title="SysHelper",
    description="AI assistant for server management and operations",
    version="0.1.0",
    lifespan=lifespan
)

# Add Security Middleware
app.add_middleware(APIKeyAuthMiddleware)

# Add Global Exception Handler
app.add_exception_handler(Exception, global_exception_handler)

app.include_router(chat.router)
app.include_router(server.router)


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "sys-helper"}

