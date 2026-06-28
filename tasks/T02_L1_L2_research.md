<!-- 作者：阿洋 -->
<!-- output_type_restriction: [research_report, wechat_article, course_material]  # R1-02 分层激活 -->

# T02 — L1 基础事实 + L2 时间演化

## role
你是L1+L2研究底座执行者。你负责收集基础事实（L1）并构建时间演化脉络（L2），为上游结构分析提供坚实的数据地基。你的输出是后续所有分析层的事实锚点。

## context
- **problem**: 用户原始问题
- **output_type**: 成品类型（由 T01 确定）
- **T00_outline_summary**: T00 的研究大纲摘要（含主干问题、子方向、证据等级要求）

## output_schema
> **JSON Schema 规范 (D2.4.1)**: 本节点 output_schema 遵循 `protocols/output-schema-spec.md` 定义的 JSON Schema 统一格式。字段类型遵循 JSON Schema Draft 2020-12 规范。
> **execution_params**: object  # 实际执行参数，必须达到 SKILL.md 规定的最低值（R2-05 防深度缩水）

```json
{
  "L1_factual_base": {
    "factual_checklist": [
      {
        "fact": "string（事实陈述，一句话一个独立事实）",
        "source_category": "L0|L1|L2|L3",
        "verification_status": "verified|partially_verified|unverified"
      }
    ],
    "key_facts_verified": [
      {
        "fact": "string",
        "source_category": "L0|L1|L2|L3",
        "source_detail": "string（具体来源名称、时间、可追溯标识）"
      }
    ],
    "data_gaps_marked": [
      {
        "gap_description": "string（缺什么数据/事实）",
        "reason_unavailable": "string（为何不可获取：未公开/不存在/语言障碍/时间限制等）"
      }
    ],
    "fact_confidence_scores": {
      "fact_key": 0.85
    }
  },
  "new_discoveries": [
    {
      "finding": "≤50字的关键事实性发现",
      "category": "factual",
      "cross_reference_potential": "HIGH|MEDIUM|LOW"
    }
  ],
  "L2_temporal_evolution": {
    "timeline_table": [
      {
        "time": "string（时间节点，精确到年/月/日）",
        "event": "string（事件描述）",
        "impact_direction": "positive|negative|neutral|complex",
        "evidence_source": "string（该时间节点的证据来源）"
      }
    ],
    "phase_divisions": [
      {
        "phase_name": "string（时期名称）",
        "start": "string（起止时间）",
        "end": "string（起止时间）",
        "defining_characteristic": "string（该时期的定义性特征）"
      }
    ],
    "turning_points": [
      {
        "point": "string（转折点名称）",
        "before_state": "string（转折前状态）",
        "after_state": "string（转折后状态）",
        "causal_mechanism": "string（因果机制说明）"
      }
    ]
  },
  "research_base_for_downstream": {
    "total_papers": "int",
    "search_sources": ["semantic_scholar", "openalex", "grobid"],
    "citation_network": {
      "nodes": "int",
      "edges": "int",
      "key_clusters": ["str"]
    },
    "concept_tags": ["str"],
    "institutions": ["str"]
  }
}
```

### 约束规则
- `factual_checklist` 数组长度 ≥ 25
- `timeline_table` 数组长度 ≥ 10，每行四个字段完整
- `phase_divisions` 数组长度 ≥ 2
- `turning_points` 数组长度 ≥ 2
- 事实陈述禁止使用模糊词："可能"、"似乎"、"大概"、"也许"、"据说"、"一般认为"（除非作为被引用方的原文原话，且标注来源）
- `fact_confidence_scores` 中键名为事实的简短标识，值域 0.0-1.0，步长 0.05
- L1 事实条目按置信度降序排列（高置信度在前）
- `new_discoveries` 数组长度 ≥ 2，每条 finding ≤ 50字，category 固定为 "factual"
- `new_discoveries[].cross_reference_potential` 中至少 1 条为 HIGH

### 质量阶梯：事实先于判断
输出必须严格遵循"事实先行"原则：每个事实陈述必须可追溯到可验证的来源（至少标注 `source_category`），在完成事实收集之前不输出任何因果推断或价值判断。

## self_check_before_output
> **量化标准 (D2.4.3)**: 本节点 self_check_before_output 遵循 `protocols/output-schema-spec.md` §4 定义的量化通过判据。self_check_score >= 85 方可输出。

### M10 逼退函数（L1+L2 毕业条件）
> **铁律**：逼退函数是毕业条件，未通过则不得进入下一层 T03。
> - [ ] **M5 trigger coverage ≥ 80%**：T13 产出的深度信号是否已覆盖 ≥ 80% 的触发类型？机制因素是否穷举？
> - [ ] **时间演变链 ≥ 5 节点**：L2 时间演变链是否包含 ≥ 5 个关键节点（每个节点有明确的起始/变化/转折特征）？

输出前必须逐项确认：
- [ ] `factual_checklist` 事实项是否 ≥ 25 条？
- [ ] `timeline_table` 时间节点是否 ≥ 10 行，且每行 `time`、`event`、`impact_direction`、`evidence_source` 四列完整？
- [ ] `phase_divisions` 时期划分是否 ≥ 2 个，每个含起止时间与定义性特征？
- [ ] `turning_points` 转折点是否 ≥ 2 个，每个含 `before_state`、`after_state`、`causal_mechanism`？
- [ ] L2 时间演化是否构建 ≥5 个时间节点的演变链？（每个节点有明确的起始/变化/转折特征）
- [ ] 事实陈述中是否不存在禁止模糊词（逐一检查）？
- [ ] 输出是否严格遵循"事实先于判断"（先有事实，后有推断）？
- [ ] `fact_confidence_scores` 是否覆盖了全部关键事实？
- [ ] `data_gaps_marked` 是否记录了至少1处数据缺口？
- [ ] 事实条目是否按置信度降序排列？
- [ ] `new_discoveries` 是否 ≥ 2 条，每条 finding ≤ 50字？
- [ ] `new_discoveries` 中至少 1 条 `cross_reference_potential` 为 HIGH？
- [ ] `new_discoveries` 的 category 是否均为 "factual"？
- [ ] Semantic Scholar API 是否成功调用
- [ ] OpenAlex API 是否成功调用
- [ ] GROBID PDF 解析是否成功（如适用）
- [ ] 搜索结果是否已去重合并
- [ ] research_base_for_downstream 字段是否完整

### 0A.22 最小事实包验证（强制性基础数据验证）

> **继承自**: 母提示 0A.22（强制性基础数据验证）
> **执行时机**: L1 事实收集完成后、输出前强制验证

#### 验证项

- [ ] **可验证事实 ≥ 5 条**：`factual_checklist` 中 `verification_status = verified` 的事实至少 5 条
- [ ] **数据来源 ≥ 3 个**：独立数据来源至少 3 个（不同域名/机构/数据库视为独立来源）
- [ ] **权威来源 ≥ 1 个**：至少 1 个来源为 L0 或 L1 等级（同行评审论文 / 官方统计 / 权威机构报告）
- [ ] **时效性检查**：数据时效性以 `run_date` 为基准，优先使用 2 年内数据（继承 0A.5 强制性时效检索开关）；偏差超过 2 年的数据点标记为 `[历史数据]`，偏差超过 5 年标记为 `[可能过时]`
- [ ] **不足事实触发补充搜索**：任一验证项未通过 → 触发 T00a 强制性时效检索开关的补充搜索流程，重新检索直至满足最低标准

#### 验证结果写入 NRSF Header

验证完成后，将验证结果写入 NRSF-Full `header/` 字段：

```yaml
nrsf_header_patch:
  fact_package_verification:
    verified_facts_count: int
    data_sources_count: int
    authoritative_sources_count: int
    timeliness_check_passed: true|false
    timeliness_deviation_max_years: float
    supplementary_search_triggered: true|false
    verified_by: "T02"
    inherited_from: "mother_prompt_0A.22"
    timestamp: "{run_date}"
```

#### 逼退条件

未通过最小事实包验证的 T02 输出不得进入 T03（L3 结构分析），必须返回补充搜索直至满足所有最低标准。

## must_not
- 禁止在事实陈述中使用模糊词（"可能"、"似乎"、"大概"、"也许"、"据说"、"一般认为"）
- 禁止输出无来源标注的数据或事实（至少标注 `source_category` 等级）
- 禁止用段落叙述代替结构化 JSON 输出（所有数据必须填入指定字段）
- 禁止先写因果判断再补事实（必须在事实确立后，才能在 L2 的 `turning_points` 中写 `causal_mechanism`）
- 禁止 `phase_divisions` 少于 2 个时期
- 禁止 `timeline_table` 少于 10 行
- 禁止 `factual_checklist` 少于 25 条

## SearXNG 优先搜索策略（Phase E 升级）

### 概述
在 L1 事实收集阶段，优先通过 SearXNG 元搜索聚合引擎发起多引擎聚合搜索。SearXNG 是搜索系统的核心组件，提供跨引擎结果聚合与去重。

### 引擎选择策略
根据 `output_type` 自动选择对应的多引擎组合（详见 `plugins/searxng-adapter.md`）：

| output_type | 引擎策略 | 引擎列表 |
|-------------|----------|----------|
| research_report | 学术研究 | arxiv, google_scholar, pubmed, crossref, semantic_scholar |
| wechat_article | 综合信息 | google, duckduckgo, bing, wikipedia, wikidata |
| course_material | 学术研究 + 综合信息 | 上述两者合并 |

### 查询步骤
1. **构造查询**：将 T00 大纲中的每个子方向分解为 2-3 个搜索关键词
2. **发起 SearXNG 请求**：向 `http://{searxng_host}:{port}/search` 发起搜索，超时 30 秒
3. **结果去重**：按 SearXNG 适配器中的去重规则处理（URL规范化、标题相似度、SimHash）
4. **来源标注**：每项结果按格式 `[来源: {类型} | {名称} | {发布日期} | {URL/出处} | {证据等级}]` 标注

### 穷尽重试策略
1. SearXNG 不可用 → 穷尽重试切换到单引擎直接搜索（Google 优先，使用 Whoogle 轻量代理）
2. 学术引擎不可用 → 穷尽重试切换到通用引擎 + arxiv API 单独调用
3. 全部不可用 → 使用 LLM 内建知识 + 标注 `[INTERNAL_REASONING]`
4. 部分引擎超时 → 跳过超时引擎，合并其余结果

### 与现有搜索的关系
- SearXNG 是 **首选搜索层**，在 wikidata 查询和 arxiv API 调用之前执行
- 若 SearXNG 成功返回学术来源结果，可减少后续 arxiv API 调用次数（仅检索 SearXNG 未覆盖的论文）
- 若 SearXNG 返回了 Wikidata 可验证的实体属性，wikidata 查询范围缩小为仅验证 SearXNG 未覆盖的高优先级事实
- **自检清单新增项**：SearXNG 是否成功调用？若回退，回退原因是否已记录？

## Meilisearch 历史知识检索（Phase E 升级）

### 概述
在开始 L1 事实收集之前，先通过 Meilisearch 检索过往研究产出，复用历史研究中已收集的事实、方法和证据链，避免重复劳动。

### 检索时机
- 在 SearXNG 搜索和 wikidata 查询 **之前** 执行（减少外部请求量）
- 在 T00 大纲解析完成后立即执行

### 检索步骤
1. **相似研究查询**（T01 风格）：查询当前问题是否有历史相似研究
   ```
   GET /indexes/research_index/search
   { "q": "{用户问题}", "limit": 5 }
   ```
2. **主题检索**（T02 风格）：按研究子课题检索历史知识
   ```
   GET /indexes/research_index/search
   { "q": "{研究子课题}", "filter": "output_type = research_report", "limit": 10 }
   ```
3. **结果处理**：
   - 若检索到相似度 > 0.7 的历史研究 → 提取 `key_findings`、`methodology`、`evidence_sources` 作为 L1 起点
   - 标注来源 `[来源: meilisearch | {research_id} | {topic} | {timestamp}]`
   - 对历史事实进行时效性检查（超过 6 个月的研究需标注 `[VERIFY_TIMELINESS]`）

### 穷尽重试策略
- Meilisearch 不可用 → 穷尽重试，跳过历史检索，从零开始收集 L1 事实
- 无匹配结果 → 正常执行 SearXNG + wikidata + arxiv 流程
- 历史数据过时 → 保留作为参考基线，但必须用新鲜搜索验证

### 自检清单新增项
- [ ] Meilisearch 历史知识检索是否已执行？
- [ ] 若命中历史研究，是否已标注时效性检查结果？
- [ ] 历史事实是否已纳入 `factual_checklist` 并标注来源为 `meilisearch:{research_id}`？

## wikidata_可选查询步骤

### 概述
在 L1 事实收集阶段，可选择性调用 Wikidata SPARQL 查询以验证关键事实（量化指标、实体属性、类归属）的客观可靠性。此步骤为可选增强环节——查询成功可提升事实置信度，查询失败不阻塞节点执行的正常推进。

### 调用条件
- 待验证事实涉及可映射至 Wikidata 实体的概念（如城市、国家、人物、机构、物种、化合物等）
- 待验证属性属于 Wikidata 可查询的类型（人口 P1082、面积 P2046、成立时间 P571、地理坐标 P625 等）
- KG 查询次数由质量驱动，不设硬性上限，穷尽查询直至信息充分

### 查询步骤
1. **实体发现**：将事实中涉及的概念映射至 Wikidata Q-ID（通过标签搜索或 LLM 已有知识）
2. **构造查询**：参考 `knowledge/knowledge-graph-integration.md` 第 2.2-2.4 节，构造对应的 SPARQL 查询模板（实体属性查询 / 关系查询 / 类查询）
3. **发起查询**：向 `https://query.wikidata.org/sparql` 发送 SPARQL 查询请求，超时 15 秒
4. **结果解析**：按 `knowledge/knowledge-graph-integration.md` 第 2.5 节解析返回的 JSON bindings
5. **事实对比**：将查询结果与待验证事实逐条对比：
   - 匹配成功 → 标注 `source_category=L0, source=wikidata:{qid}`
   - 无匹配/KG 不可用 → 穷尽重试，使用 LLM 自有知识

### 穷尽重试策略
Wikidata 不可用时（网络超时、实体未找到、查询无结果），穷尽重试，使用 LLM 自有知识：
- 标注 `source_category=L0, source=llm_knowledge, retry_reason={原因}`
- 在 `fact_confidence_scores` 中对重试事实降低 0.1 置信度（最低不低于 0.5）

### 查询质量要求
- 每个关键事实的 Wikidata 查询结果记录于 `key_facts_verified[*].source_detail`，格式为 `wikidata:{qid}::{property_label}::{value}`
- 若某关键事实无法在 Wikidata 中验证，在 `data_gaps_marked` 中记录为独立数据缺口

### 集成规范
查询模板、结果解析规则及其他细节见 `knowledge/knowledge-graph-integration.md` 第 2 节。

## arxiv 学术论文检索（条件触发）

### 触发条件
`object_type ∈ {科学, 学术, 技术, AI, 医学, 经济学}`

### API 调用格式
```
https://export.arxiv.org/api/query?search_query=all:{关键词1}+AND+all:{关键词2}&max_results=5&sortBy=relevance
```

### 参数说明
- `search_query`：URL 编码的搜索关键词，多个关键词用 `+AND+all:` 连接
- `max_results`：返回数量由质量驱动，不设上限（穷尽搜索直至信息充分）
- `sortBy`：按相关度排序

### 响应解析
返回 XML 格式，提取以下字段：
- `title`：论文标题
- `summary`：论文摘要
- `published`：发布时间
- `id`：arxiv ID（可从 `https://arxiv.org/abs/{id}` 访问）

### 纳入研究
- 将最相关的 2-3 篇论文的 abstract 纳入 L1 基础事实层
- 将论文 URL（`https://arxiv.org/abs/{id}`）列入 T05 L6 证据账本
- 证据等级标注为 **A**（同行评审论文/官方统计）

### 非学术领域回退
若 `object_type` 不匹配触发条件 → 跳过 arxiv 查询，使用常规 Web Search 作为数据来源

### 学术搜索 API 升级

v3.0 升级后，T02 的学术搜索从单一来源扩展为多源聚合：

1. **Semantic Scholar API** (主要来源)
   - 端点: https://api.semanticscholar.org/graph/v1
   - 功能: 论文搜索、引用图谱、作者画像、TLDR 摘要
   - 速率限制: 100 requests/5min (免费)
   - 优势: 引用关系完整、有 AI 生成 TLDR

2. **OpenAlex API** (补充来源)
   - 端点: https://api.openalex.org
   - 功能: 作品搜索、机构分析、概念标签、引用追踪
   - 速率限制: 无明确限制（礼貌池）
   - 优势: 开放数据、元数据丰富、概念标签体系

3. **GROBID** (PDF 解析)
   - 本地部署: docker-compose.yml 中的 grobid 服务
   - 功能: PDF 全文解析、结构化提取
   - 依赖: Docker 环境

搜索策略：
- 先用 Semantic Scholar 搜索核心论文
- 用 OpenAlex 补充机构分析和概念扩展
- 对关键 PDF 使用 GROBID 解析全文
- 合并去重后按相关性排序

---

## LightRAG 索引构建（T02 完成后）

> **能力卡**: LightRAG — 详见 `plugins/lightrag-adapter.md` 和 `knowledge/external-capabilities/TC-011-LightRAG.md`

T02 研究底座产出完成后，必须执行 LightRAG 索引构建子步骤，将检索文献构建为知识图谱索引，供后续 T08-T13 认知流水线的图检索增强使用。

### 索引构建子步骤

1. **实体抽取**：从检索文献（L1 基础事实 + L2 时间演化）中抽取实体
   - 输入：`factual_checklist`、`timeline_table`、`key_facts_verified`
   - 方法：LightRAG 内置实体抽取（基于 LLM 的命名实体识别）
   - 输出：实体列表（人物、机构、事件、概念、地点等）

2. **关系抽取**：抽取实体间关系
   - 输入：实体列表 + 原始文献文本
   - 方法：LightRAG 内置关系抽取（基于 LLM 的关系三元组抽取）
   - 输出：关系三元组列表（实体A — 关系 — 实体B）

3. **社区检测**：使用社区检测算法聚类实体
   - 输入：实体关系图
   - 方法：LightRAG 内置社区检测（基于图聚类的社区发现算法）
   - 输出：实体社区列表（每个社区包含相关实体和社区摘要）

4. **向量索引**：构建向量索引支持语义检索
   - 输入：实体、关系、社区摘要的嵌入向量
   - 方法：LightRAG 内置向量索引（基于嵌入模型的语义索引）
   - 输出：向量索引文件（存储于 `./lightrag_index/{research_id}/`）

### 索引构建流程

```yaml
lightrag_index_build:
  trigger: "T02 研究底座产出完成（L1-L2 全部层级）"
  step_1_entity_extraction:
    method: "从检索文献中抽取实体"
    sources: ["factual_checklist", "timeline_table", "key_facts_verified"]
    output: "实体列表"
  step_2_relation_extraction:
    method: "抽取实体间关系"
    sources: ["实体列表", "原始文献文本"]
    output: "关系三元组列表"
  step_3_community_detection:
    method: "使用社区检测算法聚类实体"
    sources: ["实体关系图"]
    output: "实体社区列表 + 社区摘要"
  step_4_vector_index:
    method: "构建向量索引支持语义检索"
    sources: ["实体/关系/社区摘要的嵌入向量"]
    output: "向量索引文件（./lightrag_index/{research_id}/）"
  step_5_validation:
    method: "执行测试查询验证索引质量"
    command: "rag.query('研究问题', param=QueryParam(mode='hybrid'))"
    output: "索引验证结果"
```

### 穷尽重试策略

- LightRAG 不可用 → 穷尽重试，跳过索引构建，T08-T13 回退到备用 KG 源（详见 `plugins/lightrag-adapter.md` 备用源层级）
- 索引构建部分失败 → 保留已构建部分，标注 `[PARTIAL_INDEX]`
- 嵌入模型不可用 → 使用本地备选嵌入模型，标注 `[FALLBACK_EMBEDDING]`

### 自检清单新增项

- [ ] LightRAG 索引构建是否已执行？
- [ ] 实体抽取是否覆盖了 L1 基础事实中的关键实体？
- [ ] 关系抽取是否识别了实体间的主要关系？
- [ ] 社区检测是否产出了有意义的实体聚类？
- [ ] 向量索引是否已保存至 `./lightrag_index/{research_id}/`？
- [ ] 索引验证查询是否成功返回结果？

---

## PaperQA2 文献检索自动化（R9-03）

> **能力卡片引用**: `knowledge/external-capabilities/PaperQA2.md` — 学术论文 RAG 检索与综述自动生成
> **关联卡片**: `knowledge/external-capabilities/TC-031-PaperQA2.md` — 基础问答能力卡

本节定义 PaperQA2 RAG 引擎在 T02 文献检索阶段的集成流程，作为 SearXNG + arXiv + Semantic Scholar 检索的增强层。PaperQA2 提供论文全文向量索引、引用网络遍历与综述自动生成能力，提升文献检索的深度与覆盖度。

### 子步骤 1：PaperQA2 检索（paperqa_retrieval）

使用 PaperQA2 RAG 引擎对论文全文进行向量索引，从种子论文出发检索相关文献：

1. **触发条件**：`object_type ∈ {科学, 学术, 技术, AI, 医学, 经济学}` 且 PaperQA2 服务可用
2. **检索流程**：
   - 从 T00 大纲或用户指定获取种子论文（DOI/arXiv ID/文件路径）
   - 调用 PaperQA2 RAG 引擎执行检索
   - 获取相关论文段落和引用
3. **检索输出注入**：将 PaperQA2 检索结果注入 `L1_factual_base.factual_checklist` 和 `research_base_for_downstream`
4. **与现有检索的关系**：
   - PaperQA2 优先用于学术论文全文检索（深度优先）
   - SearXNG 用于非学术来源（广度优先）
   - arXiv/Semantic Scholar API 用于元数据检索（PaperQA2 不可用时回退）
5. **穷尽重试策略**（继承 PaperQA2 能力卡）：PaperQA2 不可用 → 回退到 SearXNG 学术引擎策略 + 人工筛选

### 子步骤 2：PaperQA2 RAG 引擎全文向量索引流程

定义 PaperQA2 RAG 引擎对论文全文进行向量索引的流程：

1. **收集种子论文**（用户指定或关键词检索）：
   - 优先来源：用户在 T00 大纲中指定的种子论文
   - 次要来源：通过 arXiv API / Semantic Scholar API 关键词检索获取的种子论文
   - 种子论文数量：≥ 3 篇（质量驱动，不设上限）
2. **PaperQA2 对论文全文进行向量索引**：
   - PDF 解析：通过 GROBID 或 PaperQA2 内置解析器提取论文全文
   - 分段：按段落/章节切分论文文本
   - 嵌入：使用嵌入模型（默认 OpenAI text-embedding-3-small）生成段落向量
   - 索引：构建向量索引，支持相似度检索
3. **支持全文检索和语义检索**：
   - 全文检索：基于关键词的精确匹配
   - 语义检索：基于向量相似度的语义匹配
   - 混合检索：全文检索 + 语义检索结果融合排序
4. **索引质量要求**：
   - 索引论文数量 ≥ 种子论文数 × 3（含引用网络遍历获取的论文）
   - 每篇论文的段落索引完整（不遗漏关键章节）

### 子步骤 3：PaperQA2 引用网络遍历

定义 PaperQA2 引用网络遍历能力：

1. **遍历起点**：从种子论文出发
2. **遍历方向**：
   - **references（引用）**：追踪种子论文引用的参考文献
   - **cited-by（被引）**：追踪引用种子论文的后续研究
3. **多跳引用遍历**（最多 3 跳）：
   - 第 1 跳：种子论文的直接 references + cited-by
   - 第 2 跳：第 1 跳论文的 references + cited-by
   - 第 3 跳：第 2 跳论文的 references + cited-by
   - 默认遍历深度：1 跳（可配置至 3 跳）
4. **遍历输出**：注入 `research_base_for_downstream.citation_network`
   ```yaml
   citation_network:
     nodes: integer  # 引用网络节点数（论文数）
     edges: integer  # 引用关系边数
     key_clusters: [string]  # 关键论文聚类
     traversal_depth: integer  # 实际遍历深度（1-3）
   ```
5. **遍历去重**：引用网络中的论文按 DOI/arXiv ID 去重，避免重复索引

### 子步骤 4：PaperQA2 检索日志写入 NRSF

> **NRSF 日志格式**：PaperQA2 检索日志写入 NRSF-Full §T02

每次 PaperQA2 检索按以下格式写入 NRSF：

```
§paperqa_log:{timestamp}:
  query: "..."
  papers_retrieved: [...]
  citation_network_depth: N
  review_summary: "..."
```

字段说明：
- `timestamp`：检索时间戳（ISO 8601 格式）
- `query`：PaperQA2 检索查询
- `papers_retrieved`：检索到的论文列表（含 paper_id、title、relevance_score）
- `citation_network_depth`：引用网络遍历深度（1-3）
- `review_summary`：综述摘要（若 generate_review=true，否则为空字符串）

### 自检清单新增项
- [ ] PaperQA2 检索是否已执行（若 object_type 匹配触发条件）？
- [ ] 种子论文是否已收集（≥ 3 篇）？
- [ ] PaperQA2 全文向量索引是否成功构建？
- [ ] 引用网络遍历是否执行（默认 1 跳，可配置至 3 跳）？
- [ ] PaperQA2 检索日志是否按 `§paperqa_log:{timestamp}` 格式写入 NRSF？
- [ ] 若 PaperQA2 不可用，是否回退到 SearXNG 学术引擎策略 + 人工筛选？

---

## knowledge_refs
- `knowledge/research-methods.md` — 研究方法论（事实收集标准、时间序列分析方法、时期划分原则）
- `knowledge/evidence-standards.md` — 证据等级标准（L0-L3 定义与判定规则）
- `knowledge/source-verification.md` — 来源验证方法论
- `knowledge/knowledge-graph-integration.md` — 知识图谱集成规范（Wikidata SPARQL 查询/ConceptNet 查询）

## NRSF 追加指令

T02 完成后，将散文式研究笔记追加到 NRSF-Full §T02：
- 每段 150-300 字，段落级引用
- 包含搜索策略、关键词设计、来源发现
- 遵循 nrsf-protocol.md 的散文式笔记格式

## 双阶段输出格式

### 阶段 A：结构化分析

原有的 output_schema 格式输出，用于 Supervisor 检查。

### 阶段 B：散文式研究笔记

追加到 NRSF-Full §T02 的散文式笔记，供下游消费。

## 外部能力卡片引用

- **TC-074 WebWeaver**: 可作为研究助手加载，自动生成研究大纲并迭代收集语义和逻辑层信息。详见 `knowledge/external-capabilities/TC-074-WebWeaver.md`

---

## M5: 强制检索触发器（9 类）

```yaml
m5_force_retrieval_triggers:
  description: "当研究过程中出现以下9类信号时，强制触发补充检索，而非仅依赖LLM内建知识"
  evidence_levels:
    A: "同行评审论文/官方统计"
    B: "权威媒体/机构报告"
    C: "一般来源/间接证据"
    D: "推测/个人观点"
  iron_law: "不得使用'据悉/据研究/有研究显示/据报道'而不给具体来源"
  trigger_classes:
    T1_data_gap:  # 数据缺口触发器
      signal: "关键事实缺少具体数值、时间、来源"
      action: "强制发起 SearXNG/Wikidata 检索，填补数据缺口"
      severity: "CRITICAL"
    T2_contradiction:  # 矛盾触发器
      signal: "同一事实在不同来源中出现矛盾版本"
      action: "强制多源交叉验证，至少3个独立来源确认"
      severity: "CRITICAL"
    T3_temporal_sensitivity:  # 时效性触发器
      signal: "事实涉及时间敏感信息（如最新政策、价格、事件），且最后更新时间 > 6个月"
      action: "强制重新检索，更新时间戳"
      severity: "HIGH"
    T4_terminology_ambiguity:  # 术语歧义触发器
      signal: "关键术语在不同领域/语境中有不同含义"
      action: "强制检索术语定义，标注领域上下文"
      severity: "HIGH"
    T5_consensus_absence:  # 共识缺失触发器
      signal: "某领域/话题不存在公认的权威结论"
      action: "强制检索各学派观点，标注'学界存在分歧'"
      severity: "HIGH"
    T6_emotional_loading:  # 情感负载触发器
      signal: "话题涉及高度情感化/政治化内容，客观事实可能被立场干扰"
      action: "强制检索去政治化的原始数据/一手来源"
      severity: "MEDIUM"
    T7_quantitative_claim:  # 量化声明触发器
      signal: "文本中出现精确数值声明（如增长率、占比、排名）"
      action: "强制检索数据出处，标注统计口径和采集时间"
      severity: "CRITICAL"
    T8_emerging_topic:  # 新兴话题触发器
      signal: "话题为近3个月内新出现的事件/技术/概念"
      action: "强制检索最新报道/论文，标注'新兴领域，结论可能变化'"
      severity: "MEDIUM"
    T9_geographic_specificity:  # 地域特殊性触发器
      signal: "事实涉及特定地区/文化，可能存在地域差异"
      action: "强制检索本地来源，标注地域适用范围"
      severity: "MEDIUM"
  coverage_check: "每个研究周期结束后，检查9类触发器的覆盖情况，覆盖率 >= 80% (>= 7/9) 方可通过"
  self_check: "M5 trigger coverage >= 80%？若未达到，返回补充检索"
```