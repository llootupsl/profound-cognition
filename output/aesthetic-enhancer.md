> **作者**: 阿洋

# UIR 可执行排版引擎

> **模块标识**: `output/aesthetic-enhancer`
> **职责**: 为所有输出模块提供可执行的排版引擎规则。以 YAML 配色声明为源头，经 CSS 自定义属性映射，注入 WeasyPrint / Marp / HTML 三种排版引擎，确保跨格式视觉一致性
> **依赖**: `output/typography-system`（排版数值权威来源）
> **被依赖**: 所有输出模块

---

## 一、排版引擎选择与渲染路由矩阵

### 1.1 3 分类渲染链穷尽尝试矩阵

> 渲染策略：穷尽尝试所有可用引擎，不设首选/穷尽重试替代/回退层级。每条渲染链均为独立可用路径，按引擎可用性穷尽尝试直至成功。

| 成品类型 | 渲染链 A | 渲染链 B | 渲染链 C | 渲染链 D |
|---------|---------|---------|---------|---------|
| **research_report** | Typst 0.13+ → PDF | WeasyPrint CSS → PDF | HTML 内嵌 CSS → 浏览器打印 | Markdown 纯文本 |
| **wechat_article** | HTML 内嵌 CSS → 公众号排版 | Typst → PDF 导出 | Pandoc → Markdown | Markdown 纯文本 |
| **course_material** | Marp → Typst PDF（lecture） | Marp → PPTX | HTML 内嵌 CSS | Markdown 纯文本 |

### 1.2 渲染链详情

#### 渲染链 A：Typst（research_report 穷尽尝试路径之一）
```
typst compile --root output/typst-templates/ --font-path output/fonts research-report.typ output.pdf
```
- 模板：`output/typst-templates/research-report.typ`
- 覆盖：全息框架 3 部分 × 14 维度 × 40 方面
- 能力卡片：47 张 PHASE_CARDS 嵌入

#### 渲染链 B：WeasyPrint（PDF 穷尽尝试路径之一）
```
weasyprint input.html output.pdf -s weasyprint-style.css
```
- 支持 CSS Paged Media Level 3（@page、@bottom-center、页码计数器）
- 支持 CSS 自定义属性（:root 变量）
- 支持 break-before / break-after / break-inside: avoid 分页控制

#### 渲染链 C：HTML 内嵌 CSS（wechat_article 穷尽尝试路径之一）
- 零依赖，纯文本生成
- 模板：`output/html-templates/research-report.html` / `wechat-article.html`
- 内嵌 Mermaid.js + Prism.js

#### 渲染链 D：Markdown 纯文本（穷尽尝试最终路径）
- 不依赖任何 CSS 或外部样式
- 信息层次通过 Markdown 语意元素表达
- 确保终端/CLI 环境下的可读性

### 1.3 图生成工具路由

> **铁律**: 所有图类型必须通过代码生成（SVG / Mermaid / Canvas / CSS），**禁止使用任何 AI 生图 API**（Flux / SD / Qwen-Image / DALL-E / Midjourney）。

| 图类型 | 首选工具（代码生成） | 穷尽重试工具（代码生成） |
|--------|---------|---------|
| 框架图 / 概念图 | 内联 SVG（手绘矢量） | Mermaid graph |
| 数据图表 | Observable Plot + ECharts | 内联 SVG 柱状图/折线图模板 |
| 概念插图 | 内联 SVG（VCA 风格注入） | Mermaid graph + ASCII 兜底 |
| 思维导图 | Markmap | Mermaid mindmap |
| 知识图谱 | 内联 SVG（d3-force 风格） | Mermaid graph |
| 时间线 | 内联 SVG（时间线模板） | Mermaid timeline |
| 决策路径图 | 内联 SVG（决策树模板） | Mermaid flowchart |
| 系统/因果结构图 | 内联 SVG（因果回路模板） | Mermaid graph |

> 详见 [illustration-generator.md](./illustration-generator.md) §0 核心铁律与 §4 配图类型 → 生成方式路由表。

### 1.4 引擎选择决策树

```
成品类型？
├─ research_report → 穷尽尝试 Typst → WeasyPrint → HTML → Markdown
├─ wechat_article → 穷尽尝试 HTML（内嵌CSS）→ Typst → Pandoc → Markdown
└─ course_material
   ├─ lecture → 穷尽尝试 Marp → Typst PDF → HTML → Markdown
   └─ video_script → 纯文本 + Manim 动画脚本
```

---

## 二、排版数值引用

> 以下所有数值均引用自 [typography-system.md](./typography-system.md)，本文件不另行定义。

### 2.1 引用摘要

| 属性 | 引用值 | 来源章节 |
|------|--------|---------|
| 字号缩放比 | 1.25 modular scale | typography-system §一 |
| h1 | 2.441rem | typography-system §1.2 |
| h2 | 1.953rem | typography-system §1.2 |
| h3 | 1.563rem | typography-system §1.2 |
| h4 | 1.25rem | typography-system §1.2 |
| body | 1rem | typography-system §1.2 |
| small | 0.8rem | typography-system §1.2 |
| 网格列数 | 12 | typography-system §二 |
| 网格 gutter | 24px | typography-system §二 |
| 元素间距 | 1rem（1×） | typography-system §三 |
| 段落间距 | 1.5rem（1.5×） | typography-system §三 |
| 章节间距 | 2rem（2×） | typography-system §三 |
| 正文行宽 | 680px | typography-system §四 |
| 图表行宽 | 960px | typography-system §四 |
| 正文行高 | 1.75 | typography-system §五 |
| 标题行高 | 1.4 | typography-system §五 |

---

## 三、DLP design_tokens → CSS 变量映射

### 3.1 YAML 配色声明

> 完整 YAML 格式见 typography-system §6.2，此处列出核心声明。

```yaml
colors:
  primary:
    50:  "#E3F2FD"
    100: "#BBDEFB"
    200: "#90CAF9"
    300: "#64B5F6"
    400: "#42A5F5"
    500: "#2196F3"
    600: "#1E88E5"
    700: "#1976D2"
    800: "#1565C0"
    900: "#0D47A1"
  secondary:
    50:  "#F3E5F5"
    100: "#E1BEE7"
    200: "#CE93D8"
    300: "#BA68C8"
    400: "#AB47BC"
    500: "#9C27B0"
    600: "#8E24AA"
    700: "#7B1FA2"
    800: "#6A1B9A"
    900: "#4A148C"
  neutral:
    white:    "#FFFFFF"
    gray-50:  "#FAFAFA"
    gray-100: "#F5F5F5"
    gray-200: "#EEEEEE"
    gray-300: "#E0E0E0"
    gray-400: "#BDBDBD"
    gray-500: "#9E9E9E"
    gray-600: "#757575"
    gray-700: "#616161"
    gray-800: "#424242"
    gray-900: "#212121"
    black:    "#000000"
  semantic:
    success: { light: "#E8F5E9", main: "#4CAF50", dark: "#2E7D32", text: "#1B5E20" }
    warning: { light: "#FFF3E0", main: "#FF9800", dark: "#E65100", text: "#BF360C" }
    error:   { light: "#FFEBEE", main: "#F44336", dark: "#C62828", text: "#B71C1C" }
    info:    { light: "#E3F2FD", main: "#2196F3", dark: "#1565C0", text: "#0D47A1" }
  aliases:
    background:     "neutral.white"
    surface:        "neutral.gray-50"
    text-primary:   "neutral.gray-900"
    text-secondary: "neutral.gray-600"
    text-disabled:  "neutral.gray-400"
    border:         "neutral.gray-300"
    border-light:   "neutral.gray-200"
    link:           "primary.600"
    link-hover:     "primary.800"
```

### 3.2 映射规则

DLP design_tokens → CSS 变量映射规则：

```
R1: DLP color_palette.primary → --color-primary
R2: DLP color_palette.secondary → --color-secondary
R3: DLP color_palette.accent → --color-accent
R4: DLP color_palette.neutral → --color-neutral
R5: DLP color_palette.background → --color-background
R6: DLP color_palette.text → --color-text
R7: DLP font_stack.western → --font-western
R8: DLP font_stack.chinese → --font-chinese
R9: DLP font_stack.mono → --font-mono
R10: DLP spacing_system.base → --spacing-base
R11: DLP grid_system.columns → --grid-columns
R12: DLP grid_system.gutter → --grid-gutter
R13: DLP radius_shadow.card → --radius-card
R14: DLP radius_shadow.shadow → --shadow-default
```

---

## 四、CSS 变量定义块（引擎共享层）

### 4.1 根变量 `:root` DLP 动态生成

CSS :root 变量从 DLP color_palette 字段动态生成：

```css
:root {
  --color-primary: <DLP.color_palette.primary>;
  --color-secondary: <DLP.color_palette.secondary>;
  --color-accent: <DLP.color_palette.accent>;
  --color-neutral: <DLP.color_palette.neutral>;
  --color-background: <DLP.color_palette.background>;
  --color-text: <DLP.color_palette.text>;
  --font-western: <DLP.font_stack.western>;
  --font-chinese: <DLP.font_stack.chinese>;
  --font-mono: <DLP.font_stack.mono>;
  --spacing-base: <DLP.spacing_system.base>;
  --grid-columns: <DLP.grid_system.columns>;
  --grid-gutter: <DLP.grid_system.gutter>;
  --radius-card: <DLP.radius_shadow.card>;
  --shadow-default: <DLP.radius_shadow.shadow>;
}
```

### 4.2 暗色模式覆写（R3 映射）

```css
[data-theme="dark"] {
  --color-background:     #121212;
  --color-surface:        #1E1E1E;
  --color-text-primary:   #E0E0E0;
  --color-text-secondary: #9E9E9E;
  --color-text-disabled:  #616161;
  --color-border:         #424242;
  --color-border-light:   #333333;
  --color-link:           #64B5F6;
  --color-link-hover:     #90CAF9;

  --shadow-xs:    0 1px 2px rgba(0, 0, 0, 0.3);
  --shadow-sm:    0 1px 3px rgba(0, 0, 0, 0.4), 0 1px 2px rgba(0, 0, 0, 0.3);
  --shadow-md:    0 4px 6px rgba(0, 0, 0, 0.4), 0 2px 4px rgba(0, 0, 0, 0.3);
  --shadow-lg:    0 10px 15px rgba(0, 0, 0, 0.5), 0 4px 6px rgba(0, 0, 0, 0.3);
  --shadow-xl:    0 20px 25px rgba(0, 0, 0, 0.5), 0 10px 10px rgba(0, 0, 0, 0.3);
}
```

---

## 五、WeasyPrint CSS 排版规则

### 5.1 页面设定

```css
@page {
  size: A4;
  margin: 2.5cm 2.5cm 2.5cm 3cm;

  @top-center {
    content: "研究报告";
    font-family: var(--font-body);
    font-size: 9pt;
    color: var(--color-text-secondary);
  }

  @bottom-center {
    content: counter(page);
    font-family: var(--font-body);
    font-size: 9pt;
    color: var(--color-text-secondary);
  }

  @bottom-right {
    content: "© 阿洋";
    font-family: var(--font-body);
    font-size: 8pt;
    color: var(--color-text-disabled);
  }
}

@page :first {
  margin-top: 0;
  @top-center { content: none; }
  @bottom-center { content: none; }
  @bottom-right { content: none; }
}
```

### 5.2 文档排版规则

```css
body {
  font-family: var(--font-body);
  font-size: var(--ts-scale-body);
  line-height: var(--ts-leading-body);
  color: var(--color-text-primary);
  background: var(--color-background);
  max-width: var(--ts-line-width-body);
  margin: 0 auto;
}

h1 {
  font-family: var(--font-heading);
  font-size: var(--ts-scale-h1);
  font-weight: var(--weight-bold);
  line-height: var(--ts-leading-heading);
  color: var(--color-primary-900);
  margin-top: var(--ts-whitespace-section);
  margin-bottom: var(--ts-whitespace-paragraph);
  break-after: avoid;
}

h2 {
  font-family: var(--font-heading);
  font-size: var(--ts-scale-h2);
  font-weight: var(--weight-semibold);
  line-height: var(--ts-leading-heading);
  color: var(--color-primary-800);
  margin-top: var(--ts-whitespace-paragraph);
  margin-bottom: var(--ts-whitespace-element);
  break-after: avoid;
}

h3 {
  font-family: var(--font-heading);
  font-size: var(--ts-scale-h3);
  font-weight: var(--weight-semibold);
  line-height: var(--ts-leading-heading);
  color: var(--color-primary-700);
  margin-top: var(--ts-whitespace-paragraph);
  margin-bottom: var(--ts-whitespace-element);
  break-after: avoid;
}

h4 {
  font-family: var(--font-heading);
  font-size: var(--ts-scale-h4);
  font-weight: var(--weight-medium);
  line-height: var(--ts-leading-heading);
  color: var(--color-text-primary);
  margin-top: var(--ts-whitespace-paragraph);
  margin-bottom: var(--ts-whitespace-element);
  break-after: avoid;
}

p {
  margin-bottom: var(--ts-whitespace-paragraph);
  orphans: 3;
  widows: 3;
}

blockquote {
  border-left: 4px solid var(--color-primary-500);
  padding: var(--ts-whitespace-element) var(--ts-whitespace-paragraph);
  margin: var(--ts-whitespace-paragraph) 0;
  background: var(--color-surface);
  color: var(--color-text-secondary);
  font-style: italic;
  break-inside: avoid;
}

pre {
  font-family: var(--font-code);
  font-size: 0.875rem;
  line-height: var(--ts-leading-code);
  background: var(--color-gray-100);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-sm);
  padding: var(--ts-whitespace-element);
  overflow-x: auto;
  break-inside: avoid;
}

code {
  font-family: var(--font-code);
  font-size: 0.875rem;
  background: var(--color-gray-100);
  padding: 2px 4px;
  border-radius: var(--radius-xs);
}

table {
  width: 100%;
  max-width: var(--ts-line-width-chart);
  border-collapse: collapse;
  margin: var(--ts-whitespace-paragraph) 0;
  break-inside: avoid;
}

th {
  border-bottom: 2px solid var(--color-gray-600);
  font-weight: var(--weight-semibold);
  text-align: left;
  padding: var(--ts-whitespace-element);
}

td {
  border-bottom: 1px solid var(--color-border);
  padding: var(--ts-whitespace-element);
}

tr:nth-child(even) td {
  background: var(--color-surface);
}

a {
  color: var(--color-link);
  text-decoration: none;
}

a:hover {
  color: var(--color-link-hover);
  text-decoration: underline;
}

figure {
  margin: var(--ts-whitespace-paragraph) 0;
  break-inside: avoid;
}

figcaption {
  font-size: var(--ts-scale-small);
  color: var(--color-text-secondary);
  text-align: center;
  margin-top: var(--ts-whitespace-element);
}

img {
  max-width: 100%;
  break-inside: avoid;
}

h1 { break-before: page; }
h1:first-of-type { break-before: auto; }
```

### 5.3 WeasyPrint CLI 执行

```bash
weasyprint input.html output.pdf -s weasyprint-style.css
```

`-s` 参数指定外部样式表，与 HTML 内嵌样式叠加生效。

---

## 六、Marp 主题 CSS 排版规则

### 6.1 主题定义

```css
/* @theme profound-cognition */

@import-default;

/* ===== 全局变量 ===== */
:root {
  --color-primary-500: #2196F3;
  --color-primary-800: #1565C0;
  --color-primary-900: #0D47A1;
  --color-gray-50:     #FAFAFA;
  --color-gray-100:    #F5F5F5;
  --color-gray-300:    #E0E0E0;
  --color-gray-600:    #757575;
  --color-gray-900:    #212121;

  --font-heading: 'Inter', 'Helvetica Neue', sans-serif;
  --font-body:    'Source Serif 4', 'Georgia', serif;
  --font-code:    'JetBrains Mono', 'Consolas', monospace;

  --ts-scale-h1: 2.441rem;
  --ts-scale-h2: 1.953rem;
  --ts-scale-h3: 1.563rem;
  --ts-scale-h4: 1.25rem;
  --ts-scale-body: 1rem;
  --ts-scale-small: 0.8rem;
  --ts-leading-heading: 1.4;
  --ts-leading-body: 1.75;
}

/* ===== 幻灯片基础 ===== */
section {
  font-family: var(--font-body);
  font-size: var(--ts-scale-body);
  line-height: var(--ts-leading-body);
  color: var(--color-gray-900);
  background: #FFFFFF;
  padding: 40px 60px;
}

/* ===== 标题样式 ===== */
section h1 {
  font-family: var(--font-heading);
  font-size: var(--ts-scale-h1);
  font-weight: 700;
  line-height: var(--ts-leading-heading);
  color: var(--color-primary-900);
}

section h2 {
  font-family: var(--font-heading);
  font-size: var(--ts-scale-h2);
  font-weight: 600;
  line-height: var(--ts-leading-heading);
  color: var(--color-primary-800);
}

section h3 {
  font-family: var(--font-heading);
  font-size: var(--ts-scale-h3);
  font-weight: 600;
  line-height: var(--ts-leading-heading);
  color: var(--color-gray-900);
}

section h4 {
  font-family: var(--font-heading);
  font-size: var(--ts-scale-h4);
  font-weight: 500;
  line-height: var(--ts-leading-heading);
}

/* ===== 代码块 ===== */
section pre {
  font-family: var(--font-code);
  font-size: var(--ts-scale-small);
  line-height: 1.5;
  background: var(--color-gray-100);
  border: 1px solid var(--color-gray-300);
  border-radius: 4px;
  padding: 16px;
}

section code {
  font-family: var(--font-code);
  font-size: var(--ts-scale-small);
}

/* ===== 引用 ===== */
section blockquote {
  border-left: 4px solid var(--color-primary-500);
  padding: 12px 20px;
  background: var(--color-gray-50);
  color: var(--color-gray-600);
  font-style: italic;
}

/* ===== 表格 ===== */
section table {
  width: 100%;
  border-collapse: collapse;
}

section th {
  border-bottom: 2px solid var(--color-gray-600);
  font-weight: 600;
  text-align: left;
  padding: 8px 12px;
}

section td {
  border-bottom: 1px solid var(--color-gray-300);
  padding: 8px 12px;
}

/* ===== 封面页 ===== */
section.cover {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

section.cover h1 {
  font-size: 2.441rem;
}

/* ===== 结束页 ===== */
section.end {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}
```

### 6.2 Marp Markdown 使用方式

```markdown
---
theme: profound-cognition
marp: true
size: 16:9
paginate: true
---

---
layout: cover
---

# 研究报告标题

## 副标题

阿洋 · 2026年5月

---

# 第一章 引言

正文内容...

---
layout: end
---

# 感谢

联系方式
```

### 6.3 Marp CLI 执行

```bash
npx @marp-team/marp-cli slides.md --pdf --theme ./profound-cognition.css
npx @marp-team/marp-cli slides.md --pptx --theme ./profound-cognition.css
npx @marp-team/marp-cli slides.md --html --theme ./profound-cognition.css
```

---

## 七、Typst set 规则等效定义

### 7.1 完整 Typst 样式设定

```typst
/* ===== Marp CSS 样式系统（与 CSS 变量等效） =====

// --- 页面 ---
#set page(
  paper: "a4",
  margin: (x: 2.5cm, y: 2.5cm),
  numbering: "1",
)

// --- 字体 ---
#set text(
  font: ("Source Han Serif SC", "Source Serif 4"),
  size: 11pt,
  lang: "zh",
  exhaust-retry: true,
)

// --- 段落 ---
#set par(
  leading: 0.7em,
  justify: true,
  first-line-indent: 2em,
)

// --- 标题 ---
#set heading(numbering: "1.1.1")

#show heading.where(level: 1): it => {
  pagebreak(weak: true)
  v(0.8cm)
  text(size: 22pt, weight: "bold", fill: rgb("#0D47A1"))[#it.body]
  v(0.3cm)
  line(length: 100%, stroke: 1pt + rgb("#E0E0E0"))
}

#show heading.where(level: 2): it => {
  v(0.5cm)
  text(size: 17pt, weight: "semibold", fill: rgb("#1565C0"))[#it.body]
  v(0.2cm)
}

#show heading.where(level: 3): it => {
  v(0.4cm)
  text(size: 14pt, weight: "semibold", fill: rgb("#1976D2"))[#it.body]
  v(0.15cm)
}

// --- 代码 ---
#show raw: it => {
  set text(font: "JetBrains Mono", size: 9pt)
  block(
    fill: rgb("#F5F5F5"),
    inset: 12pt,
    radius: 4pt,
    width: 100%,
    it,
  )
}

// --- 引用 ---
#show quote: it => {
  block(
    fill: rgb("#F5F5F5"),
    inset: (x: 20pt, y: 8pt),
    stroke: (left: 4pt + rgb("#2196F3")),
    radius: (right: 8pt, bottom: 8pt),
    set text(style: "italic", fill: rgb("#757575")),
    it.body,
  )
}

// --- 表格 ---
#show table: it => {
  set table(
    stroke: (x, y) => (
      top: 0.5pt + rgb("#E0E0E0"),
      bottom: if y == 0 { 1.5pt + rgb("#757575") } else { 0.5pt + rgb("#E0E0E0") },
    ),
    fill: (x, y) => if calc.rem(y, 2) == 0 { rgb("#FAFAFA") } else { white },
    inset: 8pt,
    align: (left,) * it.columns.len(),
  )
  it
}

// --- 链接 ---
#show link: it => {
  set text(fill: rgb("#1E88E5"))
  it
}

// --- 脚注 ---
#set footnote.entry(
  separator: repeat[.] * 15,
)
```

### 7.2 颜色映射表（CSS → Typst）

| CSS 变量 | Typst 函数 | 色值 | YAML 来源 |
|---------|-----------|------|----------|
| `--color-primary-900` | `rgb("#0D47A1")` | #0D47A1 | `colors.primary.900` |
| `--color-primary-800` | `rgb("#1565C0")` | #1565C0 | `colors.primary.800` |
| `--color-primary-700` | `rgb("#1976D2")` | #1976D2 | `colors.primary.700` |
| `--color-primary-500` | `rgb("#2196F3")` | #2196F3 | `colors.primary.500` |
| `--color-primary-400` | `rgb("#42A5F5")` | #42A5F5 | `colors.primary.400` |
| `--color-primary-300` | `rgb("#64B5F6")` | #64B5F6 | `colors.primary.300` |
| `--color-primary-200` | `rgb("#90CAF9")` | #90CAF9 | `colors.primary.200` |
| `--color-primary-100` | `rgb("#BBDEFB")` | #BBDEFB | `colors.primary.100` |
| `--color-primary-50`  | `rgb("#E3F2FD")` | #E3F2FD | `colors.primary.50` |
| `--color-gray-900` | `rgb("#212121")` | #212121 | `colors.neutral.gray-900` |
| `--color-gray-800` | `rgb("#424242")` | #424242 | `colors.neutral.gray-800` |
| `--color-gray-700` | `rgb("#616161")` | #616161 | `colors.neutral.gray-700` |
| `--color-gray-600` | `rgb("#757575")` | #757575 | `colors.neutral.gray-600` |
| `--color-gray-500` | `rgb("#9E9E9E")` | #9E9E9E | `colors.neutral.gray-500` |
| `--color-gray-400` | `rgb("#BDBDBD")` | #BDBDBD | `colors.neutral.gray-400` |
| `--color-gray-300` | `rgb("#E0E0E0")` | #E0E0E0 | `colors.neutral.gray-300` |
| `--color-gray-200` | `rgb("#EEEEEE")` | #EEEEEE | `colors.neutral.gray-200` |
| `--color-gray-100` | `rgb("#F5F5F5")` | #F5F5F5 | `colors.neutral.gray-100` |
| `--color-gray-50`  | `rgb("#FAFAFA")` | #FAFAFA | `colors.neutral.gray-50` |
| `--color-white`    | `white` | #FFFFFF | `colors.neutral.white` |
| `--color-success-main` | `rgb("#4CAF50")` | #4CAF50 | `colors.semantic.success.main` |
| `--color-warning-main` | `rgb("#FF9800")` | #FF9800 | `colors.semantic.warning.main` |
| `--color-error-main`   | `rgb("#F44336")` | #F44336 | `colors.semantic.error.main` |
| `--color-info-main`    | `rgb("#2196F3")` | #2196F3 | `colors.semantic.info.main` |

### 7.3 间距映射表（CSS → Marp CSS）

| CSS 变量 | 值 | Marp CSS 等效 | typography-system 来源 |
|---------|-----|-----------|----------------------|
| `--ts-whitespace-element` | 16px | `1em` / `16pt` | §三 元素间距 |
| `--ts-whitespace-paragraph` | 24px | `1.5em` / `24pt` | §三 段落间距 |
| `--ts-whitespace-section` | 32px | `2em` / `32pt` | §三 章节间距 |

---

## 八、TypeScript 接口定义（兼容层）

### 8.1 设计令牌接口

```typescript
interface DesignTokens {
  colors: {
    primary: Record<string, string>;
    secondary: Record<string, string>;
    success: { light: string; main: string; dark: string; text: string };
    warning: { light: string; main: string; dark: string; text: string };
    error: { light: string; main: string; dark: string; text: string };
    info: { light: string; main: string; dark: string; text: string };
    neutral: Record<string, string>;
    aliases: Record<string, string>;
  };
  typography: {
    fontFamily: {
      display: string;
      heading: string;
      body: string;
      code: string;
      quote: string;
    };
    scale: {
      h1: string;
      h2: string;
      h3: string;
      h4: string;
      body: string;
      small: string;
    };
    leading: {
      body: number;
      heading: number;
      code: number;
    };
  };
  whitespace: {
    element: string;
    paragraph: string;
    section: string;
  };
  lineWidth: {
    body: string;
    chart: string;
  };
  grid: {
    columns: number;
    gutter: string;
  };
}
```

### 8.2 YAML → CSS 转换器

```typescript
function yamlToCssVars(yaml: DesignTokens): string {
  const lines: string[] = [':root {'];

  for (const [level, value] of Object.entries(yaml.colors.primary)) {
    lines.push(`  --color-primary-${level}: ${value};`);
  }
  for (const [level, value] of Object.entries(yaml.colors.secondary)) {
    lines.push(`  --color-secondary-${level}: ${value};`);
  }
  for (const [name, ref] of Object.entries(yaml.colors.aliases)) {
    const cssVar = resolveAlias(ref, yaml.colors);
    lines.push(`  --color-${name}: ${cssVar};`);
  }

  lines.push('}');
  return lines.join('\n');
}

function resolveAlias(aliasPath: string, colors: any): string {
  const parts = aliasPath.split('.');
  const category = parts[0];
  const level = parts[1];
  return `var(--color-${level})`;
}
```

---

## 九、响应式媒体查询

```css
@media (max-width: 767px) {
  :root {
    --ts-scale-h1: 1.953rem;
    --ts-scale-h2: 1.563rem;
    --ts-scale-h3: 1.25rem;
    --ts-scale-body: 0.9375rem;
    --ts-line-width-body: 100%;
    --ts-grid-gutter: var(--ts-grid-gutter-compact);
  }
}

@media (min-width: 768px) and (max-width: 1023px) {
  :root {
    --ts-scale-h1: 2.441rem;
    --ts-scale-h2: 1.563rem;
    --ts-scale-h3: 1.25rem;
    --ts-line-width-body: 720px;
  }
}

@media (min-width: 1024px) and (max-width: 1439px) {
  :root {
    --ts-line-width-body: 680px;
  }
}

@media (min-width: 1440px) {
  :root {
    --ts-line-width-body: 680px;
  }
}

@media print {
  :root {
    --color-background: white;
    --color-text-primary: black;
    --shadow-none: none;
    --border-none: 0;
  }
  .no-print { display: none; }
}
```

---

## 十、主题预设（CSS 类定义）

### 10.1 默认主题

```css
[data-theme="default"] {
  --color-primary-500: #2196F3;
  --color-secondary-500: #9C27B0;
  --font-heading: 'Inter', 'Helvetica Neue', sans-serif;
  --font-body: 'Source Serif 4', 'Georgia', serif;
}
```

### 10.2 学术主题

```css
[data-theme="academic"] {
  --color-primary-500: #1A237E;
  --color-secondary-500: #4A148C;
  --font-heading: 'Georgia', 'Times New Roman', serif;
  --font-body: 'Georgia', 'Times New Roman', serif;
  --radius-md: 0;
  --shadow-none: none;
}
```

### 10.3 极简主题

```css
[data-theme="minimal"] {
  --color-primary-500: #212121;
  --color-secondary-500: #757575;
  --font-heading: 'Helvetica Neue', Arial, sans-serif;
  --font-body: 'Helvetica Neue', Arial, sans-serif;
  --weight-heading: 300;
  --radius-sm: 2px;
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
}
```

### 10.4 创意主题

```css
[data-theme="creative"] {
  --color-primary-500: #FF6B6B;
  --color-secondary-500: #4ECDC4;
  --font-heading: 'Playfair Display', Georgia, serif;
  --font-body: 'Source Sans Pro', 'Open Sans', sans-serif;
  --weight-heading: 800;
  --radius-lg: 12px;
  --shadow-lg: 0 10px 20px rgba(0,0,0,0.1);
}
```

---

## 十一、打印样式表 (`print.css`)

```css
@media print {
  @page {
    size: A4;
    margin: 2.5cm 2.5cm 2.5cm 3cm;
    @top-center { content: "研究报告"; }
    @bottom-center { content: counter(page); }
  }

  body {
    font-family: var(--font-body);
    font-size: 11pt;
    line-height: var(--ts-leading-body);
    color: var(--color-text-primary);
  }

  h1 { font-size: 22pt; page-break-before: always; }
  h2 { font-size: 17pt; }
  h3 { font-size: 14pt; }
  h4 { font-size: 12pt; }

  pre, code {
    font-family: var(--font-code);
    font-size: 9pt;
    background: var(--color-gray-100);
    border: 1px solid var(--color-border);
  }

  blockquote {
    border-left: 4px solid var(--color-primary-500);
    padding-left: 20px;
    color: var(--color-text-secondary);
    font-style: italic;
  }

  table { border-collapse: collapse; width: 100%; }
  th { border-bottom: 2px solid var(--color-gray-600); }
  td { border-bottom: 1px solid var(--color-border); }

  a { color: var(--color-link); text-decoration: underline; }
  a[href^="http"]::after { content: " (" attr(href) ")"; }

  .no-print, nav, .toc-toggle, .theme-toggle { display: none; }
}
```

---

## 十二、穷尽尝试输出规范

当 CSS 环境和 WeasyPrint/Marp 渲染环境均不可用时，穷尽尝试 **内联样式的纯 HTML/Markdown**，确保基本可读性。

### 穷尽尝试触发条件

1. 目标环境不支持 CSS 变量（如纯文本邮件客户端）
2. 输出目标为无样式 Markdown（如 GitHub 原始文件）
3. WeasyPrint/Marp 渲染失败且无法修复
4. 渲染环境为终端/CLI 纯文本

### 风格穷尽尝试要求

| 元素 | 穷尽尝试方案 |
|------|----------|
| 标题 | 使用 `#` / `##` 层级标识，用空行区分 |
| 强调 | `**加粗**` / `*斜体*` |
| 代码 | `` `代码` `` / ` ``` ` 代码块 |
| 引用 | `>` 前缀 |
| 表格 | ASCII 表格 或 对齐的文本 |
| 图片 | Alt 文本 + 路径说明 |
| 颜色 | 不依赖颜色传达信息 |
| 间距 | 空行分隔段落和章节 |

### 穷尽尝试质量要求

- 不依赖任何 CSS 或外部样式
- 信息层次通过 Markdown 语意元素表达
- 关键信息不使用颜色编码
- 确保终端/CLI 环境下的可读性
- 图片提供完整 alt 文本
---

## 十三、图标系统集成（Iconify + Tabler Icons）

### 13.1 Iconify 接入

> 图标系统由 `plugins/iconify-adapter.md` 统一管理，本模块负责将其注入各排版引擎。

默认图标集：**Tabler Icons**（https://tabler-icons.io）

### 13.2 图标使用方式

```html
<!-- HTML 嵌入 -->
<span class="iconify" data-icon="tabler:brain"></span>
<span class="iconify" data-icon="tabler:chart-bar"></span>
<span class="iconify" data-icon="tabler:file-text"></span>

<!-- CSS 定制 -->
<style>
  .iconify {
    color: var(--color-primary-500);
    font-size: 1.25rem;
    vertical-align: -0.125em;
  }
</style>
```

### 13.3 常用图标映射

| 功能 | Tabler Icon | 用法 |
|------|------------|------|
| 研究/分析 | `tabler:brain` | 认知分析标记 |
| 数据/图表 | `tabler:chart-bar` | 数据可视化标记 |
| 文档/报告 | `tabler:file-text` | 文档输出标记 |
| 警告/注意 | `tabler:alert-triangle` | 风险提示 |
| 检查/确认 | `tabler:check` | 验证通过 |
| 链接/来源 | `tabler:link` | 引用/参考 |
| 搜索/查询 | `tabler:search` | 检索标记 |
| 设置/配置 | `tabler:settings` | 配置项标记 |
| 用户/人设 | `tabler:user` | 人设相关 |
| 时间/历史 | `tabler:clock` | 时间线标记 |

### 13.4 图标穷尽重试

当 Iconify CDN 不可用时：
1. 穷尽尝试 Unicode 符号（如 🔍 → 搜索、📊 → 图表、⚠ → 警告）
2. 穷尽尝试纯文本标签

### 13.5 WeasyPrint 中的图标

WeasyPrint 不执行 JavaScript，需使用 SVG 内联或 Unicode 符号替代：

```html
<!-- Unicode 穷尽尝试 -->
<span class="icon-exhaust-retry">📊</span>

<!-- 或使用 CSS content -->
<span class="icon-exhaust-retry icon-chart"></span>
```

```css
.icon-exhaust-retry.icon-chart::before {
  content: "📊";
}
```

### 13.6 Marp 中的图标

Marp 幻灯片中直接使用 Unicode 符号或 Emoji：

```markdown
📊 数据概览
🔍 关键发现
⚠️ 风险提示
✅ 验证通过
```

---

## 十四、TA 排版原子库对接

CSS 排版规则从 TA 库（typography-atoms.md）检索：

- 字号阶梯 → TA-SCALE-001~008（中英文双轨，中文 1.2 倍放大）
- 字重搭配 → TA-WEIGHT-001~006
- 行高与字距 → TA-LEADING-001~003 + TA-TRACKING-001~003
- 段落排版 → TA-PARA-001~006（段首缩进、段间距、悬挂缩进、首字下沉、图文绕排、多栏排版）
- 中西文混排 → TA-MIX-001~004（中英文间距、中文与数字间距、标点挤压、避头尾）

每个 TA 原子提供 CSS 实现代码，直接注入渲染输出。

---

## 十五、DLP font_stack 字段注入 CSS font-family

DLP font_stack 字段直接注入 CSS font-family：

```css
body {
  font-family: var(--font-western), var(--font-chinese), var(--font-mono);
}

h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-western), var(--font-chinese);
}

code, pre {
  font-family: var(--font-mono);
}
```

---

---
© 阿洋
