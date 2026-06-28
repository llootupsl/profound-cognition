<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

# TC-058: EconML — Heterogeneous Treatment Effects

## 基本信息
- **名称**: EconML
- **类别**: 因果推断
- **语言**: Python
- **版本要求**: ≥0.15
- **安装**: pip install econml
- **许可证**: MIT
- **仓库**: https://github.com/py-why/econml

## 核心能力
- 异质因果效应估计 (CATE)
- DoublyLearner, CausalForest, DeepIV 等
- 敏感性分析
- E-value 计算

## 在 profound-cognition 中的用途
- **T23 Step 4**: 敏感性分析
- **T23 Step 4**: E-value 计算

## 已知限制
- 需要大样本数据
- 纯文本研究场景通常仅能使用简化版本

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

| 节点 | 用途 |
|------|------|
| TM02 | 异质性处置效应估计 |

## 方法论内化

> ★核心方法论已内化于 tasks/TM02_causal_verification.md (MC-055完整内化)，以下为快速参考

### 方法论原理
EconML通过因果推断揭示处理效应的异质性，解决了平均处理效应掩盖亚群差异的问题。

### 执行步骤
1. 定义处理/结果/混杂变量
2. 选择估计器(DML/CausalForest/IV)
3. 交叉拟合
4. 估计CATE
5. 计算E-value
6. 异质性分析

### 决策规则
| 条件 | 动作 |
|------|------|
| 需要异质性因果效应 | EconML |
| 需要平均效应 | DoWhy |
| 需要贝叶斯 | PyMC |

### 输出规范
```yaml
econml_output:
  available: bool
  cate_estimate: float
  e_value: float
  heterogeneity_significant: bool
  degradation_note: str
```

### 穷尽重试策略
| 级别 | 方案 |
|------|------|
| L1 | EconML完整(AHP+熵权+TOPSIS) |
| L2 | DoWhy(平均效应) |
| L3 | 定性异质性分析 |
| L4 | 纯文字因果描述 |


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