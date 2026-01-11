"""Market sentiment analyzer service"""

import json
from typing import Optional

from pydantic import ValidationError

from .llm_client import LLMClient
from ..models.sentiment import MarketSentiment
from ..utils.logger import logger


class SentimentAnalyzer:
    """Service for analyzing market sentiment from news content."""
    
    def __init__(self, llm_client: Optional[LLMClient] = None):
        """Initialize sentiment analyzer.
        
        Args:
            llm_client: LLM client instance
        """
        self.llm_client = llm_client or LLMClient()
    
    async def analyze(self, news_content: str) -> MarketSentiment:
        """Analyze market sentiment from news content.
        
        Args:
            news_content: News content to analyze
            
        Returns:
            MarketSentiment analysis result
        """
        system_prompt = """你是一位专业的金融分析师。请分析新闻内容，提取市场情绪信息。
返回JSON格式，包含以下字段：
- score: 情绪评分（0-100整数，0=极度消极，50=中性，100=极度积极）
- category: 情绪分类（"积极"、"中性"或"消极"）
- intensity: 情绪强度（"低"、"中"或"高"）
- key_news: 支持该情绪判断的关键新闻标题或摘要列表（至少1条）"""
        
        user_prompt = f"""请分析以下新闻内容，提取市场情绪信息：

{news_content[:8000]}

请返回JSON格式的分析结果。"""
        
        try:
            response = await self.llm_client.analyze(
                prompt=user_prompt,
                system_prompt=system_prompt,
                json_mode=True
            )
            
            data = json.loads(response)
            sentiment = MarketSentiment(**data)
            
            logger.info(f"Sentiment analysis completed: {sentiment.category} ({sentiment.score}/100)")
            return sentiment
            
        except (ValidationError, ValueError) as e:
            logger.error(f"Failed to validate sentiment data: {e}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to analyze sentiment: {e}")
            raise
