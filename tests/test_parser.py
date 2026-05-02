import pytest
from unittest.mock import Mock, patch
from src.llm_parser import LLMParser
from src.models import PriceResult

@patch('src.llm_parser.genai.GenerativeModel')
def test_extract_price_data_success(MockModel):
    # Setup mock
    mock_model_instance = Mock()
    mock_response = Mock()
    mock_response.text = '{"price": 348.0, "currency": "USD", "status": "In Stock", "additional_info": "Free shipping"}'
    mock_model_instance.generate_content.return_value = mock_response
    MockModel.return_value = mock_model_instance
    
    # Run test
    parser = LLMParser()
    result = parser.extract_price_data(
        markdown_content="# Sony WH-1000XM5\nPrice: $348.00\nIn Stock",
        product_name="Sony WH-1000XM5",
        competitor="Amazon",
        url="https://amazon.com/sony"
    )
    
    # Assertions
    assert isinstance(result, PriceResult)
    assert result.price == 348.0
    assert result.currency == "USD"
    assert result.status == "In Stock"
    assert result.additional_info == "Free shipping"
    assert result.competitor == "Amazon"
    assert result.product_name == "Sony WH-1000XM5"
    assert result.url == "https://amazon.com/sony"

@patch('src.llm_parser.genai.GenerativeModel')
def test_extract_price_data_invalid_json(MockModel):
    # Setup mock to return text instead of JSON
    mock_model_instance = Mock()
    mock_response = Mock()
    mock_response.text = 'I could not find the price.'
    mock_model_instance.generate_content.return_value = mock_response
    MockModel.return_value = mock_model_instance
    
    # Run test
    parser = LLMParser()
    result = parser.extract_price_data("Markdown", "Product", "Comp", "Url")
    
    # Assertions
    assert result is None
