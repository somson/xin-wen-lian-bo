"""Stock recommendation data model"""

from datetime import datetime
from typing import List, Literal
from pydantic import BaseModel, Field, field_validator


class StockRecommendation(BaseModel):
    """Stock investment recommendation."""
    
    industry: str = Field(..., description="Recommended industry")
    reason: str = Field(..., max_length=200, description="Recommendation reason")
    companies: List[str] = Field(
        default_factory=list,
        min_length=0,
        max_length=3,
        description="List of 3 A-share market leading companies (format: 公司名称(股票代码))"
    )
    related_news: List[str] = Field(default_factory=list, description="Related news summaries")
    risk_level: Literal["低", "中", "高"] = Field(..., description="Risk level")
    disclaimer: str = Field(
        default="投资有风险，仅供参考",
        description="Risk disclaimer"
    )
    recommended_at: datetime = Field(default_factory=datetime.now, description="Recommendation timestamp")
    
    @field_validator('companies')
    @classmethod
    def validate_companies(cls, v: List[str]) -> List[str]:
        """Validate companies list."""
        if len(v) > 3:
            raise ValueError("companies list must contain at most 3 companies")
        return [company.strip() for company in v if company.strip()]
    
    @field_validator('reason')
    @classmethod
    def validate_reason(cls, v: str) -> str:
        """Validate reason length."""
        if len(v) > 200:
            raise ValueError("reason must be 200 characters or less")
        return v.strip()
