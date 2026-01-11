# LLM 新闻分析工具

使用 LLM（OpenAI）分析新闻联播内容，提取市场情绪和经济发展趋势，并生成股票投资建议。

## 功能特性

- 📰 自动读取新闻联播 Markdown 文件
- 🤖 使用 LLM 分析市场情绪和经济发展趋势
- 📊 生成结构化的分析报告
- 💡 基于分析结果提供股票推荐建议
- 📈 支持历史记录查询和趋势对比
- 📤 导出分析结果为多种格式（JSON、CSV、Markdown）
- 📱 支持飞书 Webhook 通知
- 📁 将分析结果保存到 results 文件夹

## 安装

### 前置要求

- Python 3.12+
- uv 包管理器

### 安装步骤

```bash
# 安装 uv（如果未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 进入项目目录
cd llm-analysis

# 安装依赖
uv sync

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，设置 OPENAI_API_KEY 和 FEISHU_WEBHOOK_URL
```

## 使用方法

### 分析当日新闻

```bash
# 从项目根目录运行
python analyze_news.py

# 或使用 uv
uv run python analyze_news.py
```

### 分析指定日期

```bash
python analyze_news.py --date 20250110
```

### 查询分析结果

```bash
# 查询文本格式
python analyze_news.py query --date 20250110

# 查询 JSON 格式
python analyze_news.py query --date 20250110 --format json
```

### 列出所有分析记录

```bash
python analyze_news.py list
```

### 对比分析结果

```bash
python analyze_news.py compare --dates 20250109 20250110
```

### 导出分析报告

```bash
python analyze_news.py export --date 20250110 --format json --output report.json
```

## 配置说明

在 `.env` 文件中配置以下环境变量：

- `OPENAI_API_KEY`: OpenAI API 密钥（必需）
- `OPENAI_MODEL`: 使用的模型，默认 `gpt-3.5-turbo`
- `OPENAI_TIMEOUT`: API 超时时间（秒），默认 300
- `ANALYSIS_DIR`: 分析结果存储目录，默认 `../news/analysis`
- `NEWS_DIR`: 新闻文件目录，默认 `../news`
- `RESULTS_DIR`: 结果文件目录，默认 `../results`
- `FEISHU_WEBHOOK_URL`: 飞书 Webhook URL（可选）
- `FEISHU_ENABLED`: 是否启用飞书通知，默认 `false`

## 项目结构

```
llm-analysis/
├── src/llm_analysis/      # 源代码
│   ├── models/            # 数据模型
│   ├── services/          # 业务逻辑
│   ├── storage/          # 数据存储
│   └── utils/            # 工具函数
├── tests/                # 测试代码
├── scripts/              # CLI 脚本
└── pyproject.toml       # 项目配置
```

## 开发

### 运行测试

```bash
uv run pytest
```

### 代码覆盖率

```bash
uv run pytest --cov=src/llm_analysis --cov-report=html
```

## 许可证

ISC
