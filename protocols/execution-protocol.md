> **作者**: 阿洋

# 执行协议 (Execution Protocol)

> > **状态**: 正式发布
> **适用范围**: Profound Cognition 主LLM调度执行参考
> **最后更新**: 2026-05-15

---

## 1. 协议概述

### 1.1 目的

ExecutionProtocol 定义 Profound Cognition 中主LLM的 Phase 0-3 执行规则。该协议建立了基于 DAG 的多任务调度框架，确保 57 个节点按依赖关系有序执行，并通过 Supervisor 门控机制保证每个阶段的产出质量。

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
  step_1_understand:
    description: "完整理解用户问题"
    actions:
      - 提取原始问题核心语义
      - 识别隐含预设与偏见框架
      - 推断成品类型 (output_type)

  step_2_dag_generation:
    description: "生成任务 DAG"
    actions:
      - 加载完整任务依赖定义 (tasks/T_env_probe ~ T_gate_delta，共 57 节点)
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

> **SSOT 声明**：SKILL.md 是 DAG 拓扑的唯一真实源（Single Source of Truth），包含 57 个节点的完整定义。本节仅提供 Phase 1-3 的简化 DAG 示例格式供参考，完整 DAG 拓扑（含 Phase 7 的 19 个元维度/科学层节点）以 SKILL.md 为准。若本节与 SKILL.md 冲突，以 SKILL.md 为准。

主LLM生成的 DAG 使用以下结构：

```yaml
dag:
  version: "2"
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

## 2.7 T01c 交互等待协议

T01c（输入情绪基调提取）是 DAG 中唯一需要多轮用户对话的节点。

### 2.7.1 执行流程

```
T01c 首轮调用
    ↓
T01c 输出问题集 + validation_status
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
                         携带历史问答重新调用 T01c
                                ↓
                         回到检查点（质量驱动终止）
```

### 2.7.2 WAITING_FOR_USER 状态定义

- **trigger**: T01c 输出 `validation_status == "INCOMPLETE"`
- **phase**: 仅在 Phase 1 DAG 调度循环中有效
- **behavior**: 暂停 find_ready_nodes() 调度循环，向用户输出问题集，等待用户回答
- **resume_trigger**: 用户提供新信息后，重新调用 T01c Sub-Agent
- **rounds_policy**: 不设上限，质量驱动终止
- **on_quality_satisfied**: 使用已收集信息生成最优 persona_card，标注缺失项，强制 COMPLETE
- **on_error**: 记录到 retrying_log，持续重试 T01c 直至用户回复有效输入，不设重试上限，不使用默认人设替代，质量保持

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
- 每轮 T01c 的 tok 预算：400 tok
- 用户主动放弃：回复放弃信号后触发穷尽重试（见上方 §2.7.3 用户主动放弃规则）
- 质量驱动终止：INCOMPLETE 字段持续穷尽重试直至 COMPLETE 或用户主动放弃
- T01c route: always（所有 output_type 均激活）

## 3. Phase 1 — 执行

### 3.1 执行循环

主LLM在 Phase 1 中进入调度循环，伪代码如下：

```python
# === Phase 1 DAG 调度伪代码 ===

def phase_1_execution(dag: DAG, gate_config: GateConfig) -> None:
    """
    主LLM的 Phase 1 调度循环。
    每个节点执行: 找就绪 → 组装context_package → 调用Sub-Agent → Supervisor判定
    """

    todo_list = TodoWrite.load_all_nodes(dag.nodes)

    while not all_nodes_done(dag.nodes):
        # Step 1: 找就绪节点
        ready_nodes = find_ready_nodes(dag.nodes, todo_list)

        if not ready_nodes:
            # 检查是否全部完成或存在阻塞
            blocked_nodes = find_blocked_nodes(dag.nodes, todo_list)
            if blocked_nodes:
                # EXHAUST 模式：不存在 MAX_RETRIES，节点持续重试直至通过
                for node in blocked_nodes:
                    if node.status == "retrying":
                        # 注入修正指令，重新执行
                        inject_retry_instruction(node)
                        continue
            break

        # Step 2: 并行调度就绪节点
        for node in ready_nodes:
            todo_list.mark(node.task_id, "in_progress")

        # Step 3: 组装 context_package
        for node in ready_nodes:
            context_package = assemble_context_package(
                task_id=node.task_id,
                problem=dag.problem,
                output_type=dag.output_type,
                upstream_nodes=get_upstream_outputs(node, dag)
            )

            # Step 4: 调用 Sub-Agent
            sub_agent_result = invoke_sub_agent(
                task_id=node.task_id,
                context_package=context_package,
                task_file=load_task_file(node.task_id)
            )

            # Step 5: Supervisor 判定
            verdict = invoke_supervisor(
                task_id=node.task_id,
                sub_agent_output=sub_agent_result,
                gate_config=get_gate_config(node.gate)
            )

            # Step 6: 分支处理
            if verdict == "PASS":
                store_output(node.task_id, sub_agent_result, "COMPLETED")
                todo_list.mark(node.task_id, "completed")

            elif verdict == "PASS_WITH_WARNINGS":
                store_output(node.task_id, sub_agent_result, "COMPLETED")
                node.warning_count += 1
                if node.warning_count_consecutive >= 3:
                    # 提升严格度
                    node.strict_mode = True
                todo_list.mark(node.task_id, "completed")

            elif verdict == "FAIL":
                # EXHAUST 模式：不存在重试次数上限，持续重试直至通过
                node.retry_count += 1
                # 持续重试：将 Supervisor 退回指令传递给 Sub-Agent
                retry_instruction = verdict.retry_instruction
                todo_list.mark(node.task_id, "in_progress")
                # 下一次循环会重新调度此节点（无上限重试）


def find_ready_nodes(nodes: list, todo_list: TodoList) -> list:
    """查找所有依赖已满足且状态为 pending 的节点"""
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


def assemble_context_package(task_id: str, problem: str,
                              output_type: str, upstream_nodes: list) -> dict:
    """
    组装 context_package。
    按 handoff-protocol.md 标准格式构造。
    """
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

## 附录

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| v2.0 | 2026-05-15 | 初始发布：Phase 0-3 DAG 执行框架、三道门控、ORCHESTRATOR 终局 |
| v3.1 | 2026-06-17 | 节点数修正为 57、任务范围修正为 T_env_probe ~ T_gate_delta、EXHAUST 一致性强化 |

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
- `tasks/` — 各任务定义文件（57 节点：T_env_probe ~ T_gate_delta）


---
© 阿洋
