<!-- 作者：阿洋 -->

# 上下文预算管理协议

## 1. 概述

**方法论原理**：上下文预算协议基于"认知资源有限性"的认知假设：LLM的上下文窗口是有限资源，需要在信息完整性和资源效率之间取得平衡。通过预算管理，确保关键信息优先保留，次要信息按需压缩或丢弃。

本协议定义 Profound Cognition v2 框架的上下文窗口预算主动管理机制。目标是在流水线执行过程中主动监控和控制上下文使用量，避免因上下文溢出导致的质量损失。

## 2. 监控机制

### 2.1 监控频率
- 每完成 5 个节点估算一次上下文使用量
- 在每道 Gate 之前强制估算（T07/T14/T16 执行前）
- 在 NRSF 加载前强制估算（I01 和 T20 全量加载前）

### 2.2 估算方法
- 统计已执行节点的 Context Package 累计长度
- 预估剩余节点的平均输出长度
- 计算当前使用量占预算的百分比
- 估算 NRSF-Full 的 token 占用（1 token ≈ 0.75 中文字）

## 3. 预算阈值与响应策略

### 3.1 阈值定义

| 阈值级别 | 百分比 | 说明 |
|---------|--------|------|
| GREEN | < 80% | 正常输出 |
| YELLOW | 80%-120% | 仅删除 methodology_notes 和 process_description，保留 core_conclusions/key_findings/supporting_evidence/intermediate_results 完整 |
| RED | 120%-150% | 触发批量写入（write-while-research），将当前上下文完整写入文件后继续生成，不删除任何分析维度 |
| 强制落盘 | > 150% | 强制批量写入（force batch write）+ 继续生成，不丢弃任何分析维度、不跳过任何节点、不终止研究 |

### 3.2 压缩策略细节

YELLOW 级别（80%-120%）压缩规则：
- core_conclusions: 保留完整
- key_findings: 保留完整
- supporting_evidence: 保留完整
- intermediate_results: 保留完整
- process_description: 全部删除
- methodology_notes: 全部删除

RED 级别（120%-150%）批量写入规则：
- 触发批量写入（write-while-research）：将当前所有活跃上下文（含所有分析维度）完整写入 Checkpoint 文件
- core_conclusions: 保留完整（写入文件后从上下文释放）
- key_findings: 保留完整（写入文件后从上下文释放）
- supporting_evidence: 保留完整（写入文件后从上下文释放）
- process_description: 保留完整（写入文件后从上下文释放）
- methodology_notes: 保留完整（写入文件后从上下文释放）
- 写入完成后，上下文预算重置为仅包含必要的引用指针和当前执行状态

强制落盘（> 150%）：
- 强制批量写入（force batch write）：将当前所有活跃上下文完整写入 Checkpoint 文件
- 写入完成后，上下文预算重置为仅包含引用指针和当前执行状态
- 继续生成：不丢弃任何分析维度，不跳过任何未执行节点，不终止研究
- T19 交付守卫必须标注批量写入影响范围（写入的文件路径和释放的上下文量）
- T20 渲染时附加声明："本报告因上下文预算压力（超过150%），已通过批量写入机制完整保留所有分析维度，无任何维度被丢弃或简化"

### 3.3 检查时机

在 Phase 1 执行循环中，每完成 5 个任务标记后检查上下文预算时，Orchestrator SHALL：
1. 使用 §3.4 中定义的活跃上下文（active context）核算规则计算预算使用量
2. 使用 §3.1 中定义的阈值进行 GREEN/YELLOW/RED 判定
3. 若判定为 YELLOW → 使用 §3.2 中的压缩策略
4. 若判定为 RED → 触发批量写入（write-while-research），将当前上下文写入文件后释放上下文空间

### 3.4 预算核算规则（活跃上下文）

上下文预算仅核算"活跃上下文"（active context），即尚未通过 write-to-file 写入文件的章节内容。已写入 Checkpoint 文件的章节不计入上下文预算。

核算规则：
- 活跃上下文 = 当前会话中所有节点输出 - 已写入 Checkpoint 文件的内容
- 当内容通过批量写入（write-while-research / force batch write）写入文件后，该部分内容从上下文预算中释放
- 写入文件后，上下文仅保留必要的引用指针（如文件路径、章节索引）和当前执行状态
- 此规则确保上下文预算反映的是实际内存占用，而非累计输出量

---

## 4. 强制落盘联动（EXHAUST 一致性）

当上下文预算超过强制落盘阈值（> 150%）时：
1. 强制批量写入（force batch write）：将当前所有活跃上下文完整写入 Checkpoint 文件
2. 写入完成后，上下文预算重置为仅包含引用指针和当前执行状态
3. 继续生成：不丢弃任何分析维度，不跳过任何未执行节点，**不终止研究**——EXHAUST 模式下研究仅由质量驱动条件终止，不由上下文预算终止
4. T19 交付守卫必须标注批量写入影响范围（写入的文件路径和释放的上下文量）
5. T20 渲染时附加声明："本报告因上下文预算压力（超过150%），已通过批量写入机制完整保留所有分析维度，无任何维度被丢弃或简化"

## 5. 恢复机制

如果压缩后上下文使用量回落到 GREEN 级别：
- 后续节点恢复正常输出长度
- 已压缩的节点输出不重新生成（避免重复执行）

## 6. 重要性感知压缩策略 (LLMLingua-style)

### 6.1 重要性评分维度

```yaml
importance_scoring:
  fact_density:
    weight: 0.35
    description: "事实密度（facts/token），每百字包含的可验证事实数"
  novelty:
    weight: 0.25
    description: "新颖度（是否产出超越基础事实的洞察）"
  core_relevance:
    weight: 0.30
    description: "与用户原始问题的直接相关程度"
  cross_reference_count:
    weight: 0.10
    description: "被其他节点引用的次数"
```

### 6.2 压缩执行流程

```yaml
compression_workflow:
  step_1: "当上下文预算超限时，Orchestrator 计算所有节点输出的重要性评分"
  step_2: "按评分降序排列，从最低分开始逐节点压缩"
  step_3: "将被压缩节点的完整输出替换为 summary（遵守 rule_6_minimum_fields）"
  step_4: "重复 step_2-3 直到上下文预算恢复至 soft_cap_percent 以内"
  step_5: "记录压缩日志：{node_id}: full → summary, importance_score={score}"
```

### 6.3 压缩阈值

```yaml
compression_thresholds:
  below_03: "评分 < 0.3 的节点可压缩至 50 字以内（仅保留 core_conclusion）"
  mid_range: "评分 0.3-0.7 的节点压缩至 summary 长度上限（2000字）"
  above_07: "评分 ≥ 0.7 的节点保持完整 summary 长度（2000字），不可压缩"
```

### 6.4 禁止压缩

```yaml
no_compress_zones:
  - "T13 核心结论（cognitive_synthesis.conclusions）"
  - "T09 中标记为 HIGH 的新发现"
  - "T15 中 activation_confidence ≥ 0.8 的引擎输出"
  - "context_package 中的原始问题"
```

## 7. NRSF 上下文管理

### 7.1 NRSF 加载策略选择

NRSF 加载时，根据上下文窗口大小选择加载策略（详见 nrsf-protocol.md NRSF 分层摘要机制章节）：

| 情况 | 条件 | 策略 |
|------|------|------|
| 情况 1 | NRSF-Full ≤ 50% 窗口 | 全量加载 |
| 情况 2 | NRSF-Full 在 50%-95% 窗口 | 分块加载 |
| 情况 3 | NRSF-Full > 95% 窗口 | Summary 代理 + LLMLingua 压缩 |
| 情况 4 | Summary > 窗口 | **不终止研究**——强制 write-while-research 落盘 + 分段加载 + 增量渲染，研究继续进行直至质量驱动终止 |

### 7.2 NRSF-Summary 作为轻量替代

当上下文预算紧张时：
- 优先加载 NRSF-Summary（≤ 8000 字）替代 NRSF-Full
- NRSF-Summary 包含核心论点、关键发现、未闭合论证链
- 大部分任务（T02-T06, T08-T13, T15-T19）仅需 NRSF-Summary 即可执行

### 7.3 LLMLingua 压缩集成

当 NRSF-Full 超过上下文窗口 95% 时：
- 使用 LLMLingua 对 NRSF-Full 进行重要性感知压缩
- 压缩策略与本协议 §6 的重要性评分维度一致
- 压缩后保留核心论点和关键引用，删除过程性描述

### 7.4 与 Checkpoint 协议的联动

- Checkpoint 写入前检查上下文预算
- 写入 NRSF § 节时，如果上下文预算超过 RED 阈值，触发压缩
- 压缩后继续执行，不中断研究流程

## 递归感知截断策略 (v3.1 — EXHAUST 一致性修订)

> **EXHAUST 一致性声明**：本节原 v3.0 版本含有"最大递归轮次: 10"、"Token 硬上限: 1,200,000 tok"、"节点级递归限制"等硬上限，与 EXHAUST 模式四大铁律（Token 不设上限 / 时间不设限制 / 质量唯一优先 / 永远穷尽无档位无上限）严重冲突。v3.1 已全部移除硬上限，改为质量驱动终止 + write-while-research 落盘释放上下文。

### 递归场景 Token 预算（参考性，非硬上限）

| 递归深度 | 单轮参考预算 | 累计参考预算 | 截断策略 |
|----------|----------|----------|----------|
| 0 (无递归) | 150,000 | 150,000 | 标准截断 |
| 1 (1轮递归) | 120,000 | 270,000 | 保留核心+摘要 |
| 2 (2轮递归) | 100,000 | 370,000 | 仅保留核心 |
| 3 (3轮递归) | 80,000 | 450,000 | 核心压缩+引用 |
| ≥4 (深度递归) | 60,000 | 510,000+ | 极限压缩 |

> 上表为**参考性预算估算**，用于触发 write-while-research 落盘决策，**不作为强制终止条件**。任何深度均可通过批量写入释放上下文后继续递归。

### 递归截断优先级

1. **必须保留**: 当前执行节点的完整输出、Gate 判定结果
2. **高优先级保留**: T13 对抗结果、T26 反思结论、T27 验证报告
3. **中优先级保留**: T22-T25 的 output_schema 摘要
4. **低优先级可截断**: 中间步骤的详细推理过程、重复性论述
5. **可完全移除**: 历史递归轮次的中间输出（仅保留最终结论）

### 全局安全机制（EXHAUST 一致性）

- **无最大递归轮次上限**：递归由质量驱动终止（ΔInfo(t) < ε 或所有缺口已处理），不设轮数硬上限
- **无 Token 硬上限**：通过 write-while-research 批量写入释放上下文，可无限延续
- **上下文压力响应**：当上下文使用率 > 150% 时，触发强制批量写入（force batch write），写入后继续生成，不丢弃任何分析维度、不跳过任何节点

### 节点级递归终止条件（质量驱动，非轮数硬上限）

| 节点 | 终止条件 | 说明 |
|------|----------|------|
| T13 | depth_satisfaction.score ≥ 0.85 或所有深度信号已充分处理 | 质量驱动收敛 |
| T24 | 维度覆盖完整且无新增洞察 | 质量驱动收敛 |
| T26 | 无新跨维度洞察产生 | 质量驱动收敛 |
| Gate-δ 退回 | 所有失败项已修复并通过 | 持续重试直至通过 |

### 递归上下文膨胀监控

每轮递归后检查:
1. 上下文增长率 (应 <30%/轮)
2. 新增信息密度 (应 >0.5 新洞察/千字)
3. 重复率 (应 <20%)

如任一指标不满足，触发 write-while-research 批量写入释放上下文，**不触发提前终止递归**——递归终止仅由质量驱动条件决定。

## 交叉引用

- [nrsf-protocol.md](./nrsf-protocol.md) — NRSF 叙事式研究状态文件协议
- [checkpoint-protocol.md](./checkpoint-protocol.md) — Checkpoint 原子写入与断点续传协议
- [handoff-protocol.md](./handoff-protocol.md) — Context Package 标准格式
- [formula-engine/info-decay.md](../formula-engine/info-decay.md) — 指数边际收益衰减模型

## 迭代终止逻辑（指数衰减模型）

在判断是否停止迭代时，调用 `formula-engine/info-decay` 指数边际收益衰减模型：

1. 每轮迭代后计算 ΔInfo(t) = α · exp(-λt)（默认 α=1.0, λ=0.3）
2. 当 ΔInfo(t) < ε（默认 ε=0.05）时：自动终止迭代，标记为"信息增益收敛"
3. 不做固定迭代上限限制——衰减模型动态决定何时停止
4. 替代原硬阈值：depth_satisfaction ≥ 0.9（已移除迭代次数守卫硬上限，改为质量驱动终止）

I01 终止条件已同步更新，参见 tasks/I01_iterative_deepening.md
