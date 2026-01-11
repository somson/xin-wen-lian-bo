"""File storage service for analysis results"""

import json
from pathlib import Path
from typing import Optional
from datetime import datetime

from ..models.analysis import NewsAnalysisReport
from ..config import settings
from ..utils.logger import logger


class FileStorage:
    """File storage service for saving and loading analysis results."""
    
    def __init__(self, analysis_dir: Optional[Path] = None, results_dir: Optional[Path] = None):
        """Initialize file storage.
        
        Args:
            analysis_dir: Directory for analysis JSON files
            results_dir: Directory for formatted results files
        """
        self.analysis_dir = analysis_dir or settings.analysis_dir
        self.results_dir = results_dir or settings.results_dir
        
        # Ensure directories exist
        self.analysis_dir.mkdir(parents=True, exist_ok=True)
        self.results_dir.mkdir(parents=True, exist_ok=True)
    
    def save_analysis(self, report: NewsAnalysisReport) -> Path:
        """Save analysis report to JSON file.
        
        Args:
            report: Analysis report to save
            
        Returns:
            Path to saved file
        """
        file_path = self.analysis_dir / f"{report.date}.json"
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(
                    report.model_dump(mode='json'),
                    f,
                    ensure_ascii=False,
                    indent=2,
                    default=str
                )
            
            logger.info(f"Analysis report saved to {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Failed to save analysis report: {e}")
            raise
    
    def load_analysis(self, date: str) -> Optional[NewsAnalysisReport]:
        """Load analysis report by date.
        
        Args:
            date: Date string in YYYYMMDD format
            
        Returns:
            Analysis report or None if not found
        """
        file_path = self.analysis_dir / f"{date}.json"
        
        if not file_path.exists():
            logger.warning(f"Analysis report not found: {file_path}")
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return NewsAnalysisReport(**data)
            
        except Exception as e:
            logger.error(f"Failed to load analysis report: {e}")
            raise
    
    def save_to_results(self, report: NewsAnalysisReport, format_type: str = "markdown") -> Path:
        """Save analysis report to results directory in specified format.
        
        Args:
            report: Analysis report to save
            format_type: Format type (markdown, json, text)
            
        Returns:
            Path to saved file
        """
        date = report.date
        
        if format_type == "markdown":
            content = self._format_as_markdown(report)
            file_path = self.results_dir / f"{date}.md"
        elif format_type == "json":
            content = json.dumps(
                report.model_dump(mode='json'),
                ensure_ascii=False,
                indent=2,
                default=str
            )
            file_path = self.results_dir / f"{date}.json"
        elif format_type == "text":
            content = self._format_as_text(report)
            file_path = self.results_dir / f"{date}.txt"
        else:
            raise ValueError(f"Unsupported format: {format_type}")
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"Results saved to {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Failed to save results: {e}")
            raise
    
    def _format_as_markdown(self, report: NewsAnalysisReport) -> str:
        """Format report as Markdown."""
        lines = [
            f"# 《新闻联播》分析报告 - {report.date}",
            "",
            f"**生成时间**: {report.generated_at.strftime('%Y-%m-%d %H:%M:%S')}",
            f"**分析版本**: {report.analysis_version}",
            "",
            "## 市场情绪",
            "",
            f"**评分**: {report.sentiment.score}/100",
            f"**分类**: {report.sentiment.category}",
            f"**强度**: {report.sentiment.intensity}",
            "",
            "### 关键新闻",
            ""
        ]
        
        for news in report.sentiment.key_news:
            lines.append(f"- {news}")
        
        lines.extend([
            "",
            "## 经济发展趋势",
            "",
            f"{report.trends.summary}",
            ""
        ])
        
        if report.trends.policies:
            lines.extend([
                "### 政策方向",
                ""
            ])
            for policy in report.trends.policies:
                lines.append(f"- {policy}")
            lines.append("")
        
        if report.trends.industries:
            lines.extend([
                "### 热点行业",
                ""
            ])
            for industry in report.trends.industries:
                lines.append(f"- {industry}")
            lines.append("")
        
        if report.trends.indicators:
            lines.extend([
                "### 经济指标",
                ""
            ])
            for indicator in report.trends.indicators:
                lines.append(f"- {indicator}")
            lines.append("")
        
        if report.recommendations:
            lines.extend([
                "## 推荐建议",
                ""
            ])
            for i, rec in enumerate(report.recommendations, 1):
                lines.extend([
                    f"### {i}. {rec.industry}",
                    "",
                    f"**推荐理由**: {rec.reason}",
                    ""
                ])
                
                # Add companies list if available
                if rec.companies:
                    lines.append("**相关A股头部公司**:")
                    for company in rec.companies:
                        lines.append(f"- {company}")
                    lines.append("")
                
                lines.extend([
                    f"**风险等级**: {rec.risk_level}",
                    "",
                    f"**免责声明**: {rec.disclaimer}",
                    ""
                ])
        
        return "\n".join(lines)
    
    def _format_as_text(self, report: NewsAnalysisReport) -> str:
        """Format report as plain text."""
        lines = [
            f"《新闻联播》分析报告 - {report.date}",
            f"生成时间: {report.generated_at.strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "市场情绪:",
            f"  评分: {report.sentiment.score}/100",
            f"  分类: {report.sentiment.category}",
            f"  强度: {report.sentiment.intensity}",
            "",
            "关键新闻:",
        ]
        
        for news in report.sentiment.key_news:
            lines.append(f"  - {news}")
        
        lines.extend([
            "",
            "经济发展趋势:",
            f"  {report.trends.summary}",
            ""
        ])
        
        if report.trends.policies:
            lines.append("政策方向:")
            for policy in report.trends.policies:
                lines.append(f"  - {policy}")
            lines.append("")
        
        if report.trends.industries:
            lines.append("热点行业:")
            for industry in report.trends.industries:
                lines.append(f"  - {industry}")
            lines.append("")
        
        if report.recommendations:
            lines.append("推荐建议:")
            for rec in report.recommendations:
                lines.extend([
                    f"  {rec.industry}: {rec.reason}",
                ])
                if rec.companies:
                    lines.append("  相关A股头部公司:")
                    for company in rec.companies:
                        lines.append(f"    - {company}")
                lines.extend([
                    f"  风险等级: {rec.risk_level}",
                    f"  {rec.disclaimer}",
                    ""
                ])
        
        return "\n".join(lines)
