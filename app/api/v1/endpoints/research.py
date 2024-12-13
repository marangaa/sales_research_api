from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime

from app.models.schemas.requests import ResearchRequest
from app.models.schemas.responses import ResearchJobStatus, CompanyResearchResponse
from app.models.database import get_db
from app.models.domain.database_models import ResearchJob
from app.worker import process_research

router = APIRouter()

@router.post("/research", response_model=dict)
async def initiate_research(
    request: ResearchRequest,
    db: Session = Depends(get_db)
):
    """
    Initiate a new company research job
    """
    # Create job ID
    job_id = str(uuid4())
    
    # Create job record
    job = ResearchJob(
        id=job_id,
        company_url=str(request.company_url),
        status="pending",
        progress=0.0,
        created_at=datetime.utcnow()
    )
    db.add(job)
    db.commit()
    
    # Start background task
    process_research.delay(
        job_id,
        str(request.company_url),
        request.depth.value,
        [area.value for area in request.focus_areas],
        request.output_format.value
    )
    
    return {"job_id": job_id}

@router.get("/research/{job_id}", response_model=ResearchJobStatus)
async def get_research_status(
    job_id: str,
    db: Session = Depends(get_db)
):
    """
    Get status of a research job
    """
    job = db.query(ResearchJob).filter(ResearchJob.id == job_id).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    return ResearchJobStatus(
        job_id=job.id,
        status=job.status,
        progress=job.progress,
        created_at=job.created_at,
        updated_at=job.updated_at,
        error=job.error
    )

@router.get("/research/{job_id}/result", response_model=CompanyResearchResponse)
async def get_research_result(
    job_id: str,
    db: Session = Depends(get_db)
):
    """
    Get the result of a completed research job
    """
    job = db.query(ResearchJob).filter(ResearchJob.id == job_id).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    if job.status == "failed":
        raise HTTPException(
            status_code=500,
            detail=f"Job failed: {job.error}"
        )
        
    if job.status != "completed":
        raise HTTPException(
            status_code=202,
            detail="Job still processing"
        )
        
    return CompanyResearchResponse(
        company_intel=job.result,
        metadata={
            "source": "sales_research_api",
            "generated_at": job.updated_at,
            "confidence_score": job.result.get("confidence_score", 0.0),
            "data_freshness": "cached" if job.cache_used else "real-time"
        }
    )