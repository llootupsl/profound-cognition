<!-- 作者：阿洋 -->

# Qdrant Adapter — 语义向量检索

## 适配器元数据
- role: 语义向量检索引擎，支持稀疏+稠密向量混合搜索
- embedding_model: text-embedding-3-large（1536维）
- endpoint: http://{qdrant_host}:6333

## Collection Structure（集合结构）

### collection: research_facts
- vector_size: 1536
- distance: Cosine
- payload_schema:
  - fact_id: uuid
  - text: string（事实原文）
  - source: string（来源URL）
  - confidence: float（置信度 0-1）
  - evidence_level: enum（L0-L3）
  - research_id: string
  - node_id: string（产出该事实的DAG节点）

### collection: inference_chains
- vector_size: 1536
- distance: Cosine
- payload_schema:
  - chain_id: uuid
  - premises: [string]（前提列表）
  - conclusion: string（结论）
  - chain_type: enum（deductive/inductive/abductive）
  - strength: float（推理强度 0-1）
  - research_id: string
  - node_id: string

## Integration Points（3处集成点）
1. **T02-T06 研究阶段**：语义检索补充关键词搜索
2. **T13 认知综合**：检索相关推理链辅助综合
3. **T21 知识回收**：向量化并写入研究产出

## Hybrid Search Parameters
```
{
  "vector": {embeddings},
  "sparse_vector": {sparse_embeddings},
  "fusion": "rrf",
  "limit": 20
}
```

## T02-T06调用方式
1. 对用户问题的每个子维度生成语义查询
2. 调用 Qdrant search（research_facts 集合）
3. 调用 Qdrant search（inference_chains 集合）
4. 融合结果（RRF权重：facts 0.7, chains 0.3）

## T21调用方式
1. 将T17事实核查通过的事实写入 research_facts
2. 将T09认知推理的推理链写入 inference_chains
3. 每项含完整 payload 元数据

---

## 激活条件

```yaml
activation:
  condition: "语义向量检索需求 AND Qdrant 服务可用"
  priority: "首选语义检索引擎 — 稀疏+稠密向量混合搜索"
  exhaust-retry: "若 Qdrant 不可用，穷尽尝试到 Meilisearch 关键词搜索 → LLM内建知识"
```

---

## 检索策略选择规则

```yaml
search_strategy:
  rule_1_fact_retrieval:
    trigger: "需要检索具体事实（T02/T05阶段）"
    collection: "research_facts"
    fusion: "rrf"
    limit: 20
    rrf_weights:
      facts: 0.7
      chains: 0.3
    reason: "事实检索优先使用research_facts集合"

  rule_2_chain_retrieval:
    trigger: "需要检索推理链（T09/T13阶段）"
    collection: "inference_chains"
    fusion: "rrf"
    limit: 15
    reason: "推理链检索使用inference_chains集合"

  rule_3_hybrid_retrieval:
    trigger: "需要综合检索事实+推理链"
    collections: [research_facts, inference_chains]
    fusion: "rrf"
    limit: 25
    rrf_weights:
      facts: 0.6
      chains: 0.4
    reason: "综合检索同时查询两个集合"

  rule_4_evidence_level_filter:
    trigger: "需要高置信度事实"
    collection: "research_facts"
    filter: "evidence_level >= L1"
    limit: 10
    reason: "高置信度需求过滤低级别证据"
```

---

## 与 profound-cognition Task 节点集成

```yaml
task_integration:
  T02_L1_L2_research:
    trigger: "研究底座 — 语义检索补充关键词搜索"
    strategy: "rule_1_fact_retrieval"
    output: "语义检索结果补充 T02 事实层"
    annotation: "[qdrant] 标签标记语义检索来源"

  T09_cog_reason:
    trigger: "认知推理 — 检索相关推理链辅助推理"
    strategy: "rule_2_chain_retrieval"
    output: "推理链注入 T09 推理过程"
    annotation: "[qdrant-chain] 标签标记推理链来源"

  T13_cog_synthesize:
    trigger: "认知综合 — 检索相关推理链辅助综合"
    strategy: "rule_3_hybrid_retrieval"
    output: "综合检索结果注入 T13"
    annotation: "[qdrant-hybrid] 标签标记综合检索来源"

  T21_knowledge_recovery:
    trigger: "知识回收 — 向量化并写入研究产出"
    strategy: "写入模式"
    output: "事实和推理链写入对应集合"
    annotation: "[qdrant-write] 标签标记知识回收写入"
```

---

## 错误处理

```yaml
error_handling:
  service_unavailable:
    action: "穷尽尝试到 Meilisearch 关键词搜索"
    log: "记录 Qdrant 服务不可用事件"
    exhaust_retry_chain: "Qdrant → Meilisearch → LLM内建知识"

  query_timeout:
    action: "降低limit重试，若仍超时则穷尽尝试"
    log: "记录查询超时事件"
    timeout: 15000  # ms

  empty_results:
    action: "穷尽尝试到 Meilisearch 关键词搜索"
    log: "记录空结果事件"

  embedding_failure:
    action: "穷尽重试到纯稀疏向量搜索"
    log: "记录嵌入失败事件"

  write_failure:
    action: "跳过失败条目，继续写入其余条目"
    log: "记录写入失败事件，标注 failed_item_id={id}"
```

---

## 穷尽重试策略

```yaml
exhaust_retry:
  L1_FULL:
    condition: "Qdrant 可用 + 混合搜索正常"
    behavior: "稀疏+稠密向量混合搜索 + RRF融合"

  L2_PARTIAL_DATA:
    condition: "Qdrant 可用 + 嵌入模型不可用"
    behavior: "纯稀疏向量搜索 + 标注[SPARSE-ONLY]"

  L3_TEXT_ONLY:
    condition: "Qdrant 不可用"
    behavior: "穷尽尝试到 Meilisearch 关键词搜索 + 标注[KEYWORD-ONLY]"

  L4_SERVICE_DOWN:
    condition: "所有检索服务不可用"
    behavior: "使用 LLM 内建知识 + 标注[INTERNAL_REASONING]"
```
