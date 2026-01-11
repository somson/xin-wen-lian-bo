# CLI Interface Contract: LLM 新闻分析工具

**Feature**: 001-llm-news-analysis  
**Date**: 2025-01-10

## Overview

本文档定义 LLM 新闻分析工具的 CLI（命令行接口）规范。由于这是一个命令行工具而非 Web API，接口通过命令行参数和退出码定义。

## Entry Point

**Script**: `scripts/analyze_news.py`

**Execution**: 
```bash
python -m llm_analysis.scripts.analyze_news [OPTIONS]
# 或
uv run analyze-news [OPTIONS]
```

## Commands

### 1. analyze (默认命令)

分析指定日期的新闻内容，生成分析报告。

**Usage**:
```bash
analyze-news [--date DATE] [--force]
```

**Parameters**:
- `--date DATE` (可选): 日期，格式 YYYYMMDD。默认值为当日日期。
- `--force` (可选): 强制重新分析，即使分析结果已存在。

**Behavior**:
1. 读取 `news/DATE.md` 文件
2. 调用 LLM API 进行分析
3. 生成分析报告
4. 保存到 `news/analysis/DATE.json`
5. 更新索引文件

**Exit Codes**:
- `0`: 成功
- `1`: 一般错误（文件不存在、API 错误等）
- `2`: 配置错误（API 密钥未设置等）

**Output**:
- 成功：输出分析报告摘要到 stdout
- 错误：输出错误信息到 stderr

**Example**:
```bash
# 分析今日新闻
analyze-news

# 分析指定日期
analyze-news --date 20250110

# 强制重新分析
analyze-news --date 20250110 --force
```

### 2. query

查询指定日期的分析报告。

**Usage**:
```bash
analyze-news query --date DATE [--format FORMAT]
```

**Parameters**:
- `--date DATE` (必需): 日期，格式 YYYYMMDD
- `--format FORMAT` (可选): 输出格式，可选值：`json`, `markdown`, `text`。默认值为 `text`。

**Behavior**:
1. 读取 `news/analysis/DATE.json` 文件
2. 解析 JSON 数据
3. 按指定格式输出到 stdout

**Exit Codes**:
- `0`: 成功
- `1`: 分析报告不存在
- `2`: 文件读取错误

**Example**:
```bash
# 查询今日分析报告（文本格式）
analyze-news query --date 20250110

# 查询并输出 JSON
analyze-news query --date 20250110 --format json

# 查询并输出 Markdown
analyze-news query --date 20250110 --format markdown
```

### 3. list

列出所有可用的分析报告日期。

**Usage**:
```bash
analyze-news list [--limit N]
```

**Parameters**:
- `--limit N` (可选): 限制返回数量，默认返回所有。

**Behavior**:
1. 读取 `news/analysis/index.json` 文件
2. 列出所有日期（按日期降序）
3. 输出到 stdout

**Exit Codes**:
- `0`: 成功
- `1`: 索引文件不存在或损坏

**Example**:
```bash
# 列出所有分析报告
analyze-news list

# 列出最近 10 条
analyze-news list --limit 10
```

### 4. compare

对比多个日期的分析结果。

**Usage**:
```bash
analyze-news compare --dates DATE1 DATE2 [DATE3 ...] [--metric METRIC]
```

**Parameters**:
- `--dates DATE1 DATE2 ...` (必需): 要对比的日期列表，至少两个日期
- `--metric METRIC` (可选): 对比指标，可选值：`sentiment`, `trends`, `all`。默认值为 `all`。

**Behavior**:
1. 读取所有指定日期的分析报告
2. 对比指定指标
3. 输出对比结果到 stdout

**Exit Codes**:
- `0`: 成功
- `1`: 某个日期的分析报告不存在
- `2`: 参数错误（日期少于两个）

**Example**:
```bash
# 对比两天的市场情绪
analyze-news compare --dates 20250109 20250110 --metric sentiment

# 对比多天的所有指标
analyze-news compare --dates 20250108 20250109 20250110
```

### 5. export

导出分析报告为指定格式。

**Usage**:
```bash
analyze-news export --date DATE --format FORMAT [--output FILE]
```

**Parameters**:
- `--date DATE` (必需): 日期，格式 YYYYMMDD
- `--format FORMAT` (必需): 导出格式，可选值：`json`, `csv`, `markdown`
- `--output FILE` (可选): 输出文件路径。默认输出到 stdout。

**Behavior**:
1. 读取分析报告
2. 转换为指定格式
3. 写入文件或输出到 stdout

**Exit Codes**:
- `0`: 成功
- `1`: 分析报告不存在
- `2`: 格式不支持或转换错误

**Example**:
```bash
# 导出为 JSON
analyze-news export --date 20250110 --format json --output report.json

# 导出为 CSV（输出到 stdout）
analyze-news export --date 20250110 --format csv
```

## Common Options

所有命令支持以下通用选项：

- `--verbose` / `-v`: 启用详细输出（DEBUG 级别日志）
- `--quiet` / `-q`: 静默模式（仅输出错误）
- `--config FILE`: 指定配置文件路径（默认：`.env`）
- `--help` / `-h`: 显示帮助信息

## Environment Variables

- `OPENAI_API_KEY` (必需): OpenAI API 密钥
- `OPENAI_MODEL` (可选): 使用的模型，默认值：`gpt-3.5-turbo`
- `OPENAI_TIMEOUT` (可选): API 超时时间（秒），默认值：300
- `ANALYSIS_DIR` (可选): 分析结果目录，默认值：`news/analysis`
- `NEWS_DIR` (可选): 新闻文件目录，默认值：`news`

## Error Messages

所有错误消息使用中文，格式统一：

```
错误: [错误类型] - [详细描述]
```

**错误类型**:
- `文件不存在`: 指定的文件不存在
- `API 错误`: OpenAI API 调用失败
- `配置错误`: 环境变量或配置缺失
- `数据格式错误`: JSON 解析或验证失败
- `参数错误`: 命令行参数无效

## Output Format

### Text Format (默认)

```
《新闻联播》分析报告 - 20250110

市场情绪: 积极 (评分: 75/100)
- 关键新闻: [新闻摘要1], [新闻摘要2]

经济发展趋势:
- 政策方向: [政策1], [政策2]
- 热点行业: [行业1], [行业2]
- 经济指标: [指标1], [指标2]

推荐建议:
1. [行业] - [理由]
   风险等级: [低/中/高]
   免责声明: 投资有风险，仅供参考

生成时间: 2025-01-10 20:30:00
```

### JSON Format

```json
{
  "date": "20250110",
  "sentiment": { ... },
  "trends": { ... },
  "recommendations": [ ... ],
  "generated_at": "2025-01-10T20:30:00Z"
}
```

### Markdown Format

```markdown
# 《新闻联播》分析报告 - 20250110

## 市场情绪

**评分**: 75/100  
**分类**: 积极  
**强度**: 高

### 关键新闻
- [新闻摘要1]
- [新闻摘要2]

## 经济发展趋势

### 政策方向
- [政策1]
- [政策2]

...
```

## Testing Contract

### Unit Tests

每个命令必须包含单元测试，验证：
- 参数解析正确性
- 错误处理正确性
- 输出格式正确性

### Integration Tests

集成测试验证：
- 完整命令执行流程
- 文件读写操作
- API 调用（使用 Mock）

## Versioning

CLI 接口版本通过 `--version` 选项查看：

```bash
analyze-news --version
# 输出: analyze-news 1.0.0
```

版本号遵循语义化版本（Semantic Versioning）：
- 主版本号：不兼容的 API 修改
- 次版本号：向下兼容的功能性新增
- 修订号：向下兼容的问题修正
