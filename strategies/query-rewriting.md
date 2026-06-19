<!-- 作者：阿洋 -->

# 查询重写策略

## 激活条件

```yaml
activation:
  condition: "T02/T05/T06 搜索阶段 AND 原始查询需要优化"
  trigger_rules:
    - "原始查询过于宽泛（返回结果 > 100条且相关性低）"
    - "原始查询过于狭窄（返回结果 < 5条）"
    - "需要多角度覆盖研究问题"
    - "需要反事实验证核心假设"
  priority: "必需 — 查询质量直接决定搜索结果质量"
```

---

## 1. Perplexica 多角度重写

### 1.1 重写规则
将原始查询重写为多个角度的子查询：

| 角度 | 重写模板 | 示例 |
|------|---------|------|
| 直接 | {原始查询} | "中国新能源汽车竞争格局" |
| 反面 | NOT {核心假设} | "中国新能源汽车市场萎缩" |
| 因果 | {关键词} 原因/影响 | "新能源汽车补贴退坡影响" |
| 比较 | {A} vs {B} | "比亚迪 vs 特斯拉 中国市场" |
| 趋势 | {关键词} 趋势/预测 | "新能源汽车 2025-2030 预测" |

### 1.2 重写数量
- 每个原始查询生成 3-5 个子查询
- 子查询覆盖不同语义维度
- 避免语义重复的子查询

### 1.3 重写质量评估

```yaml
quality_assessment:
  coverage_check:
    rule: "5个角度中至少覆盖3个"
    minimum: 3
    maximum: 5

  semantic_diversity:
    rule: "子查询间语义相似度 < 0.7"
    measurement: "使用embedding cosine similarity"
    threshold: 0.7

  specificity:
    rule: "子查询比原始查询更具体"
    validation: "子查询返回结果数 < 原始查询返回结果数 * 0.5"

  actionability:
    rule: "每个子查询可独立执行搜索"
    validation: "子查询不含代词或模糊引用"
```

### 1.4 重写决策树

```yaml
rewrite_decision_tree:
  Q1_结果数量:
    too_many: "> 100条且相关性低 → 应用精确匹配重写（引号包裹+site限定）"
    too_few: "< 5条 → 应用扩展重写（同义词+上位词+移除限定词）"
    adequate: "5-100条 → 应用多角度重写（5角度全覆盖）"

  Q2_查询类型:
    factual: "事实型查询 → 直接+因果+比较角度优先"
    analytical: "分析型查询 → 因果+比较+趋势角度优先"
    evaluative: "评估型查询 → 反面+比较+边界角度优先"
    exploratory: "探索型查询 → 直接+因果+趋势角度优先"

  Q3_研究阶段:
    T02_L1_L2: "事实收集 → 直接+因果+比较（3个子查询）"
    T03_L3: "结构分析 → 比较+因果+趋势（3个子查询）"
    T05_L6_L7: "证据验证 → 反面+直接+比较（3-5个子查询）"
    T06_L8_L9: "反事实 → 反面+边界+直接（3-5个子查询）"
```

---

## 2. STORM 多视角提问

### 2.1 专家视角生成
从以下视角生成提问：

| 视角 | 提问模板 | 关注维度 | 适用研究阶段 |
|------|---------|---------|------------|
| 领域专家 | 从技术/专业角度看，{研究问题}的核心机制是什么？ | 技术可行性、专业标准 | T02/T03 |
| 行业从业者 | 在实践中，{研究问题}面临哪些真实挑战？ | 实施难度、现实约束 | T04/T05 |
| 政策制定者 | 从监管角度看，{研究问题}需要哪些政策响应？ | 合规性、政策影响 | T04/T05 |
| 消费者/用户 | 从用户体验看，{研究问题}如何影响终端用户？ | 需求满足、体验影响 | T04 |
| 投资者 | 从商业回报看，{研究问题}的投资逻辑是什么？ | 市场规模、ROI、风险 | T04/T05 |

### 2.2 立场覆盖
每个核心论点需覆盖三种立场：

| 立场 | 提问模板 | 目的 |
|------|---------|------|
| 支持立场 | 为什么{观点}是对的？有哪些证据支持？ | 收集正面证据 |
| 反对立场 | 为什么{观点}是错的？有哪些反例？ | 收集反面证据，避免确认偏误 |
| 边界立场 | {观点}的适用边界是什么？在什么条件下失效？ | 识别论断的适用范围 |

### 2.3 STORM执行步骤

```yaml
storm_execution:
  step_1_identify_core_claims:
    method: "从研究问题中提取3-5个核心论点"
    output: "core_claims列表"

  step_2_generate_perspectives:
    method: "为每个核心论点生成5个专家视角的提问"
    output: "perspective_questions列表（每个论点5个问题）"

  step_3_cover_stances:
    method: "为每个核心论点覆盖3种立场"
    output: "stance_questions列表（每个论点3个立场问题）"

  step_4_deduplicate:
    method: "去除语义重复的问题（相似度 > 0.8）"
    output: "deduplicated_questions列表"

  step_5_prioritize:
    method: "按研究阶段优先级排序"
    priority: "T02事实收集 > T05证据验证 > T06反事实 > T03结构分析"
    output: "prioritized_questions列表"
```

---

## 3. 反事实查询

### 3.1 查询生成规则
- 搜索与核心假设相反的证据
- 格式："NOT {假设关键词}" 或 "{对立观点关键词}"
- 目的：确保研究不是确认偏误的产物

### 3.2 反事实查询示例
| 核心假设 | 反事实查询 |
|---------|-----------|
| "AI 将取代程序员" | "AI 无法取代程序员的原因" |
| "电动车是未来" | "电动车发展瓶颈/失败案例" |
| "远程办公提高效率" | "远程办公降低效率的证据" |

### 3.3 反事实查询强度分级

```yaml
counterfactual_intensity:
  level_1_weak:
    description: "温和反事实 — 搜索替代解释"
    template: "{关键词} 替代解释/其他因素"
    trigger: "T02 事实收集阶段"
    purpose: "扩展视野，不直接挑战假设"

  level_2_moderate:
    description: "中等反事实 — 搜索反面证据"
    template: "NOT {假设关键词} 或 {对立观点关键词}"
    trigger: "T05 证据验证阶段"
    purpose: "主动寻找反驳证据"

  level_3_strong:
    description: "强反事实 — 假设核心前提为假"
    template: "如果{核心前提}不成立，{结论}会怎样"
    trigger: "T06 反事实搜索阶段"
    purpose: "彻底挑战假设的逻辑基础"

  level_4_extreme:
    description: "极端反事实 — 假设完全相反的世界"
    template: "在{完全相反的前提}下，世界会怎样"
    trigger: "I01 补研（当研究结论过于一致时）"
    purpose: "打破思维定势，发现盲点"
```

---

## 4. 查询语言优化

### 4.1 搜索引擎语法优化

```yaml
search_syntax_optimization:
  rule_1_exact_match:
    trigger: "核心术语需要精确匹配"
    syntax: "将核心术语用双引号包裹"
    example: '"大语言模型" 幻觉'
    effect: "减少无关结果，提高精确度"

  rule_2_site_restriction:
    trigger: "需要限定在权威来源内搜索"
    syntax: "site:arxiv.org 或 site:gov.cn"
    effect: "提高来源权威度"

  rule_3_exclusion:
    trigger: "搜索结果包含大量噪声"
    syntax: "-排除词"
    example: '"AI安全" -"人工智能安全" -游戏'
    effect: "减少噪声结果"

  rule_4_filetype:
    trigger: "需要特定格式的学术文献"
    syntax: "filetype:pdf"
    example: '"transformer attention" filetype:pdf'
    effect: "直接获取PDF文献"

  rule_5_intitle:
    trigger: "核心概念必须出现在标题中"
    syntax: 'intitle:"知识图谱" 建模'
    effect: "提高标题相关性"
```

### 4.2 多语言查询优化

```yaml
multilingual_optimization:
  default: "中文 + 英文双语查询"
  rule_1_translation:
    method: "将中文查询翻译为英文后分别搜索"
    example: '"新能源汽车补贴" → "EV subsidy policy China"'

  rule_2_cultural_adaptation:
    method: "根据目标语言文化调整查询词"
    example: '"内卷" → "involution" OR "hyper-competition"'

  rule_3_regional_focus:
    method: "添加地域限定词"
    example: '"新能源汽车" 中国 → "electric vehicle" China OR Chinese'

  third_language:
    trigger: "研究主题涉及特定国家/地区"
    languages: ["日语", "韩语", "德语", "法语", "西班牙语", "阿拉伯语"]
    method: "按需添加第三语言查询"
```

---

## 5. 与 profound-cognition Task 节点集成

```yaml
task_integration:
  T02_L1_L2_research:
    trigger: "研究底座事实收集"
    rewrite_strategy: "Perplexica多角度重写（3个子查询）"
    storm_strategy: "5专家视角提问"
    counterfactual: "level_1_weak"
    output: "重写后的子查询列表 → 搜索引擎执行"
    annotation: "[query-rewrite] 标签标记重写来源"

  T03_L3_structure:
    trigger: "结构变量分析"
    rewrite_strategy: "比较+因果角度重写"
    storm_strategy: "领域专家+行业从业者视角"
    counterfactual: "level_1_weak"
    output: "结构化查询 → 变量关系搜索"
    annotation: "[query-rewrite-structure] 标签标记"

  T05_L6_L7_evidence:
    trigger: "证据验证"
    rewrite_strategy: "反面+比较角度重写（5个子查询）"
    storm_strategy: "3立场全覆盖"
    counterfactual: "level_2_moderate"
    output: "验证性查询 → 证据交叉验证"
    annotation: "[query-rewrite-evidence] 标签标记"

  T06_L8_L9_counterfactual:
    trigger: "反事实搜索"
    rewrite_strategy: "反面+边界角度重写（5个子查询）"
    storm_strategy: "反对+边界立场优先"
    counterfactual: "level_3_strong"
    output: "反事实查询 → 假设挑战"
    annotation: "[query-rewrite-counterfactual] 标签标记"

  I01_supplementary:
    trigger: "补研（结论过于一致时）"
    rewrite_strategy: "极端反事实重写"
    storm_strategy: "反对立场独占"
    counterfactual: "level_4_extreme"
    output: "极端反事实查询 → 盲点发现"
    annotation: "[query-rewrite-extreme] 标签标记"
```

---

## 6. 输出规范

```yaml
query_rewrite_output:
  original_query: str
  rewrite_method: "perplexica|storm|counterfactual|syntax_optimization|multilingual"
  sub_queries:
    - query: str
      angle: "直接|反面|因果|比较|趋势|专家视角|立场|反事实"
      target_engine: "searxng|whoogle|duckduckgo"
      language: "zh|en|ja|..."
      priority: 1-5
  quality_metrics:
    coverage_score: float  # 5角度覆盖率
    diversity_score: float  # 语义多样性
    specificity_score: float  # 具体性提升
  estimated_result_count: int
```

---

## 7. 穷尽重试策略

```yaml
exhaust_retry:
  rule_1_all_strategies:
    condition: "所有重写策略可用"
    behavior: "Perplexica 5角度 + STORM 5视角 + 反事实4级 + 语法优化5规则 + 多语言"

  rule_2_partial_strategies:
    condition: "部分重写策略不可用（如STORM视角生成失败）"
    behavior: "可用策略重写 + 标注[PARTIAL-REWRITE] + 增加可用策略的子查询数量"

  rule_3_syntax_only:
    condition: "重写策略不可用（LLM能力不足）"
    behavior: "仅使用语法优化5规则 + 标注[SYNTAX-ONLY]"

  rule_4_no_rewrite:
    condition: "所有重写能力不可用"
    behavior: "使用原始查询直接搜索 + 标注[NO-REWRITE] + 警告搜索质量可能降低"
```
