# 熔断机制（Fuse Mechanism）

> Visual DNA 审美进化 · 满分 + 熔断机制
>
> 追求五维门禁全部 100 分，但设最大重试次数 3 次，超过则质量保持为最高分方案。

---

## 1. 熔断机制算法（完整伪代码）

```text
function fuse_mechanism(render_output):
    attempt = 0
    scores_history = []
    outputs_history = []

    while attempt < 3:
        attempt += 1

        // Step 1: ASR 硬门检查
        asr_result = asr_hard_gate.check(render_output)  // 详见 asr-hard-gate.md
        if asr_result.failed:
            if attempt >= 3:
                return exhaust_retry(scores_history, outputs_history)
            render_output = fix_asr_violations(render_output, asr_result.violations)
            continue

        // Step 2: Golden Set 距离校验
        golden_result = golden_set_validator.validate(render_output)  // 详见 golden-set-validator.md
        if golden_result.failed:
            if attempt >= 3:
                return exhaust_retry(scores_history, outputs_history)
            render_output = fix_golden_deviation(render_output, golden_result)
            continue

        // Step 3: 五维门禁审查
        taste_result = taste_validator.validate(render_output)  // 详见 taste-validator.md
        scores_history.append(taste_result.scores)
        outputs_history.append(render_output)

        // Step 4: 判断是否全满分
        if taste_result.all_dimensions_pass:
            return PASS(render_output, attempt)

        // Step 5: 定向修复（仅修复未满分维度，含可回滚原则 §2.3）
        if attempt < 3:
            snapshot = copy(render_output)
            fixed_output = fix_failed_dimensions(render_output, taste_result.failed_dimensions)
            fixed_taste_result = taste_validator.validate(fixed_output)
            if sum(fixed_taste_result.scores) < sum(taste_result.scores):
                render_output = snapshot  // 回滚：修复后综合得分下降，恢复修复前版本
                continue
            render_output = fixed_output

    // Step 6: 熔断质量保持
    return exhaust_retry(scores_history, outputs_history)

function exhaust_retry(scores_history, outputs_history):
    // 边界条件：所有方案都未通过 ASR 硬门（outputs_history 为空）
    if len(outputs_history) == 0:
        return ERROR("[FUSE-FAILED] 所有方案均未通过 ASR 硬门，需人工介入")

    // 找到综合得分最高的方案
    best_index = argmax(sum(scores) for scores in scores_history)
    best_output = outputs_history[best_index]
    best_score = sum(scores_history[best_index])

    // 标注质量保持
    best_output.add_marker("[FUSE-EXHAUST-RETRY] 未达满分，已质量保持为最高分方案（综合得分 {best_score}/500）")

    return EXHAUST_RETRY(best_output, best_score)
```

### 算法关键点

- **无死循环保证**：`while attempt < 3` 严格限定循环上界，`attempt` 每轮自增，最多执行 3 次循环体后必终止。
- **前置门禁优先**：ASR 硬门 → Golden Set 校验 → 五维门禁，三者顺序不可调换，前序失败不计入五维评分历史。
- **得分历史累积**：仅当通过 ASR 硬门与 Golden Set 校验后，才将五维得分与对应输出纳入 `scores_history` / `outputs_history`，供质量保持时挑选最优。
- **定向修复**：重试时仅修复未满分维度，已满分维度保持不动，避免"修一处坏一处"的回退风险。
- **可回滚原则（§2.3）**：每次定向修复前快照当前 `render_output`，修复后重新执行五维门禁审查，若综合得分下降则回滚到修复前版本，确保修复不会导致质量退化。
- **质量保持安全网**：质量保持方案必须通过 ASR 硬门（因未通过 ASR 的方案不会进入 `outputs_history`），保证质量保持不会降到违反硬门的方案。
- **质量保持边界条件**：`exhaust_retry` 函数开头检查 `outputs_history` 是否为空，若为空（所有方案都未通过 ASR 硬门）则返回 `[FUSE-FAILED]` 错误，要求人工介入，避免 `argmax` 对空列表操作导致异常。

---

## 2. 重试策略

### 2.1 首次渲染与重试流程

- **首次渲染**：执行完整渲染管线 → ASR 硬门 → Golden Set 校验 → 五维门禁
- **若五维全满分**：直接通过，进入导出
- **若任一维度未满分**：记录得分，触发重试（重试次数 +1）
- **重试时仅修复未满分的维度**，不重新渲染已满分的部分

### 2.2 维度定向修复策略

| 未满分维度 | 修复策略 |
| --- | --- |
| 排版门禁 | 调整字号 / 字重 / 行高 / 段落排版 / 中西文混排 |
| 审美门禁 | 调整配色 / 视觉层级 / 留白 / 装饰 |
| 配图门禁 | 增加配图 / 调整风格 / 提高分辨率 / 补充 Alt / 调整排版 |
| 语义一致性门禁 | 调整段落呈现形式 / 图表类型 / 标题层级 |
| 品牌 DNA 一致性门禁 | 统一配色 / 字体 / 间距 |

### 2.3 修复原则

- **最小改动原则**：只动未满分维度对应的视觉原子，不触碰已满分维度。
- **可回滚原则**：每次修复前快照当前 `render_output`，若修复后综合得分下降，则回滚到修复前版本并计入历史。
- **不重复犯错原则**：修复策略需记录已尝试方案，避免在同一维度上反复尝试相同修复手段。

---

## 3. 最大重试 3 次限制

### 3.1 重试次数计数器

| attempt 值 | 含义 | 说明 |
| --- | --- | --- |
| 0 | 首次渲染 | 进入 `fuse_mechanism` 时的初始渲染 |
| 1 | 第一次重试 | 首次未满分后的第一次定向修复 |
| 2 | 第二次重试（最后一次） | 第一次重试后仍未满分的第二次定向修复（最后一次尝试） |
| >= 3 | 不再重试 | `while attempt < 3` 条件不满足，直接质量保持 |

> **attempt 语义说明**: 表中 `attempt` 值表示 `while attempt < 3` 循环条件检查点的值。伪代码中 `attempt` 从 0 开始，循环条件 `attempt < 3` 在 attempt=0/1/2 时为真（共 3 次迭代），attempt=3 时为假退出循环。因此最多 3 次尝试（1 次首次渲染 + 2 次重试），与伪代码 `while attempt < 3` 完全一致。

### 3.2 计数规则

- **ASR 硬门失败触发重试**：计入熔断计数（`attempt += 1`）
- **Golden Set 校验失败触发重试**：计入熔断计数（`attempt += 1`）
- **五维门禁未满分触发重试**：计入熔断计数（`attempt += 1`）
- **L1-L5 渲染层重试**：**不计入**熔断计数（详见第 5 节）

### 3.3 终止条件

- 任一 `attempt` 达到全满分 → 立即 PASS，终止流程
- `attempt` 达到 3（即 `while attempt < 3` 条件不满足）且仍未满分 → 进入质量保持流程，终止重试
- 不存在 `attempt >= 3` 的重试分支（attempt=3 时循环已退出）

---

## 4. 质量保持逻辑

### 4.1 质量保持触发条件

3 次尝试后（即 `attempt >= 3` 时）仍未全满分，触发质量保持。

### 4.2 质量保持方案选择

- 从 `scores_history` 中挑选综合得分（五维之和）最高的方案
- 若存在多个并列最高分，选择最早出现的方案（即 `attempt` 最小的那个）
- 质量保持方案必须通过 ASR 硬门（算法保证：未通过 ASR 的方案不会进入 `outputs_history`）

### 4.3 质量保持标注

质量保持方案必须添加以下标注：

```text
[FUSE-EXHAUST-RETRY] 未达满分，已质量保持为最高分方案（综合得分 XX/500）
```

其中 `XX` 为质量保持方案的综合得分（五维之和，满分 500）。

> **质量保持标注在导出环节的保留**: `[FUSE-EXHAUST-RETRY]` 标注在导出环节 `export()`（详见 `output-rendering-protocol.md` §2.3）中保留，不被内部标记剥离规则移除。最终交付物中可见质量保持标记和综合得分，确保用户知晓该输出为质量保持方案（未达五维满分），提升交付透明度。

### 4.4 质量保持失败兜底

- 若所有方案都未通过 ASR 硬门（即 `outputs_history` 为空）：返回错误，要求人工介入
- 错误信息：`[FUSE-FAILED] 所有方案均未通过 ASR 硬门，需人工介入`

---

## 5. 与其他机制的协同

### 5.1 与 L1-L5 渲染层重试的关系

| 机制 | 职责 | 触发条件 | 计数归属 |
| --- | --- | --- | --- |
| L1-L5 渲染层重试 | 渲染层重试（渲染失败时的技术重试） | 渲染引擎报错、超时、资源缺失等技术性失败 | 独立计数，不计入熔断 |
| 熔断机制 | 审美层重试（审美未满分时的质量重试） | ASR / Golden Set / 五维门禁未通过 | 熔断独立计数 |

**协同原则**：

- 两者**不冲突、不重复计数**
- L1-L5 重试**不计入**熔断的 3 次限制
- L1-L5 重试成功后，渲染输出才进入熔断的 ASR 硬门检查
- 即：L1-L5 管"能不能渲染出来"，熔断管"渲染出来的够不够好看"

### 5.2 与 ASR 硬门的关系

- ASR 硬门是熔断的**前置门禁**
- ASR 违规触发重试，**计入**熔断计数
- ASR 违规的修复策略：`fix_asr_violations(render_output, asr_result.violations)`
- 质量保持方案仍必须通过 ASR 硬门（算法保证）

### 5.3 与 Golden Set 的关系

- Golden Set 是熔断的**前置校验**
- Golden Set FAIL 触发重试，**计入**熔断计数
- Golden Set 偏差的修复策略：`fix_golden_deviation(render_output, golden_result)`
- Golden Set 校验失败不会进入五维门禁评分（避免污染得分历史）

### 5.4 与五维门禁的关系

- 五维门禁是熔断的**核心评判**
- 五维未满分触发重试，**计入**熔断计数
- 五维得分是质量保持方案选择的唯一依据（综合得分 = 五维之和）
- 五维定向修复策略：`fix_failed_dimensions(render_output, taste_result.failed_dimensions)`

### 5.5 协同流程图

```text
渲染请求
   │
   ▼
L1-L5 渲染层重试（技术重试，独立计数）
   │
   ▼ 渲染成功
熔断机制（审美重试，最多 3 次）
   │
   ├─ Step 1: ASR 硬门 ──失败──► 修复 ──► 重试（计数 +1）
   │                                  │
   │                                  └─ attempt >= 3 ──► 质量保持
   │
   ├─ Step 2: Golden Set 校验 ──失败──► 修复 ──► 重试（计数 +1）
   │                                        │
   │                                        └─ attempt >= 3 ──► 质量保持
   │
   ├─ Step 3: 五维门禁 ──未满分──► 定向修复 ──► 重试（计数 +1）
   │                                              │
   │                                              └─ attempt >= 3 ──► 质量保持
   │
   └─ 全满分 ──► PASS（进入导出）
```

---

## 6. 场景示例

### 场景 1：首次即满分

**流程**：

```text
首次渲染
   │
   ▼
ASR 硬门 ──通过──►
   │
   ▼
Golden Set 校验 ──通过──►
   │
   ▼
五维门禁 ──全满分（500/500）──►
   │
   ▼
PASS（attempt = 0）
```

**结果**：直接通过，进入导出，无重试，无质量保持。

---

### 场景 2：重试后达满分

**流程**：

```text
首次渲染（attempt = 0）
   │
   ▼
ASR 硬门 ──通过──►
   │
   ▼
Golden Set 校验 ──通过──►
   │
   ▼
五维门禁 ──配图门禁 80 分，其余满分（480/500）──►
   │
   ▼
定向修复配图门禁（增加配图 / 调整风格 / 提高分辨率）
   │
   ▼
重试 1 次（attempt = 1）
   │
   ▼
ASR 硬门 ──通过──►
   │
   ▼
Golden Set 校验 ──通过──►
   │
   ▼
五维门禁 ──全满分（500/500）──►
   │
   ▼
PASS（attempt = 1）
```

**结果**：重试 1 次后达到全满分，通过，进入导出。

---

### 场景 3：熔断质量保持

**流程**：

```text
首次渲染（attempt = 0）
   │
   ▼
ASR 硬门 ──通过──► Golden Set 校验 ──通过──►
   │
   ▼
五维门禁 ──审美门禁 95 分，其余满分（综合 480/500）──►
   │  scores_history = [{排版:100, 审美:95, 配图:100, 语义:100, 品牌:100}]
   │  outputs_history = [render_output_v0]
   ▼
定向修复审美门禁（调整配色 / 视觉层级 / 留白 / 装饰）
   │
   ▼
重试 1 次（attempt = 1）
   │
   ▼
ASR 硬门 ──通过──► Golden Set 校验 ──通过──►
   │
   ▼
五维门禁 ──审美门禁 92 分，其余满分（综合 475/500）──►
   │  scores_history = [..., {排版:100, 审美:92, 配图:100, 语义:100, 品牌:100}]
   │  outputs_history = [..., render_output_v1]
   ▼
定向修复审美门禁（换一种修复策略）
   │
   ▼
重试 2 次（attempt = 2）
   │
   ▼
ASR 硬门 ──通过──► Golden Set 校验 ──通过──►
   │
   ▼
五维门禁 ──审美门禁 90 分，其余满分（综合 470/500）──►
   │  scores_history = [..., {排版:100, 审美:90, 配图:100, 语义:100, 品牌:100}]
   │  outputs_history = [..., render_output_v2]
   ▼
attempt = 3，仍未全满分 ──► 触发质量保持
   │
   ▼
exhaust_retry(scores_history, outputs_history)
   │
   ▼
3 次尝试综合得分：480/500, 475/500, 470/500
   │
   ▼
最高分方案：第 1 次尝试（render_output_v0，480/500）
   │
   ▼
标注：[FUSE-EXHAUST-RETRY] 未达满分，已质量保持为最高分方案（综合得分 480/500）
   │
   ▼
EXHAUST_RETRY（render_output_v0, 480）
```

**结果**：3 次尝试均未达全满分，质量保持为综合得分最高的第 1 次尝试方案（480/500），添加质量保持标注后输出。

---

## 7. 不变量（Invariants）

为保证熔断机制正确性，以下不变量在任何情况下都必须成立：

1. **终止性**：`fuse_mechanism` 必在 `attempt` 达到 3 时终止，无死循环风险。
2. **ASR 优先性**：ASR 硬门永远先于 Golden Set 校验与五维门禁执行。
3. **得分历史纯洁性**：`scores_history` / `outputs_history` 仅包含通过 ASR 硬门与 Golden Set 校验的方案。
4. **质量保持安全性**：质量保持方案必须通过 ASR 硬门（由不变量 3 保证）。
5. **计数独立性**：L1-L5 渲染层重试不计入熔断的 3 次限制。
6. **定向修复性**：重试时仅修复未满分维度，不重新渲染已满分部分。
7. **质量保持标注强制性**：质量保持方案必须添加 `[FUSE-EXHAUST-RETRY]` 标注，标注格式不可省略。

<!-- 作者：阿洋 -->
