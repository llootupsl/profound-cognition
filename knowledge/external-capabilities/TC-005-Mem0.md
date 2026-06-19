<!-- 作者：阿洋 -->

# Mem0

## 基本信息
- **卡片编号**: #5
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
- **MCP Tool 名称**: mem0_operation
- **MCP 参数**: operation, data, user_id, metadata, memory_id, query, limit

## 依赖
- Mem0 服务部署 + API Key

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

暂无显式 DAG 节点消费者。保留待扩展。

