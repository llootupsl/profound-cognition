<!-- 作者：阿洋 -->

# User Feedback Protocol — 用户反馈事件化协议 (User Feedback Event-Driven Protocol) v3.0

## 概述

**方法论原理**：用户反馈协议基于"反馈是认知校准的核心机制"的认知假设：用户反馈不是简单的纠错信号，而是认知系统校准其理解与用户期望之间差距的关键输入。将反馈事件化处理，使每次反馈都成为系统改进的机会。

本协议定义用户在 DAG 执行过程中提出反馈的标准处理流程。用户的反馈被分类为三种事件类型，每种类型对应不同的回滚范围和重执行策略。

## 反馈事件类型

### 1. USER_NEW_HYPOTHESIS — 用户提出更强假设

**触发条件**：用户提出了 T09 推理路径中未覆盖的新假设或替代解释

**处理流程**：
1. Orchestrator 触发 Phase 2.5 用户反馈处理
2. 分类为 `USER_NEW_HYPOTHESIS`
3. 将新假设注入 T09（多路径推理），作为新的推理路径补充
4. 回滚范围：T09 → T10 → T11 → T12 → T13（如已执行）
5. 重执行 T09：在新假设路径上执行推理
6. 重执行 T10/T11/T12：对新推理路径进行对抗验证
7. 重执行 T13：整合新旧假设的结论
8. 产出 `hypothesis_merge_report`：对比新旧假设的结论差异

**回滚规则**：
- 已通过 Gate 的上游节点（T07/T14/T16 之前）不变
- 若 T13 还未执行 → 仅回滚 T09/T10/T11/T12
- 若 T13 已执行 → 回滚到 T09，重走 T09→T10→T11→T12→T13

### 2. USER_STRONGER_REFUTATION — 用户提出更有力反驳

**触发条件**：用户对对抗验证结果不满意，提供了新的反驳角度或证据

**处理流程**：
1. 分类为 `USER_STRONGER_REFUTATION`
2. 判断新反驳属于哪个维度：
   - 逻辑层面 → 注入 T10
   - 证据层面 → 注入 T11
   - 范围层面 → 注入 T12
3. 回滚到对应的对抗节点重新执行
4. T13 重新综合时纳入新反驳

**回滚规则**：
- 不改变已通过 Gate 的上游节点结论
- 仅回滚受影响的对抗节点及下游
- 若 T13 已执行 → 回滚范围：对应对抗节点 → T13

### 3. USER_OUTPUT_CORRECTION — 用户提出成品形态纠偏

**触发条件**：用户对输出格式不满意（如 "字号太小"、"需要加入分割线"、"配色改暖色"）

**处理流程**：
1. 分类为 `USER_OUTPUT_CORRECTION`
2. 不触发认知流水线回滚（T01-T19 不变）
3. 仅重执行 T20 渲染节点
4. T20 重新渲染时应用用户的新格式约束

**回滚规则**：
- 最小回滚范围：仅 T20 渲染节点
- T01-T19 流水线产出完全保留
- 用户可指定具体的格式修复要求

## Phase 2.5 用户反馈处理流程

```
ON user_feedback_received:
  CLASSIFY feedback type
  CASE:
    USER_NEW_HYPOTHESIS:
      ROLLBACK to T09
      INJECT new hypothesis into T09 reasoning paths
      RERUN T09 → T10 → T11 → T12 → T13
      OUTPUT hypothesis_merge_report

    USER_STRONGER_REFUTATION:
      IDENTIFY affected adversarial node (T10/T11/T12)
      ROLLBACK to affected node
      INJECT new refutation
      RERUN affected node → T13

    USER_OUTPUT_CORRECTION:
      RERUN T20 only
      APPLY user format constraints
```

## 输出

- `feedback_classification`: 事件分类
- `rollback_scope`: 回滚的节点范围
- `merge_report` (仅 USER_NEW_HYPOTHESIS): 新旧假设对比报告
- `rerun_summary`: 重执行摘要

## 交叉引用

- [nrsf-protocol.md](./nrsf-protocol.md) — NRSF 叙事式研究状态文件协议
- [checkpoint-protocol.md](./checkpoint-protocol.md) — Checkpoint 原子写入与断点续传协议

## v3.0 用户反馈扩展 (元层反馈)

### 新增反馈事件类型

| 事件类型 | 触发条件 | 目标节点 | 穷尽尝试路径 |
|----------|----------|----------|----------|
| USER_META_LAYER_FEEDBACK | 用户对元层分析结果提出修正 | T26 | T26→T27→T28→T_gate_delta |
| USER_SCENARIO_OVERRIDE | 用户要求修改情景假设 | T25 | T25→T26→T27→T28→T_gate_delta |
| USER_ETHICS_CONCERN | 用户提出伦理担忧 | T26 Step7 | T26→T27→T28→T_gate_delta |
| USER_ONTOLOGY_CORRECTION | 用户修正知识图谱实体/关系 | T28 | T28→T_gate_delta |

### 反馈处理规则
1. 元层反馈优先级高于经典层反馈
2. 伦理反馈(USER_ETHICS_CONCERN)必须触发T26重新执行Step7
3. 情景覆盖反馈(USER_SCENARIO_OVERRIDE)需重新执行T25 Step8-10
4. 本体修正反馈(USER_ONTOLOGY_CORRECTION)需重新执行T28 Step7验证
## 反馈闭环验证（R10-06）

> **方法论原理**：反馈闭环验证基于"反馈不等于解决"的认知假设：用户提出反馈后，框架重新执行并产出新输出，但新输出是否真正解决了用户的反馈？本章节定义 feedback_item 结构化格式、feedback_resolution_check 子步骤、三级评定、解决率统计与用户确认闭环，确保每次反馈都形成完整闭环。

### feedback_item 结构化格式（SubTask 5.4.1）

用户反馈被解析为结构化的 feedback_item，作为反馈处理与闭环验证的基础：

```yaml
feedback_item:
  feedback_id: "string — 反馈唯一标识（fb_{uuid}）"
  user_id: "string — 用户 ID"
  session_id: "string — 会话 ID"
  timestamp: "ISO8601 — 反馈提出时间"

  # 反馈分类
  feedback_type: "USER_NEW_HYPOTHESIS | USER_STRONGER_REFUTATION | USER_OUTPUT_CORRECTION | USER_META_LAYER_FEEDBACK | USER_SCENARIO_OVERRIDE | USER_ETHICS_CONCERN | USER_ONTOLOGY_CORRECTION"
  target_node: "string — 反馈针对的节点 ID（如 T09/T10/T13/T20/T26 等）"
  rollback_scope: ["string — 回滚的节点范围"]

  # 反馈内容（结构化）
  feedback_content:
    summary: "string — 反馈摘要（≤200字）"
    details: "string — 反馈详细描述"
    expected_change: "string — 用户期望的变更"
    evidence_provided: ["string — 用户提供的证据/参考链接"]

  # 反馈处理状态
  status: "received | processing | rerun_completed | resolution_checked | user_confirmed | closed"
  processing_log:
    - {step: "classify", timestamp: "ISO8601", result: "USER_NEW_HYPOTHESIS"}
    - {step: "rollback", timestamp: "ISO8601", result: "T09→T10→T11→T12→T13"}
    - {step: "rerun", timestamp: "ISO8601", result: "completed"}
    - {step: "resolution_check", timestamp: "ISO8601", result: "resolved"}
    - {step: "user_confirm", timestamp: "ISO8601", result: "confirmed"}

  # 闭环验证结果（见下方 feedback_resolution_check）
  resolution_check:
    verdict: "resolved | partially_resolved | unresolved"
    match_score: "float — 重新执行输出与 feedback_item 的匹配度（0-1）"
    addressed_points: ["string — 已解决的反馈点"]
    unaddressed_points: ["string — 未解决的反馈点"]
    llm_judge_rationale: "string — LLM 判定理由"

  # 用户确认（见下方用户确认闭环）
  user_confirmation:
    confirmed: "boolean — 用户是否确认反馈已解决"
    user_feedback_on_resolution: "string — 用户对解决结果的反馈"
    timestamp: "ISO8601"
```

### feedback_resolution_check 子步骤（SubTask 5.4.2）

反馈处理并重新执行后，必须进行 feedback_resolution_check，由 LLM 对比重新执行输出与原始 feedback_item，判定反馈是否真正解决：

```python
def feedback_resolution_check(feedback_item: dict, rerun_output: dict) -> dict:
    """反馈解决验证（R10-06）。

    LLM 对比重新执行输出与原始 feedback_item，判定反馈是否真正解决。

    Args:
        feedback_item: 原始反馈项（含 feedback_content.expected_change）
        rerun_output: 重新执行后的节点输出

    Returns:
        resolution_check: 解决验证结果
    """
    # 构造 LLM 判定提示词
    prompt = f"""
你是一个严格的反馈解决验证员。你的任务是判定重新执行的输出是否真正解决了用户的反馈。

## 用户原始反馈
- 摘要：{feedback_item['feedback_content']['summary']}
- 详细描述：{feedback_item['feedback_content']['details']}
- 期望变更：{feedback_item['feedback_content']['expected_change']}
- 提供证据：{feedback_item['feedback_content']['evidence_provided']}

## 重新执行后的输出
{json.dumps(rerun_output, ensure_ascii=False, indent=2)}

## 判定规则
1. 逐条检查 feedback_item 中的每个期望变更点，是否在重新执行输出中得到解决
2. 判定级别：
   - resolved：所有期望变更点都已解决（match_score ≥ 0.8）
   - partially_resolved：部分期望变更点已解决（0.5 ≤ match_score < 0.8）
   - unresolved：大部分期望变更点未解决（match_score < 0.5）
3. 列出已解决点（addressed_points）和未解决点（unaddressed_points）
4. 给出判定理由（llm_judge_rationale）

## 输出格式（JSON）
{{
  "verdict": "resolved | partially_resolved | unresolved",
  "match_score": 0.0-1.0,
  "addressed_points": ["已解决的反馈点"],
  "unaddressed_points": ["未解决的反馈点"],
  "llm_judge_rationale": "判定理由"
}}
"""

    # 调用 LLM 判定
    result = invoke_llm_judge(prompt)

    # 更新 feedback_item
    feedback_item["resolution_check"] = result
    feedback_item["status"] = "resolution_checked"

    return result
```

### 三级评定（SubTask 5.4.3）

| 评定级别 | 条件 | 处理 |
|---------|------|------|
| **resolved** | match_score ≥ 0.8，所有期望变更点已解决 | 进入用户确认闭环 |
| **partially_resolved** | 0.5 ≤ match_score < 0.8，部分期望变更点已解决 | 列出未解决点，触发二次重执行（仅针对未解决点） |
| **unresolved** | match_score < 0.5，大部分期望变更点未解决 | 触发穷尽重试，重新执行完整回滚范围，不设重试上限 |

**二次重执行规则**（partially_resolved 时）：
1. 仅针对 unaddressed_points 重新执行相关节点
2. 二次重执行后再次进行 feedback_resolution_check
3. 若仍为 partially_resolved，持续重试直至 resolved 或用户主动放弃
4. 每次重试记录到 feedback_item.processing_log

### 反馈解决率统计与框架自省（SubTask 5.4.4）

#### 解决率统计

会话结束后，统计所有 feedback_item 的解决率：

```python
def calculate_feedback_resolution_rate(feedback_items: list) -> dict:
    """计算反馈解决率（R10-06）。"""
    total = len(feedback_items)
    resolved = sum(1 for f in feedback_items if f["resolution_check"]["verdict"] == "resolved")
    partially = sum(1 for f in feedback_items if f["resolution_check"]["verdict"] == "partially_resolved")
    unresolved = sum(1 for f in feedback_items if f["resolution_check"]["verdict"] == "unresolved")

    resolution_rate = resolved / total if total > 0 else 0.0

    return {
        "total_feedbacks": total,
        "resolved": resolved,
        "partially_resolved": partially,
        "unresolved": unresolved,
        "resolution_rate": resolution_rate,  # 仅 resolved 计入分子
        "partial_rate": partially / total if total > 0 else 0.0,
        "unresolved_rate": unresolved / total if total > 0 else 0.0,
    }
```

#### <80% 触发框架自省

当反馈解决率 < 80% 时，触发框架自省流程：

```yaml
framework_self_reflection:
  trigger: "feedback_resolution_rate < 0.80"
  self_reflection_steps:
    - step_1_analyze:
        description: "分析未解决反馈的共性模式"
        actions:
          - 提取所有 partially_resolved 和 unresolved 的 feedback_item
          - 识别共性失败模式（如：某类反馈反复无法解决/某节点反复失败）
          - 生成 failure_pattern_report
    - step_2_diagnose:
        description: "诊断框架层面的根因"
        actions:
          - 检查反馈分类是否准确（是否误分类导致回滚范围错误）
          - 检查回滚范围是否完整（是否遗漏了相关节点）
          - 检查重新执行质量（Sub-Agent 输出是否达标）
          - 检查 LLM 判定是否过于严格（match_score 阈值是否需要调整）
    - step_3_improve:
        description: "生成框架改进建议"
        actions:
          - 生成 framework_improvement_report
          - 写入 docs/telemetry/feedback-self-reflection_{session_id}.json
          - 若同一失败模式连续 3 个会话出现，自动创建改进 issue
    - step_4_notify:
        description: "通知用户"
        actions:
          - 向用户展示框架自省报告
          - 说明未解决反馈的根因分析
          - 提供手动干预选项（用户可手动指定解决方案）
```

### 用户确认闭环（SubTask 5.4.5）

feedback_resolution_check 判定为 resolved 后，必须由用户确认反馈是否真正解决，形成完整闭环：

```python
def user_confirmation_loop(feedback_item: dict) -> dict:
    """用户确认闭环（R10-06）。

    Args:
        feedback_item: 已通过 resolution_check 的反馈项

    Returns:
        确认结果
    """
    # 向用户展示解决结果
    print(f"\n{'='*60}")
    print(f"反馈 {feedback_item['feedback_id']} 解决验证完成")
    print(f"{'='*60}")
    print(f"\n原始反馈：{feedback_item['feedback_content']['summary']}")
    print(f"期望变更：{feedback_item['feedback_content']['expected_change']}")
    print(f"\n解决验证结果：{feedback_item['resolution_check']['verdict']}")
    print(f"匹配度：{feedback_item['resolution_check']['match_score']:.2f}")
    print(f"\n已解决点：")
    for point in feedback_item['resolution_check']['addressed_points']:
        print(f"  ✓ {point}")
    if feedback_item['resolution_check']['unaddressed_points']:
        print(f"\n未解决点：")
        for point in feedback_item['resolution_check']['unaddressed_points']:
            print(f"  ✗ {point}")
    print(f"\nLLM 判定理由：{feedback_item['resolution_check']['llm_judge_rationale']}")

    # 等待用户确认
    while True:
        choice = input("\n反馈是否已解决？(y/n/部分): ").strip().lower()
        if choice in ("y", "yes", "是"):
            feedback_item["user_confirmation"] = {
                "confirmed": True,
                "user_feedback_on_resolution": "confirmed",
                "timestamp": get_iso_timestamp(),
            }
            feedback_item["status"] = "closed"
            return {"status": "confirmed", "feedback_item": feedback_item}
        elif choice in ("n", "no", "否"):
            user_feedback = input("请说明未解决的原因：").strip()
            feedback_item["user_confirmation"] = {
                "confirmed": False,
                "user_feedback_on_resolution": user_feedback,
                "timestamp": get_iso_timestamp(),
            }
            feedback_item["status"] = "user_rejected"
            # 用户拒绝 → 触发二次重执行
            return {"status": "rejected", "feedback_item": feedback_item, "reason": user_feedback}
        elif choice in ("部分", "partial"):
            user_feedback = input("请说明部分解决的情况：").strip()
            feedback_item["user_confirmation"] = {
                "confirmed": False,
                "user_feedback_on_resolution": f"部分解决：{user_feedback}",
                "timestamp": get_iso_timestamp(),
            }
            feedback_item["status"] = "user_partial"
            return {"status": "partial", "feedback_item": feedback_item, "reason": user_feedback}
```

**用户确认闭环规则**：
1. resolution_check 判定为 resolved → 必须由用户确认（不自动关闭）
2. 用户确认 → feedback_item.status = "closed"，反馈闭环完成
3. 用户拒绝 → 触发二次重执行（针对用户说明的未解决原因）
4. 用户部分确认 → 触发针对未解决部分的二次重执行
5. 二次重执行后再次进行 resolution_check + 用户确认
6. 持续循环直至用户确认或用户主动放弃（标注 "user_gave_up"）

## 异常处理与穷尽重试

| 异常场景 | 处理策略 |
|---------|---------|
| 用户反馈模糊无法解析 | 请求用户澄清，提供选项列表辅助明确 |
| 用户反馈与研究结论严重矛盾 | 标注"用户反馈与结论矛盾"，保留两者供后续裁决 |
| 用户反馈导致需要大规模重做 | 无论重做范围多大，持续修改直至完成 |
| 用户多次反馈相互矛盾 | 识别矛盾点，请求用户确认最终意图 |

---

## 测试用例（R10-06）

> **测试用例格式声明**：每个测试用例遵循「给定输入 X，应产出 Y」格式，覆盖反馈闭环验证的关键路径与边界条件。

### TC-1: USER_NEW_HYPOTHESIS 反馈完整闭环（resolved）

**给定输入**：
- 用户在 T13 完成后提出新假设反馈："你们没有考虑'碳关税对新能源汽车出口的间接影响'这一假设路径"
- feedback_type: `USER_NEW_HYPOTHESIS`
- target_node: `T09`
- rollback_scope: `["T09", "T10", "T11", "T12", "T13"]`
- expected_change: "在 T09 新增'碳关税间接影响'推理路径，并在 T13 综合时纳入该路径结论"
- 框架回滚 T09→T10→T11→T12→T13，重新执行后 T13 输出包含"碳关税间接影响"章节，结论已纳入新路径

**应产出**：
- feedback_resolution_check 返回 `verdict: "resolved"`，`match_score: 0.92`
- addressed_points: ["新增碳关税间接影响推理路径", "T13 综合结论已纳入新路径"]
- unaddressed_points: []
- feedback_item.status 流转：`received → processing → rerun_completed → resolution_checked → user_confirmed → closed`
- 用户确认闭环：用户输入 "y" → status = "closed"

### TC-2: USER_OUTPUT_CORRECTION 反馈（partially_resolved）

**给定输入**：
- 用户对 T20 渲染输出提出纠偏："图表配色太冷，改为暖色；同时增加数据来源标注"
- feedback_type: `USER_OUTPUT_CORRECTION`
- target_node: `T20`
- expected_change: "图表配色改为暖色系；所有图表增加数据来源标注"
- 框架仅重执行 T20，重新渲染后：图表配色已改为暖色，但仅 60% 的图表增加了数据来源标注

**应产出**：
- feedback_resolution_check 返回 `verdict: "partially_resolved"`，`match_score: 0.65`
- addressed_points: ["图表配色已改为暖色系"]
- unaddressed_points: ["40% 的图表仍缺少数据来源标注"]
- 触发二次重执行：仅针对未解决点（数据来源标注）重执行 T20
- 二次重执行后 match_score 升至 0.95 → verdict = "resolved" → 进入用户确认闭环

### TC-3: USER_STRONGER_REFUTATION 反馈（unresolved 触发穷尽重试）

**给定输入**：
- 用户对 T10 逻辑对抗结果不满意，提出新反驳："你们忽略了'供应链转移效应'这一逻辑漏洞"
- feedback_type: `USER_STRONGER_REFUTATION`
- target_node: `T10`
- expected_change: "T10 必须纳入'供应链转移效应'作为新的逻辑攻击维度"
- 框架回滚 T10→T13，重新执行后 T10 输出未包含"供应链转移效应"维度（Sub-Agent 误判为不相关）

**应产出**：
- feedback_resolution_check 返回 `verdict: "unresolved"`，`match_score: 0.25`
- addressed_points: []
- unaddressed_points: ["T10 未纳入'供应链转移效应'逻辑攻击维度"]
- 触发穷尽重试：重新执行完整回滚范围 T10→T13，不设重试上限
- 每次重试记录到 feedback_item.processing_log
- 持续重试直至 match_score ≥ 0.5（升级为 partially_resolved 或 resolved）

### TC-4: 反馈解决率 <80% 触发框架自省

**给定输入**：
- 某会话共产生 10 条 feedback_item
- 解决情况：6 条 resolved，2 条 partially_resolved，2 条 unresolved
- resolution_rate = 6/10 = 0.60（< 0.80）

**应产出**：
- calculate_feedback_resolution_rate 返回：
  ```yaml
  total_feedbacks: 10
  resolved: 6
  partially_resolved: 2
  unresolved: 2
  resolution_rate: 0.60
  partial_rate: 0.20
  unresolved_rate: 0.20
  ```
- 触发 framework_self_reflection 流程：
  - step_1_analyze：提取 4 条未完全解决的 feedback_item，识别共性失败模式（如"T10 反复忽略用户提供的逻辑维度"）
  - step_2_diagnose：诊断根因（Sub-Agent 对抗维度识别不足 / 回滚范围遗漏相关节点）
  - step_3_improve：生成 framework_improvement_report，写入 `docs/telemetry/feedback-self-reflection_{session_id}.json`
  - step_4_notify：向用户展示自省报告，提供手动干预选项

### TC-5: 用户确认闭环（用户拒绝触发二次重执行）

**给定输入**：
- 某 feedback_item 通过 feedback_resolution_check，verdict = "resolved"，match_score = 0.85
- LLM 判定所有期望变更点已解决
- 用户在确认环节输入 "n"，说明："新假设虽然纳入了，但结论方向与我的预期相反，需要重新审视"

**应产出**：
- user_confirmation_loop 返回 `{"status": "rejected", "reason": "新假设虽然纳入了，但结论方向与我的预期相反，需要重新审视"}`
- feedback_item.status = "user_rejected"
- 触发二次重执行：针对用户说明的未解决原因（结论方向问题）重新执行相关节点
- 二次重执行后再次进行 feedback_resolution_check + user_confirmation_loop
- 持续循环直至用户确认（status = "closed"）或用户主动放弃（status = "user_gave_up"）
