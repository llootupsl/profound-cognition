> **作者**: 阿洋

# 决策评估统一协议 (Decision Evaluation Protocol)

> > **状态**: 正式发布 (v2 适配)
> **适用范围**: Profound Cognition v2 — 所有决策评估模块必须实现此协议
> **最后更新**: 2026-05-15

---

## 1. 协议概述

### 1.1 目的

DecisionEvaluationProtocol 定义了决策评估模块的统一接口标准。在 Profound Cognition v2 中，决策评估模块作为 Sub-Agent 任务被主LLM调度执行。该协议确保所有决策分析过程遵循一致的方法论、评估维度和输出格式，为用户提供全面、客观、可操作的决策支持。

### 1.2 v2 多任务集成

在 v2 架构中，决策评估协议被以下任务引用：

| 任务 ID | 任务名称 | 引用方式 |
|---------|---------|---------|
| T05 | L6+L7 证据与利益相关者 | 证据等级体系 |
| T10 | 对抗逻辑 | 维度评分交叉验证 |
| T11 | 对抗证据 | 证据等级体系 |
| T13 | 认知综合 | 综合排名与建议 |

决策评估的方法论定义独立于调度框架，具体的执行上下文由主LLM通过 [handoff-protocol.md](./handoff-protocol.md) 中定义的 context_package 注入。

### 1.3 核心设计原则

- **多维平衡**: 通过五维评估框架确保决策分析的全面性
- **量化驱动**: 所有评估维度均采用可量化的评分体系
- **个性化适配**: 根据用户画像调整评估权重和呈现方式
- **场景模拟**: 支持多场景推演，降低决策不确定性
- **透明可追溯**: 评估过程和依据完全透明，支持回溯审查

### 1.4 协议在 v2 系统中的位置

```
┌──────────────────────────────────────────┐
│ v2 Phase 1 调度循环 (主LLM)              │
├──────────────────────────────────────────┤
│ T05 L6+L7 证据与利益相关者 (Sub-Agent)      │
│   └── 应用 evidence_level_validation     │
├──────────────────────────────────────────┤
│ T10 对抗逻辑 (Sub-Agent)                 │
│   └── 应用 simulate_scenarios()          │
├──────────────────────────────────────────┤
│ T11 对抗证据 (Sub-Agent)                 │
│   └── 应用 evidence_level_validation     │
├──────────────────────────────────────────┤
│ T13 认知综合 (Sub-Agent)                 │
│   └── 应用 generate_alternatives()       │
├──────────────────────────────────────────┤
│ 决策评估协议层 (Protocol)                │
│ DecisionEvaluationProtocol               │
├──────────────────────────────────────────┤
│ ┌──────────┐ ┌──────────┐ ┌────────┐   │
│ │ 五维评估 │ │ 场景模拟 │ │ 个性化 │   │
│ │ 引擎     │ │ 引擎     │ │ 适配器 │   │
│ └──────────┘ └──────────┘ └────────┘   │
├──────────────────────────────────────────┤
│ 领域分析协议层 (Domain)                  │
│ DomainAnalysisProtocol                   │
├──────────────────────────────────────────┤
│ 基础设施层 (Infrastructure)              │
└──────────────────────────────────────────┘
```

---

## 2. 核心方法定义

### 2.1 evaluate_dimensions(decision_context) -> DimensionScores

对决策选项进行五维评估，生成各维度的量化评分。

```yaml
method: evaluate_dimensions
version: "9"
description: |
 对决策上下文中的选项执行五维评估（利弊/风险/成本/价值观/长期影响），
 返回每个维度的详细评分和子类别分析。

parameters:
 decision_context:
   type: DecisionContext
   required: true
   fields:
     decision_description:
       type: string
       required: true
       min_length: 10
       max_length: 5000
       description: "决策场景描述"
     options:
       type: array
       required: true
       min_items: 2
       max_items: 10
       items:
         type: DecisionOption
         fields:
           id:
             type: string
             pattern: "^OPT-[a-f0-9]{6}$"
           name:
             type: string
             required: true
             max_length: 100
           description:
             type: string
             required: true
           pros:
             type: array
             items:
               type: string
             default: []
           cons:
             type: array
             items:
               type: string
             default: []
           estimated_cost:
             type: CostEstimate
             fields:
               monetary:
                 type: object
                 fields:
                   min:
                     type: number
                   max:
                     type: number
                   currency:
                     type: string
                     default: "CNY"
               time:
                 type: string
                 description: "时间成本描述"
               effort:
                 type: enum
                 values: [negligible, low, medium, high, extreme]
           probability_of_success:
             type: float
             min: 0.0
             max: 1.0
             default: null
           stakeholders:
             type: array
             items:
               type: Stakeholder
               fields:
                 name:
                   type: string
                 role:
                   type: string
                 influence:
                   type: enum
                   values: [low, medium, high, critical]
                 interest:
                   type: enum
                   values: [low, medium, high, critical]
     constraints:
       type: DecisionConstraints
       fields:
         budget_limit:
           type: number
           default: null
         time_limit:
           type: string
           default: null
         risk_tolerance:
           type: enum
           values: [very_low, low, moderate, high, very_high]
           default: "moderate"
         must_have:
           type: array
           items:
             type: string
           default: []
         must_not_have:
           type: array
           items:
             type: string
           default: []
     domain:
       type: string
       description: "关联的领域引擎标识"
     urgency:
       type: enum
       values: [immediate, soon, moderate, flexible, none]
       default: "moderate"

return_value:
  type: DimensionScores
  fields:
    evaluation_id:
      type: string
      pattern: "^EVAL-[A-Z]{3}-\\d{8}-[a-f0-9]{8}$"
    decision_summary:
      type: string
      max_length: 300
    options_evaluated:
      type: integer
      description: "参与评估的选项数量"

    # === 五维评估结果 ===
    dimensions:
      type: array
      items:
        type: DimensionEvaluation
        fields:
          dimension_id:
            type: string
          dimension_name:
            type: string
          weight:
            type: float
            min: 0.0
            max: 1.0
          option_scores:
            type: array
            items:
              type: OptionDimensionScore
              fields:
                option_id:
                  type: string
                raw_score:
                  type: float
                  min: 0.0
                  max: 100.0
                normalized_score:
                  type: float
                  min: 0.0
                  max: 1.0
                grade:
                  type: enum
                  values: [A_plus, A, B_plus, B, C_plus, C, D, F]
                sub_category_scores:
                  type: array
                  items:
                    type: SubCategoryScore
                    fields:
                      name:
                        type: string
                      score:
                        type: float
                      weight:
                        type: float
                      evidence:
                        type: string
                highlights:
                  type: array
                  items:
                    type: string
                concerns:
                  type: array
                  items:
                    type: string
          dimension_summary:
            type: string

    # === 综合评分 ===
    overall_ranking:
      type: array
      items:
        type: RankedOption
        fields:
          option_id:
            type: string
          option_name:
            type: string
          composite_score:
            type: float
            min: 0.0
            max: 100.0
          rank:
            type: integer
          recommendation:
            type: enum
            values: [strongly_recommended, recommended, neutral, not_recommended, strongly_not_recommended]
          key_strengths:
            type: array
            items:
              type: string
          key_weaknesses:
            type: array
            items:
              type: string

    metadata:
      type: EvaluationMetadata
      fields:
        evaluation_model:
          type: string
        execution_time_ms:
          type: integer
        protocol_version:
          type: string
          default: "9"

exceptions:
  - name: InsufficientOptionsError
    code: "DEP-E001"
    trigger: "选项数量少于2个"
    recovery: "提示用户至少提供2个选项进行比较"
  - name: IncomparableOptionsError
    code: "DEP-E002"
    trigger: "选项之间缺乏可比性（如完全不同的决策类型）"
    recovery: "尝试拆分为多个独立评估，或提示用户重新定义选项"
  - name: MissingContextError
    code: "DEP-E003"
    trigger: "决策上下文信息不足，无法进行有效评估"
    recovery: "返回缺失信息清单，引导用户补充"
  - name: ConstraintConflictError
    code: "DEP-E004"
    trigger: "约束条件之间存在矛盾（如低预算+高规格要求）"
    recovery: "识别矛盾点，建议放宽约束或调整期望"
```

### 2.2 simulate_scenarios(options) -> ScenarioProjections

对决策选项进行多场景模拟推演。

```yaml
method: simulate_scenarios
version: "9"
description: |
 对每个决策选项在多种可能场景下的表现进行模拟推演，
 生成概率化的结果预测和敏感性分析。

parameters:
  options:
    type: array
    required: true
    min_items: 2
    max_items: 10
    items:
      type: DecisionOption
      description: "待模拟的决策选项（同evaluate_dimensions中的定义）"

  simulation_config:
    type: SimulationConfig
    required: false
    default:
      scenarios: auto
      time_horizon: "P1Y"
      confidence_level: 0.8
    fields:
      scenarios:
        type: array
        items:
          type: ScenarioDefinition
          fields:
            name:
              type: string
            probability:
              type: float
              min: 0.0
              max: 1.0
            description:
              type: string
            key_variables:
              type: array
              items:
                type: VariableDefinition
                fields:
                  name:
                    type: string
                  base_value:
                    type: number
                  range:
                    type: array
                    items:
                      type: number
                    min_items: 2
                    max_items: 2
                  distribution:
                    type: enum
                    values: [normal, uniform, triangular, exponential]
                  impact_direction:
                    type: enum
                    values: [positive, negative, mixed]
        description: "自定义场景定义，auto表示自动生成"
      time_horizon:
        type: string
        pattern: "^P(\\d+Y)?(\\d+M)?(\\d+D)?$"
        default: "P1Y"
        description: "模拟时间范围（ISO 8601 Duration）"
      confidence_level:
        type: float
        min: 0.5
        max: 0.99
        default: 0.8
        description: "置信水平"
      sensitivity_variables:
        type: array
        items:
          type: string
        default: []
        description: "敏感性分析的目标变量"
      monte_carlo_runs:
        type: integer
        default: 1000
        min: 100
        max: 10000
        description: "蒙特卡洛模拟次数"

return_value:
  type: ScenarioProjections
  fields:
    simulation_id:
      type: string
      pattern: "^SIM-[A-Z]{3}-\\d{8}-[a-f0-9]{8}$"
    scenarios:
      type: array
      items:
        type: ScenarioProjection
        fields:
          scenario_name:
            type: string
          probability:
            type: float
          description:
            type: string
          option_outcomes:
            type: array
            items:
              type: OptionOutcome
              fields:
                option_id:
                  type: string
                projected_value:
                  type: float
                  description: "预测的综合价值"
                value_range:
                  type: object
                  fields:
                    low:
                      type: float
                    median:
                      type: float
                    high:
                      type: float
                confidence_interval:
                  type: object
                  fields:
                    lower:
                      type: float
                    upper:
                      type: float
                    level:
                      type: float
                key_risks:
                  type: array
                  items:
                    type: RiskFactor
                    fields:
                      name:
                        type: string
                      probability:
                        type: float
                      impact:
                        type: enum
                        values: [negligible, minor, moderate, major, catastrophic]
                      mitigation:
                        type: string
                key_opportunities:
                  type: array
                  items:
                    type: string
                timeline_milestones:
                  type: array
                  items:
                    type: Milestone
                    fields:
                      time_point:
                        type: string
                      event:
                        type: string
                      probability:
                        type: float

    sensitivity_analysis:
      type: SensitivityAnalysis
      fields:
        tornado_chart_data:
          type: array
          items:
            type: TornadoBar
            fields:
              variable:
                type: string
              low_impact:
                type: float
              base_impact:
                type: float
              high_impact:
                type: float
              direction:
                type: enum
                values: [positive, negative]
        most_sensitive_variables:
          type: array
          items:
            type: string
          description: "对结果影响最大的变量，按敏感度排序"
        robust_options:
          type: array
          items:
            type: string
          description: "在各场景下表现最稳健的选项"

    worst_case_analysis:
      type: WorstCaseAnalysis
      fields:
        scenario:
          type: string
        worst_option:
          type: string
        worst_outcome_description:
          type: string
        max_downside:
          type: float
        recovery_path:
          type: string

    best_case_analysis:
      type: BestCaseAnalysis
      fields:
        scenario:
          type: string
        best_option:
          type: string
        best_outcome_description:
          type: string
        max_upside:
          type: float

exceptions:
  - name: SimulationConvergenceError
    code: "DEP-E010"
    trigger: "蒙特卡洛模拟未收敛"
    recovery: "增加模拟次数后重试，不简化模型"
  - name: InsufficientDataError
    code: "DEP-E011"
    trigger: "场景模拟所需的基础数据不足"
    recovery: "标注数据不足，持续重试直至获取充足数据，不使用默认参数"
  - name: ScenarioInfeasibleError
    code: "DEP-E012"
    trigger: "定义的场景在逻辑上不可行"
    recovery: "标注不可行场景，继续模拟其余场景"

输出对接:
  target: "T20a 决策演化路线渲染契约"
  reference: "tasks/T20a_research_render.md §决策演化路线渲染契约"
  requirement: >
    simulate_scenarios 的输出必须满足 T20a 决策演化路线渲染契约的输入要求，
    具体包括：
  mandatory_fields:
    - field: "scenarios"
      description: "至少包含3个场景（基准/乐观/悲观），每个场景包含 option_outcomes、key_risks、key_opportunities、timeline_milestones"
      required_by: "T20a 每条路线六项要素（触发条件、关键变量值、概率区间、时间演化、敏感性Top-3、对冲策略）"
    - field: "sensitivity_analysis"
      description: "必须包含 tornado_chart_data 与 most_sensitive_variables（至少3个），供 T20a 消费为敏感性 Top-3"
      required_by: "T20a 敏感性 Top-3 要素"
    - field: "worst_case_analysis"
      description: "必须包含 worst_outcome_description 与 max_downside，供 T20a 悲观路线消费"
      required_by: "T20a 悲观路线时间演化"
    - field: "best_case_analysis"
      description: "必须包含 best_outcome_description 与 max_upside，供 T20a 乐观路线消费"
      required_by: "T20a 乐观路线时间演化"
    - field: "option_outcomes[*].value_range"
      description: "必须包含 low/median/high 三值，供 T20a 概率区间渲染"
      required_by: "T20a 概率区间渲染"
    - field: "option_outcomes[*].timeline_milestones"
      description: "必须包含至少3个时间节点（短期/中期/长期），供 T20a 时间演化三阶段消费"
      required_by: "T20a 时间演化三阶段"
  quality_gate: >
    若 simulate_scenarios 输出缺失上述任一 mandatory_field，T20a 渲染时应标注对应要素为
    [数据缺失] 并穷尽重试处理（参见 T20a 决策演化路线渲染契约消费规则）。
  note: "simulate_scenarios 的模拟结果应同时标注 run_date 与历史数据区间，以满足 T20a 路线标注格式要求。"

### 2.3 calculate_personal_fit(option, user_profile) -> FitScore

计算决策选项与用户个人画像的匹配度。

```yaml
method: calculate_personal_fit
version: "9"
description: |
 基于用户画像（价值观、技能、偏好、生活阶段等）评估
 决策选项与个人的匹配程度，提供个性化的适配建议。

parameters:
  option:
    type: DecisionOption
    required: true
    description: "待评估的决策选项"

  user_profile:
    type: UserProfile
    required: true
    fields:
      # 基本信息
      age_range:
        type: enum
        values: [under_18, 18_25, 26_35, 36_45, 46_55, 56_65, over_65]
      life_stage:
        type: enum
        values:
          - student
          - early_career
          - mid_career
          - senior_career
          - pre_retirement
          - retired
          - entrepreneur
          - freelancer
      education_level:
        type: enum
        values: [high_school, bachelor, master, doctorate, professional]

      # 技能与能力
      core_skills:
        type: array
        items:
          type: SkillItem
          fields:
            name:
              type: string
            level:
              type: enum
              values: [beginner, intermediate, advanced, expert]
            years_of_experience:
              type: integer
      learning_agility:
        type: float
        min: 0.0
        max: 1.0
        description: "学习敏捷度评分"

      # 价值观与偏好
      value_priorities:
        type: array
        items:
          type: ValuePriority
          fields:
            value:
              type: enum
              values:
                - achievement
                - autonomy
                - security
                - creativity
                - social_impact
                - work_life_balance
                - financial_growth
                - knowledge
                - recognition
                - challenge
            weight:
              type: float
              min: 0.0
              max: 1.0
      risk_preference:
        type: enum
        values: [risk_avoider, cautious, balanced, risk_taker, risk_seeker]
      decision_style:
        type: enum
        values: [analytical, intuitive, collaborative, directive, spontaneous]

      # 约束条件
      financial_situation:
        type: object
        fields:
          monthly_income_range:
            type: object
            fields:
              min:
                type: number
              max:
                type: number
              currency:
                type: string
          savings_months:
            type: integer
            description: "可维持月数的储蓄"
          debt_ratio:
            type: float
            min: 0.0
            max: 1.0
      time_commitments:
        type: array
        items:
          type: TimeCommitment
          fields:
            area:
              type: string
            hours_per_week:
              type: integer
            flexibility:
              type: enum
              values: [fixed, somewhat_flexible, highly_flexible]
      location_preferences:
        type: array
        items:
          type: string
      health_considerations:
        type: array
        items:
          type: string
        default: []

return_value:
  type: FitScore
  fields:
    fit_id:
      type: string
      pattern: "^FIT-[a-f0-9]{12}$"
    overall_fit_score:
      type: float
      min: 0.0
      max: 100.0
      description: "综合匹配度评分"
    fit_level:
      type: enum
      values:
        - excellent_match
        - good_match
        - moderate_match
        - weak_match
        - poor_match

    dimension_fits:
      type: array
      items:
        type: DimensionFit
        fields:
          dimension:
            type: string
          score:
            type: float
            min: 0.0
            max: 100.0
          alignment:
            type: enum
            values: [strongly_aligned, aligned, neutral, misaligned, strongly_misaligned]
          analysis:
            type: string
          recommendations:
            type: array
            items:
              type: string

    value_alignment:
      type: ValueAlignment
      fields:
        score:
          type: float
        matched_values:
          type: array
          items:
            type: string
        mismatched_values:
          type: array
          items:
            type: string
        compromise_required:
          type: boolean
        compromise_areas:
          type: array
          items:
            type: string

    skill_match:
      type: SkillMatch
      fields:
        score:
          type: float
        existing_skills_utilized:
          type: array
          items:
            type: string
        skills_to_develop:
          type: array
          items:
            type: SkillGap
            fields:
              skill:
                type: string
              current_level:
                type: string
              required_level:
                type: string
              gap_severity:
                type: enum
                values: [minor, moderate, significant, critical]
              learning_path:
                type: string

    lifestyle_compatibility:
      type: LifestyleCompatibility
      fields:
        score:
          type: float
        impact_areas:
          type: array
          items:
            type: ImpactArea
            fields:
              area:
                type: string
              impact_level:
                type: enum
                values: [positive, neutral, negative, highly_negative]
              description:
                type: string
              mitigation:
                type: string

    growth_potential:
      type: GrowthPotential
      fields:
        score:
          type: float
        short_term_growth:
          type: string
        long_term_growth:
          type: string
        career_trajectory_impact:
          type: string

    personal_fit_summary:
      type: string
      max_length: 2000
    key_concerns:
      type: array
      items:
        type: string
    key_advantages:
      type: array
      items:
        type: string

exceptions:
  - name: ProfileIncompleteError
    code: "DEP-E020"
    trigger: "用户画像信息不完整，无法计算匹配度"
    recovery: "返回缺失字段清单，持续重试直至用户补充完整画像，不使用默认值填充"
  - name: OptionUndefinedError
    code: "DEP-E021"
    trigger: "提供的选项定义不完整"
    recovery: "返回缺失字段清单"
```

### 2.4 generate_alternatives(constraints) -> AlternativeList

基于约束条件生成创造性的替代方案。

```yaml
method: generate_alternatives
version: "9"
description: |
 在现有选项之外，基于约束条件生成创造性的替代方案。
 运用横向思维和设计思维方法，探索非常规但可行的选项。

parameters:
  constraints:
    type: AlternativeConstraints
    required: true
    fields:
      original_options:
        type: array
        items:
          type: DecisionOption
        description: "原始选项列表，用于参考和对比"
      problem_statement:
        type: string
        required: true
        min_length: 20
        max_length: 2000
        description: "问题陈述，清晰定义需要解决的决策问题"
      hard_constraints:
        type: array
        items:
          type: Constraint
          fields:
            type:
              type: enum
              values: [budget, time, legal, ethical, technical, geographical, personal]
            description:
              type: string
            limit:
              type: string
            negotiable:
              type: boolean
              default: false
        description: "不可妥协的硬约束"
      soft_constraints:
        type: array
        items:
          type: Constraint
        description: "可以协商的软约束"
      creativity_level:
        type: enum
        values:
          - conservative
          - moderate
          - innovative
          - radical
        default: "moderate"
      domains_to_explore:
        type: array
        items:
          type: string
        default: []
        description: "参考的领域引擎列表，用于跨领域灵感"
      max_alternatives:
        type: integer
        default: 5
        min: 1
        max: 10

return_value:
  type: AlternativeList
  fields:
    generation_id:
      type: string
      pattern: "^ALT-[a-f0-9]{12}$"
    alternatives:
      type: array
      items:
        type: AlternativeOption
        fields:
          id:
            type: string
            pattern: "^ALT-OPT-[a-f0-9]{6}$"
          name:
            type: string
          description:
            type: string
          novelty:
            type: enum
            values: [incremental, combinatorial, disruptive, paradigm_shift]
          feasibility:
            type: float
            min: 0.0
            max: 1.0
          potential_upside:
            type: float
            min: 0.0
            max: 1.0
          risk_level:
            type: enum
            values: [very_low, low, medium, high, very_high]
          constraints_satisfied:
            type: array
            items:
              type: string
          constraints_violated:
            type: array
            items:
              type: string
          inspiration_sources:
            type: array
            items:
              type: string
            description: "灵感来源（如跨领域参考）"
          implementation_outline:
            type: string
          pros:
            type: array
            items:
              type: string
          cons:
            type: array
            items:
              type: string
          estimated_effort:
            type: enum
            values: [minimal, low, moderate, high, extreme]
          time_to_implement:
            type: string

    generation_metadata:
      type: object
      fields:
        creativity_level_used:
          type: string
        domains_consulted:
          type: array
          items:
            type: string
        thinking_methods_applied:
          type: array
          items:
            type: enum
            values:
              - lateral_thinking
              - first_principles
              - analogy_mapping
              - constraint_removal
              - inversion
              - scamper
              - design_thinking
              - systems_thinking

exceptions:
  - name: OverConstrainedError
    code: "DEP-E030"
    trigger: "约束条件过于严格，无法生成可行的替代方案"
    recovery: "识别最严格的约束，建议放宽建议"
  - name: NoAlternativesError
    code: "DEP-E031"
    trigger: "在给定约束下无法生成有意义的替代方案"
    recovery: "返回原始选项的优化建议"
```

### 2.5 visualize_decision_tree(options) -> DecisionTree

生成决策树可视化结构。

```yaml
method: visualize_decision_tree
version: "9"
description: |
 将决策选项、评估维度、场景分支组织为可视化的决策树结构，
 支持多种输出格式（Mermaid/JSON/SVG描述）。

parameters:
  options:
    type: array
    required: true
    min_items: 2
    max_items: 10
    items:
      type: DecisionOption

  tree_config:
    type: TreeConfig
    required: false
    default:
      include_scores: true
      include_scenarios: true
      max_depth: 3
      output_format: "mermaid"
    fields:
      include_scores:
        type: boolean
        default: true
        description: "是否在节点中包含评分"
      include_scenarios:
        type: boolean
        default: true
        description: "是否包含场景分支"
      max_depth:
        type: integer
        default: 3
        min: 1
        max: 5
        description: "决策树最大深度"
      output_format:
        type: enum
        values: [mermaid, json, dot, ascii]
        default: "mermaid"
        description: "输出格式"
      highlight_best:
        type: boolean
        default: true
        description: "是否高亮最优路径"
      dimension_weights:
        type: object
        additional_properties:
          type: float
        description: "自定义维度权重覆盖"
      collapse_threshold:
        type: float
        default: 0.1
        description: "低于此权重的分支自动折叠"

return_value:
  type: DecisionTree
  fields:
    tree_id:
      type: string
      pattern: "^TREE-[a-f0-9]{12}$"
    root:
      type: TreeNode
      fields:
        id:
          type: string
        type:
          type: enum
          values: [decision, chance, outcome, terminal]
        label:
          type: string
        description:
          type: string
        score:
          type: float
        probability:
          type: float
        children:
          type: array
          items:
            type: TreeNode
        metadata:
          type: object
          fields:
            highlighted:
              type: boolean
            dimension:
              type: string
            grade:
              type: string

    rendered_output:
      type: string
      description: "根据output_format生成的渲染结果"

    tree_statistics:
      type: object
      fields:
        total_nodes:
          type: integer
        total_leaves:
          type: integer
        max_depth:
          type: integer
        best_path:
          type: array
          items:
            type: string
        average_branching_factor:
          type: float

    legend:
      type: array
      items:
        type: LegendItem
        fields:
          symbol:
            type: string
          meaning:
            type: string
          color:
            type: string

exceptions:
  - name: TreeTooComplexError
    code: "DEP-E040"
    trigger: "决策树节点数量无上限，可视化时自动分页渲染"
    recovery: "持续扩展决策树直至完整，不设节点上限"
  - name: RenderFormatError
    code: "DEP-E041"
    trigger: "请求的输出格式不支持"
    recovery: "穷尽尝试所有可用格式（mermaid）"
```

---

## 3. 五维评估框架

### 3.1 框架总览

```yaml
five_dimension_framework:
  version: "9"
  name: "五维决策评估框架 (5D-DEF)"
  description: |
   对每个决策选项从五个独立维度进行量化评估，
   每个维度包含多个子类别，最终通过加权汇总生成综合评分。

  dimensions:
    - id: "DIM-PROS"
      name: "利弊分析"
      name_en: "Pros & Cons Analysis"
      weight: 0.25
      description: "系统分析每个选项的优缺点"
      sub_categories:
        - id: "PROS-01"
          name: "直接收益"
          weight: 0.35
          description: "选项带来的直接、可量化的收益"
          evaluation_criteria:
            - "收益的确定性程度"
            - "收益的可量化程度"
            - "收益的实现时间"
            - "收益的持续性"
        - id: "PROS-02"
          name: "间接收益"
          weight: 0.25
          description: "选项带来的间接、非量化的收益"
          evaluation_criteria:
            - "对个人成长的促进"
            - "对社交网络的拓展"
            - "对品牌/声誉的提升"
            - "对技能组合的丰富"
        - id: "PROS-03"
          name: "机会成本"
          weight: 0.20
          description: "选择此选项而放弃的其他机会"
          evaluation_criteria:
            - "放弃的最高价值替代方案"
            - "不可逆性程度"
            - "未来恢复可能性"
        - id: "PROS-04"
          name: "协同效应"
          weight: 0.20
          description: "与其他目标/计划的协同程度"
          evaluation_criteria:
            - "与现有计划的互补性"
            - "资源复用程度"
            - "规模效应潜力"

    - id: "DIM-RISK"
      name: "风险评估"
      name_en: "Risk Assessment"
      weight: 0.25
      description: "识别和量化每个选项的潜在风险"
      sub_categories:
        - id: "RISK-01"
          name: "失败概率"
          weight: 0.30
          description: "选项导致负面结果的可能性"
          evaluation_criteria:
            - "历史成功率参考"
            - "外部不确定性因素"
            - "内部执行能力匹配"
        - id: "RISK-02"
          name: "最大损失"
          weight: 0.25
          description: "最坏情况下的损失程度"
          evaluation_criteria:
            - "财务损失上限"
            - "时间损失上限"
            - "声誉损失风险"
            - "健康/安全风险"
        - id: "RISK-03"
          name: "可逆性"
          weight: 0.20
          description: "决策是否可以撤回或调整"
          evaluation_criteria:
            - "完全撤回的可能性"
            - "部分撤回的可能性"
            - "撤回成本"
            - "撤回时间窗口"
        - id: "RISK-04"
          name: "连锁风险"
          weight: 0.15
          description: "触发其他风险的可能性"
          evaluation_criteria:
            - "对其他决策的影响"
            - "多米诺效应风险"
            - "系统性风险暴露"
        - id: "RISK-05"
          name: "风险缓解能力"
          weight: 0.10
          description: "降低或转移风险的能力"
          evaluation_criteria:
            - "可用的风险缓解措施"
            - "保险/对冲工具"
            - "应急预案完备性"

    - id: "DIM-COST"
      name: "成本分析"
      name_en: "Cost Analysis"
      weight: 0.20
      description: "全面评估选项涉及的各类成本"
      sub_categories:
        - id: "COST-01"
          name: "直接成本"
          weight: 0.35
          description: "可直接归因于该选项的货币成本"
          evaluation_criteria:
            - "初始投入金额"
            - "持续运营成本"
            - "隐性成本识别"
            - "成本的可预测性"
        - id: "COST-02"
          name: "时间成本"
          weight: 0.25
          description: "投入的时间及其机会价值"
          evaluation_criteria:
            - "准备时间"
            - "执行时间"
            - "维护时间"
            - "时间灵活性"
        - id: "COST-03"
          name: "精力/心理成本"
          weight: 0.20
          description: "心理压力、认知负荷和情感消耗"
          evaluation_criteria:
            - "压力水平评估"
            - "认知负荷程度"
            - "情感消耗"
            - "倦怠风险"
        - id: "COST-04"
          name: "沉没成本"
          weight: 0.10
          description: "已投入且不可回收的成本"
          evaluation_criteria:
            - "已投入的金额"
            - "已投入的时间"
            - "已建立的关系/资源"
        - id: "COST-05"
          name: "转换成本"
          weight: 0.10
          description: "从当前状态切换到该选项的成本"
          evaluation_criteria:
            - "学习成本"
            - "迁移成本"
            - "适应期长度"

    - id: "DIM-VALUE"
      name: "价值观对齐"
      name_en: "Value Alignment"
      weight: 0.15
      description: "选项与个人核心价值观的匹配程度"
      sub_categories:
        - id: "VAL-01"
          name: "核心价值匹配"
          weight: 0.40
          description: "与用户最看重的价值观的一致性"
          evaluation_criteria:
            - "首要价值观的满足程度"
            - "价值观冲突检测"
            - "长期价值一致性"
        - id: "VAL-02"
          name: "身份认同"
          weight: 0.25
          description: "选项与个人身份认同的契合度"
          evaluation_criteria:
            - "自我形象一致性"
            - "社会认同影响"
            - "个人叙事连贯性"
        - id: "VAL-03"
          name: "伦理考量"
          weight: 0.20
          description: "选项的伦理和道德维度"
          evaluation_criteria:
            - "道德合规性"
            - "社会影响评估"
            - "公平性考量"
        - id: "VAL-04"
          name: "意义感"
          weight: 0.15
          description: "选项带来的意义感和满足感"
          evaluation_criteria:
            - "内在动机满足"
            - "目标感强度"
            - "自我实现程度"

    - id: "DIM-LONGTERM"
      name: "长期影响"
      name_en: "Long-term Impact"
      weight: 0.15
      description: "选项的中长期影响和可持续性"
      sub_categories:
        - id: "LT-01"
          name: "成长轨迹"
          weight: 0.30
          description: "对个人/组织长期发展轨迹的影响"
          evaluation_criteria:
            - "能力提升幅度"
            - "经验积累价值"
            - "职业发展推动"
            - "网络效应"
        - id: "LT-02"
          name: "可持续性"
          weight: 0.25
          description: "选项效果的长期可持续性"
          evaluation_criteria:
            - "收益持续性"
            - "适应性变化能力"
            - "抗周期性"
        - id: "LT-03"
          name: "复利效应"
          weight: 0.25
          description: "随时间累积的复合效应"
          evaluation_criteria:
            - "知识复利"
            - "人脉复利"
            - "财务复利"
            - "声誉复利"
        - id: "LT-04"
          name: "退出价值"
          weight: 0.20
          description: "退出该选项时可保留的价值"
          evaluation_criteria:
            - "可迁移技能"
            - "可保留资产"
            - "可带走的人脉"
            - "履历增值"
```

### 3.2 评分等级定义

```yaml
grading_system:
  scale: "0-100"
  grade_mapping:
    A_plus:
      range: [95, 100]
      label: "卓越"
      description: "在该维度上表现极其出色，几乎无瑕疵"
    A:
      range: [85, 94]
      label: "优秀"
      description: "在该维度上表现优秀，仅有微小改进空间"
    B_plus:
      range: [75, 84]
      label: "良好"
      description: "在该维度上表现良好，有一定改进空间"
    B:
      range: [65, 74]
      label: "中等偏上"
      description: "在该维度上表现中等偏上"
    C_plus:
      range: [55, 64]
      label: "中等"
      description: "在该维度上表现中等，需要关注"
    C:
      range: [45, 54]
      label: "中等偏下"
      description: "在该维度上表现中等偏下，存在明显不足"
    D:
      range: [30, 44]
      label: "较差"
      description: "在该维度上表现较差，需要重大改进"
    F:
      range: [0, 29]
      label: "不可接受"
      description: "在该维度上表现不可接受，属于重大风险"
```

### 3.3 权重自定义

```yaml
weight_customization:
  default_weights:
    DIM-PROS: 0.25
    DIM-RISK: 0.25
    DIM-COST: 0.20
    DIM-VALUE: 0.15
    DIM-LONGTERM: 0.15

  preset_profiles:
    conservative:
      name: "保守型决策者"
      weights:
        DIM-RISK: 0.35
        DIM-COST: 0.25
        DIM-PROS: 0.15
        DIM-VALUE: 0.15
        DIM-LONGTERM: 0.10
      description: "高度重视风险控制，倾向低风险选项"

    growth_oriented:
      name: "成长导向型"
      weights:
        DIM-LONGTERM: 0.30
        DIM-PROS: 0.25
        DIM-VALUE: 0.20
        DIM-RISK: 0.15
        DIM-COST: 0.10
      description: "重视长期成长，愿意承担适度风险"

    value_driven:
      name: "价值驱动型"
      weights:
        DIM-VALUE: 0.35
        DIM-LONGTERM: 0.20
        DIM-PROS: 0.20
        DIM-RISK: 0.15
        DIM-COST: 0.10
      description: "以价值观对齐为首要考量"

    pragmatic:
      name: "务实型"
      weights:
        DIM-COST: 0.30
        DIM-PROS: 0.30
        DIM-RISK: 0.20
        DIM-LONGTERM: 0.10
        DIM-VALUE: 0.10
      description: "注重成本效益比，追求实际回报"

    balanced:
      name: "平衡型"
      weights:
        DIM-PROS: 0.25
        DIM-RISK: 0.25
        DIM-COST: 0.20
        DIM-VALUE: 0.15
        DIM-LONGTERM: 0.15
      description: "均衡考虑所有维度（默认配置）"
```

---

## 4. 输入/输出格式规范

### 4.1 标准输入格式

```yaml
standard_input:
  version: "9"

  required_fields:
    decision_description:
      type: string
      min_length: 10
      max_length: 5000
      description: "决策场景的完整描述"

    options:
      type: array
      min_items: 2
      max_items: 10
      items:
        type: DecisionOption
      description: "待评估的决策选项列表"

  optional_fields:
    user_profile:
      type: UserProfile
      description: "用户画像（用于个性化评估）"
      required_for_methods:
        - calculate_personal_fit

    constraints:
      type: DecisionConstraints
      description: "决策约束条件"

    evaluation_config:
      type: EvaluationConfig
      fields:
        weight_profile:
          type: enum
          values: [conservative, growth_oriented, value_driven, pragmatic, balanced, custom]
          default: "balanced"
        custom_weights:
          type: object
          additional_properties:
            type: float
          description: "自定义维度权重（weight_profile为custom时使用）"
        detail_level:
          type: enum
          values: [summary, standard, detailed]
          default: "standard"
        include_recommendations:
          type: boolean
          default: true
        language:
          type: string
          default: "zh-CN"
```

### 4.2 标准输出格式

```yaml
standard_output:
  version: "9"

  core_structure:
    evaluation_id:
      type: string
      description: "评估唯一标识"

    executive_summary:
      type: string
      max_length: 2000
      description: "评估结果执行摘要"

    dimension_scores:
      type: DimensionScores
      description: "五维评估详细结果"

    overall_ranking:
      type: array
      items:
        type: RankedOption
      description: "选项综合排名"

    recommendations:
      type: array
      items:
        type: Recommendation
        fields:
          type:
            type: enum
            values: [primary, alternative, contextual, avoid]
          option_id:
            type: string
          rationale:
            type: string
          conditions:
            type: array
            items:
              type: string
          confidence:
            type: float

    caveats:
      type: array
      items:
        type: string
      description: "评估前提和注意事项"

    next_steps:
      type: array
      items:
        type: NextStep
        fields:
          action:
            type: string
          priority:
            type: enum
            values: [immediate, short_term, medium_term, long_term]
          owner:
            type: string
          deadline:
            type: string

    metadata:
      type: EvaluationMetadata
```

---

## 5. 质量门控

### 5.1 方法级质量检查点

```yaml
quality_gates:
  evaluate_dimensions:
    gate_id: "QG-EVAL-001"
    checks:
      - id: "QEC-001"
        name: "选项覆盖检查"
        condition: "所有输入选项均已评估"
        severity: "blocking"
        message: "每个输入选项必须产生对应的评估结果"
      - id: "QEC-002"
        name: "维度完整性检查"
        condition: "五个维度均已评分"
        severity: "blocking"
        message: "五维评估框架的每个维度都必须有评分"
      - id: "QEC-003"
        name: "评分范围检查"
        condition: "所有评分在0-100范围内"
        severity: "blocking"
        message: "评分值必须在有效范围内"
      - id: "QEC-004"
        name: "排名一致性检查"
        condition: "综合排名与维度评分一致"
        severity: "warning"
        message: "综合排名应与加权评分结果一致"
      - id: "QEC-005"
        name: "证据充分性检查"
        condition: "每个评分有对应的证据或理由"
        severity: "warning"
        message: "评分应附带充分的理由说明"
      - id: "QEC-006"
        name: "权重归一化检查"
        condition: "所有维度权重之和等于1.0"
        severity: "blocking"
        message: "维度权重必须归一化"

  simulate_scenarios:
    gate_id: "QG-SIM-001"
    checks:
      - id: "QSC-001"
        name: "场景覆盖检查"
        condition: "至少包含3个不同场景（乐观/基准/悲观）"
        severity: "blocking"
        message: "场景模拟必须覆盖乐观、基准和悲观情况"
      - id: "QSC-002"
        name: "概率合理性检查"
        condition: "所有场景概率之和等于1.0"
        severity: "blocking"
        message: "场景概率分布必须有效"
      - id: "QSC-003"
        name: "收敛性检查"
        condition: "蒙特卡洛模拟已收敛"
        severity: "warning"
        message: "模拟结果应达到统计收敛"
      - id: "QSC-004"
        name: "敏感性分析完整性"
        condition: "至少分析3个关键变量"
        severity: "warning"
        message: "敏感性分析应覆盖主要不确定因素"

  calculate_personal_fit:
    gate_id: "QG-FIT-001"
    checks:
      - id: "QFC-001"
        name: "匹配度范围检查"
        condition: "0 <= overall_fit_score <= 100"
        severity: "blocking"
        message: "匹配度评分必须在有效范围内"
      - id: "QFC-002"
        name: "维度覆盖检查"
        condition: "至少评估4个匹配维度"
        severity: "blocking"
        message: "个人匹配度评估应覆盖多个维度"
      - id: "QFC-003"
        name: "画像一致性检查"
        condition: "评估结果与用户画像逻辑一致"
        severity: "warning"
        message: "匹配度结果应与用户画像特征相符"

  generate_alternatives:
    gate_id: "QG-ALT-001"
    checks:
      - id: "QAC-001"
        name: "替代方案数量检查"
        condition: "至少生成1个可行替代方案"
        severity: "blocking"
        message: "必须生成至少一个可行的替代方案"
      - id: "QAC-002"
        name: "约束满足检查"
        condition: "所有硬约束均被满足"
        severity: "blocking"
        message: "生成的替代方案必须满足所有硬约束"
      - id: "QAC-003"
        name: "差异化检查"
        condition: "替代方案与原始选项有显著差异"
        severity: "warning"
        message: "替代方案应提供不同于原始选项的新视角"
      - id: "QAC-004"
        name: "可行性下限检查"
        condition: "所有替代方案可行性 >= 0.2"
        severity: "warning"
        message: "可行性过低的方案应标注明确风险"

  visualize_decision_tree:
    gate_id: "QG-TREE-001"
    checks:
      - id: "QTC-001"
        name: "树结构完整性"
        condition: "决策树包含所有输入选项"
        severity: "blocking"
        message: "决策树必须包含所有待评估的选项"
      - id: "QTC-002"
        name: "渲染格式检查"
        condition: "输出格式符合目标格式规范"
        severity: "blocking"
        message: "渲染输出必须是有效的目标格式"
      - id: "QTC-003"
        name: "节点数量检查"
        condition: "总节点数 <= 500"
        severity: "warning"
        message: "决策树复杂度应在可视化可处理范围内"
```

### 5.2 v2 Supervsior 集成

在 v2 中，决策评估产出的质量门控通过 [Supervisor Protocol](supervisors/supervisor_protocol.md) 执行。上述质量检查点作为 Supervisor checklist 的检查项，由独立检查员判定 PASS/FAIL/RETRYING。

```yaml
v2_supervisor_integration:
  decision_related_tasks:
    - task: "T05"
      supervisor_checks:
        - "L6证据边界标注完整性"
        - "L7利益相关者覆盖度"
        - "证据强度等级合理性"

    - task: "T10"
      supervisor_checks:
        - "对抗性逻辑有效性"
        - "假设推翻充分性"

    - task: "T11"
      supervisor_checks:
        - "对抗证据来源可靠性"
        - "反例充分性"

  retrying_policy:
    reference: "exhaust-retry-protocol.md"
    quality_driven: true
    on_retrying: "标注缺失维度，下游降低置信度"
```

---

## 附录

### B. 术语表

| 术语 | 英文 | 定义 |
|------|------|------|
| 五维评估 | 5D Evaluation | 利弊/风险/成本/价值观/长期影响五个维度的综合评估 |
| 场景模拟 | Scenario Simulation | 对决策选项在多种可能场景下的表现进行推演 |
| 个人匹配度 | Personal Fit | 决策选项与用户个人特征的匹配程度 |
| 决策树 | Decision Tree | 将决策过程可视化为树状结构的工具 |
| 敏感性分析 | Sensitivity Analysis | 分析关键变量变化对决策结果的影响程度 |

### C. 交叉引用

- [execution-protocol.md](./execution-protocol.md) — Phase 0-3 执行规则与 DAG 调度
- [handoff-protocol.md](./handoff-protocol.md) — Context Package 标准格式
- [exhaust-retry-protocol.md](./exhaust-retry-protocol.md) — 节点失败穷尽重试策略
- [domain-analysis-protocol.md](./domain-analysis-protocol.md) — 领域分析协议
- `supervisors/supervisor_protocol.md` — Supervisor 判定标准与宪法条款
- `tasks/T04_L4_L5_compare.md` — L4+L5 结构化比较任务
- `tasks/T10_adversarial_logic.md` — 对抗逻辑任务
- `tasks/T11_adversarial_evidence.md` — 对抗证据任务

## 交叉引用

- [nrsf-protocol.md](./nrsf-protocol.md) — NRSF 叙事式研究状态文件协议
- [self-evaluation-protocol.md](./self-evaluation-protocol.md) — T19 双阶段自评协议
- [iterative-deepening-protocol.md](./iterative-deepening-protocol.md) — I01 迭代深化协议


---
© 阿洋