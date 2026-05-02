"""Configuration and environment variable management for PriceScout"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
ENV_PATH = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)


class Settings:
    """Application settings loaded from environment variables"""

    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")
        self.firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")
        self.firecrawl_api_url = os.getenv("FIRECRAWL_API_URL", "https://api.firecrawl.dev")
        self.log_level = os.getenv("LOG_LEVEL", "INFO")

        # Validate required API keys
        self._validate_settings()

    def _validate_settings(self):
        """Validate that all required settings are present"""
        missing_keys = []

        if not self.gemini_api_key:
            missing_keys.append("GEMINI_API_KEY")
        if not self.firecrawl_api_key:
            missing_keys.append("FIRECRAWL_API_KEY")

        if missing_keys:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_keys)}. "
                f"Please set them in your .env file or environment."
            )

    def __repr__(self):
        return (
            f"Settings(gemini_api_key={'***' if self.gemini_api_key else 'None'}, "
            f"firecrawl_api_key={'***' if self.firecrawl_api_key else 'None'}, "
            f"log_level={self.log_level})"
        )


# Create a singleton instance
settings = Settings()
