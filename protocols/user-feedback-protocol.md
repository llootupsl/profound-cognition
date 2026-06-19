<!-- 作者：阿洋 -->

# User Feedback Protocol — 用户反馈事件化协议

## 概述

**方法论原理**：用户反馈协议基于"反馈是认知校准的核心机制"的认知假设：用户反馈不是简单的纠错信号，而是认知系统校准其理解与用户期望之间差距的关键输入。将反馈事件化处理，使每次反馈都成为系统改进的机会。

本协议定义用户在 DAG 执行过程中提出反馈的标准处理流程。用户的反馈被分类为三种事件类型，每种类型对应不同的回滚范围和重执行策略。

## 反馈事件类型

### 1. USER_NEW_HYPOTHESIS — 用户提出更强假设

**触发条件**：用户提出了 T09 推理路径中未覆盖的新假设或替代解释

**处理流程**：
1. Orchestrator 触发 Phase 2.5 用户反馈处理
2. 分类为 `USER_NEW_HYPOTHESIS`
3. 将新假设注入 T09（多路径推理），作为新的推理路径补充
4. 回滚范围：T09 → T10 → T11 → T12 → T13（如已执行）
5. 重执行 T09：在新假设路径上执行推理
6. 重执行 T10/T11/T12：对新推理路径进行对抗验证
7. 重执行 T13：整合新旧假设的结论
8. 产出 `hypothesis_merge_report`：对比新旧假设的结论差异

**回滚规则**：
- 已通过 Gate 的上游节点（T07/T14/T16 之前）不变
- 若 T13 还未执行 → 仅回滚 T09/T10/T11/T12
- 若 T13 已执行 → 回滚到 T09，重走 T09→T10→T11→T12→T13

### 2. USER_STRONGER_REFUTATION — 用户提出更有力反驳

**触发条件**：用户对对抗验证结果不满意，提供了新的反驳角度或证据

**处理流程**：
1. 分类为 `USER_STRONGER_REFUTATION`
2. 判断新反驳属于哪个维度：
   - 逻辑层面 → 注入 T10
   - 证据层面 → 注入 T11
   - 范围层面 → 注入 T12
3. 回滚到对应的对抗节点重新执行
4. T13 重新综合时纳入新反驳

**回滚规则**：
- 不改变已通过 Gate 的上游节点结论
- 仅回滚受影响的对抗节点及下游
- 若 T13 已执行 → 回滚范围：对应对抗节点 → T13

### 3. USER_OUTPUT_CORRECTION — 用户提出成品形态纠偏

**触发条件**：用户对输出格式不满意（如 "字号太小"、"需要加入分割线"、"配色改暖色"）

**处理流程**：
1. 分类为 `USER_OUTPUT_CORRECTION`
2. 不触发认知流水线回滚（T01-T19 不变）
3. 仅重执行 T20 渲染节点
4. T20 重新渲染时应用用户的新格式约束

**回滚规则**：
- 最小回滚范围：仅 T20 渲染节点
- T01-T19 流水线产出完全保留
- 用户可指定具体的格式修复要求

## Phase 2.5 用户反馈处理流程

```
ON user_feedback_received:
  CLASSIFY feedback type
  CASE:
    USER_NEW_HYPOTHESIS:
      ROLLBACK to T09
      INJECT new hypothesis into T09 reasoning paths
      RERUN T09 → T10 → T11 → T12 → T13
      OUTPUT hypothesis_merge_report

    USER_STRONGER_REFUTATION:
      IDENTIFY affected adversarial node (T10/T11/T12)
      ROLLBACK to affected node
      INJECT new refutation
      RERUN affected node → T13

    USER_OUTPUT_CORRECTION:
      RERUN T20 only
      APPLY user format constraints
```

## 输出

- `feedback_classification`: 事件分类
- `rollback_scope`: 回滚的节点范围
- `merge_report` (仅 USER_NEW_HYPOTHESIS): 新旧假设对比报告
- `rerun_summary`: 重执行摘要

## 交叉引用

- [nrsf-protocol.md](./nrsf-protocol.md) — NRSF 叙事式研究状态文件协议
- [checkpoint-protocol.md](./checkpoint-protocol.md) — Checkpoint 原子写入与断点续传协议

## v3.0 用户反馈扩展 (元层反馈)

### 新增反馈事件类型

| 事件类型 | 触发条件 | 目标节点 | 穷尽尝试路径 |
|----------|----------|----------|----------|
| USER_META_LAYER_FEEDBACK | 用户对元层分析结果提出修正 | T26 | T26→T27→T28→T_gate_delta |
| USER_SCENARIO_OVERRIDE | 用户要求修改情景假设 | T25 | T25→T26→T27→T28→T_gate_delta |
| USER_ETHICS_CONCERN | 用户提出伦理担忧 | T26 Step7 | T26→T27→T28→T_gate_delta |
| USER_ONTOLOGY_CORRECTION | 用户修正知识图谱实体/关系 | T28 | T28→T_gate_delta |

### 反馈处理规则
1. 元层反馈优先级高于经典层反馈
2. 伦理反馈(USER_ETHICS_CONCERN)必须触发T26重新执行Step7
3. 情景覆盖反馈(USER_SCENARIO_OVERRIDE)需重新执行T25 Step8-10
4. 本体修正反馈(USER_ONTOLOGY_CORRECTION)需重新执行T28 Step7验证
## 异常处理与穷尽重试

| 异常场景 | 处理策略 |
|---------|---------|
| 用户反馈模糊无法解析 | 请求用户澄清，提供选项列表辅助明确 |
| 用户反馈与研究结论严重矛盾 | 标注"用户反馈与结论矛盾"，保留两者供后续裁决 |
| 用户反馈导致需要大规模重做 | 无论重做范围多大，持续修改直至完成 |
| 用户多次反馈相互矛盾 | 识别矛盾点，请求用户确认最终意图 |
