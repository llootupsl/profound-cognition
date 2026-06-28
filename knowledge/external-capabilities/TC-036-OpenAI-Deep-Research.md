<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

# OpenAI Deep Research

## 基本信息
- **卡片编号**: #36
- **类型**: TC
- **优先级**: P2
- **层级**: L0

## 功能描述
OpenAI Deep Research 深度研究工具，利用 OpenAI 模型进行多步骤、多轮搜索与综合分析，自动拆解复杂研究问题并生成结构化研究报告。适用于需要深度调研、多源信息整合和长篇分析的场景。

## 调用指令

### 输入参数
- `query` (string, 研究查询主题)
- `depth` (string, 可选: shallow/medium/deep, 研究深度，默认 deep)

### 输出格式
研究报告，含摘要、分章节分析、信息来源列表、结论与建议

### 调用示例
```
openai_deep_research.research(query="全球半导体产业链重构趋势分析", depth="deep")
```

## 穷尽重试策略
- **穷尽重试替代路径**: OpenAI Deep Research → GPT-Researcher → 手动研究
- **触发条件**: OpenAI API 不可用或 Deep Research 功能受限

## MCP 适配
- **MCP Tool 名称**: openai_deep_research
- **MCP 参数**: query, depth

## 依赖
- OpenAI API Key

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