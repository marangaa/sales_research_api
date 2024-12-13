from fastapi import Header, HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session
import time
from typing import Optional

from app.core.config import settings
from app.models.database import get_db
from app.core.exceptions import RateLimitException
from app.models.domain.database_models import APIKeyUsage

api_key_header = APIKeyHeader(name=settings.API_KEY_NAME)

async def verify_api_key(
    api_key: str = Depends(api_key_header),
    db: Session = Depends(get_db)
):
    """Verify API key and check rate limits"""
    if api_key != settings.API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Invalid API key"
        )
    
    # Check rate limits
    usage = db.query(APIKeyUsage).filter(
        APIKeyUsage.api_key == api_key,
        APIKeyUsage.timestamp > time.time() - settings.RATE_LIMIT_PERIOD
    ).count()
    
    if usage >= settings.RATE_LIMIT_REQUESTS:
        raise RateLimitException()
    
    # Record API usage
    db.add(APIKeyUsage(api_key=api_key, timestamp=time.time()))
    db.commit()
    
    return api_key

async def get_optional_api_key(
    api_key: Optional[str] = Header(None, alias=settings.API_KEY_NAME)
) -> Optional[str]:
    """Get API key if provided, for differentiated rate limiting"""
    return api_key