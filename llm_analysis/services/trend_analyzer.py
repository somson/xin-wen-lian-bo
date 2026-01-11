"""Economic trends analyzer service"""

import json
from typing import Optional

from .llm_client import LLMClient
from ..models.trend import EconomicTrends
from ..utils.logger import logger


class TrendAnalyzer:
    """Service for analyzing economic trends from news content."""
    
    def __init__(self, llm_client: Optional[LLMClient] = None):
        """Initialize trend analyzer.
        
        Args:
            llm_client: LLM client instance
        """
        self.llm_client = llm_client or LLMClient()
    
    async def analyze(self, news_content: str) -> EconomicTrends:
        """Analyze economic trends from news content.
        
        Args:
            news_content: News content to analyze
            
        Returns:
            EconomicTrends analysis result
        """
        system_prompt = """你是一位专业的宏观经济分析师。请分析新闻内容，识别经济发展趋势。
返回JSON格式，包含以下字段：
- summary: 趋势总结（500字符以内，请尽量简洁）
- policies: 关键政策方向列表（可选）
- industries: 热点行业列表（可选）
- indicators: 宏观经济指标变化列表（可选）
- key_news: 支持该趋势的关键新闻引用列表（至少1条）

注意：
1. summary字段必须控制在500字符以内，请尽量简洁明了
2. policies、industries、indicators至少有一个非空列表"""
        
        user_prompt = f"""请分析以下新闻内容，识别经济发展趋势：

{news_content[:8000]}

请返回JSON格式的分析结果。"""
        
        try:
            response = await self.llm_client.analyze(
                prompt=user_prompt,
                system_prompt=system_prompt,
                json_mode=True
            )
            
            data = json.loads(response)
            trends = EconomicTrends(**data)
            
            logger.info("Trend analysis completed")
            return trends
            
        except Exception as e:
            logger.error(f"Failed to analyze trends: {e}")
            raise
