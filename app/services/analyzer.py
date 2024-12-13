import google.generativeai as genai
import typing
from typing import List, Dict, Optional

from fastapi import HTTPException

from app.core.config import settings
from app.core.logging import logger
from app.models.domain.company import CompanyIntel

class AnalyzerService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-1.5-pro-latest")

    async def analyze_content(self, crawled_data: Dict[str, str]) -> CompanyIntel:
        """
        Analyze crawled website content using Gemini to extract structured information.
        """
        # Prepare prompt with our schema
        prompt = self._build_analysis_prompt(crawled_data)
        
        try:
            result = await self.model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json",
                    response_schema=CompanyIntel
                )
            )
            
            return result.json()

        except Exception as e:
            logger.error(f"Gemini analysis failed: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Content analysis failed: {str(e)}"
            )

    def _build_analysis_prompt(self, crawled_data: Dict[str, str]) -> str:
        """
        Build a detailed prompt for Gemini to analyze website content.
        """
        return f"""
        Analyze the following website content and extract key business information according to this schema:

        {CompanyIntel.schema_json()}

        Focus on identifying:
        1. Core business model and value proposition
        2. Key products/services and their benefits
        3. Target market and customer segments
        4. Competitive advantages and market positioning
        5. Company size and growth indicators
        6. Technology stack and infrastructure
        7. Leadership team and decision makers
        8. Recent developments and news

        Website content:
        {self._format_content_for_analysis(crawled_data)}

        Return only valid JSON matching the specified schema.
        """

    def _format_content_for_analysis(self, crawled_data: Dict[str, str]) -> str:
        """
        Format crawled content for optimal analysis.
        """
        # Combine and clean content from different pages
        formatted_content = []
        
        for url, content in crawled_data.items():
            page_type = self._determine_page_type(url)
            formatted_content.append(f"\n--- {page_type} Content from {url} ---\n{content}")
            
        return "\n".join(formatted_content)

    def _determine_page_type(self, url: str) -> str:
        """
        Determine the type of page based on URL patterns.
        """
        url_lower = url.lower()
        if "about" in url_lower:
            return "Company Information"
        elif "product" in url_lower or "solution" in url_lower:
            return "Products/Services"
        elif "team" in url_lower or "leadership" in url_lower:
            return "Leadership"
        elif "news" in url_lower or "blog" in url_lower:
            return "News/Updates"
        return "General"