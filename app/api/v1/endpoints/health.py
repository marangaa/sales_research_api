from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict

from app.models.database import get_db
from app.core.config import settings

router = APIRouter()

@router.get("/", response_model=Dict[str, str])
async def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint to verify API and dependencies are working
    """
    try:
        # Test database connection
        db.execute("SELECT 1")
        
        return {
            "status": "healthy",
            "version": settings.VERSION,
            "database": "connected",
            "message": "Service is running normally"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "version": settings.VERSION,
            "database": "disconnected",
            "message": str(e)
        }