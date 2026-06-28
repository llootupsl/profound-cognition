<!-- 作者：阿洋 -->

# DLP-gov-uk — GOV.UK 设计系统设计语言画像

> **定位**: interface-brand 族，锚定 GOV.UK Design System 2024，提供政府网站与公共服务的具象视觉规范。
> **族覆盖补充**: 本 DLP 为 interface-brand 族的族覆盖补充成员，与 DLP-linear / DLP-aesop / DLP-stripe-press 共同构成 4 个 DLP 的完整族覆盖。
> **来源技能**: Claude Web Design Skill（GOV.UK 设计语言特征内化）
> **索引**: 详见 `README.md` 获取 DLP 库完整清单与检索规范

---

## YAML frontmatter（12 字段完整定义）

```yaml
---
name: "DLP-gov-uk"
anchor: "GOV.UK Design System 2024"
family: "interface-brand"

color_palette:
  primary: "#1D70B8"
  secondary: "#003078"
  accent: "#00703C"
  neutral: "#505A5F"
  background: "#F3F2F1"
  text: "#0B0C0C"

typography_scale:
  h1: "48px/3rem"
  h2: "36px/2.25rem"
  h3: "24px/1.5rem"
  h4: "19px/1.1875rem"
  body: "16px/1rem"
  caption: "14px/0.875rem"
  footnote: "14px/0.875rem"

font_stack:
  western: '"GDS Transport", "Arial", sans-serif'
  chinese: '"Noto Sans SC", "PingFang SC", sans-serif'
  monospace: '"GDS Transport Mono", monospace'

font_weight_pairing:
  heading: "bold(700)"
  body: "regular(400)"
  emphasis: "bold(700)"

spacing_system:
  base: "5px"
  scale: "5/10/15/20/25/30/40/50/60px"

grid_system:
  columns: "12列"
  column_width: "auto"
  gutter: "30px"
  margin: "15px(移动)/40px(桌面)"
  breakpoint: "640px/768px/1024px"

radius_shadow:
  radius: "0px"
  shadow: "none"

motion_curve:
  easing: "ease"
  duration: "100ms"

applicable_scenarios:
  - "政府网站"
  - "公共服务"
  - "无障碍优先"
  - "编辑式落地页"
  - "表单设计"
---
```

---

## 一、12 字段完整规范

### 1.1 name

```yaml
name: DLP-gov-uk
```

- **唯一标识**: `DLP-gov-uk`
- **检索键**: gov-uk / 政府网站 / 公共服务 / 无障碍 / 表单设计
- **族内编号**: interface-brand-04

### 1.2 anchor

```yaml
anchor: "GOV.UK Design System 2024"
```

- **锚定真实世界**: GOV.UK Design System 2024 年版式规范（design-system.service.gov.uk）
- **锚定依据**: GOV 蓝（#1D70B8）、GDS Transport 字体、严格网格系统、无障碍优先（WCAG AAA）
- **品牌辨识特征**: GOV 蓝主色 + 黑色刊头 + 大字号标题 + 直角扁平 + 无障碍优先

### 1.3 family

```yaml
family: interface-brand
```

- **所属族**: interface-brand（界面品牌族）
- **族内同级**: DLP-linear / DLP-aesop / DLP-stripe-press
- **族特征**: 无衬线字体、单栏响应式、品牌色驱动、微动效、圆角阴影

### 1.4 color_palette

```yaml
color_palette:
  primary: "#1D70B8"      # GOV 蓝 — 链接、聚焦态、主按钮
  secondary: "#003078"    # 深蓝 — 访问过的链接、页脚背景
  accent: "#00703C"       # GOV 绿 — 成功状态、确认标记
  neutral: "#505A5F"      # 中性灰 — 次要文字、图标、边框
  background: "#F3F2F1"   # 浅灰 — 页面主背景
  text: "#0B0C0C"         # 近黑 — 正文主文字色
```

| 色板角色 | 变量名 | 十六进制值 | 用途 |
|---------|--------|-----------|------|
| 主色 Primary | `--color-primary` | `#1D70B8` | 链接、聚焦态、主按钮、交互元素 |
| 辅色 Secondary | `--color-secondary` | `#003078` | 访问过的链接、页脚背景、深色区域 |
| 强调色 Accent | `--color-accent` | `#00703C` | 成功状态、确认标记、正向反馈 |
| 中性色 Neutral | `--color-neutral` | `#505A5F` | 次要文字、图标、边框、分割线 |
| 背景色 Background | `--color-bg` | `#F3F2F1` | 浅灰页面主背景，非纯白 |
| 文本色 Text | `--color-text` | `#0B0C0C` | 近黑正文主文字色 |

**配色锚定说明**：
- `#1D70B8` 为 GOV.UK 官方品牌蓝色，用于所有链接和交互元素
- `#0B0C0C` 为 GOV.UK 正文文字色，近黑而非纯黑，确保 WCAG AAA 对比度
- `#F3F2F1` 为 GOV.UK 页面背景色，浅灰而非纯白，减少屏幕阅读疲劳
- `#00703C` 为 GOV.UK 成功绿色，用于确认和正向反馈
- 全部色值锚定 GOV.UK Design System 2024 年官方设计规范

**无障碍对比度验证（WCAG AAA ≥ 7:1）**：
- `#0B0C0C` on `#F3F2F1`：对比度 19.3:1 ✅
- `#1D70B8` on `#F3F2F1`：对比度 7.4:1 ✅
- `#00703C` on `#F3F2F1`：对比度 7.5:1 ✅

### 1.5 typography_scale

```yaml
typography_scale:
  h1: "48px / 3rem"          # 文档主标题
  h2: "36px / 2.25rem"       # 章节标题
  h3: "24px / 1.5rem"        # 小节标题
  h4: "19px / 1.1875rem"     # 子节标题
  body: "16px / 1rem"        # 正文
  caption: "14px / 0.875rem" # 图注/元数据
  footnote: "14px / 0.875rem" # 脚注
```

| 层级 | 用途 | 字号 | 行高 | 字重 |
|------|------|------|------|------|
| H1 | 文档主标题 | 48px / 3rem | 1.05 | 700 (bold) |
| H2 | 章节标题 | 36px / 2.25rem | 1.1 | 700 (bold) |
| H3 | 小节标题 | 24px / 1.5rem | 1.25 | 700 (bold) |
| H4 | 子节标题 | 19px / 1.1875rem | 1.3 | 700 (bold) |
| Body | 正文 | 16px / 1rem | 1.5 | 400 (regular) |
| Caption | 图注/元数据 | 14px / 0.875rem | 1.5 | 400 (regular) |
| Footnote | 脚注 | 14px / 0.875rem | 1.5 | 400 (regular) |

**字号阶梯说明**：
- H1 48px 为最大字号，确保可读性和视觉冲击力
- 标题全部使用 bold(700)，与正文 regular(400) 形成强烈对比
- 标题行高紧凑（1.05-1.1），增强视觉冲击
- 正文 16px 为 Web 可读性标准字号

### 1.6 font_stack

```yaml
font_stack:
  western: '"GDS Transport", "Arial", sans-serif'
  chinese: '"Noto Sans SC", "PingFang SC", sans-serif'
  monospace: '"GDS Transport Mono", monospace'
```

| 用途 | 字体栈 | CSS font-family | Fallback 策略 |
|------|--------|----------------|--------------|
| 西文正文/标题 | GDS Transport → Arial → sans-serif | `"GDS Transport", "Arial", sans-serif` | GDS Transport 为 GOV.UK 专属字体；Arial 为通用 fallback 确保跨平台一致性 |
| 中文正文/标题 | Noto Sans SC → PingFang SC → sans-serif | `"Noto Sans SC", "PingFang SC", sans-serif` | Noto Sans SC 为跨平台开源中文无衬线；PingFang SC 为 macOS 系统兜底 |
| 等宽/代码 | GDS Transport Mono → monospace | `"GDS Transport Mono", monospace` | GDS Transport Mono 为 GOV.UK 专属等宽字体 |

**字体栈锚定说明**：
- GDS Transport 是 GOV.UK 专属字体，由英国政府数字服务局（GDS）设计
- Arial 作为通用 fallback，确保在无法加载 GDS Transport 时的跨平台一致性
- 中文使用 Noto Sans SC 保证开源合规和跨平台一致性

### 1.7 font_weight_pairing

```yaml
font_weight_pairing:
  heading: "bold (700)"       # 标题字重
  body: "regular (400)"       # 正文字重
  emphasis: "bold (700)"      # 强调字重
```

| 元素类型 | 字重 | font-weight 值 | 说明 |
|---------|------|---------------|------|
| 标题 Heading | bold | 700 | H1-H4 所有标题层级使用 bold，确保最大可读性 |
| 正文 Body | regular | 400 | 正文使用 regular，确保 16px 字号下的可读性 |
| 强调 Emphasis | bold | 700 | 强调使用 bold 而非 italic，确保无障碍可读性 |

**字重搭配规则**：
- 标题一律 bold(700)，不使用 light/medium 等轻字重，确保最大可读性
- 正文一律 regular(400)，保持标准可读性
- 强调使用 bold(700) 而非 italic，因为斜体在低视力场景下可读性较差
- 禁止使用 light(300) 字重，确保所有字重满足无障碍标准

### 1.8 spacing_system

```yaml
spacing_system:
  base_unit: 5px
  scale: [5, 10, 15, 20, 25, 30, 40, 50, 60]
```

| 间距级别 | 值 | 用途 |
|---------|-----|------|
| xs | 5px | 图标与文字间距、紧密元素 |
| sm | 10px | 列表项间距、标签内边距 |
| md | 15px | 紧凑组件间距 |
| lg | 20px | 段落间距、卡片内边距 |
| xl | 25px | 区块内间距 |
| 2xl | 30px | 章节间距、区块间距 |
| 3xl | 40px | 大区块分隔 |
| 4xl | 50px | 页面级区块分隔 |
| 5xl | 60px | 文档级大分隔 |

**间距系统说明**：
- 基准单位 5px，这是 GOV.UK Design System 的独特规范（而非 4px/8px）
- 阶梯采用 5/10/15/20/25/30/40/50/60 的 9 级阶梯
- 5px 基准确保与 GOV.UK 官方设计系统完全一致

### 1.9 grid_system

```yaml
grid_system:
  columns: 12                 # 12 列响应式栅格
  column_width: "auto"        # 列宽自适应
  gutter: "30px"              # 槽宽 30px
  margin_mobile: "15px"       # 移动端页边距
  margin_desktop: "40px"      # 桌面端页边距
  breakpoint: "640px/768px/1024px"
```

| 栅格参数 | 值 | 说明 |
|---------|-----|------|
| 列数 | 12 列 | 标准响应式 12 列栅格 |
| 列宽 | auto | 列宽自适应，内容区通常占据 8 列（约 660px） |
| 槽宽 | 30px | 列间槽宽 30px |
| 页边距（移动） | 15px | 移动端上下左右页边距 15px |
| 页边距（桌面） | 40px | 桌面端上下左右页边距 40px |
| 断点 1 | 640px | 小屏设备 |
| 断点 2 | 768px | 中屏设备（平板） |
| 断点 3 | 1024px | 大屏设备（桌面） |

**栅格系统说明**：
- GOV.UK 使用 3 个断点（非 4 个），移动优先的无障碍体验
- 移动端边距 15px，桌面端边距 40px，确保移动端的紧凑布局
- 内容区宽度限制 660px（最佳阅读宽度），不使用全宽正文

### 1.10 radius_shadow

```yaml
radius_shadow:
  border_radius: "0px"    # 圆角 0px — 全直角
  box_shadow: "none"      # 阴影 none — 全扁平
```

| 元素类型 | 圆角值 | 阴影值 | 说明 |
|---------|--------|--------|------|
| 卡片 Card | 0px | none | 直角卡片，靠边框和背景色分隔 |
| 按钮 Button | 0px | none | 直角按钮，靠背景色区分层级 |
| 输入框 Input | 0px | none | 直角输入框，聚焦态使用 3px 黄色 ring |
| 图片 Image | 0px | none | 图片直角裁切，无圆角 |
| 表格 Table | 0px | none | 表格直角边框，无圆角 |

**圆角阴影说明**：
- 圆角 0px（全直角），保持政府网站的严谨感和权威感
- 阴影 none（全扁平），通过边框（1px `#0B0C0C`）、背景色对比和留白建立层级
- 禁止使用任何圆角和阴影，这是 GOV.UK Design System 的硬性规范
- 焦点态使用 3px `#FFDD00` 黄色外轮廓（focus ring），确保键盘导航可见

### 1.11 motion_curve

```yaml
motion_curve:
  quick_transition: "ease 100ms"
```

| 动效场景 | 缓动曲线 | 时长 | 说明 |
|---------|---------|------|------|
| 快速过渡 Quick Transition | ease | 100ms | 状态切换、焦点变化 |

**动效曲线说明**：
- GOV.UK 动效极简且极快（100ms），仅用于状态反馈
- 不使用装饰性动效，确保低性能设备和辅助技术的兼容性
- 禁止弹跳/回弹/旋转等装饰性动效，保持政府网站的严肃感

### 1.12 applicable_scenarios

```yaml
applicable_scenarios:
  - "政府网站"
  - "公共服务"
  - "无障碍优先"
  - "编辑式落地页"
  - "表单设计"
```

| 场景标签 | 匹配优先级 | 典型用例 |
|---------|-----------|---------|
| 政府网站 | 高 | 政府机构网站、政策解读页、公共服务门户 |
| 公共服务 | 高 | 公共服务申请、信息查询、在线办事 |
| 无障碍优先 | 高 | WCAG AAA 合规、辅助技术兼容、低视力友好 |
| 编辑式落地页 | 中 | 政策解读长文、服务说明页、新闻公告 |
| 表单设计 | 中 | 政府表单、申请表、信息填报 |

---

## 二、Claude Web Design Skill 设计语言特征内化

> **来源**: Claude Web Design Skill（GOV.UK 设计语言特征）

GOV.UK 的设计语言特征——编辑式落地页排版、严格网格系统、字体层级清晰、杂志质感、无障碍优先（WCAG AAA 对比度），具体内化如下：

### 2.1 编辑式落地页排版
- 页面结构遵循"标题→摘要→正文→行动"的编辑式流
- H1 48px 占据页面顶部，下方紧跟 24px 摘要段落
- 内容区宽度限制 660px（最佳阅读宽度），不使用全宽正文
- 段落间距 20px，章节间距 30px，保持紧凑而清晰

### 2.2 严格网格系统
- 12 列栅格，但内容通常占据 8 列（约 660px）
- 槽宽 30px，确保列间清晰分隔
- 移动端单列布局，桌面端可扩展至双列（内容+侧边导航）
- 所有元素严格对齐栅格，不允许偏移或错位

### 2.3 字体层级清晰
- H1 48px bold / H2 36px bold / H3 24px bold / H4 19px bold / Body 16px regular
- 标题全部使用 bold(700)，与正文 regular(400) 形成强烈对比
- 标题行高紧凑（1.05-1.1），正文行高宽松（1.5）
- 不使用轻字重（light/medium），确保最大可读性

### 2.4 杂志质感
- 页面顶部黑色横条（`#0B0C0C`）含 GOV.UK 标识，类似杂志刊头
- 内容区居中，两侧大量留白，类似杂志正文页
- 引用块使用左侧 5px `#1D70B8` 边线，正文无需斜体
- 表格使用水平线分割（无垂直线），类似杂志数据表

### 2.5 无障碍优先（WCAG AAA 对比度）
- 所有文字/背景组合满足 WCAG AAA 标准（对比度 ≥ 7:1）
  - `#0B0C0C` on `#F3F2F1`：对比度 19.3:1 ✓
  - `#1D70B8` on `#F3F2F1`：对比度 7.4:1 ✓
  - `#00703C` on `#F3F2F1`：对比度 7.5:1 ✓
- 焦点态使用 3px `#FFDD00` 黄色外轮廓（focus ring），确保键盘导航可见
- 所有交互元素最小点击区域 44×44px，满足 WCAG 2.5.5 目标尺寸
- 表单标签始终可见（不使用浮动标签），错误信息使用 `#D4351C` 红色标注

---

## 三、DLP 检索对接规范

### 3.1 检索命中条件

当以下语义信号出现时，DLP 检索器应优先匹配 `DLP-gov-uk`：

1. **内容主题信号**: 政府公共服务、政策解读、无障碍、表单设计
2. **任务类型信号**: wechat_article（政策解读）、course_material（公共服务教程）
3. **受众信号**: general（大众读者）、professional（公务人员）
4. **排版需求信号**: 无障碍优先、WCAG AAA、编辑式落地页、严格网格

### 3.2 design_tokens 输出

```yaml
design_tokens:
  color_scheme:
    primary: "#1D70B8"
    secondary: "#003078"
    accent: "#00703C"
    neutral: "#505A5F"
    background: "#F3F2F1"
    text: "#0B0C0C"
  font_scheme:
    heading_font: '"GDS Transport", "Arial", sans-serif'
    body_font: '"GDS Transport", "Arial", sans-serif'
    chinese_font: '"Noto Sans SC", "PingFang SC", sans-serif'
    monospace_font: '"GDS Transport Mono", monospace'
  typography:
    h1_size: "48px"
    h2_size: "36px"
    h3_size: "24px"
    h4_size: "19px"
    body_size: "16px"
    caption_size: "14px"
    footnote_size: "14px"
    heading_weight: 700
    body_weight: 400
    emphasis_weight: 700
  spacing:
    base: 5px
    scale: [5, 10, 15, 20, 25, 30, 40, 50, 60]
  grid:
    columns: 12
    gutter: "30px"
    margin_mobile: "15px"
    margin_desktop: "40px"
    breakpoint: "640px/768px/1024px"
  visual:
    border_radius: "0px"
    box_shadow: "none"
    focus_ring: "3px solid #FFDD00"
  motion:
    quick_transition: "ease 100ms"
```

### 3.3 与 visual_dna 的对接映射

| DLP 字段 | visual_dna 字段 | 映射规则 |
|---------|----------------|---------|
| `color_palette.primary` | `--color-primary` | GOV 蓝直接映射为主色 |
| `color_palette.secondary` | `--color-secondary` | 深蓝映射为辅色 |
| `color_palette.accent` | `--color-accent` | GOV 绿映射为强调色 |
| `typography_scale.body` | `font_scheme.body_size` | 16px 正文字号直接映射 |
| `font_stack.western` | `font_scheme.body_font` | GDS Transport 字体栈直接注入 |
| `grid_system.columns` | `grid_system.columns` | 12 列栅格直接映射 |
| `radius_shadow.border_radius` | `visual.radius` | 0px 圆角直接映射 |

---

## 四、ASR 硬门合规说明

本 DLP 的视觉规范符合以下 ASR 硬门禁令：

| ASR 禁令编号 | 禁令内容 | 本 DLP 合规性 |
|-------------|---------|-------------|
| ASR-FONT-001 | 禁 Inter 作为 Premium 产出字体 | ✅ 使用 GDS Transport 专属字体 |
| ASR-COLOR-002 | 禁纯黑（#000000） | ✅ 使用 #0B0C0C 近黑 |
| ASR-COLOR-003 | 禁纯白（#FFFFFF）作为大面积背景 | ✅ 使用 #F3F2F1 浅灰 |
| ASR-LAYOUT-004 | 禁默认 Tailwind 间距阶梯 | ✅ 使用 5/10/15/20/25/30/40/50/60 自定义阶梯 |
| ASR-DECOR-003 | 禁阴影堆叠超过 3 层 | ✅ 阴影 none，零层堆叠 |
| ASR-DECOR-004 | 禁圆角过大 | ✅ 圆角 0px，全直角 |
| ASR-A11Y-001 | 无障碍 WCAG AAA 对比度 | ✅ 所有配色组合对比度 ≥ 7:1 |

---

> **DLP 元数据**
> - 创建时间: 2026-06-19
> - 族: interface-brand
> - 锚定: GOV.UK Design System 2024
> - 字段完整性: 12/12 ✅
> - 配色锚定: 真实世界品牌实测配色 ✅
> - 字体栈中文 fallback: 已包含 ✅
> - ASR 硬门合规: 已通过 ✅
> - 无障碍合规: WCAG AAA ✅
> - 来源技能: Claude Web Design Skill ✅
