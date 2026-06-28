<!-- 作者：阿洋 -->

# 知识图谱集成规范

> **模块标识**: `knowledge/knowledge-graph-integration`
> **依赖**: `knowledge/evidence-standards`
> **核心原则**: 在可达条件下优先使用结构化知识图谱验证事实、补充概念关联。知识图谱不可用时自动穷尽尝试至 LLM 自有知识，并明确标注 source_category 等级。
>
> **版本治理元数据 (D12.4.2)**:
> - version: 1.1
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（Wikidata + ConceptNet 三层架构）
>   - v1.1 补全版本治理元数据与交叉引用（D12.4.2-D12.4.3）

## 交叉引用

- **上游**: `knowledge/evidence-standards.md`（证据等级标准）
- **下游**: `tasks/T02_L1_L2_research.md`、`tasks/T03_L3_structural.md`、`tasks/T05_L6_L7_evidence.md`、`tasks/T08_cog_deconstruct.md`、`tasks/T21_knowledge_recycle.md`
- **相关**: `knowledge/external-capabilities-index.md`（TC-009 Wikidata、TC-010 ConceptNet、TC-011 LightRAG）、`plugins/lightrag-adapter.md`（LightRAG 适配器）、`knowledge/source-verification.md`（来源核实）
- **协议**: `protocols/execution-protocol.md`（节点执行时按需调用 KG）

---

## 1. 概述

本文档定义 Profound Cognition 框架与外部知识图谱（Wikidata、ConceptNet）的集成规范，包括查询模板、结果解析规则、穷尽尝试策略以及各任务节点的调用场景映射。

### 1.1 三层知识架构

本框架采用三层知识架构，从本地到远程、从专属到通用，逐层扩展知识覆盖范围：

| 层级 | 知识图谱 | 定位 | 核心能力 | 主调用节点 |
|------|---------|------|---------|-----------|
| L1 本地 | LightRAG | 当前研究项目的专属知识图谱 | 实体关系发现、社区检测、语义检索、增量更新 | T02、T06、T21 |
| L2 结构化 | Wikidata | 全球结构化事实数据库 | 实体属性查询、实体间关系查询、类层级查询 | T02、T03、T05 |
| L3 常识 | ConceptNet 5.7 | 常识概念网络 | 概念间语义关联、ISA 层级、能力/用途/因果关系 | T08 |

### 1.2 两大远程知识图谱

| 知识图谱 | 定位 | 核心能力 | 主调用节点 |
|---------|------|---------|-----------|
| Wikidata | 结构化事实数据库 | 实体属性查询、实体间关系查询、类层级查询 | T02、T03、T05 |
| ConceptNet 5.7 | 常识概念网络 | 概念间语义关联、ISA 层级、能力/用途/因果关系 | T08 |

### 1.3 调用原则

1. **可选非强制**：所有知识图谱查询均为可选增强步骤，非节点执行的前置条件
2. **标注来源**：通过 KG 验证的事实标注 `source_category=L0`（权威数据库）；KG 不可用时穷尽尝试 LLM 自有知识，标注 `source_category=L3, confidence_penalty=-0.2` 并注明 `exhaust-retry: llm_knowledge`
3. **不阻塞流程**：KG 查询失败或超时时，自动走穷尽尝试路径，不阻塞 Sub-Agent 执行
4. **质量驱动查询**：每个节点穷尽发起 KG 查询直至质量达标，不设上限

---

## 2. LightRAG 本地知识图谱

### 3.1 基本信息

| 项目 | 值 |
|------|-----|
| 安装方式 | `pip install lightrag-hku` |
| 存储方式 | 本地文件系统（`./lightrag_index/{research_id}/`） |
| 索引构建 | T02 研究底座产出自动构建 |
| 索引更新 | T21 知识回收产出增量更新 |
| 查询模式 | naive / local / global / hybrid |
| 超时设置 | 30 秒 |

### 2.2 与 T02 的集成：研究底座产出自动构建索引

**调用场景**：T02 研究底座产出完成后（L1-L7 全部层级），将各层级产出文本批量插入 LightRAG 索引。

**集成流程**：

1. 收集 T02 各层级产出文本（L1 事实、L2 因果链、L3 变量、L4 利益相关者、L5 情景、L6 证据、L7 综合）
2. 调用 `rag.insert(T02_collected_content)` 批量插入
3. 执行测试查询验证索引质量

**来源标注**：`source_category=L1, source=lightrag:{research_id}`

### 2.3 与 T21 的集成：知识回收产出增量更新索引

**调用场景**：T21 知识回收完成后，将新知识条目增量插入现有 LightRAG 索引。

**集成流程**：

1. 提取 T21 产出的新知识条目
2. 调用 `rag.insert(T21_new_knowledge_items)` 增量插入
3. 执行查询验证增量更新效果

**来源标注**：`source_category=L1, source=lightrag:{research_id}, update_type=incremental`

### 2.4 查询模式选择

| 查询模式 | 适用场景 | 说明 |
|---------|---------|------|
| `naive` | 快速关键词检索 | 基于关键词匹配，速度最快 |
| `local` | 具体问题检索 | 基于实体关系子图，适合具体问题 |
| `global` | 宏观问题检索 | 基于社区检测摘要，适合宏观问题 |
| `hybrid` | 综合检索 | 结合局部和全局，最全面（推荐） |

### 2.5 三层架构协同策略

| 场景 | LightRAG 角色 | Wikidata 角色 | ConceptNet 角色 |
|------|-------------|-------------|----------------|
| 事实验证 | 本地知识检索 | 交叉验证量化数据 | 语义补充 |
| 关系发现 | 实体关系抽取 | 结构化关系补充 | 常识关联 |
| 类比推理 | 本地类比 | 事实基准 | 语义路径（优先） |
| 知识回收 | 增量更新索引 | 验证新知识 | 补充关联 |

### 2.6 穷尽尝试策略

| 场景 | 判定条件 | 穷尽尝试动作 |
|------|---------|---------|
| 库未安装 | `lightrag-hku` 不可用 | 使用传统关键词检索 + Wikidata/ConceptNet 远程查询 |
| 索引损坏 | 索引文件异常 | 从 T02 产出重建索引 |
| 插入失败 | 单条内容插入失败 | 跳过失败条目，继续插入其余 |
| 查询超时 | 查询超过 30 秒 | 穷尽重试 naive 模式查询 |

---

## 3. Wikidata SPARQL 查询规范

### 2.1 基本信息

| 项目 | 值 |
|------|-----|
| Endpoint URL | `https://query.wikidata.org/sparql` |
| 查询语言 | SPARQL 1.1 |
| 响应格式 | JSON（默认）/ XML / CSV / TSV |
| 请求方式 | GET（查询串通过 `?query=` 参数传递） / POST（`application/x-www-form-urlencoded` 或 `application/sparql-query`） |
| 用户代理头 | `Profound-Cognition/2.0 (research-agent)` |
| 超时设置 | 15 秒 |

### 3.2 实体属性查询模板

查询指定实体（Q-ID）的某个属性值。

```sparql
# 查询实体属性值
SELECT ?item ?itemLabel ?property ?value ?valueLabel WHERE {
  VALUES ?item { wd:Q{entity_id} }
  ?item wdt:P{property_id} ?value .
  OPTIONAL { ?value rdfs:label ?valueLabel . FILTER(LANG(?valueLabel) = "zh") }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "zh,[AUTO_LANGUAGE],en". }
}
LIMIT 20
```

**参数说明**：
- `{entity_id}`：Wikidata 实体 ID（如北京 = Q956，气候变化 = Q125928）
- `{property_id}`：Wikidata 属性 ID（如人口 = P1082，面积 = P2046，成立时间 = P571）

### 3.3 实体间关系查询模板

查询两个实体之间的直接或间接关系。

```sparql
# 查询实体间关系
SELECT ?relation ?relationLabel WHERE {
  wd:Q{entity_id_1} ?relation wd:Q{entity_id_2} .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "zh,en". }
}
```

```sparql
# 查询实体的全部外向关系
SELECT ?property ?propertyLabel ?value ?valueLabel WHERE {
  wd:Q{entity_id} ?propStatement ?value .
  ?property wikibase:directClaim ?propStatement .
  OPTIONAL { ?value rdfs:label ?valueLabel . FILTER(LANG(?valueLabel) = "zh") }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "zh,en". }
}
LIMIT 50
```

### 3.4 类查询模板

查询实体所属的类别层级。

```sparql
# 查询实体所属的类（instance of / subclass of）
SELECT ?class ?classLabel WHERE {
  wd:Q{entity_id} wdt:P31/wdt:P279* ?class .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "zh,en". }
}
LIMIT 20
```

```sparql
# 查询某一类的所有实例
SELECT ?item ?itemLabel WHERE {
  ?item wdt:P31 wd:Q{class_id} .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "zh,en". }
}
LIMIT 50
```

### 3.5 结果解析规则

#### 3.5.1 响应结构

Wikidata SPARQL 返回标准 JSON 绑定格式：

```json
{
  "head": { "vars": ["item", "itemLabel", "value", "valueLabel"] },
  "results": {
    "bindings": [
      {
        "item": { "type": "uri", "value": "http://www.wikidata.org/entity/Q956" },
        "itemLabel": { "type": "literal", "xml:lang": "zh", "value": "北京" },
        "value": { "type": "literal", "datatype": "http://www.w3.org/2001/XMLSchema#decimal", "value": "21893095" }
      }
    ]
  }
}
```

#### 3.5.2 解析规则

| 步骤 | 操作 | 说明 |
|------|------|------|
| 1 | 检查 `results.bindings` 是否为空 | 空 → 查询无结果，走穷尽尝试策略 |
| 2 | 提取 `*.value` 字段 | URI 类型 → 提取 Q-ID；Literal 类型 → 直接使用值 |
| 3 | 提取 `*Label` 字段 | 优先取 `xml:lang="zh"` 的中文标签，无中文时取英文 |
| 4 | 事实对比 | 将查询结果与待验证事实逐条对比，记录匹配度 |
| 5 | 来源标注 | 匹配成功 → `source_category=L0, source=wikidata:{qid}` |

#### 3.5.3 数据类型处理

| XML Schema 类型 | 处理方式 |
|-----------------|---------|
| `xsd:decimal` / `xsd:integer` | 直接作为数值使用 |
| `xsd:dateTime` / `xsd:date` | 格式化为 YYYY-MM-DD |
| `xsd:string` | 直接使用 |
| `rdf:langString` | 按语言偏好取中文优先 |
| URI（entity） | 提取 Q-ID 尾号作为实体标识 |

### 3.6 实体发现辅助查询

当无法直接确定实体的 Q-ID 时，使用以下查询搜索实体。

```sparql
# 按标签搜索实体
SELECT ?item ?itemLabel ?description WHERE {
  ?item rdfs:label ?itemLabel .
  FILTER(CONTAINS(LCASE(?itemLabel), LCASE("{search_term}")))
  FILTER(LANG(?itemLabel) = "zh" || LANG(?itemLabel) = "en")
  OPTIONAL { ?item schema:description ?description . FILTER(LANG(?description) = "zh") }
}
LIMIT 10
```

### 3.7 穷尽尝试策略

| 场景 | 判定条件 | 穷尽尝试动作 |
|------|---------|---------|
| 网络超时 | 请求超过 15 秒无响应 | 跳过 Wikidata 查询，标注 `source_category=L3, source=llm_knowledge, exhaust_retry_reason=wikidata_timeout, confidence_penalty=-0.2` |
| 响应异常 | HTTP 状态码非 2xx | 同上，标注 `source_category=L3, source=llm_knowledge, exhaust_retry_reason=wikidata_http_{status_code}, confidence_penalty=-0.2` |
| 实体未找到 | 实体搜索无结果 | 使用 LLM 自有知识，标注 `source_category=L3, source=llm_knowledge, exhaust_retry_reason=entity_not_found_in_wikidata, confidence_penalty=-0.2` |
| 查询无结果 | SPARQL 返回空 bindings | 使用 LLM 自有知识，标注 `source_category=L3, source=llm_knowledge, exhaust_retry_reason=no_sparql_results, confidence_penalty=-0.2` |
| 结果矛盾 | KG 结果与 LLM 知识冲突 | 优先采信 KG 结果（`source_category=L0, source=wikidata`），同时记录 LLM 知识的差异 (`llm_divergence_noted: true`) |

---

## 4. ConceptNet 5.7 查询规范

### 4.1 基本信息

| 项目 | 值 |
|------|-----|
| API Endpoint | `https://api.conceptnet.io/` |
| 查询方式 | RESTful HTTP GET |
| 响应格式 | JSON |
| 超时设置 | 10 秒 |
| 用户代理头 | `Profound-Cognition/2.0 (research-agent)` |

### 4.2 关系类型枚举

| 关系类型 | URI | 含义 | 适用场景 |
|---------|-----|------|---------|
| IsA | `/r/IsA` | X 是 Y 的一种 | 概念分类、上下位关系 |
| HasA | `/r/HasA` | X 拥有/包含 Y | 组成关系、属性归属 |
| PartOf | `/r/PartOf` | X 是 Y 的一部分 | 整体-部分关系 |
| UsedFor | `/r/UsedFor` | X 用于做 Y | 工具/方法的用途 |
| CapableOf | `/r/CapableOf` | X 能够做 Y | 能力/功能描述 |
| Causes | `/r/Causes` | X 导致 Y | 因果关系 |
| CausesDesire | `/r/CausesDesire` | X 引发对 Y 的欲望 | 动机分析 |
| CreatedBy | `/r/CreatedBy` | X 由 Y 创建 | 来源/创作者 |
| DefinedAs | `/r/DefinedAs` | X 的定义包含 Y | 定义与语义 |
| HasProperty | `/r/HasProperty` | X 具有属性 Y | 属性描述 |
| MotivatedByGoal | `/r/MotivatedByGoal` | X 的动机源自目标 Y | 深层动机分析 |
| RelatedTo | `/r/RelatedTo` | X 与 Y 相关 | 通用关联（兜底关系） |
| Synonym | `/r/Synonym` | X 与 Y 同义 | 术语等价 |
| Antonym | `/r/Antonym` | X 与 Y 反义 | 对立概念 |
| DerivedFrom | `/r/DerivedFrom` | X 派生自 Y | 词源/概念溯源 |
| EtymologicallyRelatedTo | `/r/EtymologicallyRelatedTo` | X 与 Y 词源相关 | 语言起源联系 |

### 4.3 查询模板

#### 4.3.1 概念查询

查询与指定概念相关的所有边（前向与后向）。

```
GET /query?node=/c/zh/{concept}&language=zh&limit=20
```

**参数说明**：
- `node`：概念 URI，中文概念使用 `/c/zh/{concept}`，英文使用 `/c/en/{concept}`
- `language`：过滤语言
- `limit`：返回结果上限（建议 20）
- `offset`：分页偏移量（可选）

#### 4.3.2 关系筛选查询

查询指定概念与特定关系类型的边。

```
GET /query?start=/c/zh/{concept}&rel=/r/{relation_type}&limit=20
```

**示例**：查询"人工智能"的"能做什么"关系：

```
https://api.conceptnet.io/query?start=/c/zh/人工智能&rel=/r/CapableOf&limit=20
```

#### 4.3.3 概念间路径查询

查询两个概念之间的最短关联路径（含中间概念）。

```
GET /query?start=/c/zh/{concept_a}&end=/c/zh/{concept_b}&limit=5
```

#### 4.3.4 多语言概念查询

用英文概念 URIs 作为基准（覆盖面更广），同时获取中文关联。

```
GET /query?node=/c/en/{concept}&language=zh&limit=20
```

### 4.4 结果解析规则

#### 4.4.1 响应结构

```json
{
  "@context": ["http://api.conceptnet.io/ld/conceptnet5.7/context.ld.json"],
  "@id": "/query?node=/c/zh/人工智能&rel=/r/CapableOf&limit=3",
  "edges": [
    {
      "@id": "/a/[/r/CapableOf/,/c/zh/人工智能/,/c/zh/学习/]",
      "rel": { "@id": "/r/CapableOf", "label": "CapableOf" },
      "start": { "@id": "/c/zh/人工智能", "label": "人工智能", "language": "zh" },
      "end": { "@id": "/c/zh/学习", "label": "学习", "language": "zh" },
      "surfaceText": "[[人工智能]]可以[[学习]]",
      "weight": 1.5,
      "sources": [
        {
          "@id": "/s/resource/wordnet/3.0/",
          "contributor": "/s/resource/wordnet/3.0/"
        }
      ]
    }
  ]
}
```

#### 4.4.2 解析规则

| 步骤 | 操作 | 说明 |
|------|------|------|
| 1 | 检查 `edges` 数组是否非空 | 空 → 查询无结果，走穷尽尝试策略 |
| 2 | 按 `weight` 降序排列 | weight ≥ 1.0 为高置信度关联，0.5-1.0 为中置信度，< 0.5 为低置信度 |
| 3 | 提取 `rel.label` 作为关系类型 | 与 3.2 节枚举值对照 |
| 4 | 提取 `start.label` 和 `end.label` | 分别作为源概念和目标概念 |
| 5 | 提取 `surfaceText` | 作为自然语言表述，可直接用于概念解构中的关联表述 |
| 6 | 去重 | 同一 `(start, rel, end)` 三元组去重，保留最高 weight |

#### 4.4.3 权重阈值建议

| 场景 | 最小 weight 阈值 | 说明 |
|------|-----------------|------|
| 核心概念解构 | 1.0 | 仅采信高置信度关联 |
| 概念扩展/联想 | 0.5 | 允许中等置信度关联 |
| 发散探索 | 0.0 | 不设阈值，但标注权重 |

### 4.5 穷尽尝试策略

| 场景 | 判定条件 | 穷尽尝试动作 |
|------|---------|---------|
| 网络超时 | 请求超过 10 秒无响应 | 跳过 ConceptNet 查询，使用 LLM 概念分析能力 |
| 响应异常 | HTTP 状态码非 2xx | 同上，`exhaust_retry_reason=conceptnet_http_{status_code}` |
| 无匹配概念 | 查询返回空 edges | 使用 LLM 自有概念分析，标注 `exhaust_retry_reason=no_conceptnet_match` |
| 低权重结果 | 所有 edges 权重 < 0.5 | 使用 LLM 自有分析，记录 ConceptNet 低权重结果作为参考 |

---

## 5. 各节点调用场景表

### 5.1 节点-KG 映射总览

| 节点 | KG | 调用时机 | 调用目的 | 调用频率 | 穷尽尝试标注 |
|------|-----|---------|---------|---------|---------|
| T02 | Wikidata | L1 事实收集阶段 | 验证关键事实的客观数据（人口、面积、日期、金额等量化指标） | 质量驱动 | `source_category=L3, source=llm_knowledge, exhaust_retry_reason=*, confidence_penalty=-0.2` |
| T03 | Wikidata | L3 结构变量分析阶段 | 获取结构变量（分类体系、层级关系、地理/组织归属）的结构化数据 | 质量驱动 | 同上 |
| T05 | Wikidata | L6 证据边界层 | 验证证据链中关键断言的 Wikidata 实体匹配，补充权威数据证据 | 质量驱动 | 同上 |
| T08 | ConceptNet | 隐含假设挖掘、概念解构阶段 | 获取概念间的语义关联、ISA 层级、能力/用途/因果关系 | 质量驱动 | 记录 exhaust-retry 原因 |

### 5.2 T02 → Wikidata：事实验证

**调用场景**：在 L1 基础事实层收集核心量化指标时，对关键数据（人口、GDP、面积、成立时间、经纬度等）调用 Wikidata 进行交叉验证。

**典型查询类型**：实体属性查询（模板 2.2）

**调用示例**：
1. 识别事实中的实体概念（如"北京" → Q956）
2. 构造属性查询（如人口 P1082）
3. 对比 Wikidata 返回值与 LLM 知识
4. 标注验证结果

**融入方式**：在 L1 事实收集流程中，作为"来源交叉验证"步骤的可选增强环节。详见 [T02 任务模板中的 Wikidata 可选查询步骤](tasks/T02_L1_L2_research.md#wikidata-可选查询步骤)。

### 5.3 T03 → Wikidata：结构数据

**调用场景**：在 L3 结构变量层分析分类体系、层级归属、地理/行政/组织结构时，查询 Wikidata 的类层级和关系数据。

**典型查询类型**：类查询（模板 2.4）、实体间关系查询（模板 2.3）

**调用示例**：
1. 识别结构变量中的分类体系
2. 查询实例所归属的类别层级（P31/P279）
3. 查询实体间的组织/地理归属关系（P17、P131、P361 等）
4. 构建结构化的变量关系矩阵

### 5.4 T05 → Wikidata：证据层

**调用场景**：在 L6 证据边界层核验关键断言时，查询 Wikidata 获取可引用的权威结构化证据。

**典型查询类型**：实体属性查询（模板 2.2）、实体搜索（模板 2.6）

**调用示例**：
1. 提取待验证断言中的核心实体和属性
2. 查询 Wikidata 中对应的结构化记录
3. 将 Wikidata 返回值作为 L0 级证据纳入证据链
4. 标注 `source_category=L0, source=wikidata:{qid}`

### 5.5 T08 → ConceptNet：概念解构

**调用场景**：在子问题分解和隐含假设挖掘过程中，调用 ConceptNet 获取概念的语义关联网络，辅助识别隐藏假设和概念边界。

**典型查询类型**：概念查询（模板 3.3.1）、关系筛选查询（模板 3.3.2）、概念间路径查询（模板 3.3.3）

**调用示例**：
1. 提取子问题中的核心概念（如"人工智能"、"就业"、"不平等"）
2. 查询概念的 IsA 层级（确认概念边界）
3. 查询概念的 CapableOf / Causes / UsedFor 关联（发现潜在假设）
4. 查询两个概念间的路径（发现隐藏的中间概念）
5. 将发现的关联关系纳入 `implicit_assumptions` 分析

**融入方式**：在概念解构阶段，作为"隐含假设挖掘"的可选增强环节。详见 [T08 任务模板中的 ConceptNet 可选查询步骤](tasks/T08_cog_deconstruct.md#conceptnet-可选查询步骤)。

---

## 6. 跨 KG 协同策略

### 6.1 组合使用场景

| 场景 | Wikidata 角色 | ConceptNet 角色 |
|------|-------------|----------------|
| 概念+事实验证 | 验证概念的量化属性与客观数据 | 验证概念的语义边界与常识关联 |
| 实体-概念映射 | 提供实体的结构化属性 | 提供实体的常识性语义关联 |
| 反事实分析 | 提供事实基准数据 | 提供"如果概念关联改变"的语义路径 |

### 6.2 结果整合规范

当同一问题同时使用 Wikidata 和 ConceptNet 时：
1. Wikidata 结果优先用于**事实性结论**（量化数据、客观属性）
2. ConceptNet 结果优先用于**概念性分析**（语义关联、隐含假设、概念边界）
3. 两者冲突时：Wikidata 代表结构化共识知识，ConceptNet 代表常识认知模式——分别记录，不做调和

---

## 7. 通用穷尽尝试协议

所有节点在 KG 查询失败或不可用时，遵循统一的穷尽尝试协议：

```
KG 查询 → 成功 → 使用 KG 结果，标注 source_category=L0, source={kg}:{identifier}
       → 失败 → 使用 LLM 自有知识，标注 source_category=L3, source=llm_knowledge, exhaust_retry_reason={reason}, confidence_penalty=-0.2
```

穷尽尝试标注格式（事实条目中追加的元数据）：

```json
{
  "fact": "...",
  "source_category": "L3",
  "source": "llm_knowledge",
  "exhaust_retry_reason": "wikidata_timeout",
  "confidence_penalty": -0.2,
  "kg_query_attempted": true
}
```

### 穷尽尝试原因枚举

| 穷尽尝试原因 | 含义 |
|---------|------|
| `wikidata_timeout` | Wikidata SPARQL 查询超时 |
| `wikidata_http_{code}` | Wikidata 返回非 2xx 状态码 |
| `entity_not_found_in_wikidata` | 实体在 Wikidata 中无匹配 |
| `no_sparql_results` | SPARQL 查询返回空结果 |
| `conceptnet_timeout` | ConceptNet API 查询超时 |
| `conceptnet_http_{code}` | ConceptNet 返回非 2xx 状态码 |
| `no_conceptnet_match` | ConceptNet 中无匹配概念 |
|- `kg_exhaust_retry` | KG 查询穷尽重试直至质量达标

---
## 8. 顶层本体对齐（v3 新增）

### 8.1 BFO + SUMO 统一概念分类框架

> **能力卡**: TC-091 BFO-SUMO

**方法论原理**：顶层本体对齐是跨知识库语义互操作的基础。BFO 2.0提供现实论分类体系（持续体/事件/空间区域/时间区域），SUMO提供上位分类映射。对齐过程需要处理粒度差异、范畴冲突、多继承矛盾三类核心问题。

在 TM07 构建 OWL 本体时，引入 BFO（Basic Formal Ontology）2.0 和 SUMO（Suggested Upper Merged Ontology）作为顶层本体根节点，统一概念分类框架：

```yaml
bfo_sumo_integration:
  trigger: "TM07 执行本体构建时自动调用"
  purpose: "为本体提供上层分类根节点，确保概念分类的语义一致性和跨领域互操作性"
  bfo_levels:
    continuant: "连续体 — 时间中持续存在的实体（对象、属性、功能等）"
    occurrent: "发生体 — 时间中展开的实体（过程、事件、状态变化等）"
    - "BFO 2.0 核心分类：Entity → Continuant / Occurrent"
    - "Continuant 子类：Independent Continuant（物体、地点）/ Dependent Continuant（属性、功能、角色）"
    - "Occurrent 子类：Process（变化过程）/ Process Boundary（过程边界）/ Temporal Region（时间区域）"
  sumo_mapping:
    - "SUMO 顶层类映射到 BFO：Physical → Independent Continuant, Abstract → Dependent Continuant"
    - "SUMO 的 Process 类映射到 BFO 的 Occurrent"
    - "SUMO 的丰富中层本体（经济、军事、社会等）作为 BFO 下层补充"
  integration_steps:
    - step: "在 TM07 的 OWL Class 层次中，顶层类设为 BFO 核心类（bfo:Entity 为 owl:Thing 的子类）"
    - step: "将现有实体类型映射到 BFO+SUMO 分类体系"
    - step: "标注映射关系：exactMatch（精确对应）/ broadMatch（上位对应）/ narrowMatch（下位对应）"
    - step: "冲突处理：当概念在 BFO 和 SUMO 中分类不一致时，以 BFO 为锚点，SUMO 作为补充"
  exhaust-retry: "当本体构建穷尽重试时（TM07 RETRYING/PARTIAL_C），BFO-SUMO 对齐标记为 skipped"
```

### 8.2 KAG 融合架构参考

> **架构参考**: KAG (蚂蚁集团，Knowledge Augmented Generation) — KG-LLM 深度融合范式
> **仅参考，不注册独立能力卡**

KAG 提出了一种将知识图谱与 LLM 深度融合的范式（而非简单的 RAG 外挂），对本框架的知识图谱集成有重要参考价值：

```yaml
kag_reference:
  paradigm: "KG-LLM 双向增强”
  five_capabilities:
    kg_enhanced_llm: "KG 增强 LLM — 利用知识图谱结构化知识提高 LLM 的事实准确性和逻辑一致性"
    llm_enhanced_kg: "LLM 增强 KG — 利用 LLM 的语义理解能力自动构建、补全和推理知识图谱"
    logical_reasoning: "逻辑推理 — KG 提供符号推理（Datalog/SPARQL），LLM 提供语义推理，两者互补"
    semantic_alignment: "语义对齐 — KG schema 与 LLM 语义空间的相互映射和校准"
    knowledge_evolution: "知识演化 — KG 结构随 LLM 学习而演化，LLM 生成的新知识通过 KG 验证反哺"
  profound_cognition_alignment:
    - "T02 + T21 的知识建构-回收循环 对应 KAG 的 knowledge_evolution"
    - "T08 的 ConceptNet + T05 的 Wikidata 对应 KG 增强 LLM 的事实核查层"
    - "TM07 的 PyKEEN 嵌入 + Datalog（CozoDB）对应 logical_reasoning 的符号推理层"
    - "T13 的 NRSF 合成对应 semantic_alignment 的多层对齐"
  gap_analysis:
    missing: "KAG 的 'LLM 增强 KG'（自动构建/补全知识图谱）能力在本框架中尚未完全实现——T21 是手动回收而非自动构建"
    recommendation: "未来版本可考虑引入 KAG 的自动 KG 构建模块，作为 T21 的增强层"
```

### 8.3 新增能力卡调用声明

| 能力卡 | 调用位置 | 触发条件 | 穷尽重试策略 |
|--------|---------|---------|---------|
| TC-091 BFO-SUMO | TM07 Step 3：本体构建 | TM07 本体构建可用 | 穷尽重试所有可用本体对齐路径，标注 ontology_root='local_only' |

### 8.4 KAG逻辑形式引导检索方法论

> **架构参考**: KAG (Knowledge Augmented Generation) — 逻辑形式引导检索
> **内化目标**: 将KAG的逻辑形式（Logical Form）引导检索机制内化为profound-cognition的知识图谱查询增强策略

#### 8.4.1 核心原理

KAG的核心创新在于：不直接用自然语言查询知识图谱，而是先将自然语言问题转换为逻辑形式（Logical Form），再基于逻辑形式生成精确的图谱查询。这种方法避免了自然语言查询的歧义性，提高了检索的精确度和召回率。

**逻辑形式的定义**: 逻辑形式是对自然语言问题的形式化表示，包含实体引用、关系谓词和约束条件。例如：
- 自然语言: "北京的人口是多少？"
- 逻辑形式: `Query(Population, Entity=Beijing, Time=Latest)`
- SPARQL: `SELECT ?pop WHERE { wd:Q956 wdt:P1082 ?pop }`

#### 8.4.2 自然语言→逻辑形式转换步骤

```
Step 1: 实体识别与链接
  - 从自然语言问题中识别实体提及
  - 将实体提及链接到知识图谱中的实体ID
  - 输出：{mention: "北京", entity_id: "Q956", confidence: 0.95}

Step 2: 关系谓词识别
  - 从问题中识别关系谓词（属性/关系类型）
  - 将关系谓词映射到知识图谱的属性/关系ID
  - 输出：{predicate: "人口", property_id: "P1082", confidence: 0.90}

Step 3: 约束条件提取
  - 提取问题中的时间约束、空间约束、数量约束等
  - 输出：{constraint_type: "time", constraint_value: "latest"}

Step 4: 逻辑形式组装
  - 将实体、谓词、约束组装为逻辑形式
  - 输出：LogicalForm = Query(Predicate, Entity, Constraints)

Step 5: 查询生成
  - 将逻辑形式转换为目标知识图谱的查询语言
  - Wikidata → SPARQL
  - ConceptNet → REST API URL
  - LightRAG → 查询模式 + 参数
```

#### 8.4.3 逻辑形式引导检索规则

| 规则ID | 规则名称 | 规则内容 | 适用场景 |
|--------|---------|---------|---------|
| LF-R01 | 实体消歧优先 | 当实体提及对应多个KG实体时，优先选择与上下文最相关的实体 | 实体链接阶段 |
| LF-R02 | 谓词映射验证 | 逻辑形式中的谓词必须映射到KG中存在的属性/关系——映射失败时穷尽尝试到语义搜索 | 谓词识别阶段 |
| LF-R03 | 约束传播 | 逻辑形式中的约束条件必须传播到生成的查询中——不允许丢失约束 | 查询生成阶段 |
| LF-R04 | 多跳推理分解 | 当问题需要多跳推理时，将逻辑形式分解为多个单跳子查询，按依赖序执行 | 复杂问题 |
| LF-R05 | 结果验证 | 查询结果必须与逻辑形式的预期结构匹配——不匹配时标注异常 | 结果解析阶段 |

#### 8.4.4 与profound-cognition的集成

| 集成点 | 操作 | 效果 |
|--------|------|------|
| T02 事实验证 | 将待验证事实转换为逻辑形式，生成精确SPARQL查询 | 提高Wikidata查询的精确度 |
| T03 结构分析 | 将结构变量问题转换为逻辑形式，查询类层级和关系 | 提高结构数据的完整性 |
| T05 证据收集 | 将证据断言转换为逻辑形式，验证断言的事实基础 | 提高证据验证的可靠性 |
| T08 概念解构 | 将概念问题转换为逻辑形式，查询语义关联网络 | 提高概念分析的深度 |

### 8.5 知识图谱对齐策略

> **内化目标**: 建立profound-cognition三层知识图谱（LightRAG/Wikidata/ConceptNet）之间的语义对齐机制

#### 8.5.1 跨图谱实体对齐

```
对齐流程:

Step 1: 实体共指识别
  - 在不同KG中识别指向同一现实实体的不同标识
  - 方法：标签匹配 + 属性相似度 + 关系结构相似度
  - 输出：对齐候选对 {(LightRAG_entity, Wikidata_QID, ConceptNet_node), confidence}

Step 2: 对齐验证
  - 对每个候选对齐，验证属性一致性
  - 验证方法：比较核心属性值（名称、类型、关键属性）
  - 一致性阈值：属性匹配率 ≥ 0.7 → 确认对齐

Step 3: 对齐存储
  - 将确认的对齐关系存储为等价断言
  - 格式：owl:sameAs / skos:exactMatch / skos:closeMatch
  - 存储位置：LightRAG索引中的对齐表

Step 4: 对齐使用
  - 查询任一KG时，自动检查对齐表
  - 如果对齐实体在其他KG中有更完整的信息 → 自动补充查询
```

#### 8.5.2 跨图谱Schema对齐

| 对齐维度 | LightRAG | Wikidata | ConceptNet | 对齐方法 |
|----------|----------|----------|------------|---------|
| **实体类型** | 自由文本标签 | P31(instance of) + Q-ID | /c/{lang}/{concept} | 标签匹配 + 语义相似度 |
| **关系类型** | 自由文本关系 | P-{property_id} | /r/{relation_type} | 关系语义映射表 |
| **属性类型** | 自由文本属性 | P-{property_id} | /r/HasProperty | 属性语义映射表 |
| **数值类型** | 自由文本数值 | xsd数据类型 | weight (float) | 数值范围校准 |

#### 8.5.3 Schema对齐映射表

| ConceptNet关系 | Wikidata属性 | 语义对齐类型 | 置信度 |
|---------------|-------------|------------|--------|
| /r/IsA | P31 (instance of) / P279 (subclass of) | exactMatch | 0.95 |
| /r/PartOf | P361 (part of) | exactMatch | 0.90 |
| /r/UsedFor | P366 (use) | broadMatch | 0.75 |
| /r/CapableOf | P3931 / 自定义 | narrowMatch | 0.70 |
| /r/Causes | P828 (cause) | exactMatch | 0.85 |
| /r/HasProperty | PXXX (各类属性) | broadMatch | 0.65 |
| /r/Synonym | 无直接对应 | closeMatch | 0.80 |
| /r/Antonym | 无直接对应 | closeMatch | 0.80 |

#### 8.5.4 穷尽重试策略

| 重试级别 | 条件 | 操作 | 输出质量 |
|----------|------|------|---------|
| **L1 完整对齐** | 三层KG均可访问、对齐表完整 | 执行跨KG实体对齐 + Schema对齐 + 自动补充查询 | 精确实体对齐 + 完整Schema映射 |
| **L2 部分对齐** | 部分KG不可用或对齐表不完整 | 执行可用KG间的对齐 + 标注缺失对齐 | 部分实体对齐 + 缺失标注 |
| **L3 无对齐** | 跨KG对齐完全不可用 | 各KG独立查询 + 结果手动对比 | 独立查询结果 + 手动对比建议 |
| **L4 单KG模式** | 仅一个KG可用 | 使用单一KG查询 + 标注KG局限性 | 单KG结果 + 局限性声明 |

### 8.6 KG-LLM深度融合架构设计参考

> **架构参考**: KAG的KG-LLM双向增强范式
> **内化目标**: 为profound-cognition设计KG与LLM深度融合的架构参考

#### 8.6.1 五层融合架构

```
Layer 1: KG增强LLM（检索增强）
  - KG结构化知识 → LLM事实准确性提升
  - 实现：逻辑形式引导检索 → KG查询结果注入LLM上下文
  - profound-cognition对应：T02/T03/T05的KG查询增强

Layer 2: LLM增强KG（自动构建）
  - LLM语义理解 → KG自动构建/补全
  - 实现：LLM提取实体关系 → 验证后写入KG
  - profound-cognition对应：T21知识回收（当前为手动，未来可自动化）

Layer 3: 符号-神经混合推理
  - KG符号推理（SPARQL/Datalog）+ LLM语义推理
  - 实现：KG处理确定性推理，LLM处理模糊/创造性推理
  - profound-cognition对应：TM07的PyKEEN嵌入 + Datalog推理

Layer 4: 语义对齐层
  - KG Schema ↔ LLM语义空间的双向映射
  - 实现：实体对齐 + Schema映射 + 概念空间校准
  - profound-cognition对应：8.5节的对齐策略

Layer 5: 知识演化层
  - KG结构随LLM学习而演化，LLM新知识通过KG验证反哺
  - 实现：增量KG更新 + LLM知识验证循环
  - profound-cognition对应：T02→T21的知识建构-回收循环
```

#### 8.6.2 融合架构穷尽重试策略

| 重试级别 | 条件 | 操作 | 输出质量 |
|----------|------|------|---------|
| **L1 五层完整** | KG和LLM均完全可用 | 执行完整的五层融合推理 | 符号-神经混合推理 + 知识演化 |
| **L2 三层融合** | Layer 2/5不可用（自动构建/演化受限） | 执行Layer 1/3/4（检索增强+混合推理+对齐） | 检索增强推理 + 语义对齐 |
| **L1 仅检索增强** | 仅Layer 1可用 | KG查询结果注入LLM上下文 | 增强的LLM推理 |
| **L4 纯LLM** | KG完全不可用 | 穷尽重试纯LLM推理所有可用路径 + 标注KG缺失 | LLM推理 + 知识局限声明 |
### TC-011 LightRAG 轻量RAG检索方法论

**核心步骤**：
1. 文档索引：通过 LightRAG.index() 将文档集构建为图增强索引
2. 实体抽取：自动抽取文档中的实体和关系
3. 语义查询：通过 LightRAG.query() 执行语义检索，top_k 默认5
4. 结果排序：按语义相似度和图结构相关性排序返回结果

**决策规则**：中小规模文档集（<1000篇）优先使用LightRAG；大规模文档集使用LightRAG-MCP分布式版

**穷尽重试策略**：LightRAG → 向量检索(ChromaDB) → 关键词搜索

> 知识来源: TC-011 LightRAG


### TC-047 LightRAG-MCP MCP分布式RAG方法论

**核心步骤**：
1. MCP连接：通过MCP协议连接LightRAG服务
2. 批量索引：支持大规模文档集的分布式索引构建
3. 并行查询：支持多查询并行执行
4. 增量更新：支持文档集的增量索引更新

**决策规则**：MCP环境+大规模文档集使用LightRAG-MCP；小规模使用LightRAG本地版

**穷尽重试策略**：LightRAG-MCP → LightRAG本地 → 向量检索 → 关键词搜索

> 知识来源: TC-047 LightRAG-MCP


### TC-067 OWLAPY OWL本体构建方法论

**核心步骤**：
1. 类层次定义：使用OWLClass和IRI定义本体类层次结构
2. 属性定义：定义对象属性(OWLObjectProperty)和数据属性(OWLDataProperty)
3. 约束表达：使用OWL 2 DL表达式定义类约束（等价类、子类、不相交类）
4. 推理执行：使用OWL推理器进行一致性检查和隐含知识推导
5. 本体序列化：将本体导出为OWL/XML或Turtle格式

**决策规则**：需要OWL本体构建和DL推理时使用OWLAPY；简单schema使用JSON Schema

**穷尽重试策略**：OWLAPY → JSON Schema简化本体 → 手动类层次定义

> 知识来源: TC-067 OWLAPY


### TC-068 SSSOM 语义映射标准方法论

**核心步骤**：
1. 映射集加载：使用load_mapping_set加载SSSOM格式的映射文件
2. 映射验证：验证映射的语义正确性（skos:exactMatch/closeMatch/broadMatch/narrowMatch）
3. 映射合并：合并来自不同源的映射集，处理冲突映射
4. 置信度评估：评估每条映射的置信度和证据来源
5. 映射推理：基于映射集进行跨本体推理

**决策规则**：需要本体间语义映射和跨本体对齐时使用SSSOM；简单映射使用手动映射表

**穷尽重试策略**：SSSOM → 手动映射表(TSV) → 纯文本映射描述

> 知识来源: TC-068 SSSOM


### TC-069 PyKEEN 知识图谱嵌入方法论

**核心步骤**：
1. 数据集准备：将知识图谱三元组转换为PyKEEN兼容格式
2. 模型选择：选择嵌入模型（TransE/RotatE/ComplEx/DistMult/ConvE等）
3. 训练配置：设置训练超参数（epochs、学习率、嵌入维度、负采样策略）
4. 模型训练：执行pipeline训练，自动处理数据划分和评估
5. 链接预测：使用训练好的模型预测缺失的三元组
6. 实体对齐：利用嵌入空间进行跨图谱实体对齐

**决策规则**：需要知识图谱嵌入和链接预测时使用PyKEEN；简单关系推理使用OWLAPY

**穷尽重试策略**：PyKEEN → 基于规则的链接预测 → 手动关系推断

> 知识来源: TC-069 PyKEEN
