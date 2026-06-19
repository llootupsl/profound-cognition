<!-- 作者：阿洋 -->

# TC-060: RSI — Reasoning via Structured Interaction

## 基本信息
- **名称**: RSI (Reasoning via Structured Interaction)
- **类别**: 推理框架
- **语言**: LLM-driven
- **版本要求**: N/A
- **安装**: 无需安装（LLM 内置推理模式）
- **许可证**: N/A
- **仓库**: N/A

## 核心能力
- 结构化交互推理
- 多轮对话式推理链构建
- 推理路径分解与验证
- LLM 原生推理增强

## 在 profound-cognition 中的用途
- **T22 Step 3**: RSI 推理验证
- **T23 Step 1**: 因果图构建辅助
- **穷尽重试替代路径**: 失败时穷尽重试替代为单轮推理

## 已知限制
- 依赖 LLM 推理能力上限
- 多轮交互增加 Token 消耗
- 推理链过长可能导致上下文丢失

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

| 节点 | 用途 |
|------|------|
| TM03 | 结构化交互推理 |

## 方法论内化

> ★核心方法论已内化于 tasks/TM03_adversarial_synthesis.md (MC-057完整内化)，以下为快速参考

### 方法论原理
RSI通过结构化交互实现递归深度推理，解决了单轮推理容易陷入局部最优的问题。

### 执行步骤
1. 初始推理生成
2. 结构化质疑
3. 推理修正
4. 二次质疑
5. 收敛判定
6. 最终推理

### 决策规则
| 条件 | 动作 |
|------|------|
| 需要深度推理 | RSI |
| 需要快速推理 | 标准CoT |
| 需要多视角 | Devil's Advocate |

### 输出规范
```yaml
rsi_output:
  available: bool
  reasoning_rounds: int
  converged: bool
  final_reasoning: str
  degradation_note: str
```

### 穷尽重试策略
| 级别 | 方案 |
|------|------|
| L1 | RSI完整结构化交互推理 |
| L2 | 标准CoT |
| L3 | 单轮推理 |
| L4 | 直觉判断 |

