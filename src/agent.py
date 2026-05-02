import logging
from typing import List
from src.scraper import Scraper
from src.llm_parser import LLMParser
from src.search import SearchTool
from src.models import PriceResult

logger = logging.getLogger(__name__)

class Agent:
    """Core logic sequential flow to govern the price scraping procedure."""
    
    def __init__(self):
        self.scraper = Scraper()
        self.parser = LLMParser()
        self.searcher = SearchTool()
        
    def process_url(self, url: str, product_name: str, competitor: str) -> PriceResult | None:
        """Process a single URL: Scrape -> Parse."""
        logger.info(f"Processing {competitor} for {product_name} at {url}")
        
        # Step 1: Scrape
        markdown = self.scraper.fetch_page_content(url)
        if not markdown:
            logger.warning(f"Skipping {url} due to scraping failure.")
            return None
            
        # Step 2: Parse with LLM
        result = self.parser.extract_price_data(
            markdown_content=markdown,
            product_name=product_name,
            competitor=competitor,
            url=url
        )
        
        if not result:
            logger.warning(f"Failed to parse pricing data for {url}.")
            return None
            
        return result
        
    def run_multi_url_search(self, product_name: str, urls: List[dict]) -> List[PriceResult]:
        """
        Processes a list of URLs and returns parsed results.
        
        Args:
            urls: List of dicts, each containing: {"url": "...", "competitor": "..."}
        """
        results = []
        for item in urls:
            res = self.process_url(item["url"], product_name, item["competitor"])
            if res:
                results.append(res)
                
        return results

    def run_autonomous_search(self, product_name: str, max_results: int = 3) -> List[PriceResult]:
        """
        Fully autonomous flow: Searches for the product, then parses pricing from each link.
        """
        logger.info(f"Starting autonomous search for {product_name}...")
        urls_to_process = self.searcher.find_product_urls(product_name, max_results)
        
        if not urls_to_process:
            logger.warning(f"autonomous search found no urls for {product_name}.")
            return []
            
        logger.info(f"Found {len(urls_to_process)} links. Proceeding to extract data...")
        return self.run_multi_url_search(product_name, urls_to_process)
