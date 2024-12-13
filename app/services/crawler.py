from typing import Dict, List, Optional
from firecrawl import FirecrawlApp
from fastapi import HTTPException
from pydantic import HttpUrl

from app.core.config import settings
from app.core.logging import logger

class CrawlerService:
    def __init__(self):
        # Initialize FireCrawl with API key from settings
        self.client = FirecrawlApp(api_key=settings.FIRECRAWL_API_KEY)
        
        # Define important pages to prioritize during crawling
        self.priority_paths = [
            "/about", "/about-us", 
            "/company", 
            "/products", "/solutions",
            "/leadership", "/team",
            "/contact", "/news", "/blog"
        ]

    async def crawl_website(self, url: HttpUrl) -> Dict[str, str]:
        """
        Crawl website strategically focusing on important pages first.
        Returns a dictionary of page URLs and their content.
        """
        try:
            # First, crawl priority pages
            priority_results = {}
            for path in self.priority_paths:
                try:
                    target_url = f"{url.rstrip('/')}{path}"
                    result = await self.client.scrape_url(
                        target_url,
                        params={
                            'formats': ['markdown', 'html'],
                            'timeout': settings.CRAWLER_TIMEOUT
                        }
                    )
                    if result.get('status') == 'success':
                        priority_results[target_url] = result['content']
                except Exception as e:
                    logger.warning(f"Failed to crawl priority path {path}: {str(e)}")

            # Then do a general crawl for remaining pages
            crawl_result = await self.client.crawl_url(
                str(url),
                params={
                    'limit': settings.MAX_PAGES_PER_DOMAIN,
                    'scrapeOptions': {
                        'formats': ['markdown', 'html']
                    },
                    'exclude': list(priority_results.keys())  # Avoid re-crawling
                }
            )

            # Combine priority and general results
            all_results = {**priority_results, **crawl_result.get('pages', {})}

            if not all_results:
                raise HTTPException(
                    status_code=404,
                    detail="No content found on the specified website"
                )

            return all_results

        except Exception as e:
            logger.error(f"Crawling failed for {url}: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to crawl website: {str(e)}"
            )

    async def extract_metadata(self, html_content: str) -> Dict[str, str]:
        """Extract key metadata from HTML content"""
        # Implementation for metadata extraction
        pass