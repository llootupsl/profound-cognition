<!-- 作者：阿洋 -->

# TC-070: Neo4j — Graph Database

## 基本信息

> ★核心方法论已内化于 tasks/TM07_ontology_export.md，本文件仅作快速引用入口

- **名称**: Neo4j
- **类别**: 图数据库
- **语言**: Cypher / Python (py2neo/neo4j-driver)
- **版本要求**: ≥5.0
- **安装**: Docker 部署 (docker run neo4j)
- **许可证**: GPL-3 (Community) / Commercial (Enterprise)
- **仓库**: https://github.com/neo4j/neo4j

## 核心能力
- 原生图数据库存储与查询
- Cypher 声明式查询语言
- 图算法库 (GDS)
- 可视化与浏览器界面
- ACID 事务支持

## 在 profound-cognition 中的用途
- **T28 Step 6**: Neo4j 图数据库持久化
- **穷尽重试替代路径**: 失败时穷尽重试替代为 NetworkX 内存图

## API 示例
```python
from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

with driver.session() as session:
    session.run(
        "CREATE (a:Entity {name: $name})",
        name="Concept_A"
    )
    session.run(
        "MATCH (a:Entity {name: $from}), (b:Entity {name: $to}) "
        "CREATE (a)-[:RELATED_TO {weight: $w}]->(b)",
        from="Concept_A", to="Concept_B", w=0.8
    )

driver.close()
```

## 已知限制
- 需要 Docker 环境或独立服务器
- 社区版不支持集群
- 纯文本研究场景通常穷尽重试替代为 NetworkX 内存图
- 部署复杂度高于纯 Python 方案

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

| 节点 | 用途 |
|------|------|
| TM07 | 图数据库 |

