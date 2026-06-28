> **作者**: 阿洋

# 上下文传递协议 (Handoff Protocol) v3.0

> > **状态**: 正式发布
> **适用范围**: Profound Cognition 所有 Sub-Agent 间的数据传递
> **最后更新**: 2026-05-31
> **NRSF 模式**: 已激活 — 所有研究内容通过 NRSF §ref 机制传递，context_package 仅保留结构化元数据

---

## 1. 协议概述

### 1.1 目的

HandoffProtocol 定义了 Profound Cognition 中 Sub-Agent 之间的数据传递标准格式。该协议确保上游产出被压缩为精炼摘要后传递给下游，在下游获得足够上下文的同时，避免上下文窗口被无关细节填满。

### 1.2 核心设计原则

- **NRSF 追加优先**: 上游产出以完整散文式笔记追加到 NRSF 文档，通过 §ref 标记引用，不压缩不摘要
- **最小必要元数据**: context_package 仅传递结构化元数据（task_id、nrsf_path、gate 状态等），研究内容在 NRSF 中
- **§ref 精确引用**: 下游通过 §ref 标记精确读取所需上游内容，而非依赖压缩摘要
- **状态透明**: 每条上游产出标注 COMPLETED 或 RETRYING 状态
- **穷尽重试可见**: RETRYING 状态的上游必须标注缺失内容和处理建议

### 1.3 协议在系统中的位置

```
┌──────────────────────────────────────────┐
│ 主LLM (Phase 1 调度循环)                │
├──────────────────────────────────────────┤
│ assemble_context_package()               │
│   ├── 确认上游节点 NRSF §ref 标记        │
│   ├── 生成 nrsf_summary（仅 §ref 索引）  │
│   └── 提取关键结构化元数据               │
├──────────────────────────────────────────┤
│ context_package → Sub-Agent              │
│   ├── problem: 用户原始问题              │
│   ├── output_type: 成品类型              │
│   ├── task_id: 当前任务ID               │
│   ├── nrsf_path: NRSF 文档路径          │
│   └── upstream_refs: 上游 §ref 索引      │
├──────────────────────────────────────────┤
│ Sub-Agent 通过 §ref 读取 NRSF 内容       │
│   ├── 按 §ref 精确加载所需段落           │
│   ├── 不依赖压缩摘要                     │
│   └── 产出以 NODE 格式追加到 NRSF        │
└──────────────────────────────────────────┘
```

---

## 2. Context Package 标准格式

### 2.1 格式定义

> **v3 说明**: context_package 在 v3 中已重新定义为仅含元数据和 NRSF §ref 的轻量包装器，不再是结构性压缩方案。

```yaml
context_package:
  problem: "用户原始问题"
  output_type: "成品类型"
  task_id: "当前任务ID"
  nrsf_path: "nrsf/{research_id}.md"
  upstream_refs:
    - "§T09_1"   # T09 第1条推理路径
    - "§T09_2"   # T09 第2条推理路径
    - "§T10_1"   # T10 第1条反证
  gate_results:
    alpha: "pass|fail|pending"
    beta: "pass|fail|pending"
    gamma: "pass|fail|pending"
  discovery_log:
    - discovered_at: "T02"
      finding: "≤50字的精炼发现"
      nrsf_ref: "§T02_3"
      cross_reference_potential: "HIGH|MEDIUM|LOW"
      referenced_in: ["T03", "T09"]
      category: "factual|structural|contradiction|insight|reasoning"
```

### 2.2 字段详解

```yaml
fields:
  problem:
    type: string
    required: true
    description: "用户未经清洗的原始问题文本"
    max_length: 5000
    note: "始终传递完整原文，不压缩"

  output_type:
    type: enum
    required: true
    description: "成品类型枚举"
    values:
      - research_report
      - wechat_article
      - course_material

  task_id:
    type: string
    required: true
    pattern: "^(T|TM|I|T_)\\w+$"
    description: "当前任务的唯一标识符"
    examples: ["T02", "T01b", "T13", "T20a", "I01", "TM01", "T_gate_delta"]

  nrsf_path:
    type: string
    required: true
    description: "NRSF-Full 文档的绝对路径，下游通过此路径读取研究内容"

  upstream_refs:
    type: array
    required: true
    description: >
      当前任务所需上游节点的 §ref 标记列表。下游 Sub-Agent 根据此列表
      精确加载 NRSF 中对应段落，而非依赖压缩摘要。
      每个 §ref 指向 NRSF 中一个完整的推理路径或发现段落。
      不再使用 upstream_outputs.summary 压缩字段。

  gate_results:
    type: map
    required: true
    description: "各 Gate 门控的最新检查结果"

  upstream_outputs[].status:
    type: enum
    required: false
    values:
      - "COMPLETED"
      - "RETRYING"
    description: "上游任务的最终执行状态（保留用于状态追踪，研究内容通过 NRSF §ref 传递）"

  upstream_outputs[].retrying_note:
    type: string
    required: false
    condition: "仅在 status == 'RETRYING' 时必填"
    description: "标注缺失内容的具体说明和下游处理建议"
    fields:
      missing_content:
        type: string
        description: "缺失的具体内容描述"
      impact:
        type: string
        description: "对下游任务的预期影响"
      suggested_mitigation:
        type: string
        description: "建议下游采取的处理方式"

  discovery_log:
    type: array
    required: true
    description: "跨节点累积发现表。各 Sub-Agent 产出中的 new_discoveries 逐节点追加入此数组，传递所有已发现的关键洞察"
    max_entries: 50
    elements:
      discovered_at:
        type: string
        pattern: "^(T|TM|I|T_)\\w+$"
        description: "发现所在的任务ID"
      finding:
        type: string
        max_length: 50
        description: "精炼发现，≤50字，保留核心洞察不损失精度"
      nrsf_ref:
        type: string
        description: "该发现对应的 NRSF §ref 标记，用于精确追溯"
      cross_reference_potential:
        type: enum
        values: ["HIGH", "MEDIUM", "LOW"]
        description: "该发现与其他节点或层级的交叉引用潜力评级"
      referenced_in:
        type: array
        items: "T\\d{2}"
        description: "引用或验证了该发现的上游任务ID列表（随流水线推进逐步填充）"
      category:
        type: enum
        values: ["factual", "structural", "contradiction", "insight", "reasoning"]
        description: "发现类型：factual=事实性发现、structural=结构性发现、contradiction=矛盾性发现、insight=洞察性发现、reasoning=推理层发现（来自认知流水线推理节点的深层逻辑洞察）"
```

---

## 3. NRSF 追加规则（替代摘要压缩）

### 3.1 核心规则

```yaml
nrsf_append_rules:
  rule_1_no_compression:
    description: >
      上游产出不再压缩为摘要，而是以完整散文式笔记追加到 NRSF 文档。
      每个节点产出以 NODE 格式追加，包含完整推理路径和引用。
    enforcement: "Sub-Agent 完成后由 Orchestrator 验证 NRSF 追加完整性"

  rule_2_section_ref:
    description: "下游通过 §ref 标记精确加载所需段落，不从压缩摘要中读取"
    format: "§T{task_id}_{序号}"

  rule_3_append_only:
    description: "NRSF 文档只追加不删减，已有内容不可覆盖"

  rule_4_no_raw_output:
    description: "NRSF 中不得出现完整JSON或原始输出格式，必须为散文式笔记"
    enforcement: "不得出现未经解释的 {、[ 等结构化数据标记"

  rule_5_verbatim_facts:
    description: "事实性结论保留原文措辞，不得改写使精度降低"
    example:
      correct: "2024年全球GDP增长率为3.2%（IMF数据）"
      incorrect: "去年全球经济增长了约3个点"
```

### 3.2 §ref 引用规则

```yaml
ref_rules:
  description: >
    Orchestrator 根据下游任务的依赖关系决定传递哪些 §ref 标记。
    下游 Sub-Agent 通过 nrsf_path 加载 NRSF 文档，按 §ref 定位段落。

  mapping_examples:
    - downstream: "T02"
      upstream_refs:
        - "§T01_1"   # 问题定义
        - "§T00_1"   # 大纲范围

    - downstream: "T13"
      upstream_refs:
        - "§T09_1"   # 推理路径1
        - "§T09_2"   # 推理路径2
        - "§T10_1"   # 逻辑反证
        - "§T11_1"   # 证据缺口
        - "§T12_1"   # 范围边界

    - downstream: "T15"
      upstream_refs:
        - "§T01_1"   # 问题定义
        - "§T13_1"   # 综合结论
```

---

## 4. Context Package 长度约束

NRSF 模式下，研究内容通过 NRSF 文档传递，context_package 仅包含结构化元数据和 §ref 索引，不设长度上限。
NRSF-Full 文档的字数管理遵循 nrsf-protocol.md 的 NRSF 分层摘要机制章节。

---

## 5. RETRYING 上游处理规范

### 5.1 RETRYING 标注格式

```yaml
upstream_outputs:
  T05:
    summary: "L4对比分析部分完成，仅含欧美市场数据。"
    data:
      comparison_dimensions: ["市场份额", "增长率"]
    status: "RETRYING"
    retrying_note:
      missing_content: "亚太市场数据因来源不可用而缺失"
      impact: "下游比较分析将缺少亚太维度"
      suggested_mitigation: "建议下游T13在综合结论时标注'仅基于欧美数据'"
```

### 5.2 下游处理规则

````yaml
downstream_degradation_handling:
  rule_1_never_block:
    description: "下游任务不得因上游 RETRYING 而拒绝执行"
    action: "使用可用数据继续，标注缺口"

  rule_2_confidence_downgrade:
    description: "收到 RETRYING 上游时，下游应降低自身产出置信度"
    action: "在自身 confidence_score 中体现数据不完整性"

  rule_3_gap_marking:
    description: "在自身产出中明确标注因上游 RETRYING 导致的覆盖缺口"
    example: "本节分析仅限于欧美市场，亚太数据因T05穷尽重试不可用"

  rule_4_alternative_path:
    description: "如有替代数据路径，下游应使用替代方案"
    example: "T05 RETRYING → T13 改用 T02 原始数据直接做粗粒度对比"
````

---

## 6. 完整示例

### 6.1 T13 的 context_package 示例（NRSF 模式）

```yaml
context_package:
  problem: "中国新能源汽车产业未来五年的竞争格局将如何演变？"
  output_type: "research_report"
  task_id: "T13"
  nrsf_path: "nrsf/20260531-nev-competition.md"
  upstream_refs:
    - "§T09_1"   # 推理路径：电池技术迭代速度
    - "§T09_2"   # 推理路径：品牌溢价分化
    - "§T10_1"   # 反证：规模效应非唯一壁垒
    - "§T11_1"   # 反证：传统车企转型超预期
    - "§T12_1"   # 范围：地缘政治未纳入
  gate_results:
    alpha: "pass"
    beta: "pending"
    gamma: "pending"
```

### 6.2 包含 RETRYING 上游的示例（NRSF 模式）

```yaml
context_package:
  problem: "AI大模型对软件工程行业的影响评估"
  output_type: "research_report"
  task_id: "T17"
  nrsf_path: "nrsf/20260531-ai-se-impact.md"
  upstream_refs:
    - "§T13_1"   # 综合结论：AI编码工具效率提升
    - "§T15_1"   # 领域分析：科技领域（法律领域 RETRYING）
  gate_results:
    alpha: "pass"
    beta: "pass"
  retrying_log:
    - task: "T15"
      missing_content: "法律领域引擎因T15执行超时未能激活，缺失AI生成代码的版权归属、责任划分等法律分析"
      impact: "T17核查将缺少法律合规维度的交叉验证"
      suggested_mitigation: "在核查报告中标注'法律维度未覆盖'，降低该维度的核查完整性评分"
```

---

## 7. 跨节点发现累积表 (discovery_log)

### 7.1 概述

discovery_log 是 Profound Cognition 跨节点记忆的核心机制。各 Sub-Agent 产出的关键发现被逐节点累积传递给下游，使下游节点在综合推理时能引用流水线中所有已浮出的洞察，避免重复发现和关键信息丢失。

### 7.2 功能开关

discovery_log 在所有路径下始终启用，cross_node_memory 始终为 true。

### 7.3 累积传递规则

```yaml
discovery_log_rules:
  rule_1_accumulate:
    description: >
      主LLM在 Phase 1 执行循环中，每个 Sub-Agent 完成后提取其 output.new_discoveries，
      追加到当前累积的 discovery_log。discovery_log 随 context_package 传递给下一个 Sub-Agent。

  rule_2_downstream_must_receive:
    description: >
      下游节点必须接收上游累积的完整 discovery_log。
      不得删除、截断或选择性传递上游发现（即使下游节点自身不产出 new_discoveries）。

  rule_3_dedup:
    description: >
      主LLM在追加 new_discoveries 时执行简单去重：
      若新发现的 finding 与已有条目语义等同（≥80% 语义相似），
      则将新发现的 discovered_at 追加到已有条目的 referenced_in，不创建重复条目。

  rule_4_reference_tracking:
    description: >
      当任何 Sub-Agent 在其产出或推理中显式引用了 discovery_log 中的某个发现时，
      主LLM将该 Sub-Agent 的 task_id 追加到对应条目的 referenced_in 数组。

  rule_5_category_tagging:
    description: >
      category 字段由产出 new_discoveries 的 Sub-Agent 自行标注，
      主LLM无须修改。category 用于 T13 discovery_log 引用覆盖率计算时的加权评估。

  rule_6_cross_reference_potential:
    description: >
      cross_reference_potential 表示该发现被其他层级/节点引用的潜力。
      HIGH=可能被多个下游节点引用、MEDIUM=可能被1-2个下游节点引用、
      LOW=仅对当前节点局部有意义。
```

### 7.4 T13 引用覆盖率计算

T13 执行 discovery_log 引用检查时，按以下逻辑计算覆盖率：

```yaml
discovery_log_coverage:
  scope: "仅计算 cross_reference_potential == 'HIGH' 的发现"
  formula: "coverage = (HIGH级发现中被 referenced_in 包含 T13 或 T09~T12 的数量) / (HIGH级发现总数)"
  threshold:
    coverage >= 0.8: "引用充分，depth_satisfaction.score 中此维度计满分 0.25"
    coverage >= 0.5: "引用基本充分，depth_satisfaction.score 中此维度计 0.15（满分 0.25）"
    coverage < 0.5: "引用不足，depth_satisfaction.score 中此维度计 0.05，所有未引用的 HIGH 级发现写入 unsolved_tensions，标注 severity = critical"
  edge_case:
    description: "当 discovery_log 为空时，此维度自动满分 0.25，不扣分"
```

### 7.5 discovery_log 条目示例

```yaml
discovery_log:
  - discovered_at: "T02"
    finding: "日本失落的三十年并非单一泡沫破裂，而是人口+债务+通缩三重叠加"
    cross_reference_potential: "HIGH"
    referenced_in: ["T03", "T09", "T13"]
    category: "factual"

  - discovered_at: "T03"
    finding: "变量交互矩阵显示出口依存度与内需韧性之间存在阈值效应"
    cross_reference_potential: "HIGH"
    referenced_in: ["T04", "T13"]
    category: "structural"

  - discovered_at: "T04"
    finding: "主流叙事与技术悲观叙事在就业率预测上存在不可调和的分歧"
    cross_reference_potential: "HIGH"
    referenced_in: ["T13"]
    category: "contradiction"

  - discovered_at: "T05"
    finding: "政府刺激政策的乘数效应在债务GDP比率超90%后断崖式衰减"
    cross_reference_potential: "MEDIUM"
    referenced_in: []
    category: "insight"
```

---

## 8. §ref 直通字段传递规则

**§ref 直通字段在所有路径下始终启用，context_package 中始终传递 §ref 索引。**

### 8.1 适用条件

§ref 直通字段在所有路径下始终启用。

### 8.2 设计目的

T09/T10/T11/T12 三路对抗验证是质量最高的节点产出。在传递给 T13 综合节点时，核心结论通过 §ref 标记精确引用，T13 直接从 NRSF 文档按 §ref 加载完整推理路径，不依赖摘要压缩。此外，`discovery_log` 中 `cross_reference_potential = HIGH` 的关键发现也通过 §ref 通道传递至 T09 和 T13，确保多跳传递后关键上下文不丢失。

### 8.3 §ref 直通字段定义

| 字段 | 来源 | 格式 | 传递方式 |
|------|------|------|---------|
| critical_findings_refs | discovery_log (HIGH) | `[{nrsf_ref, finding, category, discovered_at}]` | context_package 中传递 §ref 索引，下游按需加载 |
| reasoning_paths_refs | T09 | `[{path_id, nrsf_ref}]` | context_package 中传递 §ref 索引 |
| logic_attack_refs | T10 | `[{attack_id, nrsf_ref}]` | context_package 中传递 §ref 索引 |
| evidence_gaps_refs | T11 | `[{gap_id, nrsf_ref}]` | context_package 中传递 §ref 索引 |
| scope_limits_refs | T12 | `[{limit_id, nrsf_ref}]` | context_package 中传递 §ref 索引 |

### 8.4 §ref 直通字段结构与传递规则

#### 8.4.1 critical_findings_refs

`discovery_log` 中 `cross_reference_potential = HIGH` 的关键发现通过 §ref 直通传递至 T09 和 T13。

```yaml
critical_findings_refs:
  description: "关键发现的 §ref 索引，下游从 NRSF 按需加载完整内容"
  eligibility: "discovery_log中cross_reference_potential = HIGH的发现"
  max_items: 10
  format: "nrsf_ref 索引，不压缩原始内容"
  target_nodes: [T09, T13]
```

**传递规则**：
1. 主LLM 在 assemble_context_package 阶段，从当前累积的 `discovery_log` 中筛选 `cross_reference_potential = HIGH` 的条目
2. 选取置信度最高的前 10 条（若超过 `max_items`），将其 `nrsf_ref` 放入 `critical_findings_refs`
3. §ref 索引随 `context_package` 传递给 T09 和 T13（其他节点不接收直通数据）
4. 下游按 §ref 从 NRSF 加载完整发现内容，无字数限制

#### 8.4.2 reasoning_paths_refs

T09 多路径推理产出的各路径核心结论通过 §ref 直通传递至 T13，T13 从 NRSF 加载完整推理路径。

```yaml
reasoning_paths_refs:
  description: "T09/T10/T11/T12 各推理路径的 §ref 索引直通至 T13"
  eligibility: "T09_cog_reason 的 reasoning_paths 输出，经 T10/T11/T12 魔鬼代言人反馈修正后的结论"
  max_paths: 7
  target_nodes: [T13]
```

**字段结构**：

```yaml
reasoning_paths_refs:
  - path_id: string
    nrsf_ref: string        # 对应 NRSF 中 §T09_N 标记
    confidence_ratings:
      - number
    vote_weight: number
```

**传递规则**：
1. T09 执行多路径推理后，将各推理路径追加到 NRSF 并生成 §ref 标记
2. T10/T11/T12 魔鬼代言人反馈后，更新对应路径的 confidence_ratings 和 vote_weight
3. T13 从 context_package.reasoning_paths_refs 读取 §ref 索引，按需从 NRSF 加载完整推理路径
4. 此字段始终激活

### 8.5 传递规则（T13 context_package 组装）

```yaml
context_package.critical_findings_refs = discovery_log中cross_reference_potential = HIGH的发现的 §ref 索引（上限10条）
context_package.reasoning_paths_refs = T09 各推理路径的 §ref 索引
context_package.logic_attack_refs = T10 各反证的 §ref 索引
context_package.evidence_gaps_refs = T11 各证据缺口的 §ref 索引
context_package.scope_limits_refs = T12 各范围边界的 §ref 索引
```

### 8.6 §ref 传递规则
- §ref 索引不计入 context_package 长度限制（仅为短字符串）
- T13 综合时先通过 §ref 从 NRSF 加载完整推理路径，再参考 discovery_log 的摘要
- NRSF 中对应段落无字数限制，保留完整推理过程

---

## 9. 工作模式差异（Work Mode Context Variants）

不同工作模式下，context_package 传递的内容有所不同：

| 字段 | EXHAUST-only | PLAN | EXECUTE | REVIEW | PATCH | RECOVERY |
|------|-------------|------|---------|--------|-------|----------|
| nrsf_path | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| upstream_refs | ✅ | ❌ | ✅ | ✅ | ✅ (部分) | ❌ (保留) |
| domain_depth | ✅ (full) | ✅ (outline) | ✅ (per-node) | ❌ | ❌ | ❌ |
| quality_report | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| render_config | ❌ | ❌ | ✅ | ❌ | ✅ | ✅ |
| rollback_target | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |

- **EXHAUST-only**：唯一研究模式，domain_depth = full，所有阶段穷尽执行
- **PLAN**：仅传递 outline 和路由决策上下文
- **PATCH**：额外传递 rollback_target 节点 ID 和修复目标描述
- **RECOVERY**：仅传递已完成的分析产出和渲染配置，不触发 DAG 重新执行

---

## 附录

### B. 术语表

| 术语 | 英文 | 定义 |
|------|------|------|
| Context Package | Context Package | Sub-Agent 间传递结构化元数据和 §ref 索引的标准化封装格式 |
| NRSF | Narrative Reference Stack Frame | 叙事式研究状态文件，承载所有研究内容，只追加不删减（A6.2-F7 修复，2026-06-27：缩写展开统一为 Narrative Reference Stack Frame，与 protocols/nrsf-protocol.md 权威定义对齐） |
| §ref | Section Reference | NRSF 中的段落引用标记，格式为 §T{task_id}_{序号}，下游按此精确加载内容 |
| 上游产出 | Upstream Output | 当前任务依赖节点产生的已完成输出 |
| NRSF 追加 | NRSF Append | 将节点产出以 NODE 格式追加到 NRSF 文档的过程，不压缩 |
| RETRYING | RETRYING | 节点因超时/重试耗尽等原因标记的穷尽重试状态 |

### C. 交叉引用

- [execution-protocol.md](./execution-protocol.md) — Phase 0-3 执行规则
- [exhaust-retry-protocol.md](./exhaust-retry-protocol.md) — 节点失败穷尽重试策略
- [nrsf-protocol.md](./nrsf-protocol.md) — NRSF 叙事式研究状态文件协议

---

## 隐式依赖声明

以下依赖关系未在 DAG 模板的 deps 字段中显式声明，但通过 NRSF §ref 传递数据：

| 依赖 | 传递方式 | 数据格式 | 对齐要求 |
|------|----------|----------|----------|
| T25 → T05 | NRSF §ref (stakeholder_groups) | YAML/JSON | T05 输出须含 stakeholder_groups 字段 |
| T26 → T03 | NRSF §ref (literature_entities) | YAML/JSON | T03 输出须含 literature_entities 字段 |
| T25 Step5 → T24 | NRSF §ref (equilibrium_analysis) | YAML/JSON | T24 输出须含 equilibrium_analysis 字段 |

### 数据格式对齐规则

1. **T05 → T25**: T05 输出的 stakeholder_groups 必须包含 {name, type, interests, influence_level} 字段
2. **T03 → T26**: T03 输出的 literature_entities 必须包含 {entity, type, source_paper, confidence} 字段
3. **T24 → T25 Step5**: T24 输出的 equilibrium_analysis 必须包含 {equilibrium_type, stability, conditions} 字段

### 隐式依赖验证

在 handoff_protocol 执行时，如果检测到隐式依赖的目标节点即将执行，但 context_package 中缺少对应 §ref，则：
1. 发出 WARN 级别告警
2. 尝试从上游节点的 NRSF 段落中提取
3. 如果提取失败，标记目标节点的对应步骤为 PARTIAL 执行

---

## T22-T28 数据契约字段组

### T22 → T23 系统动力学传递

```yaml
t22_to_t23:
  variables:
    stock: [{name, definition, data_available}]
    flow: [{name, definition, data_available}]
    exogenous: [{name, definition}]
    parameter: [{name, definition}]
  causal_loop_diagram:
    reinforcing_loops: [{id, description, polarity, delay}]
    balancing_loops: [{id, description, polarity, delay}]
  cib_matrix:
    available: bool
    dimensions: str
    consistency_score: float|null
  dimension_coverage:
    C9: str
    note: str
  exhaust_retry: str
  exhaust_retry_reason: str|null
```

### T22 → T25 系统动力学传递

```yaml
t22_to_t25:
  causal_loop_diagram:
    reinforcing_loops: [{id, description, polarity, delay}]
    balancing_loops: [{id, description, polarity, delay}]
  leverage_points: [{level, name, description, intervention_type}]
  system_archetypes:
    matched: [{name, description, loops_involved}]
  exhaust_retry: str
  exhaust_retry_reason: str|null
```

### T23 → T25 因果验证传递

```yaml
t23_to_t25:
  hypotheses_verified: [{cause, effect, mechanism, ate, cate, robustness, evidence_level}]
  counterfactual_scenarios: [{hypothesis_id, scenario, expected_outcome, actual_outcome, effect_size}]
  contradictions: [{type, description, source_T09, source_T22}]
  dimension_coverage:
    C10: str
  exhaust_retry: str
  exhaust_retry_reason: str|null
```

### T23 → T26 因果验证传递

```yaml
t23_to_t26:
  contradictions: [{type, description, source_T09, source_T22}]
  sensitivity_analysis:
    e_value: float|null
    confounding_robustness: str
  exhaust_retry: str
  exhaust_retry_reason: str|null
```

### T24 → T25 对抗综合传递

```yaml
t24_to_t25:
  consensus_map:
    full_consensus: [str]
    partial_consensus: [str]
    key_disagreements: [str]
  hidden_assumptions: [{assumption, revealed_by, reasonability, risk}]
  safety_analysis:
    harm_patterns: [str]
    ethical_risks: [str]
    gt_harmbench_alignment: bool
  equilibrium_analysis:
    equilibrium_type: str
    stability: str
    conditions: [str]
  exhaust_retry: str
  exhaust_retry_reason: str|null
```

### T25 → T26 情景规划传递

```yaml
t25_to_t26:
  key_uncertainties: [{name, source, type, impact}]
  scenarios: [{name, axis_values, narrative, consistency_score, equilibrium_state}]
  wild_cards: [{event, probability, impact, scenario_impact}]
  robust_strategies: [str]
  exhaust_retry: str
  exhaust_retry_reason: str|null
```

### T26 → T27 元认知反思传递

```yaml
t26_to_t27:
  cynefin:
    domain: str
    justification: str
    methodology_implications: [str]
  cognitive_biases: [{bias_name, affected_step, impact, mitigation}]
  ethics_analysis:
    dilemmas: [str]
    recommendations: [str]
  cognitive_boundaries: [{boundary, type, impact_on_conclusions}]
  dimension_coverage:
    M1_M6: {M1: str, M2: str, M3: str, M4: str, M5: str, M6: str}
    P1_P6: {P1: str, P2: str, P3: str, P4: str, P5: str, P6: str}
  exhaust_retry: str
  exhaust_retry_reason: str|null
```

---
© 阿洋

## 穷尽重试策略

### L1: 完整context_package组装
正常执行handoff协议，组装完整context_package

### L2: context_package部分组装失败
- 持续重试直至上下文传递完整，不设上限

### L3: context_package组装不可用
- 持续重试直至上下文传递完整，不设上限

### L4: 上下文传递完全不可用
- 持续重试直至上下文传递完整，不设上限


---

## 测试用例 (D3.4.4)

### 测试用例 1：Context Package 标准格式

**给定输入**：T02 完成执行，产出包含 task_id、output、nrsf_refs、execution_params。

**应产出**：Context Package 包含 task_id=T02、output（JSON Schema 校验通过）、nrsf_refs（≥1 条 §ref）、execution_params（非空），格式符合 handoff-protocol 规范。

### 测试用例 2：上游引用解析

**给定输入**：T09 的 context_package 引用 §ref:T02:main_narrative 和 §ref:T05:evidence_summary。

**应产出**：Orchestrator 解析两个 §ref，从 NRSF 中提取对应叙事片段，注入 T09 的 context_package.upstream_refs。

### 测试用例 3：§ref 不存在报错

**给定输入**：T09 引用 §ref:T02:nonexistent_narrative（该 narrative_id 不存在于 NRSF）。

**应产出**：报错"§ref:T02:nonexistent_narrative not found in NRSF"，不静默跳过。
