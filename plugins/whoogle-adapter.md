<!-- 作者：阿洋 -->

# Whoogle Adapter — 隐私搜索代理

## 适配器元数据
- role: 隐私搜索代理，无追踪的Google搜索结果
- activation: 与SearXNG互补的轻量级搜索
- endpoint: http://{whoogle_host}:5000/search

## Endpoint Configuration
```
GET /search?q={query}&language=lang_zh&safesearch=0
```

## 与SearXNG对比表

| 特性 | Whoogle | SearXNG |
|------|---------|---------|
| 引擎聚合 | 仅Google（可配） | 多引擎聚合 |
| 部署复杂度 | 极简（单容器） | 中等（需配置多引擎） |
| 资源占用 | 约100MB RAM | 约300MB RAM |
| 定制能力 | 低（样式/语言） | 高（引擎/权重/缓存） |
| 适用场景 | 快速Google隐私搜索 | 全功能元搜索 |
| 隐私保证 | 无JS/Cookie/追踪 | 无追踪+IP隐藏 |

## Integration Strategy
- SearXNG作为首选元搜索聚合层
- Whoogle作为快速Google查询的轻量级替代
- T06反事实搜索时使用Whoogle快速验证
- 两个服务同时不可用 → 穷尽尝试到LLM内建知识

---

## 激活条件

```yaml
activation:
  condition: "需要Google搜索结果 AND SearXNG不可用 或 快速Google隐私查询"
  priority: "轻量级替代 — SearXNG不可用时的Google隐私搜索"
  exhaust-retry: "若 Whoogle 不可用，穷尽尝试到 DuckDuckGo → LLM内建知识"
```

---

## 搜索策略规则

```yaml
search_strategy:
  rule_1_quick_google:
    trigger: "需要快速Google搜索结果（SearXNG不可用时）"
    params:
      language: "lang_zh"
      safesearch: 0
    reason: "Whoogle提供无追踪的Google搜索，部署简单"

  rule_2_privacy_first:
    trigger: "用户要求隐私保护搜索"
    params:
      language: "lang_zh"
      safesearch: 0
      near: "移除位置信息"
    reason: "Whoogle核心优势是隐私保护"

  rule_3_counterfactual:
    trigger: "T06反事实搜索需要快速验证"
    params:
      language: "lang_zh"
      safesearch: 0
    reason: "轻量级快速验证，不占用SearXNG资源"
```

---

## 与 profound-cognition Task 节点集成

```yaml
task_integration:
  T02_L1_L2_research:
    trigger: "SearXNG不可用时的研究底座搜索"
    strategy: "rule_1_quick_google"
    output: "搜索结果注入 T02 事实层"
    annotation: "[whoogle] 标签标记搜索来源"

  T05_L6_L7_evidence:
    trigger: "证据验证 — 快速Google验证"
    strategy: "rule_1_quick_google"
    output: "验证结果注入 T05 证据层"
    annotation: "[whoogle-verify] 标签标记验证来源"

  T06_counterfactual:
    trigger: "反事实搜索 — 快速验证"
    strategy: "rule_3_counterfactual"
    output: "反事实证据注入 T06"
    annotation: "[whoogle-counterfactual] 标签标记来源"
```

---

## 错误处理

```yaml
error_handling:
  service_unavailable:
    action: "穷尽尝试到 DuckDuckGo API"
    log: "记录 Whoogle 服务不可用事件"
    exhaust_retry_chain: "Whoogle → DuckDuckGo → LLM内建知识+[INTERNAL_REASONING]"

  timeout:
    action: "重试1次，若仍超时则穷尽尝试"
    log: "记录超时事件"
    timeout: 8000  # ms

  empty_results:
    action: "穷尽尝试到 DuckDuckGo 搜索"
    log: "记录空结果事件"

  captcha:
    action: "穷尽尝试到 DuckDuckGo 搜索"
    log: "记录Google验证码事件"
```

---

## 穷尽重试策略

```yaml
exhaust_retry:
  L1_FULL:
    condition: "Whoogle 服务可用"
    behavior: "完整Google隐私搜索 + 无追踪"

  L2_PARTIAL_DATA:
    condition: "Whoogle 可用但结果不完整"
    behavior: "返回可用结果 + DuckDuckGo补充"

  L3_TEXT_ONLY:
    condition: "Whoogle 不可用"
    behavior: "穷尽尝试到 DuckDuckGo API + 标注[INTERNAL_REASONING]"

  L4_SERVICE_DOWN:
    condition: "所有搜索服务不可用"
    behavior: "使用 LLM 内建知识 + 标注[INTERNAL_REASONING]"
```
