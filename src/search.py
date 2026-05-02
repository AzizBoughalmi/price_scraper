import logging
from typing import List, Dict, Optional
from urllib.parse import urlparse
from tavily import TavilyClient
from config.settings import settings

logger = logging.getLogger(__name__)

class SearchTool:
    """Uses Tavily to search the web for product pages."""
    
    def __init__(self):
        if not settings.tavily_api_key or settings.tavily_api_key.startswith("test_"):
            logger.warning("Using a test or missing Tavily API key! Search may fail.")
        self.client = TavilyClient(api_key=settings.tavily_api_key)
        
    def find_product_urls(self, product_name: str, max_results: int = 3) -> List[Dict[str, str]]:
        """
        Searches for product pages and returns a list of URLs and their competitors.
        
        Args:
            product_name: The name of the product to search.
            max_results: The maximum number of links to return.
            
        Returns:
            A list of dictionaries with structure: {"competitor": "...", "url": "..."}
        """
        logger.info(f"Searching web for: {product_name}")
        query = f"buy {product_name} price online store -review -video"
        
        try:
            # We use 'search_depth=basic' for speed, we just need URLs
            response = self.client.search(
                query=query, 
                search_depth="basic",
                max_results=max_results,
                include_raw_content=False
            )
            
            results = []
            for result in response.get("results", []):
                url = result.get("url")
                if url:
                    results.append({
                        "competitor": self._extract_competitor_name(url),
                        "url": url,
                        "title": result.get("title", "")
                    })
                    
            return results
            
        except Exception as e:
            logger.error(f"Tavily search failed: {str(e)}")
            return []
            
    def _extract_competitor_name(self, url: str) -> str:
        """Heuristic to extract the store name from the URL."""
        try:
            domain = urlparse(url).netloc
            # e.g., www.amazon.com -> amazon
            parts = domain.split('.')
            if 'www' in parts:
                parts.remove('www')
            if len(parts) >= 2:
                # The highest-level domain part likely to be the brand (e.g., amazon from amazon.com)
                return parts[0].capitalize()
            return domain
        except Exception:
            return "Unknown"
