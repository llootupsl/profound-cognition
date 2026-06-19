<!-- 作者：阿洋 -->

# 搜索聚合策略

## 激活条件

```yaml
activation:
  condition: "T02/T05/T06 搜索阶段 AND 需要多引擎聚合"
  trigger_rules:
    - "单一引擎搜索结果不足"
    - "需要多源交叉验证"
    - "研究问题涉及多个领域"
    - "需要权威性排序"
  priority: "必需 — 多引擎聚合是搜索质量的核心保障"
```

---

## 1. 多引擎聚合

### 1.1 聚合流程
1. 并行发送查询到多个搜索引擎
2. 收集所有结果
3. URL 级别去重
4. 质量评分排序
5. 返回 Top-N 结果

### 1.2 质量评分公式
```
quality_score = domain_authority * 0.4 + content_relevance * 0.3 + timeliness * 0.3
```

### 1.3 域名权威度评分
| 域名类别 | 权威度 |
|---------|--------|
| .edu / .gov / .org | 0.9 |
| 知名媒体 (reuters.com, bbc.com 等) | 0.8 |
| 学术平台 (arxiv.org, semanticscholar.org 等) | 0.9 |
| 行业报告 | 0.7 |
| 博客/个人网站 | 0.4 |
| 社交媒体 | 0.3 |

### 1.4 聚合决策树

```yaml
aggregation_decision_tree:
  Q1_引擎可用性:
    all_available: "SearXNG + Whoogle + DuckDuckGo + Firecrawl → 全引擎聚合"
    partial_available: "可用引擎聚合 + 标注缺失引擎"
    single_available: "单引擎搜索 + 标注[SINGLE-ENGINE]"
    none_available: "LLM内建知识 + 标注[INTERNAL_REASONING]"

  Q2_查询类型:
    academic: "SearXNG学术策略 + arxiv API + Google Scholar"
    news: "SearXNG新闻策略 + aihot热榜"
    technical: "SearXNG技术策略 + GitHub + StackOverflow"
    general: "SearXNG综合策略 + Whoogle补充"

  Q3_结果数量:
    abundant: "> 50条 → 严格去重 + 权威性排序 + Top-20"
    adequate: "10-50条 → 标准去重 + 质量排序 + Top-15"
    scarce: "< 10条 → 宽松去重 + 扩展查询 + 全部保留"
    empty: "0条 → 查询重写 + 引擎切换 + 重试"
```

### 1.5 引擎共识加成

```yaml
engine_consensus_bonus:
  description: "被多个引擎同时返回的结果具有更高可信度"
  formula: "final_score = authority_weight * relevance_score * recency_factor * consensus_bonus"
  bonus_levels:
    N_ge_3: "+0.3  # 3个以上引擎同时返回"
    N_eq_2: "+0.15  # 2个引擎同时返回"
    N_eq_1: "0  # 仅1个引擎返回"
```

---

## 2. 查询重写

### 2.1 多角度重写
将原始查询重写为 3-5 个不同角度的子查询：
- 直接查询：原始查询
- 反面查询：NOT {关键词}
- 专家视角：从领域专家角度提问
- 边界查询：{关键词} 的局限/边界/例外

### 2.2 STORM 多视角提问
从不同专家视角生成提问：
- 支持者视角：为什么这个观点是对的？
- 反对者视角：为什么这个观点是错的？
- 中立者视角：这个观点的适用边界是什么？

> 详细查询重写策略见 strategies/query-rewriting.md

---

## 3. 去重与标注

### 3.1 三级去重规则

```yaml
dedup_rules:
  level_1_url:
    method: "URL完全匹配去重"
    rule: "相同URL只保留一条，保留最先返回的结果"
    annotation: "标注重复来源数"

  level_2_title:
    method: "标题相似度去重"
    rule: "Levenshtein/Jaccard相似度 > 0.8的结果合并"
    strategy: "保留更完整的结果"

  level_3_content:
    method: "正文前200字相似度去重"
    rule: "相似度 > 0.7 → 标记为'可能重复'"
    strategy: "保留两者但降权（权重 * 0.7）"
```

### 3.2 来源标注
每条搜索结果标注：
- 来源引擎（SearXNG/Whoogle/DuckDuckGo/LLM）
- 搜索时间
- 质量评分
- 引擎共识数（被几个引擎同时返回）
- 权威度等级（1-5）

---

## 4. 三角验证

### 4.1 验证规则
- 关键事实必须 >= 2 个独立来源支持
- 权威度评分：来源权威度加权平均
- 跨国/跨语言对比验证：重要论断需跨语言来源验证

### 4.2 验证流程
1. 提取关键事实
2. 为每个事实搜索独立来源
3. 计算三角验证通过率
4. 未通过的事实标注 [未验证]

> 详细三角验证策略见 strategies/triangulation.md

---

## 5. 迭代补缺搜索

### 5.1 补缺触发条件

```yaml
gap_trigger:
  rule_1_nrsf_gap:
    condition: "NRSF中存在未闭合论证链"
    action: "针对缺口生成定向查询"

  rule_2_low_triangulation:
    condition: "三角验证通过率 < 0.70"
    action: "为未验证论断搜索补充来源"

  rule_3_source_monopoly:
    condition: "某个论断仅有一个来源支持"
    action: "搜索独立来源进行交叉验证"

  rule_4_counterfactual_missing:
    condition: "缺少反面证据"
    action: "执行反事实查询"
```

### 5.2 补缺执行流程

```yaml
gap_search_flow:
  step_1_identify:
    method: "从NRSF中识别未闭合论证链"
    output: "gap_list"

  step_2_generate_queries:
    method: "针对每个缺口生成定向查询"
    output: "gap_queries"

  step_3_execute:
    method: "执行搜索并收集结果"
    output: "gap_results"

  step_4_inject:
    method: "搜索结果追加到NRSF对应节"
    output: "updated_nrsf"

  step_5_check:
    method: "检查缺口是否闭合"
    condition: "缺口闭合或质量达标（穷尽重试，不设轮数上限）"
```

---

## 6. 搜索量化标准

```yaml
search_quantitative_standards:
  T02_L1_L2:
    min_search_rounds: 3
    min_sources: 24
    min_source_types: 4
    description: "研究底座事实收集"

  T03_L3:
    min_search_rounds: 3
    min_sources: 15
    min_source_types: 3
    description: "结构变量分析"

  T04_L4_L5:
    min_search_rounds: 3
    min_sources: 15
    min_source_types: 3
    description: "利益相关者+情景分析"

  T05_L6_L7:
    min_search_rounds: 3
    min_sources: 24
    min_source_types: 4
    description: "证据边界层"

  T06_L8_L9:
    min_search_rounds: 3
    min_sources: 9
    min_source_types: 2
    description: "反事实搜索"

  I01_supplementary:
    min_search_rounds: 3
    min_sources: 15
    min_source_types: 3
    description: "补研"

  T20_supplementary:
    min_search_rounds: 2
    min_sources: 4
    min_source_types: 1
    description: "输出补研"
```

---

## 7. 与 profound-cognition Task 节点集成

```yaml
task_integration:
  T02_L1_L2_research:
    trigger: "研究底座事实收集"
    strategy: "全引擎聚合 + Perplexica重写 + 三角验证"
    min_sources: 24
    annotation: "[search-aggregation] 标签标记聚合来源"

  T03_L3_structure:
    trigger: "结构变量分析"
    strategy: "学术引擎聚合 + 比较角度重写"
    min_sources: 15
    annotation: "[search-aggregation-structure] 标签标记"

  T05_L6_L7_evidence:
    trigger: "证据验证"
    strategy: "全引擎聚合 + 反面重写 + 三角验证"
    min_sources: 24
    annotation: "[search-aggregation-evidence] 标签标记"

  T06_L8_L9_counterfactual:
    trigger: "反事实搜索"
    strategy: "全引擎聚合 + 反事实重写 + 跨语言验证"
    min_sources: 9
    annotation: "[search-aggregation-counterfactual] 标签标记"

  I01_supplementary:
    trigger: "补研"
    strategy: "定向搜索 + 缺口补全"
    min_sources: 15
    annotation: "[search-aggregation-gap] 标签标记"
```

---

## 8. 输出规范

```yaml
search_aggregation_output:
  query: str
  engines_used: [str]
  total_results: int
  after_dedup: int
  results:
    - title: str
      url: str
      snippet: str
      engines: [str]
      authority_level: 1-5
      quality_score: float
      consensus_count: int
      dedup_level: "unique|l1_dedup|l2_dedup|l3_possible_dup"
  dedup_stats:
    l1_url_dedup: int
    l2_title_dedup: int
    l3_content_dedup: int
  triangulation:
    pass_rate: float
    unverified_claims: [str]
  gap_analysis:
    identified_gaps: [str]
    closed_gaps: [str]
    remaining_gaps: [str]
```

---

## 9. 穷尽重试策略

```yaml
exhaust_retry:
  rule_1_all_engines:
    condition: "所有搜索引擎可用 + 查询重写正常"
    behavior: "全引擎聚合 + 三级去重 + 权威性排序 + 引擎共识加成 + 三角验证"

  rule_2_partial_engines:
    condition: "部分搜索引擎不可用"
    behavior: "穷尽尝试所有可用引擎聚合 + 标注[PARTIAL-ENGINE] + 增加可用引擎搜索轮次"

  rule_3_llm_knowledge:
    condition: "所有搜索引擎不可用"
    behavior: "LLM内建知识搜索 + 标注[INTERNAL_REASONING] + 置信度惩罚-0.3"

  rule_4_no_search:
    condition: "搜索功能完全不可用"
    behavior: "使用已有知识 + 标注[NO-SEARCH] + 警告研究质量可能不足 + 建议人工搜索"
```
