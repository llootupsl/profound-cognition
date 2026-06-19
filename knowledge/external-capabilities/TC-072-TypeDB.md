---
name: TC-072-TypeDB
description: 强类型知识图谱数据库，支持实体-关系-属性类型系统
version: "1.0"
category: external-tool
consuming_engines: []
integrated_nodes: [TM07]
---

<!-- 作者：阿洋 -->


# TC-072: TypeDB — 强类型知识图谱

## 用途
基于实体-关系-属性模型的强类型知识图谱数据库，通过TypeQL查询语言强制执行schema约束，确保知识图谱的语义一致性。

## 授权/许可
AGPL-3.0 (Community) / Commercial (Enterprise)

## 下载源
https://github.com/typedb/typedb

## 集成节点
- **TM07 (本体导出)**: 将Profound Cognition的领域本体schema映射为TypeDB类型系统，利用TypeQL的类型推理进行本体一致性验证

## tool-availability 探测
```bash
# 检测TypeDB服务器
python -c "from typedb.client import TypeDB; print('TypeDB client available')" 2>/dev/null || echo "TypeDB client not installed"
# 或检测Docker
docker ps | grep typedb
```

## 穷尽重试替代链
若不可用 → 穷尽重试替代为 OWL/RDF + OWLAPY 推理；或穷尽重试替代为 NetworkX + 手动类型检查

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

| 节点 | 用途 |
|------|------|
| TM07 | 强类型知识图谱 |

## 方法论内化

> ★核心方法论已内化于 tasks/TM07_ontology_export.md，以下为快速参考

### 方法论原理
TypeDB的强类型系统使知识图谱能够表达实体间的复杂关系约束，超越RDF三元组限制。

### 执行步骤
1. 定义类型层次
2. 定义关系类型(含角色约束)
3. 定义推理规则
4. 插入实例
5. 执行TypeQL查询
6. 验证一致性

### 决策规则
| 条件 | 动作 |
|------|------|
| 需要强类型+复杂关系 | TypeDB |
| 需要标准RDF/OWL | OWLAPY+Neo4j |
| 需要Datalog | CozoDB |

### 输出规范
```yaml
typedb_output:
  available: bool
  schema_valid: bool
  query_results: list
  consistency_check: bool
  degradation_note: str
```

### 穷尽重试策略
| 级别 | 方案 |
|------|------|
| L1 | TypeDB完整强类型查询 |
| L2 | OWLAPY+Neo4j |
| L3 | 手动关系映射 |
| L4 | 纯文字关系描述 |

