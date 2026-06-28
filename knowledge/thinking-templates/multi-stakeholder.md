# 多利益相关方分析 — 从单一主体到多方博弈格局的结构化洞察

> **模块标识**: `knowledge/thinking-templates/multi-stakeholder`
> **设计依据**: 基于全域深度认知框架三层推理架构设计——多利益相关方分析遵循"角色识别→利益映射→权力评估→博弈推演"四步递进逻辑
> **依赖**: `knowledge/research-methods`、`knowledge/cognitive-framework`、`knowledge/thinking-models/general/dialectical-analysis`
> **骨架类型**: 多利益相关方分析 (Multi-Stakeholder Analysis)
>
> **版本治理元数据 (D12.4.2)**:
> - version: 1.1
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（角色识别→利益映射→权力评估→博弈推演）
>   - v1.1 补全版本治理元数据与交叉引用（D12.4.2-D12.4.3）

## 交叉引用

- **上游**: `knowledge/research-methods.md`、`knowledge/cognitive-framework.md`、`knowledge/thinking-models/general/dialectical-analysis.md`
- **下游**: `tasks/T09_cog_reason.md`（认知推理，应用多利益相关方模板）、`tasks/T15_domain_analysis.md`（领域分析）
- **相关**: `knowledge/thinking-models/decision/game-theory.md`（博弈论）、`knowledge/thinking-models/decision/decision-matrix.md`（决策矩阵）、`knowledge/thinking-templates/dialectical-synthesis.md`（辩证综合模板）、`knowledge/thinking-models/routing-table.md`（思维模型路由表）

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
- `knowledge/thinking-models/decision/game-theory.md`（博弈论 — 纳什均衡、联盟分析的理论基础）
- `knowledge/thinking-models/decision/decision-matrix.md`（决策矩阵 — 权力-利益矩阵的形式化基础）

**边界声明**：本模板提供五步多利益相关方分析的执行流程（映射→矩阵→立场→博弈→策略的伪代码），不重复阐述博弈论的纳什均衡数学证明或决策矩阵的公理化体系。当需要理论依据时，调用上述模型文件。

---

## 1. 定义

多利益相关方分析是一种将复杂问题置于多方利益主体的博弈格局中审视的系统化推理方法。它拒绝从单一主体视角（通常为分析者自身或客户）审视问题，而是要求分析者映射出所有受问题影响或能影响问题走向的主体，理解其各自的立场、利益、权力和策略空间，识别博弈的均衡状态和潜在的冲突/合作区域。

**核心法则**: 不理解利益相关方的游戏规则，你的任何政策建议都只是纸上谈兵。

---

## 2. 核心概念

| 概念 | 定义 | 分析要点 |
|------|------|----------|
| **利益相关方** | 受问题影响或能影响问题走向的任何个体/组织/群体 | 区分核心方、次要方和外围方 |
| **权力** | 影响决策或结果的能力 | 正式权力（制度授予）vs 非正式权力（影响力/资源/信息） |
| **利益** | 主体在问题中的得失关切 | 区分声称利益与真实利益——声称利益可能是策略性的 |
| **立场** | 主体对问题的公开态度或主张 | 立场可能随时间、情境和策略变化 |
| **动机** | 驱动主体行为的深层原因 | 超越"理性自利"假设——考虑声誉、身份、情感 |
| **策略空间** | 主体可以选择的行动集合 | 每个行动的成本、收益和不确定性 |
| **博弈类型** | 主体间互动的结构性特征 | 零和/正和/负和、合作/非合作、静态/动态 |
| **纳什均衡** | 每个主体在给定他人选择下都无法单方面改善的状态 | 均衡不一定是"好的"，只是"稳定的" |
| **权力-利益矩阵** | 以权力和利益为轴，定位各类利益相关方的分析工具 | 高权力+高利益→关键玩家；高权力+低利益→保持满意；低权力+高利益→保持知情；低权力+低利益→最小关注 |

---

## 3. 五步多利益相关方分析流程

```
步骤1: 利益相关方映射
  ├─ 头脑风暴: 列出所有与问题相关的个体/组织/群体
  ├─ 分类:
  │    ├─ 直接受影响方: 问题的直接受益者/受害者
  │    ├─ 间接受影响方: 通过二阶效应受影响的主体
  │    ├─ 影响者: 虽不受直接影响但能改变问题走向的主体
  │    └─ 观察者: 目前中立但可能介入的主体
  ├─ 筛选: 合并高度同质的主体，排除边际相关的主体
  └─ 角色定义: 每个主体在问题中的核心角色
        │
步骤2: 权力-利益矩阵
  ├─ 权力评估（1-5分）:
  │    ├─ 决策权: 能否直接影响结果？
  │    ├─ 资源控制: 控制哪些关键资源？
  │    ├─ 信息优势: 掌握哪些不对称信息？
  │    └─ 动员能力: 能否组织集体行动？
  ├─ 利益评估（1-5分）:
  │    ├─ 损益规模: 问题解决与否对该方的影响程度
  │    ├─ 紧迫性: 影响的即时性
  │    └─ 不可逆性: 影响的不可逆程度
  └─ 四象限定位:
  │     高权力+高利益 → 关键玩家 (Key Players): 必须深度参与
  │     高权力+低利益 → 保持满意 (Keep Satisfied): 最低限度满足
  │     低权力+高利益 → 保持知情 (Keep Informed): 信息共享
  │     低权力+低利益 → 最小关注 (Minimal Effort): 可忽略
        │
步骤3: 立场与动机分析
  ├─ 对每个关键方分析:
  │    ├─ 公开立场: 该方如何表述自己的诉求？
  │    ├─ 真实利益: 该方真正关心的得失是什么？
  │    ├─ 底线: 该方不可退让的最低要求是什么？
  │    ├─ 抱负: 该方最优情况下的最高要求是什么？
  │    ├─ 可交换项: 该方可以在哪些议题上妥协？
  │    └─ 动机层级:
  │         L1 物质利益: 资源、金钱、安全
  │         L2 制度利益: 权力、地位、自主权
  │         L3 身份利益: 认同、尊严、归属
  │         L4 价值利益: 信念、意识形态、使命感
  └─ 立场冲突地图: 哪些组合存在根本性冲突？
        │
步骤4: 博弈格局构建
  ├─ 博弈类型判定:
  │    ├─ 合作博弈 vs 非合作博弈: 是否存在有约束力的协议？
  │    ├─ 零和 vs 正和 vs 负和: 总收益的加总性质
  │    ├─ 一次性 vs 重复博弈: 主体之间是否长期互动？
  │    └─ 完全信息 vs 不完全信息: 各方是否了解他人偏好？
  ├─ 策略空间定义: 每个关键方可选的行动方案
  ├─ 收益矩阵: 各策略组合下各方的预期收益
  ├─ 均衡预测: 纳什均衡点在哪？
  │    └─ 纯策略均衡 vs 混合策略均衡
  └─ 联盟分析: 哪些主体之间可能形成联盟？
        │
步骤5: 均衡/冲突预测与策略建议
  ├─ 均衡状态: 如果不干预，博弈将收敛于何种均衡？
  │    ├─ 效率: 该均衡是帕累托最优的吗？（无人受损下无法改善他人）
  │    └─ 公平: 该均衡的分配是否可接受？
  ├─ 冲突预测:
  │    ├─ 结构性冲突: 利益不可调和的碰撞点
  │    ├─ 信息性冲突: 因信息不对称导致的误解性冲突
  │    ├─ 关系性冲突: 因历史/情感/信任导致的对抗
  │    └─ 价值性冲突: 因深层价值观差异的不可调和
  ├─ 干预策略:
  │    ├─ 规则改变: 修改博弈规则以改变均衡
  │    ├─ 信息干预: 增减信息对称性以改变策略
  │    ├─ 利益重塑: 引入新的利益维度以创造正和空间
  │    └─ 联盟工程: 培育新的联盟以改变力量对比
  └─ 可行性评估: 每个干预的建议可行性
```

### 3.1 可执行伪代码（D6.4.3）

```python
def multi_stakeholder_analysis(problem_context, decision_scope):
    """
    多利益相关方分析模板 - 可执行伪代码（D6.4.3）
    输入: problem_context(问题描述), decision_scope(决策范围和可选项)
    输出: multi_stakeholder_analysis YAML（见 §6 输出模板）
    """
    analyst_disclaimer = declare_analyst_position(problem_context)  # 分析者立场声明

    # ===== 步骤1: 利益相关方映射 =====
    all_stakeholders = brainstorm_stakeholders(problem_context)  # 头脑风暴
    stakeholders = []
    for stk in all_stakeholders:
        category = classify_stakeholder(stk, problem_context)
        # direct_affected | indirect_affected | influencer | observer
        if category != "marginal":  # 排除边际相关的主体
            stakeholders.append({
                "id": f"STK-{len(stakeholders)+1:03d}",
                "name": stk.name,
                "category": category,
                "role": define_role(stk, problem_context)
            })

    # ===== 步骤2: 权力-利益矩阵 =====
    for stk in stakeholders:
        # 权力评估（1-5分）
        stk["power"] = {
            "decision_power": score_1_to_5(stk, "decision_power"),
            "resource_control": score_1_to_5(stk, "resource_control"),
            "information_advantage": score_1_to_5(stk, "information_advantage"),
            "mobilization_capacity": score_1_to_5(stk, "mobilization_capacity"),
            "power_total": avg_power(stk),
            "power_basis": identify_power_basis(stk)  # 正式/非正式
        }
        # 利益评估（1-5分）
        stk["interest"] = {
            "stake_size": score_1_to_5(stk, "stake_size"),
            "urgency": score_1_to_5(stk, "urgency"),
            "irreversibility": score_1_to_5(stk, "irreversibility"),
            "interest_total": avg_interest(stk)
        }
        # 四象限定位
        stk["quadrant"] = classify_quadrant(stk["power"]["power_total"], stk["interest"]["interest_total"])
        # key_player | keep_satisfied | keep_informed | minimal_effort

    # ===== 步骤3: 立场与动机分析 =====
    key_players = [s for s in stakeholders if s["quadrant"] == "key_player"]
    for stk in key_players:
        stk["position"] = {
            "stated_position": identify_stated_position(stk),  # 公开立场
            "real_interests": identify_real_interests(stk),    # 真实利益
            "bottom_line": identify_bottom_line(stk),          # 不可退让的底线
            "aspiration": identify_aspiration(stk),            # 最优诉求
            "tradeables": identify_tradeables(stk)             # 可妥协/交换的议题
        }
        stk["motivation_hierarchy"] = {
            "L1_material": identify_material_interest(stk),     # 物质利益
            "L2_institutional": identify_institutional_interest(stk),  # 制度利益
            "L3_identity": identify_identity_interest(stk),     # 身份利益
            "L4_value": identify_value_interest(stk)            # 价值利益
        }

    # 立场冲突地图
    conflict_map = []
    for s1, s2 in combinations(key_players, 2):
        conflict = analyze_conflict(s1, s2)
        if conflict:
            conflict_map.append({
                "parties": [s1["id"], s2["id"]],
                "conflict_type": conflict.type,  # structural|informational|relational|value
                "conflict_nature": conflict.nature,
                "reconcilability": conflict.reconcilability  # high|medium|low|none
            })

    # ===== 步骤4: 博弈格局构建 =====
    game_structure = {
        "game_type": {
            "cooperative": assess_cooperative(key_players),
            "zero_sum_level": assess_zero_sum(conflict_map),
            "repetition": assess_repetition(key_players),
            "information": assess_information_completeness(key_players)
        },
        "strategy_space": define_strategy_space(key_players, decision_scope),
        "payoff_matrix": build_payoff_matrix(key_players, decision_scope),
        "nash_equilibria": find_nash_equilibria(payoff_matrix),
        "coalition_analysis": analyze_coalitions(key_players)
    }

    # ===== 步骤5: 均衡/冲突预测与策略建议 =====
    predictions = {
        "without_intervention": {
            "equilibrium": predict_equilibrium(game_structure),
            "efficiency": assess_pareto_optimality(game_structure),
            "fairness": assess_fairness(game_structure)
        },
        "conflict_zones": identify_conflict_zones(conflict_map),
        "cooperation_potential": identify_cooperation_space(key_players, game_structure)
    }

    strategic_recommendations = []
    for intervention in design_interventions(predictions, game_structure):
        strategic_recommendations.append({
            "target": intervention.target,
            "intervention_type": intervention.type,  # rule_change|information|interest_reshaping|coalition
            "description": intervention.description,
            "expected_effect": intervention.expected_effect,
            "resistance": assess_resistance(intervention),
            "feasibility": assess_feasibility(intervention)  # high|medium|low
        })

    return {
        "problem_context": {"issue": problem_context, "decision_scope": decision_scope,
                           "analyst_disclaimer": analyst_disclaimer},
        "stakeholder_map": stakeholders,
        "conflict_map": conflict_map,
        "game_structure": game_structure,
        "predictions": predictions,
        "strategic_recommendations": strategic_recommendations,
        "uncertainty_declaration": declare_uncertainties(stakeholders, game_structure)
    }
```

---

## 4. 利益相关方参与策略（基于权力-利益矩阵）

| 象限 | 策略 | 具体行动 |
|------|------|----------|
| **关键玩家** (高权力+高利益) | 深度合作 | 纳入决策核心圈、一对一磋商、建立正式合作机制 |
| **保持满意** (高权力+低利益) | 被动满足 | 最低限度满足其核心关切、避免激怒、建立预警机制 |
| **保持知情** (低权力+高利益) | 信息透明 | 定期通报、征求意见（非决策权）、能力建设支持 |
| **最小关注** (低权力+低利益) | 低度干预 | 仅通过公开渠道通报、不投入专项资源 |

---

## 5. 常见陷阱

1. **利益相关方遗漏**: 忽视了沉默的、弱势的、或尚未组织化的群体。**纠正**: 强制追问"谁的得失没有被计入？谁没有发言权？"
2. **动机扁平化**: 将所有主体动机简化为"理性自利"的经济人。**纠正**: 对每个关键方进行L1-L4动机层级分析，至少覆盖到L3。
3. **静态分析**: 假设立场和权力固定不变。**纠正**: 分析权力对比的变化趋势——谁在上升、谁在下降？引入时间维度。
4. **过度对称**: 假设各方掌握相同信息、有相同的分析能力。**纠正**: 显式标注各方的信息不对称和认知能力差异。
5. **博弈类型误判**: 将实际是正和博弈的情况误判为零和，导致错过合作机会。**纠正**: 在判定零和之前，强制寻找至少一个正和的可能性。
6. **分析者立场渗透**: 分析者自身的价值观和利益偏好渗透到"中立分析"中。**纠正**: 分析者应声明自身在问题中的潜在立场或利益冲突。

---

## 6. 输出模板

```yaml
multi_stakeholder_analysis:
  problem_context:
    issue: "问题描述"
    decision_scope: "决策的范围和可选项"
    analyst_disclaimer: "分析者在该问题中的潜在立场声明"

  stakeholder_map:
    - id: "STK-001"
      name: "利益相关方名称"
      category: "direct_affected|indirect_affected|influencer|observer"
      power:
        decision_power: "1-5"
        resource_control: "1-5"
        information_advantage: "1-5"
        mobilization_capacity: "1-5"
        power_total: "1-5"
        power_basis: "权力的来源（正式/非正式）"
      interest:
        stake_size: "1-5"
        urgency: "1-5"
        irreversibility: "1-5"
        interest_total: "1-5"
      quadrant: "key_player|keep_satisfied|keep_informed|minimal_effort"
      position:
        stated_position: "公开立场"
        real_interests: "真实利益"
        bottom_line: "不可退让的底线"
        aspiration: "最优诉求"
        tradeables: ["可妥协/交换的议题"]
      motivation_hierarchy:
        L1_material: "物质利益"
        L2_institutional: "制度利益"
        L3_identity: "身份利益"
        L4_value: "价值利益"

  conflict_map:
    - parties: ["STK-001", "STK-002"]
      conflict_type: "structural|informational|relational|value"
      conflict_nature: "冲突的本质描述"
      reconcilability: "high|medium|low|none"

  game_structure:
    game_type:
      cooperative: "true|false"
      zero_sum_level: "完全零和|混合|完全正和"
      repetition: "一次性|有限重复|无限重复"
      information: "完全信息|不完全信息"
    strategy_space:
      - player: "STK-001"
        options: ["可选行动方案"]
    payoff_matrix:
      strategy_combination: ["(A的战略1, B的战略2)"]
      payoffs:
        STK-001: "收益"
        STK-002: "收益"
    nash_equilibria: ["均衡预测"]
    coalition_analysis: "可能的联盟及稳定性"

  predictions:
    without_intervention:
      equilibrium: "不干预情况下的预期均衡"
      efficiency: "帕累托最优？"
      fairness: "分配公平性评估"
    conflict_zones: ["可能爆发冲突的区域"]
    cooperation_potential: ["可开发的合作空间"]

  strategic_recommendations:
    - target: "干预目标"
      intervention_type: "rule_change|information_intervention|interest_reshaping|coalition_engineering"
      description: "干预策略描述"
      expected_effect: "干预的预期效果"
      resistance: "可能遭遇的抵制"
      feasibility: "high|medium|low"

  uncertainty_declaration:
    hidden_stakeholders: "可能遗漏的利益相关方"
    information_asymmetry: "信息不对称对分析的潜在影响"
    preference_stability: "各方偏好的稳定性评估"
```

---

## 7. 快速调用指南

当问题包含以下特征时，优先使用本骨架：
- 问题涉及多个群体/组织/国家的利益冲突或协调
- 决策影响方超过2个且有策略性互动
- 问题中存在明显的权力不对称
- 需要在冲突情境中寻找合作空间
- 需要评估政策/决策在不同利益方中的可接受性

---

## 8. 失败模式闭环清单（D6.4.4）

> 本节为多利益相关方分析模板的「失败模式 → 检测信号 → 恢复策略」闭环清单。当检测到失败模式时，必须执行对应的恢复策略。

| 失败模式 | 检测信号 | 恢复策略 |
|---------|---------|---------|
| **利益相关方遗漏** | 忽视了沉默的、弱势的、或尚未组织化的群体 | 强制追问"谁的得失没有被计入？谁没有发言权？"；补充遗漏的利益相关方 |
| **动机扁平化** | 将所有主体动机简化为"理性自利"的经济人假设 | 对每个关键方进行L1-L4动机层级分析，至少覆盖到L3（身份利益） |
| **静态分析** | 假设立场和权力固定不变，忽略权力对比的变化趋势 | 引入时间维度：分析权力对比的变化趋势——谁在上升、谁在下降？标注动态趋势 |
| **过度对称** | 假设各方掌握相同信息、有相同的分析能力 | 显式标注各方的信息不对称和认知能力差异；在博弈分析中考虑不完全信息 |
| **博弈类型误判** | 将实际是正和博弈的情况误判为零和，导致错过合作机会 | 在判定零和之前，强制寻找至少一个正和的可能性；检验是否存在未被发现的正和空间 |
| **分析者立场渗透** | 分析者自身的价值观和利益偏好渗透到"中立分析"中 | 分析者应声明自身在问题中的潜在立场或利益冲突；将个人偏好标注为 alternative_frameworks |
| **声称利益与真实利益混淆** | 将利益相关方的公开声明（可能是策略性的）等同于真实利益 | 区分 stated_position 与 real_interests：对每个关键方追问"它真正关心的是什么？" |
| **纳什均衡误判** | 错误识别博弈的均衡点，或忽略了混合策略均衡 | 严格求解纳什均衡：检验纯策略均衡和混合策略均衡；标注均衡的稳定性条件 |
| **干预可行性高估** | 提出的干预策略在政治/经济/社会维度不可行 | 每条干预策略必须过四维可行性检查：政治/经济/技术/社会；任一维度不可行需标注 |
| **联盟稳定性误判** | 假设联盟是稳定的，忽略了联盟内部的利益张力 | 评估联盟的稳定性：联盟成员之间的利益一致性如何？标注联盟的潜在裂痕 |

### 8.1 失败模式检测与恢复的执行伪代码

```python
def detect_and_recover_stakeholder_failures(stakeholders, conflict_map, game_structure, recommendations):
    """
    多利益相关方分析失败模式检测与恢复（D6.4.4）
    """
    failures = []

    # 检测1: 利益相关方遗漏
    silent_groups = identify_silent_groups(stakeholders)
    if silent_groups:
        failures.append({
            "failure_mode": "stakeholder_omission",
            "missing_groups": silent_groups,
            "recovery": add_missing_stakeholders(stakeholders, silent_groups)
        })

    # 检测2: 动机扁平化
    for stk in stakeholders:
        if stk.get("quadrant") == "key_player":
            motivation = stk.get("motivation_hierarchy", {})
            if not motivation.get("L3_identity") and not motivation.get("L4_value"):
                failures.append({
                    "failure_mode": "flattened_motivation",
                    "stakeholder": stk["id"],
                    "recovery": deepen_motivation_analysis(stk, target_level="L3")
                })

    # 检测3: 静态分析
    if not any(s.get("power_trend") for s in stakeholders):
        failures.append({
            "failure_mode": "static_analysis",
            "recovery": add_temporal_dimension(stakeholders)
        })

    # 检测4: 过度对称
    info_levels = {s["id"]: s.get("information_level") for s in stakeholders}
    if len(set(info_levels.values())) == 1:
        failures.append({
            "failure_mode": "excessive_symmetry",
            "recovery": differentiate_information_asymmetry(stakeholders)
        })

    # 检测5: 博弈类型误判
    if game_structure["game_type"]["zero_sum_level"] == "完全零和":
        positive_sum_space = search_positive_sum_space(stakeholders, game_structure)
        if positive_sum_space:
            failures.append({
                "failure_mode": "game_type_misjudgment",
                "recovery": reclassify_game_type(game_structure, "混合")
            })

    # 检测6: 分析者立场渗透
    if not recommendations[0].get("analyst_disclaimer"):
        failures.append({
            "failure_mode": "analyst_bias_penetration",
            "recovery": declare_analyst_position(problem_context)
        })

    # 检测7: 声称利益与真实利益混淆
    for stk in stakeholders:
        if stk.get("quadrant") == "key_player":
            position = stk.get("position", {})
            if position.get("stated_position") and not position.get("real_interests"):
                failures.append({
                    "failure_mode": "stated_vs_real_confusion",
                    "stakeholder": stk["id"],
                    "recovery": identify_real_interests(stk)
                })

    # 检测8: 纳什均衡误判
    equilibria = game_structure.get("nash_equilibria", [])
    if not equilibria or not validate_equilibria(equilibria, game_structure["payoff_matrix"]):
        failures.append({
            "failure_mode": "equilibrium_misidentification",
            "recovery": recalculate_equilibria(game_structure, check_mixed=True)
        })

    # 检测9: 干预可行性高估
    for rec in recommendations:
        feasibility = rec.get("feasibility")
        if feasibility == "high" and not all_dimensions_checked(rec):
            failures.append({
                "failure_mode": "overestimated_feasibility",
                "recommendation": rec,
                "recovery": run_four_dimensional_feasibility_check(rec)
            })

    # 检测10: 联盟稳定性误判
    for coalition in game_structure.get("coalition_analysis", []):
        if coalition.get("stability") == "high":
            internal_tension = check_internal_tension(coalition)
            if internal_tension:
                failures.append({
                    "failure_mode": "coalition_stability_overestimate",
                    "coalition": coalition,
                    "recovery": reassess_coalition_stability(coalition, internal_tension)
                })

    return failures
```

---

© 阿洋