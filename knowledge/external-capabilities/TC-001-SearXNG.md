<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

# SearXNG

## 基本信息

> ★核心方法论已内化于 knowledge/search-strategy.md，本文件仅作快速引用入口

- **卡片编号**: #1
- **类型**: TC
- **优先级**: P0
- **层级**: L1

## 功能描述
元搜索聚合引擎，聚合 Google/Bing/DuckDuckGo 等多引擎搜索结果，支持去重和质量评分

## 调用指令

### 输入参数
- `query` (string, 搜索查询)
- `categories` (string, 可选: general/science/news/images)
- `language` (string, 可选: zh/en/all)
- `max_results` (integer, 默认 20)

### 输出格式
JSON 数组，每条含 title, url, snippet, engine, score

### 调用示例
```
searxng.search(query="中国新能源汽车竞争格局", categories="general", language="zh", max_results=20)
```

## 穷尽重试策略
- **穷尽重试替代路径**: SearXNG → Whoogle → LLM 内置搜索
- **触发条件**: SearXNG 服务不可用或超时

## MCP 适配
- **MCP Tool 名称**: searxng_search
- **MCP 参数**: query, categories, language, max_results

## 依赖
- SearXNG 服务部署

## 调用前置条件
- Python 3.9+ 运行环境（如需代码执行）
- SearXNG 服务已部署并可访问（见上方「依赖」）
- 网络连接可用（SearXNG 为远程搜索服务）
- 上游节点产出已就绪（根据消费节点依赖关系）

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

| 节点 | 用途 |
|------|------|
| T02 | 文献检索（L1 基础事实搜索） |


## 效果度量

| 度量指标 | 定义 | 目标值 |
|----------|------|--------|
| 执行成功率 | 成功调用次数 / 总调用次数 | ≥ 0.95 |
| 平均延迟 | 单次调用平均耗时 | ≤ 5s |
| 输出质量分 | Supervisor 评分（0-1） | ≥ 0.8 |
| 穷尽重试触发率 | 触发降级的调用次数 / 总调用次数 | ≤ 0.1 |

效果度量写入 NRSF，供 T19 质量检查消费。