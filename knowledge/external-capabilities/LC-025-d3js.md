<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

# D3.js

## 基本信息

> ★核心方法论已内化于 rendering-pipeline/visual-dna.md，本文件仅作快速引用入口

- **卡片编号**: #25
- **类型**: LC
- **优先级**: P2
- **层级**: L2

## 功能描述
D3.js 数据驱动文档库，支持高度自定义的数据可视化。通过数据绑定和 DOM 操作实现声明式可视化，涵盖力导向图、树状图、地理投影、桑基图、旭日图等高级图表类型，支持动画过渡、交互筛选、缩放平移等复杂交互，适用于需要精细控制视觉表达的数据可视化场景。

## 调用指令

### 输入参数
- `data` (object, 可视化数据，支持 JSON/CSV/TSV 等格式)
- `visualization_spec` (object, 可视化规格，含 chart_type/layout/encoding/interaction 等)
- `options` (object, 可选: 渲染配置，含 width/height/theme/animation 等)

### 输出格式
SVG/HTML 交互可视化

### 调用示例
```
d3_render(data={"nodes":[{"id":"A","group":1},{"id":"B","group":2}],"links":[{"source":"A","target":"B","value":5}]}, visualization_spec={"chart_type":"force_directed","layout":{"charge":-300,"distance":100},"encoding":{"color":"group","size":"value"}})
```

## 穷尽重试策略
- **穷尽重试替代路径**: D3.js → ECharts → 表格
- **触发条件**: D3.js 渲染环境不可用或可视化规格超出渲染能力

## MCP 适配
- **MCP Tool 名称**: d3_render
- **MCP 参数**: data, visualization_spec, options

## 依赖
- D3.js 7.x JS 运行环境 + Node.js（服务端渲染）

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