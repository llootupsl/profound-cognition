<!-- 作者：阿洋 -->

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
