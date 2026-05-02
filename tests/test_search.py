import pytest
from unittest.mock import Mock, patch
from src.search import SearchTool

@patch('src.search.TavilyClient')
def test_find_product_urls_success(MockTavilyClient):
    # Setup mock
    mock_client_instance = Mock()
    mock_client_instance.search.return_value = {
        "results": [
            {"url": "https://www.amazon.com/Sony-WH-1000XM5/dp/...", "title": "Sony WH-1000XM5 - Amazon.com"},
            {"url": "https://www.bestbuy.com/sony-headphones", "title": "Best Buy: Sony WH-1000XM5"},
        ]
    }
    MockTavilyClient.return_value = mock_client_instance
    
    # Run test
    searcher = SearchTool()
    results = searcher.find_product_urls("Sony WH-1000XM5", max_results=2)
    
    # Assertions
    assert len(results) == 2
    assert results[0]["competitor"] == "Amazon"
    assert results[0]["url"] == "https://www.amazon.com/Sony-WH-1000XM5/dp/..."
    assert results[1]["competitor"] == "Bestbuy"
    assert results[1]["url"] == "https://www.bestbuy.com/sony-headphones"
    
    mock_client_instance.search.assert_called_once_with(
        query="buy Sony WH-1000XM5 price online store -review -video",
        search_depth="basic",
        max_results=2,
        include_raw_content=False
    )

@patch('src.search.TavilyClient')
def test_find_product_urls_failure(MockTavilyClient):
    # Setup mock
    mock_client_instance = Mock()
    mock_client_instance.search.side_effect = Exception("API Key Invalid")
    MockTavilyClient.return_value = mock_client_instance
    
    # Run test
    searcher = SearchTool()
    results = searcher.find_product_urls("Bad Product")
    
    # Assertions
    assert results == []
