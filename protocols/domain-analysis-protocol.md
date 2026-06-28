> **作者**: 阿洋

# 领域分析统一协议 (Domain Analysis Protocol)

> > **状态**: 正式发布 (v2 适配)
> **适用范围**: Profound Cognition v2 — 所有35个领域引擎必须实现此协议
> **最后更新**: 2026-05-15

---

## 1. 协议概述

### 1.1 目的

DomainAnalysisProtocol 定义了系统中所有领域分析引擎必须遵循的统一通信接口标准。该协议确保：

- **接口一致性**: 所有领域引擎对外暴露相同的方法签名和数据结构
- **可替换性**: 任何领域引擎可以被同类型的其他引擎无缝替换
- **可组合性**: 多个领域引擎的分析结果可以交叉引用和融合
- **质量可控**: 通过统一的质量门控机制保证分析输出的可靠性
- **可观测性**: 标准化的错误处理和日志格式便于系统监控

### 1.2 v2 多任务调用方式

在 Profound Cognition v2 中，领域引擎不再被直接调用，而是通过 **[T15 领域引擎分析](tasks/T15_domain_analysis.md)** 任务批量激活和管理。调用流程如下：

```
Phase 1 调度循环
  │
  ├── T01 输入分流 → 生成 domain_engine_recommendations
  │
  ├── T13 认知综合 → 输出 core_conclusions
  │
  ├── T15 领域引擎分析 (Gate-γ 组)
  │     ├── 接收 context_package:
  │     │     ├── problem (来自主LLM)
  │     │     ├── T01.domain_engine_recommendations
  │     │     └── T13.core_conclusions
  │     │
  │     ├── 批量激活推荐的领域引擎 (≥1个)
  │     ├── 每个引擎独立执行 analyze()
  │     ├── 跨领域交叉验证 (cross_domain_bridge)
  │     └── 输出结构化领域分析结果
  │
  └── T17/T18 使用 T15 产出进行事实核查和偏差检测
```

v2 中领域引擎的执行上下文由主LLM通过 [handoff-protocol.md](./handoff-protocol.md) 中定义的 context_package 注入，单次 Sub-Agent 调用可能激活多个引擎。

### 1.3 适用范围

本协议适用于以下35个领域引擎：

| 编号 | 领域引擎标识 | 领域名称 |
|------|-------------|---------|
| D01 | `tech` | 科技与技术 |
| D02 | `health` | 医疗与健康 |
| D03 | `education` | 教育与学习 |
| D04 | `law` | 法律与合规 |
| D05 | `business` | 商业与管理 |
| D06 | `finance-quant` | 金融与量化分析 |
| D07 | `history` | 历史 |
| D08 | `science` | 科学研究 |
| D09 | `environment-climate` | 环境与气候 |
| D10 | `art` | 艺术与设计 |
| D11 | `sports` | 体育与运动 |
| D12 | `food` | 美食与烹饪 |
| D13 | `culture` | 文化 |
| D14 | `film` | 影视 |
| D15 | `media-communication` | 媒体与传播 |
| D16 | `literature` | 文学与写作 |
| D17 | `political` | 政治 |
| D18 | `psychology` | 心理与行为 |
| D19 | `social` | 社会与群体 |
| D20 | `philosophy` | 哲学与思想 |
| D21 | `religion` | 宗教与信仰 |
| D22 | `cognitive-science` | 认知科学 |
| D23 | `engineering` | 工程学 |
| D24 | `urban-planning` | 城市规划 |
| D25 | `anthropology` | 人类学 |
| D26 | `architecture` | 建筑学 |
| D27 | `data` | 数据科学 |
| D28 | `design` | 设计 |
| D29 | `diplomacy` | 外交 |
| D30 | `economics` | 经济学 |
| D31 | `linguistics` | 语言学 |
| D32 | `mathematics` | 数学 |
| D33 | `military` | 军事 |
| D34 | `music` | 音乐 |
| D35 | `national-power` | 国家综合国力 |

### 1.4 协议层级架构

```
┌─────────────────────────────────────────┐
│ v2 Phase 1 调度 (主LLM)                 │
├─────────────────────────────────────────┤
│ T15 领域引擎分析 (Sub-Agent)            │
│   ├── 接收 context_package              │
│   ├── 激活 D01-D35 (按需)               │
│   └── 跨领域交叉验证                     │
├─────────────────────────────────────────┤
│ 协议层 (Protocol Layer)                  │
│ DomainAnalysisProtocol                   │
├─────────────────────────────────────────┤
│ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐       │
│ │ D01 │ │ ... │ │ D35 │   │
│ └─────┘ └─────┘ └─────┘ └─────┘       │
│ 领域引擎实现层                            │
├─────────────────────────────────────────┤
│ 基础设施层 (Infrastructure)              │
└─────────────────────────────────────────┘
```

---

## 2. 核心方法定义

### 2.1 analyze(input, context) -> AnalysisResult

对输入内容执行完整的深度领域分析，生成结构化的分析报告。统一使用深度执行策略。

```yaml
method: analyze
version: "3.0"
description: |
 对输入内容执行完整的领域分析，返回结构化分析结果。
 这是领域引擎的核心方法，所有其他方法可视为辅助方法。

parameters:
  input:
    type: AnalysisInput
    required: true
    description: 分析输入对象，包含原始数据和元信息
    fields:
      raw_input:
        type: string
        required: true
        min_length: 1
        max_length: 100000
        description: 原始输入文本或数据
      object_type:
        type: enum
        required: true
        values:
          - text_article
          - question
          - decision_scenario
          - dataset
          - code_snippet
          - multimedia
          - conversation
          - report
        description: 输入对象的类型标识
      source_language:
        type: string
        required: false
        default: "auto"
        pattern: "^[a-z]{2}(-[A-Z]{2})?$"
        description: 输入内容的语言代码，auto表示自动检测
      metadata:
        type: object
        required: false
        description: 附加元数据
        fields:
          author:
            type: string
            description: 内容作者
          timestamp:
            type: datetime
            format: "ISO 8601"
            description: 内容创建时间
          tags:
            type: array
            items:
              type: string
            description: 内容标签
          references:
            type: array
            items:
              type: string
            description: 引用来源

  context:
    type: AnalysisContext
    required: false
    default: null
    description: 分析上下文，提供额外的背景信息
    fields:
      user_profile:
        type: UserProfile
        description: 用户画像信息
        fields:
          expertise_level:
            type: enum
            values: [novice, intermediate, expert, specialist]
            default: intermediate
          domain_familiarity:
            type: float
            min: 0.0
            max: 1.0
            default: 0.5
          preferences:
            type: object
            fields:
              detail_level:
                type: enum
                values: [brief, moderate, comprehensive]
                default: moderate
              analytical_style:
                type: enum
                values: [pragmatic, theoretical, balanced]
                default: balanced
      previous_analysis:
        type: array
        items:
          type: AnalysisResult
        description: 之前的分析结果，用于增量分析
        default: []
      domain_constraints:
        type: array
        items:
          type: string
        description: 领域特定的约束条件
        default: []

return_value:
  type: AnalysisResult
  description: 结构化分析结果
  fields:
    report_id:
      type: string
      pattern: "^RPT-[A-Z]{3}-\\d{8}-[a-f0-9]{8}$"
      description: 报告唯一标识符
    domain:
      type: string
      description: 执行分析的领域引擎标识
    analysis_summary:
      type: string
      max_length: 2000
      description: 分析结果摘要（一句话概括）
    structured_report:
      type: StructuredReport
      description: 结构化报告主体
      fields:
        sections:
          type: array
          items:
            type: ReportSection
            fields:
              heading:
                type: string
                required: true
              content:
                type: string
                required: true
              subsections:
                type: array
                items:
                  type: ReportSection
        key_findings:
          type: array
          items:
            type: Finding
            fields:
              statement:
                type: string
              evidence:
                type: array
                items:
                  type: string
              confidence:
                type: float
                min: 0.0
                max: 1.0
              significance:
                type: float
                min: 0.0
                max: 1.0
              priority:
                type: enum
                values: [critical, high, medium, low]
        insights:
          type: array
          items:
            type: Insight
            fields:
              category:
                type: string
              description:
                type: string
              supporting_data:
                type: array
                items:
                  type: string
              novelty_score:
                type: float
                min: 0.0
                max: 1.0
              actionability:
                type: float
                min: 0.0
                max: 1.0
    confidence_scores:
      type: ConfidenceScores
      fields:
        overall:
          type: float
          min: 0.0
          max: 1.0
          description: 整体置信度
        per_dimension:
          type: object
          additional_properties:
            type: float
            min: 0.0
            max: 1.0
          description: 各分析维度的置信度
        uncertainty_sources:
          type: array
          items:
            type: UncertaintySource
            fields:
              factor:
                type: string
              impact:
                type: enum
                values: [low, medium, high]
              mitigation:
                type: string
    cross_domain_links:
      type: array
      items:
        type: CrossDomainLink
        fields:
          target_domain:
            type: string
          link_type:
            type: enum
            values: [complementary, contradictory, evolutionary, causal, analogous]
          description:
            type: string
          relevance_score:
            type: float
            min: 0.0
            max: 1.0
    metadata:
      type: AnalysisMetadata
      fields:
        execution_time_ms:
          type: integer
        engine_version:
          type: string
        protocol_version:
          type: string
          default: "9"
        token_usage:
          type: object
          fields:
            input:
              type: integer
            output:
              type: integer
            total:
              type: integer

exceptions:
  - name: InvalidInputError
    code: "DAP-E001"
    trigger: "输入数据格式不符合规范或缺少必要字段"
    recovery: "返回详细的字段校验错误信息，指导调用方修正输入"
  - name: DomainNotSupportedError
    code: "DAP-E002"
    trigger: "请求的领域不在已注册的35个领域引擎范围内"
    recovery: "返回支持的领域列表，建议使用最接近的替代领域"
  - name: AnalysisCapacityExceededError
    code: "DAP-E003"
    trigger: "分析工作量超出当前引擎的单次处理能力上限（如极端庞大的输入数据）"
    recovery: "执行分批处理策略，合并分批结果后交付。不存在'低一级复杂度'——所有分析统一深度执行。"
  - name: ContextConflictError
    code: "DAP-E004"
    trigger: "提供的上下文信息与分析内容存在逻辑冲突"
    recovery: "记录冲突详情，以无上下文模式重新执行分析"
  - name: AnalysisTimeoutError
    code: "DAP-E005"
    trigger: "分析执行超时（不设超时上限，持续执行直至完成）"
    recovery: "标注 RETRYING，持续重试直至完整分析通过，不返回部分结果"
  - name: ResourceExhaustedError
    code: "DAP-E006"
    trigger: "计算资源（内存/CPU/Token配额）不足"
    recovery: "排队等待资源释放后重试。不可缩小分析范围——所有分析统一深度执行。"
```

### 2.2 extract_themes(input) -> ThemeList

从输入内容中提取核心主题和话题。

```yaml
method: extract_themes
version: "3.0"
description: |
 从输入内容中提取核心主题、子主题和话题标签。
 支持层级化主题结构，可识别显式主题和隐含主题。

parameters:
  input:
    type: ThemeExtractionInput
    required: true
    fields:
      raw_input:
        type: string
        required: true
        min_length: 10
        max_length: 50000
        description: 待提取主题的原始文本
      max_themes:
        type: integer
        required: false
        default: 10
        min: 1
        max: 50
        description: 最大提取主题数量
      extraction_depth:
        type: enum
        required: false
        default: "standard"
        values:
          - surface
          - standard
          - deep
      language:
        type: string
        required: false
        default: "auto"
        description: 文本语言

return_value:
  type: ThemeList
  fields:
    primary_themes:
      type: array
      items:
        type: Theme
        fields:
          id:
            type: string
            pattern: "^THM-[a-f0-9]{8}$"
          name:
            type: string
            required: true
          description:
            type: string
          weight:
            type: float
            min: 0.0
            max: 1.0
            description: 主题权重，表示在内容中的占比
          keywords:
            type: array
            items:
              type: string
          sub_themes:
            type: array
            items:
              type: Theme
          evidence_spans:
            type: array
            items:
              type: TextSpan
              fields:
                start:
                  type: integer
                end:
                  type: integer
                text:
                  type: string
          relevance:
            type: float
          sentiment:
            type: enum
            values: [positive, negative, neutral, mixed]
      description: 主要主题列表，按权重降序排列
    implicit_themes:
      type: array
      items:
        type: Theme
      description: 隐含主题列表（需extraction_depth >= standard）
    theme_relationships:
      type: array
      items:
        type: ThemeRelationship
        fields:
          source:
            type: string
          target:
            type: string
          relation_type:
            type: enum
            values: [hierarchical, associative, causal, contrastive, temporal]
          strength:
            type: float
            min: 0.0
            max: 1.0
    extraction_metadata:
      type: object
      fields:
        total_keywords_found:
          type: integer
        coverage_ratio:
          type: float
          description: 主题对原文内容的覆盖率
        confidence:
          type: float

exceptions:
  - name: InputTooShortError
    code: "DAP-E010"
    trigger: "输入文本长度不足10个字符"
    recovery: "提示调用方提供更多文本内容"
  - name: NoThemeDetectedError
    code: "DAP-E011"
    trigger: "无法从输入中提取到有效主题"
    recovery: "返回通用主题建议，建议用户补充上下文"
```

### 2.3 evaluate_significance(finding, domain_context) -> SignificanceScore

评估某个发现在特定领域上下文中的重要性和影响力。

```yaml
method: evaluate_significance
version: "3.0"
description: |
 评估一个分析发现在特定领域上下文中的重要性。
 综合考虑领域标准、时效性、影响范围和可操作性。

parameters:
  finding:
    type: Finding
    required: true
    fields:
      statement:
        type: string
        required: true
        description: 发现陈述
      evidence:
        type: array
        items:
          type: string
        description: 支持证据
      source_reliability:
        type: float
        min: 0.0
        max: 1.0
        default: 0.5
        description: 来源可靠性评分
      novelty:
        type: float
        min: 0.0
        max: 1.0
        default: 0.5
        description: 新颖性评分

  domain_context:
    type: DomainContext
    required: true
    fields:
      domain_id:
        type: string
        required: true
        description: 领域引擎标识
      evaluation_criteria:
        type: array
        items:
          type: EvaluationCriterion
          fields:
            name:
              type: string
            weight:
              type: float
              min: 0.0
              max: 1.0
            description:
              type: string
            scoring_rubric:
              type: string
              description: 评分标准说明
      temporal_context:
        type: object
        fields:
          reference_date:
            type: datetime
            format: "ISO 8601"
          time_sensitivity:
            type: enum
            values: [timeless, seasonal, current, outdated]
          relevance_window:
            type: string
            pattern: "^P(\\d+Y)?(\\d+M)?(\\d+D)?$"
            description: 相关性时间窗口（ISO 8601 Duration）
      impact_scope:
        type: enum
        values: [individual, team, organization, industry, global]
        default: "organization"
      stakeholder_groups:
        type: array
        items:
          type: string
        description: 利益相关方群体

return_value:
  type: SignificanceScore
  fields:
    overall_score:
      type: float
      min: 0.0
      max: 1.0
      description: 综合重要性评分
    dimension_scores:
      type: object
      fields:
        domain_relevance:
          type: float
          min: 0.0
          max: 1.0
          description: 领域相关性
        impact_magnitude:
          type: float
          min: 0.0
          max: 1.0
          description: 影响力度
        actionability:
          type: float
          min: 0.0
          max: 1.0
          description: 可操作性
        novelty_value:
          type: float
          min: 0.0
          max: 1.0
          description: 新颖价值
        timeliness:
          type: float
          min: 0.0
          max: 1.0
          description: 时效性
    significance_level:
      type: enum
      values:
        - transformative
        - substantial
        - moderate
        - marginal
        - negligible
    justification:
      type: string
      description: 评分理由说明
    comparable_findings:
      type: array
      items:
        type: object
        fields:
          finding:
            type: string
          score:
            type: float
          comparison_note:
            type: string

exceptions:
  - name: InvalidDomainError
    code: "DAP-E020"
    trigger: "提供的领域标识不在已注册范围内"
    recovery: "返回可用领域列表"
  - name: MissingCriterionError
    code: "DAP-E021"
    trigger: "领域上下文缺少必要的评估标准"
    recovery: "使用领域默认评估标准，并记录警告"
```

### 2.4 get_analysis_dimensions() -> DimensionList

获取当前领域引擎支持的所有分析维度。

```yaml
method: get_analysis_dimensions
version: "3.0"
description: |
 返回当前领域引擎支持的所有分析维度定义。
 每个维度包含名称、描述、子维度和评估标准。
 此方法不需要输入参数，用于引擎自省和能力发现。

parameters: {}

return_value:
  type: DimensionList
  fields:
    domain_id:
      type: string
      description: 领域引擎标识
    domain_name:
      type: string
      description: 领域名称
    version:
      type: string
      description: 维度定义版本
    dimensions:
      type: array
      items:
        type: AnalysisDimension
        fields:
          id:
            type: string
            pattern: "^DIM-[A-Z]{2,4}-\\d{3}$"
            description: 维度唯一标识
          name:
            type: string
            required: true
            description: 维度名称
          description:
            type: string
            required: true
            description: 维度描述
          weight:
            type: float
            min: 0.0
            max: 1.0
            default: 0.0
            description: 维度在综合分析中的权重
          sub_dimensions:
            type: array
            items:
              type: SubDimension
              fields:
                id:
                  type: string
                name:
                  type: string
                description:
                  type: string
                weight:
                  type: float
                evaluation_criteria:
                  type: array
                  items:
                    type: EvaluationCriterion
                    fields:
                      name:
                        type: string
                      description:
                        type: string
                      scale:
                        type: enum
                        values: [binary, likert_3, likert_5, likert_7, continuous_0_1, continuous_0_100]
                      benchmark:
                        type: float
                        description: 基准值
                data_requirements:
                  type: array
                  items:
                    type: DataRequirement
                    fields:
                      data_type:
                        type: string
                      required:
                        type: boolean
                      description:
                        type: string
                dependencies:
                  type: array
                  items:
                    type: string
                  description: 依赖的其他维度ID
    terminology:
      type: TerminologySystem
      fields:
        glossary:
          type: array
          items:
            type: TermDefinition
            fields:
              term:
                type: string
              definition:
                type: string
              aliases:
                type: array
                items:
                  type: string
              related_terms:
                type: array
                items:
                  type: string
              domain_specific:
                type: boolean
        abbreviations:
          type: object
          additional_properties:
            type: string
        units:
          type: array
          items:
            type: UnitDefinition
            fields:
              symbol:
                type: string
              full_name:
                type: string
              conversion_to_si:
                type: string

exceptions:
  - name: EngineNotInitializedError
    code: "DAP-E030"
    trigger: "领域引擎尚未完成初始化"
    recovery: "触发引擎初始化流程后重试"
```

### 2.5 cross_domain_bridge(analysis, target_domain) -> BridgeResult

将当前领域的分析结果桥接到目标领域，建立跨领域关联。

```yaml
method: cross_domain_bridge
version: "3.0"
description: |
 将当前领域的分析结果映射到目标领域，识别跨领域的关联性、
 互补性和矛盾点。支持24个领域之间的任意桥接。

parameters:
  analysis:
    type: AnalysisResult
    required: true
    description: 源领域的分析结果（来自analyze方法的输出）

  target_domain:
    type: string
    required: true
    pattern: "^(anthropology|architecture|art|business|cognitive-science|culture|data|design|diplomacy|economics|education|engineering|environment-climate|film|finance-quant|food|health|history|law|linguistics|literature|mathematics|media-communication|military|music|national-power|philosophy|political|psychology|religion|science|social|sports|tech|urban-planning)$"
    description: 目标领域引擎标识

  bridge_options:
    type: BridgeOptions
    required: false
    default:
      depth: standard
      include_contradictions: true
      include_analogies: true
    fields:
      depth:
        type: enum
        values: [shallow, standard, deep]
        default: standard
      include_contradictions:
        type: boolean
        default: true
        description: 是否包含跨领域矛盾点
      include_analogies:
        type: boolean
        default: true
        description: 是否包含类比关联
      max_links:
        type: integer
        default: 20
        min: 1
        max: 100

return_value:
  type: BridgeResult
  fields:
    source_domain:
      type: string
    target_domain:
      type: string
    bridge_summary:
      type: string
      description: 跨领域桥接摘要
    connections:
      type: array
      items:
        type: DomainConnection
        fields:
          source_finding:
            type: string
          target_perspective:
            type: string
          connection_type:
            type: enum
            values:
              - complementary
              - contradictory
              - evolutionary
              - causal
              - analogous
              - foundational
              - applied
          strength:
            type: float
            min: 0.0
            max: 1.0
          explanation:
            type: string
          bidirectional:
            type: boolean
    insights:
      type: array
      items:
        type: CrossDomainInsight
        fields:
          title:
            type: string
          description:
            type: string
          domains_involved:
            type: array
            items:
              type: string
          potential_applications:
            type: array
            items:
              type: string
          confidence:
            type: float
    gaps:
      type: array
      items:
        type: KnowledgeGap
        fields:
          area:
            type: string
          description:
            type: string
          suggested_research:
            type: string
          bridging_domains:
            type: array
            items:
              type: string
    bridge_quality:
      type: BridgeQuality
      fields:
        coherence_score:
          type: float
          min: 0.0
          max: 1.0
        coverage_ratio:
          type: float
          min: 0.0
          max: 1.0
        novelty_score:
          type: float
          min: 0.0
          max: 1.0

exceptions:
  - name: SameDomainError
    code: "DAP-E040"
    trigger: "源领域与目标领域相同"
    recovery: "返回提示信息，建议选择不同的目标领域"
  - name: BridgeNotSupportedError
    code: "DAP-E041"
    trigger: "源领域与目标领域之间不存在可建立的桥接关系"
    recovery: "返回推荐的替代目标领域列表"
  - name: AnalysisIncompatibleError
    code: "DAP-E042"
    trigger: "提供的分析结果格式与协议不兼容"
    recovery: "返回格式要求说明，指导调用方适配"
```

---

## 3. 输入格式规范

### 3.1 标准输入对象 (StandardInput)

```yaml
StandardInput:
  version: "3.0"
  description: "所有领域引擎必须接受的标准输入格式"

  fields:
    raw_input:
      type: string
      required: true
      constraints:
        min_length: 1
        max_length: 100000
        encoding: "UTF-8"
      description: "原始输入内容，支持纯文本、Markdown、结构化JSON字符串"
      examples:
        - "请分析人工智能在医疗诊断中的应用前景"
        - '{"question": "是否应该进行远程办公？", "context": "IT公司，500人规模"}'

    object_type:
      type: enum
      required: true
      values:
        - text_article: "文章/论文/博客"
        - question: "问题/咨询/求助"
        - decision_scenario: "决策场景/选择困境"
        - dataset: "数据集/统计资料"
        - code_snippet: "代码片段/技术方案"
        - multimedia: "多媒体内容描述"
        - conversation: "对话记录/访谈"
        - report: "报告/文档/白皮书"
      description: "输入对象的语义类型"

    execution_profile:
      type: enum
      required: false
      default: "deep"
      description: "统一使用深度执行策略，所有任务默认完整分析"
      values:
        - deep:
            description: "深度分析（默认唯一策略）"
            max_execution_time: "不设上限（EXHAUST 模式，持续执行直至完成）"
            max_tokens: "不设上限（EXHAUST 模式）"

    geo_context:
      type: GeoContext
      required: false
      description: "地理上下文信息"
      fields:
        region:
          type: string
          description: "地区/国家"
          examples: ["中国大陆", "美国", "欧盟"]
        locale:
          type: string
          pattern: "^[a-z]{2}(-[A-Z]{2})?$"
          default: "zh-CN"
        regulatory_framework:
          type: string
          description: "适用的监管框架"
          examples: ["GDPR", "个人信息保护法", "SOX"]

    constraints:
      type: AnalysisConstraints
      required: false
      description: "分析约束条件"
      fields:
        max_length:
          type: integer
          default: null
          description: "输出最大长度限制"
        focus_areas:
          type: array
          items:
            type: string
          default: []
          description: "指定关注的分析领域"
        exclude_areas:
          type: array
          items:
            type: string
          default: []
          description: "排除的分析领域"
        perspective:
          type: enum
          values: [neutral, optimistic, pessimistic, critical, advocative]
          default: "neutral"
          description: "分析视角偏好"
        format_preference:
          type: enum
          values: [narrative, bullet_points, table, mixed]
          default: "mixed"
        sensitivity_level:
          type: enum
          values: [public, internal, confidential, restricted]
          default: "public"
          description: "内容敏感度级别"
```

### 3.2 输入校验规则

```yaml
input_validation:
  pre_processing:
    - step: "encoding_check"
      rule: "输入必须为有效UTF-8编码"
      error_code: "VAL-E001"
    - step: "type_check"
      rule: "object_type必须在允许的枚举值范围内"
      error_code: "VAL-E002"
    - step: "length_check"
      rule: "raw_input长度在1-100000字符之间"
      error_code: "VAL-E003"
    - step: "sanitization"
      rule: "移除潜在的注入代码和恶意内容"
      error_code: "VAL-E004"
    - step: "language_detection"
      rule: "自动检测输入语言，支持中英文及混合输入"
      error_code: "VAL-E005"
  post_validation:
    - step: "completeness_check"
      rule: "验证必填字段均已提供"
    - step: "consistency_check"
      rule: "验证字段间的一致性（如locale与region）"
    - step: "constraint_feasibility"
      rule: "验证约束条件是否可满足"
```

---

## 4. 输出格式规范

### 4.1 标准输出对象 (StandardOutput)

```yaml
StandardOutput:
  version: "3.0"
  description: "所有领域引擎必须返回的标准输出格式"

  fields:
    structured_report:
      type: StructuredReport
      required: true
      description: "结构化分析报告"
      fields:
        title:
          type: string
          required: true
          max_length: 200
        sections:
          type: array
          items:
            type: ReportSection
          required: true
          min_items: 1
        executive_summary:
          type: string
          max_length: 1000
          description: "执行摘要"
        methodology:
          type: string
          description: "分析方法说明"
        assumptions:
          type: array
          items:
            type: string
          description: "分析假设列表"
        limitations:
          type: array
          items:
            type: string
          description: "分析局限性说明"

    insights:
      type: array
      items:
        type: Insight
      required: true
      min_items: 1
      constraints:
        - "至少包含1个高置信度洞察（confidence >= 0.7）"
      fields_per_item:
        category:
          type: string
          required: true
          description: "洞察类别"
        title:
          type: string
          required: true
        description:
          type: string
          required: true
        evidence:
          type: array
          items:
            type: string
        confidence:
          type: float
          required: true
          min: 0.0
          max: 1.0
        novelty_score:
          type: float
          min: 0.0
          max: 1.0
        actionability:
          type: float
          min: 0.0
          max: 1.0
        priority:
          type: enum
          values: [critical, high, medium, low]

    confidence_scores:
      type: ConfidenceScores
      required: true
      fields:
        overall:
          type: float
          required: true
          min: 0.0
          max: 1.0
          description: "整体置信度"
        per_dimension:
          type: object
          required: true
          additional_properties:
            type: float
            min: 0.0
            max: 1.0
          description: "各维度置信度"
        uncertainty_breakdown:
          type: array
          items:
            type: UncertaintyFactor
            fields:
              source:
                type: string
              level:
                type: float
              description:
                type: string
              mitigable:
                type: boolean

    cross_domain_links:
      type: array
      items:
        type: CrossDomainLink
      required: false
      default: []
      fields_per_item:
        target_domain:
          type: string
          required: true
        link_type:
          type: enum
          required: true
          values: [complementary, contradictory, evolutionary, causal, analogous]
        summary:
          type: string
          required: true
        relevance_score:
          type: float
          required: true
          min: 0.0
          max: 1.0
        bidirectional:
          type: boolean
          default: false
```

### 4.2 输出质量指标

```yaml
output_quality_metrics:
  readability:
    metric: "Flesch-Kincaid等效级别"
    target: "适合目标受众的阅读水平"
    thresholds:
      novice: "grade_level <= 8"
      intermediate: "grade_level <= 12"
      expert: "no restriction"
  completeness:
    metric: "必要字段填充率"
    threshold: ">= 95%"
  consistency:
    metric: "内部逻辑一致性"
    threshold: ">= 0.85"
  actionability:
    metric: "可操作性洞察占比"
    threshold: ">= 30% of insights have actionability >= 0.6"
  evidence_support:
    metric: "有证据支持的发现占比"
    threshold: ">= 80%"
```

---

## 5. 质量门控

### 5.1 方法级质量检查点

```yaml
quality_gates:
  analyze:
    gate_id: "QG-ANALYZE-001"
    checks:
      - id: "QAC-001"
        name: "输出完整性检查"
        condition: "structured_report.sections.length >= 1"
        severity: "blocking"
        message: "分析报告必须包含至少一个章节"
      - id: "QAC-002"
        name: "洞察质量检查"
        condition: "insights.length >= 1 AND insights.any(i => i.confidence >= 0.5)"
        severity: "blocking"
        message: "必须包含至少一个置信度>=0.5的洞察"
      - id: "QAC-003"
        name: "置信度合理性检查"
        condition: "confidence_scores.overall >= 0.3"
        severity: "warning"
        message: "整体置信度偏低，建议补充更多信息"
      - id: "QAC-004"
        name: "执行时间检查"
        condition: "execution_time_ms <= max_execution_time"
        severity: "warning"
        message: "分析耗时超出预期"
      - id: "QAC-005"
        name: "证据覆盖率检查"
        condition: "findings_with_evidence_ratio >= 0.7"
        severity: "warning"
        message: "超过30%的发现缺少证据支持"
      - id: "QAC-006"
        name: "内部一致性检查"
        condition: "no_contradictory_findings_in_report"
        severity: "blocking"
        message: "报告中存在自相矛盾的发现"

  extract_themes:
    gate_id: "QG-THEME-001"
    checks:
      - id: "QTC-001"
        name: "主题覆盖检查"
        condition: "primary_themes.length >= 1"
        severity: "blocking"
        message: "必须提取到至少一个主题"
      - id: "QTC-002"
        name: "权重合理性检查"
        condition: "sum(theme.weight for theme in primary_themes) <= 1.0"
        severity: "blocking"
        message: "主题权重总和不得超过1.0"
      - id: "QTC-003"
        name: "证据支撑检查"
        condition: "all themes have at least one evidence_span"
        severity: "warning"
        message: "部分主题缺少文本证据支撑"

  evaluate_significance:
    gate_id: "QG-SIG-001"
    checks:
      - id: "QSC-001"
        name: "评分范围检查"
        condition: "0.0 <= overall_score <= 1.0"
        severity: "blocking"
        message: "重要性评分必须在0-1范围内"
      - id: "QSC-002"
        name: "维度评分一致性"
        condition: "dimension_scores values correlate with overall_score"
        severity: "warning"
        message: "维度评分与综合评分存在显著偏差"
      - id: "QSC-003"
        name: "理由充分性"
        condition: "justification.length >= 50"
        severity: "blocking"
        message: "评分理由说明过于简略"

  get_analysis_dimensions:
    gate_id: "QG-DIM-001"
    checks:
      - id: "QDC-001"
        name: "维度完整性"
        condition: "dimensions.length >= 3"
        severity: "blocking"
        message: "领域引擎必须定义至少3个分析维度"
      - id: "QDC-002"
        name: "术语体系完整性"
        condition: "terminology.glossary.length >= 5"
        severity: "warning"
        message: "术语表条目过少，建议补充"
      - id: "QDC-003"
        name: "维度权重归一化"
        condition: "sum(dim.weight for dim in dimensions) <= 1.0"
        severity: "warning"
        message: "维度权重总和异常"

  cross_domain_bridge:
    gate_id: "QG-BRIDGE-001"
    checks:
      - id: "QBC-001"
        name: "连接有效性"
        condition: "connections.length >= 1"
        severity: "blocking"
        message: "必须建立至少一个跨领域连接"
      - id: "QBC-002"
        name: "桥接质量检查"
        condition: "bridge_quality.coherence_score >= 0.4"
        severity: "warning"
        message: "跨领域桥接的连贯性偏低"
      - id: "QBC-003"
        name: "双向性标注"
        condition: "all connections have bidirectional flag set"
        severity: "warning"
        message: "部分连接缺少双向性标注"
```

### 5.2 v2 Supervisor 集成

在 v2 中，领域引擎产出的质量门控通过 T15 任务的 [Supervisor Protocol](supervisors/supervisor_protocol.md) 检查执行。

```yaml
v2_supervisor_integration:
  task: "T15"
  supervisor_checks:
    - "activated_engines 包含 T01 推荐的全部引擎"
    - "每个引擎产出包含 analysis_framework"
    - "每个引擎产出包含 domain_controversies (≥2)"
    - "每个引擎产出包含 relevance_to_problem (≥2)"
    - "cross_domain_connections 非空"

  exhaust_retry_policy:
    reference: "exhaust-retry-protocol.md"
    max_retries: null  # EXHAUST 模式：不设重试上限，持续重试直至通过
    on_retrying: "注入修正指令，持续重试直至领域引擎分析通过"
```

### 5.3 质量门控执行流程

```yaml
quality_gate_execution:
  order: "post_processing"
  mode: "fail_fast_with_warnings"
  behavior:
    blocking_failure:
      action: "拒绝输出，返回错误详情和修正建议"
      retry_policy: "质量驱动持续重试（v2 QUALITY_DRIVEN），使用宽松阈值参数（仅在质量控制参数层面放宽，不降低分析深度）"
    warning:
      action: "允许输出，在结果中附加质量警告标签"
      notification: "记录到质量监控日志"
  reporting:
    format:
      type: QualityReport
      fields:
        gate_id:
          type: string
        passed:
          type: boolean
        checks_passed:
          type: integer
        checks_failed:
          type: integer
        warnings:
          type: array
          items:
            type: string
        score:
          type: float
          description: "综合质量评分 0-100"
```

---

## 6. 错误处理

### 6.1 错误类型体系

```yaml
error_hierarchy:
  base_error:
    name: DomainAnalysisError
    code_prefix: "DAP"
    fields:
      code:
        type: string
        pattern: "^DAP-E\\d{3}$"
      message:
        type: string
      detail:
        type: string
      timestamp:
        type: datetime
        format: "ISO 8601"
      domain:
        type: string
      method:
        type: string
      recoverable:
        type: boolean
      recovery_suggestion:
        type: string

  error_categories:
    input_errors:
      prefix: "DAP-E0XX"
      errors:
        - code: "DAP-E001"
          name: InvalidInputError
          severity: "high"
          recoverable: true
          description: "输入数据格式不符合规范"
        - code: "DAP-E002"
          name: DomainNotSupportedError
          severity: "high"
          recoverable: true
          description: "请求的领域不在支持范围内"
        - code: "DAP-E003"
          name: ComplexityOverflowError
          severity: "medium"
          recoverable: true
          description: "分析复杂度超出处理能力"
        - code: "DAP-E004"
          name: ContextConflictError
          severity: "medium"
          recoverable: true
          description: "上下文信息与分析内容冲突"

    execution_errors:
      prefix: "DAP-E1XX"
      errors:
        - code: "DAP-E100"
          name: AnalysisTimeoutError
          severity: "medium"
          recoverable: true
          description: "分析执行超时"
        - code: "DAP-E101"
          name: ResourceExhaustedError
          severity: "high"
          recoverable: true
          description: "计算资源不足"
        - code: "DAP-E102"
          name: EngineInternalError
          severity: "critical"
          recoverable: false
          description: "引擎内部错误"
        - code: "DAP-E103"
          name: PipelineFailureError
          severity: "high"
          recoverable: true
          description: "分析管道执行失败"

    output_errors:
      prefix: "DAP-E2XX"
      errors:
        - code: "DAP-E200"
          name: OutputFormatError
          severity: "medium"
          recoverable: true
          description: "输出格式不符合协议规范"
        - code: "DAP-E201"
          name: QualityGateFailureError
          severity: "high"
          recoverable: true
          description: "未通过质量门控检查"
        - code: "DAP-E202"
          name: ConfidenceTooLowError
          severity: "low"
          recoverable: true
          description: "分析结果置信度过低"

    bridge_errors:
      prefix: "DAP-E3XX"
      errors:
        - code: "DAP-E300"
          name: SameDomainError
          severity: "low"
          recoverable: true
          description: "源领域与目标领域相同"
        - code: "DAP-E301"
          name: BridgeNotSupportedError
          severity: "medium"
          recoverable: true
          description: "领域间不存在可建立的桥接"
```

### 6.2 恢复策略 (v2 适配)

```yaml
recovery_strategies:
  automatic_retry:
    trigger_conditions:
      - "错误代码以DAP-E1开头"
      - "recoverable == true"
    policy:
      max_retries: null  # EXHAUST 模式：不设重试上限，持续重试直至通过
      backoff: "exponential"
      base_delay_ms: 1000
      max_delay_ms: 10000
      jitter: true
      on_exhaustion: "持续重试，遵循 exhaust-retry-protocol.md（不存在放弃路径）"

  exhaust_continuation:
    trigger_conditions:
      - "DAP-E003 (AnalysisCapacityExceededError)"
      - "DAP-E100 (AnalysisTimeoutError)"
    policy:
      execution_continuation:
        description: "统一深度执行。超时或容量超出后标注穷尽重试信息继续交付，不降低分析深度。不存在'低一级复杂度'——所有分析始终执行完整深度研究。"
        annotation: "在输出中标注穷尽重试信息，下游按 exhaust-retry-protocol.md 处理"

  exhaust-retry_execution:
    trigger_conditions:
      - "DAP-E102 (EngineInternalError)"
    policy:
      exhaust_retry_to_generic: false
      annotation: "持续重试原领域引擎直至通过，不切换到通用引擎，不降低置信度"

  context_removal:
    trigger_conditions:
      - "DAP-E004 (ContextConflictError)"
    policy:
      action: "移除冲突的上下文信息"
      retry: true
      annotation: "记录被移除的上下文"

  error_propagation:
    policy:
      mode: "structured"
      format:
        type: ErrorReport
        fields:
          error_code:
            type: string
          error_message:
            type: string
          recovery_attempted:
            type: boolean
          recovery_result:
            type: enum
            values: [success, partial, failed]
          partial_results:
            type: object
          recommendations:
            type: array
            items:
              type: string
```

---

## 7. 领域外壳规范

### 7.1 外壳定义要求

每个领域引擎必须实现一个领域外壳（Domain Shell），定义该领域特有的分析能力。外壳是领域引擎的身份标识和能力声明。

```yaml
domain_shell_specification:
  version: "3.0"
  description: "领域外壳定义规范，每个领域引擎必须实现"

  required_components:

    analysis_dimensions:
      description: "该领域支持的所有分析维度"
      min_count: 3
      max_count: 15
      structure:
        type: array
        items:
          type: AnalysisDimension
          fields:
            id:
              type: string
              pattern: "^DIM-[A-Z]{2,4}-\\d{3}$"
            name:
              type: string
              max_length: 50
            description:
              type: string
              max_length: 200
            weight:
              type: float
              min: 0.0
              max: 1.0
            sub_dimensions:
              type: array
              max_items: 10
            evaluation_criteria:
              type: array
              min_items: 1
            data_requirements:
              type: array
          example:
            - id: "DIM-TECH-001"
              name: "技术可行性"
              description: "评估技术方案的可行性程度"
              weight: 0.25
              evaluation_criteria:
                - name: "成熟度"
                  scale: "likert_5"
                  benchmark: 3.0
                - name: "实现难度"
                  scale: "likert_5"
                  benchmark: 3.0

    evaluation_standards:
      description: "该领域的评估标准和基准值"
      structure:
        type: object
        fields:
          scoring_framework:
            type: string
            description: "评分框架名称"
          scales:
            type: array
            items:
              type: ScaleDefinition
              fields:
                name:
                  type: string
                type:
                  type: enum
                  values: [binary, ordinal, interval, ratio]
                levels:
                  type: array
                  items:
                    type: LevelDefinition
                    fields:
                      value:
                        type: number
                      label:
                        type: string
                      description:
                        type: string
                      range:
                        type: object
                        fields:
                          min:
                            type: number
                          max:
                            type: number
          benchmarks:
            type: object
            additional_properties:
              type: BenchmarkValue
              fields:
                value:
                  type: number
                source:
                  type: string
                last_updated:
                  type: datetime
                confidence:
                  type: float
          quality_thresholds:
            type: object
            fields:
              excellent:
                type: float
                default: 0.85
              good:
                type: float
                default: 0.7
              acceptable:
                type: float
                default: 0.5
              poor:
                type: float
                default: 0.3

    terminology_system:
      description: "该领域的专业术语定义和管理"
      structure:
        type: TerminologySystem
        fields:
          glossary:
            type: array
            min_items: 10
            items:
              type: TermDefinition
              fields:
                term:
                  type: string
                  required: true
                definition:
                  type: string
                  required: true
                  min_length: 10
                aliases:
                  type: array
                  items:
                    type: string
                related_terms:
                  type: array
                  items:
                    type: string
                domain_specific:
                  type: boolean
                  default: true
                usage_examples:
                  type: array
                  items:
                    type: string
                see_also:
                  type: array
                  items:
                    type: string
          abbreviations:
            type: object
            min_items: 5
            additional_properties:
              type: string
          units:
            type: array
            items:
              type: UnitDefinition
          classification_systems:
            type: array
            description: "领域内的分类体系"
            items:
              type: ClassificationSystem
              fields:
                name:
                  type: string
                categories:
                  type: array
                  items:
                    type: CategoryDefinition
                    fields:
                      id:
                        type: string
                      name:
                        type: string
                      description:
                        type: string
                      parent:
                        type: string

    domain_metadata:
      description: "领域引擎的基本信息"
      structure:
        type: DomainMetadata
        fields:
          domain_id:
            type: string
            pattern: "^(anthropology|architecture|art|business|cognitive-science|culture|data|design|diplomacy|economics|education|engineering|environment-climate|film|finance-quant|food|health|history|law|linguistics|literature|mathematics|media-communication|military|music|national-power|philosophy|political|psychology|religion|science|social|sports|tech|urban-planning)$"
          domain_name:
            type: string
          domain_name_en:
            type: string
          version:
            type: string
            pattern: "^\\d+\\.\\d+\\.\\d+$"
          protocol_version:
            type: string
            default: "9"
          capabilities:
            type: array
            items:
              type: enum
              values:
                - full_analysis
                - theme_extraction
                - significance_evaluation
                - cross_domain_bridging
                - real_time_analysis
                - batch_analysis
                - incremental_analysis
          supported_object_types:
            type: array
            items:
              type: enum
              values:
                - text_article
                - question
                - decision_scenario
                - dataset
                - code_snippet
                - multimedia
                - conversation
                - report
          performance_profile:
            type: object
            fields:
              avg_latency_ms:
                type: object
                additional_properties:
                  type: integer
                description: "深度分析的平均延迟"
              max_concurrent:
                type: integer
              memory_requirement_mb:
                type: integer
          known_limitations:
            type: array
            items:
              type: string
          changelog:
            type: array
            items:
              type: ChangelogEntry
              fields:
                version:
                  type: string
                date:
                  type: datetime
                changes:
                  type: array
                  items:
                    type: string
```

### 7.2 外壳注册流程 (v2 简化)

在 v2 中，外壳注册通过 T15 任务自动管理，流程如下：

```yaml
domain_shell_registration_v2:
  steps:
    - step: 1
      name: "外壳定义加载"
      description: "T15 Sub-Agent 加载所有领域引擎的外壳定义文件"
      location: "domains/*-engine.md"
      validation:
        - "所有必需组件均已定义"
        - "分析维度数量在3-15之间"
        - "术语表至少包含10个条目"
        - "所有ID符合命名规范"

    - step: 2
      name: "按需激活"
      description: "根据 T01.domain_engine_recommendations 选择性激活引擎"
      method: "仅激活推荐的引擎，不预加载全部35个引擎"

    - step: 3
      name: "分析执行"
      description: "每个激活的引擎独立执行 analyze() 方法"
      parallelism: "引擎间可并行执行"

    - step: 4
      name: "交叉验证"
      description: "对多引擎产出执行 cross_domain_bridge() 建立关联"
      output: "交叉领域关联图谱和矛盾点清单"
```

---

## 附录

### B. 术语表

| 术语 | 英文 | 定义 |
|------|------|------|
| 领域引擎 | Domain Engine | 负责特定领域分析的专业模块 |
| 领域外壳 | Domain Shell | 领域引擎的身份标识和能力声明 |
| 质量门控 | Quality Gate | 确保输出质量的自动化检查机制 |
| 跨领域桥接 | Cross-Domain Bridge | 不同领域分析结果之间的关联映射 |
| 置信度评分 | Confidence Score | 分析结果可靠性的量化评估 |
| 统一中间表示 | Unified Intermediate Representation | 标准化的数据交换格式 |

### C. 交叉引用

- [execution-protocol.md](./execution-protocol.md) — Phase 0-3 执行规则与 DAG 调度
- [handoff-protocol.md](./handoff-protocol.md) — Context Package 标准格式
- [exhaust-retry-protocol.md](./exhaust-retry-protocol.md) — 节点失败穷尽重试策略
- `supervisors/supervisor_protocol.md` — Supervisor 判定标准与宪法条款
- `tasks/T15_domain_analysis.md` — T15 领域引擎分析任务
- `tasks/T01_input_triage.md` — T01 输入分流（含 domain_engine_recommendations）

## 交叉引用

- [nrsf-protocol.md](./nrsf-protocol.md) — NRSF 叙事式研究状态文件协议
- [iterative-deepening-protocol.md](./iterative-deepening-protocol.md) — I01 迭代深化协议


---
© 阿洋

---

## 测试用例 (D3.4.4)

### 测试用例 1：领域引擎激活

**给定输入**：object_type=technology，主题为"大语言模型对就业市场的影响"。

**应产出**：激活 tech-engine（技术演化路径）+ economics-engine（劳动力市场）+ social-engine（社会变迁）+ psychology-engine（认知影响），输出领域引擎激活清单。

### 测试用例 2：跨领域冲突识别

**给定输入**：tech-engine 认为"AI 提升生产力"（正面），social-engine 认为"AI 加剧不平等"（负面）。

**应产出**：识别跨领域视角冲突，输出冲突描述 + 两个领域的证据等级 + 建议的综合结论方向。

### 测试用例 3：领域覆盖度检查

**给定输入**：研究报告涉及 8 个维度，但仅激活了 3 个领域引擎。

**应产出**：标注"领域覆盖度不足（3/8）"，列出未覆盖的维度对应的推荐领域引擎。
