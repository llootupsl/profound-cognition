<!-- 作者：阿洋 -->

# 排版原子库 (Typography Atoms)

> **定位**: 渲染管道的排版原子化能力库，为所有渲染模块提供可复用的字号/字重/行高/字距/段落/中西文混排原子。
> **强制规则**: 所有渲染模块的排版参数必须从本原子库选取原子，不得自行声明排版数值。
> **DLP 对接**: 每个原子通过 `visual_dna.font_scheme.typography_scale` 字段与 Design Language Protocol (DLP) 对接，由 Taste-Skill 仲裁。

---

## 方法论原理

排版原子库基于"原子化设计"理论：将排版系统分解为最小不可分割的原子单元（字号/字重/行高/字距/段落/混排），每个原子封装 CSS 与 Typst 双轨实现，确保跨引擎排版一致性。原子库融入了 editorialTypesetting-skill 的杂志级长文排版能力与 typography-master-skill 的层级控制能力，为渲染管线提供经过审美校准的排版原子。

### 中英文双轨规则

中文按 **1.2 倍放大规则**：同一层级下，中文字号 = 西文字号 × 1.2。此规则源于中文汉字的方块结构与西文字母的线性结构的视觉差异——汉字笔画密度高，同等字号下视觉面积大于西文字母，但为保持阅读节奏一致，中文需在字号上适度放大以平衡视觉重量。

---

## 一、字号阶梯原子（TA-SCALE）

> **融入来源**: typography-master-skill — 严格的 h1-h6 层级，每级差异 ≥ 4px
> **DLP 对接**: 每个字号原子映射到 `visual_dna.font_scheme.typography_scale` 数组中的对应层级项，由 Taste-Skill 根据 `target_audience` 参数选择基准字号。

### TA-SCALE-001: display 超大标题

- **原子 ID**: TA-SCALE-001
- **适用场景**: 超大标题/演示标题/封面主标题/英雄区标题
- **CSS 实现**:
  ```css
  .ta-scale-display {
    font-size: 4.5rem;      /* 72px 西文 */
    font-size: clamp(3rem, 8vw, 4.5rem);
    line-height: 1.1;
    font-weight: 700;
    letter-spacing: -0.03em;
  }

  /* 中文 1.2 倍放大：72px × 1.2 = 86.4px ≈ 86px */
  :lang(zh) .ta-scale-display,
  .ta-scale-display.zh {
    font-size: clamp(3.6rem, 9.6vw, 5.375rem); /* 86px / 16 = 5.375rem */
    letter-spacing: 0.02em; /* 中文标题微宽松 */
  }
  ```
- **Typst 实现**:
  ```typst
  #let ta-scale-display = {
    // 西文 72pt
    set text(size: 72pt, weight: "bold", tracking: -0.5pt)
    set par(leading: 0.8em)

    // 中文 1.2 倍放大：72pt × 1.2 = 86.4pt ≈ 86pt
    if text.lang == "zh" {
      set text(size: 86pt, tracking: 0.3pt)
    }
  }

  // 使用示例
  #show heading.where(level: 0): it => {
    set text(size: 72pt, weight: "bold")
    if text.lang == "zh" { set text(size: 86pt) }
    it
  }
  ```
- **与 DLP 对接规则**: 映射到 `typography_scale[0]`（display 层级）。当 `visual_dna.aesthetic_level == "L3-沉浸"` 时启用此原子；L1/L2 等级不使用 display 层级。Taste-Skill 根据 `content_theme` 判定是否为叙事长文/品牌故事场景，若是则激活 display 层级。

---

### TA-SCALE-002: h1 一级标题

- **原子 ID**: TA-SCALE-002
- **适用场景**: 一级标题/文档主标题/章节大标题
- **CSS 实现**:
  ```css
  .ta-scale-h1 {
    font-size: 3rem;        /* 48px 西文 */
    line-height: 1.2;
    font-weight: 700;
    letter-spacing: -0.02em;
  }

  /* 中文 1.2 倍放大：48px × 1.2 = 57.6px ≈ 57px */
  :lang(zh) .ta-scale-h1,
  .ta-scale-h1.zh {
    font-size: 3.5625rem;   /* 57px / 16 = 3.5625rem */
    letter-spacing: 0.01em;
  }
  ```
- **Typst 实现**:
  ```typst
  #let ta-scale-h1 = {
    set text(size: 48pt, weight: "bold", tracking: -0.3pt)
    set par(leading: 0.9em)

    if text.lang == "zh" {
      set text(size: 57pt, tracking: 0.2pt)
    }
  }

  #show heading.where(level: 1): it => {
    set text(size: 48pt, weight: "bold")
    if text.lang == "zh" { set text(size: 57pt) }
    it
  }
  ```
- **与 DLP 对接规则**: 映射到 `typography_scale[1]`（h1 层级）。所有 `output_type` 均启用此原子。与 `visual_dna.font_scheme.heading` 字体族绑定，Taste-Skill 根据 `design_language` 选择标题字体（学术严谨→无衬线、人文温度→衬线）。

---

### TA-SCALE-003: h2 二级标题

- **原子 ID**: TA-SCALE-003
- **适用场景**: 二级标题/章节标题/区块大标题
- **CSS 实现**:
  ```css
  .ta-scale-h2 {
    font-size: 2.25rem;     /* 36px 西文 */
    line-height: 1.25;
    font-weight: 600;
    letter-spacing: -0.015em;
  }

  /* 中文 1.2 倍放大：36px × 1.2 = 43.2px ≈ 43px */
  :lang(zh) .ta-scale-h2,
  .ta-scale-h2.zh {
    font-size: 2.6875rem;   /* 43px / 16 = 2.6875rem */
    letter-spacing: 0.01em;
  }
  ```
- **Typst 实现**:
  ```typst
  #let ta-scale-h2 = {
    set text(size: 36pt, weight: "semibold", tracking: -0.2pt)
    set par(leading: 0.95em)

    if text.lang == "zh" {
      set text(size: 43pt, tracking: 0.15pt)
    }
  }

  #show heading.where(level: 2): it => {
    set text(size: 36pt, weight: "semibold")
    if text.lang == "zh" { set text(size: 43pt) }
    it
  }
  ```
- **与 DLP 对接规则**: 映射到 `typography_scale[2]`（h2 层级）。与 h1 层级差异为 12px（48-36），满足 typography-master-skill 的"每级差异 ≥ 4px"规则。Taste-Skill 仲裁时确保 h2 字重 ≤ h1 字重，维持层级递减。

---

### TA-SCALE-004: h3 三级标题

- **原子 ID**: TA-SCALE-004
- **适用场景**: 三级标题/小节标题/卡片标题
- **CSS 实现**:
  ```css
  .ta-scale-h3 {
    font-size: 1.75rem;     /* 28px 西文 */
    line-height: 1.3;
    font-weight: 600;
    letter-spacing: -0.01em;
  }

  /* 中文 1.2 倍放大：28px × 1.2 = 33.6px ≈ 34px */
  :lang(zh) .ta-scale-h3,
  .ta-scale-h3.zh {
    font-size: 2.125rem;    /* 34px / 16 = 2.125rem */
    letter-spacing: 0.005em;
  }
  ```
- **Typst 实现**:
  ```typst
  #let ta-scale-h3 = {
    set text(size: 28pt, weight: "semibold", tracking: -0.15pt)
    set par(leading: 1em)

    if text.lang == "zh" {
      set text(size: 34pt, tracking: 0.1pt)
    }
  }

  #show heading.where(level: 3): it => {
    set text(size: 28pt, weight: "semibold")
    if text.lang == "zh" { set text(size: 34pt) }
    it
  }
  ```
- **与 DLP 对接规则**: 映射到 `typography_scale[3]`（h3 层级）。与 h2 层级差异为 8px（36-28），满足 ≥ 4px 规则。当 `visual_dna.aesthetic_level == "L1-极简"` 时，h3 为最低标题层级，不启用 h4-h6。

---

### TA-SCALE-005: h4 四级标题

- **原子 ID**: TA-SCALE-005
- **适用场景**: 四级标题/子节标题/段落小标题
- **CSS 实现**:
  ```css
  .ta-scale-h4 {
    font-size: 1.25rem;     /* 20px 西文 */
    line-height: 1.35;
    font-weight: 600;
    letter-spacing: -0.005em;
  }

  /* 中文 1.2 倍放大：20px × 1.2 = 24px */
  :lang(zh) .ta-scale-h4,
  .ta-scale-h4.zh {
    font-size: 1.5rem;      /* 24px / 16 = 1.5rem */
    letter-spacing: 0;
  }
  ```
- **Typst 实现**:
  ```typst
  #let ta-scale-h4 = {
    set text(size: 20pt, weight: "semibold", tracking: -0.1pt)
    set par(leading: 1.05em)

    if text.lang == "zh" {
      set text(size: 24pt, tracking: 0pt)
    }
  }

  #show heading.where(level: 4): it => {
    set text(size: 20pt, weight: "semibold")
    if text.lang == "zh" { set text(size: 24pt) }
    it
  }
  ```
- **与 DLP 对接规则**: 映射到 `typography_scale[4]`（h4 层级）。与 h3 层级差异为 8px（28-20），满足 ≥ 4px 规则。在 `output_type == "wechat_article"` 场景下，h4 为推荐最低标题层级（公众号标题不宜过深）。

---

### TA-SCALE-006: body 正文

- **原子 ID**: TA-SCALE-006
- **适用场景**: 正文/段落文字/列表文字/表格文字
- **CSS 实现**:
  ```css
  .ta-scale-body {
    font-size: 1rem;        /* 16px 西文 */
    line-height: 1.75;
    font-weight: 400;
    letter-spacing: 0;
  }

  /* 中文 1.2 倍放大：16px × 1.2 = 19.2px ≈ 19px */
  :lang(zh) .ta-scale-body,
  .ta-scale-body.zh {
    font-size: 1.1875rem;   /* 19px / 16 = 1.1875rem */
    letter-spacing: 0;
  }
  ```
- **Typst 实现**:
  ```typst
  #let ta-scale-body = {
    set text(size: 16pt, weight: "regular", tracking: 0pt)
    set par(leading: 1.75em)

    if text.lang == "zh" {
      set text(size: 19pt, tracking: 0pt)
    }
  }

  // 正文默认样式
  #show: set par(leading: 1.75em, justify: true)
  #show: set text(size: 16pt, weight: "regular")
  ```
- **与 DLP 对接规则**: 映射到 `typography_scale[5]`（body 层级）。这是排版的基准层级，所有其他层级以此为锚点。Taste-Skill 根据 `target_audience` 调整基准：`academic` → 16px、`youth` → 17px（移动端友好）、`professional` → 16px。与 `visual_dna.font_scheme.body` 字体族绑定。

---

### TA-SCALE-007: caption 说明文字

- **原子 ID**: TA-SCALE-007
- **适用场景**: 说明文字/图注/表注/辅助说明/元数据标签
- **CSS 实现**:
  ```css
  .ta-scale-caption {
    font-size: 0.8125rem;   /* 13px 西文 */
    line-height: 1.4;
    font-weight: 400;
    letter-spacing: 0.01em;
    color: var(--color-text-secondary);
  }

  /* 中文 1.2 倍放大：13px × 1.2 = 15.6px ≈ 16px */
  :lang(zh) .ta-scale-caption,
  .ta-scale-caption.zh {
    font-size: 1rem;        /* 16px / 16 = 1rem */
    letter-spacing: 0;
  }
  ```
- **Typst 实现**:
  ```typst
  #let ta-scale-caption = {
    set text(size: 13pt, weight: "regular", tracking: 0.1pt)
    set par(leading: 1.4em)

    if text.lang == "zh" {
      set text(size: 16pt, tracking: 0pt)
    }
  }

  // 图注样式
  #show figure.caption: it => {
    set text(size: 13pt, fill: rgb("#6B7280"))
    if text.lang == "zh" { set text(size: 16pt) }
    it
  }
  ```
- **与 DLP 对接规则**: 映射到 `typography_scale[6]`（caption 层级）。与 body 层级差异为 3px（16-13），作为辅助文字不强制 ≥ 4px 差异规则（该规则仅适用于标题层级 h1-h6）。颜色绑定 `visual_dna.color_scheme` 的 `--color-text-secondary`。

---

### TA-SCALE-008: footnote 脚注

- **原子 ID**: TA-SCALE-008
- **适用场景**: 脚注/尾注/参考文献条目/法律声明/版本信息
- **CSS 实现**:
  ```css
  .ta-scale-footnote {
    font-size: 0.75rem;     /* 12px 西文 */
    line-height: 1.5;
    font-weight: 400;
    letter-spacing: 0.01em;
    color: var(--color-text-secondary);
  }

  /* 中文 1.2 倍放大：12px × 1.2 = 14.4px ≈ 14px */
  :lang(zh) .ta-scale-footnote,
  .ta-scale-footnote.zh {
    font-size: 0.875rem;    /* 14px / 16 = 0.875rem */
    letter-spacing: 0;
  }
  ```
- **Typst 实现**:
  ```typst
  #let ta-scale-footnote = {
    set text(size: 12pt, weight: "regular", tracking: 0.1pt)
    set par(leading: 1.5em)

    if text.lang == "zh" {
      set text(size: 14pt, tracking: 0pt)
    }
  }

  // Typst 原生脚注样式覆写
  #show footnote: it => {
    set text(size: 12pt, fill: rgb("#6B7280"))
    if text.lang == "zh" { set text(size: 14pt) }
    it
  }
  ```
- **与 DLP 对接规则**: 映射到 `typography_scale[7]`（footnote 层级）。为字号阶梯的最小层级，低于此层级的文字将影响可读性。当 `output_type == "research_report"` 时强制启用（学术论文需要脚注）；`output_type == "wechat_article"` 时可选启用。

---

## 二、字重搭配原子（TA-WEIGHT）

> **融入来源**: typography-master-skill — 标题与正文的字重差异 ≥ 200（如标题 600/正文 400）
> **DLP 对接**: 每个字重原子映射到 `visual_dna.font_scheme.weight_pair` 字段，由 Taste-Skill 根据 `design_language` 选择字重搭配方案。

### TA-WEIGHT-001: 现代产品界面字重搭配

- **原子 ID**: TA-WEIGHT-001
- **适用场景**: 现代产品界面/SaaS 仪表盘/移动端 App/科技产品文档
- **CSS 实现**:
  ```css
  .ta-weight-modern h1,
  .ta-weight-modern h2,
  .ta-weight-modern h3 {
    font-weight: 600; /* semibold 标题 */
  }

  .ta-weight-modern body,
  .ta-weight-modern p,
  .ta-weight-modern li {
    font-weight: 400; /* regular 正文 */
  }

  /* 字重差异：600 - 400 = 200，满足 ≥ 200 规则 */
  ```
- **Typst 实现**:
  ```typst
  #let ta-weight-modern = {
    // 标题 semibold (600)
    #show heading.where(level: 1): it => { set text(weight: "semibold"); it }
    #show heading.where(level: 2): it => { set text(weight: "semibold"); it }
    #show heading.where(level: 3): it => { set text(weight: "semibold"); it }

    // 正文 regular (400)
    set text(weight: "regular")
  }
  ```
- **与 DLP 对接规则**: 映射到 `weight_pair: { heading: 600, body: 400 }`。当 `design_language == "科技前沿"` 或 `design_language == "教育清晰"` 时默认启用此原子。字重差异 200 满足 typography-master-skill 的最低要求，适合屏幕阅读场景。

---

### TA-WEIGHT-002: 学术论文字重搭配

- **原子 ID**: TA-WEIGHT-002
- **适用场景**: 学术论文/研究报告/期刊投稿/学位论文
- **CSS 实现**:
  ```css
  .ta-weight-academic h1,
  .ta-weight-academic h2,
  .ta-weight-academic h3 {
    font-weight: 700; /* bold 标题 */
  }

  .ta-weight-academic body,
  .ta-weight-academic p,
  .ta-weight-academic li {
    font-weight: 400; /* regular 正文 */
  }

  /* 字重差异：700 - 400 = 300，满足 ≥ 200 规则 */
  ```
- **Typst 实现**:
  ```typst
  #let ta-weight-academic = {
    // 标题 bold (700)
    #show heading.where(level: 1): it => { set text(weight: "bold"); it }
    #show heading.where(level: 2): it => { set text(weight: "bold"); it }
    #show heading.where(level: 3): it => { set text(weight: "bold"); it }

    // 正文 regular (400)
    set text(weight: "regular")
  }
  ```
- **与 DLP 对接规则**: 映射到 `weight_pair: { heading: 700, body: 400 }`。当 `design_language == "学术严谨"` 时默认启用此原子。字重差异 300 提供更强的层级对比，适合打印输出的学术论文场景。与 `output_type == "research_report"` 强绑定。

---

### TA-WEIGHT-003: 奢侈品牌字重搭配

- **原子 ID**: TA-WEIGHT-003
- **适用场景**: 奢侈品牌/高端时尚/品牌故事/沉浸式叙事
- **CSS 实现**:
  ```css
  .ta-weight-luxury h1,
  .ta-weight-luxury h2,
  .ta-weight-luxury h3 {
    font-weight: 300; /* light 标题 */
  }

  .ta-weight-luxury body,
  .ta-weight-luxury p,
  .ta-weight-luxury li {
    font-weight: 400; /* regular 正文 */
  }

  /*
   * 字重差异：400 - 300 = 100，不满足 ≥ 200 规则
   * 但奢侈品牌场景豁免此规则——light 标题是品牌调性需求
   * typography-master-skill 规则在 design_language == "人文温度" + L3-沉浸 时豁免
   */
  ```
- **Typst 实现**:
  ```typst
  #let ta-weight-luxury = {
    // 标题 light (300)
    #show heading.where(level: 1): it => { set text(weight: "light"); it }
    #show heading.where(level: 2): it => { set text(weight: "light"); it }
    #show heading.where(level: 3): it => { set text(weight: "light"); it }

    // 正文 regular (400)
    set text(weight: "regular")
  }
  ```
- **与 DLP 对接规则**: 映射到 `weight_pair: { heading: 300, body: 400 }`。当 `design_language == "人文温度"` 且 `aesthetic_level == "L3-沉浸"` 时启用此原子。此为字重差异规则的豁免场景——奢侈品牌的 light 标题是刻意的审美选择，通过纤细字重传递优雅感。Taste-Skill 仲裁时记录豁免原因。

---

### TA-WEIGHT-004: 编辑式排字重搭配

- **原子 ID**: TA-WEIGHT-004
- **适用场景**: 编辑式排版/杂志正文/新闻长文/专栏文章
- **CSS 实现**:
  ```css
  .ta-weight-editorial h1,
  .ta-weight-editorial h2,
  .ta-weight-editorial h3 {
    font-weight: 400; /* regular 标题 */
  }

  .ta-weight-editorial body,
  .ta-weight-editorial p,
  .ta-weight-editorial li {
    font-weight: 400; /* regular 正文 */
  }

  /*
   * 字重差异：400 - 400 = 0，不满足 ≥ 200 规则
   * 编辑式排版通过字号差异而非字重差异建立层级
   * 豁免条件：design_language == "人文温度" + content_theme 含"杂志/编辑/新闻"
   */
  ```
- **Typst 实现**:
  ```typst
  #let ta-weight-editorial = {
    // 标题 regular (400) — 通过字号建立层级
    #show heading.where(level: 1): it => { set text(weight: "regular"); it }
    #show heading.where(level: 2): it => { set text(weight: "regular"); it }
    #show heading.where(level: 3): it => { set text(weight: "regular"); it }

    // 正文 regular (400)
    set text(weight: "regular")
  }
  ```
- **与 DLP 对接规则**: 映射到 `weight_pair: { heading: 400, body: 400 }`。当 `design_language == "人文温度"` 且 `content_theme` 包含"杂志/编辑/新闻/专栏"关键词时启用此原子。此为字重差异规则的豁免场景——编辑式排版依赖字号差异和留白建立层级，而非字重对比。融入 editorialTypesetting-skill 的编辑式排版理念。

---

### TA-WEIGHT-005: 技术文档字重搭配

- **原子 ID**: TA-WEIGHT-005
- **适用场景**: 技术文档/API 文档/产品手册/开发指南
- **CSS 实现**:
  ```css
  .ta-weight-tech h1,
  .ta-weight-tech h2,
  .ta-weight-tech h3 {
    font-weight: 500; /* medium 标题 */
  }

  .ta-weight-tech body,
  .ta-weight-tech p,
  .ta-weight-tech li {
    font-weight: 400; /* regular 正文 */
  }

  .ta-weight-tech strong,
  .ta-weight-tech b,
  .ta-weight-tech dt {
    font-weight: 500; /* medium 强调 */
  }

  /* 字重差异：500 - 400 = 100，通过强调字重 500 补偿层级感 */
  ```
- **Typst 实现**:
  ```typst
  #let ta-weight-tech = {
    // 标题 medium (500)
    #show heading.where(level: 1): it => { set text(weight: "medium"); it }
    #show heading.where(level: 2): it => { set text(weight: "medium"); it }
    #show heading.where(level: 3): it => { set text(weight: "medium"); it }

    // 正文 regular (400)
    set text(weight: "regular")

    // 强调 medium (500)
    #show strong: it => { set text(weight: "medium"); it }
  }
  ```
- **与 DLP 对接规则**: 映射到 `weight_pair: { heading: 500, body: 400, emphasis: 500 }`。当 `design_language == "科技前沿"` 且 `output_type == "course_material"` 或内容含"文档/API/手册/指南"关键词时启用。技术文档场景下，过强的字重对比会干扰代码与文本的视觉平衡，medium 标题 + medium 强调提供温和的层级区分。

---

### TA-WEIGHT-006: 杂志长文字重搭配

- **原子 ID**: TA-WEIGHT-006
- **适用场景**: 杂志长文/深度报道/人物专访/文学翻译
- **CSS 实现**:
  ```css
  .ta-weight-magazine h1,
  .ta-weight-magazine h2,
  .ta-weight-magazine h3 {
    font-weight: 700; /* bold 标题 */
  }

  .ta-weight-magazine body,
  .ta-weight-magazine p,
  .ta-weight-magazine li {
    font-weight: 400; /* regular 正文 */
  }

  .ta-weight-magazine em,
  .ta-weight-magazine i {
    font-weight: 400; /* italic 强调，非加粗 */
    font-style: italic;
  }

  /* 字重差异：700 - 400 = 300，满足 ≥ 200 规则 */
  /* 强调使用 italic 而非 bold，是杂志排版的标志性手法 */
  ```
- **Typst 实现**:
  ```typst
  #let ta-weight-magazine = {
    // 标题 bold (700)
    #show heading.where(level: 1): it => { set text(weight: "bold"); it }
    #show heading.where(level: 2): it => { set text(weight: "bold"); it }
    #show heading.where(level: 3): it => { set text(weight: "bold"); it }

    // 正文 regular (400)
    set text(weight: "regular")

    // 强调 italic (400) — 杂志风格用斜体而非加粗
    #show emph: it => {
      set text(style: "italic", weight: "regular")
      it
    }
  }
  ```
- **与 DLP 对接规则**: 映射到 `weight_pair: { heading: 700, body: 400, emphasis: "italic" }`。当 `design_language == "人文温度"` 且 `content_theme` 含"杂志/深度/报道/专访/文学"关键词时启用。融入 editorialTypesetting-skill 的杂志级长文排版能力——italic 强调是杂志排版的标志性手法，与学术论文的 bold 强调形成区分。

---

## 三、行高与字距原子（TA-LEADING / TA-TRACKING）

> **融入来源**: editorialTypesetting-skill — 基线网格（baseline grid）系统，所有元素对齐到 4px 基线
> **DLP 对接**: 行高原子映射到 `visual_dna.font_scheme.leading` 字段，字距原子映射到 `visual_dna.font_scheme.tracking` 字段。

### TA-LEADING-001: 正文行高

- **原子 ID**: TA-LEADING-001
- **适用场景**: 正文段落/列表文字/表格文字/长文阅读
- **CSS 实现**:
  ```css
  .ta-leading-body {
    line-height: 1.75; /* 西文正文行高 */
  }

  /* 中文正文行高 1.8 优先——中文汉字方块结构需要更多行间呼吸空间 */
  :lang(zh) .ta-leading-body,
  .ta-leading-body.zh {
    line-height: 1.8;
  }

  /*
   * 行高范围 1.5-1.8，中文 1.8 优先
   * 基线网格对齐：行高 × 字号 必须是 4px 的整数倍
   * 16px × 1.75 = 28px（7×4px）✓ 对齐基线
   * 19px × 1.8 ≈ 34.2px → 取整 36px（9×4px）✓ 对齐基线
   */
  ```
- **Typst 实现**:
  ```typst
  #let ta-leading-body = {
    // 西文正文行高 1.75em
    set par(leading: 1.75em)

    // 中文正文行高 1.8em 优先
    if text.lang == "zh" {
      set par(leading: 1.8em)
    }
  }

  // 全局正文行高设置
  #show: set par(leading: 1.75em)
  ```
- **与 DLP 对接规则**: 映射到 `leading: { body: 1.75, body_zh: 1.8 }`。Taste-Skill 根据 `target_audience` 微调：`academic` → 1.75（紧凑学术风）、`general` → 1.8（宽松阅读风）。行高值必须与 4px 基线网格对齐（editorialTypesetting-skill 基线网格规则）。

---

### TA-LEADING-002: 标题行高

- **原子 ID**: TA-LEADING-002
- **适用场景**: h1-h6 所有标题层级/卡片标题/图表标题
- **CSS 实现**:
  ```css
  .ta-leading-heading {
    line-height: 1.2; /* 标题行高紧凑 */
  }

  /*
   * 标题行高范围 1.1-1.3
   * 紧凑行高增强标题视觉密度和层级感
   * 基线网格对齐：
   *   48px × 1.2 = 57.6px → 取整 56px（14×4px）✓
   *   36px × 1.2 = 43.2px → 取整 44px（11×4px）✓
   *   28px × 1.25 = 35px → 取整 36px（9×4px）✓
   */
  .ta-leading-heading.h1 { line-height: 1.2; }
  .ta-leading-heading.h2 { line-height: 1.25; }
  .ta-leading-heading.h3 { line-height: 1.3; }
  ```
- **Typst 实现**:
  ```typst
  #let ta-leading-heading = {
    // 标题行高 1.1-1.3 紧凑
    set par(leading: 1.2em)
  }

  #show heading.where(level: 1): it => { set par(leading: 1.2em); it }
  #show heading.where(level: 2): it => { set par(leading: 1.25em); it }
  #show heading.where(level: 3): it => { set par(leading: 1.3em); it }
  ```
- **与 DLP 对接规则**: 映射到 `leading: { heading: 1.2 }`。标题行高低于正文行高，形成视觉密度对比。与 4px 基线网格对齐时，允许 ±1px 取整偏差。当 `aesthetic_level == "L1-极简"` 时标题行高可收紧至 1.1。

---

### TA-LEADING-003: 说明文字行高

- **原子 ID**: TA-LEADING-003
- **适用场景**: 图注/表注/脚注/说明文字/元数据/标签文字
- **CSS 实现**:
  ```css
  .ta-leading-caption {
    line-height: 1.4; /* 说明文字行高 */
  }

  /*
   * 说明文字行高 1.4，介于标题(1.2)和正文(1.75)之间
   * 辅助文字不需要正文那么大的行间呼吸空间
   * 但也不能像标题那么紧凑，保持可读性
   * 基线网格对齐：
   *   13px × 1.4 = 18.2px → 取整 20px（5×4px）✓
   *   12px × 1.5 = 18px → 取整 20px（5×4px）✓ (脚注)
   */
  ```
- **Typst 实现**:
  ```typst
  #let ta-leading-caption = {
    set par(leading: 1.4em)
  }

  // 图注/表注样式
  #show figure.caption: it => {
    set par(leading: 1.4em)
    it
  }
  ```
- **与 DLP 对接规则**: 映射到 `leading: { caption: 1.4 }`。说明文字行高独立于正文和标题，形成第三档行高层级。与 TA-SCALE-007（caption）和 TA-SCALE-008（footnote）配合使用。

---

### TA-TRACKING-001: 标题字距（紧凑）

- **原子 ID**: TA-TRACKING-001
- **适用场景**: 大标题/展示标题/英雄区标题/封面标题
- **CSS 实现**:
  ```css
  .ta-tracking-heading {
    letter-spacing: -0.02em; /* 标题字距紧凑 */
  }

  /*
   * 标题字距 -0.02em（紧凑）
   * 大字号下字母间距视觉上会显得偏大，需要负字距补偿
   * 适用于 28px 以上的标题
   * 中文标题字距微调为 0.01em（中文不需要负字距）
   */
  :lang(zh) .ta-tracking-heading,
  .ta-tracking-heading.zh {
    letter-spacing: 0.01em;
  }
  ```
- **Typst 实现**:
  ```typst
  #let ta-tracking-heading = {
    // 西文标题字距 -0.02em 紧凑
    set text(tracking: -0.3pt)

    // 中文标题字距微宽松
    if text.lang == "zh" {
      set text(tracking: 0.15pt)
    }
  }

  #show heading: it => {
    set text(tracking: -0.3pt)
    if text.lang == "zh" { set text(tracking: 0.15pt) }
    it
  }
  ```
- **与 DLP 对接规则**: 映射到 `tracking: { heading: -0.02em, heading_zh: 0.01em }`。字距值与字号成反比——字号越大，负字距越明显。Taste-Skill 根据 `aesthetic_level` 微调：L1 → -0.01em（温和）、L2 → -0.02em（标准）、L3 → -0.03em（激进）。

---

### TA-TRACKING-002: 正文字距（默认）

- **原子 ID**: TA-TRACKING-002
- **适用场景**: 正文段落/列表文字/表格文字/所有常规阅读文字
- **CSS 实现**:
  ```css
  .ta-tracking-body {
    letter-spacing: 0; /* 正文字距默认，无调整 */
  }

  /*
   * 正文字距 0（默认）
   * 正文字号下字母间距视觉上刚好，不需要调整
   * 中英文均使用 0 字距
   */
  ```
- **Typst 实现**:
  ```typst
  #let ta-tracking-body = {
    // 正文字距 0 默认
    set text(tracking: 0pt)
  }

  // 正文默认字距
  #show: set text(tracking: 0pt)
  ```
- **与 DLP 对接规则**: 映射到 `tracking: { body: 0 }`。正文字距为排版基准值，不调整。所有 `output_type` 和 `design_language` 下均使用此默认值，不参与 Taste-Skill 仲裁。

---

### TA-TRACKING-003: 大写字距（宽松）

- **原子 ID**: TA-TRACKING-003
- **适用场景**: 标签/徽章/按钮文字/导航项/表头/全大写文字
- **CSS 实现**:
  ```css
  .ta-tracking-uppercase {
    letter-spacing: 0.05em; /* 大写字距宽松 */
    text-transform: uppercase;
  }

  /*
   * 大写字距 0.05em（宽松）
   * 全大写文字字母间距视觉上偏紧，需要正字距补偿
   * 适用于标签、徽章、按钮、导航等 UI 元素
   * 中文不适用（中文无大小写之分）
   */
  ```
- **Typst 实现**:
  ```typst
  #let ta-tracking-uppercase = {
    // 大写字距 0.05em 宽松
    set text(tracking: 0.8pt) // 0.05em × 16pt ≈ 0.8pt
    set text(style: "normal")
  }

  // 标签样式示例
  #let label(text-content) = {
    set text(tracking: 0.8pt, size: 13pt, weight: "medium")
    upper(text-content)
  }
  ```
- **与 DLP 对接规则**: 映射到 `tracking: { uppercase: 0.05em }`。当 UI 元素使用 `text-transform: uppercase` 时自动激活此字距。Taste-Skill 在 `design_language == "科技前沿"` 场景下优先使用大写标签（科技产品常用大写字母传递技术感）。

---

## 四、段落排版原子（TA-PARA）

> **融入来源**: editorialTypesetting-skill — 杂志级长文排版能力
> **DLP 对接**: 段落原子映射到 `visual_dna.font_scheme.paragraph` 字段，由 Taste-Skill 根据 `output_type` 和 `content_theme` 选择段落排版方案。

### TA-PARA-001: 段首缩进

- **原子 ID**: TA-PARA-001
- **适用场景**: 中文正文段落/学术文章/传统排版/印刷品
- **CSS 实现**:
  ```css
  .tapara-indent p {
    text-indent: 2em; /* 中文段首缩进 2字符 */
  }

  /* 英文无段首缩进 */
  .tapara-indent:lang(en) p {
    text-indent: 0;
  }

  /*
   * 中文段首缩进 2em（2个字符宽度）
   * 英文排版传统上不使用段首缩进，改用段间距分隔段落
   * 注意：首段不缩进（first-child 例外）
   */
  .tapara-indent p:first-child {
    text-indent: 0;
  }
  ```
- **Typst 实现**:
  ```typst
  #let ta-para-indent = {
    // 中文段首缩进 2em
    set par(first-line-indent: 2em)

    // 英文无段首缩进
    if text.lang == "en" {
      set par(first-line-indent: 0em)
    }
  }

  // 全局段落缩进设置
  #show: set par(first-line-indent: 2em)
  ```
- **与 DLP 对接规则**: 映射到 `paragraph: { indent: { zh: "2em", en: "0" } }`。当 `output_type == "research_report"` 且 `target_audience == "academic"` 时启用中文段首缩进。`output_type == "wechat_article"` 时不启用（公众号排版用段间距替代缩进）。融入 editorialTypesetting-skill 的中西文段落差异化处理。

---

### TA-PARA-002: 段间距

- **原子 ID**: TA-PARA-002
- **适用场景**: 所有正文段落之间/英文排版/现代 Web 排版/公众号文章
- **CSS 实现**:
  ```css
  .tapara-spacing p {
    margin-bottom: 1em; /* 段间距 1em */
    text-indent: 0;     /* 段间距模式不缩进 */
  }

  .tapara-spacing p:last-child {
    margin-bottom: 0;
  }

  /*
   * 段间距 1em，与行高 1.75em 区分
   * 段间距 > 行间距，视觉上明确区分段落边界
   * 1em 段间距 + 1.75em 行高 = 段落间视觉间隔约为行高的 1.57 倍
   */
  ```
- **Typst 实现**:
  ```typst
  #let ta-para-spacing = {
    // Typst 段间距通过 spacing 实现
    set par(spacing: 1em, first-line-indent: 0em)
  }

  // 段间距 1em
  #show: set par(spacing: 1em)
  ```
- **与 DLP 对接规则**: 映射到 `paragraph: { spacing: "1em" }`。与 TA-PARA-001 互斥——段首缩进和段间距不同时使用。当 `output_type == "wechat_article"` 或 `design_language == "科技前沿"` 时启用段间距模式（现代 Web 排版偏好段间距）。

---

### TA-PARA-003: 悬挂缩进

- **原子 ID**: TA-PARA-003
- **适用场景**: 列表项/参考文献/术语表/注释列表
- **CSS 实现**:
  ```css
  .tapara-hanging ul,
  .tapara-hanging ol {
    list-style-position: outside;
    padding-left: 1.5em;
  }

  .tapara-hanging li {
    text-indent: -1.5em; /* 悬挂缩进 */
    padding-left: 1.5em;
  }

  /* 参考文献悬挂缩进 */
  .tapara-hanging .references p {
    text-indent: -2em;
    padding-left: 2em;
  }

  /*
   * 悬挂缩进：首行突出，后续行缩进对齐
   * 适用于列表项和参考文献，使条目内容对齐
   */
  ```
- **Typst 实现**:
  ```typst
  #let ta-para-hanging = {
    // Typst 悬挂缩进通过 hanging-indent 实现
    set par(hanging-indent: 1.5em)
  }

  // 参考文献悬挂缩进
  #show bibliography: it => {
    set par(hanging-indent: 2em)
    it
  }
  ```
- **与 DLP 对接规则**: 映射到 `paragraph: { hanging_indent: "1.5em" }`。当 `output_type == "research_report"` 时自动应用于参考文献列表（GB/T 7714 格式要求悬挂缩进）。列表项场景下所有 `output_type` 均启用。

---

### TA-PARA-004: 首字下沉

- **原子 ID**: TA-PARA-004
- **适用场景**: 杂志风格/深度报道/专栏文章/文学叙事
- **CSS 实现**:
  ```css
  .tapara-dropcap p:first-of-type::first-letter {
    float: left;
    font-size: 3.5em;       /* 首字 3-4 行高 */
    line-height: 0.8;
    font-weight: 700;
    margin-right: 0.1em;
    margin-top: 0.05em;
    font-family: var(--font-heading);
  }

  /*
   * 首字下沉（Drop Cap）杂志风格
   * 首字大小 3.5em，约占 3-4 行高
   * line-height: 0.8 防止首字下沉影响行高计算
   * 仅用于文章首段，营造杂志感
   * 中文首字下沉同样适用
   */
  :lang(zh) .tapara-dropcap p:first-of-type::first-letter {
    font-size: 3em;
    margin-right: 0.15em;
  }
  ```
- **Typst 实现**:
  ```typst
  #let ta-para-dropcap(first-char) = {
    // Typst 首字下沉实现
    place(dx: -0.5em, dy: 0.1em)[
      #text(first-char, size: 3.5em, weight: "bold")
    ]
  }

  // 使用示例
  #let dropcap-article(body) = {
    // 首段首字下沉
    let first-paragraph = body.at(0)
    let first-char = first-paragraph.text.first()
    ta-para-dropcap(first-char)
    first-paragraph.slice(from: 1)
  }
  ```
- **与 DLP 对接规则**: 映射到 `paragraph: { dropcap: { enabled: false, size: "3.5em" } }`。默认不启用，当 `design_language == "人文温度"` 且 `aesthetic_level == "L3-沉浸"` 且 `content_theme` 含"杂志/专栏/叙事/文学"关键词时启用。融入 editorialTypesetting-skill 的杂志级排版能力。

---

### TA-PARA-005: 图文绕排

- **原子 ID**: TA-PARA-005
- **适用场景**: 图文混排/杂志插图/新闻配图/教程截图
- **CSS 实现**:
  ```css
  .tapara-wrap img {
    float: left;
    margin: 0 0.5em 0.5em 0;  /* 图片 float + margin 0.5em */
    max-width: 40%;
    border-radius: 4px;
  }

  .tapara-wrap img.right {
    float: right;
    margin: 0 0 0.5em 0.5em;
  }

  .tapara-wrap p {
    overflow: hidden; /* 触发 BFC，文字自动环绕 */
  }

  /*
   * 图文绕排：图片 float + margin 0.5em
   * 文字自动环绕图片
   * margin 0.5em 确保文字与图片之间有呼吸空间
   * 融入 editorialTypesetting-skill 的图文绕排规则
   */
  ```
- **Typst 实现**:
  ```typst
  #let ta-para-wrap(image-path, body, align: "left") = {
    // Typst 图文绕排通过 place + text 绕排实现
    if align == "left" {
      place(image(image-path, width: 40%), top: 0em, left: 0em, dx: 0em, dy: 0em)
      block(width: 55%, dx: 45%)[#body]
    } else {
      place(image(image-path, width: 40%), top: 0em, right: 0em)
      block(width: 55%)[#body]
    }
  }

  // 简化版：图片左浮文字右绕
  #show figure.where(kind: "float"): it => {
    place(it, float: true)
  }
  ```
- **与 DLP 对接规则**: 映射到 `paragraph: { text_wrap: { enabled: true, margin: "0.5em" } }`。当 `output_type == "wechat_article"` 或 `design_language == "人文温度"` 时启用。图片 margin 绑定 `visual_dna.grid_system` 的间距系统（0.5em ≈ 8px = 2×4px 基准）。融入 editorialTypesetting-skill 的图文绕排规则。

---

### TA-PARA-006: 多栏排版

- **原子 ID**: TA-PARA-006
- **适用场景**: 杂志排版/报纸版面/学术海报/长文分栏
- **CSS 实现**:
  ```css
  .tapara-multicol {
    column-count: 2;        /* 双栏排版 */
    column-gap: 2em;        /* 栏间距 2em */
    column-rule: 1px solid var(--color-border); /* 分隔线 */
  }

  .tapara-multicol.three-col {
    column-count: 3;
    column-gap: 1.5em;
  }

  /*
   * 多栏排版：column-count + column-gap
   * 中文 35-50 字/行 → 16px 字号下栏宽约 560-800px
   * 英文 45-75 字符/行 → 16px 字号下栏宽约 360-600px
   * 融入 typography-master-skill 的行长控制规则
   */
  @media (max-width: 767px) {
    .tapara-multicol {
      column-count: 1; /* 移动端强制单栏 */
    }
  }
  ```
- **Typst 实现**:
  ```typst
  #let ta-para-multicol(body, columns: 2) = {
    // Typst 多栏排版通过 columns 函数实现
    columns(columns, gutter: 2em, body)
  }

  // 双栏排版
  #show: columns.with(2, gutter: 2em)

  // 三栏排版
  #let three-col-doc = columns(3, gutter: 1.5em)[
    // 文档内容
  ]
  ```
- **与 DLP 对接规则**: 映射到 `paragraph: { multicolumn: { count: 2, gap: "2em" } }`。当 `output_type == "research_report"` 且页面尺寸为 A4 时默认双栏。栏宽受 typography-master-skill 行长控制约束：中文 35-50 字/行、英文 45-75 字符/行。移动端（`max-width: 767px`）强制折叠为单栏。

---

## 五、中西文混排原子（TA-MIX）

> **融入来源**: editorialTypesetting-skill — 中西文混排规则：中英文之间自动添加 1/4 em 间距
> **DLP 对接**: 混排原子映射到 `visual_dna.font_scheme.cjk_mix` 字段，所有含中文的 `output_type` 强制启用。

### TA-MIX-001: 中英文间距

- **原子 ID**: TA-MIX-001
- **适用场景**: 中英文混排/中文文档含英文术语/技术文档/学术文章
- **CSS 实现**:
  ```css
  .tamix-cn-en {
    /* CSS 原生不支持自动中英文间距，需通过 text-spacing 或 JS 处理 */
    text-spacing-trim: space-all;
    /* W3C CSS Text Module Level 4（草案阶段） */

    /* 兼容方案：通过正则替换插入 thin space */
    /* HTML 层面：中文<span class="thin-space"> </span>English */
  }

  .thin-space {
    display: inline-block;
    width: 0.25em; /* 1/4 em 间距 */
  }

  /*
   * 中英文之间自动添加 1/4 em 间距
   * 示例："使用Python开发" → "使用 Python 开发"
   * 融入 editorialTypesetting-skill 的中西文混排规则
   * 依据：GB/T 15834-2011《标点符号用法》
   */
  ```
- **Typst 实现**:
  ```typst
  #let ta-mix-cn-en = {
    // Typst 原生支持 CJK 与西文自动间距
    // 通过 set text 的 cjk-latin-spacing 控制
    set text(cjk-latin-spacing: 0.25em)

    // 或使用 Typst 内置的自动间距（推荐）
    // Typst 默认会在 CJK 与 Latin 字符间添加 1/4 em 间距
  }

  // 全局启用中英文自动间距
  #show: set text(cjk-latin-spacing: 0.25em)
  ```
- **与 DLP 对接规则**: 映射到 `cjk_mix: { cn_en_spacing: "0.25em" }`。当 `visual_dna.font_scheme` 检测到内容含中英文混排时强制启用。Typst 引擎原生支持此功能（`cjk-latin-spacing`），CSS 引擎需通过 `text-spacing` 属性或 JS 后处理实现。依据 GB/T 15834-2011 标准。

---

### TA-MIX-002: 中文与数字间距

- **原子 ID**: TA-MIX-002
- **适用场景**: 中文文档含数字/数据报告/统计文章/技术规格
- **CSS 实现**:
  ```css
  .tamix-cn-num {
    /* CSS 原生不支持自动中文与数字间距 */
    text-spacing-trim: space-all;
    /* W3C 草案属性 */

    /* 兼容方案：通过正则替换插入 thin space */
    /* "2024年" → "2024 年"（数字与中文之间） */
  }

  .num-space {
    display: inline-block;
    width: 0.25em; /* 1/4 em 间距 */
  }

  /*
   * 中文与数字之间自动添加 1/4 em 间距
   * 示例："2024年增长了15%" → "2024 年增长了 15%"
   * 融入 editorialTypesetting-skill 的中西文混排规则
   * 依据：GB/T 15834-2011《标点符号用法》
   */
  ```
- **Typst 实现**:
  ```typst
  #let ta-mix-cn-num = {
    // Typst 将数字视为 Latin 字符，cjk-latin-spacing 同样适用
    set text(cjk-latin-spacing: 0.25em)

    // Typst 自动处理：中文与数字（含阿拉伯数字）之间添加 1/4 em 间距
  }

  // 全局启用中文与数字自动间距
  #show: set text(cjk-latin-spacing: 0.25em)
  ```
- **与 DLP 对接规则**: 映射到 `cjk_mix: { cn_num_spacing: "0.25em" }`。与 TA-MIX-001 共享同一底层机制（数字在排版引擎中归类为 Latin 字符）。当 `output_type == "research_report"` 且含统计数据时强制启用。依据 GB/T 15834-2011 标准。

---

### TA-MIX-003: 标点挤压

- **原子 ID**: TA-MIX-003
- **适用场景**: 中文排版/连续标点场景/括号嵌套/引号叠加
- **CSS 实现**:
  ```css
  .tamix-punct-squeeze {
    /* CSS text-spacing（草案） */
    text-spacing-trim: trim-adjacent;
    /* 移除相邻标点间的多余间距 */

    /* 兼容方案：font-feature-settings */
    font-feature-settings: "halt" 1; /* 启用标点挤压 OpenType 特性 */
  }

  /*
   * 标点挤压：连续标点去除多余间距
   * 示例："（（嵌套））" → 挤压括号间距
   * 示例："……" → 省略号占位压缩
   * 中文标点符号本身带有全角间距，连续标点时需挤压
   * 融入 editorialTypesetting-skill 的标点挤压规则
   * 依据：GB/T 15834-2011《标点符号用法》
   */
  ```
- **Typst 实现**:
  ```typst
  #let ta-mix-punct-squeeze = {
    // Typst 原生支持中文标点挤压
    // 通过 set text 的 lang 和 region 自动启用
    set text(lang: "zh", region: "cn")

    // Typst 的 CJK 排版引擎自动处理标点挤压：
    // - 连续标点（如"。"和"」"）自动挤压间距
    // - 行首标点自动半角化
    // - 行尾标点自动全角化
  }

  // 全局启用中文标点挤压
  #show: set text(lang: "zh", region: "cn")
  ```
- **与 DLP 对接规则**: 映射到 `cjk_mix: { punct_squeeze: true }`。所有含中文的 `output_type` 强制启用。Typst 引擎通过 `lang: "zh"` 自动激活标点挤压；CSS 引擎依赖 `text-spacing-trim` 属性（浏览器支持度有限）或 OpenType `halt` 特性。依据 GB/T 15834-2011 标准。

---

### TA-MIX-004: 避头尾规则

- **原子 ID**: TA-MIX-004
- **适用场景**: 中文排版/所有中文段落/学术文章/公众号文章
- **CSS 实现**:
  ```css
  .tamix-kinsoku {
    /* CSS line-break 属性控制避头尾 */
    line-break: strict; /* 严格避头尾规则 */
    word-break: normal;

    /* CSS Text Module Level 3 */
    /* strict: 启用 CJK 避头尾规则 */
  }

  /*
   * 避头尾规则（kinsoku shori）：
   * 行首禁止字符：句号（。）、逗号（，）、顿号（、）、分号（；）、
   *              感叹号（！）、问号（？）、右引号（」』）」）、
   *              右括号（）〕】》）、省略号（……）等
   * 行尾禁止字符：左引号（「『「）、左括号（（〔【《）等
   *
   * 排版引擎须实现避头尾断行逻辑，确保上述字符不出现在行首或行尾
   * 融入 editorialTypesetting-skill 的避头尾规则
   * 依据：GB/T 15834-2011《标点符号用法》
   */
  ```
- **Typst 实现**:
  ```typst
  #let ta-mix-kinsoku = {
    // Typst 原生支持 CJK 避头尾规则
    // 设置中文语言后自动启用
    set text(lang: "zh", region: "cn")

    // Typst 的 CJK 排版引擎自动处理避头尾：
    // - 行首禁止字符自动移至上一行末尾
    // - 行尾禁止字符自动移至下一行开头
    // - 支持 GB/T 15834-2011 规定的全部避头尾字符
  }

  // 全局启用避头尾规则
  #show: set text(lang: "zh", region: "cn")
  #show: set par(justify: true) // 两端对齐配合避头尾
  ```
- **与 DLP 对接规则**: 映射到 `cjk_mix: { kinsoku: true }`。所有含中文的 `output_type` 强制启用。Typst 引擎通过 `lang: "zh"` 自动激活避头尾规则；CSS 引擎通过 `line-break: strict` 实现。与 TA-MIX-003（标点挤压）配合使用，共同确保中文排版规范性。依据 GB/T 15834-2011 标准。

---

## 六、融入内容来源标注

### 6.1 融入 editorialTypesetting-skill 的内容

| 融入能力 | 对应原子 | 融入说明 |
|---------|---------|---------|
| 杂志级长文排版：基线网格（baseline grid）系统 | TA-LEADING-001/002/003 | 所有行高原子对齐到 4px 基线网格，行高 × 字号的乘积取整为 4px 整数倍 |
| 中西文混排规则：中英文之间自动添加 1/4 em 间距 | TA-MIX-001 | 中英文之间自动插入 0.25em 间距，依据 GB/T 15834-2011 |
| 图文绕排规则：图片 float + margin 0.5em | TA-PARA-005 | 图片浮动后 margin 0.5em，文字自动环绕 |
| 杂志级首字下沉 | TA-PARA-004 | 首字 3-4 行高，杂志风格标志性排版手法 |
| 编辑式字重搭配 | TA-WEIGHT-004/006 | regular 标题 + regular 正文的编辑式排版，italic 强调 |

### 6.2 融入 typography-master-skill 的内容

| 融入能力 | 对应原子 | 融入说明 |
|---------|---------|---------|
| 字号层级：严格的 h1-h6 层级，每级差异 ≥ 4px | TA-SCALE-001 至 TA-SCALE-008 | 字号阶梯原子确保相邻标题层级差异 ≥ 4px（display→h1: 24px, h1→h2: 12px, h2→h3: 8px, h3→h4: 8px, h4→body: 4px） |
| 字重搭配：标题与正文的字重差异 ≥ 200 | TA-WEIGHT-001 至 TA-WEIGHT-006 | 字重搭配原子确保标题与正文字重差异 ≥ 200（豁免场景：奢侈品牌 light 标题、编辑式 regular 标题） |
| 行长控制：中文 35-50 字/行，英文 45-75 字符/行 | TA-PARA-006 | 多栏排版原子的栏宽受行长控制约束，确保每行字符数在可读性范围内 |

---

## 七、强制规则

1. **原子优先**: 所有渲染模块的排版参数必须从本原子库选取原子，不得自行声明排版数值。
2. **双轨实现**: 每个原子必须提供 CSS 和 Typst 双轨实现，确保跨引擎排版一致性。
3. **DLP 对接**: 每个原子必须通过 `visual_dna.font_scheme.typography_scale` 字段与 DLP 对接，由 Taste-Skill 仲裁。
4. **中英文双轨**: 中文按 1.2 倍放大规则，所有字号原子必须提供中英文双轨值。
5. **基线对齐**: 所有行高原子必须对齐到 4px 基线网格（editorialTypesetting-skill 基线网格规则）。
6. **层级差异**: 字号阶梯相邻层级差异 ≥ 4px（typography-master-skill 层级规则），字重搭配差异 ≥ 200（typography-master-skill 字重规则，含豁免场景）。
7. **中西文混排**: 所有含中文的 `output_type` 强制启用 TA-MIX-001 至 TA-MIX-004 原子（editorialTypesetting-skill 混排规则）。
8. **原子不可覆盖**: 任何渲染模块不得绕过原子库使用硬编码排版值，如需调整需通过 Taste-Skill 仲裁修改 `visual_dna`。

---

## 八、穷尽重试策略

### L1: 完整原子库可用
所有 30 个排版原子均可正常选取，CSS/Typst 双轨实现完整。

### L2: 部分原子不可用
- 穷尽尝试使用同类别其他原子替代
- 记录缺失原子 ID，使用最接近的原子质量保持
- 标注为"部分原子质量保持"输出

### L3: CSS/Typst 双轨实现部分缺失
- 穷尽尝试使用可用轨道实现（CSS 优先或 Typst 优先）
- 缺失轨道使用默认值兜底
- 标注为"单轨质量保持"输出

### L4: 原子库完全不可用
- 穷尽尝试使用 `output/typography-system.md` 的排版定义
- 使用 1.25 modular scale 字号阶梯 + 1.75/1.4 行高
- 标注为"穷尽重试排版"输出

### L5: 排版系统完全不可用
- 仅输出纯文本内容
- 无排版格式化
- 标注为"穷尽重试输出"

---

> 知识来源: editorialTypesetting-skill, typography-master-skill, rendering-pipeline/visual-dna.md, output/typography-system.md

© 阿洋
