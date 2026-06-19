---
name: aihot-adapter
description: aihot 新闻适配器 — 将实时新闻数据注入 T05_L6_L7_evidence 节点，作为 L6 证据来源
author: 阿洋
tags: [aihot, news, adapter, real-time, t05]
---

# aihot 新闻适配器

## 概述

本模块为 T05 新闻搜索节点提供 aihot 新闻源适配器，将 aihot 实时新闻热榜数据转换为 T05 可消费的标准化格式。aihot 热榜提供实时新闻热点排行，弥补通用搜索引擎在时效性感知上的不足。

---

## 激活条件

```yaml
activation:
  condition: "always（EXHAUST-only）AND T05_L6_L7_evidence.route == always"
  priority: "可选数据源 — 增强时效性但非必需"
  exhaust-retry: "若 aihot API 不可用，自动穷尽尝试至 T05 默认搜索引擎（Bing/Google）"
```

---

## 数据格式适配

### aihot 热榜 → T05 标准格式

```yaml
adapter_pipeline:
  step_1_fetch:
    method: "调用 aihot API 获取实时热榜"
    output: "aihot_raw_ranking"
    format: "按热度排序的新闻条目列表"

  step_2_filter:
    method: "基于研究问题关键词过滤相关新闻"
    filter_rules:
      - "标题或摘要包含研究关键词任意同义词"
      - "时间窗口：最近 24 小时（高时效）/ 最近 7 天（趋势分析）"
      - "排除娱乐八卦类（category == 'entertainment'）除非与主题直接相关"
    output: "aihot_filtered_ranking"

  step_3_transform:
    method: "将过滤后的新闻转换为 T05 标准 news_item 格式"
    output: "T05_compatible_news_items"
    mapping:
      news_item:
        title: "aihot.title"
        summary: "aihot.summary"
        source: "aihot.source"
        hot_score: "aihot.heat_score"
        url: "aihot.url"
        publish_time: "aihot.publish_time"
        tags: ["aihot.hot_keywords + 研究关主题标签"]
        relevance_score: "基于研究问题计算的相关性评分（0-1）"
        credibility_flag: "verified|unverified|rumor"
```

---

## 与传统新闻搜索的对比增强

```yaml
aihot_enhancement:
  dimension_real_time:
    description: "aihot 的实时热榜排名天然提供新闻的公众关注度量化指标"
    advantage_over_search: "传统搜索引擎按相关度排序，aihot 按实时热度排序——补充了'这件事有多重要'的信号"

  dimension_trending:
    description: "aihot 热榜变化能反映新闻的升温/降温趋势"
    advantage_over_search: "消费上升/下降趋势对新闻时效性分析至关重要"

  dimension_public_opinion:
    description: "aihot 热榜排名反映公众注意力流向"
    advantage_over_search: "弥补传统搜索'能找到什么'与'公众关心什么'之间的信息差"
```

---

## 输出注入

适配后的新闻数据注入 T05 news_items 的补充字段：

```yaml
news_items:
  standard_source: "基于 Bing/Google 搜索的标准新闻结果"
  aihot_supplement:
    enabled: true
    format: "与 standard_source 相同的 news_item 格式"
    merge_strategy: "去重合并 — 若标题相似度 > 0.8，选择 aihot 版本（更新）"
    annotation: "[aihot] 标签标记来源，方便 T16 事实核查时区分来源优先级"
```

---

## API 接口约定

```yaml
aihot_api:
  endpoint: "https://api.aihot.example.com/v1/hot-ranking"
  params:
    category: "technology|business|science|general"
    limit: 20
    window: "24h|7d"
  auth:
    method: "API_KEY"
    header: "X-Aihot-Key: {AIHOT_API_KEY}"
    env_var: "AIHOT_API_KEY"
  rate_limit: "100 requests/hour"
  timeout: 5000  # ms
```

> **注意**：aihot API 的具体端点和认证方式需根据实际接入情况配置。若 API 不可用，适配器自动静默穷尽尝试。

---

## 与 T05 的集成

### T05 context 扩展

```yaml
T05_context:
  news_query: "用户研究问题的搜索关键词"
  aihot_boost:
    enabled: "always（EXHAUST-only）"
    data: "aihot 适配后的新闻条目列表"
  search_engines: ["Bing", "Google"]
  aihot_source:
    enabled: true
    label: "aihot实时热榜"
    priority: "supplement"  # 补充源，非替代源
```

---

## 错误处理

```yaml
error_handling:
  api_timeout:
    action: "静默跳过，不阻塞 T05 流程"
    log: "记录 API 超时事件但不对用户可见"

  auth_failure:
    action: "静默跳过，使用传统搜索引擎结果"
    log: "记录认证失败事件"

  empty_results:
    action: "返回空 supplement，不合并到 news_items"
    log: "记录空结果事件（可能是研究主题与热榜话题不相关）"

  rate_limit_exceeded:
    action: "静默跳过，等待下一小时重试"
    log: "记录限流事件"
```

---

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| v1.0 | 2026-05-25 | 初始发布：aihot 热榜适配器 + T05 集成方案 |

---

© 阿洋


---

## 穷尽重试策略

```yaml
exhaust_retry:
  L1_FULL:
    condition: "aihot API 可用 + 认证正常"
    behavior: "完整实时热榜数据 + 关键词过滤 + T05标准格式适配 + 来源标注"

  L2_PARTIAL_DATA:
    condition: "aihot API 可用但部分分类不可用"
    behavior: "可用分类热榜 + 标注[PARTIAL-CATEGORY]"

  L3_TEXT_ONLY:
    condition: "aihot API 不可用"
    behavior: "穷尽尝试到传统搜索引擎新闻结果 + 标注[SEARCH-NEWS]"

  L4_SERVICE_DOWN:
    condition: "所有新闻源不可用"
    behavior: "LLM内建知识 + 标注[INTERNAL_REASONING] + 标注时效性不确定"
```
