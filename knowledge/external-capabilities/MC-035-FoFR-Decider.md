<!-- 作者：阿洋 -->

# FoFR-Decider

## 基本信息
- **卡片编号**: #35
- **类型**: MC
- **优先级**: P2
- **层级**: L0

## 功能描述
FoFR-Decider 决策框架方法卡片，支持多方案对比决策。通过定义决策准则和权重，对多个候选方案进行系统化评估和排序，生成带评分的决策结果。支持自定义准则维度和权重分配，适用于技术选型、方案评审、资源分配等需要结构化决策的场景。

## 调用指令

### 输入参数
- `options` (array, 候选方案列表，每项含 name 和 description)
- `criteria` (array, 决策准则列表，每项含 name 和 description)
- `weights` (object, 准则权重映射，key 为准则名称，value 为权重值 0-1)

### 输出格式
决策结果 + 评分，含各方案得分、排序、优劣势分析

### 调用示例
```
fofr_decide(options=[{"name":"方案A","description":"基于微服务架构"},{"name":"方案B","description":"基于单体架构"}], criteria=[{"name":"可扩展性","description":"系统水平扩展能力"},{"name":"开发效率","description":"功能交付速度"}], weights={"可扩展性":0.7,"开发效率":0.3})
```

## 穷尽重试策略
- **穷尽重试替代路径**: FoFR-Decider → 简单加权评分
- **触发条件**: 决策框架服务不可用或准则定义不完整

## MCP 适配
- **MCP Tool 名称**: fofr_decide
- **MCP 参数**: options, criteria, weights

## 依赖
- LLM 推理后端（支持结构化输出）

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

暂无显式 DAG 节点消费者。保留待扩展。

