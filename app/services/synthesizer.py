from typing import Dict, Optional
import google.generativeai as genai

from app.core.config import settings
from app.models.domain.company import CompanyIntel

class SynthesizerService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-1.5-pro-latest")

    async def generate_sales_brief(
        self, 
        company_data: CompanyIntel,
        output_format: str = "json"
    ) -> Dict:
        """
        Generate a sales-focused brief from analyzed and enriched company data.
        """
        try:
            prompt = self._build_synthesis_prompt(company_data, output_format)
            
            result = await self.model.generate_content(prompt)
            
            if output_format == "json":
                return result.json()
            return {"content": result.text}

        except Exception as e:
            logger.error(f"Brief generation failed: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate sales brief: {str(e)}"
            )

    def _build_synthesis_prompt(
        self, 
        company_data: CompanyIntel,
        output_format: str
    ) -> str:
        """
        Build prompt for generating sales-focused brief.
        """
        return f"""
        Create a comprehensive sales brief based on the following company information:
        {json.dumps(company_data, indent=2)}

        The brief should:
        1. Start with an executive summary
        2. Highlight key sales opportunities and pain points
        3. Identify decision makers and their potential interests
        4. Suggest targeted value propositions
        5. Include relevant competitive intelligence
        6. Provide conversation starters and engagement strategies

        Additional requirements:
        - Be concise but comprehensive
        - Focus on actionable insights
        - Include specific examples where possible
        - Highlight any time-sensitive opportunities

        Return the brief in {output_format} format.
        """