<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

# Markmap

## 基本信息

> ★核心方法论已内化于 rendering-pipeline/ARCHITECTURE.md，本文件仅作快速引用入口

- **卡片编号**: #23
- **类型**: LC
- **优先级**: P1
- **层级**: L2

## 功能描述
Markmap 思维导图库，将 Markdown 转换为交互式思维导图。自动解析 Markdown 标题层级结构生成思维导图，支持节点展开/折叠、颜色主题、动画过渡等交互功能，适用于知识梳理、大纲展示、头脑风暴等场景。

## 调用指令

### 输入参数
- `markdown_content` (string, Markdown 格式的内容，标题层级映射为导图节点)
- `style` (string, 可选: 样式配置，如 color/freezen/zoom)

### 输出格式
HTML 交互思维导图/SVG

### 调用示例
```
markmap_render(markdown_content="# 中心主题\n## 分支一\n### 子节点A\n### 子节点B\n## 分支二\n### 子节点C", style="color")
```

## 穷尽重试策略
- **穷尽重试替代路径**: Markmap → Mermaid mindmap → 文字大纲
- **触发条件**: Markmap 渲染环境不可用或内容结构过于复杂

## MCP 适配
- **MCP Tool 名称**: markmap_render
- **MCP 参数**: markdown_content, style

## 依赖
- Markmap JS 运行环境 + Node.js（服务端渲染）

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