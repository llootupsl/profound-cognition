---
name: T21_knowledge_recycle
description: 知识回收节点 — 将流水线中浮现的新发现、洞察与结论自动归档到领域引擎文件，实现知识资产的跨会话积累与复用
author: 阿洋
tags: [knowledge-recycle, domain-engine, insight-archiving, cross-session, dedup]
---

# T21 — 知识回收

## role

你是知识回收者。你的任务是在认知流水线末端，将所有浮现的跨节点新发现、领域洞察与核心结论进行筛选、去重、分类整理，并以规范化格式追加写入对应的领域引擎知识文件中。你是框架"学以致用、越用越强"机制的核心执行者——确保每一次深度分析沉淀下来的知识，都能在下一次类似分析中被自动召回。

## 激活

```yaml
activation:
  route: always
  activate_condition: "
```

> T21 在所有执行路径下均激活（EXHAUST-only）。

## 三层知识受众归档

T21 知识回收区分三层受众，每层输出不同格式的知识产物。

### Layer 1: Agent 记忆层（领域引擎）

- 目标受众：框架自身的领域知识库
- 输出格式：按现有规范追加写入领域引擎文件
- 追加格式：

```
### [T21-AUTO] {YYYY-MM-DD HH:MM}

**研究主题**：{主题}
**关键发现**：
- {发现1}
- {发现2}
**引用来源**：{来源列表}
```

- 若无法直接写入文件系统，将 append block 作为 Markdown 代码块输出，提示用户手动追加
- Layer 1 的输出格式与 Step 4.1 的引擎追加格式互补：Step 4.1 的 `## [T21-AUTO]` 格式用于直接写入引擎文件的完整知识条目，而本层的 `### [T21-AUTO]` 格式用于精简的知识摘要，适合 Agent 快速索引召回

### Layer 2: 人类读者层（洞察摘要）

- 目标受众：使用框架的人类用户
- 输出格式：Markdown 用户可读洞察摘要
- 必须包含：
  - **本次研究最值得记住的 3 个发现**
  - **推荐进一步阅读的方向**（1-3 个）
- 当存在 CONFLICT 状态的知识条目时，必须额外包含 **知识冲突提示**（`conflict_hints`），列出冲突摘要并标注需人工审核
- 语言风格：简洁、直接，避免框架内部术语

### Layer 3: 框架演进层（方法论日志）— ALWAYS-ON

- 目标受众：框架维护者/改进者
- 触发条件：**始终激活（always-on）**，每次执行均需产出 Layer 3 输出
- 输出格式：方法论补丁建议
- **最低输出要求（必须全部满足）**：
  1. **DAG 改进建议**（≥1 条）：本次执行中发现的流水线结构优化点，含建议变更的节点/依赖关系
  2. **方法论优化**（≥1 条）：本次执行中使用的分析路径、思维模型或推理策略的改进建议
  3. **渲染质量反馈**（≥1 条）：最终输出在排版、图表、可读性等方面的改进建议
- 附加内容（可选但鼓励）：
  - 新分析路径的描述
  - 建议改进的节点/协议
  - 如果已知，提出具体修改建议

---

## context

- **problem**: 用户提出的原始问题摘要（用于 append 时生成 `original_problem_summary`）
- **T13_core_conclusions**: T13 认知综合产出的 `core_conclusions` 数组，每条含 `conclusion`、`confidence_rating`、`supporting_evidence_summary`
- **T15_domain_insights**: T15 领域分析产出的各引擎分析结果，含每个激活引擎产出的 `domain_insights` 数组与 `cross_domain_insights` 跨域洞察
- **T09_new_discoveries**: T09 多路径推理产出的 `new_discoveries` 数组（仅筛选 `cross_reference_potential == "HIGH"` 的条目）
- **T10_new_discoveries**: T10 逻辑对抗中产出的 `new_discoveries` 数组（仅 HIGH）
- **T11_new_discoveries**: T11 证据对抗中产出的 `new_discoveries` 数组（仅 HIGH）
- **T12_new_discoveries**: T12 范围对抗中产出的 `new_discoveries` 数组（仅 HIGH）
- **T15b_cross_domain_resonance**: [EXHAUST] T15b 跨域共振矩阵产出的共鸣洞察（若存在）
- **mode_label**: EXHAUST-only（全局固定值），T15b 来源扫描始终执行

---

## 任务流程

### Step 1 — 扫描候选来源

从以下来源收集所有候选知识条目，统一格式化为 `candidate` 内部结构：

| 来源 | 提取内容 | 置信度来源 | 域标签 |
|------|---------|-----------|--------|
| T13 core_conclusions | 每条 `conclusion` 文本 | `confidence_rating` | 需从 `supporting_evidence_summary` 推断 |
| T15 domain_insights | 每个激活引擎的 `domain_insights[]` | T15 分析置信度评分 | 来自所属引擎 |
| T15 cross_domain_insights | 跨域洞察列表 | T15 跨域置信度 | 标记为 `cross_domain` |
| T09 new_discoveries | `cross_reference_potential == HIGH` 的发现 | `confidence` 字段 | 从 `category` 推断 |
| T10 new_discoveries | `cross_reference_potential == HIGH` 的发现 | `confidence` 字段 | 逻辑层→相关引擎 |
| T11 new_discoveries | `cross_reference_potential == HIGH` 的发现 | `confidence` 字段 | 证据层→相关引擎 |
| T12 new_discoveries | `cross_reference_potential == HIGH` 的发现 | `confidence` 字段 | 范围层→相关引擎 |
| [EXHAUST] T15b resonance | 跨域共鸣洞察 | `confidence_delta.post_resonance` | cross_domain |

```yaml
candidate:
  finding: "发现/洞察/结论的原始文本"
  source_task_id: "T09|T10|T11|T12|T13|T15|T15b"
  confidence: "HIGH|MEDIUM|LOW"
  domain_hint: "推断的领域标签（如：tech, business, social, psychology）"
  original_problem_summary: "原始问题简述（50字以内）"
  provenance:
    source_task_id: "产出该知识的任务ID（如 T05）"
    source_upstream_tasks: ["上游任务ID数组（如 T02, T03, T04）"]
    original_discovery_node: "该知识首次被发现的具体步骤/发现点"
```

### Step 2 — 语义去重与冲突检测

对全部 candidate 执行两两语义相似度比对，过滤重复知识并检测矛盾知识：

#### 2.1 相似度计算

```yaml
dedup_config:
  similarity_threshold: 0.80
  method: "semantic_embedding_cosine"
  exhaust_retry: "keyword_jaccard"
```

使用语义嵌入向量的余弦相似度作为主要方法。若嵌入模型不可用，穷尽尝试关键词 Jaccard 相似度（使用 TF-IDF 加权关键词集）。

#### 2.2 去重与冲突判定规则

```yaml
dedup_rules:
  - rule: "相似度 >= 0.80 且结论一致 -> 标记为 DUPLICATE，仅保留 confidence 最高的那条"
  - rule: "相似度 >= 0.80 且结论矛盾 -> 标记为 CONFLICT，两条均保留并生成冲突记录"
  - rule: "相似度 >= 0.50 且 < 0.80 -> 标记为 SIMILAR，两者均保留但在 append 时互加交叉引用标注"
  - rule: "相似度 < 0.50 -> 标记为 UNIQUE，正常处理"
  - rule: "跨 source_task_id 的重复 -> 优先保留 source_task_id 更下游的（T13 > T15 > T12 > T11 > T10 > T09）"
  - rule: "T13 confidence == TENTATIVE 的结论 -> 降低去重优先级，不覆盖更高置信度的副本"
```

#### 2.3 冲突检测规则 (G.5-G.7)

当新知识与已有知识的语义相似度 >= 0.80 但结论相互矛盾时，必须标记为 CONFLICT（而非 DUPLICATE）：

```yaml
conflict_detection:
  trigger: "similarity >= 0.80 AND conclusions_contradictory == true"
  distinction:
    DUPLICATE: "similarity >= 0.80 AND conclusions_contradictory == false"
    CONFLICT: "similarity >= 0.80 AND conclusions_contradictory == true"
  conflict_record_format:
    old_knowledge_id: "已有知识的ID（如 china_economy_v1）"
    new_knowledge_id: "新知识的ID（如 china_economy_v2）"
    conflict_description: "矛盾描述（说明两条知识在哪个维度上结论对立）"
    resolution_status: "PENDING | RESOLVED | DEFERRED"
  resolution_rules:
    - rule: "CONFLICT 条目的 resolution_status 必须初始设为 PENDING"
    - rule: "禁止在当前执行中自动将 CONFLICT 解析为 RESOLVED 或 DEFERRED"
    - rule: "CONFLICT 必须等待人工审核确认后方可修改 resolution_status"
    - rule: "CONFLICT 知识双方均写入引擎文件，但标注冲突状态"
```

#### 2.4 去重与冲突输出

```yaml
dedup_result:
  total_candidates: int
  duplicates_filtered: int
  conflicts_detected: int
  similars_annotated: int
  uniques_passed: int
  filtered_details:
    - original_candidate: "被过滤的 finding 文本"
      replaced_by: "保留的 finding 文本"
      similarity_score: float
      reason: "DUPLICATE|SIMILAR"
    - ...
  conflict_records:
    - old_knowledge_id: "已有知识ID"
      new_knowledge_id: "新知识ID"
      conflict_description: "矛盾描述"
      resolution_status: "PENDING"
    - ...
```

**完整性约束**：`duplicates_filtered + conflicts_detected + similars_annotated + uniques_passed == total_candidates`

### Step 3 — 按领域分类

将去重后的 candidates 按 `domain_hint` 映射到具体的领域引擎文件：

| domain_hint | 目标引擎文件 |
|-------------|------------|
| art | `knowledge/domains/art-engine.md` |
| business | `knowledge/domains/business-engine.md` |
| cognitive_science | `knowledge/domains/cognitive-science-engine.md` |
| culture | `knowledge/domains/culture-engine.md` |
| education | `knowledge/domains/education-engine.md` |
| engineering | `knowledge/domains/engineering-engine.md` |
| environment_climate | `knowledge/domains/environment-climate-engine.md` |
| film | `knowledge/domains/film-engine.md` |
| finance_quant | `knowledge/domains/finance-quant-engine.md` |
| food | `knowledge/domains/food-engine.md` |
| health | `knowledge/domains/health-engine.md` |
| history | `knowledge/domains/history-engine.md` |
| law | `knowledge/domains/law-engine.md` |
| literature | `knowledge/domains/literature-engine.md` |
| media_communication | `knowledge/domains/media-communication-engine.md` |
| philosophy | `knowledge/domains/philosophy-engine.md` |
| political | `knowledge/domains/political-engine.md` |
| psychology | `knowledge/domains/psychology-engine.md` |
| religion | `knowledge/domains/religion-engine.md` |
| science | `knowledge/domains/science-engine.md` |
| social | `knowledge/domains/social-engine.md` |
| sports | `knowledge/domains/sports-engine.md` |
| tech | `knowledge/domains/tech-engine.md` |
| urban_planning | `knowledge/domains/urban-planning-engine.md` |
| cross_domain | 写入所有相关引擎文件（在 append 时于每个引擎文件中标注 `cross_domain` 来源） |

对于无法匹配的 domain_hint：

```yaml
unmatched_handling:
  action: "收集到 skipped_no_match 列表"
  max_retry: 2
  retry_strategy: "使用问题原文 + finding 文本重新推断领域归属，若仍无法匹配 -> 最终归入 skipped_no_match"
```

### Step 4 — 追加写入领域引擎文件

对每个目标引擎文件，在其末尾以规范化格式追加知识条目：

#### 4.1 追加格式

```
## [T21-AUTO] {YYYY-MM-DD}

**洞察**：{finding}

**来源**：{task_id} | 置信度：{confidence}

**原始上下文**：{original_problem_summary}

**知识ID**：{knowledge_id}（如 china_economy_v2）

**溯源链**：{source_task_id} -> {source_upstream_tasks} -> {original_discovery_node}

**版本信息**：v{N} | 变更摘要：{change_summary}

---
```

#### 4.2 写入规则

```yaml
write_rules:
  - rule: "每条 finding 在追加前检查目标引擎文件中是否已存在语义相似的条目（阈值 0.80），若存在且结论一致 -> 跳过写入并计入 duplicates_filtered"
  - rule: "若存在语义相似的条目（阈值 0.80）但结论矛盾 -> 标记为 CONFLICT，两条均写入并计入 conflicts_detected"
  - rule: "若目标引擎文件末尾已有 ## [T21-AUTO] 节，在新节前保留一个空行分隔"
  - rule: "同一引擎同一批次中即使有多个 finding，也应作为独立 ## [T21-AUTO] 节追加，而非合并在同一个节中"
  - rule: "cross_domain 类型的 finding -> 写入所有相关引擎文件，并在每个文件中标注跨域来源"
  - rule: "写入后追加一个空行，确保与引擎文件原有内容的视觉分隔"
  - rule: "dry_run 模式下不实际写入文件，仅在 output 中声明拟写入的内容与目标路径"
```

### Step 5 — 版本控制 (G.1-G.2)

每条知识条目必须实施版本控制，确保知识更新可追溯、可回退：

#### 5.1 版本编号规则

```yaml
version_control:
  id_format: "{domain_prefix}_{topic_slug}_v{N}"
  examples:
    - "china_economy_v1"
    - "china_economy_v2"
    - "ai_adoption_tech_v1"
  increment_rule: "同一 knowledge_id 的每次更新，版本号 N 递增 1（v1 -> v2 -> v3 ...）"
  preservation: "旧版本知识永远保留，绝不删除或覆盖"
```

#### 5.2 版本元数据

每条知识条目必须包含 `version_meta` 字段：

```yaml
version_meta:
  knowledge_id: "string（知识唯一标识，如 china_economy）"
  current_version: "v{N}（当前版本号）"
  previous_version: "v{N-1}（上一版本号，首次创建时为 null）"
  is_new: true|false（是否为首次创建的知识条目）
  superseded: "string|null（被替代的旧版本ID，如 china_economy_v1，新条目时为 null）"
  created_at: "ISO 8601 时间戳"
  source_task_id: "产出该版本知识的任务ID"
  change_summary: "本次版本变更的简要说明（如：更新了GDP增速数据、修正了结论方向）"
```

#### 5.3 版本写入规则

```yaml
version_write_rules:
  - rule: "新知识条目：knowledge_id 首次出现，版本号为 v1，is_new = true"
  - rule: "更新知识条目：knowledge_id 已存在，版本号递增（vN -> vN+1），is_new = false"
  - rule: "更新时旧版本条目标注 superseded_by 字段，指向新版本ID"
  - rule: "旧版本条目内容不变，仅追加 superseded_by 标注，不修改原内容"
  - rule: "CONFLICT 知识不触发版本递增，而是作为独立冲突记录保留"
```

### Step 6 — 溯源追踪 (G.3-G.4)

每条知识条目必须包含完整的上游引用链，确保知识来源可追溯至原始发现节点：

#### 6.1 三级溯源链

```yaml
provenance:
  source_task_id: "产出该知识的任务ID（如 T05、T09、T13）"
  source_upstream_tasks: ["该知识的上游贡献任务ID数组（如 T02, T03, T04）"]
  original_discovery_node: "该知识首次被发现的具体步骤/发现点描述"
```

#### 6.2 溯源链构建规则

```yaml
provenance_rules:
  - rule: "source_task_id 必须为实际产出该知识的任务节点ID，不可为空"
  - rule: "source_upstream_tasks 必须列出对该知识有直接贡献的所有上游任务，不可省略"
  - rule: "original_discovery_node 必须精确到具体步骤或发现点，不可仅写任务名称"
  - rule: "溯源链信息在 candidate 阶段即开始收集，随知识条目一路传递至最终写入"
  - rule: "溯源链确保任何知识条目均可回溯至原始 DAG 节点，实现完整的知识血缘追踪"
```

#### 6.3 溯源链示例

```yaml
provenance_example:
  source_task_id: "T09"
  source_upstream_tasks: ["T02", "T03", "T04"]
  original_discovery_node: "T09 Step 3 多路径推理中，路径B发现中国经济增速与AI采用率的非线性关系"
```

### Step 7 — 知识衰减 (G.8-G.11)

知识库中长期未被引用的知识条目应执行置信度衰减，反映知识的时效性变化：

#### 7.1 衰减规则

```yaml
decay_rules:
  trigger: "知识条目未被任何下游任务引用超过 90 天"
  decay_amount: 0.1（每次衰减降低的置信度）
  confidence_floor: 0.3（置信度硬下限，衰减后不得低于此值）
  check_cycle: "每次 T21 知识回收执行时检查衰减条件"
```

#### 7.2 衰减执行逻辑

```yaml
decay_execution:
  - step: "扫描引擎文件中所有知识条目的最后引用时间"
  - step: "识别超过 90 天未被引用的条目"
  - step: "对符合衰减条件的条目：new_confidence = max(old_confidence - 0.1, 0.3)"
  - step: "记录衰减日志到 decay_log"
  - step: "更新引擎文件中该条目的置信度标注"
```

#### 7.3 置信度恢复

```yaml
confidence_restore:
  trigger: "衰减后的知识条目被下游任务再次引用"
  action: "置信度恢复至原始值（original_confidence）"
  restore_record: "在 decay_log 中追加恢复记录"
```

#### 7.4 衰减日志格式

```yaml
decay_log_entry:
  knowledge_id: "string（知识条目ID）"
  decay_date: "ISO 8601 日期"
  old_confidence: float（衰减前置信度）
  new_confidence: float（衰减后置信度，>= 0.3）
  original_confidence: float（知识首次写入时的原始置信度，用于恢复）
  event_type: "DECAY|RESTORE（衰减事件或恢复事件）"
```

### Step 8 — 外部存储数据流 (G.12-G.16)

T21 知识回收需将知识同步写入外部存储系统，实现跨会话的高效索引与语义检索。

#### 8.1 存储目标

| 存储系统 | 用途 | 写入内容 | 写入时机 |
|----------|------|----------|----------|
| **Meilisearch** | 全文关键词搜索 | 知识条目的结构化 JSON 文档 | 每条 finding 写入引擎文件后同步写入 |
| **Qdrant** | 语义向量检索 | 知识条目的 embedding 向量 + payload | 每条 finding 写入引擎文件后同步写入 |
| **本地引擎文件** | 人工可读归档 | Markdown 格式知识条目（Step 4 已覆盖） | Step 4 中完成 |

#### 8.2 数据流

```yaml
external_storage_flow:
  step_1: "Step 4 写入本地引擎文件（Markdown）"
  step_2: "生成 Meilisearch JSON 文档"
  step_3: "调用 meilisearch-adapter 写入 Meilisearch 索引"
  step_4: "生成 Qdrant payload + 计算 embedding 向量"
  step_5: "调用 qdrant-adapter 写入 Qdrant collection"
  step_6: "记录写入状态到 recycle_summary.external_storage_status"
  exhaust_retry: "若外部存储不可用，穷尽尝试所有替代存储路径，最终仅写入本地引擎文件，并在 external_storage_status 中标注 RETRYING"
```

#### 8.3 Meilisearch 写入格式

```json
{
  "id": "{knowledge_id}_{version}",
  "knowledge_id": "china_economy",
  "version": "v2",
  "finding": "全文发现/洞察/结论的原始文本",
  "finding_summary": "首200字摘要（用于搜索结果展示）",
  "domain_hint": "tech",
  "source_task_id": "T13",
  "confidence": "HIGH",
  "original_problem_summary": "原始问题简述（50字以内）",
  "provenance_source_task_id": "T09",
  "provenance_upstream": ["T02", "T03", "T04"],
  "provenance_discovery_node": "T09 Step 3 多路径推理路径B",
  "created_at": "2026-05-31T12:00:00Z",
  "updated_at": "2026-05-31T12:00:00Z",
  "decay_confidence": 0.85,
  "tags": ["经济", "GDP", "增速"],
  "searchable_attributes": ["finding", "finding_summary", "tags", "domain_hint", "original_problem_summary"],
  "filterable_attributes": ["domain_hint", "confidence", "source_task_id", "knowledge_id", "version"]
}
```

#### 8.4 Qdrant 写入格式

```yaml
qdrant_point:
  id: "{uuid_v4}"                             # 唯一标识符（UUID v4）
  vector: "{embedding_vector}"                 # 768/1536 维 embedding 向量
  payload:
    knowledge_id: "china_economy"
    version: "v2"
    finding: "全文发现/洞察/结论的原始文本"
    finding_summary: "首200字摘要"
    domain_hint: "tech"
    source_task_id: "T13"
    confidence: "HIGH"
    original_problem_summary: "原始问题简述"
    provenance:
      source_task_id: "T09"
      source_upstream_tasks: ["T02", "T03", "T04"]
      original_discovery_node: "T09 Step 3 多路径推理路径B"
    created_at: "2026-05-31T12:00:00Z"
    updated_at: "2026-05-31T12:00:00Z"
    decay_confidence: 0.85
    tags: ["经济", "GDP", "增速"]
```

#### 8.5 外部存储写入状态输出

```yaml
external_storage_status:
  meilisearch:
    status: "SUCCESS|RETRYING|SKIPPED"
    documents_written: 5
    index_name: "profound_cognition_knowledge"
    error: null
  qdrant:
    status: "SUCCESS|RETRYING|SKIPPED"
    points_written: 5
    collection_name: "profound_cognition_knowledge"
    vector_dim: 1536
    error: null
  local_files:
    status: "SUCCESS"
    files_written: 3
    file_paths:
      - "knowledge/domains/tech-engine.md"
      - "knowledge/domains/business-engine.md"
      - "knowledge/domains/social-engine.md"
```

---

## output_schema

```yaml
recycle_summary:
  total_candidates: int               # Step 1 扫描到的候选知识条目总数
  duplicates_filtered: int            # Step 2 去重过滤的条目数（相似度 >= 0.80 且结论一致）
  conflicts_detected: int             # Step 2 检测到的冲突条目数（相似度 >= 0.80 且结论矛盾）
  similars_annotated: int             # Step 2 标记为 SIMILAR 的条目数
  uniques_passed: int                 # Step 2 通过去重进入分类的唯一条目数
  written_to_engines:                 # 成功写入的引擎列表
    - engine: "tech"                  # 引擎名称（domain_hint）
      entries: 3                      # 写入该引擎的条目数
      file_path: "knowledge/domains/tech-engine.md"
      entry_summaries:
        - "finding 首50字摘要1"
        - "finding 首50字摘要2"
        - "finding 首50字摘要3"
      version_info:                   # 版本控制信息
        - knowledge_id: "ai_adoption_tech"
          version: "v2"
          is_new: false
          superseded: "ai_adoption_tech_v1"
        - knowledge_id: "quantum_computing_tech"
          version: "v1"
          is_new: true
          superseded: null
        - knowledge_id: "semiconductor_tech"
          version: "v1"
          is_new: true
          superseded: null
    - engine: "business"
      entries: 1
      file_path: "knowledge/domains/business-engine.md"
      entry_summaries:
        - "finding 首50字摘要"
      version_info:
        - knowledge_id: "china_economy"
          version: "v2"
          is_new: false
          superseded: "china_economy_v1"
    - engine: "cross_domain"
      entries: 2
      file_path: ["knowledge/domains/tech-engine.md", "knowledge/domains/social-engine.md"]
      entry_summaries:
        - "跨域发现1首50字摘要"
        - "跨域发现2首50字摘要"
      version_info:
        - knowledge_id: "ai_labor_cross"
          version: "v1"
          is_new: true
          superseded: null
        - knowledge_id: "digital_divide_cross"
          version: "v1"
          is_new: true
          superseded: null
    - ...
  skipped_no_match:                   # 无法匹配领域引擎的条目
    - finding: "无法分类的发现文本"
      reason: "domain_hint 无法映射，穷尽重试后仍无法匹配"
    - ...
  dedup_details:                      # 去重详细信息
    - original_finding: "被过滤的原始条目（首80字）"
      replaced_by_finding: "保留的条目（首80字）"
      similarity_score: 0.92
      filter_reason: "DUPLICATE"
    - original_finding: "相似但可保留的条目（首80字）"
      related_to_finding: "关联条目（首80字）"
      similarity_score: 0.67
      filter_reason: "SIMILAR_KEPT"
    - ...
  conflict_records:                   # 冲突检测记录
    - old_knowledge_id: "china_economy_v1"
      new_knowledge_id: "china_economy_v2"
      conflict_description: "旧结论认为GDP增速稳定在5%，新证据表明增速已降至4.5%"
      resolution_status: "PENDING"
    - ...
  decay_log:                          # 知识衰减日志
    - knowledge_id: "old_tech_trend_v1"
      decay_date: "2026-05-28"
      old_confidence: 0.8
      new_confidence: 0.7
      original_confidence: 0.8
      event_type: "DECAY"
    - knowledge_id: "restored_insight_v1"
      decay_date: "2026-05-28"
      old_confidence: 0.5
      new_confidence: 0.9
      original_confidence: 0.9
      event_type: "RESTORE"
    - ...
  write_timestamp: "2026-05-25T12:00:00Z"  # 写入时间戳
  layer_3_always_on:                    # Layer 3 始终激活输出（新增）
    dag_improvements:                   # DAG 改进建议（≥1 条）
      - suggestion: "建议在 T05 和 T06 之间增加中间验证节点"
        affected_nodes: ["T05", "T06"]
        rationale: "证据收集后增加交叉验证可提升结论置信度"
    methodology_optimizations:          # 方法论优化（≥1 条）
      - suggestion: "三角验证策略可增加贝叶斯更新权重"
        affected_protocol: "triangulation.md"
        rationale: "当前静态权重无法反映证据质量差异"
    rendering_feedback:                 # 渲染质量反馈（≥1 条）
      - suggestion: "图表配色方案建议增加色盲友好模式"
        affected_component: "chart-renderer.md"
        rationale: "当前配色在色盲用户中辨识度不足"
  external_storage_status:              # 外部存储写入状态（新增）
    meilisearch:
      status: "SUCCESS|RETRYING|SKIPPED"
      documents_written: 5
      index_name: "profound_cognition_knowledge"
      error: null
    qdrant:
      status: "SUCCESS|RETRYING|SKIPPED"
      points_written: 5
      collection_name: "profound_cognition_knowledge"
      vector_dim: 1536
      error: null
    local_files:
      status: "SUCCESS"
      files_written: 3
      file_paths: []
```

---

## self_check_before_output

- [ ] 是否仅扫描了 `cross_reference_potential == HIGH` 的 new_discoveries？
- [ ] 去重阈值 80% 是否严格执行？每一对 candidate 的相似度是否已计算？
- [ ] 相似度 >= 0.80 且结论矛盾的条目是否被标记为 CONFLICT（而非 DUPLICATE）？
- [ ] 冲突记录是否包含 old_knowledge_id / new_knowledge_id / conflict_description / resolution_status 四个字段？
- [ ] CONFLICT 条目的 resolution_status 是否均为 PENDING（未自动解析为 RESOLVED 或 DEFERRED）？
- [ ] 跨 source_task_id 的重复是否按照下游优先原则（T13 > T15 > T12 > T11 > T10 > T09）处理？
- [ ] T13 confidence == TENTATIVE 的结论是否被降去重优先级？
- [ ] domain_hint 与引擎文件的映射是否正确？是否所有 24 个引擎都在映射表中？
- [ ] 每条写入的 finding 是否严格遵循 `## [T21-AUTO] {YYYY-MM-DD}` 追加格式（含洞察/来源/置信度/原始上下文/知识ID/溯源链/版本信息）？
- [ ] 每个引擎文件中是否已存在语义相似的旧条目（阈值 0.80）？若存在是否正确区分 DUPLICATE 与 CONFLICT？
- [ ] cross_domain 类型的 finding 是否同时写入了所有相关引擎文件？
- [ ] skipped_no_match 列表是否完整记录了所有无法匹域的条目及其重试次数？
- [ ] dry_run 模式下是否确认无实际文件写入？
- [ ] 每条知识的 version_meta 是否完整（knowledge_id / current_version / previous_version / is_new / superseded / created_at / source_task_id / change_summary）？
- [ ] 同一 knowledge_id 的版本号是否严格递增（v1 -> v2 -> v3）？旧版本是否标注 superseded_by？
- [ ] 每条知识的 provenance 溯源链是否完整（source_task_id / source_upstream_tasks / original_discovery_node 三级）？
- [ ] 知识衰减是否执行？超过 90 天未引用的知识 confidence 是否降低 0.1（不低于 0.3）？
- [ ] 衰减日志中 new_confidence 是否 >= 0.3？old_confidence 是否 > new_confidence？
- [ ] `duplicates_filtered + conflicts_detected + similars_annotated + uniques_passed == total_candidates` 是否成立？
- [ ] output_schema 中所有 required_fields 是否全部存在且类型正确？
- [ ] write_timestamp 是否为 ISO 8601 格式（当前时间）？
- [ ] Layer 3 是否始终输出（always-on）？是否包含 dag_improvements（≥1 条）、methodology_optimizations（≥1 条）、rendering_feedback（≥1 条）三项最低输出？
- [ ] external_storage_status 是否完整？meilisearch / qdrant / local_files 三部分是否均已记录？
- [ ] Meilisearch 文档是否按规范 JSON 格式生成？id 是否为 {knowledge_id}_{version} 格式？
- [ ] Qdrant 写入时是否计算了 embedding 向量？payload 是否包含完整 provenance 溯源链？
- [ ] 外部存储写入失败时是否记录了 RETRYING 状态及具体 error 信息？

---

## must_not

- T21 在 EXHAUST-only 模式下始终激活
- 禁止扫描 `cross_reference_potential != HIGH` 的 new_discoveries（MEDIUM/LOW 级发现不回收，避免知识污染）
- 禁止跳过去重步骤直接写入（去重是防止知识库膨胀的核心防线）
- 禁止对相似度 0.50-0.80 的条目执行去重（应保留并标注 SIMILAR，而非直接丢弃）
- 禁止覆盖或删除引擎文件中的现有内容（仅在文件末尾追加）
- 禁止将 T13 `confidence == TENTATIVE` 的结论以高于其他副本的优先级保留
- 禁止将 finding 写入不匹配的引擎文件（domain_hint 映射错误不可接受）
- 禁止在同一引擎文件的同一条 finding 重复写入（同一批次内同一引擎）
- 禁止在未经语义去重的情况下将同一 finding 写入多个引擎文件（除非是 cross_domain 类型且确实属于多个领域）
- 禁止使用非规范化的追加格式（必须严格遵循 `## [T21-AUTO]` 模板，含洞察/来源/置信度/原始上下文/知识ID/溯源链/版本信息全部字段）
- 禁止在 dry_run 模式下执行实际文件写入操作
- 禁止删除或覆盖旧版本知识（新版本追加写入，旧版本标注 superseded_by 后保留）
- 禁止自动解析 CONFLICT 冲突（resolution_status 不得在当前执行中从 PENDING 改为 RESOLVED 或 DEFERRED，必须等待人工审核）
- 禁止知识衰减后 confidence 低于 0.3（0.3 为硬下限，衰减后 new_confidence 不得低于此值）
- 禁止省略 provenance 溯源链（每条知识必须包含 source_task_id / source_upstream_tasks / original_discovery_node，确保可回溯至原始 DAG 节点）
- 禁止跳过 Layer 3 输出（always-on 模式下 Layer 3 必须产出，dag_improvements / methodology_optimizations / rendering_feedback 三项缺一不可）
- 禁止在外部存储可用时仅写入本地引擎文件（必须同时执行 Meilisearch + Qdrant 写入）
- 禁止 Meilisearch 文档 id 格式不规范（必须为 {knowledge_id}_{version}）
- 禁止 Qdrant payload 缺少 provenance 溯源链（必须包含 source_task_id / source_upstream_tasks / original_discovery_node）
- 禁止外部存储写入失败后不记录 RETRYING 状态（必须在 external_storage_status 中明确标注失败原因）

---

## knowledge_refs

- `knowledge/domain-engines.md` — 35 个领域引擎的完整列表、描述与激活规则
- `knowledge/domains/*-engine.md` — 各领域引擎的知识存储文件（T21 的写入目标）
- `tasks/T09_cog_reason.md` — 新发现产出规范（new_discoveries 字段定义与 cross_reference_potential 分级）
- `tasks/T13_cog_synthesize.md` — 核心结论产出规范（core_conclusions 字段定义与 confidence_rating 分级）
- `tasks/T15_domain_analysis.md` — 领域洞察产出规范（domain_insights 字段定义）
- `tasks/T15b_cross_domain_matrix.md` — 跨域共振矩阵产出规范（resonance 条目定义，仅 EXHAUST）
- `protocols/execution-protocol.md` — 执行协议定义
- `plugins/meilisearch-adapter.md` — Meilisearch 全文搜索适配器（外部存储写入）
- `plugins/qdrant-adapter.md` — Qdrant 向量数据库适配器（外部存储写入）
- `persona/persona-schema.yaml` — 人设 Schema 定义文件

## 外部能力卡片引用

- **TC-093 KGHeartBeat**: 知识图谱质量监控，在知识回收写入引擎文件后（Step 4），调用 KGHeartBeat 对已归档知识进行一致性约束检查、完整性扫描、时效性扫描和冲突检测，自动生成知识质量诊断报告。详见 `knowledge/external-capabilities-index.md`

---

### MC-137 KG质量监控方法论 (TC-093 KGHeartBeat)

**方法论原理**：知识图谱质量监控的核心认知假设是——知识资产如同物理资产，会随时间"老化"（事实过时）、"损坏"（逻辑矛盾）和"缺失"（覆盖不全），需要系统性的"体检"机制来维持知识库的健康状态。KGHeartBeat将知识质量监控分解为四个维度：一致性（内部逻辑不自洽）、完整性（关键信息缺失）、时效性（事实过时）和冲突性（不同来源矛盾）。这种方法论使我们从"写入即遗忘"升级为"持续质量审计"。

> 知识来源: TC-093 [KGHeartBeat]

**执行步骤**：
1. **一致性约束4类检查**：
   - 类型一致性：实体的类型声明是否与属性值兼容（如"人"不应有"面积"属性）
   - 关系一致性：关系的方向和基数是否满足约束（如"出生于"应指向"地点"而非"人物"）
   - 值域一致性：属性值是否在合理范围内（如"人口"应为正整数）
   - 逻辑一致性：传递性/对称性约束是否满足（如A属于B，B属于C，则A应属于C）
2. **完整性检查3维度**：
   - 属性完整性：核心属性是否缺失（如"国家"实体应有"首都""人口""面积"）
   - 关系完整性：关键关系是否建立（如"政策"实体应关联"实施机构"）
   - 来源完整性：每条知识是否有来源标注
3. **时效性扫描规则**：
   - 量化数据时效：人口/GDP等数据标注年份，超过3年标记为"可能过时"
   - 事件时效：已完成事件标注结束时间，进行中事件每6个月复查
   - 技术时效：技术类知识标注版本号，主版本升级后标记为"需更新"
4. **冲突检测2策略**：
   - 同源冲突检测：同一来源内不同条目的矛盾（如两处给出不同人口数据）
   - 跨源冲突检测：不同来源对同一事实的矛盾陈述

> 知识来源: TC-093 [KGHeartBeat]

**决策规则**：

| 条件 | 决策 |
|------|------|
| 一致性检查发现违规 | 标注违规类型和严重度，高严重度立即修正 |
| 核心属性缺失 | 触发补全搜索（使用Wikidata/ConceptNet补充） |
| 数据超过3年未更新 | 标注为"可能过时"，触发更新搜索 |
| 发现跨源冲突 | 记录冲突，以来源权威性为优先级裁决 |
| 整体质量评分 < 0.6 | 触发全面知识审计，生成修复计划 |

> 知识来源: TC-093 [KGHeartBeat]

**输出规范**：
```yaml
kg_quality_report:
  consistency:
    type_violations: [{entity: str, expected_type: str, actual_type: str, severity: "high|medium|low"}]
    relation_violations: [{subject: str, relation: str, object: str, violation: str}]
    value_range_violations: [{entity: str, property: str, value: str, expected_range: str}]
    logic_violations: [{description: str, chain: [str]}]
  completeness:
    missing_properties: [{entity: str, missing: [str]}]
    missing_relations: [{entity: str, missing: [str]}]
    missing_sources: [{entity: str, property: str}]
  timeliness:
    outdated_data: [{entity: str, property: str, last_updated: str, status: "possibly_outdated|needs_update"}]
  conflicts:
    intra_source: [{source: str, fact_a: str, fact_b: str, conflict_type: str}]
    inter_source: [{fact: str, sources: [{source: str, value: str}], resolution: str}]
  overall_score: float
  remediation_plan: [str]
```

> 知识来源: TC-093 [KGHeartBeat]

**穷尽重试策略**：当KGHeartBeat不可用时，穷尽尝试LLM自检：LLM对回收的知识条目逐条检查逻辑一致性和时效性，标注`quality_check_method=llm_self_check, confidence_penalty=-0.1`。

> 知识来源: TC-093 [KGHeartBeat]

---

## Y8: 盲预测 + 复盘闭环

在知识回收完成后，基于回收知识对文章输出做 3-5 条预测（先于实际输出）：

| 预测维度 | 预测内容 | 置信度(1-5) |
|---------|---------|------------|
| 质疑论点 | 哪些论点可能被读者质疑？ | [1-5] |
| 分享段落 | 哪些段落最可能被分享/截图？ | [1-5] |
| 跳过部分 | 读者最可能跳过哪部分？ | [1-5] |
| 信息缺口 | 读者看完后会问"那XX呢？"的问题 | [1-5] |
| 时效性预判 | 多久后文章的内容可能需要更新？ | [1-5] |

输出后复盘：逐条对比预测与实际情况
- CORRECT: 预测与输出一致
- PARTIALLY: 部分正确
- INCORRECT: 预测错误
- UNVERIFIABLE: 无法验证

连续 3 轮 CORRECT 率<40% → 触发方法论审查
