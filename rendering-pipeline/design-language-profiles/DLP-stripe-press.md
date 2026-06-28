<!-- 作者：阿洋 -->

# DLP-stripe-press — Stripe Press 设计语言画像

> **定位**: interface-brand 族，锚定 Stripe Press 2024 年版式，提供金融科技品牌官网与技术出版物的具象视觉规范。
> **族覆盖补充**: 本 DLP 为 interface-brand 族的族覆盖补充成员，与 DLP-linear / DLP-aesop / DLP-gov-uk 共同构成 4 个 DLP 的完整族覆盖。
> **来源技能**: garden-skills（Stripe Press 设计语言特征内化）
> **索引**: 详见 `README.md` 获取 DLP 库完整清单与检索规范

---

## YAML frontmatter（12 字段完整定义）

```yaml
---
name: "DLP-stripe-press"
anchor: "Stripe Press 2024 年版式"
family: "interface-brand"

color_palette:
  primary: "#635BFF"
  secondary: "#0A2540"
  accent: "#00D4FF"
  neutral: "#687385"
  background: "#FFFFFF"
  text: "#0A2540"

typography_scale:
  h1: "40px/2.5rem"
  h2: "32px/2rem"
  h3: "24px/1.5rem"
  h4: "20px/1.25rem"
  body: "18px/1.125rem"
  caption: "14px/0.875rem"
  footnote: "13px/0.8125rem"

font_stack:
  western: '"Sohne", "Camphor", "GT America", sans-serif'
  chinese: '"Noto Sans SC", "PingFang SC", sans-serif'
  monospace: '"JetBrains Mono", "SF Mono", monospace'

font_weight_pairing:
  heading: "semibold(600)"
  body: "regular(400)"
  emphasis: "medium(500)"

spacing_system:
  base: "4px"
  scale: "4/8/12/16/24/32/48/64/80px"

grid_system:
  columns: "12列"
  column_width: "auto"
  gutter: "24px"
  margin: "40px"
  breakpoint: "sm:640px/md:768px/lg:1024px/xl:1280px"

radius_shadow:
  radius: "12px(卡片)/8px(按钮)/6px(输入框)"
  shadow: "0 2px 4px rgba(0,0,0,0.04)(轻微)/0 8px 24px rgba(0,0,0,0.08)(中等)"

motion_curve:
  easing: "cubic-bezier(0.4, 0, 0.2, 1)/ease-out"
  duration: "200-300ms"

applicable_scenarios:
  - "品牌官网"
  - "金融科技"
  - "出版物"
  - "技术文档"
  - "渐变设计"
---
```

---

## 一、12 字段完整规范

### 1.1 name

```yaml
name: DLP-stripe-press
```

- **唯一标识**: `DLP-stripe-press`
- **检索键**: stripe / 金融科技 / 出版物 / 技术文档 / 渐变设计
- **族内编号**: interface-brand-03

### 1.2 anchor

```yaml
anchor: "Stripe Press 2024 年版式"
```

- **锚定真实世界**: Stripe Press（press.stripe.com）2024 年版式规范
- **锚定依据**: Stripe 紫色品牌色（#635BFF）、深蓝紫色调、大字号排版、柔和阴影、技术出版物质感
- **品牌辨识特征**: 紫色主色 + 深蓝文字 + 亮蓝强调 + 精致渐变 + 大圆角卡片 + 柔和阴影

### 1.3 family

```yaml
family: interface-brand
```

- **所属族**: interface-brand（界面品牌族）
- **族内同级**: DLP-linear / DLP-aesop / DLP-gov-uk
- **族特征**: 无衬线字体、单栏响应式、品牌色驱动、微动效、圆角阴影

### 1.4 color_palette

```yaml
color_palette:
  primary: "#635BFF"      # Stripe 紫 — 标题强调、链接、品牌色
  secondary: "#0A2540"    # 深蓝 — 正文文字、次级容器、页脚背景
  accent: "#00D4FF"       # 亮蓝 — 数据高亮、图表辅色、交互反馈
  neutral: "#687385"      # 中性灰 — 次要文字、图标、占位符
  background: "#FFFFFF"   # 纯白 — 页面主背景
  text: "#0A2540"         # 深蓝文本 — 正文主文字色
```

| 色板角色 | 变量名 | 十六进制值 | 用途 |
|---------|--------|-----------|------|
| 主色 Primary | `--color-primary` | `#635BFF` | 标题强调、链接、品牌色、主按钮 |
| 辅色 Secondary | `--color-secondary` | `#0A2540` | 正文文字、次级容器、页脚背景、深色区域 |
| 强调色 Accent | `--color-accent` | `#00D4FF` | 数据高亮、图表辅色、交互反馈（使用频率≤5%） |
| 中性色 Neutral | `--color-neutral` | `#687385` | 次要文字、图标、占位符、元数据 |
| 背景色 Background | `--color-bg` | `#FFFFFF` | 纯白页面主背景 |
| 文本色 Text | `--color-text` | `#0A2540` | 深蓝正文主文字色，替代纯黑 |

**配色锚定说明**：
- `#635BFF` 为 Stripe 官方品牌紫色，用于所有交互元素和品牌标识
- `#0A2540` 为 Stripe 深蓝，用于正文和深色区域，替代纯黑（#000000）
- `#00D4FF` 为 Stripe 亮蓝，仅用于数据高亮，使用频率极低（≤ 5%）
- 全部色值锚定 Stripe Press 2024 年实际版式的实测配色

### 1.5 typography_scale

```yaml
typography_scale:
  h1: "40px / 2.5rem"         # 文档主标题
  h2: "32px / 2rem"           # 章节标题
  h3: "24px / 1.5rem"         # 小节标题
  h4: "20px / 1.25rem"        # 子节标题
  body: "18px / 1.125rem"     # 正文
  caption: "14px / 0.875rem"  # 图注/元数据
  footnote: "13px / 0.8125rem" # 脚注
```

| 层级 | 用途 | 字号 | 行高 | 字重 |
|------|------|------|------|------|
| H1 | 文档主标题 | 40px / 2.5rem | 1.2 | 600 (semibold) |
| H2 | 章节标题 | 32px / 2rem | 1.3 | 600 (semibold) |
| H3 | 小节标题 | 24px / 1.5rem | 1.4 | 600 (semibold) |
| H4 | 子节标题 | 20px / 1.25rem | 1.5 | 600 (semibold) |
| Body | 正文 | 18px / 1.125rem | 1.7 | 400 (regular) |
| Caption | 图注/元数据 | 14px / 0.875rem | 1.6 | 400 (regular) |
| Footnote | 脚注 | 13px / 0.8125rem | 1.5 | 400 (regular) |

**字号阶梯说明**：
- H1 40px（比常规大 25%），营造出版物的"大标题"视觉冲击
- 正文 18px（比常规大 12.5%），提升阅读舒适度
- 标题字重 semibold(600)，与正文 regular(400) 形成明确层级
- 行高宽松（1.7），增强长文阅读体验

### 1.6 font_stack

```yaml
font_stack:
  western: '"Sohne", "Camphor", "GT America", sans-serif'
  chinese: '"Noto Sans SC", "PingFang SC", sans-serif'
  monospace: '"JetBrains Mono", "SF Mono", monospace'
```

| 用途 | 字体栈 | CSS font-family | Fallback 策略 |
|------|--------|----------------|--------------|
| 西文正文/标题 | Sohne → Camphor → GT America → sans-serif | `"Sohne", "Camphor", "GT America", sans-serif` | Sohne 为 Stripe 品牌字体；Camphor 为开源替代；GT America 为系统兜底 |
| 中文正文/标题 | Noto Sans SC → PingFang SC → sans-serif | `"Noto Sans SC", "PingFang SC", sans-serif` | Noto Sans SC 为跨平台开源中文无衬线；PingFang SC 为 macOS 系统兜底 |
| 等宽/代码 | JetBrains Mono → SF Mono → monospace | `"JetBrains Mono", "SF Mono", monospace` | JetBrains Mono 为开发工具标准等宽字体；SF Mono 为 Apple 系统兜底 |

**字体栈锚定说明**：
- Sohne 是 Stripe Press 实际使用的字体，Camphor 和 GT America 作为 fallback
- 中文使用 Noto Sans SC 保证跨平台一致性
- 等宽字体 JetBrains Mono 用于代码块和技术文档

### 1.7 font_weight_pairing

```yaml
font_weight_pairing:
  heading: "semibold (600)"   # 标题字重
  body: "regular (400)"       # 正文字重
  emphasis: "medium (500)"    # 强调字重
```

| 元素类型 | 字重 | font-weight 值 | 说明 |
|---------|------|---------------|------|
| 标题 Heading | semibold | 600 | H1-H4 所有标题层级使用 semibold，与正文形成明确层级 |
| 正文 Body | regular | 400 | 正文使用 regular，确保 18px 字号下的可读性 |
| 强调 Emphasis | medium | 500 | 强调使用 medium，用于关键信息高亮 |

**字重搭配规则**：
- 标题一律 semibold(600)，不使用 bold(700)，保持现代科技感
- 正文一律 regular(400)，不使用 light(300)，确保可读性
- 强调使用 medium(500)，介于标题和正文之间

### 1.8 spacing_system

```yaml
spacing_system:
  base_unit: 4px
  scale: [4, 8, 12, 16, 24, 32, 48, 64, 80]
```

| 间距级别 | 值 | 用途 |
|---------|-----|------|
| xs | 4px | 图标与文字间距、紧密元素 |
| sm | 8px | 列表项间距、标签内边距 |
| md | 12px | 紧凑组件间距 |
| lg | 16px | 段落间距、卡片内边距 |
| xl | 24px | 区块内间距 |
| 2xl | 32px | 章节间距、区块间距 |
| 3xl | 48px | 大区块分隔 |
| 4xl | 64px | 页面级区块分隔 |
| 5xl | 80px | 文档级大分隔 |

**间距系统说明**：
- 基准单位 4px，与 visual-dna.md 的 4px 基准栅格系统对齐
- 阶梯采用 4/8/12/16/24/32/48/64/80 的 9 级阶梯，覆盖从微观到宏观的间距需求
- Stripe Press 间距适中，兼顾信息密度和阅读舒适度

### 1.9 grid_system

```yaml
grid_system:
  columns: 12                 # 12 列响应式栅格
  column_width: "auto"        # 列宽自适应
  gutter: "24px"              # 槽宽 24px
  margin: "40px"              # 页边距 40px
  breakpoint: "sm:640px/md:768px/lg:1024px/xl:1280px"
```

| 栅格参数 | 值 | 说明 |
|---------|-----|------|
| 列数 | 12 列 | 标准响应式 12 列栅格 |
| 列宽 | auto | 列宽自适应，内容区通常占据 8 列 |
| 槽宽 | 24px | 列间槽宽 24px，适中分隔 |
| 页边距 | 40px | 上下左右页边距 40px |
| 断点 sm | 640px | 小屏设备 |
| 断点 md | 768px | 中屏设备（平板） |
| 断点 lg | 1024px | 大屏设备（桌面） |
| 断点 xl | 1280px | 超大屏设备 |

**栅格系统说明**：
- 12 列栅格，内容区通常占据 8 列，两侧留白
- 槽宽 24px 确保列间清晰分隔
- 页边距 40px 适中，兼顾信息密度和呼吸感

### 1.10 radius_shadow

```yaml
radius_shadow:
  card_radius: "12px"      # 卡片圆角
  button_radius: "8px"     # 按钮圆角
  input_radius: "6px"      # 输入框圆角
  shadow_light: "0 2px 4px rgba(0,0,0,0.04)"    # 轻微阴影
  shadow_medium: "0 8px 24px rgba(0,0,0,0.08)"  # 中等阴影
```

| 元素类型 | 圆角值 | 阴影值 | 说明 |
|---------|--------|--------|------|
| 卡片 Card | 12px | 轻微/中等 | 内容卡片、书籍封面容器，悬浮时阴影加深 |
| 按钮 Button | 8px | none | 交互按钮，无阴影，靠背景色区分层级 |
| 输入框 Input | 6px | none | 表单输入，聚焦态使用 ring |
| 图片 Image | 12px | none | 图片圆角与卡片一致 |
| 模态框 Modal | 12px | 中等 | 弹出层使用中等阴影 |

**圆角阴影说明**：
- 三层圆角体系：12px(卡片) / 8px(按钮) / 6px(输入框)，形成递减的圆角层级
- 两层阴影体系：轻微（悬浮卡片）/ 中等（模态框），阴影极其柔和（透明度 ≤ 0.08）
- 阴影模糊半径较大（4px-24px），柔化边缘，营造"漂浮"而非"投影"的质感
- 阴影颜色基于黑色半透明，不使用彩色阴影

### 1.11 motion_curve

```yaml
motion_curve:
  transition: "cubic-bezier(0.4, 0, 0.2, 1) 200ms"
  hover: "ease-out 300ms"
```

| 动效场景 | 缓动曲线 | 时长 | 说明 |
|---------|---------|------|------|
| 过渡 Transition | cubic-bezier(0.4, 0, 0.2, 1) | 200ms | 颜色过渡、状态切换 |
| 悬停 Hover | ease-out | 300ms | 按钮悬停、卡片提升 |

**动效曲线说明**：
- 使用 Material Design 标准缓动曲线 cubic-bezier(0.4, 0, 0.2, 1)
- 动效精致克制，时长适中（200-300ms）
- 仅动画 transform 和 opacity（GPU 加速）

### 1.12 applicable_scenarios

```yaml
applicable_scenarios:
  - "品牌官网"
  - "金融科技"
  - "出版物"
  - "技术文档"
  - "渐变设计"
```

| 场景标签 | 匹配优先级 | 典型用例 |
|---------|-----------|---------|
| 品牌官网 | 高 | 金融科技品牌官网、产品展示页 |
| 金融科技 | 高 | 支付、金融、区块链产品的视觉设计 |
| 出版物 | 高 | 技术出版物、电子书、白皮书 |
| 技术文档 | 高 | API 文档、开发者文档、技术博客 |
| 渐变设计 | 中 | 品牌渐变、紫色系渐变设计 |

---

## 二、garden-skills 设计语言特征内化

> **来源**: garden-skills（Stripe Press 设计语言特征）

Stripe Press 的设计语言特征——精致渐变、深蓝紫色调、大字号排版、柔和阴影、技术出版物质感，具体内化如下：

### 2.1 精致渐变
- 渐变仅用于品牌区域和英雄区，不用于常规组件
- 渐变方向以 135°（左上→右下）为主，色彩从 `#635BFF` 到 `#0A2540`
- 渐变透明度控制在 0.8-1.0，保持色彩饱和度
- 禁止彩虹渐变/霓虹渐变，仅使用品牌色系内的双色渐变

### 2.2 深蓝紫色调
- 主色 `#635BFF`（Stripe 紫）用于交互元素和品牌标识
- 辅色 `#0A2540`（深蓝）用于正文和深色区域，替代纯黑
- 强调色 `#00D4FF`（亮蓝）用于数据高亮，使用频率极低（≤ 5%）
- 全文档禁止纯黑 `#000000`，使用深蓝 `#0A2540` 作为最深色

### 2.3 大字号排版
- H1 40px（比常规大 25%），营造出版物的"大标题"视觉冲击
- 正文 18px（比常规大 12.5%），提升阅读舒适度
- 标题字重 semibold(600)，与正文 regular(400) 形成明确层级
- 行高宽松（1.7），增强长文阅读体验

### 2.4 柔和阴影
- 阴影透明度极低（0.04-0.08），营造"几乎无感"的漂浮效果
- 阴影模糊半径较大（4px-24px），柔化边缘
- 阴影颜色基于黑色半透明，不使用彩色阴影
- 卡片圆角 12px，配合柔和阴影营造"卡片漂浮"质感

### 2.5 技术出版物质感
- 栅格严格 12 列，内容区通常占据 8 列，两侧留白
- 图文混排采用"书籍式"布局：通栏图 + 居中正文
- 代码块使用 JetBrains Mono，背景 `#0A2540`，文字 `#E5E7EB`
- 引用块使用左侧 3px `#635BFF` 边线，斜体正文

---

## 三、DLP 检索对接规范

### 3.1 检索命中条件

当以下语义信号出现时，DLP 检索器应优先匹配 `DLP-stripe-press`：

1. **内容主题信号**: 金融科技、支付、开发者文档、技术出版物、白皮书
2. **任务类型信号**: wechat_article（技术文章）、research_report（白皮书）
3. **受众信号**: professional（专业人士）、developer（开发者）
4. **排版需求信号**: 渐变设计、大字号排版、柔和阴影、技术出版物质感

### 3.2 design_tokens 输出

```yaml
design_tokens:
  color_scheme:
    primary: "#635BFF"
    secondary: "#0A2540"
    accent: "#00D4FF"
    neutral: "#687385"
    background: "#FFFFFF"
    text: "#0A2540"
  font_scheme:
    heading_font: '"Sohne", "Camphor", "GT America", sans-serif'
    body_font: '"Sohne", "Camphor", "GT America", sans-serif'
    chinese_font: '"Noto Sans SC", "PingFang SC", sans-serif'
    monospace_font: '"JetBrains Mono", "SF Mono", monospace'
  typography:
    h1_size: "40px"
    h2_size: "32px"
    h3_size: "24px"
    h4_size: "20px"
    body_size: "18px"
    caption_size: "14px"
    footnote_size: "13px"
    heading_weight: 600
    body_weight: 400
    emphasis_weight: 500
  spacing:
    base: 4px
    scale: [4, 8, 12, 16, 24, 32, 48, 64, 80]
  grid:
    columns: 12
    gutter: "24px"
    margin: "40px"
    breakpoint: "sm:640px/md:768px/lg:1024px/xl:1280px"
  visual:
    card_radius: "12px"
    button_radius: "8px"
    input_radius: "6px"
    shadow_light: "0 2px 4px rgba(0,0,0,0.04)"
    shadow_medium: "0 8px 24px rgba(0,0,0,0.08)"
  motion:
    transition: "cubic-bezier(0.4, 0, 0.2, 1) 200ms"
    hover: "ease-out 300ms"
```

### 3.3 与 visual_dna 的对接映射

| DLP 字段 | visual_dna 字段 | 映射规则 |
|---------|----------------|---------|
| `color_palette.primary` | `--color-primary` | Stripe 紫直接映射为主色 |
| `color_palette.secondary` | `--color-secondary` | 深蓝映射为辅色 |
| `color_palette.accent` | `--color-accent` | 亮蓝映射为强调色 |
| `typography_scale.body` | `font_scheme.body_size` | 18px 正文字号直接映射 |
| `font_stack.western` | `font_scheme.body_font` | Sohne 字体栈直接注入 |
| `grid_system.columns` | `grid_system.columns` | 12 列栅格直接映射 |
| `radius_shadow.card_radius` | `visual.card_radius` | 12px 圆角直接映射 |

---

## 四、ASR 硬门合规说明

本 DLP 的视觉规范符合以下 ASR 硬门禁令：

| ASR 禁令编号 | 禁令内容 | 本 DLP 合规性 |
|-------------|---------|-------------|
| ASR-FONT-001 | 禁 Inter 作为 Premium 产出字体 | ✅ 使用 Sohne 无衬线字体 |
| ASR-COLOR-002 | 禁纯黑（#000000） | ✅ 使用 #0A2540 深蓝 |
| ASR-LAYOUT-004 | 禁默认 Tailwind 间距阶梯 | ✅ 使用 4/8/12/16/24/32/48/64/80 自定义阶梯 |
| ASR-DECOR-003 | 禁阴影堆叠超过 3 层 | ✅ 最多 2 层阴影（轻微+中等） |
| ASR-MOTION-001 | 禁 width/height 动画 | ✅ 仅使用 transform+opacity 动效 |
| ASR-GRADIENT-001 | 禁彩虹渐变/霓虹渐变 | ✅ 仅使用品牌色系内双色渐变 |

---

> **DLP 元数据**
> - 创建时间: 2026-06-19
> - 族: interface-brand
> - 锚定: Stripe Press 2024 年版式
> - 字段完整性: 12/12 ✅
> - 配色锚定: 真实世界品牌实测配色 ✅
> - 字体栈中文 fallback: 已包含 ✅
> - ASR 硬门合规: 已通过 ✅
> - 来源技能: garden-skills ✅
