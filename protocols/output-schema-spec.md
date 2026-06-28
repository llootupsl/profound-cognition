> **作者**: 阿洋

# Output Schema 统一规范 (Output Schema Unified Specification)

> **状态**: 正式发布 (v3.0)
> **适用范围**: Profound Cognition — 全部 58 节点任务文件
> **最后更新**: 2026-06-25
> **关联任务**: Task 4.15 (D2.4.1 / D2.4.2 / D2.4.3)

> **职责边界声明（D3.4.1）**：本协议负责**任务文件 output_schema 的格式统一与类型校验规范**——定义 JSON Schema 元格式、context_package 类型校验机制、self_check_before_output 量化标准。本协议**不定义**研究状态存储格式（那是 `nrsf-protocol.md` 的职责），也不定义内容密度与长度展开规则（那是 `output-expansion-protocol.md` 的职责）。三者正交：NRSF 提供"存什么"，output-expansion 提供"展开多深"，本协议提供"字段类型如何校验"。详见 `docs/protocol-dependency-graph.md` §4.2。

---

## 1. 目的与范围

本规范定义 Profound Cognition 框架中全部 57 个任务节点 `output_schema` 的统一 JSON Schema 格式（D2.4.1）、`context_package` 类型校验机制（D2.4.2）、以及 `self_check_before_output` 量化标准（D2.4.3）。

### 1.1 适用对象

- `tasks/` 目录下全部任务文件的 `## output_schema` 章节
- `tasks/` 目录下全部任务文件的 `## self_check_before_output` 章节
- 节点间传递的 `context_package` 数据结构
- `supervisors/checks/` 下全部 check YAML 的校验执行依据

### 1.2 核心原则

- **统一格式**: 所有 output_schema 必须遵循 JSON Schema 元格式（Draft 2020-12）
- **类型可校验**: 所有字段必须声明 JSON Schema 兼容的类型
- **量化标准**: self_check_before_output 必须包含可量化的通过判据
- **向后兼容**: 现有 YAML/JSON 描述性定义视为语义等价，不强制重写

---

## 2. JSON Schema 统一格式规范 (D2.4.1)

### 2.1 元格式定义

每个任务文件的 `## output_schema` 章节必须遵循以下 JSON Schema 元格式。该元格式基于 [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/schema)：

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "profound-cognition/tasks/<task_id>.output_schema.json",
  "title": "<Task ID> Output Schema",
  "description": "<节点输出说明>",
  "type": "object",
  "required": ["<必填字段1>", "<必填字段2>"],
  "properties": {
    "<field_name>": {
      "type": "string|number|integer|boolean|array|object|null",
      "description": "<字段说明（≥10字）>",
      "enum": ["<可选枚举值1>", "<可选枚举值2>"],
      "items": { },
      "properties": { },
      "required": ["<子字段必填项>"],
      "minimum": 0,
      "maximum": 100
    }
  }
}
```

### 2.2 格式规则

| 规则 ID | 规则名称 | 要求 | 严重级别 |
|---------|----------|------|----------|
| R1 | 类型声明 | 每个字段必须声明 `type`（JSON Schema 七大基本类型之一：string/number/integer/boolean/array/object/null） | CRITICAL |
| R2 | 描述完整 | 每个字段必须含 `description`（≥10字），说明字段语义与取值含义 | MAJOR |
| R3 | 必填标注 | 顶层对象必须含 `required` 数组，列出所有必填字段 | CRITICAL |
| R4 | 枚举约束 | 取值有限的字段必须用 `enum` 声明所有合法值（如 `"enum": ["LOW","MEDIUM","HIGH","CRITICAL"]`） | MAJOR |
| R5 | 数组定义 | `type: array` 的字段必须含 `items` 定义元素结构 | CRITICAL |
| R6 | 对象定义 | `type: object` 的字段必须含 `properties` 定义子字段 | CRITICAL |
| R7 | 嵌套深度 | 最大嵌套深度 4 层（防止过度复杂，超出需拆分子 schema） | MINOR |
| R8 | execution_params | 所有节点必须含 `execution_params` 字段（R2-05 防深度缩水） | CRITICAL |
| R9 | applied_models | T08-T13 必须含 `applied_models` 字段（R5-01 思维模型路由） | CRITICAL |
| R10 | kg_call_log | 调用 KG 的节点必须含 `kg_call_log` 字段（R5-04 KG 集成验证） | CRITICAL |
| R11 | new_discoveries | 研究类节点必须含 `new_discoveries` 字段（至少 1 条发现） | CRITICAL |
| R12 | upstream_issues | TM03-TM06 必须含 `upstream_issues` 字段（R4-05 TM 层反馈） | MAJOR |

### 2.3 类型映射表

现有任务文件中 YAML/JSON 描述性类型与 JSON Schema 类型的映射关系：

| 现有描述 | JSON Schema type | 说明 |
|----------|------------------|------|
| `string` / `str` / `"文本"` | `string` | 字符串 |
| `int` / `integer` | `integer` | 整数 |
| `float` / `number` | `number` | 浮点数 |
| `bool` / `true\|false` | `boolean` | 布尔值 |
| `array` / `[…]` | `array` | 数组（需配 `items`） |
| `object` / `{…}` | `object` | 对象（需配 `properties`） |
| `"枚举值1\|枚举值2"` | `string` + `enum` | 枚举字符串 |

### 2.4 兼容性声明

现有任务文件中已有的 YAML/JSON 描述性定义视为**语义等价**——只要字段名、类型、必填性、枚举值与 JSON Schema 元格式一致，即视为符合本规范。本规范**不强制重写**已有字段定义，但要求：

1. 每个任务文件的 `## output_schema` 章节头部必须引用本规范（见 §2.5）
2. 新增/修改字段时必须遵循 JSON Schema 元格式
3. `supervisors/checks/` 下的 check YAML 以本规范为校验执行依据

### 2.5 引用声明（D2.4.1 统一标记）

每个任务文件的 `## output_schema` 章节必须在开头包含以下引用声明：

```
> **JSON Schema 规范 (D2.4.1)**: 本节点 output_schema 遵循 `protocols/output-schema-spec.md` 定义的 JSON Schema 统一格式。字段类型遵循 JSON Schema Draft 2020-12 规范。
```

---

## 3. context_package 类型校验机制 (D2.4.2)

### 3.1 context_package JSON Schema

`context_package` 是节点间传递的上下文数据结构，其类型校验基于以下 JSON Schema：

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "profound-cognition/context_package.schema.json",
  "title": "Context Package",
  "description": "节点间传递的上下文数据结构",
  "type": "object",
  "required": ["source_node", "target_node", "payload", "metadata"],
  "properties": {
    "source_node": {
      "type": "string",
      "description": "产出该 context_package 的上游节点 ID",
      "pattern": "^T[0-9]{2}[a-z]?|TM[0-9]{2}[a-z]?|I[0-9]{2}$"
    },
    "target_node": {
      "type": "string",
      "description": "消费该 context_package 的下游节点 ID",
      "pattern": "^T[0-9]{2}[a-z]?|TM[0-9]{2}[a-z]?|I[0-9]{2}$"
    },
    "payload": {
      "type": "object",
      "description": "上下文内容，结构由 source_node 的 output_schema 决定",
      "required": ["data"],
      "properties": {
        "§ref": {
          "type": "string",
          "description": "NRSF 叙事引用栈帧（R3-04 版本管理）",
          "pattern": "^§ref:[A-Z0-9]+:.+:v[0-9]+$"
        },
        "data": {
          "description": "实际数据，符合 source_node 的 output_schema"
        }
      }
    },
    "metadata": {
      "type": "object",
      "description": "上下文元数据",
      "required": ["timestamp", "output_hash", "version"],
      "properties": {
        "timestamp": {
          "type": "string",
          "format": "date-time",
          "description": "产出时间戳"
        },
        "output_hash": {
          "type": "string",
          "pattern": "^[a-f0-9]{64}$",
          "description": "SHA-256 哈希（R10-07 执行哈希验证）"
        },
        "version": {
          "type": "string",
          "pattern": "^v[0-9]+$",
          "description": "版本号（R3-04 §ref 版本管理）"
        },
        "retry_instruction": {
          "type": "object",
          "description": "重试反馈（R7-01），仅重试时存在",
          "properties": {
            "failure_reason": {"type": "string"},
            "improvement_suggestion": {"type": "string"},
            "reference_example": {"type": "string"}
          }
        }
      }
    },
    "recommended_thinking_models": {
      "type": "array",
      "description": "T00 推荐的思维模型列表（R5-01），仅 T00→下游传递时存在",
      "items": {
        "type": "object",
        "required": ["model_id", "activation_reason", "usage_scope"],
        "properties": {
          "model_id": {"type": "string"},
          "activation_reason": {"type": "string"},
          "usage_scope": {"type": "string"}
        }
      }
    },
    "upstream_issues": {
      "type": "array",
      "description": "TM 层反馈机制（R4-05），仅 Gate-δ 触发时存在",
      "items": {
        "type": "object",
        "required": ["issue", "source_tm_node", "feedback_count"],
        "properties": {
          "issue": {"type": "string"},
          "source_tm_node": {"type": "string"},
          "feedback_count": {"type": "integer", "minimum": 1, "maximum": 3}
        }
      }
    }
  }
}
```

### 3.2 校验机制

| 校验项 | 校验规则 | 失败处理 | 关联需求 |
|--------|----------|----------|----------|
| 类型校验 | `payload.data` 必须符合 `source_node` 的 output_schema | 拒绝接收，触发上游重试 | D2.4.2 |
| §ref 解析 | `payload.§ref` 必须存在于 NRSF | 报错，不静默跳过 | R3-04 |
| 哈希校验 | `metadata.output_hash` 必须与上游实际输出 SHA-256 一致 | 触发从 checkpoint 恢复 | R10-07 |
| 版本校验 | `metadata.version` 必须为最新或显式指定的历史版本 | 默认取最新，否则按 context_package 指定 | R3-04 |
| 反馈防循环 | `upstream_issues.feedback_count` ≤ 3 | 超过 3 次不再反馈，标注 [FEEDBACK_EXHAUSTED] | R4-05 |
| 节点 ID 格式 | `source_node` / `target_node` 必须匹配节点 ID 正则 | 拒绝接收，报错 | D2.4.2 |
| 重试指令 | `metadata.retry_instruction` 仅在重试场景存在 | 非重试场景忽略该字段 | R7-01 |

### 3.3 校验执行时机

1. **节点启动时**: 下游节点读取 context_package 前执行类型校验（D2.4.2）
2. **Gate 检查时**: Gate 节点验证所有上游 context_package 的哈希链（R10-07）
3. **重试时**: `retry_instruction` 注入 context_package 前校验其结构（R7-01）
4. **TM 层反馈时**: Gate-δ 检查时校验 `upstream_issues` 的 `feedback_count`（R4-05）

### 3.4 校验失败处理流程

```
context_package 校验失败
  │
  ├─ 类型不匹配 → 拒绝接收 → 触发上游节点重试（R7-01）
  ├─ §ref 不存在 → 报错（不静默跳过）→ 标注 [REF_NOT_FOUND]
  ├─ 哈希不匹配 → 从 checkpoint 恢复上游输出 → 重新执行下游（R10-08）
  ├─ 版本不存在 → 报错 → 标注 [VERSION_NOT_FOUND]
  └─ feedback_count > 3 → 不再反馈 → 标注 [FEEDBACK_EXHAUSTED]
```

---

## 4. self_check_before_output 量化标准 (D2.4.3)

### 4.1 量化通过判据

每个任务文件的 `## self_check_before_output` 章节的检查项必须满足以下量化通过判据：

| 检查类别 | 通过判据 | 失败处理 | 严重级别 |
|----------|----------|----------|----------|
| 结构性检查 (S) | 100% 通过（所有 required_fields 存在） | CRITICAL，必须重试 | CRITICAL |
| 深度检查 (D) | ≥ 90% 通过（CRITICAL 项 100%，MAJOR 项 ≥ 80%） | CRITICAL 项必须重试 | CRITICAL/MAJOR |
| 完整性检查 (I) | 100% 通过（所有数字/事实有来源标注） | CRITICAL，必须重试 | CRITICAL |
| 合规性检查 (C) | 100% 通过（P1-P5 宪法条款） | CRITICAL，必须重试 | CRITICAL |
| R5-01 检查 | applied_models 字段存在且非空（仅 T08-T13） | CRITICAL，必须重试 | CRITICAL |
| R3-05 检查 | 攻击质量自检通过（仅 T10/T11/T12） | CRITICAL，必须重试 | CRITICAL |

### 4.2 量化评分公式

```
self_check_score = (通过项数 / 总项数) × 100

等级划分:
- A (≥95): 优秀，可直接输出
- B (85-94): 合格，可输出但标注 [MINOR_ISSUES]
- C (70-84): 边缘，必须重试改进
- D (<70): 不合格，必须重试并升级处理（R7-01 连续 3 次重试未通过升级）
```

### 4.3 检查项分类标准

每个 self_check_before_output 检查项必须标注以下属性（与 `supervisors/checks/` YAML 对齐）：

```yaml
check_item:
  id: "S01|D01|I01|C01"  # 检查项 ID（与 check YAML 一致）
  category: "structural|depth|integrity|constitution|r5_01|r3_05"
  severity: "CRITICAL|MAJOR|MINOR"
  quantified_criteria: "可量化的通过判据（如 ≥3, =100%, 非空, ≥0.85 等）"
  failure_action: "retry|warn|block"
```

### 4.4 最低检查项数量

| 任务类型 | 最低检查项数 | 包含检查类别 |
|----------|--------------|--------------|
| Gate 节点 (T07/T14/T16/T28/T_gate_delta) | ≥ 8 项 | S + D + I + C |
| 认知节点 (T08/T09/T13) | ≥ 10 项 | S + D + I + C + R5-01 |
| 对抗节点 (T10/T11/T12/T12b) | ≥ 8 项 | S + D + I + C + R5-01 + R3-05 |
| 渲染节点 (T20a-T20d/T20) | ≥ 5 项 | S + D + I |
| TM 元层节点 (TM01-TM07) | ≥ 6 项 | S + D + I + C + R4-05 |
| 研究节点 (T02-T06) | ≥ 5 项 | S + D + I |
| 其他节点 | ≥ 5 项 | S + D + I |

### 4.5 量化标准引用声明

每个任务文件的 `## self_check_before_output` 章节必须在开头包含以下引用声明：

```
> **量化标准 (D2.4.3)**: 本节点 self_check_before_output 遵循 `protocols/output-schema-spec.md` §4 定义的量化通过判据。self_check_score ≥ 85 方可输出。
```

---

## 5. 引用关系

### 5.1 被引用方

- 本规范被 `tasks/` 下全部任务文件的 `## output_schema` 章节引用（D2.4.1）
- 本规范被 `tasks/` 下全部任务文件的 `## self_check_before_output` 章节引用（D2.4.3）
- 本规范被 `supervisors/checks/` 下全部 check YAML 引用（校验执行依据）
- 本规范被 `execution-protocol.md` 引用（context_package 传递时校验）

### 5.2 引用方

- 本规范引用 `protocols/nrsf-protocol.md`（§ref 版本管理，R3-04）
- 本规范引用 `protocols/checkpoint-protocol.md`（哈希恢复，R10-07）
- 本规范引用 `knowledge/thinking-models/routing-table.md`（R5-01 思维模型）
- 本规范引用 `SKILL.md`（execution_params 最低值，R2-05）

---

## 6. 变更日志

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-06-25 | 初始版本，定义 D2.4.1 JSON Schema 统一格式、D2.4.2 context_package 类型校验、D2.4.3 self_check_before_output 量化标准 |


---

## 测试用例 (D3.4.4)

### 测试用例 1：JSON Schema 校验通过

**给定输入**：节点 T02 的 output 符合 JSON Schema 规范（包含 task_id、output、nrsf_refs、execution_params 字段，类型正确）。

**应产出**：JSON Schema 校验通过，允许输出。

### 测试用例 2：JSON Schema 校验失败

**给定输入**：节点 T02 的 output 缺少 execution_params 字段。

**应产出**：JSON Schema 校验失败，错误信息"missing required field: execution_params"，触发重试。

### 测试用例 3：self_check 量化标准

**给定输入**：节点 T13 的 self_check_score=88（≥ 85 阈值）。

**应产出**：self_check 通过，允许输出。

### 测试用例 4：self_check 未达阈值

**给定输入**：节点 T13 的 self_check_score=80（< 85 阈值）。

**应产出**：self_check 未通过，触发重试，retry_feedback 注入 context_package。
