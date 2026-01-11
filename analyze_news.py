#!/usr/bin/env python3
"""CLI entry point for LLM News Analysis Tool"""

import asyncio
import sys
import json
from pathlib import Path
from typing import Optional


import click
from llm_analysis.services.analyzer import NewsAnalyzer
from llm_analysis.services.feishu_notifier import FeishuNotifier
from llm_analysis.storage.file_storage import FileStorage
from llm_analysis.storage.index_manager import IndexManager
from llm_analysis.utils.date_utils import validate_date, get_today_date
from llm_analysis.utils.logger import logger


@click.group()
def cli():
    """LLM News Analysis Tool - Analyze news content using LLM."""
    pass


@cli.command()
@click.option('--date', default=None, help='Date in YYYYMMDD format (default: today)')
@click.option('--force', is_flag=True, help='Force re-analysis even if result exists')
def analyze(date: Optional[str], force: bool):
    """Analyze news content and generate analysis report."""
    try:
        if date and not validate_date(date):
            click.echo(f"错误: 无效的日期格式: {date}. 期望格式: YYYYMMDD", err=True)
            sys.exit(2)
        
        analyzer = NewsAnalyzer()
        report = asyncio.run(analyzer.analyze_news(date=date, force=force))
        
        click.echo(f"分析完成！日期: {report.date}")
        click.echo(f"市场情绪: {report.sentiment.category} ({report.sentiment.score}/100)")
        click.echo(f"分析结果已保存到:")
        click.echo(f"  - 分析文件: news/analysis/{report.date}.json")
        click.echo(f"  - 结果文件: results/{report.date}.md")
        
        sys.exit(0)
        
    except FileNotFoundError as e:
        click.echo(f"错误: 文件不存在 - {e}", err=True)
        sys.exit(1)
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        click.echo(f"错误: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--date', required=True, help='Date in YYYYMMDD format')
@click.option('--format', 'format_type', default='text', type=click.Choice(['text', 'json', 'markdown']))
def query(date: str, format_type: str):
    """Query analysis report for specified date."""
    try:
        if not validate_date(date):
            click.echo(f"错误: 无效的日期格式: {date}", err=True)
            sys.exit(2)
        
        storage = FileStorage()
        report = storage.load_analysis(date)
        
        if not report:
            click.echo(f"错误: 分析报告不存在 - {date}", err=True)
            sys.exit(1)
        
        if format_type == 'json':
            output = json.dumps(
                report.model_dump(mode='json'),
                ensure_ascii=False,
                indent=2,
                default=str
            )
        elif format_type == 'markdown':
            output = storage._format_as_markdown(report)
        else:  # text
            output = storage._format_as_text(report)
        
        click.echo(output)
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"Query failed: {e}")
        click.echo(f"错误: {e}", err=True)
        sys.exit(2)


@cli.command()
@click.option('--limit', default=None, type=int, help='Limit number of results')
def list_dates(limit: Optional[int]):
    """List all available analysis dates."""
    try:
        index_manager = IndexManager()
        dates = index_manager.get_dates(limit=limit)
        
        if not dates:
            click.echo("没有找到分析记录")
            sys.exit(0)
        
        for date in dates:
            click.echo(date)
        
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"List failed: {e}")
        click.echo(f"错误: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('dates', nargs=-1, required=True)
@click.option('--metric', default='all', type=click.Choice(['sentiment', 'trends', 'all']))
def compare(dates: tuple, metric: str):
    """Compare analysis results across multiple dates."""
    try: 
        if len(dates) < 2:
            click.echo("错误: 至少需要2个日期进行对比", err=True)
            sys.exit(2)
        
        for date in dates:
            if not validate_date(date):
                click.echo(f"错误: 无效的日期格式: {date}", err=True)
                sys.exit(2)
        
        storage = FileStorage()
        reports = []
        
        for date in dates:
            report = storage.load_analysis(date)
            if not report:
                click.echo(f"错误: 分析报告不存在 - {date}", err=True)
                sys.exit(1)
            reports.append(report)
        
        # Format comparison output
        output_lines = ["## 分析结果对比\n"]
        
        if metric in ['sentiment', 'all']:
            output_lines.append("### 市场情绪对比\n")
            for report in reports:
                output_lines.append(
                    f"{report.date}: {report.sentiment.category} "
                    f"({report.sentiment.score}/100, {report.sentiment.intensity})"
                )
            output_lines.append("")
        
        if metric in ['trends', 'all']:
            output_lines.append("### 经济发展趋势对比\n")
            for report in reports:
                output_lines.append(f"{report.date}: {report.trends.summary[:100]}...")
            output_lines.append("")
        
        click.echo("\n".join(output_lines))
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"Compare failed: {e}")
        click.echo(f"错误: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--date', required=True, help='Date in YYYYMMDD format')
@click.option('--format', 'format_type', required=True, type=click.Choice(['json', 'csv', 'markdown']))
@click.option('--output', default=None, help='Output file path (default: stdout)')
def export(date: str, format_type: str, output: Optional[str]):
    """Export analysis report to specified format."""
    try:
        if not validate_date(date):
            click.echo(f"错误: 无效的日期格式: {date}", err=True)
            sys.exit(2)
        
        storage = FileStorage()
        report = storage.load_analysis(date)
        
        if not report:
            click.echo(f"错误: 分析报告不存在 - {date}", err=True)
            sys.exit(1)
        
        if format_type == 'csv':
            # Simple CSV export
            lines = [
                "日期,情绪评分,情绪分类,趋势总结",
                f"{report.date},{report.sentiment.score},{report.sentiment.category},\"{report.trends.summary}\""
            ]
            content = "\n".join(lines)
        else:
            content = storage.save_to_results(report, format_type=format_type)
            if isinstance(content, Path):
                # If save_to_results returns a path, read the content
                with open(content, 'r', encoding='utf-8') as f:
                    content = f.read()
        
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(content)
            click.echo(f"导出成功: {output}")
        else:
            click.echo(content)
        
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"Export failed: {e}")
        click.echo(f"错误: {e}", err=True)
        sys.exit(2)


@cli.command()
@click.option('--date', default=None, help='Date in YYYYMMDD format (default: today)')
def send_feishu(date: Optional[str]):
    """Send analysis report to Feishu webhook."""
    try:
        if date is None:
            date = get_today_date()
        
        if not validate_date(date):
            click.echo(f"错误: 无效的日期格式: {date}. 期望格式: YYYYMMDD", err=True)
            sys.exit(2)
        
        # Load analysis report
        storage = FileStorage()
        report = storage.load_analysis(date)
        
        if not report:
            click.echo(f"错误: 分析报告不存在 - {date}", err=True)
            click.echo(f"请先运行分析命令: python analyze_news.py analyze --date {date}", err=True)
            sys.exit(1)
        
        # Check Feishu configuration
        from llm_analysis.config import settings
        if not settings.feishu_enabled:
            click.echo("错误: 飞书通知未启用", err=True)
            click.echo("请在配置文件中设置 FEISHU_ENABLED=true", err=True)
            sys.exit(1)
        
        if not settings.feishu_webhook_url:
            click.echo("错误: 飞书 Webhook URL 未配置", err=True)
            click.echo("请在配置文件中设置 FEISHU_WEBHOOK_URL", err=True)
            sys.exit(1)
        
        # Send to Feishu
        notifier = FeishuNotifier()
        success = asyncio.run(notifier.send_analysis_report(report))
        
        if success:
            click.echo(f"✅ 飞书消息发送成功！日期: {date}")
            sys.exit(0)
        else:
            click.echo("❌ 飞书消息发送失败，请查看日志", err=True)
            sys.exit(1)
        
    except Exception as e:
        logger.error(f"Send Feishu notification failed: {e}")
        click.echo(f"错误: {e}", err=True)
        sys.exit(1)


# Alias for list command
cli.add_command(list_dates, name='list')

if __name__ == '__main__':
    cli()
