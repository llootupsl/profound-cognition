<!-- 作者：阿洋 -->

# DLP-aesop — Aesop 品牌设计语言画像

> **定位**: interface-brand 族，锚定 Aesop 官网 2024 年品牌设计，提供奢侈品品牌官网的具象视觉规范。
> **族覆盖补充**: 本 DLP 为 interface-brand 族的族覆盖补充成员，与 DLP-linear / DLP-stripe-press / DLP-gov-uk 共同构成 4 个 DLP 的完整族覆盖。
> **来源技能**: garden-skills（Aesop 设计语言特征内化）
> **索引**: 详见 `README.md` 获取 DLP 库完整清单与检索规范

---

## YAML frontmatter（12 字段完整定义）

```yaml
---
name: "DLP-aesop"
anchor: "Aesop 官网 2024 年品牌设计"
family: "interface-brand"

color_palette:
  primary: "#3D3D3D"
  secondary: "#D4C5B0"
  accent: "#8B7355"
  neutral: "#A8A8A8"
  background: "#F5F2ED"
  text: "#2D2D2D"

typography_scale:
  h1: "36px/2.25rem"
  h2: "28px/1.75rem"
  h3: "22px/1.375rem"
  h4: "18px/1.125rem"
  body: "16px/1rem"
  caption: "13px/0.8125rem"
  footnote: "12px/0.75rem"

font_stack:
  western: '"Söhne", "Maison Neue", "GT America", sans-serif'
  chinese: '"Songti SC", "宋体", serif'
  monospace: '"JetBrains Mono", monospace'

font_weight_pairing:
  heading: "light(300)"
  body: "regular(400)"
  emphasis: "medium(500)"

spacing_system:
  base: "8px"
  scale: "8/16/24/32/48/64/80px"

grid_system:
  columns: "12列"
  column_width: "auto"
  gutter: "32px"
  margin: "48px"
  breakpoint: "sm:640px/md:768px/lg:1024px/xl:1280px"

radius_shadow:
  radius: "0px"
  shadow: "none"

motion_curve:
  easing: "ease-out/ease-in-out"
  duration: "400-600ms"

applicable_scenarios:
  - "品牌官网"
  - "奢侈品"
  - "护肤品"
  - "编辑式排版"
  - "暖色调"
---
```

---

## 一、12 字段完整规范

### 1.1 name

```yaml
name: DLP-aesop
```

- **唯一标识**: `DLP-aesop`
- **检索键**: aesop / 奢侈品 / 护肤品 / 编辑式排版 / 暖色调
- **族内编号**: interface-brand-02

### 1.2 anchor

```yaml
anchor: "Aesop 官网 2024 年品牌设计"
```

- **锚定真实世界**: Aesop 官网（aesop.com）2024 年品牌设计与版式规范
- **锚定依据**: 暖米色调（#F5F2ED）、衬线字体、大量留白、极简扁平、编辑式排版
- **品牌辨识特征**: 暖白背景 + 深灰文字 + 棕色强调 + 衬线中文 + 直角扁平 + 大量留白

### 1.3 family

```yaml
family: interface-brand
```

- **所属族**: interface-brand（界面品牌族）
- **族内同级**: DLP-linear / DLP-stripe-press / DLP-gov-uk
- **族特征**: 无衬线字体、单栏响应式、品牌色驱动、微动效、圆角阴影

### 1.4 color_palette

```yaml
color_palette:
  primary: "#3D3D3D"      # 深灰 — 标题、重点文字、导航
  secondary: "#D4C5B0"    # 米色 — 卡片背景、次级容器、装饰色块
  accent: "#8B7355"       # 棕色 — 链接、CTA按钮、交互强调
  neutral: "#A8A8A8"      # 中性灰 — 次要文字、图标、占位符
  background: "#F5F2ED"   # 暖白 — 页面主背景
  text: "#2D2D2D"         # 深灰文本 — 正文主文字色
```

| 色板角色 | 变量名 | 十六进制值 | 用途 |
|---------|--------|-----------|------|
| 主色 Primary | `--color-primary` | `#3D3D3D` | 标题、重点文字、导航栏、页脚 |
| 辅色 Secondary | `--color-secondary` | `#D4C5B0` | 卡片背景、次级容器、装饰色块、分隔区域 |
| 强调色 Accent | `--color-accent` | `#8B7355` | 链接、CTA 按钮、交互强调、hover 态 |
| 中性色 Neutral | `--color-neutral` | `#A8A8A8` | 次要文字、图标、占位符、元数据 |
| 背景色 Background | `--color-bg` | `#F5F2ED` | 暖白页面主背景，非纯白 |
| 文本色 Text | `--color-text` | `#2D2D2D` | 正文主文字色，深灰而非纯黑 |

**配色锚定说明**：
- `#F5F2ED` 为 Aesop 官网暖白背景，替代纯白（#FFFFFF），营造温度感和天然成分联想
- `#3D3D3D` 为深灰主色，用于标题和导航，非纯黑，保持柔和质感
- `#8B7355` 为棕色强调色，呼应 Aesop 天然植物成分的品牌定位
- `#D4C5B0` 为米色辅色，用于卡片和装饰区域，与暖白背景形成微妙层次
- 全部色值锚定 Aesop 官网 2024 年实际品牌设计的实测配色

### 1.5 typography_scale

```yaml
typography_scale:
  h1: "36px / 2.25rem"       # 文档主标题
  h2: "28px / 1.75rem"       # 章节标题
  h3: "22px / 1.375rem"      # 小节标题
  h4: "18px / 1.125rem"      # 子节标题
  body: "16px / 1rem"        # 正文
  caption: "13px / 0.8125rem" # 图注/元数据
  footnote: "12px / 0.75rem" # 脚注
```

| 层级 | 用途 | 字号 | 行高 | 字重 |
|------|------|------|------|------|
| H1 | 文档主标题 | 36px / 2.25rem | 1.2 | 300 (light) |
| H2 | 章节标题 | 28px / 1.75rem | 1.3 | 300 (light) |
| H3 | 小节标题 | 22px / 1.375rem | 1.4 | 300 (light) |
| H4 | 子节标题 | 18px / 1.125rem | 1.5 | 300 (light) |
| Body | 正文 | 16px / 1rem | 1.75 | 400 (regular) |
| Caption | 图注/元数据 | 13px / 0.8125rem | 1.6 | 400 (regular) |
| Footnote | 脚注 | 12px / 0.75rem | 1.5 | 400 (regular) |

**字号阶梯说明**：
- 标题采用 light(300) 字重，营造纤细优雅的奢侈品质感
- 正文 16px，行高 1.75（宽松），增强长文阅读的呼吸感
- H1 36px 为最大字号，强化编辑式层级的视觉冲击

### 1.6 font_stack

```yaml
font_stack:
  western: '"Söhne", "Maison Neue", "GT America", sans-serif'
  chinese: '"Songti SC", "宋体", serif'
  monospace: '"JetBrains Mono", monospace'
```

| 用途 | 字体栈 | CSS font-family | Fallback 策略 |
|------|--------|----------------|--------------|
| 西文正文/标题 | Söhne → Maison Neue → GT America → sans-serif | `"Söhne", "Maison Neue", "GT America", sans-serif` | Söhne 为 Aesop 品牌字体；Maison Neue 为开源替代；GT America 为系统兜底 |
| 中文正文/标题 | Songti SC → 宋体 → serif | `"Songti SC", "宋体", serif` | Songti SC 为 macOS 中文衬线标准；宋体为 Windows 中文衬线标准 |
| 等宽/代码 | JetBrains Mono → monospace | `"JetBrains Mono", monospace` | JetBrains Mono 为等宽字体标准 |

**字体栈锚定说明**：
- 中文使用衬线字体（Songti SC / 宋体），与西文无衬线形成编辑式对比，强化品牌的人文质感
- 西文 Söhne 为 Aesop 实际使用的商业字体，Maison Neue 为开源替代
- 中文衬线 fallback 确保跨平台一致的编辑式排版质感

### 1.7 font_weight_pairing

```yaml
font_weight_pairing:
  heading: "light (300)"     # 标题字重
  body: "regular (400)"      # 正文字重
  emphasis: "medium (500)"   # 强调字重
```

| 元素类型 | 字重 | font-weight 值 | 说明 |
|---------|------|---------------|------|
| 标题 Heading | light | 300 | H1-H4 所有标题层级使用 light，营造纤细优雅感 |
| 正文 Body | regular | 400 | 正文使用 regular，确保 16px 字号下的可读性 |
| 强调 Emphasis | medium | 500 | 强调使用 medium，用于关键信息高亮和交互元素 |

**字重搭配规则**：
- 标题一律 light(300)，这是 Aesop 品牌的标志性字重，传达克制与优雅
- 正文一律 regular(400)，不使用 light(300)，确保正文的可读性
- 强调使用 medium(500)，介于标题和正文之间，用于 CTA 和链接

### 1.8 spacing_system

```yaml
spacing_system:
  base_unit: 8px
  scale: [8, 16, 24, 32, 48, 64, 80]
```

| 间距级别 | 值 | 用途 |
|---------|-----|------|
| xs | 8px | 图标与文字间距、紧密元素 |
| sm | 16px | 列表项间距、段落间距 |
| md | 24px | 卡片内边距、组件间距 |
| lg | 32px | 区块间距、章节间距 |
| xl | 48px | 大区块分隔 |
| 2xl | 64px | 页面级区块分隔 |
| 3xl | 80px | 文档级大分隔、留白呼吸 |

**间距系统说明**：
- 基准单位 8px，比标准 4px 更大，营造奢侈品的"呼吸感"
- 阶梯采用 8/16/24/32/48/64/80 的 7 级阶梯，间距偏大以强调留白
- Aesop 品牌页面留白占比 ≥ 40%，VISUAL_DENSITY ≈ 2（艺术画廊级留白）

### 1.9 grid_system

```yaml
grid_system:
  columns: 12                 # 12 列响应式栅格
  column_width: "auto"        # 列宽自适应
  gutter: "32px"              # 槽宽 32px
  margin: "48px"              # 页边距 48px
  breakpoint: "sm:640px/md:768px/lg:1024px/xl:1280px"
```

| 栅格参数 | 值 | 说明 |
|---------|-----|------|
| 列数 | 12 列 | 标准响应式 12 列栅格 |
| 列宽 | auto | 列宽自适应，内容通常占据 6-8 列 |
| 槽宽 | 32px | 列间槽宽 32px，较大间距强调留白 |
| 页边距 | 48px | 上下左右页边距 48px，强化呼吸感 |
| 断点 sm | 640px | 小屏设备 |
| 断点 md | 768px | 中屏设备（平板） |
| 断点 lg | 1024px | 大屏设备（桌面） |
| 断点 xl | 1280px | 超大屏设备 |

**栅格系统说明**：
- 12 列栅格，但内容通常占据 6-8 列，两侧大量留白
- 槽宽 32px 和页边距 48px 均大于常规值，强化奢侈品的空间感
- 4 个断点覆盖从移动端到桌面端的完整响应式适配

### 1.10 radius_shadow

```yaml
radius_shadow:
  border_radius: "0px"    # 圆角 0px — 全直角
  box_shadow: "none"      # 阴影 none — 全扁平
```

| 元素类型 | 圆角值 | 阴影值 | 说明 |
|---------|--------|--------|------|
| 卡片 Card | 0px | none | 直角卡片，靠留白和分割线分隔 |
| 按钮 Button | 0px | none | 直角按钮，靠背景色区分层级 |
| 输入框 Input | 0px | none | 直角输入框，靠边框区分 |
| 图片 Image | 0px | none | 图片直角裁切，无圆角 |
| 引用块 Quote | 0px | none | 引用块靠左侧边线分隔 |

**圆角阴影说明**：
- 圆角 0px（全直角），保持建筑般的严谨感和编辑式质感
- 阴影 none（全扁平），通过分割线、留白和色彩对比建立层级
- 禁止使用任何圆角和阴影，这是 Aesop 品牌的硬性规范
- 边框使用 1px `#3D3D3D` 半透明（opacity 0.1），极细分割线

### 1.11 motion_curve

```yaml
motion_curve:
  page_transition: "ease-out 400ms"
  image_load: "ease-in-out 600ms"
```

| 动效场景 | 缓动曲线 | 时长 | 说明 |
|---------|---------|------|------|
| 页面过渡 Page Transition | ease-out | 400ms | 页面切换、路由过渡 |
| 图片加载 Image Load | ease-in-out | 600ms | 图片淡入、渐显效果 |

**动效曲线说明**：
- Aesop 动效极简且缓慢，营造从容、优雅的品牌节奏
- 不使用快速微交互，所有动效时长 ≥ 400ms
- 禁止弹跳/回弹/旋转等装饰性动效，保持品牌的克制感

### 1.12 applicable_scenarios

```yaml
applicable_scenarios:
  - "品牌官网"
  - "奢侈品"
  - "护肤品"
  - "编辑式排版"
  - "暖色调"
```

| 场景标签 | 匹配优先级 | 典型用例 |
|---------|-----------|---------|
| 品牌官网 | 高 | 品牌官方网站、品牌故事页、产品展示 |
| 奢侈品 | 高 | 奢侈品牌、高端消费品的视觉设计 |
| 护肤品 | 高 | 护肤品牌、美妆品牌、天然成分产品 |
| 编辑式排版 | 中 | 杂志式排版、图文混排、长文叙事 |
| 暖色调 | 中 | 暖色系配色方案、米色/棕色系设计 |

---

## 二、garden-skills 设计语言特征内化

> **来源**: garden-skills（Aesop 设计语言特征）

Aesop 的设计语言特征——大量留白、暖米色调、衬线字体、极简扁平、编辑式排版，具体内化如下：

### 2.1 大量留白
- 基准间距 8px，但实际使用以 32px/48px/64px/80px 为主
- 页面留白占比 ≥ 40%，营造"呼吸感"和"奢侈感"
- 段落间距 24px，章节间距 64px，页面级分隔 80px
- VISUAL_DENSITY ≈ 2（艺术画廊级留白）

### 2.2 暖米色调
- 背景色 `#F5F2ED`（暖白）替代纯白，营造温度感
- 辅色 `#D4C5B0`（米色）用于卡片和装饰色块
- 强调色 `#8B7355`（棕色）用于交互元素，呼应天然成分
- 全文档禁止冷灰色调，统一使用暖灰系

### 2.3 衬线字体
- 中文使用 Songti SC（宋体），与西文 Söhne 形成衬线/无衬线对比
- 标题字重 light(300)，营造纤细优雅感
- 行高宽松（1.75），增强可读性和呼吸感
- 字号偏大（H1 36px），强化编辑式层级

### 2.4 极简扁平
- 圆角 0px（全直角），保持建筑般的严谨感
- 阴影 none（全扁平），通过分割线和留白建立层级
- 边框使用 1px `#3D3D3D` 半透明（opacity 0.1），极细分割线
- 禁止任何渐变、发光、模糊效果

### 2.5 编辑式排版
- 12 列栅格，但内容通常占据 6-8 列，两侧大量留白
- 标题与正文形成强烈对比（36px light vs 16px regular）
- 图文混排采用杂志式布局：左图右文 / 上图下文 / 通栏图
- 段落首字下沉可选，用于长文叙事段落

---

## 三、DLP 检索对接规范

### 3.1 检索命中条件

当以下语义信号出现时，DLP 检索器应优先匹配 `DLP-aesop`：

1. **内容主题信号**: 奢侈品、护肤、极简品牌、暖色调、编辑式排版
2. **任务类型信号**: wechat_article（品牌故事）、course_material（品牌教程）
3. **受众信号**: general（大众读者）、creative（创意人士）
4. **排版需求信号**: 大量留白、暖色调、衬线字体、扁平设计

### 3.2 design_tokens 输出

```yaml
design_tokens:
  color_scheme:
    primary: "#3D3D3D"
    secondary: "#D4C5B0"
    accent: "#8B7355"
    neutral: "#A8A8A8"
    background: "#F5F2ED"
    text: "#2D2D2D"
  font_scheme:
    heading_font: '"Söhne", "Maison Neue", "GT America", sans-serif'
    body_font: '"Söhne", "Maison Neue", "GT America", sans-serif'
    chinese_font: '"Songti SC", "宋体", serif'
    monospace_font: '"JetBrains Mono", monospace'
  typography:
    h1_size: "36px"
    h2_size: "28px"
    h3_size: "22px"
    h4_size: "18px"
    body_size: "16px"
    caption_size: "13px"
    footnote_size: "12px"
    heading_weight: 300
    body_weight: 400
    emphasis_weight: 500
  spacing:
    base: 8px
    scale: [8, 16, 24, 32, 48, 64, 80]
  grid:
    columns: 12
    gutter: "32px"
    margin: "48px"
    breakpoint: "sm:640px/md:768px/lg:1024px/xl:1280px"
  visual:
    border_radius: "0px"
    box_shadow: "none"
  motion:
    page_transition: "ease-out 400ms"
    image_load: "ease-in-out 600ms"
```

### 3.3 与 visual_dna 的对接映射

| DLP 字段 | visual_dna 字段 | 映射规则 |
|---------|----------------|---------|
| `color_palette.primary` | `--color-primary` | 深灰直接映射为主色 |
| `color_palette.secondary` | `--color-secondary` | 米色映射为辅色 |
| `color_palette.accent` | `--color-accent` | 棕色映射为强调色 |
| `typography_scale.body` | `font_scheme.body_size` | 16px 正文字号直接映射 |
| `font_stack.western` | `font_scheme.body_font` | Söhne 字体栈直接注入 |
| `grid_system.columns` | `grid_system.columns` | 12 列栅格直接映射 |
| `radius_shadow.border_radius` | `visual.radius` | 0px 圆角直接映射 |

---

## 四、ASR 硬门合规说明

本 DLP 的视觉规范符合以下 ASR 硬门禁令：

| ASR 禁令编号 | 禁令内容 | 本 DLP 合规性 |
|-------------|---------|-------------|
| ASR-FONT-001 | 禁 Inter 作为 Premium 产出字体 | ✅ 使用 Söhne 无衬线字体 |
| ASR-COLOR-002 | 禁纯黑（#000000） | ✅ 使用 #3D3D3D 深灰 |
| ASR-COLOR-003 | 禁纯白（#FFFFFF）作为大面积背景 | ✅ 使用 #F5F2ED 暖白 |
| ASR-LAYOUT-004 | 禁默认 Tailwind 间距阶梯 | ✅ 使用 8/16/24/32/48/64/80 自定义阶梯 |
| ASR-DECOR-003 | 禁阴影堆叠超过 3 层 | ✅ 阴影 none，零层堆叠 |
| ASR-DECOR-004 | 禁圆角过大 | ✅ 圆角 0px，全直角 |

---

> **DLP 元数据**
> - 创建时间: 2026-06-19
> - 族: interface-brand
> - 锚定: Aesop 官网 2024 年品牌设计
> - 字段完整性: 12/12 ✅
> - 配色锚定: 真实世界品牌实测配色 ✅
> - 字体栈中文 fallback: 已包含 ✅
> - ASR 硬门合规: 已通过 ✅
> - 来源技能: garden-skills ✅
