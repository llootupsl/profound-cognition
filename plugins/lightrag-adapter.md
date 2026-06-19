---
name: lightrag-adapter
description: LightRAG 适配器 — 将研究底座和知识回收产出自动构建/增量更新 LightRAG 知识图谱索引，实现三层知识架构
author: 阿洋
tags: [lightrag, knowledge-graph, adapter, t02, t21, rag]
---

# LightRAG 适配器

## 概述

本模块为 T02（研究底座）和 T21（知识回收）节点提供 LightRAG 知识图谱适配器，将研究产出自动构建为 LightRAG 本地知识图谱索引，并与 Wikidata（结构化知识）和 ConceptNet（常识推理）组成三层知识架构。LightRAG 提供实体关系发现、社区检测和语义检索能力，是研究底座知识沉淀的核心引擎。

---

## 激活条件

```yaml
activation:
  condition: "always（EXHAUST-only）AND (T02 研究底座产出 OR T21 知识回收产出) 非空"
  priority: "可选增强 — 构建本地知识图谱索引，提升后续研究的语义检索能力"
  exhaust-retry: "若 LightRAG 不可用，使用传统关键词检索 + Wikidata/ConceptNet 远程查询"
```

---

## 安装与调用

### 安装

```bash
pip install lightrag-hku
```

### Python API 调用

```python
from lightrag import LightRAG, QueryParam
from lightrag.llm import openai_complete_if_cache, openai_embed

WORKING_DIR = "./lightrag_index"

rag = LightRAG(
    working_dir=WORKING_DIR,
    llm_model_func=openai_complete_if_cache,
    embedding_func=openai_embed,
)

# 插入文档（构建索引）
rag.insert(research_content)

# 查询（语义检索）
result = rag.query("研究问题", param=QueryParam(mode="hybrid"))
```

### 查询模式

```yaml
query_modes:
  naive: "朴素检索 — 基于关键词匹配，速度最快"
  local: "局部检索 — 基于实体关系子图，适合具体问题"
  global_: "全局检索 — 基于社区检测摘要，适合宏观问题"
  hybrid: "混合检索 — 结合局部和全局，最全面（推荐）"
```

---

## 与 T02 的集成：研究底座产出自动构建 LightRAG 索引

### 集成流程

```yaml
T02_integration:
  trigger: "T02 研究底座产出完成（L1-L7 全部层级）"
  step_1_collect:
    method: "收集 T02 各层级产出文本"
    sources:
      - "L1 基础事实层：事实条目列表"
      - "L2 因果链层：因果链和机制描述"
      - "L3 结构变量层：变量定义和关系矩阵"
      - "L4 利益相关者层：利益相关者分析"
      - "L5 情景层：情景描述"
      - "L6 证据边界层：证据链和验证结果"
      - "L7 综合层：综合分析"
    output: "T02_collected_content"

  step_2_insert:
    method: "将收集的文本批量插入 LightRAG 索引"
    command: "rag.insert(T02_collected_content)"
    output: "LightRAG 索引更新"

  step_3_validate:
    method: "执行测试查询验证索引质量"
    command: "rag.query('研究问题', param=QueryParam(mode='hybrid'))"
    output: "索引验证结果"
```

### T02 context 扩展

```yaml
T02_context:
  research_query: "用户研究问题"
  lightrag_index:
    enabled: "always（EXHAUST-only）"
    working_dir: "./lightrag_index/{research_id}"
    auto_build: true
    build_trigger: "T02 产出完成"
    annotation: "[lightrag] 标签标记知识图谱来源"
```

---

## 与 T21 的集成：知识回收产出增量更新 LightRAG 索引

### 集成流程

```yaml
T21_integration:
  trigger: "T21 知识回收完成（产出新知识条目）"
  step_1_extract:
    method: "提取 T21 产出的新知识条目"
    sources:
      - "新发现的事实"
      - "修正的因果链"
      - "更新的变量关系"
      - "新的利益相关者信息"
    output: "T21_new_knowledge_items"

  step_2_incremental_insert:
    method: "将新知识条目增量插入现有 LightRAG 索引"
    command: "rag.insert(T21_new_knowledge_items)"
    strategy: "增量更新 — 不重建索引，仅插入新内容"
    output: "LightRAG 索引增量更新"

  step_3_verify:
    method: "执行查询验证增量更新效果"
    command: "rag.query('新知识相关问题', param=QueryParam(mode='hybrid'))"
    output: "增量更新验证结果"
```

### T21 context 扩展

```yaml
T21_context:
  knowledge_recovery:
    lightrag_update:
      enabled: " ∈ {DEEP, EXHAUST}"
      strategy: "incremental"
      working_dir: "./lightrag_index/{research_id}"
      annotation: "[lightrag-incremental] 标签标记增量更新来源"
```

---

## 三层知识架构

### 架构总览

```yaml
three_layer_architecture:
  layer_1_local:
    name: "LightRAG（本地知识图谱）"
    scope: "当前研究项目的专属知识图谱"
    capabilities:
      - "实体关系发现：自动从研究文本中抽取实体和关系"
      - "社区检测：识别实体社区和主题聚类"
      - "语义检索：基于向量的混合检索（naive/local/global/hybrid）"
      - "增量更新：支持新知识增量插入，无需重建索引"
    use_cases:
      - "T02-T06 研究底座中的实体关系发现"
      - "T02-T06 研究底座中的社区检测"
      - "跨研究项目的知识复用"
    data_source: "T02 研究底座产出 + T21 知识回收产出"
    storage: "本地文件系统（./lightrag_index/）"

  layer_2_structured:
    name: "Wikidata SPARQL（结构化知识查询）"
    scope: "全球结构化事实数据库"
    capabilities:
      - "实体属性查询：量化数据验证"
      - "实体间关系查询：结构化关系发现"
      - "类层级查询：分类体系验证"
    use_cases:
      - "事实性数据验证"
      - "结构化关系补充"
    data_source: "Wikidata 公开 SPARQL Endpoint"
    storage: "远程 API"

  layer_3_commonsense:
    name: "ConceptNet 5.7（常识推理）"
    scope: "常识概念网络"
    capabilities:
      - "语义关联：概念间的 IsA/PartOf/Causes 关系"
      - "类比推理：概念间的隐含关联路径"
      - "概念扩展：发散性概念联想"
    use_cases:
      - "类比和关联推理"
      - "隐含假设挖掘"
      - "概念边界确认"
    data_source: "ConceptNet 公开 API"
    storage: "远程 API"
```

### 三层协同策略

```yaml
layer_cooperation:
  fact_verification:
    flow: "LightRAG 本地检索 → Wikidata 交叉验证 → ConceptNet 语义补充"
    priority: "Wikidata > LightRAG > ConceptNet（事实性结论）"

  relationship_discovery:
    flow: "LightRAG 实体关系抽取 → ConceptNet 常识关联 → Wikidata 结构化关系"
    priority: "LightRAG > ConceptNet > Wikidata（关系发现）"

  analogy_reasoning:
    flow: "ConceptNet 语义路径 → LightRAG 本地类比 → Wikidata 事实基准"
    priority: "ConceptNet > LightRAG > Wikidata（类比推理）"

  knowledge_recovery:
    flow: "LightRAG 增量更新 → Wikidata 验证新知识 → ConceptNet 补充关联"
    priority: "LightRAG > Wikidata > ConceptNet（知识回收）"
```

### 来源标注规范

```yaml
source_annotation:
  lightrag:
    source_category: "L1"
    source: "lightrag:{research_id}"
    confidence_base: 0.8
    annotation: "[lightrag] 本地知识图谱"

  wikidata:
    source_category: "L0"
    source: "wikidata:{qid}"
    confidence_base: 0.95
    annotation: "[wikidata] 结构化知识库"

  conceptnet:
    source_category: "L2"
    source: "conceptnet:{concept}"
    confidence_base: 0.7
    annotation: "[conceptnet] 常识推理"
```

---

## 错误处理

```yaml
error_handling:
  library_not_available:
    action: "穷尽重试到传统关键词检索 + Wikidata/ConceptNet 远程查询"
    log: "记录 LightRAG 不可用事件，标注 exhaust-retry_reason=lightrag_not_installed"

  index_corrupted:
    action: "从 T02 产出重建索引"
    log: "记录索引损坏事件，标注 rebuild_trigger=corruption_detected"

  insert_failure:
    action: "跳过失败条目，继续插入其余条目"
    log: "记录插入失败事件，标注 failed_content_hash={hash}"

  query_timeout:
    action: "穷尽重试到 naive 模式查询"
    log: "记录查询超时事件，标注 exhaust-retry_mode=naive"
    timeout: 30000  # ms

  embedding_failure:
    action: "使用本地备选嵌入模型"
    log: "记录嵌入失败事件，标注 exhaust-retry_reason=embedding_error"

  disk_full:
    action: "清理旧索引缓存，释放空间后重试"
    log: "记录磁盘空间不足事件"
```

---

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| v1.0 | 2026-05-28 | 初始发布：LightRAG 适配器 + T02/T21 集成方案 + 三层知识架构 |

---

© 阿洋


---

## 穷尽重试策略

```yaml
exhaust_retry:
  L1_FULL:
    condition: "LightRAG 可用 + 嵌入模型正常"
    behavior: "完整知识图谱构建 + 四种查询模式 + 增量更新 + 三层知识架构"

  L2_PARTIAL_DATA:
    condition: "LightRAG 可用但嵌入模型异常"
    behavior: "穷尽重试到naive查询模式 + 标注[NAIVE-ONLY]"

  L3_TEXT_ONLY:
    condition: "LightRAG 不可用"
    behavior: "穷尽尝试到关键词检索 + Wikidata/ConceptNet远程查询 + 标注[KEYWORD-ONLY]"

  L4_SERVICE_DOWN:
    condition: "所有知识图谱工具不可用"
    behavior: "纯LLM内建知识 + 标注[INTERNAL_REASONING]"
```
