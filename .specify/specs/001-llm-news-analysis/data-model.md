# Data Model: LLM 新闻分析与股票推荐

**Feature**: 001-llm-news-analysis  
**Date**: 2025-01-10

## Overview

本文档定义 LLM 新闻分析系统的数据模型。所有模型使用 Pydantic 实现，提供类型验证和序列化功能。

## Core Entities

### 1. NewsAnalysisReport (新闻分析报告)

**Purpose**: 表示单日的完整分析报告，包含市场情绪、发展趋势和推荐建议。

**Fields**:
- `date: str` - 日期，格式 YYYYMMDD（如 "20250110"）
- `sentiment: MarketSentiment` - 市场情绪分析
- `trends: EconomicTrends` - 经济发展趋势分析
- `recommendations: List[StockRecommendation]` - 股票推荐建议列表
- `key_news_summaries: List[str]` - 关键新闻摘要列表
- `generated_at: datetime` - 生成时间戳
- `analysis_version: str` - 分析版本号（用于追踪模型变更）

**Validation Rules**:
- `date` 必须匹配 YYYYMMDD 格式
- `generated_at` 必须为有效的 datetime
- `recommendations` 列表不能为空（至少包含风险提示）

**Storage**: `news/analysis/YYYYMMDD.json`

**Example**:
```json
{
  "date": "20250110",
  "sentiment": {
    "score": 75,
    "category": "积极",
    "intensity": "高",
    "key_news": ["政策利好", "经济增长"]
  },
  "trends": {
    "summary": "整体向好",
    "policies": ["减税政策"],
    "industries": ["新能源", "科技"],
    "indicators": ["GDP增长", "消费回升"]
  },
  "recommendations": [
    {
      "industry": "新能源",
      "reason": "政策支持",
      "risk_level": "中",
      "disclaimer": "投资有风险，仅供参考"
    }
  ],
  "key_news_summaries": ["政策利好新能源发展"],
  "generated_at": "2025-01-10T20:30:00Z",
  "analysis_version": "1.0.0"
}
```

### 2. MarketSentiment (市场情绪分析)

**Purpose**: 表示市场情绪的分析结果。

**Fields**:
- `score: int` - 情绪评分，范围 0-100（0=极度消极，50=中性，100=极度积极）
- `category: Literal["积极", "中性", "消极"]` - 情绪分类
- `intensity: Literal["低", "中", "高"]` - 情绪强度
- `key_news: List[str]` - 支持该情绪判断的关键新闻标题或摘要

**Validation Rules**:
- `score` 必须在 0-100 范围内
- `category` 必须为三个值之一
- `key_news` 列表不能为空

**Relationships**:
- 属于 `NewsAnalysisReport`

### 3. EconomicTrends (经济发展趋势分析)

**Purpose**: 表示经济发展趋势的分析结果。

**Fields**:
- `summary: str` - 趋势总结（200字以内）
- `policies: List[str]` - 关键政策方向列表
- `industries: List[str]` - 热点行业列表
- `indicators: List[str]` - 宏观经济指标变化
- `key_news: List[str]` - 支持该趋势的关键新闻引用

**Validation Rules**:
- `summary` 不能为空，长度不超过 200 字
- `policies`, `industries`, `indicators` 至少有一个非空列表
- `key_news` 列表不能为空

**Relationships**:
- 属于 `NewsAnalysisReport`

### 4. StockRecommendation (股票推荐建议)

**Purpose**: 表示基于分析的股票或行业推荐建议。

**Fields**:
- `industry: str` - 推荐关注的行业（如 "新能源"、"科技"）
- `reason: str` - 推荐理由（200字以内）
- `related_news: List[str]` - 相关新闻摘要
- `risk_level: Literal["低", "中", "高"]` - 风险等级
- `disclaimer: str` - 风险提示和免责声明（固定文本）
- `recommended_at: datetime` - 推荐时间戳

**Validation Rules**:
- `industry` 不能为空
- `reason` 不能为空，长度不超过 200 字
- `risk_level` 必须为三个值之一
- `disclaimer` 必须包含风险提示文本

**Relationships**:
- 属于 `NewsAnalysisReport`（多对一）

### 5. AnalysisIndex (分析索引)

**Purpose**: 管理分析记录的索引，便于快速查询。

**Fields**:
- `dates: List[str]` - 已分析的日期列表（按日期排序）
- `latest: str` - 最新分析日期
- `updated_at: datetime` - 索引更新时间

**Validation Rules**:
- `dates` 列表必须按日期升序排列
- `latest` 必须存在于 `dates` 列表中
- `dates` 列表不能为空（至少有一个日期）

**Storage**: `news/analysis/index.json`

**Example**:
```json
{
  "dates": ["20250108", "20250109", "20250110"],
  "latest": "20250110",
  "updated_at": "2025-01-10T20:30:00Z"
}
```

## Data Flow

### 1. 分析流程

```
News Markdown File (news/YYYYMMDD.md)
    ↓
NewsReader Service (解析 Markdown)
    ↓
LLM Analyzer Service (调用 OpenAI API)
    ↓
NewsAnalysisReport (Pydantic Model)
    ↓
FileStorage Service (保存为 JSON)
    ↓
AnalysisIndex (更新索引)
```

### 2. 查询流程

```
User Request (日期)
    ↓
AnalysisIndex (查找日期)
    ↓
FileStorage Service (读取 JSON)
    ↓
NewsAnalysisReport (Pydantic Model)
    ↓
Return to User
```

## State Transitions

### AnalysisReport States

1. **Pending** - 分析请求已创建，等待处理
2. **Processing** - 正在调用 LLM API 进行分析
3. **Completed** - 分析完成，结果已保存
4. **Failed** - 分析失败（API 错误、超时等）

**Note**: 当前实现不显式存储状态，通过文件存在性判断（文件存在=Completed，不存在=Pending/Failed）。

## Validation Rules Summary

### Date Format
- 所有日期字段必须匹配 `YYYYMMDD` 格式
- 使用正则表达式验证：`^\d{8}$`

### Text Length Limits
- `summary`: 最大 200 字
- `reason`: 最大 200 字
- `key_news` 列表项：最大 100 字

### Numeric Ranges
- `sentiment.score`: 0-100（整数）

### Required Fields
- `NewsAnalysisReport`: date, sentiment, trends, recommendations, generated_at
- `MarketSentiment`: score, category, intensity, key_news
- `EconomicTrends`: summary, key_news（至少一个列表非空）
- `StockRecommendation`: industry, reason, risk_level, disclaimer

## Data Migration Considerations

### Version Compatibility
- `analysis_version` 字段用于追踪模型版本
- 未来模型更新时，可以识别旧版本数据
- 支持数据迁移脚本（如需要）

### Backward Compatibility
- 新增字段使用可选类型（Optional）
- 保持现有字段不变
- 版本号递增策略：主版本.次版本.修订版本

## Error Handling

### Invalid Data Scenarios
1. **JSON 格式错误**: 捕获 JSONDecodeError，返回明确的错误信息
2. **字段缺失**: Pydantic 自动验证，抛出 ValidationError
3. **类型错误**: Pydantic 自动转换或抛出错误
4. **日期格式错误**: 自定义验证器检查格式

### Data Recovery
- 索引文件损坏：重新扫描 `analysis/` 目录重建索引
- 单日分析文件损坏：标记为失败，允许重新分析
- 数据不一致：验证工具检查并修复
