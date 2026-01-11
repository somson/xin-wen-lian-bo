"""Main news analyzer service"""

from typing import Optional
from datetime import datetime

from .news_reader import NewsReader
from .sentiment_analyzer import SentimentAnalyzer
from .trend_analyzer import TrendAnalyzer
from .recommendation_engine import RecommendationEngine
from .feishu_notifier import FeishuNotifier
from ..models.analysis import NewsAnalysisReport
from ..storage.file_storage import FileStorage
from ..storage.index_manager import IndexManager
from ..utils.logger import logger
from ..utils.date_utils import get_today_date


class NewsAnalyzer:
    """Main service for analyzing news and generating reports."""
    
    def __init__(
        self,
        news_reader: Optional[NewsReader] = None,
        sentiment_analyzer: Optional[SentimentAnalyzer] = None,
        trend_analyzer: Optional[TrendAnalyzer] = None,
        recommendation_engine: Optional[RecommendationEngine] = None,
        file_storage: Optional[FileStorage] = None,
        index_manager: Optional[IndexManager] = None,
        feishu_notifier: Optional[FeishuNotifier] = None
    ):
        """Initialize news analyzer.
        
        Args:
            news_reader: News reader service
            sentiment_analyzer: Sentiment analyzer service
            trend_analyzer: Trend analyzer service
            recommendation_engine: Recommendation engine service
            file_storage: File storage service
            index_manager: Index manager service
            feishu_notifier: Feishu notifier service
        """
        self.news_reader = news_reader or NewsReader()
        self.sentiment_analyzer = sentiment_analyzer or SentimentAnalyzer()
        self.trend_analyzer = trend_analyzer or TrendAnalyzer()
        self.recommendation_engine = recommendation_engine or RecommendationEngine()
        self.file_storage = file_storage or FileStorage()
        self.index_manager = index_manager or IndexManager()
        self.feishu_notifier = feishu_notifier or FeishuNotifier()
    
    async def analyze_news(self, date: Optional[str] = None, force: bool = False) -> NewsAnalysisReport:
        """Analyze news for specified date.
        
        Args:
            date: Date string in YYYYMMDD format. If None, uses today's date.
            force: Whether to force re-analysis even if result exists
            
        Returns:
            NewsAnalysisReport
        """
        if date is None:
            date = get_today_date()
        
        # Check if analysis already exists
        if not force:
            existing = self.file_storage.load_analysis(date)
            if existing:
                logger.info(f"Analysis for {date} already exists, skipping")
                return existing
        
        logger.info(f"Starting analysis for date: {date}")
        
        # Read news content
        news_content = self.news_reader.read_news(date)
        
        # Analyze sentiment and trends in parallel
        sentiment_task = self.sentiment_analyzer.analyze(news_content)
        trend_task = self.trend_analyzer.analyze(news_content)
        
        sentiment = await sentiment_task
        trends = await trend_task
        
        # Generate recommendations
        recommendations = await self.recommendation_engine.generate_recommendations(
            sentiment, trends
        )
        
        # Extract key news summaries
        key_news_summaries = sentiment.key_news[:5] + trends.key_news[:5]
        key_news_summaries = list(dict.fromkeys(key_news_summaries))  # Remove duplicates
        
        # Create report
        report = NewsAnalysisReport(
            date=date,
            sentiment=sentiment,
            trends=trends,
            recommendations=recommendations,
            key_news_summaries=key_news_summaries,
            generated_at=datetime.now()
        )
        
        # Save to analysis directory
        self.file_storage.save_analysis(report)
        
        # Save to results directory (markdown format)
        self.file_storage.save_to_results(report, format_type="markdown")
        
        # Update index
        self.index_manager.add_date(date)
        
        # Send Feishu notification
        await self.feishu_notifier.send_analysis_report(report)
        
        logger.info(f"Analysis completed for date: {date}")
        return report
