import logging
from typing import Optional
from firecrawl import FirecrawlApp
from langfuse import observe
from config.settings import settings

logger = logging.getLogger(__name__)

class Scraper:
    """Handles web scraping using Firecrawl API to extract Markdown content."""
    
    def __init__(self):
        self.app = FirecrawlApp(
            api_key=settings.firecrawl_api_key,
            api_url=settings.firecrawl_api_url
        )
    @observe()    
    def fetch_page_content(self, url: str) -> Optional[str]:
        """
        Scrapes a URL and returns its content as Markdown.
        
        Args:
            url (str): The product URL to scrape.
            
        Returns:
            Optional[str]: The markdown content of the page, or None if failed.
        """
        try:
            logger.info(f"Scraping URL: {url}")
            
            # Use Firecrawl to extract markdown
            scrape_result = self.app.scrape(
                url, 
                formats=['markdown']
            )
            
            if hasattr(scrape_result, 'markdown') and scrape_result.markdown:
                return scrape_result.markdown
            else:
                logger.error(f"Failed to get markdown for {url}.")
                return None
                
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            return None
