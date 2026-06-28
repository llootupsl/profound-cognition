> **作者**: 阿洋

# 执行协议 (Execution Protocol)

> > **状态**: 正式发布
> **适用范围**: Profound Cognition 主LLM调度执行参考
> **最后更新**: 2026-05-15

---

## 1. 协议概述

### 1.1 目的

ExecutionProtocol 定义 Profound Cognition 中主LLM的 Phase 0-3 执行规则。该协议建立了基于 DAG 的多任务调度框架，确保 58 个节点按依赖关系有序执行，并通过 Supervisor 门控机制保证每个阶段的产出质量。

### 1.2 核心设计原则

- **DAG 调度优先**: 所有任务通过有向无环图 (DAG) 定义依赖关系，就绪节点并行执行
- **门控通过制**: Phase 1 产出进入 Phase 2 前必须通过 Gate-α/β/γ 检查
- **穷尽重试**: 节点失败时持续重试直至通过，遵循穷尽重试协议
- **上下文压缩传递**: Sub-Agent 间通过 Context Package 标准格式传递上游产出

### 1.3 协议在系统中的位置

```
┌──────────────────────────────────────────┐
│ 用户交互层 (User Input)                  │
├──────────────────────────────────────────┤
│ Phase 0: 初始化 (Main LLM)              │
│   ├── 理解问题 + 生成 DAG               │
│   └── 写入 TodoWrite                    │
├──────────────────────────────────────────┤
│ Phase 1: 执行 (Sub-Agent 并行)          │
│   ├── 找就绪节点                        │
│   ├── 组装 context_package              │
│   ├── 调用 Sub-Agent                    │
│   └── Supervisor 判定                   │
├──────────────────────────────────────────┤
│ Phase 2: 门控 (Gate-α/β/γ)             │
│   ├── Gate-α: T01-T06 研究底座覆盖度检查 │
│   ├── Gate-β: T08-T13 认知流水线检查     │
│   └── Gate-γ: T15 领域引擎覆盖度检查     │
├──────────────────────────────────────────┤
│ Phase 3: 终局 (Orchestrator + 输出)     │
│   ├── 汇总所有节点产出                   │
│   └── 调用 T20 渲染最终输出              │
└──────────────────────────────────────────┘
```

---

## 2. Phase 0 — 初始化

### 2.1 触发条件

主LLM收到用户问题后，立即进入 Phase 0 初始化流程。

### 2.2 初始化步骤

```yaml
phase_0:
  step_0_input_snapshot:
    description: "建立用户输入快照（D14.4.1）— 不可变基线"
    actions:
      - 捕获 raw_input: 用户原始问题文本（未经任何改写）
      - 捕获 timestamp: 输入接收时间（ISO 8601，含时区）
      - 计算 input_hash: SHA-256(raw_input + timestamp)
      - 捕获 input_metadata: {language, encoding: "UTF-8", char_count}
      - 写入 execution_ledger 首条记录，标记为 input_snapshot
      - immutability: 快照一旦创建不可修改，后续所有节点引用此快照作为输入基线
    failure_handling:
      - 若 raw_input 为空 → input_hash = SHA-256("EMPTY" + timestamp)，仍写入 ledger
      - 若 timestamp 解析失败 → fallback 到系统当前时间，记录 warning
    consumer: "T01 输入分流读取 input_snapshot 作为基线；T28 Gate-终 验证 input_hash 与最终输出可追溯"

  step_1_understand:
    description: "完整理解用户问题"
    actions:
      - 提取原始问题核心语义
      - 识别隐含预设与偏见框架
      - 推断成品类型 (output_type)

  step_2_dag_generation:
    description: "生成任务 DAG"
    actions:
      - 加载完整任务依赖定义 (tasks/T_env_probe ~ T_gate_delta，共 58 节点)
      - 根据问题类型裁剪非必要分支
      - 生成最终 DAG JSON

  step_3_todowrite:
    description: "写入 TodoWrite"
    actions:
      - 将 DAG 中所有节点写入 TodoWrite
      - 初始状态全部为 pending
      - T01 标记为就绪 (依赖为空)
```

### 2.3 DAG 定义格式

> **SSOT 声明**：SKILL.md 是 DAG 拓扑的唯一真实源（Single Source of Truth），包含 58 个节点的完整定义。本节仅提供 Phase 1-3 的简化 DAG 示例格式供参考，完整 DAG 拓扑（含 Phase 5 的 20 个元维度/科学层节点，含 TM06b Lean4 形式化验证）以 SKILL.md 为准。若本节与 SKILL.md 冲突，以 SKILL.md 为准。

主LLM生成的 DAG 使用以下结构：

```yaml
dag:
  version: "3.0"
  problem: "用户原始问题"
  output_type: "research_report | wechat_article | course_material"

  nodes:
    - task_id: "T01"
      name: "输入分流"
      phase: 1
      dependencies: []
      gate: "alpha"

    - task_id: "T00"
      name: "研究大纲生成"
      phase: 1
      dependencies: ["T01"]
      gate: "alpha"

    - task_id: "T02"
      name: "L1+L2 研究"
      phase: 1
      dependencies: ["T00"]
      gate: "alpha"

    - task_id: "T03"
      name: "L3 结构分析"
      phase: 1
      dependencies: ["T02"]
      gate: "alpha"

    - task_id: "T04"
      name: "L4+L5 比较叙事"
      phase: 1
      dependencies: ["T02", "T03"]
      gate: "alpha"

    - task_id: "T05"
      name: "L6+L7 证据利益"
      phase: 1
      dependencies: ["T04"]
      gate: "alpha"

    - task_id: "T06"
      name: "L8+L9 反事实边界"
      phase: 1
      dependencies: ["T05"]
      gate: "alpha"

    - task_id: "T07"
      name: "Gate-α 研究底座门控"
      phase: 1
      dependencies: ["T06"]
      gate: "alpha"

    - task_id: "T08"
      name: "认知解构"
      phase: 1
      dependencies: ["T07"]
      gate: "beta"

    - task_id: "T09"
      name: "认知推理"
      phase: 1
      dependencies: ["T08"]
      gate: "beta"

    - task_id: "T10"
      name: "对抗逻辑"
      phase: 1
      dependencies: ["T09"]
      gate: "beta"

    - task_id: "T11"
      name: "对抗证据"
      phase: 1
      dependencies: ["T09"]
      gate: "beta"

    - task_id: "T12"
      name: "对抗范围"
      phase: 1
      dependencies: ["T09"]
      gate: "beta"

    - task_id: "T13"
      name: "认知综合"
      phase: 1
      dependencies: ["T10", "T11", "T12"]
      gate: "beta"

    - task_id: "T14"
      name: "Gate-β 认知流水线门控"
      phase: 1
      dependencies: ["T13"]
      gate: "beta"

    - task_id: "T15"
      name: "领域引擎分析"
      phase: 1
      dependencies: ["T14"]
      gate: "gamma"

    - task_id: "T16"
      name: "Gate-γ 领域分析门控"
      phase: 1
      dependencies: ["T15"]
      gate: "gamma"

    - task_id: "T17"
      name: "质量事实核查"
      phase: 1
      dependencies: ["T16"]
      gate: "gamma"

    - task_id: "T18"
      name: "质量偏差检测"
      phase: 1
      dependencies: ["T16"]
      gate: "gamma"

    - task_id: "T19"
      name: "质量交付检查"
      phase: 1
      dependencies: ["T17", "T18"]
      gate: "gamma"

    - task_id: "T20"
      name: "输出渲染"
      phase: 3
      dependencies: ["T19"]
      gate: "gamma"

  edges:
    - from: "T01"
      to: "T00"
    - from: "T00"
      to: "T02"
    - from: "T02"
      to: "T03"
    - from: "T02"
      to: "T04"
    - from: "T03"
      to: "T04"
    - from: "T04"
      to: "T05"
    - from: "T05"
      to: "T06"
    - from: "T06"
      to: "T07"
    - from: "T07"
      to: "T08"
    - from: "T08"
      to: "T09"
    - from: "T09"
      to: "T10"
    - from: "T09"
      to: "T11"
    - from: "T09"
      to: "T12"
    - from: "T10"
      to: "T13"
    - from: "T11"
      to: "T13"
    - from: "T12"
      to: "T13"
    - from: "T13"
      to: "T14"
    - from: "T14"
      to: "T15"
    - from: "T15"
      to: "T16"
    - from: "T16"
      to: "T17"
    - from: "T16"
      to: "T18"
    - from: "T17"
      to: "T19"
    - from: "T18"
      to: "T19"
    - from: "T19"
      to: "T20"
```

---

## 2.6 节点 tok 预算解析规则

Phase 0 生成 DAG 后，每个节点需根据模式指令解析最终 tok 预算。解析遵循三级优先级（P1→P2→P3），优先级高的覆盖优先级低的。

### 2.6.1 三级优先级定义

| 优先级 | 条件 | 计算方式 | 说明 |
|-------|------|---------|------|
| **P1（最高）** | 节点任务文件定义了 `mode_parameters[execution_mode].tok` | 直接使用该值 | 节点级别的模式感知 tok |
| **P2** | 节点无 mode_parameters.tok，但 SKILL.md §0.0 MODE 表定义了 `tok_multiplier` | `DAG_YAML_tok × tok_multiplier` | 全局倍乘器 |
| **P3（兜底）** | 上述条件均不满足 | 使用 DAG YAML 中的静态 tok 值 | 最低优先级 |

### 2.6.2 计算示例（EXHAUST 模式，tok_multiplier = ×3.0）

| 节点 | P1 tok | P2 计算 | P3 tok | 实际使用 | 来源 |
|------|--------|---------|--------|---------|------|
| T09 | 4000 | 1500×3.0=4500 | 1500 | 4000 | P1 |
| T13 | 无 | 1000×3.0=3000 | 1000 | 3000 | P2 |
| T15 | 4000 | 2500×3.0=7500 | 2500 | 4000 | P1 |
| T01 | 无 | 600×3.0=1800 | 600 | 1800 | P2 |
| T02 | 无 | 1200×3.0=3600 | 1200 | 3600 | P2 |

### 2.6.3 resolve_node_tok 伪代码

```python
def resolve_node_tok(node_id: str, execution_mode: str, dag_tok: int) -> int:
    task_file = load_task_file(node_id)

    if task_file.mode_parameters and execution_mode in task_file.mode_parameters:
        mode_tok = task_file.mode_parameters[execution_mode].get("tok")
        if mode_tok is not None:
            return mode_tok  # P1

    tok_multiplier = get_mode_config(execution_mode).tok_multiplier
    if tok_multiplier is not None and tok_multiplier != 1.0:
        return int(dag_tok * tok_multiplier)  # P2

    return dag_tok  # P3
```

### 2.6.4 模式感知 tok 行为

> **EXHAUST-only 声明**：本框架仅运行 EXHAUST 模式（SKILL.md §0.0），不存在 FLASH/STANDARD/DEEP 模式。以下仅保留 EXHAUST 行为。

| 模式 | tok_multiplier | 行为 |
|------|---------------|------|
| EXHAUST | ×3.0 | 无 P1 的节点 → DAG_tok × 3.0 |

---

## 2.7 T00b 交互等待协议

T00b（输入情绪基调提取）是 DAG 中唯一需要多轮用户对话的节点。

### 2.7.1 执行流程

```
T00b 首轮调用
    ↓
T00b 输出问题集 + validation_status
    ↓
┌──────────────────────────────┐
│ validation_status == COMPLETE? │
└──────────────────────────────┘
    ↓ YES                    ↓ NO
传递 persona_card         进入 WAITING_FOR_USER
DAG 继续                   向用户展示问题集
                                ↓
                          用户提供回答
                                ↓
                         携带历史问答重新调用 T00b
                                ↓
                         回到检查点（质量驱动终止）
```

### 2.7.2 WAITING_FOR_USER 状态定义

- **trigger**: T00b 输出 `validation_status == "INCOMPLETE"`
- **phase**: 仅在 Phase 1 DAG 调度循环中有效
- **behavior**: 暂停 find_ready_nodes() 调度循环，向用户输出问题集，等待用户回答
- **resume_trigger**: 用户提供新信息后，重新调用 T00b Sub-Agent
- **rounds_policy**: 不设上限，质量驱动终止
- **on_quality_satisfied**: 使用已收集信息生成最优 persona_card，标注缺失项，强制 COMPLETE
- **on_error**: 记录到 retrying_log，持续重试 T00b 直至用户回复有效输入，不设重试上限，不使用默认人设替代，质量保持

### 2.7.3 用户主动放弃

若用户在任意轮次回复以下任意内容，Orchestrator SHALL 触发 `on_user_abort`：不设上限，质量驱动终止（当前轮次）：

- 中文放弃信号："跳过"、"不填"、"略过"、"不用了"、"算了"
- 英文放弃信号："skip"、"pass"、"no"、"n/a"
- 接受默认值："随便"、"默认"、"都行"、"无所谓"
- 明确拒绝："不需要"、"不想填"、"不方便"
- 或 Orchestrator 判定为用户明确表示不想继续提供人设信息的任何回复

Orchestrator 在触发穷尽重试前 SHALL 向用户发送确认消息：

> "收到。将使用已收集的信息生成你的人设卡，未填写的字段将标注为『未提供』。如希望继续补充，请直接告诉我你想补充的内容。"

**质量驱动终止时**：仍有字段 `INCOMPLETE` → 自动触发 `on_quality_satisfied` 穷尽重试（此规则保持不变）

### 2.7.4 约束

- 最大采集轮数：不设上限，质量驱动终止
- 每轮 T00b 的 tok 预算：400 tok
- 用户主动放弃：回复放弃信号后触发穷尽重试（见上方 §2.7.3 用户主动放弃规则）
- 质量驱动终止：INCOMPLETE 字段持续穷尽重试直至 COMPLETE 或用户主动放弃
- T00b route: always（所有 output_type 均激活）

## 3. Phase 1 — 执行

### 3.1 执行循环

主LLM在 Phase 1 中进入调度循环。**自 R9-05 起，调度循环由 LangGraph StateGraph 原生编排引擎驱动**（能力卡：`knowledge/external-capabilities/TC-100-LangGraph.md`），替代原有 `find_ready_nodes()` 手动遍历伪代码。LangGraph 自动处理节点依赖关系、拓扑排序与状态传递。

> **回退声明**：若 `langgraph` 库不可用（ImportError 或编译失败），回退到下方保留的伪代码编排（以注释形式文档化）。伪代码与 LangGraph 功能等价，但 LangGraph 提供原生并行调度、自动 checkpoint、interrupt_before 能力。

### 3.1.1 LangGraph 编排（R9-05 主路径）

```python
# === Phase 1 LangGraph 编排（R9-05 主路径）===
#
# LangGraph 自动处理：
#   - 节点就绪检查：依赖关系由 add_edge 注册，LangGraph 自动判定就绪
#   - 拓扑排序：LangGraph 内置拓扑排序，无需手动 find_ready_nodes()
#   - 状态传递：通过 ResearchState 自动传递 context_package
#
# 完整 StateGraph 定义见 SKILL.md「LangGraph StateGraph 映射」章节。

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, Annotated
import operator


class ResearchState(TypedDict):
    """LangGraph 状态 — context_package 是核心字段，自动在节点间传递。"""
    context_package: dict                              # 按 handoff-protocol.md 标准格式
    execution_ledger: Annotated[list, operator.add]    # 执行账本，跨节点累加
    node_outputs: dict                                 # {node_id: node_output}
    current_phase: int                                 # 当前 Phase


def make_node(task_id: str):
    """工厂函数：为每个 DAG 节点生成 LangGraph 节点函数。"""
    def node_fn(state: ResearchState) -> ResearchState:
        # Step 1: 组装 context_package（LangGraph 自动传递上游 state）
        context_package = assemble_context_package(
            task_id=task_id,
            problem=state["context_package"]["problem"],
            output_type=state["context_package"]["output_type"],
            upstream_nodes=state["node_outputs"],
        )
        # Step 2: 调用 Sub-Agent
        sub_agent_result = invoke_sub_agent(
            task_id=task_id,
            context_package=context_package,
            task_file=load_task_file(task_id),
        )
        # Step 3: Supervisor 判定
        verdict = invoke_supervisor(
            task_id=task_id,
            sub_agent_output=sub_agent_result,
            gate_config=get_gate_config(task_id),
        )
        # Step 4: 分支处理（PASS / PASS_WITH_WARNINGS / FAIL）
        if verdict in ("PASS", "PASS_WITH_WARNINGS"):
            state["node_outputs"][task_id] = sub_agent_result
            state["execution_ledger"].append(
                {"task_id": task_id, "status": "completed", "summary": summarize(sub_agent_result)}
            )
        elif verdict == "FAIL":
            # EXHAUST 模式：持续重试直至通过（无上限），由 LangGraph 循环重入实现
            state["execution_ledger"].append(
                {"task_id": task_id, "status": "retrying", "summary": verdict.retry_instruction}
            )
            # 重新触发本节点（LangGraph 支持条件边实现重试循环）
            return state
        return state
    return node_fn


def build_compiled_graph(checkpoint_backend: str = "memory"):
    """构建并编译 LangGraph StateGraph。

    节点注册与边定义见 SKILL.md「LangGraph StateGraph 映射」章节（58 节点完整定义）。
    此处展示骨架，完整 add_node/add_edge 调用从 SKILL.md 派生。
    """
    graph = StateGraph(ResearchState)

    # 注册全部 58 节点（见 SKILL.md §3-4 完整列表）
    for task_id in ALL_57_NODE_IDS:
        graph.add_node(task_id, make_node(task_id))

    # 按依赖关系添加边（见 SKILL.md §4 完整边列表）
    for edge in DAG_EDGES:
        graph.add_edge(edge["from"], edge["to"])
    graph.set_entry_point("T_env_probe")
    graph.add_edge("T21", END)
    graph.add_edge("T20d_cross_media_review", END)

    # checkpoint 后端选择
    if checkpoint_backend == "memory":
        checkpointer = MemorySaver()
    elif checkpoint_backend == "file":
        from langgraph.checkpoint.sqlite import SqliteSaver
        checkpointer = SqliteSaver.from_conn_string("checkpoints.db")
    elif checkpoint_backend == "redis":
        from langgraph.checkpoint.redis import RedisSaver
        checkpointer = RedisSaver.from_conn_info(host="localhost", port=6379)

    # 编译：interrupt_before 用于 T00b/I01 用户交互（见 §3.5 中断与用户交互）
    compiled = graph.compile(
        interrupt_before=["T00b", "I01"],
        checkpointer=checkpointer,
    )
    return compiled


def phase_1_execution(dag: DAG, gate_config: GateConfig) -> None:
    """
    主LLM的 Phase 1 调度循环（LangGraph 驱动）。
    LangGraph 自动：找就绪节点 → 组装context_package → 调用Sub-Agent → Supervisor判定
    """
    compiled_graph = build_compiled_graph(checkpoint_backend="memory")
    initial_state: ResearchState = {
        "context_package": {
            "problem": dag.problem,
            "output_type": dag.output_type,
            "upstream_outputs": {},
        },
        "execution_ledger": [],
        "node_outputs": {},
        "current_phase": 1,
    }
    # LangGraph 自动按拓扑序调度全部 58 节点
    final_state = compiled_graph.invoke(
        initial_state,
        config={"configurable": {"thread_id": dag.session_id}},
    )
```

### 3.1.2 原有伪代码（回退路径，文档化保留）

> 以下伪代码为 LangGraph 不可用时的回退路径，保留为文档说明。功能与 LangGraph 编排等价，但需主 LLM 手动模拟依赖解析、拓扑排序、状态传递。

```python
# === Phase 1 DAG 调度伪代码（回退路径 — LangGraph 不可用时使用）===
#
# [原 find_ready_nodes() 伪代码 — 已被 LangGraph 自动依赖解析替代]
# [原手动拓扑排序 — 已被 LangGraph 内置拓扑排序替代]
# [原手动状态传递 — 已被 ResearchState 自动传递替代]

def phase_1_execution_legacy(dag: DAG, gate_config: GateConfig) -> None:
    """
    [回退路径] 主LLM的 Phase 1 调度循环（伪代码）。
    每个节点执行: 找就绪 → 组装context_package → 调用Sub-Agent → Supervisor判定
    """

    todo_list = TodoWrite.load_all_nodes(dag.nodes)

    while not all_nodes_done(dag.nodes):
        # Step 1: 找就绪节点（LangGraph 主路径中此步由引擎自动完成）
        ready_nodes = find_ready_nodes(dag.nodes, todo_list)

        if not ready_nodes:
            blocked_nodes = find_blocked_nodes(dag.nodes, todo_list)
            if blocked_nodes:
                for node in blocked_nodes:
                    if node.status == "retrying":
                        inject_retry_instruction(node)
                        continue
            break

        for node in ready_nodes:
            todo_list.mark(node.task_id, "in_progress")

        for node in ready_nodes:
            context_package = assemble_context_package(
                task_id=node.task_id,
                problem=dag.problem,
                output_type=dag.output_type,
                upstream_nodes=get_upstream_outputs(node, dag)
            )
            sub_agent_result = invoke_sub_agent(
                task_id=node.task_id,
                context_package=context_package,
                task_file=load_task_file(node.task_id)
            )
            verdict = invoke_supervisor(
                task_id=node.task_id,
                sub_agent_output=sub_agent_result,
                gate_config=get_gate_config(node.gate)
            )
            if verdict == "PASS":
                store_output(node.task_id, sub_agent_result, "COMPLETED")
                todo_list.mark(node.task_id, "completed")
            elif verdict == "PASS_WITH_WARNINGS":
                store_output(node.task_id, sub_agent_result, "COMPLETED")
                node.warning_count += 1
                if node.warning_count_consecutive >= 3:
                    node.strict_mode = True
                todo_list.mark(node.task_id, "completed")
            elif verdict == "FAIL":
                node.retry_count += 1
                retry_instruction = verdict.retry_instruction
                todo_list.mark(node.task_id, "in_progress")


# [原 find_ready_nodes — 已被 LangGraph 自动依赖解析替代]
def find_ready_nodes(nodes: list, todo_list: TodoList) -> list:
    """[回退路径] 查找所有依赖已满足且状态为 pending 的节点。
    LangGraph 主路径中，此函数由引擎内置的依赖解析自动完成。"""
    ready = []
    for node in nodes:
        if todo_list.status(node.task_id) != "pending":
            continue
        all_deps_met = True
        for dep_id in node.dependencies:
            dep_status = todo_list.status(dep_id)
            if dep_status not in ("completed", "RETRYING"):
                all_deps_met = False
                break
        if all_deps_met:
            ready.append(node)
    return ready


# [原 assemble_context_package — LangGraph 主路径中由 ResearchState 自动传递]
def assemble_context_package(task_id: str, problem: str,
                              output_type: str, upstream_nodes: list) -> dict:
    """[回退路径] 组装 context_package。
    LangGraph 主路径中，context_package 作为 ResearchState 字段自动传递。"""
    package = {
        "problem": problem,
        "output_type": output_type,
        "task_id": task_id,
        "upstream_outputs": {}
    }
    for node in upstream_nodes:
        upstream_summary = summarize_output(node.output, max_chars=100)
        upstream_data = extract_key_data(node.output)
        package["upstream_outputs"][node.task_id] = {
            "summary": upstream_summary,
            "data": upstream_data,
            "status": node.status
        }
    return package
```

### 3.2 并行调度规则

```yaml
parallel_execution_rules:
  - rule: "所有依赖已满足的节点可同时调度"
    constraint: "每个 Sub-Agent 调用独立，不共享内存上下文"

  - rule: "同一 gate 组内的节点可并行，但 gate 检查需等全部完成"
    example: "T17 和 T18 可以并行，但 T19 需要两者都完成"

  - rule: "不同分支的节点可并行"
    example: "T10、T11、T12 可同时执行（三者均依赖 T09）"

  - rule: "主LLM并发上限为 3 个 Sub-Agent"
    reason: "控制上下文窗口压力，避免 token 消耗过大"
```

### 3.3 并行节点编排（LangGraph parallel / fan-out fan-in）

> **R9-05 新增**：T10/T11/T12 三路对抗验证并行执行，使用 LangGraph 的 fan-out/fan-in 模式。三路对抗节点（T10 逻辑攻击、T11 证据攻击、T12 范围攻击）均依赖 T09，可同时执行；并行结果汇总到 T12b（三路对抗交叉融合）。

#### 3.3.1 fan-out/fan-in 拓扑

```
T09 (多路径推理)
 ├──→ T10 (魔鬼代言人-逻辑攻击)  ─┐
 ├──→ T11 (魔鬼代言人-证据攻击)  ─┼──→ T12b (三路对抗交叉融合) ──→ T13
 └──→ T12 (魔鬼代言人-范围攻击)  ─┘
```

#### 3.3.2 LangGraph 实现

LangGraph 中，fan-out 通过从同一源节点（T09）向多个目标节点（T10/T11/T12）添加边实现，fan-in 通过多个源节点（T10/T11/T12）向同一目标节点（T12b）添加边实现。LangGraph 自动并行调度 fan-out 的目标节点，并在 fan-in 节点处等待所有上游完成。

```python
# === fan-out: T09 → T10/T11/T12 并行 ===
graph.add_edge("T09", "T10")
graph.add_edge("T09", "T11")
graph.add_edge("T09", "T12")

# === fan-in: T10/T11/T12 → T12b 汇总 ===
graph.add_edge("T10", "T12b")
graph.add_edge("T11", "T12b")
graph.add_edge("T12", "T12b")

# T12b 等待 T10/T11/T12 全部完成后执行
graph.add_edge("T12b", "T13")
```

#### 3.3.3 并行结果汇总到 T12b

T12b 节点函数从 `state["node_outputs"]` 中读取 T10/T11/T12 三路对抗的产出，进行交叉融合：

```python
def t12b_node(state: ResearchState) -> ResearchState:
    """三路对抗交叉融合 — 汇总 T10/T11/T12 并行结果。"""
    t10_output = state["node_outputs"]["T10"]  # 逻辑攻击结果
    t11_output = state["node_outputs"]["T11"]  # 证据攻击结果
    t12_output = state["node_outputs"]["T12"]  # 范围攻击结果

    # 交叉融合三路对抗结果
    fused = cross_fuse_adversarial(t10_output, t11_output, t12_output)
    state["node_outputs"]["T12b"] = fused
    state["execution_ledger"].append(
        {"task_id": "T12b", "status": "completed", "summary": "三路对抗交叉融合完成"}
    )
    return state
```

#### 3.3.4 其他并行组

| 并行组 | fan-out 源 | 并行节点 | fan-in 汇总节点 | 说明 |
|--------|-----------|---------|----------------|------|
| adv | T09 | T10, T11, T12 | T12b | 三路对抗验证 |
| qa | T16 | T17, T18 | T19 | 质量保障双路 |
| phase5_post_gate | T28 | T_philosophical_core, T_meta_dim_9_10, T_meta_dim_11_12, T_meta_dim_13_14, TM01 | T_gate_delta | Phase 5 后置门控五路并行 |

### 3.4 中断与用户交互（LangGraph interrupt_before）

> **R9-05 新增**：使用 LangGraph 的 `interrupt_before` 参数在指定节点前中断，等待用户输入。T00b（人设采集）和 I01（迭代深化）是 DAG 中需要用户交互的两个节点。

#### 3.4.1 中断节点定义

| 节点 | 中断原因 | 等待输入 | 恢复条件 |
|------|---------|---------|---------|
| T00b（输入情绪基调提取） | 人设采集需多轮用户对话 | 用户提供人设信息（identity/core_values/personal_stories 等 7 项必填字段） | `validation_status == COMPLETE` 或用户主动放弃 |
| I01（迭代深化补研循环） | 迭代深化需用户确认是否继续 | 用户确认继续/中止/补充方向 | `ΔInfo(t) < ε` 或所有 P0/P1 缺口已处理 |

#### 3.4.2 LangGraph interrupt_before 实现

```python
# 编译时指定 interrupt_before 节点
compiled_graph = graph.compile(
    interrupt_before=["T00b", "I01"],  # 在 T00b 和 I01 前中断
    checkpointer=checkpointer,
)

# 执行：LangGraph 在 T00b 前自动中断，返回当前 state
config = {"configurable": {"thread_id": session_id}}
state = compiled_graph.invoke(initial_state, config=config)

# T00b 中断后：向用户展示问题集，等待用户输入
# 用户提供回答后，更新 state 并恢复执行
state["context_package"]["user_persona_input"] = user_response
state = compiled_graph.invoke(None, config=config)  # 传 None 从中断点恢复

# I01 中断后：向用户确认是否继续迭代深化
state["context_package"]["user_iteration_confirm"] = user_confirm
state = compiled_graph.invoke(None, config=config)  # 恢复执行
```

#### 3.4.3 与 T00b 交互等待协议的关系

LangGraph `interrupt_before` 与 §2.7「T00b 交互等待协议」互补：
- **LangGraph interrupt_before**：提供技术层中断/恢复机制（暂停图执行、保存 checkpoint、恢复执行）
- **T00b 交互等待协议**：定义业务层交互规则（WAITING_FOR_USER 状态、用户主动放弃信号、质量驱动终止、不设上限轮次）
- 二者协作：LangGraph 负责暂停/恢复，T00b 协议负责交互内容与终止条件

### 3.5 运行时循环检测

> **R9-05 新增（配合 R1-04）**：每次调度节点前检查是否有环。编译期通过 `scripts/cycle-detection-check.py`（Kahn's algorithm）检测 DAG 是否有环；运行期通过 LangGraph 递归上限与状态指纹双重保护。发现环则报错并停止执行。

#### 3.5.1 双层循环检测机制

| 层级 | 机制 | 触发时机 | 工具 |
|------|------|---------|------|
| 编译期 | Kahn's algorithm 拓扑排序 | CI 流水线 / 本地预检 | `scripts/cycle-detection-check.py` |
| 运行期 | LangGraph 递归上限 + 状态指纹 | 每次调度节点前 | LangGraph 引擎内置 |

#### 3.5.2 运行期检测逻辑

LangGraph 在运行期通过以下机制防止循环：
1. **递归上限**：`recursion_limit` 参数限制图的最大执行步数（默认 25），超过则抛出 `RecursionError`
2. **状态指纹**：checkpointer 记录每次状态快照，若检测到状态重复（相同 state 出现两次），判定为循环

```python
# 运行期循环检测配置
compiled_graph = graph.compile(
    interrupt_before=["T00b", "I01"],
    checkpointer=checkpointer,
)

# 执行时设置递归上限（58 节点 + 重试，设为 200 留足余量）
state = compiled_graph.invoke(
    initial_state,
    config={
        "configurable": {"thread_id": session_id},
        "recursion_limit": 200,
    },
)
# 若触发 RecursionError → 判定存在运行期循环，报错并停止
```

#### 3.5.3 与 cycle-detection-check.py 配合

- **编译期**（CI）：`scripts/cycle-detection-check.py` 解析 SKILL.md 的 DAG 拓扑，使用 Kahn's algorithm 检测环。有环则 CI 失败（退出码 1），阻止合并。
- **运行期**（执行）：LangGraph 递归上限与状态指纹检测运行期异常（如条件边错误导致的循环）。发现环则报错并停止执行。
- **二者配合**：编译期检测静态拓扑环，运行期检测动态执行环，双层保护确保 DAG 无环不变式。

### 3.6 下游节点哈希验证流程（R10-07）

> **目的**：下游节点读取上游输出时，重新计算 SHA-256 哈希并与 execution_ledger 中的 output_hash 对比，确保上游产出在传递过程中未被篡改。哈希不匹配时触发 RETRYING 状态，从 checkpoint 恢复上游输出。

#### 3.6.1 哈希验证触发时机

每个节点执行 Step 1（组装 context_package）时，在读取上游节点输出后、注入 context_package 之前，执行哈希验证：

```python
def verify_upstream_hashes(node_id: str, upstream_outputs: dict, execution_ledger: list) -> bool:
    """下游节点读取上游输出时的哈希验证（R10-07）。

    Args:
        node_id: 当前节点 ID
        upstream_outputs: 从 node_outputs 读取的上游产出
        execution_ledger: 执行账本（含上游节点的 output_hash）

    Returns:
        True: 全部哈希匹配
        False: 存在哈希不匹配
    """
    upstream_node_ids = get_dependencies(node_id)
    for up_id in upstream_node_ids:
        # 1. 从 execution_ledger 获取上游节点的 output_hash
        ledger_entry = find_ledger_entry(execution_ledger, up_id)
        expected_hash = ledger_entry["output_hash"]

        # 2. 重新计算上游节点输出的 SHA-256
        actual_output = upstream_outputs[up_id]
        actual_hash = compute_sha256(serialize(actual_output))

        # 3. 对比哈希
        if actual_hash != expected_hash:
            # 哈希不匹配 → 触发 RETRYING
            log_hash_mismatch(node_id, up_id, expected_hash, actual_hash)
            trigger_retrying(node_id, reason="upstream_hash_mismatch",
                             mismatched_upstream=up_id)
            return False

    # 4. 验证 Merkle 链完整性
    for up_id in upstream_node_ids:
        up_output = upstream_outputs[up_id]
        up_ledger = find_ledger_entry(execution_ledger, up_id)
        up_upstream_hashes = up_ledger.get("upstream_hashes", [])
        recomputed_node_hash = compute_merkle_hash(up_output, up_upstream_hashes)
        if recomputed_node_hash != up_ledger["output_hash"]:
            log_merkle_chain_break(node_id, up_id)
            trigger_retrying(node_id, reason="merkle_chain_break",
                             mismatched_upstream=up_id)
            return False

    return True
```

#### 3.6.2 哈希验证集成到节点执行流程

节点执行流程更新为（在原 Step 1-4 基础上插入哈希验证步骤）：

```python
def make_node(task_id: str):
    """工厂函数：为每个 DAG 节点生成 LangGraph 节点函数（含哈希验证）。"""
    def node_fn(state: ResearchState) -> ResearchState:
        # Step 0: 哈希验证（R10-07 新增）
        upstream_outputs = {
            dep_id: state["node_outputs"][dep_id]
            for dep_id in get_dependencies(task_id)
        }
        if not verify_upstream_hashes(task_id, upstream_outputs, state["execution_ledger"]):
            # 哈希不匹配 → 触发自动恢复（见 SKILL.md §3.3.6）
            state = recover_from_hash_mismatch(state, task_id)
            return state  # 恢复后重新进入本节点

        # Step 1: 组装 context_package（上游哈希已验证）
        context_package = assemble_context_package(
            task_id=task_id,
            problem=state["context_package"]["problem"],
            output_type=state["context_package"]["output_type"],
            upstream_nodes=upstream_outputs,
        )

        # Step 2: 调用 Sub-Agent
        sub_agent_result = invoke_sub_agent(
            task_id=task_id,
            context_package=context_package,
            task_file=load_task_file(task_id),
        )

        # Step 3: Supervisor 判定
        verdict = invoke_supervisor(
            task_id=task_id,
            sub_agent_output=sub_agent_result,
            gate_config=get_gate_config(task_id),
        )

        # Step 4: 分支处理 + 哈希写入（R10-07 新增）
        if verdict in ("PASS", "PASS_WITH_WARNINGS"):
            # 计算本节点 output_hash
            output_hash = compute_sha256(serialize(sub_agent_result))
            # 计算 Merkle 链哈希（含上游哈希）
            upstream_hashes = [
                {"node_id": dep_id,
                 "output_hash": find_ledger_entry(
                     state["execution_ledger"], dep_id)["output_hash"],
                 "version": find_ledger_entry(
                     state["execution_ledger"], dep_id).get("version", "v1")}  # D14.4.2: parent_versions
                for dep_id in get_dependencies(task_id)
            ]
            merkle_hash = compute_merkle_hash(sub_agent_result, upstream_hashes)

            # D14.4.5: 派生本节点随机种子并记录（确保可复现）
            node_seed = int(compute_sha256(
                (str(state.get("global_seed", 0)) + task_id).encode("utf-8")
            )[:32], 16)
            # 调用 Sub-Agent 前已通过 set_seed(node_seed) 注入到 Sub-Agent 上下文
            # （随机过程节点 T09/T10/T11/T12/TM01/TM04 强制使用此种子）

            state["node_outputs"][task_id] = sub_agent_result
            state["execution_ledger"].append({
                "task_id": task_id,
                "status": "completed",
                "summary": summarize(sub_agent_result),
                "timestamp": get_iso_timestamp(),
                "output_hash": merkle_hash,  # R10-07: 写入哈希
                "upstream_hashes": upstream_hashes,  # R10-07: 上游哈希列表（含 D14.4.2 version）
                "version": get_next_version(state["execution_ledger"], task_id),  # D14.4.2: 版本号
                "parent_versions": [h["version"] for h in upstream_hashes],  # D14.4.2: 上游版本号列表
                "random_seed": node_seed,  # D14.4.5: 本节点使用的随机种子
            })
        elif verdict == "FAIL":
            state["execution_ledger"].append({
                "task_id": task_id,
                "status": "retrying",
                "summary": verdict.retry_instruction,
                "timestamp": get_iso_timestamp(),
            })
            return state
        return state
    return node_fn
```

#### 3.6.3 哈希不匹配时的 RETRYING 流程

```yaml
hash_mismatch_retrying:
  trigger: "verify_upstream_hashes() 返回 False"
  retrying_state:
    node_id: "{当前节点}"
    status: "RETRYING"
    reason: "upstream_hash_mismatch | merkle_chain_break"
    mismatched_upstream: "{哈希不匹配的上游节点 ID}"
    expected_hash: "{execution_ledger 中的哈希}"
    actual_hash: "{重新计算的哈希}"
  recovery_flow:
    - "从 checkpoint 恢复 mismatched_upstream 的输出快照"
    - "重新计算 mismatched_upstream 的哈希"
    - "若恢复后的哈希与 execution_ledger 一致 → 上游输出完整，重新执行当前节点"
    - "若恢复后的哈希仍不匹配 → 级联向上追溯，恢复更上游节点"
    - "持续恢复直至哈希匹配或到达叶子节点"
  max_retry: null  # EXHAUST 模式：不设上限
  logging:
    - "记录 RETRYING 事件到 execution_ledger"
    - "记录不匹配节点、预期哈希、实际哈希、恢复操作"
```

#### 3.6.4 哈希验证与 LangGraph checkpoint 的关系

- **LangGraph checkpoint**：提供状态级快照（ResearchState 的完整序列化），用于断点恢复
- **哈希验证**：提供密码学完整性验证（SHA-256），确保 checkpoint 恢复的输出未被篡改
- **二者协作**：LangGraph checkpoint 负责"恢复到哪个状态"，哈希验证负责"恢复后的状态是否完整"
- **具体流程**：哈希不匹配 → 从 LangGraph checkpoint 恢复上游输出 → 重新计算哈希 → 验证一致性 → 重新执行下游节点

### 3.7 事务性回滚机制（R10-08）

> **目的**：为 DAG 执行提供事务性安全保障。每个节点执行前保存状态快照，节点失败或 Gate 失败时回滚到检查点，确保执行状态的一致性与可恢复性。本机制基于 LangGraph checkpoint（TC-100）实现状态快照，结合 R10-07 哈希验证确保恢复后的状态完整性。

#### 3.7.1 事务性回滚规范定义（3.4.1）

**事务边界**：每个 DAG 节点构成一个原子事务单元（transactional unit），包含三个阶段：

1. **BEGIN**：保存执行前状态快照（pre-execution snapshot）
2. **COMMIT**：节点 Supervisor 判定为 PASS/PASS_WITH_WARNINGS 时，提交事务，产出写入 `node_outputs`，账本追加记录
3. **ROLLBACK**：节点 Supervisor 判定为 FAIL 时，回滚事务，恢复到 BEGIN 时的状态快照

```yaml
transactional_unit:
  node_id: "{节点 ID}"
  transaction_id: "tx_{node_id}_{timestamp}_{attempt}"
  phases:
    begin:
      action: "save_state_snapshot"
      snapshot_key: "snapshot_{node_id}_{timestamp}"
      snapshot_content: "ResearchState 的完整深拷贝（含 context_package/execution_ledger/node_outputs/current_phase）"
    commit:
      condition: "Supervisor verdict ∈ {PASS, PASS_WITH_WARNINGS}"
      actions:
        - "写入 node_outputs[task_id]"
        - "追加 execution_ledger 记录（含 output_hash，见 R10-07）"
        - "标记 todo_list[task_id] = completed"
        - "释放 begin 阶段快照（GC 回收）"
    rollback:
      condition: "Supervisor verdict == FAIL OR 节点执行异常 OR 哈希不匹配（R10-07）"
      actions:
        - "从快照恢复 ResearchState"
        - "清除本节点产生的所有 node_outputs 条目"
        - "追加 execution_ledger 回滚记录"
        - "标记 todo_list[task_id] = retrying"
        - "保留快照供回滚日志审计"
```

#### 3.7.2 节点执行前状态快照机制（3.4.2）

每个节点执行前（`make_node()` 工厂函数的 Step 0 之前），保存 ResearchState 的完整快照：

```python
def save_pre_execution_snapshot(state: ResearchState, task_id: str) -> str:
    """节点执行前保存状态快照（R10-08）。

    基于 LangGraph MemorySaver/SqliteSaver/RedisSaver 的 checkpoint 能力，
    保存 ResearchState 的完整深拷贝，用于失败时回滚。

    Args:
        state: 当前 ResearchState
        task_id: 即将执行的节点 ID

    Returns:
        snapshot_key: 快照唯一标识，用于回滚时检索
    """
    timestamp = get_iso_timestamp()
    attempt = get_current_attempt(state["execution_ledger"], task_id)
    snapshot_key = f"snapshot_{task_id}_{timestamp}_{attempt}"

    # 深拷贝当前状态（避免引用共享导致回滚后状态被污染）
    snapshot = {
        "context_package": deepcopy(state["context_package"]),
        "execution_ledger": deepcopy(state["execution_ledger"]),
        "node_outputs": deepcopy(state["node_outputs"]),
        "current_phase": state["current_phase"],
        "snapshot_metadata": {
            "snapshot_key": snapshot_key,
            "task_id": task_id,
            "timestamp": timestamp,
            "attempt": attempt,
            "state_hash": compute_sha256(serialize(state)),  # 状态指纹，用于一致性检查
        },
    }

    # 写入 LangGraph checkpoint（TC-100 能力卡）
    checkpointer.save(
        config={"configurable": {"thread_id": state["session_id"]}},
        checkpoint=snapshot,
        metadata={"type": "pre_execution", "task_id": task_id},
    )

    return snapshot_key
```

**快照存储策略**：
- **MemorySaver**（默认）：内存中保存，会话结束即释放，适合短任务
- **SqliteSaver**：持久化到 SQLite 数据库，支持跨会话恢复
- **RedisSaver**：分布式部署，支持多实例共享

**快照保留策略**：
- 最近 3 次尝试的快照保留（用于回滚日志审计）
- 超过 3 次的旧快照由 GC 回收
- Gate 节点的 pre-execution 快照永久保留（直到会话结束）

#### 3.7.3 Gate 失败触发回滚机制（3.4.3）

Gate 节点（Gate-α/β/γ/终/δ）失败时，回滚到 Gate 前的检查点，重新执行 Gate 依赖的节点：

```python
def rollback_on_gate_failure(state: ResearchState, gate_id: str, failed_checks: list) -> ResearchState:
    """Gate 失败时触发回滚至 Gate 前检查点（R10-08）。

    Args:
        state: 当前 ResearchState
        gate_id: 失败的 Gate 节点 ID（如 T07/T14/T16/T28/T_gate_delta）
        failed_checks: 未通过的检查项列表

    Returns:
        恢复后的 ResearchState
    """
    # 1. 定位 Gate 前的检查点
    gate_pre_snapshot_key = find_gate_pre_snapshot(state["execution_ledger"], gate_id)
    if gate_pre_snapshot_key is None:
        # 无检查点 → 从 Gate 的直接依赖节点重新执行
        deps = get_dependencies(gate_id)
        return rollback_to_nodes(state, deps)

    # 2. 从检查点恢复状态
    restored_state = restore_from_snapshot(gate_pre_snapshot_key)

    # 3. 标记 Gate 依赖的节点为 retrying（触发重新执行）
    deps = get_dependencies(gate_id)
    for dep_id in deps:
        restored_state["node_outputs"].pop(dep_id, None)
        restored_state["execution_ledger"].append({
            "task_id": dep_id,
            "status": "retrying",
            "reason": f"gate_{gate_id}_failed",
            "failed_checks": failed_checks,
            "timestamp": get_iso_timestamp(),
        })

    # 4. 记录回滚日志
    log_rollback_event(
        trigger_node=gate_id,
        rollback_type="gate_failure",
        snapshot_key=gate_pre_snapshot_key,
        affected_nodes=deps,
        failed_checks=failed_checks,
    )

    return restored_state
```

**Gate 回滚规则**：

| Gate | 触发条件 | 回滚目标 | 影响范围 |
|------|---------|---------|---------|
| Gate-α (T07) | T07 检查项 blocking 失败 | T07 前检查点 | T01-T06 中与失败检查项相关的节点 |
| Gate-β (T14) | T14 检查项 blocking 失败 | T14 前检查点 | T08-T13 中与失败检查项相关的节点 |
| Gate-γ (T16) | T16 检查项 blocking 失败 | T16 前检查点 | T15 及相关领域引擎节点 |
| Gate-终 (T28) | T28 检查项 blocking 失败 | T28 前检查点 | T22-T27 中与失败检查项相关的节点 |
| Gate-δ (T_gate_delta) | T_gate_delta 检查项 blocking 失败 | T_gate_delta 前检查点 | TM01-TM07/TM06b 中与失败检查项相关的节点 |

> **精准回退（R7-05 协同）**：Gate 失败时不全量回滚所有依赖节点，仅回退与失败检查项直接相关的节点。失败检查项与节点的依赖关系由 `supervisor_protocol.md` 的精准回退机制定义。

#### 3.7.4 下游节点状态清理规则（3.4.4）

节点回滚时，依赖该节点的所有下游节点（传递依赖）也必须回滚，确保状态一致性：

```python
def cleanup_downstream_nodes(state: ResearchState, rolled_back_node_id: str) -> ResearchState:
    """回滚时清理下游节点状态（R10-08）。

    使用 DAG 拓扑的逆序遍历，找出所有传递依赖 rolled_back_node_id 的下游节点，
    清除其 node_outputs 和 execution_ledger 中的完成记录。

    Args:
        state: 当前 ResearchState
        rolled_back_node_id: 被回滚的节点 ID

    Returns:
        清理后的 ResearchState
    """
    # 1. 计算传递依赖闭包（所有下游节点）
    downstream_nodes = compute_transitive_downstream(rolled_back_node_id)

    # 2. 按拓扑逆序清理（先清理最远的下游，避免中间状态不一致）
    for node_id in reversed(downstream_nodes):
        # 清除 node_outputs
        state["node_outputs"].pop(node_id, None)

        # 在 execution_ledger 中追加清理记录（不删除历史记录，保持审计轨迹）
        state["execution_ledger"].append({
            "task_id": node_id,
            "status": "rolled_back",
            "reason": f"upstream_{rolled_back_node_id}_rolled_back",
            "timestamp": get_iso_timestamp(),
        })

    # 3. 记录清理日志
    log_cleanup_event(
        trigger_node=rolled_back_node_id,
        affected_nodes=downstream_nodes,
        cleanup_type="transitive_downstream",
    )

    return state
```

**下游清理规则**：
1. **传递依赖闭包**：使用 DAG 拓扑计算所有直接和间接依赖 `rolled_back_node_id` 的节点
2. **拓扑逆序清理**：从最远的下游节点开始清理，向 `rolled_back_node_id` 方向推进
3. **审计轨迹保留**：不删除 `execution_ledger` 中的历史记录，而是追加 `rolled_back` 状态记录
4. **node_outputs 清除**：被回滚节点的 `node_outputs` 条目被清除，确保下游节点不会读到过期数据
5. **哈希链断裂处理**：回滚后，下游节点的 `output_hash` 和 `upstream_hashes` 失效，重新执行时重新计算（R10-07 协同）

#### 3.7.5 回滚日志格式（3.4.5）

每次回滚事件必须记录完整的回滚日志，写入 `execution_ledger` 和独立的 `rollback_log`：

```yaml
rollback_log_entry:
  rollback_id: "rb_{timestamp}_{random_4_hex}"
  timestamp: "ISO 8601 格式"
  trigger_node: "{触发回滚的节点 ID}"
  rollback_type: "node_failure | gate_failure | hash_mismatch | manual_rollback"
  trigger_reason: "{具体原因描述}"

  # 影响范围
  affected_nodes:
    direct: ["{直接回滚的节点 ID}"]
    transitive_downstream: ["{传递依赖的下游节点 ID 列表}"]
  total_affected: integer

  # 恢复点信息
  recovery_point:
    snapshot_key: "{恢复的快照 ID}"
    snapshot_timestamp: "{快照时间戳}"
    state_hash_before: "{回滚前状态哈希}"
    state_hash_after: "{回滚后状态哈希}"

  # 失败检查项（仅 gate_failure 类型）
  failed_checks:
    - check_id: "{检查项 ID}"
      check_desc: "{检查项描述}"
      severity: "blocking | major | minor"
      actual_value: "{实际值}"
      expected_value: "{期望值}"

  # 恢复操作
  recovery_actions:
    - "restore_from_snapshot: {snapshot_key}"
    - "cleanup_downstream: {affected_nodes}"
    - "mark_retrying: {affected_nodes}"
    - "recompute_hashes: {affected_nodes}"

  # 一致性检查结果
  consistency_check:
    pre_rollback_hash: "{回滚前状态哈希}"
    post_rollback_hash: "{回滚后状态哈希}"
    hash_match: boolean  # 恢复后的状态哈希是否与快照一致
    merkle_chain_intact: boolean  # Merkle 链是否完整
    node_outputs_consistent: boolean  # node_outputs 与 execution_ledger 是否一致
```

**日志存储位置**：
- `execution_ledger`：追加 `rolled_back` 状态记录（精简版，仅含 task_id/status/reason/timestamp）
- `rollback_log`：独立日志文件（完整版，含上述全部字段），写入 `./output/rollback_log_{session_id}.jsonl`

#### 3.7.6 回滚后状态一致性检查规则（3.4.6）

回滚后必须执行状态一致性检查，确保恢复后的状态完整且无残留污染：

```python
def verify_post_rollback_consistency(state: ResearchState, rollback_log_entry: dict) -> dict:
    """回滚后状态一致性检查（R10-08）。

    Args:
        state: 回滚后的 ResearchState
        rollback_log_entry: 回滚日志条目

    Returns:
        consistency_report: 一致性检查报告
    """
    report = {
        "rollback_id": rollback_log_entry["rollback_id"],
        "checks": [],
        "overall_status": "CONSISTENT",  # CONSISTENT | INCONSISTENT
    }

    # Check 1: 状态哈希一致性
    current_state_hash = compute_sha256(serialize(state))
    snapshot_state_hash = rollback_log_entry["recovery_point"]["state_hash_before"]
    hash_match = (current_state_hash == snapshot_state_hash)
    report["checks"].append({
        "check": "state_hash_consistency",
        "status": "PASS" if hash_match else "FAIL",
        "current_hash": current_state_hash,
        "expected_hash": snapshot_state_hash,
    })

    # Check 2: node_outputs 与 execution_ledger 一致性
    ledger_completed = {
        e["task_id"] for e in state["execution_ledger"]
        if e["status"] == "completed"
    }
    outputs_keys = set(state["node_outputs"].keys())
    orphan_outputs = outputs_keys - ledger_completed
    missing_outputs = ledger_completed - outputs_keys
    outputs_consistent = (not orphan_outputs) and (not missing_outputs)
    report["checks"].append({
        "check": "node_outputs_ledger_consistency",
        "status": "PASS" if outputs_consistent else "FAIL",
        "orphan_outputs": list(orphan_outputs),
        "missing_outputs": list(missing_outputs),
    })

    # Check 3: Merkle 链完整性（R10-07 协同）
    merkle_intact = verify_merkle_chain_integrity(state["execution_ledger"], state["node_outputs"])
    report["checks"].append({
        "check": "merkle_chain_integrity",
        "status": "PASS" if merkle_intact else "FAIL",
    })

    # Check 4: 被回滚节点无残留
    rolled_back_nodes = set(
        rollback_log_entry["affected_nodes"]["direct"] +
        rollback_log_entry["affected_nodes"]["transitive_downstream"]
    )
    residual = rolled_back_nodes & set(state["node_outputs"].keys())
    no_residual = (not residual)
    report["checks"].append({
        "check": "no_residual_rolled_back_outputs",
        "status": "PASS" if no_residual else "FAIL",
        "residual_nodes": list(residual),
    })

    # Check 5: DAG 依赖完整性
    dag_intact = verify_dag_dependency_integrity(state)
    report["checks"].append({
        "check": "dag_dependency_integrity",
        "status": "PASS" if dag_intact else "FAIL",
    })

    # 总体判定
    if any(c["status"] == "FAIL" for c in report["checks"]):
        report["overall_status"] = "INCONSISTENT"
        trigger_three_level_recovery(state, report)  # 见 §3.7.7

    return report
```

**一致性检查项汇总**：

| 检查项 | 说明 | 失败后果 |
|--------|------|---------|
| state_hash_consistency | 回滚后状态哈希与快照一致 | 从快照重新恢复 |
| node_outputs_ledger_consistency | completed 节点在 node_outputs 中存在 | 修复不一致条目 |
| merkle_chain_integrity | Merkle 链完整（R10-07） | 重新计算哈希链 |
| no_residual_rolled_back_outputs | 被回滚节点无残留输出 | 清除残留输出 |
| dag_dependency_integrity | 已完成节点的依赖也已完成 | 标记缺失依赖为 retrying |

#### 3.7.7 三级错误恢复（R10-04）

根据错误严重程度，实施三级错误恢复策略：

```yaml
three_level_recovery:
  level_1_node_level:
    description: "节点级恢复——单个节点失败时，仅回滚该节点及其下游"
    trigger:
      - "Supervisor verdict == FAIL"
      - "节点执行异常（Sub-Agent 调用失败）"
      - "哈希不匹配（R10-07）"
    recovery_action:
      - "保存 pre-execution 快照（§3.7.2）"
      - "回滚该节点（清除 node_outputs[task_id]）"
      - "清理下游节点（§3.7.4）"
      - "标记该节点及下游为 retrying"
      - "重新执行该节点"
    max_retry: null  # EXHAUST 模式：不设上限
    escalation_condition: "连续 3 次节点级恢复失败 → 升级为 Phase 级恢复"

  level_2_phase_level:
    description: "Phase 级恢复——整个 Phase 失败时，回滚该 Phase 全部节点"
    trigger:
      - "Gate 失败且节点级恢复无法修复"
      - "连续 3 次节点级恢复失败"
      - "Phase 内多个节点连锁失败（>50% 节点失败）"
    recovery_action:
      - "定位 Phase 入口节点的快照"
      - "回滚该 Phase 全部节点"
      - "清理该 Phase 的全部 node_outputs"
      - "标记该 Phase 全部节点为 pending"
      - "从 Phase 入口重新执行"
    max_retry: 2  # Phase 级恢复最多 2 次
    escalation_condition: "Phase 级恢复 2 次仍失败 → 升级为部分回滚"

  level_3_partial_rollback:
    description: "部分回滚——跨 Phase 回滚，回滚到最近的稳定检查点"
    trigger:
      - "Phase 级恢复 2 次仍失败"
      - "跨 Phase 依赖断裂"
      - "状态一致性检查 INCONSISTENT 且无法通过节点级/Phase 级恢复修复"
    recovery_action:
      - "定位最近的稳定检查点（最近一次 Gate 通过后的状态）"
      - "回滚到该检查点"
      - "清理该检查点之后的所有节点产出"
      - "向用户展示恢复点选择 UI（§3.7.8）"
      - "用户确认后从恢复点重新执行"
    max_retry: 1  # 部分回滚最多 1 次，仍失败则交还用户决策
    escalation_condition: "部分回滚 1 次仍失败 → GATE_FAILED_AFTER_RETRY，交还用户决策"
```

**三级恢复决策树**：

```
节点失败
  ↓
Level 1: 节点级恢复
  ├── 成功 → 继续执行
  └── 连续 3 次失败 ↓
Level 2: Phase 级恢复
  ├── 成功 → 从 Phase 入口重新执行
  └── 2 次失败 ↓
Level 3: 部分回滚
  ├── 成功 → 从稳定检查点重新执行
  └── 1 次失败 → GATE_FAILED_AFTER_RETRY，交还用户决策
```

#### 3.7.8 恢复点选择 UI（3.4.8）

Level 3 部分回滚时，向用户展示可用的恢复点列表，由用户选择回滚目标：

```python
def present_recovery_point_ui(state: ResearchState, failed_node: str) -> str:
    """向用户展示恢复点选择 UI（R10-08）。

    Args:
        state: 当前 ResearchState
        failed_node: 失败的节点 ID

    Returns:
        用户选择的恢复点 snapshot_key
    """
    # 1. 收集所有可用的恢复点（Gate 通过后的检查点）
    recovery_points = collect_recovery_points(state["execution_ledger"])

    # 2. 按时间倒序排列（最近的在前）
    recovery_points.sort(key=lambda x: x["timestamp"], reverse=True)

    # 3. 向用户展示恢复点列表
    print(f"\n{'='*60}")
    print(f"⚠ 节点 {failed_node} 失败，已触发部分回滚（Level 3）")
    print(f"{'='*60}")
    print(f"\n可用恢复点列表（按时间倒序）：\n")

    print(f"{'序号':<4} {'节点 ID':<20} {'时间戳':<25} {'状态摘要':<30} {'状态哈希':<16}")
    print(f"{'-'*95}")
    for i, rp in enumerate(recovery_points, 1):
        summary = rp["state_summary"][:28] + ".." if len(rp["state_summary"]) > 28 else rp["state_summary"]
        print(f"{i:<4} {rp['node_id']:<20} {rp['timestamp']:<25} {summary:<30} {rp['state_hash'][:12]+'..':<16}")

    print(f"\n{'-'*95}")
    print(f"0    {'（中止执行）':<20} {'-':<25} {'交还用户决策，不恢复':<30} {'-':<16}")

    # 4. 等待用户选择
    while True:
        choice = input(f"\n请选择恢复点序号（0-{len(recovery_points)}）：").strip()
        if choice == "0":
            return "ABORT"
        try:
            idx = int(choice)
            if 1 <= idx <= len(recovery_points):
                selected = recovery_points[idx - 1]
                print(f"\n✓ 已选择恢复点：{selected['node_id']} @ {selected['timestamp']}")
                print(f"  状态哈希：{selected['state_hash']}")
                print(f"  将回滚 {selected['downstream_count']} 个下游节点")
                return selected["snapshot_key"]
        except ValueError:
            pass
        print("无效输入，请重新选择。")
```

**恢复点列表字段**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `序号` | int | 用户选择的序号 |
| `node_id` | string | 检查点对应的节点 ID（通常为 Gate 节点） |
| `timestamp` | string | 快照时间戳（ISO 8601） |
| `state_summary` | string | 状态摘要（已完成节点数/总节点数、当前 Phase） |
| `state_hash` | string | 状态哈希前 12 位（用于审计追溯） |
| `downstream_count` | int | 回滚到该点将影响的下游节点数 |

**恢复点选择规则**：
1. **默认推荐**：最近的 Gate 通过点（最少回滚量）
2. **保守选项**：上一个 Phase 的入口点（回滚量较大但更稳定）
3. **激进选项**：失败节点的前一个节点（回滚量最小但可能不稳定）
4. **中止选项**：序号 0，交还用户决策，不恢复

> **与 LangGraph interrupt_before 的协同**：恢复点选择 UI 通过 LangGraph 的 `interrupt_before` 机制实现暂停，等待用户输入后恢复执行。这与 T00b（人设采集）和 I01（迭代深化）的交互机制一致。

---

## 4. Phase 2 — 门控

### 4.1 三道门控定义

```yaml
gates:
  gate_alpha:
    name: "Gate-α — 研究底座门控"
    trigger: "T01~T06 全部完成"
    description: "验证九层研究底座覆盖度与层间一致性"
    checks:
      - check: "T06-nine-layer-coverage"
        condition: "九层研究底座覆盖至少 7 层"
        severity: "blocking"
        message: "研究底座至少需要覆盖九层中的 7 层"

      - check: "T06-layer-consistency"
        condition: "层间无逻辑矛盾或事实冲突"
        severity: "blocking"
        message: "各层结论必须自洽，层级间推理必须连贯"

      - check: "T00-outline-alignment"
        condition: "T02~T06 产出与 T00 大纲方向一致"
        severity: "warning"
        message: "研究底座产出应与 T00 研究大纲对齐"

    on_blocking_failure:
      action: "退回至覆盖缺失层，穷尽重试直至覆盖"
      note: "EXHAUST 模式下不存在 exhausted_action，持续重试直至通过"

  gate_beta:
    name: "Gate-β — 认知流水线门控"
    trigger: "T08~T13 全部完成"
    description: "验证认知分析链的完整性、推理质量和魔鬼代言人反馈吸收"
    checks:
      - check: "T13-inputs-all-present"
        condition: "T13 综合了 T10/T11/T12 的产出"
        severity: "blocking"
        message: "T13 必须综合所有对抗攻击的输出"

      - check: "T09-paths-complete"
        condition: "T09 推理路径数与 mode_parameters[execution_mode].paths 一致且均已完整执行"
        severity: "blocking"
        message: "多路径推理必须产出 7 条独立推理路径（EXHAUST 模式唯一档位）"

      - check: "T13-adversarial-absorption"
        condition: "T13 至少吸收 1 个魔鬼代言人反馈"
        severity: "blocking"
        message: "认知综合必须吸收至少 1 条魔鬼代言人反馈"

      - check: "T10-T12-adversarial-done"
        condition: "T10/T11/T12 均依赖 T09 完成"
        severity: "blocking"
        message: "对抗三件套必须全部完成"

    on_blocking_failure:
      action: "退回至 T08 重新认知解构，穷尽重试"
      note: "EXHAUST 模式下不存在 exhausted_action，持续重试直至通过"

  gate_gamma:
    name: "Gate-γ — 领域分析门控"
    trigger: "T15 完成"
    description: "验证 T15 领域引擎覆盖度"
    checks:
      - check: "T15-engines-all-activated"
        condition: "T15.activated_engines 包含 T00 推荐的全部引擎"
        severity: "blocking"
        message: "T15 必须激活 T00 推荐的所有领域引擎"

      - check: "T15-analysis-depth"
        condition: "每个领域引擎产出充分的专项分析"
        severity: "warning"
        message: "领域分析应达到合理深度"

    on_blocking_failure:
      action: "退回至 T15 补充缺失领域，穷尽重试"
      note: "EXHAUST 模式下不存在 exhausted_action，持续重试直至通过"
```

### 4.2 门控聚合逻辑

```yaml
gate_aggregation:
  rule: "blocking 检查全部通过 → gate PASS"
  rule: "仅 warning 级失败 → gate PASS_WITH_WARNINGS"
  rule: "任一 blocking 失败 → gate FAIL → 退回修正"

  cross_gate_dependency:
    - "Gate-α (T07) 通过后，T08 被标记为就绪"
    - "Gate-β (T14) 通过后，T15 被标记为就绪"
    - "Gate-γ (T16) 通过后，T17/T18 被标记为就绪"
```

---

## 5. Phase 3 — 终局

### 5.1 ORCHESTRATOR 职责

Phase 3 由主LLM的 ORCHESTRATOR 模块负责：

```yaml
phase_3:
  orchestrator:
    description: "Phase 3 终局编排器（ORCHESTRATOR 由主LLM独立调用，不属 DAG 节点）"

    step_1_score:
      description: "三维度独立评分（不写入最终输出）"
      actions:
        - 内洽度 (1-10)：各层结论是否自洽，层级间推理是否连贯
        - 创新度 (1-10)：是否产出超越常识层面的洞察
        - 实用度 (1-10)：对用户原始问题的解决力度
      output: "不写入最终输出，仅用于质量判定"

    step_2_quality_verdict:
      description: "基于三维度评分生成质量判定"
      rules:
        - "GREEN (三项均 ≥ 6) → T20 正常渲染"
        - "YELLOW (任一 < 6 但 ≥ 4) → T20 渲染时附带置信度标注"
        - "RED (任一 < 4) → 退回 Phase 1 穷尽重试，穷尽重试，标记问题节点重执行"

    step_3_assemble_canvas:
      description: "组装最终输出画布"
      actions:
        - 按 T20 要求的格式组织全部流水线产出
        - 注入 RETRYING 节点的穷尽重试标注
        - 剥离 ORCHESTRATOR 评分与 verdict，不污染最终输出

    step_4_invoke_T20:
      description: "调用 T20 输出渲染"
      actions:
        - 传递完整画布给 T20 Sub-Agent
        - 按成品类型选择渲染模板
        - 等待渲染完成

    step_5_deliver:
      description: "向用户交付最终输出"
      actions:
        - 输出 T20.final_output
        - 附加 RETRYING 节点说明 (如有)
        - 附加质量评估摘要
```

### 5.2 终局输出结构

```yaml
final_delivery:
  main_output:
    type: "T20.final_output"
    description: "面向用户的最终渲染文档"

  quality_annex:
    type: "QualityAnnex"
    description: "内部质量评估附件 (用户不可见)"
    fields:
      total_tasks: "integer"
      completed_tasks: "integer"
      RETRYING_tasks: "integer"
      failed_checks_summary: "array"
      overall_confidence: "float (0-1)"

  retrying_notice:
    type: "RetryingNotice"
    description: "穷尽重试节点说明 (如无 RETRYING 则省略)"
    fields:
      RETRYING_task_id: "string"
      missing_content: "string"
      impact_on_output: "string"
      mitigation_applied: "string"
```

---

## 6. 异常处理

### 6.1 超时处理

```yaml
timeout_policy:
  sub_agent_timeout:
    default: null  # EXHAUST 模式：不设超时上限
    on_timeout:
      action: "标记 FAIL，进入穷尽重试流程（无次数上限）"
      note: "超时不等于放弃，持续重试直至通过"

  gate_timeout:
    default: null  # EXHAUST 模式：不设超时上限
    on_timeout:
      action: "持续重试，穷尽重试直至通过"
```

### 6.2 资源压力处理（EXHAUST 一致性）

```yaml
resource_pressure:
  context_budget_tight:
    action: "缩减并行度 (3→2→1) 以降低单轮上下文压力，持续重试未通过节点（质量保持、不跳过、不终止）——并行度调整是工程调度，不构成对 EXHAUST 'Token 不设上限'的违反"

  context_window_full:
    action: "将已完成节点的完整输出卸载到 context_package summary 并写入 Checkpoint 文件，释放上下文后继续（不降低质量标准、不丢弃分析维度）"
```

---

## 7. 执行遥测（R10-02）

### 7.1 概述

**方法论原理**：执行遥测基于"可观测性是系统可靠性的基础"的认知假设：长流程认知分析需要可观测的执行指标，使开发者与用户能复盘执行过程、定位性能瓶颈、优化资源分配。本协议定义 5 类遥测数据的采集、写入 OpenTelemetry span、会话后聚合报告的完整流程。

### 7.2 5 类遥测数据定义（SubTask 5.2.1）

每个 DAG 节点执行时，必须采集以下 5 类遥测数据：

| 遥测数据 | 字段名 | 类型 | 说明 |
|---------|--------|------|------|
| 起止时间 | `start_time` / `end_time` | ISO8601 字符串 | 节点执行的起止时间戳，用于计算执行耗时 |
| 输入/输出 Token | `input_tokens` / `output_tokens` | integer | 节点执行的输入 token 数与输出 token 数（由 tiktoken 精确计数，见 context-budget-protocol.md §2.3） |
| 重试次数 | `retry_count` | integer | 节点 Supervisor 判定 FAIL 后的重试次数（EXHAUST 模式下不设上限） |
| Supervisor 判定 | `supervisor_verdict` | string | 节点的 Supervisor 判定结果：PASS / PASS_WITH_WARNINGS / FAIL |
| Gate 结果 | `gate_result` | string | 节点所属 Gate 的检查结果（仅 Gate 节点填写）：PASS / PASS_WITH_WARNINGS / FAIL |

```yaml
telemetry_data:
  node_id: "T05"
  start_time: "2026-06-25T10:30:00.123Z"
  end_time: "2026-06-25T10:32:15.456Z"
  input_tokens: 12500
  output_tokens: 3800
  retry_count: 0
  supervisor_verdict: "PASS"
  gate_result: null  # 非 Gate 节点为 null
```

### 7.3 遥测数据写入 OpenTelemetry span（SubTask 5.2.2）

每个 DAG 节点执行时，创建一个 OpenTelemetry span，将 5 类遥测数据作为 span 属性写入。

#### 7.3.1 OpenTelemetry 集成方式

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
import tiktoken

# 初始化 TracerProvider
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer("profound-cognition.execution")

# 配置 exporter（OTLP HTTP 默认端口 4318）
otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces")
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)


def make_node_with_telemetry(task_id: str):
    """为 DAG 节点生成带遥测的 LangGraph 节点函数。"""
    def node_fn(state: ResearchState) -> ResearchState:
        with tracer.start_as_current_span(f"node.{task_id}") as span:
            # 记录起止时间与输入 token
            start_time = get_iso_timestamp()
            span.set_attribute("node.id", task_id)
            span.set_attribute("node.start_time", start_time)

            context_package = assemble_context_package(
                task_id=task_id,
                problem=state["context_package"]["problem"],
                output_type=state["context_package"]["output_type"],
                upstream_nodes=state["node_outputs"],
            )
            input_tokens = count_tokens(str(context_package))
            span.set_attribute("node.input_tokens", input_tokens)

            # 调用 Sub-Agent
            sub_agent_result = invoke_sub_agent(
                task_id=task_id,
                context_package=context_package,
                task_file=load_task_file(task_id),
            )
            output_tokens = count_tokens(str(sub_agent_result))
            span.set_attribute("node.output_tokens", output_tokens)

            # Supervisor 判定
            verdict = invoke_supervisor(
                task_id=task_id,
                sub_agent_output=sub_agent_result,
                gate_config=get_gate_config(task_id),
            )
            span.set_attribute("node.supervisor_verdict", verdict)

            # 重试次数（从 execution_ledger 统计）
            retry_count = count_retries(state["execution_ledger"], task_id)
            span.set_attribute("node.retry_count", retry_count)

            # Gate 结果（仅 Gate 节点）
            if is_gate_node(task_id):
                gate_result = verdict  # Gate 节点的 verdict 即 gate_result
                span.set_attribute("node.gate_result", gate_result)

            end_time = get_iso_timestamp()
            span.set_attribute("node.end_time", end_time)

            # 写入 execution_ledger
            state["execution_ledger"].append({
                "task_id": task_id,
                "status": "completed" if verdict in ("PASS", "PASS_WITH_WARNINGS") else "retrying",
                "telemetry": {
                    "start_time": start_time,
                    "end_time": end_time,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "retry_count": retry_count,
                    "supervisor_verdict": verdict,
                    "gate_result": verdict if is_gate_node(task_id) else None,
                },
            })
        return state
    return node_fn
```

#### 7.3.2 Span 命名规范

| Span 类型 | 命名格式 | 示例 |
|----------|---------|------|
| 节点执行 | `node.{task_id}` | `node.T05` |
| Gate 检查 | `gate.{gate_id}` | `gate.T07` |
| Phase 执行 | `phase.{phase_id}` | `phase.1` |
| 会话 | `session.{session_id}` | `session.uuid-1234` |

#### 7.3.3 Span 属性规范

所有 span 必须包含以下标准属性：

| 属性 | 类型 | 说明 |
|------|------|------|
| `node.id` | string | 节点 ID |
| `node.start_time` | string | 起始时间（ISO8601） |
| `node.end_time` | string | 结束时间（ISO8601） |
| `node.input_tokens` | int | 输入 token 数 |
| `node.output_tokens` | int | 输出 token 数 |
| `node.retry_count` | int | 重试次数 |
| `node.supervisor_verdict` | string | Supervisor 判定 |
| `node.gate_result` | string | Gate 结果（仅 Gate 节点） |
| `session.id` | string | 会话 ID（根 span 属性） |
| `framework.version` | string | 框架版本（6.0.0） |

#### 7.3.4 回退策略

若 OpenTelemetry 库不可用（ImportError）或 OTLP collector 不可达：
- 遥测数据仍写入 execution_ledger（不依赖 OpenTelemetry）
- 在 execution_ledger 中标注 `telemetry_export: "ledger_only"`（正常为 `otel_span`）
- 会话结束后从 execution_ledger 聚合生成遥测报告（功能不降级）

### 7.4 会话结束后执行遥测报告（SubTask 5.2.3）

会话结束后（Phase 3 终局完成或用户中止），从 execution_ledger 中提取所有节点的遥测数据，生成执行遥测报告。

#### 7.4.1 报告内容

```yaml
execution_telemetry_report:
  session_id: "会话ID"
  session_start: "ISO8601"
  session_end: "ISO8601"
  total_duration_seconds: float
  total_nodes_executed: integer
  total_input_tokens: integer
  total_output_tokens: integer
  total_retries: integer

  # Top-5 节点执行时间
  top5_execution_time:
    - {node_id: "T15", duration_seconds: 125.3, percent: 18.5%}
    - {node_id: "T09", duration_seconds: 98.7, percent: 14.6%}
    - {node_id: "T13", duration_seconds: 87.2, percent: 12.9%}
    - {node_id: "T02", duration_seconds: 65.4, percent: 9.7%}
    - {node_id: "T17", duration_seconds: 52.1, percent: 7.7%}

  # Top-5 节点 Token 消耗
  top5_token_consumption:
    - {node_id: "T15", input_tokens: 25000, output_tokens: 8000, total: 33000}
    - {node_id: "T09", input_tokens: 18000, output_tokens: 12000, total: 30000}
    - {node_id: "T13", input_tokens: 22000, output_tokens: 6500, total: 28500}
    - {node_id: "T02", input_tokens: 5000, output_tokens: 15000, total: 20000}
    - {node_id: "T06", input_tokens: 12000, output_tokens: 7500, total: 19500}

  # Top-5 节点重试次数
  top5_retry_count:
    - {node_id: "T13", retry_count: 4, last_verdict: "PASS"}
    - {node_id: "T09", retry_count: 2, last_verdict: "PASS"}
    - {node_id: "T17", retry_count: 1, last_verdict: "PASS_WITH_WARNINGS"}
    - {node_id: "T05", retry_count: 1, last_verdict: "PASS"}
    - {node_id: "T15", retry_count: 0, last_verdict: "PASS"}

  # Gate 通过率
  gate_pass_rate:
    gate_alpha: {verdict: "PASS", retry_count: 1, duration_seconds: 12.3}
    gate_beta: {verdict: "PASS", retry_count: 2, duration_seconds: 18.7}
    gate_gamma: {verdict: "PASS", retry_count: 0, duration_seconds: 8.5}
    gate_terminal: {verdict: "PASS", retry_count: 0, duration_seconds: 15.2}
    gate_delta: {verdict: "PASS", retry_count: 1, duration_seconds: 22.1}
    overall_pass_rate: 1.0  # 5/5 Gate 通过

  # 优化建议（基于遥测数据自动生成）
  optimization_suggestions:
    - "T15 执行时间占比 18.5%，建议优化领域引擎分析效率"
    - "T13 重试 4 次，建议检查 Supervisor 检查项是否过于严格"
    - "Gate-β 重试 2 次，建议检查 T08-T13 流水线质量"
```

#### 7.4.2 报告生成流程

```python
def generate_telemetry_report(execution_ledger: list, session_id: str) -> dict:
    """会话结束后生成执行遥测报告。"""
    telemetry_entries = [e for e in execution_ledger if "telemetry" in e]

    # 计算每个节点的执行时间
    node_durations = []
    for entry in telemetry_entries:
        t = entry["telemetry"]
        duration = parse_iso(t["end_time"]).timestamp() - parse_iso(t["start_time"]).timestamp()
        node_durations.append({
            "node_id": entry["task_id"],
            "duration_seconds": duration,
            "input_tokens": t["input_tokens"],
            "output_tokens": t["output_tokens"],
            "retry_count": t["retry_count"],
            "supervisor_verdict": t["supervisor_verdict"],
        })

    # Top-5 排序
    top5_time = sorted(node_durations, key=lambda x: x["duration_seconds"], reverse=True)[:5]
    top5_tokens = sorted(node_durations, key=lambda x: x["input_tokens"] + x["output_tokens"], reverse=True)[:5]
    top5_retries = sorted(node_durations, key=lambda x: x["retry_count"], reverse=True)[:5]

    # Gate 通过率
    gate_entries = [e for e in telemetry_entries if e["task_id"].startswith("T07") or
                    e["task_id"].startswith("T14") or e["task_id"].startswith("T16") or
                    e["task_id"].startswith("T28") or e["task_id"].startswith("T_gate_delta")]
    gate_pass_count = sum(1 for e in gate_entries if e["telemetry"]["supervisor_verdict"] in ("PASS", "PASS_WITH_WARNINGS"))
    gate_pass_rate = gate_pass_count / len(gate_entries) if gate_entries else 0

    return {
        "session_id": session_id,
        "top5_execution_time": top5_time,
        "top5_token_consumption": top5_tokens,
        "top5_retry_count": top5_retries,
        "gate_pass_rate": gate_pass_rate,
        # ... 其他字段
    }
```

### 7.5 遥测报告写入 docs/telemetry/ 目录（SubTask 5.2.4）

遥测报告生成后，写入 `docs/telemetry/` 目录，文件名格式为 `telemetry-report_{session_id}_{YYYYMMDD}.json`。

```python
import json
from pathlib import Path

def save_telemetry_report(report: dict, session_id: str) -> str:
    """保存遥测报告到 docs/telemetry/ 目录。"""
    telemetry_dir = Path("docs/telemetry")
    telemetry_dir.mkdir(parents=True, exist_ok=True)

    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"telemetry-report_{session_id}_{date_str}.json"
    filepath = telemetry_dir / filename

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    return str(filepath)
```

**目录结构**：
```
docs/telemetry/
├── README.md                                    # 格式说明
├── telemetry-report_{session_id_1}_{date}.json  # 会话 1 的遥测报告
├── telemetry-report_{session_id_2}_{date}.json  # 会话 2 的遥测报告
└── token-count-report_{session_id}.json         # token 计数聚合报告（context-budget-protocol §3.5.3）
```

**报告保留策略**：
- 最近 100 个会话的遥测报告永久保留
- 超过 100 个的旧报告自动归档到 `docs/telemetry/archive/`
- 归档报告超过 1 年自动删除

---

## 附录

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| v2.0 | 2026-05-15 | 初始发布：Phase 0-3 DAG 执行框架、三道门控、ORCHESTRATOR 终局 |
| v3.1 | 2026-06-17 | 节点数修正为 58、任务范围修正为 T_env_probe ~ T_gate_delta、EXHAUST 一致性强化 |

### B. 术语表

| 术语 | 英文 | 定义 |
|------|------|------|
| DAG | Directed Acyclic Graph | 有向无环图，定义任务间的依赖和调度顺序 |
| Sub-Agent | Sub-Agent | 执行单个任务的独立 Agent 实例 |
| Supervisor | Supervisor | 独立检查员，逐项检查 Sub-Agent 产出 |
| Gate | Gate | 门控检查点，在阶段转换时验证产出质量 |
| ORCHESTRATOR | ORCHESTRATOR | Phase 3 终局编排器，负责汇总和交付 |
| RETRYING | RETRYING | 节点穷尽重试状态，持续重试直至通过，不存在质量妥协路径 |

### C. 交叉引用

- [handoff-protocol.md](./handoff-protocol.md) — Context Package 标准格式
- [exhaust-retry-protocol.md](./exhaust-retry-protocol.md) — 节点失败穷尽重试策略
- `supervisors/supervisor_protocol.md` — Supervisor 判定标准
- `tasks/` — 各任务定义文件（58 节点：T_env_probe ~ T_gate_delta）


---
© 阿洋


---

## 测试用例 (D3.4.4)

### 测试用例 1：DAG 就绪节点识别

**给定输入**：DAG 中 T01 无依赖，T02 deps=[T01]，T03 deps=[T01]，T04 deps=[T02,T03]。当前 T01 已完成。

**应产出**：find_ready_nodes() 返回 [T02, T03]（并行就绪），T04 不在就绪列表中（依赖未满足）。

### 测试用例 2：Gate 失败回退

**给定输入**：Gate-α 检查 T01-T06 产出，发现 T03 的 self_check_score=70（< 85 阈值），判定为 fail。

**应产出**：触发 T03 回退，重新执行 T03；T04/T05/T06（依赖 T03）状态清理为 pending；回退日志记录触发节点=T03、影响范围=[T04,T05,T06]。

### 测试用例 3：并行节点执行

**给定输入**：T10/T11/T12 三个对抗节点 deps=[T09]，T09 已完成。

**应产出**：T10/T11/T12 同时进入就绪状态，并行执行，结果在 T12b 汇聚。

### 测试用例 4：循环检测

**给定输入**：DAG 中存在 A→B→C→A 的循环依赖。

**应产出**：拓扑排序检测到循环，输出错误"Cycle detected: A→B→C→A"，拒绝执行。
