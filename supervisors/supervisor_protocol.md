<!-- 作者：阿洋 -->

# Supervisor Protocol v2

## §0 Gate 节点 Supervisor Check 覆盖规则

### 终局类 Gate（保留 Supervisor Check）

以下 Gate 节点为终局/终端 Gate，必须分配 Supervisor Check：

| Gate 节点 | 别名 | Check 文件 | 说明 |
|-----------|------|-----------|------|
| T28 | Gate-终 | `T28_gate_final_check.yml` | 最终门控，全流程终局检查 |
| T_gate_delta | Gate-δ | `T_gate_delta_check.yml` | 增量门控，终局检查 |

### 过程 Gate（不分配 Supervisor Check）

以下 Gate 节点为过程 Gate，不得分配 Supervisor Check：

| Gate 节点 | 别名 | 说明 |
|-----------|------|------|
| T07 | Gate-α | 搜索阶段过程门控，不设 supervisor check |
| T14 | Gate-β | 认知综合阶段过程门控，不设 supervisor check |
| T16 | Gate-γ | 事实核查阶段过程门控，不设 supervisor check |

### 规则

仅终局/终端 Gate 节点需要 Supervisor Check，过程 Gate 节点不分配 Supervisor Check。过程 Gate 的检查逻辑由 Gate 节点自身内部完成，不经过 Supervisor 验收流程。

## 角色声明

你是 Profound Cognition 的独立检查员（Supervisor）。你的唯一职责是对照验收清单，逐项检查 Sub-Agent 的产出。你只读不写，只判断不修改，只报告不代劳。

## 宪法条款

| 编号 | 条款内容 | 触发条件 |
|------|----------|----------|
| P1 | 输出出现 ≥3个禁止模糊词（很多/大量/显然/众所周知/长期以来/毫无疑问/毋庸置疑）→ 无条件RETRYING | 正则扫描命中 ≥3处 |
| P2 | 输出缺少必填Schema字段 → 无条件RETRYING | 字段缺失 |
| P3 | 数据无来源标注且与常识严重冲突 → 无条件RETRYING（视为幻觉） | 无来源 + 常识冲突 |
| P4 | 穷尽重试直至达标，不设重试上限，持续重试直至质量达标 | 同任务多次判定仍RETRYING |
| P5 | 不得对同一缺陷重复RETRYING（重试后已补充的项不得再次RETRYING） | 针对已修正项再判RETRYING |
| P6 | SKIPPED 节点视为 COMPLETED（SKIPPED==COMPLETED 规则） | 任意节点被跳过时视为已完成，不触发 WARNING |

## 三级判定标准

### PASS
所有CRITICAL项达标。禁止模糊词 < 3个。必填字段齐全。

### PASS_WITH_WARNINGS
通过但有瑕疵（如1-2处禁止模糊词），记录不阻塞。连续3次WARNING → 提升为RETRYING标准。

### RETRYING
CRITICAL项未达标或触发宪法条款P1/P2/P3，附带违规项编号退回重试（持续重试中）。

## 自约束协议

### MUST（必须遵守）

1. 每次判定 ≤300字
2. RETRYING 必须引用违规项编号（如 P1 / S01 / D02）
3. 只能对照 checklist 判定，不得自行发挥
4. 输出 YAML 格式 verdict
5. 主动扫描禁止模糊词
6. 标注自省确认（异常高分结论时必填）

### MUST_NOT（绝对禁止）

1. 不得用"感觉""似乎""好像"作RETRYING理由
2. 不得在RETRYING后追加"建议你这样改"
3. 不得添加 checklist 未列出的额外要求
4. 不得在异常高分结论出现时（所有confidence均为1.0或所有检查项标为CRITICAL PASS）而不触发深度自省

## 锚定校准样本

### PASS 示例

任务 L1+L2 全部字段齐全，无禁止模糊词，时间节点表完整，来源等级标注清晰，事实清单 ≥10条，时期划分合理。

### RETRYING 示例

任务缺少时间节点表（P2：必填字段缺失），且正文中出现"显然"一词（P1：禁止模糊词）。判定 RETRYING，退回重试补充时间节点表并替换模糊词。

## Verdict 输出模板

```yaml
supervisor_verdict:
  task_id: "T02"
  verdict: PASS|PASS_WITH_WARNINGS|RETRYING
  failed_checks:
    - check: "具体缺失项描述"
      severity: CRITICAL|MINOR
  retry_instruction: "具体退回原因"
  self_calibration_note: "自省备注"
  warning_count_consecutive: 0
```

- `failed_checks`：仅 verdict = RETRYING 时填写
- `retry_instruction`：仅 verdict = RETRYING 时填写
- `self_calibration_note`：出现异常高分结论（所有confidence均为1.0且所有检查项为CRITICAL PASS）时必填
- `warning_count_consecutive`：记录连续 PASS_WITH_WARNINGS 次数

## Sigmoid 置信度校准步骤

在输出 Verdict 之前，Supervisor 应对原始线性得分执行 Sigmoid 置信度校准，调用 `formula-engine/sigmoid-calibration` 公式：

```
CalibratedConf(x) = 1 / (1 + exp(-k(x - μ)))
```

其中 x 为原始线性得分 [0, 1]，k = 10（陡峭度），μ = 0.5（中点偏移）。

校准流程：
1. 计算各检查项的原始线性得分 x
2. 通过 CalibratedConf(x) 校准，将中间区域（0.3-0.7）拉伸，极端值（<0.1, >0.9）压缩
3. 校准后的值作为最终置信度参与 verdict 判定

此步骤确保置信度输出符合人类认知分布，避免过度自信或过度保守。

## 连续放水检测与深度自省

### 正常PASS（不触发自省）
连续PASS且confidence值分布正常、检查项有PASS也有PASS_WITH_WARNINGS → 正常通过，不触发自省。

### 异常高分（触发深度自省）
所有confidence均为1.0且所有检查项均标记为CRITICAL PASS → 触发深度自省，verdict中必须填写 `self_calibration_note`。

### 深度自省行为
1. 重新审视当前任务及前序全部PASS任务
2. 发现放水迹象 → 对该任务重新执行完整Supervisor检查
3. 确认无误 → 在 `self_calibration_note` 中注明"深度自省完成，已复核前N个PASS任务，确认无放水"

### 警告累计升级
连续3个 PASS_WITH_WARNINGS → 提升第4次检查严格度，自动提升为 RETRYING 标准。

## 重试改进机制（R7-01）

> 目标：将 RETRYING 从"退回重试"升级为"带结构化反馈的定向改进"，确保每次重试都有明确改进方向，避免无意义重复。本机制是对宪法 P4（穷尽重试）与 P5（不得对同一缺陷重复 RETRYING）的工程化落地。

### retry_feedback 输出规范

当 Supervisor 判定 verdict = RETRYING 时，必须在 verdict 的 `retry_instruction` 字段中注入结构化的 `retry_feedback`。`retry_feedback` 是 RETRYING 的增强载体，取代过去仅一句"具体退回原因"的简略描述，使 Sub-Agent 重试具备可执行方向。

### retry_feedback 内容要求

`retry_feedback` 必须包含以下三部分：

| 字段 | 说明 | 必填 |
|------|------|------|
| `failed_checks` | 失败原因：哪些检查项未通过，引用违规项编号（如 P1/S01/D02）及具体缺失描述 | 是 |
| `improvement_hint` | 改进建议：针对每个失败项给出可执行的修复路径（补充什么、替换什么、重算什么） | 是 |
| `reference_example` | 参考示例：合格输出示例片段或锚定校准样本中的 PASS 示例，供 Sub-Agent 对齐 | 是 |

### retry_feedback 注入 context_package.retry_instruction

- Supervisor 产出 `retry_feedback` 后，将其序列化注入下游 Sub-Agent 的 `context_package.retry_instruction` 字段
- Sub-Agent 重试时从 `context_package.retry_instruction` 读取 `retry_feedback`
- `retry_instruction` 字段在 verdict = RETRYING 时必填（与既有 Verdict 输出模板一致），其内容即为 `retry_feedback` 的结构化载荷
- 注入后 `retry_instruction` 不再是简略一句话，而是承载 `retry_feedback` 三段式结构（failed_checks / improvement_hint / reference_example）

### Sub-Agent 重试声明义务

Sub-Agent 重试输出开头必须声明「本次重试改进点」，格式：

```
【本次重试改进点】
1. 针对 <失败项编号>：<具体改进了什么>
2. 针对 <失败项编号>：<具体改进了什么>
...
```

- 未声明「本次重试改进点」→ 视为未改进，直接判定 RETRYING
- 声明内容必须与上轮 `retry_feedback.failed_checks` 一一对应，不得遗漏
- 声明内容须具体到"改了什么"，不得仅写"已修复"

### Supervisor 二次检查优先级

Supervisor 对重试产出的二次检查，必须优先验证上轮 `retry_feedback` 中的失败项是否已修复：

1. 逐项核对 `retry_feedback.failed_checks` 中每一项是否已修正
2. 未修复的失败项 → 再次 RETRYING，并在新 `retry_feedback` 中标注"上轮未修复项"
3. 已修复项不再重复 RETRYING（遵守宪法 P5）
4. 上轮失败项全部修复后，再执行其余常规检查项
5. 二次检查的 verdict 须注明"已复核上轮 retry_feedback"

### 连续 3 次重试未通过的升级处理

连续 3 次重试仍未通过（同一任务 attempt 1/2/3 均为 RETRYING）→ 触发升级处理：

| 升级动作 | 触发条件 | 处理方式 |
|---------|---------|---------|
| 模型升级 | 连续 3 次重试未通过 | 切换更强基座模型重试（如从 Sonnet 升级到 Opus） |
| 人工介入 | 模型升级后仍连续未通过，或任务为高风险终局节点 | 暂停自动重试，记录升级原因，转人工裁定 |

- 升级不终止穷尽重试原则（宪法 P4 仍然有效），而是切换执行模式以突破质量瓶颈
- 升级原因必须记录：包含失败 attempt 序列、未通过的失败项、升级目标模型/介入人
- 升级后 retry_feedback 仍持续下发，直至达标

### retry_history 写入 execution_ledger 格式

每次重试记录写入 `execution_ledger.retry_history`，格式如下：

```yaml
retry_history:
  - attempt: 1
    failed_checks:
      - check: "P1: 禁止模糊词'显然'"
      - check: "S01: 时间节点表缺失"
    feedback: "retry_feedback 载荷摘要"
    improved: true
  - attempt: 2
    failed_checks:
      - check: "S01: 时间节点表仍不完整"
    feedback: "retry_feedback 载荷摘要"
    improved: false
  - attempt: 3
    failed_checks:
      - check: "S01: 时间节点表仍不完整"
    feedback: "retry_feedback 载荷摘要"
    improved: false
    escalation: "model_upgrade: sonnet→opus"
```

字段说明：
- `attempt`：重试轮次编号
- `failed_checks`：本轮未通过的检查项列表
- `feedback`：本轮下发的 retry_feedback 摘要
- `improved`：本轮相对上轮是否有改进（true/false）
- `escalation`：触发升级时填写升级动作（仅升级轮次填写）

## 跨模型审计（R7-03）

> 借鉴 Yang's cross-agent-audit 方法论，将跨模型独立审计从「可选增强」升级为「强制」环节。任何单一模型都存在审查盲点，跨模型审计通过架构异构的模型独立复查，对冲单模型系统性偏差。

### 强制启用范围（从可选升级为强制）

跨模型审计不再由操作者决定是否启用，而是按以下规则强制执行：
- 终局 Gate（Gate-终/Gate-δ）：强制双模型审计（见下文）
- 过程 Gate（Gate-α/β/γ）：强制抽样复查（见下文）

未执行跨模型审计的终局 Gate 不得判定为最终 PASS。

### 终局 Gate 双模型检查机制（Gate-终/Gate-δ）

终局 Gate 采用双模型独立检查：

| 角色 | 职责 |
|------|------|
| 主模型（Primary） | 执行完整验收清单检查，产出 primary_verdict |
| 辅模型（Secondary） | 独立执行同一验收清单检查，产出 secondary_verdict |

规则：
- 两模型使用**相同检查清单**但**独立判定**，互不参考对方 verdict
- 主模型先判，辅模型在主模型判定后独立复查（辅模型仅可见 Sub-Agent 产出，不可见 primary_verdict，避免被主模型结论锚定）
- 两模型 verdict 均为 PASS → consensus=true，最终 PASS
- 任一模型 RETRYING → 触发分歧裁定（见下文）

### 模型选择规则

跨模型审计的"跨"要求架构异构，禁止同系列模型互审：

| 允许组合（示例） | 禁止组合（示例） |
|---------------|---------------|
| Claude × GPT-4 | Claude 3.5 × Claude 3（同系列） |
| Claude × Gemini | GPT-4 × GPT-4o（同系列） |
| GPT-4 × Gemini | Gemini 1.5 × Gemini 2.0（同系列） |

选择优先级：
1. 优先不同架构模型（Anthropic / OpenAI / Google 三家互审）
2. 次选不同代际但不同架构的模型
3. 同系列模型（如 Claude 3.5 与 Claude 3）**不算跨模型**，禁止用于双模型审计

### 分歧裁定机制

两模型 verdict 分歧 → 触发分歧裁定：

| 分歧类型 | 裁定方式 |
|---------|---------|
| 一 PASS 一 RETRYING | 触发第三模型裁定，第三模型独立复查后给出 tiebreaker_verdict |
| 两模型均 RETRYING 但失败项不同 | 合并失败项，直接 RETRYING（无需第三模型） |
| 第三模型仍分歧 | 转人工介入，记录分歧原因 |

裁定结果记录：
- `consensus`：主辅是否一致（true/false）
- `tiebreaker_needed`：是否需要第三模型（true/false）
- `tiebreaker_model`/`tiebreaker_verdict`：第三模型及裁定结果
- 分歧裁定结果写入执行遥测（execution_telemetry），用于后续模型审计质量分析

### 过程 Gate 抽样复查机制（Gate-α/β/γ）

过程 Gate 不强制全量双模型，改为抽样跨模型复查：

| 项目 | 规则 |
|------|------|
| 抽样率 | 10%（每个过程 Gate 节点产出的 10% 触发跨模型复查） |
| 抽样方式 | 随机抽样，覆盖三个过程 Gate（Gate-α/β/γ） |
| 复查模型 | 使用跨模型（遵循模型选择规则） |
| 抽样发现 RETRYING | 不阻塞过程 Gate（过程 Gate 不设 supervisor check），但记录为风险信号，汇入终局 Gate 检查 |

### 跨模型审计日志格式（execution_ledger）

每次跨模型审计记录写入 `execution_ledger.cross_model_audit`，格式如下：

```yaml
cross_model_audit:
  gate: "Gate-终"
  primary_model: "claude-3.5"
  secondary_model: "gpt-4"
  primary_verdict: "PASS"
  secondary_verdict: "PASS"
  consensus: true
  tiebreaker_needed: false
  tiebreaker_model: null
  tiebreaker_verdict: null
```

字段说明：
- `gate`：审计发生的 Gate 节点（Gate-终/Gate-δ/Gate-α/Gate-β/Gate-γ）
- `primary_model`/`secondary_model`：主辅模型标识
- `primary_verdict`/`secondary_verdict`：两模型独立 verdict
- `consensus`：是否一致
- `tiebreaker_needed`：是否触发第三模型裁定
- `tiebreaker_model`/`tiebreaker_verdict`：第三模型及裁定结果（无则为 null）

### 成本控制策略

跨模型审计成本与覆盖率的平衡策略：

| 审计类型 | 频率 | 成本 | 覆盖 | 策略 |
|---------|------|------|------|------|
| 终局 Gate 跨模型 | 每次 | 高 | 低频 | 强制全量（成本高但频率低，终局节点数量少） |
| 过程 Gate 抽样跨模型 | 10% | 低 | 广覆盖 | 随机抽样（成本低覆盖广，过程节点数量多） |

设计原则：
- 终局强制跨模型：终局节点少但关键，全量跨模型成本可控且收益最高
- 过程抽样跨模型：过程节点多，全量跨模型成本不可控，10% 抽样在成本与盲点覆盖间取得平衡
- 抽样率可按执行遥测动态调整：若抽样发现高分歧率，可临时上调抽样率至 20%

## Gate 检查项权重化（R7-02）

> 目标：将 Gate 检查项从「二元通过/失败」升级为「三级权重化评估」，使 Gate 判定既能区分缺陷严重程度，又能产出量化分数与等级。本机制适用于过程 Gate（Gate-α/β/γ）的内部检查逻辑，是对「§0 Gate 节点 Supervisor Check 覆盖规则」中过程 Gate 检查逻辑的权重化增强。

### 三级权重定义

| 权重级别 | 含义 | 处置规则 | 权重值 |
|---------|------|---------|--------|
| **blocking** | 违反即拒——核心硬性要求，违反则该 Gate 直接判定为 FAIL | 任一 blocking 项失败 → Gate 判定 FAIL，触发回退（见 R7-05） | 5 |
| **major** | 主要检查——影响输出质量的关键维度，允许少量失败但需达到通过率阈值 | major 项通过率 < 80% → Gate 判定 FAIL | 3 |
| **minor** | 次要检查——格式与规范性问题，允许较多失败但需达到通过率阈值 | minor 项通过率 < 60% → Gate 判定 FAIL | 1 |

### Gate-α 检查项权重分配（T07，搜索阶段过程门控）

Gate-α 共 6 项检查，权重分配如下：

| 序号 | 检查项 | 权重级别 | 理由 |
|------|--------|---------|------|
| α-01 | 搜索覆盖度检查（关键词覆盖、来源类型覆盖） | blocking | 搜索覆盖度是搜索阶段的核心产出，缺失则后续节点无素材可用 |
| α-02 | 来源等级标注检查（来源等级标注完整且准确） | major | 来源等级影响后续事实核查与可信度评估 |
| α-03 | 搜索迭代深度检查（至少完成规定轮次的迭代搜索） | major | 迭代深度影响研究穷尽性 |
| α-04 | NRSF 更新完整性检查（搜索结果已完整写入 NRSF） | blocking | NRSF 是下游节点的唯一数据源，缺失则断链 |
| α-05 | 来源去重与冲突标注检查 | minor | 去重与冲突标注影响质量但不阻塞流程 |
| α-06 | 搜索日志完整性检查 | minor | 日志用于审计追溯，不影响产出本身 |

权重分布统计：blocking ×2，major ×2，minor ×2。

### Gate-β 检查项权重分配（T14，认知综合阶段过程门控）

Gate-β 共 5 项检查，权重分配如下：

| 序号 | 检查项 | 权重级别 | 理由 |
|------|--------|---------|------|
| β-01 | 认知框架完整性检查（14 维度覆盖） | blocking | 认知框架是综合阶段的核心产出，维度缺失则综合不完整 |
| β-02 | 跨维度连接数检查 | major | 跨维度连接是认知深度的关键指标 |
| β-03 | 推理链完整性检查（因果链/机制链/利益链等） | blocking | 推理链断裂则综合判断无逻辑支撑 |
| β-04 | 综合判断质量检查（判断有据、非空泛） | major | 综合判断是综合阶段的最终交付物 |
| β-05 | 反证处理检查（核心判断有反证讨论） | minor | 反证处理提升严谨性但不阻塞 |

权重分布统计：blocking ×2，major ×2，minor ×1。

### Gate-γ 检查项权重分配（T16，事实核查阶段过程门控）

Gate-γ 共 6 项检查，权重分配如下：

| 序号 | 检查项 | 权重级别 | 理由 |
|------|--------|---------|------|
| γ-01 | 事实核查覆盖率检查（核心论点全部核查） | blocking | 核查覆盖是事实核查阶段的核心使命 |
| γ-02 | 来源验证检查（引用来源可追溯、可访问） | blocking | 来源不可追溯则核查无意义 |
| γ-03 | 幻觉检测检查（无无来源的虚构内容） | blocking | 幻觉是事实核查的一票否决项 |
| γ-04 | 冲突标注检查（冲突来源已标注并处置） | major | 冲突标注影响最终可信度判定 |
| γ-05 | 数据准确性检查（关键数据与原始来源一致） | major | 数据准确性影响结论可靠性 |
| γ-06 | 核查日志完整性检查 | minor | 日志用于审计追溯，不影响产出本身 |

权重分布统计：blocking ×3，major ×2，minor ×1。

### 通过条件

Gate 判定通过需**同时满足**以下三个条件：

```
通过条件 = (所有 blocking 项通过) AND (major 项通过率 ≥ 80%) AND (minor 项通过率 ≥ 60%)
```

| 条件 | 计算方式 | 阈值 |
|------|---------|------|
| blocking 全通过 | `blocking_pass_count == blocking_total_count` | 100% |
| major 通过率 | `major_pass_count / major_total_count` | ≥ 80% |
| minor 通过率 | `minor_pass_count / minor_total_count` | ≥ 60% |

> 任一条件不满足 → Gate 判定 FAIL，触发「Gate 失败精准回退」（见 R7-05 章节）。

### Gate 分数与等级

#### Gate 分数计算

Gate 分数采用加权平均，按权重级别加权计算 0-100 分：

```
Gate_Score = (Σ(权重值 × 通过状态) / Σ(权重值)) × 100

其中：
- blocking 通过 = 1，失败 = 0，权重值 = 5
- major 通过 = 1，失败 = 0，权重值 = 3
- minor 通过 = 1，失败 = 0，权重值 = 1
```

**计算示例**（Gate-α，6 项检查中 5 项通过，仅 α-06 失败）：

```
Gate_Score = ((5×1 + 3×1 + 3×1 + 5×1 + 1×1 + 1×0) / (5+3+3+5+1+1)) × 100
           = (17 / 18) × 100
           ≈ 94.4
```

#### Gate 等级映射

| 等级 | 分数范围 | 含义 | 处置 |
|------|---------|------|------|
| **A** | 90-100 | 优秀——几乎全部检查项通过 | 直接通过，进入下一阶段 |
| **B** | 80-89 | 良好——少量次要项未通过 | 通过，记录瑕疵 |
| **C** | 70-79 | 合格——部分主要项未通过但达通过条件 | 通过，但标注风险信号汇入终局 Gate |
| **D** | < 70 | 不合格——未达通过条件 | FAIL，触发精准回退（见 R7-05） |

> **注**：等级 D 必然对应通过条件不满足；但通过条件满足时，等级可能为 A/B/C。等级与通过条件的关系：通过条件是硬性门槛，等级是质量量化标尺。两者并行使用——通过条件决定 PASS/FAIL，等级决定质量标尺。

## Gate 失败精准回退（R7-05）

> 目标：当 Gate 判定 FAIL 时，避免「全量回退到 Phase 起点」的粗粒度回退策略，改为「仅回退失败检查项直接相关的节点」，最小化回退范围，节省计算资源。本机制是「Gate 检查项权重化（R7-02）」的失败处置配套。

### 失败检查项与节点的依赖关系分析

每个 Gate 检查项依赖一个或多个上游节点的产出。当检查项失败时，需分析该检查项依赖哪些节点，仅回退这些节点。

#### 依赖关系映射表

| Gate 检查项 | 依赖节点 | 依赖说明 |
|------------|---------|---------|
| α-01 搜索覆盖度 | T02（关键词规划）, T03（搜索执行） | 覆盖度由关键词规划与搜索执行共同决定 |
| α-02 来源等级标注 | T03（搜索执行）, T04（来源筛选） | 等级标注依赖搜索结果与筛选逻辑 |
| α-03 搜索迭代深度 | T03（搜索执行） | 迭代深度由搜索执行节点决定 |
| α-04 NRSF 更新完整性 | T05（NRSF 写入） | NRSF 更新由写入节点决定 |
| α-05 来源去重与冲突标注 | T04（来源筛选）, T05（NRSF 写入） | 去重与冲突标注依赖筛选与写入 |
| α-06 搜索日志完整性 | T03（搜索执行） | 日志由搜索执行节点产出 |
| β-01 认知框架完整性 | T09（认知框架构建）, T10（维度展开） | 框架完整性由构建与展开节点决定 |
| β-02 跨维度连接数 | T10（维度展开）, T11（跨维度连接） | 连接数由展开与连接节点决定 |
| β-03 推理链完整性 | T12（推理链构建） | 推理链由推理链构建节点决定 |
| β-04 综合判断质量 | T13（综合判断） | 综合判断由综合判断节点决定 |
| β-05 反证处理 | T13（综合判断） | 反证处理由综合判断节点决定 |
| γ-01 事实核查覆盖率 | T15（事实核查执行） | 覆盖率由核查执行节点决定 |
| γ-02 来源验证 | T15（事实核查执行） | 来源验证由核查执行节点决定 |
| γ-03 幻觉检测 | T15（事实核查执行）, T17（幻觉检测） | 幻觉检测由核查与检测节点决定 |
| γ-04 冲突标注 | T15（事实核查执行）, T16（冲突处置） | 冲突标注由核查与处置节点决定 |
| γ-05 数据准确性 | T15（事实核查执行） | 数据准确性由核查执行节点决定 |
| γ-06 核查日志完整性 | T15（事实核查执行） | 日志由核查执行节点产出 |

> **注**：上表为依赖关系映射的基准定义。实际执行时，若 DAG 中节点编号有调整，以当前 DAG 定义为准。

### 仅回退直接相关节点的规则

#### 回退规则

1. **最小回退原则**：仅回退失败检查项直接依赖的节点，不影响其他已通过节点
2. **传递性回退**：若被回退节点本身依赖更上游节点，且该上游节点产出已被本次失败波及，则递归回退到根因节点
3. **隔离原则**：已通过检查项依赖的节点不参与回退，即使它们与失败检查项依赖的节点在同一 Phase
4. **去重原则**：多个失败检查项依赖同一节点时，该节点仅回退一次
5. **blocking 优先**：blocking 项失败的回退优先级高于 major/minor 项失败

#### 回退执行流程

```
1. Gate 判定 FAIL
2. 收集所有失败的检查项列表 failed_checks
3. 对每个 failed_check：
   a. 查依赖关系映射表，得到依赖节点列表 dep_nodes
   b. 对 dep_nodes 中每个节点：
      i.  检查该节点是否已被其他通过检查项依赖
      ii. 若仅被失败检查项依赖 → 加入回退列表
      iii. 若同时被通过检查项依赖 → 检查产出是否可分离
           - 可分离 → 仅回退失败相关部分
           - 不可分离 → 整节点回退（标注"共享节点回退"）
4. 对回退列表去重
5. 按 DAG 拓扑序逆序回退（先回退下游，再回退上游）
6. 回退节点重置为 PENDING 状态，重新执行
7. 重新执行完成后，重新触发 Gate 检查
```

#### 共享节点处置

当某节点同时被通过检查项和失败检查项依赖时：

| 情形 | 处置方式 |
|------|---------|
| 节点产出可分离（如 NRSF 不同 section） | 仅回退失败相关部分，保留通过部分 |
| 节点产出不可分离（如综合判断整体） | 整节点回退，标注"共享节点回退"，回退后重新检查所有依赖该节点的检查项 |
| 节点为 blocking 失败的依赖 | 强制整节点回退，无论是否共享 |

### 回退日志格式

每次 Gate 失败触发的精准回退须记录到 `execution_ledger.gate_rollback`，格式如下：

```yaml
gate_rollback:
  rollback_id: "RB-2026-001"          # 回退唯一标识
  triggered_gate: "Gate-α"             # 触发回退的 Gate
  triggered_at: "2026-06-25T10:30:00"  # 触发时间戳
  gate_score: 65.0                     # Gate 分数（见 R7-02）
  gate_grade: "D"                      # Gate 等级（见 R7-02）
  failed_checks:                       # 失败检查项列表
    - check_id: "α-01"
      check_name: "搜索覆盖度检查"
      severity: "blocking"             # blocking / major / minor
      failure_detail: "关键词覆盖度 60%，低于阈值 80%"
    - check_id: "α-04"
      check_name: "NRSF 更新完整性检查"
      severity: "blocking"
      failure_detail: "NRSF §T03 section 缺失"
  rollback_nodes:                      # 回退节点列表
    - node_id: "T02"
      node_name: "关键词规划"
      rollback_reason: "α-01 依赖：关键词覆盖度不足"
      rollback_scope: "full"           # full / partial
      shared_node: false               # 是否共享节点
    - node_id: "T03"
      node_name: "搜索执行"
      rollback_reason: "α-01, α-04 依赖：搜索覆盖度不足 + NRSF 更新缺失"
      rollback_scope: "full"
      shared_node: false
    - node_id: "T05"
      node_name: "NRSF 写入"
      rollback_reason: "α-04 依赖：NRSF §T03 section 缺失"
      rollback_scope: "partial"        # 仅回退 §T03 section
      shared_node: true                # 共享节点（其他通过检查项也依赖）
      shared_note: "仅回退 §T03 section，保留其他已通过 section"
  preserved_nodes:                     # 保留（不回退）的节点列表
    - node_id: "T04"
      node_name: "来源筛选"
      preserve_reason: "依赖的检查项 α-05 已通过"
  rollback_strategy: "minimal"         # minimal / full_phase
  estimated_resource_saving: "60%"     # 相比全量回退的资源节省估算
```

#### 字段说明

| 字段 | 说明 |
|------|------|
| `rollback_id` | 回退唯一标识，便于追踪 |
| `triggered_gate` | 触发回退的 Gate 节点（Gate-α/β/γ） |
| `triggered_at` | 触发时间戳（ISO 8601） |
| `gate_score` | Gate 分数（见 R7-02） |
| `gate_grade` | Gate 等级（A/B/C/D） |
| `failed_checks` | 失败检查项列表，含检查项 ID、名称、权重级别（severity）、失败详情 |
| `rollback_nodes` | 回退节点列表，含节点 ID、名称、回退原因、回退范围、是否共享节点 |
| `rollback_nodes[].rollback_scope` | 回退范围：full（整节点回退）/ partial（部分回退） |
| `rollback_nodes[].shared_node` | 是否为共享节点（多个检查项依赖） |
| `preserved_nodes` | 保留不回退的节点列表及保留原因 |
| `rollback_strategy` | 回退策略：minimal（最小回退）/ full_phase（全量回退，仅当失败波及整个 Phase 时） |
| `estimated_resource_saving` | 相比全量回退的资源节省估算百分比 |

## v3 补充检查维度

### I01 迭代深化检查
- 至少 2 轮迭代
- P0/P1 缺口全部闭合或标注
- 每轮补研结果已追加到 NRSF-Full
- 详见 checks/I01_check.yml

### Checkpoint 原子写入检查
- 临时文件存在且非空
- 包含正确的 § 节标记
- 字数达到最小要求
- 原子 rename 完成
- 详见 checks/checkpoint_check.yml

### Gate 门控检查（仅终局 Gate）

根据 §0 规则，仅终局 Gate 分配 Supervisor Check，过程 Gate（Gate-α/Gate-β/Gate-γ）不在此列。

- **Gate-终 (T28)**：最终门控检查 → 详见 `checks/T28_gate_final_check.yml`
- **Gate-δ (T_gate_delta)**：增量门控检查 → 详见 `checks/T_gate_delta_check.yml`

### 跨模型审计（强制）

> 借鉴 Yang's cross-agent-audit 方法论。跨模型审计已从「可选增强」升级为「强制」环节，详见下文「跨模型审计（R7-03）」章节。

- 终局 Gate（Gate-终、Gate-δ）：强制双模型独立审计
- 过程 Gate（Gate-α/β/γ）：强制 10% 抽样跨模型复查
- 各模型独立产出 verdict，交叉对比以发现单一模型审查盲点
- 对分歧 verdict 进行第三模型裁定或人工介入
- 未执行跨模型审计的终局 Gate 不得判定为最终 PASS

## Phase 迭代循环（v3 新增）

### 触发条件
每个 Phase（1/2/3/4/7）内全部节点执行完毕后，Supervisor 对 Phase 整体输出进行质量评估。

### 迭代规则
1. 不达标 → 自动回到该 Phase 起点重新执行全部节点
2. 穷尽重试，不设重试上限，质量驱动终止
3. 持续重试直至达标，不阻塞后续 Phase
4. 达标 → 进入下一 Phase

### 质量评估标准
- 首轮：按各节点 Supervisor Check 的 PASS/RETRYING 判定汇总
- 重试轮：仅检查上一轮 RETRYING 项是否已修正

### 注意
- 过程 Gate（Gate-α/β/γ）的判定结果不触发 Phase 迭代——Phase 迭代由 Supervisor 独立触发
- 终局 Gate（Gate-终/δ）的 RETRYING 也触发 Phase 5 迭代

## Expected Free Energy 决策调度（v3 新增）

> **能力卡**: MC-182 ActiveInference

Supervisor 在 Phase 级质量评估中，引入 Expected Free Energy（EFE）作为决策调度的参考维度：

### EFE 计算公式

```
G(π) = -E_Q[ln P(o|s)] + D_KL[Q(s|π) || P(s)]
     = -信息增益(epistemic value) + 风险(pragmatic value)
```

### EFE 在调度决策中的应用

| 调度场景 | EFE 应用 |
|---------|---------|
| 是否进入下一 Phase | EFE > 0（预期信息增益为正）→ 继续；EFE ≤ 0 → 考虑终止 |
| 是否触发 Phase 迭代 | EFE 高 → 重试可能带来显著认知收益；EFE 低 → 继续穷尽重试直至达标 |
| 资源分配优先级 | 按各 Phase EFE 降序分配计算资源，高 EFE Phase 获得优先调度 |
| 搜索深度决策 | EFE 参与 Info-Decay 模型的终止判定，两者同时满足才终止 |

### 与 Phase 迭代循环的协同

```
Phase 完成后:
1. 检查质量评估标准（PASS/RETRYING）
2. 计算该 Phase 的 EFE
3. 若 RETRYING 且 EFE > 阈值（默认 0.1）→ 触发 Phase 迭代重试
4. 若 RETRYING 且 EFE ≤ 阈值 → 继续穷尽重试直至达标（不设重试上限）
5. 若 PASS 且 EFE > 阈值 → 继续下一 Phase
6. 若 PASS 且 EFE ≤ 阈值 → 继续下一 Phase（但标注 low_efe_risk）
```

## Orchestrator 评分外部验证（R7-04）

> **目的**：Orchestrator 在 Gate 节点执行九层覆盖度评估、层间一致性分析等门控检查时，会产出结构化评分。本机制通过金标准对照、人工抽样、跨模型独立评分三重外部验证，对冲 Orchestrator 单点评分的系统性偏差，确保评分结果可信赖。本章节为新增章节，不修改既有内容。

### 金标准一致性验证

Orchestrator 评分须与人工标注的金标准报告集（见 `docs/gold-standard-reports.md`）保持一致。

| 验证项 | 规则 |
|--------|------|
| 金标准集规模 | 20 个报告（10 HIGH + 10 LOW） |
| 一致性指标 | Pearson 相关系数 r |
| 通过阈值 | **r ≥ 0.7** |
| 验证频率 | 每次 Orchestrator 评分模型变更或季度复核时执行 |
| 验证流程 | Orchestrator 对 20 个金标准报告产出自动评分 → 与人工金标准评分（HIGH=5, LOW=1）计算相关系数 → r < 0.7 触发评分校准 |

**评分维度**：Orchestrator 评分覆盖以下 5 个维度，每维 0-5 分，合计 0-25 分：

1. 字数充分性（word_count 是否达地板）
2. 维度覆盖度（coverage_dimensions / 14）
3. 证据充分性（evidence_count + counter_evidence_count）
4. 信息密度（information_density 分级）
5. 结构完整性（chapter_count + gate_pass_status + has_philosophical_core + has_scientific_layer）

### 10% 人工抽样验证机制

除金标准全量验证外，对 Orchestrator 产出的每批次评分执行 10% 随机抽样人工复核：

| 抽样项 | 规则 |
|--------|------|
| 抽样率 | 10%（每 10 个 Orchestrator 评分随机抽取 1 个） |
| 抽样方式 | 随机抽样，覆盖各 Phase 的 Gate 节点评分 |
| 复核员 | 人工标注员独立复核，不可见 Orchestrator 原始评分 |
| 偏差阈值 | |S_orchestrator - S_human| > 1 分 → 标记为偏差样本 |
| 偏差率阈值 | 抽样偏差率 > 20% → 触发全量复核 + 评分校准 |
| 记录方式 | 抽样结果写入 `execution_ledger.orchestrator_score_audit` |

**抽样日志格式**：

```yaml
orchestrator_score_audit:
  batch_id: "batch-2026Q2-001"
  total_scores: 50
  sampled_count: 5
  samples:
    - report_id: "R-2026-001"
      orchestrator_score: 4.2
      human_score: 4.0
      delta: 0.2
      verdict: "consistent"
    - report_id: "R-2026-007"
      orchestrator_score: 3.8
      human_score: 2.5
      delta: 1.3
      verdict: "deviation"
  deviation_count: 1
  deviation_rate: 0.2
  action: "none"  # 或 "trigger_calibration"
```

### 跨模型评分机制

为对冲单一模型的评分偏差，Orchestrator 评分须由 2 个架构异构的模型独立评分后取平均：

| 跨模型项 | 规则 |
|---------|------|
| 模型数量 | 2 个（架构异构，遵循跨模型审计模型选择规则） |
| 独立性 | 两模型互不可见对方评分，独立判定 |
| 聚合方式 | 算术平均：S_cross = (S_A + S_B) / 2 |
| 分歧阈值 | |S_A - S_B| > 2 分 → 触发第三模型裁定 |
| 第三模型裁定 | 第三模型独立评分 S_C，最终分 = (S_cross + S_C) / 2 |
| 模型选择 | 遵循跨模型审计（R7-03）的模型选择规则，禁止同系列模型互评 |

**跨模型评分日志格式**：

```yaml
cross_model_scoring:
  report_id: "R-2026-001"
  model_a: "claude-3.5"
  model_b: "gpt-4"
  score_a: 4.2
  score_b: 4.0
  cross_score: 4.1
  divergence: 0.2
  tiebreaker_needed: false
  tiebreaker_model: null
  tiebreaker_score: null
  final_score: 4.1
```

### 评分校准触发条件

当满足以下任一条件时，触发 Orchestrator 评分校准：

| 触发条件 | 阈值 | 校准动作 |
|---------|------|---------|
| 金标准偏差 | 任一金标准报告 \|S_orchestrator - S_gold\| > **1 分** | 标记偏差样本，重新校准评分模型权重 |
| 金标准相关系数 | r < 0.7 | 全量重新校准，暂停自动评分直至 r ≥ 0.7 |
| 人工抽样偏差率 | 抽样偏差率 > 20% | 触发全量复核 + 评分校准 |
| 跨模型分歧 | \|S_A - S_B\| > 2 分 | 触发第三模型裁定，记录分歧原因 |
| 连续偏差 | 连续 3 个批次抽样偏差率 > 10% | 强制校准 + 暂停自动评分 |

**校准流程**：

```
1. 检测到校准触发条件 → 记录 calibration_event
2. 暂停 Orchestrator 自动评分（若触发条件为 r < 0.7 或连续偏差）
3. 使用金标准集重新拟合评分权重
4. 重新计算相关系数 r，直至 r ≥ 0.7
5. 恢复自动评分，记录校准日志
```

**校准日志格式**：

```yaml
calibration_event:
  event_id: "CAL-2026-001"
  trigger: "gold_standard_deviation"  # 或 "low_correlation" / "high_sample_deviation" / "cross_model_divergence" / "consecutive_deviation"
  trigger_detail: "GSR-07 |4.8 - 3.2| = 1.6 > 1.0"
  timestamp: "ISO 8601"
  action: "recalibrate_weights"
  pre_calibration_r: 0.65
  post_calibration_r: 0.78
  status: "resolved"  # 或 "in_progress"
```

## 双 Supervisor 机制（R7-06）

> **目的**：对 CRITICAL 路径节点（`critical_path: true`）引入双 Supervisor 独立检查机制，通过两个 Supervisor 独立验收对冲单 Supervisor 系统性偏差。本机制是「跨模型审计（R7-03）」的补充——R7-03 面向 Gate 节点，R7-06 面向非 Gate 的 CRITICAL 路径节点。
> **配套**：`docs/supervisor-coverage-matrix.md`（标注各节点 `critical_path` 属性）

### 适用范围

双 Supervisor 机制仅适用于 **CRITICAL 路径节点**（非 Gate 节点）。Gate 节点的双模型审计由 R7-03 负责，不在此机制覆盖范围内。

| 节点类别 | 是否 CRITICAL 路径 | 机制 |
|---------|-------------------|------|
| Gate-终/Gate-δ（终局 Gate） | — | R7-03 跨模型审计（强制双模型） |
| Gate-α/β/γ（过程 Gate） | — | R7-03 抽样跨模型审计（10%） |
| 非 Gate 节点 + `critical_path: true` | 是 | **R7-06 双 Supervisor 机制（本节）** |
| 非 Gate 节点 + `critical_path: false` | 否 | 单 Supervisor 检查 |

> CRITICAL 路径节点清单详见 `docs/supervisor-coverage-matrix.md` §1.1 完整清单中 `critical_path: true` 的条目（约 30+ 个节点）。

### 双 Supervisor 独立检查流程

```
CRITICAL 路径节点产出完成
  ↓
Step 1: 主 Supervisor（Primary）执行完整验收清单检查
  → 产出 primary_verdict
  ↓
Step 2: 辅 Supervisor（Secondary）独立执行同一验收清单检查
  → 辅 Supervisor 仅可见 Sub-Agent 产出，不可见 primary_verdict
  → 产出 secondary_verdict
  ↓
Step 3: 共识裁定
  → 两 verdict 均为 PASS → consensus=true，最终 PASS
  → 任一 verdict 为 RETRYING → 触发分歧裁定
  → 两 verdict 均为 RETRYING → 合并失败项，直接 RETRYING
```

### 分歧裁定机制

| 分歧类型 | 裁定方式 |
|---------|---------|
| 一 PASS 一 RETRYING | 触发仲裁 Supervisor（第三 Supervisor）独立复查，给出 tiebreaker_verdict |
| 两 Supervisor 均 RETRYING 但失败项不同 | 合并失败项，直接 RETRYING（无需第三 Supervisor） |
| 第三 Supervisor 仍分歧 | 转人工介入，记录分歧原因 |

### 双 Supervisor 选择规则

双 Supervisor 机制中的「双」要求两个 Supervisor 使用**不同基座模型**，禁止同系列模型互审（与 R7-03 模型选择规则一致）：

| 允许组合（示例） | 禁止组合（示例） |
|---------------|---------------|
| Claude × GPT-4 | Claude 3.5 × Claude 3（同系列） |
| Claude × Gemini | GPT-4 × GPT-4o（同系列） |
| GPT-4 × Gemini | Gemini 1.5 × Gemini 2.0（同系列） |

### 与 R7-03 的关系

| 维度 | R7-03 跨模型审计 | R7-06 双 Supervisor 机制 |
|------|-----------------|------------------------|
| 适用节点 | Gate 节点（终局/过程） | 非 Gate 的 CRITICAL 路径节点 |
| 触发方式 | 终局 Gate 强制全量；过程 Gate 10% 抽样 | CRITICAL 路径节点强制全量 |
| 检查者 | 跨模型（主模型 + 辅模型） | 双 Supervisor（不同基座模型） |
| 分歧裁定 | 第三模型裁定 | 仲裁 Supervisor（第三 Supervisor）裁定 |
| 成本控制 | 终局全量 + 过程抽样 | 仅 CRITICAL 路径节点全量（约 30+ 节点） |

### 双 Supervisor 日志格式

每次双 Supervisor 检查记录写入 `execution_ledger.dual_supervisor_audit`：

```yaml
dual_supervisor_audit:
  node_id: "T02"
  node_name: "研究底座"
  critical_path: true
  primary_supervisor_model: "claude-3.5"
  secondary_supervisor_model: "gpt-4"
  primary_verdict: "PASS"
  secondary_verdict: "PASS"
  consensus: true
  tiebreaker_needed: false
  tiebreaker_supervisor_model: null
  tiebreaker_verdict: null
  failed_checks_primary: []
  failed_checks_secondary: []
  timestamp: "ISO 8601"
```

### 成本控制策略

双 Supervisor 机制仅覆盖 CRITICAL 路径节点（约 30+ 个），非 CRITICAL 路径节点维持单 Supervisor 检查。设计原则：
- CRITICAL 路径节点全量双 Supervisor：节点少但关键，全量双检成本可控且收益最高
- 非 CRITICAL 路径节点单 Supervisor：节点多，全量双检成本不可控，单检已足够
- 若双 Supervisor 分歧率持续偏高（>20%），可临时将双检范围扩展到非 CRITICAL 路径节点

## EFE 决策调度阈值校准机制（R7-07）

> **目的**：为「Expected Free Energy 决策调度」中的 EFE 阈值（默认 0.1）建立动态校准机制，避免阈值固化导致的调度失准。本机制是 EFE 决策调度的配套校准层。
> **前置**：EFE 决策调度章节（见上文「Expected Free Energy 决策调度」）

### 阈值校准的必要性

EFE 决策调度当前使用固定阈值 0.1 判定「是否触发 Phase 迭代重试」。固定阈值存在以下风险：
- 阈值过高：低 EFE Phase 被错误触发重试，浪费计算资源
- 阈值过低：高 EFE Phase 被错误跳过重试，错失认知收益
- 不同研究主题的 EFE 分布不同，固定阈值无法适配所有场景

### 校准数据源

| 数据源 | 用途 | 采集方式 |
|--------|------|---------|
| `execution_ledger.retry_history` | 历史重试成功率与 EFE 值的关联分析 | 每次重试自动记录 |
| `execution_ledger.cross_model_audit` | 跨模型审计分歧率与 EFE 值的关联 | 每次审计自动记录 |
| `execution_ledger.dual_supervisor_audit` | 双 Supervisor 分歧率与 EFE 值的关联 | 每次双检自动记录 |
| `execution_telemetry.phase_efe_history` | 各 Phase 历史 EFE 值分布 | 每次 Phase 完成自动记录 |

### 校准周期

| 校准类型 | 频率 | 触发条件 |
|---------|------|---------|
| 定期校准 | 每 50 次 Phase 完成后 | 自动触发 |
| 偏差触发校准 | 实时 | EFE 阈值判定结果与实际质量评估偏差率 > 30% |
| 人工触发校准 | 按需 | 人工审计发现调度异常 |

### 校准算法

```
Step 1: 收集最近 N 次 Phase 完成的 EFE 值与质量评估结果
  - N = 50（最近 50 次 Phase 完成）
  - 数据对: (efe_value, actual_quality_pass)

Step 2: 计算 EFE 阈值的 ROC 曲线
  - 遍历候选阈值 [0.05, 0.08, 0.10, 0.12, 0.15, 0.20]
  - 对每个阈值计算:
    * true_positive = EFE > 阈值 且 实际重试有收益 的次数
    * false_positive = EFE > 阈值 但 实际重试无收益 的次数
    * true_negative = EFE ≤ 阈值 且 实际不重试正确 的次数
    * false_negative = EFE ≤ 阈值 但 实际应重试 的次数

Step 3: 选择最优阈值
  - 最优阈值 = argmax(F1_score) = argmax(2·P·R / (P+R))
  - Precision P = TP / (TP + FP)
  - Recall R = TP / (TP + FN)

Step 4: 平滑更新
  - new_threshold = 0.7 × old_threshold + 0.3 × optimal_threshold
  - 平滑因子 0.3 避免阈值剧烈波动

Step 5: 记录校准日志
```

### 阈值边界约束

| 约束 | 规则 | 理由 |
|------|------|------|
| 下限 | 阈值 ≥ 0.05 | 低于 0.05 时几乎所有 Phase 都触发重试，失去筛选意义 |
| 上限 | 阈值 ≤ 0.25 | 高于 0.25 时几乎无 Phase 触发重试，丧失穷尽重试能力 |
| 变动率 | 单次校准变动 ≤ 50% | 避免阈值剧烈波动导致调度行为不稳定 |

### 校准日志格式

```yaml
efe_calibration_event:
  event_id: "EFE-CAL-2026-001"
  trigger: "periodic"  # 或 "deviation" / "manual"
  trigger_detail: "定期校准（第 50 次 Phase 完成后）"
  timestamp: "ISO 8601"
  data_points: 50
  old_threshold: 0.10
  optimal_threshold: 0.13
  new_threshold: 0.109  # 0.7×0.10 + 0.3×0.13
  roc_metrics:
    precision: 0.82
    recall: 0.75
    f1_score: 0.78
  boundary_check: "PASS"  # 0.05 ≤ 0.109 ≤ 0.25
  status: "resolved"
```

### 与 Phase 迭代循环的协同

```
Phase 完成后:
1. 检查质量评估标准（PASS/RETRYING）
2. 计算该 Phase 的 EFE
3. 读取当前 EFE 阈值（由 R7-07 校准机制动态维护）
4. 若 RETRYING 且 EFE > 当前阈值 → 触发 Phase 迭代重试
5. 若 RETRYING 且 EFE ≤ 当前阈值 → 继续穷尽重试直至达标（不设重试上限）
6. 若 PASS 且 EFE > 当前阈值 → 继续下一 Phase
7. 若 PASS 且 EFE ≤ 当前阈值 → 继续下一 Phase（标注 low_efe_risk）
8. 每 50 次 Phase 完成后，触发 EFE 阈值校准
```

## 统一检查项量化标准（R7-08）

> **目的**：统一 supervisors/checks/ 目录下 61 个 check YAML 文件的 severity 命名，消除遗留值（HIGH/MEDIUM/ERROR/WARN/warning/INFO/LOW）与标准值（CRITICAL/MAJOR/MINOR）的混用问题。本机制是检查项治理的统一量化层。
> **配套**：`scripts/supervisor-check-tests.py`（自动化校验）、`docs/supervisor-coverage-matrix.md`（覆盖度矩阵）

### 标准三级 severity 体系

Supervisor 检查项统一采用以下三级 severity 体系，与「三级判定标准」和「Gate 检查项权重化（R7-02）」对齐：

| 标准值 | 含义 | 权重值（R7-02） | 处置规则 |
|--------|------|----------------|---------|
| **CRITICAL** | 核心硬性要求，违反则直接 RETRYING | 5 (blocking) | 任一 CRITICAL 项失败 → RETRYING |
| **MAJOR** | 影响输出质量的关键维度 | 3 (major) | MAJOR 项通过率 < 80% → RETRYING |
| **MINOR** | 格式与规范性问题 | 1 (minor) | MINOR 项通过率 < 60% → RETRYING |

### 遗留值到标准值的映射

历史版本的 check YAML 文件使用了多种遗留 severity 值，统一按以下映射表迁移至标准值：

| 遗留值 | 标准值 | 映射理由 |
|--------|--------|---------|
| HIGH | CRITICAL | HIGH 对应"高优先级"，语义等同于 CRITICAL |
| ERROR | CRITICAL | ERROR 对应"错误级别"，违反即拒，等同于 CRITICAL |
| MEDIUM | MAJOR | MEDIUM 对应"中优先级"，语义等同于 MAJOR |
| WARN | MAJOR | WARN 对应"警告级别"，影响质量但不阻塞，等同于 MAJOR |
| WARNING | MAJOR | WARNING 同 WARN |
| warning（小写） | MAJOR | 同 WARNING |
| INFO | MINOR | INFO 对应"信息级别"，仅提示不影响质量 |
| LOW | MINOR | LOW 对应"低优先级"，语义等同于 MINOR |
| blocking（R7-02） | CRITICAL | R7-02 权重化中的 blocking 等同于 CRITICAL |
| major（R7-02 小写） | MAJOR | R7-02 权重化中的 major 等同于 MAJOR |
| minor（R7-02 小写） | MINOR | R7-02 权重化中的 minor 等同于 MINOR |

### 字段名统一

历史版本的 check YAML 文件使用了多种字段名变体，统一按以下映射表迁移：

| 字段 | 标准名 | 遗留别名 |
|------|--------|---------|
| 检查项标识 | `id` | `name` |
| 检查项描述 | `description` | `check`, `desc`, `rule`, `criterion` |
| 严重等级 | `severity` | `level` |
| 节点标识 | `task_id` | `check_id`, `gate_id`, `node_id`, `node` |
| 节点引用 | `task_file` | `task_name`, `protocol_ref`, `schema_file` |

### 迁移策略

迁移采用渐进式策略，不破坏现有 check YAML 文件的可用性：

| 阶段 | 动作 | 时间 |
|------|------|------|
| 阶段 1：兼容期 | `supervisor-check-tests.py` 同时接受标准值与遗留值（当前已实现） | 即日起 |
| 阶段 2：迁移期 | 逐批将遗留值修改为标准值，每次修改后运行测试脚本验证 | 30 天内 |
| 阶段 3：强制期 | `supervisor-check-tests.py` 仅接受标准值，遗留值判定为 FAIL | 60 天后 |

### 文件级 severity 与检查项级 severity 的关系

部分 check YAML 文件使用文件级 severity（如 `T07b_check.yml` 的 `severity: MEDIUM`），作为该文件内所有检查项的默认 severity。统一规则如下：

| 场景 | 规则 |
|------|------|
| 检查项有 severity | 使用检查项自身的 severity（优先级最高） |
| 检查项无 severity，文件有 severity | 继承文件级 severity |
| 检查项无 severity，文件无 severity | 标记为 `severity: MINOR`（最宽松默认值），建议补充 |

### 量化标准与 R7-02 权重化的对齐

统一量化标准与 R7-02 Gate 检查项权重化完全对齐：

| 标准值 | R7-02 权重级别 | 权重值 | 通过条件 |
|--------|---------------|--------|---------|
| CRITICAL | blocking | 5 | 100% 通过 |
| MAJOR | major | 3 | ≥ 80% 通过 |
| MINOR | minor | 1 | ≥ 60% 通过 |

> Supervisor Check 与 Gate Check 使用同一套三级 severity 体系，确保全流程质量评估的一致性。

### 自动化校验

`scripts/supervisor-check-tests.py` 的 T4 测试项负责校验 severity 枚举值。在兼容期（阶段 1），T4 接受标准值与遗留值；在强制期（阶段 3），T4 仅接受标准值（CRITICAL/MAJOR/MINOR）。

校验命令：
```bash
python scripts/supervisor-check-tests.py
```

预期输出（兼容期）：
```
[✓] T4 severity 枚举值: PASS
    全部 severity 值合法（['CRITICAL', 'MAJOR', 'MINOR', ...遗留值]）
```

预期输出（强制期）：
```
[✓] T4 severity 枚举值: PASS
    全部 severity 值合法（['CRITICAL', 'MAJOR', 'MINOR']）
```