<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

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

## 调用前置条件
- Java 运行环境已安装（PlantUML 依赖 JVM）
- Graphviz 已安装（PlantUML 依赖 Graphviz 进行布局）
- PlantUML 服务已部署并可访问（见上方「依赖」）
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