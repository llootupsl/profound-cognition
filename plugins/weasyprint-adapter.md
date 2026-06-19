---
name: weasyprint-adapter
description: WeasyPrint 适配器 — 将 HTML+CSS 内容渲染为高质量 PDF，替代 Typst 作为 document-renderer 的首选 PDF 输出引擎
author: 阿洋
tags: [weasyprint, pdf, adapter, document-renderer, css]
---

# WeasyPrint 适配器

## 概述

本模块为 document-renderer 提供 WeasyPrint PDF 渲染适配器，将 WeasyPrint 的 HTML+CSS → PDF 渲染能力集成到文档输出管线中。WeasyPrint 原生支持 CSS Paged Media 规范（@page、@font-face、页眉页脚、自动目录），是学术报告 PDF 输出的理想引擎。与 aesthetic-enhancer.md 的配色/字体系统通过 CSS 变量无缝对接。

---

## 激活条件

```yaml
activation:
  condition: "document-renderer 输出格式 == PDF AND WeasyPrint 已安装"
  priority: "首选 PDF 渲染引擎 — 原生支持 CSS Paged Media"
  exhaust-retry: "若 WeasyPrint 不可用，穷尽重试到 Pandoc → HTML → Markdown → 纯文本"
```

---

## 安装与调用

### 安装

```bash
pip install weasyprint
```

### Python API 调用

```python
from weasyprint import HTML

def render_pdf(html_content: str, output_path: str) -> None:
    HTML(string=html_content).write_pdf(output_path)
```

### 高级调用（带样式表）

```python
from weasyprint import HTML, CSS

def render_pdf_with_styles(
    html_content: str,
    output_path: str,
    custom_css: str = None,
) -> None:
    stylesheets = [CSS(filename="weasyprint-base.css")]
    if custom_css:
        stylesheets.append(CSS(string=custom_css))

    HTML(string=html_content).write_pdf(
        output_path,
        stylesheets=stylesheets,
    )
```

---

## CSS 模板变量映射

### aesthetic-enhancer.md 配色 → CSS 变量

WeasyPrint 原生支持 CSS 自定义属性，aesthetic-enhancer.md 中定义的所有 CSS 变量可直接在 WeasyPrint 样式中使用：

```css
:root {
  /* 来自 aesthetic-enhancer.md 色彩系统 */
  --color-primary-500: #2196F3;
  --color-primary-700: #1976D2;
  --color-primary-900: #0D47A1;
  --color-secondary-500: #9C27B0;
  --color-accent: #e94560;
  --color-text-primary: #212121;
  --color-text-secondary: #757575;
  --color-background: #FFFFFF;
  --color-surface: #FAFAFA;
  --color-border: #E0E0E0;

  /* 来自 aesthetic-enhancer.md 字体系统 */
  --font-heading: 'Inter', 'Helvetica Neue', sans-serif;
  --font-body: 'Source Serif 4', 'Georgia', serif;
  --font-code: 'JetBrains Mono', 'Consolas', monospace;

  /* 来自 aesthetic-enhancer.md 间距系统 */
  --spacing-base: 1rem;
  --spacing-standard: 1.5rem;
  --spacing-block: 2rem;
}
```

### WeasyPrint 专用 CSS 变量

```css
:root {
  --pdf-page-size: A4;
  --pdf-margin-outer: 2.5cm;
  --pdf-margin-inner: 2.5cm;
  --pdf-header-height: 1.5cm;
  --pdf-footer-height: 1.5cm;
  --pdf-body-font-size: 11pt;
  --pdf-heading-color: var(--color-primary-900);
  --pdf-accent-color: var(--color-accent);
}
```

---

## @page 规则模板

### 基础页面设置

```css
@page {
  size: A4;
  margin: 2.5cm;

  @bottom-center {
    content: counter(page);
    font-family: var(--font-body);
    font-size: 9pt;
    color: var(--color-text-secondary);
  }

  @top-center {
    content: string(doc-title);
    font-family: var(--font-heading);
    font-size: 9pt;
    color: var(--color-text-secondary);
  }
}

@page :first {
  @top-center { content: none; }
  @bottom-center { content: none; }
}

@page toc {
  @top-center { content: "目录"; }
  @bottom-center { content: counter(page, lower-roman); }
}

@page blank {
  @top-center { content: none; }
  @bottom-center { content: none; }
}
```

### 页眉页脚模板

```css
@page content {
  @top-left {
    content: string(chapter-title);
    font-size: 8pt;
    color: var(--color-text-secondary);
  }
  @top-right {
    content: string(doc-title);
    font-size: 8pt;
    color: var(--color-text-secondary);
  }
  @bottom-left {
    content: "Profound Cognition";
    font-size: 8pt;
    color: var(--color-text-secondary);
  }
  @bottom-right {
    content: counter(page);
    font-size: 9pt;
    color: var(--color-text-secondary);
  }
}
```

---

## @font-face 字体嵌入

```css
@font-face {
  font-family: 'Source Serif 4';
  src: url('fonts/SourceSerif4-Regular.otf') format('opentype');
  font-weight: 400;
  font-style: normal;
}

@font-face {
  font-family: 'Source Serif 4';
  src: url('fonts/SourceSerif4-Bold.otf') format('opentype');
  font-weight: 700;
  font-style: normal;
}

@font-face {
  font-family: 'Source Serif 4';
  src: url('fonts/SourceSerif4-Italic.otf') format('opentype');
  font-weight: 400;
  font-style: italic;
}

@font-face {
  font-family: 'Inter';
  src: url('fonts/Inter-Regular.otf') format('opentype');
  font-weight: 400;
  font-style: normal;
}

@font-face {
  font-family: 'Inter';
  src: url('fonts/Inter-Bold.otf') format('opentype');
  font-weight: 700;
  font-style: normal;
}

@font-face {
  font-family: 'JetBrains Mono';
  src: url('fonts/JetBrainsMono-Regular.otf') format('opentype');
  font-weight: 400;
  font-style: normal;
}

@font-face {
  font-family: 'Source Han Serif SC';
  src: url('fonts/SourceHanSerifSC-Regular.otf') format('opentype');
  font-weight: 400;
  font-style: normal;
}

@font-face {
  font-family: 'Source Han Serif SC';
  src: url('fonts/SourceHanSerifSC-Bold.otf') format('opentype');
  font-weight: 700;
  font-style: normal;
}
```

---

## 自动目录生成

```css
.toc {
  page: toc;
  page-break-after: always;
}

.toc h2 {
  string-set: doc-title content();
}

.toc-entry {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  padding: 4px 0;
  border-bottom: 1px dotted var(--color-border);
}

.toc-entry a::after {
  content: target-counter(attr(href), page);
  float: right;
}
```

### HTML 目录结构

```html
<nav class="toc">
  <h2>目录</h2>
  <div class="toc-entry">
    <a href="#chapter-1">1. 引言</a>
  </div>
  <div class="toc-entry" style="padding-left: 2em;">
    <a href="#section-1-1">1.1 研究背景</a>
  </div>
</nav>
```

---

## 与 document-renderer 的集成

### 渲染管线

```yaml
rendering_pipeline:
  step_1_generate_html:
    method: "生成 WeasyPrint 兼容的 HTML+CSS"
    requirements:
      - "@page 规则（页面尺寸、边距、页眉页脚）"
      - "@font-face 字体嵌入"
      - "CSS 变量引用 aesthetic-enhancer.md 配色/字体"
      - "自动目录（string-set + target-counter）"
    output: "weasyprint_compatible_html"

  step_2_render_pdf:
    method: "调用 WeasyPrint Python API 渲染为 PDF"
    command: "HTML(string=html_content).write_pdf(output_path)"
    output: "output.pdf"

  step_3_exhaust-retry:
    method: "若 WeasyPrint 不可用，按优先级穷尽重试"
    chain: "WeasyPrint → Pandoc → HTML → Markdown → 纯文本"
```

---

## 错误处理

```yaml
error_handling:
  library_not_available:
    action: "穷尽重试到 Pandoc 渲染管线"
    log: "记录 WeasyPrint 不可用事件，标注 exhaust-retry_reason=weasyprint_not_installed"
    exhaust_retry_chain: "Pandoc → HTML → Markdown → 纯文本"

  font_not_found:
    action: "使用系统默认字体，记录警告"
    log: "记录字体缺失事件，标注 missing_font={font_name}"
    exhaust-retry: "serif → Times New Roman; sans-serif → Arial; monospace → Courier New"

  css_parse_error:
    action: "跳过错误规则，使用剩余有效 CSS 继续渲染"
    log: "记录 CSS 解析错误，标注 error_line={line_number}"

  render_timeout:
    action: "终止渲染，穷尽重试到 Pandoc"
    log: "记录渲染超时事件，标注 exhaust-retry_reason=weasyprint_render_timeout"
    timeout: 120000  # ms

  output_too_large:
    action: "分块渲染后合并"
    log: "记录输出过大事件，标注 estimated_size={size}"
```

---

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| v1.0 | 2026-05-28 | 初始发布：WeasyPrint 适配器 + CSS 变量映射 + @page 规则模板 |

---

© 阿洋


---

## 穷尽重试策略

```yaml
exhaust_retry:
  L1_FULL:
    condition: "WeasyPrint 可用 + 自定义字体可用"
    behavior: "完整HTML+CSS→PDF渲染 + @page规则 + @font-face嵌入 + 自动目录"

  L2_PARTIAL_DATA:
    condition: "WeasyPrint 可用但自定义字体缺失"
    behavior: "WeasyPrint渲染 + 系统默认字体 + 标注[SYSTEM-FONT]"

  L3_TEXT_ONLY:
    condition: "WeasyPrint 不可用"
    behavior: "穷尽尝试到 Pandoc PDF渲染 + 标注[INTERNAL_REASONING]"

  L4_SERVICE_DOWN:
    condition: "所有PDF渲染工具不可用"
    behavior: "HTML内嵌样式/Markdown纯文本 + 标注[TEXT-ONLY]"
```
