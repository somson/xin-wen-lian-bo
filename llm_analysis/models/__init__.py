"""Data models for LLM News Analysis"""

from .sentiment import MarketSentiment
from .trend import EconomicTrends
from .recommendation import StockRecommendation
from .analysis import NewsAnalysisReport, AnalysisIndex

__all__ = [
    "MarketSentiment",
    "EconomicTrends",
    "StockRecommendation",
    "NewsAnalysisReport",
    "AnalysisIndex",
]
