# 趋势预测 — 从历史轨迹到多情景推演的动态分析

> **模块标识**: `knowledge/thinking-templates/trend-forecast`
> **设计依据**: 基于全域深度认知框架三层推理架构设计——趋势预测遵循"驱动因子识别→信号扫描→情景构建→稳健策略设计"四步递进逻辑
> **依赖**: `knowledge/research-methods`、`knowledge/cognitive-framework`
> **骨架类型**: 趋势预测 (Trend Forecast)
>
> **版本治理元数据 (D12.4.2)**:
> - version: 1.1
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（驱动因子→信号扫描→情景构建→稳健策略四步递进）
>   - v1.1 补全版本治理元数据与交叉引用（D12.4.2-D12.4.3）

## 交叉引用

- **上游**: `knowledge/research-methods.md`、`knowledge/cognitive-framework.md`
- **下游**: `tasks/T09_cog_reason.md`（认知推理，应用趋势预测模板）、`tasks/TM04_scenario_landscape.md`（情景景观，深化趋势预测）
- **相关**: `knowledge/thinking-templates/system-dynamics.md`（系统动力学模板）、`knowledge/thinking-models/decision/scenario-simulator.md`（情景模拟器）、`knowledge/thinking-models/domain-specific/tech-disruption-model.md`（技术颠覆模型）、`knowledge/thinking-models/routing-table.md`（思维模型路由表）

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
- `knowledge/thinking-models/decision/scenario-simulator.md`（情景模拟器 — 多情景构建的方法论基础）
- `knowledge/thinking-models/domain-specific/tech-disruption-model.md`（技术颠覆模型 — 技术趋势预测的专用框架）
- `knowledge/thinking-templates/system-dynamics.md`（系统动力学模板 — 趋势驱动力的系统建模基础）

**边界声明**：本模板提供五步趋势预测的执行流程（步骤1-5的伪代码），不重复阐述情景模拟器的决策理论或技术颠覆模型的创新扩散理论。当需要理论依据时，调用上述模型文件。

---

## 1. 定义

趋势预测是一种基于历史轨迹识别、驱动力量化分析和转折点信号监测，构建多情景未来图景的系统化推理方法。它拒绝线性外推的简单预测，要求分析者识别趋势背后的驱动力组合、可能的转折点、以及不同驱动力组合下的多情景分叉。趋势预测的输出是"可能性空间的地图"，而非单一的预测点。

**核心法则**: 好的趋势预测不告诉你"会发生什么"，而是告诉你"在什么条件下会发生什么，以及你现在应该监测什么信号来判断哪种情景正在成为现实。"

---

## 2. 核心概念

| 概念 | 定义 | 分析要点 |
|------|------|----------|
| **历史趋势** | 过去有明确方向性的变化模式 | 区分真正的趋势与随机波动 |
| **驱动力** | 推动趋势产生、维持或改变的根本力量 | 按作用力大小排序，区分主导驱动力与次要驱动力 |
| **惯性因子** | 维持当前趋势不变的系统性力量 | 识别路径依赖、沉没成本、制度锁定 |
| **变革因子** | 推动趋势方向或速率改变的破坏性力量 | 识别技术突破、政策转向、社会运动 |
| **转折点** | 趋势方向或速率发生质变的临界点 | 区分渐变转折与突变转折 |
| **弱信号** | 尚未被广泛认知但可能预示重大变化的早期迹象 | 从边缘信息中识别，区分噪声与信号 |
| **情景** | 在特定驱动力组合下的未来可能状态 | 情景之间必须有质的差异，而非同一路径的参数微调 |
| **概率评估** | 各情景发生的相对可能性 | 使用定性概率刻度：极可能/很可能/可能/不太可能/极不可能 |

---

## 3. 五步趋势预测流程

```
步骤1: 历史趋势识别
  ├─ 定义趋势变量: 什么在变化？（量化，含时间单位）
  ├─ 回溯时间窗口: 选取有意义的回溯期（至少覆盖一个完整周期）
  ├─ 趋势特征提取: 方向、速率、加速度、波动性
  ├─ 周期性检验: 是否存在可识别的周期模式？
  ├─ 趋势分解: 长期趋势、周期性波动、随机波动
  └─ 结构断点检测: 历史上是否发生过趋势的结构性变化？
        │
步骤2: 驱动力分解
  ├─ 识别所有驱动因素: 推动趋势的各类力量
  ├─ 驱动力分类:
  │    ├─ 持久性驱动力: 长期存在、变化缓慢的深层力量（如人口结构、气候变化）
  │    ├─ 中期驱动力: 5-10年尺度上的制度/技术/社会力量
  │    └─ 短期驱动力: 1-3年尺度上的政策/市场/事件力量
  ├─ 驱动力交互分析:
  │    ├─ 协同效应: 两个驱动力叠加效果 > 各自效果之和
  │    ├─ 拮抗效应: 两个驱动力方向相反，部分抵消
  │    └─ 触发效应: 驱动力A达到阈值后激活驱动力B
  └─ 驱动力不确定性评估: 每个驱动力的变化范围与不可预测程度
        │
步骤3: 转折点信号扫描
  ├─ 识别潜在的转折点类型:
  │    ├─ 阈值转折: 累积量跨越临界值引发质变
  │    ├─ 触媒转折: 某个事件触发系统状态突变
  │    ├─ 替代转折: 新力量替代旧力量成为主导驱动
  │    └─ 范式转折: 底层假设/规则被颠覆
  ├─ 弱信号监测清单: 哪些早期迹象值得持续关注？
  ├─ 信号强度评估: 每个弱信号的可信度（证据支持度）
  └─ 转折点前置条件: 每个转折点发生的必要条件是什么？
        │
步骤4: 多情景构建
  ├─ 情景轴选择: 选择2-3个最不确定且影响最大的驱动力作为情景轴
  ├─ 情景组合: 每个情景轴取2-3个可能状态，生成情景矩阵
  ├─ 情景筛选: 从矩阵中选择3-5个最有代表性的情景
  │    ├─ 基线情景: 当前趋势的惯性延续
  │    ├─ 乐观情景: 有利驱动力占主导
  │    ├─ 悲观情景: 不利驱动力占主导
  │    ├─ 突变情景: 转折点被触发的极端情况
  │    └─ 黑天鹅情景: 当前未预见的极端事件
  ├─ 每个情景的内容:
  │    ├─ 时间线: 关键事件序列
  │    ├─ 因果链: 驱动力如何导致该情景
  │    ├─ 关键假设: 使该情景成立的前提条件
  │    └─ 可观测信号: 该情景成为现实的早期迹象
  └─ 情景一致性检验: 情景内部是否逻辑自洽？
        │
步骤5: 概率评估
  ├─ 情景可能性排序: 相对概率（非绝对概率值）
  ├─ 概率锚定: 基于哪些依据做出概率判断？
  ├─ 关键不确定性: 哪些未知因素对概率判断影响最大？
  ├─ 稳健策略识别: 在多个情景中均有正面效果的策略
  └─ 监测建议: 应在未来关注哪些关键指标以判断情景走向？
```

### 3.1 可执行伪代码（D6.4.3）

```python
def trend_forecast(trend_variable, historical_window):
    """
    趋势预测模板 - 可执行伪代码（D6.4.3）
    输入: trend_variable(趋势变量), historical_window(回溯时间范围)
    输出: trend_forecast YAML（见 §6 输出模板）
    """
    # ===== 步骤1: 历史趋势识别 =====
    trend_def = {
        "variable": trend_variable,
        "historical_window": historical_window,
        "baseline_trajectory": None,  # 方向、速率、加速度
        "structural_breaks": []
    }
    historical_data = collect_historical_data(trend_variable, historical_window)
    trend_def["baseline_trajectory"] = extract_trend_features(historical_data)
    # 趋势分解: 长期趋势 + 周期性波动 + 随机波动
    decomposition = decompose_trend(historical_data)
    # 结构断点检测
    trend_def["structural_breaks"] = detect_structural_breaks(historical_data)

    # ===== 步骤2: 驱动力分解 =====
    driving_forces = {
        "persistent": [],   # 持久性驱动力（10-30年）
        "medium_term": [],  # 中期驱动力（5-10年）
        "short_term": [],   # 短期驱动力（1-3年）
        "interactions": []
    }
    all_forces = identify_driving_forces(trend_variable)
    for force in all_forces:
        steep_category = classify_steep(force)  # S/T/E/E/P
        impact = score_impact(force)  # 1-5
        certainty = score_certainty(force)  # 1-5
        time_scale = determine_time_scale(force)
        force_entry = {
            "force": force,
            "steep_category": steep_category,
            "impact": impact,
            "certainty": certainty,
            "trajectory": assess_force_trajectory(force)
        }
        if time_scale == "persistent":
            driving_forces["persistent"].append(force_entry)
        elif time_scale == "medium_term":
            driving_forces["medium_term"].append(force_entry)
        else:
            driving_forces["short_term"].append(force_entry)
    # 驱动力交互分析: 协同(synergy)/拮抗(antagonism)/触发(trigger)
    driving_forces["interactions"] = analyze_interactions(all_forces)

    # ===== 步骤3: 转折点信号扫描 =====
    tipping_points = []
    for tp_type in ["threshold", "catalyst", "substitution", "paradigm"]:
        candidates = identify_tipping_points(tp_type, driving_forces, trend_def)
        for tp in candidates:
            tipping_points.append({
                "id": f"TP-{len(tipping_points)+1:03d}",
                "type": tp_type,
                "description": tp.description,
                "preconditions": tp.preconditions,  # 必要条件
                "early_signals": scan_weak_signals(tp),  # 弱信号
                "signal_strength": assess_signal_strength(tp)  # strong|moderate|weak
            })

    # [v3] BifurcationKit 分岔分析（TC-097）
    if bifurcationkit_available and has_ode_model(driving_forces):
        bif_results = bifurcationkit_analyze(
            driving_forces,
            control_parameter=select_control_parameter(driving_forces)
        )
        for bp in bif_results.bifurcation_points:
            tipping_points.append({
                "id": f"TP-BIF-{len(tipping_points)+1:03d}",
                "type": "threshold",
                "description": f"{bp.bifurcation_type} 分岔点",
                "preconditions": [f"控制参数达到 {bp.parameter_value}"],
                "early_signals": [f"行为变化: {bp.behavior_before} → {bp.behavior_after}"],
                "signal_strength": "strong"
            })

    # ===== 步骤4: 多情景构建 =====
    # 选择2-3个最不确定且影响最大的驱动力作为情景轴
    scenario_axes = select_scenario_axes(driving_forces)  # 高影响+低确定性
    scenario_matrix = generate_scenario_matrix(scenario_axes)
    scenarios = []
    for i, combo in enumerate(select_representative_scenarios(scenario_matrix, n=5)):
        scenario = {
            "id": f"SCN-{i+1:03d}",
            "name": name_scenario(combo),
            "type": classify_scenario_type(combo),  # baseline|optimistic|pessimistic|disruptive|wildcard
            "key_assumptions": extract_assumptions(combo),
            "timeline": build_timeline(combo),  # 近期/中期/远期
            "causal_narrative": build_causal_narrative(combo, driving_forces),
            "observables": identify_observables(combo)  # 可观测信号
        }
        # 情景一致性检验
        assert is_internally_consistent(scenario), f"情景 {scenario['id']} 内部逻辑不自洽"
        scenarios.append(scenario)

    # ===== 步骤5: 概率评估 =====
    probability_assessment = {
        "ranking": [],  # 相对概率排序（非绝对值）
        "key_uncertainties": [],
        "robust_strategies": [],
        "monitoring_plan": {}
    }
    # 情景可能性排序
    ranked = rank_scenarios_by_probability(scenarios, driving_forces, tipping_points)
    for scenario, likelihood, rationale in ranked:
        probability_assessment["ranking"].append({
            "scenario": scenario["id"],
            "relative_likelihood": likelihood,  # most_likely|likely|possible|less_likely|least_likely
            "rationale": rationale
        })
    probability_assessment["key_uncertainties"] = identify_key_uncertainties(driving_forces, tipping_points)
    # 稳健策略: 在多个情景中均有正面效果的策略
    probability_assessment["robust_strategies"] = identify_robust_strategies(scenarios)
    probability_assessment["monitoring_plan"] = {
        "key_indicators": identify_monitoring_indicators(tipping_points, scenarios),
        "trigger_conditions": define_trigger_conditions(tipping_points),
        "review_frequency": recommend_review_frequency(driving_forces)
    }

    # ===== 输出 =====
    return {
        "trend_definition": trend_def,
        "driving_forces": driving_forces,
        "tipping_points": tipping_points,
        "scenarios": scenarios,
        "probability_assessment": probability_assessment
    }
```

---

## 4. 驱动力分析框架

### 4.1 STEEP 分类法

| 类别 | 子分类 | 典型驱动力 | 时间尺度 |
|------|--------|-----------|---------|
| **S**ocial | 人口、教育、价值观、生活方式 | 老龄化、城市化、消费升级 | 10-30年 |
| **T**echnological | 研发、扩散、替代、融合 | AI、基因编辑、能源技术 | 3-20年 |
| **E**conomic | 增长、分配、贸易、金融 | 全球化/逆全球化、利率周期 | 1-10年 |
| **E**nvironmental | 气候、资源、生态、灾害 | 碳中和、水资源压力 | 10-50年 |
| **P**olitical | 治理、地缘、法律、制度 | 监管变革、多极化、民主衰退 | 1-20年 |

### 4.2 驱动力权重矩阵

每个驱动力按两个维度评分（1-5分）：

```
                    确定性高 (→已知)
                      │
    影响大 ───────────┼─────────── 影响小
                      │
                    确定性低 (→未知)
```

- **高影响 + 高确定性**: 直接纳入所有情景的基础假设
- **高影响 + 低确定性**: 作为情景轴的候选驱动力
- **低影响 + 高确定性**: 作为背景条件
- **低影响 + 低确定性**: 低优先级，可忽略

---

## 5. 常见陷阱

1. **线性外推**: 将过去趋势简单延长到未来，忽略饱和、逆转和相变的可能。**纠正**: 对每个趋势追问"这个趋势在什么条件下会减速、停止或逆转？"
2. **近因权重过度**: 过度强调最近发生的事件对未来的影响。**纠正**: 拉长时间窗口，比较不同时期的趋势强度。
3. **单一情景思维**: 只构建一种或两种情景，缺乏对可能性空间的充分探索。**纠正**: 强制构建至少3个情景，包括一个"最不可能但你不敢完全排除"的情景。
4. **确定性错觉**: 将"可能"误说为"必将"，将"趋势"混淆为"命运"。**纠正**: 每个预测必须附带"这取决于..."的条件声明。
5. **弱信号忽略**: 只关注已被广泛讨论的趋势，忽略边缘和异质声音。**纠正**: 主动寻找来自边缘的信息源，专门扫描"大多数人不相信但正在发生的事情"。
6. **驱动力遗漏**: 忽略了跨领域的、看似不相关但实际上关键的驱动力。**纠正**: 使用STEEP框架强制扫描所有五个维度。

---

## 6. 输出模板

```yaml
trend_forecast:
  trend_definition:
    variable: "预测的趋势变量"
    historical_window: "回溯时间范围"
    baseline_trajectory: "历史趋势的量化描述（方向、速率、加速度）"
    structural_breaks: ["历史断点及触发因素"]

  driving_forces:
    persistent:
      - force: "持久性驱动力"
        steep_category: "S|T|E|E|P"
        impact: "1-5"
        certainty: "1-5"
        trajectory: "该驱动力的自身演化趋势"
    medium_term: [{同上}]
    short_term: [{同上}]
    interactions:
      - forces: ["驱动力A", "驱动力B"]
        interaction_type: "synergy|antagonism|trigger"
        effect: "交互效应的描述"

  tipping_points:
    - id: "TP-001"
      type: "threshold|catalyst|substitution|paradigm"
      description: "转折点描述"
      preconditions: ["必要条件"]
      early_signals: ["弱信号"]
      signal_strength: "strong|moderate|weak"

  scenarios:
    - id: "SCN-001"
      name: "情景名称"
      type: "baseline|optimistic|pessimistic|disruptive|wildcard"
      key_assumptions: ["核心假设"]
      timeline:
        - phase: "近期 (0-2年)"
          events: ["关键事件"]
        - phase: "中期 (2-5年)"
          events: ["关键事件"]
        - phase: "远期 (5-10年)"
          events: ["关键事件"]
      causal_narrative: "驱动力如何导致该情景的因果叙事"
      observables: ["判断该情景正在发生的可观测信号"]

  probability_assessment:
    ranking:
      - scenario: "SCN-001"
        relative_likelihood: "most_likely|likely|possible|less_likely|least_likely"
        rationale: "概率判断依据"
    key_uncertainties: ["对概率判断影响最大的未知因素"]
    robust_strategies: ["在多个情景中均有效的应对策略"]

  monitoring_plan:
    key_indicators: ["应持续追踪的关键指标"]
    trigger_conditions: ["应采取行动的指标阈值"]
    review_frequency: "建议的重新评估频率"
```

---

## 7. 快速调用指南

当问题包含以下特征时，优先使用本骨架：
- 问题形式为"X 的未来会怎样？"
- 涉及长期（>3年）的战略决策，需要对未来做判断
- 环境中存在多个方向相反且高度不确定的驱动力
- 需要为不同的未来可能性做准备（而非押注单一预测）
- 需要在"趋势消失/逆转"的假设下做压力测试

---
## 8. 外部能力卡片引用（v3 新增）

### 8.1 BifurcationKit.jl 分岔分析引擎

> **能力卡**: TC-097 BifurcationKit

**方法论原理**：分岔分析是动力系统行为突变检测的核心工具。BifurcationKit通过数值延拓方法追踪平衡点/周期轨道随参数变化的路径，识别分岔点（鞍结分岔/Hopf分岔/倍周期分岔），预测系统行为质变。

在趋势预测的"转折点信号扫描"阶段（步骤三），当系统变量可连续化建模时，调用 BifurcationKit.jl 进行严格的分岔分析：

```yaml
bifurcationkit_integration:
  trigger: "存在微分方程模型或连续化状态变量，需识别临界点"
  workflow:
    - step: "将趋势系统的驱动力关系编码为微分方程（ODE）或映射（map）"
    - step: "选择分岔参数（控制参数）：选择对系统行为影响最大且可观测的参数"
    - step: "执行延拓（Continuation）：追踪平衡点和周期轨随参数变化的路径"
    - step: "检测分岔点类型：Fold（鞍结）/ Hopf / Pitchfork / Transcritical / Period-Doubling"
    - step: "绘制分岔图（Bifurcation Diagram）：横轴=控制参数，纵轴=状态变量"
    - step: "输出临界点列表：参数阈值、分岔类型、分岔前后的系统行为变化"
  bifurcation_types:
    fold: "Fold/Saddle-Node 分岔 — 平衡点出现/消失，系统状态突变（如金融市场崩盘）"
    hopf: "Hopf 分岔 — 平衡点失稳产生周期振荡（如商业周期从稳态转入波动）"
    pitchfork: "Pitchfork 分岔 — 对称破缺，系统从单一态分裂为多态（如社会共识分裂）"
    transcritical: "Transcritical 分岔 — 两个平衡点交换稳定性（如技术替代：旧技术→新技术）"
    period_doubling: "倍周期分岔 — 周期翻倍，混沌前兆（如供应链牛鞭效应加剧）"
  exhaust-retry: "无法建立微分方程模型时，穷尽重试为定性转折点分析（识别转折类型但不计算精确阈值），标注 bifurcation='qualitative'"
```

**输出规范**：
```yaml
bifurcation_output:
  bifurcation_available: bool
  control_parameter: str
  bifurcation_points:
    - parameter_value: float
      bifurcation_type: "fold|hopf|pitchfork|transcritical|period_doubling"
      behavior_before: str
      behavior_after: str
  bifurcation_diagram: str|null
  critical_thresholds:
    - parameter: str
      threshold: float
      warning_level: "safe|warning|critical"
  degradation_note: str|null
```

### 8.2 能力卡调用声明

| 能力卡 | 调用位置 | 触发条件 | 穷尽重试策略 |
|--------|---------|---------|---------|
| TC-097 BifurcationKit | 步骤三：转折点信号扫描 | 可建立ODE模型 + 连续化变量 | 穷尽重试为定性转折分析，标注 bifurcation='qualitative' |

---

## 9. 失败模式闭环清单（D6.4.4）

> 本节提供「失败模式 → 检测信号 → 恢复策略」三列结构，配套检测伪代码，确保趋势预测的常见失败模式可被自动识别与修复。

| 失败模式 | 检测信号 | 恢复策略 |
|---------|---------|---------|
| **线性外推** | `baseline_trajectory` 仅含线性趋势，无饱和/逆转/相变检验 | 对每个趋势追问"在什么条件下会减速、停止或逆转？"，调用 `detect_structural_breaks()` 检验非线性 |
| **近因权重过度** | `historical_window` 过短（<1个完整周期）或仅参考最近3年数据 | 拉长时间窗口，比较不同时期的趋势强度，至少覆盖一个完整周期 |
| **单一情景思维** | `scenarios` 列表长度 < 3，或所有情景类型相同（如全部为 baseline） | 强制构建至少3个情景，包括一个"最不可能但你不敢完全排除"的 wildcard 情景 |
| **确定性错觉** | `probability_assessment.ranking` 中存在 `relative_likelihood=most_likely` 但无 `rationale` | 每个预测必须附带"这取决于..."的条件声明，强制提供概率锚定依据 |
| **弱信号忽略** | `tipping_points[].early_signals` 为空，或所有信号 `signal_strength=weak` 但未标注 | 主动寻找来自边缘的信息源，专门扫描"大多数人不相信但正在发生的事情" |
| **驱动力遗漏** | `driving_forces` 中 STEEP 五大类任一类别为空 | 使用 STEEP 框架强制扫描所有五个维度（Social/Technological/Economic/Environmental/Political） |
| **情景同质化** | `scenarios` 中各情景的 `key_assumptions` 高度重叠，无质的差异 | 强制要求情景之间必须有质的差异，而非同一路径的参数微调 |
| **转折点类型混淆** | `tipping_points[].type` 标注与实际机制不符（如将渐变过程标注为 catalyst） | 验证转折点类型：threshold=累积量跨越临界值，catalyst=事件触发突变，substitution=新力量替代旧力量，paradigm=底层假设颠覆 |
| **概率排序无依据** | `probability_assessment.ranking` 中 `rationale` 为空或仅写"专家判断" | 强制提供概率锚定依据：基于哪些历史数据、驱动力分析、转折点信号做出判断 |
| **监测计划缺失** | `probability_assessment.monitoring_plan` 为空或 `key_indicators` 为空 | 强制识别应持续追踪的关键指标，定义触发行动的阈值，建议重新评估频率 |

### 9.1 失败模式检测伪代码

```python
def detect_and_recover_trend_forecast_failures(analysis_result):
    """
    趋势预测失败模式检测与恢复（D6.4.4）
    输入: analysis_result（trend_forecast YAML 输出）
    输出: failure_report + recovered_analysis
    """
    failures = []

    # FM-01: 线性外推
    trajectory = analysis_result["trend_definition"]["baseline_trajectory"]
    if is_purely_linear(trajectory) and not has_nonlinear_checks(analysis_result):
        failures.append({
            "mode": "linear_extrapolation",
            "signal": "baseline_trajectory 仅含线性趋势，无饱和/逆转检验",
            "recovery": "追问'在什么条件下会减速/停止/逆转？'，调用 detect_structural_breaks()"
        })

    # FM-02: 近因权重过度
    window = analysis_result["trend_definition"]["historical_window"]
    if is_short_window(window) or not covers_full_cycle(window):
        failures.append({
            "mode": "recency_bias",
            "signal": f"historical_window={window} 过短或未覆盖完整周期",
            "recovery": "拉长时间窗口，至少覆盖一个完整周期"
        })

    # FM-03: 单一情景思维
    scenarios = analysis_result["scenarios"]
    if len(scenarios) < 3 or len(set(s["type"] for s in scenarios)) < 2:
        failures.append({
            "mode": "single_scenario",
            "signal": f"情景数量={len(scenarios)}（<3）或类型单一",
            "recovery": "强制构建至少3个情景，包括一个 wildcard 情景"
        })

    # FM-04: 确定性错觉
    ranking = analysis_result["probability_assessment"]["ranking"]
    for r in ranking:
        if r["relative_likelihood"] == "most_likely" and not r.get("rationale"):
            failures.append({
                "mode": "certainty_illusion",
                "signal": f"情景 {r['scenario']} 标注为 most_likely 但无 rationale",
                "recovery": "每个预测必须附带'这取决于...'的条件声明"
            })

    # FM-05: 弱信号忽略
    tipping_points = analysis_result["tipping_points"]
    for tp in tipping_points:
        if not tp.get("early_signals"):
            failures.append({
                "mode": "weak_signal_ignored",
                "signal": f"转折点 {tp['id']} 无弱信号标注",
                "recovery": "主动寻找边缘信息源，扫描'大多数人不相信但正在发生的事'"
            })

    # FM-06: 驱动力遗漏
    driving_forces = analysis_result["driving_forces"]
    all_forces = driving_forces["persistent"] + driving_forces["medium_term"] + driving_forces["short_term"]
    steep_categories = set(f["steep_category"] for f in all_forces)
    required_steep = {"S", "T", "E", "P"}  # STEEP 五大类（E 出现两次但集合去重）
    if not required_steep.issubset(steep_categories):
        missing = required_steep - steep_categories
        failures.append({
            "mode": "force_omitted",
            "signal": f"STEEP 类别缺失: {missing}",
            "recovery": "使用 STEEP 框架强制扫描所有五个维度"
        })

    # FM-07: 情景同质化
    assumptions_sets = [frozenset(s["key_assumptions"]) for s in scenarios]
    for i, j in combinations(range(len(assumptions_sets)), 2):
        overlap = assumptions_sets[i] & assumptions_sets[j]
        min_len = min(len(assumptions_sets[i]), len(assumptions_sets[j]))
        if min_len > 0 and len(overlap) > 0.7 * min_len:
            failures.append({
                "mode": "scenario_homogeneity",
                "signal": f"情景 {scenarios[i]['id']} 和 {scenarios[j]['id']} 假设高度重叠",
                "recovery": "强制要求情景之间有质的差异，而非参数微调"
            })

    # FM-08: 转折点类型混淆
    valid_types = {"threshold", "catalyst", "substitution", "paradigm"}
    for tp in tipping_points:
        if tp["type"] not in valid_types:
            failures.append({
                "mode": "tipping_type_confused",
                "signal": f"转折点 {tp['id']} 类型={tp['type']} 不在标准定义中",
                "recovery": f"使用标准类型: {valid_types}"
            })

    # FM-09: 概率排序无依据
    for r in ranking:
        if not r.get("rationale") or r["rationale"] == "专家判断":
            failures.append({
                "mode": "ranking_without_basis",
                "signal": f"情景 {r['scenario']} 概率排序无依据",
                "recovery": "强制提供概率锚定依据：历史数据/驱动力分析/转折点信号"
            })

    # FM-10: 监测计划缺失
    monitoring = analysis_result["probability_assessment"].get("monitoring_plan", {})
    if not monitoring or not monitoring.get("key_indicators"):
        failures.append({
            "mode": "monitoring_missing",
            "signal": "monitoring_plan 为空或 key_indicators 为空",
            "recovery": "强制识别监测指标，定义触发阈值，建议评估频率"
        })

    return {
        "failure_count": len(failures),
        "failures": failures,
        "recovery_actions": [f["recovery"] for f in failures]
    }
```

---
© 阿洋