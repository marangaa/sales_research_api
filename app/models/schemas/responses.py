# app/models/schemas/responses.py
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum

class JobStatus(str, Enum):
    PENDING = "pending"
    CRAWLING = "crawling"
    ANALYZING = "analyzing"
    ENRICHING = "enriching"
    SYNTHESIZING = "synthesizing"
    COMPLETED = "completed"
    FAILED = "failed"

class ResearchJobStatus(BaseModel):
    job_id: str
    status: JobStatus
    progress: float = 0.0
    message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    error: Optional[str] = None

class CompanyResearchResponse(BaseModel):
    company_intel: Dict
    metadata: Dict[str, any] = {
        "source": "sales_research_api",
        "generated_at": datetime.now(),
        "confidence_score": 0.0,
        "data_freshness": "real-time"
    }