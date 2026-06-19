<!-- 作者：阿洋 -->

# TC-061: EMA Workbench — Exploratory Modeling Analysis

## 基本信息
- **名称**: EMA Workbench
- **类别**: 探索性建模
- **语言**: Python
- **版本要求**: ≥2.0
- **安装**: pip install ema_workbench
- **许可证**: BSD-3
- **仓库**: https://github.com/quaquel/EMAworkbench

## 核心能力
- 探索性建模与分析 (EMA)
- 不确定性下的策略评估
- 情景发现 (PRIM, CART)
- 鲁棒性优化
- 参数扫描与敏感性分析

## 在 profound-cognition 中的用途
- **T22 Step 5**: EMA 探索性建模
- **T25 Step 2**: 情景发现与鲁棒性评估
- **穷尽重试替代路径**: 失败时穷尽重试替代为定性情景分析

## API 示例
```python
from ema_workbench import Model, RealParameter, ScalarOutcome, perform_experiments

model = Model("research_model", function=model_function)
model.uncertainties = [
    RealParameter("param1", 0.1, 1.0),
    RealParameter("param2", 0.0, 10.0)
]
model.outcomes = [
    ScalarOutcome("outcome1")
]
results = perform_experiments(model, 1000)
```

## 已知限制
- 需要可参数化的模型函数
- 大规模实验计算开销大
- 纯文本研究场景需构建伪模型函数

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

| 节点 | 用途 |
|------|------|
| TM04 | 探索性建模分析 |

