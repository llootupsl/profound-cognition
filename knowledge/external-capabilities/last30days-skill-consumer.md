<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

# last30days-skill 核心算法消费文件

> **文件**: `knowledge/external-capabilities/last30days-skill-consumer.md`
> **来源项目**: [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill)
> **能力卡编号**: TC-098
> **消费节点**: T02 研究底座、I01 补研、knowledge/search-strategy.md
> **内化日期**: 2026-06-14

---

## 一、方法论原理

last30days-skill 是跨平台趋势情报采集与排序系统，其核心认知假设是——**单一信息源存在系统性偏差，时效性信息具有边际价值递减特性，多源共识信号比单源高排名更可靠**。该系统采用"两阶段搜索 + 四阶段评分 + 意图感知重排"的三层架构，将异构搜索结果（Reddit/X/YouTube/HN/Polymarket/Bluesky/Web）转化为带置信度的优先级证据列表。

核心原理可拆解为三条：
1. **两阶段渐进搜索**：先广度发现（Broad Discovery），再智能补充（Intelligent Follow-up），避免一次性搜索的上下文爆炸
2. **四阶段评分管道**：本地相关性 → 加权RRF融合 → LLM语义重排 → 最终评分，逐层提纯
3. **时效性指数衰减**：30天窗口内，信息价值随时间指数递减，越新的内容获得越高分数

---

## 二、执行步骤

### 步骤1：查询规划（Query Planning）

```
输入: 用户主题 topic
输出: QueryPlan 对象

1. 意图分类（Intent Classification）:
   - comparison: 对比分析 → 偏好头对头基准测试
   - how_to: 操作指南 → 偏好教程和代码示例
   - breaking_news: 突发新闻 → 偏好时效性和第一手报道
   - prediction: 预测分析 → 偏好量化预测和市场数据
   - general: 通用 → 均衡偏好

2. 子查询生成:
   - 原始查询 → 3-5个不同语义角度的子查询
   - 同义词扩展: js→javascript, ml→machine learning
   - 反事实查询: NOT {关键词} 或 {对立观点}

3. 来源权重分配（source_weights）:
   - Reddit: 1.0（社区讨论深度最高）
   - X/Twitter: 0.9（实时性最强）
   - Hacker News: 0.9（技术社区权威）
   - YouTube: 0.7（视频内容信息密度较低）
   - Web Search: 0.8（补充博客/新闻/教程）
   - Polymarket: 0.7（预测市场情绪指标）
```

### 步骤2：两阶段搜索

#### 阶段2a：广度发现（Broad Discovery）

```
并行搜索所有配置平台:
  - Reddit: ScrapeCreators API / OpenAI Responses API
  - X/Twitter: xAI Responses API / Cookie认证GraphQL
  - YouTube: Data API v3 + yt-dlp字幕提取
  - Hacker News: Algolia免费API
  - Polymarket: Gamma API（预测市场数据）
  - Bluesky: AT Protocol搜索
  - Web: DuckDuckGo / Google搜索API

每平台返回: 标题 + URL + 摘要 + 发布日期 + 互动数据
```

#### 阶段2b：智能补充（Intelligent Follow-up）

```
1. 实体提取: 从阶段2a结果中自动识别:
   - @账号（Twitter/X专家）
   - 子reddit名称
   - YouTube频道
   - 关键术语/产品名

2. 针对性搜索: 对提取的实体进行定向搜索
   - 发现某专家 → 搜索其30天内所有推文
   - 发现某子论坛频繁出现 → 专门搜索该版块

3. 结果去重与合并:
   - 双向匹配 + 同义词扩展
   - 近重复检测（dedupe.py）
```

### 步骤3：四阶段评分管道

#### 阶段3a：本地相关性评分（Local Relevance）

```
token_overlap_relevance(query, text) → [0.0, 1.0]

评分公式:
  score = 0.55 × coverage^1.35        # 查询token覆盖率（55%权重）
        + 0.25 × informative_overlap    # 高信号token重叠度（25%权重）
        + 0.20 × precision              # 匹配精度，惩罚关键词堆砌（20%权重）
        + phrase_bonus                  # 精确短语匹配加成（+0.12或+0.16）

其中:
  coverage = |query_tokens ∩ text_tokens| / |query_tokens|
  informative_overlap = |high_signal_tokens ∩ text_tokens| / |high_signal_tokens|
    （排除 "review", "vs", "update" 等低信号词）
  precision = |matches| / |text_tokens|
  phrase_bonus = 0.16 if exact_phrase_in_text else 0.12 if near_match else 0

预处理:
  1. 小写化 + 去标点
  2. 停用词移除（the, and, how 等）
  3. 同义词扩展（js→javascript, ml→machine learning）
```

#### 阶段3b：加权RRF融合（Weighted Reciprocal Rank Fusion）

```
RRF_score(item) = Σ(weight_i / (k + rank_i))

其中:
  weight_i = 来源i的source_weight（见步骤1）
  rank_i = item在来源i结果中的排名
  k = 60（平滑常数，降低高排名的过大影响）

示例:
  某结果在Reddit排第1（weight=1.0）, 在X排第3（weight=0.9）:
  RRF = 1.0/(60+1) + 0.9/(60+3) = 0.0164 + 0.0143 = 0.0307
```

#### 阶段3c：LLM语义重排（LLM Reranking）

```
输入: RRF融合后的Top-N候选（短名单）
输出: 每个候选的rerank_score（0-100）

意图感知评分偏好:
  | intent        | 评分偏好                           |
  |---------------|-----------------------------------|
  | comparison    | 头对头基准测试、对比分析             |
  | how_to        | 实用演示、代码示例、教程             |
  | breaking_news | 时效性、第一手报道（优于深度）       |
  | prediction    | 量化预测、市场数据                   |

安全防护: 所有候选片段包裹在 <untrusted_content> 标签中，
         防止来自网页内容的提示注入攻击
```

#### 阶段3d：最终评分计算

```
final_score = rerank_score × 0.70      # LLM语义相关性（0-100）
            + normalized_rrf × 0.25    # RRF位置分（归一化至0-100）
            + engagement_boost × 0.05  # 对数归一化互动量

穷尽重试方案（LLM不可用时）:
  exhaust_retry_score = local_relevance × 0.70
                 + freshness × 0.20
                 + source_quality × 0.10
```

### 步骤4：时效性衰减模型（Recency Decay）

```
衰减公式:
  recency_score = base_score × exp(-λ × days_old)

其中:
  base_score = 原始评分（步骤3的final_score）
  λ = 衰减系数（默认0.05，可配置）
  days_old = 内容发布距今天数

30天窗口内衰减示例（λ=0.05）:
  | 天数 | 衰减因子 | 保留比例 |
  |------|---------|---------|
  | 0    | 1.000   | 100%    |
  | 7    | 0.705   | 70.5%   |
  | 14   | 0.497   | 49.7%   |
  | 21   | 0.350   | 35.0%   |
  | 30   | 0.223   | 22.3%   |

信息新鲜度判定规则:
  | 天数范围   | 新鲜度等级 | 标注     |
  |-----------|-----------|---------|
  | 0-3天     | 极新鲜     | FRESH   |
  | 4-10天    | 新鲜       | RECENT  |
  | 11-20天   | 一般       | NORMAL  |
  | 21-30天   | 过时       | STALE   |
  | >30天     | 超出窗口   | EXPIRED |

半衰期配置:
  - 快速衰减（新闻/热点）: half_life = 7天 → λ = ln(2)/7 ≈ 0.099
  - 标准衰减（技术讨论）: half_life = 14天 → λ = ln(2)/14 ≈ 0.050
  - 慢速衰减（学术/深度）: half_life = 30天 → λ = ln(2)/30 ≈ 0.023
```

### 步骤5：来源权威性加权（Source Authority）

```
权威性评分规则:
  | 来源类型                     | 权威度 | 说明                     |
  |-----------------------------|--------|-------------------------|
  | r/MachineLearning等高质子论坛 | 1.0    | 社区审核严格，讨论深度高   |
  | r/AskReddit等低质子论坛       | 0.5    | 内容泛化，噪声多           |
  | Twitter认证账号/行业专家       | 1.0    | 额外权重加成               |
  | Twitter普通账号               | 0.6    | 标准权重                   |
  | HN高赞帖子                   | 0.9    | 技术社区权威               |
  | YouTube高订阅频道             | 0.8    | 内容质量有保障             |
  | Polymarket高流动性合约        | 0.8    | 市场信号可靠               |

互动量归一化:
  engagement_boost = log(1 + upvotes + comments + shares) / log(1 + max_engagement)
```

### 步骤6：跨平台收敛检测（Cross-Platform Convergence）

```
收敛判定:
  同一主题/观点在 ≥ 3 个不同平台被独立提及 → 标注为"跨平台共识"
  收敛加成: consensus_boost = +0.3（≥3平台）, +0.15（2平台）, 0（1平台）

模式识别:
  - 上升趋势: 多平台讨论量逐日递增
  - 峰值事件: 某日多平台同时爆发讨论
  - 衰退趋势: 讨论量逐日递减
```

### 步骤7：报告生成

```
输出结构:
  # last30days Report: {topic}
  ## Sources Searched (N platforms)
  ## Key Findings
  ### Finding 1: {标题} [{FRESH/RECENT/NORMAL/STALE}]
  - 来源: Reddit r/xxx + X @yyy + HN
  - 收敛: 3平台共识
  - 评分: 87.3
  - 摘要: ...
  ## Trend Analysis
  ## Comparative Analysis (如intent=comparison)
  ## Prediction Markets (如intent=prediction)
```

---

## 三、决策规则

| 决策点 | 条件 | 动作 |
|--------|------|------|
| 搜索阶段 | 首次搜索 | 执行广度发现（阶段2a） |
| 搜索阶段 | 广度发现结果不足 | 执行智能补充（阶段2b），提取实体定向搜索 |
| 搜索阶段 | 智能补充仍不足 | 扩展查询词（同义词/上位词），重试 |
| 评分阶段 | LLM可用 | 执行完整四阶段评分管道 |
| 评分阶段 | LLM不可用 | 穷尽重试替代为三信号评分（相关性70%+时效20%+来源10%） |
| 时效性 | 内容 > 30天 | 标注EXPIRED，排除出报告（除非是唯一来源） |
| 时效性 | 内容 21-30天 | 标注STALE，降低权重但保留 |
| 收敛检测 | ≥3平台共识 | 标注高可信度，优先纳入证据链 |
| 收敛检测 | 仅1平台 | 标注低可信度，需独立来源验证 |
| 去重 | URL完全匹配 | 保留最先返回的结果 |
| 去重 | 标题相似度 > 0.8 | 合并，保留更完整的结果 |
| 去重 | 正文前200字相似度 > 0.7 | 标记可能重复，保留但降权 |
| 对比模式 | intent=comparison | 生成X vs Y对比分析报告 |
| 预测模式 | intent=prediction | 整合Polymarket预测市场数据 |

---

## 四、输出规范

```yaml
last30days_output:
  topic: str
  intent: "comparison|how_to|breaking_news|prediction|general"
  search_phases:
    broad_discovery:
      platforms_searched: [str]
      total_results: int
      duration_seconds: int
    intelligent_followup:
      entities_extracted: int
      targeted_searches: int
      additional_results: int
  scoring_pipeline:
    local_relevance_applied: bool
    rrf_fusion_applied: bool
    llm_rerank_applied: bool
    exhaust_retry_used: bool
  results:
    - title: str
      url: str
      snippet: str
      source_platform: str
      source_authority: float
      freshness: "FRESH|RECENT|NORMAL|STALE|EXPIRED"
      days_old: int
      recency_decay_factor: float
      local_relevance: float
      rrf_score: float
      rerank_score: float|null
      final_score: float
      engagement: int
      consensus_count: int
      consensus_boost: float
  trend_analysis:
    direction: "rising|peaking|declining|stable"
    peak_date: str|null
    platform_convergence: [str]
  dedup_stats:
    url_dedup: int
    title_dedup: int
    content_dedup: int
```

---

## 五、与 profound-cognition 架构集成

### 5.1 消费节点映射

| profound-cognition 节点 | 集成方式 | 说明 |
|------------------------|---------|------|
| T02 研究底座 | 两阶段搜索 + 四阶段评分 | 替代/增强现有搜索聚合策略 |
| I01 补研 | 智能补充搜索 | 缺口识别 → 实体提取 → 定向搜索 |
| search-strategy.md | 时效性衰减模型 | 补充现有质量评分公式中的时效性维度 |
| search-aggregation.md | RRF融合 + 收敛检测 | 增强多引擎聚合的排序质量 |

### 5.2 与现有公式引擎的关系

| 公式引擎 | 关系 | 说明 |
|---------|------|------|
| FE-003 Info-Decay | 互补 | Info-Decay用于迭代终止判断；last30days衰减用于搜索结果排序 |
| FE-001 Softmax-Attention | 可组合 | last30days评分可作为Softmax输入的注意力权重 |

### 5.3 穷尽重试策略

| 穷尽重试路径 | 触发条件 | 行为 |
|-------------|---------|------|
| 完整四阶段 → 穷尽重试替代三信号 | LLM API超时/配额耗尽 | 使用exhaust_retry_score，标注`llm_rerank_exhaust_retry=true` |
| 全平台搜索 → 部分平台 | 某平台API不可用 | 跳过不可用平台，标注`partial_search=true` |
| 部分平台 → LLM内建知识 | 所有外部平台不可用 | 使用LLM内建知识，标注`internal_reasoning=true, confidence_penalty=-0.3` |
| 标准衰减 → 快速衰减 | 研究主题为突发新闻 | 切换half_life=7天，标注`fast_decay=true` |

> 知识来源: TC-098 last30days-skill (mvanhorn/last30days-skill)
