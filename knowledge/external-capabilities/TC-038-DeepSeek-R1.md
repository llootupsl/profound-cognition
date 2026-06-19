<!-- 作者：阿洋 -->

# DeepSeek-R1

## 基本信息
- **卡片编号**: #38
- **类型**: TC
- **优先级**: P2
- **层级**: L0

## 功能描述
DeepSeek-R1 推理模型，支持长链推理（Chain-of-Thought），通过显式推理步骤实现复杂逻辑推演、数学证明和多步决策。模型自动输出完整推理过程，适用于需要深度逻辑分析和逐步推导的场景。

## 调用指令

### 输入参数
- `prompt` (string, 推理提示词)
- `max_tokens` (integer, 可选, 最大输出 token 数，默认 8192)
- `reasoning_effort` (string, 可选: low/medium/high, 推理努力程度，默认 high)

### 输出格式
推理过程 + 结论，含 reasoning_content（推理链）和 content（最终结论）

### 调用示例
```
deepseek_r1_reason.infer(prompt="证明：对于任意正整数 n，n^3 - n 总能被 6 整除", max_tokens=4096, reasoning_effort="high")
```

## 穷尽重试策略
- **穷尽重试替代路径**: DeepSeek-R1 → Claude Extended Thinking → 标准推理
- **触发条件**: DeepSeek API 不可用或响应超时

## MCP 适配
- **MCP Tool 名称**: deepseek_r1_reason
- **MCP 参数**: prompt, max_tokens, reasoning_effort

## 依赖
- DeepSeek API Key

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

暂无显式 DAG 节点消费者。保留待扩展。

## 方法论内化

> ★核心方法论已内化于 knowledge/domains/literature-engine.md，以下为快速参考

### 方法论原理
DeepSeek-R1通过长链推理(chain-of-thought)实现深度文献分析，特别擅长数学推理和逻辑链条验证。

### 执行步骤
1. 输入文献+分析指令
2. 触发长链推理
3. 逐步分解论证
4. 验证逻辑一致性
5. 输出结构化分析

### 决策规则
| 条件 | 动作 |
|------|------|
| 需要深度逻辑推理 | DeepSeek-R1 |
| 需要广泛覆盖 | Claude Extended Thinking |
| 标准分析 | 通用LLM |

### 输出规范
```yaml
deepseek_r1_output:
  available: bool
  reasoning_chain: str
  conclusion: str
  logic_consistency: bool
  degradation_note: str
```

### 穷尽重试策略
| 级别 | 方案 |
|------|------|
| L1 | DeepSeek-R1完整长链推理 |
| L2 | Claude Extended Thinking |
| L3 | 标准LLM推理 |
| L4 | 人工分析 |

