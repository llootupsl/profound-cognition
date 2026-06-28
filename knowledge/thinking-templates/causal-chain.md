# 因果链分析 — 从相关性到因果机制的逐层追溯

> **模块标识**: `knowledge/thinking-templates/causal-chain`
> **设计依据**: 基于全域深度认知框架三层推理架构设计——因果关系链追溯遵循"相关性识别→因果方向判定→机制链构建→反向验证"四步递进逻辑，融合系统动力学建模与第一性原理拆解的思想
> **依赖**: `knowledge/research-methods`、`knowledge/cognitive-framework`
> **骨架类型**: 因果链分析 (Causal Chain Analysis)
>
> **版本治理元数据 (D12.4.2)**:
> - version: 1.1
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（因果链四步递进分析）
>   - v1.1 补全版本治理元数据与交叉引用（D12.4.2-D12.4.3）

## 交叉引用

- **上游**: `knowledge/research-methods.md`（九层研究底座）、`knowledge/cognitive-framework.md`（认知流水线）
- **下游**: `tasks/T09_cog_reason.md`（认知推理，应用因果链模板）、`tasks/TM02_causal_verification.md`（因果验证，深化因果链分析）
- **相关**: `knowledge/thinking-templates/system-dynamics.md`（系统动力学模板）、`knowledge/thinking-models/general/first-principles.md`（第一性原理）、`knowledge/thinking-models/general/counterfactual-reasoning.md`（反事实推理）、`knowledge/thinking-models/routing-table.md`（思维模型路由表）

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
- `knowledge/thinking-models/general/first-principles.md`（第一性原理 — 因果链追溯的还原论基础）
- `knowledge/thinking-models/general/counterfactual-reasoning.md`（反事实推理 — 因果方向判定的逻辑基础）

**边界声明**：本模板提供六步因果链分析的执行流程（步骤1-6的伪代码），不重复阐述第一性原理的还原论哲学基础或反事实推理的 Lewis 语义学理论。当需要理论依据时，调用上述模型文件。

---

## 1. 定义

因果链分析是一种将复杂现象逐层追溯其因果链条的系统化推理方法。它拒绝将"相关性"等同于"因果性"，拒绝停留在单一层面的原因解释，而是要求分析者在每个因果节点上追问"是什么导致了这一步？"，直到追溯至不可再分的基础驱动力。因果链的每个环节必须满足因果三要素：时间先后、关联存在、排除替代解释。

**核心法则**: 每一个"因为"后面必须能回答"这个因为又是被什么引起的？"

---

## 2. 核心概念

| 概念 | 定义 | 判别标准 |
|------|------|----------|
| **直接原因** | 在时间上最接近结果、无中间变量的原因 | "去掉它，结果是否立即改变？" |
| **间接原因** | 通过中间变量传导影响的远端原因 | 因果链长度 ≥ 2 |
| **根因** | 因果链追溯终点，不可再分解的基础驱动因素 | "它是由什么引起的？" → 无法再回答 |
| **混淆变量** | 同时影响原因和结果的第三变量 | 控制后因果强度是否降低 ≥ 30%？ |
| **中介变量** | 因果链条中的传导节点 | 原因通过它传递到结果 |
| **调节变量** | 改变因果强度或方向的条件变量 | 在不同水平下因果效应是否显著不同？ |
| **虚假因果** | 看似有因果关系实则为共因或巧合的关系 | 控制共因后关联是否消失？ |
| **因果链反馈** | 因果链的终端影响回传到前端的闭环 | 输出变量的变化是否反作用于输入变量？ |
| **因果强度** | 原因对结果的影响量级 | 效应量 (Cohen's d / β / OR) |

---

## 3. 六步因果链分析流程

```
步骤1: 问题定义
  ├─ 明确待解释的"结果变量": 可量化、有明确时间边界
  ├─ 定义分析的时间范围: 起点和终点
  └─ 声明排除的维度: 哪些可能相关但本次不分析
        │
步骤2: 候选原因识别
  ├─ 脑暴所有可能影响结果的因素（不设约束）
  ├─ 按来源分类: 内生因素 vs 外生因素 vs 结构因素
  ├─ 按性质分类: 物理/制度/行为/认知/随机
  ├─ [v3] causal-learn 因果发现: 基于 TC-086 causal-learn 方法论：PC算法骨架学习→V结构定向→Meek规则 / GES前向搜索+后向搜索+BIC评分 / LiNGAM-ICA非混合→因果序→回归剪枝
  └─ [v3] 标注 causal-learn 发现的因果关系 vs 理论推导的因果关系
        │
步骤3: 因果链MECE构建
  ├─ 对每个候选原因追问"是什么引起的？"构建因果树
  ├─ 合并交叉的因果枝，识别共同上游节点
  ├─ 标注每条因果链的类型: 直接/间接/反馈
  ├─ 标注混淆变量和中介变量
  └─ 检查 MECE: 因果链之间互斥且整体穷尽
        │
步骤4: 关键节点识别
  ├─ 计算每个节点的因果效应量（或估算其相对强度）
  ├─ 识别"瓶颈节点": 因果链中效应最大或最可干预的点
  ├─ 识别"分叉节点": 一个原因作用于多个下游结果
  └─ 识别"汇聚节点": 多个原因汇聚到同一结果
        │
步骤5: 反向验证
  ├─ 推演: 若移除某节点，下游因果链是否断裂？
  ├─ 反事实检验: 若某节点取反值，结论方向是否翻转？
  ├─ 替代因果解释: 是否存在与当前因果链等价但机制不同的解释？
  └─ 证据谱系检验: 每个因果环节的证据等级 (L0-L3)
        │
步骤6: 结论
  ├─ 主因果链: 从根因到结果的完整因果路径
  ├─ 因果归因: 每个环节的效应量与置信度
  ├─ 替代因果链: 被排除但值得关注的备选因果路径
  ├─ 不确定性声明: 因果推断的局限性（混淆变量可能未完全控制等）
  └─ 可干预点排序: 按干预可行性和因果效应量排序
```

### 3.1 可执行伪代码（D6.4.3）

```python
def causal_chain_analysis(problem, time_scope, excluded_dimensions):
    """
    因果链分析模板 - 可执行伪代码（D6.4.3）
    输入: problem(问题陈述), time_scope(时间范围), excluded_dimensions(排除维度)
    输出: causal_chain_analysis YAML（见 §6 输出模板）
    """
    # ===== 步骤1: 问题定义 =====
    effect_variable = define_effect_variable(problem)  # 可量化、有明确时间边界
    assert is_quantifiable(effect_variable), "结果变量必须可量化"
    analysis_scope = {
        "time_scope": time_scope,
        "excluded_dimensions": excluded_dimensions
    }

    # ===== 步骤2: 候选原因识别 =====
    candidates = brainstorm_candidates(effect_variable)  # 不设约束脑暴
    candidates = classify_by_source(candidates)  # 内生/外生/结构
    candidates = classify_by_nature(candidates)  # 物理/制度/行为/认知/随机

    # [v3] causal-learn 因果发现（TC-086）
    if causal_learn_available and has_structured_data(candidates):
        cl_results = causal_learn_discover(
            candidates,
            algorithms=["PC", "GES", "LiNGAM"],  # 至少3种交叉验证
            cross_validate=True
        )
        candidates = annotate_source(candidates, cl_results)  # data_driven vs theory_driven

    # ===== 步骤3: 因果链MECE构建 =====
    causal_tree = build_causal_tree(candidates)  # 对每个候选追问"是什么引起的？"
    causal_tree = merge_cross_branches(causal_tree)  # 识别共同上游节点
    causal_tree = annotate_chain_type(causal_tree)  # 直接/间接/反馈
    causal_tree = annotate_confounders_mediators(causal_tree)  # 混淆变量/中介变量
    assert is_mece(causal_tree), "因果链必须互斥且整体穷尽"

    # ===== 步骤4: 关键节点识别 =====
    for node in causal_tree.nodes:
        node.effect_size = compute_effect_size(node)  # Cohen's d / β / OR（见 §9）
    bottleneck_nodes = identify_bottleneck_nodes(causal_tree)  # 效应最大或最可干预
    junction_nodes = identify_junction_nodes(causal_tree)  # 一因多果（分叉）
    convergence_nodes = identify_convergence_nodes(causal_tree)  # 多因一果（汇聚）

    # ===== 步骤5: 反向验证 =====
    for node in causal_tree.nodes:
        node.removal_test = simulate_removal(node)  # 移除后下游是否断裂？
        node.counterfactual = counterfactual_test(node)  # 取反值后结论是否翻转？
    alternative_chains = find_alternative_explanations(effect_variable)
    evidence_audit = audit_evidence_levels(causal_tree)  # 每个环节证据等级 L0-L3

    # ===== 步骤6: 结论 =====
    return {
        "primary_chain": trace_root_to_effect(causal_tree),  # 主因果链
        "attribution": [  # 因果归因
            {"node": n, "effect_size": n.effect_size, "confidence": n.confidence}
            for n in causal_tree.nodes
        ],
        "alternative_chains": alternative_chains,  # 替代因果链
        "uncertainty": declare_uncertainty(causal_tree),  # 不确定性声明
        "intervention_points": rank_interventions(bottleneck_nodes)  # 可干预点排序
    }
```

---

## 4. 因果推断的七条黄金法则

| 法则 | 内容 | 违反后果 |
|------|------|----------|
| **时间先行** | 原因必须在时间上先于结果 | 无法区分因果方向 |
| **非虚假性** | 排除共同原因驱动的虚假关联 | 将相关性误判为因果性 |
| **剂量-反应** | 原因强度变化与结果强度变化对应 | 阈值效应被忽略 |
| **可重复性** | 因果效应在不同条件下复现 | 将孤例当成普遍规律 |
| **可干预性** | 理论上可对原因进行干预并观测结果变化 | 混淆可干预因果与不可干预的结构性关联 |
| **机制透明** | 因果链条的每一步都有可验证的机制解释 | "黑箱因果"无法被检验 |
| **特异性** | 原因与结果之间的对应关系明确，不含糊 | 将多因一果误判为一因一果 |

---

## 5. 常见陷阱

1. **回归为名**: 以"这是多方面因素共同作用的结果"回避具体归因分析。**纠正**: 多因素必须按效应量排序，不可笼统。
2. **混淆相关性为因果性**: "A 和 B 高度相关，所以 A 导致 B"。**纠正**: 对每对 (A, B) 追问"有第三种因素 C 同时影响 A 和 B 吗？"
3. **因果链断裂**: 跳跃式推理——从"A出现"直接跳到"E发生"，跳过中间的 B、C、D。**纠正**: 因果链必须逐环推导，每环间距不超过一个因果步。
4. **因果方向反转**: 将结果误判为原因——"因为医院多，所以病人多"。**纠正**: 对每个因果关系追问时间顺序。
5. **选择性因果**: 只收集支持预设因果方向的证据，忽略反证。**纠正**: 对每条因果链主动寻找反向证据。
6. **层次混淆**: 将宏观结构原因（如"制度缺陷"）与微观行为原因（如"个人决策失误"）置于同一因果链层级。**纠正**: 因果链必须区分逻辑层次：范式层 > 制度层 > 行为层 > 事件层。

---

## 6. 输出模板

```yaml
causal_chain_analysis:
  problem_definition:
    effect_variable: "待解释的结果变量（量化定义）"
    time_scope: "分析的时间范围"
    excluded_dimensions: ["本次排除的维度及理由"]

  candidate_causes:
    endogenous: ["内生因素"]
    exogenous: ["外生因素"]
    structural: ["结构性因素"]

  causal_chain:
    primary_chain:
      - step: 1
        node: "节点名称"
        node_type: "root_cause|mediator|moderator|direct_cause"
        description: "因果机制的详细描述"
        evidence_level: "L0|L1|L2|L3"
        evidence_source: "证据来源"
        effect_size: "效应量（如有量化数据）"
        next: "指向下一个节点的因果关联"
      - step: N
        node: "最终结果"
        node_type: "effect"
        description: "结果状态描述"

    feedback_loops:
      - id: "FB-001"
        type: "reinforcing|balancing"
        chain: ["节点序列"]
        dominance_condition: "该反馈主导的条件"

  key_nodes:
    bottleneck_nodes: ["瓶颈节点及干预意义"]
    junction_nodes: ["分叉节点及影响范围"]
    convergence_nodes: ["汇聚节点及多因归并方式"]

  reverse_validation:
    removal_test: "移除关键节点后下游影响"
    counterfactual_test: "关键节点取反值后的因果链变化"
    alternative_chains: ["替代因果路径及排除理由"]
    evidence_audit: "各环节证据等级的分布与缺口"

  conclusions:
    main_causal_path: "从根因到结果的完整因果路径（一句话概述）"
    attribution:
      - node: "节点名称"
        contribution: "归因占比或效应量"
        confidence: "HIGH|MEDIUM|LOW|TENTATIVE"
    intervention_points:
      - node: "可干预节点"
        feasibility: "high|medium|low"
        expected_impact: "预期因果效应"
        time_lag: "干预到效果的预期延迟"

  uncertainty_declaration:
    unmeasured_confounders: "可能未控制的混淆变量"
    causal_direction_ambiguity: "因果方向不确定的环节"
    generalizability_limit: "因果链可推广的边界"
```

---

## 7. 快速调用指南

当问题包含以下特征时，优先使用本骨架：
- 问题形式为"为什么 X 会 Y？"
- 涉及明确的因果归因需求
- 需要区分相关性和因果性
- 需要为干预设计提供因果依据
- 问题涉及因果链中的反馈循环

---

## 8. causal-learn 因果发现集成（v3 新增）

> **能力卡**: TC-086 causal-learn

### 8.1 调用时机

在步骤 2（候选原因识别）中，当有结构化或半结构化数据可用时，调用 causal-learn 的因果发现算法：

```
causal-learn 调用流程:
1. 数据准备: 将因果变量转化为结构化的数值数据矩阵
2. 算法选择: 从 30+ 种算法中选择 3-5 种代表性算法
   - PC（约束式，基于条件独立检验）
   - GES（评分式，基于 BIC 评分搜索）
   - LiNGAM（函数式，基于非高斯性假设）
   - NOTEARS（连续优化式，基于可微分评分）
   - FCI（可处理潜在混淆变量）
3. 因果图学习: 各算法独立输出因果图（DAG/PAG）
4. 交叉验证: 至少 3 种算法一致的因果边才接受
5. 结果回注: 将 causal-learn 发现的因果图回注到 causal_chain_analysis.causal_chain

标注规则:
- causal-learn 发现的因果关系标注: source=causal-learn, algorithm={algorithm_name}
- 与理论推导的因果关系区分标注：data_driven vs theory_driven
```

### 8.2 与 DoWhy TC-057 的互补关系

```
causal-learn (TC-086) → DoWhy (TC-057) = 完整因果推断管道:
1. causal-learn: 从数据学习因果图结构（因果发现）
2. DoWhy: 基于因果图估计因果效应量（因果推断）
3. 输出: 因果图 + 因果效应量 + 反事实预测
```

---

## 9. 因果效应量计算步骤（v3 新增）

> **能力卡**: MC-152 Causal-Effect-Confounding

### 9.1 效应量公式体系

| 效应量指标 | 公式 | 适用数据类型 | 解释基准 |
|-----------|------|-------------|---------|
| **Cohen's d** | d = (M₁ - M₂) / S_pooled，其中 S_pooled = √[(S₁² + S₂²)/2] | 连续变量 vs 连续变量 | 标准差单位 |
| **标准化回归系数 β** | β = b × (S_X / S_Y)，其中 b 为原始回归系数 | 连续变量（控制其他变量后） | 标准差单位 |
| **优势比 (Odds Ratio)** | OR = (a/c) / (b/d) = ad/bc（2×2列联表） | 二分类变量 vs 二分类变量 | 几率倍数 |
| **相对风险 (RR)** | RR = [a/(a+b)] / [c/(c+d)] | 二分类暴露 vs 二分类结局 | 风险倍数 |
| **风险差 (RD)** | RD = [a/(a+b)] - [c/(c+d)] | 二分类暴露 vs 二分类结局 | 绝对概率差 |
| **Eta² (η²)** | η² = SS_between / SS_total | 分类变量 vs 连续变量 | 方差解释比例 |

### 9.2 效应量判定阈值

| 效应量指标 | 小效应 | 中效应 | 大效应 |
|-----------|--------|--------|--------|
| Cohen's d | 0.2 | 0.5 | 0.8 |
| 标准化 β | 0.10 | 0.30 | 0.50 |
| Odds Ratio | 1.5 / 0.67 | 2.5 / 0.40 | 4.3 / 0.23 |
| Eta² | 0.01 | 0.06 | 0.14 |

### 9.3 效应量计算执行步骤

```
步骤1: 确定变量类型组合（连续-连续 / 分类-连续 / 分类-分类）
步骤2: 选择对应效应量指标（见9.1公式体系）
步骤3: 收集或估算所需统计量（均值、标准差、频次等）
步骤4: 代入公式计算效应量点估计
步骤5: 计算 95% 置信区间（bootstrap 或解析方法）
步骤6: 按阈值表判定效应大小等级
步骤7: 标注效应量到 causal_chain_analysis.causal_chain.effect_size
```

---

## 10. 混淆变量识别四步法（v3 新增）

> **能力卡**: MC-152 Causal-Effect-Confounding

### 10.1 四步识别流程

```
步骤1: 绘制因果图骨架
  ├─ 列出所有已知变量（暴露X、结局Y、候选混淆C₁...Cₙ）
  ├─ 标注已知的因果方向（X→Y, C→X, C→Y）
  └─ 标注不确定的因果方向（用双向箭头标记）

步骤2: 应用后门准则（Back-door Criterion）
  ├─ 条件1: Z 不包含 X 的后代（控制后代会引入选择偏倚）
  ├─ 条件2: 控制 Z 后，X 到 Y 的所有后门路径被阻断
  └─ 满足条件的 Z 即为充分混淆控制集

步骤3: 量化混淆影响
  ├─ 计算粗效应量（未控制混淆）
  ├─ 计算调整效应量（控制混淆后）
  ├─ 混淆影响比 = |粗效应 - 调整效应| / |粗效应|
  └─ 混淆影响比 ≥ 10% → 该变量为实质性混淆变量

步骤4: 控制后阈值判定
  ├─ 控制所有识别的混淆变量后，重新计算效应量
  ├─ 若调整后效应量仍显著（p < 0.05 或 CI 不含 0/OR 不含 1）→ 因果关系稳健
  ├─ 若调整后效应量不显著 → 因果关系可能为虚假相关
  └─ 若调整后效应量方向翻转 → 存在辛普森悖论，需分层分析
```

### 10.2 混淆变量控制后阈值判定规则

| 控制后状态 | 判定 | 后续行动 |
|-----------|------|---------|
| 效应量变化 < 10% 且仍显著 | 混淆影响小，因果稳健 | 标注 LOW confounding risk |
| 效应量变化 10%-30% 且仍显著 | 存在混淆但因果仍成立 | 标注 MEDIUM confounding risk，报告调整前后效应量 |
| 效应量变化 > 30% 且仍显著 | 严重混淆，因果需谨慎解读 | 标注 HIGH confounding risk，必须报告调整后效应量 |
| 效应量变为不显著 | 因果关系可能为虚假相关 | 标注 POSSIBLE SPURIOUS，建议进一步验证 |
| 效应量方向翻转 | 辛普森悖论 | 标注 SIMPSON_PARADOX，必须分层分析 |

### 10.3 因果效应量与混淆控制输出 yaml 规范

```yaml
causal_effect_analysis:
  effect_sizes:
    - variable_pair: "X → Y"
      effect_type: "Cohen's d | β | OR | RR | η²"
      crude_estimate: float
      adjusted_estimate: float
      confidence_interval: [lower, upper]
      magnitude: "small|medium|large"
      significance: "significant|not_significant"
  confounding_assessment:
    - confounder: "混淆变量名"
      backdoor_path: "X ← C → Y"
      confounding_ratio: float
      control_status: "controlled|uncontrolled|partially_controlled"
      post_control_verdict: "LOW|MEDIUM|HIGH|POSSIBLE_SPURIOUS|SIMPSON_PARADOX"
  overall_causal_verdict:
    robustness: "robust|conditional|fragile|spurious"
    unmeasured_confounders: ["可能遗漏的混淆变量"]
    sensitivity_to_unmeasured: "E-value 或 Rosenbaum 界限"
```

### 10.4 因果效应量穷尽重试策略

```yaml
causal_effect_exhaust_retry:
  RETRYING_QUANTITATIVE:
    trigger: "无法获取量化数据计算效应量（无原始数据、仅有文献描述）"
    exhaust-retry: "使用定性效应量估计（大/中/小）替代定量计算，基于文献描述和专家判断"
    output_annotation: "因果效应量穷尽重试：使用定性估计替代定量计算"

  RETRYING_CONFOUNDING:
    trigger: "无法执行混淆变量控制（关键混淆变量无数据）"
    exhaust-retry: "使用倾向评分匹配的模拟估计或文献报告的调整值，标注为间接估计"
    output_annotation: "混淆控制穷尽重试：使用间接估计替代直接控制"

  FULL_EXHAUST_RETRY:
    trigger: "既无量化数据也无文献参考，因果效应量完全无法估计"
    exhaust-retry: "穷尽重试所有替代方法——使用LLM内建推理+类比推断输出因果方向（正/负/无）和定性强度（强/中/弱），持续重试直至获得更高质量证据"
    output_annotation: "因果效应量穷尽重试中：使用内建推理+类比推断输出定性因果方向和强度"
    confidence_adjustment: "因果结论 confidence 标注为 LOW，持续穷尽重试直至获得更高质量证据"
```

> 知识来源: MC-152 [Causal-Effect-Confounding]

---

## 11. causal-learn 30+算法分类与选择决策树（TC-086）

> **能力卡**: TC-086 causal-learn

### 11.1 算法分类体系

causal-learn 提供 30+ 种因果发现算法，按方法论分为5大类：

| 算法类别 | 核心方法 | 代表算法 | 适用数据类型 | 因果图输出 |
|---------|---------|---------|------------|-----------|
| **约束式** | 条件独立检验 | PC, PC-Stable, FCI, FCI-Max, CD-NOD, GES-Constraint | 连续/离散/混合 | CPDAG/PAG |
| **评分式** | BIC/BDeu评分搜索 | GES, MMHC, TABU, Hill-Climbing | 连续/离散 | CPDAG |
| **函数式** | 非高斯/非线性假设 | LiNGAM, ICA-LiNGAM, DirectLiNGAM, ANM, PNL | 连续（非高斯） | DAG |
| **连续优化式** | 可微分评分函数 | NOTEARS, NOTEARS-Linear, GOLEM, DAG-GNN, Gran-DAG | 连续 | DAG |
| **混合/其他** | 结合多种方法 | MMHC, CMU, SADA, CCDr | 连续/混合 | CPDAG/DAG |

### 11.2 算法选择决策树

```
数据输入
  │
  ├─ Q1: 数据类型？
  │   ├─ 连续数据 → Q2
  │   ├─ 离散数据 → Q4
  │   └─ 混合数据 → MMHC（混合式，唯一支持混合数据）
  │
  ├─ Q2: 数据是否满足非高斯假设？
  │   ├─ YES → Q3
  │   └─ NO → Q5
  │
  ├─ Q3: 变量间关系是否线性？
  │   ├─ YES → LiNGAM（函数式，线性非高斯，输出DAG）
  │   │         或 DirectLiNGAM（更稳健的LiNGAM变体）
  │   ├─ NO → ANM（加性噪声模型，非线性）
  │   │        或 PNL（后非线性模型，更一般）
  │   └─ 不确定 → LiNGAM + ANM 交叉验证
  │
  ├─ Q4: 离散数据因果发现
  │   ├─ 变量少（<10）→ PC + GES 交叉验证
  │   └─ 变量多（≥10）→ MMHC（混合式，效率更高）
  │
  ├─ Q5: 是否存在潜在混淆变量？
  │   ├─ YES → FCI（可处理潜在混淆，输出PAG）
  │   │         或 FCI-Max（FCI的优化版本）
  │   └─ NO → Q6
  │
  ├─ Q6: 变量数量？
  │   ├─ < 20 → PC + GES + NOTEARS（3种交叉验证）
  │   ├─ 20-100 → NOTEARS + GOLEM（连续优化，可扩展）
  │   └─ > 100 → SADA（分治式，大规模因果发现）
  │
  └─ 推荐默认组合：
      纯文本研究场景 → PC + GES + NOTEARS（3种交叉验证）
      有结构化数据场景 → PC + GES + LiNGAM + NOTEARS + GOLEM（5种交叉验证）
```

### 11.3 交叉验证规则

```
因果边接受标准:
- 至少3种算法一致的因果边 → 接受（标注 confidence: HIGH）
- 2种算法一致 → 接受但穷尽重试（标注 confidence: MEDIUM）
- 仅1种算法发现 → 不接受，标记为"弱证据"（标注 confidence: LOW）

因果方向判定:
- 所有发现该边的算法方向一致 → 方向确定
- 方向不一致 → 标注为"方向待定"，使用CPDAG表示（无向边）
```

### 11.4 causal-learn 与 profound-cognition Layer 对照映射

| causal-learn步骤 | 对应Layer | 映射说明 |
|-----------------|----------|---------|
| 数据准备 | Layer1 感知 | 原始数据感知与预处理 |
| 算法选择 | Layer2 分解 | 分解问题特征选择算法 |
| 因果图学习 | Layer4 推理 | 算法执行因果推理 |
| 交叉验证 | Layer5 反事实 | 多算法交叉验证检验 |
| 结果回注 | Layer6 因果 | 因果图回注因果链分析 |

### 11.5 causal-learn 穷尽重试策略

```yaml
causal_learn_exhaust_retry:
  L1_FULL:
    condition: "causal-learn可用，5类算法均可选"
    action: "按决策树选择3-5种算法+交叉验证"
    confidence: "HIGH"

  L2_PARTIAL_ALGORITHMS:
    condition: "部分算法不可用（如LiNGAM需要非高斯数据但数据为高斯）"
    action: "使用可用算法子集，至少保证2种不同类别的算法交叉验证"
    confidence: "MEDIUM"
    output_annotation: "causal-learn部分穷尽重试：算法子集交叉验证"

  L3_SINGLE_ALGORITHM:
    condition: "仅1种算法可用"
    action: "使用单一算法但增加bootstrap验证（100次重采样）"
    confidence: "LOW-MEDIUM"
    output_annotation: "causal-learn穷尽重试：单一算法+bootstrap验证"

  L4_QUALITATIVE_CAUSAL:
    condition: "causal-learn完全不可用"
    action: "纯定性因果分析——基于文献推理+因果三要素检验"
    confidence: "LOW"
    output_annotation: "causal-learn完全穷尽重试：纯定性因果分析"
```

> 知识来源: TC-086 [causal-learn]

---

### [causal-learn] 源码逻辑引入

#### 核心算法逻辑

**1. PC 算法源码级伪代码**

```
PC算法核心流程（causallearn/search/ConstraintBased/PC.py）:

function PC(data, alpha=0.05, indep_test="fisherz"):
    # 阶段1：骨架学习（条件独立性检验）
    G = complete_graph(data.variables)  # 完全无向图
    sep_set = {}  # 分离集：记录使X⊥Y|S的S

    depth = 0
    while depth <= max_adjacent(G) - 1:
        for (X, Y) in edges(G):
            # 找X的所有相邻节点（除Y外）
            adj_X = neighbors(G, X) - {Y}

            # 枚举depth大小的条件集
            for S in combinations(adj_X, depth):
                # 条件独立性检验
                p_value = indep_test(data, X, Y, S)
                if p_value > alpha:
                    # X ⊥ Y | S → 移除边 X-Y
                    remove_edge(G, X, Y)
                    sep_set[(X, Y)] = S
                    sep_set[(Y, X)] = S
                    break  # 找到一个分离集即可

        depth += 1

    # 阶段2：方向定向（V-结构和方向传播）
    for (X, Y, Z) in unshielded_triples(G):
        # V-结构：X-Y-Z且X和Z不相邻
        if Y not in sep_set[(X, Z)]:
            # Y不在X-Z的分离集中 → V-结构 X→Y←Z
            orient_edge(G, X, Y, direction=X→Y)
            orient_edge(G, Z, Y, direction=Z→Y)

    # 方向传播规则（Meek规则）
    repeat until no_change:
        # R1: X→Y-Z且X和Z不相邻 → Y→Z
        # R2: X→Y→Z且X-Z → X→Z
        # R3: X-Y→Z且X-W→Z且Y和W不相邻 → X→Z
        # R4: X-Y→Z且X→W→Z且W-Y → Y→Z
        apply_meek_rules(G)

    return G  # 部分有向无环图（CPDAG）
```

**2. GES 算法源码级伪代码**

```
GES算法核心流程（causallearn/search/ScoreBased/GES.py）:

function GES(data, score_func="local_BIC"):
    # 阶段1：前向搜索（添加边）
    G = empty_graph(data.variables)  # 空图
    while True:
        best_score = -inf
        best_edge = None

        for (X, Y) in all_possible_edges(G):
            if edge_exists(G, X, Y):
                continue

            # 尝试添加边 X→Y
            G_temp = add_edge(G, X, Y)
            if is_dag(G_temp):  # 确保无环
                score_delta = compute_local_score(G_temp, X, Y, data) -
                              compute_local_score(G, X, Y, data)
                if score_delta > best_score:
                    best_score = score_delta
                    best_edge = (X, Y, X→Y)

        if best_score <= 0:
            break  # 无法通过添加边改善评分
        G = add_edge(G, best_edge)

    # 阶段2：后向搜索（删除边）
    while True:
        best_score = -inf
        best_edge = None

        for (X, Y) in edges(G):
            # 尝试删除边 X-Y
            G_temp = remove_edge(G, X, Y)
            score_delta = compute_local_score(G_temp, X, Y, data) -
                          compute_local_score(G, X, Y, data)
            if score_delta > best_score:
                best_score = score_delta
                best_edge = (X, Y)

        if best_score <= 0:
            break  # 无法通过删除边改善评分
        G = remove_edge(G, best_edge)

    return G  # CPDAG

# BIC局部评分:
function compute_local_score(G, X, Y, data):
    # local_BIC = log_likelihood(X, parents(X), data) - k/2 * log(n)
    # k = 参数数量, n = 样本量
    parents_X = get_parents(G, X)
    ll = gaussian_log_likelihood(data[X], data[parents_X])
    k = len(parents_X) + 1  # 回归系数+方差
    return ll - k / 2 * log(len(data))
```

**3. LiNGAM 算法源码级伪代码**

```
LiNGAM算法核心流程（causallearn/search/FCMBased/LiNGAM.py）:

function LiNGAM(data):
    # 前提：变量间为线性关系且误差项非高斯

    # 步骤1：中心化数据
    X = center(data)

    # 步骤2：ICA独立成分分析
    # 混合模型: X = B * X + E → (I-B) * X = E → X = A * E
    # 其中 A = (I-B)^(-1) 是混合矩阵
    W = fastICA(X)  # 解混矩阵，W * X ≈ E

    # 步骤3：从W恢复因果矩阵B
    # A = W^(-1) = (I-B)^(-1) → B = I - A^(-1) = I - W
    # 但需要确定变量排列顺序

    # 步骤4：确定因果顺序（因果变量应在残差中最先出现）
    # 使用基于残差的排列方法
    order = find_causal_order(W, X)

    # 步骤5：按因果顺序回归得到B矩阵
    B = zeros(n_vars, n_vars)
    for i in range(1, n_vars):
        for j in range(i):
            # X[order[i]] 对 X[order[j]] (j<i) 回归
            B[order[i], order[j]] = regression_coefficient(
                X[order[i]], X[order[j]]
            )

    # 步骤6：剪枝（移除接近零的系数）
    for i, j in indices(B):
        if abs(B[i, j]) < threshold:
            B[i, j] = 0

    # B[i,j] ≠ 0 → X[j] → X[i] (j是i的因果父节点)
    return B  # 因果邻接矩阵

function find_causal_order(W, X):
    # 基于行范数确定因果顺序
    # 因果源变量的W行范数最小（残差独立性最强）
    row_norms = [norm(W[i]) for i in range(n_vars)]
    order = argsort(row_norms)  # 按范数升序排列
    return order
```

#### 数据结构设计

```
核心数据结构:

1. CausalGraph: 因果图
   - G: nx.Graph or adjacency_matrix  # 无向/有向图
   - sep_set: Dict[(node, node), set]  # PC算法分离集
   - is_dag(): bool                    # 是否为DAG

2. PCResult: PC算法结果
   - G: CausalGraph           # 学习到的CPDAG
   - sep_set: Dict            # 分离集
   - p_values: Dict           # 条件独立性p值

3. GESResult: GES算法结果
   - G: CausalGraph           # 学习到的CPDAG
   - score: float             # 最终BIC评分
   - edge_operations: list    # 添加/删除边的操作序列

4. LiNGAMResult: LiNGAM结果
   - B: ndarray               # 因果邻接矩阵 B[i,j]=X[j]→X[i]
   - causal_order: list       # 因果变量顺序
   - residuals: ndarray       # 独立残差
```

#### 决策流程

```
causal-learn 算法选择决策流程:

1. 数据类型判断
   ├─ 连续变量 → Q2
   └─ 混合/离散变量 → PC (约束法)

2. 连续变量 → 分布假设
   ├─ 高斯分布 → PC 或 GES
   ├─ 非高斯分布 → LiNGAM
   └─ 未知分布 → PC (非参数检验)

3. 样本量判断
   ├─ n > 1000 → GES (评分法更高效)
   └─ n < 1000 → PC (约束法更稳健)

4. 交叉验证 → 至少2种不同类别算法验证
```

#### 穷尽重试策略

```yaml
causal_learn_source_exhaust_retry:
  L1_FULL_ALGORITHMS:
    condition: "causal-learn可用，5类算法均可选"
    action: "按决策树选择3-5种算法+交叉验证"
    confidence: "HIGH"

  L2_PARTIAL_ALGORITHMS:
    condition: "部分算法不可用"
    action: "使用可用算法子集，至少2种不同类别交叉验证"
    confidence: "MEDIUM"
    output_annotation: "causal-learn部分穷尽重试：算法子集交叉验证"

  L3_SINGLE_ALGORITHM:
    condition: "仅1种算法可用"
    action: "单一算法+bootstrap验证（100次重采样）"
    confidence: "LOW-MEDIUM"
    output_annotation: "causal-learn穷尽重试：单一算法+bootstrap验证"

  L4_QUALITATIVE_CAUSAL:
    condition: "causal-learn完全不可用"
    action: "纯定性因果分析——基于文献推理+因果三要素检验"
    confidence: "LOW"
    output_annotation: "causal-learn完全穷尽重试：纯定性因果分析"
```

---

## 12. 失败模式闭环清单（D6.4.4）

> 本节为因果链分析模板的「失败模式 → 检测信号 → 恢复策略」闭环清单。当检测到失败模式时，必须执行对应的恢复策略。

| 失败模式 | 检测信号 | 恢复策略 |
|---------|---------|---------|
| **相关性误判为因果性** | 高相关系数但无时间先后证据，或无合理的因果机制解释 | 启动因果三要素检验：(1)时间先行 (2)关联存在 (3)排除替代解释；若三要素任一不满足，降级为"相关关系"而非"因果关系" |
| **因果链断裂** | 从节点A直接跳到节点E，跳过中间的B/C/D，因果步距>1 | 强制逐环推导：对每对相邻节点追问"是什么引起的？"，每环间距不超过一个因果步；补全缺失的中间节点 |
| **因果方向反转** | 将结果误判为原因（如"医院多导致病人多"） | 对每个因果关系追问时间顺序：原因必须在时间上先于结果；使用反事实检验验证方向 |
| **混淆变量未控制** | 控制前后效应量变化>10%，或存在已知的共同原因 | 执行混淆变量识别四步法（§10）：绘制因果图骨架→应用后门准则→量化混淆影响→控制后阈值判定 |
| **选择性因果** | 仅收集支持预设因果方向的证据，忽略反证 | 对每条因果链主动寻找至少2个反向证据；实施"红队"挑战，尝试推翻自己的因果结论 |
| **层次混淆** | 将宏观结构原因与微观行为原因置于同一因果链层级 | 区分因果链逻辑层次：范式层 > 制度层 > 行为层 > 事件层；每层原因归入对应层级 |
| **虚假反馈回路** | 将线性因果链误判为反馈回路，或反馈方向标注错误 | 检验反馈回路闭合性：终端节点必须反作用于起始节点；标注回路极性（R增强/B平衡） |
| **证据等级不足** | 因果链关键节点的证据等级为L0（无证据）或仅有孤证 | 启动穷尽重试策略：寻找更多证据源；若仍无法获得，标注 confidence=LOW 并声明局限性 |
| **MECE违反** | 因果链之间有重叠，或存在未覆盖的候选原因 | 重新构建因果树：合并重叠分支，补充遗漏的候选原因，确保互斥且整体穷尽 |
| **过度归因** | 将多因一果简化为单一原因，或效应量分配之和>100% | 强制归因分解：对多因一果的汇聚节点，各原因效应量之和应≤100%；标注各原因的独立贡献率 |

### 12.1 失败模式检测与恢复的执行伪代码

```python
def detect_and_recover_causal_chain_failures(causal_tree):
    """
    因果链分析失败模式检测与恢复（D6.4.4）
    """
    failures = []

    for node in causal_tree.nodes:
        # 检测1: 相关性误判为因果性
        if node.correlation_high and not node.has_temporal_precedence:
            failures.append({
                "failure_mode": "correlation_as_causation",
                "node": node,
                "recovery": apply_causal_triad_test(node)
            })

        # 检测2: 因果链断裂
        if node.causal_step_distance > 1:
            failures.append({
                "failure_mode": "chain_break",
                "node": node,
                "recovery": fill_intermediate_nodes(node)
            })

        # 检测3: 因果方向反转
        if not node.temporal_order_correct:
            failures.append({
                "failure_mode": "direction_reversal",
                "node": node,
                "recovery": reverse_causal_direction(node)
            })

        # 检测4: 混淆变量未控制
        if node.confounding_ratio > 0.10:
            failures.append({
                "failure_mode": "uncontrolled_confounder",
                "node": node,
                "recovery": apply_backdoor_criterion(node)
            })

        # 检测5: 证据等级不足
        if node.evidence_level == "L0" or node.evidence_count < 2:
            failures.append({
                "failure_mode": "insufficient_evidence",
                "node": node,
                "recovery": exhaust_retry_evidence_collection(node)
            })

    # 检测6: MECE违反
    if not is_mece(causal_tree):
        failures.append({
            "failure_mode": "mece_violation",
            "recovery": rebuild_causal_tree_mece(causal_tree)
        })

    # 检测7: 过度归因
    for effect_node in causal_tree.convergence_nodes:
        total_attribution = sum(n.effect_size for n in effect_node.causes)
        if total_attribution > 1.0:
            failures.append({
                "failure_mode": "over_attribution",
                "node": effect_node,
                "recovery": redistribute_attribution(effect_node)
            })

    return failures
```

---

© 阿洋