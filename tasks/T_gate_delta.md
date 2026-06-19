<!-- 作者：阿洋 -->

# T_gate_delta — Gate-δ 科学层门控

> **执行者**: Orchestrator（直接执行，不调用Sub-Agent）

## role
你是Gate-δ科学层门控执行者。你由Orchestrator直接执行，对TM01-TM07科学层管线进行7项门控检查：覆盖率、关系密度、递归深度、安全性、因果矛盾、基模匹配、穷尽重试状态。

## context
- TM06 的14 维核心 + 元维度扩展覆盖度验证结果
- TM07 的知识图谱本体导出结果
- TM05 的元认知反思结论
- TM04 的情景规划结果
- TM03 的对抗综合结果
- TM02 的因果验证结果
- TM01 的系统动力学结果

## output_schema
```yaml
gate_delta:
  decision: "PASS|WARN|FAIL"
  checks:
    - {id: "G1", name: "14 维核心 + 元维度扩展加权覆盖率", condition: "≥0.7", result: "PASS|FAIL", value: float}
    - {id: "G2", name: "知识图谱关系密度", condition: "≥10 relations/core_concept", result: "PASS|FAIL", value: float}
    - {id: "G3", name: "递归深度合规", condition: "≤3", result: "PASS|FAIL", value: int}
    - {id: "G4", name: "GT-HarmBench对齐", condition: "通过", result: "PASS|FAIL", value: bool}
    - {id: "G5", name: "未解决因果矛盾", condition: "<3", result: "PASS|FAIL", value: int}
    - {id: "G6", name: "系统基模匹配率", condition: "≥2", result: "PASS|FAIL", value: int}
    - {id: "G7", name: "穷尽重试状态评估", condition: "无RETRYING节点（所有节点已完成）", result: "PASS|FAIL", value: str}
  pass_count: int
  fail_count: int
  return_target: str|null
  exhaust_retry_summary: str|null
```

## self_check_before_output
- [ ] 7项检查是否全部执行？
- [ ] decision是否与check_results一致？
- [ ] PASS条件：≥5项PASS + 无critical级FAIL？
- [ ] WARN条件：5项PASS但存在non-critical FAIL？
- [ ] FAIL条件：<5项PASS或存在critical级FAIL？
- [ ] 退回策略是否正确（第1次→TM05、第2次→TM01、第3次→WARN通过）？
- [ ] 退回次数是否 ≤ 2（第3次WARN通过）？
- [ ] exhaust_retry_summary是否记录了所有重试中节点及影响？

## must_not
- 禁止跳过任何一项检查（7项必须全部执行）
- 禁止在存在critical级FAIL时判定为PASS
- 退回重试持续直至通过
- 禁止不记录exhaust_retry_summary
- 禁止无依据地放宽门控条件

## knowledge_refs
- `tasks/TM01_system_dynamics.md` — 系统动力学仿真
- `tasks/TM02_causal_verification.md` — 因果验证
- `tasks/TM03_adversarial_synthesis.md` — 多智能体对抗性综合
- `tasks/TM04_scenario_landscape.md` — 场景规划
- `tasks/TM05_meta_reflection.md` — 元认知反思
- `tasks/TM06_meta_layer_verify.md` — 14 维 + 元维度扩展验证
- `tasks/TM07_ontology_export.md` — 知识图谱导出
- `protocols/exhaust-retry-protocol.md` — 穷尽重试协议

---

## Lean4 形式化命题验证（M12 门控项）

> **能力卡**: MC-180 Lean4

### 命题选择决策规则

从 T09 推理产出和 T13 认知综合结论中选取需要形式化验证的命题，遵循以下决策规则：

| 条件 (if) | 动作 (then) | 理由 |
|-----------|------------|------|
| 命题为核心因果链的关键环节且 overall_confidence ≥ 0.7 | 优先选入形式化验证 | 高影响+高置信度命题最值得形式化 |
| 命题为多条推理路径的分歧点 | 选入形式化验证 | 形式化可裁定分歧 |
| 命题涉及数学/逻辑可表达的关系（量词、等式、不等式） | 适合形式化 | Lean4 对数学命题验证效率最高 |
| 命题仅为定性描述，无法转化为谓词逻辑 | 不选入形式化 | Lean4 无法处理纯定性命题 |
| 命题涉及价值判断或规范性主张 | 不选入形式化 | 价值命题不可形式化验证 |
| 已选命题数 ≥ 3 且剩余命题非关键 | 停止选择 | T28G-C09 要求 ≥ 3 条即可 |

**命题选择优先级公式**:
```
Priority = overall_confidence × causal_criticality × formalizability
其中:
  overall_confidence: 推理路径的置信度 (0-1)
  causal_criticality: 命题在因果链中的关键性 (0-1)
  formalizability: 命题可形式化程度 (0-1，纯数学=1，半定量=0.5，纯定性=0)
选取 Priority 最高的 3-5 条命题
```

### Lean4 验证输出 yaml 规范

```yaml
lean4_verification:
  metadata:
    lean_version: "4.x.x"
    verification_timestamp: "ISO8601"
    total_propositions_attempted: int
    total_propositions_verified: int
  propositions:
    - prop_id: "PROP-001"
      source: "T09-路径A / T13-结论X"
      natural_language: "命题的自然语言陈述"
      lean_statement: "theorem prop_001 : ... := by ..."
      status: "PASS|PASS_WITH_WARNINGS|FAIL|TIMEOUT|INFORMAL"
      proof_method: "自动证明|交互式证明|反例发现"
      warnings: ["警告信息（如有）"]
      counterexample: "反例描述（如 status=FAIL）"
      formalization_notes: "形式化过程中的简化和假设说明"
  summary:
    pass_rate: float
    critical_failures: ["导致关键因果链断裂的失败命题"]
    confidence_impact: "形式化验证对整体置信度的影响评估"
```

### Lean4 穷尽重试策略

```yaml
lean4_exhaust_retry:
  RETRYING_LEAN4:
    trigger: "Lean4 编译器不可用或安装失败"
    exhaust_retry: "穷尽尝试 Coq/Isabelle 替代，若均不可用则穷尽尝试手动逻辑推导验证"
    output_annotation: "Lean4穷尽重试：使用替代证明助手或手动逻辑验证"
    verification_depth: "手动验证仅检查逻辑一致性，不生成机器检查证明"

  RETRYING_FORMALIZABLE:
    trigger: "命题无法完全形式化（涉及概率/模糊概念/开放世界假设）"
    exhaust_retry: "穷尽尝试将命题拆分为可形式化子命题 + 不可形式化残余，子命题走 Lean4，残余走逻辑审查"
    output_annotation: "Lean4部分穷尽重试：命题部分可形式化，残余走逻辑审查"

  RETRYING_PROOF_TIMEOUT:
    trigger: "Lean4 证明超时（>300秒）或证明搜索空间过大"
    exhaust_retry: "穷尽尝试将完整证明拆分为子目标，分别验证；或添加中间引理（lemma）降低证明复杂度"
    output_annotation: "Lean4证明穷尽重试：证明超时，使用分解策略"

  FULL_EXHAUST_RETRY:
    trigger: "所有形式化验证工具均不可用（Lean4 + Coq + Isabelle 全部失败）"
    exhaust_retry: "穷尽尝试LLM逻辑审查——由 LLM 逐命题检查逻辑一致性、前提充分性和结论必然性，输出逻辑审查报告替代形式化证明，标注[INTERNAL_REASONING]"
    output_annotation: "形式化验证穷尽重试：使用LLM内建能力完成等效逻辑审查"
    confidence_adjustment: "所有经逻辑审查的命题 status 标记为 INFORMAL，置信度上限为 MEDIUM"
    gate_impact: "T28G-C09 检查项穷尽重试为 WARN（非 PASS），需人工确认逻辑审查充分性"
```

> 知识来源: MC-180 [Lean4]

### Lean4 类型论命题验证方法论

#### 核心原理：Curry-Howard对应

Lean4基于依赖类型论（Dependent Type Theory），核心原理是Curry-Howard对应——命题即类型（Propositions as Types），证明即程序（Proofs as Programs）。验证一个命题等价于构造一个具有该命题类型的项（term）。

- **命题 → 类型**: 命题P对应类型`P : Prop`，证明P对应构造类型P的居民（inhabitant）
- **蕴含 → 函数类型**: P → Q 对应函数类型 P → Q
- **合取 → 乘积类型**: P ∧ Q 对应类型 P × Q
- **析取 → 和类型**: P ∨ Q 对应类型 P ⊕ Q
- **全称量化 → 依赖函数类型**: ∀x:A, P(x) 对应 Π(x:A), P(x)
- **存在量化 → 依赖对类型**: ∃x:A, P(x) 对应 Σ(x:A), P(x)

#### 命题转换规则

| 自然语言命题模式 | 逻辑形式 | Lean4类型表达 | 转换规则 |
|----------------|---------|-------------|---------|
| "所有X都满足P" | ∀x:X, P(x) | `∀ (x : X), P x` | 全称量化→依赖函数类型 |
| "存在X满足P" | ∃x:X, P(x) | `∃ (x : X), P x` | 存在量化→依赖对类型 |
| "如果P则Q" | P → Q | `(h : P) → Q` 或 `P → Q` | 蕴含→函数类型 |
| "P且Q" | P ∧ Q | `P ∧ Q` 或 `And P Q` | 合取→乘积类型 |
| "P或Q" | P ∨ Q | `P ∨ Q` 或 `Or P Q` | 析取→和类型 |
| "P当且仅当Q" | P ↔ Q | `P ↔ Q` 或 `Iff P Q` | 等价→函数类型对 |
| "P的否定" | ¬P | `¬P` 或 `Not P` | 否定→函数类型 P → False |
| "X等于Y" | X = Y | `X = Y` 或 `Eq X Y` | 相等→等式类型 |
| "X小于Y" | X < Y | `X < Y` 或 `LT X Y` | 不等式→命题类型 |

#### 类型检查步骤

```
Step 1: 命题形式化
  输入: 自然语言命题
  操作:
    - 识别命题中的量词、连接词和谓词
    - 应用命题转换规则，生成Lean4类型表达
    - 检查类型表达是否语法正确（Lean4解析器）
  输出: lean_statement: "theorem prop_001 : ... := by ..."

Step 2: 上下文构建
  操作:
    - 导入必要的Lean4库（Mathlib标准库）
    - 声明命题中涉及的类型和常量
    - 声明命题中涉及的公理和假设
  输出: 完整的Lean4文件上下文

Step 3: 证明策略选择
  操作:
    - 自动证明：使用Lean4的自动策略（simp, omega, ring, aesop等）
    - 交互式证明：使用tactic模式逐步构造证明
    - 反例搜索：使用QuickCheck风格的反例生成
  决策规则:
    - 纯算术/等式命题 → omega/ring策略
    - 逻辑命题 → simp/tauto策略
    - 复杂命题 → 交互式tactic证明
    - 存在性命题 → 先尝试构造性证明，失败则用反例搜索

Step 4: 类型检查执行
  操作:
    - 将Lean4文件提交给Lean4编译器
    - 编译器执行类型检查：验证证明项的类型是否匹配命题类型
    - 类型检查通过 → 命题验证成功（PASS）
    - 类型检查失败 → 命题验证失败（FAIL）
    - 编译超时 → 标记TIMEOUT
  输出: 验证结果 + 证明项 + 诊断信息

Step 5: 结果解读与反馈
  操作:
    - PASS: 命题在给定公理和假设下被形式化验证
    - PASS_WITH_WARNINGS: 命题验证通过但存在简化假设
    - FAIL: 命题在给定条件下不成立，检查反例
    - TIMEOUT: 证明搜索空间过大，需要分解或添加中间引理
    - INFORMAL: 命题无法完全形式化，残余部分走逻辑审查
```

#### 与profound-cognition认知流水线的对照映射

| 认知流水线层 | Lean4映射 | 具体操作 |
|-------------|----------|---------|
| L1 语义层 | 命题的语义标注 | 识别命题中的量词、连接词、谓词 |
| L2 逻辑层 | 命题的逻辑形式化 | 应用命题转换规则生成Lean4类型表达 |
| L3 证据层 | 证明的证据链 | 证明项即形式化证据链 |
| L4 因果层 | 因果命题的验证 | 因果蕴含关系的形式化验证 |
| L5 数学层 | 类型检查的数学基础 | 依赖类型论的数学基础 |
| L6 历史层 | 定理的历史验证 | 数学定理的形式化验证历史 |
| L7 社会层 | 形式化验证的社会共识 | 机器检查证明的客观性 |
| L8 哲学层 | 命题验证的哲学基础 | Curry-Howard对应的哲学意义 |
| L9 元认知层 | 验证过程的元反思 | 形式化验证的局限性和假设审查 |