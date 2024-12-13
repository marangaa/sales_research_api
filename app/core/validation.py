from typing import Any, Dict, Optional
from pydantic import BaseModel, ValidationError, HttpUrl
from urllib.parse import urlparse
import re
import html


class DataValidator:
    """Base validator class with common validation methods"""

    @staticmethod
    def sanitize_html(text: str) -> str:
        """Remove HTML tags and escape special characters"""
        # First remove HTML tags
        clean_text = re.sub(r'<[^>]+>', '', text)
        # Then escape special characters
        return html.escape(clean_text)

    @staticmethod
    def validate_url(url: str) -> Optional[str]:
        """Validate and normalize URL"""
        try:
            parsed = urlparse(url)
            if all([parsed.scheme, parsed.netloc]):
                return url.lower()
        except Exception:
            return None
        return None

    @staticmethod
    def clean_string(text: str) -> str:
        """Clean and normalize string input"""
        # Remove control characters and extra whitespace
        clean = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text)
        clean = re.sub(r'\s+', ' ', clean).strip()
        return clean


class CompanyDataValidator(DataValidator):
    """Validator for company-related data"""

    def __init__(self):
        self.website_pattern = re.compile(
            r'^https?://(?:www\.)?'
            r'[a-zA-Z0-9-]+(?:\.[a-zA-Z]{2,})+/?'
        )

        self.email_pattern = re.compile(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        )

    def validate_company_url(self, url: str) -> Optional[str]:
        """Validate company website URL"""
        if not self.website_pattern.match(url):
            return None
        return self.validate_url(url)

    def validate_company_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and clean company data"""
        cleaned_data = {}

        # Clean and validate each field
        for key, value in data.items():
            if isinstance(value, str):
                cleaned_value = self.clean_string(value)
                if key == 'website':
                    cleaned_value = self.validate_company_url(cleaned_value)
                elif key == 'email':
                    if not self.email_pattern.match(cleaned_value):
                        cleaned_value = None
                cleaned_data[key] = cleaned_value
            elif isinstance(value, list):
                cleaned_data[key] = [
                    self.clean_string(item) if isinstance(item, str) else item
                    for item in value
                ]
            else:
                cleaned_data[key] = value

        return cleaned_data


class ContentValidator(DataValidator):
    """Validator for crawled content"""

    def __init__(self):
        self.max_content_length = 1000000  # 1MB
        self.allowed_tags = {
            'p', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'ul', 'ol', 'li', 'a', 'strong', 'em', 'b', 'i'
        }

    def validate_content(self, content: str) -> Optional[str]:
        """Validate and clean crawled content"""
        if len(content) > self.max_content_length:
            return None

        # Remove potentially dangerous tags while keeping safe ones
        cleaned = re.sub(
            r'<([^>]+)>',
            lambda m: m.group(0) if m.group(1).split()[0] in self.allowed_tags else '',
            content
        )

        return self.clean_string(cleaned)