import json
from pathlib import Path
from .models import PriceResult

def save_results(results: list[PriceResult], filepath: str | Path):
    path = Path(filepath)
    data = [r.model_dump() for r in results]
    
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            try:
                existing = json.load(f)
            except json.JSONDecodeError:
                existing = []
        data = existing + data
        
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def load_results(filepath: str | Path) -> list[PriceResult]:
    path = Path(filepath)
    if not path.exists():
        return []
        
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    return [PriceResult(**item) for item in data]
