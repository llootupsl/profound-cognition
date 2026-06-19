<!-- 作者：阿洋 -->

# Mermaid

## 基本信息

> ★核心方法论已内化于 rendering-pipeline/ARCHITECTURE.md，本文件仅作快速引用入口

- **卡片编号**: #21
- **类型**: LC
- **优先级**: P1
- **层级**: L2

## 功能描述
Mermaid 流程图/时序图库，支持 Markdown 语法绘制图表。提供流程图、时序图、甘特图、类图、状态图、ER 图、思维导图等多种图表类型，使用纯文本定义图表结构，适用于架构文档、流程说明、系统设计等场景。

## 调用指令

### 输入参数
- `definition` (string, Mermaid 语法的图表定义)
- `output_format` (string, 可选: svg/png，默认 svg)

### 输出格式
SVG/PNG

### 调用示例
```
mermaid_render(definition="graph TD\n    A[开始] --> B{判断}\n    B -->|是| C[执行]\n    B -->|否| D[结束]", output_format="svg")
```

## 穷尽重试策略
- **穷尽重试替代路径**: Mermaid → ASCII 图 → 文字描述
- **触发条件**: Mermaid 渲染失败或语法解析错误

## MCP 适配
- **MCP Tool 名称**: mermaid_render
- **MCP 参数**: definition, output_format

## 依赖
- Mermaid CLI (mmdc) + Node.js + Chromium（PNG 渲染）

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

暂无显式 DAG 节点消费者。保留待扩展。

