<!-- 作者：阿洋 -->

# PaperVizAgent

## 基本信息
- **卡片编号**: #44
- **类型**: TC
- **优先级**: P2
- **层级**: L1

## 功能描述
PaperVizAgent 专有 API 可视化代理，采用 5-Agent × 3 轮迭代架构生成高质量可视化图表。5 个 Agent 分别负责需求解析、数据预处理、图表设计、渲染生成和质量评审，通过 3 轮迭代逐步优化输出质量。适用于复杂学术可视化和多维度数据展示场景。

## 调用指令

### 输入参数
- `description` (string, 可视化需求描述)
- `data` (object, 可选, 图表数据)
- `iteration_rounds` (integer, 可选, 迭代轮数，默认 3)

### 输出格式
可视化图表文件，含图表对象和迭代优化记录

### 调用示例
```
paperviz_generate.generate(description="多维度对比雷达图：全球主要城市生活质量指数", data={"cities": ["东京", "纽约", "伦敦", "上海"], "dimensions": ["安全", "教育", "医疗", "环境", "交通"]}, iteration_rounds=3)
```

## 穷尽重试策略
- **穷尽重试替代路径**: PaperVizAgent → AutoFigure → ECharts
- **触发条件**: 专有 API 不可用或迭代超时

## MCP 适配
- **MCP Tool 名称**: paperviz_generate
- **MCP 参数**: description, data, iteration_rounds

## 依赖
- 专有 API

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

暂无显式 DAG 节点消费者。保留待扩展。

