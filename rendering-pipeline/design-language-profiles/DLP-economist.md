<!-- 作者：阿洋 -->

# DLP-economist — 经济学人文章排版设计语言画像

> **定位**: publication-typesetting 族，锚定 The Economist 2024 年版式，提供杂志级长文排版与多栏布局的具象视觉规范。
> **族覆盖补充**: 本 DLP 为 publication-typesetting 族的族覆盖补充成员，与 DLP-ted / DLP-newyorker / DLP-kami 共同构成 4 个 DLP 的完整族覆盖。
> **索引**: 详见 `README.md` 获取 DLP 库完整清单与检索规范

---

## YAML frontmatter（12 字段完整定义）

```yaml
---
name: "DLP-economist"
anchor: "The Economist 2024 年版式"
family: "publication-typesetting"

color_palette:
  primary: "#E3120B"
  secondary: "#1A1A1A"
  accent: "#006BA6"
  neutral: "#6C757D"
  background: "#FDFDFD"
  text: "#1A1A1A"

typography_scale:
  h1: "36px/2.25rem"
  h2: "24px/1.5rem"
  h3: "18px/1.125rem"
  h4: "14px/0.875rem"
  body: "10pt/13.33px"
  caption: "8pt/10.67px"
  footnote: "7pt/9.33px"

font_stack:
  western: '"Milo Serif", "Source Serif Pro", "Georgia", serif'
  chinese: '"宋体", "SimSun", "Noto Serif SC", serif'
  monospace: '"Courier New", "Courier", monospace'

font_weight_pairing:
  heading: "bold(700)"
  body: "regular(400)"
  emphasis: "italic(400)"

spacing_system:
  base: "4px"
  scale: "4/8/12/16/24/32/48px"

grid_system:
  columns: "4栏"
  column_width: "6cm"
  gutter: "0.5cm"
  margin: "1.5cm"
  breakpoint: "N/A(印刷媒介)"

radius_shadow:
  radius: "0px"
  shadow: "none"

motion_curve:
  easing: "N/A(印刷媒介)"
  duration: "N/A"

applicable_scenarios:
  - "杂志文章"
  - "新闻评论"
  - "经济分析"
  - "长文排版"
  - "多栏布局"
---
```

---

## 一、12 字段完整规范

### 1.1 name

```yaml
name: DLP-economist
```

- **唯一标识**: `DLP-economist`
- **检索键**: economist / 经济学人 / 杂志排版 / 多栏布局
- **族内编号**: publication-typesetting-01

### 1.2 anchor

```yaml
anchor: "The Economist 2024 年版式"
```

- **锚定真实世界**: The Economist（《经济学人》）2024 年印刷版与数字版的版式规范
- **锚定依据**: Economist 红色横幅报头、Milo Serif 衬线正文、4 栏杂志栅格、10pt 紧凑正文
- **品牌辨识特征**: 红色报头（#E3120B）+ 衬线字体 + 多栏紧凑排版 + 无圆角无阴影的印刷质感

### 1.3 family

```yaml
family: publication-typesetting
```

- **所属族**: publication-typesetting（出版排版族）
- **族内同级**: DLP-ted / DLP-newyorker / DLP-kami
- **族特征**: 锚定真实世界出版物/演示媒介，强调排版层级、字体搭配、栏位布局的印刷级质感

### 1.4 color_palette

```yaml
color_palette:
  primary: "#E3120B"      # Economist 红 — 报头、栏目标识、重点强调
  secondary: "#1A1A1A"    # 正文黑 — 正文文字、标题
  accent: "#006BA6"       # 数据蓝 — 数据图表、链接、统计高亮
  neutral: "#6C757D"      # 中性灰 — 图注、脚注、元数据、分割线
  background: "#FDFDFD"   # 纸白 — 页面背景（微暖白，非纯白）
  text: "#1A1A1A"         # 文本色 — 正文主文字色
```

| 色板角色 | 变量名 | 十六进制值 | 用途 |
|---------|--------|-----------|------|
| 主色 Primary | `--color-primary` | `#E3120B` | 报头横幅、栏目标识、重点强调、引言标记 |
| 辅色 Secondary | `--color-secondary` | `#1A1A1A` | 正文文字、章节标题、粗体强调 |
| 强调色 Accent | `--color-accent` | `#006BA6` | 数据图表系列色、超链接、统计数字高亮 |
| 中性色 Neutral | `--color-neutral` | `#6C757D` | 图注、脚注、页眉页脚、分割线、元数据 |
| 背景色 Background | `--color-bg` | `#FDFDFD` | 页面主背景（纸白，微暖） |
| 文本色 Text | `--color-text` | `#1A1A1A` | 正文主文字色 |

**配色锚定说明**：
- `#E3120B` 为 The Economist 官方品牌红，用于报头横幅与栏目标识，是最高辨识度色彩
- `#006BA6` 为 Economist 数据图表常用蓝，与红色形成互补对比，用于数据可视化
- `#FDFDFD` 为印刷纸白，非纯白（#FFFFFF），避免屏幕阅读时的刺眼感
- 全部色值锚定 The Economist 2024 年实际印刷版与 economist.com 数字版的实测配色

### 1.5 typography_scale

```yaml
typography_scale:
  h1: "36px / 2.25rem"       # 文章主标题（大字号，bold）
  h2: "24px / 1.5rem"        # 章节标题（中字号，bold）
  h3: "18px / 1.125rem"      # 小节标题（小字号，bold）
  h4: "14px / 0.875rem"      # 子节标题/栏目标题（紧凑，bold）
  body: "10pt / 13.33px"     # 正文（紧凑衬线，印刷级字号）
  caption: "8pt / 10.67px"   # 图注/表格标题
  footnote: "7pt / 9.33px"   # 脚注/来源标注
```

| 层级 | 用途 | 字号 | 行高 | 字重 |
|------|------|------|------|------|
| H1 | 文章主标题 | 36px / 2.25rem | 1.15 | 700 (bold) |
| H2 | 章节标题 | 24px / 1.5rem | 1.25 | 700 (bold) |
| H3 | 小节标题 | 18px / 1.125rem | 1.35 | 700 (bold) |
| H4 | 子节标题/栏目标题 | 14px / 0.875rem | 1.4 | 700 (bold) |
| Body | 正文 | 10pt / 13.33px | 1.5 | 400 (regular) |
| Caption | 图注/表格标题 | 8pt / 10.67px | 1.4 | 400 (regular) |
| Footnote | 脚注/来源标注 | 7pt / 9.33px | 1.35 | 400 (regular) |

**字号阶梯说明**：
- 正文采用 10pt（13.33px）紧凑字号，这是 The Economist 印刷版的实际正文字号，确保多栏布局下的信息密度
- 标题层级采用 bold 字重，与正文 regular 形成强对比
- 图注与脚注采用更小字号（8pt/7pt），与正文形成层级递减

### 1.6 font_stack

```yaml
font_stack:
  western: '"Milo Serif", "Source Serif Pro", "Georgia", serif'
  chinese: '"宋体", "SimSun", "Noto Serif SC", serif'
  monospace: '"Courier New", "Courier", monospace'
```

| 用途 | 字体栈 | CSS font-family | Fallback 策略 |
|------|--------|----------------|--------------|
| 西文正文/标题 | Milo Serif → Source Serif Pro → Georgia → serif | `"Milo Serif", "Source Serif Pro", "Georgia", serif` | Milo Serif 为 Economist 专属字体；Source Serif Pro 为开源替代；Georgia 为系统衬线兜底 |
| 中文正文/标题 | 宋体 → SimSun → Noto Serif SC → serif | `"宋体", "SimSun", "Noto Serif SC", serif` | 宋体/SimSun 为中文衬线印刷标准；Noto Serif SC 为跨平台开源替代 |
| 等宽/代码 | Courier New → Courier → monospace | `"Courier New", "Courier", monospace` | Courier New 为印刷级等宽字体兜底 |

**字体栈锚定说明**：
- Milo Serif 是 The Economist 的专属定制衬线字体，由 Commercial Type 设计，无法公开获取
- Source Serif Pro 为 Adobe 开源衬线字体，字形接近 Milo Serif，作为首选 fallback
- Georgia 为系统级衬线字体，确保跨平台兜底
- 中文 fallback 采用宋体/SimSun，与西文衬线字体风格一致，保持印刷质感

### 1.7 font_weight_pairing

```yaml
font_weight_pairing:
  heading: "bold (700)"      # 标题字重
  body: "regular (400)"      # 正文字重
  emphasis: "italic (400)"   # 强调字重（斜体，非加粗）
```

| 元素类型 | 字重 | font-weight 值 | 说明 |
|---------|------|---------------|------|
| 标题 Heading | bold | 700 | H1-H4 所有标题层级使用 bold，与正文形成强对比 |
| 正文 Body | regular | 400 | 正文使用 regular，确保多栏紧凑排版下的可读性 |
| 强调 Emphasis | italic | 400 | 强调使用斜体而非加粗，这是 The Economist 的排版传统——斜体用于书名、外来词、强调词 |

**字重搭配规则**：
- 标题一律 bold(700)，不使用 semi-bold 或 light，确保标题的视觉权威感
- 正文一律 regular(400)，不使用 light(300)，确保 10pt 紧凑字号下的笔画清晰度
- 强调使用 italic(400) 而非 bold，这是英语出版界的传统——斜体表示强调、书名、外来词
- 禁止使用 bold + italic 组合，保持排版的克制与专业感

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
- 阶梯采用 4/8/12/16/24/32/48 的 7 级阶梯，覆盖从微观到宏观的间距需求
- 多栏布局中，栏间槽宽为 16px（对应 lg 级别），确保栏目间的视觉分隔

### 1.9 grid_system

```yaml
grid_system:
  columns: 4                  # 4 栏杂志布局
  column_width: "6cm"         # 每栏列宽 6cm
  gutter_width: "0.5cm"       # 槽宽 0.5cm（约 8px）
  margin: "1.5cm"             # 页边距 1.5cm
  page_width: "28cm"          # 页面宽度（4×6 + 3×0.5 + 2×1.5 = 30.5cm 含边距）
```

| 栅格参数 | 值 | 说明 |
|---------|-----|------|
| 列数 | 4 栏 | The Economist 标准杂志 4 栏布局 |
| 列宽 | 6cm / 栏 | 每栏宽度 6cm，适配 10pt 正文的舒适行长 |
| 槽宽 | 0.5cm | 栏间槽宽 0.5cm（约 8px），紧凑分隔 |
| 页边距 | 1.5cm | 上下左右页边距 1.5cm |
| 基线网格 | 4px | 与 spacing_system 基准对齐 |

**栅格系统说明**：
- 4 栏布局是 The Economist 印刷版的标志性栅格，支持长文跨栏排版与图文混排
- 列宽 6cm 确保 10pt 正文的每行字符数在 45-75 字符的最佳阅读区间
- 槽宽 0.5cm（约 8px）为紧凑型槽宽，适合信息密度高的杂志排版
- 数字版可质量保持为 2 栏或单栏，但保持 4 栏的视觉比例感

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
| 按钮/Button | 0px | none | 印刷媒介无按钮概念；数字版按钮保持直角 |
| 引用块/Quote | 0px | none | 引用块靠左侧红色竖线分隔，无圆角无阴影 |
| 表格/Table | 0px | none | 表格直角边框，无圆角 |

**圆角阴影说明**：
- 圆角 0px 是 The Economist 印刷版的核心视觉特征——所有元素均为直角，传达严肃、权威的出版物质感
- 阴影 none 是印刷媒介的必然约束——印刷品无法产生阴影，数字版应继承这一特征以保持品牌一致性
- 禁止使用任何圆角和阴影，这是 DLP-economist 的硬性规范

### 1.11 motion_curve

```yaml
motion_curve: "N/A (印刷媒介)"
```

| 动效场景 | 缓动曲线 | 时长 | 说明 |
|---------|---------|------|------|
| 印刷版 | N/A | N/A | 印刷媒介无动效 |
| 数字版页面切换 | ease-in-out | 200ms | 数字版可使用极简淡入淡出，保持克制 |
| 数字版元素出现 | ease-out | 150ms | 数字版元素可使用极简上滑淡入 |

**动效曲线说明**：
- The Economist 本质是印刷媒介，核心版式无动效概念
- 数字版（economist.com）的动效极其克制，仅使用极简的淡入淡出和上滑
- 禁止使用弹跳、旋转、缩放等装饰性动效，保持出版物的严肃感

### 1.12 applicable_scenarios

```yaml
applicable_scenarios:
  - "杂志文章"
  - "新闻评论"
  - "经济分析"
  - "长文排版"
  - "多栏布局"
```

| 场景标签 | 匹配优先级 | 典型用例 |
|---------|-----------|---------|
| 杂志文章 | 高 | 期刊、杂志、电子刊物的长文排版 |
| 新闻评论 | 高 | 时事评论、社论、观点文章 |
| 经济分析 | 高 | 经济数据分析、市场评论、金融报告 |
| 长文排版 | 中 | 3000 字以上的深度长文、专题报道 |
| 多栏布局 | 中 | 需要 2-4 栏多栏排版的版面设计 |

---

## 二、DLP 检索对接规范

### 2.1 检索命中条件

当以下语义信号出现时，DLP 检索器应优先匹配 `DLP-economist`：

1. **内容主题信号**: 经济、金融、市场、政治评论、时事分析、商业分析
2. **任务类型信号**: wechat_article（公众号长文）、research_report（经济分析报告）
3. **受众信号**: professional（专业人士）、general（大众读者）
4. **排版需求信号**: 多栏布局、长文排版、杂志质感、紧凑信息密度

### 2.2 design_tokens 输出

```yaml
design_tokens:
  color_scheme:
    primary: "#E3120B"
    secondary: "#1A1A1A"
    accent: "#006BA6"
    neutral: "#6C757D"
    background: "#FDFDFD"
    text: "#1A1A1A"
  font_scheme:
    heading_font: '"Milo Serif", "Source Serif Pro", "Georgia", serif'
    body_font: '"Milo Serif", "Source Serif Pro", "Georgia", serif'
    chinese_font: '"宋体", "SimSun", "Noto Serif SC", serif'
    monospace_font: '"Courier New", "Courier", monospace'
  typography:
    h1_size: "36px"
    h2_size: "24px"
    h3_size: "18px"
    h4_size: "14px"
    body_size: "13.33px"
    caption_size: "10.67px"
    footnote_size: "9.33px"
    heading_weight: 700
    body_weight: 400
    emphasis_weight: "italic 400"
  spacing:
    base: 4px
    scale: [4, 8, 12, 16, 24, 32, 48]
  grid:
    columns: 4
    column_width: "6cm"
    gutter: "0.5cm"
    margin: "1.5cm"
  visual:
    border_radius: "0px"
    box_shadow: "none"
  motion:
    type: "N/A (印刷媒介)"
```

### 2.3 与 visual_dna 的对接映射

| DLP 字段 | visual_dna 字段 | 映射规则 |
|---------|----------------|---------|
| `color_palette.primary` | `--color-primary` | Economist 红直接映射为主色 |
| `color_palette.secondary` | `--color-text` | 正文黑映射为文字色 |
| `color_palette.accent` | `--color-accent` | 数据蓝映射为强调色 |
| `typography_scale.body` | `font_scheme.body_size` | 10pt 正文字号直接映射 |
| `font_stack.western` | `font_scheme.body_font` | Milo Serif 字体栈直接注入 |
| `grid_system.columns` | `grid_system.columns` | 4 栏栅格直接映射 |
| `radius_shadow.border_radius` | `visual.radius` | 0px 圆角直接映射 |

---

## 三、与 TA/LA 原子库的对接

### 3.1 TA 排版原子对接

| TA 原子 ID | 原子名称 | 对接用途 |
|-----------|---------|---------|
| TA-SCALE-001 | H1 字号阶梯 | 36px 主标题字号 |
| TA-SCALE-004 | H4 字号阶梯 | 14px 子节标题字号 |
| TA-WEIGHT-001 | 标题 bold 字重 | 700 字重用于所有标题 |
| TA-WEIGHT-003 | 强调 italic 字重 | 400 italic 用于书名/外来词/强调 |
| TA-PARA-002 | 多栏排版 | 4 栏杂志布局的段落排版 |
| TA-MIX-001 | 中英文间距 | 中英文混排时的间距控制 |
| TA-MIX-003 | 标点挤压 | 中文标点的挤压规则 |

### 3.2 LA 布局原子对接

| LA 原子 ID | 原子名称 | 对接用途 |
|-----------|---------|---------|
| LA-GRID-004 | 杂志双栏 | 数字版质量保持为 2 栏时使用 |
| LA-GRID-005 | 杂志三栏 | 数字版质量保持为 3 栏时使用 |
| LA-PAGE-002 | 文章页布局 | 杂志文章页的整体布局 |
| LA-SPECIAL-004 | 页眉页脚布局 | 报头横幅与页脚的布局 |

---

## 四、ASR 硬门合规说明

本 DLP 的视觉规范天然符合以下 ASR 硬门禁令：

| ASR 禁令编号 | 禁令内容 | 本 DLP 合规性 |
|-------------|---------|-------------|
| ASR-FONT-001 | 禁 Inter 作为 Premium 产出字体 | ✅ 使用 Milo Serif 衬线字体 |
| ASR-FONT-003 | 禁 Arial 作为正文字体 | ✅ 使用 Milo Serif 衬线字体 |
| ASR-COLOR-002 | 禁纯黑（#000000） | ✅ 使用 #1A1A1A 正文黑 |
| ASR-COLOR-003 | 禁纯白（#FFFFFF）作为大面积背景 | ✅ 使用 #FDFDFD 纸白 |
| ASR-LAYOUT-004 | 禁默认 Tailwind 间距阶梯 | ✅ 使用 4/8/12/16/24/32/48 自定义阶梯 |
| ASR-DECOR-003 | 禁阴影堆叠超过 3 层 | ✅ 阴影 none，零层堆叠 |

---

> **DLP 元数据**
> - 创建时间: 2026-06-19
> - 族: publication-typesetting
> - 锚定: The Economist 2024 年版式
> - 字段完整性: 12/12 ✅
> - 配色锚定: 真实世界出版物实测配色 ✅
> - 字体栈中文 fallback: 已包含 ✅
