> **作者**: 阿洋

# 输出渲染协议 (Output Rendering Protocol)

> > **状态**: 正式发布 (v2 适配)
> **适用范围**: Profound Cognition — 所有最终输出渲染
> **最后更新**: 2026-05-15

---

## 1. 协议概述

### 1.1 目的

OutputRenderingProtocol 定义了系统将内部结构化分析结果渲染为面向用户最终输出的统一接口标准。该协议确保：

- **一致性**: 所有输出遵循统一的格式规范和质量标准
- **多格式支持**: 支持渲染为多种格式（Markdown、纯文本等）
- **质量保证**: 通过质量门控确保输出满足用户需求
- **可追溯性**: 保留足够的元数据以支持输出溯源
- **内部标记剥离**: 用户看到的输出中不包含任何内部工作流程标记

### 1.2 v2 集成说明

在 Profound Cognition 中，输出渲染由 **[T20 输出渲染](tasks/T20a_research_render.md)** 作为 Phase 3 核心任务执行：

```
Phase 1 完成 (Gate-γ 通过)
  └── Phase 4 (输出渲染与交付层)
        └── T20 写作中补研 + 渲染 (Sub-Agent)
              ├── 加载 NRSF-Full + output-expansion-protocol + typography-guide
              ├── 逐章渲染 + 每章自检 + 按需补研
              ├── 执行 parse() → render() → export()
              ├── T20c 可访问性检查 + SHA-256 哈希
              └── 通过 Gate-终 (T28) 后交付用户
```

渲染上下文通过 [handoff-protocol.md](./handoff-protocol.md) 注入，包含上游全部产出摘要。

### 1.3 核心设计原则

- **用户视角优先**: 输出结构以用户需求为中心，符合UX自然语言交互规范
- **内容与格式分离**: 内部结构化数据与最终渲染格式完全解耦
- **渐进式渲染**: 支持从概要到详细的渐进式内容展开
- **品牌标识**: 输出中包含一致的品牌标识和信息
- **无障碍访问**: 输出兼容屏幕阅读器等辅助技术

### 1.3.1 §1-§8 全息框架结构约束

渲染必须严格遵循 §1-§8 全息框架结构，不得以"话题更适合自定义结构"为由替换：

| 章节 | 标题 | 字数下限 | 内容要求 |
|------|------|---------|---------|
| §1 | 问题认知与定义（4 维） | ≥8000 | 问题定义、边界界定、认知框架 |
| §2 | 全维全域分析（8 维） | ≥22000 | 多维度全覆盖分析 |
| §3 | 极限决策推理（2 维） | ≥8000 | 决策推理、极限情境 |
| §4 | 元层综合与跨维洞察 | ≥8000 | 跨维度综合、元层反思 |
| §5 | 科学深度层 | ≥30000 | 系统动力学/因果验证/多智能体对抗/情景规划/元认知/覆盖验证/本体导出 |
| §6 | 元维度扩展（9-14，6 维） | ≥12000 | 无知之学/认知神经心理学/二阶方法论/深度时间思维/悲剧性智慧/知识生命体化 |
| §7 | 哲学内核三元组 | ≥6000 | 哲学三元组深度审视 |
| §8 | 未来研究议程 | ≥6000 | 研究缺口、未来方向 |

**铁律**：§1-§8 的结构、章节语义、字数地板是不可变约束。无论研究话题是什么（商业/技术/社会/科学），都必须映射到这 8 部分结构中。渲染时须逐部分核对字数，任一部分未达标则退回补全。

### 1.4 协议层级架构

```
┌─────────────────────────────────────────────────┐
│ Phase 4 (输出渲染与交付层) -ORCHESTRATOR          │
├─────────────────────────────────────────────────┤
│ T20: OutputRender Sub-Agent (Sub-Agent)          │
│   ├── context_package (全流水线上游数据)         │
│   ├── parse()   → 解析上游输出数据               │
│   ├── render()  → 渲染为输出内容                 │
│   └── export()  → 导出最终格式                   │
├─────────────────────────────────────────────────┤
│ OutputRendering 协议层 (Protocol Layer)          │
│ Input Processing → Content Structuring →         │
│ Format Rendering → Quality Verification          │
├─────────────────────────────────────────────────┤
│ UIR v2.0 统一中间表示 (Unified Intermediate)     │
├─────────────────────────────────────────────────┤
│ 内部处理标记 (Internal Markers)                  │
└─────────────────────────────────────────────────┘
```

---

## 2. 核心方法定义

### 2.1 parse(internal_data) -> UIRDocument

解析系统内部工作流程中产生的结构化数据，将上下文、元数据、核心事实和结论转换为标准化的统一中间表示 (UIR) 文档对象。

```yaml
method: parse
version: "9"
description: |
 将来自工作台和分析引擎的内部数据解析为统一中间表示文档。
 此步骤负责**剥离所有内部标记**，只提取面向用户可展示的核心内容。

parameters:
  internal_data:
    type: InternalData
    required: true
    description: "系统内部工作流程生成的原始数据"
    fields:
      research_outline:
        type: object
        required: false
        description: "研究大纲框架"
      factual_checklist:
        type: array
        required: false
        description: "核心事实核查清单"
      cross_analysis:
        type: array
        required: false
        description: "跨领域分析结果"
      conflict_resolution:
        type: object
        required: false
        description: "冲突统一结论"
      research_data:
        type: object
        required: false
        description: "原始研究数据"
      thought_chain:
        type: array
        required: false
        description: "内部思维链数据"
      workbench_output:
        type: object
        required: false
        description: "工作台阶段输出"
      domain_engines_output:
        type: array
        required: false
        description: "领域引擎分析结果"

      metadata:
        type: MetaContext
        required: true
        description: "必要的上下文元数据"
        fields:
          user_original_question:
            type: string
            description: "用户原始提问内容"
          output_type:
            type: string
            description: "期望的成品类型"
          sensitivity_level:
            type: enum
            values: [low, medium, high, critical]
            description: "话题敏感性级别"
          reader_name:
            type: string
            description: "目标读者"
          domain_tags:
            type: array
            items:
              type: string
            description: "关联领域标签"

      quality_results:
        type: object
        required: false
        description: "质量门控检查结果"

  extraction_rules:
    type: ExtractionRules
    required: false
    default: "auto"
    description: "内容提取规则配置"
    fields:
      include_thought_chain:
        type: boolean
        default: false
        description: "内部标记不可在用户输出中可见"

return_value:
  type: UIRDocument
  description: "统一中间表示文档"
  fields:
    document_id:
      type: string
      pattern: "^UIR-[a-f0-9]{12}$"
    meta:
      type: DocumentMeta
      fields:
        title:
          type: string
        author:
          type: string
          default: "Profound Cognition | 阿洋"
        created_at:
          type: datetime
        version:
          type: string
        language:
          type: string
        output_type:
          type: string
        tags:
          type: array
          items:
            type: string
    abstract:
      type: string
      max_length: 300
      description: "文档摘要"
    sections:
      type: array
      items:
        type: UIRSection
        fields:
          id:
            type: string
          heading:
            type: string
          level:
            type: integer
            min: 1
            max: 6
          content:
            type: string
            description: "去掉所有内部标记的纯净内容"
          subsections:
            type: array
            items:
              type: UIRSection
          data_sources:
            type: array
            items:
              type: DataSource
              fields:
                id:
                  type: string
                source_type:
                  type: string
                url:
                  type: string
                title:
                  type: string
                access_date:
                  type: string
                excerpt:
                  type: string
                reliability:
                  type: float
                  min: 0.0
                  max: 1.0
          illustrations:
            type: array
            items:
              type: IllustrationReference
              fields:
                illustration_id:
                  type: string
                caption:
                  type: string
                alt_text:
                  type: string
                position:
                  type: enum
                  values: [top, bottom, inline, aside]
          confidence_indicator:
            type: float
            min: 0.0
            max: 1.0
            description: "此章节内容的置信度"
          factcheck_status:
            type: enum
            values: [verified, partially_verified, unverified, disputed]
    recommendations:
      type: UIRRecommendations
      fields:
        primary:
          type: array
          items:
            type: Recommendation
        alternatives:
          type: array
          items:
            type: Recommendation
        implementation_roadmap:
          type: string
          description: "实施路线图说明"
    references:
      type: array
      items:
        type: Reference
        fields:
          citation:
            type: string
          url:
            type: string
          type:
            type: enum
            values: [academic, news, official, industry, other]
          relevance:
            type: float

exceptions:
  - name: DataIntegrityError
    code: "ORP-E001"
    trigger: "内部数据关键字段缺失或损坏"
    recovery: "持续重试解析受损数据段直至成功，不设重试上限，不跳过受损数据段"
  - name: MarkersNotCleanError
    code: "ORP-E002"
    trigger: "输出内容中残留内部标记"
    recovery: "执行二次清理流程"
  - name: IncompleteDataError
    code: "ORP-E008"
    trigger: "上游节点 RETRYING 导致数据不完整"
    recovery: "标注数据缺口，降低对应章节置信度，参考 exhaust-retry-protocol.md"
  - name: ValidationError
    code: "ORP-E009"
    trigger: "输入数据不符合UIR规范"
    recovery: "记录错误详情，使用格式默认值填充（仅限格式字段，不涉及分析内容质量），持续重试直至输入数据符合规范"
```

### 2.2 render(uir_document, visual_dna) -> RenderedOutput

将统一中间表示文档渲染为面向用户的二维化成品内容。

> **visual_dna 注入路径说明**: `visual_dna` 对象作为 `render()` 方法的显式第二参数注入，由 `visual-dna.md` 生成、经 DLP 检索器（`dlp-retriever.md`）命中 DLP 后适配为 `design_tokens` 并由 Taste-Skill 仲裁后产出。`visual_dna` 携带配色方案（`color_scheme`）、字体方案（`font_scheme`）、栅格系统（`grid_system`）、线条样式（`line_style`）、动效配置（`motion_profile`）等视觉参数，渲染器消费这些参数生成符合品牌 DNA 的视觉输出。`visual_dna` 同时通过 `uir_document.meta` 字段冗余传递（作为 alternative_approach），确保渲染器在无法直接接收第二参数时仍可从 UIR 文档元数据中获取视觉参数。

```yaml
method: render
version: "9"
description: |
 将UIR文档渲染为面向用户的最终输出内容。
 根据文档的output_type自动选择最佳的渲染模板和规则。
 visual_dna对象作为显式第二参数注入，提供配色/字体/栅格/动效等视觉参数。

parameters:
  uir_document:
    type: UIRDocument
    required: true
    description: "统一中间表示文档（来自parse输出）"

  visual_dna:
    type: VisualDNA
    required: true
    description: "视觉DNA对象（来自visual-dna.md生成、DLP检索器适配、Taste-Skill仲裁），携带配色/字体/栅格/动效等视觉参数。同时通过uir_document.meta字段冗余传递作为alternative_approach。"
    fields:
      color_scheme:
        type: object
        description: "配色方案（来自DLP color_palette 6色板）"
      font_scheme:
        type: object
        description: "字体方案（来自DLP font_stack + typography_scale）"
      grid_system:
        type: object
        description: "栅格系统（来自DLP spacing_system + grid_system）"
      line_style:
        type: object
        description: "线条样式（来自DLP radius_shadow）"
      motion_profile:
        type: object
        description: "动效配置（来自DLP motion_curve）"
      dlp_anchor:
        type: string
        description: "DLP锚点名称（可追溯）"

  render_config:
    type: RenderConfig
    required: false
    default: "auto"
    fields:
      template:
        type: string
        description: "渲染模板名称"
        default: "auto_select"
      format:
        type: enum
        values: [markdown, plaintext, json_summary, html]
        default: "markdown"
        description: "目标输出格式"
      include_appendix:
        type: boolean
        default: true
        description: "是否包含附录"
      include_data_sources:
        type: boolean
        default: true
        description: "是否包含数据来源"
      include_confidence_scores:
        type: boolean
        default: true
        description: "是否包含置信度"
      include_recommendations:
        type: boolean
        default: true
        description: "是否包含建议"
      citation_style:
        type: enum
        values: [numbered, author_date, footnote, hyperlink]
        default: "numbered"
        description: "引用风格"
      heading_style:
        type: enum
        values: [markdown_hashes, markdown_underlines, numbered]
        default: "markdown_hashes"
      emoji_policy:
        type: enum
        values: [allow_all, minimal, none]
        default: "minimal"
        description: "Emoji使用策略"
      brand_policy:
        type: enum
        values: [full, minimal, none]
        default: "minimal"
        description: "品牌标识显示策略"
      quality_assurance:
        type: QAConfig
        fields:
          auto_bold_keywords:
            type: boolean
            default: true
          highlight_unsupported:
            type: boolean
            default: true
          version_watermark:
            type: boolean
            default: false

return_value:
  type: RenderedOutput
  fields:
    output_id:
      type: string
      pattern: "^RND-[a-f0-9]{12}$"
    title:
      type: string
    rendered_content:
      type: string
      description: "根据format参数的最终渲染内容"
    format:
      type: string
    template_used:
      type: string
    sections_count:
      type: integer
    word_count:
      type: integer
    estimated_reading_time_minutes:
      type: integer
    rendering_metadata:
      type: RenderingMetadata
      fields:
        render_time_ms:
          type: integer
        template_version:
          type: string
        simplification_level:
          type: float
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
  - name: RenderTemplateNotFoundError
    code: "ORP-E010"
    trigger: "指定的渲染模板不存在"
    recovery: "使用默认模板（default_report）渲染"
  - name: ContentOverflowError
    code: "ORP-E011"
    trigger: "渲染内容超出token限制"
    recovery: "分块渲染或执行精简策略"
```

### 2.3 export(rendered_output) -> FinalExport

导出渲染后的输出为最终交付格式。

```yaml
method: export
version: "9"
description: |
 将渲染后的输出导出为最终交付格式。
 负责添加品牌标识、版权信息、格式最终化等后处理。

parameters:
  rendered_output:
    type: RenderedOutput
    required: true
    description: "渲染后的输出内容（来自render输出）"

  export_config:
    type: ExportConfig
    required: false
    default: "standard"
    fields:
      target_format:
        type: enum
        values: [markdown, plaintext, json_summary, html, docx]
        default: "markdown"
        description: "目标输出格式；research_report 默认值覆盖为 docx"
        overrides:
          research_report:
            default: "docx"
            note: "research_report 默认导出为 .docx 格式，同时保留 .pdf"
      add_brand_header:
        type: boolean
        default: true
      add_brand_footer:
        type: boolean
        default: true
      include_disclaimer:
        type: boolean
        default: true
      include_copyright:
        type: boolean
        default: true
      include_step_indicators:
        type: boolean
        default: false
        description: "禁止显示内部工作流程步骤标记"

return_value:
  type: FinalExport
  fields:
    final_output:
      type: string
      description: "最终交付给用户的完整输出内容"
    metadata:
      type: ExportMetadata
      fields:
        version:
          type: string
        timestamp:
          type: datetime
        output_type:
          type: string
        format:
          type: string
        content_hash:
          type: string
          description: "内容哈希值，用于完整性验证"
    quality_assessment:
      type: QualityAssessment
      fields:
        overall_score:
          type: float
          min: 0.0
          max: 1.0
        completeness:
          type: float
        accuracy:
          type: float
        clarity:
          type: float
        actionability:
          type: float
        degradation_count:
          type: integer
          description: "RETRYING 上游节点数量"

exceptions:
  - name: ExportFormatError
    code: "ORP-E020"
    trigger: "导出过程中格式转换失败"
    recovery: "穷尽尝试所有可用格式"
  - name: ContentValidationError
    code: "ORP-E021"
    trigger: "导出内容验证未通过"
    recovery: "标注警告，允许导出"
```

### 2.4 beautify(rendered_output) -> EnhancedOutput

应用UX自然语言交互规范进行最终美学增强。

```yaml
method: beautify
version: "9"
description: |
 对最终输出内容进行美化增强，确保输出符合UX自然语言交互规范：
 加粗专业名词、添加适当的Emoji、确保格式整洁。

parameters:
  rendered_output:
    type: RenderedOutput
    required: true
    description: "渲染后的输出内容（来自render输出）"

  beautify_config:
    type: BeautifyConfig
    required: false
    default: "standard"
    fields:
      professional_terms_highlight:
        type: boolean
        default: true
        description: "是否加粗专业名词和关键结论"
      emoji_enhancement:
        type: boolean
        default: true
        description: "是否使用emoji增强可读性"
      typography_optimization:
        type: boolean
        default: true
        description: "是否优化排版"
      brand_identity:
        type: boolean
        default: true
        description: "是否保持品牌一致性"
      color_scheme:
        type: enum
        values: [none, monochrome, accent, full]
        default: "none"
        description: "色彩方案"

return_value:
  type: EnhancedOutput
  fields:
    enhanced_content:
      type: string
      description: "美化后的输出内容"
    enhancements_applied:
      type: array
      items:
        type: Enhancement
        fields:
          type:
            type: string
          description:
            type: string
          element_count:
            type: integer
    quality_score:
      type: float
      min: 0.0
      max: 1.0
      description: "美化后的UX质量评分"

exceptions:
  - name: BeautifyError
    code: "ORP-E030"
    trigger: "美化过程出现异常"
    recovery: "返回未经美化的原始渲染输出"
```

### 2.5 docx_export 配置

当 `target_format` 为 `docx` 时，系统按以下配置执行 Word (.docx) 导出。

```yaml
docx_export:
  version: "1.0"
  description: "Word (.docx) 导出配置，适用于 research_report 等需要可编辑文档的输出场景"
  applies_when: "export_config.target_format == 'docx'"

  primary_path:
    engine: "pandoc"
    command: "pandoc {input} -o {output}.docx --reference-doc=template.docx --toc --toc-depth=3"
    input_format: "markdown"
    input_source: "Step6 合并 Markdown 或 Step5 HTML+CSS"
    validation:
      - "docx 文件可被 Microsoft Word / LibreOffice Writer 正常打开"
      - "封面（标题/副标题/日期/作者/版本）完整"
      - "自动目录（TOC）≥3 级标题深度，页码正确"
      - "页眉页脚完整（页眉=短标题，页脚=页码+总页数）"
      - "所有图片以'图N'连续编号，无跳号"
      - "所有表格为中文学术三线表格式（顶线粗/栏目线细/底线粗/无竖线/无行线）"

  exhaust-retry_path:
    engine: "python-docx"
    library: "python-docx (pip install python-docx)"
    note: "pandoc CLI 不可用时，通过 python-docx 库程序化生成 .docx"
    trigger: "pandoc 不可用或 pandoc 转换失败"
    validation:
      - "docx 文件结构完整（可被 Word/LibreOffice 打开）"
      - "基本样式（标题层级、正文、表格）正确"
      - "封面要素完整"
      - "尝试自动生成目录（若 python-docx 版本支持）"

  degrade_path:
    engine: "md+guidance"
    output: "Markdown 文件 + pandoc 转换指南"
    note: "pandoc 和 python-docx 均不可用时的最终穷尽重试"
    trigger: "pandoc 不可用 且 python-docx 不可用"
    validation:
      - "Markdown 格式正确（标题层级、表格、列表、引用块）"
      - "指南包含完整的 pandoc 命令模板"
      - "指南包含参考模板（template.docx）说明"
      - "指南包含手动转换步骤（封面制作、目录生成、页码添加）"

  output_registration:
    final_deliverable: "report.docx"
    also_keep: "report.pdf"
    docx_path_used: "pandoc | python-docx | md+guidance"
    actual_rendering_chain: "Typst → WeasyPrint → {docx_path_used}"
```

---

## 3. UIR v2.0 规范

### 3.1 文档模型定义

```yaml
UIR_v2_specification:
  version: "2.0"
  description: "统一中间表示（Unified Intermediate Representation）用于表示从系统工作台提取的中间态输出。"
  revision_date: "2026-05-15"

  # === 根文档 ===
  root_document:
    type: UIRDocument
    required: true
    description: "UIR文档的根节点，代表整个分析输出。"
    fields:
      document_id:
        type: string
        required: true
      meta:
        type: DocumentMeta
        required: true
        description: "文档级别的元数据"
        fields:
          title:
            type: string
            required: true
            description: "输出文档的标题，由大纲步骤 T00 生成的 outline 中提取"
          author:
            type: string
            required: true
            default: "Profound Cognition | 阿洋"
            description: "文档作者信息，用于品牌标识"
          created_at:
            type: datetime
            format: "ISO 8601"
            description: "文档生成时间"
          version:
            type: string
            description: "生成的版本号"
          language:
            type: string
            description: "内容主语言"
          output_type:
            type: string
            required: true
            description: "从输入分流步骤 T01 中提取的最终输出类型"
          tags:
            type: array
            items:
              type: string
            description: "从工作台提取的领域标签及关键主题"

      abstract:
        type: string
        required: true
        max_length: 300
        description: "文档摘要，从研究结果和结论中提取生成的简短概述"

      sections:
        type: array
        required: true
        min_items: 1
        description: "文档主体，由大纲框架映射的各章节内容"
        items:
          type: UIRSection

      recommendations:
        type: UIRRecommendations
        required: false
        default: null
        description: "总结性推荐部分，仅在 original_question 需要建议时填充"

      references:
        type: array
        required: false
        default: []
        description: "数据引用聚合，从各章节中提取"
        items:
          type: Reference

      quality_annex:
        type: QualityAnnex
        required: false
        description: "内部质量评估附件（用户不可见），在 Phase 3 生成"
        fields:
          total_tasks:
            type: integer
          completed_tasks:
            type: integer
          retrying_tasks:
            type: integer
          degradation_details:
            type: array
            items:
              type: object
              fields:
                task_id:
                  type: string
                missing_content:
                  type: string
                impact:
                  type: string
          overall_confidence:
            type: float
            min: 0.0
            max: 1.0

  # === 章节 ===
  section:
    type: UIRSection
    description: "文档中的单个章节定义"
    fields:
      id:
        type: string
        required: true
        description: "章节唯一ID，如'SECTION_01', 'SECTION_03_SUB_02'格式"
      heading:
        type: string
        required: true
        description: "章节标题，从大纲继承"
      level:
        type: integer
        required: true
        min: 1
        max: 6
        description: "章节层级，1为最高级标题"
      content:
        type: string
        required: true
        description: "去除了内部标记的纯内容文本"
      subsections:
        type: array
        required: false
        default: []
        description: "子章节列表"
        items:
          type: UIRSection
      data_sources:
        type: array
        required: false
        default: []
        description: "本章节引用的数据源列表"
        items:
          type: DataSource
          fields:
            id:
              type: string
              required: true
            source_type:
              type: string
            url:
              type: string
            title:
              type: string
            access_date:
              type: string
            excerpt:
              type: string
            reliability:
              type: float
              min: 0.0
              max: 1.0
      illustrations:
        type: array
        required: false
        default: []
        description: "本章节所含插图列表"
        items:
          type: IllustrationReference
          fields:
            illustration_id:
              type: string
              required: true
            caption:
              type: string
            alt_text:
              type: string
            position:
              type: enum
              values: [top, bottom, inline, aside]
      confidence_indicator:
        type: float
        required: false
        min: 0.0
        max: 1.0
        description: "本章节内容的置信度评分"
      factcheck_status:
        type: enum
        required: false
        values: [verified, partially_verified, unverified, disputed]
        description: "本章节事实核查状态"

  # === 建议 ===
  recommendations:
    type: UIRRecommendations
    description: "综合建议部分"
    fields:
      primary:
        type: array
        items:
          type: Recommendation
          fields:
            title:
              type: string
            description:
              type: string
            priority:
              type: enum
              values: [immediate, short_term, medium_term, long_term]
            confidence:
              type: float
              min: 0.0
              max: 1.0
            supporting_evidence:
              type: array
              items:
                type: string
      alternatives:
        type: array
        items:
          type: Recommendation
      implementation_roadmap:
        type: string
        description: "实施路线图的文字描述"

  # === 引用 ===
  references:
    type: Reference
    description: "文档引用的外部来源"
    fields:
      citation:
        type: string
        description: "引用文本"
      url:
        type: string
        description: "来源链接"
      type:
        type: enum
        values: [academic, news, official, industry, other]
      relevance:
        type: float
        min: 0.0
        max: 1.0
```

### 3.2 内部标记剥离规则

```yaml
marker_stripping_rules:
  version: "2.0"
  description: "定义哪些内容必须在parse阶段被移除，确保用户永远看不到内部工作流程标记。"

  must_strip:
    internal_markers:
      - pattern: "T\\d{2}->"
        description: "任务ID前缀标记"
        example: "T01->初步判定输出类型为research_report"
        replace_with: "初步判定输出类型为research_report"

      - pattern: "T\\d{2}输出:"
        description: "任务输出标签"
        example: "T01输出: 经分析发现..."
        replace_with: "经分析发现..."

      - pattern: "\\[T\\d{2}.*?\\]"
        description: "方括号任务标记"
        example: "结论[T13已确认]已通过验证"
        replace_with: "结论已通过验证"

      - pattern: "^>>>.*?<<<$"
        description: "内部指令标记"
        example: ">>>开始执行T01任务<<<\n内容..."
        replace_with: "内容..."

    workflow_markers:
      - pattern: "Phase [0-3]"
        description: "阶段标记"
        replace_with: "依据上下文替换或移除"

      - pattern: "Gate-\\w"
        description: "门控标记"
        replace_with: "移除"

      - pattern: "\\[RETRYING:.*?\\]"
        description: "穷尽重试标记（内部用）"
        replace_with: "转为用户可读的穷尽重试说明"

    metadata_only_content:
      - pattern: "token_usage|execution_time|retry_count|confidence_scores_detail"
        description: "仅限元数据的内容"
        replace_with: "完全移除"

  preserve_but_rewrite:
    retrying_notices:
      description: "穷尽重试信息需要保留但改写为用户可读"
      example:
        input: "[RETRYING:T05] missing亚太数据"
        output: "注：此部分分析缺少亚太市场数据，结论需审慎参考"

    confidence:
      description: "置信度信息保留但统一格式"
      rewrite_rule: "整体置信度: {score}%。{uncertainty_note}"

  quality_assurance:
    post_strip_check:
      check: "搜索所有known_marker_patterns，确保输出中无残留"
      action: "发现残留标记→执行二次清理"
    counter_check:
      check: "比较剥离前后的文本长度"
      expected_range: "剥离后文本长度为剥离前的60-95%"
```

---

## 4. 格式规范

### 4.1 Markdown 格式

```yaml
markdown_format:
  version: "2.0"
  description: "Markdown格式的渲染规范"

  structure:
    brand_header:
      required: true
      template: |
        > **作者**: 阿洋
      position: "文档最顶部"
      spacing: "后跟一个空行"

    title:
      required: true
      template: "# {meta.title}"
      formatting: "一级标题，前后各一个空行"

    sections:
      hierarchy:
        level_1: "## {heading}"
        level_2: "### {heading}"
        level_3: "#### {heading}"
        level_4: "##### {heading}"
        level_5: "###### {heading}"
      spacing:
        before_heading: "一个空行"
        after_heading: "一个空行"
        between_paragraphs: "一个空行"

    emphasis:
      strong:
        marker: "**text**"
        usage: "加粗专业名词和关键结论"
      italic:
        marker: "*text*"
        usage: "强调次要概念"

    lists:
      unordered:
        marker: "- item"
        nesting_indent: "2 spaces per level"
      ordered:
        marker: "1. item"
        nesting_indent: "3 spaces per level"

    code_blocks:
      inline_code:
        marker: "`code`"
        usage: "行内代码、文件名、变量名"
      fenced_code:
        marker: "```language\ncode\n```"
        usage: "多行代码块"
        supported_languages:
          - python
          - javascript
          - typescript
          - bash
          - sql
          - yaml
          - json
          - text

    tables:
      required: true
      template: |
        | Header 1 | Header 2 | Header 3 |
        | -------- | -------- | -------- |
        | value    | value    | value    |

    blockquotes:
      marker: "> content"
      usage: "重要引用、注意事项、关键结论"

    horizontal_rules:
      marker: "---"
      usage: "在品牌标识与文档正文之间添加分隔线"

  illustrations:
    inline:
      template: "![{alt_text}]({illustration_id})"
    with_caption:
      template: "![{alt_text}]({illustration_id})\n*{caption}*"

  references:
    numbered:
      template: "[^{ref_id}]"
      footnote: "[^{ref_id}]: {citation}"
    hyperlink:
      template: "[{citation}]({url})"

  brand_footer:
    required: true
    template: "---\n© 阿洋"
    position: "文档最底部"

  special_elements:
    callout_boxes:
      syntax: "> **{type}**: {content}"
      types:
        - "重要"
        - "注意"
        - "警告"
        - "提示"
        - "结论"
    progress_indicators:
      syntax: "已分析：{ratio}"
      position: "引用章节底部"
```

### 4.2 纯文本格式

```yaml
plaintext_format:
  version: "2.0"
  description: "穷尽重试/备份时的纯文本渲染规范"

  structure:
    title:
      template: "{title}\n{'=' * len(title)}"
    sections:
      template: "{heading}\n{'-' * len(heading)}"
    emphasis:
      strong: "*text*"
      italic: "/text/"
    lists:
      marker: "- "
    horizontal_rules:
      marker: "---"

  notes:
    description: "用于无格式环境（如文本编辑器）。剥离所有装饰性元素，仅保留结构层次。"
```

### 4.3 JSON 摘要格式

```yaml
json_summary_format:
  version: "2.0"
  description: "用于程序化处理的结构化JSON格式"

  structure:
    type: object
    fields:
      document_id:
        type: string
      title:
        type: string
      author:
        type: string
      created_at:
        type: string
      output_type:
        type: string
      abstract:
        type: string
      sections:
        type: array
        items:
          type: object
          fields:
            heading:
              type: string
            level:
              type: integer
            content_summary:
              type: string
            confidence:
              type: float
            factcheck_status:
              type: string
      recommendations:
        type: array
        items:
          type: object
          fields:
            title:
              type: string
            description:
              type: string
            priority:
              type: string
            confidence:
              type: float
      references:
        type: array
        items:
          type: object
          fields:
            citation:
              type: string
            url:
              type: string
            type:
              type: string
      quality:
        type: object
        fields:
          overall_score:
            type: float
          completeness:
            type: float
          accuracy:
            type: float
```

---

## 5. 质量门控

### 5.1 方法级质量检查点

```yaml
quality_gates:
  parse:
    gate_id: "QG-PARSE-001"
    checks:
      - id: "QPC-001"
        name: "UIR文档完整性"
        condition: "uir_document.sections.length >= 1"
        severity: "blocking"
        message: "UIR文档必须包含至少一个章节"
      - id: "QPC-002"
        name: "标题完整性"
        condition: "uir_document.meta.title is not null and valid"
        severity: "blocking"
        message: "文档必须包含有效标题"
      - id: "QPC-003"
        name: "内部标记清理"
        condition: "no_internal_markers_found"
        severity: "blocking"
        message: "UIR文档中不得包含任何内部标记"
      - id: "QPC-004"
        name: "摘要完整性"
        condition: "uir_document.abstract.length >= 20"
        severity: "warning"
        message: "文档摘要过短"
      - id: "QPC-005"
        name: "章节内容完整性"
        condition: "all_sections_have_content"
        severity: "warning"
        message: "部分章节内容为空"
      - id: "QPC-006"
        name: "穷尽重试标注完整性"
        condition: "所有RETRYING节点在对应章节有标注"
        severity: "warning"
        message: "部分穷尽重试节点未在输出中标注"

  render:
    gate_id: "QG-RENDER-001"
    checks:
      - id: "QRC-001"
        name: "渲染内容完整性"
        condition: "rendered_content.length >= 100"
        severity: "blocking"
        message: "渲染内容长度不足"
      - id: "QRC-002"
        name: "品牌标识检查"
        condition: "brand_header_present"
        severity: "warning"
        message: "缺少品牌头部标识"
      - id: "QRC-003"
        name: "格式有效性"
        condition: "output is valid target_format"
        severity: "blocking"
        message: "渲染输出不是有效的目标格式"
      - id: "QRC-004"
        name: "章节计数一致性"
        condition: "sections_count matches uir_document.sections.length"
        severity: "blocking"
        message: "渲染后章节数量与UIR文档不一致"
      - id: "QRC-005"
        name: "内部标记残留"
        condition: "no_internal_markers_in_rendered"
        severity: "blocking"
        message: "渲染输出中残留内部标记"

  export:
    gate_id: "QG-EXPORT-001"
    checks:
      - id: "QEC-001"
        name: "最终输出非空"
        condition: "final_output.length >= 100"
        severity: "blocking"
        message: "最终输出内容长度不足"
      - id: "QEC-002"
        name: "内容哈希"
        condition: "content_hash is valid"
        severity: "blocking"
        message: "内容哈希生成失败"
      - id: "QEC-003"
        name: "声明完整性"
        condition: "disclaimer_present"
        severity: "warning"
        message: "缺少免责声明"

  beautify:
    gate_id: "QG-BEAUTIFY-001"
    checks:
      - id: "QBC-001"
        name: "美化有效性"
        condition: "enhanced_content is not null"
        severity: "blocking"
        message: "美化处理失败"
      - id: "QBC-002"
        name: "UX质量评分"
        condition: "quality_score >= 0.6"
        severity: "warning"
        message: "美化后的UX质量低于标准"
      - id: "QBC-003"
        name: "专业名词加粗"
        condition: "professional_terms_highlighted if enabled"
        severity: "warning"
        message: "专业名词加粗未完全应用"
      - id: "QBC-004"
        name: "内容完整性"
        condition: "no_content_loss_during_beautify"
        severity: "blocking"
        message: "美化过程中内容丢失"
```

### 5.2 v2 Gate-Final 集成

```yaml
gate_final:
  gate_id: "GATE-FINAL"
  description: "v2 Phase 3 终局门控，检查 T20 输出完整性"
  trigger: "T20 完成"
  checks:
    - id: "GF-001"
      name: "pre_render_actions完成"
      condition: "T20.pre_render_actions 全部为 true"
      severity: "blocking"
      message: "渲染前必须剥离内部标记"

    - id: "GF-002"
      name: "输出非空"
      condition: "T20.final_output 非空且长度合理"
      severity: "blocking"
      message: "最终输出不得为空"

    - id: "GF-003"
      name: "RETRYING标注"
      condition: "所有RETRYING节点在输出中有对应说明"
      severity: "warning"
      message: "部分穷尽重试信息未在最终输出中体现"

    - id: "GF-004"
      name: "品牌标识完整"
      condition: "brand_header和brand_footer存在"
      severity: "warning"
      message: "品牌标识不完整"
```

### 5.2.1 Gate-Final 升级为五维门禁审查器 + 熔断机制

```yaml
gate_final_v3:
  gate_id: "GATE-FINAL-V3"
  description: "Gate-Final 升级为五维门禁审查器 + 熔断机制，对接 Visual DNA 审美进化体系"
  trigger: "T20 完成（beautify 后、export 前）"
  version: "3.0"

  five_dimension_gates:
    - id: "FDG-001"
      name: "ASR 硬门检查"
      ref: "asr-hard-gate.md"
      description: "44 条禁令违反即拒"
      severity: "blocking"
      action_on_fail: "拒绝并触发重试"

    - id: "FDG-002"
      name: "Golden Set 距离校验"
      ref: "golden-set-validator.md"
      description: "距离 > 0.5 即拒"
      severity: "blocking"
      threshold: 0.5
      action_on_fail: "拒绝并触发重试"

    - id: "FDG-003"
      name: "五维门禁审查"
      ref: "taste-validator.md"
      description: "排版/审美/配图/语义一致性/品牌 DNA 一致性，任一维度未满分即打回"
      dimensions:
        - "排版"
        - "审美"
        - "配图"
        - "语义一致性"
        - "品牌 DNA 一致性"
      severity: "blocking"
      action_on_fail: "打回并触发重试"

    - id: "FDG-004"
      name: "熔断判定"
      ref: "fuse-mechanism.md"
      description: "持续重试直至通过，质量保持"
      max_retry: 3
      action_on_exceed: "持续重试直至通过，质量保持"

  execution_order:
    - "FDG-001 ASR 硬门检查"
    - "FDG-002 Golden Set 距离校验"
    - "FDG-003 五维门禁审查"
    - "FDG-004 熔断判定"
  note: "四步顺序执行，任一硬门失败即触发重试；持续重试直至通过，质量保持"
```

### 5.3 质量门控执行流程

```yaml
quality_gate_execution:
  pre_parse:
    - check: "输入数据完整性"
    - check: "RETRYING 节点清单"
  post_parse:
    - check: "内部标记剥离完成"
    - check: "UIR文档结构完整"
  post_render:
    - check: "格式有效性"
    - check: "品牌标识存在"
  post_export:
    - check: "Gate-Final 全部检查"
  mode: "fail_fast_on_blocking"
  exhaust_retry_integration:
    description: "RETRYING 节点信息通过 exhaust-retry-protocol.md 在各阶段被处理和标注"
```

### 5.4 质量门控新增（beautify 后、export 前）

在 beautify 阶段完成后、export 阶段开始前，强制执行以下门控链：

```yaml
post_beautify_pre_export_gate:
  gate_id: "QG-POST-BEAUTIFY-001"
  description: "beautify 后、export 前的强制门控链，对接 Visual DNA 审美进化体系"
  trigger: "beautify 阶段完成"
  position: "beautify 后、export 前"
  pass_condition: "门控链必须全部通过才能进入 export 阶段"
  fail_action: "触发重试，持续重试直至通过，质量保持"

  gate_chain:
    - step: 1
      name: "ASR 硬门"
      ref: "asr-hard-gate.md"
      rule: "违反即拒，触发重试"
      severity: "blocking"

    - step: 2
      name: "Golden Set 距离校验"
      ref: "golden-set-validator.md"
      rule: "FAIL 即拒，触发重试"
      severity: "blocking"

    - step: 3
      name: "五维门禁审查"
      ref: "taste-validator.md"
      rule: "任一维度未满分即打回，触发重试"
      dimensions:
        - "排版"
        - "审美"
        - "配图"
        - "语义一致性"
        - "品牌 DNA 一致性"
      severity: "blocking"

    - step: 4
      name: "熔断判定"
      ref: "fuse-mechanism.md"
      rule: "持续重试直至通过，质量保持"
      max_retry: 3
      severity: "blocking"

  execution_rule: "门控链必须全部通过才能进入 export 阶段"
```

---

## 6. TA 排版原子库对接

render 阶段从 TA 库（typography-atoms.md）检索排版原子：

- 字号阶梯 → TA-SCALE-001~008（中英文双轨）
- 字重搭配 → TA-WEIGHT-001~006
- 行高与字距 → TA-LEADING-001~003 + TA-TRACKING-001~003
- 段落排版 → TA-PARA-001~006
- 中西文混排 → TA-MIX-001~004

每个 TA 原子提供 CSS 和 Typst 双轨实现，render 阶段根据输出格式选择对应实现。

---

## 7. LA 布局原子库对接

render 阶段从 LA 库（layout-atoms.md）检索布局原子：

- 栅格布局 → LA-GRID-001~006（12 列/6 列/黄金分割/杂志双栏三栏/竖版卡片）
- 卡片布局 → LA-CARD-001~006
- 页面布局 → LA-PAGE-001~004
- 响应式布局 → LA-RESP-001~004
- 特殊布局 → LA-SPEC-001~004

每个 LA 原子提供 HTML+CSS 和 Typst 双轨实现，render 阶段根据输出格式选择对应实现。

---

## 附录

### B. 品牌元素规范

| 元素 | 规范 | 位置 |
|------|------|------|
| 作者标识 | `> **作者**: 阿洋` | 文档顶部 |
| 署名 | `---\n© 阿洋` | 文档底部 |
| 系统引用 | `Profound Cognition` | 会议记录/程序接口等必要场景 |
| 版本信息 | `Profound Cognition` | 内部日志/元数据 |

### C. 术语表

| 术语 | 英文 | 定义 |
|------|------|------|
| UIR | Unified Intermediate Representation | 统一中间表示，内部数据到用户输出的桥梁 |
| 内部标记 | Internal Marker | 系统工作流程中产生的任务ID、阶段标记等元数据 |
| 渲染 | Rendering | 将结构化数据转换为用户可读格式的过程 |
| 美化 | Beautify | 对输出内容进行UX优化的最终步骤 |
| Gate-Final | Gate-Final | v2 Phase 3 终局门控检查点 |

### D. 交叉引用 (v2)

- [execution-protocol.md](./execution-protocol.md) — v2 Phase 0-3 执行规则（含 ORCHESTRATOR 终局）
- [handoff-protocol.md](./handoff-protocol.md) — v2 Context Package 标准格式
- [exhaust-retry-protocol.md](./exhaust-retry-protocol.md) — v2 穷尽重试策略（RETRYING 节点终局标注）
- [illustration-generation-protocol.md](./illustration-generation-protocol.md) — v2 插图生成协议
- `supervisors/supervisor_protocol.md` — Supervisor 判定标准
- `tasks/T20a_research_render.md` — T20 输出渲染任务


---
© 阿洋