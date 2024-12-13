from fastapi import HTTPException, status
from typing import Optional, Dict, Any

class BaseAPIException(HTTPException):
    """Base exception for API errors"""
    def __init__(
        self,
        status_code: int,
        detail: str,
        headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)

class CrawlerException(BaseAPIException):
    """Raised when website crawling fails"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Crawler error: {detail}"
        )

class AnalysisException(BaseAPIException):
    """Raised when content analysis fails"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis error: {detail}"
        )

class EnrichmentException(BaseAPIException):
    """Raised when data enrichment fails"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Enrichment error: {detail}"
        )

class CacheException(BaseAPIException):
    """Raised when cache operations fail"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Cache error: {detail}"
        )

class RateLimitException(BaseAPIException):
    """Raised when rate limit is exceeded"""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later."
        )