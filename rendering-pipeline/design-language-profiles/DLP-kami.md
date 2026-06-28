<!-- 作者：阿洋 -->

# DLP-kami — 纸感美学设计语言画像

> **定位**: publication-typesetting 族，锚定 Kami 纸感美学设计，融入 Kami Skill 的纸感美学专精能力。
> **融入来源技能**: Kami Skill — 纸感美学特征（米色底调 #F5F0E6、衬线字体 EB Garamond、高级出版物级阅读质感、微妙的纸感阴影、阅读优先的单栏布局）
> **索引**: 详见 `README.md` 获取 DLP 库完整清单与检索规范

---

## YAML frontmatter（12 字段完整定义）

```yaml
---
name: "DLP-kami"
anchor: "Kami 纸感美学设计"
family: "publication-typesetting"

color_palette:
  primary: "#3D3522"
  secondary: "#8B7355"
  accent: "#A0522D"
  neutral: "#C4B998"
  background: "#F5F0E6"
  text: "#3D3522"

typography_scale:
  h1: "32px/2rem"
  h2: "24px/1.5rem"
  h3: "20px/1.25rem"
  h4: "16px/1rem"
  body: "16px/1rem"
  caption: "13px/0.8125rem"
  footnote: "12px/0.75rem"

font_stack:
  western: '"EB Garamond", "Crimson Text", "Georgia", serif'
  chinese: '"宋体", "SimSun", "Noto Serif SC", serif'
  monospace: '"Courier New", "Courier", monospace'

font_weight_pairing:
  heading: "regular(400)"
  body: "regular(400)"
  emphasis: "italic(400)"

spacing_system:
  base: "8px"
  scale: "8/16/24/32/48/64px"

grid_system:
  columns: "单栏"
  column_width: "65ch(约620px)"
  gutter: "N/A"
  margin: "48px"
  breakpoint: "N/A(阅读媒介)"

radius_shadow:
  radius: "2px"
  shadow: "0 1px 3px rgba(61,53,34,0.08)"

motion_curve:
  easing: "ease-out"
  duration: "200-300ms"

applicable_scenarios:
  - "阅读体验"
  - "纸感美学"
  - "米色底调"
  - "衬线字体"
  - "高级出版物"
  - "散文"
  - "随笔"
---
```

---

## 一、12 字段完整规范

### 1.1 name

```yaml
name: DLP-kami
```

- **唯一标识**: `DLP-kami`
- **检索键**: kami / 纸感美学 / 米色底调 / 衬线字体 / 阅读体验 / 散文 / 随笔
- **族内编号**: publication-typesetting-04

### 1.2 anchor

```yaml
anchor: "Kami 纸感美学设计"
```

- **锚定真实世界**: Kami 纸感美学设计体系（以"纸"为核心媒介的高級阅读体验设计）
- **锚定依据**: 米色纸感底调（#F5F0E6）、EB Garamond 衬线字体、微妙纸感阴影、阅读优先的单栏布局
- **品牌辨识特征**: 米色底调 + 衬线字体 + 微妙纸感阴影 + 单栏阅读优先布局 + 高级出版物级阅读质感

### 1.3 family

```yaml
family: publication-typesetting
```

- **所属族**: publication-typesetting（出版排版族）
- **族内同级**: DLP-economist / DLP-ted / DLP-newyorker
- **族特征**: 锚定真实世界出版物/美学体系，本 DLP 专注"纸感美学"这一独特的阅读体验设计领域

### 1.4 color_palette

```yaml
color_palette:
  primary: "#3D3522"      # 深棕 — 标题、正文文字（纸感深色）
  secondary: "#8B7355"    # 浅棕 — 辅助文字、次要强调
  accent: "#A0522D"       # 赭石 — 重点强调、引言标记、链接
  neutral: "#C4B998"      # 中性米 — 图注、脚注、分割线、元数据
  background: "#F5F0E6"   # 米色纸感 — 页面背景（核心特征色）
  text: "#3D3522"         # 文本色 — 正文主文字色（深棕）
```

| 色板角色 | 变量名 | 十六进制值 | 用途 |
|---------|--------|-----------|------|
| 主色 Primary | `--color-primary` | `#3D3522` | 标题、正文文字（深棕色，纸感墨色） |
| 辅色 Secondary | `--color-secondary` | `#8B7355` | 辅助文字、次要强调、次要标题 |
| 强调色 Accent | `--color-accent` | `#A0522D` | 重点强调、引言标记、超链接（赭石色） |
| 中性色 Neutral | `--color-neutral` | `#C4B998` | 图注、脚注、分割线、元数据（中性米色） |
| 背景色 Background | `--color-bg` | `#F5F0E6` | 页面主背景（米色纸感，核心特征色） |
| 文本色 Text | `--color-text` | `#3D3522` | 正文主文字色（深棕，纸感墨色） |

**配色锚定说明**：
- `#F5F0E6` 为 Kami 纸感美学的核心底色——米色纸感背景，模拟真实纸张的温暖色调，是本 DLP 的最高辨识度色彩
- `#3D3522` 为深棕色文字色，模拟纸张上的墨水色调，比纯黑更温暖、更柔和，适合长时间阅读
- `#A0522D` 为赭石色强调色，与米色底调形成温暖和谐的对比，用于重点强调
- `#8B7355` 为浅棕色辅助色，用于次要文字和辅助标题
- `#C4B998` 为中性米色，用于图注和分割线，与背景色和谐统一
- 全部色值锚定 Kami 纸感美学设计体系的实际配色，传达"纸"的温暖与质感

### 1.5 typography_scale

```yaml
typography_scale:
  h1: "32px / 2rem"          # 文章主标题（大字号，regular）
  h2: "24px / 1.5rem"        # 章节标题（中字号，regular）
  h3: "20px / 1.25rem"       # 小节标题（小字号，regular）
  h4: "16px / 1rem"          # 子节标题（紧凑，regular）
  body: "16px / 1rem"        # 正文（阅读优先级标准字号）
  caption: "13px / 0.8125rem"  # 图注/辅助文字
  footnote: "12px / 0.75rem"   # 脚注/来源标注
```

| 层级 | 用途 | 字号 | 行高 | 字重 |
|------|------|------|------|------|
| H1 | 文章主标题 | 32px / 2rem | 1.3 | 400 (regular) |
| H2 | 章节标题 | 24px / 1.5rem | 1.4 | 400 (regular) |
| H3 | 小节标题 | 20px / 1.25rem | 1.45 | 400 (regular) |
| H4 | 子节标题 | 16px / 1rem | 1.5 | 400 (regular) |
| Body | 正文 | 16px / 1rem | 1.8 | 400 (regular) |
| Caption | 图注/辅助文字 | 13px / 0.8125rem | 1.5 | 400 (regular) |
| Footnote | 脚注/来源标注 | 12px / 0.75rem | 1.45 | 400 (regular) |

**字号阶梯说明**：
- 正文采用 16px（1rem），这是 Web 阅读的标准字号，确保跨设备的最佳可读性
- **所有标题层级使用 regular(400) 而非 bold**——与 DLP-newyorker 类似，靠字号和字体建立层级
- 行高 1.8（正文）比其他 DLP 更宽松，营造纸感阅读的舒适呼吸感
- 字号阶梯采用 1.25 倍递增比例（32→24→20→16），形成温和的视觉层级

### 1.6 font_stack

```yaml
font_stack:
  western: '"EB Garamond", "Crimson Text", "Georgia", serif'
  chinese: '"宋体", "SimSun", "Noto Serif SC", serif'
  monospace: '"Courier New", "Courier", monospace'
```

| 用途 | 字体栈 | CSS font-family | Fallback 策略 |
|------|--------|----------------|--------------|
| 西文正文/标题 | EB Garamond → Crimson Text → Georgia → serif | `"EB Garamond", "Crimson Text", "Georgia", serif` | EB Garamond 为纸感美学首选衬线字体；Crimson Text 为开源替代；Georgia 为系统衬线兜底 |
| 中文正文/标题 | 宋体 → SimSun → Noto Serif SC → serif | `"宋体", "SimSun", "Noto Serif SC", serif` | 宋体/SimSun 为中文衬线印刷标准；Noto Serif SC 为跨平台开源替代 |
| 等宽/代码 | Courier New → Courier → monospace | `"Courier New", "Courier", monospace` | Courier New 为印刷级等宽字体兜底 |

**字体栈锚定说明**：
- EB Garamond 是 Kami 纸感美学的首选字体——基于 Claude Garamond 的 16 世纪衬线字体设计，传达古典书籍的质感
- Crimson Text 为开源衬线字体，字形接近 EB Garamond，作为首选 fallback
- Georgia 为系统级衬线字体，确保跨平台兜底
- 中文 fallback 采用宋体/SimSun/Noto Serif SC，与西文衬线字体风格一致，保持纸感阅读体验
- Garamond 字体的选择传达纸感美学的"古典书籍传承"——这是文艺复兴以来的排版传统

### 1.7 font_weight_pairing

```yaml
font_weight_pairing:
  heading: "regular (400)"    # 标题字重（regular，非 bold）
  body: "regular (400)"       # 正文字重
  emphasis: "italic (400)"    # 强调字重（斜体）
```

| 元素类型 | 字重 | font-weight 值 | 说明 |
|---------|------|---------------|------|
| 标题 Heading | regular | 400 | 所有标题使用 regular，靠字号和 Garamond 字体本身建立层级 |
| 正文 Body | regular | 400 | 正文使用 regular，与标题字重一致，形成统一的纸感阅读质感 |
| 强调 Emphasis | italic | 400 | 强调使用斜体，用于书名、外来词、强调词、散文中的情感表达 |

**字重搭配规则**：
- 标题一律 regular(400)，不使用 bold——纸感美学追求温和优雅的视觉层级，而非强烈的字重对比
- 正文一律 regular(400)，与标题字重统一，营造纸感阅读的连贯性
- 强调使用 italic(400)，Garamond 的斜体特别优美，适合散文和随笔的情感表达
- 禁止使用 bold 字重，保持纸感美学的柔和与优雅

### 1.8 spacing_system

```yaml
spacing_system:
  base_unit: 8px
  scale: [8, 16, 24, 32, 48, 64]
```

| 间距级别 | 值 | 用途 |
|---------|-----|------|
| xs | 8px | 字符间距微调、图标与文字紧贴 |
| sm | 16px | 段落内行间距微调、列表项间距 |
| md | 24px | 段落间距、图注与正文间距 |
| lg | 32px | 小节标题与正文间距、元素组间距 |
| xl | 48px | 章节标题上下间距、大元素间距 |
| 2xl | 64px | 页面边距、大区块分隔 |

**间距系统说明**：
- 基准单位 8px，适应纸感阅读的舒适间距需求
- 阶梯采用 8/16/24/32/48/64 的 6 级阶梯，间距较为宽松，营造纸感阅读的呼吸感
- 段落间距 24px（md 级别），确保散文和随笔的段落分明
- 页面边距 48px（xl 级别），确保内容不贴边，营造高级出版物的留白感

### 1.9 grid_system

```yaml
grid_system:
  columns: 1                  # 单栏阅读优先布局
  column_width: "65ch"        # 列宽 65 字符（约 620px）
  gutter_width: "N/A"         # 单栏无槽宽
  margin: "48px"              # 页面边距 48px
```

| 栅格参数 | 值 | 说明 |
|---------|-----|------|
| 列数 | 1 栏 | 阅读优先的单栏布局，专注沉浸式阅读体验 |
| 列宽 | 65ch（约 620px） | 65 字符列宽，这是排版学的最佳行长（45-75 字符区间） |
| 槽宽 | N/A | 单栏布局无槽宽概念 |
| 页面边距 | 48px | 四周边距 48px，确保内容不贴边 |
| 基线网格 | 8px | 与 spacing_system 基准对齐 |

**栅格系统说明**：
- 单栏布局是 Kami 纸感美学的核心——"阅读优先"意味着专注沉浸式阅读，不分散注意力
- 列宽 65ch（约 620px）是排版学的最佳行长，确保每行字符数在 45-75 的最佳阅读区间
- 65ch 使用 CSS 的 ch 单位，自动适应当前字体的字符宽度，确保不同字体下的最佳行长
- 页面边距 48px 营造高级出版物的留白感，避免内容贴边的廉价感

### 1.10 radius_shadow

```yaml
radius_shadow:
  border_radius: "2px"    # 圆角 2px — 微妙圆角
  box_shadow: "0 1px 3px rgba(61,53,34,0.08)"  # 轻微纸感阴影
```

| 元素类型 | 圆角值 | 阴影值 | 说明 |
|---------|--------|--------|------|
| 卡片/Card | 2px | 0 1px 3px rgba(61,53,34,0.08) | 微妙圆角 + 轻微纸感阴影，模拟纸张的物理质感 |
| 图片/Image | 2px | 0 1px 3px rgba(61,53,34,0.08) | 图片微妙圆角 + 轻微阴影，营造纸张上的图片质感 |
| 引用块/Quote | 2px | 0 1px 3px rgba(61,53,34,0.08) | 引用块微妙圆角 + 轻微阴影 |
| 按钮/Button | 2px | 0 1px 3px rgba(61,53,34,0.08) | 按钮微妙圆角 + 轻微阴影 |
| 表格/Table | 2px | 0 1px 3px rgba(61,53,34,0.08) | 表格微妙圆角 + 轻微阴影 |

**圆角阴影说明**：
- 圆角 2px 是 Kami 纸感美学的独特特征——微妙的圆角模拟纸张的柔和边缘，而非印刷级的绝对直角
- 阴影 `0 1px 3px rgba(61,53,34,0.08)` 是轻微的纸感阴影，模拟纸张在桌面上的微妙投影
- 阴影颜色使用 rgba(61,53,34,0.08)——基于深棕色 #3D3522 的 8% 透明度，与整体配色和谐统一
- 阴影极其轻微（0.08 透明度），不喧宾夺主，仅提供微妙的层次感
- 这是本 DLP 与 DLP-economist/DLP-newyorker（0px 圆角 + none 阴影）的关键差异——纸感美学需要微妙的物理质感

### 1.11 motion_curve

```yaml
motion_curve:
  page_transition: "ease-out 300ms"    # 页面过渡
```

| 动效场景 | 缓动曲线 | 时长 | 说明 |
|---------|---------|------|------|
| 页面过渡 | ease-out | 300ms | 页面切换的平滑过渡，模拟翻页的自然感 |
| 元素出现 | ease-out | 200ms | 元素的淡入出现，克制而自然 |
| 元素消失 | ease-in | 200ms | 元素的淡出消失 |
| 滚动 | N/A | N/A | 纸感美学不使用滚动动效，保持阅读的沉静感 |

**动效曲线说明**：
- 页面过渡使用 ease-out 300ms，模拟翻页的自然减速感
- 动效极其克制，仅用于页面过渡和元素出现/消失
- 禁止使用弹跳、旋转、缩放等装饰性动效，保持纸感阅读的沉静感
- 动效服务于阅读体验，而非炫技——这是纸感美学的动效哲学

### 1.12 applicable_scenarios

```yaml
applicable_scenarios:
  - "阅读体验"
  - "纸感美学"
  - "米色底调"
  - "衬线字体"
  - "高级出版物"
  - "散文"
  - "随笔"
```

| 场景标签 | 匹配优先级 | 典型用例 |
|---------|-----------|---------|
| 阅读体验 | 高 | 追求沉浸式阅读体验的长文、电子书 |
| 纸感美学 | 高 | 需要纸感质感的数字出版物 |
| 米色底调 | 高 | 使用米色/暖色底调的阅读场景 |
| 衬线字体 | 高 | 使用衬线字体的文学排版 |
| 高级出版物 | 中 | 高端杂志、文学刊物、艺术出版物 |
| 散文 | 中 | 散文、随笔、个人感悟类文章 |
| 随笔 | 中 | 随笔、日记、文学创作 |

---

## 二、Kami Skill 融入内容

> **融入来源技能**: Kami Skill
> **融入形式**: Kami 纸感美学五大特征完整融入本 DLP 的视觉规范

### 2.1 Kami 纸感美学五大特征

本 DLP 完整融入 Kami Skill 定义的纸感美学五大特征：

| 特征编号 | 特征名称 | 融入字段 | 融入说明 |
|---------|---------|---------|---------|
| KAMI-FEATURE-01 | 米色底调 | color_palette.background (#F5F0E6) | 米色纸感底调是 Kami 美学的核心特征，模拟真实纸张的温暖色调 |
| KAMI-FEATURE-02 | 衬线字体 | font_stack.western (EB Garamond) | EB Garamond 衬线字体传达古典书籍的质感，是纸感美学的字体选择 |
| KAMI-FEATURE-03 | 高级出版物级阅读质感 | typography_scale + font_weight_pairing | regular 字重 + 1.8 行高 + 16px 正文，营造高级出版物的阅读质感 |
| KAMI-FEATURE-04 | 微妙的纸感阴影 | radius_shadow.box_shadow | 0 1px 3px rgba(61,53,34,0.08) 轻微阴影，模拟纸张的物理质感 |
| KAMI-FEATURE-05 | 阅读优先的单栏布局 | grid_system.columns (1 栏) + column_width (65ch) | 单栏 65ch 列宽，专注沉浸式阅读体验 |

### 2.2 Kami Skill 方法论融入

```yaml
kami_skill_integration:
  source_skill: "Kami Skill"
  integration_points:
    - point: "米色底调"
      field: "color_palette.background (#F5F0E6)"
      description: "米色纸感底调 #F5F0E6 是 Kami 美学的核心特征色，模拟真实纸张的温暖色调，避免纯白背景的刺眼感"
    - point: "衬线字体"
      field: "font_stack.western (EB Garamond)"
      description: "EB Garamond 衬线字体基于 16 世纪 Garamond 设计，传达古典书籍的质感，是纸感美学的首选字体"
    - point: "高级出版物级阅读质感"
      field: "typography_scale (regular 字重 + 1.8 行高) + font_weight_pairing (全 regular)"
      description: "所有层级使用 regular 字重，正文行高 1.8，营造高级出版物的温和优雅阅读质感"
    - point: "微妙的纸感阴影"
      field: "radius_shadow.box_shadow (0 1px 3px rgba(61,53,34,0.08))"
      description: "轻微纸感阴影模拟纸张在桌面上的微妙投影，阴影颜色基于深棕色 #3D3522 的 8% 透明度"
    - point: "阅读优先的单栏布局"
      field: "grid_system.columns (1 栏) + column_width (65ch)"
      description: "单栏 65ch 列宽，专注沉浸式阅读体验，65ch 是排版学的最佳行长"
```

---

## 三、DLP 检索对接规范

### 3.1 检索命中条件

当以下语义信号出现时，DLP 检索器应优先匹配 `DLP-kami`：

1. **内容主题信号**: 散文、随笔、文学、阅读、纸感、美学、个人感悟、日记
2. **任务类型信号**: wechat_article（公众号长文）、文学类输出
3. **受众信号**: general（大众读者）、literary（文学读者）
4. **排版需求信号**: 阅读优先、纸感美学、米色底调、衬线字体、单栏布局

### 3.2 design_tokens 输出

```yaml
design_tokens:
  color_scheme:
    primary: "#3D3522"
    secondary: "#8B7355"
    accent: "#A0522D"
    neutral: "#C4B998"
    background: "#F5F0E6"
    text: "#3D3522"
  font_scheme:
    heading_font: '"EB Garamond", "Crimson Text", "Georgia", serif'
    body_font: '"EB Garamond", "Crimson Text", "Georgia", serif'
    chinese_font: '"宋体", "SimSun", "Noto Serif SC", serif'
    monospace_font: '"Courier New", "Courier", monospace'
  typography:
    h1_size: "32px"
    h2_size: "24px"
    h3_size: "20px"
    h4_size: "16px"
    body_size: "16px"
    caption_size: "13px"
    footnote_size: "12px"
    heading_weight: 400
    body_weight: 400
    emphasis_weight: "italic 400"
    body_line_height: 1.8
  spacing:
    base: 8px
    scale: [8, 16, 24, 32, 48, 64]
  grid:
    columns: 1
    column_width: "65ch"
    gutter: "N/A"
    margin: "48px"
  visual:
    border_radius: "2px"
    box_shadow: "0 1px 3px rgba(61,53,34,0.08)"
  motion:
    page_transition: "ease-out 300ms"
```

### 3.3 与 visual_dna 的对接映射

| DLP 字段 | visual_dna 字段 | 映射规则 |
|---------|----------------|---------|
| `color_palette.background` | `--color-bg` | 米色纸感背景直接映射（核心特征色） |
| `color_palette.primary` | `--color-text` | 深棕色文字色直接映射 |
| `color_palette.accent` | `--color-accent` | 赭石色强调色直接映射 |
| `typography_scale.body` | `font_scheme.body_size` | 16px 正文字号直接映射 |
| `font_stack.western` | `font_scheme.body_font` | EB Garamond 字体栈直接注入 |
| `grid_system.column_width` | `grid_system.column_width` | 65ch 列宽直接映射 |
| `radius_shadow.box_shadow` | `visual.box_shadow` | 纸感阴影直接映射 |
| `motion_curve.page_transition` | `motion_profile.transition` | ease-out 300ms 直接映射 |

---

## 四、与 TA/LA 原子库的对接

### 4.1 TA 排版原子对接

| TA 原子 ID | 原子名称 | 对接用途 |
|-----------|---------|---------|
| TA-SCALE-001 | H1 字号阶梯 | 32px 文章主标题字号 |
| TA-SCALE-004 | H4 字号阶梯 | 16px 子节标题字号 |
| TA-WEIGHT-002 | 正文 regular 字重 | 400 字重用于正文 |
| TA-WEIGHT-004 | 标题 regular 字重 | 400 字重用于标题（纸感美学特色） |
| TA-WEIGHT-003 | 强调 italic 字重 | 400 italic 用于书名/外来词/散文情感表达 |
| TA-LINE-003 | 宽松行高 | 1.8 行高用于纸感阅读 |
| TA-PARA-001 | 段落间距 | 24px 段落间距用于散文排版 |
| TA-MIX-001 | 中英文间距 | 中英文混排时的间距控制 |

### 4.2 LA 布局原子对接

| LA 原子 ID | 原子名称 | 对接用途 |
|-----------|---------|---------|
| LA-GRID-001 | 单栏栅格 | 阅读优先的单栏布局 |
| LA-PAGE-002 | 文章页布局 | 纸感阅读的文章页整体布局 |
| LA-SPECIAL-001 | 首字下沉布局 | 散文/随笔的首字下沉布局 |

---

## 五、ASR 硬门合规说明

本 DLP 的视觉规范天然符合以下 ASR 硬门禁令：

| ASR 禁令编号 | 禁令内容 | 本 DLP 合规性 |
|-------------|---------|-------------|
| ASR-FONT-001 | 禁 Inter 作为 Premium 产出字体 | ✅ 使用 EB Garamond 衬线字体 |
| ASR-FONT-003 | 禁 Arial 作为正文字体 | ✅ 使用 EB Garamond 衬线字体 |
| ASR-COLOR-002 | 禁纯黑（#000000） | ✅ 使用 #3D3522 深棕色文字 |
| ASR-COLOR-003 | 禁纯白（#FFFFFF）作为大面积背景 | ✅ 使用 #F5F0E6 米色纸感背景 |
| ASR-LAYOUT-004 | 禁默认 Tailwind 间距阶梯 | ✅ 使用 8/16/24/32/48/64 自定义阶梯 |
| ASR-DECOR-003 | 禁阴影堆叠超过 3 层 | ✅ 仅 1 层轻微阴影（0.08 透明度） |
| ASR-DECOR-004 | 禁毛玻璃效果用于正文区域 | ✅ 无毛玻璃，仅轻微纸感阴影 |

---

## 六、与同族 DLP 的差异化对比

| 对比维度 | DLP-economist | DLP-newyorker | DLP-kami | 差异说明 |
|---------|--------------|---------------|----------|---------|
| 背景色 | #FDFDFD（纸白） | #FCFAF5（米白） | #F5F0E6（米色纸感） | Kami 背景最暖，纸感最强 |
| 文字色 | #1A1A1A（正文黑） | #1A1A1A（正文黑） | #3D3522（深棕） | Kami 使用深棕色，最柔和 |
| 字体 | Milo Serif | Caslon | EB Garamond | 不同的衬线字体传统 |
| 标题字重 | bold(700) | regular(400) | regular(400) | Economist 加粗，其余不加粗 |
| 栏数 | 4 栏 | 3 栏 | 1 栏 | Kami 单栏阅读优先 |
| 圆角 | 0px | 0px | 2px | Kami 独有微妙圆角 |
| 阴影 | none | none | 轻微纸感阴影 | Kami 独有纸感阴影 |
| 行高 | 1.5 | 1.6 | 1.8 | Kami 行高最宽松 |
| 适用场景 | 经济分析 | 文学评论 | 散文/随笔 | 不同的内容定位 |

---

> **DLP 元数据**
> - 创建时间: 2026-06-19
> - 族: publication-typesetting
> - 锚定: Kami 纸感美学设计
> - 融入技能: Kami Skill ✅
> - 字段完整性: 12/12 ✅
> - 配色锚定: 真实世界美学体系实测配色 ✅
> - 字体栈中文 fallback: 已包含 ✅
> - 融入内容标注: Kami Skill 五大特征已明确标注 ✅
