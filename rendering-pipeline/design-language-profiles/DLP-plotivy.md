<!-- 作者：阿洋 -->

# DLP-plotivy 设计语言画像

> **族**: data-visualization
> **锚定**: Plotivy 全期刊规范匹配系统
> **融入来源**: Plotivy
> **索引**: 详见 `README.md` 获取 DLP 库完整清单与检索规范

---

## YAML frontmatter（12 字段完整定义）

```yaml
---
name: "DLP-plotivy"
anchor: "Plotivy 全期刊规范匹配系统"
family: "data-visualization"

color_palette:
  primary: "#2E5C8A"
  secondary: "#C0392B"
  accent: "#27AE60"
  neutral: "#7F8C8D"
  background: "#FFFFFF"
  text: "#2C3E50"

typography_scale:
  h1: "12px/0.75rem"
  h2: "11px/0.6875rem"
  h3: "N/A"
  h4: "N/A"
  body: "10px/0.625rem"
  caption: "9px/0.5625rem"
  footnote: "N/A"

font_stack:
  western: '"Computer Modern", "Times New Roman", serif'
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
  column_width: "600x400px(图表区域)"
  gutter: "N/A"
  margin: "45px(左)/25px(右/上/下)"
  breakpoint: "N/A(印刷媒介)"

radius_shadow:
  radius: "0px"
  shadow: "none"

motion_curve:
  easing: "N/A(印刷媒介)"
  duration: "N/A"

applicable_scenarios:
  - "期刊配图"
  - "自动校准"
  - "出版级参数"
  - "多期刊兼容"
  - "LaTeX渲染"
---
```

---

## 1. name

`DLP-plotivy`

## 2. anchor

`"Plotivy 全期刊规范匹配系统"`

锚定 Plotivy——全期刊规范匹配系统。Plotivy 能够自动校准出版级参数（字号/线宽/边距），支持 Nature、Science、IEEE、Springer 等多期刊规范匹配，内置 LaTeX 公式渲染和矢量图输出能力，并提供颜色盲友好色板。其核心价值是"一次绘图，多期刊兼容"——研究者无需为不同期刊重新调整图表参数，Plotivy 自动适配目标期刊的配图规范。

## 3. family

`data-visualization`

## 4. color_palette

| 色板角色 | 变量名 | 十六进制值 | 用途 |
|---------|--------|-----------|------|
| 主色 Primary | `--color-primary` | `#2E5C8A` | 通用期刊蓝，用于主数据系列、关键曲线 |
| 辅色 Secondary | `--color-secondary` | `#C0392B` | 期刊红，用于对比数据系列、高亮曲线 |
| 强调色 Accent | `--color-accent` | `#27AE60` | 期刊绿，用于第三数据系列、正向结果 |
| 中性色 Neutral | `--color-neutral` | `#7F8C8D` | 辅助文字、轴线、刻度标签 |
| 背景色 Background | `--color-bg` | `#FFFFFF` | 纯白背景，出版标准 |
| 文本色 Text | `--color-text` | `#2C3E50` | 标题、标签、图例文字（深蓝灰） |

**数据系列色板**（Plotivy 默认颜色盲友好色板）：

| 系列序号 | 十六进制值 | 典型用途 |
|---------|-----------|---------|
| 系列 1 | `#2E5C8A` | 主数据系列（通用期刊蓝） |
| 系列 2 | `#C0392B` | 对比数据系列（期刊红） |
| 系列 3 | `#27AE60` | 第三系列（期刊绿） |
| 系列 4 | `#F39C12` | 第四系列（期刊橙） |
| 系列 5 | `#8E44AD` | 第五系列（期刊紫） |
| 系列 6 | `#16A085` | 第六系列（期刊青） |

**扩展语义色**：

| 变量名 | 十六进制值 | 用途 |
|--------|-----------|------|
| `--color-grid` | `#D5D8DC` | 网格线（淡灰） |
| `--color-axis` | `#2C3E50` | 坐标轴线（深蓝灰） |
| `--color-spine` | `#2C3E50` | 图表边框（深蓝灰） |
| `--color-errorbar` | `#7F8C8D` | 误差棒 |
| `--color-confidence` | `#85C1E9` | 置信区间填充（浅蓝） |

**颜色盲友好说明**：以上色板基于 Wong's color palette 优化，通过红绿色盲（protanopia/deuteranopia）、蓝黄色盲（tritanopia）和全色盲（monochromacy）模拟测试，在所有色盲模式下均可区分。Plotivy 的颜色盲友好色板是其核心特性之一，确保图表在所有读者面前均清晰可辨。

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

**自动校准说明**：以上字号为默认值，Plotivy 会根据目标期刊规范自动校准。例如：
- Nature 期刊：字号缩小至 7-8pt（约 9.33-10.67px）
- IEEE 期刊：字号保持 10-12px
- Science 期刊：字号缩小至 7-9pt（约 9.33-12px）

## 6. font_stack

| 用途 | 西文字体栈 | CSS font-family |
|------|-----------|----------------|
| 学术图表 | Computer Modern, Times New Roman, serif | `"Computer Modern", "Times New Roman", serif` |
| 中文 fallback | 宋体, SimSun, serif | `"宋体", "SimSun", serif` |
| 等宽 | Courier New, monospace | `"Courier New", monospace` |

**完整字体栈声明**：
```css
font-family: "Computer Modern", "Times New Roman", "宋体", "SimSun", serif; /* 学术图表全局 */
font-family: "Courier New", monospace; /* 等宽数值 */
```

**字体自动切换说明**：Plotivy 根据目标期刊自动切换字体：
- Nature/Science：切换为 Arial/Helvetica 无衬线字体
- IEEE/Springer：保持 Computer Modern/Times New Roman 衬线字体
- 通用模式：使用 Computer Modern（LaTeX 默认字体）

## 7. font_weight_pairing

| 元素类型 | 字重 | 字重值 | 说明 |
|---------|------|--------|------|
| 图表标题 | regular | 400 | 学术图表标题不加粗 |
| 轴标题 | regular | 400 | X/Y 轴标题 |
| 刻度标签 | regular | 400 | 轴刻度数值 |
| 图例 | regular | 400 | 图例文字 |
| 图注 | regular | 400 | 图表说明 |

**字重搭配原则**：Plotivy 全局使用 regular(400)，不使用加粗。学术图表通过字号差异和字体族建立层级，而非字重差异。这符合多期刊兼容的通用规范——不同期刊对字重的偏好不同，regular 是最安全的通用选择。

## 8. spacing_system

**基准值**: 2px

| 间距阶梯 | 值 | 用途 |
|---------|-----|------|
| xs | 2px | 刻度标签与轴的间距、图例项间距 |
| sm | 4px | 轴标题与刻度标签的间距 |
| md | 6px | 图表标题与图表区域的间距 |
| lg | 8px | 图例与图表边缘的间距 |
| xl | 12px | 图表区域与图注的间距 |

**自动校准说明**：以上间距为默认值，Plotivy 会根据目标期刊规范自动校准。例如：
- Nature 期刊：间距缩小至 1-2px（紧凑布局）
- IEEE 期刊：间距保持 2-4px
- Springer 期刊：间距增大至 3-6px（宽松布局）

## 9. grid_system

| 参数 | 值 | 说明 |
|------|-----|------|
| 图表区域默认尺寸 | 600x400px | 标准单图尺寸 |
| 左边距 | 45px | 预留 Y 轴标签空间 |
| 右边距 | 25px | 右侧留白 |
| 上边距 | 25px | 预留标题空间 |
| 下边距 | 25px | 预留 X 轴标签空间 |
| 网格线 | 水平+垂直 | 双向网格线，淡灰 #D5D8DC |
| 网格线粗细 | 0.5px | 极细，不干扰数据阅读 |
| 网格线样式 | 实线 | 实线网格 |
| 坐标轴线 | 0.75pt | #2C3E50，深蓝灰细轴线 |

**栅格规则**：
- 水平和垂直网格线均保留，颜色 #D5D8DC，粗细 0.5px，实线样式
- 坐标轴线 0.75pt（约 1px），深蓝灰 #2C3E50
- 图表边框（spine）四边均保留，0.75pt 深蓝灰

**自动校准说明**：以上栅格参数为默认值，Plotivy 会根据目标期刊规范自动校准。例如：
- Nature 期刊：边距缩小至 5mm，网格线可选
- IEEE 期刊：边距保持 45/25px，网格线保留
- Science 期刊：边距缩小至 4mm，网格线极淡

## 10. radius_shadow

| 参数 | 值 | 说明 |
|------|-----|------|
| 圆角 | 0px | 所有元素直角，出版规范 |
| 阴影 | none | 无阴影，平面化呈现 |

**设计意图**：Plotivy 追求出版级平面质感，拒绝任何圆角和阴影装饰，确保图表可直接用于多期刊投稿。

## 11. motion_curve

| 参数 | 值 | 说明 |
|------|-----|------|
| 动效 | N/A(印刷媒介) | 静态图表，无动效 |

**说明**：Plotivy 定位为静态学术出版配图生成系统，所有输出为静态矢量图（SVG/PDF）或高分辨率位图（PNG/TIFF @300dpi+），不包含任何动效。动效字段标记为 N/A(印刷媒介)。

## 12. applicable_scenarios

```json
["期刊配图", "自动校准", "出版级参数", "多期刊兼容", "LaTeX渲染"]
```

**场景匹配权重**：
- 期刊配图（多期刊兼容需求） → 权重 1.0（最佳匹配）
- 自动校准出版级参数 → 权重 1.0
- 出版级参数需求（字号/线宽/边距） → 权重 0.95
- LaTeX 公式渲染需求 → 权重 0.9
- 多期刊投稿（Nature/Science/IEEE/Springer） → 权重 0.9

---

## 融入内容：Plotivy

> **来源技能**: Plotivy
> **融入形式**: 全期刊规范匹配特征规范

### Plotivy 核心特征

1. **自动校准出版级参数（字号/线宽/边距）**：Plotivy 的核心能力是自动校准图表的出版级参数。研究者只需绘制一次图表，Plotivy 根据目标期刊规范自动调整字号、线宽、边距、分辨率等参数，确保图表符合目标期刊的投稿要求。这消除了为不同期刊重新调整图表参数的重复劳动。

2. **支持 Nature/Science/IEEE/Springer 多期刊规范**：Plotivy 内置了主流学术期刊的配图规范数据库：

| 期刊 | 字号规范 | 线宽规范 | 边距规范 | 字体规范 |
|------|---------|---------|---------|---------|
| Nature | 7-8pt | 0.5-0.75pt | 5mm | Arial |
| Science | 7-9pt | 0.5-1.0pt | 4mm | Arial |
| IEEE | 10-12px | 1.0-1.5pt | 45/25px | Times New Roman |
| Springer | 8-10pt | 0.75-1.0pt | 6mm | Computer Modern |

3. **LaTeX 公式渲染**：Plotivy 完整支持 LaTeX 公式渲染，可在图表标题、轴标签、图例中插入复杂的数学公式。LaTeX 渲染确保公式排版与正文一致，是学术出版的核心需求。Plotivy 支持两种 LaTeX 渲染模式：
   - `mathtext`：轻量级数学公式渲染，无需系统 LaTeX 环境
   - `usetex=True`：完整 LaTeX 引擎渲染，支持所有 LaTeX 语法

4. **矢量图输出**：Plotivy 支持多种矢量图输出格式（SVG/PDF/EPS），确保图表在任何缩放级别下均保持锐利。矢量图是学术出版的黄金标准——可缩放、可编辑、印刷级清晰。对于必须使用位图的场景，Plotivy 支持 300dpi+ 的高分辨率 PNG/TIFF 输出。

5. **颜色盲友好色板**：Plotivy 内置颜色盲友好色板，基于 Wong's color palette 优化，通过红绿色盲、蓝黄色盲和全色盲模拟测试。颜色盲友好色板确保图表在所有读者面前均清晰可辨，这是现代学术出版的伦理要求。

### Plotivy 期刊规范自动校准算法

```
输入: 图表对象 + 目标期刊名
  ↓
1. 查询期刊规范数据库，获取目标期刊的字号/线宽/边距/字体规范
  ↓
2. 自动校准字号: 按期刊规范缩放字号阶梯
  ↓
3. 自动校准线宽: 按期刊规范调整数据线/轴线/网格线粗细
  ↓
4. 自动校准边距: 按期刊规范调整图表边距
  ↓
5. 自动切换字体: 按期刊规范切换字体族
  ↓
6. 输出: 符合目标期刊规范的图表对象
```

### Plotivy 线宽规范

| 元素 | 默认线宽 | Nature 校准 | IEEE 校准 | 说明 |
|------|---------|------------|----------|------|
| 数据线 | 1.5pt | 0.75pt | 1.5pt | 主数据系列 |
| 坐标轴线 | 0.75pt | 0.5pt | 1.0pt | 细轴线 |
| 网格线 | 0.5pt | 0.5pt | 0.5pt | 淡灰网格 |
| 图例边框 | 0pt | 0pt | 0.5pt | 无边框/细边框 |
| 误差棒 | 1.0pt | 0.5pt | 1.0pt | 误差范围 |

### 禁止事项

- 禁止使用未通过色盲测试的配色
- 禁止使用低分辨率位图（< 300dpi）投稿
- 禁止使用非矢量格式提交线图
- 禁止字号低于 6pt
- 禁止使用 3D 效果
- 禁止使用渐变填充
- 禁止忽略目标期刊的配图规范

---

## 与 visual_dna 的对接映射

### 配色注入映射

| DLP color_palette | visual_dna.color_scheme | 映射规则 |
|-------------------|------------------------|---------|
| `primary: #2E5C8A` | `--color-primary` | 通用期刊蓝/主数据系列/关键曲线 |
| `secondary: #C0392B` | `--color-secondary` | 期刊红/对比数据系列/高亮曲线 |
| `accent: #27AE60` | `--color-accent` | 期刊绿/第三数据系列/正向结果 |
| `neutral: #7F8C8D` | `--color-text-secondary` | 辅助文字/轴线/刻度标签 |
| `background: #FFFFFF` | `--color-bg` | 纯白背景/出版标准 |
| `text: #2C3E50` | `--color-text` | 标题/标签/图例文字（深蓝灰） |

### 字体注入映射

| DLP font_stack | visual_dna.font_scheme | 映射规则 |
|----------------|----------------------|---------|
| `学术图表: "Computer Modern", "Times New Roman", serif` | 标题/正文字体族（西文衬线） | 首选 Computer Modern，Times New Roman fallback |
| `中文 fallback: "宋体", "SimSun", serif` | 标题/正文字体族（中文） | 中文 fallback 宋体 |
| `等宽: "Courier New", monospace` | 代码字体族 | 等宽数值字体 |

### 图形规范注入映射

| DLP 字段 | visual_dna 字段 | 映射规则 |
|---------|----------------|---------|
| `grid_system: 600x400px, 双向网格线 #D5D8DC` | `grid_system` | 双向网格线直接继承 |
| `spacing_system: 2px 基准` | `line_style` | 间距阶梯直接继承 |
| `radius_shadow: 0px/none` | `line_style` | 强制直角零阴影 |
| `motion_curve: N/A(印刷媒介)` | `motion_profile` | 禁用动效 |
