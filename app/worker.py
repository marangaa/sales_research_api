from celery import Celery
from celery.result import AsyncResult
from typing import Dict, Optional
from datetime import datetime, timedelta

from app.core.config import settings
from app.services.crawler import CrawlerService
from app.services.analyzer import AnalyzerService
from app.services.enricher import EnricherService
from app.services.synthesizer import SynthesizerService
from app.models.database import SessionLocal
from app.models.domain.database_models import ResearchJob, ResearchCache

celery = Celery(
    "sales_research",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

@celery.task(bind=True)
def process_research(
    self,
    job_id: str,
    company_url: str,
    depth: str,
    focus_areas: List[str],
    output_format: str
) -> Dict:
    """
    Process the research job in the background
    """
    try:
        # Initialize services
        crawler = CrawlerService()
        analyzer = AnalyzerService()
        enricher = EnricherService()
        synthesizer = SynthesizerService()
        
        # Get database session
        db = SessionLocal()
        
        # Update job status
        job = db.query(ResearchJob).filter(ResearchJob.id == job_id).first()
        
        # Check cache first
        cached_data = _check_cache(db, company_url)
        if cached_data and not force_refresh:
            return _generate_from_cache(cached_data, output_format)

        # Step 1: Crawl website
        job.status = "crawling"
        job.progress = 0.25
        db.commit()
        
        crawled_data = crawler.crawl_website(company_url)
        
        # Step 2: Analyze content
        job.status = "analyzing"
        job.progress = 0.50
        db.commit()
        
        analyzed_data = analyzer.analyze_content(crawled_data)
        
        # Step 3: Enrich data
        job.status = "enriching"
        job.progress = 0.75
        db.commit()
        
        enriched_data = enricher.enrich_company_data(analyzed_data)
        
        # Step 4: Generate final brief
        job.status = "synthesizing"
        job.progress = 0.90
        db.commit()
        
        final_brief = synthesizer.generate_sales_brief(
            enriched_data,
            output_format
        )
        
        # Update cache
        _update_cache(db, company_url, {
            "crawl_data": crawled_data,
            "analyzed_data": analyzed_data,
            "enriched_data": enriched_data
        })
        
        # Complete job
        job.status = "completed"
        job.progress = 1.0
        job.result = final_brief
        db.commit()
        
        return final_brief

    except Exception as e:
        job.status = "failed"
        job.error = str(e)
        db.commit()
        raise

def _check_cache(db, company_url: str) -> Optional[Dict]:
    """Check if valid cached data exists"""
    cache = db.query(ResearchCache).filter(
        ResearchCache.company_url == company_url,
        ResearchCache.cache_valid_until > datetime.utcnow()
    ).first()
    return cache

def _update_cache(db, company_url: str, data: Dict):
    """Update cache with new data"""
    cache = ResearchCache(
        company_url=company_url,
        **data,
        cache_valid_until=datetime.utcnow() + timedelta(days=1)
    )
    db.add(cache)
    db.commit()