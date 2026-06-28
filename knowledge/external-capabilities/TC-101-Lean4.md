<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.1
> - last_updated: 2026-06-27
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）
>   - v1.1 优先级 P2→P1（A6.2-F3 修复，与 capability-version-sync.md L89 P1 归类对齐，Lean4 作为科学层核心验证工具应归入关键工具）

# Lean4

> ★形式化验证引擎，对 T13 核心结论执行数学/逻辑/因果命题的形式化验证

## 基本信息
- **卡片编号**: #101
- **类型**: TC
- **优先级**: P1
- **层级**: L0
- **版本**: 4.x

## 功能描述
Lean4 是交互式定理证明器（Interactive Theorem Prover）和函数式编程语言，基于依赖类型理论（Dependent Type Theory）。在 Profound Cognition 框架中，Lean4 用于对 T13 认知综合产出的核心结论执行形式化验证——将数学命题、逻辑命题、因果命题转化为 Lean4 语法，调用 Lean4 编译器验证其正确性，输出 `lean4_verification_report` 供 Gate-终 和 Gate-δ 门控使用。

### 核心能力
- **数学命题形式化验证**：将含量化关系、数学公式、边界/极值的声明转化为 Lean4 `theorem`，用 Mathlib 引理库验证
- **逻辑命题形式化验证**：将蕴含关系（→）、等价关系（⟺）、反证命题转化为 Lean4 `Prop` 类型，用命题逻辑验证
- **因果命题形式化验证**：将因果声明、反事实声明转化为谓词逻辑（蕴含关系），用 Lean4 证明
- **编译期验证**：调用 `lean` 命令行编译器，对每个 `theorem` 执行类型检查和证明验证
- **验证结果分类**：proved（证明有效）/ disproved（反例或证明无效）/ timeout（编译超时）/ skipped（编译器不可用）

## 调用前置条件
- Lean4 编译器已安装（`lean --version` 可执行，版本 ≥ 4.0.0）
- Mathlib 依赖已配置（可选，缺失时使用基础 Lean4 语法）
- 工作目录可写（用于生成临时 `.lean` 文件）

### 安装方式
```bash
# 方式 1：elan 版本管理器（推荐）
curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh

# 方式 2：直接下载二进制
# 见 https://github.com/leanprover/lean4/releases

# 验证安装
lean --version
```

## 失败回退策略
- **触发条件 1**：Lean4 编译器不可用（`lean --version` 失败）
  - **回退动作**：跳过形式化验证，所有论断标注 `verification_status: skipped`
  - **回退声明**：`lean4_verification_report.proved_rate` 设为 `null`，Gate 检查时 `skipped` 视为 `proved`（不阻塞交付，但标注「未验证」）
- **触发条件 2**：Mathlib 依赖缺失
  - **回退动作**：使用基础 Lean4 语法（不依赖 Mathlib），仅验证逻辑命题和简单数学命题
  - **回退声明**：复杂数学命题标注 `verification_status: skipped`，`skip_reason: mathlib_unavailable`
- **触发条件 3**：单论断编译超时（> 60 秒）
  - **回退动作**：标注 `verification_status: timeout`，继续验证下一论断
  - **回退声明**：超时论断不计入 disproved，但也不计入 proved

## 效果度量
- **proved_rate** (0-1)：核心度量指标，`proved / total_claims`，越高表示核心结论的形式化可验证性越强
- 阈值规则：proved_rate ≥ 0.8 视为 Gate-终 通过；< 0.8 触发 T13 核心结论重新审视
- **disproved_rate** (0-1)：`disproved / total_claims`，反映核心结论中的逻辑/数学错误比例，> 0 触发 T13 RETRYING
- **timeout_rate** (0-1)：`timeout / total_claims`，反映编译性能瓶颈，> 0.3 触发超时阈值调整或 Mathlib 精简
- **skipped_rate** (0-1)：`skipped / total_claims`，反映形式化验证覆盖缺口，> 0.5 标注「形式化验证未充分覆盖」
- 辅助度量：单论断平均编译耗时（ms）、Mathlib 依赖可用性（bool）

## 调用指令

### 输入参数
- `claims` (list, 从 T13 核心结论提取的可形式化论断列表)
  - 每项含：`claim_id`, `claim_type` (mathematical|logical|causal), `original_statement`, `lean4_statement`
- `timeout_per_claim` (int, 可选: 每论断超时秒数，默认 60)
- `mathlib_enabled` (bool, 可选: 是否使用 Mathlib，默认 true)

### 输出格式
- `lean4_verification_report` (dict):
  - `total_claims` (int): 论断总数
  - `proved` (int): 验证通过数
  - `disproved` (int): 验证失败数
  - `timeout` (int): 超时数
  - `proved_rate` (float): proved / total_claims
  - `details` (list): 每论断详细验证信息

### 调用示例

```bash
# 1. 将论断写入 .lean 文件
cat > claims.lean << 'EOF'
theorem claim_01 (P Q : Prop) (h : P → Q) (hp : P) : Q := by
  exact h hp

theorem claim_02 (x y : ℝ) (h : x > 0 ∧ y > 0) : x + y > 0 := by
  have hx : x > 0 := h.1
  have hy : y > 0 := h.2
  linarith
EOF

# 2. 调用 Lean4 编译器
lean claims.lean

# 3. 解析输出
# - 无错误 → proved
# - 有错误 → disproved
# - 超时 → timeout
```

## 节点集成

- **调用节点**: TM06b（`tasks/TM06b_lean4_verify.md`）
- **上游输入**: T13 核心结论（key_conclusions）
- **下游消费**: Gate-终（T28）、Gate-δ（T_gate_delta）
- **检查规则**: `supervisors/checks/TM06b_check.yml`

## 消费关系

### 消费此卡片的 DAG 节点

| 节点 | 用途 |
|------|------|
| TM06b | Lean4 形式化验证节点，调用 Lean4 编译器对 T13 核心结论执行命题级验证 |

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

## 与其他工具的关系

- **与 TM02 因果验证互补**：TM02 用 DoWhy/EconML 做统计因果推断，TM06b 用 Lean4 做逻辑因果验证，二者从不同角度验证因果声明
- **与 T17 事实核查互补**：T17 用 CoVe 做外部事实核查，TM06b 做内部逻辑一致性验证
- **不替代**：TM06 的 14 维覆盖度验证（TM06b 是命题级形式化验证，TM06 是维度级覆盖度验证）
