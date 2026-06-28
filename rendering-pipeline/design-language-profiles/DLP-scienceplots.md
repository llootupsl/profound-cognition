<!-- 作者：阿洋 -->

# DLP-scienceplots 设计语言画像

> **族**: data-visualization
> **锚定**: SciencePlots Matplotlib 样式库
> **融入来源**: SciencePlots
> **索引**: 详见 `README.md` 获取 DLP 库完整清单与检索规范

---

## YAML frontmatter（12 字段完整定义）

```yaml
---
name: "DLP-scienceplots"
anchor: "SciencePlots Matplotlib 样式库"
family: "data-visualization"

color_palette:
  primary: "#0C5DA5"
  secondary: "#FF2C00"
  accent: "#00B945"
  neutral: "#6C757D"
  background: "#FFFFFF"
  text: "#1A1A1A"

typography_scale:
  h1: "12px/0.75rem"
  h2: "11px/0.6875rem"
  h3: "N/A"
  h4: "N/A"
  body: "10px/0.625rem"
  caption: "9px/0.5625rem"
  footnote: "N/A"

font_stack:
  western: '"Times New Roman", "Times", serif'
  chinese: '"宋体", "SimSun", serif'
  monospace: '"Courier New", monospace'

font_weight_pairing:
  heading: "regular(400)"
  body: "regular(400)"
  emphasis: "regular(400)"

spacing_system:
  base: "2px"
  scale: "2/4/6/8/12px"

grid_system:
  columns: "N/A(图表)"
  column_width: "640x480px(图表区域)"
  gutter: "N/A"
  margin: "50px(左)/30px(右/上/下)"
  breakpoint: "N/A(印刷媒介)"

radius_shadow:
  radius: "0px"
  shadow: "none"

motion_curve:
  easing: "N/A(印刷媒介)"
  duration: "N/A"

applicable_scenarios:
  - "学术论文配图"
  - "Matplotlib"
  - "科学绘图"
  - "顶刊配色"
  - "矢量图"
---
```

---

## 1. name

`DLP-scienceplots`

## 2. anchor

`"SciencePlots Matplotlib 样式库"`

锚定 SciencePlots——Matplotlib 官方级科学绘图样式库。SciencePlots 提供了符合顶刊投稿规范的 Matplotlib 样式表，包括 Nature、Science、IEEE 等期刊的配色、线宽、字体规范。其核心特征是 Times New Roman 衬线字体、顶刊正版配色线宽、淡灰网格线、细轴线、无边框图例，并支持 LaTeX 公式渲染，是学术圈最广泛使用的 Matplotlib 样式库之一。

## 3. family

`data-visualization`

## 4. color_palette

| 色板角色 | 变量名 | 十六进制值 | 用途 |
|---------|--------|-----------|------|
| 主色 Primary | `--color-primary` | `#0C5DA5` | 科学蓝，用于主数据系列、关键曲线 |
| 辅色 Secondary | `--color-secondary` | `#FF2C00` | 科学红，用于对比数据系列、高亮曲线 |
| 强调色 Accent | `--color-accent` | `#00B945` | 科学绿，用于第三数据系列、正向结果 |
| 中性色 Neutral | `--color-neutral` | `#6C757D` | 辅助文字、轴线、刻度标签 |
| 背景色 Background | `--color-bg` | `#FFFFFF` | 纯白背景，适合论文印刷 |
| 文本色 Text | `--color-text` | `#1A1A1A` | 标题、标签、图例文字 |

**数据系列色板**（SciencePlots 默认配色，按系列顺序循环）：

| 系列序号 | 十六进制值 | 典型用途 |
|---------|-----------|---------|
| 系列 1 | `#0C5DA5` | 主数据系列（科学蓝） |
| 系列 2 | `#FF2C00` | 对比数据系列（科学红） |
| 系列 3 | `#00B945` | 第三系列（科学绿） |
| 系列 4 | `#FF9500` | 第四系列（科学橙） |
| 系列 5 | `#845B97` | 第五系列（科学紫） |
| 系列 6 | `#474747` | 第六系列（深灰） |

**扩展语义色**：

| 变量名 | 十六进制值 | 用途 |
|--------|-----------|------|
| `--color-grid` | `#CCCCCC` | 网格线（淡灰） |
| `--color-axis` | `#1A1A1A` | 坐标轴线（黑色） |
| `--color-spine` | `#1A1A1A` | 图表边框（黑色） |
| `--color-errorbar` | `#6C757D` | 误差棒 |

## 5. typography_scale

| 层级 | 用途 | 字号 (px) | 字号 (rem) | 行高 | 字重 |
|------|------|----------|-----------|------|------|
| h1 | 图表标题 | 12px | 0.75rem | 1.3 | 400 |
| h2 | 轴标题 | 11px | 0.6875rem | 1.4 | 400 |
| body | 刻度标签 | 10px | 0.625rem | 1.5 | 400 |
| caption | 图注 | 9px | 0.5625rem | 1.5 | 400 |

**字号使用规则**：
- 图表标题居中或左对齐，常规（400），12px
- 轴标题（X 轴/Y 轴标题）常规（400），11px
- 刻度标签常规（400），10px，紧贴轴线
- 图注位于图表下方，常规（400），9px

## 6. font_stack

| 用途 | 西文字体栈 | CSS font-family |
|------|-----------|----------------|
| 学术图表 | Times New Roman, Times, serif | `"Times New Roman", "Times", serif` |
| 中文 fallback | 宋体, SimSun, serif | `"宋体", "SimSun", serif` |
| 等宽 | Courier New, monospace | `"Courier New", monospace` |

**完整字体栈声明**：
```css
font-family: "Times New Roman", "Times", "宋体", "SimSun", serif; /* 学术图表全局 */
font-family: "Courier New", monospace; /* 等宽数值 */
```

**LaTeX 渲染模式**：
当启用 LaTeX 公式渲染时，使用 `mathtext` 或 `usetex=True`：
- `mathtext`：Matplotlib 内置数学公式渲染，字体默认为 Computer Modern
- `usetex=True`：调用系统 LaTeX 引擎，完整 LaTeX 语法支持

## 7. font_weight_pairing

| 元素类型 | 字重 | 字重值 | 说明 |
|---------|------|--------|------|
| 图表标题 | regular | 400 | 学术图表标题不加粗，保持克制 |
| 轴标题 | regular | 400 | X/Y 轴标题 |
| 刻度标签 | regular | 400 | 轴刻度数值 |
| 图例 | regular | 400 | 图例文字 |
| 图注 | regular | 400 | 图表说明 |

**字重搭配原则**：SciencePlots 全局使用 regular(400)，不使用加粗。学术图表通过字号差异和字体族（Times New Roman 衬线）建立层级，而非字重差异。这符合顶刊配图规范——克制、专业、不喧宾夺主。

## 8. spacing_system

**基准值**: 2px

| 间距阶梯 | 值 | 用途 |
|---------|-----|------|
| xs | 2px | 刻度标签与轴的间距、图例项间距 |
| sm | 4px | 轴标题与刻度标签的间距 |
| md | 6px | 图表标题与图表区域的间距 |
| lg | 8px | 图例与图表边缘的间距 |
| xl | 12px | 图表区域与图注的间距 |

## 9. grid_system

| 参数 | 值 | 说明 |
|------|-----|------|
| 图表区域默认尺寸 | 640x480px | Matplotlib 默认 6.4x4.8 英寸 @100dpi |
| 左边距 | 50px | 预留 Y 轴标签空间 |
| 右边距 | 30px | 右侧留白 |
| 上边距 | 30px | 预留标题空间 |
| 下边距 | 30px | 预留 X 轴标签空间 |
| 网格线 | 水平+垂直 | 双向网格线，淡灰 #CCCCCC |
| 网格线粗细 | 0.5px | 极细，不干扰数据阅读 |
| 网格线样式 | 虚线 | dasharray: 2,2 |
| 坐标轴线 | 0.5pt | #1A1A1A，细轴线 |

**栅格规则**：
- 水平和垂直网格线均保留，颜色 #CCCCCC，粗细 0.5px，虚线样式
- 坐标轴线 0.5pt（约 0.67px），黑色 #1A1A1A，符合顶刊细轴线规范
- 图表边框（spine）四边均保留，0.5pt 黑色

## 10. radius_shadow

| 参数 | 值 | 说明 |
|------|-----|------|
| 圆角 | 0px | 所有元素直角，学术规范 |
| 阴影 | none | 无阴影，平面化呈现 |

**设计意图**：SciencePlots 追求学术出版的严谨平面质感，拒绝任何圆角和阴影装饰，确保图表可直接用于论文投稿。

## 11. motion_curve

| 参数 | 值 | 说明 |
|------|-----|------|
| 动效 | N/A(印刷媒介) | 静态图表，无动效 |

**说明**：SciencePlots 定位为静态学术图表生成库，所有输出为静态图片（PNG/PDF/SVG），不包含任何动效。动效字段标记为 N/A(印刷媒介)。

## 12. applicable_scenarios

```json
["学术论文配图", "Matplotlib", "科学绘图", "顶刊配色", "矢量图"]
```

**场景匹配权重**：
- 学术论文配图（Nature/Science/IEEE 投稿） → 权重 1.0（最佳匹配）
- Matplotlib 科学绘图 → 权重 1.0
- 顶刊正版配色线宽需求 → 权重 0.95
- 矢量图输出（PDF/SVG） → 权重 0.9
- LaTeX 公式渲染需求 → 权重 0.85

---

## 融入内容：SciencePlots

> **来源技能**: SciencePlots
> **融入形式**: Matplotlib 官方级样式特征规范

### SciencePlots 核心特征

1. **顶刊正版配色线宽**：SciencePlots 提供了 Nature、Science、IEEE 等顶刊的正版配色方案和线宽规范。配色采用低饱和度专业色系（科学蓝 #0C5DA5、科学红 #FF2C00、科学绿 #00B945），线宽统一为 1.5pt（约 2px），确保图表在印刷和屏幕上均清晰可辨。

2. **Times New Roman 字体**：全局使用 Times New Roman 衬线字体，这是学术论文配图的标准字体。Times New Roman 在印刷品中具有最佳的 readability 和 professionalism 平衡，是 Nature、Science 等顶刊的指定字体之一。

3. **网格线淡灰**：网格线使用 #CCCCCC（淡灰），粗细 0.5px，虚线样式（dasharray: 2,2）。网格线作为数据阅读的辅助参考，不干扰数据系列的视觉主体地位。水平和垂直网格线均保留，便于精确读取数值。

4. **轴线细**：坐标轴线粗细 0.5pt（约 0.67px），黑色 #1A1A1A。细轴线是顶刊配图的标志特征，与粗轴线相比，细轴线更克制、更专业，不与数据系列争夺视觉注意力。

5. **图例无边框**：图例不显示边框（frameon=False），仅显示图例文字和颜色标记。无边框图例更简洁，减少视觉噪音，符合学术图表的克制美学。

6. **支持 LaTeX 公式渲染**：SciencePlots 完整支持 LaTeX 公式渲染，可通过 `mathtext` 或 `usetex=True` 在图表标题、轴标签、图例中插入复杂的数学公式。这是科学绘图的核心需求，确保公式排版与正文一致。

### SciencePlots 样式表映射

| 样式表名 | 适用场景 | 配色特征 |
|---------|---------|---------|
| `science` | 通用科学绘图 | 科学蓝/红/绿六色板 |
| `nature` | Nature 期刊投稿 | 科学蓝/红/绿 + 细轴线 |
| `scienceieee` | IEEE 期刊投稿 | 科学蓝/红/绿 + IEEE 双栏适配 |
| `scatter` | 散点图专用 | 透明度 0.7 + 边缘色 |
| `highvis` | 高对比度需求 | 高饱和度配色 |

### 线宽规范

| 元素 | 线宽 | 说明 |
|------|------|------|
| 数据线（折线/曲线） | 1.5pt (2px) | 主数据系列 |
| 坐标轴线 | 0.5pt (0.67px) | 细轴线 |
| 网格线 | 0.5pt (0.67px) | 淡灰虚线 |
| 图例边框 | 0pt | 无边框 |
| 误差棒 | 1.0pt (1.33px) | 误差范围 |

### 禁止事项

- 禁止使用默认 Matplotlib 配色（`tab:blue`, `tab:orange` 等）
- 禁止使用粗轴线（>1pt）
- 禁止图例有边框
- 禁止使用无衬线字体作为主字体
- 禁止使用 3D 效果
- 禁止使用渐变填充

---

## 与 visual_dna 的对接映射

### 配色注入映射

| DLP color_palette | visual_dna.color_scheme | 映射规则 |
|-------------------|------------------------|---------|
| `primary: #0C5DA5` | `--color-primary` | 科学蓝/主数据系列/关键曲线 |
| `secondary: #FF2C00` | `--color-secondary` | 科学红/对比数据系列/高亮曲线 |
| `accent: #00B945` | `--color-accent` | 科学绿/第三数据系列/正向结果 |
| `neutral: #6C757D` | `--color-text-secondary` | 辅助文字/轴线/刻度标签 |
| `background: #FFFFFF` | `--color-bg` | 纯白背景/论文印刷 |
| `text: #1A1A1A` | `--color-text` | 标题/标签/图例文字 |

### 字体注入映射

| DLP font_stack | visual_dna.font_scheme | 映射规则 |
|----------------|----------------------|---------|
| `学术图表: "Times New Roman", "Times", serif` | 标题/正文字体族（西文衬线） | 首选 Times New Roman，Times fallback |
| `中文 fallback: "宋体", "SimSun", serif` | 标题/正文字体族（中文） | 中文 fallback 宋体 |
| `等宽: "Courier New", monospace` | 代码字体族 | 等宽数值字体 |

### 图形规范注入映射

| DLP 字段 | visual_dna 字段 | 映射规则 |
|---------|----------------|---------|
| `grid_system: 640x480px, 双向网格线 #CCCCCC` | `grid_system` | 双向网格线直接继承 |
| `spacing_system: 2px 基准` | `line_style` | 间距阶梯直接继承 |
| `radius_shadow: 0px/none` | `line_style` | 强制直角零阴影 |
| `motion_curve: N/A(印刷媒介)` | `motion_profile` | 禁用动效 |
