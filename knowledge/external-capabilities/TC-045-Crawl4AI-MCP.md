<!-- 作者：阿洋 -->

# Crawl4AI MCP

## 基本信息
- **卡片编号**: #45
- **类型**: TC
- **优先级**: P2
- **层级**: L1

## 功能描述
Crawl4AI MCP 适配器，将 Crawl4AI 网页抓取与解析工具封装为 MCP Tool，使其可通过 MCP 协议统一调用。保留 Crawl4AI 的全部功能，包括 JavaScript 渲染、反爬虫绕过和 Markdown 转换，同时获得 MCP 生态的标准化调用能力。

## 调用指令

### 输入参数
- 同 Crawl4AI（url, output_format, js_rendering, timeout 等）

### 输出格式
同 Crawl4AI（Markdown/HTML/纯文本）

### 调用示例
```
crawl4ai_mcp_fetch.fetch(url="https://example.com/article", output_format="markdown", js_rendering=true)
```

## 穷尽重试策略
- **穷尽重试替代路径**: Crawl4AI MCP → Crawl4AI 直接调用
- **触发条件**: MCP Server 不可用或协议通信失败

## MCP 适配
- **MCP Tool 名称**: crawl4ai_mcp_fetch
- **MCP 参数**: 同 Crawl4AI 参数

## 依赖
- Crawl4AI + MCP Server

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

暂无显式 DAG 节点消费者。保留待扩展。

