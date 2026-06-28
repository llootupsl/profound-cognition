<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

# PaperQA2

## 基本信息
- **卡片编号**: #31
- **类型**: TC
- **优先级**: P2
- **层级**: L1

## 功能描述
PaperQA2 论文问答系统，支持对论文集合进行问答。自动解析论文 PDF、构建索引并执行检索增强问答，提供带引用的精准答案。支持多论文交叉引用和证据链追踪，适用于文献综述、论文深度理解、研究对比分析等场景。

## 调用指令

### 输入参数
- `question` (string, 针对论文集合的提问)
- `papers` (array, 论文文件路径或 DOI 列表)
- `max_results` (integer, 可选: 最大返回结果数，默认 5)

### 输出格式
答案 + 引用（含论文标题、段落、页码）

### 调用示例
```
paperqa2_query(question="Transformer架构在视觉任务中的主要改进方向有哪些？", papers=["10.48550/arXiv.2010.11929", "/papers/vit_survey.pdf"], max_results=5)
```

## 穷尽重试策略
- **穷尽重试替代路径**: PaperQA2 → LightRAG → 关键词搜索
- **触发条件**: PaperQA2 服务不可用或论文解析失败

## MCP 适配
- **MCP Tool 名称**: paperqa2_query
- **MCP 参数**: question, papers, max_results

## 依赖
- PaperQA2 服务部署 + 嵌入模型 + LLM 推理后端

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

暂无显式 DAG 节点消费者。保留待扩展。

## 方法论内化

> ★核心方法论已内化于 knowledge/domains/science-engine.md，以下为快速参考

### 方法论原理
PaperQA2通过RAG+LLM实现论文的自动问答和摘要，解决了研究者面对海量文献时的信息提取效率问题。

### 执行步骤
1. 论文PDF解析
2. 分段+嵌入索引
3. 问题驱动的检索
4. LLM生成答案+引用
5. 答案验证

### 决策规则
| 条件 | 动作 |
|------|------|
| 需要论文深度问答 | PaperQA2 |
| 需要快速摘要 | GPT-Researcher |
| 无API | 手动阅读 |

### 输出规范
```yaml
paperqa2_output:
  available: bool
  answer: str
  citations: list
  confidence: float
  degradation_note: str
```

### 穷尽重试策略
| 级别 | 方案 |
|------|------|
| L1 | PaperQA2完整RAG问答 |
| L2 | GPT-Researcher(简化检索) |
| L3 | 关键词搜索 |
| L4 | 手动阅读 |


## 效果度量

| 度量指标 | 定义 | 目标值 |
|----------|------|--------|
| 执行成功率 | 成功调用次数 / 总调用次数 | ≥ 0.95 |
| 平均延迟 | 单次调用平均耗时 | ≤ 5s |
| 输出质量分 | Supervisor 评分（0-1） | ≥ 0.8 |
| 穷尽重试触发率 | 触发降级的调用次数 / 总调用次数 | ≤ 0.1 |

效果度量写入 NRSF，供 T19 质量检查消费。