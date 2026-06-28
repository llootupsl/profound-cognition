<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

> **Deprecated**: true
> **Superseded by**: [Mem0.md](./Mem0.md)（#5b v6.0 增强版）
> **Deprecation date**: 2026-06-27
> **Deprecation reason**: 基础版已被 v6.0 增强版取代，MCP Tool 名称不一致（`mem0_cross_session` vs `mem0_operation`），存在重复能力卡

# Mem0

## 基本信息
- **卡片编号**: #5（已弃用，迁移至 #5b）
- **类型**: TC
- **优先级**: P0
- **层级**: L1

## 功能描述
记忆管理服务，提供三操作模型（add/search/update），用于 NRSF-Summary 的增量管理。支持 Mem0g 图增强版提供实体关系图。

## 调用指令

### 输入参数
- `operation` (string, 操作类型: add/search/update)
- `data` (string, 操作数据)
- `user_id` (string, 用户标识)
- `metadata` (object, 可选元数据，含 task_id/timestamp/research_id)
- `memory_id` (string, update 操作必需)
- `query` (string, search 操作必需)
- `limit` (integer, search 操作，默认 10)

### 输出格式
- add → memory_id
- search → 记忆片段数组
- update → 确认

### 调用示例
```
mem0.add(data="研究发现中国新能源汽车出口增长30%", user_id="research_001", metadata={"task_id": "T03", "timestamp": "2026-05-30T14:30:00", "research_id": "uuid"})
```

## 穷尽重试策略
- **穷尽重试替代路径**: Mem0 → 纯文件模式（NRSF-Summary Markdown 文件）
- **触发条件**: Mem0 API 连续 3 次超时

## MCP 适配
> **【A6.2-F6 修复，Wave 7，2026-06-27】废弃警告**：本卡的 MCP Tool 名称 `mem0_operation` 已废弃。增强版 [Mem0.md](./Mem0.md)（#5b v6.0）使用新 MCP Tool 名称 `mem0_cross_session`，参数集已扩展（含 `memory_layer`、`semantic_search`）。下游消费方应迁移至 `mem0_cross_session`，本卡仅保留用于历史兼容追溯。
- **MCP Tool 名称**: mem0_operation（已废弃，迁移至 `mem0_cross_session`，见 Mem0.md #5b）
- **MCP 参数**: operation, data, user_id, metadata, memory_id, query, limit

## 依赖
- Mem0 服务部署 + API Key

## 调用前置条件
- Python 3.9+ 运行环境（如需代码执行）
- Mem0 服务已部署 + API Key 已配置（见上方「依赖」）
- 网络连接可用（Mem0 为远程记忆服务）
- 上游节点产出已就绪（根据消费节点依赖关系）

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