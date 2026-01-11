# 新闻联播项目代码质量原则 (Constitution)

## 核心原则

### I. 错误处理优先 (Error Handling First)

**必须遵守**: 所有异步操作、文件操作、网络请求必须包含完整的错误处理机制。

- **网络请求**: 必须捕获并处理网络错误、超时、HTTP 错误状态码
- **文件操作**: 必须处理文件不存在、权限不足、磁盘空间不足等异常
- **DOM 操作**: 必须验证 DOM 元素存在性，避免 `null` 引用错误
- **JSON 解析**: 必须处理无效 JSON 格式，提供默认值或错误信息
- **错误传播**: 使用 `try-catch` 或 Promise `.catch()`，避免未捕获的异常

**反例**:
```javascript
// ❌ 错误：缺少错误处理
const abstract = dom.window.document.querySelector('selector').innerHTML;

// ✅ 正确：包含错误处理
const element = dom.window.document.querySelector('selector');
if (!element) {
  throw new Error('无法找到摘要元素');
}
const abstract = element.innerHTML;
```

### II. 类型安全与输入验证 (Type Safety & Input Validation)

**必须遵守**: 所有函数参数和外部数据必须进行类型检查和验证。

- **参数验证**: 函数入口必须验证参数类型、范围、必需性
- **外部数据**: 从网络、文件、用户输入获取的数据必须验证格式
- **默认值**: 为可选参数提供合理的默认值
- **类型转换**: 显式类型转换，避免隐式转换导致的错误
- **边界检查**: 数组访问、字符串操作前检查边界

**反例**:
```javascript
// ❌ 错误：缺少类型检查
const readFile = path => {
  return new Promise((resolve, reject) => {
    fs.readFile(path, {}, (err, data) => {
      if (err) reject(err);
      resolve(data);
    });
  });
};

// ✅ 正确：包含类型验证
const readFile = (path) => {
  if (typeof path !== 'string' || path.trim() === '') {
    return Promise.reject(new TypeError('路径必须是非空字符串'));
  }
  return new Promise((resolve, reject) => {
    fs.readFile(path, { encoding: 'utf8' }, (err, data) => {
      if (err) reject(err);
      resolve(data);
    });
  });
};
```

### III. 现代 JavaScript 语法规范 (Modern JavaScript Standards)

**必须遵守**: 使用 ES6+ 语法，避免过时的 JavaScript 特性。

- **变量声明**: 优先使用 `const`，需要重新赋值时使用 `let`，禁止使用 `var`
- **箭头函数**: 优先使用箭头函数，保持上下文一致性
- **模板字符串**: 使用模板字符串替代字符串拼接
- **解构赋值**: 使用解构赋值简化对象和数组操作
- **可选链**: 使用可选链操作符 `?.` 安全访问嵌套属性
- **空值合并**: 使用 `??` 提供默认值

**反例**:
```javascript
// ❌ 错误：使用 var 和字符串拼接
var links = [];
let mdNews = '';
mdNews += '### ' + title + '\n\n' + content + '\n\n';

// ✅ 正确：使用 const 和模板字符串
const links = [];
let mdNews = '';
mdNews += `### ${title}\n\n${content}\n\n`;
```

### IV. 代码可读性与文档 (Code Readability & Documentation)

**必须遵守**: 代码必须清晰易读，关键逻辑必须有注释说明。

- **函数命名**: 使用描述性的函数名，动词开头（如 `get`, `save`, `update`）
- **变量命名**: 使用有意义的变量名，避免单字母变量（循环计数器除外）
- **JSDoc 注释**: 所有公共函数必须包含 JSDoc 注释，说明参数、返回值、异常
- **复杂逻辑**: 复杂算法和业务逻辑必须有行内注释说明
- **代码组织**: 相关功能组织在一起，避免过长的函数（建议 < 50 行）

**示例**:
```javascript
/**
 * 获取新闻列表
 * @param {string|number} date - 日期，格式为 YYYYMMDD
 * @returns {Promise<{abstract: string, news: string[]}>} 包含摘要链接和新闻链接数组的对象
 * @throws {Error} 当网络请求失败或日期格式无效时抛出错误
 */
const getNewsList = async (date) => {
  // 实现...
};
```

### V. 异步操作最佳实践 (Async/Await Best Practices)

**必须遵守**: 正确处理异步操作，避免回调地狱和未处理的 Promise。

- **优先使用 async/await**: 优先使用 `async/await` 而非 Promise 链
- **错误处理**: 所有 `await` 调用必须包含在 `try-catch` 中
- **并发控制**: 合理使用 `Promise.all()` 进行并发操作，注意错误处理
- **避免嵌套**: 避免深层嵌套的异步操作
- **超时控制**: 网络请求必须设置超时时间

**反例**:
```javascript
// ❌ 错误：未处理的 Promise 和嵌套回调
const newsList = await getNewsList(DATE);
const abstract = await getAbstract(newsList.abstract);
const news = await getNews(newsList.news);

// ✅ 正确：包含错误处理
try {
  const newsList = await getNewsList(DATE);
  const abstract = await getAbstract(newsList.abstract);
  const news = await getNews(newsList.news);
  // 处理结果...
} catch (error) {
  console.error('获取新闻失败:', error);
  process.exit(1);
}
```

### VI. 资源管理与清理 (Resource Management)

**必须遵守**: 合理管理资源，避免内存泄漏和资源浪费。

- **文件句柄**: 使用 `fs.promises` 或确保文件操作完成后关闭句柄
- **网络连接**: 确保 HTTP 请求正确关闭
- **内存使用**: 避免在循环中创建大量对象，及时释放不需要的引用
- **临时文件**: 清理临时文件和目录
- **错误恢复**: 操作失败时清理已创建的资源

### VII. 配置与常量管理 (Configuration & Constants)

**必须遵守**: 将配置和常量集中管理，避免硬编码。

- **魔法数字/字符串**: 将魔法数字和字符串提取为命名常量
- **配置文件**: 使用配置文件或环境变量管理配置
- **路径管理**: 使用 `path` 模块处理文件路径，避免字符串拼接
- **URL 管理**: 将 API URL 和端点提取为常量

**反例**:
```javascript
// ❌ 错误：硬编码的 URL 和选择器
const HTML = await fetch(`http://tv.cctv.com/lm/xwlb/day/${date}.shtml`);
const title = dom.window.document.querySelector('#page_body > div.allcontent > div.video18847 > div.playingVideo > div.tit');

// ✅ 正确：提取为常量
const BASE_URL = 'http://tv.cctv.com/lm/xwlb/day';
const SELECTORS = {
  TITLE: '#page_body > div.allcontent > div.video18847 > div.playingVideo > div.tit',
  CONTENT: '#content_area'
};
const HTML = await fetch(`${BASE_URL}/${date}.shtml`);
const title = dom.window.document.querySelector(SELECTORS.TITLE);
```

### VIII. 代码复用与模块化 (Code Reusability & Modularity)

**必须遵守**: 遵循 DRY（Don't Repeat Yourself）原则，提高代码复用性。

- **函数提取**: 重复的逻辑提取为独立函数
- **模块划分**: 按功能划分模块，保持模块职责单一
- **工具函数**: 通用工具函数放在独立的工具模块中
- **避免重复**: 相同或相似的代码块必须提取为函数

### IX. 日志与调试 (Logging & Debugging)

**必须遵守**: 提供适当的日志输出，便于调试和监控。

- **日志级别**: 区分不同日志级别（debug, info, warn, error）
- **结构化日志**: 使用结构化日志格式，包含上下文信息
- **敏感信息**: 避免在日志中输出敏感信息（密码、token 等）
- **生产环境**: 生产环境减少详细日志，保留关键操作日志
- **错误日志**: 错误必须记录完整的堆栈信息

**示例**:
```javascript
// ✅ 正确：结构化日志
console.log('[INFO]', { action: '获取新闻列表', date: DATE });
console.error('[ERROR]', { action: '获取新闻失败', error: error.message, stack: error.stack });
```

### X. 测试与质量保证 (Testing & Quality Assurance)

**必须遵守**: 关键功能必须包含测试，确保代码质量。

- **单元测试**: 核心函数必须包含单元测试
- **集成测试**: 关键流程必须包含集成测试
- **错误场景**: 测试必须包含正常流程和错误场景
- **测试覆盖率**: 关键路径测试覆盖率应达到 80% 以上
- **测试可维护性**: 测试代码必须清晰易读，便于维护

## 代码审查检查清单

在提交代码前，必须检查以下项目：

- [ ] 所有异步操作包含错误处理
- [ ] 所有函数参数包含类型验证
- [ ] 使用 `const`/`let` 而非 `var`
- [ ] 所有公共函数包含 JSDoc 注释
- [ ] 没有硬编码的配置值
- [ ] 代码中没有未使用的导入
- [ ] 所有网络请求包含超时和错误处理
- [ ] DOM 操作前验证元素存在性
- [ ] 文件操作包含错误处理
- [ ] 日志输出适当且不包含敏感信息

## 质量门禁

以下情况必须修复后才能合并代码：

1. **严重错误**: 未捕获的异常、内存泄漏、资源未释放
2. **类型错误**: 缺少类型检查导致运行时错误
3. **安全漏洞**: 敏感信息泄露、注入攻击风险
4. **性能问题**: 明显的性能瓶颈（如 N+1 查询）
5. **代码规范**: 违反核心原则的代码

## 持续改进

- **代码审查**: 所有代码必须经过审查
- **重构**: 定期重构技术债务
- **学习**: 关注最佳实践和新技术
- **反馈**: 从错误和问题中学习改进

## 治理规则

1. **原则优先**: 本原则文档优先于其他编码规范
2. **例外处理**: 违反原则需要文档说明原因和替代方案
3. **定期审查**: 每季度审查和更新原则文档
4. **团队共识**: 原则变更需要团队讨论和批准

---

**最后更新**: 2025-01-10
**版本**: 1.0.0
