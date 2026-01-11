# GitHub Actions Workflow 配置说明

## 工作流说明

`daily-news-analysis.yml` 工作流会自动：
1. 抓取当日新闻（使用 Node.js）
2. 分析新闻内容（使用 Python + LLM）
3. 发送分析报告到飞书
4. 提交分析结果到仓库

## 触发条件

- **定时触发**: 每天 UTC 16:00（北京时间 00:00）
- **手动触发**: 在 GitHub Actions 页面手动运行
- **推送触发**: 当 `news/*.md` 文件更新时

## 必需的 GitHub Secrets

在 GitHub 仓库设置中添加以下 Secrets：

### 必需配置

1. **OPENAI_API_KEY**
   - OpenAI API 密钥
   - 必需，用于 LLM 分析

2. **FEISHU_WEBHOOK_URL**
   - 飞书 Webhook URL
   - 必需，用于发送通知

### 可选配置

3. **OPENAI_API_BASE_URL**
   - OpenAI API 基础 URL
   - 可选，默认使用官方 API

4. **OPENAI_MODEL**
   - 使用的模型名称
   - 可选，默认：`gpt-3.5-turbo`

5. **OPENAI_TIMEOUT**
   - API 超时时间（秒）
   - 可选，默认：`300`

6. **FEISHU_ENABLED**
   - 是否启用飞书通知
   - 可选，默认：`true`

## 配置步骤

1. 进入 GitHub 仓库
2. 点击 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**
4. 添加上述 Secrets

## 工作流步骤

1. ✅ Checkout 代码
2. ✅ 安装 Node.js 依赖
3. ✅ 抓取新闻（`node index.js`）
4. ✅ 安装 Python 和 uv
5. ✅ 安装 Python 依赖
6. ✅ 检查新闻文件是否存在
7. ✅ 分析新闻（如果文件存在）
8. ✅ 发送飞书通知（如果分析成功）
9. ✅ 上传分析结果作为 Artifact
10. ✅ 提交并推送结果到仓库

## 注意事项

- 如果抓取失败，工作流会继续执行（使用已有数据）
- 只有分析成功时才会发送飞书通知
- 只有分析成功时才会提交结果到仓库
- 分析结果会保存为 Artifact，保留 30 天
