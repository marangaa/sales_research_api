from typing import List, Optional, TypedDict

class ExecutiveInfo(TypedDict):
    name: str
    title: str
    linkedin_url: Optional[str]

class CompanyIntel(TypedDict):
    company_name: str
    industry: str
    company_size: Optional[str]
    company_stage: Optional[str]
    headquarters: Optional[str]
    founded_year: Optional[int]
    
    # Products and Services
    key_products: List[str]
    value_propositions: List[str]
    target_markets: List[str]
    
    # People and Organization
    key_executives: List[ExecutiveInfo]
    
    # Technical Information
    technologies_used: List[str]
    
    # Business Intelligence
    competitive_advantages: List[str]
    pain_points: List[str]
    recent_developments: List[str]
    
    # Market Position
    competitors: List[str]
    market_position: Optional[str]
    
    # Additional Context
    funding_status: Optional[str]
    recent_news: List[str]
    
    # Analysis Metadata
    confidence_score: float
    last_updated: str
    data_sources: List[str]