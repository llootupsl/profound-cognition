<!-- 作者：阿洋 -->

# TC-057: DoWhy — Causal Inference Library

> ★核心方法论已内化于 tasks/TM02_causal_verification.md（MC-054 四步法 + TC-057 识别工具方法论 + 源码逻辑引入 + dowhy_estimation 子步骤）

> **版本治理元数据 (D12.4.2)**:
> - version: 1.2
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（基础能力卡 + API 示例）
>   - v1.1 内化于 TM02（MC-054 四步法 + TC-057 识别工具方法论 + 源码逻辑引入）
>   - v1.2 新增 DoWhy 四步流程定义、causal_effect_estimates/robustness_check 字段、EconML CATE 后端声明（R9-04/Task 5.23）

## 基本信息
- **名称**: DoWhy
- **类别**: 因果推断
- **语言**: Python
- **版本要求**: ≥0.8
- **安装**: pip install dowhy
- **许可证**: MIT
- **仓库**: https://github.com/py-why/dowhy

## 核心能力
- 因果效应估计 (ATE/CATE/ITE)
- 反事实分析
- 反驳检验 (Refutation tests)
- 识别策略 (backdoor/frontdoor/IV)
- 与 EconML 集成（CATE 估计后端）

## 在 profound-cognition 中的用途
- **TM02 Step 2**: 因果识别与因果效应估计
- **TM02 Step 3**: 反事实分析
- **TM02 Step 5**: 稳健性检验
- **TM02 dowhy_estimation 子步骤**: 四步流程闭环（R9-04）

## API 示例
```python
import dowhy
from dowhy import CausalModel

model = CausalModel(
    data=data,
    treatment="treatment_var",
    outcome="outcome_var",
    common_causes=["confounder1", "confounder2"]
)
identified_estimand = model.identify_effect()
estimate = model.estimate_effect(identified_estimand)
refutation = model.refute_estimate(identified_estimand, estimate)
```

## DoWhy 四步流程定义（R9-04 / Task 5.23.3）

> **方法论原理**：DoWhy 四步流程将因果推断从"跑回归看 p 值"升级为"先证明可识别，再估计，最后验证"的结构化推理过程。每一步都有明确的输入、输出和通过判据，形成可审计的闭环。

### 步骤 1：假设（Model — 因果建模）

**输入**：领域知识、T09 因果图、T22 系统变量集合
**任务**：将领域知识编码为因果图（DAG），声明处理变量、结果变量、混杂变量、工具变量和中介变量
**输出**：CausalModel 对象（包含因果 DAG + 变量声明）
**通过判据**：因果图无环、变量角色明确标注、关键混杂变量无遗漏

```yaml
model_step:
  inputs:
    causal_graph: "T09 因果图（DAG）"
    variables:
      treatment: "处理变量"
      outcome: "结果变量"
      common_causes: "混杂变量集合"
      instruments: "工具变量集合（可选）"
      mediators: "中介变量集合（可选）"
      effect_modifiers: "效应修饰变量集合（可选）"
  outputs:
    causal_model: "CausalModel 对象"
  pass_criteria:
    - "因果图无环（isAcyclic=true）"
    - "处理变量与结果变量在图中存在有向路径"
    - "关键混杂变量已声明（基于 T09 因果图）"
```

### 步骤 2：识别（Identify — 因果效应可识别性判定）

**输入**：CausalModel 对象
**任务**：使用 do-calculus 判断目标因果效应是否可从观测数据中识别，选择识别策略（backdoor/frontdoor/IV）
**输出**：IdentifiedEstimand 对象（包含识别策略 + 调整集）
**通过判据**：至少一种识别策略可用；若不可识别，标注 UNIDENTIFIABLE 并穷尽重试为敏感性分析

```yaml
identify_step:
  inputs:
    causal_model: "CausalModel 对象"
  outputs:
    identified_estimand:
      estimand_type: "ate | cate | ite"
      identifying_strategy: "backdoor | frontdoor | iv | unidentifiable"
      backdoor_variables: "后门调整集（若 strategy=backdoor）"
      frontdoor_variables: "前门中介集（若 strategy=frontdoor）"
      iv_instruments: "工具变量集（若 strategy=iv）"
  pass_criteria:
    - "至少一种识别策略可用（backdoor/frontdoor/IV）"
    - "若不可识别，标注 UNIDENTIFIABLE 并触发穷尽重试"
  decision_tree:
    backdoor_first: "优先尝试后门准则"
    frontdoor_fallback: "后门调整集不可观测时尝试前门准则"
    iv_fallback: "后门和前门均不满足时尝试工具变量法"
    unidentifiable: "所有策略均不满足时标注不可识别"
```

### 步骤 3：估计（Estimate — 因果效应计算）

**输入**：IdentifiedEstimand 对象 + 观测数据（或 T09 伪数据集）
**任务**：选择估计方法（回归/IPW/双重机器学习），计算 ATE/CATE/ITE
**输出**：CausalEstimate 对象（包含效应量点估计 + 标准误 + 置信区间 + p 值）
**通过判据**：效应量估计成功；若使用伪数据集，必须标注警告

```yaml
estimate_step:
  inputs:
    identified_estimand: "IdentifiedEstimand 对象"
    data: "观测数据或 T09 伪数据集"
  outputs:
    causal_estimate:
      value: "效应量点估计（float）"
      stderr: "标准误（float）"
      ci: "[置信区间下界, 置信区间上界]"
      p_value: "p 值（float）"
      estimand_type: "ate | cate | ite"
  pass_criteria:
    - "效应量估计成功（value 非 null）"
    - "若使用伪数据集，pseudo_data_warning=true"
  method_selection:
    backdoor_regression: "调整集小 + 数据大 → 线性回归调整"
    ipw: "倾向性评分可行 → 逆概率加权"
    frontdoor_chain: "前门策略 → 链式分解 P(Y|do(X))=Σ_m P(M|X)×Σ_x' P(Y|M,X')×P(X')"
    iv_wald: "IV 策略 → Wald 估计量或 2SLS"
    econml_cate: "需要 CATE → 调用 EconML 后端（TC-058）"
```

### 步骤 4：反驳（Refute — 稳健性验证）

**输入**：CausalEstimate 对象 + 观测数据
**任务**：执行多种鲁棒性检验（Placebo treatment、Random common cause、Data subset）
**输出**：RefutationResult 列表
**通过判据**：至少 2/3 反驳检验通过 → STRONG；1/3 通过 → MEDIUM；0/3 通过 → WEAK

```yaml
refute_step:
  inputs:
    causal_estimate: "CausalEstimate 对象"
    data: "观测数据"
  outputs:
    refutation_results:
      - method: "placebo | random_common_cause | data_subset | dummy_outcome"
        estimate_with_refutation: "反驳后的效应量"
        p_value: "反驳检验 p 值"
        passed: "是否通过反驳（bool）"
  pass_criteria:
    strong: "≥2/3 反驳通过 → robustness=STRONG"
    medium: "1/3 反驳通过 → robustness=MEDIUM"
    weak: "0/3 反驳通过 → robustness=WEAK"
  refutation_methods:
    placebo_treatment: "用随机变量替换处理变量，预期效应为零；若非零则存在未控制混杂"
    random_common_cause: "添加随机公共原因变量，效应应不变；若变化则模型敏感"
    data_subset: "在随机子集上重复估计，检验效应稳定性"
    dummy_outcome: "用随机变量替换结果变量，预期效应消失；若非零则模型误设"
```

## causal_effect_estimates 字段定义（Task 5.23.4）

> **字段用途**：标准化 DoWhy 因果效应估计结果的输出格式，供 TM02 output_schema 和下游节点（T13/T27）消费。

```yaml
causal_effect_estimates:
  # 元数据
  estimation_id: "string — 估计唯一标识（est_{uuid}）"
  hypothesis_id: "string — 对应的因果假设 ID"
  timestamp: "ISO8601 — 估计时间戳"

  # 识别结果
  identification:
    strategy: "backdoor | frontdoor | iv | unidentifiable"
    adjustment_set: ["混杂变量列表（backdoor）"]
    mediator: "string | null（frontdoor 中介变量）"
    instrument: "string | null（IV 工具变量）"
    identifiable: true | false

  # 估计结果
  estimation:
    estimand_type: "ate | cate | ite"
    method: "regression | ipw | double_ml | wald | 2sls | frontdoor_chain"
    value: "float — 效应量点估计"
    stderr: "float — 标准误"
    ci_lower: "float — 置信区间下界"
    ci_upper: "float — 置信区间上界"
    p_value: "float — 显著性 p 值"
    n_samples: "integer — 样本量"
    pseudo_data_warning: "bool — 是否使用伪数据集"

  # CATE 异质性（来自 EconML 后端）
  cate_heterogeneity:
    available: "bool — EconML CATE 估计是否可用"
    method: "DoublyLearner | CausalForestDML | LinearDML | SparseLinearDML | null"
    subgroups:
      - subgroup: "子群体描述"
        features: "特征字典"
        cate: "float — 条件平均处理效应"
        ci_lower: "float"
        ci_upper: "float"
    heterogeneity_significant: "bool — 异质性是否显著"

  # 反事实场景
  counterfactual:
    scenarios:
      - condition: "反事实条件描述"
        expected_outcome: "反事实预期结果"
        actual_outcome: "实际结果"
        effect_size: "float | null — 效应量"
```

## robustness_check 字段定义（Task 5.23.4）

> **字段用途**：标准化 DoWhy 反驳检验结果的输出格式，量化因果效应的稳健性。

```yaml
robustness_check:
  # 元数据
  check_id: "string — 稳健性检查唯一标识（rob_{uuid}）"
  estimation_id: "string — 对应的 causal_effect_estimates.estimation_id"
  timestamp: "ISO8601 — 检查时间戳"

  # 反驳检验结果
  refutation_tests:
    - method: "placebo_treatment | random_common_cause | data_subset | dummy_outcome"
      description: "检验方法描述"
      estimate_with_refutation: "float — 反驳后的效应量"
      original_estimate: "float — 原始效应量"
      effect_change: "float — 效应量变化幅度（绝对值）"
      p_value: "float — 反驳检验 p 值"
      passed: "bool — 是否通过反驳检验"
      pass_criteria: "通过判据描述（如 p>0.05 或 |effect_change|<threshold）"

  # 稳健性综合评定
  robustness_summary:
    tests_passed: "integer — 通过的反驳检验数"
    tests_total: "integer — 总反驳检验数"
    robustness_level: "STRONG | MEDIUM | WEAK | UNCERTAIN"
    robustness_score: "float — 稳健性评分（tests_passed/tests_total）"
    level_criteria:
      strong: "≥2/3 反驳通过"
      medium: "1/3 反驳通过"
      weak: "0/3 反驳通过"
      uncertain: "不可识别或伪数据集"

  # 敏感性分析（E-value）
  sensitivity_analysis:
    e_value: "float | null — E-value（使效应消失的最小混杂强度）"
    confounding_robustness: "HIGH | MEDIUM | LOW — 混杂稳健性"
    interpretation: "E-value 解读（如'E-value=2.5 意味着需要 2.5 倍强度的未观测混杂才能使效应消失'）"

  # 穷尽重试状态
  retry_status:
    level: "FULL | PARTIAL_A | PARTIAL_B | RETRYING"
    degradation_note: "string | null — 降级说明（如'穷尽重试 L4：纯文字因果结构分析'）"
```

## EconML CATE 估计后端声明（Task 5.23.5）

> **架构关系**：DoWhy 是因果推断的主引擎，负责建模→识别→估计→反驳四步流程。EconML 作为 DoWhy 的 CATE 估计后端，专注于异质性处理效应估计。二者通过 DoWhy 的 `method_name` 参数集成。

### 集成方式

```python
# DoWhy 调用 EconML 进行 CATE 估计
from dowhy import CausalModel

model = CausalModel(data=data, treatment="T", outcome="Y", common_causes=["X1", "X2"])

# 识别
identified_estimand = model.identify_effect()

# 估计 ATE（DoWhy 原生）
ate_estimate = model.estimate_effect(identified_estimand, method_name="backdoor.linear_regression")

# 估计 CATE（调用 EconML 后端）
cate_estimate = model.estimate_effect(
    identified_estimand,
    method_name="backdoor.econml.dml.DoublyLearner",
    target_units="ate",  # 或 "ate" / 具体特征值
    method_params={
        "init_params": {
            "model_y": "sklearn.ensemble.RandomForestRegressor",
            "model_t": "sklearn.ensemble.RandomForestClassifier",
        }
    }
)
```

### DoWhy ↔ EconML 职责分工

| 维度 | DoWhy（主引擎） | EconML（CATE 后端） |
|------|----------------|-------------------|
| **建模** | ✅ 因果图构建、变量角色声明 | ❌ 不负责建模 |
| **识别** | ✅ 后门/前门/IV 识别策略 | ❌ 不负责识别 |
| **ATE 估计** | ✅ 回归/IPW/2SLS | ❌ 不负责 ATE |
| **CATE 估计** | 🔗 调用 EconML 后端 | ✅ DoublyLearner/CausalForestDML |
| **反驳** | ✅ Placebo/Subset/Dummy | ❌ 不负责反驳 |
| **敏感性** | 🔗 调用 EconML E-value | ✅ E-value 计算 |

### 决策规则

| 条件 | 决策 |
|------|------|
| 需要平均效应（ATE） | DoWhy 原生估计（regression/IPW） |
| 需要异质效应（CATE） | DoWhy 调用 EconML 后端（DML/CausalForest） |
| 特征维度 ≤ 10 且样本量充足 | EconML CausalForestDML（非参数 CATE） |
| 特征维度 > 10 | EconML SparseLinearDML（稀疏线性 CATE） |
| EconML 不可用 | 穷尽重试为定性异质性分析（基于理论推理） |
| 无实证数据 | 使用伪数据集 + DoWhy 原生估计，标注警告 |

## 已知限制
- 需要结构化数据（纯文本研究需伪数据集）
- 伪数据集结果仅提供定性参考
- 因果图假设的正确性影响结果可靠性
- EconML CATE 估计需要大样本数据
- 前门准则和 IV 法的假设条件较强，实际场景中难以完全满足

## 穷尽重试策略

当 DoWhy 不可用时，按 L1→L2→L3→L4 逐级穷尽重试：

| 级别 | 条件 | 方案 |
|------|------|------|
| L1 | DoWhy 完整可用 | 完整四步法：建模→识别→估计→反驳 |
| L2 | DoWhy 部分可用 | 手动后门准则判定 + 定性反驳检验 |
| L3 | DoWhy 不可用 | 因果图 + 识别策略声明（无数值估计） |
| L4 | 因果推断完全不可用 | 纯文字因果结构分析（因果图 + 文字解释 + 置信度评级） |

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

| 节点 | 用途 | 子步骤 |
|------|------|--------|
| TM02 | 因果推断 | dowhy_estimation（四步流程闭环） |

## 交叉引用

- **上游**: `tasks/TM01_system_dynamics.md`（系统动力学，提供因果图输入）、`tasks/T09_cog_reason.md`（认知推理，提供因果方向假设）
- **下游**: `tasks/T13_cog_synthesize.md`（认知综合，消费因果效应估计）、`tasks/T27_ethics_analysis.md`（伦理分析，消费因果矛盾）
- **相关**: `knowledge/external-capabilities/TC-058-EconML.md`（EconML CATE 估计后端）、`knowledge/external-capabilities/TC-059-Pyro.md`（Pyro 贝叶斯推断）、`knowledge/external-capabilities/TC-090-pgmpy.md`（pgmpy 贝叶斯网络）

---

## 调用前置条件

- Python 3.9+ 运行环境（如需代码执行）
- 对应工具库已安装（详见卡片「安装」或「基本信息」字段）
- 网络连接可用（如需远程 API 或数据源）
- 上游节点产出已就绪（根据消费节点依赖关系）

## 效果度量

| 度量指标 | 定义 | 目标值 |
|----------|------|--------|
| 执行成功率 | 成功调用次数 / 总调用次数 | ≥ 0.95 |
| 平均延迟 | 单次调用平均耗时 | ≤ 5s |
| 输出质量分 | Supervisor 评分（0-1） | ≥ 0.8 |
| 穷尽重试触发率 | 触发降级的调用次数 / 总调用次数 | ≤ 0.1 |

效果度量写入 NRSF，供 T19 质量检查消费。
© 阿洋

