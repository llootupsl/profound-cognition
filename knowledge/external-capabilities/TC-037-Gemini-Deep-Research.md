<!-- 作者：阿洋 -->

# Gemini Deep Research

## 基本信息
- **卡片编号**: #37
- **类型**: TC
- **优先级**: P2
- **层级**: L0

## 功能描述
Gemini Deep Research 深度研究工具，利用 Google Gemini 模型的超长上下文窗口进行多步骤深度搜索与综合分析，自动拆解复杂研究问题并生成结构化研究报告。适用于需要大规模信息整合、多文档对比和深度推理的场景。

## 调用指令

### 输入参数
- `query` (string, 研究查询主题)
- `depth` (string, 可选: shallow/medium/deep, 研究深度，默认 deep)

### 输出格式
研究报告，含摘要、分章节分析、信息来源列表、结论与建议

### 调用示例
```
gemini_deep_research.research(query="全球半导体产业链重构趋势分析", depth="deep")
```

## 穷尽重试策略
- **穷尽重试替代路径**: Gemini Deep Research → GPT-Researcher → 手动研究
- **触发条件**: Google AI API 不可用或 Deep Research 功能受限

## MCP 适配
- **MCP Tool 名称**: gemini_deep_research
- **MCP 参数**: query, depth

## 依赖
- Google AI API Key

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

暂无显式 DAG 节点消费者。保留待扩展。

