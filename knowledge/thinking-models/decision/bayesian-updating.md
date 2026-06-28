<!-- 作者：阿洋 -->

# 贝叶斯更新模型 — 基于新证据更新置信度的数学框架

> **模块标识**: `knowledge/thinking-models/decision/bayesian-updating`
> **职责**: 作为决策分析系统的概率推理引擎，接收假设与证据流，通过贝叶斯公式动态更新各假设的置信度，为推理路径评分和假设筛选提供量化基础
> **依赖**: `knowledge/thinking-models/decision/decision-matrix`、`knowledge/thinking-models/general/critical-thinking`、`knowledge/research-methods`
> **核心能力**: 先验概率设定、似然度评估、后验概率计算、证据序列迭代更新、置信度收敛检测

---

## 一、模块定位

### 1.1 在框架架构中的角色

```
┌─────────────────────────────────────────────────────────────────┐
│                    概率推理处理流水线                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  假设生成 ──▶ 先验设定 ──▶ 证据收集 ──▶ 本模块触发              │
│                                    │                            │
│                                    ▼                            │
│                      ┌─────────────────────┐                   │
│                      │  bayesian-updating  │                   │
│                      │  (贝叶斯更新引擎)    │                   │
│                      └────────┬────────────┘                   │
│                               │                                │
│              ┌────────────────┼────────────────┐               │
│              ▼                ▼                ▼               │
│         后验概率输出    置信度排序      收敛/发散判定            │
│         (T09使用)      (T05使用)       (质量门控)               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 触发条件

当问题涉及以下场景时自动触发：

- 多假设竞争且需要量化置信度排序
- 证据逐步累积需要动态更新判断
- 需要区分"先验信念"与"证据支持"
- 推理路径的 confidence_score 需要动态计算而非静态赋值

---

## 二、贝叶斯公式与核心概念

### 2.1 贝叶斯公式

```
P(H|E) = P(E|H) × P(H) / P(E)

其中:
  P(H|E) = 后验概率 — 观察到证据E后，假设H成立的概率
  P(E|H) = 似然度 — 假设H成立时，观察到证据E的概率
  P(H)   = 先验概率 — 观察到证据E之前，假设H成立的概率
  P(E)   = 证据概率 — 在所有假设下观察到证据E的总概率
```

### 2.2 全概率展开

```
P(E) = Σ P(E|Hi) × P(Hi)  对所有互斥假设Hi求和

当假设空间为 {H, ¬H} 时:
P(E) = P(E|H) × P(H) + P(E|¬H) × P(¬H)
```

### 2.3 核心概念

| 概念 | 定义 | 示例 |
|------|------|------|
| **先验概率 P(H)** | 观察新证据前对假设的置信度 | 基于历史数据，某市场策略成功率 P=0.6 |
| **似然度 P(E\|H)** | 假设为真时观察到证据的概率 | 如果策略有效，销售额增长的概率 P=0.8 |
| **后验概率 P(H\|E)** | 观察到证据后对假设的更新置信度 | 观察到销售额增长后，策略有效的概率 |
| **证据概率 P(E)** | 在所有假设下观察到证据的总概率 | 归一化常数，确保后验概率和为1 |
| **贝叶斯因子** | 似然度之比，衡量证据对假设的支持强度 | P(E\|H) / P(E\|¬H) |

---

## 三、先验概率设定规则

### 3.1 先验强度分类

| 先验类型 | 概率范围 | 适用场景 | 设定依据 |
|----------|---------|---------|---------|
| **无信息先验** | P = 0.5 | 完全无先验知识、全新领域、首次分析 | 均匀分布假设，不偏向任何假设 |
| **弱先验** | 0.3 ≤ P ≤ 0.7 | 有限先验知识、领域经验不足、初步判断 | 基于少量历史数据或专家直觉 |
| **强先验** | P < 0.1 或 P > 0.9 | 充分先验知识、大量历史数据、已验证规律 | 基于大量实证数据或已验证理论 |

### 3.2 先验设定约束

1. **所有互斥假设的先验概率之和必须为1**: Σ P(Hi) = 1
2. **无信息先验优先原则**: 当先验知识不足时，优先使用无信息先验，避免先验偏误
3. **先验强度与证据需求反比**: 先验越强，改变信念所需证据越多；先验越弱，证据的影响越大
4. **先验声明强制**: 每个假设必须显式声明先验概率及其设定依据，禁止隐含先验

### 3.3 先验偏误检测

```
先验偏误自检:
1. 如果先验 P > 0.9，是否因为"一直相信"而非"已验证"？
2. 如果先验 P < 0.1，是否因为"从未见过"而非"已证伪"？
3. 先验是否受到可得性启发（近期事件过度影响）？
4. 先验是否受到锚定效应（初始值过度影响）？
5. 如果交换先验（0.9→0.1），结论是否发生不合理的大幅变化？
```

---

## 四、似然度评估框架

### 4.1 似然度评估等级

| 等级 | P(E\|H) 范围 | 描述 | 评估依据 |
|------|-------------|------|---------|
| 极强支持 | 0.90-1.00 | 假设几乎必然产生该证据 | 因果机制明确、历史验证充分 |
| 强支持 | 0.70-0.89 | 假设很可能产生该证据 | 因果机制较明确、有历史先例 |
| 中等支持 | 0.40-0.69 | 假设有相当概率产生该证据 | 机制部分明确、有一定依据 |
| 弱支持 | 0.20-0.39 | 假设可能产生该证据 | 机制不明确、依据有限 |
| 极弱支持 | 0.00-0.19 | 假设不太可能产生该证据 | 机制矛盾或无依据 |

### 4.2 似然度评估规则

1. **因果机制优先**: 基于因果机制评估似然度，而非纯统计相关
2. **反事实对比**: 同时评估 P(E|H) 和 P(E|¬H)，差异越大证据越有区分力
3. **贝叶斯因子阈值**:

| 贝叶斯因子 BF | 证据强度 | 解释 |
|--------------|---------|------|
| BF < 1 | 反对假设 | 证据更支持替代假设 |
| 1 ≤ BF < 3 | 微弱支持 | 证据几乎无区分力 |
| 3 ≤ BF < 10 | 中等支持 | 证据有一定区分力 |
| 10 ≤ BF < 30 | 强支持 | 证据显著支持假设 |
| BF ≥ 30 | 极强支持 | 证据强烈支持假设 |

---

## 五、迭代更新流程

### 5.1 证据序列更新

```
初始状态: P(H) = 先验概率

证据1到达: P(H|E1) = P(E1|H) × P(H) / P(E1)
更新后: P(H) ← P(H|E1)

证据2到达: P(H|E2) = P(E2|H) × P(H) / P(E2)
更新后: P(H) ← P(H|E2)

... 依次迭代

最终: P(H) = 经所有证据更新后的后验概率
```

### 5.2 收敛检测

```
收敛判定:
- 如果连续3条证据的后验概率变化 < 0.05 → 标记为"已收敛"
- 如果后验概率在 0.3-0.7 之间反复震荡 → 标记为"证据冲突"
- 如果后验概率持续向0或1移动 → 标记为"强信号方向"

未收敛处理:
- 已收敛: 停止证据收集，输出当前后验概率
- 证据冲突: 标注冲突证据对，建议深入分析冲突原因
- 强信号方向: 继续收集证据直至收敛或达到证据上限

### 5.4 PyMC 贝叶斯概率编程步骤（v3 新增）

> **能力卡**: TC-084 PyMC

在收敛判定后，新增 PyMC 概率编程步骤进行更精确的后验分布估计：

```
PyMC 调用流程:
1. 先验设定: 将 bayesian-updating 的先验概率 P(H) 转化为 PyMC 先验分布（默认 Beta 分布）
2. 观测数据输入: 将证据流似然度 P(E|H) 转化为观测模型（默认 Bernoulli 观测）
3. MCMC 采样: 执行 MCMC 采样（NUTS 或 Metropolis-Hastings，≥2000 采样 + 1000 预热）
4. 后验分布: 提取后验分布的均值、94% HDI（最高密度区间）、R-hat 收敛诊断
5. 结果回注: 将 PyMC 后验分布回注到 bayesian_updating_analysis.posterior_distribution

标注规则:
- PyMC 结果标注: source=PyMC, method=MCMC, n_samples=2000, r_hat_ok=true
- PyMC 不可用时: 穷尽尝试解析贝叶斯更新，标注 source=analytical_bayesian, exhaust_retry_reason=pymc_unavailable
```

**与 Pyro TC-059 的互补关系**:
- Pyro TC-059：变分推断（Variational Inference），适合高维模型和快速近似
- PyMC TC-084：MCMC 采样，适合精确后验估计和不确定性量化
- 选择规则：维度 < 10 → PyMC MCMC（精确优先）；维度 ≥ 10 → Pyro VI（效率优先）

### 5.5 证据独立性检查

```
证据独立性自检:
1. Ei 和 Ej 是否来自同一信息源？（同源证据应合并）
2. Ei 是否因果依赖于 Ej？（依赖证据应作为一条复合证据）
3. Ei 和 Ej 是否由同一底层因素驱动？（共因证据应标注）
4. 独立证据的更新效果 > 相关证据的更新效果
```

---

## 六、与任务节点的协同

### 6.1 与 T09（推理路径设计）的集成

每条推理路径的 `confidence_score` 使用贝叶斯更新而非静态评分：

```
推理路径置信度更新:
1. 初始: confidence_score = 先验概率 P(H)
2. 每条新证据到达: confidence_score = P(H|E_new)
3. 路径排序: 按 confidence_score 降序排列
4. 路径筛选: confidence_score < 0.1 的路径标记为"低置信度"
5. 路径合并: 多条路径指向同一假设时，合并后验概率
```

### 6.2 与 T05（假设管理）的集成

每条新证据出现时更新相关假设的先验概率：

```
假设-证据联动:
1. T05 生成假设时，同时设定先验概率
2. 每条新证据到达时，对所有相关假设执行贝叶斯更新
3. 后验概率变化 > 0.2 的假设标记为"高敏感假设"
4. 后验概率 < 0.05 的假设标记为"可淘汰假设"
5. 后验概率 > 0.95 的假设标记为"高置信假设"
6. 更新结果回传 T05，驱动假设池的动态调整
```

### 6.3 与 decision-matrix 的集成

贝叶斯更新为决策矩阵提供概率基础：

- 风险评估维度中的"发生概率"使用贝叶斯后验概率
- 场景模拟器中的情景概率使用贝叶斯更新结果
- 一票否决机制中的"致命风险"判定基于后验概率阈值

---

## 七、输出模板

```yaml
bayesian_updating_analysis:
  hypothesis_space:
    - id: "H-001"
      statement: "假设陈述"
      prior: 0.0-1.0
      prior_type: "uninformative/weak/strong"
      prior_basis: "先验设定依据"
  evidence_stream:
    - id: "E-001"
      description: "证据描述"
      likelihood:
        P_E_given_H001: 0.0-1.0
        P_E_given_not_H001: 0.0-1.0
      bayes_factor: 0.0+
      independence_check: "independent/dependent/co-causal"
  posterior_distribution:
    - id: "H-001"
      posterior: 0.0-1.0
      posterior_change: -1.0-1.0
      sensitivity: "high/medium/low"
      status: "high_confidence/active/low_confidence/eliminated"
  convergence_status: "converged/conflicting/strong_signal"
  key_findings:
    strongest_evidence: "对后验影响最大的证据ID及说明"
    most_sensitive_hypothesis: "对证据最敏感的假设ID及说明"
    conflicting_evidence_pairs: ["冲突证据对"]
  verification_recommendations:
    - "建议收集的进一步证据及预期影响"
```

---

## 八、质量自检清单

### 概率一致性
- 所有互斥假设的先验概率之和 = 1.0
- 所有互斥假设的后验概率之和 = 1.0
- 每次更新后后验概率在 [0, 1] 范围内
- 贝叶斯因子计算正确

### 先验合理性
- 每个假设的先验类型已声明
- 先验设定依据已记录
- 先验偏误自检已完成
- 无隐含先验

### 证据质量
- 每条证据的似然度已评估
- 证据独立性已检查
- 贝叶斯因子已计算
- 冲突证据已标注

### 收敛判定
- 收敛/冲突/强信号状态已标注
- 未收敛时已给出进一步证据建议
- 证据序列更新顺序已记录

---

## 八、贝叶斯推理决策规则（MC-140 Bayesian-Inference）

| 条件 | 判定 | 行动 |
|------|------|------|
| 后验概率 P(H\|E) > 0.95 | 高置信假设 | 标记为"高置信"，可进入决策依据层 |
| 后验概率 P(H\|E) 在 0.7-0.95 | 中置信假设 | 继续收集证据，可作条件性决策依据 |
| 后验概率 P(H\|E) 在 0.3-0.7 | 低置信假设 | 不可作为决策依据，必须补充证据 |
| 后验概率 P(H\|E) < 0.05 | 可淘汰假设 | 标记为"可淘汰"，从假设池移除 |
| 连续3条证据后验变化 < 0.05 | 已收敛 | 停止证据收集，输出当前后验 |
| 后验在 0.3-0.7 反复震荡 | 证据冲突 | 标注冲突证据对，深入分析冲突原因 |
| 先验 P > 0.9 且无实证依据 | 先验偏误风险 | 穷尽重试先验至 0.7，重新计算后验 |
| 贝叶斯因子 BF ≥ 30 | 极强证据 | 证据强烈支持假设，可提高决策权重 |
| 贝叶斯因子 BF < 1 | 反对证据 | 证据反对假设，降低假设优先级 |
| 证据独立性检查失败 | 证据冗余 | 合并同源/依赖证据，重新计算后验 |

> 知识来源: MC-140 Bayesian-Inference

---

## 九、贝叶斯推理穷尽重试策略

| 重试层级 | 条件 | 替代方案 |
|---------|------|---------|
| L1 完整贝叶斯更新 | 先验可设定、似然度可评估、证据流可用 | 完整执行迭代更新流程，输出精确后验分布 |
| L2 近似贝叶斯更新 | 似然度无法精确评估但可做区间估计 | 使用似然度区间 [L_low, L_high] 计算后验区间，标注"区间估计" |
| L3 定性贝叶斯更新 | 无法量化先验或似然度 | 使用定性标签（高/中/低）替代数值，标注"定性推理" |
| L4 纯逻辑推理 | 无任何概率信息可用 | 仅做逻辑推理（若A则B），标注"无概率基础，纯逻辑推理" |

> 知识来源: MC-140 Bayesian-Inference

---

## 十、贝叶斯因子收敛决策规则（MC-141 Bayes-Factor-Convergence）

| 条件 | 判定 | 行动 |
|------|------|------|
| BF序列单调递增且 BF_latest ≥ 30 | 强收敛 | 停止证据收集，接受H1为强证据支持 |
| BF序列单调递减且 BF_latest < 1 | 强反向收敛 | 停止证据收集，接受H0 |
| BF序列在 1-10 间震荡 | 弱收敛/证据冲突 | 继续收集证据，分析冲突来源 |
| BF从 < 1 翻转至 > 3 | 证据方向反转 | 标注"证据反转"，重新评估假设 |
| 连续5条证据 BF 变化率 < 5% | BF已收敛 | 停止BF追踪，使用当前BF值 |
| PyMC MCMC R-hat > 1.05 | 采样未收敛 | 增加采样次数（≥5000），或切换为Pyro VI |
| PyMC HDI 宽度 > 后验标准差2倍 | 后验不确定性过大 | 标注"高不确定性"，建议补充先验信息 |

> 知识来源: MC-141 Bayes-Factor-Convergence

---

## 十一、贝叶斯因子收敛输出yaml规范

```yaml
bayes_factor_convergence:
  hypothesis_pair:
    H1: "假设1陈述"
    H0: "零假设陈述"
  bf_sequence:
    - evidence_id: "E-001"
      bayes_factor: 0.0+
      cumulative_bf: 0.0+
      direction: "increasing/decreasing/oscillating"
  convergence_status:
    bf_converged: true|false
    convergence_type: "strong_convergence/weak_convergence/divergence/reversal"
    final_bf: 0.0+
    evidence_strength: "decisive/strong/moderate/anecdotal/negative"
  pymc_results:
    available: true|false
    method: "MCMC/VI"
    n_samples: 0
    r_hat: 0.0
    hdi_width: 0.0
    posterior_mean: 0.0
    posterior_std: 0.0
  recommendation:
    action: "accept_H1/accept_H0/continue_collection/reverse_assessment"
    confidence: 0.0-1.0
    next_evidence_type: "建议收集的证据类型"
```

> 知识来源: MC-141 Bayes-Factor-Convergence

---

## 十二、贝叶斯因子收敛穷尽重试策略

| 重试层级 | 条件 | 替代方案 |
|---------|------|---------|
| L1 完整BF收敛分析 | BF序列可计算、PyMC可用 | 完整BF追踪+MCMC后验估计 |
| L2 解析BF收敛 | PyMC不可用但BF可解析计算 | 使用解析贝叶斯因子，标注 source='analytical' |
| L3 单点BF评估 | 证据不足以构建BF序列 | 仅计算当前BF值，标注"单点评估，无法判定收敛" |
| L4 纯先验比较 | 无似然度信息 | 仅比较先验概率，标注"无证据更新，纯先验比较" |

> 知识来源: MC-141 Bayes-Factor-Convergence

---

## 九、PyMC MCMC 采样方法论（TC-084）

> **能力卡**: TC-084 PyMC

### 9.1 核心原理

PyMC 是 Python 概率编程库，通过 MCMC（Markov Chain Monte Carlo）采样从后验分布中抽取样本，实现对复杂概率模型的精确后验推断。当解析贝叶斯更新不可行（多参数、非共轭先验、层次模型）时，PyMC 提供数值后验估计。

**MCMC 核心算法**：

| 算法 | 全称 | 适用场景 | 优势 | 局限 |
|------|------|---------|------|------|
| **NUTS** | No-U-Turn Sampler | 连续参数、多维度模型 | 自适应步长、高效探索、无需手动调参 | 需要求导、离散参数不适用 |
| **Metropolis-Hastings** | MH 采样 | 离散参数、不可微模型 | 通用性强、无需梯度 | 效率低、需手动调步长 |
| **DEMetropolisZ** | 差分进化Metropolis | 多模态后验 | 全局探索能力强 | 需要多链并行 |

### 9.2 PyMC MCMC 执行步骤

```
步骤1: 模型构建
  ├─ 定义先验分布：为每个参数指定先验（如 pm.Normal, pm.Beta, pm.Gamma）
  ├─ 定义似然函数：将观测数据与参数关联（如 pm.Bernoulli, pm.Poisson）
  ├─ 检查先验-似然共轭性：共轭→可解析更新；非共轭→需MCMC
  └─ 输出：PyMC 模型对象

步骤2: 采样配置
  ├─ 选择采样器：连续参数→NUTS；离散参数→Metropolis-Hastings
  ├─ 设置链数：≥4条独立链（用于R-hat诊断）
  ├─ 设置采样数：tune=1000（预热）+ draws=2000（有效采样）
  ├─ 设置初始值：init='advi'或'jitter+adapt_diag'
  └─ 输出：采样配置参数

步骤3: 执行采样
  ├─ 运行 pm.sample() 执行MCMC采样
  ├─ 监控采样进度和运行时间
  └─ 输出：InferenceData对象（含4条链×2000采样）

步骤4: 收敛诊断
  ├─ R-hat诊断：R-hat < 1.05 → 链已收敛
  │   └─ R-hat ≥ 1.05 → 增加采样数或检查模型
  ├─ 有效样本量（ESS）：ESS > 400 → 采样充分
  │   └─ ESS < 400 → 增加采样数
  ├─ 能量图（Energy Plot）：检查HMC能量分布是否匹配
  └─ 输出：收敛诊断报告

步骤5: 后验分析
  ├─ 后验摘要：pm.summary() 输出均值、标准差、HDI（最高密度区间）
  ├─ 后验预测检验：pm.sample_posterior_predictive() 检查模型拟合
  ├─ 参数相关性：检查后验参数间的相关性结构
  └─ 输出：后验分布统计量 + 预测检验结果
```

### 9.3 R-hat 收敛诊断详解

```
R-hat 计算方法:
1. 将 M 条链的采样结果分为前半段和后半段，共 2M 段
2. 计算段内方差 W 和段间方差 B
3. R-hat = √[(n-1)/n + B/(n×W)]
   其中 n 为每段采样数

收敛判定标准:
| R-hat值 | 判定 | 行动 |
|---------|------|------|
| < 1.01 | 强收敛 | 采样结果可信 |
| 1.01-1.05 | 弱收敛 | 可用但建议增加采样 |
| 1.05-1.10 | 未收敛 | 增加采样数或检查模型 |
| > 1.10 | 严重未收敛 | 必须重新设计模型或采样策略 |
```

### 9.4 PyMC 与 profound-cognition Layer 对照映射

| PyMC步骤 | 对应Layer | 映射说明 |
|----------|----------|---------|
| 步骤1 模型构建 | Layer2 分解 | 将假设分解为参数化概率模型 |
| 步骤2 采样配置 | Layer4 推理 | 配置推理策略和参数 |
| 步骤3 执行采样 | Layer4 推理 | 执行概率推理计算 |
| 步骤4 收敛诊断 | Layer5 反事实 | 诊断推理结果是否可靠 |
| 步骤5 后验分析 | Layer8 决策 | 后验分布驱动决策 |

### 9.5 PyMC 穷尽重试策略

```yaml
pymc_exhaust_retry:
  L1_FULL:
    condition: "PyMC可用，模型可构建，NUTS采样成功"
    action: "完整5步MCMC流程，4链×2000采样，R-hat诊断"
    confidence: "HIGH"

  L2_MH_EXHAUST_RETRY:
    condition: "NUTS不可用（离散参数或不可微模型）"
    action: "穷尽重试到Metropolis-Hastings采样，增加采样数至5000"
    confidence: "MEDIUM"
    output_annotation: "PyMC穷尽重试：使用MH采样替代NUTS"

  L3_ANALYTICAL_BAYESIAN:
    condition: "PyMC完全不可用，但先验-似然共轭"
    action: "使用解析贝叶斯更新（共轭先验公式）"
    confidence: "MEDIUM"
    output_annotation: "PyMC穷尽重试：使用解析贝叶斯更新"

  L4_MANUAL_UPDATE:
    condition: "PyMC不可用且先验-似然非共轭"
    action: "手动贝叶斯更新——逐条证据应用贝叶斯公式，数值近似"
    confidence: "LOW"
    output_annotation: "PyMC完全穷尽重试：手动数值贝叶斯更新"
```

> 知识来源: TC-084 [PyMC]

---

### [PyMC] 源码逻辑引入

#### 核心算法逻辑

**1. MCMC采样器选择源码逻辑**

```
采样器自动选择机制（pymc/sampling/forward.py）:

function auto_assign_sampler(model):
    for var in model.free_RVs:
        # 检查变量类型和约束
        var_type = var.type
        var_dtype = var.dtype

        if var.is_continuous and var.is_differentiable:
            # 连续可微变量 → NUTS（No-U-Turn Sampler）
            # NUTS是PyMC的默认采样器
            assign NUTS(var)

        elif var.is_discrete or not var.is_differentiable:
            # 离散变量或不可微变量 → Metropolis-Hastings
            # NUTS需要梯度，离散变量无法使用
            assign Metropolis(var)

        elif var.has_bounded_support:
            # 有界变量 → 使用变换后的NUTS
            # 自动logit/log变换将有界空间映射到无界空间
            assign NUTS(var, transform=logit_transform)

    # 混合模型：连续+离散变量使用复合采样器
    # 连续变量用NUTS，离散变量用MH，交替采样

NUTS采样器核心逻辑（pymc/sampling/strategies/nuts.py）:

function NUTS_step(q0, logp, grad_logp, step_size, max_treedepth=10):
    # q0: 当前参数位置, logp: 对数后验, grad_logp: 梯度
    r0 = sample_momentum()  # 采样动量
    u = uniform(0, exp(logp(q0) - 0.5 * r0·r0))  # 切片变量

    # 构建二叉树（双向扩展）
    q_minus, q_plus = q0, q0
    r_minus, r_plus = r0, r0
    j = 0  # 树深度
    n = 1  # 有效样本数
    s = 1  # 继续标志

    while s == 1 and j < max_treedepth:
        # 随机选择扩展方向（前向/后向）
        direction = random_choice([-1, +1])

        if direction == -1:
            q_minus, r_minus, _, _, q_prime, n_prime, s_prime =
                build_tree(q_minus, r_minus, u, direction, j, step_size, logp, grad_logp)
        else:
            _, _, q_plus, r_plus, q_prime, n_prime, s_prime =
                build_tree(q_plus, r_plus, u, direction, j, step_size, logp, grad_logp)

        if s_prime == 1 and uniform() < n_prime / n:
            q0 = q_prime  # 接受新位置

        # U-Turn检测：动量方向是否反转
        s = s_prime * (no_u_turn(q_minus, q_plus, r_minus, r_plus))
        n += n_prime
        j += 1

    return q0

Metropolis-Hastings采样器核心逻辑:

function MH_step(q0, logp, proposal_scale):
    # 从提议分布中采样
    q_proposal = q0 + normal(0, proposal_scale)

    # 计算接受概率
    log_alpha = logp(q_proposal) - logp(q0)
    alpha = min(1, exp(log_alpha))

    # 接受/拒绝
    if uniform() < alpha:
        return q_proposal  # 接受
    else:
        return q0          # 拒绝，保持原位
```

**2. 先验分布设定规则源码逻辑**

```
先验分布自动选择（pymc/distributions/continuous.py）:

function auto_prior(variable_name, data, prior_type="default"):
    if prior_type == "default":
        # 默认弱信息先验规则:
        if variable_is_probability_parameter:
            # 概率参数 ∈ [0,1] → Beta(2,2) 或 Uniform(0,1)
            return Beta(alpha=2, beta=2)

        elif variable_is_positive_real:
            # 正实参数 → HalfNormal(sigma=数据标准差)
            return HalfNormal(sigma=std(data) * 2)

        elif variable_is_location:
            # 位置参数 → Normal(mu=mean(data), sigma=std(data)*5)
            return Normal(mu=mean(data), sigma=std(data) * 5)

        elif variable_is_scale:
            # 尺度参数 → HalfCauchy(beta=数据标准差)
            # 或 Exponential(rate=1/数据标准差)
            return HalfCauchy(beta=std(data))

    elif prior_type == "noninformative":
        # 无信息先验:
        return Flat()  # 均匀分布（-∞, +∞）

    elif prior_type == "informative":
        # 需要用户提供具体参数
        raise RequiresUserInput

先验预测检查源码:

function prior_predictive_check(model, samples=500):
    # 从先验分布采样，检查先验预测是否合理
    prior_samples = sample_prior_predictive(model, samples)

    for var in model.observed_RVs:
        # 检查先验预测是否覆盖观测数据范围
        prior_min = min(prior_samples[var])
        prior_max = max(prior_samples[var])
        obs_min = min(model.observed_data[var])
        obs_max = max(model.observed_data[var])

        if obs_min < prior_min or obs_max > prior_max:
            warn(f"先验预测未覆盖观测数据范围: {var}")
            suggest_adjusting_prior(var)

    return prior_samples
```

**3. R-hat 收敛诊断算法源码逻辑**

```
R-hat收敛诊断（pymc/diagnostics.py）:

function compute_rhat(chains, split=True):
    # chains: list of arrays, 每条链的采样结果
    # split=True: 将每条链拆分为前后两半，增加链数

    if split:
        # 拆分每条链为前后两半
        split_chains = []
        for chain in chains:
            mid = len(chain) // 2
            split_chains.append(chain[:mid])
            split_chains.append(chain[mid:])
        chains = split_chains

    m = len(chains)       # 链数
    n = len(chains[0])    # 每条链长度

    # 步骤1：计算每条链的均值
    chain_means = [mean(chain) for chain in chains]

    # 步骤2：计算总体均值
    overall_mean = mean(chain_means)

    # 步骤3：计算链间方差 B
    B = n / (m - 1) * sum((chain_mean - overall_mean)^2
                          for chain_mean in chain_means)

    # 步骤4：计算链内方差 W
    chain_vars = [var(chain) for chain in chains]
    W = mean(chain_vars)

    # 步骤5：计算边际后验方差估计
    var_hat = (n - 1) / n * W + 1 / n * B

    # 步骤6：计算R-hat
    rhat = sqrt(var_hat / W)

    return rhat

# 收敛判定标准:
# R-hat < 1.01 → 收敛良好
# 1.01 ≤ R-hat < 1.05 → 基本收敛，需更多采样
# R-hat ≥ 1.05 → 未收敛，需增加迭代或调整模型

function compute_ess(chains):
    # 有效样本量（Effective Sample Size）
    # ESS = m * n / (1 + 2 * Σ(autocorrelation))

    for chain in chains:
        autocorr = compute_autocorrelation(chain)
        # 截断法：当连续两个自相关之和 < 0 时停止
        sum_autocorr = 0
        for lag in range(1, len(chain)):
            if autocorr[lag] + autocorr[lag+1] < 0:
                break
            sum_autocorr += autocorr[lag]

    ess = m * n / (1 + 2 * sum_autocorr)

    # ESS判定:
    # ESS > 400 → 采样效率良好
    # ESS < 400 → 需增加采样数
    return ess
```

#### 数据结构设计

```
核心数据结构:

1. Model: PyMC概率模型
   - free_RVs: list[TensorVariable]    # 自由随机变量
   - observed_RVs: list[TensorVariable] # 观测随机变量
   - deterministics: list[TensorVariable] # 确定性变换
   - logp(): 对数后验概率函数

2. InferenceData: 采样结果
   - posterior: Dict[str, ndarray]     # 后验采样 (chain, draw, *shape)
   - prior: Dict[str, ndarray]        # 先验采样
   - sample_stats: Dict[str, ndarray] # 采样统计（diverging, energy等）
   - log_likelihood: Dict[str, ndarray] # 对数似然

3. SamplerReport: 采样器报告
   - n_tune: int              # 调优步数
   - n_draws: int             # 采样步数
   - n_chains: int            # 链数
   - diverging: int           # 发散次数
   - rhat: Dict[str, float]   # 各变量R-hat
   - ess: Dict[str, float]    # 各变量ESS
```

#### 决策流程

```
PyMC MCMC 采样决策流程:

1. 模型构建 → 定义先验分布 + 似然函数
2. 先验预测检查 → prior_predictive_check() 验证先验合理性
3. 采样器选择 → auto_assign_sampler()
   ├─ 连续可微 → NUTS
   ├─ 离散/不可微 → Metropolis-Hastings
   └─ 混合 → 复合采样器
4. 采样执行 → sample(4链×2000步, tune=1000)
5. 收敛诊断 → compute_rhat() + compute_ess()
   ├─ R-hat < 1.01 且 ESS > 400 → 收敛，输出后验
   ├─ R-hat ≥ 1.05 → 增加迭代或重新参数化
   └─ 发散 > 0 → 调整target_accept或重新参数化
6. 后验分析 → 提取后验统计量和预测分布
```

#### 穷尽重试策略

```yaml
pymc_source_exhaust_retry:
  L1_NUTS_FULL:
    condition: "PyMC可用，NUTS采样成功，R-hat<1.01"
    action: "4链×2000步NUTS采样 + R-hat/ESS诊断 + 后验分析"
    confidence: "HIGH"

  L2_MH_EXHAUST_RETRY:
    condition: "NUTS不可用（离散参数或不可微模型）"
    action: "穷尽重试到Metropolis-Hastings，增加采样至5000步"
    confidence: "MEDIUM"
    output_annotation: "PyMC穷尽重试：使用MH采样替代NUTS"

  L3_ANALYTICAL_BAYESIAN:
    condition: "PyMC不可用，但先验-似然共轭"
    action: "解析贝叶斯更新（共轭先验公式）"
    confidence: "MEDIUM"
    output_annotation: "PyMC穷尽重试：解析贝叶斯更新"

  L4_MANUAL_UPDATE:
    condition: "PyMC不可用且先验-似然非共轭"
    action: "手动贝叶斯更新——逐条证据应用贝叶斯公式"
    confidence: "LOW"
    output_annotation: "PyMC完全穷尽重试：手动数值贝叶斯更新"
```
