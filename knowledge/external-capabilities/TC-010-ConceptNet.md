<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

# ConceptNet

## 基本信息

> ★核心方法论已内化于 knowledge/domains/cognitive-science-engine.md，本文件仅作快速引用入口

- **卡片编号**: #10
- **类型**: TC
- **优先级**: P1
- **层级**: L1

## 功能描述
ConceptNet 概念关系网络查询，提供常识知识和概念间语义关系图谱。支持多语言概念查询，关系类型包括 IsA/PartOf/UsedFor/CapableOf/RelatedTo 等，用于概念扩展、语义推理和知识关联。

## 调用指令

### 输入参数
- `concept` (string, 查询概念，如 "人工智能")
- `relation` (string, 可选关系类型过滤: IsA/PartOf/UsedFor/CapableOf/RelatedTo 等)
- `limit` (integer, 返回关系数量上限，默认 20)

### 输出格式
关系图 JSON，含起始概念、关系类型、终止概念、权重

### 调用示例
```
conceptnet.query(concept="人工智能", relation="IsA", limit=10)
conceptnet.query(concept="machine learning", limit=20)
```

## 穷尽重试策略
- **穷尽重试替代路径**: ConceptNet → LLM 推理
- **触发条件**: ConceptNet API 连续 3 次超时或服务不可用

## MCP 适配
- **MCP Tool 名称**: conceptnet_query
- **MCP 参数**: concept, relation, limit

## 依赖
- ConceptNet API（https://api.conceptnet.io）

## 消费关系

### 消费此卡片的领域引擎

| 引擎名称 | 激活条件 | 使用方式 |
|---------|---------|---------|
| cognitive-science-engine | on-demand | 常识知识图谱用于心智模型构建和常识推理分析 |

### 消费此卡片的 DAG 节点

暂无显式 DAG 节点消费者。


## 效果度量

| 度量指标 | 定义 | 目标值 |
|----------|------|--------|
| 执行成功率 | 成功调用次数 / 总调用次数 | ≥ 0.95 |
| 平均延迟 | 单次调用平均耗时 | ≤ 5s |
| 输出质量分 | Supervisor 评分（0-1） | ≥ 0.8 |
| 穷尽重试触发率 | 触发降级的调用次数 / 总调用次数 | ≤ 0.1 |

效果度量写入 NRSF，供 T19 质量检查消费。