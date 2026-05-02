from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone

class PriceResult(BaseModel):
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    competitor: str
    product_name: str
    price: float
    currency: str
    url: str
    status: str
    additional_info: Optional[str] = None
