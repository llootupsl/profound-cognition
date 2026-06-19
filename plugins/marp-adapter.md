---
name: marp-adapter
description: Marp CLI 适配器 — 将结构化内容转换为 Marp Markdown 幻灯片，渲染为 PPTX/PDF/HTML 格式
author: 阿洋
tags: [marp, slides, adapter, slide-renderer, pptx]
---

# Marp CLI 适配器

## 概述

本模块为 slide-renderer 提供 Marp CLI 幻灯片渲染适配器，将 6 种幻灯片类型映射为 Marp Markdown + 主题 CSS，通过 Marp CLI 渲染为 PPTX/PDF/HTML 格式。Marp 使用标准 Markdown 语法 + YAML 指令，学习成本低，输出质量高，与 aesthetic-enhancer.md 的配色系统通过主题 CSS 无缝对接。

---

## 激活条件

```yaml
activation:
  condition: "slide-renderer 输出格式 ∈ {PPTX, PDF, HTML-SLIDES} AND Marp CLI 已安装"
  priority: "首选幻灯片渲染引擎 — 标准 Markdown 语法，输出质量高"
  exhaust-retry: "若 Marp 不可用，穷尽重试到 HTML 幻灯片 → Markdown 大纲"
```

---

## 安装与调用

### 安装

```bash
npm install -g @marp-team/marp-cli
```

### CLI 调用

```bash
# 渲染为 PPTX
npx @marp-team/marp-cli slides.md --pptx -o output.pptx

# 渲染为 PDF
npx @marp-team/marp-cli slides.md --pdf -o output.pdf

# 渲染为 HTML
npx @marp-team/marp-cli slides.md --html -o output.html

# 指定主题 CSS
npx @marp-team/marp-cli slides.md --theme theme.css --pptx -o output.pptx

# 允许本地文件引用
npx @marp-team/marp-cli slides.md --allow-local-files --pptx -o output.pptx
```

---

## 6 种幻灯片类型的 Marp Markdown 模板

### 1. 封面幻灯片

```markdown
---
marp: true
theme: profound-cognition
paginate: true
---

<!-- _class: cover -->
<!-- _paginate: false -->

# {{TITLE}}

## {{SUBTITLE}}

<div class="meta">
  {{AUTHOR}} · {{DATE}}
</div>
```

### 2. 目录幻灯片

```markdown
---

<!-- _class: toc -->

# 目录

1. **第一章** — 研究背景与问题
2. **第二章** — 方法论
3. **第三章** — 核心发现
4. **第四章** — 数据分析
5. **第五章** — 结论与建议
```

### 3. 内容幻灯片

```markdown
---

<!-- _class: content -->

# 章节标题

- **要点一**：详细描述文字
- **要点二**：详细描述文字
- **要点三**：详细描述文字

> 关键引用或补充说明
```

### 4. 图表幻灯片

```markdown
---

<!-- _class: chart -->

# 数据趋势分析

![width:700px](./charts/revenue-trend.png)

*图：2025年度各季度营收趋势*
```

### 5. 引用幻灯片

```markdown
---

<!-- _class: quote -->

> "数据驱动的决策需要可靠的来源和严谨的验证"

— 方法论原则
```

### 6. 总结幻灯片

```markdown
---

<!-- _class: summary -->

# 核心结论

| # | 结论 | 置信度 |
|---|------|--------|
| 1 | 结论一描述 | 高 |
| 2 | 结论二描述 | 中 |
| 3 | 结论三描述 | 高 |

**下一步行动**：建议与展望
```

---

## 主题 CSS 定义

### profound-cognition 主题（配色来自 aesthetic-enhancer.md）

```css
/* @theme profound-cognition */

@import default;

section {
  font-family: 'Inter', 'Helvetica Neue', 'PingFang SC', sans-serif;
  color: #212121;
  background: #ffffff;
  font-size: 28px;
  line-height: 1.6;
}

section.cover {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  color: #ffffff;
  text-align: center;
  justify-content: center;
}

section.cover h1 {
  font-size: 48px;
  font-weight: 700;
  color: #ffffff;
  letter-spacing: 0.02em;
}

section.cover h2 {
  font-size: 24px;
  font-weight: 300;
  color: rgba(255, 255, 255, 0.85);
}

section.cover .meta {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.7);
  margin-top: 32px;
}

section.toc {
  background: #fafbfc;
}

section.toc h1 {
  color: #0D47A1;
  font-size: 36px;
}

section.toc ol {
  font-size: 22px;
  line-height: 2;
}

section.content h1 {
  color: #0D47A1;
  font-size: 36px;
  border-bottom: 3px solid #e94560;
  padding-bottom: 12px;
}

section.content ul {
  font-size: 24px;
  line-height: 1.8;
}

section.content strong {
  color: #1976D2;
}

section.chart {
  text-align: center;
  justify-content: center;
}

section.chart h1 {
  color: #0D47A1;
  font-size: 32px;
  text-align: center;
}

section.quote {
  background: #fafbfc;
  justify-content: center;
  text-align: center;
}

section.quote blockquote {
  font-family: 'Source Serif 4', 'Georgia', serif;
  font-size: 32px;
  font-style: italic;
  color: #424242;
  border-left: 4px solid #e94560;
  padding-left: 24px;
  max-width: 80%;
  margin: 0 auto;
}

section.summary h1 {
  color: #0D47A1;
  font-size: 36px;
}

section.summary table {
  font-size: 20px;
  width: 100%;
  border-collapse: collapse;
}

section.summary th {
  background: #0D47A1;
  color: #ffffff;
  padding: 12px 16px;
  text-align: left;
}

section.summary td {
  padding: 10px 16px;
  border-bottom: 1px solid #e0e0e0;
}

section.summary strong {
  color: #e94560;
}

header {
  font-size: 12px;
  color: #9e9e9e;
  text-align: right;
}

footer {
  font-size: 12px;
  color: #9e9e9e;
}

section::after {
  content: attr(data-marpit-pagination) ' / ' attr(data-marpit-pagination-total);
  font-size: 14px;
  color: #9e9e9e;
  text-align: right;
  padding-right: 24px;
}

section.cover::after {
  content: none;
}
```

---

## 与 slide-renderer 的集成

### 渲染管线

```yaml
rendering_pipeline:
  step_1_map_slides:
    method: "将 6 种幻灯片类型映射为 Marp Markdown + 主题 CSS"
    slide_type_mapping:
      cover: "<!-- _class: cover -->"
      toc: "<!-- _class: toc -->"
      content: "<!-- _class: content -->"
      chart: "<!-- _class: chart -->"
      quote: "<!-- _class: quote -->"
      summary: "<!-- _class: summary -->"
    output: "slides.md"

  step_2_render:
    method: "调用 Marp CLI 渲染为 PPTX/PDF/HTML"
    command: "npx @marp-team/marp-cli slides.md --theme theme.css --pptx -o output.pptx"
    output: "output.pptx | output.pdf | output.html"

  step_3_exhaust-retry:
    method: "若 Marp 不可用，按优先级穷尽重试"
    chain: "Marp CLI → HTML 幻灯片 → Markdown 大纲"
```

---

## 错误处理

```yaml
error_handling:
  cli_not_available:
    action: "穷尽重试到 HTML 幻灯片渲染"
    log: "记录 Marp CLI 不可用事件，标注 exhaust-retry_reason=marp_not_installed"
    exhaust_retry_chain: "HTML 幻灯片 → Markdown 大纲"

  render_failure:
    action: "穷尽重试到 HTML 幻灯片渲染"
    log: "记录 Marp 渲染失败事件，标注 exhaust-retry_reason=marp_render_failed"

  theme_css_error:
    action: "使用 Marp 默认主题继续渲染"
    log: "记录主题 CSS 错误，标注 exhaust-retry_reason=marp_theme_error"

  output_format_unsupported:
    action: "穷尽重试到 PDF 格式输出"
    log: "记录格式不支持事件，标注 unsupported_format={format}"

  image_not_found:
    action: "跳过图片，使用占位文字替代"
    log: "记录图片缺失事件，标注 missing_image={path}"

  font_not_found:
    action: "使用系统默认字体"
    log: "记录字体缺失事件，标注 missing_font={font_name}"
```

---

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| v1.0 | 2026-05-28 | 初始发布：Marp CLI 适配器 + 6 种幻灯片模板 + 主题 CSS |

---

© 阿洋


---

## 穷尽重试策略

```yaml
exhaust_retry:
  L1_FULL:
    condition: "Marp CLI 可用 + 主题CSS正常"
    behavior: "完整Marp Markdown→PPTX/PDF/HTML渲染 + 自定义主题"

  L2_PARTIAL_DATA:
    condition: "Marp CLI 可用但主题CSS异常"
    behavior: "Marp默认主题渲染 + 标注[DEFAULT-THEME]"

  L3_TEXT_ONLY:
    condition: "Marp CLI 不可用"
    behavior: "穷尽尝试到 HTML幻灯片渲染 + 标注[HTML-SLIDES]"

  L4_SERVICE_DOWN:
    condition: "所有幻灯片渲染工具不可用"
    behavior: "Markdown大纲 + 标注[MARKDOWN-ONLY]"
```
