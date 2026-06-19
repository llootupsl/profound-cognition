<!-- 作者：阿洋 -->

# DLP-springer: Springer 设计语言画像

> **锚定真实世界**: Springer Nature 期刊 2024 年版式
> **融入来源技能**: Rxiv-Maker（Springer 风格、留白克制、预印本规范）
> **族归属**: academic-journal（学术期刊族）
> **索引**: 详见 `README.md` 获取 DLP 库完整清单与检索规范

---

## YAML frontmatter（12 字段完整定义）

```yaml
---
name: "DLP-springer"
anchor: "Springer Nature 期刊 2024 年版式"
family: "academic-journal"

color_palette:
  primary: "#1A1A1A"       # 主色 - 近黑正文（Springer 正文略柔于纯黑）
  secondary: "#005CAB"     # 辅色 - Springer蓝（期刊标识与栏目分隔色）
  accent: "#0066CC"        # 强调色 - 链接蓝（正文超链接与 DOI 链接色）
  neutral: "#6C757D"       # 中性色 - 次要文字灰（图注、脚注、元数据）
  background: "#FFFFFF"    # 背景色 - 纯白背景（印刷标准）
  text: "#1A1A1A"          # 文本色 - 近黑正文（与主色一致）

typography_scale:
  h1: "22px/1.375rem"      # 文章主标题（Article Title）
  h2: "16px/1rem"          # 一级章节标题（Section Heading）
  h3: "14px/0.875rem"      # 二级章节标题（Subsection Heading）
  h4: "12px/0.75rem"       # 三级章节标题（Sub-subsection Heading）
  body: "10pt/13.33px"     # 正文（Springer 单栏预印本布局，10pt 为印刷标准）
  caption: "8pt/10.67px"   # 图注（图标题与图说明文字）
  footnote: "7pt/9.33px"   # 脚注（参考文献与补充说明）

font_stack:
  western: '"Latin Modern Roman", "Computer Modern", "Times New Roman", serif'
  chinese: '"宋体", "SimSun", serif'
  monospace: '"Latin Modern Mono", "Courier New", monospace'

font_weight_pairing:
  heading: "bold(700)"     # 标题粗体
  body: "regular(400)"     # 正文常规
  emphasis: "italic(400)"  # 强调斜体（物种名、基因名、术语首次出现）

spacing_system:
  base: "4px"
  scale: "4/8/12/16/24/32px"

grid_system:
  columns: "单栏"           # Springer 预印本为单栏（与 Nature/Science/IEEE 双栏不同）
  column_width: "16cm"     # 单栏列宽（预印本标准宽度）
  gutter: "N/A"            # 单栏无槽宽
  margin: "2.5cm"          # 页边距（略宽于 Nature/Science 的 2cm，确保阅读舒适）
  breakpoint: "N/A(印刷媒介)"

radius_shadow:
  radius: "0px"            # 直角（学术期刊强制直角）
  shadow: "none"           # 无阴影（印刷媒介无 elevation 概念）

motion_curve:
  easing: "N/A(印刷媒介)"
  duration: "N/A"

applicable_scenarios:
  - "学术论文"
  - "期刊投稿"
  - "预印本"
  - "科学研究"
---
```

---

## 一、配色方案详解

### 1.1 6 色板（锚定 Springer Nature 期刊 2024 实际版式）

| 色板角色 | 十六进制 | RGB | 用途 | 锚定来源 |
|---------|---------|-----|------|---------|
| 主色 Primary | `#1A1A1A` | rgb(26,26,26) | 正文文字、标题、图表轴线 | Springer 正文印刷标准 |
| 辅色 Secondary | `#005CAB` | rgb(0,92,171) | 期刊标识、栏目分隔线、章节标题装饰 | Springer 官方蓝 |
| 强调色 Accent | `#0066CC` | rgb(0,102,204) | 超链接、DOI 链接、引用跳转 | Springer 数字版链接色 |
| 中性色 Neutral | `#6C757D` | rgb(108,117,125) | 图注、脚注、作者署名、元数据 | Springer 图注灰 |
| 背景色 Background | `#FFFFFF` | rgb(255,255,255) | 页面背景、图表背景 | Springer 印刷白 |
| 文本色 Text | `#1A1A1A` | rgb(26,26,26) | 正文（与主色一致） | Springer 正文色 |

### 1.2 配色使用规则

1. **正文**: 使用 `#1A1A1A`（近黑），不得使用纯黑 `#000000`（Springer 数字版略柔）
2. **标题**: 使用 `#1A1A1A`，章节标题可使用 Springer 蓝 `#005CAB` 作为装饰色（如标题下划线）
3. **链接**: 使用 `#0066CC`，下划线 1px solid `#0066CC`
4. **图注**: 使用 `#6C757D`，字号 8pt，与正文 `#1A1A1A` 形成层级
5. **图表轴线**: 使用 `#1A1A1A`，线宽 1px（数据线 1.5px）
6. **禁止渐变**: Springer 期刊零渐变，所有色块为纯色

### 1.3 与 DLP-nature / DLP-science / DLP-ieee 的配色差异

| 色板角色 | DLP-nature | DLP-science | DLP-ieee | DLP-springer | 差异说明 |
|---------|-----------|-------------|----------|-------------|---------|
| 主色 | `#000000` | `#1A1A1A` | `#000000` | `#1A1A1A` | Springer 与 Science 一致（近黑） |
| 辅色 | `#E60012` | `#F47C20` | `#00629B` | `#005CAB` | Springer 蓝略深于 IEEE 蓝 |
| 强调色 | `#0066CC` | `#0066CC` | `#0066CC` | `#0066CC` | 一致（学术链接蓝标准） |
| 中性色 | `#6C757D` | `#6C757D` | `#6C757D` | `#6C757D` | 一致（学术图注灰标准） |

---

## 二、字体方案详解

### 2.1 字体族

| 用途 | 西文字体 | 中文字体 | CSS font-family |
|------|---------|---------|----------------|
| 标题 | Latin Modern Roman | 宋体 / SimSun | `"Latin Modern Roman", "Computer Modern", "Times New Roman", "宋体", "SimSun", serif` |
| 正文 | Latin Modern Roman | 宋体 / SimSun | `"Latin Modern Roman", "Computer Modern", "Times New Roman", "宋体", "SimSun", serif` |
| 代码 | Latin Modern Mono | — | `"Latin Modern Mono", "Courier New", monospace` |

### 2.2 字号阶梯（单栏布局，预印本标准）

| 层级 | 字号 | 行高 | 字重 | 用途 |
|------|------|------|------|------|
| H1 | 22px / 1.375rem | 1.3 | 700 | 文章主标题 |
| H2 | 16px / 1rem | 1.4 | 700 | 一级章节标题 |
| H3 | 14px / 0.875rem | 1.5 | 700 | 二级章节标题 |
| H4 | 12px / 0.75rem | 1.5 | 700 | 三级章节标题 |
| Body | 10pt / 13.33px | 1.7 | 400 | 正文（单栏，行高略宽于双栏） |
| Caption | 8pt / 10.67px | 1.5 | 400 | 图注 |
| Footnote | 7pt / 9.33px | 1.4 | 400 | 脚注/参考文献 |

> **Springer 特色**: 正文行高 1.7（略宽于 Nature/Science/IEEE 的 1.6），因为单栏布局行宽更大，需要更宽的行高确保可读性。

### 2.3 与 DLP-nature / DLP-science / DLP-ieee 的字体差异

| 维度 | DLP-nature | DLP-science | DLP-ieee | DLP-springer | 差异说明 |
|------|-----------|-------------|----------|-------------|---------|
| 西文字体 | Times New Roman | Helvetica Neue | Times New Roman | Latin Modern Roman | Springer 用 LaTeX 默认字体 |
| 中文字体 | 宋体 | 黑体 | 宋体 | 宋体 | Springer 与 Nature/IEEE 一致 |
| 栅格 | 双栏 | 双栏 | 双栏 | 单栏 | Springer 预印本为单栏 |
| 行高 | 1.6 | 1.6 | 1.6 | 1.7 | Springer 单栏行高略宽 |
| 页边距 | 2cm | 2cm | 0.75inch | 2.5cm | Springer 留白最克制 |

> **关键差异**: Springer 使用 Latin Modern Roman（LaTeX 默认字体），而非 Times New Roman——这反映了 Springer 预印本（arXiv 兼容）的 LaTeX 传统。

### 2.4 字重配对

- **标题 bold(700)**: 所有层级标题使用粗体
- **正文 regular(400)**: 正文使用常规字重
- **强调 italic(400)**: 物种名（*Homo sapiens*）、基因名（*BRCA1*）、术语首次出现使用斜体

---

## 三、栅格与间距

### 3.1 单栏栅格（Springer 预印本标准）

| 参数 | 值 | 说明 |
|------|-----|------|
| 栏数 | 单栏 | 预印本单栏布局（与 Nature/Science/IEEE 双栏不同） |
| 列宽 | 16cm | 单栏列宽（预印本标准宽度） |
| 槽宽 | N/A | 单栏无槽宽 |
| 页边距 | 2.5cm | 上下左右页边距（略宽于 Nature/Science 的 2cm） |
| 断点 | N/A | 印刷媒介无响应式断点 |

> **Springer 特色**: Springer 预印本为单栏布局（16cm 宽），页边距 2.5cm（略宽于 Nature/Science 的 2cm），确保单栏长行阅读舒适。正式出版的 Springer 期刊可能切换为双栏，但预印本（arXiv 兼容）统一为单栏。

### 3.2 间距系统（4px 基准）

| 间距 | 值 | 用途 |
|------|-----|------|
| xs | 4px | 图标与文字间距 |
| sm | 8px | 图注内边距 |
| md | 12px | 段落间距 |
| lg | 16px | 章节间距 |
| xl | 24px | 图表与正文间距 |
| 2xl | 32px | 大区块分隔 |

---

## 四、圆角与阴影

| 元素类型 | 圆角 | 阴影 |
|---------|------|------|
| 图片/图表 | 0px（直角） | none |
| 表格 | 0px（直角） | none |
| 文本框 | 0px（直角） | none |
| 按钮（数字版） | 0px（直角） | none |

> **强制规则**: Springer 期刊强制直角零阴影，任何圆角或阴影都会破坏学术严谨性。

---

## 五、动效

**N/A（印刷媒介）**

Springer 期刊为印刷媒介，无动效定义。数字版（link.springer.com）仅有简单的页面跳转，无过渡动效。

---

## 六、融入 Rxiv-Maker 内容

> 知识来源: Rxiv-Maker（Springer 风格、留白克制、预印本规范）

### 6.1 Springer 风格

1. **LaTeX 传统**: Springer 预印本继承 LaTeX 排版传统，使用 Latin Modern Roman 字族（Computer Modern 的现代衍生）
2. **单栏布局**: 预印本统一为单栏（16cm 宽），正式出版后可能切换为双栏
3. **章节编号**: 阿拉伯数字编号（1 / 1.1 / 1.1.1），不用罗马数字（与 IEEE 不同）
4. **标题装饰**: 章节标题可用 Springer 蓝 `#005CAB` 作为装饰色（如标题下划线、编号色）
5. **图表标题**: 图标题在图下方（Fig. 1: ...），表标题在表上方（Table 1: ...）
6. **公式编号**: 公式居中，编号右对齐 `(1)` / `(2)`（与 IEEE 一致）

### 6.2 留白克制（页边距 2.5cm 确保阅读舒适）

1. **页边距 2.5cm**: 上下左右页边距均为 2.5cm（略宽于 Nature/Science 的 2cm）
2. **留白策略**: Springer 预印本采用"克制留白"——页边距略宽，但不过度留白，确保单栏 16cm 列宽内的阅读舒适性
3. **段落间距**: 段落间距 12px（md），首行缩进 2 字符（中文）/ 0.5cm（西文）
4. **章节间距**: 章节间距 16px（lg），章节标题上方留白 24px（xl）
5. **图表间距**: 图表与正文间距 24px（xl），图表内边距 8px（sm）
6. **行高策略**: 正文行高 1.7（略宽于双栏的 1.6），因为单栏行宽更大，需要更宽的行高引导视线换行

> **留白克制原则**: Springer 预印本的留白策略是"克制而舒适"——页边距 2.5cm 确保阅读舒适，但不追求艺术性留白；所有留白服务于阅读体验，而非视觉表现力。

### 6.3 预印本规范（arXiv 兼容格式）

1. **arXiv 兼容**: Springer 预印本必须兼容 arXiv 提交格式（LaTeX 源码 + PDF 编译版）
2. **文档类**: `\documentclass{article}` 或 `\documentclass{svjour3}`（Springer 官方文档类）
3. **页面尺寸**: A4（21cm × 29.7cm），页边距 2.5cm，单栏 16cm 列宽
4. **字体**: Latin Modern Roman（LaTeX 默认），不得使用系统字体（确保跨平台一致）
5. **图片格式**: PDF/EPS（矢量图）或 PNG/JPG（位图，≥300 DPI）
6. **参考文献**: BibTeX 格式，`\bibliographystyle{spbasic}` 或 `\bibliographystyle{plain}`
7. **元数据**: 必须包含 `\title{}` / `\author{}` / `\abstract{}` / `\keywords{}`
8. **提交格式**: LaTeX 源码打包为 .zip（含 .tex / .bib / 图片），PDF 编译版单独提交

### 6.4 Rxiv-Maker 渲染映射

| Rxiv-Maker 功能 | 渲染结果 | DLP-springer 消费点 |
|----------------|---------|-------------------|
| `\documentclass{article}` | 单栏预印本版式 | `grid_system: 单栏, 16cm` |
| Latin Modern Roman 字体 | LaTeX 默认衬线字体 | `font_stack.western: "Latin Modern Roman"` |
| 页边距 2.5cm | 克制留白 | `grid_system.margin: 2.5cm` |
| arXiv 兼容格式 | 可直接提交 arXiv | `applicable_scenarios: ["预印本"]` |
| BibTeX 参考文献 | `\bibliographystyle{spbasic}` | sci-paper-writing 参考文献规范 |

---

## 七、Springer Nature 期刊版式细节

### 7.1 首页布局

1. **标题**: 居中，22px，粗体
2. **作者署名**: 居中，12px，作者名用上标数字标注单位
3. **作者单位**: 居中，10px，斜体
4. **摘要**: 有 "Abstract" 标签，10pt，不超过 250 字
5. **关键词**: 有 "Keywords" 标签，8pt，逗号分隔
6. **正文**: 单栏，10pt，首行缩进

### 7.2 章节编号规范

1. **一级章节**: 阿拉伯数字 `1 Introduction` / `2 Related Work` / `3 Method`（首字母大写，左对齐）
2. **二级章节**: `2.1 Dataset` / `2.2 Model Architecture`（首字母大写，左对齐）
3. **三级章节**: `2.1.1 Training` / `2.1.2 Inference`（首字母大写，左对齐）
4. **四级章节**: 不推荐使用（Springer 建议最多 3 级章节）

### 7.3 与 Nature 正刊的版式差异

| 维度 | DLP-nature（正刊） | DLP-springer（预印本） | 差异说明 |
|------|------------------|---------------------|---------|
| 栅格 | 双栏（8.5cm/栏） | 单栏（16cm） | 正刊双栏，预印本单栏 |
| 字体 | Times New Roman | Latin Modern Roman | 正刊用商业字体，预印本用 LaTeX 默认 |
| 页边距 | 2cm | 2.5cm | 预印本留白更克制 |
| 行高 | 1.6 | 1.7 | 单栏行高略宽 |
| 辅色 | `#E60012`（Nature红） | `#005CAB`（Springer蓝） | 期刊标识色不同 |
| 摘要 | 无 "Abstract" 标签 | 有 "Abstract" 标签 | Nature 特殊规范 |

> **定位差异**: DLP-nature 锚定 Nature 正刊版式（双栏印刷版），DLP-springer 锚定 Springer Nature 期刊预印本版式（单栏 arXiv 兼容版）——两者均为 Springer Nature 集团旗下，但版式定位不同。

---

## 八、brand-identity-skill 消费映射

### 8.1 配色注入映射

| DLP color_palette | visual_dna.color_scheme | 映射规则 |
|-------------------|------------------------|---------|
| `primary: #1A1A1A` | `--color-primary` | 正文/标题/轴线 |
| `secondary: #005CAB` | `--color-secondary` | 期刊标识/章节装饰 |
| `accent: #0066CC` | `--color-accent` | 超链接/DOI |
| `neutral: #6C757D` | `--color-text-secondary` | 图注/脚注 |
| `background: #FFFFFF` | `--color-bg` | 页面背景 |
| `text: #1A1A1A` | `--color-text` | 正文 |

### 8.2 字体注入映射

| DLP font_stack | visual_dna.font_scheme | 映射规则 |
|----------------|----------------------|---------|
| `western: "Latin Modern Roman", "Computer Modern", "Times New Roman", serif` | 标题/正文字体族（西文） | 首选 Latin Modern Roman |
| `chinese: "宋体", "SimSun", serif` | 标题/正文字体族（中文） | 中文 fallback 宋体 |
| `monospace: "Latin Modern Mono", "Courier New", monospace` | 代码字体族 | 代码块字体 |

### 8.3 图形规范注入映射

| DLP 字段 | visual_dna 字段 | 映射规则 |
|---------|----------------|---------|
| `grid_system: 单栏, 16cm` | `grid_system` | 单栏栅格直接继承 |
| `spacing_system: 4px 基准` | `line_style` | 间距阶梯直接继承 |
| `radius_shadow: 0px/none` | `line_style` | 强制直角零阴影 |
| `motion_curve: N/A` | `motion_profile` | 禁用动效 |

---

## 九、适用场景

| 场景 | 匹配度 | 说明 |
|------|--------|------|
| 学术论文 | ★★★★★ | Springer 期刊版式直接适用 |
| 期刊投稿 | ★★★★★ | Springer Nature 期刊投稿标准 |
| 预印本 | ★★★★★ | arXiv 兼容预印本标准版式 |
| 科学研究 | ★★★★☆ | 科研报告可参考 Springer 预印本版式 |

---

## 十、检索映射

| content_theme | output_type | target_audience | 命中 DLP |
|--------------|-------------|-----------------|---------|
| 预印本/arXiv | research_report | academic | DLP-springer |
| Springer/Springer Nature/预印本 | research_report | academic | DLP-springer |
| LaTeX/单栏/Computer Modern | research_report | academic | DLP-springer |

> 知识来源: Rxiv-Maker / Springer Nature 期刊 2024 年版式 / brand-identity-skill 元规则 / academic-journal 族规范
