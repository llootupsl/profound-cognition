# 认知流水线理论

> **模块标识**: `knowledge/cognitive-framework`
> **作者**: 阿洋
> **依赖**: `knowledge/research-methods`
> **核心能力**: 57节点DAG编排 + 14维全息框架 + §1-§8结构 + 5个Phase（Phase 1/2/3/4/7）+ Long CoT多路径推理 + 7项收敛清单

---

## 1. 概述

认知流水线是 Profound Cognition 框架的认知处理核心，融合 Long Chain-of-Thought (Long CoT) 范式实现多路径深度推理。它贯穿从问题输入到结构化报告产出的完整认知链路。本框架以 **57 节点 DAG** 为编排骨架，以 **14 维全息框架** 为内容覆盖标准，以 **§1-§8 结构** 为交付形态，通过 **5 个 Phase**（Phase 1 研究底座层 / Phase 2 认知流水线层 / Phase 3 领域分析与质量保障层 / Phase 4 输出渲染与交付层 / Phase 7 元维度引擎+科学层）逐层推进。

### 1.0 核心概念：14 维全息框架与元维度

**14 维全息框架** 是本框架的内容覆盖标准，确保研究无盲区。前 8 维构成 §1-§3 全息核心，后 6 维（维度 9-14）为**元维度**扩展，对应 §6 元维度扩展章节：

| 维度编号 | 维度名称 | 所属章节 | 类型 |
|---------|---------|---------|------|
| 1-4 | 问题认知与定义（4 维） | §1 | 全息核心 |
| 5-8 | 全维全域分析（4 维）+ 极限决策推理（2 维） | §2/§3 | 全息核心 |
| 9-10 | 无知之学 + 认知神经心理学 | §6 | 元维度 |
| 11-12 | 二阶方法论 + 深度时间思维 | §6 | 元维度 |
| 13-14 | 悲剧性智慧 + 知识生命体化 | §6 | 元维度 |

**元维度**（Meta-dimensions）是超越常规分析维度的"关于维度本身的维度"，包括：对无知的元认知（维度 9-10）、对方法论的方法论反思（维度 11-12）、对知识本体的存在论审视（维度 13-14）。元维度扩展由 Phase 7 的 `T_meta_dim_9_10`、`T_meta_dim_11_12`、`T_meta_dim_13_14` 三个节点执行。

**§1-§8 结构** 是最终交付报告的不可变骨架：
- §1 问题认知与定义（≥8000 字）
- §2 全维全域分析（≥22000 字）
- §3 极限决策推理（≥8000 字）
- §4 元层综合（≥8000 字）
- §5 科学深度层（≥30000 字）
- §6 元维度扩展（≥12000 字）
- §7 哲学内核三元组（≥6000 字）
- §8 未来研究议程（≥6000 字）

### 1.1 核心融合技术

| 技术 | 说明 |
|------|------|
| **Long CoT 长链推理** | 深度推理 + 广泛探索 + 可行反思，不在表面结论处停止 |
| **自适应分支** | 不确定性节点自动触发多路径探索，节省75-85%推理资源 |
| **多视角协同** | 关键认知节点自动切换2-3个分析视角，识别单一视角盲区 |
| **自反思回环** | Draft → Critique → Revision 三阶段迭代精炼 |
| **深度优先 + 广度优先双模** | 高确定性方向深度挖掘，高不确定性方向广度覆盖 |

### 1.2 架构总览

本框架采用 **57 节点 DAG**（有向无环图）编排，分布于 5 个 Phase：

```
Phase 1 — 研究底座层 (15 nodes)
  T_env_probe → T00a → T01(输入分流) → T01b → T01c → T01d → T00 → T02~T06
  九层研究底座 L1-L9 逐层递进，建立研究基线

Phase 2 — 认知流水线层 (9 nodes)
  T07 → T08(认知解构) → T09(多路径推理,7条) → T10/T11/T12(三路对抗) → T12b → T13 → I01 → T14
  Long CoT 多路径推理 + 三路对抗验证

Phase 3 — 领域分析与质量保障层 (8 nodes)
  T15~T19 领域引擎分析 + 质量保障 + 自评

Phase 4 — 输出渲染与交付层 (6 nodes)
  T20a/T20b/T20c 渲染 + T22~T28 全息框架章节生成 + 交付

Phase 7 — 元维度引擎 + 科学层 (19 nodes)
  T22~T28(14维全息框架) + T_meta_dim_9_10/11_12/13_14(元维度) + T_philosophical_core(哲学三元组) + TM01~TM07(科学层7模块)
  14维全息框架覆盖 + 元维度扩展 + 科学深度层
```

**57 节点 DAG 核心节点说明**（与 SKILL.md 拓扑定义一致）：

| 节点ID | 节点名称 | 所属Phase | 功能 |
|--------|---------|----------|------|
| T01 | 输入分流 | Phase 1 | 对象分类+偏见扫描+敏感度+文化材料判定 |
| T01b | 写作声音校准 | Phase 1 | always 路由，覆盖全部 output_type |
| T01c | 输入情绪基调提取 | Phase 1 | 情绪基调与风格偏好识别 |
| T05 | L6+L7证据利益 | Phase 1 | L6 证据边界 + L7 利益相关者 |
| T09 | 多路径推理(7条+MPEP) | Phase 2 | 7条推理路径 + Multi-Path Exploration with Branch Pruning |
| T10 | 魔鬼代言人-逻辑攻击 | Phase 2 | 逻辑维度攻击结论 |
| T11 | 魔鬼代言人-证据攻击 | Phase 2 | 证据维度攻击结论 |
| T12 | 魔鬼代言人-范围攻击 | Phase 2 | 范围维度攻击结论 |
| T13 | 认知综合+深度信号扫描 | Phase 2 | 3轮递归+direct_passthrough |
| TM01~TM07 | 科学层7模块 | Phase 7 | 系统动力学/因果验证/多智能体对抗/情景规划/元认知/覆盖验证/本体导出 |
| T_meta_dim_9_10/11_12/13_14 | 元维度扩展 | Phase 7 | 维度9-14元维度分析 |
| T_philosophical_core | 哲学内核三元组 | Phase 7 | 哲学三元组 |

---

## 2. 认知流水线（对应 Phase 2 多路径推理）

> **注意**：本节描述的认知流水线对应 57 节点 DAG 中的 Phase 2 节点（T08-T14）。下方"T01-T12"为本节理论描述的历史编号，**与 DAG 节点 T01（输入分流）、T05（L6+L7证据利益）、T09（多路径推理）、T10（魔鬼代言人-逻辑攻击）等不是同一指代**。为避免混淆，下方括号标注对应的 DAG 节点。

### Step 1: 问题解构

**目标**: 将模糊、复杂的原始问题转化为结构化的子问题清单，同时识别所有隐含假设。

**操作**:
- [DAG T08 认知解构] 递归问题分解：执行 L1 层问题分解，生成结构化子问题树
- [DAG T08 认知解构] 隐含假设挖掘：对每个子问题进行假设扫描，输出假设清单

**输出结构**:
```yaml
step_1_deconstruction:
  core_question: "精炼后的核心问题"
  sub_questions:
    - id: "SQ-001"
      text: "子问题文本"
      priority: "high/medium/low"
      type: "factual/analytical/evaluative/creative"
      assumptions:
        - id: "ASM-001"
          statement: "假设陈述"
          type: "explicit/implicit/hidden"
          criticality: "critical/significant/minor"
          testable: true/false
      dependencies: ["SQ-002"]
  mece_compliance:
    mutually_exclusive: true
    collectively_exhaustive: true
```

**质量门控 QG1** - 通过标准：
- 子问题满足 MECE 原则
- 隐藏假设识别率 >= 80%
- 每个子问题有明确的依赖或独立标注
- 高优先级子问题不超过总数的30%

**注意**: 在 Step 1 之前，必须先完成研究底座 L1-L4。L5-L9 可在流水线执行中并行完成。

---

### Step 2: 假设推演

**目标**: 对 Step 1 识别的关键假设进行反事实推演和本质追溯，建立假设之间的逻辑关系。

**操作**:
- T03 反事实推演器：对每个关键假设执行"如果...不成立"的反事实推演
- T04 第一性原理拆解器：将问题拆解到不可再分的基本事实

**输出结构**:
```yaml
step_2_hypothesis_reasoning:
  counterfactuals:
    - assumption_id: "ASM-001"
      original: "原假设"
      negation: "反事实前提"
      implications:
        - chain: "推演链"
          impact: "high/medium/low"
          probability: 0.0-1.0
      conclusion: "反事实结论"
      robustness: "robust/fragile/unknown"
  first_principles:
    - domain: "领域"
      axioms: ["基本事实/公理"]
      derived_principles: ["推导出的原理"]
      confidence: 0.0-1.0
  variable_matrix:
    key_variables:
      - name: "变量名"
        type: "independent/dependent/confounding"
        range: "取值范围"
        sensitivity: "high/medium/low"
```

**质量门控 QG2** - 通过标准：
- 关键变量覆盖率 >= 90%
- 每个关键假设必须有对应的反事实推演（覆盖率100%）
- 每个推导链至少有一个公理级锚点
- 高敏感度变量全部标注

---

### Step 3: 正反论证

**目标**: 对推演结论进行多视角辩论、攻击性检验、偏见检测和事实核查，最终整合为稳健结论。

**操作**:
- T05 多视角辩论引擎：至少3个不同立场对结论进行辩论
- T06 结论攻击器（魔鬼代言人）：主动寻找结论漏洞
- T07 认知偏差检测器：检测8种核心偏差
- T08 事实验证器：对关键事实声明进行核查
- T09 共识整合器：整合多方观点，形成最终共识

**输出结构**:
```yaml
step_3_adversarial_validation:
  perspectives:
    - stance: "立场描述"
      arguments: ["论点"]
      evidence_strength: 0.0-1.0
  attacks:
    - target_conclusion: "被攻击的结论"
      attack_type: "logic_flaw/evidence_gap/counter_example/scope_overreach"
      severity: "critical/significant/minor"
      rebuttal: "反驳/修复"
      status: "resolved/unresolved/mitigated"
  bias_report:
    detected_biases:
      - type: "偏差类型"
        location: "出现位置"
        severity: "high/medium/low"
        mitigation: "缓解措施"
  fact_checks:
    - claim: "事实声明"
      verdict: "verified/unverified/refuted/uncertain"
      confidence: 0.0-1.0
  evidence_ledger:
    - argument: "论点"
      source: "来源"
      source_grade: "EA/EB/EC/ED/EE"
      support_strength: "strong/moderate/weak"
      counter_evidence: "反证标注"
  consensus:
    agreed_conclusions: ["共识结论"]
    contested_points: ["争议点"]
    remaining_uncertainties: ["未解决问题"]
```

**质量门控 QG3** - 通过标准：
- 结论攻击覆盖率 = 100%
- 高/中 severity 偏差全部有缓解措施
- 关键声明核查率 = 100%
- 争议点解决率 >= 80%
- **证据账本门控**: Step 3 完成后必须输出证据账本（evidence_ledger），至少5行

---

### Step 4: 报告生成

**目标**: 将全部认知过程的结构化输出整合为最终报告，包含溯源标注和可视化图表。

**操作**:
- [DAG T13 认知综合] 引用溯源：为每个结论标注证据来源和推导路径
- [DAG T13 认知综合] 结构可视化：生成论证结构图、因果图、置信度热力图

**输出结构**:
```yaml
step_4_report:
  metadata:
    question: "原始问题"
    pipeline_depth: "实际执行的递归层数"
  executive_summary: "执行摘要（300字以内）"
  conclusions:
    - id: "CON-001"
      statement: "结论陈述"
      confidence: 0.0-1.0
      evidence_chain: ["证据链引用ID"]
      provenance:
        sources: ["原始来源"]
        derivation_path: "推导路径"
      assumptions_depended: ["依赖假设"]
  visualizations:
    - type: "argument_map/causal_graph/confidence_heatmap/timeline"
      data: {}
  appendix:
    full_assumption_list: []
    full_evidence_matrix: []
    quality_gate_results: {}
```

---

## 3. 递归深挖机制

### 3.1 七层递归框架

认知流水线的每个步骤内部，递归深挖引擎按以下七层执行深度推理：

```
L1 问题解构 ──→ L2 证据收集 ──→ L3 模式识别 ──→ L4 因果推理
                                                    │
L7 元认知反思 ←── L6 跨域综合 ←── L5 反证检验 ←────────┘
```

**L1 问题解构**: 将核心问题分解为 MECE 子问题清单，识别关键维度和依赖关系。

**L2 证据收集**: 为每个子问题从多源收集证据，构建证据矩阵，标注可靠性、冲突和缺口。

**L3 模式识别**: 从证据中识别有意义的模式、趋势和规律，区分强模式和弱模式，识别异常值。

**L4 因果推理**: 构建有向无环因果图（DAG），区分直接/间接/虚假因果，识别混淆变量和中介变量。

**L5 反证检验**: 对因果结论进行系统性反证攻击，评估结论存活率，标注开放问题。

**L6 跨域综合**: 引入至少2个相关领域知识，进行跨域映射和类比推理，识别单领域盲区。

**L7 元认知反思**: 审视整个分析过程的方法论局限，量化不确定性，评估偏差，定义适用边界。

### 3.2 认知跃迁标准 (CL1-CL6)

每层间过渡必须满足认知跃迁评分 >= 0.7，否则必须回溯修正。

| 编号 | 标准 | 权重 | 通过阈值 | 检测方法 |
|------|------|------|---------|---------|
| CL1 | 信息增量 | 0.25 | 新增信息占比 >= 20% | 集合差计算 |
| CL2 | 维度扩展 | 0.15 | 至少新增1个分析维度 | 维度集合差 |
| CL3 | 逻辑递进 | 0.20 | 第N+1层引用并转化第N层核心结论 | 依赖链路检测 |
| CL4 | 确定性变化 | 0.15 | 至少1个结论置信度变化 >= 0.1 | 置信度差值 |
| CL5 | 视角转换 | 0.10 | 至少1个分析视角与上层不同 | 视角集合差 |
| CL6 | 可验证性 | 0.15 | 核心结论100%有验证方案 | 验证方案覆盖率 |

**综合评分公式**:
```
Leap_Score = 0.25×CL1 + 0.15×CL2 + 0.20×CL3 + 0.15×CL4 + 0.10×CL5 + 0.15×CL6
Leap_Score >= 0.7 → 有效跃迁，继续 | < 0.7 → 回溯修正
```

### 3.3 五项禁止规则 (P1-P5)

以下行为严格禁止，检测到必须回溯修正：

| 编号 | 禁止行为 | 检测方法 |
|------|---------|---------|
| P1 | 信息重组伪装新发现 | Jaccard相似度 >= 0.95 |
| P2 | 同一结论换述 | 语义相似度 >= 0.95 且无信息增量 |
| P3 | 无证据支持的推测升级 | 置信度提升 >= 0.3 未引入新证据 |
| P4 | 循环论证 | 论证依赖图存在环路 |
| P5 | 无关维度扩展 | 新维度与核心问题相关性 < 0.3 |

### 3.4 四项执行约束

| 约束 | 规则 | 示例 |
|------|------|------|
| C1 不可压缩 | 不可合并层级 | 禁止 L1+L2 合并执行 |
| C2 不可重复 | 同一层不可执行两次 | 不达标必须回溯到前一层 |
| C3 不可跳过 | 中间层级必须全部执行 | 不可 L1→L3 跳过 L2 |
| C4 不可降低标准 | 不可提前终止 | 初始决定深度不可下调 |

---

## 4. 7项收敛清单 (C1-C7)

递归终止的唯一有效条件：全部7项通过。任一项不通过，必须继续递归深挖或切换分析维度。

### C1: 证据穷尽检查

**问题**: 本次递归涉及的所有可检索事实是否已全部检索？

**通过标准**: 已穷尽所有可检索的关键事实来源，无遗漏的主要证据线索。

**不通过标准**: 存在已知可获取但未检索的证据来源；存在可预见的搜索方向但未探索。

**不通过行动**: 继续递归，补充缺失的证据检索。

---

### C2: 反事实推演检查

**问题**: 是否已对每个核心结论执行至少1个反事实推演？

**通过标准**: 每个核心结论至少通过了1次反事实检验，反事实推演覆盖了结论的成立条件检验。

**不通过标准**: 有核心结论未执行反事实推演；反事实推演停留在表面，未真正检验结论边界。

**不通过行动**: 继续递归，补充反事实推演。

---

### C3: 多维度覆盖检查

**问题**: 是否已从至少5个不同分析维度审视问题？

**通过标准**: 已从经济/政治/社会/文化/技术/心理/历史/生态等至少5个维度分析，各维度产出有实质内容。

**不通过标准**: 分析维度不足5个；某些维度仅有标签而无实质分析。

**不通过行动**: 继续递归，补充缺失的分析维度。

---

### C4: 矛盾解决检查

**问题**: 分析中是否存在未解决的自相矛盾？

**通过标准**: 所有已识别的矛盾均已解释（陈述矛盾产生的原因和条件）或标注为开放问题（明确承认无法当前解决）。

**不通过标准**: 存在已发现但未处理的矛盾；存在隐含但未识别的矛盾。

**不通过行动**: 继续递归，解决或标注未解决的矛盾。

---

### C5: 替代解释排除检查

**问题**: 是否已提出并排除至少2个主要的替代解释？

**通过标准**: 至少2个替代解释已被认真检验（检查其证据支持、逻辑一致性和解释力）并被合理排除，而非仅被提及后忽略。

**不通过标准**: 替代解释不足2个；替代解释仅被草率提及而未严格检验。

**不通过行动**: 继续递归，提出和严格检验替代解释。

---

### C6: 不确定性量化检查

**问题**: 是否已对每个核心结论标注了不确定性和置信区间？

**通过标准**: 每个核心结论附带不确定性评估（高/中/低可信度及置信度描述），不确定性来源已被识别。

**不通过标准**: 核心结论缺乏不确定性标注；不确定性描述模糊笼统。

**不通过行动**: 继续递归，量化不确定性。

---

### C7: 知识边界标记检查

**问题**: 是否已标注已知/已知未知/未知未知的知识边界？

**通过标准**: 已明确标注已知之已知（确证知识）、已知之未知（已识别缺口）、未知之未知（可能遗漏的领域），每个标注有具体内容。

**不通过标准**: 知识边界标注缺失或仅为形式化声明而无实质内容。

**不通过行动**: 继续递归，映射知识边界。

---

### 收敛清单协议

```
执行流程:
每层递归完成后 → 逐项检查 C1-C7 → 记录每项通过/不通过状态

终止条件:
全部7项通过 + 已完成至少5层递归 → 允许终止

维度切换触发:
任意3项连续2层未通过 → 触发维度切换（变换分析角度重新递归）

禁止行为:
"连续2层无CL≥0.5" → 维度切换信号，不是终止理由
"证据支持度<0.4" → 应触发新搜索方向
"推理循环" → 应切换到新分析维度
```

---

## 5. Long CoT多路径推理

### 5.1 推理深度控制

```
表层答案 → 不得停止，必须追问为什么、还有什么、是否有反例
   ↓
机制层   → 追问该机制的前提条件、边界、替代机制
   ↓
基础层   → 检讨理论本身的假设、适用条件和争议
   ↓
边界层   → 标注可验证事实边界，记录已确认和未确认部分
```

### 5.2 多路径探索与自适应分支

**分支必要性评估**:
- 存在 >= 2个看似合理的不同结论 → 分支
- 证据支持度 < 0.7 → 分支
- 存在不同视角可能挑战当前结论 → 分支
- 节点在主线关键路径上 → 分支
- 3次独立推理一致性 < 0.7 → 分支（Self-Consistency）

**分支规则**: 最大分支数5条，每分支最大深度3层。所有分支必须收敛比较，选择最优路径，被淘汰路径中独特洞见融入主路径。

**剪枝规则**:
- 连续2步未产生新证据 → 标记证据不足后剪枝
- 内部出现不可调和矛盾 → 标记逻辑失败后剪枝
- 累积置信度 < 0.3 → 标记低概率后剪枝

### 5.3 多视角协同验证

**三视角强制检验**:
1. **建设性支持者**: 寻找支持当前结论的证据和逻辑
2. **严格批评者**: 寻找漏洞、反例和逻辑缺陷
3. **中立观察者**: 无预设立场评估两方论证质量

**三阶段执行**: 独立分析轮 → 交叉批评轮 → 收敛综合轮

### 5.4 自反思回环

```
Draft（草稿生成）→ Critique（自我批评）→ Revision（修订精炼）
                         ↑____________________________↓
                        (质量驱动迭代，直至无新增问题方可退出)
```

**批评维度**: 未检查的假设、证据链完整性、逻辑漏洞、确认偏误痕迹、未考虑的框架、适用范围界定。

### 5.5 深度优先与广度优先双模

**深度优先模式**: 适用条件：确定性较高，证据支持度 >= 0.7。行为：沿当前方向持续深挖。

**广度优先模式**: 适用条件：高不确定性，证据支持度 < 0.7。行为：展开多个方向并行探索，收敛后选择主方向。

**模式切换**: 找到证据支持度 >= 0.8 的方向 → 广度转深度。证据支持度下降到 < 0.5 → 深度转广度。

---

## 6. 认知技术集成（对应 57 节点 DAG）

> **注意**：下表为认知流水线理论中的技术映射，"理论编号"列为本节历史编号，"对应DAG节点"列映射到 57 节点 DAG 中的实际节点。DAG 节点 T01=输入分流（非递归问题分解器）、T05=L6+L7证据利益（非多视角辩论引擎）、T09=多路径推理（非共识整合器）、T10=魔鬼代言人-逻辑攻击（非引用溯源器）。

| 理论编号 | 技术名称 | 所属步骤 | 功能 | 对应DAG节点 |
|------|---------|---------|------|------------|
| 理论-T01 | 递归问题分解 | Step 1 | MECE原则递归分解 | T08 认知解构 |
| 理论-T02 | 隐含假设挖掘 | Step 1 | 三层假设扫描（显性/隐性/隐藏） | T08 认知解构 |
| 理论-T03 | 反事实推演 | Step 2 | "如果...不成立"推演 | T09 多路径推理 |
| 理论-T04 | 第一性原理拆解 | Step 2 | 追溯至不可再分的基本事实 | T09 多路径推理 |
| 理论-T05 | 多视角辩论 | Step 3 | 至少3个立场结构化辩论 | T09 多路径推理 |
| 理论-T06 | 结论攻击（魔鬼代言人） | Step 3 | 魔鬼代言人漏洞检测 | T10 魔鬼代言人-逻辑攻击 |
| 理论-T07 | 认知偏差检测 | Step 3 | 8种核心偏差扫描 | T09 多路径推理 |
| 理论-T08 | 事实验证 | Step 3 | 独立核查与真伪判定 | T09 多路径推理 |
| 理论-T09 | 共识整合 | Step 3 | 多源整合与争议标注 | T13 认知综合 |
| 理论-T10 | 引用溯源 | Step 4 | 完整证据溯源链 | T13 认知综合 |
| 理论-T11 | 结构可视化 | Step 4 | 论证结构图/因果图等 | T13 认知综合 |
| 理论-T12 | 多格式解析 | 输入预处理 | 多格式标准化输入 | T01 输入分流 |

> **DAG 节点命名澄清**（避免与理论编号混淆）：
> - **DAG T01 = 输入分流**（对象分类+偏见扫描+敏感度+文化材料判定），非"递归问题分解器"
> - **DAG T05 = L6+L7证据利益**（L6 证据边界 + L7 利益相关者），非"多视角辩论引擎"
> - **DAG T09 = 多路径推理**（7条推理路径+MPEP），非"共识整合器"
> - **DAG T10 = 魔鬼代言人-逻辑攻击**（逻辑维度攻击结论），非"引用溯源器"

---

## 7. 流水线配置与终止条件

### 7.1 统一执行配置

所有任务默认执行完整深度研究流水线，不区分复杂度等级。

```yaml
pipeline_config:
  quality_gate_threshold: 0.8
  max_retries_per_gate: null  # EXHAUST 模式：不设重试上限，持续重试直至通过
  timeout_per_step_ms: 300000
  parallel_execution:
    step2_parallel: true
    step3_parallel: true
```

### 7.2 终止条件（严格限定）

```
允许终止的唯一条件:
├─ 每步完成 + 7项收敛清单全部通过 + 已完成至少5层递归
│
├─ 注意：以下不是终止条件：
│  • "连续2步无CL≥0.5" → 触发维度切换的信号
│  • "证据支持度<0.4" → 触发新搜索方向
│  • "推理循环" → 切换到新分析维度
│
└─ 深度有强制底线：至少完成完整四步 + 5层递归，低于此数视为执行失败
```

---

## 8. SOAR 认知架构参考（v3 新增）

> **来源**: SOAR Cognitive Architecture (Laird, 2012)
> **用途**: 为 profound-cognition 的 57 节点 DAG + 5 个 Phase 架构提供认知科学理论基础

### 8.1 三层抽象

SOAR 将认知系统分为三个抽象层次：

| 层次 | SOAR 定义 | profound-cognition 对应 |
|------|----------|------------------------|
| **知识级 (Knowledge Level)** | 基于"理性原则"的行为描述——系统做什么，为什么做 | Phase 1（T00-T07）：输入解析、问题解构、证据收集 |
| **符号级 (Symbol Level)** | 知识的具体表示和推理操作——系统如何表示和处理知识 | Phase 2-3（T08-T19）：推理演绎、验证对抗、知识整合 |
| **实现级 (Implementation Level)** | 底层硬件/软件实现 | Phase 4（T20a-c）输出渲染 + Phase 7（T22-T28, TM01-TM07）元维度扩展与科学层深挖 |

### 8.2 核心机制映射

| SOAR 机制 | 定义 | profound-cognition 对应 |
|-----------|------|------------------------|
| **工作记忆 (Working Memory)** | 当前激活的知识状态 | NRSF 文档当前 § 节内容 |
| **长期记忆 (Long-term Memory)** | 持久化规则和事实 | NRSF-Full 完整文档 + 知识图谱 |
| **决策循环 (Decision Cycle)** | 提议→评估→选择的认知循环 | DAG 节点执行→Gate 判定→Supervisor 验收 |
| **僵局驱动学习 (Impasse-driven Learning)** | 遇到未知状态时触发子目标学习 | depth_signal 触发深递归 |
| **组块化 (Chunking)** | 将问题解决经验转化为新规则 | 认知跃迁（CL1-CL6）记录 |

### 8.3 设计依据

profound-cognition 的 57 节点 DAG 架构在设计上遵循 SOAR 的知识级→符号级→实现级三层抽象，Phase 1 对应知识级（问题理解和信息收集），Phase 2 对应符号级（推理和知识操作），Phase 4+Phase 7 对应实现级（输出渲染和元维度扩展）。这一设计确保了认知流水线在每一层都有明确的认知科学依据。

### 8.4 产生式系统推理规则

SOAR的核心推理机制是产生式系统（Production System），通过"条件-动作"规则在工作记忆上进行模式匹配和推理。

#### 8.4.1 产生式规则结构

```
规则格式:
  IF <条件模式> THEN <动作>
  其中:
    - 条件模式: 工作记忆中的元素模式匹配
    - 动作: 对工作记忆的修改（添加/删除/修改元素）

profound-cognition映射:
  IF <DAG节点状态 + 上下文条件> THEN <认知操作>
```

#### 8.4.2 核心产生式规则集

| 规则ID | 条件模式 | 动作 | profound-cognition映射 |
|--------|---------|------|----------------------|
| **PR-01** | 工作记忆中存在未解决的子目标 ∧ 子目标优先级 ≥ high | 激活深度推理模式，分配额外token预算 | depth_signal触发 → T09多路径推理 |
| **PR-02** | 工作记忆中存在冲突的假设 ∧ 冲突未解决 | 激活对抗验证，构建正方/反方论证 | cognitive_conflict → T10-T12三路对抗 |
| **PR-03** | 当前推理路径的信息增益 < 阈值ε ∧ 持续2轮 | 终止当前路径，切换到更高信息增益的路径 | EFE低 → 路径切换 |
| **PR-04** | 工作记忆中存在僵局（无规则可匹配） | 触发子目标生成，创建新的学习目标 | impasse → depth_signal递归深挖 |
| **PR-05** | 问题解决完成 ∧ 解决方案经过验证 | 执行组块化，将解决方案抽象为新规则 | 认知跃迁CL1-CL6记录 → 规则库更新 |
| **PR-06** | 工作记忆中证据不足 ∧ 关键假设未验证 | 触发证据收集，搜索补充信息 | Gate判定"证据不足" → T05证据收集 |
| **PR-07** | 多条规则同时匹配（冲突集非空） | 执行偏好评估，选择最优规则 | UCB排序 → 最优路径选择 |

#### 8.4.3 推理循环

```
SOAR决策循环在profound-cognition中的实现:

1. 感知阶段 (Elaboration Phase)
   - 输入当前DAG节点状态到工作记忆
   - 所有满足条件的产生式规则并行激活
   - 生成候选动作集合

2. 决策阶段 (Decision Phase)
   - 对候选动作集合执行偏好评估（见8.5）
   - 选择最优动作
   - 如果无法选择（僵局）→ 触发PR-04

3. 应用阶段 (Application Phase)
   - 执行选定动作
   - 更新工作记忆
   - 更新DAG节点状态

4. 学习阶段 (Learning Phase)
   - 如果问题解决 → 执行PR-05组块化
   - 如果遇到僵局 → 记录僵局类型和解决策略
```

### 8.5 偏好机制决策逻辑

SOAR的偏好机制（Preference Mechanism）用于在多条竞争规则中选择最优行动。

#### 8.5.1 偏好类型

| 偏好类型 | 符号 | 含义 | profound-cognition映射 |
|----------|------|------|----------------------|
| **更好偏好** | A > B | A比B更可取 | UCB排序中A的分数高于B |
| **等同偏好** | A = B | A和B同样可取 | UCB排序中A和B分数相同 |
| **更好或等同** | A ≥ B | A至少和B一样可取 | UCB排序中A的分数 ≥ B |
| **禁止偏好** | A ✗ | A不可接受 | Gate判定A不通过 |
| **要求偏好** | A ✓ | A必须被选择 | Gate判定A为唯一通过项 |

#### 8.5.2 偏好评估决策流程

```
Step 1: 收集所有候选动作的偏好
  - 对当前冲突集中的每个候选动作，收集所有相关偏好
  - 偏好来源：规则指定的偏好 + 元认知偏好 + 历史经验偏好

Step 2: 过滤阶段
  - 移除所有被"禁止偏好"标记的候选动作
  - 保留被"要求偏好"标记的候选动作（如果存在）
  - 如果无候选动作通过 → 触发僵局处理

Step 3: 排序阶段
  - 对剩余候选动作按偏好关系构建偏序图
  - 计算每个候选动作的综合偏好分数：
    score(A) = w1 × EFE_score(A) + w2 × UCB_score(A) + w3 × historical_score(A)
    其中:
      - EFE_score: 期望自由能评分（信息增益 vs 风险）
      - UCB_score: 上置信界评分（探索 vs 利用）
      - historical_score: 历史成功率评分
      - w1, w2, w3: 权重（可由元认知层动态调整）

Step 4: 选择阶段
  - 如果存在唯一最优候选 → 选择该候选
  - 如果存在多个等同最优候选 → 随机选择（探索性）或选择历史最优（利用性）
  - 如果无法确定偏好 → 触发元认知介入

Step 5: 元认知覆盖
  - 元认知监控有权覆盖偏好评估结果
  - 覆盖条件：检测到系统性偏差 或 认知资源即将耗尽
  - 覆盖操作：强制选择资源消耗最低的候选动作
```

#### 8.5.3 偏好机制与 Phase/节点对照映射

| 认知流水线 Phase/节点 | 偏好机制操作 | 决策逻辑 |
|----------------------|------------|---------|
| Phase 1（T00-T03）输入解析 | 输入格式偏好选择 | 要求偏好：必须支持指定格式；更好偏好：结构化 > 非结构化 |
| Phase 1（T04-T05）问题解构 | 子问题优先级偏好 | 更好偏好：高影响子问题 > 低影响子问题；禁止偏好：循环依赖 |
| Phase 1（T06-T07）证据收集 | 证据源偏好 | 更好偏好：一手源 > 二手源；更好偏好：同行评审 > 非评审 |
| Phase 2（T08-T09）推理演绎 | 推理路径偏好 | 更好偏好：高EFE路径 > 低EFE路径；更好偏好：逻辑有效 > 直觉判断 |
| Phase 2（T10-T12）验证对抗 | 对抗策略偏好 | 要求偏好：必须包含反方论证；更好偏好：强反例 > 弱反例 |
| Phase 2-3（T13-T19）知识整合 | 整合策略偏好 | 更好偏好：跨域映射 > 单域分析；更好偏好：高一致性 > 低一致性 |
| Phase 4（T20a-c）输出优化 | 输出格式偏好 | 要求偏好：必须符合输出规范；更好偏好：受众适配 > 通用格式 |
| Phase 7（T22-T28, TM01-TM07）元认知监控 | 元认知覆盖偏好 | 禁止偏好：系统性偏差输出；要求偏好：质量门控通过 |

### 8.6 穷尽重试策略

| 重试级别 | 条件 | 操作 | 输出质量 |
|----------|------|------|---------|
| **L1 完整模式** | 产生式系统完整可用、偏好机制正常运作 | 执行完整的产生式推理 + 偏好评估 + 组块化学习 | 定量偏好分数 + 推理路径选择依据 + 学习记录 |
| **L2 穷尽重试偏好评估** | 偏好机制受限（如历史经验库不完整） | 穷尽重试所有替代偏好评估路径，直至质量达标 | 偏好分数 + 推理路径选择依据 + 重试路径记录 |
| **L3 穷尽重试规则集** | 产生式规则集不完整（缺少领域特定规则） | 穷尽重试所有可用推理规则 + 标注领域特定规则缺口 + 持续补充直至覆盖 | 推理结果 + 规则覆盖声明 |
| **L4 穷尽重试领域知识** | 缺乏该认知领域的SOAR映射知识 | 穷尽重试所有可用认知架构路径 + 标注领域假设 + 持续补充领域知识直至达标 | 认知推理 + 领域假设标注 + 知识补充记录 |

---

## 9. pymdp 主动推理原理（v3 新增）

> **能力卡**: MC-182 ActiveInference
> **来源**: pymdp / ActiveInference.jl (Friston 自由能原理)
> **用途**: 引入自由能原理驱动"信息增益 vs 时间成本"动态平衡

### 9.1 自由能原理概述

主动推理（Active Inference）基于自由能原理（Free Energy Principle），将认知系统视为持续最小化"变分自由能"（Variational Free Energy）的推理机器。自由能 = 复杂性 - 准确性，最小化自由能意味着在"模型简单性"和"数据拟合度"之间寻找最优平衡。

### 9.2 Expected Free Energy（EFE）决策机制

每个 DAG 节点完成后，计算 Expected Free Energy 以动态决定是否继续探索：

```
G(π) = E_Q[ln Q(s|π) - ln P(s, o|π)]
     = -E_Q[ln P(o|s)] + D_KL[Q(s|π) || P(s)]
     = -信息增益(epistemic value) + 风险(pragmatic value)
```

其中：
- **信息增益项（Epistemic Value）**: 探索新状态能带来的认知收益
- **风险项（Pragmatic Value）**: 偏离先验信念的代价

### 9.3 在 profound-cognition 中的应用

| 应用场景 | 机制 |
|---------|------|
| 搜索深度决策 | EFE 高（信息增益 > 风险）→ 继续深入搜索；EFE 低 → 终止搜索 |
| 路径选择 | 各推理路径的 EFE 参与 UCB 排序，信息增益高的路径优先探索 |
| 迭代终止 | 当 ΔInfo(t) < ε 且 EFE 接近于 0 → 双重确认终止 |
| 资源分配 | Token 预算按 EFE 比例分配：高 EFE 节点获得更多推理资源 |

### 9.4 与指数衰减模型的协同

```
EFE 主动推理 + 指数衰减模型 = 双重终止保障：
1. EFE 从"前瞻"角度判断是否值得继续探索（预期收益）
2. ΔInfo(t) 从"回顾"角度判断已获收益是否递减（实际收益）
3. 两者同时满足终止条件 → 安全终止
```

### 9.5 pymdp 完整调用流程

> **能力卡**: MC-182 ActiveInference

pymdp 是 Python 实现的主动推理库，基于 Friston 自由能原理。以下为在 profound-cognition 中的完整调用流程：

```yaml
pymdp_workflow:
  step_1_model_definition:
    description: "定义生成模型（Generative Model）"
    operations:
      - "定义隐藏状态空间：num_states = [n_s1, n_s2, ...]，每个模态的状态数"
      - "定义观测空间：num_obs = [n_o1, n_o2, ...]，每个模态的观测数"
      - "定义控制状态空间：num_controls = [n_c1, n_c2, ...]，可执行动作数"
      - "构建先验偏好：C = preference_matrix，描述期望观测的先验偏好"

  step_2_parameter_initialization:
    description: "初始化模型参数"
    operations:
      - "A 矩阵（似然矩阵）：P(o|s)，给定状态下的观测概率——A[i][:,:,j] = P(o_i|s_j)"
      - "B 矩阵（转移矩阵）：P(s_t|s_{t-1}, u)，给定动作下的状态转移概率"
      - "D 向量（先验状态）：P(s_0)，初始状态分布"
      - "C 矩阵（偏好矩阵）：log P(o)，期望观测的先验偏好（编码目标）"

  step_3_inference:
    description: "执行主动推理循环"
    operations:
      - "变分后验更新：q(s) ← argmin F，最小化变分自由能"
      - "EFE 计算：G(π) = Σ_t EFE(π, t)，计算每条策略的期望自由能"
      - "策略选择：π* = argmin G(π)，选择 EFE 最小的策略"
      - "动作执行：u* = π*(0)，执行最优策略的第一个动作"

  step_4_output_extraction:
    description: "提取推理结果"
    operations:
      - "后验状态分布：q(s_t|o_1:t)"
      - "策略后验：q(π) ∝ exp(-γ × G(π))"
      - "自由能值：F = D_KL[q(s)||P(s)] - E_q[ln P(o|s)]"
      - "信息增益：E_q[ln q(s|π) - ln P(s|π)]"

  step_5_integration_with_pipeline:
    description: "与认知流水线集成"
    operations:
      - "将 DAG 节点映射为 pymdp 的隐藏状态"
      - "将推理路径选择映射为策略选择"
      - "将 EFE 值映射为 UCB 排序中的探索价值"
      - "将自由能变化映射为 depth_signal 的触发信号"
```

### 9.6 ActiveInference 输出 yaml 规范

```yaml
active_inference_output:
  model_specification:
    num_states: [int]
    num_obs: [int]
    num_controls: [int]
    preference_entropy: float
  inference_results:
    posterior_states:
      - time_step: int
        distribution: [float]
        dominant_state: "最可能状态描述"
    policy_posterior:
      - policy_id: "π-001"
        probability: float
        efe_value: float
        selected: bool
    free_energy:
      initial: float
      final: float
      reduction: float
    information_gain:
      total: float
      per_modality: [float]
  pipeline_integration:
    depth_signal: "continue|terminate"
    efe_ranking: [{policy_id: "π-001", rank: int, efe: float}]
    resource_allocation: [{node_id: "N-001", token_budget: float}]
```

### 9.7 ActiveInference 穷尽重试策略

```yaml
active_inference_exhaust_retry:
  RETRYING_PYMDP:
    trigger: "pymdp 库不可用或导入失败"
    exhaust_retry: "穷尽重试解析公式手动计算 EFE 和自由能近似值，基于简化假设（独立模态、高斯近似），持续重试直至质量达标"
    output_annotation: "ActiveInference穷尽重试：pymdp不可用，使用解析近似替代数值计算"
    accuracy_note: "解析近似在模态间强耦合时精度下降，持续重试改进"

  RETRYING_MODEL_SPEC:
    trigger: "问题无法有效映射为 pymdp 的状态-观测-控制模型（问题过于模糊或非结构化）"
    exhaust_retry: "穷尽重试概念级主动推理——仅计算信息增益的定性估计（高/中/低）和风险项的定性评估，不执行数值计算，持续重试直至质量达标"
    output_annotation: "ActiveInference穷尽重试：使用概念级推理替代数值模型"

  RETRYING_COMPUTATION:
    trigger: "EFE 计算超时或状态空间过大导致计算不可行"
    exhaust_retry: "穷尽重试采样近似（Monte Carlo EFE 估计，采样100-500次）替代精确计算，持续重试直至质量达标"
    output_annotation: "ActiveInference穷尽重试：使用Monte Carlo采样近似替代精确EFE计算"

  FULL_EXHAUST_RETRY:
    trigger: "主动推理完全不可用（pymdp + 解析近似 + 概念推理均失败）"
    exhaust_retry: "穷尽重试所有可用启发式路径——使用信息增益递减率 ΔInfo(t)/ΔInfo(t-1) 作为终止信号，不计算 EFE，持续重试直至质量达标"
    output_annotation: "ActiveInference穷尽重试：使用信息增益递减启发式替代EFE计算"
    confidence_adjustment: "深度决策和资源分配的置信度持续重试提升"
```

> 知识来源: MC-182 [ActiveInference]

### 9.8 pymdp与DAG固定拓扑的对照改造方案

pymdp的主动推理模型基于马尔可夫决策过程（MDP）的动态状态转移，而profound-cognition的认知流水线基于DAG（有向无环图）的固定拓扑。两者之间存在根本性的架构差异，需要改造方案实现有效集成。

#### 9.8.1 架构差异对照

| 维度 | pymdp原生架构 | profound-cognition DAG架构 | 差异性质 |
|------|-------------|--------------------------|---------|
| **拓扑结构** | 动态状态转移图（可循环） | 固定DAG（无循环） | 根本差异 |
| **时间模型** | 离散时间步 t=0,1,2,... | DAG节点执行序（拓扑序） | 可映射 |
| **状态空间** | 隐藏状态 s ∈ S | DAG节点 N ∈ Nodes | 可映射 |
| **观测空间** | 观测 o ∈ O | 节点输出 output(N) | 可映射 |
| **动作空间** | 控制状态 u ∈ U | 路径选择/深度决策 | 部分可映射 |
| **策略空间** | 策略 π = (u_0, u_1, ..., u_T) | 推理路径 path = (N_1, N_2, ..., N_k) | 需要改造 |

#### 9.8.2 DAG→MDP映射方案

```
映射规则:

1. 状态映射:
   - 每个DAG节点 N_i 映射为 pymdp 的一个隐藏状态模态
   - 节点的执行状态映射为状态值：
     s_i = 0 (未执行) | 1 (执行中) | 2 (已完成) | 3 (跳过)

2. 观测映射:
   - 每个节点的输出质量映射为观测值：
     o_i = "high_quality" | "medium_quality" | "low_quality" | "no_output"

3. 转移映射:
   - DAG的边 (N_i → N_j) 映射为状态转移：
     P(s_j=1 | s_i=2, u=execute_next) = 1.0
     即：前驱节点完成后，执行动作"继续"将激活后继节点
   - DAG的固定拓扑约束转移矩阵B：
     B[i][:,:,u] 中，只有DAG边允许的转移概率为非零

4. 策略映射:
   - 每条DAG路径映射为一条策略
   - 策略长度 = 路径长度
   - 策略选择 = 路径选择

5. 偏好映射:
   - C矩阵编码对高质量输出的偏好
   - C[i]["high_quality"] > C[i]["medium_quality"] > C[i]["low_quality"]
```

#### 9.8.3 固定拓扑约束下的EFE计算改造

```
标准EFE:
  G(π) = -E_Q[ln P(o|s)] + D_KL[Q(s|π) || P(s)]

DAG约束下的EFE改造:
  G_DAG(π) = -E_Q[ln P(o|s) | DAG_topology] + D_KL[Q(s|π) || P(s) | DAG_topology]

其中DAG_topology约束:
  1. 转移约束: P(s_j|s_i, u) = 0 如果 (N_i → N_j) ∉ DAG_edges
  2. 执行约束: 节点N_i只有在所有前驱节点完成后才能执行
  3. 路径约束: 策略π必须对应DAG中的一条有效路径

改造后的EFE计算步骤:
  Step 1: 枚举DAG中的所有有效路径（从当前节点到终端节点）
  Step 2: 对每条路径计算EFE（仅考虑路径上的节点）
  Step 3: 选择EFE最小的路径
  Step 4: 执行路径的第一个动作（下一个DAG节点）
```

#### 9.8.4 动态平衡决策规则

```
在DAG固定拓扑约束下，主动推理的动态平衡决策规则:

规则1: 路径选择
  - 对DAG中从当前节点出发的所有可达路径，计算EFE
  - 选择EFE最小的路径（信息增益最高 + 风险最低）
  - 如果多条路径EFE相近（差异 < δ）→ 保留多条路径并行探索

规则2: 深度决策
  - 当前节点完成后，计算继续深入 vs 终止的EFE差值
  - ΔEFE = EFE(continue) - EFE(terminate)
  - ΔEFE < 0 → 继续深入（信息增益超过风险）
  - ΔEFE ≥ 0 → 终止当前路径

规则3: 资源分配
  - 按EFE比例分配token预算
  - 高EFE路径获得更多资源（探索价值高）
  - 低EFE路径获得较少资源（接近收敛）

规则4: 异常处理
  - 如果DAG节点执行失败 → 更新转移概率（将该路径的EFE调高）
  - 如果信息增益突然下降 → 触发提前终止检查
  - 如果自由能持续上升 → 触发元认知介入
```

#### 9.8.5 穷尽重试策略补充

| 重试级别 | 条件 | 操作 | 输出质量 |
|----------|------|------|---------|
| **L1 完整DAG-MDP映射** | DAG拓扑可完整映射为MDP | 执行完整的DAG约束EFE计算 + 路径选择 + 动态平衡 | 定量EFE + 最优路径 + 资源分配方案 |
| **L2 简化MDP映射** | DAG节点过多导致状态空间爆炸 | 聚合DAG节点为场景级MDP + 计算场景级EFE + 穷尽重试直至质量达标 | 场景级EFE + 近似最优路径 + 重试记录 |
| **L3 概念级映射** | 无法构建数值MDP模型 | 基于DAG结构的概念级推理——定性评估路径的信息增益和风险 + 穷尽重试所有概念路径 | 定性路径评估 + 概念级决策建议 + 重试记录 |
| **L4 无映射** | DAG与MDP完全无法对应 | 穷尽重试DAG原生执行模式所有可用路径（不使用主动推理），持续重试直至质量达标 | DAG顺序执行 + 启发式深度决策 + 重试记录 |

---

## 10. MIDCA 双过程元认知架构参考（v3 新增）

> **来源**: MIDCA (Metacognitive Integrated Dual-Cycle Architecture)
> **用途**: 为 profound-cognition 提供系统 1/系统 2 + 元认知监控的理论框架

### 10.1 三层架构

| 系统 | 特征 | profound-cognition 对应 |
|------|------|------------------------|
| **系统 1（快速直觉）** | 自动、快速、无意识、情感驱动 | Phase 1 研究底座层（T01 输入分流、T02-T06 研究底座中的直觉判断） |
| **系统 2（慢速分析）** | 受控、缓慢、有意识、逻辑驱动 | Phase 2 认知流水线层（T09 多路径推理、T10-T12 三路对抗、T13 认知综合） |
| **元认知监控** | 监控系统 1/2 的输出质量，分配认知资源 | Supervisor Protocol + Gate 门控 + depth_signal 扫描 + Phase 7 元维度引擎 |

#### 10.1.1 系统1（快速直觉）详细操作步骤

```
Step 1: 模式识别触发
  - 输入到达后，系统1在 < 500ms 内完成初步模式匹配
  - 基于经验库中的相似案例，生成直觉判断
  - 输出标记：system_1_heuristic = true

Step 2: 启发式推理
  - 可用性启发式(availability): 优先调用最近/最显著的相关知识
  - 代表性启发式(representativeness): 基于原型匹配进行分类判断
  - 锚定启发式(anchoring): 以初始信息为锚点进行快速估计
  - 每个启发式输出附带置信度标记：heuristic_confidence ∈ [0, 1]

Step 3: 直觉输出生成
  - 生成直觉判断列表：{判断内容, 置信度, 启发式类型, 触发条件}
  - 标记需要系统2介入的条件：
    - heuristic_confidence < 0.6
    - 判断涉及高权重结论（impact ≥ "high"）
    - 多个启发式产生冲突判断
```

#### 10.1.2 系统2（慢速分析）详细操作步骤

```
Step 1: 系统2激活条件判定
  - 条件A: 系统1输出 heuristic_confidence < 0.6
  - 条件B: 任务类型为"analytical"或"evaluative"
  - 条件C: 元认知监控发出 cognitive_conflict 信号
  - 条件D: Gate 门控要求深度分析（depth_required ≥ 2）
  - 任一条件满足 → 激活系统2

Step 2: 假设空间构建
  - 对系统1的每个直觉判断，构建对立假设
  - 生成假设空间 H = {h_1, h_2, ..., h_n}，其中至少包含系统1的直觉判断和其否定
  - 为每个假设分配先验概率 P(h_i)

Step 3: 证据驱动的贝叶斯更新
  - 收集支持/反对每个假设的证据
  - 执行贝叶斯更新：P(h_i|e) ∝ P(e|h_i) × P(h_i)
  - 计算后验概率分布，识别最可能假设

Step 4: 多路径推理与对抗验证
  - T09 多路径推理：对最可能假设执行至少2条独立推理路径
  - T10-T12 三路对抗：正方/反方/裁判的辩证验证
  - 输出综合判断：{判断内容, 置信度, 推理路径, 对抗结果}
```

#### 10.1.3 元认知监控详细操作步骤

```
Step 1: 认知资源分配
  - 评估当前任务的认知负荷：cognitive_load = f(问题复杂度, 不确定性, 时间约束)
  - 分配系统1/系统2的资源比例：
    - cognitive_load < 0.3 → 系统1:系统2 = 80:20
    - 0.3 ≤ cognitive_load < 0.7 → 系统1:系统2 = 40:60
    - cognitive_load ≥ 0.7 → 系统1:系统2 = 20:80

Step 2: 输出质量监控
  - 对系统1输出：检查启发式偏差标记
  - 对系统2输出：检查逻辑一致性和证据充分性
  - 对综合输出：检查系统1/系统2结论的一致性

Step 3: 冲突检测与解决
  - 检测系统1与系统2的结论冲突
  - 冲突解决策略：
    - 事实类问题 → 以系统2结论为准
    - 创意类问题 → 保留系统1直觉，系统2提供约束
    - 伦理类问题 → 两者并列呈现，标注价值分歧
  - 发出 cognitive_conflict 信号（如适用）

Step 4: 元认知反思
  - 记录本次认知过程的元数据：
    {系统1判断, 系统2判断, 冲突是否存在, 冲突解决策略, 最终结论, 置信度}
  - 更新认知偏差防御规则库
```

### 10.2 认知偏差防御

MIDCA 的元认知层通过以下机制防御认知偏差：

#### 10.2.1 核心偏差防御规则

| 偏差类型 | 定义 | 防御机制 | 触发条件 | 操作 |
|----------|------|---------|---------|------|
| **确认偏差** | 倾向于搜索支持已有信念的证据 | 反向证据强制搜索 | 系统2激活时 | 必须搜索至少N条反对当前假设的证据，N = 假设权重 × 3 |
| **锚定效应** | 过度依赖初始信息 | 锚点重置协议 | 系统1输出后 | 系统2分析时忽略系统1的具体数值，仅保留方向性信息 |
| **可得性偏差** | 高估容易想到的事件的概率 | 基准率校准 | 概率估计时 | 强制引入基准率(base rate)数据，调整直觉概率估计 |
| **过度自信** | 高估自己判断的准确性 | 置信度校准 | 置信度 > 0.9时 | 执行10%置信度缩减 + 要求提供反对证据 |
| **框架效应** | 判断受问题表述方式影响 | 框架重述检验 | 决策类任务 | 用至少2种不同框架重述问题，检查结论是否一致 |
| **沉没成本** | 因已投入资源而继续无效行动 | 独立评估协议 | 迭代深度 > 3时 | 假设从零开始，是否仍会做出相同选择 |
| **后见之明** | 事后高估事前预测的准确性 | 预测记录比对 | 结论验证时 | 比对初始预测与最终结论，标注预测偏差 |

#### 10.2.2 偏差防御执行流程

```
Phase 1: 预防（系统1输出阶段）
  - 所有系统1输出自动标注：system_1_heuristic = true
  - 标注使用的启发式类型和已知偏差倾向
  - 对高偏差风险的直觉判断发出预警

Phase 2: 检测（系统2分析阶段）
  - 系统2分析时，对照偏差防御规则表逐一检查
  - 对每条规则，评估是否满足触发条件
  - 满足触发条件 → 执行对应防御操作

Phase 3: 校正（元认知监控阶段）
  - 检查系统2分析是否遗漏了偏差防御
  - 对已检测到的偏差，验证校正操作是否有效
  - 输出偏差防御报告：{偏差类型, 检测结果, 校正操作, 校正效果}
```

### 10.3 与 profound-cognition 的对照

profound-cognition 的 T09（多路径推理）和 T10-T12（三路对抗）天然实现了系统 2 的慢速分析，而 Supervisor Protocol 和 Gate 门控体系实现了元认知监控。MIDCA 的引入为这一设计提供了认知科学的理论支撑。

#### 10.3.1 MIDCA与57节点DAG完整映射表

| DAG Phase / 节点 | MIDCA系统归属 | 系统1操作 | 系统2操作 | 元认知监控 |
|-------------|-------------|---------|---------|-----------|
| **Phase 1 T01 输入分流** | 系统1主导 | 模式识别：快速分类输入类型和格式 | 格式验证：检查输入完整性和一致性 | 输入质量评估：是否需要补充信息 |
| **Phase 1 T00 研究大纲** | 系统1+系统2 | 直觉分解：基于经验快速识别子问题结构 | MECE验证：检查子问题的互斥性和完备性 | 假设扫描：识别隐含假设的覆盖率 |
| **Phase 1 T02-T05 研究底座** | 系统2主导 | 来源直觉：快速判断信息源的可靠性 | 交叉验证：多源信息的一致性检验 | 证据充分性：判断证据是否足以支撑结论 |
| **Phase 2 T09 多路径推理** | 系统2主导 | 推理直觉：基于类比快速生成推理方向 | 逻辑验证：逐步检查推理链的逻辑有效性 | 推理一致性：检查推理路径间是否存在矛盾 |
| **Phase 2 T10-T12 三路对抗** | 系统2主导 | 反例直觉：快速识别可能的反例 | 系统反证：构建形式化的反证论证 | 对抗充分性：判断对抗是否足够严格 |
| **Phase 2 T13 认知综合** | 系统1+系统2 | 关联直觉：快速识别跨域知识关联 | 深度整合：系统化构建跨域知识映射 | 整合一致性：检查跨域映射的逻辑一致性 |
| **Phase 4 T20a/T20b/T20c 渲染** | 系统1主导 | 表达直觉：基于受众特征选择表达方式 | 结构验证：检查输出结构的完整性 | 输出质量：最终质量门控 |
| **Phase 7 TM01-TM07 + 元维度** | 元认知主导 | 过程直觉：对认知过程效率的快速评估 | 过程分析：系统化分析认知过程的瓶颈 | 全局监控：认知资源分配、偏差防御、质量守卫 |

#### 10.3.2 穷尽重试策略

| 重试级别 | 条件 | 操作 | 输出质量 |
|----------|------|------|---------|
| **L1 完整模式** | 系统1/系统2/元认知三层完整可用 | 执行完整的双过程推理 + 元认知监控 + 偏差防御 | 定量偏差检测 + 校正报告 + 置信度校准 |
| **L2 穷尽重试元认知** | 元认知监控受限（如资源约束） | 执行系统1+系统2双过程推理，穷尽重试所有元认知监控路径，直至偏差校正完成 | 偏差预警 + 校正的直觉判断 + 重试记录 |
| **L3 穷尽重试系统2** | 系统2不可用（如时间约束极紧） | 穷尽重试所有可用分析路径 + 标注所有判断为 heuristic + 持续重试直至系统2验证可行 | 判断 + 偏差风险标注 + 验证记录 |
| **L4 穷尽重试领域知识** | 缺乏该领域的认知偏差模式知识 | 穷尽重试所有可用偏差防御规则 + 标注领域特殊性假设 + 持续补充领域知识 | 偏差防御 + 领域假设标注 + 知识补充记录 |

---

### [pymdp] 源码逻辑引入

#### 核心算法逻辑

**1. 自由能原理计算源码逻辑**

```
变分自由能计算核心（pymdp/inference/free_energy.py）:

function compute_variational_free_energy(prior, posterior, likelihood):
    # 变分自由能 F = D_KL[q(s)||p(s)] - E_q[ln p(o|s)]
    # = 精度项（KL散度）+ 复杂度项（负期望对数似然）

    # 项1：KL散度——后验与先验的差异
    kl_divergence = 0
    for state in all_states:
        kl_divergence += posterior[state] * (
            log(posterior[state]) - log(prior[state])
        )

    # 项2：期望对数似然——观测与状态的匹配度
    expected_log_likelihood = 0
    for state in all_states:
        for obs in all_observations:
            expected_log_likelihood += posterior[state] * log(likelihood[obs, state])

    # 变分自由能 = KL散度 - 期望对数似然
    F = kl_divergence - expected_log_likelihood

    # 自由能越低 → 后验越接近真实后验 → 推理越准确
    return F
```

**2. EFE（预期自由能）计算源码步骤**

```
预期自由能计算（pymdp/control/efe.py）:

function compute_efe(agent, policy, time_horizon):
    # EFE(π) = E_efe[信息增益项] + E_efe[效用项]
    # 最小化EFE = 最大化信息增益 + 最大化偏好满足

    efe = 0

    for t in 1..time_horizon:
        # 对策略π下的每个时间步预测状态和观测
        predicted_states = predict_next_state(agent, policy, t)
        predicted_observations = predict_observation(predicted_states)

        # 项1：认识价值（Epistemic Value）= 信息增益
        # = E[q(o|π)] [D_KL[q(s|o,π) || q(s|π)]]
        # 高信息增益 → 不确定状态下的探索
        epistemic_value = 0
        for obs in all_observations:
            p_obs = predicted_observations[obs]
            # 后验（获得观测后）vs 先验（获得观测前）的KL散度
            posterior_given_obs = bayes_update(predicted_states, obs)
            kl = kl_divergence(posterior_given_obs, predicted_states)
            epistemic_value += p_obs * kl

        # 项2：效用价值（Pragmatic Value）= 偏好满足
        # = E[q(o|π)] [ln p_c(o)]
        # p_c = 偏好分布（agent的C矩阵）
        pragmatic_value = 0
        for obs in all_observations:
            p_obs = predicted_observations[obs]
            pragmatic_value += p_obs * log(agent.C[obs])

        # EFE = -认识价值 - 效用价值（最小化 = 最大化两者）
        efe += -epistemic_value - pragmatic_value

    return efe

# 策略选择：选择EFE最小的策略
function select_policy(agent, policies):
    efe_values = {}
    for policy in policies:
        efe_values[policy] = compute_efe(agent, policy, time_horizon)

    # softmax选择（允许随机探索）
    selected = softmax_sample(efe_values, alpha=agent.action_selection_precision)
    return selected
```

**3. 动态平衡决策源码逻辑**

```
探索-利用动态平衡（pymdp/agent/agent.py）:

function active_inference_step(agent, observation):
    # 步骤1：感知——更新状态后验
    agent.qs = update_posterior(agent, observation)
    # 使用变分推理最小化自由能
    # q(s) ≈ argmin F(q, p)

    # 步骤2：策略评估——计算每个策略的EFE
    for policy in agent.policies:
        agent.EFE[policy] = compute_efe(agent, policy, agent.planning_horizon)

    # 步骤3：策略选择——softmax采样
    selected_policy = select_policy(agent, agent.policies)

    # 步骤4：动作执行——取策略的第一步动作
    action = selected_policy.actions[0]
    agent.action = action

    # 步骤5：学习（可选）——更新模型参数
    if agent.learning_enabled:
        # 更新A矩阵（似然/观测模型）
        agent.A = update_likelihood(agent.A, observation, agent.qs)
        # 更新B矩阵（转移模型）
        agent.B = update_transition(agent.B, agent.qs_prev, action, agent.qs)
        # 更新C向量（偏好）——基于奖励信号
        if agent.reward is not None:
            agent.C = update_preferences(agent.C, observation, agent.reward)

    return action

# 探索-利用平衡机制:
# - 高不确定性状态 → 认识价值主导 → 探索行为
# - 低不确定性状态 → 效用价值主导 → 利用行为
# - action_selection_precision (α) 控制探索程度:
#   α高 → 更确定性选择最优策略（利用倾向）
#   α低 → 更随机选择（探索倾向）
```

#### 数据结构设计

```
核心数据结构:

1. Agent: 主动推理智能体
   - A: ndarray (n_obs, n_states)    # 似然矩阵 P(o|s)
   - B: ndarray (n_states, n_states, n_actions) # 转移矩阵 P(s'|s,a)
   - C: ndarray (n_obs,)             # 偏好向量 log P_c(o)
   - D: ndarray (n_states,)          # 先验 P(s_0)
   - qs: ndarray (n_states,)         # 当前状态后验
   - policies: list[Policy]          # 可选策略列表
   - EFE: Dict[Policy, float]        # 各策略EFE值

2. Policy: 策略
   - actions: list[int]              # 动作序列
   - horizon: int                    # 时间视野

3. InferenceResult: 推理结果
   - qs: ndarray                     # 状态后验
   - free_energy: float              # 变分自由能
   - selected_policy: Policy         # 选中策略
   - action: int                     # 执行动作
```

#### 决策流程

```
pymdp 主动推理决策流程:

1. 观测获取 → 接收环境观测o
2. 状态推断 → update_posterior() 最小化自由能
3. 策略评估 → compute_efe() 计算各策略EFE
   ├─ 认识价值高 → 探索（减少不确定性）
   └─ 效用价值高 → 利用（满足偏好）
4. 策略选择 → softmax采样（α控制探索度）
5. 动作执行 → 执行选中策略的第一步
6. 模型更新（可选）→ 学习A/B/C矩阵
```

#### 穷尽重试策略

```yaml
pymdp_source_exhaust_retry:
  L1_FULL_ACTIVE_INFERENCE:
    condition: "pymdp可用，A/B/C/D矩阵可配置"
    action: "完整主动推理：状态推断+EFE策略评估+动作选择+学习"
    confidence: "HIGH"

  L2_SIMPLIFIED_EFE_RETRY:
    condition: "pymdp可用但学习不可用"
    action: "穷尽重试简化EFE（实用价值优先 + 认知价值近似）——保留完整EFE框架但认知价值使用简化近似（状态熵代替完整后验KL散度）；策略评估保留，持续重试直至质量达标"
    confidence: "MEDIUM→HIGH（持续重试提升）"
    output_annotation: "认知价值已被近似，穷尽重试改进策略选择的探索行为"

  L3_QUALITATIVE_INFERENCE_RETRY:
    condition: "pymdp不可用，但可手动贝叶斯推理"
    action: "穷尽重试定性主动推理——不计算数值自由能，用文字描述'策略减少不确定性的方向'；用简单加权代替贝叶斯推断；持续重试直至质量达标"
    confidence: "LOW-MEDIUM→HIGH（持续重试提升）"
    output_annotation: "定性推理，穷尽重试改进自由能计算近似"

  L4_HEURISTIC_RETRY:
    condition: "贝叶斯推理不可行"
    action: "穷尽重试所有启发式路径——基于直觉的探索-利用平衡，持续重试直至质量达标"
    confidence: "LOW→MEDIUM（持续重试提升）"
    output_annotation: "pymdp穷尽重试：启发式决策持续重试改进"
```

---

© 阿洋
