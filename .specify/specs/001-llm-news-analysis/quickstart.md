# Quick Start Guide: LLM 新闻分析工具

**Feature**: 001-llm-news-analysis  
**Date**: 2025-01-10

## Prerequisites

- Python 3.12 或更高版本
- uv 包管理器（[安装指南](https://github.com/astral-sh/uv)）
- OpenAI API 密钥
- 现有新闻爬取系统已运行（生成 `news/YYYYMMDD.md` 文件）

## Installation

### 1. 安装 uv（如果未安装）

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. 创建 Python 项目

```bash
cd /path/to/xin-wen-lian-bo
mkdir -p llm-analysis
cd llm-analysis

# 使用 uv 初始化项目
uv init --name llm-analysis --python 3.12
```

### 3. 安装依赖

```bash
# 添加依赖
uv add openai pydantic python-dotenv httpx

# 添加开发依赖
uv add --dev pytest pytest-asyncio pytest-mock pytest-cov
```

### 4. 配置环境变量

创建 `.env` 文件：

```bash
cp .env.example .env
```

编辑 `.env` 文件，设置 OpenAI API 密钥：

```env
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_TIMEOUT=300
ANALYSIS_DIR=../news/analysis
NEWS_DIR=../news
```

## Basic Usage

### 1. 分析当日新闻

```bash
# 分析今日新闻（默认行为）
uv run python scripts/analyze_news.py

# 或使用 uv run（如果配置了脚本）
uv run analyze-news
```

### 2. 分析指定日期

```bash
uv run analyze-news --date 20250110
```

### 3. 查询分析结果

```bash
# 查询今日分析报告（文本格式）
uv run analyze-news query --date 20250110

# 查询并输出 JSON
uv run analyze-news query --date 20250110 --format json

# 查询并输出 Markdown
uv run analyze-news query --date 20250110 --format markdown
```

### 4. 列出所有分析报告

```bash
uv run analyze-news list

# 列出最近 10 条
uv run analyze-news list --limit 10
```

### 5. 对比分析结果

```bash
# 对比两天的市场情绪
uv run analyze-news compare --dates 20250109 20250110 --metric sentiment

# 对比多天的所有指标
uv run analyze-news compare --dates 20250108 20250109 20250110
```

### 6. 导出分析报告

```bash
# 导出为 JSON
uv run analyze-news export --date 20250110 --format json --output report.json

# 导出为 CSV
uv run analyze-news export --date 20250110 --format csv --output report.csv
```

## Integration with Existing System

### 方式 1: 手动调用

在新闻爬取完成后，手动运行分析：

```bash
# 1. 爬取新闻（现有 Node.js 脚本）
node index.js

# 2. 分析新闻（新增 Python 脚本）
cd llm-analysis
uv run analyze-news
```

### 方式 2: 自动化脚本

创建集成脚本 `scripts/daily-update.sh`:

```bash
#!/bin/bash
set -e

# 爬取新闻
echo "正在爬取新闻..."
node index.js

# 分析新闻
echo "正在分析新闻..."
cd llm-analysis
uv run analyze-news

echo "完成！"
```

### 方式 3: Cron 定时任务

设置每日定时任务（例如：每日 21:00 执行）：

```bash
# 编辑 crontab
crontab -e

# 添加任务（每日 21:00 执行）
0 21 * * * cd /path/to/xin-wen-lian-bo && ./scripts/daily-update.sh >> logs/daily-update.log 2>&1
```

## Project Structure

```
xin-wen-lian-bo/
├── llm-analysis/              # Python 分析模块
│   ├── pyproject.toml         # uv 项目配置
│   ├── uv.lock                # 依赖锁定文件
│   ├── .env                   # 环境变量（不提交到 Git）
│   ├── .env.example           # 环境变量示例
│   ├── src/
│   │   └── llm_analysis/      # 源代码
│   ├── tests/                 # 测试代码
│   └── scripts/
│       └── analyze_news.py    # CLI 入口
├── news/                      # 新闻文件（现有）
│   ├── YYYYMMDD.md
│   └── analysis/              # 分析结果（新增）
│       ├── index.json
│       └── YYYYMMDD.json
└── index.js                   # 现有爬虫脚本
```

## Testing

### 运行测试

```bash
cd llm-analysis

# 运行所有测试
uv run pytest

# 运行测试并显示覆盖率
uv run pytest --cov=src/llm_analysis --cov-report=html

# 运行特定测试文件
uv run pytest tests/unit/test_models.py
```

### Mock OpenAI API

测试使用 Mock，避免实际 API 调用：

```python
# tests/conftest.py
import pytest
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def mock_openai_client():
    client = MagicMock()
    client.chat.completions.create = AsyncMock(
        return_value=MagicMock(
            choices=[MagicMock(
                message=MagicMock(content='{"test": "data"}')
            )]
        )
    )
    return client
```

## Troubleshooting

### 问题 1: OpenAI API 密钥未设置

**错误信息**: `错误: 配置错误 - OPENAI_API_KEY 未设置`

**解决方法**:
1. 检查 `.env` 文件是否存在
2. 确认 `OPENAI_API_KEY` 已设置
3. 重新加载环境变量

### 问题 2: 新闻文件不存在

**错误信息**: `错误: 文件不存在 - news/20250110.md`

**解决方法**:
1. 确认新闻爬取脚本已运行
2. 检查日期格式是否正确（YYYYMMDD）
3. 确认文件路径正确

### 问题 3: API 调用超时

**错误信息**: `错误: API 错误 - 请求超时`

**解决方法**:
1. 检查网络连接
2. 增加超时时间（设置 `OPENAI_TIMEOUT`）
3. 检查 API 密钥是否有效
4. 检查 OpenAI API 服务状态

### 问题 4: JSON 解析错误

**错误信息**: `错误: 数据格式错误 - JSON 解析失败`

**解决方法**:
1. 检查分析结果文件是否损坏
2. 删除损坏的文件，重新分析
3. 检查 LLM 返回格式是否符合预期

## Next Steps

1. **阅读文档**:
   - [数据模型](./data-model.md) - 了解数据结构
   - [API 合约](./contracts/cli-interface.md) - 了解 CLI 接口
   - [研究文档](./research.md) - 了解技术决策

2. **运行示例**:
   - 使用示例数据测试分析功能
   - 验证输出格式

3. **集成到现有系统**:
   - 设置自动化脚本
   - 配置定时任务

4. **扩展功能**:
   - 添加更多分析指标
   - 优化 Prompt 设计
   - 添加缓存机制

## Support

如遇到问题，请检查：
1. 日志输出（使用 `--verbose` 选项）
2. 错误信息（使用 `--help` 查看帮助）
3. 文档和示例代码
