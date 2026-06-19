<!-- 作者：阿洋 -->

# STORM

> ★核心方法论已内化于 knowledge/domains/literature-engine.md

## 基本信息
- **卡片编号**: #29
- **类型**: TC
- **优先级**: P2
- **层级**: L0

## 功能描述
STORM 多视角研究工具，从不同专家视角生成研究问题。模拟多位领域专家对同一主题进行独立提问，通过视角聚合和问题去重形成多维度问题集，支持深度控制和研究方向扩展，适用于研究课题探索、文献综述准备、问题空间拓展等场景。

## 调用指令

### 输入参数
- `topic` (string, 研究主题)
- `perspectives` (array, 可选: 专家视角列表，如 ["经济学家","社会学家","技术专家"])
- `depth` (integer, 可选: 研究深度层级，默认 2)

### 输出格式
多视角问题列表，每条含 perspective、question、rationale

### 调用示例
```
storm_generate(topic="大语言模型对高等教育的影响", perspectives=["教育学家","技术伦理专家","政策制定者"], depth=3)
```

## 穷尽重试策略
- **穷尽重试替代路径**: STORM → 手动多视角提问
- **触发条件**: STORM 服务不可用或 LLM 推理后端超时

## MCP 适配
- **MCP Tool 名称**: storm_generate
- **MCP 参数**: topic, perspectives, depth

## 依赖
- STORM 服务部署 + LLM 推理后端

## 消费关系

### 消费此卡片的领域引擎

| 引擎名称 | 激活条件 | 使用方式 |
|---------|---------|---------|
| literature-engine | on-demand | 跨文本综合、文献综述生成 - 通过 STORM API 调用 |

### 消费此卡片的 DAG 节点

暂无显式 DAG 节点消费者。

