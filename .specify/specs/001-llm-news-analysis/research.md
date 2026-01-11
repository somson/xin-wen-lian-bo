# Research & Design Decisions: LLM 新闻分析与股票推荐

**Feature**: 001-llm-news-analysis  
**Date**: 2025-01-10

## Technology Choices

### Decision 1: Python 3.12 + uv 包管理器

**Decision**: 使用 Python 3.12 作为实现语言，uv 作为包管理工具。

**Rationale**:
- Python 3.12 提供最新的类型注解和异步特性支持
- uv 是现代化的 Python 包管理器，速度快，依赖解析准确
- Python 生态对 LLM API 调用有良好的支持（OpenAI SDK）
- 与现有 Node.js 项目可以很好地共存（通过文件系统交互）

**Alternatives Considered**:
- **Node.js**: 现有项目使用 Node.js，但 LLM SDK 支持不如 Python 丰富
- **Go/Rust**: 性能更好，但开发效率和生态支持不如 Python
- **pip/poetry**: 传统包管理器，uv 更现代且快速

### Decision 2: OpenAI API 作为 LLM 服务提供商

**Decision**: 使用 OpenAI API（GPT-4 或 GPT-3.5-turbo）进行文本分析。

**Rationale**:
- OpenAI API 对中文支持良好
- API 稳定，文档完善
- 支持结构化输出（JSON mode）
- 有完善的 Python SDK
- 符合用户指定的技术栈要求

**Alternatives Considered**:
- **Claude API**: 性能优秀，但 API 稳定性略逊于 OpenAI
- **本地 LLM**: 无需 API 费用，但需要大量计算资源，部署复杂
- **其他云服务**: 如阿里云、腾讯云，但中文金融领域分析能力待验证

**Implementation Notes**:
- 使用 `openai` Python SDK（官方推荐）
- 配置 API 密钥通过环境变量（`.env` 文件）
- 实现重试机制和错误处理
- 使用 JSON mode 确保结构化输出

### Decision 3: JSON 文件存储

**Decision**: 使用 JSON 文件存储分析结果，而非数据库。

**Rationale**:
- 与现有项目存储方式一致（`catalogue.json`）
- 简单易维护，无需额外数据库服务
- 适合单用户、低并发场景
- 易于版本控制和备份
- 数据量小（每日一条记录，30天约30条）

**Alternatives Considered**:
- **SQLite**: 更适合复杂查询，但增加复杂度
- **PostgreSQL/MySQL**: 过度设计，当前需求不需要
- **MongoDB**: 文档数据库，但增加部署复杂度

**Storage Structure**:
```
news/analysis/
├── index.json          # 索引文件：{ "dates": ["20250110", ...], "latest": "20250110" }
└── 20250110.json       # 单日分析结果
```

### Decision 4: Pydantic 数据验证

**Decision**: 使用 Pydantic 进行数据模型定义和验证。

**Rationale**:
- 提供类型安全的数据模型
- 自动数据验证和序列化
- 与 Python 类型提示完美集成
- 符合 Constitution 原则 II（类型安全）
- 支持 JSON Schema 生成（可用于 API 文档）

**Alternatives Considered**:
- **dataclasses**: 标准库，但缺少验证功能
- **attrs**: 功能类似，但 Pydantic 更流行
- **手动验证**: 不符合代码质量原则

### Decision 5: 异步编程模型

**Decision**: 使用 `async/await` 进行异步编程。

**Rationale**:
- OpenAI API 调用是 I/O 密集型操作，异步可以提高效率
- 符合 Constitution 原则 V（异步操作最佳实践）
- Python 3.12 对异步支持完善
- 支持并发处理（如需要同时分析多条新闻）

**Implementation**:
- 使用 `aiohttp` 或 `httpx` 进行异步 HTTP 请求
- OpenAI SDK 支持异步调用
- 使用 `asyncio` 管理异步任务

## Integration Patterns

### Pattern 1: 与现有 Node.js 系统集成

**Approach**: 通过文件系统交互，Python 模块读取 Node.js 生成的 Markdown 文件。

**Rationale**:
- 最小化系统耦合
- 两个系统可以独立运行和测试
- 通过文件系统作为数据交换接口
- 符合微服务架构思想

**Implementation**:
- Python 脚本读取 `news/YYYYMMDD.md` 文件
- 解析 Markdown 内容
- 生成分析结果写入 `news/analysis/YYYYMMDD.json`
- Node.js 系统可以读取 JSON 结果（如需要）

### Pattern 2: LLM Prompt 设计

**Approach**: 使用结构化 Prompt，要求 LLM 返回 JSON 格式结果。

**Rationale**:
- 确保输出格式一致
- 便于解析和验证
- 减少后处理工作
- 提高可靠性

**Prompt Structure**:
1. **角色定义**: 定义 LLM 为金融分析师
2. **任务描述**: 分析新闻内容，提取市场情绪和趋势
3. **输出格式**: 指定 JSON Schema
4. **示例**: 提供示例输出（few-shot learning）
5. **约束**: 强调风险提示和免责声明

### Pattern 3: 错误处理和重试机制

**Approach**: 实现指数退避重试，设置超时时间。

**Rationale**:
- API 调用可能失败（网络、限流等）
- 符合 Constitution 原则 I（错误处理优先）
- 提高系统可靠性

**Implementation**:
- 最大重试次数：3次
- 重试间隔：指数退避（1s, 2s, 4s）
- 超时时间：300秒（5分钟）
- 错误分类：网络错误、API 错误、超时错误

## Best Practices

### Practice 1: 环境变量管理

- 使用 `python-dotenv` 加载 `.env` 文件
- 提供 `.env.example` 模板
- 不在代码中硬编码 API 密钥
- 使用 Pydantic Settings 管理配置

### Practice 2: 日志记录

- 使用 Python `logging` 模块
- 区分日志级别（DEBUG, INFO, WARNING, ERROR）
- 记录关键操作（分析开始、完成、失败）
- 不在日志中输出敏感信息

### Practice 3: 测试策略

- 单元测试：测试各个服务模块
- 集成测试：测试完整分析流程
- Mock OpenAI API：避免实际 API 调用
- 使用 pytest fixtures 管理测试数据

### Practice 4: 代码组织

- 按功能划分模块（models, services, storage）
- 单一职责原则
- 依赖注入（便于测试）
- 接口抽象（便于替换实现）

## Open Questions Resolved

### Q1: 如何处理超长新闻内容？

**Answer**: 
- 使用 OpenAI API 的上下文窗口限制（GPT-4: 128k tokens）
- 如果内容过长，进行分块处理
- 先提取关键信息，再进行分析
- 或使用摘要功能先压缩内容

### Q2: 分析结果如何与现有系统集成？

**Answer**:
- 通过 JSON 文件存储，现有系统可以读取
- 如果需要 Web 界面，可以扩展 `index.html` 读取分析结果
- 保持向后兼容，不影响现有功能

### Q3: 如何处理 API 费用？

**Answer**:
- 每日仅分析一次，成本可控
- 使用 GPT-3.5-turbo 降低成本（如 GPT-4 太贵）
- 实现缓存机制，避免重复分析
- 监控 API 使用量

## References

- [OpenAI Python SDK Documentation](https://github.com/openai/openai-python)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [uv Package Manager](https://github.com/astral-sh/uv)
- [Python asyncio Best Practices](https://docs.python.org/3/library/asyncio.html)
