<!-- 作者：阿洋 -->

# MC-182: ActiveInference — 主动推理框架

> ★核心方法论已内化于 knowledge/cognitive-framework.md

## 基本信息
- **名称**: ActiveInference (pymdp/ActiveInference.jl)
- **类别**: 方法论卡片
- **类型**: MC
- **语言**: Python/Julia
- **许可证**: MIT
- **仓库**: https://github.com/infer-actively/pymdp

## 核心能力
- 自由能原理驱动决策
- 变分自由能计算（KL散度 + 期望对数似然）
- 预期自由能（认知价值 + 实用价值）
- 主动推理循环（感知→策略评估→动作→学习）
- A/B/C/D矩阵数据结构

## 在 profound-cognition 中的用途
- **supervisor protocol**: "信息增益 vs 时间成本"动态平衡

## 消费节点
- supervisor protocol
