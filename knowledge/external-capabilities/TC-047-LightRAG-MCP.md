<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

# LightRAG MCP

## 基本信息
- **卡片编号**: #47
- **类型**: TC
- **优先级**: P2
- **层级**: L1

## 功能描述
LightRAG MCP 适配器，将 LightRAG 轻量 RAG 框架封装为 MCP Tool，使其可通过 MCP 协议统一调用。保留 LightRAG 的全部功能，包括图增强检索、实体抽取、关系构建和增量索引，同时获得 MCP 生态的标准化调用能力。

## 调用指令

### 输入参数
- 同 LightRAG（operation, documents, query, top_k 等）

### 输出格式
同 LightRAG（检索结果数组，每条含 content、source、score）

### 调用示例
```
lightrag_mcp_operation.operation(operation="index", documents=["/data/report_2026.pdf"])
lightrag_mcp_operation.operation(operation="query", query="中国新能源汽车出海策略分析", top_k=5)
```

## 穷尽重试策略
- **穷尽重试替代路径**: LightRAG MCP → LightRAG 直接调用
- **触发条件**: MCP Server 不可用或协议通信失败

## MCP 适配
- **MCP Tool 名称**: lightrag_mcp_operation
- **MCP 参数**: 同 LightRAG 参数

## 依赖
- LightRAG + MCP Server

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

暂无显式 DAG 节点消费者。保留待扩展。


## 效果度量

| 度量指标 | 定义 | 目标值 |
|----------|------|--------|
| 执行成功率 | 成功调用次数 / 总调用次数 | ≥ 0.95 |
| 平均延迟 | 单次调用平均耗时 | ≤ 5s |
| 输出质量分 | Supervisor 评分（0-1） | ≥ 0.8 |
| 穷尽重试触发率 | 触发降级的调用次数 / 总调用次数 | ≤ 0.1 |

效果度量写入 NRSF，供 T19 质量检查消费。