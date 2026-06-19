> **作者**: 阿洋

# WeasyPrint 研究报告代码生成规范

> **模块标识**: `output/document-renderer`
> **职责**: 将结构化研究内容转换为 WeasyPrint 兼容的 HTML+CSS，通过 WeasyPrint Python API 渲染输出高质量 PDF 研究报告。WeasyPrint 原生支持 CSS Paged Media 规范（@page、@font-face、页眉页脚、自动目录），是学术报告 PDF 输出的理想引擎
> **CLI 命令**: `weasyprint input.html output.pdf`（或 Python API `HTML(string=html).write_pdf()`）
> **依赖**: `output/aesthetic-enhancer`, `output/illustration-generator`, `output/chart-renderer`, `plugins/weasyprint-adapter`

---

## 一、WeasyPrint PDF 渲染管线

### 1.1 管线总览

```
结构化研究内容
  → Step 1: 生成 WeasyPrint 兼容的 HTML+CSS
      - @page 规则（页面尺寸、边距、页眉页脚）
      - @font-face 字体嵌入
      - CSS 变量引用 aesthetic-enhancer.md 配色/字体
      - 自动目录（string-set + target-counter）
  → Step 2: 调用 WeasyPrint Python API 渲染为 PDF
      - HTML(string=html_content).write_pdf(output_path)
  → Step 3: 若 WeasyPrint 不可用 → 穷尽重试管线
      - Pandoc → HTML → Markdown → 纯文本
```

### 1.2 Step 1: 生成 WeasyPrint 兼容 HTML+CSS

#### 1.2.1 @page 规则

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
```

#### 1.2.2 @font-face 字体嵌入

```css
@font-face {
  font-family: 'Source Serif 4';
  src: url('output/fonts/SourceSerif4-Regular.otf') format('opentype');
  font-weight: 400;
  font-style: normal;
}

@font-face {
  font-family: 'Source Serif 4';
  src: url('output/fonts/SourceSerif4-Bold.otf') format('opentype');
  font-weight: 700;
  font-style: normal;
}

@font-face {
  font-family: 'Source Han Serif SC';
  src: url('output/fonts/SourceHanSerifSC-Regular.otf') format('opentype');
  font-weight: 400;
  font-style: normal;
}

@font-face {
  font-family: 'Source Han Serif SC';
  src: url('output/fonts/SourceHanSerifSC-Bold.otf') format('opentype');
  font-weight: 700;
  font-style: normal;
}

@font-face {
  font-family: 'Inter';
  src: url('output/fonts/Inter-Regular.otf') format('opentype');
  font-weight: 400;
  font-style: normal;
}

@font-face {
  font-family: 'Inter';
  src: url('output/fonts/Inter-Bold.otf') format('opentype');
  font-weight: 700;
  font-style: normal;
}

@font-face {
  font-family: 'JetBrains Mono';
  src: url('output/fonts/JetBrainsMono-Regular.otf') format('opentype');
  font-weight: 400;
  font-style: normal;
}
```

#### 1.2.3 页眉页脚

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
    content: "";
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

#### 1.2.4 自动目录

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

### 1.3 Step 2: 调用 WeasyPrint Python API

```python
from weasyprint import HTML, CSS

def render_pdf(html_content: str, output_path: str) -> None:
    HTML(string=html_content).write_pdf(output_path)
```

### 1.4 Step 3: 穷尽重试管线

```yaml
exhaust_retry_pipeline:
  level_1_weasyprint:
    condition: "WeasyPrint 已安装"
    action: "HTML(string=html_content).write_pdf(output_path)"
    output: "高质量 PDF（含 @page 规则、字体嵌入、页眉页脚、自动目录）"

  level_2_pandoc:
    condition: "WeasyPrint 不可用，Pandoc 已安装"
    action: "pandoc input.md -o output.pdf"
    output: "标准 PDF（无自定义 @page 规则）"

  level_3_html:
    condition: "Pandoc 不可用"
    action: "输出 HTML 文件"
    output: "可在浏览器中查看和打印的 HTML"

  level_4_markdown:
    condition: "仅需文本输出"
    action: "输出标准 Markdown 文件"
    output: "纯 Markdown 文本"

  level_5_plain_text:
    condition: "最简输出"
    action: "输出纯文本"
    output: "无格式的纯文本"
```

### 1.5 WeasyPrint 渲染管线（research_master / lecture_notes 首选）

- 输入：HTML + CSS 内联
- 处理：WeasyPrint 编译
- 输出：PDF（300dpi）
- 穷尽重试：WeasyPrint → Pandoc → HTML 纯文本

---

## 二、HTML 结构规范

### 2.1 文档骨架

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>{{TITLE}}</title>
  <style>
    /* @page 规则 */
    /* @font-face 字体嵌入 */
    /* CSS 变量（来自 aesthetic-enhancer.md） */
    /* 排版样式 */
  </style>
</head>
<body>
  <header class="cover">
    <h1>{{TITLE}}</h1>
    <p class="subtitle">{{SUBTITLE}}</p>
    <div class="meta">{{AUTHOR}} · {{DATE}}</div>
  </header>

  <nav class="toc">
    <h2>目录</h2>
    <!-- 自动目录 -->
  </nav>

  <main>
    <section id="chapter-1">
      <h2 string-set="chapter-title content()">第一章 引言</h2>
      <!-- 内容 -->
    </section>
  </main>

  <footer class="references">
    <h2>参考文献</h2>
    <!-- 参考文献 -->
  </footer>
</body>
</html>
```

### 2.2 CSS 变量映射（来自 aesthetic-enhancer.md）

```css
:root {
  --color-primary-500: #2196F3;
  --color-primary-700: #1976D2;
  --color-primary-900: #0D47A1;
  --color-accent: #e94560;
  --color-text-primary: #212121;
  --color-text-secondary: #757575;
  --color-background: #FFFFFF;
  --color-surface: #FAFAFA;
  --color-border: #E0E0E0;

  --font-heading: 'Inter', 'Helvetica Neue', sans-serif;
  --font-body: 'Source Serif 4', 'Georgia', serif;
  --font-code: 'JetBrains Mono', 'Consolas', monospace;

  --spacing-base: 1rem;
  --spacing-standard: 1.5rem;
  --spacing-block: 2rem;
}
```

---

## 三、多级标题结构

### 3.1 标题层级定义

```css
h1 {
  font-family: var(--font-heading);
  font-size: 28pt;
  font-weight: 700;
  color: var(--color-primary-900);
  margin-top: 2cm;
  margin-bottom: 0.5cm;
  page-break-before: always;
  string-set: chapter-title content();
}

h1:first-of-type {
  page-break-before: avoid;
}

h2 {
  font-family: var(--font-heading);
  font-size: 17pt;
  font-weight: 700;
  color: var(--color-primary-700);
  margin-top: 0.8cm;
  margin-bottom: 0.3cm;
}

h3 {
  font-family: var(--font-heading);
  font-size: 14pt;
  font-weight: 700;
  color: luma(40);
  margin-top: 0.6cm;
  margin-bottom: 0.2cm;
}

h4 {
  font-family: var(--font-heading);
  font-size: 12pt;
  font-weight: 700;
  color: luma(60);
  margin-top: 0.4cm;
  margin-bottom: 0.1cm;
}
```

### 3.2 标题编号格式

| 格式 | CSS counter 样式 | 示例 |
|------|-----------------|------|
| 阿拉伯数字 | `counter(h2) "." counter(h3) "." counter(h4)` | 1. 1.1 1.1.1 |
| 中文数字 | 自定义 counter-style | 一、(一)、1 |
| 无编号 | 不使用 counter | 纯文字标题 |

```css
body {
  counter-reset: h2-counter;
}

h2 {
  counter-reset: h3-counter;
  counter-increment: h2-counter;
}

h2::before {
  content: counter(h2-counter) ". ";
}

h3 {
  counter-reset: h4-counter;
  counter-increment: h3-counter;
}

h3::before {
  content: counter(h2-counter) "." counter(h3-counter) " ";
}

h4 {
  counter-increment: h4-counter;
}

h4::before {
  content: counter(h2-counter) "." counter(h3-counter) "." counter(h4-counter) " ";
}
```

---

## 四、数学公式

### 4.1 行内公式

```html
<p>勾股定理：<span class="math">a² + b² = c²</span>，其中 <span class="math">a, b</span> 为直角边，<span class="math">c</span> 为斜边。</p>
```

### 4.2 独立公式块

```html
<div class="equation" id="eq:sum">
  <span class="math">∑<sub>i=1</sub><sup>n</sup> i = n(n+1)/2</span>
  <span class="eq-number">(1)</span>
</div>
```

### 4.3 KaTeX 渲染（推荐）

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16/dist/katex.min.css">
<script src="https://cdn.jsdelivr.net/npm/katex@0.16/dist/katex.min.js"></script>

<p>勾股定理：$a^2 + b^2 = c^2$</p>

<div class="equation">
  $$\sum_{i=1}^{n} i = \frac{n(n+1)}{2}$$
</div>
```

---

## 五、数据表格

### 5.1 基础表格

```html
<table>
  <caption>2025年度各季度营收数据</caption>
  <thead>
    <tr>
      <th>季度</th>
      <th>营收（万元）</th>
      <th>同比增长</th>
      <th>环比增长</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Q1</td><td>1,250</td><td>+12.3%</td><td>+3.2%</td></tr>
    <tr><td>Q2</td><td>1,480</td><td>+15.7%</td><td>+18.4%</td></tr>
    <tr><td>Q3</td><td>1,320</td><td>+8.9%</td><td>−10.8%</td></tr>
    <tr><td>Q4</td><td>1,680</td><td>+22.1%</td><td>+27.3%</td></tr>
  </tbody>
</table>
```

### 5.2 带样式的表格

```css
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 10pt;
  margin: 1em 0;
}

table caption {
  font-weight: 600;
  margin-bottom: 0.5em;
  text-align: left;
}

table th {
  background: var(--color-primary-900);
  color: #fff;
  padding: 8pt 12pt;
  text-align: left;
  font-family: var(--font-heading);
}

table td {
  padding: 6pt 12pt;
  border-bottom: 1px solid var(--color-border);
}

table tbody tr:nth-child(even) {
  background: var(--color-surface);
}
```

### 5.3 三线表（学术论文标准）

```css
table.three-line {
  border-top: 2pt solid var(--color-text-primary);
  border-bottom: 2pt solid var(--color-text-primary);
}

table.three-line thead {
  border-bottom: 1pt solid var(--color-text-primary);
}

table.three-line th,
table.three-line td {
  border: none;
  padding: 6pt 12pt;
}
```

---

## 六、引用与文献标注

### 6.1 内部引用

```html
<section id="chapter-1">
  <h2 string-set="chapter-title content()">第一章 引言</h2>
  <p>如第一章所述...</p>
</section>

<figure id="fig:trend">
  <img src="./charts/revenue-trend.png" alt="数据趋势">
  <figcaption>图 1：数据趋势</figcaption>
</figure>
<p>参见 <a href="#fig:trend">图 1</a>。</p>
```

### 6.2 文献引用

```html
<p>张三（2025）提出了... <sup>[1]</sup> <sup>[2,3]</sup></p>

<footer class="references">
  <h2>参考文献</h2>
  <ol>
    <li>张三. 研究标题. 期刊名, 2025.</li>
    <li>李四. 研究标题. 期刊名, 2024.</li>
    <li>王五. 研究标题. 期刊名, 2023.</li>
  </ol>
</footer>
```

### 6.3 脚注

```html
<p>这是一个需要说明的断言。<a href="#fn1" class="footnote-ref">[1]</a></p>

<footer class="footnotes">
  <p id="fn1"><sup>1</sup> 这是脚注的详细说明。</p>
</footer>
```

---

## 七、WeasyPrint CLI 命令

### 7.1 基本编译

```bash
weasyprint input.html output.pdf
```

### 7.2 Python API 编译

```python
from weasyprint import HTML, CSS

HTML(string=html_content).write_pdf("output.pdf")

HTML(filename="input.html").write_pdf("output.pdf")

HTML(string=html_content).write_pdf(
    "output.pdf",
    stylesheets=[CSS(filename="custom.css")],
)
```

### 7.3 高级选项

```python
from weasyprint import HTML

HTML(string=html_content).write_pdf(
    "output.pdf",
    presentational_hints=True,
    optimize_images=True,
    jpeg_quality=90,
    dpi=300,
)
```

---

## 八、中文排版要点

### 8.1 中文字体配置

```css
body {
  font-family: 'Source Han Serif SC', 'Source Serif 4', serif;
  font-size: 11pt;
  line-height: 1.7;
  text-align: justify;
}

h1, h2, h3, h4, h5, h6 {
  font-family: 'Inter', 'Source Han Serif SC', sans-serif;
}
```

### 8.2 中文排版规则

```css
p {
  text-indent: 2em;
  text-align: justify;
  line-height: 1.7;
  orphans: 2;
  widows: 2;
}

@page {
  size: A4;
  margin: 2.5cm 2cm;
}
```

---

## 九、完整模板组合

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>研究报告</title>
<style>
:root {
  --color-primary-500: #2196F3;
  --color-primary-700: #1976D2;
  --color-primary-900: #0D47A1;
  --color-accent: #e94560;
  --color-text-primary: #212121;
  --color-text-secondary: #757575;
  --color-background: #FFFFFF;
  --color-surface: #FAFAFA;
  --color-border: #E0E0E0;
  --font-heading: 'Inter', 'Helvetica Neue', sans-serif;
  --font-body: 'Source Serif 4', 'Georgia', serif;
  --font-code: 'JetBrains Mono', 'Consolas', monospace;
}

@page {
  size: A4;
  margin: 2.5cm;
  @bottom-center { content: counter(page); font-size: 9pt; color: var(--color-text-secondary); }
  @top-center { content: string(doc-title); font-size: 9pt; color: var(--color-text-secondary); }
}
@page :first { @top-center { content: none; } @bottom-center { content: none; } }
@page toc { @top-center { content: "目录"; } @bottom-center { content: counter(page, lower-roman); } }

@font-face { font-family: 'Source Serif 4'; src: url('output/fonts/SourceSerif4-Regular.otf'); font-weight: 400; }
@font-face { font-family: 'Source Serif 4'; src: url('output/fonts/SourceSerif4-Bold.otf'); font-weight: 700; }
@font-face { font-family: 'Source Han Serif SC'; src: url('output/fonts/SourceHanSerifSC-Regular.otf'); font-weight: 400; }
@font-face { font-family: 'Source Han Serif SC'; src: url('output/fonts/SourceHanSerifSC-Bold.otf'); font-weight: 700; }
@font-face { font-family: 'Inter'; src: url('output/fonts/Inter-Regular.otf'); font-weight: 400; }
@font-face { font-family: 'Inter'; src: url('output/fonts/Inter-Bold.otf'); font-weight: 700; }

body {
  font-family: 'Source Han Serif SC', 'Source Serif 4', serif;
  font-size: 11pt;
  line-height: 1.7;
  color: var(--color-text-primary);
  text-align: justify;
}

h1, h2, h3, h4 { font-family: 'Inter', 'Source Han Serif SC', sans-serif; }

h1 { font-size: 22pt; font-weight: 700; color: var(--color-primary-900); page-break-before: always; string-set: chapter-title content(); }
h2 { font-size: 17pt; font-weight: 700; color: var(--color-primary-700); }
h3 { font-size: 14pt; font-weight: 700; }
h4 { font-size: 12pt; font-weight: 700; }

p { text-indent: 2em; margin-bottom: 0.5em; }

.cover { page-break-after: always; text-align: center; padding-top: 8cm; }
.cover h1 { font-size: 28pt; page-break-before: avoid; string-set: doc-title content(); }
.cover .subtitle { font-size: 16pt; color: var(--color-text-secondary); }
.cover .meta { font-size: 12pt; color: var(--color-text-secondary); margin-top: 2cm; }

.toc { page: toc; page-break-after: always; }
.toc-entry { display: flex; justify-content: space-between; padding: 4px 0; border-bottom: 1px dotted var(--color-border); }
.toc-entry a::after { content: target-counter(attr(href), page); float: right; }

table { width: 100%; border-collapse: collapse; margin: 1em 0; }
th { background: var(--color-primary-900); color: #fff; padding: 8pt 12pt; text-align: left; }
td { padding: 6pt 12pt; border-bottom: 1px solid var(--color-border); }

.references { page-break-before: always; }
</style>
</head>
<body>

<header class="cover">
  <h1>研究报告标题</h1>
  <p class="subtitle">副标题</p>
  <div class="meta">作者：阿洋 · 日期：2026年5月</div>
</header>

<nav class="toc">
  <h2>目录</h2>
  <div class="toc-entry"><a href="#chapter-1">1. 引言</a></div>
  <div class="toc-entry" style="padding-left:2em"><a href="#section-1-1">1.1 研究背景</a></div>
  <div class="toc-entry"><a href="#chapter-2">2. 方法</a></div>
  <div class="toc-entry"><a href="#chapter-3">3. 结果</a></div>
  <div class="toc-entry"><a href="#chapter-4">4. 讨论</a></div>
</nav>

<main>
  <section id="chapter-1">
    <h1 string-set="chapter-title content()">引言</h1>
    <p>正文内容...</p>
  </section>

  <section id="chapter-2">
    <h1 string-set="chapter-title content()">方法</h1>
    <p>正文内容...</p>
  </section>

  <section id="chapter-3">
    <h1 string-set="chapter-title content()">结果</h1>
    <p>正文内容...</p>
  </section>

  <section id="chapter-4">
    <h1 string-set="chapter-title content()">讨论</h1>
    <p>正文内容...</p>
  </section>
</main>

<footer class="references">
  <h2>参考文献</h2>
  <ol>
    <li>参考文献条目...</li>
  </ol>
</footer>

</body>
</html>
```

---

## 穷尽尝试输出规范

当 WeasyPrint 渲染环境不可用时，穷尽尝试所有可用引擎输出，确保任意环境下均能生成可读文档。

### 穷尽尝试触发条件

1. `weasyprint` Python 包不可用（未安装）
2. WeasyPrint 渲染错误且无法修复
3. 所需字体不可用且无法下载
4. 目标环境明确要求其他格式

### 穷尽重试管线

| 优先级 | 引擎 | 输出格式 | 条件 |
|--------|------|---------|------|
| 1 | WeasyPrint | 高质量 PDF | WeasyPrint 已安装 |
| 2 | Pandoc | 标准 PDF | `pandoc` 命令可用 |
| 3 | 浏览器打印 | HTML | 浏览器环境可用 |
| 4 | 纯 Markdown | .md 文件 | 任意环境 |
| 5 | 纯文本 | .txt 文件 | 最简环境 |

### Markdown 等效输出要求

| WeasyPrint HTML 元素 | Markdown 等效 |
|---------------------|-------------|
| `<h1>` | `# 一级标题` |
| `<h2>` | `## 二级标题` |
| `<table>` | Markdown 表格 + `*表：x*` |
| `<span class="math">` | `$...$` (LaTeX) |
| `<a href="#...">` | `[参见 §1](#sec-intro)` |
| `.footnotes` | `[^1]` + `[^1]: ...` |
| `.references ol` | 编号列表 `[1] ...` |
| `<img>` | `![alt](path)` |
| `<blockquote>` | `> ...` |

### Markdown 穷尽尝试模板结构

```markdown
# 研究报告标题

> **作者**：阿洋
> **日期**：2026年5月

---

## 目录

- [第一章 引言](#第一章-引言)
- [第二章 方法](#第二章-方法)
- ...

---

## 第一章 引言

正文内容...

---

## 参考文献

[1] ...
[2] ...
```

### 穷尽尝试质量要求

- 标题层级：严格按 H1→H2→H3 递进，不跳级
- 表格：使用标准 Markdown 表格语法，列对齐规范
- 代码：使用三反引号围栏 + 语言标识
- 图片：提供 alt 文本和可选的 title
- 公式：LaTeX 格式（`$...$` 行内 / `$$...$$` 独立块）
- 引用：脚注式标注 `[^N]`
- 字符编码：UTF-8，BOM 禁止（与框架编码规范一致）

## v3 渲染更新

### NRSF 集成
- T20 渲染从 NRSF-Full 对应 § 节提取研究内容
- 按 output-expansion-protocol.md 的章节展开密度规则展开
- 每章自检不通过时触发补研（见 write-while-research-protocol.md）

### T20c 可访问性检查
- 图片 alt 文本
- 表格标题行
- 标题层级连续性
- 链接描述性文本

### SHA-256 哈希
- 渲染完成后计算 NRSF-Full 的 SHA-256 哈希
- 写入输出文件元数据和 checkpoint_history

---
© 阿洋