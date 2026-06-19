<!-- 作者：阿洋 -->

# Whoogle

## 基本信息

> ★核心方法论已内化于 knowledge/search-strategy.md，本文件仅作快速引用入口

- **卡片编号**: #2
- **类型**: TC
- **优先级**: P0
- **层级**: L1

## 功能描述
Google 搜索代理，提供无广告、无追踪的 Google 搜索结果，作为 SearXNG 的备选

## 调用指令

### 输入参数
- `query` (string, 搜索查询)
- `language` (string, 可选: lang_zh/lang_en)
- `near` (string, 可选: 地理位置限制)

### 输出格式
JSON 数组，每条含 title, url, snippet

### 调用示例
```
whoogle.search(query="AI safety research 2024", language="lang_en")
```

## 穷尽重试策略
- **穷尽重试替代路径**: Whoogle → LLM 内置搜索
- **触发条件**: Whoogle 服务不可用

## MCP 适配
- **MCP Tool 名称**: whoogle_search
- **MCP 参数**: query, language, near

## 依赖
- Whoogle 服务部署

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

暂无显式 DAG 节点消费者。保留待扩展。

