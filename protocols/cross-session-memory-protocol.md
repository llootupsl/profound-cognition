<!-- 作者：阿洋 -->

# 跨会话记忆协议 (Cross-Session Memory Protocol) v3.0

## 1. 协议概述

**方法论原理**：跨会话记忆协议基于"认知连续性是深度研究的基石"的认知假设：单次会话的认知产出是有限的，跨会话的记忆积累能使框架从"每次从零开始"进化为"持续学习的研究伙伴"。本协议定义三层结构化记忆、断点续传、记忆衰减、记忆审计四大机制，使 Profound Cognition 能跨会话积累用户偏好、历史结论与未解决问题。

**触发条件**：
- 会话开始时：检索用户偏好与历史相关结论
- 会话结束时：写入本次会话的结论与未解决问题
- 用户请求时：审计或删除记忆

**能力卡引用**：[knowledge/external-capabilities/Mem0.md](../knowledge/external-capabilities/Mem0.md)

## 2. 三层记忆架构

### 2.1 第一层：用户偏好层（SubTask 5.3.2）

**目的**：存储用户的长期偏好，使框架能"记住"用户，无需每次会话重复采集 Persona 与偏好。

#### 2.1.1 偏好字段定义

```yaml
user_preference:
  user_id: "string — 用户唯一标识"
  preferences:
    output_type: "research_report | wechat_article | course_material"
    persona:
      identity: "用户身份信息（姓名/职业/机构）"
      core_values: "核心价值观列表"
      personal_stories: "个人故事列表"
      communication_style: "沟通风格"
      expertise_level: "专业水平"
      interests: "兴趣领域列表"
      goals: "研究目标列表"
    citation_style: "apa | mla | chicago | gb_t_7714 | inline"
    depth_preference: "exhaust | standard | brief"
    language: "zh | en | bilingual"
    format_preferences:
      font_size: "small | medium | large"
      color_scheme: "warm | cool | neutral"
      structure: "linear | hierarchical | network"
  last_updated: "ISO8601"
  confidence: "float — 偏好置信度（0-1，基于交互次数）"
  source: "T00b_persona_collection | user_explicit | inferred"
```

#### 2.1.2 偏好写入时机

| 时机 | 触发节点 | 写入内容 | confidence |
|------|---------|---------|------------|
| T00b 人设采集完成 | T00b | 完整 Persona 7 字段 | 0.9（用户明确提供） |
| 用户在会话中修正偏好 | 任意节点 | 修正的偏好字段 | 0.95（用户明确修正） |
| 框架推断偏好 | T20 输出渲染后 | output_type/depth_preference | 0.5（推断） |

#### 2.1.3 偏好读取时机

| 时机 | 触发节点 | 读取内容 | 用途 |
|------|---------|---------|------|
| 会话开始 | T00b | 完整偏好 | 预填 Persona 字段，减少采集轮次 |
| DAG 生成 | T00 | output_type/depth_preference | 影响 DAG 裁剪与节点激活 |
| T20 渲染 | T20 | format_preferences/citation_style | 影响渲染格式 |

#### 2.1.4 偏好冲突处理

当用户在会话中明确修正的偏好与历史偏好冲突时：
1. **以用户最新明确修正为准**（confidence 0.95 覆盖历史 0.9）
2. 更新偏好层的对应字段
3. 在 execution_ledger 中记录偏好变更：`{event: "preference_updated", field: "output_type", old: "wechat_article", new: "research_report", source: "user_explicit"}`
4. **不删除历史偏好**，仅更新（保留变更历史用于审计）

### 2.2 第二层：历史结论层（SubTask 5.3.3）

**目的**：将 T13 认知综合产出的核心结论写入结构化数据库，支持语义检索，使新会话能复用历史研究结论。

#### 2.2.1 结论写入流程

```python
def write_historical_conclusion(t13_output: dict, user_id: str, research_id: str) -> str:
    """T13 完成后，将核心结论写入历史结论层。

    Args:
        t13_output: T13 认知综合的输出
        user_id: 用户 ID
        research_id: 研究会话 ID

    Returns:
        memory_id: 写入的记忆 ID
    """
    from mem0 import Memory
    memory = Memory()

    # 提取核心结论
    conclusions = t13_output["cognitive_synthesis"]["conclusions"]

    # 为每个结论生成 embedding（用于语义检索）
    for conclusion in conclusions:
        conclusion["embedding"] = generate_embedding(conclusion["content"])

    # 写入 Mem0
    memory_id = memory.add(
        data={
            "user_id": user_id,
            "research_id": research_id,
            "problem": t13_output["problem"],
            "conclusions": conclusions,
            "domain_engines_activated": t13_output.get("activated_engines", []),
            "tags": extract_tags(t13_output["problem"]),
        },
        user_id=user_id,
        memory_layer="conclusion",
        metadata={
            "research_id": research_id,
            "timestamp": get_iso_timestamp(),
            "t13_version": "v3.0",
        },
    )
    return memory_id
```

#### 2.2.2 结论检索流程

```python
def search_historical_conclusions(query: str, user_id: str, limit: int = 5) -> list:
    """语义检索历史结论。

    Args:
        query: 检索查询（通常是当前研究问题）
        user_id: 用户 ID
        limit: 返回结果数上限

    Returns:
        匹配的历史结论列表
    """
    from mem0 import Memory
    memory = Memory()

    results = memory.search(
        query=query,
        user_id=user_id,
        memory_layer="conclusion",
        limit=limit,
        semantic_search=True,  # 启用向量语义检索
    )

    # 按记忆衰减权重排序（见 §4）
    results.sort(key=lambda x: x["score"] * memory_weight(x), reverse=True)
    return results
```

#### 2.2.3 结论复用规则

| 复用场景 | 触发节点 | 复用方式 | 标注要求 |
|---------|---------|---------|---------|
| 历史结论直接引用 | T02/T03 | 将历史结论作为研究起点 | 标注 `[历史结论: research_id, memory_id]` |
| 历史结论作为对比 | T13 | 与本次结论对比，识别共识/分歧 | 标注 `[历史对比: research_id]` |
| 历史结论验证 | T17 | 用新证据验证历史结论是否仍成立 | 标注 `[历史验证: research_id, verdict]` |

> **重要声明**：历史结论复用不等于"复制粘贴"。复用时必须：
> 1. 标注来源（research_id + memory_id）
> 2. 用新证据验证历史结论是否仍成立
> 3. 若历史结论被新证据推翻，必须更新历史结论层（update 操作）

### 2.3 第三层：未解决问题层（SubTask 5.3.4）

**目的**：将 I01 迭代深化中标记为 unclosable 的缺口写入数据库，使后续会话能继续探索未闭合问题。

#### 2.3.1 缺口写入流程

```python
def write_unclosable_gaps(i01_output: dict, user_id: str, research_id: str) -> list:
    """I01 完成后，将 unclosable gaps 写入未解决问题层。

    Args:
        i01_output: I01 迭代深化的输出
        user_id: 用户 ID
        research_id: 研究会话 ID

    Returns:
        写入的 memory_id 列表
    """
    from mem0 import Memory
    memory = Memory()

    unclosable_gaps = i01_output.get("unclosable_gaps", [])
    memory_ids = []

    for gap in unclosable_gaps:
        memory_id = memory.add(
            data={
                "user_id": user_id,
                "research_id": research_id,
                "problem": i01_output["problem"],
                "gap_id": gap["gap_id"],
                "description": gap["description"],
                "gap_type": gap["gap_type"],  # data_gap | method_gap | theory_gap | evidence_gap
                "attempted_approaches": gap.get("attempted_approaches", []),
                "why_unclosable": gap["why_unclosable"],
                "priority": gap["priority"],  # P0 | P1 | P2
                "embedding": generate_embedding(gap["description"]),
            },
            user_id=user_id,
            memory_layer="unsolved",
            metadata={
                "research_id": research_id,
                "timestamp": get_iso_timestamp(),
                "gap_type": gap["gap_type"],
                "priority": gap["priority"],
            },
        )
        memory_ids.append(memory_id)

    return memory_ids
```

#### 2.3.2 缺口检索与续研

新会话开始时，若研究问题与历史未解决问题语义相似，框架应主动提示用户：

```python
def check_related_unsolved_problems(query: str, user_id: str) -> list:
    """检查当前研究问题是否与历史未解决问题相关。

    Args:
        query: 当前研究问题
        user_id: 用户 ID

    Returns:
        相关的未解决问题列表
    """
    from mem0 import Memory
    memory = Memory()

    results = memory.search(
        query=query,
        user_id=user_id,
        memory_layer="unsolved",
        limit=3,
        semantic_search=True,
    )

    # 仅返回语义相似度 > 0.7 的结果
    return [r for r in results if r["score"] > 0.7]
```

**续研提示模板**：
```
检测到您在历史会话（{research_id}）中有 {N} 个未解决的问题与当前研究相关：

1. [{gap_type}] {description}
   - 已尝试方法：{attempted_approaches}
   - 无法闭合原因：{why_unclosable}
   - 优先级：{priority}

是否要在本次会话中继续探索这些问题？
- 是 → 将未解决问题注入 I01，作为新一轮迭代的起点
- 否 → 仅记录，不注入
```

## 3. 断点续传（跨会话检查点）（SubTask 5.3.5）

**目的**：将 checkpoint-protocol.md 的检查点机制扩展为跨会话检查点，使用户能在新会话中恢复历史会话的执行状态。

### 3.1 跨会话检查点格式

```yaml
cross_session_checkpoint:
  checkpoint_id: "string — 跨会话检查点唯一标识"
  user_id: "string — 用户 ID"
  original_session_id: "string — 原始会话 ID"
  new_session_id: "string — 新会话 ID"
  created_at: "ISO8601"

  # 恢复点信息
  recovery_point:
    phase_id: "integer — 原始会话中断时的 Phase"
    node_completion_status: {node_id: "completed | retrying | pending"}
    last_completed_node: "string — 最后完成的节点 ID"
    next_node: "string — 下一个待执行的节点 ID"

  # 恢复内容
  restorable_content:
    context_package: "dict — 原始会话的 context_package 快照"
    node_outputs: "dict — 已完成节点的输出"
    execution_ledger: "list — 执行账本"
    nrsf_position: "string — NRSF 写入位置"

  # 跨会话记忆引用
  memory_references:
    preference_memory_id: "string — 用户偏好记忆 ID"
    conclusion_memory_ids: ["string — 历史结论记忆 ID 列表"]
    unsolved_memory_ids: ["string — 未解决问题记忆 ID 列表"]

  # 衰减状态
  decay_status:
    checkpoint_age_days: "integer — 检查点创建后的天数"
    decay_weight: "float — 衰减权重（0-1）"
    restorable: "boolean — 是否可恢复（衰减权重 > 0.3 时可恢复）"
```

### 3.2 跨会话恢复流程

```python
def resume_cross_session(user_id: str, original_session_id: str) -> dict:
    """跨会话恢复执行状态。

    Args:
        user_id: 用户 ID
        original_session_id: 原始会话 ID

    Returns:
        恢复后的 ResearchState
    """
    # 1. 从 Mem0 检索跨会话检查点
    checkpoint = mem0.search(
        query=f"checkpoint:{original_session_id}",
        user_id=user_id,
        memory_layer="checkpoint",
        limit=1,
    )

    if not checkpoint or not checkpoint[0]["decay_status"]["restorable"]:
        return {"status": "not_restorable", "reason": "checkpoint_decayed_or_not_found"}

    # 2. 恢复执行状态
    cp = checkpoint[0]
    restored_state = {
        "context_package": cp["restorable_content"]["context_package"],
        "node_outputs": cp["restorable_content"]["node_outputs"],
        "execution_ledger": cp["restorable_content"]["execution_ledger"],
        "current_phase": cp["recovery_point"]["phase_id"],
    }

    # 3. 标记已完成节点为 CACHED
    for node_id, status in cp["recovery_point"]["node_completion_status"].items():
        if status == "completed":
            restored_state["node_outputs"][node_id]["_cached"] = True

    # 4. 注入跨会话记忆
    restored_state["context_package"]["memory_references"] = cp["memory_references"]

    # 5. 生成新会话 ID
    new_session_id = generate_uuid()
    restored_state["session_id"] = new_session_id

    return {
        "status": "restored",
        "new_session_id": new_session_id,
        "restored_state": restored_state,
        "next_node": cp["recovery_point"]["next_node"],
    }
```

### 3.3 跨会话检查点写入时机

| 时机 | 触发条件 | 写入内容 |
|------|---------|---------|
| 用户主动中止会话 | 用户发送"中止"信号 | 当前完整执行状态 |
| 会话超时 | 会话超过 24 小时未活动 | 当前完整执行状态 |
| Phase 完成后 | 每个 Phase 完成后 | Phase 级检查点（增量） |
| 用户请求保存 | 用户发送"保存进度" | 当前完整执行状态 |

## 4. 记忆衰减（SubTask 5.3.6）

**目的**：避免记忆数据库无限膨胀，对历史结论层与未解决问题层实施艾宾浩斯遗忘曲线衰减。

### 4.1 衰减规则

| 记忆层 | 是否衰减 | 衰减策略 | 理由 |
|--------|---------|---------|------|
| 用户偏好层 | **不衰减** | 永久保留 | 偏好是长期稳定的，不应遗忘 |
| 历史结论层 | **衰减** | 艾宾浩斯遗忘曲线 | 旧结论可能过时，应降权 |
| 未解决问题层 | **衰减**（较慢） | 衰减速度 ×0.5 | 未解决问题仍值得探索，衰减更慢 |
| 跨会话检查点 | **衰减** | 艾宾浩斯遗忘曲线 | 旧检查点可能已过时 |

### 4.2 衰减权重计算

```python
import math

def memory_weight(age_in_days: int, access_count: int, memory_layer: str) -> float:
    """记忆权重计算（艾宾浩斯遗忘曲线变体）。

    Args:
        age_in_days: 记忆创建后的天数
        access_count: 被检索访问的次数
        memory_layer: 记忆层

    Returns:
        权重 (0-1)
    """
    if memory_layer == "preference":
        return 1.0  # 偏好层不衰减

    # 基础遗忘曲线：R = exp(-t/S)
    base_S = 30  # 默认记忆强度 30 天
    if memory_layer == "unsolved":
        base_S = 60  # 未解决问题衰减更慢（60 天）
    elif memory_layer == "checkpoint":
        base_S = 15  # 检查点衰减更快（15 天）

    # 每次访问增强记忆强度
    S = base_S * (1 + math.log(1 + access_count))
    retention = math.exp(-age_in_days / S)
    return retention
```

### 4.3 衰减处理动作

| 权重范围 | 处理动作 | 说明 |
|---------|---------|------|
| > 0.3 | 正常保留 | 检索时正常返回 |
| 0.1 - 0.3 | 标记"弱记忆" | 检索时降权（score × 0.5） |
| < 0.1 | 进入"待遗忘"队列 | 30 天后自动删除（除非被访问） |
| 被访问 | 重置衰减 | access_count + 1，权重回升 |

### 4.4 衰减触发时机

- 每日凌晨 02:00 自动触发衰减扫描（cron job）
- 新记忆写入前，触发一次衰减扫描
- 用户请求记忆审计时，实时计算衰减权重

## 5. 记忆审计（SubTask 5.3.7）

**目的**：保障用户对自身记忆的知情权、控制权与被遗忘权。

### 5.1 审计操作

| 操作 | 命令 | 说明 |
|------|------|------|
| 查看全部记忆 | `audit list` | 列出用户的所有记忆（三层） |
| 查看指定层记忆 | `audit list --layer preference` | 列出指定层的记忆 |
| 删除指定记忆 | `audit delete --memory-id {id}` | 删除指定记忆 |
| 删除指定层全部记忆 | `audit delete --layer conclusion` | 删除指定层的全部记忆 |
| 删除全部记忆 | `audit delete --all` | 删除用户的所有记忆（被遗忘权） |
| 导出全部记忆 | `audit export` | 导出为 JSON 文件（数据可携带权） |

### 5.2 审计报告格式

```yaml
memory_audit_report:
  user_id: "string"
  generated_at: "ISO8601"
  summary:
    preference_count: integer
    conclusion_count: integer
    unsolved_count: integer
    checkpoint_count: integer
    total_memories: integer
    total_storage_kb: float
  oldest_memory: "ISO8601"
  newest_memory: "ISO8601"
  decay_status:
    healthy_memories: integer  # 权重 > 0.3
    weak_memories: integer     # 权重 0.1-0.3
    pending_forget: integer    # 权重 < 0.1
  memories:
    preference: [...]
    conclusion: [...]
    unsolved: [...]
    checkpoint: [...]
```

### 5.3 被遗忘权保障

用户行使被遗忘权（删除全部记忆）时：
1. 框架必须立即删除用户的所有记忆（三层 + 检查点）
2. 删除完成后返回确认：`{status: "all_deleted", user_id: "...", deleted_count: N}`
3. 删除操作不可撤销，框架应在删除前向用户确认
4. 删除操作记录到系统审计日志（仅记录"用户行使被遗忘权"，不记录删除的内容）

## 6. 异常处理与穷尽重试

| 异常场景 | 处理策略 |
|---------|---------|
| Mem0 服务不可用 | 回退到纯文件模式（NRSF-Summary Markdown + JSON 索引），持续重试 Mem0 直至可用 |
| 向量数据库不可用 | 语义检索回退到关键词检索，持续重试向量数据库 |
| 记忆写入失败 | 持续重试写入直至成功，不设重试上限 |
| 记忆检索超时 | 持续重试检索，不跳过记忆读取（记忆是会话质量的重要输入） |
| 跨会话检查点损坏 | 从上一个有效检查点恢复；若无有效检查点，从头开始执行 |
| 记忆衰减扫描失败 | 持续重试扫描，不影响正常会话执行（衰减是后台任务） |

## 7. 交叉引用

- [Mem0.md](../knowledge/external-capabilities/Mem0.md) — Mem0 跨会话记忆系统能力卡
- [TC-005-Mem0.md](../knowledge/external-capabilities/TC-005-Mem0.md) — Mem0 基础工具卡（**已弃用**，迁移至 [Mem0.md](../knowledge/external-capabilities/Mem0.md) v6.0 增强版；见 W4-F5）
- [checkpoint-protocol.md §10](./checkpoint-protocol.md) — 跨会话检查点扩展
- [context-budget-protocol.md](./context-budget-protocol.md) — 上下文预算管理（与记忆加载协同）
- [execution-protocol.md](./execution-protocol.md) — 执行协议（T00b/T13/I01 节点消费记忆）

## 附录

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| v3.0 | 2026-06-25 | 初始发布：三层记忆架构、断点续传、记忆衰减、记忆审计 |

---

## 测试用例 (D3.4.4)

### 测试用例 1：用户偏好层写入与读取

**给定输入**：T00b 人设采集完成，用户明确指定 output_type=research_report、depth_preference=exhaust、citation_style=gb_t_7714，confidence=0.9。

**应产出**：用户偏好层写入完整偏好字段（output_type/persona/citation_style/depth_preference），confidence=0.9，source=T00b_persona_collection。下次会话开始时 T00b 读取该偏好，预填 Persona 字段，减少采集轮次。

### 测试用例 2：偏好冲突处理

**给定输入**：历史偏好 output_type=wechat_article（confidence=0.9），用户在本次会话中明确修正为 output_type=research_report。

**应产出**：以用户最新修正为准（confidence=0.95 覆盖历史 0.9），更新偏好层对应字段，execution_ledger 记录 `{event: "preference_updated", field: "output_type", old: "wechat_article", new: "research_report", source: "user_explicit"}`，不删除历史偏好（保留变更历史）。

### 测试用例 3：历史结论语义检索与复用

**给定输入**：用户发起新研究会话，研究问题为"AI 对就业市场的影响"。历史结论层存在一条记忆：research_id=R001，问题="人工智能技术对劳动力市场的冲击"，语义相似度=0.85。

**应产出**：search_historical_conclusions 返回该历史结论（score=0.85 > 0.7 阈值），T02 将其作为研究起点，标注 `[历史结论: R001, memory_id]`。复用时用新证据验证历史结论是否仍成立。

### 测试用例 4：未解决问题续研提示

**给定输入**：用户发起新研究会话，研究问题为"碳中和对能源转型的影响"。历史未解决问题层存在 2 条语义相似度 > 0.7 的 unclosable gaps（gap_type=data_gap，priority=P0）。

**应产出**：check_related_unsolved_problems 返回 2 条相关未解决问题，向用户展示续研提示模板，询问"是否要在本次会话中继续探索这些问题"。用户选择"是"则注入 I01 作为新一轮迭代起点。

### 测试用例 5：跨会话检查点恢复

**给定输入**：用户请求恢复历史会话 S001 的执行状态，存在跨会话检查点（checkpoint_age_days=10，decay_weight=0.52，restorable=true）。

**应产出**：resume_cross_session 返回 status=restored，恢复 context_package/node_outputs/execution_ledger，已完成节点标记为 _cached=true，生成新会话 ID，next_node 指向待执行节点。衰减权重 0.52 > 0.3 阈值，正常可恢复。

### 测试用例 6：记忆衰减与遗忘

**给定输入**：历史结论层某条记忆 age_in_days=45，access_count=2，memory_layer=conclusion。

**应产出**：memory_weight 计算 S=30×(1+log(3))≈30×2.099=62.97，retention=exp(-45/62.97)≈exp(-0.715)≈0.489。权重 0.489 > 0.3，正常保留，检索时正常返回。若该记忆 30 天内未被访问，权重降至 0.1-0.3 区间，标记"弱记忆"并降权（score × 0.5）。

### 测试用例 7：被遗忘权行使

**给定输入**：用户发送 `audit delete --all` 命令，行使被遗忘权。

**应产出**：框架立即删除用户的所有记忆（偏好层 + 结论层 + 未解决问题层 + 检查点层），返回 `{status: "all_deleted", user_id: "...", deleted_count: N}`，删除操作不可撤销，删除前向用户确认，系统审计日志仅记录"用户行使被遗忘权"不记录删除内容。
