<!-- 作者：阿洋 -->

# 上下文预算监控协议 (Context Budget Monitoring Protocol) v3.0

> **协议版本**: v3.0
> **状态**: 正式发布 (v3.0)
> **适用范围**: Profound Cognition 全流水线上下文使用监控
> **最后更新**: 2026-06-26

> **职责边界声明（D3.4.2）**：本协议的角色为**监控上下文使用量并主动触发恢复动作**，而非限制上下文。原 v3.0 版本的硬上限（Token 硬上限、最大递归轮次等）已通过 v3.1 修订全部移除，与 EXHAUST 模式四大铁律（Token 不设上限 / 时间不设限制 / 质量唯一优先 / 永远穷尽无档位无上限）保持一致。本协议不截断、不丢弃任何分析维度，仅通过 LLMLingua 压缩 + write-while-research 落盘释放上下文窗口，质量驱动终止。详见 §递归感知截断策略 (v3.1 — EXHAUST 一致性修订)。

## 1. 概述

**方法论原理**：上下文预算协议基于"认知资源有限性"的认知假设：LLM的上下文窗口是有限资源，需要在信息完整性和资源效率之间取得平衡。通过上下文使用监控（D3.4.2：监控而非限制），在保留全部信息完整性的前提下，主动触发 LLMLingua 压缩与 write-while-research 落盘释放上下文窗口，确保关键信息可恢复且不丢失。

本协议定义 Profound Cognition v6.0.0 框架的上下文使用监控协议（D3.4.2：监控角色，非限制角色）。目标是在流水线执行过程中主动监控上下文使用量并触发恢复动作（LLMLingua 压缩、write-while-research 落盘释放），而非通过硬上限截断输出——与 EXHAUST 模式"Token 不设上限"原则一致。

## 2. 监控机制

### 2.1 监控频率
- 每完成 5 个节点估算一次上下文使用量
- 在每道 Gate 之前强制估算（T07/T14/T16 执行前）
- 在 NRSF 加载前强制估算（I01 和 T20 全量加载前）

### 2.2 估算方法
- 统计已执行节点的 Context Package 累计长度
- 预估剩余节点的平均输出长度
- 计算当前使用量占预算的百分比
- 估算 NRSF-Full 的 token 占用（1 token ≈ 0.75 中文字）

### 2.3 tiktoken 精确 token 计数（R10-01）

**方法论原理**：自 R10-01 起，上下文预算从「字符数估算」升级为「tiktoken 精确 token 计数」。tiktoken 是 OpenAI 开源的 BPE 分词器，与 GPT/Claude 等主流 LLM 的分词规则高度一致，能精确计算上下文实际占用的 token 数，避免字符估算的偏差（中文 1 字 ≈ 1.3 token，英文 1 词 ≈ 1.3 token，代码与符号差异更大）。

#### 2.3.1 tiktoken 集成方式

```python
import tiktoken

# 默认使用 cl100k_base 编码（GPT-4/Claude 通用）
def count_tokens(text: str, encoding_name: str = "cl100k_base") -> int:
    """使用 tiktoken 精确计算文本的 token 数。

    Args:
        text: 待计数的文本
        encoding_name: 分词器编码名称（默认 cl100k_base）

    Returns:
        token 数量
    """
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(text))


def count_context_tokens(context_package: dict, node_outputs: dict) -> dict:
    """计算当前活跃上下文的精确 token 数。

    核算范围：
    - context_package 中的所有字段（problem/output_type/upstream_outputs）
    - node_outputs 中尚未落盘的所有节点输出
    - execution_ledger 的累计条目

    Args:
        context_package: 当前上下文包
        node_outputs: 所有节点的输出

    Returns:
        token 计数明细
    """
    breakdown = {
        "context_package_tokens": count_tokens(str(context_package)),
        "node_outputs_tokens": 0,
        "execution_ledger_tokens": 0,
        "total_tokens": 0,
    }
    for node_id, output in node_outputs.items():
        breakdown["node_outputs_tokens"] += count_tokens(str(output))
    breakdown["execution_ledger_tokens"] = count_tokens(str(context_package.get("execution_ledger", [])))
    breakdown["total_tokens"] = (
        breakdown["context_package_tokens"]
        + breakdown["node_outputs_tokens"]
        + breakdown["execution_ledger_tokens"]
    )
    return breakdown
```

#### 2.3.2 编码选择策略

| 模型系列 | 推荐编码 | 说明 |
|---------|---------|------|
| GPT-4 / GPT-3.5 | cl100k_base | OpenAI 官方推荐 |
| Claude | cl100k_base | 与 Claude 分词高度一致（偏差 <2%） |
| Gemini | cl100k_base | 近似估算（偏差 <5%） |
| 国产模型（GLM/Qwen） | cl100k_base | 近似估算（偏差 <8%，中文略偏高） |

> **回退策略**：若 tiktoken 不可用（ImportError），回退到字符估算（中文 1 字 ≈ 1.3 token，英文 1 词 ≈ 1.3 token），并在 execution_ledger 中标注 `token_count_method: "char_estimate"`。

#### 2.3.3 计数时机（R10-01 强化）

- 每完成 1 个节点后立即计数（替代原"每 5 个节点估算一次"）
- 在每道 Gate 之前强制计数（T07/T14/T16 执行前）
- 在 NRSF 加载前强制计数（I01 和 T20 全量加载前）
- 在 LLMLingua 压缩前后各计数一次（验证压缩效果）
- 在 Checkpoint 落盘前后各计数一次（验证释放效果）

#### 2.3.4 与原字符估算的关系

- 原 §2.2 的字符估算方法保留为回退路径（tiktoken 不可用时使用）
- tiktoken 计数结果与字符估算可能存在 10-20% 偏差，以 tiktoken 为准
- 历史执行记录中的字符估算数据不回溯重算，仅对新会话采用 tiktoken
- 预算百分比计算公式：`budget_percent = (active_context_tokens / context_window_limit) × 100`

## 3. 预算阈值与响应策略

### 3.1 阈值定义

> **R10-01 阈值收紧声明**：自 R10-01 起，阈值从原 GREEN<80%/YELLOW 80-120%/RED 120-150%/强制落盘>150% 收紧为 GREEN<60%/YELLOW 60-80%/RED 80-95%/强制落盘>95%。收紧原因：tiktoken 精确计数替代字符估算后，计数偏差从 ±20% 降至 ±2%，原阈值留有的"估算安全垫"不再需要。新阈值更早触发缓解动作，避免临近溢出时才被动应对。

| 阈值级别 | 百分比 | 说明 |
|---------|--------|------|
| GREEN | < 60% | 正常输出，无需干预 |
| YELLOW | 60%-80% | **LLMLingua 压缩**（R10-01）：使用 LLMLingua 对 `process_description` 与 `methodology_notes` 进行重要性感知压缩（压缩率 30-50%），压缩后内容仍留在活跃上下文。若压缩后仍未回落到 GREEN，则将压缩后的 `process_description` 与 `methodology_notes` 写入 Checkpoint 文件后从上下文释放，保留 core_conclusions/key_findings/supporting_evidence/intermediate_results 完整。落盘后仍可被下游节点通过 Checkpoint 读取，不构成信息丢失 |
| RED | 80%-95% | **主动落盘到 Checkpoint**（R10-01）：将当前上下文完整写入 Checkpoint 文件后释放全部活跃上下文，不删除任何分析维度。下游节点从 Checkpoint 按需加载。RED 级别是"主动缓解"的最后窗口，必须在达到强制落盘阈值前完成落盘 |
| 强制落盘 | > 95% | 强制批量写入（force batch write）+ 继续生成，不丢弃任何分析维度、不跳过任何节点、不终止研究 |

### 3.2 压缩策略细节

YELLOW 级别（60%-80%）LLMLingua 压缩 + 落盘后释放规则（R10-01 + R2-03）：

**阶段一：LLMLingua 重要性感知压缩（R10-01 新增）**

当预算进入 YELLOW（60%-80%）时，首先使用 LLMLingua 对 `process_description` 与 `methodology_notes` 进行重要性感知压缩，不落盘，仅压缩：

```python
def yellow_llmlingua_compress(node_outputs: dict) -> dict:
    """YELLOW 级别 LLMLingua 压缩（R10-01）。

    对所有节点的 process_description 与 methodology_notes 执行 LLMLingua 压缩，
    压缩率目标 30-50%，压缩后内容仍留在活跃上下文。
    """
    from llmlingua import PromptCompressor

    compressor = PromptCompressor(model_name="bge-large-zh-v1.5")
    for node_id, output in node_outputs.items():
        if "process_description" in output:
            original = output["process_description"]
            compressed = compressor.compress_prompt(
                original,
                rate=0.5,  # 目标压缩率 50%
                force_replace=False,
            )
            output["process_description"] = compressed["compressed_prompt"]
            output["_compression_meta"] = {
                "original_tokens": count_tokens(original),
                "compressed_tokens": count_tokens(compressed["compressed_prompt"]),
                "compression_ratio": compressed["rate"],
                "method": "llmlingua",
            }
        if "methodology_notes" in output:
            original = output["methodology_notes"]
            compressed = compressor.compress_prompt(original, rate=0.5)
            output["methodology_notes"] = compressed["compressed_prompt"]
    return node_outputs
```

**阶段二：压缩后仍未回落到 GREEN → 落盘后释放（R2-03 保留）**

若 LLMLingua 压缩后预算仍未回落到 GREEN（<60%），则将压缩后的 `process_description` 与 `methodology_notes` 写入 Checkpoint 文件后从上下文释放：
- core_conclusions: 保留完整（留在活跃上下文）
- key_findings: 保留完整（留在活跃上下文）
- supporting_evidence: 保留完整（留在活跃上下文）
- intermediate_results: 保留完整（留在活跃上下文）
- process_description: **LLMLingua 压缩后写入 Checkpoint 文件，再从上下文释放**（不删除，落盘后仍可被下游节点通过 Checkpoint 读取）
- methodology_notes: **LLMLingua 压缩后写入 Checkpoint 文件，再从上下文释放**（不删除，落盘后仍可被下游节点通过 Checkpoint 读取）

> **R2-03 关键声明**：methodology_notes 和 process_description 落盘后仍可被下游节点通过 Checkpoint 读取，不构成信息丢失。这与旧版的「删除」有本质区别——旧版删除后信息永久丢失，新版落盘后信息持久化存储，仅从活跃上下文中释放以腾出预算空间，下游节点可通过引用指针（文件路径+章节索引）按需加载。

RED 级别（80%-95%）主动落盘到 Checkpoint 规则（R10-01）：

RED 级别是"主动缓解"的最后窗口，必须在达到强制落盘阈值（>95%）前完成落盘。RED 触发时：
1. **跳过 LLMLingua 压缩**（RED 级别时间紧迫，直接落盘）
2. 触发批量写入（write-while-research）：将当前所有活跃上下文（含所有分析维度）完整写入 Checkpoint 文件
- core_conclusions: 保留完整（写入 Checkpoint 文件后从上下文释放）
- key_findings: 保留完整（写入 Checkpoint 文件后从上下文释放）
- supporting_evidence: 保留完整（写入 Checkpoint 文件后从上下文释放）
- process_description: 保留完整（写入 Checkpoint 文件后从上下文释放）
- methodology_notes: 保留完整（写入 Checkpoint 文件后从上下文释放）
3. 写入完成后，上下文预算重置为仅包含必要的引用指针和当前执行状态
4. 下游节点通过引用指针从 Checkpoint 按需加载所需内容
5. **RED 落盘必须在预算达到 95% 前完成**，否则升级为强制落盘

强制落盘（> 95%）：
- 强制批量写入（force batch write）：将当前所有活跃上下文完整写入 Checkpoint 文件
- 写入完成后，上下文预算重置为仅包含引用指针和当前执行状态
- 继续生成：不丢弃任何分析维度，不跳过任何未执行节点，不终止研究
- T19 交付守卫必须标注批量写入影响范围（写入的文件路径和释放的上下文量）
- T20 渲染时附加声明："本报告因上下文预算压力（超过95%），已通过批量写入机制完整保留所有分析维度，无任何维度被丢弃或简化"

### 3.3 检查时机

在 Phase 1 执行循环中，每完成 1 个节点后检查上下文预算时（R10-01 强化，原为每 5 个节点），Orchestrator SHALL：
1. 使用 §2.3 中定义的 tiktoken 精确计数计算活跃上下文 token 数
2. 使用 §3.1 中定义的阈值进行 GREEN/YELLOW/RED/强制落盘 判定
3. 若判定为 YELLOW → 使用 §3.2 阶段一中的 LLMLingua 压缩规则（压缩 process_description 与 methodology_notes），压缩后仍未回落到 GREEN 则执行阶段二落盘后释放
4. 若判定为 RED → 触发批量写入（write-while-research），将当前上下文完整写入 Checkpoint 文件后释放全部活跃上下文（主动落盘，不等达到强制落盘阈值）
5. 若判定为强制落盘 → 强制批量写入，继续生成

### 3.4 预算核算规则（活跃上下文）

上下文预算仅核算"活跃上下文"（active context），即尚未通过 write-to-file 写入文件的章节内容。已写入 Checkpoint 文件的章节不计入上下文预算。

核算规则：
- 活跃上下文 = 当前会话中所有节点输出 - 已写入 Checkpoint 文件的内容
- 当内容通过批量写入（write-while-research / force batch write）写入文件后，该部分内容从上下文预算中释放
- 写入文件后，上下文仅保留必要的引用指针（如文件路径、章节索引）和当前执行状态
- 此规则确保上下文预算反映的是实际内存占用，而非累计输出量
- **R10-01 强化**：活跃上下文 token 数由 tiktoken 精确计算（§2.3），不再使用字符估算

### 3.5 token 计数日志写入 execution_ledger（R10-01）

**方法论原理**：每次 token 计数结果必须写入 execution_ledger，形成可审计的预算使用轨迹。这使事后能复盘预算压力点、优化阈值配置、验证 LLMLingua 压缩效果。

#### 3.5.1 日志条目格式

每次 token 计数（§2.3.3 定义的计数时机）后，向 execution_ledger 追加一条 token 计数日志：

```yaml
token_count_log:
  log_type: "token_count"
  timestamp: "ISO8601时间戳"
  trigger: "node_completed | pre_gate | pre_nrsf_load | post_llmlingua | post_checkpoint_flush"
  trigger_node: "触发计数的节点ID（如 T05）"
  token_count_method: "tiktoken | char_estimate"
  encoding: "cl100k_base"
  breakdown:
    context_package_tokens: integer
    node_outputs_tokens: integer
    execution_ledger_tokens: integer
    total_active_tokens: integer
  context_window_limit: integer
  budget_percent: float
  threshold_level: "GREEN | YELLOW | RED | FORCE_FLUSH"
  action_taken: "none | llmlingua_compress | checkpoint_flush | force_flush"
  released_tokens: integer  # 落盘/压缩后释放的 token 数（action_taken != none 时填写）
  post_action_budget_percent: float  # 采取行动后的预算百分比（action_taken != none 时填写）
```

#### 3.5.2 日志写入时机

| 触发事件 | trigger 字段 | 必填 |
|---------|-------------|------|
| 节点执行完成 | `node_completed` | 是 |
| Gate 检查前 | `pre_gate` | 是 |
| NRSF 加载前 | `pre_nrsf_load` | 是 |
| LLMLingua 压缩后 | `post_llmlingua` | 是（仅 YELLOW 触发压缩时） |
| Checkpoint 落盘后 | `post_checkpoint_flush` | 是（仅 RED/强制落盘时） |

#### 3.5.3 日志聚合与报告

会话结束后，从 execution_ledger 中提取所有 `log_type == "token_count"` 的条目，生成 token 计数聚合报告：

```yaml
token_count_summary:
  session_id: "会话ID"
  total_count_events: integer
  method_distribution:
    tiktoken: integer  # 使用 tiktoken 计数的次数
    char_estimate: integer  # 回退到字符估算的次数
  threshold_distribution:
    GREEN: integer  # 处于 GREEN 级别的计数次数
    YELLOW: integer
    RED: integer
    FORCE_FLUSH: integer
  peak_budget_percent: float  # 峰值预算百分比
  peak_trigger_node: "峰值出现时的节点ID"
  total_released_tokens: integer  # 累计释放的 token 数
  llmlingua_compression_stats:
    total_compressions: integer
    avg_compression_ratio: float
    avg_tokens_saved: float
  checkpoint_flush_stats:
    total_flushes: integer
    avg_flush_tokens: float
```

此聚合报告写入 `docs/telemetry/token-count-report_{session_id}.json`（与执行遥测协议 §5.2 协同）。

---

## 4. 强制落盘联动（EXHAUST 一致性）

当上下文预算超过强制落盘阈值（> 95%）时：
1. 强制批量写入（force batch write）：将当前所有活跃上下文完整写入 Checkpoint 文件
2. 写入完成后，上下文预算重置为仅包含引用指针和当前执行状态
3. 继续生成：不丢弃任何分析维度，不跳过任何未执行节点，**不终止研究**——EXHAUST 模式下研究仅由质量驱动条件终止，不由上下文预算终止
4. T19 交付守卫必须标注批量写入影响范围（写入的文件路径和释放的上下文量）
5. T20 渲染时附加声明："本报告因上下文预算压力（超过95%），已通过批量写入机制完整保留所有分析维度，无任何维度被丢弃或简化"

## 5. 恢复机制

如果落盘释放后上下文使用量回落到 GREEN 级别：
- 后续节点恢复正常输出长度
- 已落盘释放的节点输出不重新加载到活跃上下文（避免重复占用预算），下游节点通过 Checkpoint 引用指针按需读取
- 落盘后的 methodology_notes 和 process_description 可被任何下游节点通过 Checkpoint 文件路径+章节索引读取，不构成信息丢失

## 6. 重要性感知压缩策略 (LLMLingua-style)

### 6.1 重要性评分维度

```yaml
importance_scoring:
  fact_density:
    weight: 0.35
    description: "事实密度（facts/token），每百字包含的可验证事实数"
  novelty:
    weight: 0.25
    description: "新颖度（是否产出超越基础事实的洞察）"
  core_relevance:
    weight: 0.30
    description: "与用户原始问题的直接相关程度"
  cross_reference_count:
    weight: 0.10
    description: "被其他节点引用的次数"
```

### 6.2 压缩执行流程

```yaml
compression_workflow:
  step_1: "当上下文预算超限时，Orchestrator 计算所有节点输出的重要性评分"
  step_2: "按评分降序排列，从最低分开始逐节点压缩"
  step_3: "将被压缩节点的完整输出替换为 summary（遵守 rule_6_minimum_fields）"
  step_4: "重复 step_2-3 直到上下文预算恢复至 soft_cap_percent 以内"
  step_5: "记录压缩日志：{node_id}: full → summary, importance_score={score}"
```

### 6.3 压缩阈值

```yaml
compression_thresholds:
  below_03: "评分 < 0.3 的节点可压缩至 50 字以内（仅保留 core_conclusion）"
  mid_range: "评分 0.3-0.7 的节点压缩至 summary 长度上限（2000字）"
  above_07: "评分 ≥ 0.7 的节点保持完整 summary 长度（2000字），不可压缩"
```

### 6.4 禁止压缩

```yaml
no_compress_zones:
  - "T13 核心结论（cognitive_synthesis.conclusions）"
  - "T09 中标记为 HIGH 的新发现"
  - "T15 中 activation_confidence ≥ 0.8 的引擎输出"
  - "context_package 中的原始问题"
```

## 7. NRSF 上下文管理

### 7.1 NRSF 加载策略选择

NRSF 加载时，根据上下文窗口大小选择加载策略（详见 nrsf-protocol.md NRSF 分层摘要机制章节）：

| 情况 | 条件 | 策略 |
|------|------|------|
| 情况 1 | NRSF-Full ≤ 50% 窗口 | 全量加载 |
| 情况 2 | NRSF-Full 在 50%-95% 窗口 | 分块加载 |
| 情况 3 | NRSF-Full > 95% 窗口 | Summary 代理 + LLMLingua 压缩 |
| 情况 4 | Summary > 窗口 | **不终止研究**——强制 write-while-research 落盘 + 分段加载 + 增量渲染，研究继续进行直至质量驱动终止 |

### 7.2 NRSF-Summary 作为轻量替代

当上下文预算紧张时：
- 优先加载 NRSF-Summary（≤ 8000 字）替代 NRSF-Full
- NRSF-Summary 包含核心论点、关键发现、未闭合论证链
- 大部分任务（T02-T06, T08-T13, T15-T19）仅需 NRSF-Summary 即可执行

### 7.3 LLMLingua 压缩集成

当 NRSF-Full 超过上下文窗口 95% 时：
- 使用 LLMLingua 对 NRSF-Full 进行重要性感知压缩
- 压缩策略与本协议 §6 的重要性评分维度一致
- 压缩后保留核心论点和关键引用，删除过程性描述

### 7.4 与 Checkpoint 协议的联动

- Checkpoint 写入前检查上下文预算
- 写入 NRSF § 节时，如果上下文预算超过 RED 阈值，触发压缩
- 压缩后继续执行，不中断研究流程

## 递归感知截断策略 (v3.1 — EXHAUST 一致性修订)

> **EXHAUST 一致性声明**：本节原 v3.0 版本含有"最大递归轮次: 10"、"Token 硬上限: 1,200,000 tok"、"节点级递归限制"等硬上限，与 EXHAUST 模式四大铁律（Token 不设上限 / 时间不设限制 / 质量唯一优先 / 永远穷尽无档位无上限）严重冲突。v3.1 已全部移除硬上限，改为质量驱动终止 + write-while-research 落盘释放上下文。

### 递归场景 Token 预算（参考性，非硬上限）

| 递归深度 | 单轮参考预算 | 累计参考预算 | 截断策略 |
|----------|----------|----------|----------|
| 0 (无递归) | 150,000 | 150,000 | 标准截断 |
| 1 (1轮递归) | 120,000 | 270,000 | 保留核心+摘要 |
| 2 (2轮递归) | 100,000 | 370,000 | 仅保留核心 |
| 3 (3轮递归) | 80,000 | 450,000 | 核心压缩+引用 |
| ≥4 (深度递归) | 60,000 | 510,000+ | 极限压缩 |

> 上表为**参考性预算估算**，用于触发 write-while-research 落盘决策，**不作为强制终止条件**。任何深度均可通过批量写入释放上下文后继续递归。

### 递归截断优先级

1. **必须保留**: 当前执行节点的完整输出、Gate 判定结果
2. **高优先级保留**: T13 对抗结果、T26 反思结论、T27 验证报告
3. **中优先级保留**: T22-T25 的 output_schema 摘要
4. **低优先级可截断**: 中间步骤的详细推理过程、重复性论述
5. **可完全移除**: 历史递归轮次的中间输出（仅保留最终结论）

### 全局安全机制（EXHAUST 一致性）

- **无最大递归轮次上限**：递归由质量驱动终止（ΔInfo(t) < ε 或所有缺口已处理），不设轮数硬上限
- **无 Token 硬上限**：通过 write-while-research 批量写入释放上下文，可无限延续
- **上下文压力响应**：当上下文使用率 > 95% 时，触发强制批量写入（force batch write），写入后继续生成，不丢弃任何分析维度、不跳过任何节点

### 节点级递归终止条件（质量驱动，非轮数硬上限）

| 节点 | 终止条件 | 说明 |
|------|----------|------|
| T13 | depth_satisfaction.score ≥ 0.85 或所有深度信号已充分处理 | 质量驱动收敛 |
| T24 | 维度覆盖完整且无新增洞察 | 质量驱动收敛 |
| T26 | 无新跨维度洞察产生 | 质量驱动收敛 |
| Gate-δ 退回 | 所有失败项已修复并通过 | 持续重试直至通过 |

### 递归上下文膨胀监控

每轮递归后检查:
1. 上下文增长率 (应 <30%/轮)
2. 新增信息密度 (应 >0.5 新洞察/千字)
3. 重复率 (应 <20%)

如任一指标不满足，触发 write-while-research 批量写入释放上下文，**不触发提前终止递归**——递归终止仅由质量驱动条件决定。

## 交叉引用

- [nrsf-protocol.md](./nrsf-protocol.md) — NRSF 叙事式研究状态文件协议
- [checkpoint-protocol.md](./checkpoint-protocol.md) — Checkpoint 原子写入与断点续传协议
- [handoff-protocol.md](./handoff-protocol.md) — Context Package 标准格式
- [formula-engine/info-decay.md](../formula-engine/info-decay.md) — 指数边际收益衰减模型

## 迭代终止逻辑（指数衰减模型）

在判断是否停止迭代时，调用 `formula-engine/info-decay` 指数边际收益衰减模型：

1. 每轮迭代后计算 ΔInfo(t) = α · exp(-λt)（默认 α=1.0, λ=0.3）
2. 当 ΔInfo(t) < ε（默认 ε=0.05）时：自动终止迭代，标记为"信息增益收敛"
3. 不做固定迭代上限限制——衰减模型动态决定何时停止
4. 替代原硬阈值：depth_satisfaction ≥ 0.9（已移除迭代次数守卫硬上限，改为质量驱动终止）

I01 终止条件已同步更新，参见 tasks/I01_iterative_deepening.md

## 测试用例（D3.4.4）

> 本章节定义 context-budget-protocol 的验证测试用例，每个用例采用「给定输入 X，应产出 Y」格式。

### TC-1: tiktoken 精确计数（GREEN 级别）

**给定输入**：上下文窗口限制 200,000 tokens，当前活跃上下文经 tiktoken (cl100k_base) 计数为 80,000 tokens（budget_percent = 40%），触发事件为 T05 节点执行完成。

**应产出**：
- threshold_level = "GREEN"
- action_taken = "none"
- execution_ledger 追加一条 token_count_log，log_type="token_count"，trigger="node_completed"，token_count_method="tiktoken"
- 不触发 LLMLingua 压缩，不触发 Checkpoint 落盘

### TC-2: YELLOW 级别触发 LLMLingua 压缩

**给定输入**：上下文窗口限制 200,000 tokens，T10/T11/T12 并行执行完成后活跃上下文经 tiktoken 计数为 140,000 tokens（budget_percent = 70%），处于 YELLOW 区间（60%-80%）。所有节点的 process_description 与 methodology_notes 总计 60,000 tokens。

**应产出**：
- threshold_level = "YELLOW"
- action_taken = "llmlingua_compress"
- 对所有节点的 process_description 与 methodology_notes 执行 LLMLingua 压缩（目标压缩率 50%）
- 压缩后 process_description + methodology_notes 约 30,000 tokens，总活跃上下文降至约 110,000 tokens（budget_percent ≈ 55%，回落到 GREEN）
- execution_ledger 追加两条日志：一条 trigger="node_completed"（压缩前），一条 trigger="post_llmlingua"（压缩后）
- post_action_budget_percent ≈ 55%

### TC-3: YELLOW 压缩后仍未回落到 GREEN → 落盘后释放

**给定输入**：上下文窗口限制 200,000 tokens，活跃上下文 150,000 tokens（budget_percent = 75%，YELLOW）。LLMLingua 压缩 process_description 与 methodology_notes 后，总活跃上下文仅降至 130,000 tokens（budget_percent = 65%，仍为 YELLOW，未回落到 GREEN）。

**应产出**：
- 执行阶段二：将压缩后的 process_description 与 methodology_notes 写入 Checkpoint 文件后从上下文释放
- 释放后活跃上下文降至约 70,000 tokens（budget_percent ≈ 35%，GREEN）
- execution_ledger 追加 trigger="post_checkpoint_flush" 日志，released_tokens ≈ 60,000
- Checkpoint 文件包含压缩后的 process_description 与 methodology_notes，附引用指针
- 下游节点可通过引用指针按需读取

### TC-4: RED 级别主动落盘到 Checkpoint

**给定输入**：上下文窗口限制 200,000 tokens，T15 领域引擎分析完成后活跃上下文 180,000 tokens（budget_percent = 90%，RED 区间 80%-95%）。

**应产出**：
- threshold_level = "RED"
- action_taken = "checkpoint_flush"
- 跳过 LLMLingua 压缩（RED 级别时间紧迫）
- 触发批量写入（write-while-research），将全部活跃上下文（core_conclusions/key_findings/supporting_evidence/process_description/methodology_notes/intermediate_results）完整写入 Checkpoint 文件
- 释放后活跃上下文重置为仅含引用指针和执行状态（约 5,000 tokens，budget_percent ≈ 2.5%，GREEN）
- execution_ledger 追加 trigger="post_checkpoint_flush" 日志，released_tokens ≈ 175,000
- 下游节点（T16/T17/T18/T19）通过引用指针从 Checkpoint 按需加载

### TC-5: 强制落盘（>95%）

**给定输入**：上下文窗口限制 200,000 tokens，由于 NRSF-Full 大量加载，活跃上下文达到 196,000 tokens（budget_percent = 98%，>95%，强制落盘）。

**应产出**：
- threshold_level = "FORCE_FLUSH"
- action_taken = "force_flush"
- 强制批量写入（force batch write），将全部活跃上下文完整写入 Checkpoint 文件
- 释放后活跃上下文重置为仅含引用指针和执行状态
- 继续生成：不丢弃任何分析维度，不跳过任何未执行节点，不终止研究
- T19 交付守卫标注批量写入影响范围（写入的文件路径和释放的上下文量）
- T20 渲染时附加声明："本报告因上下文预算压力（超过95%），已通过批量写入机制完整保留所有分析维度，无任何维度被丢弃或简化"

### TC-6: tiktoken 不可用回退字符估算

**给定输入**：tiktoken 库未安装（ImportError），上下文窗口限制 200,000 tokens，当前活跃上下文按字符估算（中文 1 字 ≈ 1.3 token）为 100,000 tokens（budget_percent = 50%，GREEN）。

**应产出**：
- token_count_method = "char_estimate"（非 tiktoken）
- execution_ledger 日志中标注 token_count_method="char_estimate"
- threshold_level = "GREEN"
- 后续若触发 YELLOW/RED，仍按字符估算的预算百分比决策
- 在 token 计数聚合报告中，method_distribution.char_estimate += 1
