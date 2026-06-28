<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

# Wikidata

## 基本信息

> ★核心方法论已内化于 knowledge/domains/data-engine.md，本文件仅作快速引用入口

- **卡片编号**: #9
- **类型**: TC
- **优先级**: P1
- **层级**: L1

## 功能描述
Wikidata 结构化知识库查询，提供实体属性、关系和声明的高精度结构化数据访问。支持 SPARQL 查询和实体直接查询两种模式，用于事实核查、知识增强和实体消歧。

## 调用指令

### 输入参数
- `query` (string, SPARQL 查询语句，与 entity_id 二选一)
- `entity_id` (string, Wikidata 实体 ID，如 Q148 代表中国，与 query 二选一)
- `property` (string, 可选属性 ID，如 P31 实例关系、P585 时间点，配合 entity_id 使用)
- `language` (string, 可选，返回标签语言，默认 zh)

### 输出格式
JSON 结构化数据，含实体标签、描述、属性值和限定符

### 调用示例
```
wikidata.query(entity_id="Q148", property="P31", language="zh")
wikidata.query(query="SELECT ?item ?itemLabel WHERE { ?item wdt:P31 wd:Q5. ?item wdt:P27 wd:Q148. } LIMIT 10", language="zh")
```

## 穷尽重试策略
- **穷尽重试替代路径**: Wikidata → ConceptNet → LLM 知识
- **触发条件**: Wikidata API 连续 3 次超时或 SPARQL 端点不可用

## MCP 适配
- **MCP Tool 名称**: wikidata_query
- **MCP 参数**: query, entity_id, property, language

## 依赖
- Wikidata 公共 API / SPARQL 端点（https://query.wikidata.org）

## 调用前置条件
- Python 3.9+ 运行环境（如需代码执行）
- Wikidata 公共 API / SPARQL 端点可访问（见上方「依赖」）
- 网络连接可用（Wikidata 为远程服务）
- 上游节点产出已就绪（根据消费节点依赖关系）

## 消费关系

### 消费此卡片的领域引擎

| 引擎名称 | 激活条件 | 使用方式 |
|---------|---------|---------|
| data-engine | on-demand | 实体属性验证、事实核查、数据溯源 - 通过 Wikidata API 查询 |

### 消费此卡片的 DAG 节点

暂无显式 DAG 节点消费者。


## 效果度量

| 度量指标 | 定义 | 目标值 |
|----------|------|--------|
| 执行成功率 | 成功调用次数 / 总调用次数 | ≥ 0.95 |
| 平均延迟 | 单次调用平均耗时 | ≤ 5s |
| 输出质量分 | Supervisor 评分（0-1） | ≥ 0.8 |
| 穷尽重试触发率 | 触发降级的调用次数 / 总调用次数 | ≤ 0.1 |

效果度量写入 NRSF，供 T19 质量检查消费。