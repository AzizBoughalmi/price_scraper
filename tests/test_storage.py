import pytest
import os
from pathlib import Path
from src.models import PriceResult
from src.storage import save_results, load_results

def test_save_and_load_results(tmp_path):
    test_file = tmp_path / "test_results.json"
    
    # Create mock data
    result1 = PriceResult(
        competitor="Amazon",
        product_name="Test Product",
        price=99.99,
        currency="USD",
        url="https://amazon.com/test",
        status="In Stock"
    )
    
    # Test saving
    save_results([result1], test_file)
    assert test_file.exists()
    
    # Test loading
    loaded = load_results(test_file)
    assert len(loaded) == 1
    assert loaded[0].competitor == "Amazon"
    assert loaded[0].price == 99.99
    
    # Test appending
    result2 = PriceResult(
        competitor="Target",
        product_name="Test Product",
        price=89.99,
        currency="USD",
        url="https://target.com/test",
        status="Out of Stock"
    )
    save_results([result2], test_file)
    
    loaded_again = load_results(test_file)
    assert len(loaded_again) == 2
    assert loaded_again[1].competitor == "Target"
