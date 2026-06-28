<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

# ECharts

## 基本信息

> ★核心方法论已内化于 rendering-pipeline/visual-dna.md，本文件仅作快速引用入口

- **卡片编号**: #18
- **类型**: LC
- **优先级**: P1
- **层级**: L2

## 功能描述
ECharts 数据可视化库，支持丰富的图表类型和交互功能。涵盖折线图、柱状图、饼图、散点图、热力图、地图等数十种图表类型，支持动画、缩放、数据筛选等交互操作，适用于数据分析和可视化展示。

## 调用指令

### 输入参数
- `chart_type` (string, 图表类型: line/bar/pie/scatter/heatmap/map 等)
- `data` (object, 图表数据，含 series/axis 等结构)
- `options` (object, 可选: 图表配置项，含 title/legend/tooltip/theme 等)

### 输出格式
SVG/PNG/HTML 交互图表

### 调用示例
```
echarts_render(chart_type="bar", data={"xAxis":["Q1","Q2","Q3","Q4"],"series":[120,200,150,80]}, options={"title":"季度销售额","theme":"dark"})
```

## 穷尽重试策略
- **穷尽重试替代路径**: ECharts → 静态图表(Matplotlib) → 表格
- **触发条件**: ECharts 渲染环境不可用或数据量超出浏览器承载

## MCP 适配
- **MCP Tool 名称**: echarts_render
- **MCP 参数**: chart_type, data, options

## 依赖
- ECharts 5.x JS 运行环境 + Node.js（服务端渲染）

## 调用前置条件
- Node.js 运行环境（服务端渲染场景）
- ECharts 5.x JS 库已加载（见上方「依赖」）
- 浏览器 DOM 环境（前端渲染场景）
- 上游节点产出已就绪（根据消费节点依赖关系）

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

暂无显式 DAG 节点消费者。保留待扩展。


## 效果度量

| 度量指标 | 定义 | 目标值 |
|----------|------|--------|
| 执行成功率 | 成功调用次数 / 总调用次数 | ≥ 0.95 |
| 平均延迟 | 单次调用平均耗时 | ≤ 5s |
| 输出质量分 | Supervisor 评分（0-1） | ≥ 0.8 |
| 穷尽重试触发率 | 触发降级的调用次数 / 总调用次数 | ≤ 0.1 |

效果度量写入 NRSF，供 T19 质量检查消费。