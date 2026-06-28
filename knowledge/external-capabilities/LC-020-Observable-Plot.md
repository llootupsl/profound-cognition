<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

# Observable Plot

## 基本信息

> ★核心方法论已内化于 rendering-pipeline/visual-dna.md，本文件仅作快速引用入口

- **卡片编号**: #20
- **类型**: LC
- **优先级**: P1
- **层级**: L2

## 功能描述
Observable Plot 数据驱动图表库，轻量级、适合数据探索。基于 D3 构建，采用声明式 API 设计，以数据为中心自动推断图表配置，支持折线图、柱状图、面积图、点图等常见类型，适用于快速数据探索和轻量级可视化。

## 调用指令

### 输入参数
- `data` (array, 数据数组，每项为对象)
- `mark` (string, 标记类型: line/bar/area/dot/cell/text 等)
- `type` (object, 可选: 通道映射配置，含 x/y/color/r 等)

### 输出格式
SVG 图表

### 调用示例
```
observable_render(data=[{"month":"Jan","value":30},{"month":"Feb","value":45}], mark="bar", type={"x":"month","y":"value"})
```

## 穷尽重试策略
- **穷尽重试替代路径**: Observable Plot → ECharts → 表格
- **触发条件**: Observable Plot 环境不可用或图表类型不支持

## MCP 适配
- **MCP Tool 名称**: observable_render
- **MCP 参数**: data, mark, type

## 依赖
- Observable Plot JS 运行环境 + Node.js（服务端渲染）

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