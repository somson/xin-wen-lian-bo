# Implementation Plan: LLM 新闻分析与股票推荐

**Branch**: `001-llm-news-analysis` | **Date**: 2025-01-10 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-llm-news-analysis/spec.md`

## Summary

实现一个使用 LLM（OpenAI）分析当日新闻联播内容的工具，自动提取市场情绪和经济发展趋势，并基于分析结果提供股票投资建议。系统将作为现有新闻爬取系统的扩展模块，使用 Python 3.12 和 uv 包管理器构建，通过 OpenAI API 进行文本分析，并将分析结果保存为结构化数据供用户查询和导出。

## Technical Context

**Language/Version**: Python 3.12  
**Primary Dependencies**: 
- `openai` - OpenAI API 客户端
- `pydantic` - 数据验证和设置管理
- `python-dotenv` - 环境变量管理
- `aiohttp` 或 `httpx` - 异步 HTTP 客户端（用于 OpenAI API 调用）
- `orjson` 或 `ujson` - 高性能 JSON 处理（可选）

**Storage**: 
- JSON 文件存储（与现有 `news/catalogue.json` 模式一致）
- 分析结果存储在 `news/analysis/YYYYMMDD.json` 格式
- 历史记录索引存储在 `news/analysis/index.json`

**Testing**: 
- `pytest` - 测试框架
- `pytest-asyncio` - 异步测试支持
- `pytest-mock` - Mock 和 Fixture 支持
- `pytest-cov` - 代码覆盖率

**Target Platform**: 
- Linux/macOS/Windows（命令行工具）
- 与现有 Node.js 爬虫系统集成

**Project Type**: Single project (CLI tool + library)

**Performance Goals**: 
- 单次分析请求完成时间 < 5 分钟（符合 SC-001）
- LLM API 调用超时处理 < 5 秒（符合 SC-005）
- 历史报告查询响应时间 < 3 秒（符合 SC-004）

**Constraints**: 
- 必须与现有 Node.js 项目共存
- 必须能够读取现有 `news/YYYYMMDD.md` 文件格式
- OpenAI API 调用必须包含错误处理和重试机制
- 必须支持中文文本分析
- 分析结果必须包含风险提示和免责声明

**Scale/Scope**: 
- 每日处理一次新闻分析（与新闻爬取频率一致）
- 保存至少 30 天历史记录
- 单用户使用（无并发用户需求）
- 预计代码规模：~2000-3000 LOC

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. 错误处理优先 ✅

- ✅ 所有 OpenAI API 调用必须包含 try-catch 和超时处理
- ✅ 文件读取操作必须处理文件不存在的情况
- ✅ JSON 解析必须处理格式错误
- ✅ 必须处理 LLM 服务不可用的情况（FR-009）

### II. 类型安全与输入验证 ✅

- ✅ 使用 Pydantic 进行数据模型验证
- ✅ 函数参数必须进行类型注解（Python type hints）
- ✅ 外部数据（新闻内容、API 响应）必须验证格式
- ✅ 日期格式验证（YYYYMMDD）

### III. 现代 Python 语法规范 ✅

- ✅ 使用 Python 3.12 特性（类型注解、async/await）
- ✅ 使用 `async/await` 进行异步操作
- ✅ 使用类型提示（Type Hints）
- ✅ 使用 f-strings 而非字符串拼接

### IV. 代码可读性与文档 ✅

- ✅ 所有公共函数必须包含 docstring（Google 或 NumPy 风格）
- ✅ 复杂逻辑必须有注释说明
- ✅ 使用有意义的函数和变量名
- ✅ 函数长度建议 < 50 行

### V. 异步操作最佳实践 ✅

- ✅ 使用 `async/await` 而非回调
- ✅ 所有异步操作包含错误处理
- ✅ 合理使用并发（如需要同时分析多条新闻）
- ✅ API 调用设置超时时间

### VI. 资源管理与清理 ✅

- ✅ 文件操作使用上下文管理器（`with` 语句）
- ✅ HTTP 连接正确关闭
- ✅ 避免内存泄漏（及时释放大对象）

### VII. 配置与常量管理 ✅

- ✅ 使用环境变量管理 API 密钥
- ✅ 将配置提取为常量或配置文件
- ✅ 使用 `python-dotenv` 管理环境变量

### VIII. 代码复用与模块化 ✅

- ✅ 按功能划分模块（models, services, cli）
- ✅ 通用工具函数放在独立模块
- ✅ 避免代码重复

### IX. 日志与调试 ✅

- ✅ 使用 Python `logging` 模块
- ✅ 区分日志级别（DEBUG, INFO, WARNING, ERROR）
- ✅ 记录关键操作和错误
- ✅ 不在日志中输出敏感信息（API 密钥）

### X. 测试与质量保证 ✅

- ✅ 核心函数包含单元测试
- ✅ 关键流程包含集成测试
- ✅ 测试覆盖率目标：关键路径 80%+

**Gate Status**: ✅ PASSED - 所有原则均符合要求

## Project Structure

### Documentation (this feature)

```text
specs/001-llm-news-analysis/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
# Python LLM 分析模块（与现有 Node.js 项目共存）
llm-analysis/
├── pyproject.toml       # uv 项目配置
├── uv.lock              # uv 锁定文件
├── .env.example         # 环境变量示例
├── README.md            # 模块说明文档
├── src/
│   └── llm_analysis/
│       ├── __init__.py
│       ├── models/              # 数据模型
│       │   ├── __init__.py
│       │   ├── analysis.py      # 分析报告模型
│       │   ├── sentiment.py     # 市场情绪模型
│       │   ├── trend.py         # 发展趋势模型
│       │   └── recommendation.py # 推荐建议模型
│       ├── services/            # 业务逻辑
│       │   ├── __init__.py
│       │   ├── news_reader.py   # 新闻内容读取
│       │   ├── llm_client.py    # OpenAI API 客户端
│       │   ├── analyzer.py      # 分析服务
│       │   ├── sentiment_analyzer.py  # 情绪分析
│       │   ├── trend_analyzer.py       # 趋势分析
│       │   └── recommendation_engine.py # 推荐引擎
│       ├── storage/             # 数据存储
│       │   ├── __init__.py
│       │   ├── file_storage.py  # 文件存储实现
│       │   └── index_manager.py # 索引管理
│       └── utils/               # 工具函数
│           ├── __init__.py
│           ├── date_utils.py    # 日期工具
│           ├── text_utils.py    # 文本处理工具
│           └── validators.py   # 验证工具
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # pytest 配置
│   ├── unit/                    # 单元测试
│   │   ├── test_models.py
│   │   ├── test_services.py
│   │   └── test_utils.py
│   ├── integration/             # 集成测试
│   │   ├── test_analyzer.py
│   │   └── test_storage.py
│   └── contract/                # 合约测试
│       └── test_openai_api.py
└── scripts/
    └── analyze_news.py          # CLI 入口脚本

# 现有 Node.js 项目结构保持不变
news/
├── YYYYMMDD.md                 # 新闻文件（现有）
├── catalogue.json              # 目录索引（现有）
└── analysis/                   # 新增：分析结果目录
    ├── index.json              # 分析记录索引
    └── YYYYMMDD.json           # 每日分析结果
```

**Structure Decision**: 
采用单项目结构，Python 模块作为独立目录 `llm-analysis/` 与现有 Node.js 项目共存。使用 uv 管理 Python 依赖，通过 CLI 脚本与现有系统集成。分析结果存储在 `news/analysis/` 目录下，保持与现有 `news/` 目录结构的一致性。

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |

## Phase 0: Research Complete ✅

所有技术决策已在 `research.md` 中记录：
- ✅ Python 3.12 + uv 包管理器选择
- ✅ OpenAI API 集成方案
- ✅ JSON 文件存储策略
- ✅ Pydantic 数据验证
- ✅ 异步编程模型
- ✅ 与现有系统集成模式

## Phase 1: Design Complete ✅

### Data Model ✅
- ✅ `data-model.md` 已创建
- ✅ 定义了所有核心实体（NewsAnalysisReport, MarketSentiment, EconomicTrends, StockRecommendation, AnalysisIndex）
- ✅ 包含验证规则、数据流、状态转换

### API Contracts ✅
- ✅ `contracts/cli-interface.md` 已创建
- ✅ 定义了所有 CLI 命令（analyze, query, list, compare, export）
- ✅ 包含参数、行为、退出码、错误处理规范

### Quick Start Guide ✅
- ✅ `quickstart.md` 已创建
- ✅ 包含安装、配置、基本使用、集成指南
- ✅ 包含故障排除和下一步建议

## Next Steps

1. **运行 `/speckit.tasks`**: 将计划分解为具体任务
2. **实现代码**: 根据任务列表开始实现
3. **测试**: 编写并运行测试
4. **集成**: 与现有系统集成

## Generated Artifacts

- ✅ `plan.md` - 实现计划（本文档）
- ✅ `research.md` - 技术研究和决策
- ✅ `data-model.md` - 数据模型定义
- ✅ `contracts/cli-interface.md` - CLI 接口规范
- ✅ `quickstart.md` - 快速开始指南

所有 Phase 1 设计文档已完成，准备进入 Phase 2（任务分解）。
