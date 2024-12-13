from sqlalchemy import Column, String, JSON, DateTime, Float, Integer
from sqlalchemy.sql import func
from app.models.database import Base

class ResearchJob(Base):
    __tablename__ = "research_jobs"

    id = Column(String, primary_key=True)
    company_url = Column(String, index=True)
    status = Column(String)
    progress = Column(Float)
    result = Column(JSON, nullable=True)
    error = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Cache control
    cache_valid_until = Column(DateTime(timezone=True))
    version = Column(Integer, default=1)

class ResearchCache(Base):
    __tablename__ = "research_cache"

    company_url = Column(String, primary_key=True)
    crawl_data = Column(JSON)
    analyzed_data = Column(JSON)
    enriched_data = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    cache_valid_until = Column(DateTime(timezone=True))