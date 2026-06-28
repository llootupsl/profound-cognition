<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

# GPT-Researcher

## 基本信息

> ★核心方法论已内化于 knowledge/domains/science-engine.md，本文件仅作快速引用入口

- **卡片编号**: #30
- **类型**: TC
- **优先级**: P2
- **层级**: L0

## 功能描述
GPT-Researcher 自动研究代理，支持自主搜索和报告生成。自动分解研究问题、并行执行多源搜索、提取和整合信息，生成结构化研究报告。支持自定义报告类型（研究报告/资源摘要/大纲）和来源限制，适用于自动化调研、竞品分析、行业研究等场景。

## 调用指令

### 输入参数
- `query` (string, 研究问题或主题)
- `report_type` (string, 可选: 报告类型 research_report/resource_report/outline，默认 research_report)
- `source_urls` (array, 可选: 限定搜索来源 URL 列表)

### 输出格式
研究报告 Markdown 文档，含引用来源

### 调用示例
```
gpt_researcher_query(query="2026年全球AI芯片市场格局分析", report_type="research_report", source_urls=["https://example.com/ai-chips"])
```

## 穷尽重试策略
- **穷尽重试替代路径**: GPT-Researcher → 手动搜索+综合
- **触发条件**: GPT-Researcher 服务不可用或搜索源全部失效

## MCP 适配
- **MCP Tool 名称**: gpt_researcher_query
- **MCP 参数**: query, report_type, source_urls

## 依赖
- GPT-Researcher 服务部署 + LLM 推理后端 + 搜索引擎 API

## 消费关系

### 消费此卡片的领域引擎

| 引擎名称 | 激活条件 | 使用方式 |
|---------|---------|---------|
| science-engine | on-demand | 文献检索、实验方案设计、多源证据综合 |

### 消费此卡片的 DAG 节点

暂无显式 DAG 节点消费者。


## 效果度量

| 度量指标 | 定义 | 目标值 |
|----------|------|--------|
| 执行成功率 | 成功调用次数 / 总调用次数 | ≥ 0.95 |
| 平均延迟 | 单次调用平均耗时 | ≤ 5s |
| 输出质量分 | Supervisor 评分（0-1） | ≥ 0.8 |
| 穷尽重试触发率 | 触发降级的调用次数 / 总调用次数 | ≤ 0.1 |

效果度量写入 NRSF，供 T19 质量检查消费。