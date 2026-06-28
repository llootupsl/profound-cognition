# 逐层剥开推理 — 从表象到范式的五层因果深度追溯

> **模块标识**: `knowledge/thinking-templates/layer-peeling`
> **设计依据**: 基于全域深度认知框架三层推理架构设计——逐层剥开推理遵循"表象层→机制层→假设层→范式层"四层递进穿透逻辑
> **依赖**: `knowledge/research-methods`、`knowledge/cognitive-framework`、`knowledge/thinking-models/general/first-principles`、`knowledge/thinking-models/general/critical-thinking`
> **骨架类型**: 逐层剥开推理 (Layer Peeling)
>
> **版本治理元数据 (D12.4.2)**:
> - version: 1.1
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（四层递进穿透逻辑）
>   - v1.1 补全版本治理元数据与交叉引用（D12.4.2-D12.4.3）

## 交叉引用

- **上游**: `knowledge/research-methods.md`、`knowledge/cognitive-framework.md`、`knowledge/thinking-models/general/first-principles.md`、`knowledge/thinking-models/general/critical-thinking.md`
- **下游**: `tasks/T08_cog_deconstruct.md`（认知解构，应用逐层剥开模板）、`tasks/T09_cog_reason.md`（认知推理）
- **相关**: `knowledge/thinking-templates/causal-chain.md`（因果链模板）、`knowledge/thinking-models/general/layer-peeling.md`（逐层剥开模型）、`knowledge/thinking-models/routing-table.md`（思维模型路由表）

---

## 模板与模型的边界（D6.4.1）

> 本节明确「思维模板」（骨架级）与「思维模型」（方法论级）的边界与协作关系。

| 维度 | 思维模板（本文件） | 思维模型（thinking-models/） |
|------|------------------|---------------------------|
| **层级** | 骨架级（Skeleton-level） | 方法论级（Methodology-level） |
| **职责** | 提供"如何执行"的步骤流程 | 提供"为什么这样执行"的理论背景 |
| **内容** | 可执行伪代码 + 输入输出 schema + 失败模式闭环 | 理论渊源 + 假设体系 + 适用条件 + 局限性 |
| **抽象度** | 中（直接可调用） | 高（需模板将其落地为具体步骤） |
| **调用关系** | 模板调用模型的方法论指导 | 模型为模板提供理论支撑和边界条件 |

**本模板对应的方法论级模型**：
- `knowledge/thinking-models/general/first-principles.md`（第一性原理 — 逐层还原的方法论基础）
- `knowledge/thinking-models/general/critical-thinking.md`（批判性思维 — 假设审视的逻辑工具）
- `knowledge/thinking-models/general/layer-peeling.md`（逐层剥开模型 — 层次分析的理论框架）

**边界声明**：本模板提供五层剥开（L0表象→L1直接原因→L2结构→L3机制→L4范式）的执行流程伪代码，不重复阐述第一性原理的还原论哲学或批判性思维的假设审视理论。当需要理论依据时，调用上述模型文件。

---

## 1. 定义

逐层剥开推理是一种强制性的深度分析纪律——它不允许分析者在任何一层停留，而是在每一层都追问"这一层是由什么构成的？什么导致了这一层的状态？"直到抵达不可再分解的范式层。每层有明确的触发条件（什么信号表明需要进入该层）和终止条件（什么信号表明该层已完成，应进入下一层），从而防止分析过早终止于浅层解释。

**核心法则**: 你停在的每一层，都是一种选择——你必须清楚你为什么选择停在这里，以及下一层可能有什么你选择不看的洞察。

---

## 2. 五层剥开架构总览

```
L0 表象层 ─── 这是什么？（可观测现象的描述）
    │  触发: 问题被首次提出
    │  终止: 现象被完整、无歧义地描述；不同观察者对"发生了什么"达成一致
    ▼
L1 直接原因层 ─── 什么直接导致了表象？
    │  触发: L0 完成 + 我们对"为什么发生"没有清晰的因果路径
    │  终止: 每个表象的直接原因被识别；因果链的"第一步"被建立
    ▼
L2 结构层 ─── 什么结构性因素导致了这些直接原因？
    │  触发: L1 完成 + 追问"这些直接原因不是随机的——什么系统性地产生了它们？"
    │  终止: 结构性因素（制度/规则/权力/资源分布）被识别；这些因素解释力 > 个人行为解释力
    ▼
L3 机制层 ─── 什么机制维持、复制或放大了这些结构？
    │  触发: L2 完成 + 追问"这些结构为什么能持续存在？为什么没有被改变？"
    │  终止: 反馈回路被识别；维持机制的可操作描述被建立；正反馈和负反馈的作用被理解
    ▼
L4 范式层 ─── 什么信念、价值观、世界观使这些机制被认为理所当然？
    │  触发: L3 完成 + 追问"为什么人们接受这些机制？换一种完全不同的范式会怎样？"
    │  终止: 底层假设被显式化；范式在其内部逻辑上自洽但被外部审视；替代范式被检验
```

### 2.1 可执行伪代码（D6.4.3）

```python
def layer_peeling_analysis(problem, scope):
    """
    逐层剥开推理模板 - 可执行伪代码（D6.4.3）
    输入: problem(待分析的原始问题), scope(分析范围声明)
    输出: layer_peeling_analysis YAML（见 §6 输出模板）
    """
    current_layer = "L0"
    analysis = {"problem": problem, "scope": scope}

    # ===== L0: 表象层 =====
    # 触发: 问题被首次提出
    # 终止: 现象被完整描述 + 观察者达成一致 + 数据来源标注 + 观察/解释分离
    analysis["L0_surface"] = {
        "phenomenon": describe_phenomenon(problem),  # 不带解释，只描述事实
        "time_scope": define_time_scope(problem),
        "spatial_scope": define_spatial_scope(problem),
        "magnitude": quantify_magnitude(problem),
        "data_sources": assess_data_reliability(problem),
        "observation_vs_interpretation": separate_observation_from_interpretation(problem)
    }
    assert l0_termination_conditions_met(analysis["L0_surface"]), "L0 终止条件未满足"
    current_layer = "L1"

    # ===== L1: 直接原因层 =====
    # 触发: L0完成 + 对"为什么发生"没有清晰因果路径
    # 终止: 直接原因识别 + 因果机制描述 + 充分/必要区分 + 反事实检验 + 时间序列自洽
    analysis["L1_direct_cause"] = {
        "causes": []
    }
    for cause in identify_direct_causes(analysis["L0_surface"]):
        analysis["L1_direct_cause"]["causes"].append({
            "cause": cause,
            "mechanism": describe_mechanism(cause, analysis["L0_surface"]),
            "necessity": classify_necessity(cause),  # necessary|sufficient|contributory
            "evidence_level": classify_evidence(cause),  # L0-L3
            "counterfactual_test": simulate_removal(cause)  # 若移除，现象是否消失？
        })
    assert l1_termination_conditions_met(analysis["L1_direct_cause"]), "L1 终止条件未满足"
    analysis["L1_direct_cause"]["L1_to_L2_transition"] = describe_causal_transition(
        analysis["L1_direct_cause"], "L2_structural"
    )
    current_layer = "L2"

    # ===== L2: 结构层 =====
    # 触发: L1完成 + 追问"什么系统性地产生了这些直接原因？"
    # 终止: 结构因素解释力>个人行为 + 制度约束描述 + 权力分布映射 + 路径依赖识别
    analysis["L2_structural"] = {
        "institutional_constraints": identify_institutional_constraints(analysis["L1_direct_cause"]),
        "power_structure": map_power_structure(analysis["L1_direct_cause"]),
        "path_dependency": identify_path_dependency(analysis["L1_direct_cause"])
    }
    assert l2_termination_conditions_met(analysis["L2_structural"]), "L2 终止条件未满足"
    analysis["L2_structural"]["L2_to_L3_transition"] = describe_causal_transition(
        analysis["L2_structural"], "L3_mechanism"
    )
    current_layer = "L3"

    # ===== L3: 机制层 =====
    # 触发: L2完成 + 追问"这些结构为什么能持续存在？为什么没有被改变？"
    # 终止: 至少1正反馈+1负反馈回路 + 主导条件描述 + 利益驱动识别 + 系统抗性评估
    analysis["L3_mechanism"] = {
        "feedback_loops": identify_feedback_loops(analysis["L2_structural"]),
        "interest_alignment": identify_beneficiaries(analysis["L2_structural"]),
        "system_resistance": assess_system_resistance(analysis["L2_structural"])
    }
    # 验证: 至少1个正反馈回路和1个负反馈回路
    loop_types = [loop["type"] for loop in analysis["L3_mechanism"]["feedback_loops"]]
    assert "reinforcing" in loop_types and "balancing" in loop_types, "需至少1正1负反馈回路"
    assert l3_termination_conditions_met(analysis["L3_mechanism"]), "L3 终止条件未满足"
    analysis["L3_mechanism"]["L3_to_L4_transition"] = describe_causal_transition(
        analysis["L3_mechanism"], "L4_paradigm"
    )
    current_layer = "L4"

    # ===== L4: 范式层 =====
    # 触发: L3完成 + 追问"为什么人们接受这些机制？换一种范式会怎样？"
    # 终止: ≥3个底层假设显式化 + 假设分类 + 来源追溯 + ≥1替代范式检验 + 不可问之问题识别
    analysis["L4_paradigm"] = {
        "foundational_assumptions": identify_assumptions(analysis["L0_surface"], analysis["L1_direct_cause"],
                                                          analysis["L2_structural"], analysis["L3_mechanism"]),
        "paradigm_genealogy": trace_paradigm_origin(analysis["L3_mechanism"]),
        "alternative_paradigm": test_alternative_paradigm(analysis["L3_mechanism"]),
        "paradigm_blind_spots": identify_taboo_questions(analysis["L4_paradigm"])
    }
    # 验证: 至少3个底层假设被显式化
    assert len(analysis["L4_paradigm"]["foundational_assumptions"]) >= 3, "需至少3个底层假设"
    assert l4_termination_conditions_met(analysis["L4_paradigm"]), "L4 终止条件未满足"

    # ===== 综合分析 =====
    analysis["synthesis"] = {
        "cross_layer_insights": synthesize_cross_layer_insights(analysis),  # 每层贡献了什么独特认知？
        "depth_audit": {
            "max_depth_reached": current_layer,
            "early_termination": check_early_termination(analysis),  # null 或 {reason, risk, reentry_condition}
            "layer_coherence": check_layer_coherence(analysis)  # 各层之间因果链是否连贯？
        },
        "what_changed": describe_cognitive_shift(analysis),  # 经过五层剥开，理解发生了什么改变？
        "actionable_insight": extract_actionable_insight(analysis)  # 最有价值的可行动洞察
    }
    analysis["uncertainty_declaration"] = declare_uncertainties(analysis)

    return analysis
```

---

## 3. 各层详述

### L0: 表象层 (Surface Phenomenon)

**核心问题**: 发生了什么？

**分析任务**:
- 精确描述可观测的现象——不带解释，只描述事实
- 区分"观察"和"解释"——"销售额下降了15%"是观察，"因为市场不景气"是解释（应归入L1）
- 界定现象的时空范围: 何时、何地、持续多久、范围多大？
- 识别数据来源和可靠性: 谁观测的？如何记录？有无偏差？

**触发条件**: 问题被首次提出，或当前对"发生了什么"存在不一致描述。

**终止条件**（全部满足才进入L1）:
- [ ] 现象被完整描述，包含时间、地点、范围、量级
- [ ] 不同观察者对"发生了什么"达成一致（分歧仅为解释层面）
- [ ] 数据来源和可靠性已被标注
- [ ] "观察"和"解释"已被明确分离

**典型输出**:
```yaml
L0_surface:
  phenomenon: "完整、不冗余的现象描述"
  time_scope: "时间范围"
  spatial_scope: "空间/领域范围"
  magnitude: "量级/程度"
  data_sources: ["数据来源及可靠性评估"]
  observation_vs_interpretation:
    observations: ["纯观察（不含解释）"]
    deferred_interpretations: ["推迟到L1处理的解释性陈述"]
```

---

### L1: 直接原因层 (Direct Cause)

**核心问题**: 什么直接导致了L0中的现象？

**分析任务**:
- 识别与现象在时间上最近、无中间变量的直接原因
- 对每个直接原因追问:"它是如何导致现象的？机制是什么？"
- 区分充分原因（单个原因足以导致现象）和必要原因（多个原因缺一不可）
- 标注每个原因的证据等级 (L0-L3)

**触发条件**: L0完成，且我们对"为什么发生"没有清晰的因果路径。

**终止条件**（全部满足才进入L2）:
- [ ] 所有表象的直接原因已被识别
- [ ] 每个原因到现象的因果机制已被描述
- [ ] 充分原因 vs 必要原因的区分已完成
- [ ] "如果不是X，现象Y是否还会发生？"的检验已完成
- [ ] 在L1层面，原因与现象之间的时间序列自洽

**典型输出**:
```yaml
L1_direct_cause:
  causes:
    - cause: "直接原因描述"
      mechanism: "该原因导致现象的因果机制"
      necessity: "necessary|sufficient|contributory"
      evidence_level: "L0|L1|L2|L3"
      evidence_source: "证据来源"
      counterfactual_test: "若移除该原因，现象是否消失/减弱？"
```

---

### L2: 结构层 (Structural Layer)

**核心问题**: 什么结构性因素系统性地产出了L1中的直接原因？

**分析任务**:
- 从"谁做了什么"转向"什么结构让这些人倾向这样做"
- 识别制度约束: 哪些规则/法律/规范/激励结构引导了行为？
- 识别权力结构: 资源/信息/决策权如何分布？
- 识别路径依赖: 历史选择如何约束了当前选项空间？
- 区分"结构"（相对稳定的约束条件）和"行为"（结构下的个体选择）

**触发条件**: L1完成 + 追问"这些直接原因不是随机的——什么系统性地产生了它们？"

**终止条件**（全部满足才进入L3）:
- [ ] 结构性因素被识别，其解释力 > 个人行为/偶然性解释力
- [ ] 核心制度约束（显性和隐性规则）已被描述
- [ ] 权力/资源/信息的不对称分布已被映射
- [ ] 路径依赖和锁定效应已被识别
- [ ] "如果结构性条件不同，L1中的直接原因是否会显著改变？"的检验已完成

**典型输出**:
```yaml
L2_structural:
  institutional_constraints:
    - constraint: "制度/规则约束描述"
      type: "formal|informal"
      enforcement: "执行机制"
      behavioral_impact: "该约束如何引导了L1中识别的原因行为"
  power_structure:
    resource_distribution: "关键资源的分布情况（不均衡程度）"
    decision_authority: "决策权分布"
    information_asymmetry: "信息不对称的分布"
    access_barriers: "获取资源/权力的准入障碍"
  path_dependency:
    historical_choices: ["历史上的关键选择"]
    lock_in_mechanism: "锁定效应的维持机制"
    counterfactual: "如果历史选择不同，当前结构可能如何不同？"
```

---

### L3: 机制层 (Mechanism Layer)

**核心问题**: 什么机制维持、复制或放大了L2中的结构？

**分析任务**:
- 识别自我维持的反馈回路: 结构→行为→结果→结构
- 区分正反馈（放大现有结构）和负反馈（纠正偏离）
- 识别"为什么改变不了"的根源——系统抗性
- 分析"谁从现有结构中受益"——结构维持的利益驱动
- 识别替代机制: 在什么条件下，其他机制可能替代当前机制？

**触发条件**: L2完成 + 追问"这些结构为什么能持续存在？为什么没有被改变？"

**终止条件**（全部满足才进入L4）:
- [ ] 至少识别出1个正反馈回路和1个负反馈回路
- [ ] 每个回路的"主导条件"已被描述（在什么条件下该回路主导系统行为？）
- [ ] 结构维持的利益驱动已被识别
- [ ] 系统抗性的来源和强度已被评估
- [ ] "为什么改变尝试失败？"能被该层的机制解释

**典型输出**:
```yaml
L3_mechanism:
  feedback_loops:
    - id: "LOOP-001"
      type: "reinforcing|balancing"
      description: "回路的内在机制描述"
      chain: ["变量序列"]
      dominance_condition: "该回路主导系统时的条件"
      effect_on_structure: "该回路如何维持或改变L2的结构"
  interest_alignment:
    beneficiaries: ["从现有结构中受益的群体"]
    benefit_mechanism: "受益机制"
    resistance_to_change: "这些群体抵制变革的方式和强度"
  system_resistance:
    sources: ["系统抗性的来源"]
    historical_evidence: "历史上改变尝试失败的案例和原因"
    counter_mechanisms: "在什么条件下，替代机制可能占据主导？"
```

---

### L4: 范式层 (Paradigm Layer)

**核心问题**: 什么信念、价值观、世界观使L3中的机制被认为理所当然（甚至不被视为"可以选择"的）？

**分析任务**:
- 识别底层假设: 在L0-L3的分析中，哪些命题被当作"不言自明"的真理？
- 区分三种假设: (1) 可验证的事实假设 (2) 被广泛接受但未验证的信念 (3) 不可验证的价值判断
- 范式溯源: 这些假设来自什么思想传统/文化/意识形态？
- 替代范式检验: 如果采用完全不同的范式，L0-L3中的每个判断会如何变化？
- 识别"受惑于范式"的盲区: 在现有范式下，什么问题甚至不会被提出？

**触发条件**: L3完成 + 追问"为什么人们接受这些机制？换一种完全不同的范式会怎样？"

**终止条件**（全部满足才进入综合分析）:
- [ ] 至少3个底层假设被显式化
- [ ] 每个假设被分类为: 可验证事实/未验证信念/不可验证价值
- [ ] 假设的来源（思想传统/文化/意识形态）被追溯
- [ ] 至少1个替代范式被认真检验
- [ ] 在替代范式下，L0-L3的分析哪些会改变、哪些不变——被明确标注
- [ ] 当前范式下的"不可问之问题"（taboo questions）被识别

**典型输出**:
```yaml
L4_paradigm:
  foundational_assumptions:
    - assumption: "底层假设陈述"
      type: "verifiable_fact|unverified_belief|value_judgment"
      origin: "该假设的思想/文化/意识形态来源"
      questioned_in_L0_L3: "true|false（在前几层中是否被追问过？）"
      if_false: "如果该假设为假，L0-L3的哪些结论会改变？"
  paradigm_genealogy:
    tradition: "该范式的思想传统溯源"
    historical_formation: "该范式是如何历史地形成的？"
    dominance_reason: "该范式为什么成为主导（而非其他范式）？"
  alternative_paradigm:
    name: "替代范式名称"
    core_assumptions: ["替代范式的核心假设"]
    implications: "在替代范式下，L0-L3的分析结论如何不同？"
    irreconcilable_differences: "两种范式之间不可调和的差异"
  paradigm_blind_spots:
    unasked_questions: ["在当前范式下不会被提出的问题"]
    excluded_perspectives: ["被当前范式排除的视角"]
    cross_paradigm_insights: ["跨范式比较产生的新洞察"]
```

---

## 4. 剥开层级的纪律规则

| 规则 | 内容 | 违反示例 |
|------|------|----------|
| **不可跳跃** | L0→L2 跳过 L1 是禁止的 | "销售额下降是因为市场结构问题"（跳过了"什么直接行为导致了下降"） |
| **不可混淆** | L1的直接原因不能与L2的结构原因混为一谈 | "管理层决策失误是结构性原因"（不对——是行为原因，属L1） |
| **不可早停** | 在L1或L2停止必须给出明确理由 | 默认必须抵达L4范式层；提前终止需写"停止声明" |
| **可回溯** | 上层发现可能修改对下层的解释 | 在L4发现某个"事实"实为价值观假设 → 回溯修改L0 |
| **每层自洽** | 每层的分析在内部必须逻辑自洽 | L2的结论不能与L1的因果链相矛盾 |

### 4.1 提前终止声明模板

如果在某层决定不继续剥开，必须填写：

```yaml
early_termination:
  stopped_at_layer: "L1|L2|L3"
  reason: "停止原因（实证需求已满足 | 超出分析范围 | 资源/时间约束）"
  what_is_left_unexamined: "未分析的更深层可能包含什么？"
  risk_of_early_stop: "提前停止可能导致什么误解？"
  reentry_condition: "在什么条件下应重新启动更深层的分析？"
```

---

## 5. 常见陷阱

1. **混淆"表象"与"原因"**: 将同一现象的不同表述当作因果解释——"销售额下降是因为收入减少"（销售额就是收入）。**纠正**: 原因必须是不同变量。
2. **结构归因过早停止**: "这是制度问题"——然后呢？什么维持了这个制度？**纠正**: 在结构层（L2）结束时追问"这个结构为什么没有被改变？"强制进入L3。
3. **范式层的虚无主义**: "一切都是视角——没有真理。" → 分析结束。**纠正**: 范式层不是终点——它是"在知道这一切后，什么仍然成立？"的起点。
4. **层间不连贯**: L2的分析和L1的分析无法衔接——L2说的结构问题和L1说的直接原因之间的因果链缺失。**纠正**: 每层之间的过渡必须有明确的因果链条。
5. **伪深度**: 用复杂的术语和框架包装简单观察。**纠正**: 每层的分析必须产生可验证的新认知——如果某层的结论去掉专业术语后和上一层相同，说明没有真正剥开。

---

## 6. 输出模板（完整五层）

```yaml
layer_peeling_analysis:
  problem: "待分析的原始问题"
  scope: "分析范围声明"

  L0_surface:
    phenomenon: "现象描述"
    time_scope: "时间范围"
    spatial_scope: "空间/领域范围"
    magnitude: "量级"
    data_sources: ["数据来源"]
    observation_vs_interpretation:
      observations: ["纯观察"]
      deferred_interpretations: ["推迟到L1的解释"]

  L1_direct_cause:
    causes:
      - cause: "直接原因"
        mechanism: "因果机制"
        necessity: "necessary|sufficient|contributory"
        evidence_level: "L0|L1|L2|L3"
        counterfactual_test: "反事实检验结果"
    L1_to_L2_transition: "从直接原因到结构性因素的因果过渡"

  L2_structural:
    institutional_constraints: [{同上模板}]
    power_structure: [{同上模板}]
    path_dependency: [{同上模板}]
    L2_to_L3_transition: "从结构因素到维持机制的因果过渡"

  L3_mechanism:
    feedback_loops: [{同上模板}]
    interest_alignment: [{同上模板}]
    system_resistance: [{同上模板}]
    L3_to_L4_transition: "从维持机制到范式的因果过渡"

  L4_paradigm:
    foundational_assumptions: [{同上模板}]
    paradigm_genealogy: [{同上模板}]
    alternative_paradigm: [{同上模板}]
    paradigm_blind_spots: [{同上模板}]

  synthesis:
    cross_layer_insights: "跨五层的核心洞见（每层贡献了什么独特认知？）"
    depth_audit:
      max_depth_reached: "L0|L1|L2|L3|L4"
      early_termination: "null | {reason, risk, reentry_condition}"
      layer_coherence: "各层之间因果链是否连贯？"
    what_changed: "经过五层剥开，对问题的最初理解发生了什么改变？"
    actionable_insight: "在了解了所有层面之后，最有价值的可行动洞察是什么？"

  uncertainty_declaration:
    layer_specific_uncertainties: "各层独有的不确定性"
    cross_layer_uncertainties: "跨层的不确定性（某层的假设影响了另一层的推导）"
    unresolved_tensions: "层间的未解决矛盾"
```

---

## 7. 快速调用指南

当问题包含以下特征时，优先使用本骨架：
- 问题表面上很简单，但直觉告诉你不应该停止在一个浅层答案上
- 反复出现的长期性问题（"为什么这个问题总是解决不了？"）
- 存在明显的"我们所做的应该有效但就是无效"的矛盾
- 需要挖掘隐含假设和思维盲区
- 需要在多个分析层次之间建立因果连贯性

---

## 8. 失败模式闭环清单（D6.4.4）

> 本节为逐层剥开推理模板的「失败模式 → 检测信号 → 恢复策略」闭环清单。当检测到失败模式时，必须执行对应的恢复策略。

| 失败模式 | 检测信号 | 恢复策略 |
|---------|---------|---------|
| **混淆表象与原因** | 将同一现象的不同表述当作因果解释（如"销售额下降是因为收入减少"——销售额就是收入） | 原因必须是不同变量：检验 cause ≠ effect_variable；若相同，重新识别真正的直接原因 |
| **层级跳跃** | 从L0直接跳到L2或L3，跳过中间层（如"销售额下降是因为市场结构问题"跳过L1） | 强制逐层推导：不可跳跃规则——L0→L1→L2→L3→L4，每层必须完成并满足终止条件后才进入下一层 |
| **层级混淆** | 将L1的直接原因与L2的结构原因混为一谈（如"管理层决策失误是结构性原因"） | 区分"行为"（L1）与"结构"（L2）：行为是结构下的个体选择，结构是相对稳定的约束条件 |
| **结构归因过早停止** | 在L2停止，未追问"这个结构为什么没有被改变？"（未进入L3机制层） | 强制进入L3：在L2结束时追问"这个结构为什么能持续存在？"，识别维持机制的反馈回路 |
| **范式层虚无主义** | 在L4得出"一切都是视角——没有真理"后停止分析 | 范式层不是终点——它是"在知道这一切后，什么仍然成立？"的起点；标注范式后继续提取可行动洞察 |
| **层间不连贯** | L2的分析与L1无法衔接，L2说的结构问题和L1说的直接原因之间因果链缺失 | 每层之间的过渡必须有明确的因果链条：填写 L1_to_L2_transition / L2_to_L3_transition / L3_to_L4_transition |
| **伪深度** | 用复杂的术语和框架包装简单观察，去掉专业术语后和上一层相同 | 每层的分析必须产生可验证的新认知：若某层结论去掉术语后与上一层相同，说明没有真正剥开 |
| **提前终止未声明** | 在L1或L2停止但未填写提前终止声明 | 强制填写 early_termination 声明：stopped_at_layer + reason + what_is_left_unexamined + risk + reentry_condition |
| **假设类型混淆** | 将不可验证的价值判断当作可验证的事实假设 | 对每个假设分类：verifiable_fact / unverified_belief / value_judgment；价值判断不可实证裁决 |
| **替代范式检验敷衍** | 仅提及替代范式但未认真检验其对L0-L3分析的影响 | 至少1个替代范式被认真检验：在替代范式下，L0-L3的哪些结论会改变、哪些不变——必须明确标注 |

### 8.1 失败模式检测与恢复的执行伪代码

```python
def detect_and_recover_layer_peeling_failures(analysis):
    """
    逐层剥开推理失败模式检测与恢复（D6.4.4）
    """
    failures = []

    # 检测1: 混淆表象与原因
    for cause in analysis.get("L1_direct_cause", {}).get("causes", []):
        if cause["cause"] == analysis["L0_surface"]["phenomenon"]:
            failures.append({
                "failure_mode": "phenomenon_as_cause",
                "layer": "L1",
                "recovery": reidentify_direct_causes(analysis["L0_surface"])
            })

    # 检测2: 层级跳跃
    expected_order = ["L0_surface", "L1_direct_cause", "L2_structural", "L3_mechanism", "L4_paradigm"]
    for i, layer in enumerate(expected_order[1:], 1):
        if layer in analysis and expected_order[i-1] not in analysis:
            failures.append({
                "failure_mode": "layer_skip",
                "skipped_from": expected_order[i-1],
                "skipped_to": layer,
                "recovery": fill_skipped_layers(analysis, expected_order[i-1], layer)
            })

    # 检测3: 层级混淆（行为 vs 结构）
    if "L2_structural" in analysis:
        for constraint in analysis["L2_structural"].get("institutional_constraints", []):
            if constraint.get("type") == "behavioral":
                failures.append({
                    "failure_mode": "layer_conflation",
                    "recovery": move_to_l1(constraint)
                })

    # 检测4: 结构归因过早停止（L3缺失）
    if "L2_structural" in analysis and "L3_mechanism" not in analysis:
        failures.append({
            "failure_mode": "premature_structural_stop",
            "recovery": force_enter_l3(analysis["L2_structural"])
        })

    # 检测5: 范式层虚无主义
    if "L4_paradigm" in analysis:
        l4_synthesis = analysis.get("synthesis", {}).get("actionable_insight", "")
        if not l4_synthesis or "没有真理" in str(l4_synthesis):
            failures.append({
                "failure_mode": "paradigmatic_nihilism",
                "recovery": extract_post_paradigm_insights(analysis["L4_paradigm"])
            })

    # 检测6: 层间不连贯
    for i in range(len(expected_order) - 1):
        current = expected_order[i]
        next_layer = expected_order[i + 1]
        transition_key = f"{current.split('_')[0]}_to_{next_layer.split('_')[0]}_transition"
        if current in analysis and next_layer in analysis:
            if transition_key not in analysis[current] and f"{current.split('_')[0]}_to_{next_layer.split('_')[0]}_transition" not in analysis.get(current, {}):
                failures.append({
                    "failure_mode": "layer_incoherence",
                    "layers": (current, next_layer),
                    "recovery": describe_causal_transition(analysis[current], next_layer)
                })

    # 检测7: 伪深度
    for i in range(1, len(expected_order)):
        current = expected_order[i]
        prev = expected_order[i - 1]
        if current in analysis and prev in analysis:
            if not produces_novel_insight(analysis[current], analysis[prev]):
                failures.append({
                    "failure_mode": "pseudo_depth",
                    "layer": current,
                    "recovery": deepen_analysis(analysis[current], require_novelty=True)
                })

    # 检测8: 提前终止未声明
    max_depth = analysis.get("synthesis", {}).get("depth_audit", {}).get("max_depth_reached", "")
    if max_depth and max_depth != "L4":
        early_term = analysis.get("synthesis", {}).get("depth_audit", {}).get("early_termination")
        if not early_term:
            failures.append({
                "failure_mode": "undeclared_early_termination",
                "stopped_at": max_depth,
                "recovery": fill_early_termination_declaration(analysis, max_depth)
            })

    # 检测9: 假设类型混淆
    if "L4_paradigm" in analysis:
        for assumption in analysis["L4_paradigm"].get("foundational_assumptions", []):
            if assumption["type"] == "value_judgment" and assumption.get("claimed_as_fact"):
                failures.append({
                    "failure_mode": "assumption_type_confusion",
                    "assumption": assumption,
                    "recovery": reclassify_assumption(assumption, correct_type="value_judgment")
                })

    # 检测10: 替代范式检验敷衍
    if "L4_paradigm" in analysis:
        alt = analysis["L4_paradigm"].get("alternative_paradigm", {})
        if not alt.get("implications") or alt.get("implications") == "无变化":
            failures.append({
                "failure_mode": "superficial_alternative_paradigm",
                "recovery": seriously_test_alternative_paradigm(analysis, alt)
            })

    return failures
```

---

© 阿洋