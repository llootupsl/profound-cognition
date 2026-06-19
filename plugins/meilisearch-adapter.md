<!-- 作者：阿洋 -->

# Meilisearch Adapter — 跨项目知识复用

## 适配器元数据
- role: 跨项目历史研究知识复用搜索引擎
- endpoint: http://{meilisearch_host}:7700
- api_key: {MASTER_KEY}

## Integration Points（3处集成点）
1. **T01 — 输入分流**：查询历史相似研究，避免重复劳动
2. **T02 — 研究阶段**：检索过往研究的发现、方法、证据链
3. **T21 — 知识回收**：将当前研究成果写入索引供未来复用

## Index Schema（7个索引字段）
| 字段 | 类型 | 说明 |
|------|------|------|
| research_id | string | 研究唯一标识符 |
| topic | string | 研究主题 |
| output_type | enum | research_report/wechat_article/course_material |
| key_findings | [string] | 关键发现列表 |
| methodology | [string] | 使用方法论 |
| evidence_sources | [object] | 证据来源（URL+标题+日期） |
| timestamp | number | 索引时间戳 |

## Ranking Rules（排序规则）
1. `words` — 词频匹配
2. `typo` — 容忍拼写错误（1字符）
3. `proximity` — 词项邻近度

## Hybrid Search（混合搜索方式）
- 关键词搜索（Meilisearch全文索引）
- 向量搜索（通过Qdrant嵌入）
- 融合策略：Reciprocal Rank Fusion (RRF)

## T01调用：相似历史研究查询
```
GET /indexes/research_index/search
{
  "q": "{用户问题}",
  "limit": 5,
  "attributesToRetrieve": ["research_id", "topic", "key_findings", "timestamp"]
}
```

## T21调用：写入研究产出
```
POST /indexes/research_index/documents
{
  "research_id": "{current_uuid}",
  "topic": "{研究主题}",
  "output_type": "{成品类型}",
  "key_findings": [...],
  "methodology": [...],
  "evidence_sources": [...],
  "timestamp": {unix_ts}
}
```

## T02调用：检索历史知识
```
GET /indexes/research_index/search
{
  "q": "{研究子课题}",
  "filter": "output_type = research_report",
  "limit": 10
}
```

---

## 激活条件

```yaml
activation:
  condition: "跨项目历史研究知识复用 AND Meilisearch 服务可用"
  priority: "首选关键词搜索引擎 — 全文索引+容错+排序"
  exhaust-retry: "若 Meilisearch 不可用，穷尽尝试到 Qdrant 语义搜索 → LLM内建知识"
```

---

## 检索策略选择规则

```yaml
search_strategy:
  rule_1_similar_research:
    trigger: "T01 输入分流 — 查询历史相似研究"
    params:
      limit: 5
      attributesToRetrieve: [research_id, topic, key_findings, timestamp]
    reason: "避免重复劳动，复用历史研究"

  rule_2_knowledge_retrieval:
    trigger: "T02 研究阶段 — 检索过往研究的方法和证据链"
    params:
      limit: 10
      filter: "output_type = research_report"
    reason: "深度研究需要历史方法论参考"

  rule_3_cross_project:
    trigger: "跨项目知识复用"
    params:
      limit: 15
      attributesToRetrieve: [research_id, topic, key_findings, methodology, evidence_sources]
    reason: "跨项目复用需要完整方法论和证据链"

  rule_4_recent_first:
    trigger: "需要最新研究参考"
    sort: "timestamp:desc"
    limit: 10
    reason: "时效性需求优先最新研究"
```

---

## 与 profound-cognition Task 节点集成

```yaml
task_integration:
  T01_input_routing:
    trigger: "输入分流 — 查询历史相似研究"
    strategy: "rule_1_similar_research"
    output: "相似历史研究列表注入 T01"
    annotation: "[meilisearch] 标签标记历史研究来源"

  T02_L1_L2_research:
    trigger: "研究底座 — 检索过往研究发现和方法"
    strategy: "rule_2_knowledge_retrieval"
    output: "历史知识注入 T02 事实层"
    annotation: "[meilisearch-knowledge] 标签标记历史知识来源"

  T21_knowledge_recovery:
    trigger: "知识回收 — 将研究成果写入索引"
    strategy: "写入模式"
    output: "研究产出写入 research_index"
    annotation: "[meilisearch-write] 标签标记知识回收写入"
```

---

## 错误处理

```yaml
error_handling:
  service_unavailable:
    action: "穷尽尝试到 Qdrant 语义搜索"
    log: "记录 Meilisearch 服务不可用事件"
    exhaust_retry_chain: "Meilisearch → Qdrant → LLM内建知识"

  query_timeout:
    action: "降低limit重试"
    log: "记录查询超时事件"
    timeout: 10000  # ms

  empty_results:
    action: "返回空结果，不阻塞流程"
    log: "记录空结果事件（可能是新主题无历史研究）"

  write_failure:
    action: "重试1次，若仍失败则记录待写入队列"
    log: "记录写入失败事件"

  auth_failure:
    action: "穷尽尝试到 Qdrant 语义搜索"
    log: "记录认证失败事件"
```

---

## 穷尽重试策略

```yaml
exhaust_retry:
  L1_FULL:
    condition: "Meilisearch 可用 + 全文索引正常"
    behavior: "完整关键词搜索 + 容错 + 排序"

  L2_PARTIAL_DATA:
    condition: "Meilisearch 可用 + 索引不完整"
    behavior: "可用索引搜索 + 标注[PARTIAL-INDEX]"

  L3_TEXT_ONLY:
    condition: "Meilisearch 不可用"
    behavior: "穷尽尝试到 Qdrant 语义搜索 + 标注[SEMANTIC-ONLY]"

  L4_SERVICE_DOWN:
    condition: "所有检索服务不可用"
    behavior: "使用 LLM 内建知识 + 标注[INTERNAL_REASONING]"
```
