"""News analysis report data model"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

from .sentiment import MarketSentiment
from .trend import EconomicTrends
from .recommendation import StockRecommendation
from ..utils.date_utils import validate_date


class NewsAnalysisReport(BaseModel):
    """Complete news analysis report."""
    
    date: str = Field(..., description="Date in YYYYMMDD format")
    sentiment: MarketSentiment = Field(..., description="Market sentiment analysis")
    trends: EconomicTrends = Field(..., description="Economic trends analysis")
    recommendations: List[StockRecommendation] = Field(
        default_factory=list,
        description="Stock recommendations"
    )
    key_news_summaries: List[str] = Field(
        default_factory=list,
        description="Key news summaries"
    )
    generated_at: datetime = Field(default_factory=datetime.now, description="Generation timestamp")
    analysis_version: str = Field(default="1.0.0", description="Analysis version")
    
    @field_validator('date')
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        """Validate date format."""
        if not validate_date(v):
            raise ValueError(f"Invalid date format: {v}. Expected YYYYMMDD.")
        return v
    
    @field_validator('recommendations')
    @classmethod
    def validate_recommendations(cls, v: List[StockRecommendation]) -> List[StockRecommendation]:
        """Ensure at least one recommendation (with disclaimer)."""
        if not v:
            # Add default disclaimer recommendation
            from .recommendation import StockRecommendation
            v = [
                StockRecommendation(
                    industry="通用",
                    reason="市场分析仅供参考",
                    risk_level="中",
                    disclaimer="投资有风险，建议仅供参考，不构成投资建议"
                )
            ]
        return v


class AnalysisIndex(BaseModel):
    """Analysis index for tracking history."""
    
    dates: List[str] = Field(..., description="List of analyzed dates")
    latest: str = Field(..., description="Latest analysis date")
    updated_at: datetime = Field(default_factory=datetime.now, description="Index update timestamp")
    
    @field_validator('dates')
    @classmethod
    def validate_dates(cls, v: List[str]) -> List[str]:
        """Validate and sort dates."""
        for date in v:
            if not validate_date(date):
                raise ValueError(f"Invalid date format: {date}")
        # Sort dates in ascending order
        return sorted(v)
    
    @field_validator('latest')
    @classmethod
    def validate_latest(cls, v: str, info) -> str:
        """Validate latest date exists in dates list."""
        dates = info.data.get('dates', [])
        if dates and v not in dates:
            raise ValueError(f"latest date {v} must be in dates list")
        return v
