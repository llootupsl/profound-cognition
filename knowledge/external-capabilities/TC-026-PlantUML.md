<!-- 作者：阿洋 -->

# PlantUML

## 基本信息
- **卡片编号**: #26
- **类型**: TC
- **优先级**: P2
- **层级**: L1

## 功能描述
PlantUML UML 图生成工具，支持类图、时序图、用例图、活动图、组件图、状态图、对象图、部署图等标准 UML 图表类型。采用简洁的文本描述语法，自动排版生成规范图表，适用于软件架构设计、系统建模、文档编写等场景。

## 调用指令

### 输入参数
- `definition` (string, PlantUML 语法的图表定义文本)
- `output_format` (string, 可选: 输出格式 svg/png/pdf/eps，默认 svg)

### 输出格式
SVG/PNG/PDF/EPS 图表文件

### 调用示例
```
plantuml_render(definition="@startuml\nAlice -> Bob: Hello\nBob --> Alice: Hi\n@enduml", output_format="svg")
```

## 穷尽重试策略
- **穷尽重试替代路径**: PlantUML → Mermaid → ASCII 图
- **触发条件**: PlantUML 服务不可用或语法解析失败

## MCP 适配
- **MCP Tool 名称**: plantuml_render
- **MCP 参数**: definition, output_format

## 依赖
- PlantUML 服务部署（需 Java 运行环境 + Graphviz）

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

暂无显式 DAG 节点消费者。保留待扩展。

