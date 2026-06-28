---
name: qwen-image-adapter
description: 代码生成图适配器 — 以 SVG/Mermaid/Canvas/CSS/Typst 代码生成图像
author: 阿洋
tags: [code-first, image, adapter, svg, mermaid]
---

<!-- 作者：阿洋 -->

# Code-First Image Adapter — 代码生成图适配器

> **v2.0 重构说明**: 本适配器原为 Qwen-Image 文生图 API 适配器，已彻底重构为代码生成图适配器。
> 重构动机：用户明确要求"大多数时候图片应该用代码生成，而非用API"，且已引入大量开源渲染项目（sci-paper-writing / Nature Skills / Quarkdown / Rxiv-Maker / Scientific Visualization / PaperBanana / SciencePlots / Plotivy / Impeccable / garden-skills / editorialTypesetting / slidecraft / typography-master / Kami / guizang-social-card / techarticleimage / algorithmic-art / data-visualization-craft / brand-identity）以摆脱生图 API 依赖。
> 本适配器现以 SVG / Mermaid / Canvas / CSS / Typst 绘图代码为唯一图像生成方式，**完全禁用** Flux / Stable Diffusion / Qwen-Image / DALL-E / Midjourney 等所有 AI 生图 API。

## 适配器配置

- role: 代码生成图引擎，用于生成概念插图、信息图、装饰图、品牌视觉元素
- model: 无（纯代码生成，无外部 API 依赖）
- endpoint: 无（本地代码生成）
- 自足性: ✅ 完全自足，无需任何外部服务或 API 密钥

## §0 核心铁律

```yaml
core_principles:
  rule_1: "代码生成优先——所有图像必须通过 SVG / Mermaid / Canvas / CSS / Typst draw 代码生成"
  rule_2: "禁止任何 AI 生图 API——Flux / SD / Qwen-Image / DALL-E / Midjourney 一律禁用"
  rule_3: "矢量优先——SVG / Mermaid 矢量格式为首选，确保印刷级清晰度"
  rule_4: "风格统一——所有生成图必须遵循当前 DLP（Dynamic Layout Profile）的视觉规范"
  rule_5: "VCA 对接——生成图必须从 VCA 原子库检索匹配的艺术流派风格"

forbidden_apis:
  - "Flux.1 Dev"
  - "Stable Diffusion (SD 1.5 / SDXL / SD 3.5)"
  - "Qwen-Image / qwen-image-max"
  - "DashScope 文生图 API"
  - "DALL-E 2 / DALL-E 3"
  - "Midjourney"
  - "ComfyUI API"
  - "Replicate 图像生成 API"
  - "Stability AI API"
  - "任何形式的 AI 文生图 / 图生图 API"
```

## §1 代码生成图优先级链

```yaml
code_first_priority_chain:
  L1_SVG_INLINE:
    description: "内联 SVG——首选方式，矢量可缩放，平台原生渲染"
    use_cases: ["概念图", "信息图", "对比图", "流程图", "知识图谱", "时间线", "决策路径图"]
    advantages: ["完全自足", "矢量无损", "可编程控制", "支持 CSS 动画"]
    template_source: "output/illustration-generator.md §1 内联 SVG 生成规范"

  L2_MERMAID:
    description: "Mermaid 代码块——结构化图表首选，平台原生渲染"
    use_cases: ["流程图", "时序图", "甘特图", "思维导图", "时间线", "象限图", "需求图"]
    advantages: ["语法简洁", "平台原生支持", "版本可控", "可 diff"]
    template_source: "output/illustration-generator.md §2 Mermaid 代码块生成规范"

  L3_OBSERVABLE_PLOT:
    description: "Observable Plot——数据可视化首选，声明式语法"
    use_cases: ["柱状图", "折线图", "散点图", "面积图", "热力图"]
    advantages: ["声明式", "数据驱动", "交互式", "顶刊审美"]
    template_source: "output/chart-renderer.md"

  L4_ECHARTS:
    description: "ECharts——交互式数据可视化"
    use_cases: ["复杂图表", "动态图表", "仪表盘"]
    advantages: ["丰富的图表类型", "交互性强", "主题可定制"]
    template_source: "output/chart-renderer.md"

  L5_MARKMAP:
    description: "Markmap——思维导图专用"
    use_cases: ["思维导图", "概念图", "知识树"]
    advantages: ["Markdown 语法", "可折叠", "层级清晰"]
    template_source: "output/mindmap-renderer.md"

  L6_CANVAS_MATPLOTLIB:
    description: "Canvas / Matplotlib——科学计算图表"
    use_cases: ["科学图表", "数学函数图", "统计图", "3D 图"]
    advantages: ["科学计算集成", "Nature/Science 配色", "出版级输出"]
    template_source: "output/chart-renderer.md"

  L7_ASCII_TEXT:
    description: "ASCII / 纯文本——最终穷尽重试"
    use_cases: ["终端环境", "纯文本输出", "Markdown 兜底"]
    advantages: ["零依赖", "终端可读"]
    template_source: "output/illustration-generator.md §5 ASCII 兜底规范"
```

## §2 配图类型 → 代码生成方式路由表

```yaml
type_to_code_router:
  concept_illustration:
    description: "概念插图——全息框架各维度配图"
    primary: "内联 SVG（output/illustration-generator.md §1.1 知识图谱模板）"
    secondary: "Mermaid graph（output/illustration-generator.md §2.1）"
    forbidden: "Qwen-Image / Flux / SD / DALL-E"

  calligraphy_title:
    description: "标题艺术字 / 书法"
    primary: "SVG <text> + CSS font-family + font-weight（衬线/手写体字体栈）"
    secondary: "Typst text() + font() 函数"
    forbidden: "Qwen-Image 书法生成"

  infographic:
    description: "数据可视化辅助 / 信息图"
    primary: "内联 SVG（output/illustration-generator.md §1.3 对比信息图模板）"
    secondary: "Observable Plot + ECharts"
    forbidden: "Qwen-Image 信息图生成"

  brand_identity:
    description: "招牌文字 / 品牌标识"
    primary: "SVG <text> + <path>（品牌 Logo 矢量绘制）"
    secondary: "CSS @font-face + 品牌字体"
    forbidden: "Qwen-Image 品牌生成"

  data_chart:
    description: "数据图表"
    primary: "Observable Plot / ECharts（output/chart-renderer.md）"
    secondary: "内联 SVG（output/illustration-generator.md §1.6 柱状图模板）"
    forbidden: "Qwen-Image 图表生成"

  knowledge_graph:
    description: "知识图谱"
    primary: "内联 SVG（output/illustration-generator.md §1.1 知识图谱模板）"
    secondary: "Mermaid graph / d3-force"
    forbidden: "Qwen-Image 知识图谱生成"

  timeline:
    description: "时间线"
    primary: "内联 SVG（output/illustration-generator.md §1.2 时间线模板）"
    secondary: "Mermaid timeline"
    forbidden: "Qwen-Image 时间线生成"

  decision_tree:
    description: "决策路径图"
    primary: "内联 SVG（output/illustration-generator.md §1.5 决策路径图模板）"
    secondary: "Mermaid flowchart"
    forbidden: "Qwen-Image 决策树生成"

  causal_loop:
    description: "系统/因果结构图"
    primary: "内联 SVG（output/illustration-generator.md §1.4 系统因果结构图模板）"
    secondary: "Mermaid graph"
    forbidden: "Qwen-Image 因果图生成"
```

## 激活条件

```yaml
activation:
  condition: "需要生成配图（概念插图/信息图/装饰图/品牌视觉元素/数据图表/知识图谱/时间线/决策树/因果图）AND output_type ∈ {research_report, course_material, wechat_article}"
  priority: "代码生成图首选 — 完全自足+矢量优先+VCA风格注入+DLP匹配，禁用所有AI生图API"
  exhaust-retry: "SVG → Mermaid → Observable Plot → ECharts → Markmap → Canvas/Matplotlib → ASCII（详见 §8 穷尽重试策略）"
  trigger_nodes:
    - "T20_output_rendering: 输出渲染阶段需要配图时"
    - "T13_cog_synthesize: 认知综合阶段概念可视化辅助"
    - "T27_visualization_orchestration: 统一可视化编排"
    - "T20a_research_render: 研究报告渲染强制配图"
  platform_requirements:
    - "无外部API依赖（纯代码生成）"
    - "支持SVG/Mermaid原生渲染的平台环境"
  deactivation: "当所有配图需求已满足或 output_type 不需要配图时，本适配器不激活"
```

---

## §3 与 profound-cognition Task 节点集成

```yaml
task_integration:
  T20_output_rendering:
    trigger: "输出渲染 — 需要配图时"
    strategy: "按 §2 路由表选择代码生成方式"
    output: "SVG / Mermaid 代码块直接嵌入 final_output"
    annotation: "[code-generated] 标签标记代码生成图（替代原 [qwen-image] 标签）"
    quality_gate: "通过 ASR 硬门禁（rendering-pipeline/asr-hard-gate.md）"

  T13_cog_synthesize:
    trigger: "认知综合 — 概念可视化辅助"
    strategy: "内联 SVG 知识图谱模板（§1.1）"
    output: "概念图嵌入综合分析"
    annotation: "[code-generated-concept] 标签标记概念插图"

  T27_visualization_orchestration:
    trigger: "统一可视化编排"
    strategy: "按配图类型路由（§2）"
    output: "矢量图嵌入研究报告"
    annotation: "[code-generated-viz] 标签标记可视化产出"

  T20a_research_render:
    trigger: "研究报告渲染 — 强制配图"
    strategy: "按 SKILL.md §0.1 D 强制配图规则，使用代码生成图"
    output: "SVG / Mermaid 代码块嵌入报告"
    annotation: "[code-generated-figure] 标签标记报告配图"
```

## §4 VCA 原子库对接规范

> 配图生成时必须从 VCA（Visual Creative Atoms）原子库检索匹配的艺术流派风格。

```yaml
vca_integration:
  description: |
    本适配器作为 VCA 原子库的执行层，将 VCA 风格规范注入代码生成图。
    VCA 原子定义了配色、字体、布局、装饰等视觉规范，
    本适配器按 VCA 规范生成 SVG / Mermaid 代码。

  mapping:
    - vca_atom: "VCA-ART-003 瑞士风格"
      code_implementation: "SVG + 网格布局 + 无衬线字体 + 低饱和配色"
      use_cases: ["技术文章封面图", "信息图", "数据可视化"]

    - vca_atom: "VCA-ART-005 包豪斯"
      code_implementation: "SVG + 几何形状 + 三原色 + 功能性布局"
      use_cases: ["品牌视觉元素", "装饰图"]

    - vca_atom: "VCA-DATA-001 经济学人风格"
      code_implementation: "Observable Plot + 直接标注 + 低饱和色板"
      use_cases: ["数据图表", "统计信息图"]

    - vca_atom: "VCA-DATA-006 Distill 风格"
      code_implementation: "D3.js + 动画过渡 + 解释性可视化"
      use_cases: ["交互式数据可视化"]

    - vca_atom: "VCA-BRAND-001 Logo 占位"
      code_implementation: "SVG <path> + 品牌色填充 + 矢量绘制"
      use_cases: ["品牌标识", "招牌文字"]

    - vca_atom: "VCA-GEN-001 流场"
      code_implementation: "Canvas + Perlin 噪声 + 粒子系统"
      use_cases: ["生成式艺术背景", "封面装饰"]

  retrieval_flow:
    step_1: "识别配图内容类型（技术封面/数据可视/品牌视觉/生成式艺术）"
    step_2: "从 VCA 原子库检索匹配原子"
    step_3: "加载 VCA 原子的风格规范（配色/字体/布局/装饰）"
    step_4: "按 VCA 风格规范生成 SVG / Mermaid / Canvas 代码"
    step_5: "代码嵌入 final_output，通过 ASR 硬门检查"
```

## §5 DLP 驱动风格选择

> 配图风格由当前激活的 DLP（Dynamic Layout Profile）的 `applicable_scenarios` 字段决定。

```yaml
dlp_driven_style:
  academic_journal:
    figure_style: "学术配图风格"
    code_implementation: "SVG + 低饱和色系 + Arial/Helvetica 无衬线 + 细网格"
    format: "SVG 矢量（印刷级 ≥ 300dpi 等效）"
    decoration: "无装饰，信息密度优先"

  interface_brand:
    figure_style: "产品配图风格"
    code_implementation: "SVG + 品牌色 + 阴影/圆角 + 高完成度"
    format: "SVG / PNG（通过 SVG → PNG 转换）"
    decoration: "适度阴影/圆角，体现产品质感"

  publication_typesetting:
    figure_style: "杂志配图风格"
    code_implementation: "SVG + 编辑色板 + 衬线标题 + 图文混排"
    format: "SVG / PNG（编辑式）"
    decoration: "编辑式装饰，图文协调"

  data_visualization:
    figure_style: "数据可视风格"
    code_implementation: "Observable Plot + Tufte 原则 + 数据语义色"
    format: "SVG 矢量优先"
    decoration: "无冗余装饰，清晰克制"
```

## §6 SVG 代码生成模板索引

> 完整 SVG 模板见 `output/illustration-generator.md §1`，本节仅提供索引。

```yaml
svg_templates:
  template_1_knowledge_graph:
    description: "知识图谱——概念关系网络"
    source: "output/illustration-generator.md §1.1"
    elements: ["<circle> 节点", "<line> 关系", "<text> 标签"]
    style: "DLP academic-journal 族"

  template_2_timeline:
    description: "时间线——事件时序演变"
    source: "output/illustration-generator.md §1.2"
    elements: ["<line> 主轴", "<circle> 事件点", "<text> 标签"]
    style: "DLP publication-typesetting 族"

  template_3_comparison_infographic:
    description: "对比信息图——多维度对比"
    source: "output/illustration-generator.md §1.3"
    elements: ["<rect> 对比块", "<text> 标签", "<path> 图标"]
    style: "DLP interface-brand 族"

  template_4_causal_structure:
    description: "系统因果结构图——因果回路"
    source: "output/illustration-generator.md §1.4"
    elements: ["<path> 箭头", "<rect> 节点", "<text> 标签", "+/- 符号"]
    style: "DLP academic-journal 族"

  template_5_decision_path:
    description: "决策路径图——决策树"
    source: "output/illustration-generator.md §1.5"
    elements: ["<rect> 决策节点", "<circle> 机会节点", "<path> 分支"]
    style: "DLP data-visualization 族"

  template_6_bar_chart:
    description: "柱状图——数据对比"
    source: "output/illustration-generator.md §1.6"
    elements: ["<rect> 柱", "<line> 坐标轴", "<text> 标签"]
    style: "DLP data-visualization 族"
```

## §7 质量检查清单

```yaml
quality_checklist:
  - id: "QC-001"
    check: "未使用任何 AI 生图 API（Flux / SD / Qwen-Image / DALL-E / Midjourney）"
    severity: "blocking"
    on_fail: "重写为代码生成图"

  - id: "QC-002"
    check: "SVG / Mermaid 代码块语法正确，可被平台原生渲染"
    severity: "blocking"
    on_fail: "修正语法错误"

  - id: "QC-003"
    check: "配图风格与当前 DLP 的 applicable_scenarios 匹配"
    severity: "blocking"
    on_fail: "调整风格至 DLP 族对应规范"

  - id: "QC-004"
    check: "VCA 原子库已检索匹配原子（若适用）"
    severity: "warning"
    on_fail: "标注 [VCA_ALTERNATIVE]，使用 DLP 默认风格"

  - id: "QC-005"
    check: "矢量格式优先（SVG / Mermaid），位图仅作兜底"
    severity: "blocking"
    on_fail: "转换为矢量格式"

  - id: "QC-006"
    check: "通过 ASR 硬门禁（asr-hard-gate.md）全量检查"
    severity: "blocking"
    on_fail: "按 ASR 违规清单修正"

  - id: "QC-007"
    check: "配图含完整图注（编号 / 标题 / 数据来源 / 说明）"
    severity: "blocking"
    on_fail: "补齐图注"

  - id: "QC-008"
    check: "配图含 alt_text 无障碍替代文本"
    severity: "blocking"
    on_fail: "补齐 alt_text"
```

## §8 穷尽重试策略

```yaml
exhaust_retry:
  description: |
    按 EXHAUST 模式四大铁律，代码生成图的穷尽重试链。
    不存在"放弃生成图"的选项——任何场景下都必须产出配图。

  L1_FULL:
    condition: "代码生成环境可用（默认）"
    behavior: "完整 SVG / Mermaid 代码生成 + VCA 风格注入 + DLP 匹配"

  L2_PARTIAL_STYLE:
    condition: "VCA 原子库不可用或无匹配原子"
    behavior: "使用 DLP 默认风格生成 SVG / Mermaid，标注 [VCA_ALTERNATIVE]"

  L3_TEXT_ONLY_MERMAID:
    condition: "SVG 生成失败（语法错误 / 复杂度过高）"
    behavior: "穷尽重试至 Mermaid 代码块，标注 [MERMAID_FALLBACK]"

  L4_ASCII:
    condition: "Mermaid 也不可用（终端环境 / 纯文本输出）"
    behavior: "穷尽重试至 ASCII 图表，标注 [ASCII_FALLBACK]"

  forbidden_paths:
    - "❌ 穷尽重试至 AI 生图 API（Flux / SD / Qwen-Image 等）"
    - "❌ 跳过配图生成"
    - "❌ 输出'图片生成失败'占位符"
```

## §9 错误处理

```yaml
error_handling:
  svg_syntax_error:
    action: "修正 SVG 语法，穷尽重试直至通过 ASR 硬门"
    log: "记录 SVG 语法错误事件"

  mermaid_render_failure:
    action: "穷尽重试至内联 SVG，标注 [SVG_FALLBACK]"
    log: "记录 Mermaid 渲染失败事件"

  vca_atom_not_found:
    action: "使用 DLP 默认风格，标注 [VCA_ALTERNATIVE]"
    log: "记录 VCA 原子未命中事件"

  dlp_not_activated:
    action: "默认使用 academic-journal 族风格，标注 [DLP_ALTERNATIVE]"
    log: "记录 DLP 未激活事件"

  content_too_complex:
    action: "拆分为多张子图，每张聚焦一个核心概念"
    log: "记录内容复杂度过高事件"

  resolution_insufficient:
    action: "提升 SVG viewBox 尺寸 / 增加 dpi 参数"
    log: "记录分辨率不足事件"
```

## §10 与其他模块的协作关系

```yaml
module_collaboration:
  output_illustration_generator:
    relation: "本适配器是 illustration-generator.md 的执行层"
    flow: "illustration-generator.md 定义规范 → 本适配器执行代码生成"

  output_chart_renderer:
    relation: "数据图表由 chart-renderer.md 主导，本适配器协作"
    flow: "chart-renderer.md 生成 Observable Plot / ECharts 代码 → 本适配器嵌入"

  output_mindmap_renderer:
    relation: "思维导图由 mindmap-renderer.md 主导，本适配器协作"
    flow: "mindmap-renderer.md 生成 Markmap 代码 → 本适配器嵌入"

  plugins_paper_figure_adapter:
    relation: "手绘框架图由 paper-figure-adapter.md 主导"
    flow: "paper-figure-adapter.md 生成 SVG → 本适配器协作嵌入"

  rendering_pipeline_visual_creative_atoms:
    relation: "VCA 原子库提供风格规范，本适配器执行"
    flow: "VCA 原子库检索 → 本适配器按规范生成代码"

  rendering_pipeline_asr_hard_gate:
    relation: "ASR 硬门禁检查本适配器产出"
    flow: "本适配器生成代码 → ASR 硬门检查 → 通过 / 拒绝"
```

## §11 版本历史

```yaml
version_history:
  v1_0:
    date: "2026-05-15"
    description: "初始版本——Qwen-Image 文生图 API 适配器"
    status: "deprecated"
    issues:
      - "依赖 AI 生图 API，违反用户'代码生成优先'原则"
      - "需要 DashScope API 密钥，非自足"
      - "生成图为位图，非矢量，印刷质量不足"
      - "与 illustration-generation-protocol.md §6.4 强制 Mermaid/SVG 矛盾"

  v2_0:
    date: "2026-06-21"
    description: "彻底重构为代码生成图适配器"
    status: "active"
    changes:
      - "完全移除 Qwen-Image / Flux / SD / DALL-E / Midjourney 等 AI 生图 API 依赖"
      - "新增 §0 核心铁律，明确 forbidden_apis 清单"
      - "新增 §1 代码生成图优先级链（SVG → Mermaid → Observable Plot → ECharts → Markmap → Canvas/Matplotlib → ASCII）"
      - "新增 §2 配图类型 → 代码生成方式路由表"
      - "新增 §4 VCA 原子库对接规范"
      - "新增 §5 DLP 驱动风格选择"
      - "新增 §6 SVG 代码生成模板索引"
      - "新增 §7 质量检查清单（含'未使用任何 AI 生图 API'检查）"
      - "重构 §8 穷尽重试策略，明确禁止穷尽重试至 AI 生图 API"
      - "重构 §3 Task 节点集成，将 [qwen-image] 标签替换为 [code-generated] 标签"
    motivation: |
      用户明确要求："我们大多数时候图片应该用代码生成，而非用API"。
      用户已引入大量开源渲染项目（学术期刊级 / 界面与Web设计类 / 通用高审美排版出品类 / 视觉创意与数据可视化类），
      这些项目的源码已足以支撑代码生成图的审美/排版/配图需求，
      无需依赖任何 AI 生图 API。
```

---

© 阿洋
