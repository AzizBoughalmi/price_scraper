import json
import logging
from typing import Optional
import google.generativeai as genai
from langfuse import observe , Langfuse
from config.settings import settings
from src.models import PriceResult

logger = logging.getLogger(__name__)

class LLMParser:
    """Parses markdown content using Gemini to extract structured pricing data."""
    
    def __init__(self):
        genai.configure(api_key=settings.gemini_api_key)
        # Using gemini-2.5-flash since gemini-4o-mini is an OpenAI model name. You requested "gemini".
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    @observe(as_type="generation")    
    def extract_price_data(self, markdown_content: str, product_name: str, competitor: str, url: str) -> Optional[PriceResult]:
        """
        Extracts price data from markdown content.
        
        Args:
            markdown_content: The website body text.
            product_name: The expected product name.
            competitor: The name of the competitor.
            url: The source URL.
            
        Returns:
            PriceResult if successful, None otherwise.
        """
        prompt = f"""
        Extract the pricing information for the product "{product_name}" from the following markdown text scraped from an online store.
        
        Website Content:
        {markdown_content[:20000]} # Limit context length if needed
        
        Please provide the extraction strictly in JSON format matching this schema:
        {{
            "price": <float, the numerical price, e.g. 348.0>,
            "currency": "<string, e.g. 'USD', 'EUR'>",
            "status": "<string, e.g. 'In Stock', 'Out of Stock', 'Unknown'>",
            "additional_info": "<string, optional details like shipping or discounts>"
        }}
        
        Ensure the response is ONLY valid JSON, without markdown formatting blocks like ```json.
        """
        
        try:
            logger.info(f"Extracting data for {product_name}...")
            response = self.model.generate_content(prompt)
            
            # Clean up response if it contains markdown code blocks
            response_text = response.text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
                
            parsed_data = json.loads(response_text.strip())

            Langfuse().update_current_generation(model=self.model.model_name, input=prompt, output=response_text)
            # Return structured result
            return PriceResult(
                competitor=competitor,
                product_name=product_name,
                price=float(parsed_data.get("price", 0.0)),
                currency=parsed_data.get("currency", "USD"),
                url=url,
                status=parsed_data.get("status", "Unknown"),
                additional_info=parsed_data.get("additional_info")
            )
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM JSON response: {str(e)}")
            logger.debug(f"Raw response: {response.text}")
            return None
        except Exception as e:
            logger.error(f"LLM extraction failed: {str(e)}")
            return None
