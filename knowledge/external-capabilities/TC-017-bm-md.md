<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

# 内置公众号排版系统

## 基本信息
- **卡片编号**: #17
- **类型**: TC
- **优先级**: P1
- **层级**: L1

## 功能描述
Markdown 排版工具，支持 Markdown 到多种格式的转换和美化。提供丰富的模板和样式，可将 Markdown 源文件转换为 HTML、PDF、DOCX 等格式，适用于报告生成、文档发布等场景。

## 调用指令

### 输入参数
- `source` (string, Markdown 源文件内容或路径)
- `format` (string, 目标格式: html/pdf/docx)
- `template` (string, 可选: 模板名称，如 academic/report/slides)

### 输出格式
HTML/PDF/DOCX

### 调用示例
```
bm_convert(source="report.md", format="pdf", template="academic")
```

## 穷尽重试策略
- **穷尽重试替代路径**: 内置公众号排版系统 → pandoc → 手动排版
- **触发条件**: 内置公众号排版系统 服务不可用或转换失败

## MCP 适配
- **MCP Tool 名称**: bm_convert
- **MCP 参数**: source, format, template

## 依赖
- 内置公众号排版系统 服务部署 + pandoc（穷尽重试替代备用）

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