<!-- 作者：阿洋 -->

# 执行遥测报告目录 (Execution Telemetry Reports)

## 目录用途

本目录存放 Profound Cognition v6.0 框架执行会话的遥测报告。每个会话结束后，框架自动生成执行遥测报告并写入本目录，用于复盘执行过程、定位性能瓶颈、优化资源分配。

## 报告来源

- **执行遥测报告**：由 `protocols/execution-protocol.md §7.4` 定义的会话后聚合报告
- **Token 计数聚合报告**：由 `protocols/context-budget-protocol.md §3.5.3` 定义的 token 计数聚合报告

## 文件命名规范

### 执行遥测报告

```
telemetry-report_{session_id}_{YYYYMMDD}.json
```

示例：`telemetry-report_uuid-1234-abcd_20260625.json`

### Token 计数聚合报告

```
token-count-report_{session_id}.json
```

示例：`token-count-report_uuid-1234-abcd.json`

## 报告格式（JSON Schema）

### 执行遥测报告 Schema

```json
{
  "session_id": "string — 会话唯一标识",
  "session_start": "ISO8601 — 会话起始时间",
  "session_end": "ISO8601 — 会话结束时间",
  "total_duration_seconds": "float — 会话总耗时（秒）",
  "total_nodes_executed": "integer — 执行的节点总数",
  "total_input_tokens": "integer — 累计输入 token 数",
  "total_output_tokens": "integer — 累计输出 token 数",
  "total_retries": "integer — 累计重试次数",

  "top5_execution_time": [
    {
      "node_id": "string — 节点 ID",
      "duration_seconds": "float — 执行耗时（秒）",
      "percent": "float — 占总会话耗时的百分比"
    }
  ],

  "top5_token_consumption": [
    {
      "node_id": "string — 节点 ID",
      "input_tokens": "integer — 输入 token 数",
      "output_tokens": "integer — 输出 token 数",
      "total": "integer — 总 token 数"
    }
  ],

  "top5_retry_count": [
    {
      "node_id": "string — 节点 ID",
      "retry_count": "integer — 重试次数",
      "last_verdict": "string — 最终判定（PASS/PASS_WITH_WARNINGS/FAIL）"
    }
  ],

  "gate_pass_rate": {
    "gate_alpha": {
      "verdict": "string — Gate-α 判定",
      "retry_count": "integer — 重试次数",
      "duration_seconds": "float — Gate 检查耗时"
    },
    "gate_beta": { "verdict": "...", "retry_count": 0, "duration_seconds": 0.0 },
    "gate_gamma": { "verdict": "...", "retry_count": 0, "duration_seconds": 0.0 },
    "gate_terminal": { "verdict": "...", "retry_count": 0, "duration_seconds": 0.0 },
    "gate_delta": { "verdict": "...", "retry_count": 0, "duration_seconds": 0.0 },
    "overall_pass_rate": "float — Gate 总通过率（0-1）"
  },

  "optimization_suggestions": [
    "string — 基于遥测数据自动生成的优化建议"
  ]
}
```

### Token 计数聚合报告 Schema

```json
{
  "session_id": "string — 会话唯一标识",
  "total_count_events": "integer — token 计数事件总数",
  "method_distribution": {
    "tiktoken": "integer — 使用 tiktoken 计数的次数",
    "char_estimate": "integer — 回退到字符估算的次数"
  },
  "threshold_distribution": {
    "GREEN": "integer — 处于 GREEN 级别的计数次数",
    "YELLOW": "integer",
    "RED": "integer",
    "FORCE_FLUSH": "integer"
  },
  "peak_budget_percent": "float — 峰值预算百分比",
  "peak_trigger_node": "string — 峰值出现时的节点 ID",
  "total_released_tokens": "integer — 累计释放的 token 数",
  "llmlingua_compression_stats": {
    "total_compressions": "integer — LLMLingua 压缩总次数",
    "avg_compression_ratio": "float — 平均压缩率",
    "avg_tokens_saved": "float — 平均节省 token 数"
  },
  "checkpoint_flush_stats": {
    "total_flushes": "integer — Checkpoint 落盘总次数",
    "avg_flush_tokens": "float — 平均每次落盘释放的 token 数"
  }
}
```

## 报告示例

### 执行遥测报告示例

```json
{
  "session_id": "uuid-1234-abcd",
  "session_start": "2026-06-25T10:00:00.000Z",
  "session_end": "2026-06-25T11:12:30.000Z",
  "total_duration_seconds": 4350.0,
  "total_nodes_executed": 57,
  "total_input_tokens": 285000,
  "total_output_tokens": 92000,
  "total_retries": 8,
  "top5_execution_time": [
    {"node_id": "T15", "duration_seconds": 125.3, "percent": 2.88},
    {"node_id": "T09", "duration_seconds": 98.7, "percent": 2.27},
    {"node_id": "T13", "duration_seconds": 87.2, "percent": 2.00},
    {"node_id": "T02", "duration_seconds": 65.4, "percent": 1.50},
    {"node_id": "T17", "duration_seconds": 52.1, "percent": 1.20}
  ],
  "top5_token_consumption": [
    {"node_id": "T15", "input_tokens": 25000, "output_tokens": 8000, "total": 33000},
    {"node_id": "T09", "input_tokens": 18000, "output_tokens": 12000, "total": 30000},
    {"node_id": "T13", "input_tokens": 22000, "output_tokens": 6500, "total": 28500},
    {"node_id": "T02", "input_tokens": 5000, "output_tokens": 15000, "total": 20000},
    {"node_id": "T06", "input_tokens": 12000, "output_tokens": 7500, "total": 19500}
  ],
  "top5_retry_count": [
    {"node_id": "T13", "retry_count": 4, "last_verdict": "PASS"},
    {"node_id": "T09", "retry_count": 2, "last_verdict": "PASS"},
    {"node_id": "T17", "retry_count": 1, "last_verdict": "PASS_WITH_WARNINGS"},
    {"node_id": "T05", "retry_count": 1, "last_verdict": "PASS"},
    {"node_id": "T15", "retry_count": 0, "last_verdict": "PASS"}
  ],
  "gate_pass_rate": {
    "gate_alpha": {"verdict": "PASS", "retry_count": 1, "duration_seconds": 12.3},
    "gate_beta": {"verdict": "PASS", "retry_count": 2, "duration_seconds": 18.7},
    "gate_gamma": {"verdict": "PASS", "retry_count": 0, "duration_seconds": 8.5},
    "gate_terminal": {"verdict": "PASS", "retry_count": 0, "duration_seconds": 15.2},
    "gate_delta": {"verdict": "PASS", "retry_count": 1, "duration_seconds": 22.1},
    "overall_pass_rate": 1.0
  },
  "optimization_suggestions": [
    "T15 执行时间占比 2.88%，建议优化领域引擎分析效率",
    "T13 重试 4 次，建议检查 Supervisor 检查项是否过于严格",
    "Gate-β 重试 2 次，建议检查 T08-T13 流水线质量"
  ]
}
```

## 报告保留策略

- 最近 100 个会话的遥测报告永久保留
- 超过 100 个的旧报告自动归档到 `docs/telemetry/archive/`
- 归档报告超过 1 年自动删除

## 隐私与安全

- 遥测报告仅包含执行指标（时间/token 数/重试次数/Gate 结果），**不包含**用户原始问题、节点输出内容、Persona 信息
- 遥测报告可安全地用于跨会话性能分析与基准测试
- 若用户要求删除遥测数据，可直接删除本目录下的对应 JSON 文件

## 交叉引用

- [protocols/execution-protocol.md §7](../protocols/execution-protocol.md) — 执行遥测协议定义
- [protocols/context-budget-protocol.md §3.5](../protocols/context-budget-protocol.md) — Token 计数日志定义
