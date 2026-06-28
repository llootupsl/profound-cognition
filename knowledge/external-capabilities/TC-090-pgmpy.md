<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-27
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（Wave 4 Step 4 补建，对应 W4-FX 项，提取自现有内化机制）

# TC-090: pgmpy — 贝叶斯网络推理

## 基本信息
- **名称**: pgmpy
- **类别**: 贝叶斯网络推理
- **语言**: Python
- **版本要求**: >=0.1.20
- **许可证**: MIT
- **仓库**: https://github.com/pgmpy/pgmpy
- **维护方**: pgmpy

## 核心能力
- 贝叶斯网络结构学习（PC/GES/Hill Climbing）
- 概率推断（变量消除/信念传播）
- 参数学习（最大似然/贝叶斯估计）
- 动态贝叶斯网络支持

## 在 profound-cognition 中的用途
- **TM02 MC-135**: TM02 因果验证 MC-135 节点（贝叶斯网络推理）
- **状态**: 提级（已补建独立卡）
- **内化位置**: thinking-models/general/MC-135-bayesian-network.md（方法论内化）

## 消费节点
- TM02 MC-135（提级（已补建独立卡））

## 调用前置条件

- Python 3.9+ 运行环境（如需代码执行）
- 对应工具库已安装（详见「基本信息」字段）
- 网络连接可用（如需远程 API 或数据源）
- 上游节点产出已就绪（根据消费节点依赖关系）

## 调用指令（P1-10 / A6.9-F2 修复，Wave 5：补全 pgmpy 专属调用代码示例）

> **设计原则**：以下代码示例覆盖 TM02 MC-135 贝叶斯网络推理核心调用场景，按"结构学习 → 参数学习 → 概率推断"递进。

### 1. 贝叶斯网络结构学习（PC 算法 + Hill Climbing）

```python
import pandas as pd
import numpy as np
from pgmpy.estimators import PC, HillClimbSearch, BicScore

def learn_bayesian_network_structure(data: pd.DataFrame, method: str = 'pc'):
    """从数据中学习贝叶斯网络结构。

    Args:
        data: 观测数据 DataFrame（列名为变量名）
        method: 结构学习方法（'pc' / 'hill_climbing'）

    Returns:
        model: 学习到的贝叶斯网络模型（DAG）
    """
    if method == 'pc':
        # PC 算法（基于条件独立性测试）
        estimator = PC(data=data)
        model = estimator.estimate(variant='stable', ci_test='chi_square', significance_level=0.05)
    elif method == 'hill_climbing':
        # Hill Climbing 算法（基于评分搜索）
        hc = HillClimbSearch(data=data)
        model = hc.estimate(scoring_method=BicScore(data=data), max_indegree=4, max_iter=int(1e4))
    else:
        raise ValueError(f"未知方法: {method}，支持 'pc' 或 'hill_climbing'")

    return model
```

### 2. 参数学习（最大似然估计 + 贝叶斯估计）

```python
from pgmpy.models import BayesianNetwork
from pgmpy.estimators import MaximumLikelihoodEstimator, BayesianEstimator

def learn_parameters(model: BayesianNetwork, data: pd.DataFrame, method: str = 'mle'):
    """学习贝叶斯网络参数（条件概率分布 CPD）。

    Args:
        model: 已知结构的贝叶斯网络模型
        data: 观测数据 DataFrame
        method: 参数学习方法（'mle' 最大似然 / 'bayesian' 贝叶斯估计）

    Returns:
        model: 含参数的贝叶斯网络模型
    """
    if method == 'mle':
        # 最大似然估计
        model.fit(data, estimator=MaximumLikelihoodEstimator)
    elif method == 'bayesian':
        # 贝叶斯估计（带先验，等效样本量 prior_type='BDeu'）
        model.fit(data, estimator=BayesianEstimator, prior_type='BDeu', equivalent_sample_size=10)
    else:
        raise ValueError(f"未知方法: {method}，支持 'mle' 或 'bayesian'")

    return model
```

### 3. 概率推断（变量消除 + 信念传播）

```python
from pgmpy.models import BayesianNetwork
from pgmpy.inference import VariableElimination, BeliefPropagation

def probabilistic_inference(
    model: BayesianNetwork,
    query_variables: list,
    evidence: dict,
    algorithm: str = 'variable_elimination'
):
    """贝叶斯网络概率推断：给定证据，查询目标变量的后验分布。

    Args:
        model: 含参数的贝叶斯网络模型
        query_variables: 查询变量列表
        evidence: 证据字典（{变量: 取值}）
        algorithm: 推断算法（'variable_elimination' / 'belief_propagation'）

    Returns:
        posterior: 查询变量的后验概率分布
    """
    if algorithm == 'variable_elimination':
        # 变量消除算法（精确推断）
        inferencer = VariableElimination(model)
        posterior = inferencer.query(variables=query_variables, evidence=evidence, joint=True)
    elif algorithm == 'belief_propagation':
        # 信念传播算法（近似推断，适用于大网络）
        inferencer = BeliefPropagation(model)
        inferencer.calibrate()
        posterior = inferencer.query(variables=query_variables, evidence=evidence, joint=True)
    else:
        raise ValueError(f"未知算法: {algorithm}，支持 'variable_elimination' 或 'belief_propagation'")

    return posterior
```

### 4. TM02 MC-135 贝叶斯网络因果推断（与 PyMC 互补）

```python
from pgmpy.models import BayesianNetwork
from pgmpy.estimators import HillClimbSearch, BicScore
import pandas as pd

def tm02_bayesian_network_causal_inference(
    treatment: str,
    outcome: str,
    data: pd.DataFrame,
    confounders: list
):
    """TM02 MC-135 节点：用贝叶斯网络进行因果推断。

    与 TC-084 PyMC（贝叶斯概率编程）互补：
    - PyMC 适合连续变量的参数化因果推断
    - pgmpy 适合离散/混合变量的结构因果发现

    Args:
        treatment: 处理变量名
        outcome: 结果变量名
        data: 观测数据
        confounders: 混杂变量名列表

    Returns:
        causal_effect: 处理变量对结果变量的因果效应
    """
    # Step 1: 结构学习（自动发现因果图）
    hc = HillClimbSearch(data=data)
    structure = hc.estimate(scoring_method=BicScore(data=data))

    # Step 2: 构建贝叶斯网络模型
    edges = list(structure.edges())
    model = BayesianNetwork(edges)

    # Step 3: 参数学习
    model.fit(data, estimator=BayesianEstimator, prior_type='BDeu', equivalent_sample_size=10)

    # Step 4: do-calculus 因果推断（Pearl's intervention）
    from pgmpy.estimators.CausalInference import CausalInference
    causal_infer = CausalInference(model, data, confounders=confounders)
    causal_effect = causal_infer.query(treatment, outcome, do={treatment: 1})

    return causal_effect
```

### 5. 命令行调用（CLI 模式）

```bash
# 安装
pip install pgmpy>=0.1.20 pandas numpy scipy

# 验证安装
python -c "import pgmpy; print(pgmpy.__version__)"

# 运行结构学习（假设脚本保存为 bn_learn.py）
python bn_learn.py --data data.csv --method pc --output model.json
```

## 失败回退策略（P1-10 修复，Wave 5：补全 pgmpy 专属失败模式）

- **触发条件**: 工具不可用、调用超时、输出质量不达标、依赖缺失、**结构学习失败（学到空图或完全连通图）、参数学习不收敛、推断数值不稳定（概率含 NaN/Inf）、网络规模超出内存限制**
- **回退路径**:
  1. **L1_FULL（pgmpy 完整运行）**：结构学习+参数学习+推断全部成功 → 使用贝叶斯网络后验作为最终输出
  2. **L2_PARTIAL（pgmpy 受限运行）**：部分环节失败 → ①结构学习失败时，改用 Hill Climbing 替代 PC 算法；②参数学习不收敛时，改用 MLE 替代贝叶斯估计；③推断不稳定时，切换至 BeliefPropagation 近似算法
  3. **L3_TEXT_ONLY（LLM 内建推理）**：pgmpy 全部算法均不可用 → 降级到 LLM 内建贝叶斯网络推理能力（基于思维模型 MC-135），标注 [INTERNAL_REASONING]，并标注 `bayesian_network_calibration_unavailable: true`
  4. **L4_SERVICE_DOWN（无结构推断）**：LLM 内建推理不可用 → 仅产出定性结论，标注 `structural_inference_unavailable: true`，要求人工介入
- **回退声明**: 回退后失去工具增强能力，但保证流程不中断（EXHAUST 铁律）；任何降级均须写入 execution_ledger.fallback_chain
- **穷尽重试**: 按 L1_FULL → L2_PARTIAL → L3_TEXT_ONLY → L4_SERVICE_DOWN 逐级降级，每级最多重试 3 次（不设总重试上限，符合 EXHAUST 铁律）
- **与 TC-084 PyMC 互补关系**：pgmpy 失败时若 PyMC 可用，可切换至 PyMC（TC-084）执行连续变量贝叶斯推断；反之亦然

## 效果度量（P1-10 修复，Wave 5：补全 pgmpy 专属度量指标）

| 度量指标 | 定义 | 目标值 |
|----------|------|--------|
| 执行成功率 | 成功调用次数 / 总调用次数 | >= 0.95 |
| 平均延迟 | 单次调用平均耗时（含结构学习+推断） | <= 10s（小网络）/ <= 60s（大网络） |
| 输出质量分 | Supervisor 评分（0-1） | >= 0.8 |
| 穷尽重试触发率 | 触发降级的调用次数 / 总调用次数 | <= 0.1 |
| **结构学习成功率** | 学到有效 DAG（非空图非完全连通图）的次数 / 总次数 | >= 0.85 |
| **推断数值稳定性** | 推断结果无 NaN/Inf 的次数 / 总次数 | >= 0.99 |
| **BIC 评分改善率** | 学习到的网络 BIC 评分优于随机网络的次数 / 总次数 | >= 0.90 |

效果度量写入 NRSF，供 T19 质量检查消费。

## 替代关系
- **可被替代为**: PyMC（TC-084，贝叶斯概率编程）+ causal-learn（TC-086，因果发现）
- **替代说明**: 见能力卡注册表

## Audit-6 Wave 4 备注
- **核验状态**: ⚠️仅理论引入 → ✅已补建独立能力卡（Wave 4 Step 4 - W4-F2）
- **核验日期**: 2026-06-27
- **审计员**: 独立审计子代理（Audit-6）
- **修复说明**: 原本仅有理论提及/内化机制，无独立能力卡文件；现已补建独立卡，保留原内化位置作为方法论引用
