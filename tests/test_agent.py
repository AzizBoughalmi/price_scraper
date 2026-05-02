import pytest
from unittest.mock import Mock, patch
from src.agent import Agent
from src.models import PriceResult

@patch('src.agent.SearchTool')
@patch('src.agent.Scraper')
@patch('src.agent.LLMParser')
def test_agent_process_url(MockParser, MockScraper, MockSearcher):
    # Setup mocks
    mock_scraper_inst = Mock()
    mock_parser_inst = Mock()
    mock_searcher_inst = Mock()
    
    MockScraper.return_value = mock_scraper_inst
    MockParser.return_value = mock_parser_inst
    MockSearcher.return_value = mock_searcher_inst
    
    mock_scraper_inst.fetch_page_content.return_value = "Markdown test"
    
    expected_result = PriceResult(
        competitor="Amazon",
        product_name="Product",
        price=10.0,
        currency="USD",
        url="http://test.com",
        status="In Stock"
    )
    mock_parser_inst.extract_price_data.return_value = expected_result
    
    # Run test
    agent = Agent()
    agent.scraper = mock_scraper_inst
    agent.parser = mock_parser_inst
    
    result = agent.process_url("http://test.com", "Product", "Amazon")
    
    # Assertions
    assert result == expected_result
    mock_scraper_inst.fetch_page_content.assert_called_once_with("http://test.com")
    mock_parser_inst.extract_price_data.assert_called_once_with(
        markdown_content="Markdown test",
        product_name="Product",
        competitor="Amazon",
        url="http://test.com"
    )
