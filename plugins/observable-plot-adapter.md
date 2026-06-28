---
name: observable-plot-adapter
description: Observable Plot 适配器 — 将数据可视化需求映射为 Observable Plot 声明式图表，输出 SVG/HTML 格式
author: 阿洋
tags: [observable-plot, chart, adapter, chart-renderer, svg]
---

# Observable Plot 适配器

## 概述

本模块为 chart-renderer 提供 Observable Plot 图表渲染适配器，将 5 种数据图表类型映射为 Observable Plot 声明式 API 调用，输出 SVG/HTML 格式。Observable Plot 语法简洁、交互自动、体积轻量（~100KB），适合数据分布/趋势/对比/相关性类图表。与 chart-renderer 的双引擎选择逻辑集成，作为数据驱动图表的首选引擎。

---

## 激活条件

```yaml
activation:
  condition: "chart-renderer 图表需求 ∈ {数据分布, 趋势, 对比, 相关性, 小多图} AND JavaScript 环境可用"
  priority: "数据驱动图表的首选引擎 — 简洁声明式 API"
  exhaust-retry: "若 Observable Plot CDN 不可用，穷尽重试到 ECharts → Mermaid → Markdown 表格"
```

---

## CDN 引用

```html
<script type="module">
  import * as Plot from "https://cdn.jsdelivr.net/npm/@observablehq/plot@0.6/+esm";
</script>
```

---

## 5 种图表模板

### 1. 柱状图

```javascript
function renderBarChart(data, containerId) {
  const chart = Plot.plot({
    title: "{{CHART_TITLE}}",
    width: 700,
    height: 400,
    marginLeft: 60,
    marginBottom: 50,
    x: { label: "{{X_LABEL}}", grid: false },
    y: { label: "{{Y_LABEL}}", grid: true },
    marks: [
      Plot.barY(data, {
        x: "{{X_FIELD}}",
        y: "{{Y_FIELD}}",
        fill: "{{COLOR_FIELD}}",
        tip: true,
      }),
      Plot.ruleY([0]),
    ],
    color: {
      range: ["#BBDEFB", "#2196F3", "#0D47A1"],
      legend: true,
    },
  });
  document.getElementById(containerId).append(chart);
}
```

**数据格式**：

```json
[
  { "category": "Q1", "value": 1250, "year": "2025" },
  { "category": "Q2", "value": 1480, "year": "2025" },
  { "category": "Q3", "value": 1320, "year": "2025" },
  { "category": "Q4", "value": 1680, "year": "2025" }
]
```

### 2. 折线图

```javascript
function renderLineChart(data, containerId) {
  const chart = Plot.plot({
    title: "{{CHART_TITLE}}",
    width: 700,
    height: 400,
    marginLeft: 60,
    marginBottom: 50,
    x: { label: "{{X_LABEL}}" },
    y: { label: "{{Y_LABEL}}", grid: true },
    marks: [
      Plot.line(data, {
        x: "{{X_FIELD}}",
        y: "{{Y_FIELD}}",
        stroke: "{{SERIES_FIELD}}",
        strokeWidth: 2,
      }),
      Plot.dot(data, {
        x: "{{X_FIELD}}",
        y: "{{Y_FIELD}}",
        fill: "{{SERIES_FIELD}}",
        r: 3,
        tip: true,
      }),
    ],
    color: { legend: true },
  });
  document.getElementById(containerId).append(chart);
}
```

**数据格式**：

```json
[
  { "quarter": "Q1", "value": 980, "series": "2024" },
  { "quarter": "Q2", "value": 1120, "series": "2024" },
  { "quarter": "Q1", "value": 1250, "series": "2025" },
  { "quarter": "Q2", "value": 1480, "series": "2025" }
]
```

### 3. 散点图

```javascript
function renderScatterPlot(data, containerId) {
  const chart = Plot.plot({
    title: "{{CHART_TITLE}}",
    width: 700,
    height: 500,
    marginLeft: 60,
    marginBottom: 50,
    x: { label: "{{X_LABEL}}", grid: true },
    y: { label: "{{Y_LABEL}}", grid: true },
    marks: [
      Plot.dot(data, {
        x: "{{X_FIELD}}",
        y: "{{Y_FIELD}}",
        fill: "{{CATEGORY_FIELD}}",
        r: "{{SIZE_FIELD}}",
        opacity: 0.7,
        tip: true,
      }),
      Plot.linearRegressionY(data, {
        x: "{{X_FIELD}}",
        y: "{{Y_FIELD}}",
        stroke: "#e94560",
        strokeWidth: 1.5,
      }),
    ],
    color: { legend: true },
  });
  document.getElementById(containerId).append(chart);
}
```

**数据格式**：

```json
[
  { "x_value": 10, "y_value": 25, "category": "A", "size": 5 },
  { "x_value": 20, "y_value": 45, "category": "B", "size": 8 },
  { "x_value": 30, "y_value": 35, "category": "A", "size": 6 }
]
```

### 4. 热力图

```javascript
function renderHeatmap(data, containerId) {
  const chart = Plot.plot({
    title: "{{CHART_TITLE}}",
    width: 600,
    height: 500,
    marginLeft: 80,
    marginBottom: 50,
    x: { label: "{{X_LABEL}}" },
    y: { label: "{{Y_LABEL}}" },
    color: {
      type: "diverging",
      scheme: "RdBu",
      legend: true,
      label: "{{VALUE_LABEL}}",
    },
    marks: [
      Plot.cell(data, {
        x: "{{X_FIELD}}",
        y: "{{Y_FIELD}}",
        fill: "{{VALUE_FIELD}}",
        tip: true,
      }),
    ],
  });
  document.getElementById(containerId).append(chart);
}
```

**数据格式**：

```json
[
  { "row": "A", "col": "X", "value": 0.85 },
  { "row": "A", "col": "Y", "value": -0.32 },
  { "row": "B", "col": "X", "value": -0.15 },
  { "row": "B", "col": "Y", "value": 0.72 }
]
```

### 5. 小多图（Facet）

```javascript
function renderFacetChart(data, containerId) {
  const chart = Plot.plot({
    title: "{{CHART_TITLE}}",
    width: 900,
    height: 500,
    marginLeft: 50,
    marginBottom: 40,
    fx: { label: "{{FACET_LABEL}}" },
    x: { label: "{{X_LABEL}}" },
    y: { label: "{{Y_LABEL}}", grid: true },
    marks: [
      Plot.barY(data, {
        x: "{{X_FIELD}}",
        y: "{{Y_FIELD}}",
        fx: "{{FACET_FIELD}}",
        fill: "{{COLOR_FIELD}}",
        tip: true,
      }),
      Plot.ruleY([0]),
    ],
    color: { legend: true },
  });
  document.getElementById(containerId).append(chart);
}
```

**数据格式**：

```json
[
  { "category": "Q1", "value": 1250, "region": "华东", "type": "A" },
  { "category": "Q2", "value": 1480, "region": "华东", "type": "A" },
  { "category": "Q1", "value": 980, "region": "华北", "type": "A" },
  { "category": "Q2", "value": 1120, "region": "华北", "type": "A" }
]
```

---

## 数据格式规范

### 输入格式

```yaml
input_format:
  type: "JSON 数组"
  encoding: "UTF-8"
  requirements:
    - "每个元素为扁平 JSON 对象"
    - "字段名使用 snake_case 命名"
    - "数值字段为 number 类型（非字符串）"
    - "分类字段为 string 类型"
    - "缺失值使用 null（非空字符串）"
```

### 输出格式

```yaml
output_format:
  primary: "SVG（内嵌于 HTML）"
  secondary: "HTML（完整可交互页面）"
  export:
    svg: "可直接提取 SVG 节点用于嵌入"
    png: "通过 canvas 转换导出"
```

---

## 与 chart-renderer 的集成：双引擎选择逻辑

### 引擎选择决策树

```yaml
engine_selection:
  rule_1_structural:
    types: ["流程图", "关系图", "因果回路图", "架构图"]
    engine: "Mermaid"
    reason: "结构性图表需要节点-边布局，Mermaid 原生支持"

  rule_2_data_driven:
    types: ["数据分布", "趋势", "对比", "相关性", "小多图"]
    engine: "Observable Plot"
    reason: "数据驱动图表需要精确的坐标映射和交互，Observable Plot 声明式 API 更简洁"

  rule_3_conceptual:
    types: ["概念图", "思维导图", "知识图谱"]
    engine: "Markmap"
    reason: "概念性图表需要层级展开和折叠交互，Markmap 原生支持"

  rule_4_complex:
    types: ["桑基图", "地图", "3D", "仪表盘", "雷达图"]
    engine: "ECharts"
    reason: "复杂图表需要全功能渲染引擎，ECharts 覆盖最广"
```

### 集成流程

```
chart-renderer 接收图表需求
  → 判断图表类型
  → 结构性图表 → Mermaid
  → 数据驱动图表 → Observable Plot（本适配器）
  → 概念性图表 → Markmap
  → 复杂图表 → ECharts
  → 穷尽重试：CDN 不可用 → Markdown 表格
```

---

## 色彩规范（与 aesthetic-enhancer.md 对齐）

```javascript
const PLOT_COLORS = {
  primary: "#2196F3",
  accent: "#e94560",
  categorical: ["#2196F3", "#4CAF50", "#FF9800", "#9C27B0", "#F44336",
                "#00BCD4", "#607D8B", "#795548"],
  sequential: ["#E3F2FD", "#BBDEFB", "#90CAF9", "#64B5F6", "#42A5F5",
               "#2196F3", "#1E88E5", "#1976D2", "#1565C0", "#0D47A1"],
  diverging: ["#1565C0", "#64B5F6", "#E3F2FD", "#FFEBEE", "#EF9A9A", "#C62828"],
};
```

---

## 错误处理

```yaml
error_handling:
  cdn_unavailable:
    action: "穷尽重试到 ECharts CDN，若仍不可用则穷尽重试到 Mermaid"
    log: "记录 Observable Plot CDN 加载失败事件"
    exhaust_retry_chain: "Observable Plot → ECharts → Mermaid → Markdown 表格"

  data_format_error:
    action: "尝试自动修正数据格式（类型转换、缺失值处理）"
    log: "记录数据格式错误事件，标注 error_field={field_name}"
    exhaust-retry: "修正失败则穷尽重试到 Markdown 表格"

  render_error:
    action: "穷尽重试到 ECharts 渲染相同数据"
    log: "记录 Observable Plot 渲染错误事件"

  empty_data:
    action: "显示空数据占位图"
    log: "记录空数据事件"

  container_not_found:
    action: "使用 document.body 作为容器"
    log: "记录容器未找到事件，标注 container_id={id}"
```

---

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| v1.0 | 2026-05-28 | 初始发布：Observable Plot 适配器 + 5 种图表模板 + 双引擎选择逻辑 |

---

© 阿洋


---

## 穷尽重试策略

```yaml
exhaust_retry:
  L1_FULL:
    condition: "Observable Plot CDN 可用 + JavaScript 环境正常"
    behavior: "完整声明式图表 + 交互 + SVG/HTML输出"

  L2_PARTIAL_DATA:
    condition: "Observable Plot CDN 可用但部分功能异常"
    behavior: "基础图表渲染 + 标注[PARTIAL-FEATURE]"

  L3_TEXT_ONLY:
    condition: "Observable Plot CDN 不可用"
    behavior: "穷尽尝试到 ECharts/Mermaid 图表 + 标注[INTERNAL_REASONING-CHART]"

  L4_SERVICE_DOWN:
    condition: "所有图表渲染工具不可用"
    behavior: "Markdown表格 + 标注[TABLE-ONLY]"
```
