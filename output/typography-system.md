> **作者**: 阿洋

# 排版系统精确定义

> **模块标识**: `output/typography-system`
> **职责**: 为所有输出模块提供精确的排版数值定义与使用规范。所有数值均为权威来源，aesthetic-enhancer.md 及其他模块必须引用本文件定义，不得自行声明
> **依赖**: `output/font-scheme`
> **被依赖**: `output/aesthetic-enhancer`, `output/document-renderer`, `output/html-templates`

---

## 一、字体缩放比：1.25 Modular Scale

### 1.1 缩放比定义

| 参数 | 值 | 说明 |
|------|-----|------|
| 缩放比（ratio） | **1.25** | Major Third 音程对应的排版缩放比 |
| 基准值（base） | **1rem** = 16px | 正文基准字号 |
| 缩放方向 | 向上乘、向下除 | 标题逐级乘以 1.25，辅助文字除以 1.25 |

### 1.2 完整字号层级

| 层级 | CSS 变量 | 计算公式 | 精确 rem 值 | 等效 px 值 | 用途 |
|------|---------|---------|------------|-----------|------|
| h1 | `--ts-scale-h1` | 1rem × 1.25⁴ | **2.441rem** | 39.06px | 一级标题 / 章节标题 |
| h2 | `--ts-scale-h2` | 1rem × 1.25³ | **1.953rem** | 31.25px | 二级标题 / 节标题 |
| h3 | `--ts-scale-h3` | 1rem × 1.25² | **1.563rem** | 25.00px | 三级标题 / 小节标题 |
| h4 | `--ts-scale-h4` | 1rem × 1.25¹ | **1.25rem** | 20.00px | 四级标题 / 段落标题 |
| body | `--ts-scale-body` | 1rem × 1.25⁰ | **1rem** | 16.00px | 正文 / 段落文字 |
| small | `--ts-scale-small` | 1rem × 1.25⁻¹ | **0.8rem** | 12.80px | 辅助文字 / 注释 / 标签 |

### 1.3 使用规则

1. **严格层级**：标题必须按 h1→h2→h3→h4 顺序递进，禁止跳级（如 h1 直接接 h3）
2. **唯一基准**：所有字号必须基于 1rem 基准通过 1.25 的幂次计算得出，不得使用任意值
3. **扩展规则**：如需超出上述层级（如 display 封面大标题），按公式继续向上乘：display = 1rem × 1.25⁵ = 3.052rem（48.83px）
4. **响应式缩放**：移动端可将基准值从 1rem 调整为 0.9375rem（15px），缩放比不变，所有层级自动等比缩放

### 1.4 CSS 变量声明

```css
:root {
  --ts-ratio: 1.25;
  --ts-scale-small: 0.8rem;
  --ts-scale-body: 1rem;
  --ts-scale-h4: 1.25rem;
  --ts-scale-h3: 1.563rem;
  --ts-scale-h2: 1.953rem;
  --ts-scale-h1: 2.441rem;
}
```

---

## 二、网格系统：12 列网格

### 2.1 网格定义

| 参数 | 值 | 说明 |
|------|-----|------|
| 列数 | **12** | 可被 2、3、4、6 整除，支持多种布局组合 |
| 列间距（gutter） | **24px** | 相邻列之间的间距，固定值 |
| 间距数 | 11 | 12 列之间有 11 个 gutter |
| 基准单位 | 24px | gutter 值 = 1 个基准单位，与间距系统的 `--space-6` 对齐 |

### 2.2 布局组合

| 组合 | 列分配 | 宽度占比 | 适用场景 |
|------|--------|---------|---------|
| 全宽 | 12 | 100% | 标题、正文、全宽图表 |
| 1/2 + 1/2 | 6 + 6 | 50% + 50% | 双栏对比、图文并排 |
| 1/3 + 2/3 | 4 + 8 | 33.3% + 66.7% | 侧边栏 + 主内容 |
| 2/3 + 1/3 | 8 + 4 | 66.7% + 33.3% | 主内容 + 侧边栏 |
| 1/3 + 1/3 + 1/3 | 4 + 4 + 4 | 33.3% × 3 | 三栏数据卡片 |
| 1/4 + 1/4 + 1/4 + 1/4 | 3 + 3 + 3 + 3 | 25% × 4 | 四栏指标展示 |

### 2.3 使用规则

1. **列宽计算**：单列宽度 = (容器宽度 - 11 × 24px) / 12
2. **gutter 不可压缩**：24px gutter 在任何断点下不得小于 16px（移动端可降至 16px）
3. **嵌套网格**：允许网格嵌套，嵌套网格的 gutter 仍为 24px
4. **偏移**：使用 `offset-N`（N 为列数）实现左偏移，不使用右偏移

### 2.4 CSS 变量声明

```css
:root {
  --ts-grid-columns: 12;
  --ts-grid-gutter: 24px;
  --ts-grid-gutter-compact: 16px;
}
```

### 2.5 CSS Grid 模板

```css
.layout-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: var(--ts-grid-gutter);
}

@media (max-width: 767px) {
  .layout-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: var(--ts-grid-gutter-compact);
  }
}
```

---

## 三、留白比例：1:1.5:2

### 3.1 比例定义

| 层级 | 比例系数 | CSS 变量 | 基于基准 16px 的值 | 用途 |
|------|---------|---------|-------------------|------|
| 元素间距 | **1** | `--ts-whitespace-element` | 16px（1rem） | 行内元素间距、列表项间距、标签间距 |
| 段落间距 | **1.5** | `--ts-whitespace-paragraph` | 24px（1.5rem） | 段落之间、标题与正文之间 |
| 章节间距 | **2** | `--ts-whitespace-section` | 32px（2rem） | 章节之间、大块内容分隔 |

### 3.2 使用规则

1. **基准绑定**：比例系数基于正文基准字号（1rem = 16px），当基准变化时留白等比缩放
2. **元素间距（1×）**：用于同一逻辑块内的元素分隔，如列表项之间、表单字段之间、标签之间
3. **段落间距（1.5×）**：用于不同逻辑段落之间的分隔，如正文段落之间、标题与首段之间、图表与说明文字之间
4. **章节间距（2×）**：用于不同章节或大块内容之间的分隔，如 h1 前的间距、独立模块之间
5. **标题间距规则**：h1 上方 = 章节间距（2×），h1 下方 = 段落间距（1.5×）；h2/h3 上方 = 段落间距（1.5×），h2/h3 下方 = 元素间距（1×）
6. **禁止任意值**：所有垂直留白必须使用上述三个层级之一，不得插入自定义间距值

### 3.3 CSS 变量声明

```css
:root {
  --ts-whitespace-ratio-element: 1;
  --ts-whitespace-ratio-paragraph: 1.5;
  --ts-whitespace-ratio-section: 2;
  --ts-whitespace-element: 1rem;
  --ts-whitespace-paragraph: 1.5rem;
  --ts-whitespace-section: 2rem;
}
```

### 3.4 应用示例

```css
p { margin-bottom: var(--ts-whitespace-paragraph); }
li { margin-bottom: var(--ts-whitespace-element); }
h1 { margin-top: var(--ts-whitespace-section); margin-bottom: var(--ts-whitespace-paragraph); }
h2, h3 { margin-top: var(--ts-whitespace-paragraph); margin-bottom: var(--ts-whitespace-element); }
section + section { margin-top: var(--ts-whitespace-section); }
```

---

## 四、行宽约束

### 4.1 行宽定义

| 语境 | 最大宽度 | CSS 变量 | 字符数/行（约） | 说明 |
|------|---------|---------|---------------|------|
| 正文 | **680px** | `--ts-line-width-body` | 75 | 最优阅读行宽，基于 16px 宋体/衬线体 |
| 图表 | **960px** | `--ts-line-width-chart` | — | 图表、数据表、代码块等宽内容 |

### 4.2 使用规则

1. **正文强制约束**：正文容器必须设置 `max-width: 680px`，超出时居中显示
2. **图表扩展宽度**：图表、数据表、代码块可使用 960px 扩展宽度，但仍需在页面边距内
3. **全宽例外**：封面页、分隔页、导航栏不受行宽约束
4. **响应式**：当视口宽度小于 680px 时，正文宽度自动为 100% 减去页面边距
5. **字符数验证**：正文行宽 680px 在 16px 字号下约容纳 75 个西文字符或 37.5 个中文字符，符合 45-80 字符/行的可读性标准

### 4.3 CSS 变量声明

```css
:root {
  --ts-line-width-body: 680px;
  --ts-line-width-chart: 960px;
}
```

### 4.4 应用示例

```css
.prose { max-width: var(--ts-line-width-body); margin-inline: auto; }
.figure-container { max-width: var(--ts-line-width-chart); margin-inline: auto; }
```

---

## 五、行高

### 5.1 行高定义

| 语境 | 行高值 | CSS 变量 | 说明 |
|------|--------|---------|------|
| 正文 | **1.75** | `--ts-leading-body` | 无单位值，提供充裕的行间呼吸空间，适合长文阅读 |
| 标题 | **1.4** | `--ts-leading-heading` | 无单位值，紧凑行高增强标题视觉密度和层级感 |

### 5.2 使用规则

1. **无单位值**：行高必须使用无单位数值（1.75 / 1.4），而非固定 px 值，确保字号变化时行高等比缩放
2. **正文行高 1.75**：适用于所有段落文字、列表文字、表格文字、注释文字
3. **标题行高 1.4**：适用于 h1-h4 所有标题层级，以及卡片标题、图表标题
4. **代码块例外**：代码块行高可使用 1.5（`--ts-leading-code`），兼顾可读性与紧凑性
5. **引用块**：引用块使用正文行高 1.75

### 5.3 CSS 变量声明

```css
:root {
  --ts-leading-body: 1.75;
  --ts-leading-heading: 1.4;
  --ts-leading-code: 1.5;
}
```

### 5.4 应用示例

```css
body, p, li, td, th, figcaption { line-height: var(--ts-leading-body); }
h1, h2, h3, h4, .card-title { line-height: var(--ts-leading-heading); }
pre, code { line-height: var(--ts-leading-code); }
```

---

## 六、配色映射管线：YAML → CSS 变量 → 模板

### 6.1 映射管线概览

```
YAML 配色声明 → CSS 自定义属性（:root） → 引擎模板注入
                                            ├→ WeasyPrint @page + body 规则
                                            ├→ Marp 主题 CSS（/* @theme */ 块）
                                            └→ HTML 内联/内嵌样式
```

### 6.2 YAML 配色声明格式

```yaml
colors:
  primary:
    50:  "#E3F2FD"
    100: "#BBDEFB"
    200: "#90CAF9"
    300: "#64B5F6"
    400: "#42A5F5"
    500: "#2196F3"
    600: "#1E88E5"
    700: "#1976D2"
    800: "#1565C0"
    900: "#0D47A1"
  secondary:
    50:  "#F3E5F5"
    100: "#E1BEE7"
    200: "#CE93D8"
    300: "#BA68C8"
    400: "#AB47BC"
    500: "#9C27B0"
    600: "#8E24AA"
    700: "#7B1FA2"
    800: "#6A1B9A"
    900: "#4A148C"
  neutral:
    white:   "#FFFFFF"
    gray-50: "#FAFAFA"
    gray-100: "#F5F5F5"
    gray-200: "#EEEEEE"
    gray-300: "#E0E0E0"
    gray-400: "#BDBDBD"
    gray-500: "#9E9E9E"
    gray-600: "#757575"
    gray-700: "#616161"
    gray-800: "#424242"
    gray-900: "#212121"
    black:   "#000000"
  semantic:
    success: { light: "#E8F5E9", main: "#4CAF50", dark: "#2E7D32", text: "#1B5E20" }
    warning: { light: "#FFF3E0", main: "#FF9800", dark: "#E65100", text: "#BF360C" }
    error:   { light: "#FFEBEE", main: "#F44336", dark: "#C62828", text: "#B71C1C" }
    info:    { light: "#E3F2FD", main: "#2196F3", dark: "#1565C0", text: "#0D47A1" }
  aliases:
    background:    "neutral.white"
    surface:       "neutral.gray-50"
    text-primary:  "neutral.gray-900"
    text-secondary: "neutral.gray-600"
    text-disabled: "neutral.gray-400"
    border:        "neutral.gray-300"
    border-light:  "neutral.gray-200"
    link:          "primary.600"
    link-hover:    "primary.800"
```

### 6.3 YAML → CSS 变量映射规则

#### 6.3.1 色阶映射

| YAML 路径 | CSS 变量 | 转换规则 |
|-----------|---------|---------|
| `colors.primary.N` | `--color-primary-N` | 直接赋值色值 |
| `colors.secondary.N` | `--color-secondary-N` | 直接赋值色值 |
| `colors.neutral.gray-N` | `--color-gray-N` | 直接赋值色值 |
| `colors.neutral.white` | `--color-white` | 直接赋值色值 |
| `colors.neutral.black` | `--color-black` | 直接赋值色值 |
| `colors.semantic.TYPE.STATE` | `--color-TYPE-STATE` | 直接赋值色值 |
| `colors.aliases.NAME` | `--color-NAME` | 解析引用后赋值 `var(--color-xxx)` |

#### 6.3.2 别名解析规则

YAML 中的 `aliases` 字段使用点号路径引用已定义的色值：

```
aliases.background = "neutral.white"
→ CSS: --color-background: var(--color-white);
```

解析步骤：
1. 读取别名值（如 `"neutral.white"`）
2. 拆分为类别 + 层级（`neutral` + `white`）
3. 查找对应 CSS 变量名（`--color-white`）
4. 生成 `var()` 引用而非硬编码色值

#### 6.3.3 暗色模式覆写

```yaml
dark_overrides:
  aliases:
    background:    "neutral.gray-900-override:#121212"
    surface:       "neutral.gray-900-override:#1E1E1E"
    text-primary:  "neutral.gray-300-override:#E0E0E0"
    text-secondary: "neutral.gray-500-override:#9E9E9E"
    text-disabled: "neutral.gray-700-override:#616161"
    border:        "neutral.gray-800-override:#424242"
    border-light:  "neutral.gray-800-override:#333333"
    link:          "primary.300-override:#64B5F6"
    link-hover:    "primary.200-override:#90CAF9"
```

生成规则：

```css
[data-theme="dark"] {
  --color-background: #121212;
  --color-surface: #1E1E1E;
  /* ... */
}
```

暗色模式下别名直接使用硬编码色值（不使用 `var()` 引用），因为暗色值与亮色值无对应关系。

### 6.4 CSS 变量 → 引擎模板注入

#### 6.4.1 WeasyPrint 注入

WeasyPrint 支持 CSS Paged Media 规范，CSS 变量在 `@page` 和 `@media print` 中直接生效：

```css
@page {
  size: A4;
  margin: 2.5cm;
  @top-center { content: "研究报告"; color: var(--color-text-secondary); }
  @bottom-center { content: counter(page); color: var(--color-text-secondary); }
}

body {
  font-family: var(--font-body);
  font-size: var(--ts-scale-body);
  line-height: var(--ts-leading-body);
  color: var(--color-text-primary);
  max-width: var(--ts-line-width-body);
}
```

#### 6.4.2 Marp 注入

Marp 主题使用 `/* @theme name */` 指令，CSS 变量在 `section` 和 `section::after` 选择器中生效：

```css
/* @theme research-theme */
section {
  font-family: var(--font-body);
  font-size: var(--ts-scale-body);
  line-height: var(--ts-leading-body);
  color: var(--color-text-primary);
  max-width: var(--ts-line-width-chart);
}

section h1 { font-size: var(--ts-scale-h1); line-height: var(--ts-leading-heading); }
section h2 { font-size: var(--ts-scale-h2); line-height: var(--ts-leading-heading); }
```

#### 6.4.3 HTML 内嵌注入

HTML 模板在 `<style>` 块中直接声明 CSS 变量，无需外部文件：

```html
<style>
  :root { /* 所有 CSS 变量声明 */ }
  body { font-family: var(--font-body); /* ... */ }
</style>
```

### 6.5 映射验证清单

| 检查项 | 验证方法 |
|--------|---------|
| YAML 色值格式 | 正则匹配 `^#[0-9A-Fa-f]{6}$` |
| 别名引用完整性 | 所有 aliases 路径在 colors 中存在 |
| CSS 变量无遗漏 | YAML 中声明的色值均有对应 CSS 变量 |
| 暗色模式覆盖完整 | 所有亮色别名在 dark_overrides 中均有覆写 |
| 引擎注入无断链 | 模板中引用的 CSS 变量均在 :root 中声明 |

---

## 七、跨引擎一致性校验

### 7.1 一致性要求

| 属性 | WeasyPrint | Marp | HTML | 允许偏差 |
|------|-----------|------|------|---------|
| 字号层级 | 1.25 modular scale | 1.25 modular scale | 1.25 modular scale | 0 |
| 行高 | 1.75 / 1.4 | 1.75 / 1.4 | 1.75 / 1.4 | 0 |
| 行宽 | 680px / 960px | 960px（幻灯片全宽） | 680px / 960px | Marp 允许 960px |
| 网格 | 12 列 / 24px gutter | 不适用（幻灯片布局） | 12 列 / 24px gutter | Marp 免检 |
| 留白比例 | 1:1.5:2 | 1:1.5:2 | 1:1.5:2 | 0 |
| 色值 | CSS 变量 | CSS 变量 | CSS 变量 | 0 |

### 7.2 偏差说明

- **Marp 行宽**：幻灯片场景下正文使用 960px 全宽，不适用 680px 正文行宽约束
- **Marp 网格**：幻灯片使用固定比例布局（如 50/50、60/40），不使用 12 列网格
- **WeasyPrint 字号**：PDF 输出时基准字号可从 1rem（16px）调整为 11pt，缩放比不变

---

## 八、中文学术排版规则

### 8.1 标点挤压

中文标点与西文字符之间不加空格，中文标点之间自动挤压。排版引擎应实现标点宽度压缩逻辑，避免连续标点（如"……"）占用过多视觉空间。

### 8.2 避头尾规则

- **行首禁止字符**：句号（。）、逗号（，）、顿号（、）、分号（；）、感叹号（！）、问号（？）、右引号（」』）」）、右括号（）〕】》）、省略号（……）等
- **行尾禁止字符**：左引号（「『「）、左括号（（〔【《）等
- 排版引擎须实现避头尾（kinsoku shori）断行逻辑，确保上述字符不出现在行首或行尾

### 8.3 中英文间距

中英文之间自动插入 1/4em 间距。该间距由排版引擎自动处理，无需手动插入空格。

### 8.4 数字与中文间距

数字与中文之间自动插入 1/4em 间距。该间距由排版引擎自动处理，无需手动插入空格。

### 8.5 标准依据

本节规则依据 **GB/T 15834-2011《标点符号用法》** 制定，适用于所有中文输出场景。

---

## 九、Typst 排版引擎优先级

### 9.1 引擎优先级排序

| 优先级 | 排版引擎 | 适用场景 | 核心优势 | 限制 |
|--------|---------|---------|---------|------|
| 1 | **Typst** | 研究论文、PDF报告、学术排版、书籍 | 现代语法，编译速度快（毫秒级），程序化排版，增量编译 | 生态较新，LaTeX 宏包兼容性有限 |
| 2 | WeasyPrint | HTML→PDF 转换、简单报告、信函 | 基于 CSS 布局，Web 标准，无需额外学习 | 分页控制不如 Typst/LaTeX 精细 |
| 3 | Marp | 幻灯片、演示文稿、培训材料 | Markdown 驱动，主题化，实时预览 | 不适合长文档排版 |
| 4 | HTML | 网页展示、交互式文档、在线阅读 | 浏览器原生渲染，交互性强 | 打印输出一致性依赖 WeasyPrint |

### 9.2 Typst 首选场景

以下场景 Typst 作为唯一首选引擎，其他引擎不参与竞争：

| 场景 | 原因 |
|------|------|
| 学术论文（含公式） | Typst 数学排版能力与 LaTeX 相当，语法更简洁 |
| 多语言混排（中日韩 + 西文） | Typst 原生支持 CJK，无需额外宏包 |
| 程序化生成报告 | Typst 可脚本化调用，支持 JSON/YAML 数据注入 |
| 版本控制友好 | Typst 源码为纯文本，diff 可读性优于 LaTeX |
| 大规模文档（100+ 页） | 增量编译，修改一处仅重新编译受影响部分 |

### 9.3 引擎穷尽重试策略

当首选引擎不可用时，按以下顺序穷尽尝试：

1. **Typst 不可用 → WeasyPrint**：适用于纯文本报告，不含复杂数学公式
2. **WeasyPrint 不可用 → HTML**：保留样式，但分页控制丢失
3. **Marp 不可用 → HTML 幻灯片**：使用 reveal.js 或 remark.js 替代

### 9.4 Typst 模板声明

项目中的 Typst 模板位于 `output/typst-templates/` 目录，按产品类型组织：

| 模板文件 | 产品类型 | 用途 |
|---------|---------|------|
| `research-report.typ` | 研究论文 | 学术 PDF 报告主模板（内含封面页/目录页/维度分析页/附录页宏定义） |
| `course-lecture.typ` | 课程讲义 | 课程幻灯片/讲义模板 |
| `wechat-article-export.typ` | 公众号文章 | 公众号文章导出模板 |

> **注意**：封面页、目录页、维度分析页、附录页的排版宏已内含于 `research-report.typ` 主模板中，无需单独引用外部文件。

---

## 十、产品类型差异化排版规则

### 10.1 研究论文（Research Paper / PDF）

| 属性 | 值 | 说明 |
|------|-----|------|
| 排版引擎 | Typst（首选）→ WeasyPrint | 公式密集型优先 Typst |
| 正文字体 | 衬线体（Source Serif 4 / Charter） | 长文阅读首选衬线体 |
| 标题字体 | 无衬线体（Glow Sans SC / Source Han Sans SC） | 标题与正文形成视觉对比 |
| 代码字体 | Fragment Mono / JetBrains Mono | 9pt 代码块字号 |
| 正文行宽 | 680px（`--ts-line-width-body`） | 标准阅读行宽 |
| 图表行宽 | 960px（`--ts-line-width-chart`） | 图表可扩展宽度 |
| 页边距 | A4 上下 2.5cm，左右 2.5cm | 标准学术页边距 |
| 正文行高 | 1.75（`--ts-leading-body`） | 充裕行间呼吸空间 |
| 标题行高 | 1.4（`--ts-leading-heading`） | 紧凑增强层级感 |
| 字号层级 | 1.25 modular scale | 基于 1rem = 16px 基准 |
| 网格 | 12 列 / 24px gutter | 全标准网格系统 |
| 留白比例 | 1:1.5:2 | 严格遵循三档留白 |
| 引用格式 | GB/T 7714-2015 | 中文国家标准引用格式 |
| 页码 | 底部居中 | WeasyPrint `@bottom-center` / Typst `page.numbering` |
| 页眉 | 章节标题 | WeasyPrint `@top-center` / Typst `page.header` |
| 暗色模式 | 不支持 | 打印输出为亮色模式 |
| 中文学术规则 | 全量启用 | 标点挤压、避头尾、中英文间距 |

### 10.2 幻灯片（Slides / Marp / HTML）

| 属性 | 值 | 说明 |
|------|-----|------|
| 排版引擎 | Marp（首选）→ HTML 幻灯片 | Markdown 驱动，主题化 |
| 正文字体 | 无衬线体（Glow Sans SC / Source Han Sans SC） | 屏幕投影须用无衬线体 |
| 标题字体 | 无衬线体（Glow Sans SC / Source Han Sans SC） | 统一字体家族 |
| 代码字体 | JetBrains Mono / Cascadia Code | 代码演示场景 |
| 正文行宽 | 960px（幻灯片全宽） | 不适用 680px 正文约束 |
| 字号基准 | 正文最小 18pt | 投影环境下须加大字号 |
| 标题字号 | h1: 36pt+，h2: 28pt+ | 确保后排可读 |
| 行高 | 正文 1.6，标题 1.3 | 幻灯片场景略微收紧 |
| 网格 | 不使用 12 列网格 | 使用固定比例布局（50/50、60/40、70/30） |
| 留白比例 | 1:1.5:2 | 保持比例，但基准值调整为 1.25rem |
| 配色 | 主题色 + 高对比度 | 确保投影仪下可辨识 |
| 页面比例 | 16:9 | 标准宽屏比例 |
| 代码块 | 最大 20 行 | 超出折叠或分页 |
| 中文学术规则 | 标点挤压 + 中英文间距 | 避头尾规则在幻灯片中穷尽重试为可选 |

### 10.3 公众号文章（WeChat Article / HTML）

| 属性 | 值 | 说明 |
|------|-----|------|
| 排版引擎 | HTML（首选）→ WeasyPrint（导出 PDF） | 公众号原生 HTML 渲染 |
| 正文字体 | 系统默认（Microsoft YaHei / PingFang SC） | 公众号环境仅支持系统字体 |
| 标题字体 | 系统默认加粗 | 无法使用自定义 webfont |
| 代码字体 | Consolas / SF Mono | 系统默认等宽字体 |
| 正文行宽 | 680px（`--ts-line-width-body`） | 标准阅读行宽 |
| 字号基准 | 正文 16px（1rem） | 移动端阅读友好 |
| 标题字号 | h1: 20px，h2: 18px | 公众号标题不宜过大 |
| 行高 | 正文 1.75，标题 1.5 | 移动端行高略大于桌面端 |
| 网格 | 不使用 12 列网格 | 公众号使用单列布局 |
| 留白比例 | 1:1.5:2 | 保持比例体系 |
| 配色 | 公众号主题色注入 | 通过 `data-theme` 属性注入 |
| 图片 | 宽度 100%，最大 680px | 响应式图片，WebP 格式 |
| 卡片 | Moka / 内置公众号排版系统 样式映射 | 公众号卡片排版工具链 |
| 暗色模式 | 支持（`data-theme="dark"`） | 微信暗色模式适配 |
| 中文学术规则 | 标点挤压 + 中英文间距 | 完整启用 |
| 排版工具 | Moka → 内置公众号排版系统 → Panelizer | 三级排版工具链 |

### 10.4 产品类型差异对照总表

| 属性 | 研究论文 | 幻灯片 | 公众号文章 |
|------|---------|--------|-----------|
| 首选引擎 | Typst | Marp | HTML |
| 正文字体 | 衬线体 | 无衬线体 | 系统默认 |
| 正文行宽 | 680px | 960px | 680px |
| 正文字号 | 16px | 18pt+ | 16px |
| 网格 | 12 列 | 固定比例 | 单列 |
| 暗色模式 | 否 | 可选 | 是 |
| 引用格式 | GB/T 7714 | 无 | 无 |
| 页码 | 是 | 否 | 否 |
| 避头尾 | 强制 | 可选 | 强制 |

---

© 阿洋
