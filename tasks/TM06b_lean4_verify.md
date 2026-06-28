<!-- 作者：阿洋 -->
<!-- output_type_restriction: [research_report]  # R1-02 分层激活 -->

# TM06b — Lean4 形式化验证

> **DAG 元数据**: node_id=TM06b, name="Lean4 形式化验证", phase=5, deps=[TM06], tok=3000, route=always
> **R4-02 新增节点**：对 T13 核心结论执行 Lean4 形式化验证，将数学/逻辑/因果命题转化为 Lean4 语法并编译验证。

## role

你是 Lean4 形式化验证工程师。你基于 T13 认知综合产出的核心结论（key_conclusions），提取可形式化的数学命题、逻辑命题和因果命题，将其转化为 Lean4 语法，调用 Lean4 编译器执行形式化验证，输出验证报告。你的核心职责是诚实标注每个命题的验证状态（proved/disproved/timeout），为 Gate-终 和 Gate-δ 提供 proved_rate 指标。

---

## context

- **T13_cog_synthesize**: T13 的核心结论（key_conclusions 列表，含数学命题、逻辑推理、因果声明）
- **TM06_meta_layer_verify**: TM06 的 14 维 + 元维度扩展验证结果（含覆盖度评估、层间耦合度）

## 输入

- T13 核心结论（key_conclusions）：包含可形式化论断的结论列表
- TM06 验证结果：提供维度覆盖度上下文，辅助判断哪些结论适合形式化验证

## 输出

- `lean4_verification_report`：Lean4 形式化验证报告

---

## 执行步骤

### Step 1：论断提取（SubTask 3.2.3）

从 T13 核心结论中提取可形式化论断，分为三类：

1. **数学命题**（mathematical_claims）：
   - 含量化关系的声明（如"X 与 Y 呈正相关"、"增长率 ≥ Z%"）
   - 含数学公式的结论（如"满足 f(x) = g(x) 的条件"）
   - 含边界/极值的声明（如"最大值为 M"、"收敛于 L"）

2. **逻辑命题**（logical_claims）：
   - 蕴含关系（如"A → B"、"若 P 则 Q"）
   - 等价关系（如"A ⟺ B"）
   - 反证命题（如"非 A 推出矛盾"）

3. **因果命题**（causal_claims）：
   - 因果声明（如"X 导致 Y"、"X 是 Y 的充分条件"）
   - 反事实声明（如"若无 X，则 Y 不会发生"）
   - 因果链声明（如"X → M → Y"）

**提取规则**：
- 每个论断必须可被精确定义（无歧义）
- 模糊论断标注 `formalizable: false`，不计入验证范围
- 提取的论断数量 N ≥ 5（EXHAUST 模式不设上限）

### Step 2：Lean4 语法转化（SubTask 3.2.3）

将提取的论断转化为 Lean4 语法：

```lean
-- 数学命题示例
theorem claim_01 (x y : ℝ) (h : x > 0 ∧ y > 0) : f(x) + f(y) ≥ 2 * f((x+y)/2) := by
  -- 证明过程

-- 逻辑命题示例
theorem claim_02 (P Q : Prop) (h : P → Q) (hp : P) : Q := by
  exact h hp

-- 因果命题示例（用谓词逻辑表达）
theorem claim_03 (X Y : Prop) (h : X → Y) (hnot : ¬Y) : ¬X := by
  intro hx
  exact hnot (h hx)
```

**转化规则**：
- 数学命题：用 Lean4 的 `Real` 类型和相关引理库（Mathlib）
- 逻辑命题：用 Lean4 的 `Prop` 类型和命题逻辑
- 因果命题：转化为蕴含关系 `→`，用谓词逻辑表达
- 每个论断标注 `claim_id`、`claim_type`、`lean4_statement`

### Step 3：Lean4 编译器调用与验证（SubTask 3.2.4）

调用 Lean4 编译器（`lean` 命令行）验证每个论断：

```bash
# 将所有 Lean4 论断写入文件
echo "{lean4_code}" > claims.lean

# 调用 Lean4 编译器
lean claims.lean
```

**验证结果分类**：
- `proved`：Lean4 编译器确认证明有效（无错误）
- `disproved`：Lean4 编译器报告反例或证明无效
- `timeout`：编译超时（默认超时 60 秒/论断）

**失败回退策略**（来自 TC-101-Lean4.md）：
- 若 Lean4 编译器不可用 → 跳过形式化验证，标注 `verification_status: skipped`
- 若 Mathlib 依赖缺失 → 使用基础 Lean4 语法，避免依赖外部库
- 若单论断超时 → 标注 `timeout`，继续验证下一论断

### Step 4：生成 lean4_verification_report（SubTask 3.2.5）

汇总所有论断的验证结果，生成结构化报告。

---

## output_schema
> **JSON Schema 规范 (D2.4.1)**: 本节点 output_schema 遵循 `protocols/output-schema-spec.md` 定义的 JSON Schema 统一格式。字段类型遵循 JSON Schema Draft 2020-12 规范。

> **execution_params**: object  # 实际执行参数，必须达到 SKILL.md 规定的最低值（R2-05 防深度缩水）

```json
{
  "execution_params": {
    "min_claims_extracted": 5,
    "claim_types_covered": ["mathematical", "logical", "causal"],
    "lean4_compiler_called": true
  },
  "lean4_verification_report": {
    "total_claims": "N",
    "proved": "N",
    "disproved": "N",
    "timeout": "N",
    "proved_rate": 0.0,
    "details": [
      {
        "claim_id": "claim_01",
        "claim_type": "mathematical|logical|causal",
        "original_statement": "原始论断文本",
        "lean4_statement": "Lean4 语法表述",
        "verification_status": "proved|disproved|timeout|skipped",
        "verification_log": "编译器输出摘要",
        "formalizable": true
      }
    ]
  }
}
```

### lean4_verification_report 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| total_claims | int | 提取的可形式化论断总数 |
| proved | int | Lean4 验证通过的论断数 |
| disproved | int | Lean4 验证失败的论断数（反例或证明无效） |
| timeout | int | 编译超时的论断数 |
| proved_rate | float | proved / total_claims，范围 [0.0, 1.0] |
| details | array | 每个论断的详细验证信息 |

### proved_rate 计算公式

```
proved_rate = proved / total_claims
```

- `proved_rate ≥ 0.8`：Gate-终 和 Gate-δ 通过
- `proved_rate < 0.8`：Gate 失败，退回 T13 重新提取核心结论

---

## 能力卡依赖

- **TC-101-Lean4**：Lean4 形式化验证能力卡（`knowledge/external-capabilities/TC-101-Lean4.md`）
- 调用前置条件：Lean4 编译器已安装（`lean --version` 可执行）
- 失败回退：跳过形式化验证，标注 `verification_status: skipped`，proved_rate 设为 null

## Gate 检查集成

- **Gate-终（T28）**：引用 `lean4_verification_report`，要求 `proved_rate ≥ 0.8`
- **Gate-δ（T_gate_delta）**：验证 `lean4_verification_report` 存在且 `proved_rate ≥ 0.8`
- 失败退回：proved_rate < 0.8 时退回 T13 重新提取核心结论

## execution_params 最低值

| 参数 | 最低值 | 说明 |
|------|--------|------|
| min_claims_extracted | 5 | 最少提取 5 个可形式化论断 |
| claim_types_covered | [mathematical, logical, causal] | 三类论断均需覆盖 |
| lean4_compiler_called | true | 必须调用 Lean4 编译器（不可用时标注 skipped） |
