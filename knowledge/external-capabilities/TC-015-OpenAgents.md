<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

# OpenAgents

## 基本信息
- **卡片编号**: #15
- **类型**: TC
- **优先级**: P1
- **层级**: L0

## 功能描述
OpenAgents MCP+A2A 协议框架，122 张能力卡片通过 MCP Tool 协议注册和调用，子代理间通过 A2A 协议传递消息。提供统一的多代理协作基础设施，支持工具发现、能力注册、消息路由和任务编排，是全域深度认知框架的代理间通信核心。

## 调用指令

### 输入参数
- `protocol` (string, 协议类型: mcp/a2a)
- `tool_name` (string, MCP 模式必需，目标工具名称)
- `params` (object, MCP 模式必需，工具调用参数)
- `message` (string, A2A 模式必需，传递消息内容)
- `target` (string, A2A 模式必需，目标代理标识)

### 输出格式
- MCP → 工具调用结果 JSON
- A2A → 消息确认含 message_id、status

### 调用示例
```
openagents.call(protocol="mcp", tool_name="searxng_search", params={"query": "AI趋势", "language": "zh"})
openagents.call(protocol="a2a", message="请执行深度研究任务T03", target="research_agent")
```

## 穷尽重试策略
- **穷尽重试替代路径**: OpenAgents → 直接函数调用
- **触发条件**: MCP 服务不可用或 A2A 消息路由失败

## MCP 适配
- **MCP Tool 名称**: openagents_call
- **MCP 参数**: protocol, tool_name, params, message, target

## 依赖
- OpenAgents 服务部署 + MCP Server + A2A 消息中间件

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