import pytest
from unittest.mock import Mock, patch
from src.scraper import Scraper

@patch('src.scraper.FirecrawlApp')
def test_fetch_page_content_success(MockFirecrawlApp):
    # Setup mock
    mock_app_instance = Mock()
    mock_scrape_result = Mock()
    mock_scrape_result.markdown = '# Test Product\nPrice: $99.99'
    mock_app_instance.scrape.return_value = mock_scrape_result
    MockFirecrawlApp.return_value = mock_app_instance
    
    # Run test
    scraper = Scraper()
    content = scraper.fetch_page_content("https://example.com/product")
    
    # Assertions
    assert content == '# Test Product\nPrice: $99.99'
    mock_app_instance.scrape.assert_called_once_with(
        "https://example.com/product",
        formats=['markdown']
    )

@patch('src.scraper.FirecrawlApp')
def test_fetch_page_content_failure(MockFirecrawlApp):
    # Setup mock
    mock_app_instance = Mock()
    mock_app_instance.scrape.side_effect = Exception("API Error")
    MockFirecrawlApp.return_value = mock_app_instance
    
    # Run test
    scraper = Scraper()
    content = scraper.fetch_page_content("https://example.com/product")
    
    # Assertions
    assert content is None
