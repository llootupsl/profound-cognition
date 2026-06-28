<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

# Google ADK

## 基本信息
- **卡片编号**: #41
- **类型**: MC
- **优先级**: P2
- **层级**: L0

## 功能描述
Google ADK Agent 开发工具包，提供 MemoryService 第三存储层和 Event Tracing 审计日志层。MemoryService 为 Agent 提供持久化记忆存储能力，支持跨会话状态保持；Event Tracing 提供全链路事件追踪与审计日志，支持 Agent 行为可观测性和合规审计。

## 调用指令

### 输入参数
- `operation` (string, 操作类型: memory/trace)
- `params` (object, 操作参数)
  - memory 操作: action(store/recall/query), key, value, namespace
  - trace 操作: action(start/end/log), event_name, metadata, trace_id

### 输出格式
- memory 操作: 存储确认，含 key, status, timestamp
- trace 操作: 审计日志，含 trace_id, event_name, timestamp, status

### 调用示例
```
google_adk_operation.operation(operation="memory", params={"action": "store", "key": "session_context", "value": "用户偏好：中文输出", "namespace": "user_prefs"})
google_adk_operation.operation(operation="trace", params={"action": "log", "event_name": "tool_invocation", "metadata": {"tool": "searxng_search", "duration_ms": 1200}, "trace_id": "trace-001"})
```

## 穷尽重试策略
- **穷尽重试替代路径**: Google ADK → 纯文件 NRSF-Summary + 本地日志
- **触发条件**: Google ADK SDK 不可用或服务连接失败

## MCP 适配
- **MCP Tool 名称**: google_adk_operation
- **MCP 参数**: operation, params

## 依赖
- Google ADK SDK

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