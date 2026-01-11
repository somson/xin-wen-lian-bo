"""Stock recommendation engine service"""

import json
from typing import List, Optional

from .llm_client import LLMClient
from ..models.recommendation import StockRecommendation
from ..models.sentiment import MarketSentiment
from ..models.trend import EconomicTrends
from ..utils.logger import logger


class RecommendationEngine:
    """Service for generating stock recommendations based on analysis."""
    
    def __init__(self, llm_client: Optional[LLMClient] = None):
        """Initialize recommendation engine.
        
        Args:
            llm_client: LLM client instance
        """
        self.llm_client = llm_client or LLMClient()
    
    async def generate_recommendations(
        self,
        sentiment: MarketSentiment,
        trends: EconomicTrends
    ) -> List[StockRecommendation]:
        """Generate stock recommendations based on sentiment and trends.
        
        Args:
            sentiment: Market sentiment analysis
            trends: Economic trends analysis
            
        Returns:
            List of stock recommendations
        """
        system_prompt = """你是一位专业的股票投资顾问。基于市场情绪和经济发展趋势，提供股票投资建议。
返回JSON格式，包含recommendations数组，每个推荐包含：
- industry: 推荐关注的行业
- reason: 推荐理由（200字以内）
- companies: A股市场相关的头部公司列表（必须包含3个，格式：公司名称(股票代码)，例如：贵州茅台(600519)）
- related_news: 相关新闻摘要列表（可选）
- risk_level: 风险等级（"低"、"中"或"高"）

注意：
1. 必须包含风险提示和免责声明
2. companies字段必须包含3个A股头部公司，格式为"公司名称(股票代码)"
3. 选择公司时，优先考虑行业龙头、市值较大、知名度高的A股上市公司"""
        
        analysis_summary = f"""市场情绪：{sentiment.category}（评分：{sentiment.score}/100，强度：{sentiment.intensity}）
经济发展趋势：{trends.summary}
热点行业：{', '.join(trends.industries[:5]) if trends.industries else '无'}
政策方向：{', '.join(trends.policies[:3]) if trends.policies else '无'}"""
        
        user_prompt = f"""基于以下分析结果，提供股票投资建议：

{analysis_summary}

请返回JSON格式，包含recommendations数组（建议1-3个推荐）。每个推荐必须：
1. 包含风险提示
2. 在companies字段中提供3个A股市场相关的头部公司，格式为"公司名称(股票代码)"
3. 选择的公司应该是该行业的龙头企业、市值较大、知名度高的A股上市公司"""
        
        try:
            response = await self.llm_client.analyze(
                prompt=user_prompt,
                system_prompt=system_prompt,
                json_mode=True
            )
            
            data = json.loads(response)
            recommendations_data = data.get('recommendations', [])
            
            recommendations = [
                StockRecommendation(**rec) for rec in recommendations_data
            ]
            
            logger.info(f"Generated {len(recommendations)} recommendations")
            return recommendations
            
        except Exception as e:
            logger.error(f"Failed to generate recommendations: {e}")
            # Return default disclaimer recommendation on error
            return [
                StockRecommendation(
                    industry="通用",
                    reason="市场分析仅供参考",
                    companies=[],
                    risk_level="中",
                    disclaimer="投资有风险，建议仅供参考，不构成投资建议"
                )
            ]
