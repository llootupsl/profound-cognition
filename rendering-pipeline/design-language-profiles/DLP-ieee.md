<!-- 作者：阿洋 -->

# DLP-ieee: IEEE/ACM 设计语言画像

> **锚定真实世界**: IEEE/ACM 正刊 2024 年版式
> **融入来源技能**: sci-paper-writing（IEEE/ACM 双栏版式规范、参考文献规范、公式排版规则）+ Quarkdown（IEEE/ACM 官方模板兼容、LaTeX 语法兼容）
> **族归属**: academic-journal（学术期刊族）
> **索引**: 详见 `README.md` 获取 DLP 库完整清单与检索规范

---

## YAML frontmatter（12 字段完整定义）

```yaml
---
name: "DLP-ieee"
anchor: "IEEE/ACM 正刊 2024 年版式"
family: "academic-journal"

color_palette:
  primary: "#000000"       # 主色 - 正文黑（IEEE 正文使用纯黑）
  secondary: "#00629B"     # 辅色 - IEEE蓝（IEEE 期刊标识色）
  accent: "#0066CC"        # 强调色 - 链接蓝（正文超链接与 DOI 链接色）
  neutral: "#6C757D"       # 中性色 - 次要文字灰（图注、脚注、元数据）
  background: "#FFFFFF"    # 背景色 - 纯白背景（印刷标准）
  text: "#1A1A1A"          # 文本色 - 近黑正文（数字渲染时略柔于纯黑）

typography_scale:
  h1: "24px/10pt"          # 文章主标题（Article Title，IEEE 用 10pt）
  h2: "10pt/13.33px"       # 一级章节标题（Section Heading，罗马数字编号）
  h3: "10pt/13.33px"       # 二级章节标题（Subsection Heading，字母编号）
  h4: "10pt/13.33px"       # 三级章节标题（Sub-subsection Heading，数字编号）
  body: "10pt/13.33px"     # 正文（IEEE 双栏布局，10pt 为印刷标准）
  caption: "8pt/10.67px"   # 图注（图标题与图说明文字）
  footnote: "8pt/10.67px"  # 脚注（IEEE 脚注与图注同字号）

font_stack:
  western: '"Times New Roman", "Times", serif'
  chinese: '"宋体", "SimSun", serif'
  monospace: '"Courier New", monospace'

font_weight_pairing:
  heading: "bold(700)"     # 标题粗体（罗马数字编号的章节标题）
  body: "regular(400)"     # 正文常规
  emphasis: "italic(400)"  # 强调斜体（术语首次出现、数学符号）

spacing_system:
  base: "4px"
  scale: "4/8/12/16/24/32px"

grid_system:
  columns: "双栏"
  column_width: "3.5inch/栏"   # IEEE 双栏列宽（约 8.89cm）
  gutter: "0.25inch"            # 栏间距（约 0.635cm）
  margin: "0.75inch"            # 页边距（约 1.905cm）
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
  - "工程研究"
  - "计算机科学"
  - "电子工程"
---
```

---

## 一、配色方案详解

### 1.1 6 色板（锚定 IEEE/ACM 正刊 2024 实际版式）

| 色板角色 | 十六进制 | RGB | 用途 | 锚定来源 |
|---------|---------|-----|------|---------|
| 主色 Primary | `#000000` | rgb(0,0,0) | 正文文字、标题、图表轴线 | IEEE 正文印刷标准 |
| 辅色 Secondary | `#00629B` | rgb(0,98,155) | 期刊标识、会议名称、栏目标识 | IEEE 官方蓝 |
| 强调色 Accent | `#0066CC` | rgb(0,102,204) | 超链接、DOI 链接、引用跳转 | IEEE 数字版链接色 |
| 中性色 Neutral | `#6C757D` | rgb(108,117,125) | 图注、脚注、作者署名、元数据 | IEEE 图注灰 |
| 背景色 Background | `#FFFFFF` | rgb(255,255,255) | 页面背景、图表背景 | IEEE 印刷白 |
| 文本色 Text | `#1A1A1A` | rgb(26,26,26) | 数字渲染正文（略柔于纯黑） | IEEE 数字版正文色 |

### 1.2 配色使用规则

1. **正文**: 使用 `#000000`（印刷）或 `#1A1A1A`（数字），不得使用灰色正文
2. **标题**: 使用 `#000000`，章节标题用罗马数字编号（I. II. III.），不得使用 IEEE 蓝作为标题色
3. **链接**: 使用 `#0066CC`，下划线 1px solid `#0066CC`
4. **图注**: 使用 `#6C757D`，字号 8pt，与正文 `#000000` 形成层级
5. **图表轴线**: 使用 `#000000`，线宽 1px（数据线 1.5px）
6. **禁止渐变**: IEEE/ACM 正刊零渐变，所有色块为纯色

### 1.3 与 DLP-nature / DLP-science 的配色差异

| 色板角色 | DLP-nature | DLP-science | DLP-ieee | 差异说明 |
|---------|-----------|-------------|----------|---------|
| 主色 | `#000000` | `#1A1A1A` | `#000000` | IEEE 与 Nature 一致（纯黑） |
| 辅色 | `#E60012` | `#F47C20` | `#00629B` | IEEE 蓝区别于 Nature 红/Science 橙 |
| 强调色 | `#0066CC` | `#0066CC` | `#0066CC` | 一致（学术链接蓝标准） |

---

## 二、字体方案详解

### 2.1 字体族

| 用途 | 西文字体 | 中文字体 | CSS font-family |
|------|---------|---------|----------------|
| 标题 | Times New Roman | 宋体 / SimSun | `"Times New Roman", "Times", "宋体", "SimSun", serif` |
| 正文 | Times New Roman | 宋体 / SimSun | `"Times New Roman", "Times", "宋体", "SimSun", serif` |
| 代码 | Courier New | — | `"Courier New", monospace` |

### 2.2 字号阶梯（IEEE 双栏标准，字号统一）

| 层级 | 字号 | 行高 | 字重 | 用途 |
|------|------|------|------|------|
| H1 | 24px / 10pt | 1.2 | 700 | 文章主标题（居中，24px 数字渲染） |
| H2 | 10pt / 13.33px | 1.5 | 700 | 一级章节标题（罗马数字 I. II. III.） |
| H3 | 10pt / 13.33px | 1.5 | 700 | 二级章节标题（字母 A. B. C.） |
| H4 | 10pt / 13.33px | 1.5 | 700 | 三级章节标题（数字 1) 2) 3)） |
| Body | 10pt / 13.33px | 1.6 | 400 | 正文（双栏） |
| Caption | 8pt / 10.67px | 1.5 | 400 | 图注 |
| Footnote | 8pt / 10.67px | 1.5 | 400 | 脚注（IEEE 脚注与图注同字号） |

> **IEEE 特色**: IEEE 章节标题（H2/H3/H4）与正文字号一致（均为 10pt），仅通过编号格式（罗马数字/字母/数字）和字重区分层级——这是 IEEE 与 Nature/Science 的显著差异。

### 2.3 与 DLP-nature / DLP-science 的字体差异

| 维度 | DLP-nature | DLP-science | DLP-ieee | 差异说明 |
|------|-----------|-------------|----------|---------|
| 西文字体 | Times New Roman（衬线） | Helvetica Neue（无衬线） | Times New Roman（衬线） | IEEE 与 Nature 一致（衬线） |
| 中文字体 | 宋体（衬线） | 黑体（无衬线） | 宋体（衬线） | IEEE 与 Nature 一致（宋体） |
| H2 字号 | 18px | 16px | 10pt/13.33px | IEEE 章节标题与正文同字号 |
| H3 字号 | 16px | 14px | 10pt/13.33px | IEEE 章节标题与正文同字号 |
| H4 字号 | 14px | 12px | 10pt/13.33px | IEEE 章节标题与正文同字号 |

### 2.4 字重配对

- **标题 bold(700)**: 所有层级标题使用粗体，章节标题用编号区分层级
- **正文 regular(400)**: 正文使用常规字重
- **强调 italic(400)**: 术语首次出现、数学符号（如 *x*, *y*, *n*）使用斜体

---

## 三、栅格与间距

### 3.1 双栏栅格（IEEE 印刷标准，inch 单位）

| 参数 | 值 | 说明 |
|------|-----|------|
| 栏数 | 双栏 | 正文双栏布局 |
| 列宽 | 3.5inch/栏（约 8.89cm） | 每栏宽度（IEEE 标准） |
| 槽宽 | 0.25inch（约 0.635cm） | 栏间距（IEEE 标准） |
| 页边距 | 0.75inch（约 1.905cm） | 上下左右页边距（IEEE 标准） |
| 断点 | N/A | 印刷媒介无响应式断点 |

> **IEEE 特色**: IEEE 使用 inch 为单位（美国工程标准），Nature/Science 使用 cm 为单位（欧洲科学标准）。

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

> **强制规则**: IEEE/ACM 正刊强制直角零阴影，任何圆角或阴影都会破坏学术严谨性。

---

## 五、动效

**N/A（印刷媒介）**

IEEE/ACM 正刊为印刷媒介，无动效定义。数字版（ieeexplore.ieee.org）仅有简单的页面跳转，无过渡动效。

---

## 六、融入 sci-paper-writing 内容

> 知识来源: sci-paper-writing（IEEE/ACM 双栏版式规范、参考文献规范、公式排版规则）

### 6.1 IEEE/ACM 双栏版式规范

1. **栏数**: 强制双栏（Conference Proceedings 与 Transactions 一致）
2. **列宽**: 3.5inch/栏（约 8.89cm），不得超出
3. **槽宽**: 0.25inch（约 0.635cm），栏间留白
4. **页边距**: 0.75inch（约 1.905cm），上下左右一致
5. **跨栏元素**: 仅以下元素可跨双栏：
   - 文章标题（H1）
   - 作者署名与单位
   - 摘要（Abstract）
   - 关键词（Index Terms）
   - 跨栏图表（spanning figures/tables）
   - 致谢（Acknowledgment）
   - 参考文献（References）
6. **分栏规则**: 正文从摘要后开始双栏排版，不得手动断栏，由排版引擎自动处理

### 6.2 参考文献规范（IEEE 引用格式）

1. **正文引用格式**: 方括号数字 `[1]` / `[1], [2]` / `[1]–[3]`（连续引用用 en-dash）
2. **引用位置**: 引用编号置于句末标点前（如 `... as shown in [1].`）
3. **参考文献列表**: 标题 "References"（居中，粗体），列表项左对齐，编号右对齐
4. **参考文献条目格式**:
   - 期刊: `[1] J. K. Author, "Title of paper," Abbrev. Title of Periodical, vol. x, no. x, pp. xxx–xxx, Abbrev. Month, year.`
   - 会议: `[2] J. K. Author, "Title of paper," in Abbrev. Name of Conf., City of Conf., Abbrev. State, year, pp. xxx–xxx.`
   - 书籍: `[3] J. K. Author, Title of Book, xth ed. City of Publisher, State: Publisher, year, pp. xxx–xxx.`
5. **作者名缩写**: 姓在前，名缩写（如 `J. K. Author`），多作者用逗号分隔，最后一位前加 `and`
6. **期刊名缩写**: 使用 IEEE 官方缩写表（如 `IEEE Trans. Pattern Anal. Mach. Intell.`）

### 6.3 公式排版规则

1. **公式位置**: 公式居中排版，独占一行
2. **公式编号**: 编号右对齐，格式 `(1)` / `(2)` / `(3)`——圆括号内阿拉伯数字
3. **公式引用**: 正文引用公式用 `(1)`，不得用 `Eq. (1)` 或 `Equation (1)`（IEEE 规范）
4. **多行公式**: 多行公式用 `align` 环境，等号对齐
5. **数学符号**: 标量斜体（*x*, *y*），向量粗体（**x**, **y**），矩阵粗体大写（**X**, **Y**）
6. **公式标点**: 公式末尾根据语境加逗号或句号（如 `... = 0,` 或 `... = 0.`）

### 6.4 IEEE 章节编号规范

1. **一级章节**: 罗马数字 `I. INTRODUCTION` / `II. RELATED WORK` / `III. METHOD`（全大写，居中或左对齐）
2. **二级章节**: 字母 `A. Dataset` / `B. Model Architecture`（首字母大写，左对齐）
3. **三级章节**: 数字 `1) Training:` / `2) Inference:`（首字母大写，左对齐，冒号结尾）
4. **四级章节**: 小写字母 `(a):` / `(b):`（仅必要时使用）

---

## 七、融入 Quarkdown 内容

> 知识来源: Quarkdown（IEEE/ACM 官方模板兼容、LaTeX 语法兼容）

### 7.1 IEEE/ACM 官方模板兼容

1. **IEEEtran 文档类**: Quarkdown 必须兼容 `\documentclass{IEEEtran}` 语法
2. **模板选项**:
   - `\documentclass[conference]{IEEEtran}`（会议论文）
   - `\documentclass[journal]{IEEEtran}`（期刊论文）
   - `\documentclass[compsoc]{IEEEtran}`（计算机学会版式）
3. **ACM 模板兼容**: Quarkdown 必须兼容 `\documentclass{acmart}` 语法
4. **模板选项**:
   - `\documentclass[sigconf]{acmart}`（会议论文）
   - `\documentclass[acmtog]{acmart}`（图形学期刊）
   - `\documentclass[acmsmall]{acmart}`（小格式期刊）

### 7.2 LaTeX 语法兼容

1. **文档类声明**: `\documentclass{IEEEtran}` 或 `\documentclass{acmart}`
2. **包加载**: Quarkdown 必须兼容 IEEE 论文常用包：
   - `\usepackage{graphicx}`（图片）
   - `\usepackage{amsmath}`（数学公式）
   - `\usepackage{booktabs}`（三线表）
   - `\usepackage{cite}`（引用）
   - `\usepackage{url}` / `\usepackage{hyperref}`（超链接）
3. **标题与作者**:
   ```latex
   \title{Paper Title}
   \author{\IEEEauthorblockN{Author Name}
   \IEEEauthorblockA{Author Affiliation}}
   ```
4. **图表环境**: `\begin{figure}` / `\begin{table}`，跨栏用 `\begin{figure*}` / `\begin{table*}`
5. **参考文献**: `\bibliographystyle{IEEEtran}` + `\bibliography{refs}`

### 7.3 Quarkdown 渲染映射

| Quarkdown 语法 | 渲染结果 | DLP-ieee 消费点 |
|---------------|---------|----------------|
| `\documentclass{IEEEtran}` | IEEE 双栏版式 | `grid_system: 双栏, 3.5inch/栏` |
| `\title{...}` | 居中粗体标题 | `typography_scale.h1: 24px/10pt` |
| `\section{...}` | 罗马数字编号标题 | `typography_scale.h2: 10pt` |
| `\cite{...}` | `[1]` 格式引用 | sci-paper-writing 参考文献规范 |
| `\begin{equation}` | 居中公式 + 右对齐编号 | sci-paper-writing 公式排版规则 |
| `\begin{figure*}` | 跨栏图表 | `grid_system: 双栏, 跨栏 7.25inch` |

---

## 八、brand-identity-skill 消费映射

### 8.1 配色注入映射

| DLP color_palette | visual_dna.color_scheme | 映射规则 |
|-------------------|------------------------|---------|
| `primary: #000000` | `--color-primary` | 正文/标题/轴线 |
| `secondary: #00629B` | `--color-secondary` | 期刊标识/会议名称 |
| `accent: #0066CC` | `--color-accent` | 超链接/DOI |
| `neutral: #6C757D` | `--color-text-secondary` | 图注/脚注 |
| `background: #FFFFFF` | `--color-bg` | 页面背景 |
| `text: #1A1A1A` | `--color-text` | 数字版正文 |

### 8.2 字体注入映射

| DLP font_stack | visual_dna.font_scheme | 映射规则 |
|----------------|----------------------|---------|
| `western: "Times New Roman", "Times", serif` | 标题/正文字体族（西文） | 首选 Times New Roman |
| `chinese: "宋体", "SimSun", serif` | 标题/正文字体族（中文） | 中文 fallback 宋体 |
| `monospace: "Courier New", monospace` | 代码字体族 | 代码块字体 |

### 8.3 图形规范注入映射

| DLP 字段 | visual_dna 字段 | 映射规则 |
|---------|----------------|---------|
| `grid_system: 双栏, 3.5inch/栏` | `grid_system` | 双栏栅格直接继承（inch 单位） |
| `spacing_system: 4px 基准` | `line_style` | 间距阶梯直接继承 |
| `radius_shadow: 0px/none` | `line_style` | 强制直角零阴影 |
| `motion_curve: N/A` | `motion_profile` | 禁用动效 |

---

## 九、适用场景

| 场景 | 匹配度 | 说明 |
|------|--------|------|
| 学术论文 | ★★★★★ | IEEE/ACM 正刊版式直接适用 |
| 期刊投稿 | ★★★★★ | IEEE Transactions / ACM 期刊投稿标准 |
| 工程研究 | ★★★★★ | 工程领域论文标准版式 |
| 计算机科学 | ★★★★★ | CS 领域会议/期刊标准（CVPR/ICCV/ACL 等） |
| 电子工程 | ★★★★★ | EE 领域期刊标准（IEEE Trans. 系列） |

---

## 十、检索映射

| content_theme | output_type | target_audience | 命中 DLP |
|--------------|-------------|-----------------|---------|
| 工程研究/计算机科学/电子工程 | research_report | academic | DLP-ieee |
| IEEE/ACM/会议论文/Transactions | research_report | academic | DLP-ieee |
| LaTeX/IEEEtran/acmart | research_report | academic | DLP-ieee |

> 知识来源: sci-paper-writing / Quarkdown / IEEE/ACM 正刊 2024 年版式 / brand-identity-skill 元规则
