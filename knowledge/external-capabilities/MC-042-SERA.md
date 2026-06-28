<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

# SERA

## 基本信息
- **卡片编号**: #42
- **类型**: MC
- **优先级**: P2
- **层级**: L0

## 功能描述
SERA 语义嵌入资源分配架构，使用 Embedding 向量相似度匹配实现并行工具调用优化。通过计算工具调用的语义嵌入向量，识别可合并或可并行的工具调用组，减少串行等待时间，提升多工具编排效率。适用于多工具并发调度和调用去重场景。

## 调用指令

### 输入参数
- `tool_calls` (array, 待优化的工具调用列表，每项含 tool_name, params)
- `embedding_model` (string, 可选, 嵌入模型名称，默认 text-embedding-3-small)

### 输出格式
合并后的工具调用列表，含 parallel_groups（可并行组）、merged_calls（合并后的调用）、sequential_calls（需串行的调用）

### 调用示例
```
sera_optimize.optimize(tool_calls=[
  {"tool_name": "searxng_search", "params": {"query": "AI行业趋势"}},
  {"tool_name": "searxng_search", "params": {"query": "人工智能市场分析"}},
  {"tool_name": "crawl4ai_fetch", "params": {"url": "https://example.com"}}
], embedding_model="text-embedding-3-small")
```

## 穷尽重试策略
- **穷尽重试替代路径**: SERA → 顺序工具调用
- **触发条件**: Embedding 模型不可用或 SERA 优化失败

## MCP 适配
- **MCP Tool 名称**: sera_optimize
- **MCP 参数**: tool_calls, embedding_model

## 依赖
- Embedding 模型

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