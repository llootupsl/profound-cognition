<!-- 作者：阿洋 -->

# TC-059: Pyro — Probabilistic Programming

## 基本信息

> ★核心方法论已内化于 tasks/TM02_causal_verification.md，本文件仅作快速引用入口

- **名称**: Pyro
- **类别**: 概率编程
- **语言**: Python
- **版本要求**: ≥1.8
- **安装**: pip install pyro-ppl
- **许可证**: Apache 2.0
- **仓库**: https://github.com/pyro-ppl/pyro

## 核心能力
- 贝叶斯建模
- MCMC 采样 (HMC, NUTS)
- 变分推断 (SVI)
- 后验预测检验

## 在 profound-cognition 中的用途
- **T23 Step 6**: Pyro 概率编程验证
- **穷尽重试替代路径**: 失败时穷尽重试替代为定性概率评估

## 已知限制
- MCMC 采样计算开销大
- 模型收敛需要调参
- 纯文本研究场景通常穷尽重试替代为定性评估

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

| 节点 | 用途 |
|------|------|
| TM02 | 概率编程 |

