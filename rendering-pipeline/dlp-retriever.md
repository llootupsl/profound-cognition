<!-- 作者：阿洋 -->

# DLP 检索器规范 (DLP Retriever Specification)

> **定位**: Visual DNA 审美进化层的中枢检索模块。将 Visual DNA 中枢从"生成器"转变为"选择器 + 适配器"——基于内容语义 + 用户偏好 + 任务类型，从 16 个 DLP 中检索最匹配的 1 个主 DLP + 1 个备选 DLP，并将 DLP 的 12 字段规范适配为 UIR v2.0 可消费的 `design_tokens` 对象。
> **强制规则**: DLP 检索器在 Taste-Skill 生成 `visual_dna` 前必须命中一个主 DLP，未命中时执行质量保持策略回退到默认族默认 DLP。
> **消费节点**: T20a/T20b/T20c/T27, rendering-pipeline/visual-dna.md, rendering-pipeline/taste-skill-consumer.md

---

## 一、方法论原理

DLP 检索器是 Visual DNA 审美进化项目的核心组件，采用"语义提取 → 任务映射 → 族内打分 → 适配输出"四阶段决策范式。其核心设计原理是"选择优于生成"——与其让 AI 凭空生成视觉参数（容易陷入 AI Slop），不如从 16 个锚定真实世界设计实体的 DLP 中检索最匹配的一个，确保视觉输出可追溯、可复现、可对标。

DLP 检索器不是简单的关键词匹配器，而是具备语义理解力的决策引擎——它需要从 UIR v2.0 全息框架的 §1-§8 中提取内容语义信号，结合任务类型和用户偏好，在 4 族 16 个 DLP 中做出超越模板化的审美决策。

### 1.1 与现有模块的关系

| 模块 | 职责 | 与 DLP 检索器的关系 |
|------|------|-------------------|
| `visual-dna.md` | 生成唯一 visual_dna 对象 | 消费 DLP 检索器输出的 `design_tokens` |
| `taste-skill-consumer.md` | 三旋钮系统 + 反 Slop 规则 | DLP 检索器命中 DLP 后，三旋钮 DV/MI/VD 作为微调参数 |
| `design-language-profiles/README.md` | 16 个 DLP 的元规范与检索映射 | DLP 检索器是其 §4 检索规范的深度实现 |
| `design-language-profiles/DLP-*.md` | 16 个 DLP 的 12 字段完整定义 | DLP 检索器的检索源 |

### 1.2 检索流程总览

```
输入: UIR v2.0 文档（§1-§8 全息框架）+ 任务类型 + 用户偏好
  ↓
Step 1: 语义信号提取（从 §1-§8 提取内容主题/领域/受众）
  ↓
Step 2: 任务类型映射（4 种任务类型 → 4 族优先级）
  ↓
Step 3: 族内打分（目标族内 4 个 DLP 按场景标签匹配度打分）
  ↓
Step 4: 适配器输出（DLP 12 字段 → design_tokens 对象）
  ↓
输出: 主 DLP + 备选 DLP + design_tokens 对象 + 置信度
```

---

## 二、语义信号提取算法

### 2.1 UIR v2.0 全息框架 §1-§8 结构

DLP 检索器从 UIR v2.0 文档的 §1-§8 全息框架中提取三类语义信号：**内容主题**、**领域分类**、**目标受众**。UIR v2.0 的 8 部分结构如下：

| 部分 | 标准名称 | 语义角色 | 提取信号 |
|------|---------|---------|---------|
| §1 | 问题认知与定义（4 维） | 摘要层 — 问题定义与核心论点 | 内容主题关键词 |
| §2 | 全维全域分析（8 维） | 背景层 — 全维度背景分析 | 内容主题关键词 |
| §3 | 极限决策推理（2 维） | 方法层 — 推理方法与决策路径 | 领域分类信号 |
| §4 | 元层综合与跨维洞察 | 分析层 — 跨维度综合分析 | 领域分类信号 |
| §5 | 科学深度层（7 模块） | 讨论层 — 科学验证与深度讨论 | 目标受众推断 |
| §6 | 元维度扩展（9-14，6 维） | 扩展层 — 元维度扩展分析 | 领域分类补充 |
| §7 | 哲学内核三元组 | 哲学层 — 本体论/认识论/价值论 | 内容主题补充 |
| §8 | 未来研究议程 | 结论层 — 未来方向与结论 | 目标受众推断 |

### 2.2 信号提取伪代码

```python
# ============================================================
# DLP 检索器 — 语义信号提取算法
# 输入: UIR v2.0 文档（含 §1-§8 全息框架完整内容）
# 输出: semantic_signals = {content_theme, domain, target_audience}
# ============================================================

function extract_semantic_signals(uir_document):
    """
    从 UIR v2.0 文档的 §1-§8 全息框架中提取三类语义信号
    """

    # ---- Step 1: 内容主题提取（从 §1 摘要层 + §2 背景层）----
    # §1 问题认知与定义：提取问题陈述中的核心关键词
    section_1 = uir_document.get_section("§1")
    # §2 全维全域分析：提取背景分析中的领域关键词
    section_2 = uir_document.get_section("§2")

    # 从 §1 提取问题定义关键词（问题陈述、核心论点、研究问题）
    problem_keywords = extract_keywords(section_1.problem_statement, max_count=10)
    # 从 §2 提取背景维度关键词（8 维分析中的高频术语）
    background_keywords = extract_keywords(section_2.all_dimensions, max_count=15)

    # 合并去重，按词频排序，取 Top-10 作为内容主题
    content_theme_keywords = merge_and_deduplicate(
        problem_keywords,
        background_keywords,
        strategy="frequency_weighted"
    )[:10]

    # 内容主题分类（映射到预设主题类别）
    content_theme = classify_theme(content_theme_keywords)
    # 预设主题类别:
    #   - 科技/数据/AI
    #   - 人文/社会/文化
    #   - 教育/培训/课程
    #   - 商业/市场/金融
    #   - 医疗/健康/生物
    #   - 创意/设计/艺术
    #   - 工程/计算机/电子
    #   - 经济/政治/政策
    #   - 通用/其他

    # ---- Step 2: 领域分类提取（从 §3 方法层 + §4 分析层）----
    # §3 极限决策推理：提取推理方法涉及的学科领域
    section_3 = uir_document.get_section("§3")
    # §4 元层综合与跨维洞察：提取跨维分析涉及的学科领域
    section_4 = uir_document.get_section("§4")

    # 从 §3 提取方法论关键词（推理框架、决策模型、分析方法）
    method_domains = extract_domain_tags(section_3.reasoning_methods)
    # 从 §4 提取跨维分析涉及的学科（跨维度综合时涉及的领域）
    analysis_domains = extract_domain_tags(section_4.cross_dimensional_insights)

    # 合并去重，按出现频次排序
    domain_candidates = merge_and_deduplicate(
        method_domains,
        analysis_domains,
        strategy="frequency_weighted"
    )

    # 领域分类（映射到 35 个领域引擎之一）
    domain = classify_domain(domain_candidates)
    # 领域引擎映射示例:
    #   science-engine → 学术研究（理科）
    #   engineering-engine → 工程研究
    #   economics-engine → 经济分析
    #   business-engine → 商业分析
    #   design-engine → 设计/创意
    #   education-engine → 教育培训
    #   ...（共 35 个领域引擎）

    # ---- Step 3: 目标受众推断（从 §5 讨论层 + §8 结论层）----
    # §5 科学深度层：从讨论深度和验证方法推断受众水平
    section_5 = uir_document.get_section("§5")
    # §8 未来研究议程：从结论的方向性推断受众类型
    section_8 = uir_document.get_section("§8")

    # 从 §5 分析科学验证深度（7 模块的复杂度暗示受众专业水平）
    science_depth_signals = analyze_science_depth(section_5.seven_modules)
    #   - 系统动力学建模 → academic（需要建模知识）
    #   - 因果验证 → academic（需要统计知识）
    #   - 多智能体对抗 → professional（需要博弈论知识）
    #   - 情景规划 → professional/general（可理解性强）
    #   - 元认知反思 → academic（需要哲学知识）
    #   - 覆盖验证 → academic（需要方法论知识）
    #   - 本体导出 → academic（需要本体论知识）

    # 从 §8 分析未来研究议程的受众指向
    future_research_signals = analyze_audience_pointing(section_8.future_agenda)
    #   - "为政策制定者提供..." → professional/policy
    #   - "为公众理解..." → general
    #   - "为学术同行..." → academic
    #   - "为教育实践..." → professional/education
    #   - "为青年群体..." → youth

    # 综合推断目标受众
    target_audience = infer_audience(science_depth_signals, future_research_signals)
    # 受众类别: academic / general / professional / youth

    # ---- Step 4: 组装语义信号对象 ----
    semantic_signals = {
        "content_theme": content_theme,        # 内容主题（预设类别 + 关键词列表）
        "content_theme_keywords": content_theme_keywords,  # 原始关键词
        "domain": domain,                      # 领域分类（35 个领域引擎之一）
        "domain_candidates": domain_candidates, # 原始领域候选
        "target_audience": target_audience,    # 目标受众（4 类之一）
        "extraction_confidence": calculate_confidence(
            content_theme_keywords, domain_candidates, target_audience
        )
    }

    return semantic_signals


# ============================================================
# 辅助函数：关键词提取
# ============================================================

function extract_keywords(text, max_count):
    """
    从文本中提取关键词：
    1. 分词（中英文混合分词）
    2. 去停用词
    3. TF-IDF 加权
    4. 专业术语加权（学术术语 ×1.5 权重）
    5. 取 Top-N
    """
    tokens = tokenize(text)
    tokens = remove_stopwords(tokens)
    weighted_tokens = apply_tfidf(tokens)
    weighted_tokens = boost_technical_terms(weighted_tokens, factor=1.5)
    return top_n(weighted_tokens, max_count)


function extract_domain_tags(text):
    """
    从文本中提取领域标签：
    1. 匹配 35 个领域引擎的关键词词典
    2. 统计每个领域的匹配命中数
    3. 返回命中数 > 0 的领域列表（按命中数降序）
    """
    domain_hits = {}
    for domain_engine in DOMAIN_ENGINES_35:
        hit_count = count_keyword_matches(text, domain_engine.keyword_dict)
        if hit_count > 0:
            domain_hits[domain_engine.name] = hit_count
    return sorted(domain_hits.keys(), key=lambda k: domain_hits[k], reverse=True)


function classify_theme(keywords):
    """
    将关键词列表分类到预设主题类别
    使用关键词 → 主题类别的映射词典
    """
    theme_scores = {}
    for theme_category, theme_keywords in THEME_MAPPING.items():
        score = sum(1 for kw in keywords if kw in theme_keywords)
        theme_scores[theme_category] = score
    best_theme = max(theme_scores, key=theme_scores.get)
    if theme_scores[best_theme] == 0:
        return "通用/其他"
    return best_theme


function classify_domain(domain_candidates):
    """
    将领域候选列表分类到单一领域
    取命中数最高的领域引擎
    """
    if not domain_candidates:
        return "general-engine"
    return domain_candidates[0]


function infer_audience(science_depth_signals, future_research_signals):
    """
    综合科学深度信号和未来研究信号推断目标受众
    """
    # 科学深度信号权重 60%，未来研究信号权重 40%
    audience_scores = {"academic": 0, "general": 0, "professional": 0, "youth": 0}

    for signal in science_depth_signals:
        audience_scores[signal.audience] += signal.weight * 0.6

    for signal in future_research_signals:
        audience_scores[signal.audience] += signal.weight * 0.4

    return max(audience_scores, key=audience_scores.get)


function calculate_confidence(theme_kw, domains, audience):
    """
    计算语义信号提取的置信度
    """
    theme_confidence = min(len(theme_kw) / 10.0, 1.0)  # 关键词数量
    domain_confidence = min(len(domains) / 3.0, 1.0)    # 领域候选数量
    audience_confidence = 1.0 if audience != "general" else 0.5  # 受众明确度

    return (theme_confidence * 0.4 + domain_confidence * 0.35 + audience_confidence * 0.25)
```

### 2.3 信号提取输出规范

```yaml
semantic_signals:
  content_theme: "科技/数据/AI"           # 预设主题类别
  content_theme_keywords:                  # 原始关键词（Top-10）
    - "大语言模型"
    - "多智能体"
    - "认知架构"
    - "..."
  domain: "tech-engine"                    # 35 个领域引擎之一
  domain_candidates:                       # 原始领域候选（按命中数降序）
    - "tech-engine"
    - "cognitive-science-engine"
    - "..."
  target_audience: "academic"              # 4 类受众之一
  extraction_confidence: 0.85              # 提取置信度（0.0-1.0）
```

---

## 三、任务类型映射

### 3.1 四种任务类型完整映射表

DLP 检索器支持 4 种任务类型，每种任务类型对应一个优先族和一个次选族。任务类型是族预筛选的主要依据，权重为 35%。

| 任务类型 | 优先族 | 次选族 | 映射逻辑 | 典型场景 |
|---------|--------|--------|---------|---------|
| `research_report` | academic-journal | data-visualization | 学术研究报告需要严谨的期刊版式，数据图表作为补充 | 学术论文、期刊投稿、同行评审、预印本、科研报告 |
| `wechat_article` | publication-typesetting | interface-brand | 公众号文章需要杂志级排版与长文阅读体验 | 新闻杂志、深度报道、品牌叙事、长文排版 |
| `course_material` | interface-brand | publication-typesetting | 课程材料需要清晰的界面层级与教育可读性 | 讲义、视频脚本、教学课件、培训材料 |
| 数据可视化任务 | data-visualization | academic-journal | 数据可视化任务需要图表优先的视觉规范 | 数据图表、统计可视化、学术配图、交互式仪表盘 |

### 3.2 任务类型检测算法

```python
# ============================================================
# DLP 检索器 — 任务类型映射算法
# 输入: semantic_signals + 显式任务类型（可选）
# 输出: task_type_mapping = {primary_family, secondary_family, task_type}
# ============================================================

function map_task_type(semantic_signals, explicit_task_type=None):
    """
    将任务类型映射到 DLP 族优先级
    """

    # 任务类型 → 族映射表
    TASK_FAMILY_MAPPING = {
        "research_report": {
            "primary_family": "academic-journal",
            "secondary_family": "data-visualization",
            "rationale": "学术研究报告需要严谨的期刊版式，数据图表作为补充"
        },
        "wechat_article": {
            "primary_family": "publication-typesetting",
            "secondary_family": "interface-brand",
            "rationale": "公众号文章需要杂志级排版与长文阅读体验"
        },
        "course_material": {
            "primary_family": "interface-brand",
            "secondary_family": "publication-typesetting",
            "rationale": "课程材料需要清晰的界面层级与教育可读性"
        },
        "data_visualization": {
            "primary_family": "data-visualization",
            "secondary_family": "academic-journal",
            "rationale": "数据可视化任务需要图表优先的视觉规范"
        }
    }

    # Step 1: 确定任务类型
    if explicit_task_type is not None:
        task_type = explicit_task_type
    else:
        # 从语义信号推断任务类型
        task_type = infer_task_type(semantic_signals)

    # Step 2: 查映射表获取族优先级
    if task_type in TASK_FAMILY_MAPPING:
        mapping = TASK_FAMILY_MAPPING[task_type]
    else:
        # 未知任务类型 → 默认 research_report 映射
        task_type = "research_report"
        mapping = TASK_FAMILY_MAPPING[task_type]

    # Step 3: 数据可视化任务的特殊检测
    # 如果内容主题包含大量数据可视化关键词，即使任务类型不是 data_visualization，
    # 也将 data-visualization 族加入候选
    data_viz_keywords = ["图表", "数据可视化", "统计图", "折线图", "柱状图",
                         "散点图", "热力图", "仪表盘", "数据面板"]
    if any(kw in semantic_signals.content_theme_keywords for kw in data_viz_keywords):
        # 数据可视化信号检测到，提升 data-visualization 族优先级
        if mapping["primary_family"] != "data-visualization":
            mapping["secondary_family"] = "data-visualization"

    return {
        "task_type": task_type,
        "primary_family": mapping["primary_family"],
        "secondary_family": mapping["secondary_family"],
        "rationale": mapping["rationale"]
    }


function infer_task_type(semantic_signals):
    """
    从语义信号推断任务类型（当未显式提供时）
    """
    # 基于内容主题和受众推断
    theme = semantic_signals.content_theme
    audience = semantic_signals.target_audience
    domain = semantic_signals.domain

    # 推断规则
    if domain in ["science-engine", "engineering-engine", "mathematics-engine",
                   "physics-engine", "health-engine"]:
        return "research_report"

    if theme in ["创意/设计/艺术", "人文/社会/文化"]:
        if audience in ["general", "youth"]:
            return "wechat_article"

    if theme in ["教育/培训/课程"]:
        return "course_material"

    if theme in ["商业/市场/金融", "经济/政治/政策"]:
        if audience == "academic":
            return "research_report"
        else:
            return "wechat_article"

    if theme in ["科技/数据/AI"]:
        if audience == "academic":
            return "research_report"
        elif audience == "professional":
            return "course_material"
        else:
            return "wechat_article"

    # 默认
    return "research_report"
```

### 3.3 任务类型映射输出规范

```yaml
task_type_mapping:
  task_type: "research_report"
  primary_family: "academic-journal"
  secondary_family: "data-visualization"
  rationale: "学术研究报告需要严谨的期刊版式，数据图表作为补充"
  data_viz_detected: false  # 是否检测到数据可视化信号
```

---

## 四、族内打分算法

### 4.1 打分规则

在目标族内对 4 个 DLP 按场景标签（`applicable_scenarios`）匹配度打分：

| 匹配类型 | 分值 | 判定条件 |
|---------|------|---------|
| 完全匹配 | +1.0 | DLP 场景标签与语义信号关键词完全一致（精确字符串匹配） |
| 部分匹配 | +0.5 | DLP 场景标签与语义信号关键词存在语义相似（同义词/上位词/下位词匹配） |
| 不匹配 | 0 | DLP 场景标签与语义信号关键词无匹配关系 |

**最终得分** = Σ(每个场景标签的匹配分值) / 场景标签总数 × 100%

**排序规则**: 取 Top-1 为主 DLP，Top-2 为备选 DLP。

### 4.2 打分伪代码

```python
# ============================================================
# DLP 检索器 — 族内打分算法
# 输入: target_family + semantic_signals + task_type_mapping
# 输出: scored_dlps = [{dlp_name, score, match_details}, ...]（按分数降序）
# ============================================================

function score_dlps_in_family(target_family, semantic_signals, task_type_mapping):
    """
    在目标族内对 4 个 DLP 按场景标签匹配度打分
    """

    # Step 1: 获取目标族内的所有 DLP（每族 4 个）
    family_dlps = get_dlps_by_family(target_family)
    # academic-journal: [DLP-nature, DLP-science, DLP-ieee, DLP-springer]
    # interface-brand: [DLP-linear, DLP-aesop, DLP-stripe-press, DLP-gov-uk]
    # publication-typesetting: [DLP-economist, DLP-ted, DLP-newyorker, DLP-kami]
    # data-visualization: [DLP-economist-chart, DLP-scienceplots, DLP-nature-figure, DLP-plotivy]

    # Step 2: 构建匹配关键词集（从语义信号中提取）
    match_keywords = build_match_keywords(semantic_signals, task_type_mapping)
    # match_keywords 包含:
    #   - content_theme_keywords（内容主题关键词）
    #   - domain_keywords（领域关键词）
    #   - audience_keywords（受众关键词）
    #   - task_type_keywords（任务类型关键词）

    # Step 3: 对每个 DLP 打分
    scored_dlps = []
    for dlp in family_dlps:
        score, match_details = score_single_dlp(dlp, match_keywords)
        scored_dlps.append({
            "dlp_name": dlp.name,
            "dlp_family": dlp.family,
            "score": score,
            "match_details": match_details,
            "applicable_scenarios": dlp.applicable_scenarios
        })

    # Step 4: 按分数降序排序
    scored_dlps.sort(key=lambda x: x["score"], reverse=True)

    # Step 5: 选取主 DLP 和备选 DLP
    primary_dlp = scored_dlps[0] if scored_dlps else None
    secondary_dlp = scored_dlps[1] if len(scored_dlps) > 1 else None

    return {
        "scored_dlps": scored_dlps,
        "primary_dlp": primary_dlp,
        "secondary_dlp": secondary_dlp,
        "confidence": calculate_retrieval_confidence(scored_dlps)
    }


function score_single_dlp(dlp, match_keywords):
    """
    对单个 DLP 按场景标签匹配度打分
    """
    scenarios = dlp.applicable_scenarios  # DLP 的场景标签列表
    total_score = 0.0
    match_details = []

    for scenario_tag in scenarios:
        match_type, matched_keyword = match_scenario_tag(scenario_tag, match_keywords)

        if match_type == "exact":
            total_score += 1.0
            match_details.append({
                "scenario_tag": scenario_tag,
                "match_type": "exact",
                "matched_keyword": matched_keyword,
                "score": 1.0
            })
        elif match_type == "partial":
            total_score += 0.5
            match_details.append({
                "scenario_tag": scenario_tag,
                "match_type": "partial",
                "matched_keyword": matched_keyword,
                "score": 0.5
            })
        else:
            match_details.append({
                "scenario_tag": scenario_tag,
                "match_type": "none",
                "matched_keyword": None,
                "score": 0.0
            })

    # 归一化得分：总得分 / 场景标签数 × 100%
    normalized_score = total_score / len(scenarios) if scenarios else 0.0

    return normalized_score, match_details


function match_scenario_tag(scenario_tag, match_keywords):
    """
    匹配场景标签与关键词
    返回: (match_type, matched_keyword)
    match_type: "exact" | "partial" | "none"
    """
    # Step 1: 精确匹配（完全字符串一致）
    for keyword in match_keywords:
        if scenario_tag == keyword:
            return ("exact", keyword)

    # Step 2: 包含匹配（场景标签包含关键词，或关键词包含场景标签）
    for keyword in match_keywords:
        if keyword in scenario_tag or scenario_tag in keyword:
            return ("exact", keyword)

    # Step 3: 同义词匹配（使用同义词词典）
    for keyword in match_keywords:
        if are_synonyms(scenario_tag, keyword):
            return ("partial", keyword)

    # Step 4: 上下位词匹配（使用 WordNet/领域本体）
    for keyword in match_keywords:
        if is_hypernym_or_hyponym(scenario_tag, keyword):
            return ("partial", keyword)

    # Step 5: 语义相似度匹配（使用词向量余弦相似度）
    for keyword in match_keywords:
        similarity = calculate_semantic_similarity(scenario_tag, keyword)
        if similarity >= 0.75:  # 语义相似度阈值
            return ("partial", keyword)

    return ("none", None)


function build_match_keywords(semantic_signals, task_type_mapping):
    """
    从语义信号和任务类型映射中构建匹配关键词集
    """
    keywords = set()

    # 内容主题关键词
    keywords.update(semantic_signals.content_theme_keywords)

    # 领域关键词（从领域引擎的关键词词典中提取）
    domain_engine = get_domain_engine(semantic_signals.domain)
    keywords.update(domain_engine.keyword_dict[:20])  # 取 Top-20 领域关键词

    # 受众关键词
    audience_keywords = {
        "academic": ["学术论文", "期刊投稿", "科学研究", "同行评审", "学术"],
        "general": ["大众", "公众", "通用", "科普"],
        "professional": ["专业", "行业", "职业", "实践"],
        "youth": ["青年", "学生", "教育", "学习"]
    }
    keywords.update(audience_keywords.get(semantic_signals.target_audience, []))

    # 任务类型关键词
    task_type_keywords = {
        "research_report": ["学术论文", "研究报告", "期刊", "科研"],
        "wechat_article": ["公众号", "文章", "杂志", "长文", "排版"],
        "course_material": ["课程", "讲义", "教学", "课件", "教育"],
        "data_visualization": ["数据可视化", "图表", "统计", "数据"]
    }
    keywords.update(task_type_keywords.get(task_type_mapping.task_type, []))

    return list(keywords)


function calculate_retrieval_confidence(scored_dlps):
    """
    计算检索置信度
    基于主 DLP 与备选 DLP 的分数差和主 DLP 的绝对分数
    """
    if not scored_dlps:
        return 0.0

    primary_score = scored_dlps[0]["score"]

    if len(scored_dlps) > 1:
        secondary_score = scored_dlps[1]["score"]
        # 分数差越大，置信度越高（主 DLP 明显优于备选）
        score_gap = primary_score - secondary_score
    else:
        score_gap = 0.0

    # 置信度 = 主 DLP 绝对分数 × 0.7 + 分数差 × 0.3
    confidence = primary_score * 0.7 + min(score_gap, 1.0) * 0.3

    return min(confidence, 1.0)
```

### 4.3 打分输出规范

```yaml
scoring_result:
  target_family: "academic-journal"
  scored_dlps:
    - dlp_name: "DLP-nature"
      dlp_family: "academic-journal"
      score: 0.85
      match_details:
        - scenario_tag: "学术论文"
          match_type: "exact"
          matched_keyword: "学术论文"
          score: 1.0
        - scenario_tag: "期刊投稿"
          match_type: "exact"
          matched_keyword: "期刊投稿"
          score: 1.0
        - scenario_tag: "科学研究"
          match_type: "exact"
          matched_keyword: "科学研究"
          score: 1.0
        - scenario_tag: "同行评审"
          match_type: "partial"
          matched_keyword: "学术"
          score: 0.5
    - dlp_name: "DLP-springer"
      dlp_family: "academic-journal"
      score: 0.62
      match_details: [...]
    - dlp_name: "DLP-science"
      dlp_family: "academic-journal"
      score: 0.50
      match_details: [...]
    - dlp_name: "DLP-ieee"
      dlp_family: "academic-journal"
      score: 0.25
      match_details: [...]
  primary_dlp:
    dlp_name: "DLP-nature"
    score: 0.85
  secondary_dlp:
    dlp_name: "DLP-springer"
    score: 0.62
  confidence: 0.70  # 0.85×0.7 + (0.85-0.62)×0.3 = 0.595+0.069 = 0.664
```

---

## 五、16 个 DLP 场景标签汇总表

### 5.1 完整场景标签汇总

下表汇总了 16 个 DLP 的完整场景标签（`applicable_scenarios`），供族内打分算法使用。

#### academic-journal 族（学术期刊族，4 个 DLP）

| DLP 名称 | 锚定实体 | 场景标签 | 族默认 |
|---------|---------|---------|--------|
| DLP-nature | Nature 正刊 2024 年版式 | 学术论文, 期刊投稿, 科学研究, 同行评审 | ✅ 默认锚点 |
| DLP-science | Science 正刊 2024 年版式 | 学术论文, 期刊投稿, 科学研究, 跨学科研究 | |
| DLP-ieee | IEEE/ACM 正刊 2024 年版式 | 学术论文, 期刊投稿, 工程研究, 计算机科学, 电子工程 | |
| DLP-springer | Springer Nature 期刊 2024 年版式 | 学术论文, 期刊投稿, 预印本, 科学研究 | |

#### interface-brand 族（界面品牌族，4 个 DLP）

| DLP 名称 | 锚定实体 | 场景标签 | 族默认 |
|---------|---------|---------|--------|
| DLP-linear | Linear.app 2024 年产品界面 | 产品界面, SaaS, 项目管理, 开发工具, 暗色模式 | ✅ 默认锚点 |
| DLP-aesop | Aesop 官网 2024 年品牌设计 | 品牌官网, 奢侈品, 护肤品, 编辑式排版, 暖色调 | |
| DLP-stripe-press | Stripe Press 2024 年界面 | 品牌官网, 金融科技, 出版物, 技术文档, 渐变设计 | |
| DLP-gov-uk | GOV.UK Design System 2024 | 政府网站, 公共服务, 无障碍优先, 编辑式落地页, 表单设计 | |

#### publication-typesetting 族（出版物排版族，4 个 DLP）

| DLP 名称 | 锚定实体 | 场景标签 | 族默认 |
|---------|---------|---------|--------|
| DLP-economist | The Economist 2024 年版式 | 杂志文章, 新闻评论, 经济分析, 长文排版, 多栏布局 | ✅ 默认锚点 |
| DLP-ted | TED 演讲幻灯片 2024 版式 | 演示文稿, TED风格, 极简电影感, 大字号, 留白驱动 | |
| DLP-newyorker | The New Yorker 2024 版式 | 杂志文章, 文学评论, 长文叙事, 文化评论, 多栏布局 | |
| DLP-kami | Kami 纸质美学 2024 版式 | 阅读体验, 纸感美学, 米色底调, 衬线字体, 高级出版物, 散文, 随笔 | |

#### data-visualization 族（数据可视化族，4 个 DLP）

| DLP 名称 | 锚定实体 | 场景标签 | 族默认 |
|---------|---------|---------|--------|
| DLP-economist-chart | The Economist 数据图表 2024 | 数据可视化, 经济数据, 新闻图表, 统计图表, 清晰克制 | ✅ 默认锚点 |
| DLP-scienceplots | SciencePlots Python 库风格 | 学术论文配图, Matplotlib, 科学绘图, 顶刊配色, 矢量图 | |
| DLP-nature-figure | Nature 图表规范 2024 | Nature配图, 学术配图, 矢量图, 印刷级, 机制示意图 | |
| DLP-plotivy | Plotly 美学模板 2024 | 期刊配图, 自动校准, 出版级参数, 多期刊兼容, LaTeX渲染 | |

### 5.2 场景标签去重索引

为加速族内打分算法的匹配过程，以下为 16 个 DLP 所有场景标签的去重索引（共 42 个唯一标签）：

| 场景标签 | 所属 DLP（可多个） |
|---------|------------------|
| 学术论文 | DLP-nature, DLP-science, DLP-ieee, DLP-springer |
| 期刊投稿 | DLP-nature, DLP-science, DLP-ieee, DLP-springer |
| 科学研究 | DLP-nature, DLP-science, DLP-springer |
| 同行评审 | DLP-nature |
| 跨学科研究 | DLP-science |
| 工程研究 | DLP-ieee |
| 计算机科学 | DLP-ieee |
| 电子工程 | DLP-ieee |
| 预印本 | DLP-springer |
| 产品界面 | DLP-linear |
| SaaS | DLP-linear |
| 项目管理 | DLP-linear |
| 开发工具 | DLP-linear |
| 暗色模式 | DLP-linear |
| 品牌官网 | DLP-aesop, DLP-stripe-press |
| 奢侈品 | DLP-aesop |
| 护肤品 | DLP-aesop |
| 编辑式排版 | DLP-aesop |
| 暖色调 | DLP-aesop |
| 金融科技 | DLP-stripe-press |
| 出版物 | DLP-stripe-press |
| 技术文档 | DLP-stripe-press |
| 渐变设计 | DLP-stripe-press |
| 政府网站 | DLP-gov-uk |
| 公共服务 | DLP-gov-uk |
| 无障碍优先 | DLP-gov-uk |
| 编辑式落地页 | DLP-gov-uk |
| 表单设计 | DLP-gov-uk |
| 杂志文章 | DLP-economist, DLP-newyorker |
| 新闻评论 | DLP-economist |
| 经济分析 | DLP-economist |
| 长文排版 | DLP-economist |
| 多栏布局 | DLP-economist, DLP-newyorker |
| 演示文稿 | DLP-ted |
| TED风格 | DLP-ted |
| 极简电影感 | DLP-ted |
| 大字号 | DLP-ted |
| 留白驱动 | DLP-ted |
| 文学评论 | DLP-newyorker |
| 长文叙事 | DLP-newyorker |
| 文化评论 | DLP-newyorker |
| 阅读体验 | DLP-kami |
| 纸感美学 | DLP-kami |
| 米色底调 | DLP-kami |
| 衬线字体 | DLP-kami |
| 高级出版物 | DLP-kami |
| 散文 | DLP-kami |
| 随笔 | DLP-kami |
| 数据可视化 | DLP-economist-chart |
| 经济数据 | DLP-economist-chart |
| 新闻图表 | DLP-economist-chart |
| 统计图表 | DLP-economist-chart |
| 清晰克制 | DLP-economist-chart |
| 学术论文配图 | DLP-scienceplots |
| Matplotlib | DLP-scienceplots |
| 科学绘图 | DLP-scienceplots |
| 顶刊配色 | DLP-scienceplots |
| 矢量图 | DLP-scienceplots, DLP-nature-figure |
| Nature配图 | DLP-nature-figure |
| 学术配图 | DLP-nature-figure |
| 印刷级 | DLP-nature-figure |
| 机制示意图 | DLP-nature-figure |
| 期刊配图 | DLP-plotivy |
| 自动校准 | DLP-plotivy |
| 出版级参数 | DLP-plotivy |
| 多期刊兼容 | DLP-plotivy |
| LaTeX渲染 | DLP-plotivy |

---

## 六、适配器输出

### 6.1 DLP 12 字段 → design_tokens 映射

适配器将 DLP 的 12 字段规范转换为 UIR v2.0 可消费的 `design_tokens` 对象。`design_tokens` 是 `visual_dna` 的具象锚点层，所有视觉参数可追溯到 DLP 锚定实体。

| DLP 字段 | design_tokens 字段 | 映射规则 |
|---------|-------------------|---------|
| `color_palette` (6 色板) | `color_palette` | 6 色直接映射：primary/secondary/accent/neutral/background/text |
| `typography_scale` (字号阶梯) | `typography.scale` | h1-h4/body/caption/footnote 字号直接映射 |
| `font_stack` (字体栈) | `typography.font_stack` | western/chinese/monospace 三栈直接映射 |
| `font_weight_pairing` (字重配对) | `typography.weight_pairing` | heading/body/emphasis 字重直接映射 |
| `spacing_system` (间距系统) | `spacing` | base + scale 数组直接映射 |
| `grid_system` (栅格系统) | `grid` | columns/gutter/margin/breakpoints 直接映射 |
| `radius_shadow` (圆角阴影) | `radius` + `shadow` | 拆分为 radius（card/button/input）和 shadow（light/medium） |
| `motion_curve` (动效曲线) | `motion` | easing + duration 直接映射（印刷媒介填 N/A） |
| `name` | `dlp_anchor` | DLP 名称作为可追溯锚点 |
| `anchor` | `dlp_anchor_description` | 锚定实体描述 |
| `family` | `dlp_family` | 族分类 |
| `applicable_scenarios` | `dlp_scenarios` | 场景标签列表 |

### 6.2 design_tokens 完整结构

```yaml
design_tokens:
  # ---- 可追溯锚点 ----
  dlp_anchor: "DLP-nature"                          # 命中的 DLP 名称
  dlp_anchor_description: "Nature 正刊 2024 年版式"  # 锚定实体描述
  dlp_family: "academic-journal"                     # 族分类

  # ---- 配色方案（6 色板）----
  color_palette:
    primary: "#000000"       # 主色 — 标题、重点强调、链接
    secondary: "#E60012"     # 辅色 — 次要强调、数据高亮
    accent: "#0066CC"        # 强调色 — 关键警示、CTA
    neutral: "#6C757D"       # 中性色 — 次要文字、图注
    background: "#FFFFFF"    # 背景色 — 页面主背景
    text: "#1A1A1A"          # 文本色 — 正文主文字色

  # ---- 字体方案 ----
  typography:
    # 字号阶梯
    scale:
      h1: "24px/1.5rem"       # 文章主标题
      h2: "18px/1.125rem"     # 一级章节标题
      h3: "16px/1rem"         # 二级章节标题
      h4: "14px/0.875rem"     # 三级章节标题
      body: "10pt/13.33px"    # 正文
      caption: "8pt/10.67px"  # 图注
      footnote: "7pt/9.33px"  # 脚注
    # 字体栈
    font_stack:
      western: '"Times New Roman", "STIX Two Text", serif'
      chinese: '"宋体", "SimSun", serif'
      monospace: '"Courier New", monospace'
    # 字重配对
    weight_pairing:
      heading: "bold(700)"    # 标题字重
      body: "regular(400)"    # 正文字重
      emphasis: "italic(400)" # 强调字重

  # ---- 间距系统 ----
  spacing:
    base: "4px"                       # 基准单位
    scale: [4, 8, 12, 16, 24, 32]     # 间距阶梯（px 数组）

  # ---- 栅格系统 ----
  grid:
    columns: "双栏"                   # 列数（单栏/双栏/三栏/四栏/12列）
    gutter: "0.5cm"                   # 槽宽
    margin: "2cm"                     # 页边距
    breakpoints: "N/A(印刷媒介)"       # 断点（印刷媒介为 N/A）

  # ---- 圆角 ----
  radius:
    card: "0px"       # 卡片圆角
    button: "0px"     # 按钮圆角
    input: "0px"      # 输入框圆角

  # ---- 阴影 ----
  shadow:
    light: "none"     # 轻微阴影
    medium: "none"    # 中等阴影

  # ---- 动效 ----
  motion:
    duration: "N/A"                    # 动效时长（印刷媒介为 N/A）
    easing: "N/A(印刷媒介)"             # 缓动函数（印刷媒介为 N/A）

  # ---- 场景标签（可追溯）----
  dlp_scenarios:
    - "学术论文"
    - "期刊投稿"
    - "科学研究"
    - "同行评审"
```

### 6.3 适配器伪代码

```python
# ============================================================
# DLP 检索器 — 适配器算法
# 输入: primary_dlp（命中的 DLP 对象，含 12 字段完整定义）
# 输出: design_tokens 对象（供 visual_dna.md 消费）
# ============================================================

function adapt_dlp_to_design_tokens(primary_dlp):
    """
    将 DLP 的 12 字段规范转换为 UIR v2.0 可消费的 design_tokens 对象
    """

    design_tokens = {
        # ---- 可追溯锚点 ----
        "dlp_anchor": primary_dlp.name,
        "dlp_anchor_description": primary_dlp.anchor,
        "dlp_family": primary_dlp.family,

        # ---- 配色方案（6 色板直接映射）----
        "color_palette": {
            "primary": primary_dlp.color_palette.primary,
            "secondary": primary_dlp.color_palette.secondary,
            "accent": primary_dlp.color_palette.accent,
            "neutral": primary_dlp.color_palette.neutral,
            "background": primary_dlp.color_palette.background,
            "text": primary_dlp.color_palette.text
        },

        # ---- 字体方案 ----
        "typography": {
            "scale": {
                "h1": primary_dlp.typography_scale.h1,
                "h2": primary_dlp.typography_scale.h2,
                "h3": primary_dlp.typography_scale.h3,
                "h4": primary_dlp.typography_scale.h4,
                "body": primary_dlp.typography_scale.body,
                "caption": primary_dlp.typography_scale.caption,
                "footnote": primary_dlp.typography_scale.footnote
            },
            "font_stack": {
                "western": primary_dlp.font_stack.western,
                "chinese": primary_dlp.font_stack.chinese,
                "monospace": primary_dlp.font_stack.monospace
            },
            "weight_pairing": {
                "heading": primary_dlp.font_weight_pairing.heading,
                "body": primary_dlp.font_weight_pairing.body,
                "emphasis": primary_dlp.font_weight_pairing.emphasis
            }
        },

        # ---- 间距系统 ----
        "spacing": {
            "base": primary_dlp.spacing_system.base,
            "scale": parse_scale_string(primary_dlp.spacing_system.scale)
        },

        # ---- 栅格系统 ----
        "grid": {
            "columns": primary_dlp.grid_system.columns,
            "gutter": primary_dlp.grid_system.gutter,
            "margin": primary_dlp.grid_system.margin,
            "breakpoints": primary_dlp.grid_system.breakpoint
        },

        # ---- 圆角（从 radius_shadow 拆分）----
        "radius": extract_radius(primary_dlp.radius_shadow),

        # ---- 阴影（从 radius_shadow 拆分）----
        "shadow": extract_shadow(primary_dlp.radius_shadow),

        # ---- 动效 ----
        "motion": {
            "duration": primary_dlp.motion_curve.duration,
            "easing": primary_dlp.motion_curve.easing
        },

        # ---- 场景标签 ----
        "dlp_scenarios": primary_dlp.applicable_scenarios
    }

    return design_tokens


function extract_radius(radius_shadow):
    """
    从 DLP 的 radius_shadow 字段拆分出圆角对象
    支持两种格式：
    1. 单一圆角值（如 "0px"）→ 统一应用到 card/button/input
    2. 分层圆角值（如 card_radius/button_radius/input_radius）→ 分别映射
    """
    if hasattr(radius_shadow, "card_radius"):
        return {
            "card": radius_shadow.card_radius,
            "button": radius_shadow.button_radius,
            "input": radius_shadow.input_radius
        }
    else:
        # 单一圆角值统一应用
        unified_radius = radius_shadow.radius if hasattr(radius_shadow, "radius") else "0px"
        return {
            "card": unified_radius,
            "button": unified_radius,
            "input": unified_radius
        }


function extract_shadow(radius_shadow):
    """
    从 DLP 的 radius_shadow 字段拆分出阴影对象
    支持两种格式：
    1. 单一阴影值（如 "none"）→ 统一应用到 light/medium
    2. 分层阴影值（如 shadow_light/shadow_medium）→ 分别映射
    """
    if hasattr(radius_shadow, "shadow_light"):
        return {
            "light": radius_shadow.shadow_light,
            "medium": radius_shadow.shadow_medium
        }
    else:
        unified_shadow = radius_shadow.shadow if hasattr(radius_shadow, "shadow") else "none"
        return {
            "light": unified_shadow,
            "medium": unified_shadow
        }


function parse_scale_string(scale_str):
    """
    将间距阶梯字符串（如 "4/8/12/16/24/32px"）解析为数组
    """
    if isinstance(scale_str, list):
        return scale_str
    # 移除 px 后缀，按 / 分割，转为整数数组
    cleaned = scale_str.replace("px", "")
    parts = cleaned.split("/")
    return [int(p.strip()) for p in parts]
```

### 6.4 适配器输出与 visual_dna 的对接

`design_tokens` 对象生成后，由 `visual-dna.md` 消费，注入 `visual_dna` 的各字段：

| design_tokens 字段 | visual_dna 字段 | 映射规则 |
|-------------------|----------------|---------|
| `color_palette.primary` | `color_scheme.--color-primary` | 直接映射 |
| `color_palette.secondary` | `color_scheme.--color-secondary` | 直接映射 |
| `color_palette.accent` | `color_scheme.--color-accent` | 直接映射 |
| `color_palette.neutral` | `color_scheme.--color-text-secondary` | 直接映射 |
| `color_palette.background` | `color_scheme.--color-bg` | 直接映射 |
| `color_palette.text` | `color_scheme.--color-text` | 直接映射 |
| `typography.font_stack.western` | `font_scheme` 标题/正文西文字体 | 作为 font-family 首选 |
| `typography.font_stack.chinese` | `font_scheme` 标题/正文中文 fallback | 作为 font-family 中文 fallback |
| `typography.font_stack.monospace` | `font_scheme` 代码字体 | 作为 code/pre 的 font-family |
| `typography.scale` | `font_scheme` 字号阶梯 | 直接映射 |
| `typography.weight_pairing` | `font_scheme` 字重配对 | 直接映射 |
| `spacing` | `grid_system` 间距规范 | 直接映射 |
| `grid` | `grid_system` 栅格参数 | 直接映射 |
| `radius` | `line_style` 圆角规范 | 直接映射 |
| `shadow` | `line_style` 阴影规范 | 直接映射 |
| `motion` | `motion_profile` 动效配置 | 直接映射（N/A 时禁用动效） |

---

## 七、质量保持策略

### 7.1 质量保持触发条件

质量保持策略在以下情况触发：

| 触发条件 | 判定标准 | 质量保持动作 |
|---------|---------|---------|
| 置信度不足 | 检索置信度 < 0.6 | 回退到任务类型映射的默认族 |
| 族内全部 DLP 得分为 0 | 所有 DLP 的场景标签均不匹配 | 使用族默认锚点 |
| 语义信号提取失败 | 提取置信度 < 0.3 | 使用全局默认 DLP-nature |
| 任务类型未知 | 任务类型不在 4 种已知类型中 | 默认 research_report 映射 |
| UIR 文档缺失 | §1-§8 全息框架不完整 | 使用全局默认 DLP-nature |

### 7.2 质量保持链路

```
正常检索（置信度 ≥ 0.6）
  ↓ 质量保持触发
Level 1: 回退到任务类型映射的默认族
  ↓ 仍无法满足
Level 2: 在默认族内选择场景标签最通用的 DLP
  ↓ 仍无法满足
Level 3: 使用全局默认 DLP-nature（学术严谨默认锚点）
```

> **Level 3 质量保持与 Golden Set 对应关系**: DLP-nature 是 16 个 DLP 之一（academic-journal 族），Golden Set 中包含 GS-nature-01/02/03 三个样本。Level 3 质量保持为 DLP-nature 时，Golden Set 距离校验（`golden-set-validator.md`）使用 GS-nature-01/02/03 样本作为距离基准——即质量保持方案的 Golden Set 距离计算以 DLP-nature 对应的 3 个 Golden 样本为参照，确保质量保持方案与 Golden Set 校验的 DLP 锚点一致，避免质量保持后 DLP 与 Golden Set 样本不匹配导致的距离校验异常。

### 7.3 默认族与默认 DLP 映射

| 任务类型 | 默认族 | 默认 DLP | 质量保持理由 |
|---------|--------|---------|---------|
| research_report | academic-journal | DLP-nature | 学术严谨是 research_report 的最安全默认 |
| wechat_article | publication-typesetting | DLP-economist | 杂志级排版是 wechat_article 的最安全默认 |
| course_material | interface-brand | DLP-linear | 清晰界面层级是 course_material 的最安全默认 |
| data_visualization | data-visualization | DLP-economist-chart | 清晰克制是数据可视化的最安全默认 |
| 未知/全局默认 | academic-journal | DLP-nature | 学术严谨是全局最安全默认 |

### 7.4 质量保持策略伪代码

```python
# ============================================================
# DLP 检索器 — 质量保持策略算法
# 输入: scoring_result + task_type_mapping + semantic_signals
# 输出: final_dlp + exhaust_retry_log
# ============================================================

function apply_exhaust_retry_strategy(scoring_result, task_type_mapping, semantic_signals):
    """
    质量保持策略：当检索置信度不足时，回退到默认族默认 DLP
    """

    exhaust_retry_log = []
    confidence = scoring_result.confidence if scoring_result else 0.0

    # ---- Level 0: 正常检索（置信度 ≥ 0.6）----
    if confidence >= 0.6 and scoring_result.primary_dlp is not None:
        exhaust_retry_log.append({
            "level": 0,
            "trigger": "none",
            "action": "使用正常检索结果",
            "dlp": scoring_result.primary_dlp.dlp_name,
            "confidence": confidence
        })
        return {
            "final_dlp": scoring_result.primary_dlp,
            "secondary_dlp": scoring_result.secondary_dlp,
            "exhaust_retry_used": False,
            "exhaust_retry_log": exhaust_retry_log,
            "final_confidence": confidence
        }

    # ---- Level 1: 回退到任务类型映射的默认族 ----
    exhaust_retry_log.append({
        "level": 1,
        "trigger": f"置信度 {confidence:.2f} < 0.6" if confidence < 0.6 else "主 DLP 为空",
        "action": f"回退到任务类型 {task_type_mapping.task_type} 的默认族 {task_type_mapping.primary_family}",
        "confidence": confidence
    })

    # 获取默认族
    default_family = task_type_mapping.primary_family

    # 获取默认族的默认 DLP
    FAMILY_DEFAULT_DLP = {
        "academic-journal": "DLP-nature",
        "interface-brand": "DLP-linear",
        "publication-typesetting": "DLP-economist",
        "data-visualization": "DLP-economist-chart"
    }

    default_dlp_name = FAMILY_DEFAULT_DLP.get(default_family, "DLP-nature")

    # ---- Level 2: 在默认族内选择场景标签最通用的 DLP ----
    # 检查默认 DLP 是否可用
    default_dlp = get_dlp_by_name(default_dlp_name)

    if default_dlp is not None:
        exhaust_retry_log.append({
            "level": 2,
            "trigger": "默认族默认 DLP 可用",
            "action": f"使用默认族 {default_family} 的默认 DLP {default_dlp_name}",
            "dlp": default_dlp_name,
            "confidence": 0.5  # 质量保持后的固定置信度
        })
        return {
            "final_dlp": {
                "dlp_name": default_dlp_name,
                "dlp_family": default_family,
                "score": 0.5,
                "match_details": [],
                "applicable_scenarios": default_dlp.applicable_scenarios
            },
            "secondary_dlp": None,
            "exhaust_retry_used": True,
            "exhaust_retry_log": exhaust_retry_log,
            "final_confidence": 0.5
        }

    # ---- Level 3: 使用全局默认 DLP-nature ----
    exhaust_retry_log.append({
        "level": 3,
        "trigger": f"默认族 {default_family} 的默认 DLP {default_dlp_name} 不可用",
        "action": "使用全局默认 DLP-nature（学术严谨默认锚点）",
        "dlp": "DLP-nature",
        "confidence": 0.3  # 全局默认的固定置信度
    })

    global_default_dlp = get_dlp_by_name("DLP-nature")

    return {
        "final_dlp": {
            "dlp_name": "DLP-nature",
            "dlp_family": "academic-journal",
            "score": 0.3,
            "match_details": [],
            "applicable_scenarios": global_default_dlp.applicable_scenarios
        },
        "secondary_dlp": None,
        "exhaust_retry_used": True,
        "exhaust_retry_log": exhaust_retry_log,
        "final_confidence": 0.3
    }
```

### 7.5 质量保持策略输出规范

```yaml
exhaust_retry_result:
  final_dlp:
    dlp_name: "DLP-nature"
    dlp_family: "academic-journal"
    score: 0.5
    match_details: []
    applicable_scenarios:
      - "学术论文"
      - "期刊投稿"
      - "科学研究"
      - "同行评审"
  secondary_dlp: null
  exhaust_retry_used: true
  exhaust_retry_log:
    - level: 1
      trigger: "置信度 0.45 < 0.6"
      action: "回退到任务类型 research_report 的默认族 academic-journal"
      confidence: 0.45
    - level: 2
      trigger: "默认族默认 DLP 可用"
      action: "使用默认族 academic-journal 的默认 DLP DLP-nature"
      dlp: "DLP-nature"
      confidence: 0.5
  final_confidence: 0.5
```

---

## 八、完整检索流程伪代码

### 8.1 主流程

```python
# ============================================================
# DLP 检索器 — 完整检索主流程
# 输入: UIR v2.0 文档 + 显式任务类型（可选）+ 用户偏好（可选）
# 输出: dlp_retriever_output（含主 DLP + 备选 DLP + design_tokens + 置信度）
# ============================================================

function dlp_retriever(uir_document, explicit_task_type=None, user_preference=None):
    """
    DLP 检索器主入口
    将 Visual DNA 中枢从"生成器"转变为"选择器 + 适配器"
    """

    # ============================================================
    # Step 1: 语义信号提取（从 UIR v2.0 §1-§8 全息框架）
    # ============================================================
    semantic_signals = extract_semantic_signals(uir_document)

    # ============================================================
    # Step 2: 任务类型映射（4 种任务类型 → 4 族优先级）
    # ============================================================
    task_type_mapping = map_task_type(semantic_signals, explicit_task_type)

    # ============================================================
    # Step 3: 族预筛选（确定目标族）
    # ============================================================
    # 优先在 primary_family 中检索
    # 如果 primary_family 检索置信度低，在 secondary_family 中补充检索
    target_family = task_type_mapping.primary_family

    # ============================================================
    # Step 4: 族内打分（目标族内 4 个 DLP 按场景标签匹配度打分）
    # ============================================================
    scoring_result = score_dlps_in_family(
        target_family=target_family,
        semantic_signals=semantic_signals,
        task_type_mapping=task_type_mapping
    )

    # ============================================================
    # Step 5: 质量保持策略（置信度不足时回退到默认族默认 DLP）
    # ============================================================
    exhaust_retry_result = apply_exhaust_retry_strategy(
        scoring_result=scoring_result,
        task_type_mapping=task_type_mapping,
        semantic_signals=semantic_signals
    )

    # ============================================================
    # Step 6: 适配器输出（DLP 12 字段 → design_tokens 对象）
    # ============================================================
    final_dlp_name = exhaust_retry_result.final_dlp.dlp_name
    final_dlp_object = get_dlp_by_name(final_dlp_name)
    design_tokens = adapt_dlp_to_design_tokens(final_dlp_object)

    # ============================================================
    # Step 7: 组装最终输出
    # ============================================================
    dlp_retriever_output = {
        # 检索结果
        "matched_dlp": final_dlp_name,
        "matched_family": exhaust_retry_result.final_dlp.dlp_family,
        "match_score": exhaust_retry_result.final_dlp.score,
        "exhaust_retry_used": exhaust_retry_result.exhaust_retry_used,
        "exhaust_retry_reason": exhaust_retry_result.exhaust_retry_log[-1]["trigger"] if exhaust_retry_result.exhaust_retry_used else None,

        # 备选 DLP
        "secondary_dlp": exhaust_retry_result.secondary_dlp.dlp_name if exhaust_retry_result.secondary_dlp else None,
        "secondary_dlp_score": exhaust_retry_result.secondary_dlp.score if exhaust_retry_result.secondary_dlp else None,

        # 候选 DLP 列表（完整打分排名）
        "candidate_dlps": [
            {
                "dlp": item.dlp_name,
                "score": item.score,
                "family": item.dlp_family
            }
            for item in (scoring_result.scored_dlps if scoring_result else [])
        ],

        # 语义信号
        "semantic_signals": semantic_signals,

        # 任务类型映射
        "task_type_mapping": task_type_mapping,

        # 适配器输出（供 visual_dna.md 消费）
        "design_tokens": design_tokens,

        # 质量保持日志
        "exhaust_retry_log": exhaust_retry_result.exhaust_retry_log,

        # 最终置信度
        "confidence": exhaust_retry_result.final_confidence,

        # 可追溯锚点声明
        "visual_dna_anchor": f"{final_dlp_name} 的 12 字段将作为 visual_dna 生成的具象锚点"
    }

    return dlp_retriever_output
```

### 8.2 完整输出规范

```yaml
dlp_retriever_output:
  # ---- 检索结果 ----
  matched_dlp: "DLP-nature"
  matched_family: "academic-journal"
  match_score: 0.85
  exhaust_retry_used: false
  exhaust_retry_reason: null

  # ---- 备选 DLP ----
  secondary_dlp: "DLP-springer"
  secondary_dlp_score: 0.62

  # ---- 候选 DLP 列表 ----
  candidate_dlps:
    - dlp: "DLP-nature"
      score: 0.85
      family: "academic-journal"
    - dlp: "DLP-springer"
      score: 0.62
      family: "academic-journal"
    - dlp: "DLP-science"
      score: 0.50
      family: "academic-journal"
    - dlp: "DLP-ieee"
      score: 0.25
      family: "academic-journal"

  # ---- 语义信号 ----
  semantic_signals:
    content_theme: "科技/数据/AI"
    content_theme_keywords: ["大语言模型", "多智能体", "认知架构", "..."]
    domain: "tech-engine"
    domain_candidates: ["tech-engine", "cognitive-science-engine"]
    target_audience: "academic"
    extraction_confidence: 0.85

  # ---- 任务类型映射 ----
  task_type_mapping:
    task_type: "research_report"
    primary_family: "academic-journal"
    secondary_family: "data-visualization"
    rationale: "学术研究报告需要严谨的期刊版式，数据图表作为补充"

  # ---- 适配器输出 ----
  design_tokens:
    dlp_anchor: "DLP-nature"
    dlp_anchor_description: "Nature 正刊 2024 年版式"
    dlp_family: "academic-journal"
    color_palette:
      primary: "#000000"
      secondary: "#E60012"
      accent: "#0066CC"
      neutral: "#6C757D"
      background: "#FFFFFF"
      text: "#1A1A1A"
    typography:
      scale:
        h1: "24px/1.5rem"
        h2: "18px/1.125rem"
        h3: "16px/1rem"
        h4: "14px/0.875rem"
        body: "10pt/13.33px"
        caption: "8pt/10.67px"
        footnote: "7pt/9.33px"
      font_stack:
        western: '"Times New Roman", "STIX Two Text", serif'
        chinese: '"宋体", "SimSun", serif'
        monospace: '"Courier New", monospace'
      weight_pairing:
        heading: "bold(700)"
        body: "regular(400)"
        emphasis: "italic(400)"
    spacing:
      base: "4px"
      scale: [4, 8, 12, 16, 24, 32]
    grid:
      columns: "双栏"
      gutter: "0.5cm"
      margin: "2cm"
      breakpoints: "N/A(印刷媒介)"
    radius:
      card: "0px"
      button: "0px"
      input: "0px"
    shadow:
      light: "none"
      medium: "none"
    motion:
      duration: "N/A"
      easing: "N/A(印刷媒介)"
    dlp_scenarios:
      - "学术论文"
      - "期刊投稿"
      - "科学研究"
      - "同行评审"

  # ---- 质量保持日志 ----
  exhaust_retry_log:
    - level: 0
      trigger: "none"
      action: "使用正常检索结果"
      dlp: "DLP-nature"
      confidence: 0.85

  # ---- 最终置信度 ----
  confidence: 0.85

  # ---- 可追溯锚点声明 ----
  visual_dna_anchor: "DLP-nature 的 12 字段将作为 visual_dna 生成的具象锚点"
```

---

## 九、与其他文件的对接

### 9.1 引用 `design-language-profiles/` 目录下的 16 个 DLP 文件

DLP 检索器的检索源是 `design-language-profiles/` 目录下的 16 个 DLP 文件。每个 DLP 文件包含完整的 12 字段 YAML frontmatter 定义，DLP 检索器通过读取这些文件获取 DLP 的 `applicable_scenarios`（场景标签）和 12 字段完整规范。

| DLP 文件 | 族 | DLP 检索器读取的字段 |
|---------|-----|---------------------|
| `DLP-nature.md` | academic-journal | applicable_scenarios + 12 字段 |
| `DLP-science.md` | academic-journal | applicable_scenarios + 12 字段 |
| `DLP-ieee.md` | academic-journal | applicable_scenarios + 12 字段 |
| `DLP-springer.md` | academic-journal | applicable_scenarios + 12 字段 |
| `DLP-linear.md` | interface-brand | applicable_scenarios + 12 字段 |
| `DLP-aesop.md` | interface-brand | applicable_scenarios + 12 字段 |
| `DLP-stripe-press.md` | interface-brand | applicable_scenarios + 12 字段 |
| `DLP-gov-uk.md` | interface-brand | applicable_scenarios + 12 字段 |
| `DLP-economist.md` | publication-typesetting | applicable_scenarios + 12 字段 |
| `DLP-ted.md` | publication-typesetting | applicable_scenarios + 12 字段 |
| `DLP-newyorker.md` | publication-typesetting | applicable_scenarios + 12 字段 |
| `DLP-kami.md` | publication-typesetting | applicable_scenarios + 12 字段 |
| `DLP-economist-chart.md` | data-visualization | applicable_scenarios + 12 字段 |
| `DLP-scienceplots.md` | data-visualization | applicable_scenarios + 12 字段 |
| `DLP-nature-figure.md` | data-visualization | applicable_scenarios + 12 字段 |
| `DLP-plotivy.md` | data-visualization | applicable_scenarios + 12 字段 |

### 9.2 输出 `design_tokens` 对象供 `visual-dna.md` 消费

DLP 检索器输出的 `design_tokens` 对象由 `visual-dna.md` 消费，注入 `visual_dna` 的各字段。对接流程如下：

```
DLP 检索器输出 design_tokens
  ↓
visual-dna.md §一 生成流程接收 design_tokens
  ↓
visual-dna.md 将 design_tokens 注入 visual_dna 对象:
  - design_tokens.color_palette → visual_dna.color_scheme
  - design_tokens.typography → visual_dna.font_scheme
  - design_tokens.spacing → visual_dna.grid_system（间距部分）
  - design_tokens.grid → visual_dna.grid_system（栅格部分）
  - design_tokens.radius → visual_dna.line_style（圆角部分）
  - design_tokens.shadow → visual_dna.line_style（阴影部分）
  - design_tokens.motion → visual_dna.motion_profile
  ↓
visual_dna 对象（带 DLP 锚点的抽象描述符）
  ↓
Taste-Skill 仲裁
  ↓
渲染管道消费 visual_dna
```

### 9.3 与 `taste-skill-consumer.md` 的三旋钮系统协同

DLP 检索器与 `taste-skill-consumer.md` 的三旋钮系统（DV/MI/VD）协同工作。DLP 检索器提供**具象锚点**（DLP 的 12 字段规范），三旋钮系统提供**微调参数**（对 DLP 锚点的偏差控制）。

| 协同维度 | DLP 检索器职责 | 三旋钮系统职责 | 协同规则 |
|---------|--------------|--------------|---------|
| 配色 | 提供 DLP 6 色板作为基色 | 不直接调整配色 | 三旋钮不覆盖 DLP 配色，配色以 DLP 为准 |
| 字体 | 提供 DLP 字体栈与字号阶梯 | 不直接调整字体 | 三旋钮不覆盖 DLP 字体，字体以 DLP 为准 |
| 布局对称性 | 提供 DLP 栅格系统 | DESIGN_VARIANCE (DV) 控制布局对称性 | DV 在 DLP 栅格基础上微调对称/不对称程度 |
| 动效强度 | 提供 DLP 动效曲线（或 N/A） | MOTION_INTENSITY (MI) 控制动效强度 | MI 在 DLP 动效基础上微调强度；DLP 为 N/A 时 MI 强制为 1-3 |
| 信息密度 | 提供 DLP 间距系统 | VISUAL_DENSITY (VD) 控制信息密度 | VD 在 DLP 间距基础上微调密度；VD > 7 时间距缩小，VD < 4 时间距放大 |

**协同流程**：

```
Step 1: DLP 检索器命中 DLP-{entity}，输出 design_tokens
  ↓
Step 2: taste-skill-consumer.md 读取 design_tokens，作为 visual_dna 的具象基线
  ↓
Step 3: taste-skill-consumer.md 根据三旋钮（DV/MI/VD）对 design_tokens 进行微调:
  - DV 微调布局对称性（在 DLP 栅格基础上）
  - MI 微调动效强度（在 DLP 动效基础上，DLP 为 N/A 时仅允许 CSS 过渡）
  - VD 微调信息密度（在 DLP 间距基础上）
  ↓
Step 4: 微调后的 visual_dna 对象下发至渲染管道
  ↓
Step 5: 所有渲染输出可追溯到 DLP-{entity} 的具象参数 + 三旋钮微调参数
```

**协同约束**：

1. **DLP 优先原则**: 三旋钮微调不得覆盖 DLP 的硬性规范（如 DLP 圆角为 0px 时，三旋钮不得添加圆角）
2. **印刷媒介约束**: DLP 动效为 N/A（印刷媒介）时，MI 强制限制在 1-3 范围（仅允许 CSS 过渡）
3. **配色不可变性**: 三旋钮不得修改 DLP 的 6 色板，配色以 DLP 为唯一真实源
4. **字体不可变性**: 三旋钮不得修改 DLP 的字体栈和字号阶梯，字体以 DLP 为唯一真实源
5. **仲裁优先级**: 当 DLP 规范与三旋钮微调冲突时，以 DLP 规范为准（硬冲突拒绝覆盖）

### 9.4 与 `design-language-profiles/README.md` §4 检索规范的关系

本文件是 `design-language-profiles/README.md` §4 检索规范的深度实现：

| README §4 定义 | 本文件实现 |
|---------------|---------|
| §4.1 检索输入（3 参数） | §二 语义信号提取算法（从 UIR §1-§8 提取 3 类信号） |
| §4.2 检索算法（4 步） | §三 + §四 + §七 完整实现（任务映射 + 族内打分 + 质量保持策略） |
| §4.3 检索映射表 | §三 任务类型映射表 + §五 16 DLP 场景标签汇总表 |
| §4.4 检索回退策略 | §七 质量保持策略（3 级质量保持链路） |
| §4.5 检索输出规范 | §八 完整输出规范（含 design_tokens） |

**本文件相对 README §4 的增强**：

1. **语义信号提取**: README §4.1 仅定义 3 参数输入，本文件 §二 增加了从 UIR v2.0 §1-§8 全息框架提取语义信号的完整算法
2. **任务类型映射**: README §4.2 未区分任务类型，本文件 §三 增加了 4 种任务类型到 4 族的完整映射
3. **族内打分**: README §4.2 仅给出匹配度公式，本文件 §四 增加了完整的族内打分伪代码（含完全匹配/部分匹配/不匹配三档）
4. **适配器输出**: README §4.5 仅输出 DLP 名称，本文件 §六 增加了 DLP 12 字段到 design_tokens 的完整适配器
5. **质量保持策略**: README §4.4 仅给出回退表，本文件 §七 增加了 3 级质量保持链路的完整伪代码
6. **三旋钮协同**: README 未涉及与 taste-skill-consumer.md 的协同，本文件 §九.3 增加了三旋钮系统协同规范

---

## 十、穷尽重试策略

| 穷尽重试路径 | 触发条件 | 行为 |
|-------------|---------|------|
| 正常检索 → Level 1 质量保持 | 置信度 < 0.6 | 回退到任务类型映射的默认族 |
| Level 1 → Level 2 质量保持 | 默认族默认 DLP 不可用 | 在默认族内选择场景标签最通用的 DLP |
| Level 2 → Level 3 质量保持 | 默认族内无可用 DLP | 使用全局默认 DLP-nature |
| Level 3 → 硬编码兜底 | DLP-nature 文件也不可用 | 使用硬编码的 DLP-nature 12 字段默认值 |
| 语义信号提取失败 → 默认信号 | UIR 文档 §1-§8 不完整 | 使用默认信号：content_theme="通用", domain="general-engine", target_audience="academic" |
| 任务类型未知 → 默认类型 | 任务类型不在 4 种已知类型中 | 默认 research_report 映射 |
| 族内全部 DLP 得分为 0 → 族默认 | 所有 DLP 场景标签均不匹配 | 使用族默认锚点 |

### 10.1 硬编码兜底（DLP-nature 12 字段默认值）

当所有质量保持路径均失败时，使用以下硬编码的 DLP-nature 12 字段默认值：

```yaml
# 硬编码兜底 — DLP-nature 12 字段默认值
name: "DLP-nature"
anchor: "Nature 正刊 2024 年版式"
family: "academic-journal"

color_palette:
  primary: "#000000"
  secondary: "#E60012"
  accent: "#0066CC"
  neutral: "#6C757D"
  background: "#FFFFFF"
  text: "#1A1A1A"

typography_scale:
  h1: "24px/1.5rem"
  h2: "18px/1.125rem"
  h3: "16px/1rem"
  h4: "14px/0.875rem"
  body: "10pt/13.33px"
  caption: "8pt/10.67px"
  footnote: "7pt/9.33px"

font_stack:
  western: '"Times New Roman", "STIX Two Text", serif'
  chinese: '"宋体", "SimSun", serif'
  monospace: '"Courier New", monospace'

font_weight_pairing:
  heading: "bold(700)"
  body: "regular(400)"
  emphasis: "italic(400)"

spacing_system:
  base: "4px"
  scale: "4/8/12/16/24/32px"

grid_system:
  columns: "双栏"
  column_width: "8.5cm/栏"
  gutter: "0.5cm"
  margin: "2cm"
  breakpoint: "N/A(印刷媒介)"

radius_shadow:
  radius: "0px"
  shadow: "none"

motion_curve:
  easing: "N/A(印刷媒介)"
  duration: "N/A"

applicable_scenarios:
  - "学术论文"
  - "期刊投稿"
  - "科学研究"
  - "同行评审"
```

---

> **知识来源**: Visual DNA 审美进化项目 / brand-identity-skill 元规则 / Taste-Skill 全局审美总控 / UIR v2.0 全息框架 §1-§8 / design-language-profiles 16 个 DLP
