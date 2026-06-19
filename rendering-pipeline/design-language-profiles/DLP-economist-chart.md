<!-- 作者：阿洋 -->

# DLP-economist-chart 设计语言画像

> **族**: data-visualization
> **锚定**: The Economist 数据图表 2024
> **融入来源**: data-visualization-craft
> **索引**: 详见 `README.md` 获取 DLP 库完整清单与检索规范

---

## YAML frontmatter（12 字段完整定义）

```yaml
---
name: "DLP-economist-chart"
anchor: "The Economist 数据图表 2024"
family: "data-visualization"

color_palette:
  primary: "#E3120B"
  secondary: "#006BA6"
  accent: "#3D1308"
  neutral: "#6C757D"
  background: "#FDFDFD"
  text: "#1A1A1A"

typography_scale:
  h1: "14px/0.875rem"
  h2: "12px/0.75rem"
  h3: "N/A"
  h4: "N/A"
  body: "10px/0.625rem"
  caption: "9px/0.5625rem"
  footnote: "8px/0.5rem"

font_stack:
  western: '"Milo Serif", "Source Serif Pro", serif(标题)/"Helvetica Neue", "Arial", sans-serif(数据标签)'
  chinese: '"宋体", "SimSun", serif'
  monospace: '"Courier New", monospace'

font_weight_pairing:
  heading: "bold(700)"
  body: "regular(400)"
  emphasis: "regular(400)"

spacing_system:
  base: "2px"
  scale: "2/4/6/8/12/16px"

grid_system:
  columns: "N/A(图表)"
  column_width: "600x400px(图表区域)"
  gutter: "N/A"
  margin: "40px(左)/20px(右/上/下)"
  breakpoint: "N/A(印刷媒介)"

radius_shadow:
  radius: "0px"
  shadow: "none"

motion_curve:
  easing: "N/A(印刷媒介)"
  duration: "N/A"

applicable_scenarios:
  - "数据可视化"
  - "经济数据"
  - "新闻图表"
  - "统计图表"
  - "清晰克制"
---
```

---

## 1. name

`DLP-economist-chart`

## 2. anchor

`"The Economist 数据图表 2024"`

锚定《经济学人》杂志 2024 年度数据图表的视觉规范。The Economist 的数据图表以"清晰克制无冗余"著称，采用低饱和度专业色系，网格线极淡，数据标签直接标注于数据系列之上而非依赖图例，每张图表必含来源标注，标题左对齐加粗，是全球财经新闻数据可视化的标杆。

## 3. family

`data-visualization`

## 4. color_palette

| 色板角色 | 变量名 | 十六进制值 | 用途 |
|---------|--------|-----------|------|
| 主色 Primary | `--color-primary` | `#E3120B` | Economist 标志红，用于关键数据系列、标题强调、趋势高亮 |
| 辅色 Secondary | `--color-secondary` | `#006BA6` | 数据蓝，用于次要数据系列、对比基准线 |
| 强调色 Accent | `--color-accent` | `#3D1308` | 深红，用于负向数据、警示标注、深度强调 |
| 中性色 Neutral | `--color-neutral` | `#6C757D` | 辅助文字、轴线、刻度标签 |
| 背景色 Background | `--color-bg` | `#FDFDFD` | 纸白背景，模拟印刷质感 |
| 文本色 Text | `--color-text` | `#1A1A1A` | 标题、正文、数据标签 |

**数据系列色板**（按系列顺序循环使用）：

| 系列序号 | 十六进制值 | 典型用途 |
|---------|-----------|---------|
| 系列 1 | `#E3120B` | 主数据系列（Economist 红） |
| 系列 2 | `#006BA6` | 对比数据系列（数据蓝） |
| 系列 3 | `#3D1308` | 第三系列（深红） |
| 系列 4 | `#379A8B` | 第四系列（青绿） |
| 系列 5 | `#EBB26E` | 第五系列（暖橙） |
| 系列 6 | `#B4A4B4` | 第六系列（灰紫） |

**扩展语义色**：

| 变量名 | 十六进制值 | 用途 |
|--------|-----------|------|
| `--color-grid` | `#E5E5E5` | 网格线（极淡） |
| `--color-axis` | `#6C757D` | 坐标轴线 |
| `--color-source` | `#6C757D` | 来源标注文字 |
| `--color-annotation` | `#E3120B` | 数据标注线、注释箭头 |

## 5. typography_scale

| 层级 | 用途 | 字号 (px) | 字号 (rem) | 行高 | 字重 |
|------|------|----------|-----------|------|------|
| h1 | 图表标题 | 14px | 0.875rem | 1.3 | 700 |
| h2 | 副标题 | 12px | 0.75rem | 1.4 | 400 |
| body | 数据标签 | 10px | 0.625rem | 1.5 | 400 |
| caption | 图注 | 9px | 0.5625rem | 1.5 | 400 |
| footnote | 来源标注 | 8px | 0.5rem | 1.4 | 400 |

**字号使用规则**：
- 图表标题左对齐，加粗（700），14px
- 副标题紧跟标题下方，常规（400），12px，用于补充说明图表范围或时间区间
- 数据标签直接标注在数据系列上，10px，避免使用图例
- 来源标注位于图表左下角，8px，格式："Source: xxx"

## 6. font_stack

| 用途 | 西文字体栈 | CSS font-family |
|------|-----------|----------------|
| 标题 | Milo Serif, Source Serif Pro, serif | `"Milo Serif", "Source Serif Pro", serif` |
| 数据标签 | Helvetica Neue, Arial, sans-serif | `"Helvetica Neue", "Arial", sans-serif` |
| 中文 fallback | 宋体, SimSun, serif | `"宋体", "SimSun", serif` |
| 等宽 | Courier New, monospace | `"Courier New", monospace` |

**完整字体栈声明**：
```css
font-family: "Milo Serif", "Source Serif Pro", "宋体", "SimSun", serif; /* 标题 */
font-family: "Helvetica Neue", "Arial", "宋体", "SimSun", sans-serif; /* 数据标签 */
font-family: "Courier New", monospace; /* 等宽数值 */
```

## 7. font_weight_pairing

| 元素类型 | 字重 | 字重值 | 说明 |
|---------|------|--------|------|
| 图表标题 | bold | 700 | 左对齐加粗，建立视觉锚点 |
| 副标题 | regular | 400 | 辅助说明，不与标题争夺注意力 |
| 数据标签 | regular | 400 | 直接标注，清晰可读 |
| 刻度标签 | regular | 400 | 轴刻度数值 |
| 图注 | regular | 400 | 补充说明 |
| 来源标注 | regular | 400 | 左下角，弱化处理 |

**字重搭配原则**：仅标题使用 bold(700)，其余全部 regular(400)，通过字号差异而非字重差异建立层级。

## 8. spacing_system

**基准值**: 2px

| 间距阶梯 | 值 | 用途 |
|---------|-----|------|
| xs | 2px | 数据标签与数据点的间距、刻度标签与轴的间距 |
| sm | 4px | 标题与副标题间距、图注间距 |
| md | 6px | 数据系列间距、注释间距 |
| lg | 8px | 图表区域内边距、图例间距 |
| xl | 12px | 标题区块与图表区域的间距 |
| 2xl | 16px | 图表区域与来源标注的间距 |

## 9. grid_system

| 参数 | 值 | 说明 |
|------|-----|------|
| 图表区域默认尺寸 | 600x400px | 标准单图尺寸 |
| 左边距 | 40px | 预留 Y 轴标签空间 |
| 右边距 | 20px | 右侧留白 |
| 上边距 | 20px | 预留标题空间 |
| 下边距 | 20px | 预留 X 轴标签和来源空间 |
| 网格线 | 水平网格线仅 | 仅水平方向，极淡 #E5E5E5 |
| 网格线粗细 | 0.5px | 极细，不干扰数据阅读 |
| 坐标轴线 | 1px | #6C757D，仅 X 轴和 Y 轴 |

**栅格规则**：
- 仅保留水平网格线（横向参考线），删除垂直网格线
- 网格线颜色 #E5E5E5，粗细 0.5px，确保数据系列为视觉主体
- 坐标轴线 1px #6C757D，X 轴和 Y 轴均保留但弱化

## 10. radius_shadow

| 参数 | 值 | 说明 |
|------|-----|------|
| 圆角 | 0px | 所有元素直角，模拟印刷质感 |
| 阴影 | none | 无阴影，平面化呈现 |

**设计意图**：Economist 数据图表追求印刷级平面质感，拒绝任何圆角和阴影装饰，确保数据本身是唯一的视觉焦点。

## 11. motion_curve

| 参数 | 值 | 说明 |
|------|-----|------|
| 动效 | N/A(印刷媒介) | 静态图表，无动效 |

**说明**：Economist 数据图表定位为静态印刷级图表，所有输出为静态图片，不包含任何动效。动效字段标记为 N/A(印刷媒介)。

## 12. applicable_scenarios

```json
["数据可视化", "经济数据", "新闻图表", "统计图表", "清晰克制"]
```

**场景匹配权重**：
- 经济数据 / 财经新闻图表 → 权重 1.0（最佳匹配）
- 统计图表 / 数据分析报告 → 权重 0.9
- 政策解读 / 宏观经济趋势 → 权重 0.85
- 商业报告数据图 → 权重 0.8

---

## 融入内容：data-visualization-craft

> **来源技能**: data-visualization-craft
> **融入形式**: 经济学人级数据图特征规范

### 经济学人级数据图核心特征

1. **清晰克制无冗余**：移除一切非数据装饰元素——无图表边框、无背景填充、无 3D 效果、无渐变填充。图表中唯一存在的视觉元素是数据本身和必要的参考结构（轴线、网格线、标签）。

2. **低饱和度专业色系**：主色 #E3120B（Economist 标志红）用于关键数据系列，辅色 #006BA6（数据蓝）用于对比系列。所有颜色饱和度控制在 60%-75% 区间，避免高饱和度的"塑料感"。

3. **网格线极淡**：水平网格线使用 #E5E5E5（接近背景色），粗细 0.5px，仅作为数据阅读的辅助参考线，不干扰数据系列的视觉主体地位。垂直网格线完全删除。

4. **数据标签直接标注**：数据系列标签直接标注在数据系列末端或上方，而非使用独立图例。这减少了眼睛在图例和数据之间来回跳转的认知负担。当系列超过 4 个时，才使用简洁的行内图例。

5. **来源标注必填**：每张图表左下角必须标注数据来源，格式为 "Source: xxx"，字号 8px，颜色 #6C757D。这是 Economist 数据图表的强制规范，确保数据可追溯。

6. **图表标题左对齐加粗**：标题位于图表左上角，左对齐，加粗（700），14px。副标题紧跟其下，常规（400），12px，用于补充说明时间范围或数据口径。

### 数据系列配色使用规则

| 数据系列数量 | 配色策略 |
|-------------|---------|
| 1 个系列 | 使用主色 #E3120B |
| 2 个系列 | 主色 #E3120B + 辅色 #006BA6 |
| 3 个系列 | 主色 + 辅色 + 强调色 #3D1308 |
| 4-6 个系列 | 按数据系列色板顺序循环 |
| >6 个系列 | 合并次要系列为"其他"，控制在 6 个以内 |

### 禁止事项

- 禁止 3D 图表（3D 饼图、3D 柱状图）
- 禁止渐变填充
- 禁止图表边框
- 禁止背景色填充（除背景色 #FDFDFD 外）
- 禁止图例遮挡数据
- 禁止无来源标注的图表
- 禁止彩虹色板用于顺序数据

---

## 与 visual_dna 的对接映射

### 配色注入映射

| DLP color_palette | visual_dna.color_scheme | 映射规则 |
|-------------------|------------------------|---------|
| `primary: #E3120B` | `--color-primary` | Economist 标志红/关键数据系列/标题强调 |
| `secondary: #006BA6` | `--color-secondary` | 数据蓝/次要数据系列/对比基准线 |
| `accent: #3D1308` | `--color-accent` | 深红/负向数据/警示标注 |
| `neutral: #6C757D` | `--color-text-secondary` | 辅助文字/轴线/刻度标签 |
| `background: #FDFDFD` | `--color-bg` | 纸白背景/印刷质感 |
| `text: #1A1A1A` | `--color-text` | 标题/正文/数据标签 |

### 字体注入映射

| DLP font_stack | visual_dna.font_scheme | 映射规则 |
|----------------|----------------------|---------|
| `标题: "Milo Serif", "Source Serif Pro", serif` | 标题字体族（西文衬线） | 首选 Milo Serif，Source Serif Pro fallback |
| `数据标签: "Helvetica Neue", "Arial", sans-serif` | 数据标签字体族（西文无衬线）+ 中文 fallback 宋体 | 数据标签首选 Helvetica Neue，中文 fallback 宋体 |
| `等宽: "Courier New", monospace` | 代码字体族 | 等宽数值字体 |

### 图形规范注入映射

| DLP 字段 | visual_dna 字段 | 映射规则 |
|---------|----------------|---------|
| `grid_system: 600x400px, 水平网格线 #E5E5E5` | `grid_system` | 仅水平网格线直接继承 |
| `spacing_system: 2px 基准` | `line_style` | 间距阶梯直接继承 |
| `radius_shadow: 0px/none` | `line_style` | 强制直角零阴影 |
| `motion_curve: N/A(印刷媒介)` | `motion_profile` | 禁用动效 |
