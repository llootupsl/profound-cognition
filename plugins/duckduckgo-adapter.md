<!-- 作者：阿洋 -->

# DuckDuckGo 适配器 (DuckDuckGo Adapter)

> 工具: DuckDuckGo Instant Answer API
> 类型: 即时搜索
> 配置: 零配置、零 API Key

## 搜索端点
- 主端点: https://api.duckduckgo.com/
- 参数: q=查询词&format=json&no_html=1&skip_disambig=1

## 结果类型
- Abstract: 主题摘要
- RelatedTopics: 相关主题
- Infobox: 信息框（结构化数据）

## 使用策略
- 适合快速事实查询（日期、定义、统计数据）
- 不适合深度研究（结果深度有限）
- 作为 SearXNG 的补充，优先用于即时事实验证

---

## 激活条件

```yaml
activation:
  condition: "快速事实查询 AND SearXNG 不可用或作为补充"
  priority: "补充 — 即时事实验证，优先级低于 SearXNG"
  exhaust-retry: "若 DuckDuckGo API 不可用，穷尽尝试到 Whoogle → LLM内建知识"
```

---

## 查询策略规则

```yaml
query_strategy:
  rule_1_fact_check:
    trigger: "需要快速验证事实（日期、定义、统计数据）"
    params:
      skip_disambig: 1
      no_html: 1
    expected_types: [Abstract, Infobox]
    reason: "即时答案API适合快速事实查询"

  rule_2_concept_explore:
    trigger: "需要了解概念概览"
    params:
      skip_disambig: 0
      no_html: 1
    expected_types: [Abstract, RelatedTopics]
    reason: "保留消歧页帮助概念探索"

  rule_3_supplement:
    trigger: "SearXNG 结果不足，需要补充来源"
    params:
      skip_disambig: 1
      no_html: 1
    expected_types: [Abstract, RelatedTopics, Infobox]
    reason: "作为补充来源扩展搜索覆盖"
```

---

## 与 profound-cognition Task 节点集成

```yaml
task_integration:
  T02_L1_L2_research:
    trigger: "研究底座事实收集 — SearXNG结果不足时补充"
    strategy: "rule_3_supplement"
    output: "补充事实条目注入 T02"
    annotation: "[duckduckgo] 标签标记补充来源"

  T05_L6_L7_evidence:
    trigger: "证据验证 — 快速事实验证"
    strategy: "rule_1_fact_check"
    output: "事实验证结果注入 T05"
    annotation: "[duckduckgo-verify] 标签标记验证来源"

  T06_counterfactual:
    trigger: "反事实搜索 — 概念边界探索"
    strategy: "rule_2_concept_explore"
    output: "概念消歧结果注入 T06"
    annotation: "[duckduckgo-explore] 标签标记探索来源"
```

---

## 错误处理

```yaml
error_handling:
  api_timeout:
    action: "穷尽尝试到 Whoogle 搜索"
    log: "记录 DuckDuckGo API 超时事件"
    timeout: 5000  # ms

  empty_results:
    action: "返回空结果，不阻塞流程"
    log: "记录空结果事件"

  rate_limit:
    action: "等待后重试（间隔5秒）"
    log: "记录限流事件"

  api_error:
    action: "穷尽尝试到 Whoogle → LLM内建知识"
    log: "记录API错误事件，标注 error_code={code}"
```

---

## 穷尽重试策略

```yaml
exhaust_retry:
  L1_FULL:
    condition: "DuckDuckGo API 可用"
    behavior: "完整即时答案 + 相关主题 + 信息框"

  L2_PARTIAL_DATA:
    condition: "DuckDuckGo API 部分结果类型缺失"
    behavior: "返回可用结果类型 + 标注缺失类型"

  L3_TEXT_ONLY:
    condition: "DuckDuckGo API 不可用"
    behavior: "穷尽尝试到 Whoogle/LLM内建知识 + 标注[INTERNAL_REASONING]"

  L4_SERVICE_DOWN:
    condition: "所有搜索服务不可用"
    behavior: "使用 LLM 内建知识 + 标注[INTERNAL_REASONING]"
```
