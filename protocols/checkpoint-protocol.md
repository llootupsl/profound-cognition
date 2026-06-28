<!-- 作者：阿洋 -->

# 检查点与断点恢复协议 (Checkpoint & Recovery Protocol) v3.0

## 1. 协议概述

**方法论原理**：检查点协议基于"可恢复性是长流程可靠性的基础"的认知假设：长时间运行的认知分析流程可能因中断、错误或资源限制而失败，检查点机制使流程能够从最近的有效状态恢复，避免从头重新执行。

本协议定义认知流水线的检查点保存与断点恢复机制，确保长时间运行的推理任务在中断后可从最近状态恢复，避免重复计算。检查点在每个 Phase 完成后自动触发，保存完整上下文快照。

**触发条件**：每个 Phase（Phase 0-4、Phase 5）完成后自动触发检查点保存；用户再次触发同等任务时触发断点恢复。

## 2. 检查点保存

每个 Phase 完成后自动保存上下文快照：
- phase_id：当前 Phase 编号
- node_completion_status：各节点完成状态映射 {node_id: completed|retrying|skipped}
- core_conclusions：该 Phase 产出的核心结论摘要（≤ 500 字）
- nrsf_position：NRSF 中的当前写入位置

**Phase 4（输出渲染）检查点额外保存**：
- rendered_sections：已渲染的 §1-§8 章节列表及字数
- rendering_artifacts：渲染产物路径（HTML/Markdown/DOCX）
- gate_terminal_status：Gate-终 (T28) 检查状态

**Phase 5（元维度引擎）检查点额外保存**：
- meta_dimensions_status：元维度 9-14 扩展完成状态
- scientific_layer_status：TM01-TM07 科学层 8 模块完成状态
- philosophical_core_status：哲学三元组完成状态
- knowledge_graph_ontology：知识图谱本体导出状态（TM07）

## 3. 断点恢复

用户再次触发同等任务时：
1. 读取最近 checkpoint
2. 从对应 Phase 起点恢复执行
3. 已完成的节点标记为 CACHED，不重新执行

## 4. 增量更新模式

已完成报告支持基于新数据/新证据增量追加：
1. 定位到报告最后一个完整章节
2. 在该章节后追加新的 §N+1 增量章节
3. 增量章节标注数据来源时间和有效期限

## 5. 时间衰减权重

来源越近权重越高：
w(source) = exp(-λ · age_in_days)
- λ = 0.01（默认，来源约 100 天后权重降至 ~0.37）
- 对超过 365 天的来源，权重自动 < 0.03

## 6. 输出规范

```yaml
checkpoint:
  phase_id: "Phase 0|1|2|3|4|7"
  timestamp: "ISO8601时间戳"
  node_completion_status: {node_id: "completed|retrying|skipped|cached"}
  core_conclusions: "该Phase核心结论摘要"
  nrsf_position: "NRSF当前写入位置"
  recovery_point: "恢复执行的起点节点"
  # Phase 4 额外字段
  rendered_sections: ["§1", "§2", ...]
  rendering_artifacts: {html: "path", markdown: "path", docx: "path"}
  gate_terminal_status: "pass|fail|pending"
  # Phase 5 额外字段
  meta_dimensions_status: {dim_9_10: "completed", dim_11_12: "completed", dim_13_14: "completed"}
  scientific_layer_status: {TM01: "completed", TM02: "completed", ..., TM07: "completed"}
  philosophical_core_status: "completed"
  knowledge_graph_ontology: "exported|pending"
```

## 7. 异常处理与穷尽重试

| 异常场景 | 处理策略 |
|---------|---------|
| 检查点文件损坏或丢失 | 从上一个有效检查点恢复；若无任何有效检查点，从头开始执行 |
| 检查点版本不兼容 | 忽略不兼容检查点，从头开始执行，标注"检查点版本不兼容" |
| 恢复后节点状态不一致 | 对CACHED节点执行轻量验证（检查输出字段是否存在），不一致的节点重新执行 |
| 增量更新与已有内容冲突 | 冲突部分标注"时间戳冲突"，保留两个版本供人工裁决 |
| 存储空间不足无法保存检查点 | 持续重试保存直至成功，不设重试上限，不跳过完整上下文快照 |

## 决策规则

| 条件 | 动作 | 优先级 |
|------|------|--------|
| Phase完成且输出通过门控 | 保存检查点 | P0 |
| 长时间运行任务(>30min) | 每15min增量保存 | P1 |
| 用户中断请求 | 立即保存当前状态 | P0 |
| 检查点文件损坏 | 从最近有效检查点恢复 | P0 |
| 增量更新累积>5次 | 压缩为完整检查点 | P2 |
| 恢复后输出与之前不一致 | 重新执行当前Phase | P1 |

## 8. Context-Budget 落盘支持（R2-03 扩展）

> **扩展目的**：本协议原仅支持 Phase 级检查点保存。R2-03 将 context-budget 从「删除」改为「落盘后释放」后，Checkpoint 需扩展支持节点级上下文落盘，使 methodology_notes 和 process_description 等被释放的内容持久化存储，供下游节点按需读取。

### 8.1 落盘触发条件

> **R10-01 阈值同步**：自 R10-01 起，context-budget 阈值已收紧（详见 context-budget-protocol.md §3.1）。本表的触发条件已同步更新。

| 触发源 | 触发条件 | 落盘内容 | 协议引用 |
|--------|---------|---------|---------|
| context-budget YELLOW | 上下文使用量 60%-80% | LLMLingua 压缩后的 methodology_notes + process_description（压缩后仍未回落 GREEN 时落盘） | context-budget-protocol.md §3.2 |
| context-budget RED | 上下文使用量 80%-95% | 全部活跃上下文（含所有分析维度，主动落盘） | context-budget-protocol.md §3.2 |
| context-budget 强制落盘 | 上下文使用量 > 95% | 全部活跃上下文（强制批量写入） | context-budget-protocol.md §4 |

### 8.2 落盘 Checkpoint 格式

```yaml
context_budget_checkpoint:
  checkpoint_type: "yellow_flush|red_flush|force_flush"
  timestamp: "ISO8601时间戳"
  trigger_node: "触发落盘的节点ID"
  budget_percent: "触发时的上下文使用百分比"
  flushed_content:
    methodology_notes:
      - {node_id: "string", content: "string", section_index: "string"}
    process_description:
      - {node_id: "string", content: "string", section_index: "string"}
    # RED/强制落盘时额外包含：
    core_conclusions:
      - {node_id: "string", content: "string", section_index: "string"}
    key_findings:
      - {node_id: "string", content: "string", section_index: "string"}
    supporting_evidence:
      - {node_id: "string", content: "string", section_index: "string"}
    intermediate_results:
      - {node_id: "string", content: "string", section_index: "string"}
  reference_pointers:
    - {node_id: "string", file_path: "Checkpoint文件路径", section_index: "章节索引"}
  released_budget_tokens: "释放的上下文 token 数"
```

### 8.3 下游节点按需加载机制

下游节点执行时，如需读取已落盘的 methodology_notes 或 process_description：
1. 检查 context_package 中的 reference_pointers 字段
2. 根据 file_path + section_index 定位 Checkpoint 文件中的对应章节
3. 按需加载到当前节点的活跃上下文（加载后该部分内容重新计入上下文预算）
4. 加载完成后执行节点逻辑

### 8.4 落盘不构成信息丢失声明

> **R2-03 铁律**：context-budget 落盘后释放 ≠ 删除。落盘后的内容持久化存储在 Checkpoint 文件中，下游节点可通过引用指针按需读取。这与旧版的「删除」有本质区别——删除后信息永久丢失，落盘后释放仅从活跃上下文中移除以腾出预算空间，信息本身完整保留。

## 9. LangGraph Checkpoint 集成（R9-05）

> **集成声明**：自 R9-05 起，Profound Cognition 引入 LangGraph StateGraph 原生编排引擎（能力卡：`knowledge/external-capabilities/TC-100-LangGraph.md`）。LangGraph 的 checkpoint 机制提供状态级技术快照，与本协议原有的 Phase 级业务语义检查点互补共存。

### 9.1 LangGraph checkpoint 自动保存状态

LangGraph 在图执行的每一步自动保存 ResearchState 快照（含 `context_package`、`execution_ledger`、`node_outputs`、`current_phase`），无需手动触发。每个节点执行完成后，checkpointer 自动写入一条 checkpoint 记录。

```python
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.redis import RedisSaver

# 编译时注入 checkpointer，LangGraph 自动在每个节点后保存状态
compiled_graph = graph.compile(
    interrupt_before=["T00b", "I01"],
    checkpointer=checkpointer,  # 自动保存状态
)

# 执行时通过 thread_id 关联 checkpoint 序列
state = compiled_graph.invoke(
    initial_state,
    config={"configurable": {"thread_id": session_id}},
)
```

### 9.2 断点恢复：从最近 checkpoint 恢复

LangGraph 支持从任意 checkpoint 恢复执行。通过 `thread_id` 定位 checkpoint 序列，调用 `invoke(None, config)` 从最近 checkpoint 恢复：

```python
# 从最近 checkpoint 恢复执行（传 None 表示从断点继续）
state = compiled_graph.invoke(
    None,  # None = 从最近 checkpoint 恢复
    config={"configurable": {"thread_id": session_id}},
)

# 查看完整 checkpoint 历史
state_history = list(compiled_graph.get_state_history(
    config={"configurable": {"thread_id": session_id}},
))
# 可定位到任意历史 checkpoint，从该点分叉重执行
```

### 9.3 checkpoint 存储：支持内存/文件/Redis 后端

LangGraph checkpointer 支持三种存储后端，按持久性需求选择：

| 后端 | 类 | 持久性 | 适用场景 | 配置 |
|------|-----|--------|---------|------|
| 内存 | `MemorySaver` | 进程级（重启丢失） | 开发调试、单次执行 | `MemorySaver()` |
| 文件 | `SqliteSaver` | 持久（SQLite 文件） | 单机生产、断点恢复 | `SqliteSaver.from_conn_string("checkpoints.db")` |
| Redis | `RedisSaver` | 持久（分布式） | 多实例、高可用 | `RedisSaver.from_conn_info(host, port)` |

```python
# 按场景选择后端
if checkpoint_backend == "memory":
    checkpointer = MemorySaver()
elif checkpoint_backend == "file":
    checkpointer = SqliteSaver.from_conn_string("checkpoints.db")
elif checkpoint_backend == "redis":
    checkpointer = RedisSaver.from_conn_info(host="localhost", port=6379)
```

### 9.4 与现有 Checkpoint 协议的兼容性说明

本协议原有的 Phase 级业务语义检查点（§2-§7）与 LangGraph 状态级技术检查点（§9）互补共存，二者不冲突：

| 维度 | 现有 Phase 级检查点（§2-§7） | LangGraph 状态级检查点（§9） |
|------|---------------------------|---------------------------|
| **粒度** | Phase 级（每个 Phase 完成后） | 节点级（每个节点完成后自动） |
| **内容** | 业务语义（core_conclusions、nrsf_position、rendered_sections 等） | 技术状态（ResearchState：context_package、execution_ledger、node_outputs） |
| **触发** | Phase 完成后手动/半自动触发 | LangGraph 引擎自动触发 |
| **恢复** | 从对应 Phase 起点恢复 | 从任意节点 checkpoint 恢复 |
| **存储** | NRSF 文件 / Checkpoint YAML | 内存 / SQLite / Redis |

**兼容性规则**：
1. **共存**：LangGraph checkpoint 不替代现有 Phase 级检查点。Phase 级检查点保存业务语义（如 rendered_sections、gate_terminal_status），LangGraph checkpoint 保存技术状态（如 node_outputs、execution_ledger）。二者各自不可替代。
2. **恢复优先级**：断点恢复时，优先从 LangGraph checkpoint 恢复技术状态（节点级粒度更细），再叠加 Phase 级检查点的业务语义字段。
3. **回退兼容**：若 LangGraph 不可用，回退到现有 Phase 级检查点协议（§2-§7），功能不降级（仅失去节点级粒度的断点恢复能力）。
4. **Context-Budget 落盘**：§8 的 context-budget 落盘机制独立于 LangGraph checkpoint，二者各自工作。LangGraph checkpoint 保存完整 ResearchState，context-budget 落盘保存被释放的上下文片段，下游节点可同时引用两者。

## 10. 跨会话检查点（R10-03/R9-08 扩展）

> **扩展目的**：本协议原仅支持单会话内的检查点保存与恢复。R10-03/R9-08 引入跨会话记忆系统（Mem0）后，Checkpoint 需扩展为跨会话检查点，使用户能在新会话中恢复历史会话的执行状态，实现"断点续研"。本章节定义跨会话检查点的格式、写入时机、恢复流程与衰减规则。完整跨会话记忆协议见 [cross-session-memory-protocol.md](./cross-session-memory-protocol.md)。

### 10.1 跨会话检查点格式

跨会话检查点是对现有 Phase 级检查点（§2-§7）和 LangGraph checkpoint（§9）的扩展，增加跨会话恢复所需的元数据与记忆引用：

```yaml
cross_session_checkpoint:
  checkpoint_id: "string — 跨会话检查点唯一标识（cscp_{uuid}）"
  user_id: "string — 用户唯一标识"
  original_session_id: "string — 原始会话 ID"
  new_session_id: "string — 新会话 ID（恢复时生成）"
  created_at: "ISO8601"

  # 恢复点信息
  recovery_point:
    phase_id: "integer — 原始会话中断时的 Phase（1-5）"
    node_completion_status: {node_id: "completed | retrying | pending"}
    last_completed_node: "string — 最后完成的节点 ID"
    next_node: "string — 下一个待执行的节点 ID"

  # 恢复内容（从 LangGraph checkpoint 提取）
  restorable_content:
    context_package: "dict — 原始会话的 context_package 快照"
    node_outputs: "dict — 已完成节点的输出"
    execution_ledger: "list — 执行账本"
    nrsf_position: "string — NRSF 写入位置"

  # 跨会话记忆引用（指向 Mem0 中的记忆条目）
  memory_references:
    preference_memory_id: "string — 用户偏好记忆 ID"
    conclusion_memory_ids: ["string — 历史结论记忆 ID 列表"]
    unsolved_memory_ids: ["string — 未解决问题记忆 ID 列表"]

  # 衰减状态（见 §10.4）
  decay_status:
    checkpoint_age_days: "integer — 检查点创建后的天数"
    decay_weight: "float — 衰减权重（0-1）"
    restorable: "boolean — 是否可恢复（衰减权重 > 0.3 时可恢复）"
```

### 10.2 跨会话检查点写入时机

| 时机 | 触发条件 | 写入内容 | 存储位置 |
|------|---------|---------|---------|
| 用户主动中止会话 | 用户发送"中止"信号 | 当前完整执行状态 | Mem0（checkpoint 层） |
| 会话超时 | 会话超过 24 小时未活动 | 当前完整执行状态 | Mem0（checkpoint 层） |
| Phase 完成后 | 每个 Phase 完成后 | Phase 级检查点（增量） | Mem0（checkpoint 层） |
| 用户请求保存 | 用户发送"保存进度" | 当前完整执行状态 | Mem0（checkpoint 层） |

### 10.3 跨会话恢复流程

```python
def resume_cross_session(user_id: str, original_session_id: str) -> dict:
    """跨会话恢复执行状态（R10-03/R9-08）。

    Args:
        user_id: 用户 ID
        original_session_id: 原始会话 ID

    Returns:
        恢复结果
    """
    from mem0 import Memory
    memory = Memory()

    # 1. 从 Mem0 检索跨会话检查点
    checkpoint = memory.search(
        query=f"checkpoint:{original_session_id}",
        user_id=user_id,
        memory_layer="checkpoint",
        limit=1,
    )

    # 2. 检查衰减状态
    if not checkpoint or not checkpoint[0]["decay_status"]["restorable"]:
        return {
            "status": "not_restorable",
            "reason": "checkpoint_decayed_or_not_found",
        }

    # 3. 恢复执行状态
    cp = checkpoint[0]
    restored_state = {
        "context_package": cp["restorable_content"]["context_package"],
        "node_outputs": cp["restorable_content"]["node_outputs"],
        "execution_ledger": cp["restorable_content"]["execution_ledger"],
        "current_phase": cp["recovery_point"]["phase_id"],
    }

    # 4. 标记已完成节点为 CACHED（不重新执行）
    for node_id, status in cp["recovery_point"]["node_completion_status"].items():
        if status == "completed":
            restored_state["node_outputs"][node_id]["_cached"] = True

    # 5. 注入跨会话记忆引用
    restored_state["context_package"]["memory_references"] = cp["memory_references"]

    # 6. 生成新会话 ID
    new_session_id = generate_uuid()
    restored_state["session_id"] = new_session_id

    # 7. 向用户展示恢复摘要
    print(f"已恢复会话 {original_session_id} 的执行状态：")
    print(f"  - 恢复点：Phase {cp['recovery_point']['phase_id']}, 节点 {cp['recovery_point']['last_completed_node']}")
    print(f"  - 下一节点：{cp['recovery_point']['next_node']}")
    print(f"  - 已完成节点：{sum(1 for s in cp['recovery_point']['node_completion_status'].values() if s == 'completed')} 个")
    print(f"  - 新会话 ID：{new_session_id}")

    return {
        "status": "restored",
        "new_session_id": new_session_id,
        "restored_state": restored_state,
        "next_node": cp["recovery_point"]["next_node"],
    }
```

### 10.4 跨会话检查点衰减

跨会话检查点遵循艾宾浩斯遗忘曲线衰减（详见 cross-session-memory-protocol.md §4）：

| 检查点年龄 | 衰减权重 | 处理 |
|-----------|---------|------|
| < 15 天 | > 0.37 | 正常可恢复 |
| 15-30 天 | 0.14-0.37 | 可恢复，但标注"检查点较旧" |
| 30-60 天 | 0.02-0.14 | 标记"弱检查点"，恢复前向用户确认 |
| > 60 天 | < 0.02 | 不可恢复，自动删除 |

> **衰减例外**：用户显式标记为"永久保存"的检查点不衰减（如重要研究的断点）。

### 10.5 与现有检查点机制的关系

跨会话检查点（§10）与现有检查点机制互补共存：

| 维度 | Phase 级检查点（§2-§7） | LangGraph checkpoint（§9） | 跨会话检查点（§10） |
|------|---------------------------|---------------------------|---------------------------|
| **粒度** | Phase 级 | 节点级 | 会话级 |
| **存储** | NRSF 文件 / YAML | 内存 / SQLite / Redis | Mem0（跨会话持久化） |
| **生命周期** | 单会话 | 单会话 | 跨会话（带衰减） |
| **恢复范围** | Phase 起点恢复 | 节点级恢复 | 跨会话恢复 |
| **衰减** | 不衰减 | 不衰减 | 艾宾浩斯遗忘曲线 |

**协作规则**：
1. 会话内恢复优先使用 LangGraph checkpoint（粒度最细）
2. 跨会话恢复使用跨会话检查点（§10），恢复后叠加 LangGraph checkpoint 的节点级状态
3. 三种检查点各自独立工作，互不干扰

---

## 测试用例 (D3.4.4)

### 测试用例 1：Phase 级检查点保存

**给定输入**：Phase 1（研究底座）完成，T01-T06 全部节点状态为 completed，核心结论摘要为"全球经济秩序重建的核心叙事"。

**应产出**：检查点保存 phase_id=Phase 1，node_completion_status 包含 T01-T06 全部 completed，core_conclusions 非空（≤500 字），nrsf_position 指向当前 NRSF 写入位置。

### 测试用例 2：断点恢复

**给定输入**：用户再次触发同等任务，存在最近 checkpoint（phase_id=Phase 2，T07-T13 部分完成）。

**应产出**：从 Phase 2 起点恢复执行，T07-T13 中已完成的节点标记为 CACHED 不重新执行，未完成节点继续执行。

### 测试用例 3：时间衰减权重

**给定输入**：来源 A 发布于 10 天前，来源 B 发布于 200 天前，λ=0.01。

**应产出**：来源 A 权重 w=exp(-0.01×10)≈0.905，来源 B 权重 w=exp(-0.01×200)≈0.135。来源 B 权重 < 0.37 阈值，标注"检查点较旧"。

### 测试用例 4：跨会话检查点衰减

**给定输入**：跨会话检查点年龄 45 天，未标注"永久保存"。

**应产出**：衰减权重 0.02-0.14，标注"弱检查点"，恢复前向用户确认。
