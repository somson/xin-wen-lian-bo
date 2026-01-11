# 新闻联播文字稿项目技术方案

## 项目概述

本项目是一个自动化爬取和展示央视网《新闻联播》文字稿的系统。通过定时任务自动抓取每日新闻联播内容，转换为 Markdown 格式存储，并提供 Web 界面供用户浏览。

## 技术架构

### 技术栈

- **运行环境**: Node.js (ES6 Modules)
- **核心依赖**:
  - `jsdom` (^20.0.0) - HTML DOM 解析和操作
  - `node-fetch` (^3.2.10) - HTTP 请求库
- **前端技术**:
  - Showdown.js - Markdown 转 HTML
  - GitHub Markdown CSS - Markdown 样式

### 项目结构

```
xin-wen-lian-bo/
├── index.js              # 主爬虫脚本
├── fetch.js              # HTTP 请求封装模块
├── index.html            # 首页展示页面
├── package.json          # 项目配置和依赖
├── README.md             # 项目说明和目录索引
├── DEVELOP.md            # 开发文档（待完善）
├── news/                 # 新闻存储目录
│   ├── catalogue.json    # 新闻目录索引（JSON格式）
│   └── YYYYMMDD.md       # 每日新闻文件（Markdown格式）
└── web/                  # Web 前端资源
    ├── view.html         # 新闻详情页
    ├── github-markdown.min.css  # Markdown 样式
    └── showdown.min.js   # Markdown 转换库
```

## 核心功能模块

### 1. 数据爬取模块 (`index.js`)

#### 1.1 日期处理
- 自动获取当前日期，格式化为 `YYYYMMDD` 格式
- 生成对应的文件路径和目录结构

#### 1.2 新闻列表获取 (`getNewsList`)
- **目标URL**: `http://tv.cctv.com/lm/xwlb/day/{date}.shtml`
- **实现方式**:
  - 使用 `fetch.js` 获取 HTML 内容
  - 使用 `jsdom` 解析 HTML DOM
  - 提取所有 `<a>` 标签的链接
  - 去重处理，分离摘要链接和新闻链接数组

#### 1.3 新闻摘要获取 (`getAbstract`)
- 从摘要链接页面提取新闻简介
- 使用 CSS 选择器定位内容区域
- 格式化处理：将分号和冒号后添加换行

#### 1.4 新闻详情获取 (`getNews`)
- 遍历新闻链接数组
- 对每个链接：
  - 获取 HTML 内容
  - 提取标题（去除 `[视频]` 标记）
  - 提取正文内容（`#content_area` 元素）
- 返回新闻对象数组

#### 1.5 Markdown 转换 (`newsToMarkdown`)
- 将新闻数据转换为 Markdown 格式
- 包含：
  - 标题和日期
  - 新闻摘要
  - 详细新闻列表（标题、内容、原文链接）
  - 更新时间戳

#### 1.6 文件存储 (`saveTextToFile`)
- 将 Markdown 内容保存到 `news/YYYYMMDD.md` 文件

#### 1.7 目录更新 (`updateCatalogue`)
- **更新 `catalogue.json`**:
  - 读取现有目录数据
  - 在数组开头插入新日期和摘要
  - 保存 JSON 文件
- **更新 `README.md`**:
  - 在 `<!-- INSERT -->` 标记后插入新的日期链接

### 2. HTTP 请求模块 (`fetch.js`)

#### 2.1 请求封装
- 封装 `node-fetch` 为 Promise 形式
- 配置请求头，模拟浏览器请求：
  - User-Agent 和 Accept 头
  - Cookie 信息
  - CORS 相关头
  - Referer 设置

#### 2.2 特点
- 返回 HTML 文本内容
- 支持自定义请求头，避免反爬虫限制

### 3. 前端展示模块

#### 3.1 首页 (`index.html`)
- **功能**:
  - 从 `/news/catalogue.json` 加载新闻目录
  - 使用 Showdown.js 将 Markdown 转换为 HTML
  - 展示新闻摘要列表和链接
- **样式**:
  - 使用 GitHub Markdown CSS
  - 响应式布局，全屏显示

#### 3.2 详情页 (`web/view.html`)
- **功能**:
  - 通过 URL 参数 `date` 获取指定日期的新闻
  - 从 `/news/{date}.md` 加载 Markdown 内容
  - 转换为 HTML 并渲染
  - 错误处理：加载失败时显示错误页面
- **特点**:
  - 动态标题设置
  - 错误容错机制

## 数据流程

```
1. 定时任务触发
   ↓
2. 获取当前日期 (YYYYMMDD)
   ↓
3. 爬取新闻列表页面
   ↓
4. 提取摘要链接和新闻链接数组
   ↓
5. 获取新闻摘要内容
   ↓
6. 遍历获取每条新闻详情
   ↓
7. 转换为 Markdown 格式
   ↓
8. 保存到 news/YYYYMMDD.md
   ↓
9. 更新 catalogue.json
   ↓
10. 更新 README.md
```

## 关键技术点

### 1. DOM 解析
- 使用 `jsdom` 在 Node.js 环境中模拟浏览器 DOM
- 通过 CSS 选择器精确定位内容元素

### 2. 数据去重
- 新闻链接数组使用 `includes()` 方法去重
- 确保每条新闻只处理一次

### 3. 文件操作
- 使用 Node.js `fs` 模块进行文件读写
- Promise 封装，支持异步操作
- 错误处理机制

### 4. Markdown 格式
- 标准 Markdown 语法
- 包含标题、链接、列表等元素
- 便于版本控制和阅读

### 5. 前端渲染
- 客户端 Markdown 转 HTML
- 无需后端服务器，纯静态页面
- 使用 Fetch API 加载数据

## 部署方案

### 运行方式
```bash
# 安装依赖
npm install

# 执行爬虫脚本
npm run index
# 或
node index.js
```

### 定时任务
- 建议使用 cron 或系统定时任务
- 每日 20-22 点执行（新闻联播播出后）
- 确保网络连接正常

### Web 服务
- 可使用任意静态文件服务器
- 支持 GitHub Pages、Netlify、Vercel 等平台
- 需要支持 JSON 和 Markdown 文件的访问

## 扩展性考虑

### 1. 错误处理
- 网络请求失败重试机制
- 文件写入失败回滚
- 数据格式异常处理

### 2. 性能优化
- 并发请求多条新闻（当前为串行）
- 缓存已爬取内容，避免重复请求
- 增量更新机制

### 3. 功能扩展
- 支持历史日期爬取
- 搜索功能
- RSS 订阅
- 数据导出（PDF、Word 等）

## 注意事项

1. **反爬虫**: 央视网可能有反爬虫机制，需要合理设置请求间隔和请求头
2. **数据准确性**: 依赖央视网页面结构，页面改版可能导致爬虫失效
3. **存储空间**: 长期运行会产生大量 Markdown 文件，需考虑存储管理
4. **版权问题**: 爬取内容仅供学习研究，注意版权合规

## 依赖版本

- Node.js: 建议 14+ (支持 ES6 Modules)
- jsdom: ^20.0.0
- node-fetch: ^3.2.10

## 总结

本项目采用 Node.js + 前端静态页面的架构，实现了新闻联播文字稿的自动化采集、存储和展示。技术方案简洁高效，易于维护和扩展。核心优势在于：

- **轻量级**: 无复杂框架，依赖少
- **易部署**: 纯静态前端，无需后端服务
- **易维护**: 代码结构清晰，模块化设计
- **可扩展**: 预留扩展接口，便于功能增强
