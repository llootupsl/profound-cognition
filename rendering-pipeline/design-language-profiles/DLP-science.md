<!-- 作者：阿洋 -->

# DLP-science: Science 正刊设计语言画像

> **锚定真实世界**: Science 正刊 2024 年版式
> **融入来源技能**: Science 正刊版式规范（族覆盖补充，补全 Nature 之外的顶刊版式覆盖）
> **族归属**: academic-journal（学术期刊族）
> **索引**: 详见 `README.md` 获取 DLP 库完整清单与检索规范

---

## YAML frontmatter（12 字段完整定义）

```yaml
---
name: "DLP-science"
anchor: "Science 正刊 2024 年版式"
family: "academic-journal"

color_palette:
  primary: "#1A1A1A"       # 主色 - 近黑正文（Science 正文略柔于纯黑）
  secondary: "#BA0C2F"     # 辅色 - AAAS红（AAAS/Science官方标识色）
  accent: "#0066CC"        # 强调色 - 链接蓝（正文超链接与 DOI 链接色）
  neutral: "#6C757D"       # 中性色 - 次要文字灰（图注、脚注、元数据）
  background: "#FFFFFF"    # 背景色 - 纯白背景（印刷标准）
  text: "#1A1A1A"          # 文本色 - 近黑正文（与主色一致）

typography_scale:
  h1: "22px/1.375rem"      # 文章主标题（Article Title）
  h2: "16px/1rem"          # 一级章节标题（Section Heading）
  h3: "14px/0.875rem"      # 二级章节标题（Subsection Heading）
  h4: "12px/0.75rem"       # 三级章节标题（Sub-subsection Heading）
  body: "10pt/13.33px"     # 正文（Science 双栏布局字号偏小，10pt 为印刷标准）
  caption: "8pt/10.67px"   # 图注（图标题与图说明文字）
  footnote: "7pt/9.33px"   # 脚注（参考文献与补充说明）

font_stack:
  western: '"Whitman", "Times New Roman", "Georgia", serif'
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
  column_width: "8.3cm/栏"
  gutter: "0.6cm"
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
  - "跨学科研究"
---
```

---

## 一、配色方案详解

### 1.1 6 色板（锚定 Science 正刊 2024 实际版式）

| 色板角色 | 十六进制 | RGB | 用途 | 锚定来源 |
|---------|---------|-----|------|---------|
| 主色 Primary | `#1A1A1A` | rgb(26,26,26) | 正文文字、标题、图表轴线 | Science 正文印刷标准 |
| 辅色 Secondary | `#BA0C2F` | rgb(186,12,47) | 期刊标识、封面标题、栏目分隔线 | AAAS/Science 官方标识红 |
| 强调色 Accent | `#0066CC` | rgb(0,102,204) | 超链接、DOI 链接、引用跳转 | Science 数字版链接色 |
| 中性色 Neutral | `#6C757D` | rgb(108,117,125) | 图注、脚注、作者署名、元数据 | Science 图注灰 |
| 背景色 Background | `#FFFFFF` | rgb(255,255,255) | 页面背景、图表背景 | Science 印刷白 |
| 文本色 Text | `#1A1A1A` | rgb(26,26,26) | 正文（与主色一致） | Science 正文色 |

### 1.2 配色使用规则

1. **正文**: 使用 `#1A1A1A`（近黑），不得使用纯黑 `#000000`（Science 数字版略柔于 Nature）
2. **标题**: 使用 `#1A1A1A`，不得使用 Science 橙作为标题色（橙色仅用于期刊标识）
3. **链接**: 使用 `#0066CC`，下划线 1px solid `#0066CC`
4. **图注**: 使用 `#6C757D`，字号 8pt，与正文 `#1A1A1A` 形成层级
5. **图表轴线**: 使用 `#1A1A1A`，线宽 1px（数据线 1.5px）
6. **禁止渐变**: Science 正刊零渐变，所有色块为纯色

### 1.3 与 DLP-nature 的配色差异

| 色板角色 | DLP-nature | DLP-science | 差异说明 |
|---------|-----------|-------------|---------|
| 主色 | `#000000`（纯黑） | `#1A1A1A`（近黑） | Science 略柔于 Nature |
| 辅色 | `#E60012`（Nature红） | `#BA0C2F`（AAAS红） | 期刊标识色不同 |
| 强调色 | `#0066CC` | `#0066CC` | 一致（学术链接蓝标准） |
| 中性色 | `#6C757D` | `#6C757D` | 一致（学术图注灰标准） |
| 背景色 | `#FFFFFF` | `#FFFFFF` | 一致（印刷白标准） |
| 文本色 | `#1A1A1A` | `#1A1A1A` | 一致 |

---

## 二、字体方案详解

### 2.1 字体族

| 用途 | 西文字体 | 中文字体 | CSS font-family |
|------|---------|---------|----------------|
| 标题 | Whitman | 宋体 / SimSun | `"Whitman", "Times New Roman", "Georgia", "宋体", "SimSun", serif` |
| 正文 | Whitman | 宋体 / SimSun | `"Whitman", "Times New Roman", "Georgia", "宋体", "SimSun", serif` |
| 代码 | Courier New | — | `"Courier New", monospace` |

### 2.2 字号阶梯（双栏布局，字号偏小）

| 层级 | 字号 | 行高 | 字重 | 用途 |
|------|------|------|------|------|
| H1 | 22px / 1.375rem | 1.3 | 700 | 文章主标题 |
| H2 | 16px / 1rem | 1.4 | 700 | 一级章节标题 |
| H3 | 14px / 0.875rem | 1.5 | 700 | 二级章节标题 |
| H4 | 12px / 0.75rem | 1.5 | 700 | 三级章节标题 |
| Body | 10pt / 13.33px | 1.6 | 400 | 正文（双栏） |
| Caption | 8pt / 10.67px | 1.5 | 400 | 图注 |
| Footnote | 7pt / 9.33px | 1.4 | 400 | 脚注/参考文献 |

### 2.3 与 DLP-nature 的字体差异

| 维度 | DLP-nature | DLP-science | 差异说明 |
|------|-----------|-------------|---------|
| 西文字体 | Times New Roman（衬线） | Whitman（衬线） | Nature 用 Times New Roman，Science 用 Whitman，同为衬线但 Whitman 字宽更紧凑、x 高度更高 |
| 中文字体 | 宋体 / SimSun（衬线） | 宋体 / SimSun（衬线） | 与西文字体风格对齐 |
| H1 字号 | 24px | 22px | Science 标题略小 |
| H2 字号 | 18px | 16px | Science 章节标题略小 |

> **关键差异**: Nature 使用 Times New Roman 衬线字体，Science 使用 Whitman 衬线字体——两本顶刊同为衬线字体，但 Whitman 的字宽更紧凑、x 高度更高，视觉上比 Times New Roman 更现代。

### 2.4 字重配对

- **标题 bold(700)**: 所有层级标题使用粗体
- **正文 regular(400)**: 正文使用常规字重
- **强调 italic(400)**: 物种名（*Homo sapiens*）、基因名（*BRCA1*）、术语首次出现使用斜体

---

## 三、栅格与间距

### 3.1 双栏栅格（Science 印刷标准）

| 参数 | 值 | 说明 |
|------|-----|------|
| 栏数 | 双栏 | 正文双栏布局 |
| 列宽 | 8.3cm/栏 | 每栏宽度（略窄于 Nature 的 8.5cm） |
| 槽宽 | 0.6cm | 栏间距（略宽于 Nature 的 0.5cm） |
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

> **强制规则**: Science 正刊强制直角零阴影，任何圆角或阴影都会破坏学术严谨性。

---

## 五、动效

**N/A（印刷媒介）**

Science 正刊为印刷媒介，无动效定义。数字版（science.org）仅有简单的页面跳转，无过渡动效。

---

## 六、Science 正刊版式特征

### 6.1 与 Nature 的版式差异总览

| 维度 | DLP-nature | DLP-science | 差异说明 |
|------|-----------|-------------|---------|
| 西文字体 | Times New Roman（衬线） | Whitman（衬线） | Nature 用 Times New Roman，Science 用 Whitman，同为衬线但 Whitman 更现代 |
| 中文字体 | 宋体（衬线） | 宋体（衬线） | 与西文风格对齐 |
| 辅色 | `#E60012`（Nature红） | `#BA0C2F`（AAAS红） | 期刊标识色不同 |
| 列宽 | 8.5cm | 8.3cm | Science 略窄 |
| 槽宽 | 0.5cm | 0.6cm | Science 略宽 |
| H1 字号 | 24px | 22px | Science 标题略小 |
| 主色 | `#000000`（纯黑） | `#1A1A1A`（近黑） | Science 略柔 |

### 6.2 Science 正刊版式细节

1. **首页布局**: 标题→作者署名→作者单位→摘要（有 "Abstract" 标签）→正文→参考文献
2. **摘要规范**: 摘要有 "Abstract" 标签（与 Nature 不同），字号 10pt，不超过 125 字
3. **栏目分类**: Science 分 Research Articles / Reports / Reviews / Perspectives 等栏目，不同栏目版式略有差异
4. **参考文献**: 参考文献字号 7pt，作者名缩写（如 "J. Smith"），期刊名斜体
5. **图表跨栏**: 重要图表可跨双栏（17.2cm 宽），位于页面顶部或底部
6. **图注规范**: 图标题位于图下方，图注 8pt，子图用小写字母标注（与 Nature 一致）

### 6.3 Science 跨学科特征

Science 作为跨学科期刊，版式需兼容：
- **生命科学**: 基因名斜体（与 Nature 一致）
- **物理科学**: 公式排版（居中，编号右对齐）
- **社会科学**: 图表规范（数据可视化优先）

---

## 七、brand-identity-skill 消费映射

### 7.1 配色注入映射

| DLP color_palette | visual_dna.color_scheme | 映射规则 |
|-------------------|------------------------|---------|
| `primary: #1A1A1A` | `--color-primary` | 正文/标题/轴线 |
| `secondary: #BA0C2F` | `--color-secondary` | 期刊标识/栏目分隔 |
| `accent: #0066CC` | `--color-accent` | 超链接/DOI |
| `neutral: #6C757D` | `--color-text-secondary` | 图注/脚注 |
| `background: #FFFFFF` | `--color-bg` | 页面背景 |
| `text: #1A1A1A` | `--color-text` | 正文 |

### 7.2 字体注入映射

| DLP font_stack | visual_dna.font_scheme | 映射规则 |
|----------------|----------------------|---------|
| `western: "Whitman", "Times New Roman", "Georgia", serif` | 标题/正文字体族（西文） | 首选 Whitman |
| `chinese: "宋体", "SimSun", serif` | 标题/正文字体族（中文） | 中文 fallback 宋体 |
| `monospace: "Courier New", monospace` | 代码字体族 | 代码块字体 |

### 7.3 图形规范注入映射

| DLP 字段 | visual_dna 字段 | 映射规则 |
|---------|----------------|---------|
| `grid_system: 双栏, 8.3cm/栏` | `grid_system` | 双栏栅格直接继承 |
| `spacing_system: 4px 基准` | `line_style` | 间距阶梯直接继承 |
| `radius_shadow: 0px/none` | `line_style` | 强制直角零阴影 |
| `motion_curve: N/A` | `motion_profile` | 禁用动效 |

---

## 八、适用场景

| 场景 | 匹配度 | 说明 |
|------|--------|------|
| 学术论文 | ★★★★★ | Science 正刊版式直接适用 |
| 期刊投稿 | ★★★★★ | Science 期刊投稿标准 |
| 科学研究 | ★★★★☆ | 科研报告可参考 Science 版式 |
| 跨学科研究 | ★★★★★ | Science 跨学科版式优势 |

---

## 九、检索映射

| content_theme | output_type | target_audience | 命中 DLP |
|--------------|-------------|-----------------|---------|
| 跨学科研究/科学前沿 | research_report | academic | DLP-science |
| Science/科学/AAAS | research_report | academic | DLP-science |
| 衬线学术排版 | research_report | academic | DLP-science |

> 知识来源: Science 正刊 2024 年版式 / brand-identity-skill 元规则 / academic-journal 族规范

---

## 融入内容：Science 正刊版式规范

> **来源**: Science 正刊版式规范（AAAS 出版规范）
> **融入形式**: Science 期刊版式特征内化

### Science 正刊版式核心特征内化

1. **AAAS 出版规范内化**: Science 由美国科学促进会（AAAS）出版，其版式遵循 AAAS 官方出版规范。本 DLP 将 AAAS 的双栏 8.3cm 列宽、0.6cm 槽宽、2cm 页边距等印刷规范内化为 `grid_system` 字段，确保 Science 期刊投稿排版的精确匹配。

2. **Whitman 衬线字体体系**: Science 正刊使用 Whitman 衬线字体（与 Nature 的 Times New Roman 同为衬线字体，但 Whitman 的字宽更紧凑、x 高度更高，视觉上比 Times New Roman 更现代），本 DLP 将其内化为 `font_stack.western` 字段，中文 fallback 采用宋体/SimSun 以保持衬线风格的一致性。

3. **双栏紧凑布局**: Science 采用双栏布局，列宽 8.3cm（略窄于 Nature 的 8.5cm），槽宽 0.6cm（略宽于 Nature 的 0.5cm），正文 10pt 字号偏小，适应双栏紧凑排版的信息密度需求。本 DLP 将其内化为 `typography_scale.body` 和 `grid_system` 字段。

4. **AAAS 红色品牌标识**: Science/AAAS 封面与栏目标识使用官方标识红 `#BA0C2F`（与 Nature 红色 `#E60012` 区分），本 DLP 将其内化为 `color_palette.secondary`，仅用于期刊标识和栏目分隔，不用于标题或正文。

5. **近黑正文色**: Science 正文使用 `#1A1A1A`（近黑），略柔于 Nature 的纯黑 `#000000`，本 DLP 将其内化为 `color_palette.primary` 和 `color_palette.text`，确保数字版阅读的柔和度。

6. **跨学科版式兼容**: Science 作为跨学科期刊，版式需兼容生命科学（基因名斜体）、物理科学（公式排版）、社会科学（数据可视化），本 DLP 在 `font_weight_pairing.emphasis` 中保留 italic(400) 用于物种名和基因名，体现跨学科版式的包容性。
