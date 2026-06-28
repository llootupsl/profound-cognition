<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

# PaperQA2

## 基本信息
- **卡片编号**: PaperQA2（学术论文 RAG 检索与综述自动生成器）
- **类型**: TC（学术研究工具）
- **优先级**: P1
- **层级**: L1
- **版本同步**: 与官方 paperqa 库（https://github.com/Future-House/paper-qa）同步
- **关联卡片**: `knowledge/external-capabilities/TC-031-PaperQA2.md`（基础问答能力卡）

## 功能描述
学术论文 RAG 检索与综述自动生成工具。基于 PaperQA2 RAG 引擎对论文全文进行向量索引，支持引用网络遍历与综述自动生成。PaperQA2 由 Future House 开发，是学术论文问答领域 SOTA 系统，在 PaperQA benchmark 上达到 71% 准确率（超越人类专家平均水平）。本卡片在基础问答能力（TC-031）之上，扩展文献综述自动化能力，服务于 T02 文献检索、T03-T06 深度分析、T15 领域分析等节点。

## 核心能力
- **论文全文向量索引**：对论文 PDF 全文进行分段、嵌入、索引，支持全文检索和语义检索
- **引用网络遍历**：从种子论文追踪引用（references）和被引（cited-by），支持多跳引用遍历（最多 3 跳）
- **综述自动生成**：基于检索结果自动生成领域文献综述，包含研究脉络、关键论文、研究空白
- **RAG 问答**：问题驱动的检索增强问答，提供带引用的精准答案

## 调用前置条件
- Python 3.9+
- paperqa 库已安装（`pip install paperqa`）
- 嵌入模型（默认 OpenAI text-embedding-3-small，可替换为本地模型）
- LLM 推理后端（用于答案生成与综述生成）
- 论文 PDF 来源：arXiv API / Semantic Scholar API / 本地 PDF 文件

## 调用指令

### 输入参数
- `query` (string, 检索/问答查询)
- `seed_papers` (array, 可选: 种子论文列表，DOI/arXiv ID/文件路径)
- `max_papers` (integer, 可选: 最大检索论文数，默认 20)
- `citation_depth` (integer, 可选: 引用网络遍历深度，默认 1，最大 3)
- `generate_review` (boolean, 可选: 是否生成文献综述，默认 false)

### 输出格式
```yaml
paperqa_output:
  available: boolean
  papers_retrieved:
    - paper_id: "string（DOI/arXiv ID）"
      title: "string"
      abstract: "string"
      relevance_score: float
      citation_context: "string（引用上下文）"
  citation_network:
    nodes: integer
    edges: integer
    depth: integer
    key_clusters: [string]
  review_summary: "string（综述摘要，generate_review=true 时输出）"
  answer: "string（RAG 问答答案）"
  citations: list
  confidence: float
  degradation_note: "string（降级说明，正常为空）"
```

### 调用示例
```
paperqa2.retrieve(
  query="Transformer架构在视觉任务中的主要改进方向",
  seed_papers=["10.48550/arXiv.2010.11929"],
  max_papers=20,
  citation_depth=2,
  generate_review=true
)
```

## 失败回退策略
- **穷尽重试替代路径**: PaperQA2 → SearXNG + 人工筛选 → 关键词搜索
- **触发条件**: paperqa 库不可用 / 嵌入模型不可用 / LLM 推理后端不可用 / 论文 PDF 解析失败
- **回退行为**: 回退到 SearXNG + 人工筛选模式，通过 SearXNG 学术引擎策略（arxiv, google_scholar, semantic_scholar）检索论文，由执行者人工筛选与综述

## 效果度量
- **papers_retrieved** (integer)：检索到的相关论文数量
- **citation_coverage** (float)：引用网络覆盖率，已遍历引用数 / 总引用数，[0.0, 1.0]
- **review_quality** (string)：综述质量评级，A/B/C/D
  - A: 覆盖研究脉络 + 关键论文 + 研究空白，引用 ≥ 10 篇
  - B: 覆盖研究脉络 + 关键论文，引用 ≥ 5 篇
  - C: 覆盖关键论文，引用 ≥ 3 篇
  - D: 综述不完整或引用 < 3 篇

## MCP 适配
- **MCP Tool 名称**: paperqa2_retrieve
- **MCP 参数**: query, seed_papers, max_papers, citation_depth, generate_review

## 依赖
- paperqa 库（官方实现）
- 嵌入模型（OpenAI / 本地模型）
- LLM 推理后端（用于答案生成与综述生成）
- 论文 PDF 来源：arXiv API / Semantic Scholar API / 本地 PDF

## 消费关系

### 消费此卡片的领域引擎
暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

| 节点 | 用途 |
|------|------|
| T02 | PaperQA2 检索（论文全文向量索引 + 引用网络遍历） |
| T03 | PaperQA2 查询（L3 结构变量分析的论文段落检索） |
| T04 | PaperQA2 查询（L4 比较参照案例的论文检索） |
| T05 | PaperQA2 查询（L6 证据账本的论文证据检索） |
| T06 | PaperQA2 查询（L8 反事实推演的论文先例检索） |
| T15 | PaperQA2 文献综述（领域文献综述自动生成） |

## 与 SearXNG 适配器的关系
PaperQA2 专注于学术论文 RAG 检索，SearXNG 专注于通用网络搜索。两者互补：
- PaperQA2 优先用于学术论文全文检索与综述生成
- SearXNG 用于非学术来源（新闻、报告、网页）的检索
- PaperQA2 不可用时回退到 SearXNG 学术引擎策略

## 与现有 TC-031-PaperQA2.md 的关系
本卡片（`PaperQA2.md`）是 TC-031-PaperQA2.md 的扩展版，新增以下能力：
- 引用网络遍历（references + cited-by，多跳遍历）
- 综述自动生成（研究脉络 + 关键论文 + 研究空白）
- 文献检索流程定义（种子论文 → 向量索引 → 检索）
- NRSF 检索日志格式

TC-031-PaperQA2.md 保留为基础问答能力卡（question + papers → answer + citations），本卡片扩展为完整的文献综述自动化能力卡。
