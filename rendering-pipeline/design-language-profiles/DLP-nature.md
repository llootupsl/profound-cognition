<!-- 作者：阿洋 -->

# DLP-nature: Nature 正刊设计语言画像

> **锚定真实世界**: Nature 正刊 2024 年版式
> **融入来源技能**: Nature Skills（Nature 正刊视觉标准）
> **族归属**: academic-journal（学术期刊族）
> **索引**: 详见 `README.md` 获取 DLP 库完整清单与检索规范

---

## YAML frontmatter（12 字段完整定义）

```yaml
---
name: "DLP-nature"
anchor: "Nature 正刊 2024 年版式"
family: "academic-journal"

color_palette:
  primary: "#000000"       # 主色 - 正文黑（Nature 正文使用纯黑）
  secondary: "#E60012"     # 辅色 - Nature红（期刊 logo 与封面标识色）
  accent: "#0066CC"        # 强调色 - 链接蓝（正文超链接与 DOI 链接色）
  neutral: "#6C757D"       # 中性色 - 次要文字灰（图注、脚注、元数据）
  background: "#FFFFFF"    # 背景色 - 纯白背景（印刷标准）
  text: "#1A1A1A"          # 文本色 - 近黑正文（数字渲染时略柔于纯黑）

typography_scale:
  h1: "24px/1.5rem"        # 文章主标题（Article Title）
  h2: "18px/1.125rem"      # 一级章节标题（Section Heading）
  h3: "16px/1rem"          # 二级章节标题（Subsection Heading）
  h4: "14px/0.875rem"      # 三级章节标题（Sub-subsection Heading）
  body: "10pt/13.33px"     # 正文（Nature 双栏布局字号偏小，10pt 为印刷标准）
  caption: "8pt/10.67px"   # 图注（图标题与图说明文字）
  footnote: "7pt/9.33px"   # 脚注（参考文献与补充说明）

font_stack:
  western: '"Times New Roman", "STIX Two Text", serif'
  chinese: '"宋体", "SimSun", serif'
  monospace: '"Courier New", monospace'

font_weight_pairing:
  heading: "bold(700)"     # 标题粗体
  body: "regular(400)"     # 正文常规
  emphasis: "italic(400)"  # 强调斜体（物种名、基因名、术语首次出现）

spacing_system:
  base: "4px"
  scale: "4/8/12/16/24/32px"

grid_system:
  columns: "双栏"
  column_width: "8.5cm/栏"
  gutter: "0.5cm"
  margin: "2cm"
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
  - "科学研究"
  - "同行评审"
---
```

---

## 一、配色方案详解

### 1.1 6 色板（锚定 Nature 正刊 2024 实际版式）

| 色板角色 | 十六进制 | RGB | 用途 | 锚定来源 |
|---------|---------|-----|------|---------|
| 主色 Primary | `#000000` | rgb(0,0,0) | 正文文字、标题、图表轴线 | Nature 正文印刷标准 |
| 辅色 Secondary | `#E60012` | rgb(230,0,18) | 期刊标识、封面标题、栏目分隔线 | Nature logo 官方红 |
| 强调色 Accent | `#0066CC` | rgb(0,102,204) | 超链接、DOI 链接、引用跳转 | Nature 数字版链接色 |
| 中性色 Neutral | `#6C757D` | rgb(108,117,125) | 图注、脚注、作者署名、元数据 | Nature 图注灰 |
| 背景色 Background | `#FFFFFF` | rgb(255,255,255) | 页面背景、图表背景 | Nature 印刷白 |
| 文本色 Text | `#1A1A1A` | rgb(26,26,26) | 数字渲染正文（略柔于纯黑） | Nature 数字版正文色 |

### 1.2 配色使用规则

1. **正文**: 使用 `#000000`（印刷）或 `#1A1A1A`（数字），不得使用灰色正文
2. **标题**: 使用 `#000000`，不得使用 Nature 红作为标题色（红色仅用于期刊标识）
3. **链接**: 使用 `#0066CC`，下划线 1px solid `#0066CC`
4. **图注**: 使用 `#6C757D`，字号 8pt，与正文 `#000000` 形成层级
5. **图表轴线**: 使用 `#000000`，线宽 1px（数据线 1.5px）
6. **禁止渐变**: Nature 正刊零渐变，所有色块为纯色

---

## 二、字体方案详解

### 2.1 字体族

| 用途 | 西文字体 | 中文字体 | CSS font-family |
|------|---------|---------|----------------|
| 标题 | Times New Roman | 宋体 / SimSun | `"Times New Roman", "STIX Two Text", "宋体", "SimSun", serif` |
| 正文 | Times New Roman | 宋体 / SimSun | `"Times New Roman", "STIX Two Text", "宋体", "SimSun", serif` |
| 代码 | Courier New | — | `"Courier New", monospace` |

### 2.2 字号阶梯（双栏布局，字号偏小）

| 层级 | 字号 | 行高 | 字重 | 用途 |
|------|------|------|------|------|
| H1 | 24px / 1.5rem | 1.3 | 700 | 文章主标题 |
| H2 | 18px / 1.125rem | 1.4 | 700 | 一级章节标题 |
| H3 | 16px / 1rem | 1.5 | 700 | 二级章节标题 |
| H4 | 14px / 0.875rem | 1.5 | 700 | 三级章节标题 |
| Body | 10pt / 13.33px | 1.6 | 400 | 正文（双栏） |
| Caption | 8pt / 10.67px | 1.5 | 400 | 图注 |
| Footnote | 7pt / 9.33px | 1.4 | 400 | 脚注/参考文献 |

### 2.3 字重配对

- **标题 bold(700)**: 所有层级标题使用粗体
- **正文 regular(400)**: 正文使用常规字重
- **强调 italic(400)**: 物种名（*Homo sapiens*）、基因名（*BRCA1*）、术语首次出现使用斜体

---

## 三、栅格与间距

### 3.1 双栏栅格（Nature 印刷标准）

| 参数 | 值 | 说明 |
|------|-----|------|
| 栏数 | 双栏 | 正文双栏布局 |
| 列宽 | 8.5cm/栏 | 每栏宽度 |
| 槽宽 | 0.5cm | 栏间距 |
| 页边距 | 2cm | 上下左右页边距 |
| 断点 | N/A | 印刷媒介无响应式断点 |

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

> **强制规则**: Nature 正刊强制直角零阴影，任何圆角或阴影都会破坏学术严谨性。

---

## 五、动效

**N/A（印刷媒介）**

Nature 正刊为印刷媒介，无动效定义。数字版（nature.com）仅有简单的页面跳转，无过渡动效。

---

## 六、融入 Nature Skills 内容

> 知识来源: Nature Skills（Nature 正刊视觉标准）

### 6.1 图注规范（Nature 正刊强制规则）

1. **图标题位置**: 图标题（Figure caption）必须位于图的**下方**，不得在图上方
2. **图注字号**: 图注使用 8pt 字号（`caption: "8pt/10.67px"`），字重 regular(400)
3. **图注颜色**: 图注文字使用中性色 `#6C757D`，图标题标签（如 "Fig. 1"）使用主色 `#000000` 加粗
4. **图注结构**: `Fig. 1 | 图标题. a, 子图说明. b, 子图说明.`（"|" 分隔图号与标题，子图用小写字母标注）
5. **图注宽度**: 图注宽度与图宽度一致，不超过单栏宽度（8.5cm）或跨栏宽度（17.5cm）

### 6.2 扩展数据图规则（Supplementary Figures）

1. **编号规则**: 扩展数据图（Extended Data Figures）编号使用 **S1/S2/S3...**（S 代表 Supplementary）
2. **标题前缀**: `Extended Data Fig. S1 |`（不得使用 "Figure S1" 或 "Supplementary Figure 1"）
3. **引用格式**: 正文引用扩展数据图使用 `(Extended Data Fig. S1)` 或 `(Extended Data Figs. S1, S2)`
4. **颜色规范**: 扩展数据图配色与正文图一致，使用同一 6 色板
5. **字号规范**: 扩展数据图字号与正文图一致（图注 8pt，轴标签 7pt）

### 6.3 正文引用格式

1. **图引用**: `(Fig. 1a)` / `(Fig. 1a, b)` / `(Figs. 1a, 2c)`——"Fig." 缩写，小写字母标注子图，逗号分隔
2. **表引用**: `(Table 1)` / `(Tables. 1, 2)`——"Table" 不缩写
3. **扩展数据引用**: `(Extended Data Fig. S1)` / `(Extended Data Table 1)`
4. **参考文献引用**: 上标数字 `¹` 或 `[1]`（Nature 数字版用上标，印刷版用上标）
5. **公式引用**: `(Eq. 1)` 或 `(1)`——公式编号在右侧括号内

### 6.4 Nature 正刊版式细节

1. **首页布局**: 标题→作者署名→作者单位→摘要（无 "Abstract" 标签）→正文→方法→参考文献
2. **摘要规范**: 摘要无 "Abstract" 标签，直接以段落形式跟在作者单位下方，字号 10pt，不超过 200 字
3. **方法部分**: 方法（Methods）部分位于正文之后，字号 8pt（小于正文 10pt）
4. **参考文献**: 参考文献字号 7pt，作者名缩写（如 "Smith, J."），期刊名斜体
5. **图表跨栏**: 重要图表可跨双栏（17.5cm 宽），位于页面顶部或底部

---

## 七、brand-identity-skill 消费映射

### 7.1 配色注入映射

| DLP color_palette | visual_dna.color_scheme | 映射规则 |
|-------------------|------------------------|---------|
| `primary: #000000` | `--color-primary` | 正文/标题/轴线 |
| `secondary: #E60012` | `--color-secondary` | 期刊标识/栏目分隔 |
| `accent: #0066CC` | `--color-accent` | 超链接/DOI |
| `neutral: #6C757D` | `--color-text-secondary` | 图注/脚注 |
| `background: #FFFFFF` | `--color-bg` | 页面背景 |
| `text: #1A1A1A` | `--color-text` | 数字版正文 |

### 7.2 字体注入映射

| DLP font_stack | visual_dna.font_scheme | 映射规则 |
|----------------|----------------------|---------|
| `western: "Times New Roman", "STIX Two Text", serif` | 标题/正文字体族（西文） | 首选 Times New Roman |
| `chinese: "宋体", "SimSun", serif` | 标题/正文字体族（中文） | 中文 fallback 宋体 |
| `monospace: "Courier New", monospace` | 代码字体族 | 代码块字体 |

### 7.3 图形规范注入映射

| DLP 字段 | visual_dna 字段 | 映射规则 |
|---------|----------------|---------|
| `grid_system: 双栏, 8.5cm/栏` | `grid_system` | 双栏栅格直接继承 |
| `spacing_system: 4px 基准` | `line_style` | 间距阶梯直接继承 |
| `radius_shadow: 0px/none` | `line_style` | 强制直角零阴影 |
| `motion_curve: N/A` | `motion_profile` | 禁用动效 |

---

## 八、适用场景

| 场景 | 匹配度 | 说明 |
|------|--------|------|
| 学术论文 | ★★★★★ | Nature 正刊版式直接适用 |
| 期刊投稿 | ★★★★★ | Nature 系列期刊投稿标准 |
| 科学研究 | ★★★★☆ | 科研报告可参考 Nature 版式 |
| 同行评审 | ★★★★☆ | 评审稿格式参考 Nature 双栏 |

---

## 九、检索映射

| content_theme | output_type | target_audience | 命中 DLP |
|--------------|-------------|-----------------|---------|
| 学术论文/期刊投稿/同行评审 | research_report | academic | DLP-nature |
| Nature/自然/正刊 | research_report | academic | DLP-nature |
| 生物学/医学/化学/物理 | research_report | academic | DLP-nature（首选） |

> 知识来源: Nature Skills / Nature 正刊 2024 年版式 / brand-identity-skill 元规则
