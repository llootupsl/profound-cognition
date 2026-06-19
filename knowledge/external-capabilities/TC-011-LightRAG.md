<!-- 作者：阿洋 -->

# LightRAG

## 基本信息
- **卡片编号**: #11
- **类型**: TC
- **优先级**: P1
- **层级**: L1

## 功能描述
LightRAG 轻量 RAG 框架，支持文档索引和语义检索。采用图增强检索策略，结合实体抽取和关系构建实现高效知识检索。适用于研究文献、报告文档的增量索引和精准语义查询。

## 调用指令

### 输入参数
- `operation` (string, 操作类型: index/query)
- `documents` (array, index 操作必需，文档路径或文本数组)
- `query` (string, query 操作必需，语义查询文本)
- `top_k` (integer, query 操作返回结果数，默认 5)

### 输出格式
检索结果数组，每条含 content、source、score

### 调用示例
```
lightrag.operation(operation="index", documents=["/data/report_2026.pdf", "/data/market_analysis.md"])
lightrag.operation(operation="query", query="中国新能源汽车出海策略分析", top_k=5)
```

## 穷尽重试策略
- **穷尽重试替代路径**: LightRAG → 简单向量搜索 → 关键词搜索
- **触发条件**: LightRAG 服务不可用或索引损坏

## MCP 适配
- **MCP Tool 名称**: lightrag_operation
- **MCP 参数**: operation, documents, query, top_k

## 依赖
- LightRAG 服务部署 + 嵌入模型（推荐 text-embedding-3-small）

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

暂无显式 DAG 节点消费者。保留待扩展。

