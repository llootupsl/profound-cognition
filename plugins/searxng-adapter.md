<!-- 作者：阿洋 -->

# SearXNG Adapter — 元搜索聚合层

## 适配器元数据
- role: 元搜索聚合引擎，聚合多个搜索引擎结果
- activation: T02/T05/T06 搜索步骤优先调用
- endpoint: http://{searxng_host}:{port}/search

## Multi-Engine Strategy（多引擎聚合策略）

### 策略1: 学术研究（research_report）
- engines: [arxiv, google_scholar, pubmed, crossref, semantic_scholar]
- category: academic

### 策略2: 综合信息（通用）
- engines: [google, duckduckgo, bing, wikipedia, wikidata]
- category: general

### 策略3: 新闻时事
- engines: [google_news, bing_news, newsapi]
- category: news

### 策略4: 技术交叉验证
- engines: [github, stackoverflow, techcrunch, reddit, hackernews]
- category: tech

## Result Deduplication（结果去重规则）
1. URL规范化：去除协议前缀、www子域、尾部斜杠
2. 标题相似度：Levenshtein距离 > 0.85视为重复
3. 内容片段哈希：取前200字符的SimHash比较
4. 跨引擎去重：保留来自最多引擎的结果（加权排序）

## Source Annotation（来源标注格式）
每项搜索结果标注：
```
[来源: {引擎} | {URL} | {标题} | {日期} | {相关性评分}/10]
```

## Privacy Guarantee
- SearXNG部署于本地/内网，不向外部引擎发送用户IP
- 查询词自动脱敏（移除PII）
- 无Cookie追踪
- 搜索结果缓存时间：24h（减少外部请求）

## Exhaust-Retry Strategy（穷尽尝试策略）
1. SearXNG不可用 → 穷尽尝试到单引擎直接搜索（Google优先）
2. 学术引擎不可用 → 穷尽尝试到通用引擎 + arxiv API单独调用
3. 全部不可用 → 使用LLM内建知识 + 标注[INTERNAL_REASONING]
4. 部分引擎超时 → 跳过超时引擎，合并其余结果

---

## 激活条件

```yaml
activation:
  condition: "T02/T05/T06 搜索步骤 AND SearXNG 服务可用"
  priority: "首选元搜索聚合层 — 多引擎聚合+去重+隐私保护"
  exhaust-retry: "若 SearXNG 不可用，穷尽尝试到单引擎直接搜索（Google优先）"
```

---

## 搜索策略选择决策树

```yaml
strategy_selection:
  Q1_产品类型:
    research_report:
      strategy: "策略1 学术研究"
      engines: [arxiv, google_scholar, pubmed, crossref, semantic_scholar]
      reason: "研究报告需要学术文献支撑"
    wechat_article:
      strategy: "策略2 综合信息"
      engines: [google, duckduckgo, bing, wikipedia, wikidata]
      reason: "公众号文章需要通俗易懂的综合信息"
    course_material:
      strategy: "策略1+2 混合"
      engines: [arxiv, google_scholar, google, wikipedia, wikidata]
      reason: "课程材料需要学术+通俗双源"

  Q2_搜索意图:
    事实验证:
      strategy: "策略2 综合信息"
      reason: "事实验证需要多源交叉确认"
    深度研究:
      strategy: "策略1 学术研究"
      reason: "深度研究需要学术文献"
    时效性:
      strategy: "策略3 新闻时事"
      reason: "时效性需求需要新闻源"
    技术实现:
      strategy: "策略4 技术交叉验证"
      reason: "技术问题需要开发者社区源"

  Q3_搜索深度:
    L1_基础事实:
      max_results: 10
      dedup_threshold: 0.85
    L2_因果链:
      max_results: 20
      dedup_threshold: 0.80
    L3-L7:
      max_results: 30
      dedup_threshold: 0.75
```

---

## 与 profound-cognition Task 节点集成

```yaml
task_integration:
  T02_L1_L2_research:
    trigger: "研究底座事实收集阶段"
    strategy: "策略1或策略2（按产品类型选择）"
    output: "research_items 注入 T02 事实层"
    annotation: "[searxng] 标签标记搜索来源"

  T05_L6_L7_evidence:
    trigger: "证据验证阶段"
    strategy: "策略2 综合信息（多源交叉验证）"
    output: "evidence_items 注入 T05 证据层"
    annotation: "[searxng-verify] 标签标记验证来源"

  T06_counterfactual:
    trigger: "反事实搜索阶段"
    strategy: "策略2+4 混合（综合+技术）"
    output: "counterfactual_evidence 注入 T06"
    annotation: "[searxng-counterfactual] 标签标记反事实来源"
```

---

## 错误处理

```yaml
error_handling:
  service_unavailable:
    action: "穷尽尝试到单引擎直接搜索（Google优先）"
    log: "记录 SearXNG 服务不可用事件"
    exhaust_retry_chain: "SearXNG → Google → DuckDuckGo → LLM内建知识+[INTERNAL_REASONING]"

  engine_timeout:
    action: "跳过超时引擎，合并其余引擎结果"
    log: "记录引擎超时事件，标注 timeout_engine={engine_name}"
    timeout: 10000  # ms

  rate_limit:
    action: "指数退避重试（1s→2s→4s），穷尽重试直至成功"
    log: "记录限流事件"

  empty_results:
    action: "切换搜索策略重试（如从学术切换到综合）"
    log: "记录空结果事件，标注 query={query}"

  dedup_failure:
    action: "跳过去重，返回原始合并结果"
    log: "记录去重失败事件"
```

---

## 穷尽重试策略

```yaml
exhaust_retry:
  L1_FULL:
    condition: "SearXNG 可用 + 所有引擎正常"
    behavior: "完整多引擎聚合 + 去重 + 来源标注"

  L2_PARTIAL_DATA:
    condition: "SearXNG 可用 + 部分引擎超时/不可用"
    behavior: "可用引擎聚合 + 标注缺失引擎 + 降低去重阈值"

  L3_TEXT_ONLY:
    condition: "SearXNG 不可用"
    behavior: "穷尽尝试到单引擎搜索（Google/DuckDuckGo）+ 标注[SINGLE-ENGINE]"

  L4_SERVICE_DOWN:
    condition: "所有搜索引擎不可用"
    behavior: "使用 LLM 内建知识 + 标注[INTERNAL_REASONING] + 建议用户手动搜索"
```
