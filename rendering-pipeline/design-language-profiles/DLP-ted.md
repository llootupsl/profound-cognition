<!-- 作者：阿洋 -->

# DLP-ted — TED 演示风格设计语言画像

> **定位**: publication-typesetting 族，锚定 TED Talks 2024 年演示风格，融入 slidecraft-skill 的 TED 风格演示专精能力。
> **融入来源技能**: slidecraft-skill — TED 风格演示特征（极简电影感、大字号排版、大量留白、每页一个核心观点、拒绝花哨模板、靠排版层级与留白出高级感）
> **索引**: 详见 `README.md` 获取 DLP 库完整清单与检索规范

---

## YAML frontmatter（12 字段完整定义）

```yaml
---
name: "DLP-ted"
anchor: "TED Talks 2024 年演示风格"
family: "publication-typesetting"

color_palette:
  primary: "#E62B1E"
  secondary: "#1A1A1A"
  accent: "#FFFFFF"
  neutral: "#767676"
  background: "#1A1A1A"
  text: "#FFFFFF"

typography_scale:
  h1: "72px/4.5rem"
  h2: "48px/3rem"
  h3: "36px/2.25rem"
  h4: "28px/1.75rem"
  body: "24px/1.5rem"
  caption: "18px/1.125rem"
  footnote: "14px/0.875rem"

font_stack:
  western: '"TED Serif", "Georgia", "Times New Roman", serif'
  chinese: '"宋体", "SimSun", "Noto Serif SC", serif'
  monospace: '"Courier New", "Courier", monospace'

font_weight_pairing:
  heading: "bold(700)"
  body: "regular(400)"
  emphasis: "italic(400)"

spacing_system:
  base: "8px"
  scale: "8/16/24/32/48/64/96px"

grid_system:
  columns: "单栏"
  column_width: "1280px"
  gutter: "N/A"
  margin: "64px"
  breakpoint: "N/A(演示媒介)"

radius_shadow:
  radius: "0px"
  shadow: "none"

motion_curve:
  easing: "ease-in-out/ease-out"
  duration: "200-400ms"

applicable_scenarios:
  - "演示文稿"
  - "TED风格"
  - "极简电影感"
  - "大字号"
  - "留白驱动"
---
```

---

## 一、12 字段完整规范

### 1.1 name

```yaml
name: DLP-ted
```

- **唯一标识**: `DLP-ted`
- **检索键**: ted / 演示文稿 / 幻灯片 / 极简电影感 / 大字号 / 留白驱动
- **族内编号**: publication-typesetting-02

### 1.2 anchor

```yaml
anchor: "TED Talks 2024 年演示风格"
```

- **锚定真实世界**: TED Talks 2024 年官方演示幻灯片风格（TED Conference 演讲者幻灯片规范）
- **锚定依据**: TED 红色品牌色（#E62B1E）、大字号演示排版（72px 大标题）、16:9 单栏演示栅格、极简电影感视觉风格
- **品牌辨识特征**: TED 红 + 深色模式背景 + 大字号衬线标题 + 极简留白 + 每页一个核心观点

### 1.3 family

```yaml
family: publication-typesetting
```

- **所属族**: publication-typesetting（出版排版族）
- **族内同级**: DLP-economist / DLP-newyorker / DLP-kami
- **族特征**: 锚定真实世界出版物/演示媒介，本 DLP 专注演示文稿（slide）这一特殊出版形态

### 1.4 color_palette

```yaml
color_palette:
  # 深色模式（TED 演讲默认）
  primary: "#E62B1E"       # TED 红 — 品牌标识、重点强调、CTA
  secondary: "#1A1A1A"     # 正文黑 — 深色模式背景
  accent: "#FFFFFF"        # 白 — 深色模式正文文字
  neutral: "#767676"       # 中性灰 — 辅助文字、元数据
  background: "#1A1A1A"    # 深色模式背景
  text: "#FFFFFF"          # 深色模式文本色

  # 浅色模式（部分 TED 演讲使用）
  background_light: "#FFFFFF"   # 浅色模式背景
  text_light: "#1A1A1A"         # 浅色模式文本色
```

| 色板角色 | 变量名 | 深色模式值 | 浅色模式值 | 用途 |
|---------|--------|-----------|-----------|------|
| 主色 Primary | `--color-primary` | `#E62B1E` | `#E62B1E` | TED 品牌红，用于 logo、重点强调、引言标记 |
| 辅色 Secondary | `--color-secondary` | `#1A1A1A` | `#1A1A1A` | 深色模式背景 / 浅色模式正文 |
| 强调色 Accent | `--color-accent` | `#FFFFFF` | `#1A1A1A` | 深色模式正文 / 浅色模式正文 |
| 中性色 Neutral | `--color-neutral` | `#767676` | `#767676` | 辅助文字、元数据、时间戳 |
| 背景色 Background | `--color-bg` | `#1A1A1A` | `#FFFFFF` | 演示页面背景 |
| 文本色 Text | `--color-text` | `#FFFFFF` | `#1A1A1A` | 演示正文文字 |

**配色锚定说明**：
- `#E62B1E` 为 TED 官方品牌红，用于 TED logo 与重点强调，是最高辨识度色彩
- 深色模式（背景 #1A1A1A + 文字 #FFFFFF）是 TED 演讲的主流模式，营造电影感与沉浸感
- 浅色模式（背景 #FFFFFF + 文字 #1A1A1A）用于部分需要明亮氛围的演讲
- `#767676` 中性灰用于辅助信息，确保不干扰核心观点的视觉聚焦

### 1.5 typography_scale

```yaml
typography_scale:
  h1: "72px / 4.5rem"      # 演示大标题（超大字号，bold）
  h2: "48px / 3rem"        # 章节标题（大字号，bold）
  h3: "36px / 2.25rem"     # 小节标题（中字号，bold）
  h4: "28px / 1.75rem"     # 子节标题（小字号，bold）
  body: "24px / 1.5rem"    # 正文（演示级大字号）
  caption: "18px / 1.125rem"  # 图注/辅助文字
  footnote: "14px / 0.875rem" # 脚注/来源标注
```

| 层级 | 用途 | 字号 | 行高 | 字重 |
|------|------|------|------|------|
| H1 | 演示大标题 | 72px / 4.5rem | 1.1 | 700 (bold) |
| H2 | 章节标题 | 48px / 3rem | 1.2 | 700 (bold) |
| H3 | 小节标题 | 36px / 2.25rem | 1.25 | 700 (bold) |
| H4 | 子节标题 | 28px / 1.75rem | 1.3 | 700 (bold) |
| Body | 正文 | 24px / 1.5rem | 1.4 | 400 (regular) |
| Caption | 图注/辅助文字 | 18px / 1.125rem | 1.35 | 400 (regular) |
| Footnote | 脚注/来源标注 | 14px / 0.875rem | 1.3 | 400 (regular) |

**字号阶梯说明**：
- 演示文稿采用超大字号阶梯，H1 达到 72px，确保远距离可读性
- 正文字号 24px 远大于印刷媒介（对比 DLP-economist 的 13.33px），适应演示场景的观看距离
- 字号阶梯遵循 1.5 倍递增比例（72→48→36→28→24），形成清晰的视觉层级
- 大字号排版是 TED 风格的核心特征——靠字号差异建立信息层级，而非靠颜色或装饰

### 1.6 font_stack

```yaml
font_stack:
  western: '"TED Serif", "Georgia", "Times New Roman", serif'
  chinese: '"宋体", "SimSun", "Noto Serif SC", serif'
  monospace: '"Courier New", "Courier", monospace'
```

| 用途 | 字体栈 | CSS font-family | Fallback 策略 |
|------|--------|----------------|--------------|
| 西文标题/正文 | TED Serif → Georgia → Times New Roman → serif | `"TED Serif", "Georgia", "Times New Roman", serif` | TED Serif 为 TED 定制衬线字体；Georgia 为系统衬线兜底；Times New Roman 为经典衬线兜底 |
| 中文标题/正文 | 宋体 → SimSun → Noto Serif SC → serif | `"宋体", "SimSun", "Noto Serif SC", serif` | 宋体/SimSun 为中文衬线标准；Noto Serif SC 为跨平台开源替代 |
| 等宽/代码 | Courier New → Courier → monospace | `"Courier New", "Courier", monospace` | Courier New 为等宽字体兜底 |

**字体栈锚定说明**：
- TED Serif 是 TED Conference 的定制衬线字体，用于官方演讲幻灯片
- Georgia 为系统级衬线字体，字形接近 TED Serif，作为首选 fallback
- Times New Roman 为经典衬线字体，确保跨平台兜底
- 中文 fallback 采用宋体/SimSun，与西文衬线字体风格一致
- 衬线字体的选择传达 TED 的"思想严肃性"——这不是娱乐，而是值得认真对待的观点

### 1.7 font_weight_pairing

```yaml
font_weight_pairing:
  heading: "bold (700)"      # 标题字重
  body: "regular (400)"      # 正文字重
  emphasis: "italic (400)"   # 强调字重（斜体）
```

| 元素类型 | 字重 | font-weight 值 | 说明 |
|---------|------|---------------|------|
| 标题 Heading | bold | 700 | H1-H4 所有标题层级使用 bold，配合大字号形成强烈视觉冲击 |
| 正文 Body | regular | 400 | 正文使用 regular，确保大字号下的优雅感 |
| 强调 Emphasis | italic | 400 | 强调使用斜体，用于引言、书名、外来词 |

**字重搭配规则**：
- 标题一律 bold(700)，配合 72px 大字号，形成"一句话击中观众"的视觉冲击力
- 正文一律 regular(400)，大字号 regular 比大字号 bold 更优雅、更易读
- 强调使用 italic(400)，保持 TED 风格的克制与高级感
- 禁止使用 bold + italic 组合，避免视觉过度强调

### 1.8 spacing_system

```yaml
spacing_system:
  base_unit: 8px
  scale: [8, 16, 24, 32, 48, 64, 96]
```

| 间距级别 | 值 | 用途 |
|---------|-----|------|
| xs | 8px | 字符间距微调、图标与文字紧贴 |
| sm | 16px | 元素内间距、列表项间距 |
| md | 24px | 段落间距、图注与正文间距 |
| lg | 32px | 小节标题与正文间距、元素组间距 |
| xl | 48px | 章节标题上下间距、大元素间距 |
| 2xl | 64px | 页面边距、大区块分隔 |
| 3xl | 96px | 页面级大留白、核心观点的呼吸空间 |

**间距系统说明**：
- 基准单位 8px（大于 DLP-economist 的 4px），适应演示文稿的大字号场景
- 阶梯采用 8/16/24/32/48/64/96 的 7 级阶梯，最大间距达 96px，支撑 TED 风格的大量留白
- 96px 的大留白是 TED 风格的核心——"留白驱动"意味着核心观点周围有充足的呼吸空间
- 页面边距 64px（对应 2xl 级别），确保内容不贴边，营造高级感

### 1.9 grid_system

```yaml
grid_system:
  columns: 1                  # 单栏演示布局
  column_width: "1280px"      # 16:9 标准演示宽度
  gutter_width: "N/A"         # 单栏无槽宽
  margin: "64px"              # 页面边距 64px
  aspect_ratio: "16:9"        # 16:9 宽屏比例
```

| 栅格参数 | 值 | 说明 |
|---------|-----|------|
| 列数 | 1 栏 | TED 风格核心：单栏布局，每页一个核心观点 |
| 列宽 | 1280px | 16:9 标准演示画布宽度（对应 720px 高度） |
| 槽宽 | N/A | 单栏布局无槽宽概念 |
| 页面边距 | 64px | 四周边距 64px，确保内容不贴边 |
| 宽高比 | 16:9 | 标准演示文稿宽屏比例 |

**栅格系统说明**：
- 单栏布局是 TED 风格的核心——"每页一个核心观点"意味着不需要多栏分散注意力
- 1280×720px（16:9）是演示文稿的标准画布尺寸，兼容主流投影设备
- 64px 页面边距营造大量留白，这是 TED 风格"留白驱动"的具象体现
- 拒绝花哨的多栏模板，靠单栏 + 大字号 + 留白出高级感

### 1.10 radius_shadow

```yaml
radius_shadow:
  border_radius: "0px"    # 圆角 0px — 扁平设计
  box_shadow: "none"      # 阴影 none — 扁平设计
```

| 元素类型 | 圆角值 | 阴影值 | 说明 |
|---------|--------|--------|------|
| 卡片/Card | 0px | none | 扁平设计，无圆角无阴影 |
| 图片/Image | 0px | none | 图片直角裁切，全屏铺满 |
| 按钮/Button | 0px | none | 扁平按钮，靠颜色区分而非阴影 |
| 引用块/Quote | 0px | none | 引用块靠字号和留白区分，无圆角无阴影 |
| 背景/Background | 0px | none | 纯色背景，无渐变无阴影 |

**圆角阴影说明**：
- 圆角 0px + 阴影 none 是 TED 风格的扁平设计核心——拒绝一切装饰性视觉效果
- 扁平设计传达"内容为王"的理念——观众的注意力应聚焦在观点上，而非视觉装饰
- 禁止使用圆角、阴影、渐变、毛玻璃等装饰效果，这是 DLP-ted 的硬性规范

### 1.11 motion_curve

```yaml
motion_curve:
  slide_transition: "ease-in-out 400ms"   # 幻灯片切换
  element_appearance: "ease-out 200ms"    # 元素出现
```

| 动效场景 | 缓动曲线 | 时长 | 说明 |
|---------|---------|------|------|
| 幻灯片切换 | ease-in-out | 400ms | 幻灯片之间的过渡，平滑而不突兀 |
| 元素出现 | ease-out | 200ms | 单个元素的出现动效，快速而自然 |
| 元素消失 | ease-in | 200ms | 单个元素的消失动效 |
| 重点强调 | N/A | N/A | TED 风格不使用强调动效，靠字号和留白强调 |

**动效曲线说明**：
- 幻灯片切换使用 ease-in-out 400ms，平滑过渡，不分散观众注意力
- 元素出现使用 ease-out 200ms，快速自然，避免等待感
- 禁止使用弹跳、旋转、缩放、弹性等装饰性动效
- 动效极其克制，服务于内容呈现而非炫技——这是 TED 风格"极简电影感"的动效体现

### 1.12 applicable_scenarios

```yaml
applicable_scenarios:
  - "演示文稿"
  - "TED风格"
  - "极简电影感"
  - "大字号"
  - "留白驱动"
```

| 场景标签 | 匹配优先级 | 典型用例 |
|---------|-----------|---------|
| 演示文稿 | 高 | TED 风格演讲幻灯片、产品发布会演示 |
| TED风格 | 高 | 需要极简电影感的演示场景 |
| 极简电影感 | 高 | 追求沉浸式视觉体验的演示 |
| 大字号 | 中 | 需要远距离可读性的演示场景 |
| 留白驱动 | 中 | 通过大量留白营造高级感的演示 |

---

## 二、slidecraft-skill 融入内容

> **融入来源技能**: slidecraft-skill
> **融入形式**: TED 风格演示特征完整融入本 DLP 的视觉规范

### 2.1 TED 风格演示六大特征

本 DLP 完整融入 slidecraft-skill 定义的 TED 风格演示六大特征：

| 特征编号 | 特征名称 | 融入字段 | 融入说明 |
|---------|---------|---------|---------|
| TED-FEATURE-01 | 极简电影感 | color_palette + radius_shadow + motion_curve | 深色模式背景 + 扁平设计 + 克制动效，营造电影级沉浸感 |
| TED-FEATURE-02 | 大字号排版 | typography_scale | H1 72px 超大字号，靠字号差异建立层级 |
| TED-FEATURE-03 | 大量留白 | spacing_system + grid_system | 96px 最大间距 + 64px 页面边距，留白驱动设计 |
| TED-FEATURE-04 | 每页一个核心观点 | grid_system（单栏） | 单栏布局强制每页聚焦一个观点 |
| TED-FEATURE-05 | 拒绝花哨模板 | radius_shadow（0px/none） | 扁平设计，零圆角零阴影零渐变 |
| TED-FEATURE-06 | 靠排版层级与留白出高级感 | typography_scale + spacing_system | 字号阶梯 + 间距阶梯共同构建高级感 |

### 2.2 slidecraft-skill 方法论融入

```yaml
slidecraft_skill_integration:
  source_skill: "slidecraft-skill"
  integration_points:
    - point: "极简电影感"
      field: "color_palette (深色模式) + motion_curve (克制动效)"
      description: "深色背景 #1A1A1A + 白色文字 + 极简淡入淡出动效，营造电影级视觉沉浸感"
    - point: "大字号排版"
      field: "typography_scale (H1 72px)"
      description: "演示级超大字号阶梯，72px 大标题确保远距离可读性，靠字号差异建立信息层级"
    - point: "大量留白"
      field: "spacing_system (96px 最大间距) + grid_system (64px 边距)"
      description: "留白驱动设计，核心观点周围有充足呼吸空间，拒绝信息堆砌"
    - point: "每页一个核心观点"
      field: "grid_system (单栏布局)"
      description: "单栏布局强制每页聚焦一个观点，拒绝多栏分散注意力"
    - point: "拒绝花哨模板"
      field: "radius_shadow (0px/none)"
      description: "扁平设计，零圆角零阴影零渐变，拒绝一切装饰性视觉效果"
    - point: "靠排版层级与留白出高级感"
      field: "typography_scale + spacing_system"
      description: "不靠颜色和装饰，靠字号阶梯（72→48→36→28→24）和间距阶梯（8→96）构建高级感"
```

---

## 三、DLP 检索对接规范

### 3.1 检索命中条件

当以下语义信号出现时，DLP 检索器应优先匹配 `DLP-ted`：

1. **内容主题信号**: 演讲、演示、分享、keynote、TED
2. **任务类型信号**: course_material（课件材料）、演示文稿类输出
3. **受众信号**: general（大众观众）、professional（专业观众）
4. **排版需求信号**: 大字号、留白驱动、极简电影感、单栏演示

### 3.2 design_tokens 输出

```yaml
design_tokens:
  color_scheme:
    primary: "#E62B1E"
    secondary: "#1A1A1A"
    accent: "#FFFFFF"
    neutral: "#767676"
    background: "#1A1A1A"
    text: "#FFFFFF"
    background_light: "#FFFFFF"
    text_light: "#1A1A1A"
  font_scheme:
    heading_font: '"TED Serif", "Georgia", "Times New Roman", serif'
    body_font: '"TED Serif", "Georgia", "Times New Roman", serif'
    chinese_font: '"宋体", "SimSun", "Noto Serif SC", serif'
    monospace_font: '"Courier New", "Courier", monospace'
  typography:
    h1_size: "72px"
    h2_size: "48px"
    h3_size: "36px"
    h4_size: "28px"
    body_size: "24px"
    caption_size: "18px"
    footnote_size: "14px"
    heading_weight: 700
    body_weight: 400
    emphasis_weight: "italic 400"
  spacing:
    base: 8px
    scale: [8, 16, 24, 32, 48, 64, 96]
  grid:
    columns: 1
    column_width: "1280px"
    gutter: "N/A"
    margin: "64px"
    aspect_ratio: "16:9"
  visual:
    border_radius: "0px"
    box_shadow: "none"
  motion:
    slide_transition: "ease-in-out 400ms"
    element_appearance: "ease-out 200ms"
```

### 3.3 与 visual_dna 的对接映射

| DLP 字段 | visual_dna 字段 | 映射规则 |
|---------|----------------|---------|
| `color_palette.primary` | `--color-primary` | TED 红直接映射为主色 |
| `color_palette.background` | `--color-bg` | 深色模式背景直接映射 |
| `color_palette.text` | `--color-text` | 白色文字直接映射 |
| `typography_scale.h1` | `font_scheme.h1_size` | 72px 大标题字号直接映射 |
| `font_stack.western` | `font_scheme.body_font` | TED Serif 字体栈直接注入 |
| `grid_system.columns` | `grid_system.columns` | 单栏栅格直接映射 |
| `motion_curve.slide_transition` | `motion_profile.transition` | ease-in-out 400ms 直接映射 |

---

## 四、与 TA/LA 原子库的对接

### 4.1 TA 排版原子对接

| TA 原子 ID | 原子名称 | 对接用途 |
|-----------|---------|---------|
| TA-SCALE-001 | H1 字号阶梯 | 72px 演示大标题字号 |
| TA-SCALE-008 | display 字号 | 72px 超大字号演示场景 |
| TA-WEIGHT-001 | 标题 bold 字重 | 700 字重用于所有标题 |
| TA-WEIGHT-003 | 强调 italic 字重 | 400 italic 用于引言/书名 |
| TA-LINE-001 | 正文行高 | 1.4 行高用于 24px 正文 |
| TA-PARA-006 | 单栏排版 | 单栏演示布局的段落排版 |

### 4.2 LA 布局原子对接

| LA 原子 ID | 原子名称 | 对接用途 |
|-----------|---------|---------|
| LA-GRID-001 | 单栏栅格 | 演示文稿单栏布局 |
| LA-PAGE-004 | 演示页布局 | TED 风格演示页整体布局 |
| LA-RESP-004 | 超宽屏断点 | 16:9 宽屏演示的响应式断点 |

---

## 五、ASR 硬门合规说明

本 DLP 的视觉规范天然符合以下 ASR 硬门禁令：

| ASR 禁令编号 | 禁令内容 | 本 DLP 合规性 |
|-------------|---------|-------------|
| ASR-FONT-001 | 禁 Inter 作为 Premium 产出字体 | ✅ 使用 TED Serif 衬线字体 |
| ASR-COLOR-002 | 禁纯黑（#000000） | ✅ 使用 #1A1A1A 深色背景 |
| ASR-LAYOUT-002 | 禁 h-screen 全屏占位 | ✅ 使用 16:9 标准画布尺寸 |
| ASR-LAYOUT-004 | 禁默认 Tailwind 间距阶梯 | ✅ 使用 8/16/24/32/48/64/96 自定义阶梯 |
| ASR-MOTION-002 | 禁 linear 缓动 | ✅ 使用 ease-in-out 和 ease-out |
| ASR-DECOR-003 | 禁阴影堆叠超过 3 层 | ✅ 阴影 none，零层堆叠 |
| ASR-DECOR-004 | 禁毛玻璃效果用于正文区域 | ✅ 扁平设计，无毛玻璃 |

---

> **DLP 元数据**
> - 创建时间: 2026-06-19
> - 族: publication-typesetting
> - 锚定: TED Talks 2024 年演示风格
> - 融入技能: slidecraft-skill ✅
> - 字段完整性: 12/12 ✅
> - 配色锚定: 真实世界出版物实测配色 ✅
> - 字体栈中文 fallback: 已包含 ✅
> - 融入内容标注: slidecraft-skill 六大特征已明确标注 ✅
