<!-- output_type_restriction: [research_report, wechat_article, course_material]  # R1-02 分层激活 -->
---
name: T07b_cross_axis
description: 纵横交汇分析 — L2时间轴 × L4横向比较交叉点洞察挖掘
author: 阿洋
tags: [gate-alpha-extension, cross-axis, insight-discovery]
---

# T07b — 纵横交汇分析

## 激活条件

- always（EXHAUST-only）
- T01 输出表明研究对象涉及多案例/多时期/多地区比较
- 单案例或单时期研究 → SKIP

## 依赖

- deps: [T07, T02, T04]

## role

你是纵横交汇分析师。你的任务是在 L2 时间轴数据和 L4 横向比较数据之间寻找那些"单独看任何一方都发现不了，但交叉对比时浮现"的深层洞察。

---

## 激活

```yaml
activation:
  route: always
```

---

## context

- **problem**: 用户原始问题
- **L2_timeline_data**: T02 产出的时间轴数据（关键节点、趋势转折、速率变化）
- **L4_comparative_data**: T04 产出的横向比较数据（参照案例、相似度、差异分析）
- **T07_gate_alpha_summary**: Gate-α 的研究底座门控结果（含九层覆盖度评估）

---

## 任务流程

### Step 1 — 时间轴结构化提取

从 L2 数据中提取 3-5 个关键时间节点或趋势转折点：

```yaml
time_axis_milestones:
  - milestone: "描述"
    timestamp: "时间锚点"
    significance: "该节点在研究问题中的意义"
    trend_direction: "upward|downward|plateau|inflection|acceleration|deceleration"
```

### Step 2 — 横向比较结构化提取

从 L4 数据中提取 3-5 个最相关的参照案例：

```yaml
comparative_anchors:
  - case: "参照案例名称"
    similarity_score: 0.0-1.0
    key_difference: "与本案例的关键差异"
    applicable_pattern: "可迁移的模式或教训"
```

### Step 3 — 交叉洞察生成

对每个时间锚点与每个参照案例进行配对分析（配对数量由质量驱动，不设上限），筛选出有意义的交叉点：

```yaml
cross_analysis_matrix:
  for_each_pair:
    time_milestone: "时间锚点"
    comparative_case: "参照案例"
    cross_question: "该参照案例在此时间节点上的类似情境是如何演化的？"
    emergent_insight: "交叉后浮现的新洞察（若无意义则跳过）"
```

筛选规则：
- 若 time_milestone 的 trend_direction 与 comparative_case 在类似阶段的 trend 一致 → pattern_emergence
- 若两者趋势相反 → contrast_amplification
- 若参照案例的后续发展可为当前研究问题提供因果线索 → causal_transfer
- 若参照案例在类似阶段没有发生预期中的事件 → anomaly_detection

### Step 4 — 最少产出要求

从所有交叉对中，最终产出至少 3 条交叉洞察（若交叉对数不足 3，后续 AI 自行补足）。

---

## output_schema
> **JSON Schema 规范 (D2.4.1)**: 本节点 output_schema 遵循 `protocols/output-schema-spec.md` 定义的 JSON Schema 统一格式。字段类型遵循 JSON Schema Draft 2020-12 规范。

> **execution_params**: object  # 实际执行参数，必须达到 SKILL.md 规定的最低值（R2-05 防深度缩水）

```yaml
time_axis_milestones:
  - milestone: string
    timestamp: string
    significance: string
    trend_direction: "upward|downward|plateau|inflection|acceleration|deceleration"

comparative_anchors:
  - case: string
    similarity_score: 0.0-1.0
    key_difference: string
    applicable_pattern: string

cross_axis_insights:
  - insight_id: "CA-1"
    insight: "横纵交汇洞察描述"
    time_axis_point: "L2 时间轴的哪个节点触发了此洞察"
    compare_axis_point: "L4 横向比较的哪个案例触发了此洞察"

## 外部能力卡片引用

- **TC-081 Pol.is**: 在跨轴检查中，利用Pol.is的意见分组算法识别不同分析维度（如经济vs社会vs政治）上的意见一致性/冲突模式。详见 `knowledge/external-capabilities/TC-081-Polis.md`
    intersection_type: "pattern_emergence|contrast_amplification|causal_transfer|anomaly_detection"
    confidence: 0.0-1.0
    supporting_evidence: "支持该洞察的证据简述"
```

---

## self_check_before_output
> **量化标准 (D2.4.3)**: 本节点 self_check_before_output 遵循 `protocols/output-schema-spec.md` §4 定义的量化通过判据。self_check_score >= 85 方可输出。

- [ ] time_axis_milestones 是否至少 3 个？
- [ ] comparative_anchors 是否至少 3 个？
- [ ] cross_axis_insights 是否至少 3 条？
- [ ] 每条 cross_axis_insight 是否都有明确的 time_axis_point 和 compare_axis_point？
- [ ] intersection_type 分配是否准确（非随机选择）？
- [ ] 是否存在无意义的交叉对（即强行配对产生无实质洞察的对）？若有，是否已过滤？

---

## must_not

- 不得产出少于 3 条交叉洞察
- 不得使用相同或高度重复的洞察描述
- 不得跳过 intersection_type 标注
- 不得生成没有明确时间锚点和比较锚点的"悬浮洞察"

---

## knowledge_refs

- `knowledge/thinking-models/` — 领域思维模型库（按需参照）

## NRSF 追加指令

T07b 完成后，将散文式研究笔记追加到 NRSF-Full §T07b：
- 每段 150-300 字，段落级引用
- 包含交叉轴配对策略、洞察筛选逻辑、参照案例选择依据
- 遵循 nrsf-protocol.md 的散文式笔记格式

## 双阶段输出格式

### 阶段 A：结构化交叉轴分析

原有的 output_schema 格式输出，用于 Supervisor 检查。

### 阶段 B：散文式研究笔记

追加到 NRSF-Full §T07b 的散文式笔记，供下游消费。
