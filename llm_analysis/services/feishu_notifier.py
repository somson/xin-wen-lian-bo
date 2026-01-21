"""Feishu webhook notification service"""

import json
from typing import Optional
from datetime import datetime

import httpx

from ..models.analysis import NewsAnalysisReport
from ..config import settings
from ..utils.logger import logger


class FeishuNotifier:
    """Service for sending notifications to Feishu webhook."""
    
    def __init__(self, webhook_url: Optional[str] = None, enabled: Optional[bool] = None):
        """Initialize Feishu notifier.
        
        Args:
            webhook_url: Feishu webhook URL
            enabled: Whether notifications are enabled
        """
        self.webhook_url = webhook_url or settings.feishu_webhook_url
        self.enabled = enabled if enabled is not None else settings.feishu_enabled
    
    async def send_analysis_report(self, report: NewsAnalysisReport) -> bool:
        """Send analysis report to Feishu webhook.
        
        Args:
            report: Analysis report to send
            
        Returns:
            True if sent successfully, False otherwise
        """
        if not self.enabled or not self.webhook_url:
            logger.info("Feishu notifications disabled or webhook URL not configured")
            return False
        
        try:
            message = self._format_message(report)
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    self.webhook_url,
                    json=message,
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
            
            logger.info(f"Analysis report sent to Feishu webhook successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send Feishu notification: {e}")
            return False
    
    def _format_message(self, report: NewsAnalysisReport) -> dict:
        """Format analysis report as Feishu message.
        
        Args:
            report: Analysis report
            
        Returns:
            Formatted message dictionary
        """
        elements = []
        
        # Header with generation time
        elements.append({
            "tag": "markdown",
            "content": f"**生成时间**: {report.generated_at.strftime('%Y-%m-%d %H:%M:%S')}"
        })
        elements.append({"tag": "hr"})
        
        # Market Sentiment Section
        sentiment_lines = [
            f"**评分**: {report.sentiment.score}/100",
            f"**分类**: {report.sentiment.category}",
            f"**强度**: {report.sentiment.intensity}",
            "",
            "**关键新闻**:"
        ]
        for news in report.sentiment.key_news:
            sentiment_lines.append(f"- {news}")
        
        elements.append({
            "tag": "markdown",
            "content": "**一、市场情绪**\n\n" + "\n".join(sentiment_lines)
        })
        elements.append({"tag": "hr"})
        
        # Economic Trends Section
        trends_lines = [report.trends.summary, ""]
        
        if report.trends.policies:
            trends_lines.append("**政策方向**:")
            for policy in report.trends.policies:
                trends_lines.append(f"- {policy}")
            trends_lines.append("")
        
        if report.trends.industries:
            trends_lines.append("**热点行业**:")
            for industry in report.trends.industries:
                trends_lines.append(f"- {industry}")
            trends_lines.append("")
        
        if report.trends.indicators:
            trends_lines.append("**经济指标**:")
            for indicator in report.trends.indicators:
                trends_lines.append(f"- {indicator}")
            trends_lines.append("")
        
        elements.append({
            "tag": "markdown",
            "content": "**二、经济发展趋势**\n\n" + "\n".join(trends_lines)
        })
        elements.append({"tag": "hr"})
        
        # Recommendations Section
        if report.recommendations:
            recommendations_lines = []
            for i, rec in enumerate(report.recommendations, 1):
                recommendations_lines.append(f"**{i}. {rec.industry}**")
                recommendations_lines.append("")
                recommendations_lines.append(f"**推荐理由**: {rec.reason}")
                recommendations_lines.append("")
                
                if rec.companies:
                    recommendations_lines.append("**相关A股头部公司**:")
                    for company in rec.companies:
                        recommendations_lines.append(f"- {company}")
                    recommendations_lines.append("")
                
                recommendations_lines.append(f"**风险等级**: {rec.risk_level}")
                recommendations_lines.append("")
            
            elements.append({
                "tag": "markdown",
                "content": "**三、推荐建议**\n\n" + "\n".join(recommendations_lines)
            })
            elements.append({"tag": "hr"})
        
        # Disclaimer
        elements.append({
            "tag": "note",
            "elements": [
                {
                    "tag": "plain_text",
                    "content": "⚠️ 免责声明: 投资有风险，建议仅供参考，不构成投资建议"
                }
            ]
        })

        # @所有人
        elements.append({
            "tag": "div",
            "text": {
                "content": "<at id=all></at>",
                "tag": "lark_md"
            }
        })
        # Construct card message
        content = {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": f"《新闻联播》分析报告 - {report.date}"
                },
                "template": "blue"
            },
            "elements": elements
        }
        
        return {
            "msg_type": "interactive",
            "card": content
        }
