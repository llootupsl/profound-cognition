<!-- 作者：阿洋 -->

# TC-057: DoWhy — Causal Inference Library

> ★核心方法论已内化于 tasks/TM02_causal_verification.md

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
- 与 EconML 集成

## 在 profound-cognition 中的用途
- **T23 Step 2**: 因果效应估计
- **T23 Step 3**: 反事实分析
- **T23 Step 5**: 稳健性检验

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

## 已知限制
- 需要结构化数据（纯文本研究需伪数据集）
- 伪数据集结果仅提供定性参考
- 因果图假设的正确性影响结果可靠性

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

| 节点 | 用途 |
|------|------|
| TM02 | 因果推断 |

