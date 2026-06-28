<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

# AIHot

## 基本信息
- **卡片编号**: #16
- **类型**: TC
- **优先级**: P1
- **层级**: L1

## 功能描述
AIHot AI 工具热力图，提供 AI 工具生态概览和趋势分析。聚合多维度工具数据，支持按类别、时间范围和地区筛选，输出工具排名和热度趋势，用于技术选型参考和竞争格局分析。

## 调用指令

### 输入参数
- `category` (string, 可选工具类别: llm/rag/agent/vector-db/ide，默认全部)
- `time_range` (string, 可选时间范围: 7d/30d/90d/1y，默认 30d)
- `region` (string, 可选地区: global/cn/us/eu，默认 global)

### 输出格式
工具排名和趋势数据 JSON，含工具名称、类别、热度评分、趋势变化、链接

### 调用示例
```
aihot.query(category="rag", time_range="30d", region="global")
aihot.query(category="agent", time_range="90d", region="cn")
```

## 穷尽重试策略
- **穷尽重试替代路径**: AIHot → 手动搜索
- **触发条件**: AIHot API 不可用或数据过期

## MCP 适配
- **MCP Tool 名称**: aihot_query
- **MCP 参数**: category, time_range, region

## 依赖
- AIHot 服务部署 / 公共 API

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

暂无显式 DAG 节点消费者。保留待扩展。


## 效果度量

| 度量指标 | 定义 | 目标值 |
|----------|------|--------|
| 执行成功率 | 成功调用次数 / 总调用次数 | ≥ 0.95 |
| 平均延迟 | 单次调用平均耗时 | ≤ 5s |
| 输出质量分 | Supervisor 评分（0-1） | ≥ 0.8 |
| 穷尽重试触发率 | 触发降级的调用次数 / 总调用次数 | ≤ 0.1 |

效果度量写入 NRSF，供 T19 质量检查消费。