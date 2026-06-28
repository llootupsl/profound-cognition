<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

# LightRAG

## 基本信息
- **卡片编号**: #11
- **类型**: TC
- **优先级**: P1
- **层级**: L1

## 功能描述
LightRAG 轻量 RAG 框架，支持文档索引和语义检索。采用图增强检索策略，结合实体抽取和关系构建实现高效知识检索。适用于研究文献、报告文档的增量索引和精准语义查询。

## 调用前置条件
- Python 3.8+
- LightRAG 服务已部署并可访问（`lightrag --version` 可执行，或 HTTP 端点可达）
- 嵌入模型已配置（推荐 text-embedding-3-small 或同等嵌入模型）
- 索引数据已初始化（query 操作前需先完成 index 操作）
- 工作目录可写（用于存储索引文件和缓存）
- 查询模式已配置（默认 hybrid）

## 调用指令

### 输入参数
- `operation` (string, 操作类型: index/query)
- `documents` (array, index 操作必需，文档路径或文本数组)
- `query` (string, query 操作必需，语义查询文本)
- `top_k` (integer, query 操作返回结果数，默认 5)

### 输出格式
检索结果数组，每条含 content、source、score

### 调用示例
```
lightrag.operation(operation="index", documents=["/data/report_2026.pdf", "/data/market_analysis.md"])
lightrag.operation(operation="query", query="中国新能源汽车出海策略分析", top_k=5)
```

### 查询模式（Query Modes）

LightRAG 支持 4 种查询模式，根据查询语义复杂度自适应选择：

| 模式 | 适用场景 | 检索策略 | 示例 |
|------|----------|----------|------|
| `local` | 局部事实查询 | 仅检索与查询直接相关的实体与关系 | "XX 公司 2025 年 Q3 营收是多少？" |
| `global` | 全局综述查询 | 检索跨主题的高层级关系 | "半导体产业链的整体结构是什么？" |
| `hybrid` | 混合查询（默认） | 同时检索 local + global，综合返回 | "XX 公司在半导体产业链中的地位？" |
| `naive` | 朴素关键词查询 | 直接向量检索（无图增强） | "RISC-V 架构" |

**调用示例**：
```python
lightrag.operation(
    operation="query",
    query="中国新能源汽车出海策略分析",
    mode="hybrid",  # local | global | hybrid | naive
    top_k=5,
)
```

**模式选择规则**：
- 默认使用 `hybrid` 模式
- 若查询包含具体实体名称（人名/公司名/产品名），使用 `local`
- 若查询为开放式/综述性问题，使用 `global`
- 若 `hybrid` 模式延迟 > 10s，回退到 `naive`

## 穷尽重试策略
- **穷尽重试替代路径**: LightRAG → 简单向量搜索 → 关键词搜索
- **触发条件**: LightRAG 服务不可用或索引损坏

## 效果度量
- **检索相关性分数** (0-1)：每条检索结果的 score 字段，越高表示语义相关性越强
- **检索覆盖率**：query 操作返回结果数 / top_k，反映索引完整性
- **检索延迟** (ms)：从 query 到返回结果的耗时，反映服务性能
- 阈值规则：检索相关性分数均值 ≥ 0.7 视为有效检索；< 0.7 触发索引重建或回退到简单向量搜索
- 辅助度量：索引文档数、索引大小（MB）、查询 QPS

## MCP 适配
- **MCP Tool 名称**: lightrag_operation
- **MCP 参数**: operation, documents, query, top_k

## 依赖
- LightRAG 服务部署 + 嵌入模型（推荐 text-embedding-3-small）

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

| 节点 | 消费方式 | 说明 |
|------|---------|------|
| T08（L1 多源研究） | `query(mode=hybrid)` | 增量检索已索引文献 |
| T09（L2 深度研究） | `query(mode=global)` | 综述性问题检索 |
| T10（对抗分析） | `query(mode=local)` | 针对特定实体检索反证 |
| T11（L3 极限研究） | `query(mode=hybrid)` | 深度混合检索 |
| T12（综合辩证） | `query(mode=naive)` | 快速关键词检索验证 |
| T12b（融合综合） | `query(mode=hybrid)` | 综合检索融合证据 |
| T13（认知综合） | `query(mode=global)` | 全局结论检索 |
| T15（证据验证） | `query(mode=local)` | 实体级证据验证 |

（注：上述消费关系为协议层声明，任务层调用由执行引擎根据上下文自动触发）

