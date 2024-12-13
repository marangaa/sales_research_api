from fastapi import APIRouter
from app.api.v1.endpoints import research, health

# Create API router
api_router = APIRouter()

# Include routes from endpoints
api_router.include_router(
    research.router,
    prefix="/research",
    tags=["research"]
)

api_router.include_router(
    health.router,
    prefix="/health",
    tags=["health"]
)