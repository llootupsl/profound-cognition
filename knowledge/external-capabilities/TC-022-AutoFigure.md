<!-- 作者：阿洋 -->

# AutoFigure

## 基本信息
- **卡片编号**: #22
- **类型**: TC
- **优先级**: P1
- **层级**: L1

## 功能描述
AutoFigure 开源图表生成工具，Generator+Evaluator 循环迭代生成高质量图表。通过自然语言描述自动生成图表代码，内置评估器对生成结果进行质量评分和迭代优化，支持多种图表风格和输出格式，适用于自动化报告和文档插图生成。

## 调用指令

### 输入参数
- `description` (string, 图表的自然语言描述)
- `data` (object, 可选: 图表数据)
- `style` (string, 可选: 图表风格，如 minimal/colorful/academic)

### 输出格式
SVG/draw.io 格式图表

### 调用示例
```
autofigure_generate(description="展示微服务架构中各服务的调用关系", data={"services":["API Gateway","User Service","Order Service","Payment Service"],"calls":[["API Gateway","User Service"],["API Gateway","Order Service"],["Order Service","Payment Service"]]}, style="minimal")
```

## 穷尽重试策略
- **穷尽重试替代路径**: AutoFigure → Mermaid/TikZ/PlantUML
- **触发条件**: AutoFigure 服务不可用或迭代超过最大次数

## MCP 适配
- **MCP Tool 名称**: autofigure_generate
- **MCP 参数**: description, data, style

## 依赖
- AutoFigure 服务部署 + LLM 推理后端

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

暂无显式 DAG 节点消费者。保留待扩展。

