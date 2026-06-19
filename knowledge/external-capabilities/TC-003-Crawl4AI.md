<!-- 作者：阿洋 -->

# Crawl4AI

## 基本信息

> ★核心方法论已内化于 knowledge/search-strategy.md，本文件仅作快速引用入口

- **卡片编号**: #3
- **类型**: TC
- **优先级**: P0
- **层级**: L1

## 功能描述
网页抓取与解析工具，支持 JavaScript 渲染、反爬虫绕过、Markdown 转换

## 调用指令

### 输入参数
- `url` (string, 目标 URL)
- `output_format` (string, 可选: markdown/text/html)
- `js_rendering` (boolean, 默认 true)
- `timeout` (integer, 默认 30s)

### 输出格式
Markdown/HTML/纯文本

### 调用示例
```
crawl4ai.fetch(url="https://example.com/article", output_format="markdown", js_rendering=true)
```

## 穷尽重试策略
- **穷尽重试替代路径**: Crawl4AI → requests + BeautifulSoup → LLM 内置 fetch
- **触发条件**: Crawl4AI 服务不可用

## MCP 适配
- **MCP Tool 名称**: crawl4ai_fetch
- **MCP 参数**: url, output_format, js_rendering, timeout

## 依赖
- Crawl4AI 服务部署

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

暂无显式 DAG 节点消费者。保留待扩展。

