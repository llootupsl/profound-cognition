<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

# DeerFlow

## 基本信息
- **卡片编号**: #6
- **类型**: TC
- **优先级**: P0
- **层级**: L1

## 功能描述
并行编排框架，将全串行 DAG 改为 4 个并行组（G1-G4），Orchestrator 作为 DAG 状态机持有者。支持部分失败处理。

## 调用指令

### 输入参数
- `research_id` (string, 研究标识)
- `parallel_group` (string, 并行组: G1|G2|G3|G4)
- `tasks` (array, 任务列表，每项含 task_id/context_package/nrsf_path)
- `callback` (object, 含 on_complete/on_partial_failure)

### 输出格式
YAML 格式响应，含 research_id/parallel_group/results（每项含 task_id/status/nrsf_section/word_count）/partial_failure_handling

### 调用示例
```
deerflow.execute(research_id="uuid", parallel_group="G2", tasks=[{"task_id":"T03","context_package":{...},"nrsf_path":"nrsf/uuid.md"}])
```

## 穷尽重试策略
- **穷尽重试替代路径**: DeerFlow → 串行 Orchestrator
- **触发条件**: DeerFlow 服务不可用

## MCP 适配
- **MCP Tool 名称**: deerflow_execute
- **MCP 参数**: research_id, parallel_group, tasks, callback

## 依赖
- DeerFlow 服务部署

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