# 系统动力学分析 — 从线性因果到非线性反馈的结构洞察

> **模块标识**: `knowledge/thinking-templates/system-dynamics`
> **设计依据**: 基于全域深度认知框架三层推理架构设计——系统动力学分析遵循"反馈环路识别→延迟与非线性效应→杠杆点定位→政策抵抗预判"四步递进逻辑
> **依赖**: `knowledge/research-methods`、`knowledge/cognitive-framework`、`knowledge/thinking-models/general/systems-thinking`
> **骨架类型**: 系统动力学分析 (System Dynamics Analysis)
>
> **版本治理元数据 (D12.4.2)**:
> - version: 1.1
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（反馈环路→延迟→杠杆点→政策抵抗四步递进）
>   - v1.1 补全版本治理元数据与交叉引用（D12.4.2-D12.4.3）

## 交叉引用

- **上游**: `knowledge/research-methods.md`、`knowledge/cognitive-framework.md`、`knowledge/thinking-models/general/systems-thinking.md`
- **下游**: `tasks/TM01_system_dynamics.md`（系统动力学节点，深化系统动力学模板）、`tasks/T22_nrsf_synthesize.md`（系统基模匹配）
- **相关**: `knowledge/thinking-templates/causal-chain.md`（因果链模板）、`knowledge/thinking-templates/trend-forecast.md`（趋势预测模板）、`knowledge/penrose-templates.md`（Penrose 因果回路图模板）、`knowledge/thinking-models/routing-table.md`（思维模型路由表）

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
- `knowledge/thinking-models/general/systems-thinking.md`（系统思维 — 系统动力学分析的理论基础）
- `knowledge/thinking-templates/causal-chain.md`（因果链模板 — 系统动力学反馈回路的因果基础）
- `knowledge/thinking-templates/trend-forecast.md`（趋势预测模板 — 系统动力学的时间演化延伸）

**边界声明**：本模板提供六步系统动力学分析的执行流程（步骤1-6的伪代码），不重复阐述系统思维的哲学基础或因果链的因果推断理论。当需要理论依据时，调用上述模型文件。

---

## 1. 定义

系统动力学分析是一种将研究对象视为由相互作用、反馈循环和非线性关系构成的动态系统的推理方法。它超越线性因果链，关注系统的内部结构如何产生行为模式，包括延迟效应、存量-流量动态、正负反馈循环的相互作用、系统抗性（policy resistance）和涌现行为。分析的目标是识别高杠杆干预点，而非对孤立要素的参数调优。

**核心法则**: 系统行为不由其最优部件决定，而由其最薄弱的反馈环节决定。你不能通过优化部件来优化系统。

---

## 2. 核心概念

| 概念 | 定义 | 分析标记 |
|------|------|----------|
| **系统边界** | 区分"系统内"与"系统外"的划分 | 边界选择决定分析视角——声明纳入和排除的要素 |
| **存量** | 系统的累积状态变量（系统的"记忆"） | 存量产生惯性，存量变化需要时间 |
| **流量** | 改变存量的流入和流出速率 | 流量的变化取决于存量水平和其他变量 |
| **正反馈** | 放大变化的自我强化循环（R） | 增长引擎或恶性循环——系统远离平衡 |
| **负反馈** | 抑制变化的自我修正循环（B） | 稳定器或目标寻求——系统趋向平衡 |
| **延迟** | 因果之间的时间滞后 | 延迟破坏直觉——长延迟 + 强正反馈 = 超调振荡 |
| **非线性** | 因果关系的非比例性 | 阈值、饱和、边际递减、相变——线性外推失效 |
| **涌现** | 系统整体表现出部分不具备的属性 | 在局部层面无法预测 |
| **杠杆点** | 小变化产生大系统影响的干预点 | 按Meadows 12级排序——参数调优效果最弱 |
| **系统抗性** | 系统抵制外部干预的内在倾向 | 负反馈回路自动抵消干预效果 |
| **路径依赖** | 历史选择约束未来可能空间 | 早期选择产生锁定效应，增量变化难以逆转 |
| **非意图后果** | 干预引发的超出预期的系统反应 | 干预绕过负反馈→短期改善→长期恶化 |

---

## 3. 六步系统动力学分析流程

```
步骤1: 系统边界定义
  ├─ 系统命名与目的: 该系统存在的功能或目标是什么？
  ├─ 时间范围: 分析的起点和终点
  ├─ 纳入的要素: 系统内的核心变量
  ├─ 排除的要素: 系统外但对系统有影响的环境因素
  └─ 边界声明: 排除的要素如果被纳入，可能如何改变分析结论？
        │
步骤2: 要素识别
  ├─ 核心存量: 哪些是可累积的系统状态变量？
  │    └─ 对每个存量: 它的流入和流出是什么？
  ├─ 关键变量: 哪些变量影响流量速率？
  ├─ 外部变量: 哪些是系统无法控制的外生输入？
  └─ 参数: 哪些是相对固定的常量？
        │
步骤3: 反馈回路构建
  ├─ 绘制因果回路图 (Causal Loop Diagram, CLD):
  │    └─ 节点 = 变量，箭头 = 因果关系，+/- = 同向/反向关系
  ├─ 识别反馈回路:
  │    ├─ 正反馈回路 (R): 偶数的"-"号 → 自我强化
  │    └─ 负反馈回路 (B): 奇数的"-"号 → 自我修正/目标寻求
  ├─ 标注延迟: 每条因果链上的时间滞后（单位）
  ├─ 标注非线性: 阈值、饱和点、边际变化点
  └─ 识别主导回路: 在系统当前状态下，哪个反馈起主导作用？
        │
步骤4: 杠杆点分析
  ├─ 按 Meadows 12级杠杆点排序系统内的可干预点:
  │     12. 参数与数值         ─ 最弱
  │     11. 缓冲规模
  │     10. 存量-流量结构
  │      9. 延迟长度
  │      8. 负反馈强度
  │      7. 正反馈增益
  │      6. 信息流结构
  │      5. 系统规则
  │      4. 自组织能力
  │      3. 系统目标
  │      2. 心智模型/范式
  │      1. 超越范式            ─ 最强
  ├─ 识别高杠杆点: 位于层级 4-7 的最有效且可达的干预点
  └─ 为何更高层级的杠杆点难以触及？
        │
步骤5: 干预策略设计
  ├─ 干预点选择: 基于可行性、预期效果和时间延迟
  ├─ 干预方式: 直接改变变量 vs 改变反馈结构 vs 改变系统目标
  ├─ 时间路径推演: 干预后系统在短/中/长期的预期行为
  │    └─ "更糟之前更好"（Worse-Before-Better）vs "更好之后更糟"（Better-Before-Worse）
  └─ 组合策略: 多个干预点的协同设计
        │
步骤6: 非意图后果分析
  ├─ 二阶效应: 干预的第一轮间接后果
  ├─ 三阶效应: 二阶效应的再影响
  ├─ 系统抗性检测: 系统存在哪些会抵消干预的负反馈？
  ├─ 边界外溢: 干预是否会影响系统外的变量？
  └─ 情景压力测试: 干预在不同初始条件下的效果
```

### 3.1 可执行伪代码（D6.4.3）

```python
def system_dynamics_analysis(system_name, purpose, time_horizon):
    """
    系统动力学分析模板 - 可执行伪代码（D6.4.3）
    输入: system_name(系统名称), purpose(系统目的), time_horizon(时间范围)
    输出: system_dynamics_analysis YAML（见 §6 输出模板）
    """
    # ===== 步骤1: 系统边界定义 =====
    boundary = {
        "name": system_name,
        "purpose": purpose,
        "time_horizon": time_horizon,
        "included": [],  # 系统内的核心变量
        "excluded": [],  # 系统外但影响系统的环境因素
        "boundary_impact_statement": None  # 排除要素被纳入时的影响
    }
    boundary["included"] = identify_core_variables(system_name)
    boundary["excluded"] = identify_exogenous_factors(system_name)
    boundary["boundary_impact_statement"] = assess_boundary_impact(boundary)

    # ===== 步骤2: 要素识别 =====
    elements = {
        "core_stocks": [],  # 可累积的系统状态变量
        "key_variables": [],  # 影响流量速率的变量
        "exogenous": boundary["excluded"],  # 外生输入
        "parameters": []  # 相对固定的常量
    }
    for stock_candidate in identify_stocks(boundary["included"]):
        stock = {
            "name": stock_candidate,
            "inflows": identify_inflows(stock_candidate),
            "outflows": identify_outflows(stock_candidate),
            "initial_value": get_initial_value(stock_candidate)
        }
        elements["core_stocks"].append(stock)
    elements["key_variables"] = identify_rate_variables(elements["core_stocks"])
    elements["parameters"] = identify_constants(boundary["included"])

    # ===== 步骤3: 反馈回路构建 =====
    cld = build_causal_loop_diagram(elements)  # 节点=变量，箭头=因果，+/-同向/反向
    loops = []
    for loop in identify_loops(cld):
        loop_type = "R" if count_negative_links(loop) % 2 == 0 else "B"  # R=正反馈，B=负反馈
        loops.append({
            "id": f"LOOP-{len(loops)+1:03d}",
            "type": loop_type,
            "name": name_loop(loop),
            "chain": trace_loop_chain(loop),
            "delays": annotate_delays(loop),  # 每条因果链的时间滞后
            "nonlinearities": annotate_nonlinearities(loop),  # 阈值/饱和/边际变化
            "dominance_condition": assess_dominance(loop, elements),
            "archetype": match_archetype(loop)  # 增长极限/转移负担/公地悲剧等
        })
    dominant_loop = identify_dominant_loop(loops, current_state=elements)

    # ===== 步骤4: 杠杆点分析 =====
    leverage_points = []
    for point in identify_intervention_points(cld, elements):
        meadows_level = classify_meadows_level(point)  # 1-12 级（12最弱，1最强）
        leverage_points.append({
            "meadows_level": meadows_level,
            "name": point.name,
            "current_state": assess_current_state(point),
            "potential_change": assess_potential_change(point),
            "feasibility": assess_feasibility(point),  # high|medium|low
            "expected_impact": estimate_impact(point),
            "time_to_effect": estimate_delay(point),
            "resistance_detection": predict_resistance(point, loops)
        })
    # 高杠杆点：层级 4-7 的最有效且可达的干预点
    high_leverage = [lp for lp in leverage_points if 4 <= lp["meadows_level"] <= 7]

    # ===== 步骤5: 干预策略设计 =====
    intervention_strategy = {
        "primary_intervention": select_primary_intervention(high_leverage),
        "intervention_mode": None,  # direct_change | feedback_restructure | goal_change
        "time_path": {},  # short/medium/long_term 预期行为
        "combined_strategy": None
    }
    intervention_strategy["intervention_mode"] = determine_intervention_mode(
        intervention_strategy["primary_intervention"]
    )
    # 时间路径推演："更糟之前更好"(Worse-Before-Better) vs "更好之后更糟"(Better-Before-Worse)
    intervention_strategy["time_path"] = {
        "short_term": simulate_short_term(intervention_strategy, elements),
        "medium_term": simulate_medium_term(intervention_strategy, elements, loops),
        "long_term": simulate_long_term(intervention_strategy, elements, loops, dominant_loop)
    }
    intervention_strategy["combined_strategy"] = design_combined_strategy(high_leverage)

    # ===== 步骤6: 非意图后果分析 =====
    unintended = {
        "second_order": [],  # 二阶效应
        "third_order": [],   # 三阶效应
        "system_resistance": [],  # 系统抗性检测
        "boundary_spillover": None,  # 边界外溢
        "scenario_stress_test": None  # 情景压力测试
    }
    unintended["second_order"] = analyze_second_order_effects(
        intervention_strategy, loops
    )
    unintended["third_order"] = analyze_third_order_effects(
        unintended["second_order"], loops
    )
    # 系统抗性检测：哪些负反馈会抵消干预？
    unintended["system_resistance"] = [
        loop for loop in loops
        if loop["type"] == "B" and will_counter_intervention(loop, intervention_strategy)
    ]
    unintended["boundary_spillover"] = assess_boundary_spillover(
        intervention_strategy, boundary
    )
    unintended["scenario_stress_test"] = stress_test_under_conditions(
        intervention_strategy, elements, boundary
    )

    # ===== 输出 =====
    return {
        "system_definition": boundary,
        "elements": elements,
        "causal_loop_diagram": {"loops": loops, "dominant_loop": dominant_loop},
        "leverage_points": leverage_points,
        "intervention_strategy": intervention_strategy,
        "unintended_consequences": unintended,
        "uncertainty_declaration": declare_uncertainties(elements, loops, cld)
    }
```

---

## 4. 因果回路图的符号规范

```
变量A ────(+)──→ 变量B   : A增加 → B增加（同向）
变量A ────(-)──→ 变量B   : A增加 → B减少（反向）

反馈回路标记:
  R: 正反馈（Reinforcing）— 环内有偶数个(-)
  B: 负反馈（Balancing）  — 环内有奇数个(-)

延迟标记:
变量A ──(+)──∥──→ 变量B  : A到B的因果传导有显著延迟

存量标记:
存量 [Population] ──→ 流量箭头 : 存量影响流量速率
```

### 4.1 经典系统基模

| 基模 | 结构 | 典型行为 | 干预方向 |
|------|------|---------|---------|
| **增长极限** | 增长引擎(R) + 抑制负反馈(B) | S形增长后停滞 | 解除抑制约束，而非继续推动增长 |
| **转移负担** | 症状缓解(B1) + 根本方案(B2)，B1削弱B2 | 对症状方案成瘾，根本问题恶化 | 识别并切断症状缓解对根本方案的削弱 |
| **公地悲剧** | 多个主体独立的增长回路(R)共享有限资源 | 资源耗尽 | 改变资源使用规则（层级5的干预） |
| **目标侵蚀** | 目标与实际差距驱动目标下调(B) | 标准持续降低 | 锁定目标，分离目标设定与差距评估 |
| **恶性竞争** | 两方正反馈(R)驱动对方更强反应 | 升级螺旋 | 打破反馈循环，单方面穷尽重试 |
| **成功者成功** | 两个增长回路，初期优势驱动资源倾斜(R) | "富者愈富" | 改变资源分配规则 |

---

## 5. 常见陷阱

1. **边界划得过窄**: 将关键的外部驱动力排除在系统外，导致分析遗漏重要的因果链。**纠正**: 强制追问"排除了什么？如果纳入分析，结论会有何不同？"
2. **反馈盲区**: 只看到单向因果（A→B），忽略反馈（B→A）。**纠正**: 对每对因果追问"B是否也影响A？"，画出完整的因果回路。
3. **延迟无视**: 假设因果是瞬间的，忽略时间滞后。**纠正**: 对每条因果链标注时间单位，并在推演中显式考虑延迟。
4. **线性世界**: 默认因果关系是线性的、成比例的。**纠正**: 对每个因果关系追问"当A增加一倍时，B也增加一倍吗？什么水平上该关系会变化？"
5. **杠杆点过高**: 识别了最优的杠杆点但它在现实中不可触及。**纠正**: 对每个杠杆点标注可干预性评估——现实可达 vs 理论最优。
6. **忽视系统抗性**: 设计了干预但未考虑系统会如何抵抗它。**纠正**: 对每个干预追问"系统有哪些机制会试图抵消这个干预？"

---

## 6. 输出模板

```yaml
system_dynamics_analysis:
  system_definition:
    name: "系统名称"
    purpose: "系统目的或核心功能"
    time_horizon: "分析的时间范围"
    boundary:
      included: ["系统内的核心要素"]
      excluded: ["排除的环境因素"]
      boundary_impact_statement: "如果纳入排除要素可能如何改变结论"

  elements:
    core_stocks:
      - name: "存量名称"
        unit: "度量单位"
        inflows: ["流入变量"]
        outflows: ["流出变量"]
        initial_value: "当前水平"
    key_variables: ["影响流量的关键变量"]
    exogenous: ["外生变量（系统不控制）"]

  causal_loop_diagram:
    loops:
      - id: "LOOP-001"
        type: "R|B"
        name: "回路名称"
        chain: ["A ─(+)→ B ─(-)→ C ─(+)→ A"]
        delays:
          - from: "A"
            to: "B"
            lag: "延迟时间与单位"
        dominance_condition: "该回路主导的条件"
        archetype: "增长极限|转移负担|公地悲剧|目标侵蚀|恶性竞争|成功者成功|none"

  leverage_points:
    - meadows_level: 6
      name: "杠杆点名称"
      current_state: "当前状态"
      potential_change: "可行的改变"
      feasibility: "high|medium|low"
      expected_impact: "干预的预期效果"
      time_to_effect: "从干预到效果的预期延迟"
      resistance_detection: "系统可能抵抗该干预的机制"

  intervention_strategy:
    primary_intervention:
      target: "主要干预点"
      mechanism: "干预机制的因果描述"
      time_path:
        short_term: "短期（<1年）预期行为"
        medium_term: "中期（1-3年）预期行为"
        long_term: "长期（>3年）预期行为"
    combined_strategy: "多点组合干预的协同设计"

  unintended_consequences:
    second_order:
      - effect: "二阶效应描述"
        likelihood: "high|medium|low"
        severity: "high|medium|low"
    third_order:
      - effect: "三阶效应描述"
        likelihood: "high|medium|low"
    boundary_spillover: "系统边界外的溢出效应"
    scenario_stress_test: "不同初始条件下干预效果的差异性评估"

  uncertainty_declaration:
    model_limitations: "模型的结构性局限"
    omitted_variables: "被忽略但又可能重要的变量"
    nonlinearity_unknowns: "未被完全建模的非线性关系"
```

---

## 7. 快速调用指南

当问题包含以下特征时，优先使用本骨架：
- 问题涉及多个因素间的循环因果关系
- 干预历史上反复失败（建议方案与问题原因互为因果）
- 存在明显的"越努力越糟糕"或"短期有效长期恶化"模式
- 问题涉及存量消耗、公共资源管理、增长极限
- 需要在系统层面设计干预策略，而非单点优化

---
## 8. 外部能力卡片引用（v3 新增）

### 8.1 PySD 系统动力学仿真引擎

> **能力卡**: TC-096 PySD

在系统动力学分析的"干预策略设计"阶段（步骤五），当因果回路图构建完成后，调用 PySD 将定性模型转化为可仿真的存量-流量模型：

```yaml
pysd_integration:
  trigger: "因果回路图包含 ≥ 3 个闭合回路，且至少有 2 个存量变量"
  workflow:
    - step: "将因果回路图（CLD）转化为存量-流量图（SFD）：识别存量/流量/辅助变量/常量"
    - step: "为每个流量编写速率方程（rate equation），基于存量水平和辅助变量"
    - step: "配置仿真参数：时间范围（start/end/delta）、积分方法（Euler/RK4）、时间步长"
    - step: "执行仿真：生成时间序列数据（各存量和流量随时间变化）"
    - step: "参数敏感性扫描：对关键参数（±20%）执行 Monte Carlo 扫描，识别高敏感参数"
    - step: "输出：仿真时间序列图 + 参数敏感性排序 + 临界参数阈值预警"
  compatibility:
    - "兼容 Vensim .mdl 模型文件（可直接加载已有系统动力学模型）"
    - "支持 XMILE 标准格式导入/导出"
    - "与 Mesa ABM（TC-055）互补：PySD 提供宏观系统动力学，Mesa 提供微观 Agent 行为"
  exhaust-retry: "无定量参数时，仅输出定性存量-流量图设计，标注 simulation_available=false"
```

**输出规范**：
```yaml
pysd_output:
  simulation_available: bool
  model_file: str|null
  time_series:
    - variable: str
      data: [{time: float, value: float}]
  sensitivity_analysis:
    - parameter: str
      range: [float, float]
      impact_score: float
  critical_thresholds:
    - parameter: str
      threshold_value: float
      behavior_change: str
  degradation_note: str|null
```

### 8.2 能力卡调用声明

| 能力卡 | 调用位置 | 触发条件 | 穷尽重试策略 |
|--------|---------|---------|---------|
| TC-096 PySD | 步骤五：干预策略设计 | 闭合回路 ≥ 3 且存量变量 ≥ 2 | 穷尽重试为定性存量-流量图，标注 sim='qualitative' |

---

## 9. 失败模式闭环清单（D6.4.4）

> 本节提供「失败模式 → 检测信号 → 恢复策略」三列结构，配套检测伪代码，确保系统动力学分析的常见失败模式可被自动识别与修复。

| 失败模式 | 检测信号 | 恢复策略 |
|---------|---------|---------|
| **边界划得过窄** | `boundary.excluded` 包含对系统有显著影响的外部驱动力，或 `boundary_impact_statement` 为空 | 强制追问"排除了什么？如果纳入分析，结论会有何不同？"，对每个排除要素评估边界影响 |
| **反馈盲区** | `causal_loop_diagram.loops` 中所有回路都是单向因果（A→B），无 B→A 反馈边 | 对每对因果追问"B 是否也影响 A？"，调用 `identify_loops()` 补全反馈回路 |
| **延迟无视** | `loops[].delays` 为空或所有延迟标注为 0 | 对每条因果链标注时间单位，在推演中显式考虑延迟，长延迟+强正反馈需标注超调振荡风险 |
| **线性世界假设** | `loops[].nonlinearities` 为空，但系统涉及存量消耗/饱和/阈值效应 | 对每个因果关系追问"当A增加一倍时，B也增加一倍吗？什么水平上该关系会变化？"，标注阈值/饱和/边际变化点 |
| **杠杆点过高** | `leverage_points` 中推荐的干预点 `feasibility=low` 但 `meadows_level` ≤ 3（理论最优但不可达） | 对每个杠杆点标注可干预性评估，优先推荐层级 4-7 的可行干预点，更高层级标注为"理论最优但现实不可达" |
| **忽视系统抗性** | `intervention_strategy` 未包含 `resistance_detection`，或抗性检测为空 | 对每个干预追问"系统有哪些机制会试图抵消这个干预？"，调用 `analyze_system_resistance()` 识别抵消回路 |
| **存量-流量混淆** | `elements.core_stocks` 中包含实际上是流量变量的项，或 `inflows/outflows` 标注错误 | 验证每个存量是否为累积状态变量（有初始值、有流入流出），流量变量移入 `key_variables` |
| **主导回路误判** | `dominant_loop` 标注与当前系统状态不符（如系统处于增长期但标注负反馈为主导） | 重新评估各回路在当前状态下的主导性，调用 `assess_dominance()` 基于存量水平和参数值判定 |
| **基型匹配错误** | `loops[].archetype` 标注与回路结构不符（如标注"增长极限"但无抑制负反馈） | 验证基型匹配：增长极限需 R+B，转移负担需 B1+B2 且 B1削弱B2，公地悲剧需多个独立R共享资源 |
| **非意图后果遗漏** | `unintended_consequences.second_order` 为空，或仅分析一阶效应 | 强制执行二阶/三阶效应分析，调用 `analyze_second_order_effects()` 和 `analyze_third_order_effects()` |

### 9.1 失败模式检测伪代码

```python
def detect_and_recover_system_dynamics_failures(analysis_result):
    """
    系统动力学分析失败模式检测与恢复（D6.4.4）
    输入: analysis_result（system_dynamics_analysis YAML 输出）
    输出: failure_report + recovered_analysis
    """
    failures = []

    # FM-01: 边界划得过窄
    boundary = analysis_result["system_definition"]["boundary"]
    if not boundary.get("boundary_impact_statement"):
        failures.append({
            "mode": "narrow_boundary",
            "signal": "boundary_impact_statement 为空",
            "recovery": "对每个排除要素评估边界影响，强制追问'如果纳入分析，结论会有何不同？'"
        })

    # FM-02: 反馈盲区
    loops = analysis_result["causal_loop_diagram"]["loops"]
    if not loops or all(not has_feedback_edge(loop) for loop in loops):
        failures.append({
            "mode": "feedback_blindness",
            "signal": "无反馈回路或所有回路都是单向因果",
            "recovery": "对每对因果追问'B是否也影响A？'，调用 identify_loops() 补全反馈回路"
        })

    # FM-03: 延迟无视
    for loop in loops:
        delays = loop.get("delays", [])
        if not delays or all(d.get("lag", 0) == 0 for d in delays):
            failures.append({
                "mode": "delay_ignored",
                "signal": f"回路 {loop['id']} 无延迟标注或所有延迟为0",
                "recovery": "对每条因果链标注时间单位，长延迟+强正反馈需标注超调振荡风险"
            })

    # FM-04: 线性世界假设
    for loop in loops:
        if not loop.get("nonlinearities"):
            failures.append({
                "mode": "linear_assumption",
                "signal": f"回路 {loop['id']} 无非线性标注",
                "recovery": "追问'当A增加一倍时B是否也增加一倍？'，标注阈值/饱和/边际变化点"
            })

    # FM-05: 杠杆点过高
    leverage_points = analysis_result["leverage_points"]
    for lp in leverage_points:
        if lp["meadows_level"] <= 3 and lp["feasibility"] == "low":
            failures.append({
                "mode": "leverage_too_high",
                "signal": f"杠杆点 {lp['name']} 层级={lp['meadows_level']} 但可行性=low",
                "recovery": "优先推荐层级4-7的可行干预点，更高层级标注为'理论最优但现实不可达'"
            })

    # FM-06: 忽视系统抗性
    strategy = analysis_result["intervention_strategy"]
    resistance = strategy.get("resistance_detection")
    if not resistance or (isinstance(resistance, list) and not resistance):
        failures.append({
            "mode": "resistance_ignored",
            "signal": "intervention_strategy 未包含系统抗性检测",
            "recovery": "对每个干预追问'系统有哪些机制会抵消这个干预？'，调用 analyze_system_resistance()"
        })

    # FM-07: 存量-流量混淆
    elements = analysis_result["elements"]
    for stock in elements.get("core_stocks", []):
        if "initial_value" not in stock or not stock.get("inflows") or not stock.get("outflows"):
            failures.append({
                "mode": "stock_flow_confusion",
                "signal": f"存量 {stock['name']} 缺少 initial_value/inflows/outflows",
                "recovery": "验证存量是否为累积状态变量，流量变量移入 key_variables"
            })

    # FM-08: 主导回路误判
    dominant = analysis_result["causal_loop_diagram"].get("dominant_loop")
    if dominant:
        system_state = infer_system_state(elements)
        if dominant["type"] == "B" and system_state == "growing":
            failures.append({
                "mode": "dominance_misjudged",
                "signal": f"系统处于增长期但主导回路标注为负反馈(B)",
                "recovery": "重新评估各回路主导性，调用 assess_dominance() 基于存量水平判定"
            })

    # FM-09: 基型匹配错误
    archetype_map = {
        "增长极限": {"requires": ["R", "B"]},
        "转移负担": {"requires": ["B1", "B2"]},
        "公地悲剧": {"requires": ["R", "R", "shared_resource"]},
        "目标侵蚀": {"requires": ["B"]},
        "恶性竞争": {"requires": ["R", "R"]},
        "成功者成功": {"requires": ["R", "R"]}
    }
    for loop in loops:
        archetype = loop.get("archetype")
        if archetype and archetype != "none":
            required = archetype_map.get(archetype, {}).get("requires", [])
            if not validate_archetype_structure(loop, required):
                failures.append({
                    "mode": "archetype_mismatch",
                    "signal": f"回路 {loop['id']} 标注基型={archetype} 但结构不符",
                    "recovery": f"验证基型匹配：{archetype} 需要 {required}"
                })

    # FM-10: 非意图后果遗漏
    unintended = analysis_result["unintended_consequences"]
    if not unintended.get("second_order"):
        failures.append({
            "mode": "unintended_omitted",
            "signal": "second_order 效应为空，仅分析一阶效应",
            "recovery": "强制执行二阶/三阶效应分析，调用 analyze_second_order_effects()"
        })

    return {
        "failure_count": len(failures),
        "failures": failures,
        "recovery_actions": [f["recovery"] for f in failures]
    }
```

---
© 阿洋