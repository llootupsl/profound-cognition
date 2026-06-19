<!-- 作者：阿洋 -->

# xAI Grok

## 基本信息
- **卡片编号**: #39
- **类型**: TC
- **优先级**: P2
- **层级**: L1

## 功能描述
xAI Grok 搜索工具，支持实时信息搜索与社交媒体数据检索。利用 Grok 模型的实时知识获取能力，提供最新资讯、热点事件和社交媒体动态的搜索与摘要。适用于需要实时信息和社交舆情分析的场景。

## 调用指令

### 输入参数
- `query` (string, 搜索查询)
- `search_mode` (string, 可选: web/social/auto, 搜索模式，默认 auto)

### 输出格式
搜索结果 + 摘要，含 title, url, snippet, source_type, summary

### 调用示例
```
xai_grok_search.search(query="2026年AI行业最新动态", search_mode="auto")
```

## 穷尽重试策略
- **穷尽重试替代路径**: xAI Grok → SearXNG → LLM 内置搜索
- **触发条件**: xAI API 不可用或搜索功能受限

## MCP 适配
- **MCP Tool 名称**: xai_grok_search
- **MCP 参数**: query, search_mode

## 依赖
- xAI API Key

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

暂无显式 DAG 节点消费者。保留待扩展。

