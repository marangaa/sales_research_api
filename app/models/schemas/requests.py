# app/models/schemas/requests.py
from pydantic import BaseModel, HttpUrl, Field, validator
from typing import List, Optional
from enum import Enum

class ResearchDepth(str, Enum):
    BASIC = "basic"
    DEEP = "deep"

class OutputFormat(str, Enum):
    JSON = "json"
    MARKDOWN = "markdown"

class FocusArea(str, Enum):
    TECH_STACK = "tech_stack"
    DECISION_MAKERS = "decision_makers"
    MARKET_POSITION = "market_position"
    PRODUCTS = "products"
    COMPETITORS = "competitors"
    FUNDING = "funding"

class ResearchRequest(BaseModel):
    company_url: HttpUrl
    depth: ResearchDepth = Field(
        default=ResearchDepth.BASIC,
        description="Depth of research to perform"
    )
    focus_areas: Optional[List[FocusArea]] = Field(
        default=[],
        description="Specific areas to focus research on"
    )
    output_format: OutputFormat = Field(
        default=OutputFormat.JSON,
        description="Desired format of the output"
    )
    force_refresh: bool = Field(
        default=False,
        description="Force new research even if cached data exists"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "company_url": "https://example.com",
                "depth": "deep",
                "focus_areas": ["tech_stack", "decision_makers"],
                "output_format": "json",
                "force_refresh": False
            }
        }