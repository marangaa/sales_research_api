import pytest
from unittest.mock import patch, MagicMock
from app.services.crawler import CrawlerService
from app.core.exceptions import CrawlerException


@pytest.mark.asyncio
async def test_crawl_website_success():
    crawler = CrawlerService()
    test_url = "https://example.com"

    mock_response = {
        "status": "success",
        "content": {"text": "Test content"}
    }

    with patch("firecrawl.FirecrawlApp.scrape_url") as mock_scrape:
        mock_scrape.return_value = mock_response
        result = await crawler.crawl_website(test_url)

        assert result is not None
        assert "content" in result
        assert result["content"]["text"] == "Test content"


@pytest.mark.asyncio
async def test_crawl_website_failure():
    crawler = CrawlerService()
    test_url = "https://example.com"

    with patch("firecrawl.FirecrawlApp.scrape_url") as mock_scrape:
        mock_scrape.side_effect = Exception("Crawling failed")

        with pytest.raises(CrawlerException):
            await crawler.crawl_website(test_url)