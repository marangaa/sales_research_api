from pydantic_settings import BaseSettings
from typing import List, Optional
from functools import lru_cache

class Settings(BaseSettings):
    # Basic API Configuration
    PROJECT_NAME: str = "Sales Research API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "AI-powered sales prospect research automation"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False
    
    # Security
    SECRET_KEY: str
    ALLOWED_ORIGINS: List[str] = ["*"]
    API_KEY_NAME: str = "X-API-Key"
    API_KEY: str
    
    # Database
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: str = "5432"
    DATABASE_URL: Optional[str] = None

    # Redis and Celery
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    CELERY_BROKER_URL: str = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
    CELERY_RESULT_BACKEND: str = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
    
    # External APIs
    FIRECRAWL_API_KEY: str
    GEMINI_API_KEY: str
    PERPLEXITY_API_KEY: str
    
    # Service Configuration
    CRAWLER_TIMEOUT: int = 300  # seconds
    MAX_PAGES_PER_DOMAIN: int = 100
    CACHE_EXPIRATION: int = 86400  # 24 hours
    MAX_RETRIES: int = 3
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 3600  # 1 hour
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Construct DATABASE_URL if not provided
        if not self.DATABASE_URL:
            self.DATABASE_URL = (
                f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
            )

@lru_cache
def get_settings() -> Settings:
    """Cached settings instance"""
    return Settings()

settings = get_settings()