> **作者**: 阿洋

# 插图生成协议 (Illustration Generation Protocol)

> > **状态**: 正式发布 (v2 适配)
> **适用范围**: Profound Cognition — 所有插图生成模块
> **最后更新**: 2026-05-15

---

## 1. 协议概述

### 1.1 目的

IllustrationGenerationProtocol 定义了系统生成插图的统一接口标准。该协议确保：

- **策略一致性**: 所有插图生成遵循相同的策略选择流程
- **内容适配**: 插图类型与内容上下文智能匹配
- **领域感知**: 插图风格与领域特征保持一致
- **质量可控**: 通过统一质量门控确保插图质量
- **资源优化**: 根据不同平台和用途优化尺寸和格式

### 1.2 v2 集成说明

在 Profound Cognition 中，插图生成协议被以下任务引用：

| 任务 ID | 任务名称 | 引用方式 |
|---------|---------|---------|
| T20 | 输出渲染 | 按需调用插图策略，在 final_output 中嵌入插图 |

插图生成由 T20 任务在输出渲染阶段根据内容需要触发，上下文通过 [handoff-protocol.md](./handoff-protocol.md) 注入。

#### 1.2.1 Hook6 配图前自检规则

在生成每张插图之前，必须执行 Hook6 配图前自检，确保插图质量与必要性：

```yaml
hook6_self_check:
  name: "Hook6 配图前自检"
  description: |
    在生成每张插图（figure）之前，必须通过以下五项自检。
    自检不通过时，需按规则调整。

  checks:
    - id: "H6-001"
      question: "该插图是否必要？(Is this figure necessary?)"
      rationale: "避免为无意义内容生成装饰性插图"
      on_fail:
        action: "删除冗余插图"
        description: "若插图对内容理解无实质贡献，则不生成该插图（内容判断，非质量妥协）"

    - id: "H6-002"
      question: "该插图是否增强理解？(Does it enhance understanding?)"
      rationale: "插图应降低认知负担而非增加"
      on_fail:
        action: "调整或合并"
        description: "若插图无法有效增强理解，考虑调整类型或合并入其他插图"

    - id: "H6-003"
      question: "是否存在更优的插图类型？(Is there a better type?)"
      rationale: "确保所选插图类型与内容最适配"
      on_fail:
        action: "调整插图类型"
        description: "根据内容特征重新选择更优的插图类型"

    - id: "H6-004"
      question: "配图风格是否与当前 DLP 一致？(Does the figure style match the current DLP?)"
      rationale: "配图风格必须与当前 DLP（Dynamic Layout Profile）的 applicable_scenarios 字段匹配，确保视觉语言与版面策略一致"
      on_fail:
        action: "调整配图风格以匹配 DLP"
        description: "检查当前 DLP 的 applicable_scenarios 字段，将配图风格调整为对应族（academic-journal/interface-brand/publication-typesetting/data-visualization）的规范风格"

    - id: "H6-005"
      question: "配图分辨率是否达标？(Does the figure resolution meet the standard?)"
      rationale: "印刷场景分辨率 ≥ 300dpi，Web 场景宽度 ≥ 1920px，确保配图在不同交付场景下的清晰度"
      on_fail:
        action: "提升配图分辨率至标准"
        description: "印刷场景提升至 ≥ 300dpi，Web 场景提升至宽度 ≥ 1920px，矢量格式（SVG/PDF）天然满足印刷要求"

  execution_timing:
    description: "自检在 T27 可视化编排（visualization orchestration）之前执行"
    position: "before T27 visualization orchestration"

  failure_handling:
    strategies:
      - action: "adjust_figure_type"
        description: "调整为更适配的插图类型"
        trigger: "H6-003 不通过"
      - action: "merge_figures"
        description: "将多张低价值插图合并为一张综合插图"
        trigger: "H6-001 或 H6-002 不通过，且内容相关"
      - action: "delete_figure"
        description: "删除冗余或无效插图"
        trigger: "H6-001 不通过，且无法通过合并解决"
      - action: "adjust_style_to_dlp"
        description: "调整配图风格以匹配当前 DLP 的 applicable_scenarios"
        trigger: "H6-004 不通过"
      - action: "upgrade_resolution"
        description: "提升配图分辨率至印刷/Web 场景标准"
        trigger: "H6-005 不通过"
```

### 1.3 核心设计原则

- **内容优先**: 插图服务于内容，不做无意义的装饰
- **策略驱动**: 基于内容分析自动选择最优生成策略
- **可理解性**: 插图应提升内容的可理解性而非增加认知负担
- **多模态适配**: 支持图表、信息图、流程图等多种插图类型
- **渐进增强**: 基础图形到复杂可视化的渐进式生成

#### 1.3.1 插图类型 → 后端路由对照表

> 消费节点：T27（统一可视化编排）

| 插图类型 | 首选后端 | 穷尽尝试替代后端 |
|----------|---------|--------------|
| 柱/折/饼/散点 | ECharts(CLI) / Plotly | Mermaid |
| 声明式统计图 | Observable-Plot(CLI) | Mermaid |
| 流程/时序/状态 | Mermaid（全平台） | — |
| 思维导图 | Markmap(CLI) | Mermaid mindmap |
| 时间线 | vis-timeline / Mermaid timeline | — |
| 知识图谱 | d3-force / 图数据库+pyvis / Markmap | Mermaid graph |
| 学术图规范 | PubFig（matplotlib paper style） | — |
| 甘特 | tui.chart / Mermaid gantt | — |

---

## 2. 核心方法定义

### 2.1 analyze_content(content) -> ContentProfile

分析待插图的内容，生成内容画像。

```yaml
method: analyze_content
version: "3.0"
description: |
 分析文本内容的特征，为后续策略选择和生成提供决策依据。
 提取内容的复杂度、结构化程度、可视化需求等特征。

parameters:
  content:
    type: string
    required: true
    min_length: 50
    max_length: 50000
    description: "需要插图的内容文本"

  content_metadata:
    type: ContentMetadata
    required: false
    default: null
    fields:
      content_type:
        type: enum
        values:
          - research_report
          - educational_content
          - general_article
      domain:
        type: string
        description: "关联的领域引擎ID"
      reader_name:
        type: enum
        values: [general, technical, executive, academic, youth]
        default: "general"
      language:
        type: string
        default: "zh-CN"

return_value:
  type: ContentProfile
  fields:
    profile_id:
      type: string
      pattern: "^CP-[a-f0-9]{12}$"
    complexity_analysis:
      type: ComplexityAnalysis
      fields:
        overall_complexity:
          type: enum
          values: [simple, moderate, complex, highly_complex]
        data_density:
          type: float
          min: 0.0
          max: 1.0
          description: "数据密集度"
        concept_abstraction:
          type: float
          min: 0.0
          max: 1.0
          description: "概念抽象度"
        structural_clarity:
          type: float
          min: 0.0
          max: 1.0
          description: "结构清晰度"
    visualization_needs:
      type: VisualizationNeeds
      fields:
        needs_score:
          type: float
          min: 0.0
          max: 1.0
          description: "可视化需求程度"
        recommended_types:
          type: array
          items:
            type: enum
            values:
              - data_chart
              - process_flow
              - comparison_matrix
              - timeline
              - hierarchy_tree
              - concept_map
              - infographic
              - illustration
              - diagram
              - geographic_map
          description: "推荐的插图类型，按优先级排序"
        key_visual_points:
          type: array
          items:
            type: VisualPoint
            fields:
              content_span:
                type: string
                description: "原文中的关键段落"
              visual_type:
                type: string
                description: "最适配的视觉类型"
              rationale:
                type: string
              priority:
                type: enum
                values: [must_have, recommended, optional]
    content_structure:
      type: ContentStructure
      fields:
        sections:
          type: array
          items:
            type: SectionInfo
            fields:
              heading:
                type: string
              content_type:
                type: string
              visual_suitability:
                type: float
                min: 0.0
                max: 1.0
        data_elements:
          type: array
          items:
            type: DataElement
            fields:
              type:
                type: enum
                values: [statistical, comparative, temporal, hierarchical, relational, processual]
              content:
                type: string
              suggested_chart_type:
                type: string
              importance:
                type: float
    domain_context:
      type: DomainContext
      fields:
        domain_id:
          type: string
        style_preferences:
          type: array
          items:
            type: string
        common_visual_patterns:
          type: array
          items:
            type: string

exceptions:
  - name: ContentTooShortError
    code: "IGP-E001"
    trigger: "内容长度不足50字符"
    recovery: "返回最小化插图建议"
  - name: ContentNotVisualizableError
    code: "IGP-E002"
    trigger: "内容无法有效可视化（如纯哲学论述）"
    recovery: "返回抽象概念图策略和小幅降低的置信度"
```

### 2.2 select_strategy(profile) -> GenerationStrategy

根据内容画像选择最优的插图生成策略。

```yaml
method: select_strategy
version: "3.0"
description: |
 基于内容画像，从策略库中选择最适配的插图生成策略。
 考虑内容复杂度、领域特征、目标受众等因素。

parameters:
  profile:
    type: ContentProfile
    required: true
    description: "内容画像（来自analyze_content输出）"

  strategy_constraints:
    type: StrategyConstraints
    required: false
    default: null
    fields:
      max_illustrations:
        type: integer
        default: 10
        description: "质量驱动生成插图数量"
      preferred_types:
        type: array
        items:
          type: string
        default: []
        description: "偏好的插图类型（覆盖自动推荐）"
      exclude_types:
        type: array
        items:
          type: string
        default: []
        description: "排除的插图类型"
      color_palette:
        type: string
        description: "指定色彩方案"
      aspect_ratio:
        type: string
        pattern: "^\\d+:\\d+$"
        default: "16:9"
        description: "插图宽高比"

return_value:
  type: GenerationStrategy
  fields:
    strategy_id:
      type: string
      pattern: "^STR-[a-f0-9]{12}$"
    primary_strategy:
      type: StrategyItem
      fields:
        name:
          type: string
          description: "策略名称"
        description:
          type: string
        suitable_for:
          type: array
          items:
            type: string
        expected_quality:
          type: float
          min: 0.0
          max: 1.0
    illustration_plan:
      type: array
      items:
        type: IllustrationPlan
        fields:
          id:
            type: string
            pattern: "^ILL-[a-f0-9]{8}$"
          type:
            type: string
            description: "插图类型"
          title:
            type: string
          description:
            type: string
          placement:
            type: object
            fields:
              section:
                type: string
              position:
                type: enum
                values: [before, after, inline, standalone]
          data_source:
            type: string
            description: "数据来源"
          style_preset:
            type: string
          priority:
            type: enum
            values: [must_have, recommended, optional]
          estimated_complexity:
            type: enum
            values: [low, medium, high]
    style_guide:
      type: StyleGuide
      fields:
        color_palette:
          type: ColorPalette
          fields:
            primary:
              type: string
              pattern: "^#[0-9a-fA-F]{6}$"
            secondary:
              type: string
              pattern: "^#[0-9a-fA-F]{6}$"
            accent:
              type: string
              pattern: "^#[0-9a-fA-F]{6}$"
            background:
              type: string
              pattern: "^#[0-9a-fA-F]{6}$"
            text:
              type: string
              pattern: "^#[0-9a-fA-F]{6}$"
            palette_name:
              type: string
        typography:
          type: TypographyGuide
          fields:
            font_family:
              type: string
            title_size:
              type: string
            body_size:
              type: string
            label_size:
              type: string
        visual_style:
          type: enum
          values: [academic_journal, interface_brand, publication_typesetting, data_visualization]
          description: "由当前 DLP 的 applicable_scenarios 字段决定（详见 §4 DLP 驱动风格选择）"
        icon_style:
          type: enum
          values: [line, filled, flat, gradient, none]
        grid_style:
          type: enum
          values: [visible, subtle, hidden]
    resource_estimation:
      type: ResourceEstimation
      fields:
        total_illustrations:
          type: integer
        estimated_tokens:
          type: integer
        estimated_time_seconds:
          type: integer
        complexity_distribution:
          type: object
          properties:
            low:
              type: integer
            medium:
              type: integer
            high:
              type: integer

exceptions:
  - name: NoSuitableStrategyError
    code: "IGP-E010"
    trigger: "无法找到适配当前内容的策略"
    recovery: "返回通用策略，并降低质量预期"
  - name: ResourceInsufficientError
    code: "IGP-E011"
    trigger: "预估资源超出可用限额"
    recovery: "按优先级裁剪插图计划，优先生成must_have项"
```

### 2.3 generate(plan, strategy) -> IllustratedContent

根据策略和计划生成插图内容。

```yaml
method: generate
version: "3.0"
description: |
 根据选定的策略和插图计划，生成实际的插图内容。
 支持多种输出格式和渲染方式。

parameters:
  plan:
    type: IllustrationPlan
    required: true
    description: "插图生成计划（来自select_strategy输出）"

  strategy:
    type: GenerationStrategy
    required: true
    description: "生成策略（来自select_strategy输出）"

  generation_config:
    type: GenerationConfig
    required: false
    default:
      output_format: "svg"
      dpi: 150
      quality: "high"
    fields:
      output_format:
        type: enum
        values: [svg, png_base64, mermaid, plantuml, ascii, json_description, html_canvas]
        default: "svg"
        description: "输出格式"
      dpi:
        type: integer
        default: 150
        min: 72
        max: 300
        description: "分辨率（用于位图格式）"
      quality:
        type: enum
        values: [draft, standard, high, production]
        default: "high"
        description: "输出质量等级"
      max_width:
        type: integer
        default: 1200
        description: "最大宽度（像素）"
      max_height:
        type: integer
        default: 1600
        description: "最大高度（像素）"
      include_caption:
        type: boolean
        default: true
      include_source:
        type: boolean
        default: true
      watermark:
        type: object
        fields:
          enabled:
            type: boolean
            default: false
          text:
            type: string
          position:
            type: enum
            values: [top_left, top_right, bottom_left, bottom_right, center]
            default: "bottom_right"

return_value:
  type: IllustratedContent
  fields:
    illustrations:
      type: array
      items:
        type: Illustration
        fields:
          illustration_id:
            type: string
            pattern: "^ILL-[a-f0-9]{8}$"
          plan_id:
            type: string
            description: "对应的插图计划ID"
          type:
            type: string
          title:
            type: string
          caption:
            type: string
          alt_text:
            type: string
            description: "无障碍替代文本"
          content:
            type: string
            description: "根据output_format的实际插图内容"
          format:
            type: string
          dimensions:
            type: Dimensions
            fields:
              width:
                type: integer
              height:
                type: integer
              unit:
                type: string
                default: "px"
          file_size_bytes:
            type: integer
          quality_score:
            type: float
            min: 0.0
            max: 1.0
            description: "生成质量自评分"
          warnings:
            type: array
            items:
              type: string
          source_data:
            type: object
            description: "数据来源追溯"
    generation_metadata:
      type: GenerationMetadata
      fields:
        strategy_used:
          type: string
        generation_time_ms:
          type: integer
        total_tokens_used:
          type: integer
        success_rate:
          type: float
          description: "成功生成的插图比例"
    quality_report:
      type: GenerationQualityReport
      fields:
        overall_quality:
          type: float
          min: 0.0
          max: 1.0
        per_illustration_quality:
          type: array
          items:
            type: object
            fields:
              illustration_id:
                type: string
              score:
                type: float
              issues:
                type: array
                items:
                  type: string
        improvement_suggestions:
          type: array
          items:
            type: string

exceptions:
  - name: GenerationFailedError
    code: "IGP-E020"
    trigger: "单个插图生成失败"
    recovery: "持续重试该插图生成直至成功，不设重试上限，不跳过该插图"
  - name: FormatNotSupportedError
    code: "IGP-E021"
    trigger: "请求的输出格式不支持"
    recovery: "穷尽尝试所有可用格式（svg），并标注格式穷尽重试"
  - name: ContentTooComplexError
    code: "IGP-E022"
    trigger: "内容过于复杂，无法在单张插图中有效呈现"
    recovery: "拆分为多张子插图以完整呈现内容，不简化表示"
  - name: DataInsufficientError
    code: "IGP-E023"
    trigger: "数据不足以生成准确的数据图表"
    recovery: "生成带标注的完整图表，持续重试直至数据充足，不生成简化版"
```

### 2.4 adapt_format(illustration, target) -> AdaptedIllustration

将插图适配到不同的输出格式和平台。

```yaml
method: adapt_format
version: "3.0"
description: |
 将已生成的插图转换为目标平台所需的格式。
 支持格式转换、尺寸调整、质量优化等操作。

parameters:
  illustration:
    type: Illustration
    required: true
    description: "待转换的插图"

  target:
    type: FormatTarget
    required: true
    fields:
      platform:
        type: enum
        required: true
        values: [web, print, presentation, mobile, email, document, social_media, raw_text]
        description: "目标平台"
      format:
        type: enum
        values: [svg, png_base64, mermaid, plantuml, ascii, json_description, html_canvas]
        description: "目标格式"
      max_dimensions:
        type: Dimensions
        description: "目标尺寸限制"
      compression:
        type: object
        fields:
          enabled:
            type: boolean
            default: false
          level:
            type: enum
            values: [lossless, low, medium, high]
            default: "medium"
      responsive:
        type: boolean
        default: false
        description: "是否生成响应式变体"
      dark_mode:
        type: boolean
        default: false
        description: "是否为深色模式适配"

return_value:
  type: AdaptedIllustration
  fields:
    illustration_id:
      type: string
      description: "关联的原始插图ID"
    adapted_content:
      type: string
      description: "适配后的插图内容"
    format:
      type: string
      description: "目标格式"
    platform:
      type: string
      description: "目标平台"
    dimensions:
      type: Dimensions
    file_size_bytes:
      type: integer
    adaptations_applied:
      type: array
      items:
        type: Adaptation
        fields:
          type:
            type: enum
            values: [format_conversion, resize, compression, color_adjustment, dark_mode, simplification, annotation_addition]
          description:
            type: string
          quality_impact:
            type: float
            min: 0.0
            max: 1.0
            description: "质量影响程度"
    notes:
      type: array
      items:
        type: string
      description: "适配说明和注意事项"

exceptions:
  - name: AdaptationUnsupportedError
    code: "IGP-E030"
    trigger: "目标格式转换不支持"
    recovery: "返回最接近的支持格式"
```

---

## 3. 插图类型规范

### 3.1 支持的插图类型

```yaml
illustration_types:
  data_visualization:
    - type: "bar_chart"
      name: "柱状图"
      suitable_for: "分类数据对比"
      supported_formats: [svg, mermaid, png_base64, json_description]
      complexity: [low, medium]
    - type: "line_chart"
      name: "折线图"
      suitable_for: "趋势变化展示"
      supported_formats: [svg, mermaid, png_base64, json_description]
      complexity: [low, medium]
    - type: "pie_chart"
      name: "饼图"
      suitable_for: "占比分布展示"
      supported_formats: [svg, mermaid, png_base64, json_description]
      complexity: [low]
    - type: "radar_chart"
      name: "雷达图"
      suitable_for: "多维对比分析"
      supported_formats: [svg, mermaid, png_base64, json_description]
      complexity: [medium]
    - type: "scatter_plot"
      name: "散点图"
      suitable_for: "相关性分析展示"
      supported_formats: [svg, png_base64, json_description]
      complexity: [medium, high]
    - type: "heatmap"
      name: "热力图"
      suitable_for: "密度/强度分布展示"
      supported_formats: [svg, png_base64, json_description]
      complexity: [medium, high]
    - type: "waterfall_chart"
      name: "瀑布图"
      suitable_for: "累积效应展示"
      supported_formats: [svg, mermaid, json_description]
      complexity: [medium]
    - type: "gantt_chart"
      name: "甘特图"
      suitable_for: "时间线/项目管理"
      supported_formats: [svg, mermaid, json_description]
      complexity: [medium, high]

  structural_diagrams:
    - type: "flowchart"
      name: "流程图"
      suitable_for: "流程逻辑展示"
      supported_formats: [svg, mermaid, plantuml, json_description]
      complexity: [low, medium, high]
    - type: "hierarchy_tree"
      name: "层级树"
      suitable_for: "层级结构展示"
      supported_formats: [svg, mermaid, plantuml, json_description]
      complexity: [low, medium]
    - type: "mind_map"
      name: "思维导图"
      suitable_for: "发散思维组织"
      supported_formats: [svg, mermaid, json_description]
      complexity: [medium, high]
    - type: "venn_diagram"
      name: "韦恩图"
      suitable_for: "集合关系展示"
      supported_formats: [svg, json_description]
      complexity: [low, medium]
    - type: "swimlane_diagram"
      name: "泳道图"
      suitable_for: "跨职能流程展示"
      supported_formats: [svg, mermaid, plantuml]
      complexity: [medium, high]

  concept_illustrations:
    - type: "concept_map"
      name: "概念图"
      suitable_for: "概念关系展示"
      supported_formats: [svg, json_description]
      complexity: [medium, high]
    - type: "comparison_matrix"
      name: "对比矩阵"
      suitable_for: "多维度对比展示"
      supported_formats: [svg, mermaid, json_description]
      complexity: [low, medium]
    - type: "timeline"
      name: "时间线"
      suitable_for: "时间序列展示"
      supported_formats: [svg, mermaid, json_description]
      complexity: [low, medium]
    - type: "cycle_diagram"
      name: "循环图"
      suitable_for: "循环/迭代过程展示"
      supported_formats: [svg, mermaid, json_description]
      complexity: [low, medium]
    - type: "pyramid_diagram"
      name: "金字塔图"
      suitable_for: "层级/重要性展示"
      supported_formats: [svg, json_description]
      complexity: [low]
    - type: "funnel_diagram"
      name: "漏斗图"
      suitable_for: "转化/筛选过程展示"
      supported_formats: [svg, json_description]
      complexity: [low, medium]

  infographics:
    - type: "statistical_infographic"
      name: "统计信息图"
      suitable_for: "数据故事讲述"
      supported_formats: [svg, png_base64, json_description]
      complexity: [high]
    - type: "process_infographic"
      name: "流程信息图"
      suitable_for: "步骤/流程展示"
      supported_formats: [svg, json_description]
      complexity: [medium, high]
    - type: "comparison_infographic"
      name: "对比信息图"
      suitable_for: "方案A vs B展示"
      supported_formats: [svg, json_description]
      complexity: [medium, high]
    - type: "geographic_map"
      name: "地理分布图"
      suitable_for: "地理数据展示"
      supported_formats: [svg, json_description]
      complexity: [high]

  knowledge_graphs:
    - type: "knowledge_graph"
      name: "知识图谱"
      suitable_for: "实体关系、知识网络、概念关联展示"
      supported_formats: [svg, mermaid, json_description, html_canvas]
      complexity: [medium, high]
      backend_tools:
        primary: [mermaid_graph, markmap, d3_force, neo4j_pyvis]
        description: "Mermaid graph / Markmap / d3-force / 图数据库+pyvis"

  photos_and_realia:
    - type: "photo_realia"
      name: "实景/示意照片"
      suitable_for: "实景展示、场景示意、概念可视化"
      supported_formats: [svg, mermaid, json_description]
      complexity: [low, medium]
      backend_tools:
        primary: [inline_svg, mermaid_graph, observable_plot]
        description: "内联 SVG（手绘矢量）/ Mermaid graph / Observable Plot——代码生成图，完全自足，无 AI 生图 API 依赖"
      annotation: "code_generated"
      forbidden_backends: ["qwen_image", "flux", "stable_diffusion", "dall_e", "midjourney"]
      forbidden_note: "禁止使用任何 AI 生图 API，详见 illustration-generator.md §0 核心铁律"
```

### 3.2 类型选择决策树

```yaml
type_selection_decision_tree:
  condition_1:
    question: "内容是否包含定量数据？"
    yes_path:
      question: "数据的核心特征是什么？"
      answers:
        comparison: "柱状图 / 雷达图"
        proportion: "饼图 / 堆叠柱状图"
        trend: "折线图 / 面积图"
        correlation: "散点图 / 气泡图"
        distribution: "直方图 / 箱线图 / 热力图"
        cumulative: "瀑布图"
      condition: "数据点数量"
        gt_50: "自动穷尽重试为聚合图表"
        gt_200: "自动穷尽重试为统计摘要图"
    no_path:
      question: "内容的核心结构是什么？"
      answers:
        sequential: "流程图 / 时间线"
        hierarchical: "层级树 / 组织结构图"
        relational: "概念图 / 网络图"
        comparative: "对比矩阵 / 韦恩图"
        cyclical: "循环图"
        branching: "决策树 / 思维导图"

  complexity_adjustment:
    condition: "内容复杂度"
    logic: "复杂度越高，插图类型越偏向结构化（流程图/层级树）而非自由型（插图/信息图）"
```

---

## 4. DLP 驱动风格选择

> 本节原为 6 种静态风格预设（minimalist/corporate/academic/creative/technical/elegant），现已升级为 DLP（Dynamic Layout Profile）驱动的动态风格选择机制。配图风格不再由领域硬编码决定，而是由当前激活的 DLP 的 `applicable_scenarios` 字段动态决定，确保配图视觉语言与版面策略始终保持一致。

### 4.1 DLP 族 → 配图风格映射

配图风格由当前 DLP 的 `applicable_scenarios` 字段决定：

```yaml
dlp_driven_style_selection:
  description: |
    配图风格不再使用静态预设，而是由当前激活的 DLP（Dynamic Layout Profile）
    的 applicable_scenarios 字段动态决定。
    每个 DLP 族对应一套配图视觉规范，确保配图与版面策略一致。

  mapping:
    - dlp_family: "academic-journal"
      applicable_scenarios: ["学术论文", "期刊投稿", "学术报告"]
      figure_style: "学术配图风格"
      style_characteristics:
        format: "矢量图（SVG/PDF）"
        saturation: "低饱和"
        color_system: "专业色系（蓝/灰/黑为主）"
        typography: "Arial/Helvetica 无衬线，最小 7pt"
        grid: "细网格可见"
        decoration: "无装饰，信息密度优先"
      typical_elements:
        - "子图标注 a/b/c 加粗"
        - "图注位于图下方"
        - "误差线、显著性标注规范"
        - "颜色无障碍友好（通过色盲测试）"

    - dlp_family: "interface-brand"
      applicable_scenarios: ["产品文档", "品牌物料", "界面设计"]
      figure_style: "产品配图风格"
      style_characteristics:
        format: "SVG/PNG（高完成度）"
        saturation: "中饱和，品牌色驱动"
        color_system: "品牌主色 + 辅助色"
        typography: "品牌字体，标题/正文层级清晰"
        grid: "8pt 基线网格"
        decoration: "适度阴影/圆角，体现产品质感"
      typical_elements:
        - "品牌 Logo 占位"
        - "产品截图框/设备模型"
        - "品牌纹理背景（克制使用）"
        - "高完成度渲染"

    - dlp_family: "publication-typesetting"
      applicable_scenarios: ["杂志", "编辑排版", "长文专题"]
      figure_style: "杂志配图风格"
      style_characteristics:
        format: "SVG/PNG（编辑式）"
        saturation: "中高饱和，编辑色板"
        color_system: "编辑色板（暖灰 + 强调色）"
        typography: "衬线标题 + 无衬线正文，图文协调"
        grid: "栏宽对齐网格"
        decoration: "编辑式装饰，图文混排"
      typical_elements:
        - "图文协调的版式"
        - "引文/侧栏配图"
        - "章节头图"
        - "信息图与正文穿插"

    - dlp_family: "data-visualization"
      applicable_scenarios: ["数据报告", "仪表盘", "分析图表"]
      figure_style: "数据可视风格"
      style_characteristics:
        format: "SVG（矢量优先）"
        saturation: "低饱和，数据语义色"
        color_system: "数据语义色板（顺序/发散/分类）"
        typography: "无衬线，标签清晰"
        grid: "数据网格，轴线克制"
        decoration: "无冗余装饰，清晰克制"
      typical_elements:
        - "Tufte 原则：数据墨水比最大化"
        - "无 chartjunk"
        - "直接标注优于图例"
        - "色盲友好调色板"
```

### 4.2 DLP 风格选择决策流程

```yaml
dlp_style_decision_flow:
  step_1:
    action: "读取当前激活的 DLP"
    input: "DLP Profile（含 applicable_scenarios 字段）"
    output: "DLP 族标识（academic-journal / interface-brand / publication-typesetting / data-visualization）"

  step_2:
    action: "匹配 DLP 族 → 配图风格"
    input: "DLP 族标识"
    output: "配图风格规范（format/saturation/color_system/typography/grid/decoration）"
    rule: "严格按 §4.1 mapping 表映射，不允许跨族混用"

  step_3:
    action: "应用风格规范至插图计划"
    input: "配图风格规范 + IllustrationPlan"
    output: "带风格约束的 IllustrationPlan"
    note: "风格规范写入 style_guide.visual_style 字段"

  alternative_approach:
    trigger: "当前无激活 DLP 或 DLP 族无法识别"
    action: "默认使用 academic-journal 族配图风格（最保守、最通用）"
    warning: "标注 [DLP_ALTERNATIVE]，提示用户激活 DLP 以获得精准风格匹配"
```

### 4.3 与 Hook6 的联动

DLP 驱动风格选择与 Hook6 自检的 H6-004 检查项联动：

- **H6-004 检查逻辑**: 配图生成前，验证所选风格是否与当前 DLP 的 `applicable_scenarios` 匹配
- **不通过时**: 触发 `adjust_style_to_dlp` 策略，重新按 §4.1 mapping 表选择正确风格
- **DLP 缺失时**: 触发 alternative_approach 流程，使用 academic-journal 族默认风格并标注警告

---

## 5. 质量门控

### 5.1 方法级质量检查点

```yaml
quality_gates:
  analyze_content:
    gate_id: "QG-CONTENT-001"
    checks:
      - id: "QCC-001"
        name: "内容分析完整性"
        condition: "profile.complexity_analysis is not null"
        severity: "blocking"
        message: "必须完成复杂度分析"
      - id: "QCC-002"
        name: "可视化需求合理性"
        condition: "0 <= profile.visualization_needs.needs_score <= 1.0"
        severity: "blocking"
        message: "可视化需求评分必须在0-1之间"
      - id: "QCC-003"
        name: "推荐类型检查"
        condition: "profile.visualization_needs.recommended_types.length >= 1"
        severity: "warning"
        message: "应至少推荐一种插图类型"

  select_strategy:
    gate_id: "QG-STRATEGY-001"
    checks:
      - id: "QSC-001"
        name: "策略有效性"
        condition: "strategy.primary_strategy is not null"
        severity: "blocking"
        message: "必须选择有效的生成策略"
      - id: "QSC-002"
        name: "插图计划完整性"
        condition: "strategy.illustration_plan.length >= 1"
        severity: "blocking"
        message: "必须生成至少一个插图计划"
      - id: "QSC-003"
        name: "风格指南完整性"
        condition: "strategy.style_guide.color_palette is not null"
        severity: "blocking"
        message: "必须定义色彩方案"
      - id: "QSC-004"
        name: "资源合理性"
        condition: "strategy.resource_estimation.estimated_tokens <= token_budget"
        severity: "warning"
        message: "预估资源超出预算"

  generate:
    gate_id: "QG-GENERATE-001"
    checks:
      - id: "QGC-001"
        name: "插图生成率"
        condition: "generation_metadata.success_rate >= 0.7"
        severity: "blocking"
        message: "插图生成成功率应达到70%以上"
      - id: "QGC-002"
        name: "质量评分"
        condition: "quality_report.overall_quality >= 0.6"
        severity: "warning"
        message: "生成质量低于预期"
      - id: "QGC-003"
        name: "可访问性检查"
        condition: "all illustrations have alt_text"
        severity: "blocking"
        message: "所有插图必须包含替代文本"
      - id: "QGC-004"
        name: "尺寸合理性"
        condition: "all illustrations.dimensions within max limits"
        severity: "warning"
        message: "部分插图尺寸超出限制"

  adapt_format:
    gate_id: "QG-ADAPT-001"
    checks:
      - id: "QAC-001"
        name: "格式有效性"
        condition: "adapted_content is valid target_format"
        severity: "blocking"
        message: "转换后的内容必须是有效的目标格式"
      - id: "QAC-002"
        name: "质量损失限制"
        condition: "max quality_impact across all adaptations <= 0.3"
        severity: "warning"
        message: "格式转换导致的质量损失过大"
```

### 5.2 v2 集成

在 v2 中，插图生成作为 T20 输出渲染的组成部分，质量检查集成在 [Supervisor Protocol](supervisors/supervisor_protocol.md) 的 T20 检查中。

```yaml
v2_integration:
  task: "T20"
  illustration_role: "T20 在渲染阶段按需调用插图生成策略"
  supervisor_checks:
    - "插图类型与内容匹配"
    - "插图风格与输出类型一致"
    - "所有插图含替代文本"

  exhaust_retry_policy:
    reference: "exhaust-retry-protocol.md"
    on_generation_failed: "穷尽重试所有替代渲染引擎，最终使用 LLM 内建能力生成插图，标注 [INTERNAL_REASONING]"
    on_quality_low: "持续重试直至质量达标，不存在降低质量标准的路径"
```

### 5.3 质量门控执行流程

```yaml
quality_gate_execution:
  order: "inline_with_generation"
  mode: "collect_errors"
  behavior:
    per_illustration:
      on_pass: "正常交付"
      on_warning: "交付但附加质量标签"
      on_blocking: "持续重试直至配图生成成功，不设重试上限"
    overall:
      min_success_rate: 0.7
      on_below_threshold: "降低生成质量期望，优先交付高优先级插图"
```

---

## 6. 论文框架图生成工作流 (Paper Framework Figure Generation)

> 本节内容定义 内联 Mermaid/SVG 图生成 的 13 步子代理工作流（已合并自原 figure-generation-protocol.md）。

### 6.1 概述

论文框架图生成从 MD 图方案升级为 内联 Mermaid/SVG 图生成流程（自足）。核心目标：生成高质量、可迭代、符合学术规范的论文框架图和架构图。

### 6.2 13 步工作流

| 步骤 | 名称 | 输入 | 输出 | 判定规则 |
|------|------|------|------|---------|
| S0 | 启动 | NRSF-Full + output_type | 研究主题 + 图需求列表 | 研究主题明确则继续 |
| P1 | 材料导入 | NRSF-Full 对应 § 节 | 结构化材料摘要 | 材料充足则继续，不足则穷尽尝试回到 S0 补充 |
| P2 | 图需求诊断 | NRSF 内容 + output_type | 图类型列表 + 优先级 | 自动化模式：从 NRSF 内容 + output_type 自动推断 |
| P3 | 文本候选 | 图类型列表 | 每张图的文本描述 + 关系定义 | 文本描述完整则继续 |
| P4 | 候选图设置 | 文本描述 | 布局方案 + 样式参数 | 布局合理则继续 |
| P5 | 第一轮候选图 | 布局方案 + 样式参数 | 4-6 张候选图 | 图生成成功则继续 |
| P6 | 第一轮复盘 | 4-6 张候选图 | 评分 + 改进建议 | 自动化模式：LLM 判断选择 |
| P6b | 二轮优化 | 改进建议 | 优化后的图方案 | 方案可行则继续 |
| P6b-I | 二轮变体图 | 优化方案 | 2-3 张变体图 | 图生成成功则继续 |
| P6c | 二轮选择 | 变体图 | 最终图选择 | 自动化模式：LLM 判断选择 |
| P7 | 最终图 brief | 选定的图 | 完整图规格说明 | 规格完整则继续 |
| P8 | 正式生成 | 图规格说明 | 高质量最终图 | 图生成成功则继续 |
| P9 | 审稿式检查 | 最终图 + NRSF 内容 | 通过/不通过 | 通过则输出，不通过则穷尽尝试回到 P6b |

#### 各步骤详细说明

- **S0 启动**: 从 NRSF-Full 提取研究主题和核心论点，根据 output_type 确定图的风格和规范。
- **P1 材料导入**: 从 NRSF-Full 对应 § 节提取与图相关的材料（概念定义、关系描述、数据点、流程描述）。
- **P2 图需求诊断**: 分析 NRSF 内容确定图类型需求。图类型分类：概念框架图、架构图、因果回路图、时间线图、对比矩阵图、数据可视化图。自动化模式从 NRSF 内容 + output_type 自动推断。
- **P3 文本候选**: 为每张图编写文本描述，定义元素关系和层次结构。
- **P4 候选图设置**: 确定布局方案（层次/力导向/圆形/网格）和样式参数（颜色/字体/线型/节点形状）。
- **P5 第一轮候选图**: 生成 4-6 张候选图，使用多种布局和样式组合。
- **P6 第一轮复盘**: 评估候选图质量，评分维度：信息完整性、视觉清晰度、学术规范性、美观度。自动化模式由 LLM 选择最优 2-3 张。
- **P6b 二轮优化**: 根据改进建议调整布局、样式、元素位置。
- **P6b-I 二轮变体图**: 基于优化方案生成 2-3 张变体图，核心结构一致，细节调整。
- **P6c 二轮选择**: 从变体图中选择最终图，自动化模式由 LLM 判断。
- **P7 最终图 brief**: 编写完整图规格说明（标题、caption、legend、数据来源、尺寸、格式）。
- **P8 正式生成**: 按规格说明生成高质量最终图，输出 PNG（300dpi）+ SVG（矢量）。
- **P9 审稿式检查**: 检查图与 NRSF 内容一致性、学术规范性、caption/legend 完整性。不通过则穷尽尝试回到 P6b。

### 6.3 自动化模式规则

#### P2 图需求诊断自动化

从 NRSF 内容 + output_type 自动推断图需求：
- `research_report` → 至少 1 张概念框架图 + 至少 1 张数据可视化图
- `course_material` → 至少 1 张概念框架图
- `wechat_article` → 至少 1 张数据可视化图

#### P6/P6c 候选图选择自动化

LLM 判断选择最优候选图，判断标准：
1. 信息完整性（是否包含所有必要元素）
2. 视觉清晰度（元素是否可辨识）
3. 学术规范性（是否符合学术图规范）
4. 美观度（配色和布局是否协调）

### 6.4 图生成方式（默认自足，不依赖任何外部服务）

#### 默认主方式（强制）

在目标平台（Claude Code / Cursor / Trae / Codex）上，**直接在成品文件中写出 Mermaid 代码块或内联 SVG**，作为默认且强制的图生成方式——这些平台原生渲染 Mermaid/SVG，无需任何外部服务或额外技能。research_report 的强制配图（见 SKILL.md §0.1 D：≥⌈字数/3000⌉ 张、三类齐全）一律以此方式落地。

#### 可选增强（仅当对应能力可用时，且绝不阻塞配图）

```
Mermaid/SVG（默认 · 强制 · 自足） → 本地开源制图增强（可选） → 外部论文制图服务（可选）
```

- 若部署了外部论文制图服务/技能，可在 Mermaid/SVG 基础上做美化增强；
- 任何外部能力**不可用时一律回落到 Mermaid/SVG，绝不省略图**——"图生成失败/服务不可达"不是跳过配图的理由。

### 6.5 论文图生成方案矩阵

| 优先级 | 引擎 | 输出格式 | 自足性 |
|--------|------|---------|--------|
| **主方案（强制 · 默认）** | **Mermaid / 内联 SVG** | 矢量 / MD，平台原生渲染 | ✅ 完全自足，无需外部服务 |
| 可选开源增强 | 本地开源 Generator+Evaluator 制图 | SVG / draw.io | 需本地部署 |
| ~~可选服务增强~~ | ~~外部论文制图服务~~ | ~~PNG / SVG~~ | ~~需外部 API~~ **已废弃** |

> **PaperBanana 专有 API 废弃说明**: PaperBanana 原使用 Nano Banana Pro（Gemini 3 Pro Image）Google 专有 API 生成插图，违反"代码生成优先"原则，**已全面废弃**。所有原 PaperBanana 消费场景改为**代码生成**（内联 SVG / Mermaid / Canvas / Typst draw），由 LLM 直接书写代码生成顶刊级学术插图。详见 [illustration-generator.md §0 核心铁律](../output/illustration-generator.md)。

### 6.6 图与 NRSF 的交互

- **图需求来源**: P2 图需求诊断从 NRSF-Full 对应 § 节提取，图的内容必须与 NRSF 中的研究发现一致。
- **图产出记录**: 生成的图信息（标题、类型、caption、legend）记录在 NRSF §T20 下。图文件存储在 `output/{research_id}/figures/` 目录。
- **图引用标准**: 每张图必须有 caption（图标题）和 legend（图例说明）。caption 格式：`图 {N}: {标题} — {简短描述}`。legend 格式：说明图中各元素含义、数据来源、颜色编码。

---

## 7. PaperBanana 5 智能体流水线（v2.0 代码生成版）

> **来源技能**: PaperBanana Skill
> **融入目的**: 全类型学术配图质感统一，通过 5 智能体流水线确保配图质量闭环
> **v2.0 重构说明**: PaperBanana 原依赖 Google 专有 API（Nano Banana Pro / Gemini 3 Pro Image）生成插图，违反"代码生成优先"原则。现已重构为**纯代码生成**流水线——所有配图由 LLM 直接书写内联 SVG / Mermaid / Canvas / Typst draw 代码生成，**完全不依赖任何 AI 生图 API**。详见 [illustration-generator.md §0 核心铁律](../output/illustration-generator.md)。

融入 PaperBanana Skill 的 5 智能体流水线（v2.0 代码生成版），用于全类型学术配图质感统一：

```yaml
paperbanana_pipeline:
  description: |
    PaperBanana 5 智能体流水线（v2.0 代码生成版），用于全类型学术配图质感统一。
    每张学术配图均需经过 5 个智能体的完整流水线处理，
    确保配图从需求分析到最终精修的质量闭环。
    所有配图必须通过代码生成（内联 SVG / Mermaid / Canvas / Typst draw），
    禁止使用任何 AI 生图 API（Flux/SD/Qwen-Image/DALL-E/Midjourney/Nano Banana Pro/Gemini Image）。

  core_rules:
    rule_1: "代码生成优先——所有配图必须由 LLM 直接书写代码生成"
    rule_2: "禁止任何 AI 生图 API——Flux/SD/Qwen-Image/DALL-E/Midjourney/Nano Banana Pro/Gemini Image 一律禁用"
    rule_3: "矢量优先——输出 SVG/Mermaid 矢量格式，确保可缩放、可编辑"
    rule_4: "风格统一——通过 visual_dna CSS 变量注入配色/字体/线宽，禁止硬编码"

  agents:
    - id: "PB-AGENT-01"
      name: "analyze 智能体"
      role: "分析配图需求"
      responsibilities:
        - "分析配图需求，确定图表类型"
        - "识别数据类型（定量/定性/分类/时序）"
        - "确定目标期刊风格规范"
      input: "配图需求 + 内容上下文 + DLP 风格规范"
      output: "配图需求分析报告（图表类型/数据类型/目标期刊）"

    - id: "PB-AGENT-02"
      name: "plan 智能体"
      role: "规划配图布局与视觉方案"
      responsibilities:
        - "规划配图布局（子图排列/比例/留白）"
        - "制定配色方案（低饱和专业色系）"
        - "选择字体（Arial/Helvetica 无衬线）"
        - "选择代码生成方式（SVG/Mermaid/Canvas/Typst draw）"
      input: "配图需求分析报告"
      output: "配图规划方案（布局/配色/字体/代码生成方式）"

    - id: "PB-AGENT-03"
      name: "generate 智能体"
      role: "生成配图代码初稿"
      responsibilities:
        - "根据规划方案直接书写内联 SVG / Mermaid / Canvas / Typst draw 代码"
        - "输出矢量格式（SVG/PDF），确保矢量可缩放、可编辑"
        - "禁止调用任何 AI 生图 API"
        - "SVG 必须包含 viewBox、xmlns、role='img'、<title>、<desc> 无障碍标签"
      input: "配图规划方案"
      output: "配图代码初稿（SVG/Mermaid/Canvas/Typst draw 代码）"

    - id: "PB-AGENT-04"
      name: "review 智能体"
      role: "审查配图质量"
      responsibilities:
        - "审查配图代码是否符合学术出版规范"
        - "检查 Alt 文本完整性（SVG <title>/<desc>）"
        - "验证与正文协调性"
        - "检查是否使用了任何 AI 生图 API（必须为代码生成）"
      input: "配图代码初稿 + 正文内容"
      output: "配图审查报告（通过/不通过 + 改进建议）"

    - id: "PB-AGENT-05"
      name: "refine 智能体"
      role: "精修配图代码"
      responsibilities:
        - "根据审查反馈精修配图代码"
        - "调整细节至出版级质量"
        - "输出最终配图代码（出版级质量）"
      input: "配图代码初稿 + 审查报告"
      output: "最终配图代码（出版级质量）"

  flow: "analyze → plan → generate（代码生成）→ review → refine"
  retry_policy: "review 不通过时，回流至 generate 重新生成代码，穷尽重试直至 review 通过。禁止回落至 AI 生图 API。"
  forbidden_apis:
    - "Nano Banana Pro / Gemini 3 Pro Image"
    - "Flux.1 Dev / BFL API"
    - "Stable Diffusion / Stability AI API"
    - "Qwen-Image / DashScope 文生图"
    - "DALL-E 3 / OpenAI Images API"
    - "Midjourney / Imagine API"
    - "ComfyUI（自部署）"
    - "Replicate 图像生成 API"
```

### 7.1 与 §6 论文框架图工作流的关系

PaperBanana 5 智能体流水线（v2.0 代码生成版）是 §6 论文框架图生成工作流的**质量增强层**：

- §6 的 P5（第一轮候选图）→ 对应 PaperBanana generate 智能体（代码生成）
- §6 的 P6（第一轮复盘）→ 对应 PaperBanana review 智能体
- §6 的 P6b（二轮优化）→ 对应 PaperBanana refine 智能体
- §6 的 P2（图需求诊断）→ 对应 PaperBanana analyze 智能体
- §6 的 P4（候选图设置）→ 对应 PaperBanana plan 智能体

> **注意**: PaperBanana v2.0 已完全废弃 Google 专有 API（Nano Banana Pro / Gemini 3 Pro Image），改为**纯代码生成**方式。所有配图由 LLM 直接书写内联 SVG / Mermaid / Canvas / Typst draw 代码生成，绝不省略配图，绝不回落至 AI 生图 API。

---

## 8. Scientific Visualization 矢量图输出规则

> **来源技能**: Scientific Visualization Skill
> **融入目的**: 对齐 Nature/Science 绘图规范，确保学术配图达到顶刊出版标准

融入 Scientific Visualization 的 Nature/Science 绘图规范：

```yaml
scientific_visualization_rules:
  description: |
    Scientific Visualization 矢量图输出规则，对齐 Nature/Science 绘图规范。
    学术论文配图必须遵循以下规范，确保达到顶刊出版标准。

  rules:
    - id: "SV-R001"
      rule: "学术论文配图必须输出 SVG/PDF 矢量格式（非位图）"
      rationale: "矢量格式可无损缩放，满足印刷与屏幕双场景需求"
      enforcement: "blocking"

    - id: "SV-R002"
      rule: "印刷级分辨率 ≥ 300dpi"
      rationale: "Nature/Science 印刷要求最低 300dpi"
      enforcement: "blocking"
      note: "矢量格式（SVG/PDF）天然满足此要求；位图格式必须 ≥ 300dpi"

    - id: "SV-R003"
      rule: "字体使用 Arial/Helvetica（无衬线），最小字号 7pt"
      rationale: "Nature/Science 统一要求无衬线字体，7pt 为最小可读字号"
      enforcement: "blocking"

    - id: "SV-R004"
      rule: "子图标注 a/b/c 加粗"
      rationale: "子图标注加粗便于正文引用，Nature/Science 标准格式"
      enforcement: "blocking"

    - id: "SV-R005"
      rule: "图注在图下方"
      rationale: "图注统一置于图下方，符合学术出版惯例"
      enforcement: "blocking"

    - id: "SV-R006"
      rule: "颜色无障碍友好（通过色盲测试）"
      rationale: "确保色觉障碍读者可辨识，Nature 自 2020 起强制要求"
      enforcement: "blocking"
      test_tools: ["Coblis", "Sim Daltonism", "Color Oracle"]

  color_palette_recommendations:
    sequential: "Viridis / Plasma / Inferno（色盲友好顺序色板）"
    diverging: "RdBu / BrBG（色盲友好发散色板）"
    categorical: "Okabe-Ito 8 色色板（专为色盲设计）"
    avoid: "红绿对比（约 8% 男性色盲无法区分）"
```

### 8.1 与 Hook6 H6-005 的联动

Scientific Visualization 矢量图输出规则与 Hook6 的 H6-005 检查项联动：

- **H6-005 检查逻辑**: 配图分辨率是否达标（印刷 ≥ 300dpi，Web ≥ 1920px）
- **矢量格式优先**: SVG/PDF 矢量格式天然满足印刷分辨率要求
- **位图兜底**: 当必须使用位图时，强制 ≥ 300dpi（印刷）/ ≥ 1920px（Web）

---

## 9. Scientific Image Prompting 图形摘要专用流程

> **来源技能**: Scientific Image Prompting Skill
> **融入目的**: 为学术论文生成图形摘要（Graphical Abstract）和机制示意图，提升论文可发现性与可理解性

融入 Scientific Image Prompting 的图形摘要/机制示意图能力：

```yaml
scientific_image_prompting_flow:
  description: |
    Scientific Image Prompting 图形摘要专用流程。
    为学术论文自动生成图形摘要和机制示意图，
    提升论文可发现性（视觉吸引）与可理解性（流程可视化）。

  graphical_abstract:
    trigger: "§1 摘要部分自动生成 1 张图形摘要（Graphical Abstract）"
    style: "简约克制，匹配正刊调性"
    purpose: "一图概括论文核心发现，吸引读者阅读全文"
    count: "每篇论文 1 张图形摘要"
    placement: "置于摘要之后、正文之前"

  mechanism_diagram:
    purpose: "解释复杂流程，使用箭头+图标+标签"
    elements:
      - "箭头：表示流程方向/因果关系"
      - "图标：表示关键实体/组件"
      - "标签：标注关键参数/状态"
    style: "清晰、简洁、可读性优先"
    count: "按需生成，每张聚焦一个核心机制"

  size_specifications:
    single_column: "89mm（单栏宽度）"
    double_column: "183mm（双栏宽度）"
    note: "图形摘要尺寸根据期刊要求选择单栏或双栏"

  generation_flow:
    step_1: "分析摘要内容，提取核心发现和关键概念"
    step_2: "确定图形摘要布局（单栏/双栏）"
    step_3: "生成图形摘要初稿（简约克制风格）"
    step_4: "审查与正刊调性一致性"
    step_5: "精修输出（SVG 矢量格式）"
```

### 9.1 图形摘要与 DLP 的联动

- **academic-journal 族 DLP**: 图形摘要强制生成，风格匹配期刊调性
- **data-visualization 族 DLP**: 图形摘要以数据可视为核心，突出关键数据点
- **其他族 DLP**: 按需生成图形摘要，不强制

---

## 10. VCA 原子库对接规则

> **来源**: VCA（Visual Creative Atoms）原子库 — `visual-creative-atoms.md`
> **融入目的**: 配图生成时从 VCA 库检索匹配的艺术流派风格，确保视觉风格有据可依、可复用

配图生成时从 VCA 库（visual-creative-atoms.md）检索匹配的艺术流派风格：

```yaml
vca_integration_rules:
  description: |
    VCA 原子库对接规则。配图生成时从 VCA 库（visual-creative-atoms.md）
    检索匹配的艺术流派风格，确保视觉风格有据可依、可复用、可追溯。
    每个 VCA 原子定义了一种经过验证的视觉风格规范，
    配图生成时按内容类型检索并应用对应 VCA 原子。

  mapping:
    - content_type: "技术文章封面图"
      vca_atoms:
        primary: "VCA-ART-003 瑞士风格"
        secondary: "VCA-ART-005 包豪斯"
      style_characteristics: "网格驱动、信息层级清晰、无衬线字体"
      retrieval_rule: "技术文章封面优先检索 VCA-ART-003，备选 VCA-ART-005"

    - content_type: "数据可视配图"
      vca_atoms:
        primary: "VCA-DATA-001 经济学人风格"
        secondary: "VCA-DATA-006 Distill 风格"
      style_characteristics: "克制配色、直接标注、高数据墨水比"
      retrieval_rule: "数据可视配图优先检索 VCA-DATA-001，备选 VCA-DATA-006"

    - content_type: "品牌视觉元素"
      vca_atoms:
        primary: "VCA-BRAND-001 Logo 占位"
        secondary: "VCA-BRAND-003 品牌纹理"
      style_characteristics: "品牌色驱动、一致性优先"
      retrieval_rule: "品牌视觉元素优先检索 VCA-BRAND-001，备选 VCA-BRAND-003"

    - content_type: "生成式艺术背景"
      vca_atoms:
        primary: "VCA-GEN-001 流场"
        secondary: "VCA-GEN-004 Perlin 噪声"
      style_characteristics: "算法生成、有机纹理、低饱和"
      retrieval_rule: "生成式艺术背景优先检索 VCA-GEN-001，备选 VCA-GEN-004"

  retrieval_flow:
    step_1: "识别配图内容类型（技术封面/数据可视/品牌视觉/生成式艺术）"
    step_2: "按 mapping 表检索对应 VCA 原子"
    step_3: "加载 VCA 原子的风格规范（配色/字体/布局/装饰）"
    step_4: "将 VCA 风格规范注入 IllustrationPlan 的 style_guide"
    step_5: "按注入的风格规范生成配图"

  alternative_approach:
    trigger: "VCA 原子库不可用或无匹配原子"
    action: "回落至 §4 DLP 驱动风格选择，使用 DLP 族默认风格"
    warning: "标注 [VCA_ALTERNATIVE]，提示 VCA 原子库未命中"
```

### 10.1 VCA 原子库与 DLP 的优先级关系

当 VCA 原子库与 DLP 风格规范同时存在时，遵循以下优先级：

1. **VCA 原子库优先**: 若 VCA 原子库命中匹配原子，使用 VCA 原子的风格规范（更精细、更专业）
2. **DLP 兜底**: 若 VCA 原子库未命中，回落至 DLP 驱动风格选择（§4）
3. **Hook6 校验**: 无论使用 VCA 还是 DLP 风格，均需通过 H6-004 风格一致性检查

---

## 附录

### B. 术语表

| 术语 | 英文 | 定义 |
|------|------|------|
| 内容画像 | Content Profile | 对内容特征的结构化分析结果 |
| 生成策略 | Generation Strategy | 根据内容特征选择的最优插图生成方案 |
| DLP 驱动风格选择 | DLP-Driven Style Selection | 由当前 DLP 的 applicable_scenarios 字段动态决定配图风格的机制（替代原静态风格预设） |
| VCA 原子库 | Visual Creative Atoms Library | 经过验证的视觉风格规范库（visual-creative-atoms.md），配图生成时按内容类型检索匹配原子 |
| PaperBanana 流水线 | PaperBanana 5-Agent Pipeline (v2.0 Code-First) | 5 智能体（analyze/plan/generate/review/refine）学术配图质量闭环流水线（**v2.0 代码生成版**，原专有 API 已废弃，所有配图由 LLM 直接书写代码生成） |
| 图形摘要 | Graphical Abstract | 一图概括论文核心发现的视觉摘要，置于摘要之后正文之前 |
| 矢量图输出规范 | Vector Output Standard | Nature/Science 绘图规范，要求 SVG/PDF 矢量格式、≥300dpi、无衬线字体、色盲友好 |

### C. 交叉引用 (v2)

- [execution-protocol.md](./execution-protocol.md) — v2 Phase 0-3 执行规则
- [handoff-protocol.md](./handoff-protocol.md) — v2 Context Package 标准格式
- [exhaust-retry-protocol.md](./exhaust-retry-protocol.md) — v2 穷尽重试策略
- [output-rendering-protocol.md](./output-rendering-protocol.md) — v2 输出渲染协议
- `tasks/T20a_research_render.md` — T20 研究报告渲染任务

## 交叉引用

- [§4 DLP 驱动风格选择](#4-dlp-驱动风格选择) — 由 DLP applicable_scenarios 字段动态决定配图风格（替代原 6 种静态预设）
- [§6 论文框架图生成工作流](#6-论文框架图生成工作流-paper-framework-figure-generation) — 内联 Mermaid/SVG 图生成 子代理协议（已合并入本文档）
- [§7 PaperBanana 5 智能体流水线](#7-paperbanana-5-智能体流水线) — 来源：PaperBanana Skill（**v2.0 代码生成版**，原专有 API 已废弃），5 智能体学术配图质量闭环（代码生成）
- [§8 Scientific Visualization 矢量图输出规则](#8-scientific-visualization-矢量图输出规则) — 来源：Scientific Visualization Skill，Nature/Science 绘图规范
- [§9 Scientific Image Prompting 图形摘要专用流程](#9-scientific-image-prompting-图形摘要专用流程) — 来源：Scientific Image Prompting Skill，图形摘要/机制示意图
- [§10 VCA 原子库对接规则](#10-vca-原子库对接规则) — 来源：VCA 原子库（visual-creative-atoms.md），艺术流派风格检索
- [nrsf-protocol.md](./nrsf-protocol.md) — NRSF 叙事式研究状态文件协议


---
© 阿洋


---

## 测试用例 (D3.4.4)

### 测试用例 1：图表类型选择

**给定输入**：研究报告中需要展示"全球 GDP 增长率 2010-2025 时间序列"。

**应产出**：选择折线图（时间序列数据），标注 x 轴=年份、y 轴=GDP 增长率，生成 Mermaid 或 ECharts 代码。

### 测试用例 2：Penrose 因果回路图生成

**给定输入**：TM01 系统动力学产出包含增强回路 R1（投资→产能→收入→投资）。

**应产出**：生成 Penrose DSL 代码，包含 R1 节点和正反馈边，标注回路类型为"增强回路"。

### 测试用例 3：图表质量检查

**给定输入**：生成的图表缺少标题、轴标签和图例。

**应产出**：质量检查失败，标注"缺少 title/x_label/y_label/legend"，触发重试。
