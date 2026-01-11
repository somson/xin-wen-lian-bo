"""Economic trends data model"""

from typing import List
from pydantic import BaseModel, Field, field_validator


class EconomicTrends(BaseModel):
    """Economic development trends analysis result."""
    
    summary: str = Field(..., max_length=500, description="Trend summary")
    policies: List[str] = Field(default_factory=list, description="Key policy directions")
    industries: List[str] = Field(default_factory=list, description="Hot industries")
    indicators: List[str] = Field(default_factory=list, description="Macroeconomic indicators")
    key_news: List[str] = Field(..., min_length=1, description="Key news supporting trends")
    
    @field_validator('summary')
    @classmethod
    def validate_summary(cls, v: str) -> str:
        """Validate and truncate summary if too long."""
        v = v.strip()
        max_length = 500
        if len(v) > max_length:
            # Try to truncate at sentence boundary
            truncated = v[:max_length]
            # Find last sentence-ending punctuation
            last_period = truncated.rfind('。')
            last_exclamation = truncated.rfind('！')
            last_question = truncated.rfind('？')
            last_comma = truncated.rfind('，')
            
            cut_point = max(last_period, last_exclamation, last_question, last_comma)
            
            # Only use sentence boundary if we keep at least 80% of text
            if cut_point > max_length * 0.8:
                v = truncated[:cut_point + 1] + "..."
            else:
                v = truncated + "..."
        return v
    
    @field_validator('key_news')
    @classmethod
    def validate_key_news(cls, v: List[str]) -> List[str]:
        """Validate key news list."""
        if not v or len(v) == 0:
            raise ValueError("key_news must contain at least one item")
        return [item.strip() for item in v if item.strip()]
    
    def model_post_init(self, __context):
        """Validate that at least one list is non-empty."""
        if not any([self.policies, self.industries, self.indicators]):
            raise ValueError("At least one of policies, industries, or indicators must be non-empty")
