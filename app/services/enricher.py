from openai import OpenAI
from typing import Dict, List
import json

from app.core.config import settings
from app.models.domain.company import CompanyIntel

class EnricherService:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.PERPLEXITY_API_KEY,
            base_url="https://api.perplexity.ai"
        )

    async def enrich_company_data(self, company_data: CompanyIntel) -> CompanyIntel:
        """
        Enrich company data with additional information from the web.
        """
        try:
            # Create targeted queries based on company data
            queries = self._generate_enrichment_queries(company_data)
            
            enriched_data = company_data.copy()
            
            for query in queries:
                response = await self._query_perplexity(query)
                enriched_data = self._update_company_data(enriched_data, response)
            
            return enriched_data

        except Exception as e:
            logger.error(f"Enrichment failed: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Data enrichment failed: {str(e)}"
            )

    def _generate_enrichment_queries(self, company_data: CompanyIntel) -> List[str]:
        """
        Generate specific queries for additional research.
        """
        return [
            f"What are the latest news and developments about {company_data['company_name']}?",
            f"What is {company_data['company_name']}'s market position and main competitors?",
            f"What are {company_data['company_name']}'s recent funding rounds or financial updates?",
            f"What are common customer reviews and feedback about {company_data['company_name']}?"
        ]

    async def _query_perplexity(self, query: str) -> Dict:
        """
        Query Perplexity API with structured output.
        """
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a business research assistant. Provide factual, "
                    "up-to-date information about companies with source citations."
                )
            },
            {
                "role": "user",
                "content": query
            }
        ]

        response = await self.client.chat.completions.create(
            model="llama-3.1-sonar-large-128k-online",
            messages=messages,
        )
        
        return response.choices[0].message.content

    def _update_company_data(
        self, 
        company_data: CompanyIntel, 
        enrichment_response: str
    ) -> CompanyIntel:
        """
        Update company data with enriched information.
        """
        # Implementation for updating company data
        pass