from pydantic import BaseModel, validator, HttpUrl
from typing import List, Optional
from enum import Enum

from app.core.validation import CompanyDataValidator


class ResearchDepthValidator(str, Enum):
    BASIC = "basic"
    DEEP = "deep"

class OutputFormatValidator(str, Enum):
    JSON = "json"
    MARKDOWN = "markdown"

class ResearchRequestValidator(BaseModel):
    company_url: HttpUrl
    depth: ResearchDepthValidator
    focus_areas: Optional[List[str]] = []
    output_format: OutputFormatValidator = OutputFormatValidator.JSON

    @validator('focus_areas')
    def validate_focus_areas(cls, v):
        allowed_areas = {
            'tech_stack', 'decision_makers', 'market_position',
            'products', 'competitors', 'funding'
        }
        if not all(area in allowed_areas for area in v):
            raise ValueError(f"Invalid focus areas. Allowed values: {allowed_areas}")
        return v

    @validator('company_url')
    def validate_company_url(cls, v):
        validator = CompanyDataValidator()
        cleaned_url = validator.validate_company_url(str(v))
        if not cleaned_url:
            raise ValueError("Invalid company URL")
        return cleaned_url

class ValidationError(Exception):
    """Custom validation error"""
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")