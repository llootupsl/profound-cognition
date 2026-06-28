<!-- 作者：阿洋 -->

# DLP-newyorker — 纽约客杂志设计语言画像

> **定位**: publication-typesetting 族，锚定 The New Yorker 2024 年版式，提供文学评论与长文叙事的杂志级排版规范。
> **族覆盖补充**: 本 DLP 为 publication-typesetting 族的族覆盖补充成员，与 DLP-economist / DLP-ted / DLP-kami 共同构成 4 个 DLP 的完整族覆盖。
> **索引**: 详见 `README.md` 获取 DLP 库完整清单与检索规范

---

## YAML frontmatter（12 字段完整定义）

```yaml
---
name: "DLP-newyorker"
anchor: "The New Yorker 2024 年版式"
family: "publication-typesetting"

color_palette:
  primary: "#1A1A1A"
  secondary: "#CD2026"
  accent: "#0066CC"
  neutral: "#6C757D"
  background: "#FCFAF5"
  text: "#1A1A1A"

typography_scale:
  h1: "42px/2.625rem"
  h2: "28px/1.75rem"
  h3: "22px/1.375rem"
  h4: "16px/1rem"
  body: "11pt/14.67px"
  caption: "9pt/12px"
  footnote: "8pt/10.67px"

font_stack:
  western: '"Caslon", "Adobe Caslon Pro", "Rietveld", serif'
  chinese: '"宋体", "SimSun", "Noto Serif SC", serif'
  monospace: '"Courier New", "Courier", monospace'

font_weight_pairing:
  heading: "regular(400)"
  body: "regular(400)"
  emphasis: "italic(400)"

spacing_system:
  base: "4px"
  scale: "4/8/12/16/24/32/48px"

grid_system:
  columns: "3栏"
  column_width: "7cm"
  gutter: "0.6cm"
  margin: "2cm"
  breakpoint: "N/A(印刷媒介)"

radius_shadow:
  radius: "0px"
  shadow: "none"

motion_curve:
  easing: "N/A(印刷媒介)"
  duration: "N/A"

applicable_scenarios:
  - "杂志文章"
  - "文学评论"
  - "长文叙事"
  - "文化评论"
  - "多栏布局"
---
```

---

## 一、12 字段完整规范

### 1.1 name

```yaml
name: DLP-newyorker
```

- **唯一标识**: `DLP-newyorker`
- **检索键**: newyorker / 纽约客 / 文学评论 / 长文叙事 / 文化评论
- **族内编号**: publication-typesetting-03

### 1.2 anchor

```yaml
anchor: "The New Yorker 2024 年版式"
```

- **锚定真实世界**: The New Yorker（《纽约客》）2024 年印刷版与数字版的版式规范
- **锚定依据**: Caslon 衬线正文、3 栏杂志栅格、11pt 正文、米白背景（#FCFAF5）、New Yorker 红色标识（#CD2026）
- **品牌辨识特征**: Caslon 衬线字体 + 3 栏文学排版 + 米白纸感背景 + 文学叙事级长文排版

### 1.3 family

```yaml
family: publication-typesetting
```

- **所属族**: publication-typesetting（出版排版族）
- **族内同级**: DLP-economist / DLP-ted / DLP-kami
- **族特征**: 锚定真实世界出版物，本 DLP 专注文学评论与文化叙事类杂志排版

### 1.4 color_palette

```yaml
color_palette:
  primary: "#1A1A1A"      # 正文黑 — 正文文字、标题（纽约客以黑色为主色调）
  secondary: "#CD2026"    # New Yorker 红 — 品牌标识、栏目标识、重点强调
  accent: "#0066CC"       # 链接蓝 — 超链接、数字版交互元素
  neutral: "#6C757D"      # 中性灰 — 图注、脚注、元数据、分割线
  background: "#FCFAF5"   # 米白 — 页面背景（微暖米白，非纯白）
  text: "#1A1A1A"         # 文本色 — 正文主文字色
```

| 色板角色 | 变量名 | 十六进制值 | 用途 |
|---------|--------|-----------|------|
| 主色 Primary | `--color-primary` | `#1A1A1A` | 正文文字、标题、主体内容（纽约客以黑色为视觉主色） |
| 辅色 Secondary | `--color-secondary` | `#CD2026` | New Yorker 红色品牌标识、栏目标识、引言标记 |
| 强调色 Accent | `--color-accent` | `#0066CC` | 超链接、数字版交互元素、在线引用 |
| 中性色 Neutral | `--color-neutral` | `#6C757D` | 图注、脚注、页眉页脚、分割线、元数据 |
| 背景色 Background | `--color-bg` | `#FCFAF5` | 页面主背景（米白，微暖，纸质感） |
| 文本色 Text | `--color-text` | `#1A1A1A` | 正文主文字色 |

**配色锚定说明**：
- `#1A1A1A` 为 The New Yorker 的正文黑，作为主色——纽约客以黑色文字为视觉主体，红色仅用于品牌标识
- `#CD2026` 为 New Yorker 官方品牌红，用于报头标识与栏目强调，辨识度极高
- `#FCFAF5` 为纽约客印刷版的米白纸感背景，比纯白更温暖，适合长时间文学阅读
- `#0066CC` 为数字版链接蓝，与黑色正文形成清晰对比
- 全部色值锚定 The New Yorker 2024 年实际印刷版与 newyorker.com 数字版的实测配色

### 1.5 typography_scale

```yaml
typography_scale:
  h1: "42px / 2.625rem"       # 文章主标题（大字号，regular 而非 bold）
  h2: "28px / 1.75rem"        # 章节标题（中字号，regular）
  h3: "22px / 1.375rem"       # 小节标题（小字号，regular）
  h4: "16px / 1rem"           # 子节标题（紧凑，regular）
  body: "11pt / 14.67px"      # 正文（衬线，文学阅读级字号）
  caption: "9pt / 12px"       # 图注/表格标题
  footnote: "8pt / 10.67px"   # 脚注/来源标注
```

| 层级 | 用途 | 字号 | 行高 | 字重 |
|------|------|------|------|------|
| H1 | 文章主标题 | 42px / 2.625rem | 1.2 | 400 (regular) |
| H2 | 章节标题 | 28px / 1.75rem | 1.3 | 400 (regular) |
| H3 | 小节标题 | 22px / 1.375rem | 1.35 | 400 (regular) |
| H4 | 子节标题 | 16px / 1rem | 1.4 | 400 (regular) |
| Body | 正文 | 11pt / 14.67px | 1.6 | 400 (regular) |
| Caption | 图注/表格标题 | 9pt / 12px | 1.45 | 400 (regular) |
| Footnote | 脚注/来源标注 | 8pt / 10.67px | 1.4 | 400 (regular) |

**字号阶梯说明**：
- 正文采用 11pt（14.67px），比 DLP-economist 的 10pt 略大，适合文学叙事的长文阅读
- **所有标题层级使用 regular(400) 而非 bold**——这是 The New Yorker 的标志性排版特征，标题靠字号和字体而非字重建立层级
- H1 达到 42px，比 DLP-economist 的 36px 更大，适应文学长文的标题气势
- 行高 1.6（正文）比 DLP-economist 的 1.5 更宽松，适合文学阅读的舒适度

### 1.6 font_stack

```yaml
font_stack:
  western: '"Caslon", "Adobe Caslon Pro", "Rietveld", serif'
  chinese: '"宋体", "SimSun", "Noto Serif SC", serif'
  monospace: '"Courier New", "Courier", monospace'
```

| 用途 | 字体栈 | CSS font-family | Fallback 策略 |
|------|--------|----------------|--------------|
| 西文正文/标题 | Caslon → Adobe Caslon Pro → Rietveld → serif | `"Caslon", "Adobe Caslon Pro", "Rietveld", serif` | Caslon 为纽约客专属正文字体；Adobe Caslon Pro 为开源替代；Rietveld 为标题字体兜底 |
| 中文正文/标题 | 宋体 → SimSun → Noto Serif SC → serif | `"宋体", "SimSun", "Noto Serif SC", serif` | 宋体/SimSun 为中文衬线印刷标准；Noto Serif SC 为跨平台开源替代 |
| 等宽/代码 | Courier New → Courier → monospace | `"Courier New", "Courier", monospace` | Courier New 为印刷级等宽字体兜底 |

**字体栈锚定说明**：
- Caslon 是 The New Yorker 的标志性正文字体，基于 William Caslon 的 18 世纪衬线字体设计
- Adobe Caslon Pro 为 Adobe 公司的 Caslon 数字版本，作为首选 fallback
- Rietveld 为纽约客标题使用的字体，作为标题场景的兜底
- 中文 fallback 采用宋体/SimSun，与西文衬线字体风格一致，保持文学质感
- Caslon 字体的选择传达纽约客的"文学传统"——这是自 1925 年创刊以来的排版传承

### 1.7 font_weight_pairing

```yaml
font_weight_pairing:
  heading: "regular (400)"    # 标题字重（regular，非 bold）
  body: "regular (400)"       # 正文字重
  emphasis: "italic (400)"    # 强调字重（斜体）
```

| 元素类型 | 字重 | font-weight 值 | 说明 |
|---------|------|---------------|------|
| 标题 Heading | regular | 400 | **纽约客标志性特征**：所有标题使用 regular 而非 bold，靠字号和 Caslon 字体本身建立层级 |
| 正文 Body | regular | 400 | 正文使用 regular，与标题字重一致，形成统一的文学质感 |
| 强调 Emphasis | italic | 400 | 强调使用斜体，用于书名、外来词、强调词、心理独白 |

**字重搭配规则**：
- **标题一律 regular(400)，不使用 bold**——这是 The New Yorker 与 The Economist 最大的排版差异
- 纽约客靠 Caslon 字体本身的字形特征和字号差异建立标题层级，而非靠字重加粗
- 正文一律 regular(400)，与标题字重统一，营造文学叙事的连贯阅读感
- 强调使用 italic(400)，这是文学出版界的传统——斜体用于书名、外来词、心理独白、强调词
- 禁止使用 bold 字重，保持纽约客的文学优雅感

### 1.8 spacing_system

```yaml
spacing_system:
  base_unit: 4px
  scale: [4, 8, 12, 16, 24, 32, 48]
```

| 间距级别 | 值 | 用途 |
|---------|-----|------|
| xs | 4px | 字符间距微调、图标与文字紧贴 |
| sm | 8px | 段落内行间距微调、列表项间距 |
| md | 12px | 栏目内段落间距、图注与正文间距 |
| lg | 16px | 栏目间距（槽宽）、小节标题与正文间距 |
| xl | 24px | 章节标题上下间距、图片与正文间距 |
| 2xl | 32px | 大章节分隔、栏目组间距 |
| 3xl | 48px | 页面级大分隔、报头与正文间距 |

**间距系统说明**：
- 基准单位 4px，与 visual-dna.md 的 4px 基准栅格系统对齐
- 阶梯采用 4/8/12/16/24/32/48 的 7 级阶梯，与 DLP-economist 一致
- 多栏布局中，栏间槽宽为 16px（对应 lg 级别），确保栏目间的视觉分隔
- 文学长文的段落间距较大（24px），适应长篇叙事的阅读节奏

### 1.9 grid_system

```yaml
grid_system:
  columns: 3                  # 3 栏杂志布局
  column_width: "7cm"         # 每栏列宽 7cm
  gutter_width: "0.6cm"       # 槽宽 0.6cm（约 10px）
  margin: "2cm"               # 页边距 2cm
```

| 栅格参数 | 值 | 说明 |
|---------|-----|------|
| 列数 | 3 栏 | The New Yorker 标准杂志 3 栏布局 |
| 列宽 | 7cm / 栏 | 每栏宽度 7cm，比 DLP-economist 的 6cm 更宽，适合文学阅读 |
| 槽宽 | 0.6cm | 栏间槽宽 0.6cm（约 10px），比 DLP-economist 的 0.5cm 更宽 |
| 页边距 | 2cm | 上下左右页边距 2cm，比 DLP-economist 的 1.5cm 更宽 |
| 基线网格 | 4px | 与 spacing_system 基准对齐 |

**栅格系统说明**：
- 3 栏布局是 The New Yorker 印刷版的标志性栅格，比 DLP-economist 的 4 栏更宽松
- 列宽 7cm 比 DLP-economist 的 6cm 更宽，适应 11pt 正文的舒适文学阅读
- 槽宽 0.6cm（约 10px）比 DLP-economist 的 0.5cm 更宽，营造文学排版的呼吸感
- 页边距 2cm 比 DLP-economist 的 1.5cm 更宽，整体留白更多，适合文学叙事的沉浸感

### 1.10 radius_shadow

```yaml
radius_shadow:
  border_radius: "0px"    # 圆角 0px — 印刷级直角
  box_shadow: "none"      # 阴影 none — 印刷媒介无阴影
```

| 元素类型 | 圆角值 | 阴影值 | 说明 |
|---------|--------|--------|------|
| 卡片/Card | 0px | none | 印刷媒介无圆角无阴影，靠栏位与分割线分隔 |
| 图片/Image | 0px | none | 图片直角裁切，无圆角 |
| 引用块/Quote | 0px | none | 引用块靠左侧红色竖线分隔，无圆角无阴影 |
| 表格/Table | 0px | none | 表格直角边框，无圆角 |
| 装饰元素 | 0px | none | 纽约客风格的插图/漫画均为直角，无圆角 |

**圆角阴影说明**：
- 圆角 0px 是 The New Yorker 印刷版的核心视觉特征——所有元素均为直角，传达文学出版的严肃感
- 阴影 none 是印刷媒介的必然约束——印刷品无法产生阴影
- 纽约客的标志性插图和漫画均为直角矩形，无圆角处理
- 禁止使用任何圆角和阴影，这是 DLP-newyorker 的硬性规范

### 1.11 motion_curve

```yaml
motion_curve: "N/A (印刷媒介)"
```

| 动效场景 | 缓动曲线 | 时长 | 说明 |
|---------|---------|------|------|
| 印刷版 | N/A | N/A | 印刷媒介无动效 |
| 数字版页面切换 | ease-in-out | 300ms | 数字版可使用极简淡入淡出，保持克制 |
| 数字版元素出现 | ease-out | 200ms | 数字版元素可使用极简上滑淡入 |

**动效曲线说明**：
- The New Yorker 本质是印刷媒介，核心版式无动效概念
- 数字版（newyorker.com）的动效极其克制，仅使用极简的淡入淡出
- 禁止使用弹跳、旋转、缩放等装饰性动效，保持文学出版的沉静感

### 1.12 applicable_scenarios

```yaml
applicable_scenarios:
  - "杂志文章"
  - "文学评论"
  - "长文叙事"
  - "文化评论"
  - "多栏布局"
```

| 场景标签 | 匹配优先级 | 典型用例 |
|---------|-----------|---------|
| 杂志文章 | 高 | 期刊、杂志、文学刊物的长文排版 |
| 文学评论 | 高 | 书评、文学批评、作家访谈 |
| 长文叙事 | 高 | 非虚构叙事、深度报道、纪实文学 |
| 文化评论 | 高 | 文化现象评论、艺术评论、社会观察 |
| 多栏布局 | 中 | 需要 3 栏多栏排版的版面设计 |

---

## 二、DLP 检索对接规范

### 2.1 检索命中条件

当以下语义信号出现时，DLP 检索器应优先匹配 `DLP-newyorker`：

1. **内容主题信号**: 文学、文化、艺术、叙事、非虚构、书评、影评、文化评论
2. **任务类型信号**: wechat_article（公众号长文）、research_report（文化研究）
3. **受众信号**: general（大众读者）、academic（文学研究者）
4. **排版需求信号**: 文学叙事、长文排版、3 栏布局、Caslon 衬线质感

### 2.2 design_tokens 输出

```yaml
design_tokens:
  color_scheme:
    primary: "#1A1A1A"
    secondary: "#CD2026"
    accent: "#0066CC"
    neutral: "#6C757D"
    background: "#FCFAF5"
    text: "#1A1A1A"
  font_scheme:
    heading_font: '"Caslon", "Adobe Caslon Pro", "Rietveld", serif'
    body_font: '"Caslon", "Adobe Caslon Pro", "Rietveld", serif'
    chinese_font: '"宋体", "SimSun", "Noto Serif SC", serif'
    monospace_font: '"Courier New", "Courier", monospace'
  typography:
    h1_size: "42px"
    h2_size: "28px"
    h3_size: "22px"
    h4_size: "16px"
    body_size: "14.67px"
    caption_size: "12px"
    footnote_size: "10.67px"
    heading_weight: 400
    body_weight: 400
    emphasis_weight: "italic 400"
  spacing:
    base: 4px
    scale: [4, 8, 12, 16, 24, 32, 48]
  grid:
    columns: 3
    column_width: "7cm"
    gutter: "0.6cm"
    margin: "2cm"
  visual:
    border_radius: "0px"
    box_shadow: "none"
  motion:
    type: "N/A (印刷媒介)"
```

### 2.3 与 visual_dna 的对接映射

| DLP 字段 | visual_dna 字段 | 映射规则 |
|---------|----------------|---------|
| `color_palette.primary` | `--color-text` | 正文黑映射为文字色（纽约客以黑色为主色） |
| `color_palette.secondary` | `--color-primary` | New Yorker 红映射为主色（品牌标识色） |
| `color_palette.background` | `--color-bg` | 米白背景直接映射 |
| `typography_scale.body` | `font_scheme.body_size` | 11pt 正文字号直接映射 |
| `font_stack.western` | `font_scheme.body_font` | Caslon 字体栈直接注入 |
| `grid_system.columns` | `grid_system.columns` | 3 栏栅格直接映射 |
| `font_weight_pairing.heading` | `font_scheme.heading_weight` | regular(400) 标题字重直接映射 |

---

## 三、与 TA/LA 原子库的对接

### 3.1 TA 排版原子对接

| TA 原子 ID | 原子名称 | 对接用途 |
|-----------|---------|---------|
| TA-SCALE-001 | H1 字号阶梯 | 42px 文学大标题字号 |
| TA-SCALE-003 | H3 字号阶梯 | 22px 小节标题字号 |
| TA-WEIGHT-002 | 正文 regular 字重 | 400 字重用于正文 |
| TA-WEIGHT-004 | 标题 regular 字重 | 400 字重用于标题（纽约客特色） |
| TA-WEIGHT-003 | 强调 italic 字重 | 400 italic 用于书名/外来词/心理独白 |
| TA-LINE-002 | 正文行高 1.6 | 文学阅读级行高 |
| TA-PARA-002 | 多栏排版 | 3 栏杂志布局的段落排版 |
| TA-PARA-005 | 首字下沉 | 文学叙事的首字下沉排版 |
| TA-MIX-001 | 中英文间距 | 中英文混排时的间距控制 |

### 3.2 LA 布局原子对接

| LA 原子 ID | 原子名称 | 对接用途 |
|-----------|---------|---------|
| LA-GRID-005 | 杂志三栏 | 3 栏杂志布局 |
| LA-PAGE-002 | 文章页布局 | 文学文章页的整体布局 |
| LA-SPECIAL-001 | 首字下沉布局 | 文学叙事的首字下沉布局 |
| LA-SPECIAL-004 | 页眉页脚布局 | 报头标识与页脚的布局 |

---

## 四、ASR 硬门合规说明

本 DLP 的视觉规范天然符合以下 ASR 硬门禁令：

| ASR 禁令编号 | 禁令内容 | 本 DLP 合规性 |
|-------------|---------|-------------|
| ASR-FONT-001 | 禁 Inter 作为 Premium 产出字体 | ✅ 使用 Caslon 衬线字体 |
| ASR-FONT-003 | 禁 Arial 作为正文字体 | ✅ 使用 Caslon 衬线字体 |
| ASR-COLOR-002 | 禁纯黑（#000000） | ✅ 使用 #1A1A1A 正文黑 |
| ASR-COLOR-003 | 禁纯白（#FFFFFF）作为大面积背景 | ✅ 使用 #FCFAF5 米白背景 |
| ASR-LAYOUT-004 | 禁默认 Tailwind 间距阶梯 | ✅ 使用 4/8/12/16/24/32/48 自定义阶梯 |
| ASR-DECOR-003 | 禁阴影堆叠超过 3 层 | ✅ 阴影 none，零层堆叠 |

---

## 五、与 DLP-economist 的差异化对比

| 对比维度 | DLP-economist | DLP-newyorker | 差异说明 |
|---------|--------------|---------------|---------|
| 栏数 | 4 栏 | 3 栏 | 纽约客更宽松，适合文学阅读 |
| 列宽 | 6cm | 7cm | 纽约客栏宽更大，行长更舒适 |
| 正文字号 | 10pt | 11pt | 纽约客字号更大，适合文学叙事 |
| 标题字重 | bold(700) | regular(400) | **核心差异**：纽约客标题不加粗 |
| 背景色 | #FDFDFD（纸白） | #FCFAF5（米白） | 纽约客背景更暖，纸感更强 |
| 主色 | #E3120B（Economist 红） | #1A1A1A（正文黑） | 经济学人以红色为主色，纽约客以黑色为主色 |
| 字体 | Milo Serif | Caslon | 不同的衬线字体传统 |
| 适用场景 | 经济分析、新闻评论 | 文学评论、长文叙事 | 不同的内容定位 |

---

> **DLP 元数据**
> - 创建时间: 2026-06-19
> - 族: publication-typesetting
> - 锚定: The New Yorker 2024 年版式
> - 字段完整性: 12/12 ✅
> - 配色锚定: 真实世界出版物实测配色 ✅
> - 字体栈中文 fallback: 已包含 ✅
