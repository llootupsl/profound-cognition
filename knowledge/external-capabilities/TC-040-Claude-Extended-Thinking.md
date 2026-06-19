<!-- 作者：阿洋 -->

# Claude Extended Thinking

## 基本信息
- **卡片编号**: #40
- **类型**: TC
- **优先级**: P2
- **层级**: L0

## 功能描述
Claude Extended Thinking 扩展思考模式，支持长链推理（Extended Thinking），通过分配额外思考预算实现深度逻辑推演、复杂问题分解和多步决策。模型在输出最终结论前先完成内部思考过程，适用于需要深度分析和审慎推理的场景。

## 调用指令

### 输入参数
- `prompt` (string, 推理提示词)
- `thinking_budget` (integer, 可选, 思考 token 预算，默认 10000)

### 输出格式
思考过程 + 结论，含 thinking（思考链）和 response（最终结论）

### 调用示例
```
claude_extended_think.think(prompt="分析量子计算对现有加密体系的潜在威胁及应对策略", thinking_budget=20000)
```

## 穷尽重试策略
- **穷尽重试替代路径**: Claude Extended Thinking → 标准推理
- **触发条件**: Anthropic API 不可用或 Extended Thinking 功能受限

## MCP 适配
- **MCP Tool 名称**: claude_extended_think
- **MCP 参数**: prompt, thinking_budget

## 依赖
- Anthropic API Key

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

暂无显式 DAG 节点消费者。保留待扩展。

