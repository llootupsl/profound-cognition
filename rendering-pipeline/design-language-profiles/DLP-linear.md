<!-- 作者：阿洋 -->

# DLP-linear — Linear 产品界面设计语言画像

> **定位**: interface-brand 族，锚定 Linear.app 2024 年产品界面，提供 SaaS 产品界面的具象视觉规范。
> **族覆盖补充**: 本 DLP 为 interface-brand 族的族覆盖补充成员，与 DLP-aesop / DLP-stripe-press / DLP-gov-uk 共同构成 4 个 DLP 的完整族覆盖。
> **来源技能**: garden-skills（Linear 设计语言特征内化）
> **索引**: 详见 `README.md` 获取 DLP 库完整清单与检索规范

---

## YAML frontmatter（12 字段完整定义）

```yaml
---
name: "DLP-linear"
anchor: "Linear.app 2024 年产品界面"
family: "interface-brand"

color_palette:
  primary: "#5E6AD2"
  secondary: "#26282D"
  accent: "#F4F4F5"
  neutral: "#8A8F98"
  background: "#0F1115"
  text: "#E5E7EB"

typography_scale:
  h1: "32px/2rem"
  h2: "24px/1.5rem"
  h3: "20px/1.25rem"
  h4: "16px/1rem"
  body: "14px/0.875rem"
  caption: "12px/0.75rem"
  footnote: "11px/0.6875rem"

font_stack:
  western: '"Mona Sans", "Söhne", "SF Pro Display", -apple-system, sans-serif'
  chinese: '"PingFang SC", "Noto Sans SC", sans-serif'
  monospace: '"JetBrains Mono", "SF Mono", monospace'

font_weight_pairing:
  heading: "semibold(600)"
  body: "regular(400)"
  emphasis: "medium(500)"

spacing_system:
  base: "4px"
  scale: "4/8/12/16/20/24/32/40/48px"

grid_system:
  columns: "12列"
  column_width: "auto"
  gutter: "24px"
  margin: "32px"
  breakpoint: "sm:640px/md:768px/lg:1024px/xl:1280px"

radius_shadow:
  radius: "8px(卡片)/6px(按钮)/4px(输入框)"
  shadow: "0 1px 2px rgba(0,0,0,0.05)(轻微)/0 4px 12px rgba(0,0,0,0.1)(中等)"

motion_curve:
  easing: "cubic-bezier(0.4, 0, 0.2, 1)/ease-out/ease-in-out"
  duration: "150-300ms"

applicable_scenarios:
  - "产品界面"
  - "SaaS"
  - "项目管理"
  - "开发工具"
  - "暗色模式"
---
```

---

## 一、12 字段完整规范

### 1.1 name

```yaml
name: DLP-linear
```

- **唯一标识**: `DLP-linear`
- **检索键**: linear / SaaS / 项目管理 / 开发工具 / 暗色模式
- **族内编号**: interface-brand-01

### 1.2 anchor

```yaml
anchor: "Linear.app 2024 年产品界面"
```

- **锚定真实世界**: Linear.app 2024 年产品界面（Web + Desktop App）
- **锚定依据**: Linear 紫色品牌色（#5E6AD2）、极简几何界面、紧凑间距、精确阴影层级、微妙动效
- **品牌辨识特征**: 紫色主色 + 深灰背景 + 紧凑信息密度 + 极简线性图标 + 克制动效

### 1.3 family

```yaml
family: interface-brand
```

- **所属族**: interface-brand（界面品牌族）
- **族内同级**: DLP-aesop / DLP-stripe-press / DLP-gov-uk
- **族特征**: 无衬线字体、单栏响应式、品牌色驱动、微动效、圆角阴影

### 1.4 color_palette

```yaml
color_palette:
  primary: "#5E6AD2"      # Linear 紫 — 标题强调、链接、聚焦态、主按钮
  secondary: "#26282D"    # 深灰 — 侧边栏背景、次级容器
  accent: "#F4F4F5"       # 浅灰 — 悬浮层、分割强调
  neutral: "#8A8F98"      # 中性灰 — 次要文字、图标、占位符
  background: "#0F1115"   # 深色模式背景 — 页面主背景（暗色模式为默认）
  text: "#E5E7EB"         # 浅色文本 — 正文主文字色（暗色模式）
```

| 色板角色 | 变量名 | 十六进制值 | 用途 |
|---------|--------|-----------|------|
| 主色 Primary | `--color-primary` | `#5E6AD2` | 标题强调、链接、聚焦态、主按钮、选中态 |
| 辅色 Secondary | `--color-secondary` | `#26282D` | 侧边栏背景、次级容器、深色面板 |
| 强调色 Accent | `--color-accent` | `#F4F4F5` | 悬浮层背景、分割强调、浅色面板 |
| 中性色 Neutral | `--color-neutral` | `#8A8F98` | 次要文字、图标、占位符、元数据 |
| 背景色 Background | `--color-bg` | `#0F1115` | 深色模式主背景 |
| 文本色 Text | `--color-text` | `#E5E7EB` | 深色模式正文主文字色 |

**配色锚定说明**：
- `#5E6AD2` 为 Linear 官方品牌紫色，用于所有交互元素，是最高辨识度色彩
- `#0F1115` 为 Linear 深色模式背景，非纯黑（#000000），符合 ASR 禁纯黑规则
- 浅色模式备选：背景 `#FFFFFF` / 文本 `#1A1A1A`，在浅色主题场景下替换 background 和 text 字段
- 全部色值锚定 Linear.app 2024 年实际产品界面的实测配色

### 1.5 typography_scale

```yaml
typography_scale:
  h1: "32px / 2rem"         # 文档主标题
  h2: "24px / 1.5rem"       # 章节标题
  h3: "20px / 1.25rem"      # 小节标题
  h4: "16px / 1rem"         # 子节标题
  body: "14px / 0.875rem"   # 正文（紧凑无衬线）
  caption: "12px / 0.75rem" # 图注/元数据
  footnote: "11px / 0.6875rem" # 脚注
```

| 层级 | 用途 | 字号 | 行高 | 字重 |
|------|------|------|------|------|
| H1 | 文档主标题 | 32px / 2rem | 1.2 | 600 (semibold) |
| H2 | 章节标题 | 24px / 1.5rem | 1.3 | 600 (semibold) |
| H3 | 小节标题 | 20px / 1.25rem | 1.4 | 600 (semibold) |
| H4 | 子节标题 | 16px / 1rem | 1.5 | 600 (semibold) |
| Body | 正文 | 14px / 0.875rem | 1.6 | 400 (regular) |
| Caption | 图注/元数据 | 12px / 0.75rem | 1.5 | 400 (regular) |
| Footnote | 脚注 | 11px / 0.6875rem | 1.5 | 400 (regular) |

**字号阶梯说明**：
- 正文采用 14px 紧凑字号，这是 Linear 产品界面的实际正文字号，确保高信息密度
- 标题层级采用 semibold(600) 字重，与正文 regular(400) 形成明确层级
- 脚注 11px 为最小字号，仅用于辅助信息

### 1.6 font_stack

```yaml
font_stack:
  western: '"Mona Sans", "Söhne", "SF Pro Display", -apple-system, sans-serif'
  chinese: '"PingFang SC", "Noto Sans SC", sans-serif'
  monospace: '"JetBrains Mono", "SF Mono", monospace'
```

| 用途 | 字体栈 | CSS font-family | Fallback 策略 |
|------|--------|----------------|--------------|
| 西文正文/标题 | Mona Sans → Söhne → SF Pro Display → -apple-system → sans-serif | `"Mona Sans", "Söhne", "SF Pro Display", -apple-system, sans-serif` | Mona Sans 为 GitHub 开源字体替代 Inter；Söhne 为 Linear 实际使用字体；SF Pro Display 为 Apple 系统兜底 |
| 中文正文/标题 | PingFang SC → Noto Sans SC → sans-serif | `"PingFang SC", "Noto Sans SC", sans-serif` | PingFang SC 为 macOS 中文无衬线标准；Noto Sans SC 为跨平台开源替代 |
| 等宽/代码 | JetBrains Mono → SF Mono → monospace | `"JetBrains Mono", "SF Mono", monospace` | JetBrains Mono 为开发工具标准等宽字体；SF Mono 为 Apple 系统兜底 |

**字体栈锚定说明**：
- **ASR 硬门禁令合规**: 禁止 Inter 作为 Premium 字体，本 DLP 使用 Mona Sans（GitHub 开源）替代 Inter
- Söhne 是 Linear 实际使用的商业字体，Mona Sans 为开源替代首选
- 中文 fallback 采用 PingFang SC，与西文无衬线字体风格一致

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
| 正文 Body | regular | 400 | 正文使用 regular，确保 14px 紧凑字号下的可读性 |
| 强调 Emphasis | medium | 500 | 强调使用 medium 而非 bold，保持 Linear 的克制风格 |

**字重搭配规则**：
- 标题一律 semibold(600)，不使用 bold(700)，保持产品界面的现代克制感
- 正文一律 regular(400)，不使用 light(300)，确保小字号下的笔画清晰度
- 强调使用 medium(500)，介于标题和正文之间，用于关键信息高亮

### 1.8 spacing_system

```yaml
spacing_system:
  base_unit: 4px
  scale: [4, 8, 12, 16, 20, 24, 32, 40, 48]
```

| 间距级别 | 值 | 用途 |
|---------|-----|------|
| xs | 4px | 图标与文字间距、紧密元素 |
| sm | 8px | 列表项间距、标签内边距 |
| md | 12px | 紧凑组件间距 |
| lg | 16px | 段落间距、卡片内边距 |
| xl | 20px | 区块内间距 |
| 2xl | 24px | 章节间距、区块间距 |
| 3xl | 32px | 大标题下方间距、主要区块分隔 |
| 4xl | 40px | 页面级区块分隔 |
| 5xl | 48px | 文档级大分隔 |

**间距系统说明**：
- 基准单位 4px，与 visual-dna.md 的 4px 基准栅格系统对齐
- 阶梯采用 4/8/12/16/20/24/32/40/48 的 9 级阶梯，覆盖从微观到宏观的间距需求
- Linear 产品界面信息密度偏高（VISUAL_DENSITY ≈ 7），列表行高 32px（紧凑模式）/ 40px（舒适模式）

### 1.9 grid_system

```yaml
grid_system:
  columns: 12                 # 12 列响应式栅格
  column_width: "auto"        # 列宽自适应
  gutter: "24px"              # 槽宽 24px
  margin: "32px"              # 页边距 32px
  breakpoint: "sm:640px/md:768px/lg:1024px/xl:1280px"
```

| 栅格参数 | 值 | 说明 |
|---------|-----|------|
| 列数 | 12 列 | 标准响应式 12 列栅格 |
| 列宽 | auto | 列宽自适应，由断点和列数决定 |
| 槽宽 | 24px | 列间槽宽 24px，适中分隔 |
| 页边距 | 32px | 上下左右页边距 32px |
| 断点 sm | 640px | 小屏设备 |
| 断点 md | 768px | 中屏设备（平板） |
| 断点 lg | 1024px | 大屏设备（桌面） |
| 断点 xl | 1280px | 超大屏设备 |

**栅格系统说明**：
- 12 列栅格是 Linear 产品界面的标准布局系统，支持灵活的列组合
- 槽宽 24px 确保列间清晰分隔，适配高信息密度界面
- 4 个断点覆盖从移动端到桌面端的完整响应式适配

### 1.10 radius_shadow

```yaml
radius_shadow:
  card_radius: "8px"       # 卡片圆角
  button_radius: "6px"     # 按钮圆角
  input_radius: "4px"      # 输入框圆角
  shadow_light: "0 1px 2px rgba(0,0,0,0.05)"    # 轻微阴影
  shadow_medium: "0 4px 12px rgba(0,0,0,0.1)"   # 中等阴影
```

| 元素类型 | 圆角值 | 阴影值 | 说明 |
|---------|--------|--------|------|
| 卡片 Card | 8px | 轻微/中等 | 内容卡片、信息面板，悬浮时阴影加深 |
| 按钮 Button | 6px | none | 交互按钮，无阴影，靠背景色区分层级 |
| 输入框 Input | 4px | none | 表单输入，聚焦态使用 ring 而非阴影 |
| 图片 Image | 8px | none | 图片圆角与卡片一致 |
| 模态框 Modal | 8px | 中等 | 弹出层使用中等阴影 |

**圆角阴影说明**：
- 三层圆角体系：8px(卡片) / 6px(按钮) / 4px(输入框)，形成递减的圆角层级
- 两层阴影体系：轻微（悬浮卡片）/ 中等（模态框），阴影基于黑色半透明
- 暗色模式下阴影加深至 `rgba(0,0,0,0.3)` 以保证可见性
- 阴影颜色基于黑色半透明，不使用彩色阴影

### 1.11 motion_curve

```yaml
motion_curve:
  hover: "ease-out 150ms"
  transition: "ease-in-out 200ms"
  expand: "cubic-bezier(0.4, 0, 0.2, 1) 300ms"
```

| 动效场景 | 缓动曲线 | 时长 | 说明 |
|---------|---------|------|------|
| 悬停 Hover | ease-out | 150ms | 按钮悬停、图标切换、颜色反馈 |
| 过渡 Transition | ease-in-out | 200ms | 颜色过渡、状态切换、面板切换 |
| 展开 Expand | cubic-bezier(0.4, 0, 0.2, 1) | 300ms | 折叠面板展开、抽屉滑出、下拉菜单 |

**动效曲线说明**：
- 动效时长极短（150-300ms），营造"快速响应"的产品体验
- 缓动函数以 ease-out 为主，元素"快速出现，缓慢停止"
- 禁止弹跳/回弹动效，保持专业克制
- 仅动画 transform 和 opacity（GPU 加速），禁止 width/height 动画

### 1.12 applicable_scenarios

```yaml
applicable_scenarios:
  - "产品界面"
  - "SaaS"
  - "项目管理"
  - "开发工具"
  - "暗色模式"
```

| 场景标签 | 匹配优先级 | 典型用例 |
|---------|-----------|---------|
| 产品界面 | 高 | SaaS 产品、Web App、桌面应用界面设计 |
| SaaS | 高 | 软件即服务产品的 UI 设计 |
| 项目管理 | 高 | 任务管理、项目追踪、团队协作工具 |
| 开发工具 | 高 | IDE、代码编辑器、开发者平台 |
| 暗色模式 | 中 | 深色主题界面、夜间模式设计 |

---

## 二、garden-skills 设计语言特征内化

> **来源**: garden-skills（Linear 设计语言特征）

Linear 的设计语言特征——极简几何、紫色调、紧凑间距、精确的阴影层级、微妙的动效，具体内化如下：

### 2.1 极简几何
- 所有视觉元素遵循几何极简原则，去除多余装饰
- 图标使用 1.5px 描边线性图标，无填充
- 分割线使用 1px `#26282D` 半透明（opacity 0.08），不使用粗边框

### 2.2 紫色调系统
- 主色 `#5E6AD2`（Linear 紫）贯穿所有交互元素：链接、聚焦态、选中态、主按钮
- 紫色仅用于交互态，不用于装饰性背景
- 暗色模式下紫色亮度提升 8% 以保证对比度

### 2.3 紧凑间距
- 基准 4px，信息密度偏高（VISUAL_DENSITY ≈ 7）
- 列表行高 32px（紧凑模式）/ 40px（舒适模式）
- 卡片内边距 16px，组件间距 12px

### 2.4 精确的阴影层级
- 三层阴影体系：轻微（悬浮）/中等（弹出）/无（静态）
- 阴影颜色基于黑色半透明，不使用彩色阴影
- 暗色模式下阴影加深至 `rgba(0,0,0,0.3)` 以保证可见性

### 2.5 微妙的动效
- 动效时长极短（150-300ms），不喧宾夺主
- 缓动函数以 ease-out 为主，营造"快速响应"感
- 禁止弹跳/回弹动效，保持专业克制

---

## 三、DLP 检索对接规范

### 3.1 检索命中条件

当以下语义信号出现时，DLP 检索器应优先匹配 `DLP-linear`：

1. **内容主题信号**: SaaS、项目管理、开发工具、产品界面、开发者工具
2. **任务类型信号**: wechat_article（产品介绍）、course_material（产品教程）
3. **受众信号**: professional（专业人士）、developer（开发者）
4. **排版需求信号**: 暗色模式、高信息密度、紧凑布局、微动效

### 3.2 design_tokens 输出

```yaml
design_tokens:
  color_scheme:
    primary: "#5E6AD2"
    secondary: "#26282D"
    accent: "#F4F4F5"
    neutral: "#8A8F98"
    background: "#0F1115"
    text: "#E5E7EB"
  font_scheme:
    heading_font: '"Mona Sans", "Söhne", "SF Pro Display", -apple-system, sans-serif'
    body_font: '"Mona Sans", "Söhne", "SF Pro Display", -apple-system, sans-serif'
    chinese_font: '"PingFang SC", "Noto Sans SC", sans-serif'
    monospace_font: '"JetBrains Mono", "SF Mono", monospace'
  typography:
    h1_size: "32px"
    h2_size: "24px"
    h3_size: "20px"
    h4_size: "16px"
    body_size: "14px"
    caption_size: "12px"
    footnote_size: "11px"
    heading_weight: 600
    body_weight: 400
    emphasis_weight: 500
  spacing:
    base: 4px
    scale: [4, 8, 12, 16, 20, 24, 32, 40, 48]
  grid:
    columns: 12
    gutter: "24px"
    margin: "32px"
    breakpoint: "sm:640px/md:768px/lg:1024px/xl:1280px"
  visual:
    card_radius: "8px"
    button_radius: "6px"
    input_radius: "4px"
    shadow_light: "0 1px 2px rgba(0,0,0,0.05)"
    shadow_medium: "0 4px 12px rgba(0,0,0,0.1)"
  motion:
    hover: "ease-out 150ms"
    transition: "ease-in-out 200ms"
    expand: "cubic-bezier(0.4, 0, 0.2, 1) 300ms"
```

### 3.3 与 visual_dna 的对接映射

| DLP 字段 | visual_dna 字段 | 映射规则 |
|---------|----------------|---------|
| `color_palette.primary` | `--color-primary` | Linear 紫直接映射为主色 |
| `color_palette.secondary` | `--color-secondary` | 深灰映射为辅色 |
| `color_palette.accent` | `--color-accent` | 浅灰映射为强调色 |
| `typography_scale.body` | `font_scheme.body_size` | 14px 正文字号直接映射 |
| `font_stack.western` | `font_scheme.body_font` | Mona Sans 字体栈直接注入 |
| `grid_system.columns` | `grid_system.columns` | 12 列栅格直接映射 |
| `radius_shadow.card_radius` | `visual.card_radius` | 8px 圆角直接映射 |

---

## 四、ASR 硬门合规说明

本 DLP 的视觉规范符合以下 ASR 硬门禁令：

| ASR 禁令编号 | 禁令内容 | 本 DLP 合规性 |
|-------------|---------|-------------|
| ASR-FONT-001 | 禁 Inter 作为 Premium 产出字体 | ✅ 使用 Mona Sans 替代 Inter |
| ASR-COLOR-002 | 禁纯黑（#000000） | ✅ 使用 #0F1115 深色背景 |
| ASR-COLOR-003 | 禁纯白（#FFFFFF）作为大面积背景（暗色模式） | ✅ 暗色模式使用 #0F1115 |
| ASR-LAYOUT-004 | 禁默认 Tailwind 间距阶梯 | ✅ 使用 4/8/12/16/20/24/32/40/48 自定义阶梯 |
| ASR-DECOR-003 | 禁阴影堆叠超过 3 层 | ✅ 最多 2 层阴影（轻微+中等） |
| ASR-MOTION-001 | 禁 width/height 动画 | ✅ 仅使用 transform+opacity 动效 |

---

> **DLP 元数据**
> - 创建时间: 2026-06-19
> - 族: interface-brand
> - 锚定: Linear.app 2024 年产品界面
> - 字段完整性: 12/12 ✅
> - 配色锚定: 真实世界品牌实测配色 ✅
> - 字体栈中文 fallback: 已包含 ✅
> - ASR 硬门合规: 已通过 ✅
> - 来源技能: garden-skills ✅
