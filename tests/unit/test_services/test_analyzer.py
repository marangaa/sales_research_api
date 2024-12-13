import pytest
from unittest.mock import patch, MagicMock
from app.services.analyzer import AnalyzerService
from app.core.exceptions import AnalysisException


@pytest.mark.asyncio
async def test_analyze_content_success():
    analyzer = AnalyzerService()
    test_data = {"url": "content"}

    mock_response = {
        "company_name": "Test Corp",
        "industry": "Technology"
    }

    with patch("google.generativeai.GenerativeModel.generate_content") as mock_generate:
        mock_generate.return_value = MagicMock(json=lambda: mock_response)
        result = await analyzer.analyze_content(test_data)

        assert result is not None
        assert result["company_name"] == "Test Corp"
        assert result["industry"] == "Technology"