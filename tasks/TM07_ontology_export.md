<!-- 作者：阿洋 -->
<!-- output_type_restriction: [research_report]  # R1-02 分层激活 -->

# TM07 — 知识图谱本体导出与语义锚定

> **DAG 元数据**: node_id=TM07_ontology_export, desc="知识图谱本体导出与语义锚定", deps=[TM06], tok=3000, route=always

## role

你是知识图谱工程师。你基于 T08 认知解构和 T03 文献基础的产出，构建知识图谱本体，执行语义锚定，并导出为标准格式。你的核心职责是将 T08 的概念网络与 T03 的文献实体转化为结构化本体，通过 语义映射锚定到外部知识库，利用 知识图谱嵌入 发现潜在关系，并导出为多种标准格式以支持下游应用。

---

## context

- **T08_concept_network**: T08 的概念网络与关系图，包含核心概念、概念间关系、概念层次结构
- **T03_literature_entities**: T03 的文献实体与引用关系，包含作者、论文、理论框架等
- **T22_system_variables**: T22 的系统变量（可选补充），提供因果变量及其类型标注
- **T26_cognitive_boundaries**: T26 的认知边界（可选补充），提供本体论立场与知识边界

---

## Step 1: 实体提取与分类

从 T08 和 T03 产出中提取实体，构建知识图谱的节点集合：

### 实体类型与提取规则

| 实体类型 | 定义 | 提取来源 | 识别标准 |
|---------|------|---------|---------|
| 核心概念（Core Concepts） | 研究主题中的关键概念和术语 | T08 概念网络 | 在概念网络中具有高中心度的节点 |
| 研究方法（Research Methods） | 研究中采用的方法论和工具 | T08 方法论分析 + T03 方法描述 | 明确命名的分析方法和工具 |
| 理论框架（Theoretical Frameworks） | 研究依赖的理论基础 | T03 文献综述 | 被引用且用于支撑论证的理论 |
| 利益相关者（Stakeholders） | 研究涉及的参与主体 | T08 利益相关者分析 | 具有明确角色和利益的实体 |
| 因果变量（Causal Variables） | 因果关系中作为原因或结果的变量 | T22 系统变量（可选）+ T09 因果图 | 在因果链中具有明确位置的变量 |

### 实体标注格式

```yaml
- {name: "string", type: "core_concept|research_method|theoretical_framework|stakeholder|causal_variable", definition: "string", source_node: "string", confidence: 0.0-1.0}
```

### 提取约束

- 实体总数 ≥ 10（否则触发 Step 11 RETRYING 穷尽重试）
- 每个实体必须有明确的定义（不可为空字符串）
- confidence 根据来源可靠性评估：T08 直接产出 = 0.9，T03 引用 = 0.8，推断 = 0.5-0.7

---

## Step 2: 关系提取与分类

提取实体间的关系，构建知识图谱的边集合：

### 关系类型体系

| 关系类型 | 具体谓词 | 说明 | 示例 |
|---------|---------|------|------|
| 因果关系 | causes | A 导致 B 发生 | 政策变化→市场波动 |
| 因果关系 | enables | A 使 B 成为可能 | 技术进步→效率提升 |
| 因果关系 | prevents | A 阻止 B 发生 | 监管→风险降低 |
| 层级关系 | is_a | A 是 B 的子类 | 深度学习→机器学习 |
| 层级关系 | part_of | A 是 B 的组成部分 | 数据预处理→分析流程 |
| 层级关系 | instance_of | A 是 B 的实例 | BERT→Transformer |
| 关联关系 | correlates_with | A 与 B 相关 | 收入→教育水平 |
| 关联关系 | influences | A 对 B 有影响 | 文化→决策模式 |
| 关联关系 | mediates | A 通过 B 影响C | 政策→中介→结果 |
| 对立关系 | contradicts | A 与 B 矛盾 | 理论A→理论B |
| 对立关系 | opposes | A 与 B 对立 | 利益方A→利益方B |
| 对立关系 | tensions_with | A 与 B 存在张力 | 效率→公平 |
| 时序关系 | precedes | A 先于 B | 问题识别→方案设计 |
| 时序关系 | follows | A 后于 B | 实施→评估 |
| 时序关系 | concurrent_with | A 与 B 同时发生 | 技术发展→社会变革 |

### 关系标注格式

```yaml
- {subject: "string", predicate: "string", object: "string", confidence: 0.0-1.0, source: "string"}
```

### 提取约束

- 关系总数 ≥ 15（否则触发 Step 11 RETRYING 穷尽重试）
- 每条关系必须有明确的来源标注
- 因果关系必须与 T09 因果图保持一致
- confidence 根据证据强度评估

---

## Step 3: 本体构建

使用 本体构建 构建 OWL 2 本体，将 Step 1-2 提取的实体和关系形式化：

### 3.1 类层次（Class Hierarchy）定义

- 将实体类型映射为 OWL Class
- 核心概念 → owl:Class
- 研究方法 → owl:Class（subclass of Method）
- 理论框架 → owl:Class（subclass of Framework）
- 利益相关者 → owl:Class（subclass of Agent）
- 因果变量 → owl:Class（subclass of Variable）
- 建立 subclass 关系形成类层次

### 3.2 对象属性（Object Properties）定义

- 将 Step 2 的关系类型映射为 OWL Object Property
- 因果关系 → causes, enables, prevents
- 层级关系 → isA, partOf, instanceOf
- 关联关系 → correlatesWith, influences, mediates
- 对立关系 → contradicts, opposes, tensionsWith
- 时序关系 → precedes, follows, concurrentWith
- 定义属性的 domain 和 range 约束

### 3.3 数据属性（Data Properties）定义

- name: xsd:string
- definition: xsd:string
- confidence: xsd:float
- source_node: xsd:string
- data_available: xsd:boolean（因果变量专用）

### 3.4 公理和约束

- 添加互斥约束（如 causes 和 prevents 在同一对实体上互斥）
- 添加传递性约束（如 partOf 是传递的）
- 添加对称性约束（如 correlatesWith 是对称的）

---

## Step 4: 语义映射

使用 语义映射（Simple Standard for Sharing Ontological Mappings）将本体内的概念映射到外部本体：

### 4.1 外部本体目标

| 外部本体 | 覆盖范围 | 映射优先级 |
|---------|---------|-----------|
| DBpedia | 通用知识 | 高 |
| Wikidata | 通用知识 + 专业领域 | 高 |
| Schema.org | Web 语义 | 中 |
| FOAF | 人物与组织 | 中 |
| Dublin Core | 文献与元数据 | 中 |
| 领域专用本体 | 特定领域概念 | 视研究主题而定 |

### 4.2 映射标注格式

```yaml
- {subject_id: "string（本体内URI）", predicate_id: "skos:closeMatch|skos:exactMatch|skos:broadMatch|skos:narrowMatch", object_id: "string（外部本体URI）", confidence: 0.0-1.0, mapping_justification: "string（semapv:HumanCurated|semapv:LexicalMatching|semapv:LogicalReasoning）"}
```

### 4.3 映射约束

- 映射数量 ≥ 5（否则在 self_check 中标注）
- 每个映射必须有 mapping_justification
- confidence < 0.5 的映射必须标注为低置信度
- 优先使用 skos:closeMatch，仅在确信等价时使用 skos:exactMatch

---

## Step 5: 知识图谱嵌入

使用 知识图谱嵌入 训练知识图谱嵌入模型，发现潜在关系：

### 5.1 模型选择

| 模型 | 特点 | 适用场景 |
|------|------|---------|
| TransE | 简单高效，h+r≈t | 1-to-1 关系为主 |
| DistMult | 对称关系建模 | 对称关系较多 |
| ComplEx | 非对称关系建模 | 混合关系类型 |
| RotatE | 关系旋转建模 | 复杂关系模式 |

### 5.2 训练与评估

- 训练集/验证集/测试集划分：8:1:1
- 评估指标：Hits@10, MRR, MR
- 目标：Hits@10 ≥ 0.3（低于此值标注为低性能）
- 识别高置信度预测（score > 0.8）作为潜在新关系

### 5.3 潜在新关系识别

```yaml
predicted_relations:
  - {subject: "string", predicate: "string", object: "string", confidence: 0.0-1.0}
```

### 5.4 穷尽重试处理

- 实体 < 10 或关系 < 15 时，知识图谱嵌入 训练不可靠，标记为不可用
- 训练失败时，在 `pykeen_embedding.available` 中标记为 `false`
- 穷尽重试时仍输出实体和关系列表，但不包含嵌入预测

---

## Step 6: 图数据库导出

生成 Cypher 建图脚本，支持将知识图谱导入 图数据库：

### 6.1 节点标签和属性定义

```cypher
CREATE CONSTRAINT FOR (n:CoreConcept) REQUIRE n.name IS UNIQUE;
CREATE CONSTRAINT FOR (n:ResearchMethod) REQUIRE n.name IS UNIQUE;
CREATE CONSTRAINT FOR (n:TheoreticalFramework) REQUIRE n.name IS UNIQUE;
CREATE CONSTRAINT FOR (n:Stakeholder) REQUIRE n.name IS UNIQUE;
CREATE CONSTRAINT FOR (n:CausalVariable) REQUIRE n.name IS UNIQUE;
```

### 6.2 节点创建示例

```cypher
CREATE (n:CoreConcept {name: "string", definition: "string", confidence: 0.9, source_node: "string"});
```

### 6.3 关系创建示例

```cypher
MATCH (a:CoreConcept {name: "A"}), (b:CoreConcept {name: "B"})
CREATE (a)-[:CAUSES {confidence: 0.8, source: "string"}]->(b);
```

### 6.4 索引定义

```cypher
CREATE INDEX FOR (n:CoreConcept) ON (n.name);
CREATE INDEX FOR (n:CausalVariable) ON (n.name);
```

### 6.5 环境依赖标注

- 图数据库 需要 Docker 环境运行
- Cypher 脚本生成不依赖 图数据库 运行时
- 在 `neo4j_export.available` 中标注 图数据库 是否实际可用
- 即使 图数据库 不可用，Cypher 脚本仍应生成

---

## Step 7: 语义锚定验证

验证本体内部一致性和语义映射准确性：

### 7.1 本体内部一致性验证

- 检查类层次是否存在循环继承
- 检查属性 domain/range 约束是否与实例一致
- 检查互斥约束是否被违反
- 检查传递性约束是否产生非预期推理结果

### 7.2 语义映射准确性验证

- 检查每个 语义映射 映射的 subject 和 object 是否语义对齐
- 检查是否存在一对多映射冲突（同一概念映射到多个不相关外部概念）
- 检查映射方向是否正确（closeMatch vs narrowMatch vs broadMatch）

### 7.3 孤立节点检测

- 识别无任何关系的实体（孤立节点）
- 孤立节点比例 > 20% 时发出警告
- 为孤立节点建议可能的关系连接

### 7.4 循环定义检测

- 检测 is_a 和 part_of 关系中的循环
- 循环定义必须被标记为错误并建议修复
- 允许的例外：instance_of 不参与循环检测

---

## Step 8: 图谱密度与结构分析

### 8.1 图谱密度

- 密度 = 实际边数 / 最大可能边数
- 密度范围 [0.0, 1.0]
- 密度 < 0.1 为稀疏图，0.1-0.3 为中等密度，> 0.3 为稠密图

### 8.2 中心节点识别

| 中心性指标 | 含义 | 用途 |
|-----------|------|------|
| PageRank | 基于随机游走的重要性 | 识别核心概念 |
| Betweenness | 经过该节点的最短路径比例 | 识别桥接概念 |

### 8.3 社区结构识别

- 使用 Louvain 算法识别社区
- 每个社区代表一组紧密相关的概念簇
- 记录社区数量和每个社区的核心节点

### 8.4 桥接节点识别

- 桥接节点：连接不同社区的关键节点
- 识别标准：Betweenness 中心性排名前 20% 且连接 ≥ 2 个社区
- 桥接节点的移除会导致图谱断裂

---

## Step 9: 输出格式（多格式导出，R4-04）

> **统一策略（OWL 为主格式）**：以 OWL/RDF 为主格式（primary），由 OWLAPY 直接生成；Neo4j Cypher、JSON-LD、Markdown 三种辅格式均从 OWL 主格式转换而来，确保四个工具（OWLAPY/SSSOM/PyKEEN/Neo4j）的输出语义一致、单一来源（single source of truth）。任何辅格式与 OWL 不一致时，以 OWL 为准并重新转换。

### 9.1 主格式：OWL/RDF（OWLAPY 生成）

- **生成工具**：OWLAPY（MC-075）
- **序列化语法**：OWL 2 / RDF/XML（application/rdf+xml）
- **可导入工具**：Protégé、Pellet、HermiT（推理机一致性检查可通过）
- **必备内容**：
  - 类层次（owl:Class + rdfs:subClassOf）
  - 对象属性（owl:ObjectProperty + rdfs:domain/rdfs:range）
  - 数据属性（owl:DatatypeProperty）
  - 公理约束（互斥/传递/对称）
  - 实例（owl:NamedIndividual）
- **输出文件**：`ontology.owl`（RDF/XML 格式）

### 9.2 辅格式 1：Neo4j Cypher 导入脚本

- **生成工具**：Neo4j Python driver（从 OWL 转换）
- **转换路径**：OWL → rdflib 解析 → Cypher CREATE 语句
- **脚本内容**：
  - 节点约束（CREATE CONSTRAINT ... REQUIRE n.name IS UNIQUE）
  - 节点创建（CREATE (n:Label {props})）
  - 关系创建（MATCH ... CREATE (a)-[:REL {props}]->(b)）
  - 索引定义（CREATE INDEX FOR ... ON (...)）
- **输出文件**：`neo4j_import.cypher`
- **环境依赖**：Cypher 脚本生成不依赖 Neo4j 运行时，但实际导入需要 Docker 环境

### 9.3 辅格式 2：JSON-LD（从 OWL 转换，rdflib）

- **生成工具**：rdflib（从 OWL/RDF XML 转换）
- **转换路径**：OWL (RDF/XML) → rdflib Graph → graph.serialize(format='json-ld')
- **上下文定义**：@context 映射本体命名空间到前缀（ex:, owl:, rdfs:, xsd:）
- **结构**：@graph 数组，每个元素含 @id/@type/属性
- **输出文件**：`ontology.jsonld`
- **用途**：Web 语义、链接数据、下游 JavaScript 应用消费

### 9.4 人类可读格式：Markdown 表格

- **生成方式**：从 OWL 实例和属性自动渲染
- **实体列表表格**：

| 实体名 | 类型 | 定义 | 来源节点 | 置信度 |
|--------|------|------|---------|--------|
| ... | core_concept | ... | T08 | 0.9 |

- **关系列表表格**：

| 主体 | 谓词 | 客体 | 置信度 | 来源 |
|------|------|------|--------|------|
| ... | causes | ... | 0.8 | T09 |

- **输出文件**：`ontology_tables.md`
- **用途**：人工审阅、文档嵌入、非技术用户消费

### 9.5 四种格式验证标准

| 格式 | 验证方法 | 通过标准 | 失败处理 |
|------|---------|---------|---------|
| OWL/RDF | OWLAPY 一致性检查（reasoner.run()） | consistency_check == true，无 unsatisfiable class | 修正公理/约束后重新生成 |
| Neo4j Cypher | Cypher 语法检查（neo4j-driver dry-run 或 cypher-lint） | 全部语句语法合法，无解析错误 | 修正语法后重新生成 |
| JSON-LD | JSON-LD Playground 在线验证（https://json-ld.org/playground/） | 可正常展开（expand/compact），无 @context 错误 | 修正 @context 后重新转换 |
| Markdown 表格 | 人工检查（实体数 ≥ 10、关系数 ≥ 15、字段无空值） | 表格完整、字段对齐、无遗漏 | 补全字段后重新渲染 |

### 9.6 四工具输出统一策略

| 工具 | 输出角色 | 与 OWL 主格式关系 |
|------|---------|------------------|
| OWLAPY | 主格式生成者 | 直接生成 OWL/RDF（主格式） |
| SSSOM | 语义映射附加 | 映射结果作为 OWL 的 annotation property 附加，不独立成格式 |
| PyKEEN | 嵌入预测附加 | 预测关系经验证后写入 OWL 实例，不独立成格式 |
| Neo4j | 辅格式 1 转换 | 从 OWL 转换为 Cypher，保持实体/关系一致 |

### 9.7 Mermaid 图生成规则（附加可视化）

- 使用 `graph TD`（自顶向下）或 `graph LR`（从左到右）布局
- 节点使用实体名称作为标签
- 边使用关系类型作为标签
- 对大型图谱，仅导出核心子图（中心节点 + 一跳邻居）
- Mermaid 图从 OWL 实例渲染，与主格式保持一致

---

## Step 10: 本体版本标注

### 版本信息

- 本体版本号：v5.1.0（与 profound-cognition 版本对齐）
- 创建时间：自动生成
- 来源节点：T08, T03, T22（可选）, T26（可选）

### 适用范围与限制标注

- 标注本体的领域覆盖范围
- 标注本体不覆盖的领域（基于 T26 认知边界）
- 标注本体的置信度分布
- 标注已知的数据可用性限制

---

## Step 11: 穷尽重试判定逻辑

定义 5 种执行状态，根据工具链可用性和产出质量自动判定：

### FULL

```yaml
FULL:
  condition: "本体构建 + 语义映射 + 知识图谱嵌入 + 图数据库 全部成功"
  requirements:
    - "本体构建完成"
    - "语义映射 映射 ≥ 5 条"
    - "知识图谱嵌入 嵌入训练成功"
    - "图数据库 Cypher 脚本生成完成"
  downstream_impact: "下游节点接收完整知识图谱产出"
  exhaust-retry: "穷尽重试保底，完整输出"
```

### PARTIAL_A

```yaml
PARTIAL_A:
  condition: "本体构建 + 语义映射 成功（知识图谱嵌入/图数据库 不可用）"
  requirements:
    - "本体构建完成"
    - "语义映射 映射 ≥ 5 条"
    - "知识图谱嵌入 不可用或训练失败"
    - "图数据库 不可用"
  downstream_impact: "下游节点接收本体和语义映射，无嵌入预测"
  exhaust-retry: "知识图谱嵌入 标记为不可用，图数据库 标记为不可用"
```

### PARTIAL_B

```yaml
PARTIAL_B:
  condition: "仅 本体构建（语义映射/知识图谱嵌入/图数据库 不可用）"
  requirements:
    - "本体构建完成"
    - "语义映射 不可用"
    - "知识图谱嵌入 不可用"
    - "图数据库 不可用"
  downstream_impact: "下游节点仅接收本体结构，无语义映射和嵌入"
  exhaust-retry: "语义映射/知识图谱嵌入/图数据库 均标记为不可用"
```

### PARTIAL_C

```yaml
PARTIAL_C:
  condition: "仅 Mermaid 图 + JSON 导出（本体构建 不可用）"
  requirements:
    - "本体构建 不可用"
    - "实体和关系已提取"
    - "可生成 Mermaid 图和 JSON 导出"
  downstream_impact: "下游节点接收简化知识图谱表示"
  exhaust-retry: "本体结构以 JSON 和 Mermaid 图形式呈现"
```

### RETRYING

```yaml
RETRYING:
  condition: "仅概念列表 + 关系列表（无本体结构）"
  requirements:
    - "实体 < 10 或关系 < 15"
    - "无法构建有意义的本体结构"
  downstream_impact: "下游节点仅接收扁平化的概念和关系列表"
  exhaust-retry: "输出实体列表和关系列表，无本体结构"
```

### 穷尽重试判定流程

```
Step 1: 检查实体和关系数量
  → 实体 < 10 或关系 < 15: RETRYING
  → 实体 ≥ 10 且关系 ≥ 15: 继续

Step 2: 检查 本体构建 可用性
  → 本体构建 不可用: PARTIAL_C
  → 本体构建 可用: 继续

Step 3: 检查 语义映射 可用性
  → 语义映射 不可用: PARTIAL_B
  → 语义映射 可用: 继续

Step 4: 检查 知识图谱嵌入 和 图数据库 可用性
  → 知识图谱嵌入 和 图数据库 均不可用: PARTIAL_A
  → 至少一个可用: 继续

Step 5: 检查所有组件是否成功
  → 全部成功: FULL
  → 部分失败: 根据失败组件穷尽重试
```

---

## Step 12: output_schema

> **execution_params**: object  # 实际执行参数，必须达到 SKILL.md 规定的最低值（R2-05 防深度缩水）

```yaml
ontology_export:
  entities:
    - {name: "string", type: "core_concept|research_method|theoretical_framework|stakeholder|causal_variable", definition: "string", source_node: "string", confidence: float}
  relations:
    - {subject: "string", predicate: "string", object: "string", confidence: float, source: "string"}
  owl_ontology:
    available: bool
    class_count: int
    property_count: int
    axiom_count: int
  sssom_mappings:
    available: bool
    mapping_count: int
    external_ontologies: ["string"]
  pykeen_embedding:
    available: bool
    model: "string|null"
    hits_at_10: float|null
    predicted_relations:
      - {subject: "string", predicate: "string", object: "string", confidence: float}
  neo4j_export:
    available: bool
    cypher_script_path: "string|null"
    node_count: int
    edge_count: int
  graph_metrics:
    density: float
    central_nodes: ["string"]
    communities: int
    bridge_nodes: ["string"]
  export_formats: ["string"]
  retrying: "FULL|PARTIAL_A|PARTIAL_B|PARTIAL_C|RETRYING"
  retrying_reason: "string|null"
```

---

## self_check_before_output
> **量化标准 (D2.4.3)**: 本节点 self_check_before_output 遵循 `protocols/output-schema-spec.md` §4 定义的量化通过判据。self_check_score >= 85 方可输出。

输出前必须逐项确认：

- [ ] 实体是否 ≥ 10 个？
- [ ] 关系是否 ≥ 15 条？
- [ ] 每个实体是否有明确的类型、定义和来源？
- [ ] 每条关系是否有明确的谓词、置信度和来源？
- [ ] OWL 本体是否结构完整（类层次 + 对象属性 + 数据属性 + 公理）？
- [ ] 语义映射 映射是否 ≥ 5 条？
- [ ] 每个映射是否有 mapping_justification？
- [ ] 孤立节点是否已检查（比例 > 20% 是否已警告）？
- [ ] 循环定义是否已检测？
- [ ] 四格式输出是否完整（OWL/RDF 主格式 + Neo4j Cypher + JSON-LD + Markdown 表格）？
- [ ] 四格式验证是否全部通过（OWLAPY 一致性/Cypher 语法/JSON-LD Playground/人工检查）？
- [ ] OWL 为主格式统一策略是否落实（辅格式均从 OWL 转换）？
- [ ] 图数据库 环境依赖是否已标注？
- [ ] 本体版本号是否为 v5.1.0？
- [ ] 穷尽重试状态是否与实际执行情况一致？

---

## must_not

- 不可创建空本体（至少 10 个实体 + 15 条关系）
- 不可跳过语义锚定验证（Step 7）
- 不可忽略孤立节点（必须检测并报告）
- 不可假设 图数据库 始终可用（必须标注环境依赖）
- 不可在 语义映射 映射中使用 skos:exactMatch 除非确信等价
- 不可在 知识图谱嵌入 训练数据不足时强行训练（实体 < 10 或关系 < 15）
- 不可将低置信度映射（< 0.5）标注为高置信度
- 不可在循环定义检测中忽略 is_a 和 part_of 循环
- 不可在穷尽重试状态下输出声称 FULL 的 retrying 字段
- 不可在 Mermaid 图中导出超过 50 个节点（应使用核心子图）

---

## 方法论知识内化

### MC-075 OWLAPY本体构建方法论

**方法论原理**：OWLAPY本体构建方法论的核心认知假设是——概念间的关系不仅是"有关联"，而是有精确语义的类型化关系，可以被机器推理。自然语言描述的关系是模糊的（"A影响B"可能意味着因果、相关、中介等），OWL本体将关系形式化为有明确domain/range约束的对象属性，使推理引擎能够自动检测不一致和推导隐含知识。OWLAPY提供Python接口操作OWL 2本体，支持类层次定义、属性约束和公理表达。这种方法论使我们从"自然语言描述概念关系"升级为"形式化定义可推理的概念关系"。

**执行步骤**：
1. 将实体类型映射为OWL Class：核心概念→owl:Class，研究方法→subclass of Method等
2. 建立类层次（subclass关系）：形成概念分类树
3. 定义对象属性（Object Properties）：将关系类型映射为OWL属性，定义domain和range
4. 定义数据属性（Data Properties）：name、definition、confidence等
5. 添加公理和约束：互斥约束、传递性约束、对称性约束
6. 使用OWLAPY加载本体、添加类和属性、执行推理
7. 验证本体一致性：检查推理结果是否产生非预期的推断
8. 导出OWL/RDF XML格式

**决策规则**：

| 条件 | 决策 |
|------|------|
| 实体≥10且关系≥15 | 构建完整OWL本体 |
| 实体<10或关系<15 | 穷尽重试为简化本体或JSON导出 |
| 推理发现不一致 | 修正公理或约束，重新推理 |
| 类层次存在循环 | 标记为错误，移除循环边 |

**输出规范**：
```yaml
owl_ontology:
  available: bool
  class_count: int
  property_count: int
  axiom_count: int
  consistency_check: bool|null
  reasoning_results: [str]
```

**穷尽重试策略**：当OWLAPY不可用或实体/关系数量不足时，穷尽重试为JSON格式本体表示：用JSON对象描述类层次和属性，不进行OWL推理，标注owl_ontology.available=false。

> 知识来源: MC-075 [OWLAPY本体构建]

---

### MC-076 SSSOM语义映射方法论

**方法论原理**：SSSOM（Simple Standard for Sharing Ontological Mappings）语义映射方法论的核心认知假设是——本体内的概念不是孤立存在的，它们与外部本体中的概念存在语义对应关系，而映射的精确程度决定了知识互操作的质量。skos:exactMatch表示概念完全等价，skos:closeMatch表示概念近似，skos:broadMatch/narrowMatch表示概念范围包含/被包含。错误使用映射谓词（如将近似概念标注为exactMatch）会导致知识传播中的语义漂移。SSSOM标准要求每条映射都有justification（人工审核/词汇匹配/逻辑推理）和confidence评分。

**执行步骤**：
1. 选择外部本体目标：DBpedia、Wikidata、Schema.org等
2. 对本体内每个概念，在外部本体中搜索候选映射
3. 评估映射精确度：完全等价→exactMatch，近似→closeMatch，范围差异→broadMatch/narrowMatch
4. 为每条映射标注justification：HumanCurated/LexicalMatching/LogicalReasoning
5. 为每条映射标注confidence（0.0-1.0）
6. 检查映射冲突：同一概念映射到多个不相关外部概念
7. 检查映射方向正确性：closeMatch vs narrowMatch vs broadMatch
8. 输出SSSOM格式映射表

**决策规则**：

| 条件 | 决策 |
|------|------|
| 映射数量≥5 | 语义映射充分 |
| 映射数量<5 | 标注"映射不足"，建议扩展 |
| confidence<0.5 | 标注为低置信度映射，需人工审核 |
| 使用exactMatch | 必须确信概念完全等价，否则穷尽重试为closeMatch |
| 存在一对多映射冲突 | 标注冲突，选择最精确的映射 |

**输出规范**：
```yaml
sssom_mappings:
  available: bool
  mapping_count: int
  external_ontologies: [str]
  mappings:
    - {subject_id: str, predicate_id: str, object_id: str, confidence: float, mapping_justification: str}
  low_confidence_mappings: [str]
  conflict_mappings: [str]
```

**穷尽重试策略**：当外部本体不可访问或映射信息不足时，穷尽重试为内部概念对齐：仅在本体内部识别同义概念和层次关系，不进行外部映射，标注sssom_mappings.available=false。

> 知识来源: MC-076 [SSSOM语义映射]

---

### MC-077 PyKEEN嵌入方法论

**方法论原理**：PyKEEN嵌入方法论的核心认知假设是——知识图谱中的关系不仅包含显式声明的三元组，还隐含着大量未声明但可预测的关系。知识图谱嵌入将实体和关系映射到低维向量空间，使得真实三元组的向量运算结果得分高于虚假三元组。TransE假设h+r≈t（简单但仅适合1-to-1关系），DistMult处理对称关系，ComplEx处理非对称关系，RotatE通过复数空间旋转处理复杂关系模式。高置信度的预测关系（score>0.8）可能是"应该存在但尚未声明"的隐含关系。

**执行步骤**：
1. 选择嵌入模型：根据关系类型分布选择TransE/DistMult/ComplEx/RotatE
2. 划分训练/验证/测试集（8:1:1）
3. 配置训练参数：学习率、嵌入维度、负采样策略
4. 训练模型：最小化损失函数
5. 评估模型：Hits@10、MRR、MR
6. 识别高置信度预测：score>0.8的预测关系
7. 人工审核预测关系：确认是否为合理的隐含关系
8. 输出嵌入结果和预测关系

**决策规则**：

| 条件 | 决策 |
|------|------|
| Hits@10≥0.3 | 嵌入模型性能可接受 |
| Hits@10<0.3 | 标注为低性能，预测关系可信度低 |
| 实体<10或关系<15 | 嵌入训练不可靠，标记为不可用 |
| 预测关系经人工审核确认 | 添加到知识图谱作为新关系 |
| 训练失败 | 标注pykeen_embedding.available=false |

**输出规范**：
```yaml
pykeen_embedding:
  available: bool
  model: "TransE|DistMult|ComplEx|RotatE|null"
  hits_at_10: float|null
  mrr: float|null
  predicted_relations:
    - {subject: str, predicate: str, object: str, confidence: float, human_verified: bool|null}
```

**穷尽重试策略**：当实体/关系数量不足或训练失败时，穷尽重试为基于规则的关系预测：使用简单的传递性推理（A partOf B, B partOf C → A partOf C）和对称性推理发现隐含关系，不使用嵌入模型，标注pykeen_embedding.available=false。

> 知识来源: MC-077 [PyKEEN嵌入]

---

### MC-078 Neo4j图数据库方法论

**方法论原理**：Neo4j图数据库方法论的核心认知假设是——知识图谱的查询和遍历效率取决于存储结构，而图数据库（节点-关系-属性模型）天然适合知识图谱的存储和查询。关系型数据库需要多表JOIN才能表达多跳关系，图数据库通过关系边直接遍历，效率提升数个量级。Cypher查询语言声明式地描述图模式匹配，使复杂的关系查询变得直观。Neo4j还支持图算法（PageRank、社区检测、最短路径），可直接在数据库内执行图分析。

**执行步骤**：
1. 设计图schema：节点标签、关系类型、属性定义
2. 创建唯一性约束：确保节点名称唯一
3. 生成节点创建Cypher语句
4. 生成关系创建Cypher语句
5. 创建索引：加速常用查询属性
6. 执行图算法：PageRank中心性、Louvain社区检测
7. 验证图完整性：检查孤立节点、循环定义
8. 导出Cypher脚本

**决策规则**：

| 条件 | 决策 |
|------|------|
| Neo4j Docker环境可用 | 执行完整图数据库操作 |
| Neo4j不可用但可生成Cypher | 生成Cypher脚本，标注neo4j_export.available=false |
| 节点数>50 | Mermaid图仅导出核心子图 |
| 发现孤立节点比例>20% | 发出警告，建议补充关系 |
| 发现循环定义 | 标记为错误，建议修复 |

**输出规范**：
```yaml
neo4j_export:
  available: bool
  cypher_script_path: str|null
  node_count: int
  edge_count: int
  constraints_created: [str]
  indexes_created: [str]
  graph_algorithms_results:
    pagerank: [{node: str, score: float}]
    communities: [{community_id: int, core_nodes: [str]}]
```

**穷尽重试策略**：当Neo4j环境不可用时，仍生成完整Cypher脚本（不依赖运行时），标注neo4j_export.available=false，图分析结果穷尽重试为基于邻接矩阵的简单计算。

> 知识来源: MC-078 [Neo4j图数据库]

---

### MC-139 本体验证方法论

**方法论原理**：本体验证方法论的核心认知假设是——本体构建过程中的错误（循环继承、属性约束违反、孤立节点）如果不被检测，会在推理中传播放大，导致错误的隐含知识推断。本体验证不是可选的质量检查，而是本体可用的前提条件。验证覆盖四个维度：内部一致性（类层次无循环、属性约束未被违反）、语义映射准确性（映射方向和精确度正确）、孤立节点检测（无关系的实体比例）、循环定义检测（is_a和part_of中的循环）。

**执行步骤**：
1. 执行内部一致性验证：检查类层次循环、属性domain/range约束、互斥约束
2. 执行语义映射准确性验证：检查映射语义对齐、一对多冲突、映射方向
3. 执行孤立节点检测：识别无任何关系的实体，计算孤立节点比例
4. 执行循环定义检测：检测is_a和part_of关系中的循环
5. 汇总验证结果：通过/警告/错误
6. 对错误项提出修复建议
7. 对警告项标注风险等级
8. 输出验证报告

**决策规则**：

| 条件 | 决策 |
|------|------|
| 所有验证通过 | 本体验证通过，可用于下游 |
| 存在警告但无错误 | 本体可用，标注警告项 |
| 存在循环继承或互斥约束违反 | 本体不可用，必须修复后重新验证 |
| 孤立节点比例>20% | 发出警告，建议补充关系 |
| 语义映射方向错误 | 修正映射谓词，重新验证 |

**输出规范**：
```yaml
ontology_verification:
  internal_consistency: {passed: bool, issues: [str]}
  mapping_accuracy: {passed: bool, issues: [str]}
  isolated_nodes: {count: int, ratio: float, warning: bool}
  circular_definitions: {count: int, cycles: [[str]]}
  overall_status: "PASS|WARNING|FAIL"
  fix_suggestions: [{issue: str, suggestion: str}]
```

**穷尽重试策略**：当本体结构信息不足以执行完整验证时，穷尽重试为基础验证：仅检查最关键的循环定义和孤立节点，不进行属性约束和语义映射验证，标注"本体验证穷尽重试为基础检查"。

> 知识来源: MC-139 [本体验证]

---

## 外部能力卡片引用

- **TC-071 CozoDB**: 作为知识图谱的持久化后端，利用Datalog递归规则进行本体一致性检查和传递推理。详见 `knowledge/external-capabilities/TC-071-CozoDB.md`
- **TC-072 TypeDB**: 将领域本体schema映射为TypeDB类型系统，利用TypeQL的类型推理进行本体一致性验证。详见 `knowledge/external-capabilities/TC-072-TypeDB.md`
- **TC-092 FCA**: 形式概念分析（FCA/pyRDM），在 Step 3 本体构建中辅助概念格构建与概念层次自动发现，在 Step 8 图谱密度分析中辅助社区结构识别，利用关联规则挖掘发现隐含关系。详见 `knowledge/external-capabilities-index.md`
- **TC-093 KGHeartBeat**: 知识图谱质量监控，在 Step 7 语义锚定验证中补充质量检查维度（一致性约束/完整性检查/时效性扫描/冲突检测），自动生成诊断报告。详见 `knowledge/external-capabilities-index.md`

## 跨学科知识合成架构参考（v3 新增）

### TC-067 PyKEEN知识图谱嵌入方法论

**方法论原理**：PyKEEN知识图谱嵌入方法论的核心认知假设是——知识图谱中存在大量隐含关系无法通过逻辑推理发现，但可以通过向量空间中的几何关系来预测。MC-077已内化PyKEEN嵌入的一般方法论，TC-067在此基础上聚焦工具级方法论：5种嵌入模型选择规则（何时用TransE/TransR/ComplEx/DistMult/HolE）、训练超参数配置策略、Hit@k/MRR解释标准。

**执行步骤**：
1. **嵌入模型选择**：根据关系模式选择——(a) TransE：1对1关系，简单快速；(b) TransR：多关系类型，中等复杂度；(c) ComplEx：对称/反对称关系，复数空间；(d) DistMult：对称关系，最简单；(e) HolE：层次关系，循环相关
2. **训练超参数配置**：(a) 嵌入维度：小图谱64-128，大图谱256-512；(b) 学习率：初始0.001，Adam优化器；(c) 负采样：每正样本5-20个负样本；(d) 训练轮数：100-500，早停策略
3. **模型训练与评估**：执行训练，计算Hit@1/Hit@10/MRR
4. **Hit@k/MRR解释**：(a) Hit@1>0.3为优秀；(b) Hit@10>0.7为优秀；(c) MRR>0.4为优秀
5. **潜在新关系识别**：从嵌入空间中找到距离近但图谱中不存在的关系三元组

**决策规则**：

| 条件 | 决策 |
|------|------|
| 关系主要为1对1 | 使用TransE |
| 关系类型多样 | 使用TransR或ComplEx |
| 存在对称关系 | 使用ComplEx或DistMult |
| 存在层次关系 | 使用HolE |
| MRR>0.4 | 嵌入质量优秀，潜在关系可信 |
| 0.2≤MRR≤0.4 | 嵌入质量中等，需人工验证 |
| MRR<0.2 | 嵌入质量差，需调整模型 |
| PyKEEN不可用 | 穷尽重试为手动关系推断 |

**输出规范**：
```yaml
pykeen_embedding:
  available: bool
  model: "TransE|TransR|ComplEx|DistMult|HolE|null"
  model_choice_reason: str|null
  hyperparameters: {embedding_dim: int, learning_rate: float, num_negs: int, batch_size: int, epochs: int}
  evaluation: {hit_at_1: float, hit_at_10: float, mrr: float}
  quality: "excellent|good|moderate|poor|null"
  potential_relations: [{head: str, relation: str, tail: str, score: float}]
  retrying_note: str|null
```

**穷尽重试策略**：当PyKEEN不可用时，按L1→L2→L3→L4逐级穷尽重试：L1 PyKEEN完整嵌入→L2 手动TransE近似（NumPy）→L3 基于规则的关系推断→L4 纯人工关系审查。

> 知识来源: TC-067 PyKEEN

---

### TC-068 SSSOM语义映射工具方法论

**方法论原理**：SSSOM语义映射工具方法论的核心认知假设是——不同本体之间的概念对齐需要标准化的映射描述格式。MC-076已内化SSSOM语义映射的一般方法论，TC-068在此基础上聚焦工具级方法论：映射谓词选择规则（exactMatch/closeMatch/narrowMatch/broadMatch）、映射置信度评估方法、映射集合并与冲突解决策略。

**执行步骤**：
1. **映射谓词选择**：(a) skos:exactMatch：概念完全等价；(b) skos:closeMatch：近似等价；(c) skos:narrowMatch：源概念是目标概念的特化；(d) skos:broadMatch：源概念是目标概念的泛化
2. **映射置信度评估**：(a) 标签相似度；(b) 结构相似度；(c) 语义相似度；(d) 综合置信度=加权平均
3. **映射集生成**：按SSSOM标准格式输出——subject_id, predicate_id, object_id为必填
4. **映射集合并**：检测冲突映射，高置信度优先+人工审核
5. **映射验证**：检查exactMatch等价性、方向正确性、循环映射

**决策规则**：

| 条件 | 决策 |
|------|------|
| 概念标签相同且定义一致 | skos:exactMatch，置信度0.9+ |
| 概念标签相似且定义近似 | skos:closeMatch，置信度0.7-0.9 |
| 源概念是目标概念的子类 | skos:narrowMatch，置信度0.6-0.8 |
| 源概念是目标概念的父类 | skos:broadMatch，置信度0.6-0.8 |
| 映射置信度<0.5 | 标注"低置信度"，建议人工审核 |
| SSSOM工具不可用 | 穷尽重试为手动映射表 |

**输出规范**：
```yaml
sssom_mapping:
  available: bool
  mapping_count: int
  mappings:
    - {subject_id: str, predicate_id: str, object_id: str, confidence: float, justification: str}
  conflicts: [{subject: str, object_a: str, object_b: str, resolution: str}]
  validation_result: {exact_match_correct: bool, direction_correct: bool, circular_found: bool}
  retrying_note: str|null
```

**穷尽重试策略**：当SSSOM工具不可用时，按L1→L2→L3→L4逐级穷尽重试：L1 SSSOM标准映射→L2 手动SSSOM格式映射→L3 简化映射表→L4 纯文本映射描述。

> 知识来源: TC-068 SSSOM

---

### TC-069 Datalog递归查询方法论（CozoDB）

**方法论原理**：Datalog递归查询方法论的核心认知假设是——知识图谱中的传递关系无法通过单次查询获得，必须通过递归规则迭代推导。CozoDB将Datalog与图数据库结合，使递归推理可以在图结构上高效执行。

**执行步骤**：
1. **递归规则定义**：(a) 基础规则：从已有事实直接推导；(b) 递归规则：从已推导的事实进一步推导；(c) 终止条件：不再产生新事实时停止
2. **传递闭包推导**：例如A is_a C :- A is_a B, B is_a C
3. **递归规则优化**：(a) 消除冗余规则；(b) 魔法集优化；(c) 半朴素求值
4. **一致性检查**：(a) 循环检测；(b) 矛盾检测
5. **多跳关系推导**：利用递归规则发现隐含的多跳关系

**决策规则**：

| 条件 | 决策 |
|------|------|
| 需要传递闭包 | 定义递归规则，执行不动点计算 |
| 需要一致性检查 | 定义循环/矛盾检测规则 |
| 递归深度>10 | 检查无限递归，添加深度限制 |
| CozoDB不可用 | 穷尽重试为NetworkX传递闭包+SQLite递归CTE |

**输出规范**：
```yaml
datalog_reasoning:
  available: bool
  recursive_rules: [{name: str, base_rule: str, recursive_rule: str}]
  results:
    - {rule_name: str, derived_facts: int, execution_time_ms: float|null}
  consistency_checks:
    - {check_type: "cycle|contradiction", passed: bool, violations: [str]}
  retrying_note: str|null
```

**穷尽重试策略**：当CozoDB不可用时，按L1→L2→L3→L4逐级穷尽重试：L1 CozoDB完整Datalog推理→L2 NetworkX传递闭包+SQLite递归CTE→L3 手动传递闭包计算→L4 纯定性传递关系声明。

> 知识来源: TC-069 Datalog-CozoDB

---

### TC-070 Neo4j图数据库方法论

**方法论原理**：Neo4j图数据库方法论的核心认知假设是——知识图谱的持久化存储和高效查询需要原生图数据库。MC-078已内化Neo4j的一般方法论，TC-070在此基础上聚焦工具级方法论：Cypher查询优化策略、GDS图算法应用规则、ACID事务与批量导入选择策略。

**执行步骤**：
1. **Schema设计**：定义节点标签、关系类型和属性约束
2. **索引设计**：为高频查询路径创建索引
3. **Cypher脚本生成**：生成节点创建、关系创建、索引定义的Cypher脚本
4. **GDS图算法应用**：(a) PageRank识别核心概念；(b) Louvain社区检测；(c) 最短路径发现隐含连接
5. **数据导入策略**：(a) <10000三元组：Cypher CREATE；(b) ≥10000：UNWIND批量；(c) 超大规模：neo4j-admin import

**决策规则**：

| 条件 | 决策 |
|------|------|
| 需要持久化存储 | 使用Neo4j，生成Cypher脚本 |
| 仅需内存分析 | 使用NetworkX |
| 需要图算法分析 | 使用GDS库 |
| Neo4j不可用 | 穷尽重试为NetworkX内存图+GraphML导出 |

**输出规范**：
```yaml
neo4j_export:
  available: bool
  cypher_scripts: {nodes: str, relationships: str, indexes: str, constraints: str}
  import_strategy: "CREATE|UNWIND|admin_import"
  gds_algorithms: [{name: str, parameters: {str: str}, results_summary: str}]
  index_design: [{label: str, property: str, type: "unique|index|fulltext"}]
  retrying_note: str|null
```

**穷尽重试策略**：当Neo4j不可用时，按L1→L2→L3→L4逐级穷尽重试：L1 Neo4j完整图数据库→L2 NetworkX+GraphML导出→L3 JSON图数据导出→L4 Mermaid图可视化。

> 知识来源: TC-070 Neo4j

---

### TC-071 CozoDB存储优化方法论

**方法论原理**：CozoDB存储优化方法论的核心认知假设是——知识图谱的查询性能不仅取决于算法复杂度，还取决于存储布局和索引策略。CozoDB作为嵌入式Datalog图数据库，聚焦于索引设计规则、递归查询优化策略、存储引擎选择。

**执行步骤**：
1. **存储引擎选择**：(a) 内存后端：最快不持久；(b) SQLite后端：轻量持久；(c) RocksDB后端：高性能持久
2. **索引设计**：(a) 实体查询：entity_id主索引；(b) 关系查询：(from, relation, to)复合索引；(c) 属性查询：高频过滤属性二级索引
3. **递归查询优化**：(a) 半朴素求值；(b) 魔法集变换；(c) 规则重写
4. **查询性能监控**：记录执行时间和资源消耗
5. **存储压缩**：冗余删除+等价合并+历史归档

**决策规则**：

| 条件 | 决策 |
|------|------|
| 临时分析场景 | 使用内存后端 |
| 单机持久化场景 | 使用SQLite后端 |
| 生产环境场景 | 使用RocksDB后端 |
| 递归查询慢 | 应用半朴素求值+魔法集变换 |
| CozoDB不可用 | 穷尽重试为SQLite递归CTE |

**输出规范**：
```yaml
cozodb_storage:
  available: bool
  storage_engine: "mem|sqlite|rocksdb|null"
  indexes: [{name: str, fields: [str], type: "primary|composite|secondary"}]
  optimization_applied: [str]
  query_performance: [{query: str, time_ms: float|null}]
  storage_stats: {total_triples: int, storage_size_mb: float|null}
  retrying_note: str|null
```

**穷尽重试策略**：当CozoDB不可用时，按L1→L2→L3→L4逐级穷尽重试：L1 CozoDB完整存储优化→L2 SQLite递归CTE→L3 NetworkX+JSON序列化→L4 纯文件存储。

> 知识来源: TC-071 CozoDB

---

### TC-072 TypeDB强类型知识图谱方法论

**方法论原理**：TypeDB的强类型系统使知识图谱能够表达实体间的复杂关系约束，超越RDF的三元组限制。传统RDF知识图谱仅能表达"主-谓-宾"三元组，关系的结构约束（如角色约束、基数约束、类型继承）必须通过额外的OWL公理来补充。TypeDB通过类型继承（Entity→Person/Organization等）、角色约束（关系中的参与者必须有特定类型）和推理规则（含递归规则），将声明式知识建模与自动化推理统一在同一个类型系统中。这种方法论使我们从"三元组+额外公理"升级为"类型即约束"的知识建模范式。

**执行步骤**：
1. 定义类型层次：从顶层Entity/Relation/Attribute向下定义类型继承（如Entity→Person/Organization等）
2. 定义关系类型（含角色约束）：为每个关系定义角色及其类型约束（如employment关系包含employee:Person和employer:Organization两个角色）
3. 定义推理规则（含递归规则）：编写TypeQL推理规则，支持传递性推理（如A supervises B, B supervises C → A manages C）
4. 插入实例数据：按类型层次和角色约束插入实体和关系实例
5. 执行TypeQL查询（含模式推理）：利用推理规则自动推导隐含关系，执行聚合和分组查询
6. 验证一致性约束：检查实例数据是否满足类型约束和角色约束

**决策规则**：

| 条件 | 决策 |
|------|------|
| 需要强类型约束+复杂关系 | 使用TypeDB |
| 需要标准RDF/OWL | 使用OWLAPY+Neo4j |
| 需要高性能Datalog | 使用CozoDB |
| 关系需要角色约束和类型继承 | 使用TypeDB |
| 仅需简单三元组存储 | 使用Neo4j或RDF |
| TypeDB不可用 | 穷尽重试为OWLAPY+Neo4j替代 |

**输出规范**：
```yaml
typedb_ontology:
  available: bool
  type_hierarchy: [{parent: str, children: [str]}]
  relation_types: [{name: str, roles: [{name: str, player_type: str}]}]
  inference_rules: [{name: str, when: str, then: str}]
  instance_stats: {entities: int, relations: int, attributes: int}
  consistency_check: {passed: bool, violations: [str]}
  retrying_note: str|null
```

**穷尽重试策略**：当TypeDB不可用时，按L1→L2→L3→L4逐级穷尽重试：L1 TypeDB完整（类型层次+角色约束+推理规则+一致性验证）→L2 OWLAPY+Neo4j替代（用OWL本体表达类型约束，用Neo4j存储实例，推理能力受限）→L3 手动关系映射（手动定义类型约束和关系规则，无自动推理）→L4 纯文字关系描述（仅用自然语言描述实体间关系，无形式化约束）。

> 知识来源: TC-072 TypeDB

---

### BioSage 跨学科知识合成

> **架构参考**: BioSage — 跨学科知识合成框架
> **仅参考，不注册独立能力卡**

BioSage 提出的跨学科知识合成方法论对 TM07 的本体构建有重要参考价值，特别是在多领域知识整合方面：

```yaml
biosage_reference:
  purpose: "指导 TM07 在多领域本体构建时实现概念的系统化整合"
  alignment_with_TM07:
    - "BioSage 的概念融合层 → TM07 Step 1 实体类型分类中的跨域实体识别"
    - "BioSage 的理论桥接层 → TM07 Step 3 本体构建中的跨域公理定义"
    - "BioSage 的实证合成层 → TM07 Step 4 语义映射中的多外部本体协同标注"
  gap_analysis:
    missing: "BioSage 的自动化跨学科概念对齐能力（LLM-based Concept Alignment）在本框架中尚未完全实现"
    recommendation: "未来版本可考虑引入 BioSage 的自动化概念对齐模块，增强 TM07 Step 4 的语义映射能力"
```

---

### TC-093 KGHeartBeat知识图谱质量监控方法论

**方法论原理**：知识图谱质量监控是KG持续维护的基础，通过一致性/完整性/时效性三维度检测确保KG可靠性。KGHeartBeat将质量监控算法化，支持自动检测模式约束违反、属性/关系/实例覆盖率不足、时间戳过期等问题，是TM07本体导出后质量保障的关键方法论。

**执行步骤**：
1. 一致性约束检查（4类）：(a) 模式约束——实例是否符合其类型的属性定义；(b) 逆关系约束——若A→R→B存在，则B→R⁻→A应存在；(c) 传递性约束——若A→partOf→B且B→partOf→C，则A→partOf→C应存在；(d) 基数约束——关系的基数限制（如一人仅一个出生地）
2. 完整性检查（3维度）：(a) 属性覆盖率——具有必需属性的实例比例；(b) 关系覆盖率——具有期望关系的实例比例；(c) 实例覆盖率——各概念类型下的实例数量是否充分
3. 时效性扫描：检测时间戳过期的实体和关系，标记需更新的知识
4. 冲突检测（2策略）：(a) 源权威度优先——高权威度来源覆盖低权威度来源的矛盾信息；(b) 时间戳优先——较新信息覆盖较旧信息的矛盾信息
5. 质量评分计算：综合一致性、完整性、时效性三维度加权评分
6. 修复建议生成：针对检测到的问题生成具体修复操作建议

**决策规则**：
- if 一致性违反>阈值 → P0修复（立即处理，影响KG可靠性）
- if 完整性<阈值 → P1补充（优先处理，影响KG可用性）
- if 时效性过期 → P2更新（常规处理，影响KG时效性）

**输出规范**：
```yaml
kg_heartbeat:
  consistency_check:
    schema_violations: [{entity: str, violation: str, severity: "P0|P1|P2"}]
    inverse_relation_violations: [{relation: str, missing_inverse: str}]
    transitivity_violations: [{chain: [str], missing: str}]
    cardinality_violations: [{entity: str, relation: str, expected: int, actual: int}]
    overall_score: float
  completeness_check:
    attribute_coverage: {total: int, covered: int, ratio: float}
    relation_coverage: {total: int, covered: int, ratio: float}
    instance_coverage: [{concept_type: str, expected: int, actual: int, ratio: float}]
    overall_score: float
  timeliness_check:
    expired_entities: [{entity: str, last_updated: str, expiry_threshold: str}]
    expired_relations: [{relation: str, last_updated: str, expiry_threshold: str}]
    overall_score: float
  conflict_detection:
    conflicts: [{entity: str, field: str, sources: [str], resolution_strategy: str}]
  quality_score: {consistency: float, completeness: float, timeliness: float, overall: float}
  repair_suggestions: [{issue: str, action: str, priority: "P0|P1|P2"}]
  retrying_note: str|null
```

**穷尽重试策略**：L1 KGHeartBeat完整监控（一致性4类+完整性3维度+时效性+冲突检测+评分+修复建议）→L2 手动SPARQL检查（手动编写SPARQL查询检查关键约束，无自动评分）→L3 采样检查（随机抽取10%实体进行人工检查，无全面覆盖）→L4 人工审查（专家逐项审查关键实体，无系统化方法）

> 知识来源: TC-093 KGHeartBeat

