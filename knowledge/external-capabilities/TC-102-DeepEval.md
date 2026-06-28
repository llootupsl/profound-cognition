<!-- 作者：阿洋 -->

# TC-102: DeepEval — LLM 评估框架

> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡 + T19b 六维映射 + 多模型投票 + JSON 报告 + pytest 集成）（R9-07/Task 5.24）

## 基本信息
- **名称**: DeepEval
- **类别**: LLM 评估框架
- **语言**: Python
- **版本要求**: ≥2.0.0
- **安装**: pip install deepeval
- **许可证**: Apache-2.0
- **仓库**: https://github.com/confident-ai/deepeval
- **卡片编号**: #102
- **类型**: TC
- **优先级**: P1
- **层级**: L0

## 核心能力
- **LLM 输出评估**：对 LLM 生成的文本进行多维度质量评估
- **标准指标库**：内置 AnswerRelevancy、Faithfulness、ContextualRelevancy、ContextualPrecision、ContextualRecall、Hallucination、Toxicity、Bias、GEEval 等指标
- **自定义评估**：通过 GEEval（生成式评估）支持自定义评估维度与评分标准
- **多模型投票**：支持多个 LLM 作为评估器，对同一输入独立评分后聚合（中位数投票）
- **pytest 集成**：通过 `@assert_test` 装饰器将评估用例接入 pytest 测试体系，支持 CI/CD
- **JSON 报告**：评估结果输出为标准化 JSON 报告，便于下游消费与审计

## 在 profound-cognition 中的用途
- **T19b 处方门控**: 对处方质量执行六维度评估（R9-07）
- **T19 交付守卫**: 辅助交付物质量评估
- **T17 事实核查**: 辅助幻觉检测（Hallucination 指标）

## T19b 六个评估维度 → DeepEval 指标映射（Task 5.24.2）

> **映射目的**：将 T19b 处方门控节点的六个评估维度映射到 DeepEval 标准指标，使处方门控从"规则判定"升级为"LLM 评估 + 规则判定"双重验证。每个维度对应一个 DeepEval 指标（原生或 GEEval 自定义），输出 0-1 分制的连续评分，与 T19b 原有的二元/三级判定互补。

### 维度 1：处方有效性（Prescription Validity）

- **T19b 来源**：核心职责 1 — 处方必须同时包含 action + timeline + success_criteria 三要素
- **DeepEval 指标**：`GEEval`（自定义评估）+ `AnswerRelevancy`
- **评估问题**：处方是否包含具体行动、可量化时间线、可度量成功标准？
- **评分标准**：
  - 1.0 = 三要素齐全且内容具体（动词短语+操作对象+执行方式 / 可量化时间范围 / 可度量验证条件）
  - 0.5 = 三要素齐全但内容模糊（如"尽快""适时"等模糊时间线）
  - 0.0 = 任一要素缺失

```python
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCaseParams

validity_metric = GEval(
    name="Prescription Validity",
    criteria="评估处方是否同时包含具体行动（动词短语+操作对象+执行方式）、可量化时间线（如'3个月内'而非'尽快'）、可度量成功标准（如'响应时间降低至200ms以下'）",
    evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
    evaluation_steps=[
        "检查 action 字段是否存在且为具体动词短语",
        "检查 timeline 字段是否存在且为可量化时间范围（不含'尽快''适时''条件成熟时'等模糊表述）",
        "检查 success_criteria 字段是否存在且为可度量验证条件",
        "三要素齐全且具体 → 1.0；齐全但模糊 → 0.5；任一缺失 → 0.0",
    ],
)
```

### 维度 2：证据链合规性（Evidence Chain Compliance）

- **T19b 来源**：核心职责 2 — 铁律4，处方必须基于已验证的证据链（§ref 引用链可追溯至 NRSF-Full）
- **DeepEval 指标**：`Faithfulness`（忠实度）+ `ContextualFaithfulness`
- **评估问题**：处方是否忠于其声明的证据来源？证据链是否可追溯且经 T17 核查？
- **评分标准**：
  - 1.0 = 证据链完整且可追溯至 NRSF-Full，T17 核查为非幻觉引用
  - 0.5 = 证据链存在但部分来源不可追溯
  - 0.0 = 无证据链支撑（evidence_orphan）

```python
from deepeval.metrics import FaithfulnessMetric

faithfulness_metric = FaithfulnessMetric(
    threshold=0.8,
    model="gpt-4o",
)
# retrieval_context 中填入 NRSF-Full 中对应证据源文本
# actual_output 中填入处方文本
```

### 维度 3：置信度门控（Confidence Gating）

- **T19b 来源**：核心职责 3 — 三级置信度门控（≥0.8 / 0.6-0.8 / <0.6）
- **DeepEval 指标**：`GEEval`（自定义评估）
- **评估问题**：处方的置信度评级是否与证据强度匹配？置信度 < 0.6 的处方是否被正确降级？
- **评分标准**：
  - 1.0 = 置信度评级与证据强度匹配，降级规则正确执行
  - 0.5 = 置信度评级存在偏差但降级规则执行正确
  - 0.0 = 置信度评级与证据强度严重不匹配，或降级规则未执行

```python
confidence_metric = GEval(
    name="Confidence Gating",
    criteria="评估处方置信度评级是否与证据强度匹配：confidence>=0.8 应保持 strong_prescription；0.6<=confidence<0.8 应附加置信度标注；confidence<0.6 应降级为 observation_suggestion",
    evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.EXPECTED_OUTPUT],
    evaluation_steps=[
        "验证 confidence>=0.8 的处方是否标记为 strong_prescription",
        "验证 0.6<=confidence<0.8 的处方是否附加置信度标注",
        "验证 confidence<0.6 的处方是否移入 downgraded_prescriptions",
        "验证无法映射到具体结论的处方是否默认 confidence=0.5 并触发降级",
    ],
)
```

### 维度 4：互斥性检查（Mutual Exclusion Check）

- **T19b 来源**：核心职责 4 — 两两比对识别逻辑矛盾与行动冲突
- **DeepEval 指标**：`GEEval`（自定义评估）
- **评估问题**：处方集合中是否存在逻辑矛盾或行动冲突？互斥处方对是否已正确处理？
- **评分标准**：
  - 1.0 = 无互斥冲突，或互斥处方对已正确处理（保留高置信度者，拒绝低者）
  - 0.5 = 存在互斥处方对但已记录原因
  - 0.0 = 存在未处理的互斥处方对

```python
exclusion_metric = GEval(
    name="Mutual Exclusion Check",
    criteria="评估处方集合中是否存在逻辑矛盾（如'立即执行A'与'暂缓执行A'）或行动冲突（如'增加X预算'与'削减X预算'），互斥处方对应保留置信度较高者",
    evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
    evaluation_steps=[
        "两两比对所有 valid_prescriptions",
        "识别逻辑矛盾（方向冲突）",
        "识别行动冲突（资源冲突）",
        "验证互斥处方对是否保留置信度较高者、拒绝较低者",
        "验证置信度相同时是否均降级为 observation_suggestion",
    ],
)
```

### 维度 5：可执行性验证（Executability Verification）

- **T19b 来源**：核心职责 5 — 用户可直接执行 + 执行前提明确 + 结果可观测
- **DeepEval 指标**：`GEEval`（自定义评估）+ `AnswerRelevancy`
- **评估问题**：处方是否可被用户直接执行？执行前提是否明确？结果是否可观测？
- **评分标准**：
  - 1.0 = 三项全满足（可直接执行 + 前提明确 + 结果可观测）
  - 0.5 = 部分满足
  - 0.0 = 不可执行（non_executable）

```python
executability_metric = GEval(
    name="Executability Verification",
    criteria="评估处方是否满足：1)用户可直接执行（无需专业工具/特殊权限/第三方协作即可启动第一步）；2)执行前提明确（执行条件在用户当前上下文中可满足）；3)结果可观测（成功标准可通过用户可获取的信息验证）",
    evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
    evaluation_steps=[
        "检查用户是否可直接执行（无需额外工具/权限/协作）",
        "检查执行前提是否在用户当前上下文中可满足",
        "检查成功标准是否可通过用户可获取的信息验证",
        "三项全满足 → 1.0；部分满足 → 0.5；不可执行 → 0.0",
    ],
)
```

### 维度 6：门控综合判定（Gate Decision Integrity）

- **T19b 来源**：self_check_before_output 第 5 项 — prescription_gate_result 是否正确反映了门控状态
- **DeepEval 指标**：`GEEval`（自定义评估）
- **评估问题**：prescription_gate_result（pass/fail）是否与实际门控状态一致？存在被拒绝的关键处方且无有效替代时是否为 fail？
- **评分标准**：
  - 1.0 = gate_result 与门控状态完全一致
  - 0.5 = gate_result 存在边界模糊但可接受
  - 0.0 = gate_result 与门控状态矛盾（如存在 rejected 且无有效替代时设为 pass）

```python
gate_integrity_metric = GEval(
    name="Gate Decision Integrity",
    criteria="评估 prescription_gate_result 是否正确反映门控状态：pass=所有处方通过门控（或无处方需门控）；fail=存在被拒绝的处方且无有效替代",
    evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.EXPECTED_OUTPUT],
    evaluation_steps=[
        "验证存在 rejected_prescriptions 且无有效替代时 gate_result=fail",
        "验证所有处方通过门控（或无处方）时 gate_result=pass",
        "验证 downgraded_prescriptions 不影响 gate_result（降级非拒绝）",
        "验证 gate_summary 中计数与实际处方列表一致",
    ],
)
```

### 映射汇总表

| # | T19b 评估维度 | DeepEval 指标 | 评分范围 | 通过阈值 | 失败动作 |
|---|--------------|--------------|---------|---------|---------|
| 1 | 处方有效性 | GEEval + AnswerRelevancy | 0.0-1.0 | ≥0.8 | 标记 invalid_prescription |
| 2 | 证据链合规性 | Faithfulness + ContextualFaithfulness | 0.0-1.0 | ≥0.8 | 标记 evidence_orphan |
| 3 | 置信度门控 | GEEval | 0.0-1.0 | ≥0.7 | 触发降级复审 |
| 4 | 互斥性检查 | GEEval | 0.0-1.0 | ≥0.8 | 触发互斥裁决 |
| 5 | 可执行性验证 | GEEval + AnswerRelevancy | 0.0-1.0 | ≥0.7 | 标记 non_executable |
| 6 | 门控综合判定 | GEEval | 0.0-1.0 | ≥0.9 | 触发 gate_result 复审 |

## 多模型投票机制（Task 5.24.3）

> **机制原理**：单一 LLM 评估器存在评估偏差（如 GPT-4o 倾向给高分、Claude 倾向给低分）。多模型投票机制使用 3 个异构 LLM 作为评估器，对同一处方独立评分，取中位数作为最终评分，消除单一模型偏差。当三模型评分分歧过大（标准差 > 0.2）时，标记为 `low_consensus` 并触发人工裁决。

### 评估器配置

```python
from deepeval.models import DeepEvalBaseLLM

# 三个异构评估器（来自不同厂商，降低同源偏差）
EVALUATOR_MODELS = [
    "gpt-4o",           # OpenAI 评估器
    "claude-3-5-sonnet",# Anthropic 评估器
    "gemini-1.5-pro",   # Google 评估器
]
```

### 投票流程

```python
import statistics

def multi_model_vote(prescription, dimension_metric, evaluators=EVALUATOR_MODELS):
    """多模型投票评估

    Args:
        prescription: 待评估的处方文本
        dimension_metric: DeepEval 指标实例（含评估维度定义）
        evaluators: 评估器模型列表（默认 3 个异构 LLM）

    Returns:
        vote_result: 包含各模型评分、中位数、共识度、最终评分的字典
    """
    scores = []
    model_details = []

    for model_name in evaluators:
        # 为每个评估器创建独立的指标实例（避免状态污染）
        metric = clone_metric_with_model(dimension_metric, model_name)
        score = metric.measure(prescription)
        scores.append(score)
        model_details.append({
            "model": model_name,
            "score": score,
            "reasoning": metric.reasoning if hasattr(metric, "reasoning") else None,
        })

    # 取中位数（消除极端值影响）
    median_score = statistics.median(scores)
    # 计算标准差（衡量共识度）
    std_dev = statistics.stdev(scores) if len(scores) > 1 else 0.0

    # 共识度判定
    if std_dev <= 0.1:
        consensus_level = "HIGH"   # 高共识
    elif std_dev <= 0.2:
        consensus_level = "MEDIUM" # 中共识
    else:
        consensus_level = "LOW"    # 低共识，触发人工裁决

    return {
        "model_votes": model_details,
        "median_score": median_score,
        "std_dev": std_dev,
        "consensus_level": consensus_level,
        "final_score": median_score,  # 最终评分取中位数
        "needs_human_review": consensus_level == "LOW",
    }
```

### 投票决策规则

| 条件 | 决策 |
|------|------|
| 中位数 ≥ 阈值 且 共识度 = HIGH | 评估通过，采纳中位数评分 |
| 中位数 ≥ 阈值 且 共识度 = MEDIUM | 评估通过，附加共识度标注 |
| 中位数 ≥ 阈值 且 共识度 = LOW | 标记 `low_consensus`，触发人工裁决 |
| 中位数 < 阈值 | 评估不通过，按维度失败动作处理 |
| 评估器不可用（API 错误等） | 穷尽重试：剩余 2 个评估器取中位数 → 1 个评估器直接采用 → 规则判定（无 LLM 评估） |

### 穷尽重试策略

当 DeepEval 评估器不可用时，按 L1→L2→L3→L4 逐级穷尽重试：

| 级别 | 条件 | 方案 |
|------|------|------|
| L1 | 3 个评估器全部可用 | 完整多模型投票（中位数 + 共识度） |
| L2 | 1 个评估器不可用 | 剩余 2 个评估器取平均值，标注 `reduced_quorum` |
| L3 | 仅 1 个评估器可用 | 单模型评估，标注 `single_evaluator_warning` |
| L4 | 所有 LLM 评估器不可用 | 回退到 T19b 原有规则判定（无 LLM 评估），标注 `rule_based_fallback` |

## 标准化 JSON 报告（Task 5.24.4）

> **报告用途**：将 DeepEval 评估结果固化为标准化 JSON 报告，供 T19b output_schema 消费、下游节点（T19/T28）审计、CI/CD 质量门控使用。

### JSON 报告 Schema

```yaml
deepeval_report:
  # 元数据
  report_id: "string — 报告唯一标识（de_{uuid}）"
  timestamp: "ISO8601 — 评估时间戳"
  prescription_id: "string — 对应 T19b 的处方 ID（如 RX-001）"
  evaluator_config:
    models: ["gpt-4o", "claude-3-5-sonnet", "gemini-1.5-pro"]
    deepeval_version: "string — DeepEval 版本号"

  # 六维度评估结果
  dimension_scores:
    - dimension: "validity | evidence_compliance | confidence_gating | mutual_exclusion | executability | gate_integrity"
      deepeval_metric: "GEEval | Faithfulness | AnswerRelevancy | ContextualFaithfulness"
      threshold: "float — 通过阈值"
      model_votes:
        - model: "string — 评估器模型名"
          score: "float — 该模型评分（0.0-1.0）"
          reasoning: "string — 评分理由"
      median_score: "float — 中位数评分"
      std_dev: "float — 标准差"
      consensus_level: "HIGH | MEDIUM | LOW"
      passed: "bool — 是否通过阈值"
      failure_action: "string | null — 失败时触发的动作"

  # 综合评定
  overall_assessment:
    dimensions_passed: "integer — 通过的维度数"
    dimensions_total: "integer — 总维度数（6）"
    overall_score: "float — 六维度中位数评分的均值"
    overall_verdict: "pass | fail | needs_review"
    needs_human_review: "bool — 是否需要人工裁决（任一维度共识度=LOW 时为 true）"
    review_reason: "string | null — 需人工裁决的原因"

  # 穷尽重试状态
  retry_status:
    level: "L1 | L2 | L3 | L4"
    degradation_note: "string | null — 降级说明"
    unavailable_models: ["string — 不可用的评估器列表"]

  # 与 T19b 门控的集成
  t19b_integration:
    gate_result_consistency: "bool — DeepEval 评估结果与 T19b 规则判定是否一致"
    discrepancy_note: "string | null — 不一致时的说明"
    recommended_action: "string — 建议动作（如'采纳 DeepEval 评估'或'维持 T19b 规则判定'）"
```

### JSON 报告示例

```json
{
  "report_id": "de_550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2026-06-25T10:30:00+08:00",
  "prescription_id": "RX-001",
  "evaluator_config": {
    "models": ["gpt-4o", "claude-3-5-sonnet", "gemini-1.5-pro"],
    "deepeval_version": "2.0.0"
  },
  "dimension_scores": [
    {
      "dimension": "validity",
      "deepeval_metric": "GEEval",
      "threshold": 0.8,
      "model_votes": [
        {"model": "gpt-4o", "score": 1.0, "reasoning": "三要素齐全且具体"},
        {"model": "claude-3-5-sonnet", "score": 1.0, "reasoning": "action/timeline/success_criteria 均明确"},
        {"model": "gemini-1.5-pro", "score": 0.9, "reasoning": "三要素齐全，时间线略宽泛"}
      ],
      "median_score": 1.0,
      "std_dev": 0.058,
      "consensus_level": "HIGH",
      "passed": true,
      "failure_action": null
    }
  ],
  "overall_assessment": {
    "dimensions_passed": 6,
    "dimensions_total": 6,
    "overall_score": 0.95,
    "overall_verdict": "pass",
    "needs_human_review": false,
    "review_reason": null
  },
  "retry_status": {
    "level": "L1",
    "degradation_note": null,
    "unavailable_models": []
  },
  "t19b_integration": {
    "gate_result_consistency": true,
    "discrepancy_note": null,
    "recommended_action": "采纳 DeepEval 评估，与 T19b 规则判定一致"
  }
}
```

### 报告写入位置

- **文件路径**: `reports/deepeval/{session_id}/{prescription_id}_deepeval_report.json`
- **NRSF 引用**: 评估报告通过 §ref 标记引用至 NRSF-Full，供下游节点追溯
- **T19b 消费**: T19b 在 output_schema 中新增 `deepeval_assessment` 字段引用此报告

## pytest 集成（Task 5.24.5）

> **集成目的**：将 DeepEval 评估用例接入 pytest 测试体系，使处方门控评估可在 CI/CD 中自动运行，形成"代码即测试、测试即评估"的闭环。

### pytest 集成架构

```python
# tests/conftest.py
import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import GEval, FaithfulnessMetric, AnswerRelevancyMetric
from deepeval.models import DeepEvalBaseLLM

# 评估器配置（可通过环境变量覆盖）
EVALUATOR_MODELS = [
    pytest.env("DEEPEVAL_MODEL_1", default="gpt-4o"),
    pytest.env("DEEPEVAL_MODEL_2", default="claude-3-5-sonnet"),
    pytest.env("DEEPEVAL_MODEL_3", default="gemini-1.5-pro"),
]

# 六维度指标工厂
def build_t19b_metrics():
    """构建 T19b 六维度 DeepEval 指标集合"""
    return {
        "validity": GEval(name="Prescription Validity", criteria="...", evaluation_steps=[...]),
        "evidence_compliance": FaithfulnessMetric(threshold=0.8),
        "confidence_gating": GEval(name="Confidence Gating", criteria="...", evaluation_steps=[...]),
        "mutual_exclusion": GEval(name="Mutual Exclusion Check", criteria="...", evaluation_steps=[...]),
        "executability": GEval(name="Executability Verification", criteria="...", evaluation_steps=[...]),
        "gate_integrity": GEval(name="Gate Decision Integrity", criteria="...", evaluation_steps=[...]),
    }
```

### 测试用例定义

```python
# tests/test_t19b_prescription_gate.py
import pytest
import json
from deepeval import assert_test
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from tests.conftest import build_t19b_metrics, EVALUATOR_MODELS

# 加载处方测试数据（JSON fixture）
@pytest.fixture
def prescription_cases():
    with open("tests/fixtures/t19b_prescription_cases.json", "r", encoding="utf-8") as f:
        return json.load(f)

# 单维度单模型评估测试
@pytest.mark.parametrize("case", prescription_cases())
def test_prescription_validity(case):
    """测试处方有效性维度（单模型）"""
    metrics = build_t19b_metrics()
    test_case = LLMTestCase(
        input=case["input"],
        actual_output=case["actual_output"],
        expected_output=case.get("expected_output", ""),
        retrieval_context=case.get("evidence_chain", []),
    )
    assert_test(test_case, [metrics["validity"]])

# 多模型投票评估测试
@pytest.mark.parametrize("case", prescription_cases())
def test_prescription_multimodel_vote(case):
    """测试处方六维度多模型投票评估"""
    from tests.deepeval_voting import multi_model_vote

    metrics = build_t19b_metrics()
    test_case = LLMTestCase(
        input=case["input"],
        actual_output=case["actual_output"],
        expected_output=case.get("expected_output", ""),
        retrieval_context=case.get("evidence_chain", []),
    )

    vote_results = {}
    for dim_name, metric in metrics.items():
        result = multi_model_vote(test_case, metric, EVALUATOR_MODELS)
        vote_results[dim_name] = result

    # 断言所有维度通过阈值
    for dim_name, result in vote_results.items():
        assert result["final_score"] >= 0.7, f"维度 {dim_name} 评分 {result['final_score']} 低于阈值"
        # 低共识度时标记需人工审查（不直接失败）
        if result["consensus_level"] == "LOW":
            pytest.warn(f"维度 {dim_name} 共识度低，需人工裁决: std={result['std_dev']}")
```

### pytest 运行命令

```bash
# 运行全部 T19b 处方门控评估测试
pytest tests/test_t19b_prescription_gate.py -v

# 运行指定维度测试
pytest tests/test_t19b_prescription_gate.py -k "validity" -v

# 生成 JSON 报告
pytest tests/test_t19b_prescription_gate.py --deepeval-report-json

# CI/CD 集成（失败时阻断流水线）
pytest tests/test_t19b_prescription_gate.py --tb=short --maxfail=3
```

### CI/CD 集成（.github/workflows/ci.yml）

```yaml
name: DeepEval Quality Gate
on: [push, pull_request]
jobs:
  deepeval-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"
      - name: Install dependencies
        run: pip install deepeval pytest
      - name: Run DeepEval tests
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
        run: pytest tests/test_t19b_prescription_gate.py --deepeval-report-json
      - name: Upload DeepEval report
        uses: actions/upload-artifact@v4
        with:
          name: deepeval-report
          path: reports/deepeval/
```

### 测试用例 Fixture 格式

```json
// tests/fixtures/t19b_prescription_cases.json
[
  {
    "case_id": "TC-001",
    "input": "评估处方 RX-001 的有效性",
    "actual_output": "在3个月内完成X系统的Y模块重构，使响应时间降低至200ms以下",
    "expected_output": "valid_prescription",
    "evidence_chain": ["§ref:T09:causal_hypothesis_1:v3.0"],
    "expected_dimension_scores": {
      "validity": 1.0,
      "evidence_compliance": 0.9,
      "confidence_gating": 0.85,
      "mutual_exclusion": 1.0,
      "executability": 0.9,
      "gate_integrity": 1.0
    }
  }
]
```

## 已知限制
- 需要至少 1 个 LLM API 密钥（多模型投票需 3 个）
- API 调用成本随评估维度和处方数量线性增长
- 评估延迟较高（六维度 × 三模型 = 18 次 LLM 调用/处方）
- GEEval 自定义指标的评分可能因模型版本变化而漂移
- 纯文本研究场景中 evidence_chain 可能为空，导致 Faithfulness 指标退化为 N/A

## 穷尽重试策略

当 DeepEval 不可用时，按 L1→L2→L3→L4 逐级穷尽重试：

| 级别 | 条件 | 方案 |
|------|------|------|
| L1 | 3 个评估器全部可用 | 完整多模型投票（中位数 + 共识度） |
| L2 | 1 个评估器不可用 | 剩余 2 个评估器取平均值，标注 `reduced_quorum` |
| L3 | 仅 1 个评估器可用 | 单模型评估，标注 `single_evaluator_warning` |
| L4 | 所有 LLM 评估器不可用 | 回退到 T19b 原有规则判定（无 LLM 评估），标注 `rule_based_fallback` |

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

| 节点 | 用途 | 集成方式 |
|------|------|---------|
| T19b | 处方门控六维度评估 | DeepEval 评估 + T19b 规则判定双重验证 |
| T19 | 交付物质量评估 | 辅助评估（可选） |
| T17 | 幻觉检测 | Hallucination 指标（可选） |

## 交叉引用

- **上游**: `tasks/T19b_prescription_gate.md`（处方门控节点，提供六维度评估需求）、`tasks/T19_delivery_guard.md`（交付守卫，提供评估上下文）
- **下游**: `protocols/self-evaluation-protocol.md`（自评协议，消费 DeepEval 报告）、`protocols/output-schema-spec.md`（输出 Schema 规范，定义 deepeval_assessment 字段）
- **相关**: `knowledge/external-capabilities/TC-100-LangGraph.md`（LangGraph 编排引擎，DeepEval 测试可集成至 LangGraph CI）、`knowledge/evidence-standards.md`（证据等级标准，与 Faithfulness 指标互补）

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
