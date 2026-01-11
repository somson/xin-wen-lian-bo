"""Market sentiment data model"""

from typing import List, Literal
from pydantic import BaseModel, Field, field_validator


class MarketSentiment(BaseModel):
    """Market sentiment analysis result."""
    
    score: int = Field(..., ge=0, le=100, description="Sentiment score (0-100)")
    category: Literal["积极", "中性", "消极"] = Field(..., description="Sentiment category")
    intensity: Literal["低", "中", "高"] = Field(..., description="Sentiment intensity")
    key_news: List[str] = Field(..., min_length=1, description="Key news supporting sentiment")
    
    @field_validator('key_news')
    @classmethod
    def validate_key_news(cls, v: List[str]) -> List[str]:
        """Validate key news list."""
        if not v or len(v) == 0:
            raise ValueError("key_news must contain at least one item")
        return [item.strip() for item in v if item.strip()]
