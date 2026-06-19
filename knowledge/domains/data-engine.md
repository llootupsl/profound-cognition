<!-- 作者：阿洋 -->

# 数据科学领域引擎 -- Data Science Domain Engine

> **模块标识**: `knowledge/domains/data-engine`
> **职责**: 为Profound Cognition提供数据科学领域的深度认知分析能力，覆盖数据质量、统计分析、机器学习和可视化。

---

## 1. 核心分析框架

### 维度一：数据质量与预处理（Data Quality and Preprocessing）

**定义**: 评估数据的完整性、准确性、一致性和时效性，并进行必要的清洗和转换。

**具体分析方法**:
- **数据画像**: 缺失率、异常值、分布形态、重复率的系统扫描
- **数据溯源**: 追溯数据来源、收集方法、采样策略和潜在偏差
- **数据清洗策略**: 缺失值处理（删除/插补）、异常值处理（截断/变换）
- **特征工程**: 特征选择、提取、编码和归一化的合理性评估

### 维度二：统计方法与推断（Statistical Methods and Inference）

**定义**: 选择合适的统计方法进行假设检验、参数估计和不确定性量化。

**具体分析方法**:
- **描述性统计**: 集中趋势、离散程度、分布形态的恰当选择
- **推断性统计**: 假设检验（t检验、ANOVA、卡方检验）的适用性评估
- **贝叶斯方法**: 先验选择、后验更新、MCMC收敛诊断
- **多重比较与P值**: 多重检验校正（Bonferroni、FDR）、P-hacking防范

### 维度三：模型选择与评估（Model Selection and Evaluation）

**定义**: 选择适当的机器学习模型并进行严谨的评估和验证。

**具体分析方法**:
- **模型选择**: 偏差-方差权衡、正则化、交叉验证策略
- **评估指标**: 分类（准确率、精确率、召回率、F1、AUC）、回归（MSE、MAE、R²）
- **过拟合检测**: 训练-验证-测试集划分、学习曲线分析
- **可解释性**: SHAP值、LIME、特征重要性的一致性检查

---

## 2. 分析器清单

| # | 分析器名称 | 激活条件 | 输出格式 |
|---|-----------|---------|---------|
| 1 | 数据质量评估 | 有数据 | 完整性 + 准确性 + 偏差 + 时效性 |
| 2 | 统计方法评估 | 有分析 | 方法选择 + 假设检验 + 效应量 |
| 3 | 可视化评估 | 有图表 | 图表类型 + 表达准确性 + 误导检测 |
| 4 | 模型选择分析 | 有模型 | 偏差-方差 + 复杂度 + 适用性 |
| 5 | 结果解读 | 有结果 | 统计显著性 + 实际显著性 + 因果解读 |
| 6 | 数据伦理评估 | 始终 | 隐私 + 公平性 + 透明性 + 同意义务 |

### 调用矩阵

| 分析器 | T15 领域分析 | T15b 跨域矩阵 | T08 认知解构 | T09 认知推理 | T05 证据 | T06 反事实 |
|--------|:-----------:|:------------:|:-----------:|:-----------:|:-------:|:--------:|
| 数据质量评估 | ✓ | ✓ | ✓ | ✓ | - | - |
| 统计方法评估 | ✓ | ✓ | ✓ | ✓ | - | - |
| 可视化评估 | ✓ | ✓ | ✓ | ✓ | - | - |
| 模型选择分析 | ✓ | ✓ | ✓ | ✓ | - | - |
| 结果解读 | ✓ | ✓ | ✓ | ✓ | - | - |
| 数据伦理评估 | ✓ | ✓ | ✓ | ✓ | - | - |


## 3. 外部能力卡片引用

- **TC-009 Wikidata**: 结构化知识图谱，可辅助数据科学领域的实体属性验证、事实核查和数据溯源。详见 `knowledge/external-capabilities/TC-009-Wikidata.md`

## 依赖的能力卡片

| 卡片 | 用途 | 激活条件 | 使用方式 |
|------|------|---------|---------|
| TC-009 Wikidata | 结构化知识图谱查询，用于实体属性验证、事实核查和数据溯源 | on-demand | 插件调用 |

---

## 4. SPARQL查询方法论 (TC-009 Wikidata)

### 4.1 方法论原理

SPARQL查询方法论的核心认知假设是——结构化知识图谱中的信息以"实体-属性-值"三元组形式组织，通过模式化的查询模板可以高效、精确地检索结构化事实。Wikidata作为全球最大的开放结构化知识库，其SPARQL端点提供了4类核心查询模式：实体查询（查什么）、属性查询（查哪个属性）、限定符查询（查条件细节）、引用查询（查来源）。掌握这4类模板的组合使用，可以从Wikidata中提取出远超搜索摘要的精确结构化数据。这种方法论使我们从"模糊搜索"升级为"精确结构化查询"。

> 知识来源: TC-009 [Wikidata]

### 4.2 执行步骤

1. **实体查询模板**：通过标签或描述定位目标实体
   ```sparql
   SELECT ?item ?itemLabel WHERE {
     ?item rdfs:label ?itemLabel .
     FILTER(CONTAINS(LCASE(?itemLabel), LCASE("{search_term}")))
     FILTER(LANG(?itemLabel) = "zh" || LANG(?itemLabel) = "en")
   } LIMIT 10
   ```
2. **属性查询模板**：查询指定实体的特定属性值
   ```sparql
   SELECT ?value ?valueLabel WHERE {
     wd:Q{entity_id} wdt:P{property_id} ?value .
     SERVICE wikibase:label { bd:serviceParam wikibase:language "zh,en". }
   } LIMIT 20
   ```
3. **限定符查询模板**：查询属性的限定条件（时间、地点、原因等）
   ```sparql
   SELECT ?value ?valueLabel ?qualifier ?qualifierLabel WHERE {
     wd:Q{entity_id} p:P{property_id} ?statement .
     ?statement ps:P{property_id} ?value .
     OPTIONAL { ?statement ?qualifierProp ?qualifier .
       ?qualifierProp wikibase:qualifier ?qualifierLabel }
     SERVICE wikibase:label { bd:serviceParam wikibase:language "zh,en". }
   }
   ```
4. **引用查询模板**：查询声明的来源引用
   ```sparql
   SELECT ?reference ?referenceLabel WHERE {
     wd:Q{entity_id} p:P{property_id} ?statement .
     ?statement prov:wasDerivedFrom ?refNode .
     ?refNode ?refProp ?reference .
     SERVICE wikibase:label { bd:serviceParam wikibase:language "zh,en". }
   }
   ```

> 知识来源: TC-009 [Wikidata]

### 4.3 决策规则

| 条件 | 决策 |
|------|------|
| 需要验证量化数据（人口/GDP/面积） | 使用属性查询模板，优先查询P1082/P2131/P2046 |
| 需要验证实体间关系 | 使用属性查询+限定符查询组合 |
| 不确定实体Q-ID | 先用实体查询模板搜索，再确认 |
| 需要数据来源验证 | 使用引用查询模板追踪声明来源 |
| SPARQL查询超时（>15s） | 穷尽重试：调整查询策略后重试，引用 exhaust-retry-protocol.md |
| 查询返回空结果 | 检查Q-ID和P-ID是否正确，尝试英文标签搜索 |

> 知识来源: TC-009 [Wikidata]

### 4.4 输出规范

```yaml
wikidata_query_result:
  query_type: "entity|property|qualifier|reference"
  entity_id: str
  property_id: str|null
  results:
    - value: str
      value_label: str
      qualifiers: [{property: str, value: str}]
      references: [{source: str, url: str|null}]
  source_category: "L0"
  source: "wikidata:{qid}"
```

> 知识来源: TC-009 [Wikidata]

### 4.5 穷尽重试策略

| 重试路径 | 触发条件 | 行为 |
|---------|---------|------|
| Wikidata → ConceptNet | Wikidata连续3次超时 | 使用ConceptNet常识关联替代，标注`retry_path=conceptnet`，持续尝试恢复Wikidata |
| ConceptNet → LLM知识 | ConceptNet也不可用 | 使用LLM自有知识，标注`source_category=L3, confidence_penalty=-0.2`，持续尝试恢复外部数据源 |
| SPARQL语法错误 | 查询返回400 | 修正查询语法后重试，持续尝试直至成功 |

> 知识来源: TC-009 [Wikidata]
> 引用 exhaust-retry-protocol.md：当外部数据源不可用时，不穷尽重试替代，而是穷尽尝试所有替代路径，持续重试直至质量达标。


### TC-070 Neo4j 图数据库持久化方法论

**核心步骤**：
1. 图模型设计：定义节点标签、关系类型和属性schema
2. Cypher查询构建：使用声明式Cypher语言构建图查询（MATCH/WHERE/CREATE/RETURN）
3. 批量导入：使用CSV文件批量导入节点和关系数据
4. 图算法执行：调用GDS图算法库执行中心性、社区检测、路径查询
5. 事务管理：使用ACID事务确保数据一致性

**决策规则**：需要图数据库持久化和复杂图查询时使用Neo4j；内存图计算使用NetworkX

**穷尽重试策略**：Neo4j → NetworkX内存图 → 邻接表+字典（穷尽尝试所有替代路径，引用 exhaust-retry-protocol.md）

> 知识来源: TC-070 Neo4j


### TC-071 CozoDB Datalog传递推理方法论

**核心步骤**：
1. Datalog规则定义：定义递归规则进行传递闭包推理（如A→B, B→C推导A→C）
2. 时态图查询：利用Datalog的时态查询能力进行时间维度上的关系推理
3. 一致性检查：利用递归规则进行本体一致性验证
4. 多跳关系推导：通过递归规则发现隐含的多跳关系路径
5. 嵌入式部署：作为嵌入式数据库直接集成到Python应用中

**决策规则**：需要传递闭包推理和递归查询时使用CozoDB；简单图查询使用Neo4j

**穷尽重试策略**（引用 exhaust-retry-protocol.md）：CozoDB → NetworkX传递闭包+手动递归 → SQLite递归CTE

> 知识来源: TC-071 CozoDB


### TC-072 TypeDB 强类型知识图谱方法论

**核心步骤**：
1. Schema定义：使用TypeQL定义实体类型、关系类型和角色类型
2. 类型推理：利用TypeDB的类型推理引擎自动推导实例的类型归属
3. 规则定义：定义推理规则实现隐含知识的自动推导
4. 约束验证：利用强类型系统确保知识图谱的语义一致性
5. 查询执行：使用TypeQL进行模式匹配查询

**决策规则**：需要强类型约束和自动类型推理时使用TypeDB；灵活schema使用Neo4j

**穷尽重试策略**（引用 exhaust-retry-protocol.md）：TypeDB → OWL/RDF+OWLAPY推理 → NetworkX+手动类型检查

> 知识来源: TC-072 TypeDB

---

## 5. 领域引擎穷尽重试策略

> 引用 exhaust-retry-protocol.md：当领域数据或工具不可用时，不穷尽重试替代，而是穷尽尝试所有替代路径，持续重试直至质量达标。

```yaml
domain_engine_exhaust_retry:
  L1_FULL:
    condition: "领域知识完整，所有分析器可用，数据源可访问"
    tools: [data_profiling, statistical_testing, ML_evaluation, SHAP_LIME, Wikidata, Neo4j, CozoDB]
    action: "完整数据科学分析工具链：数据画像+统计推断+ML模型评估与可解释性+SPARQL结构化查询+图数据库持久化+传递推理"
    confidence: "HIGH"
  L2_RETRYING_PARTIAL:
    condition: "部分数据源不可用或部分分析器需重试"
    tools: [simplified_statistics, basic_model_evaluation, manual_data_quality, basic_Wikidata]
    action: "穷尽重试：尝试所有替代路径获取数据，使用简化统计分析+手动数据质量检查+简化模型评估作为重试中间态"
    confidence: "MEDIUM"
    output_annotation: "领域引擎重试中：简化统计分析，正在穷尽尝试恢复可解释性工具"
  L3_RETRYING_TEXT:
    condition: "所有外部数据源不可用，穷尽重试后仅剩LLM自有知识"
    tools: [qualitative_data_analysis, informal_statistical_reasoning]
    action: "穷尽重试：定性数据分析+非形式化统计推理+定性数据质量评估+直觉性模型判断，标注'穷尽重试后仍无外部验证'"
    confidence: "LOW-MEDIUM"
    output_annotation: "领域引擎穷尽重试：定性数据分析模式"
  L4_EXHAUSTED:
    condition: "领域知识完全不足（超出LLM知识范围的专业数据工程领域），穷尽所有替代路径后仍无法获得足够信息"
    tools: []
    action: "穷尽重试后仍领域知识不足，标注不确定性，建议人工专家介入"
    confidence: "LOW"
    output_annotation: "领域引擎穷尽重试后仍不足：建议专家介入"
```
