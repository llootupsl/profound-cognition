<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

# TC-084: PyMC — 贝叶斯概率编程

> ★核心方法论已内化于 knowledge/thinking-models/decision/bayesian-updating.md

## 基本信息
- **名称**: PyMC
- **类别**: 概率编程
- **语言**: Python
- **版本要求**: ≥5.0
- **许可证**: Apache 2.0
- **仓库**: https://github.com/pymc-devs/pymc

## 核心能力
- 贝叶斯概率编程（先验+观测数据→MCMC采样→后验分布）
- NUTS采样器（No-U-Turn Sampler）
- 自动先验分配
- R-hat收敛诊断与ESS计算
- 与Pyro TC-059互补

## 在 profound-cognition 中的用途
- **TM02**: 贝叶斯因果推断
- **bayesian-updating.md**: 贝叶斯更新核心执行引擎

## 消费节点
- TM02
- bayesian-updating.md

## 调用前置条件

- Python 3.9+ 运行环境（如需代码执行）
- 对应工具库已安装（详见卡片「安装」或「基本信息」字段）
- 网络连接可用（如需远程 API 或数据源）
- 上游节点产出已就绪（根据消费节点依赖关系）

## 调用指令（P1-9 / A6.9-F1 修复，Wave 5：补全 PyMC 专属调用代码示例）

> **设计原则**：以下代码示例覆盖 TM02 贝叶斯因果推断与 bayesian-updating.md 思维模型核心调用场景，按"基础调用 → 因果推断 → 收敛诊断"递进。

### 1. 基础贝叶斯推断调用（先验+观测数据→后验分布）

```python
import pymc as pm
import numpy as np

def bayesian_inference(observed_data: np.ndarray, prior_mu: float = 0.0, prior_sigma: float = 1.0):
    """基础贝叶斯推断：给定观测数据，推断参数后验分布。

    Args:
        observed_data: 观测数据数组
        prior_mu: 先验均值（默认 0.0）
        prior_sigma: 先验标准差（默认 1.0）

    Returns:
        trace: PyMC 后验采样轨迹（ArviZ InferenceData 对象）
    """
    with pm.Model() as model:
        # 定义先验
        mu = pm.Normal('mu', mu=prior_mu, sigma=prior_sigma)
        sigma = pm.HalfNormal('sigma', sigma=1.0)

        # 定义似然
        likelihood = pm.Normal('obs', mu=mu, sigma=sigma, observed=observed_data)

        # NUTS 采样（默认 4 chains × 1000 draws）
        trace = pm.sample(draws=1000, chains=4, tune=500, target_accept=0.9, return_inferencedata=True)

    return trace
```

### 2. TM02 贝叶斯因果推断调用（DoWhy 后端集成）

```python
import pymc as pm
import numpy as np
import arviz as az

def tm02_bayesian_causal_inference(
    treatment: np.ndarray,
    outcome: np.ndarray,
    confounders: np.ndarray,
    prior_causal_effect: float = 0.0
):
    """TM02 贝叶斯因果推断：估计处理变量对结果变量的因果效应后验。

    Args:
        treatment: 处理变量（T）
        outcome: 结果变量（Y）
        confounders: 混杂变量矩阵（X）
        prior_causal_effect: 因果效应先验均值（默认 0.0，无偏先验）

    Returns:
        causal_effect_posterior: 因果效应后验分布摘要
    """
    with pm.Model() as causal_model:
        # 因果效应先验
        tau = pm.Normal('tau', mu=prior_causal_effect, sigma=1.0)

        # 混杂调整系数
        beta = pm.Normal('beta', mu=0.0, sigma=1.0, shape=confounders.shape[1])

        # 噪声项
        sigma = pm.HalfNormal('sigma', sigma=1.0)

        # 结构方程：Y = tau*T + beta*X + epsilon
        mu = tau * treatment + pm.math.dot(confounders, beta)
        likelihood = pm.Normal('Y_obs', mu=mu, sigma=sigma, observed=outcome)

        # 采样
        trace = pm.sample(draws=2000, chains=4, tune=1000, target_accept=0.95)

    # 后验摘要
    causal_effect_posterior = az.summary(trace, var_names=['tau'], hdi_prob=0.95)
    return causal_effect_posterior
```

### 3. 收敛诊断调用（R-hat + ESS）

```python
import arviz as az

def diagnose_convergence(trace):
    """PyMC 采样收敛诊断：R-hat < 1.1 且 ESS > 400 视为收敛。

    Args:
        trace: PyMC 采样轨迹

    Returns:
        diagnosis: 收敛诊断报告
    """
    # R-hat 收敛诊断（Gelman-Rubin）
    rhat = az.rhat(trace)

    # 有效样本量（ESS）
    ess_bulk = az.ess(trace, method='bulk')
    ess_tail = az.ess(trace, method='tail')

    # 发散警告
    divergences = trace.sample_stats.diverging.sum().item()

    diagnosis = {
        'rhat_max': float(rhat.max()),
        'ess_bulk_min': float(ess_bulk.min()),
        'ess_tail_min': float(ess_tail.min()),
        'divergences': int(divergences),
        'converged': (
            float(rhat.max()) < 1.1
            and float(ess_bulk.min()) > 400
            and int(divergences) < 10
        )
    }
    return diagnosis
```

### 4. 命令行调用（CLI 模式）

```bash
# 安装
pip install pymc>=5.0 arviz numpy

# 验证安装
python -c "import pymc; print(pymc.__version__)"

# 运行贝叶斯模型（假设脚本保存为 bayes_model.py）
python bayes_model.py --data data.csv --prior-mu 0.0 --prior-sigma 1.0
```

## 失败回退策略（P1-9 修复，Wave 5：补全 PyMC 专属失败模式）

- **触发条件**: 工具不可用、调用超时、输出质量不达标、依赖缺失、**MCMC 不收敛（R-hat ≥ 1.1）、ESS < 400、发散样本 > 10**
- **回退路径**:
  1. **L1_FULL（PyMC 完整运行）**：MCMC 收敛 → 使用后验分布作为最终输出
  2. **L2_PARTIAL（PyMC 受限运行）**：MCMC 部分收敛（个别参数 R-hat 1.1-1.2）→ 增加采样次数至 draws=4000, tune=2000，重新采样；若仍不收敛，仅使用收敛参数的后验，未收敛参数标注 `uncertainty_calibration_failed`
  3. **L3_TEXT_ONLY（LLM 内建推理）**：PyMC 不可用或全部参数不收敛 → 降级到 LLM 内建贝叶斯推理能力，标注 [INTERNAL_REASONING]，并标注 `bayesian_calibration_unavailable: true`
  4. **L4_SERVICE_DOWN（无概率推断）**：LLM 内建推理不可用 → 仅产出定性结论，标注 `quantitative_inference_unavailable: true`，要求人工介入
- **回退声明**: 回退后失去工具增强能力，但保证流程不中断（EXHAUST 铁律）；任何降级均须写入 execution_ledger.fallback_chain
- **穷尽重试**: 按 L1_FULL → L2_PARTIAL → L3_TEXT_ONLY → L4_SERVICE_DOWN 逐级降级，每级最多重试 3 次（不设总重试上限，符合 EXHAUST 铁律）

## 效果度量（P1-9 修复，Wave 5：补全 PyMC 专属度量指标）

| 度量指标 | 定义 | 目标值 |
|----------|------|--------|
| 执行成功率 | 成功调用次数 / 总调用次数 | ≥ 0.95 |
| 平均延迟 | 单次调用平均耗时（含 MCMC 采样） | ≤ 30s（小数据集）/ ≤ 300s（大数据集） |
| 输出质量分 | Supervisor 评分（0-1） | ≥ 0.8 |
| 穷尽重试触发率 | 触发降级的调用次数 / 总调用次数 | ≤ 0.1 |
| **MCMC 收敛率** | R-hat < 1.1 且 ESS > 400 的参数数 / 总参数数 | ≥ 0.90 |
| **发散样本率** | 发散样本数 / 总采样数 | ≤ 0.01 |
| **后验 HDI 紧致度** | 95% HDI 宽度 / 参数尺度 | ≤ 0.5（数据充足时） |

效果度量写入 NRSF，供 T19 质量检查消费。