<!-- 作者：阿洋 -->

# Plotly

## 基本信息

> ★核心方法论已内化于 rendering-pipeline/visual-dna.md，本文件仅作快速引用入口

- **卡片编号**: #19
- **类型**: LC
- **优先级**: P1
- **层级**: L2

## 功能描述
Plotly 交互式图表库，支持科学计算和统计分析图表。提供 3D 图表、统计图表、金融图表、地理地图等专业图表类型，支持 Python/R/JS 多语言绑定，适用于科研数据可视化和探索性数据分析。

## 调用指令

### 输入参数
- `chart_type` (string, 图表类型: scatter/line/bar/3d_surface/heatmap/box/violin 等)
- `data` (object, 图表数据，含 traces 结构)
- `layout` (object, 可选: 布局配置，含 title/xaxis/yaxis/coloraxis 等)

### 输出格式
HTML 交互图表/SVG/PNG

### 调用示例
```
plotly_render(chart_type="3d_surface", data={"z":[[1,2,3],[4,5,6],[7,8,9]]}, layout={"title":"3D Surface Plot","coloraxis":{"colorscale":"Viridis"}})
```

## 穷尽重试策略
- **穷尽重试替代路径**: Plotly → Matplotlib → 表格
- **触发条件**: Plotly 渲染环境不可用或交互功能非必需

## MCP 适配
- **MCP Tool 名称**: plotly_render
- **MCP 参数**: chart_type, data, layout

## 依赖
- Plotly.py / Plotly.js 运行环境 + Node.js（服务端渲染）

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

暂无显式 DAG 节点消费者。保留待扩展。

