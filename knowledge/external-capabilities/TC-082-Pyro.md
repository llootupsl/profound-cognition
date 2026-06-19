---
name: TC-082-Pyro

> ★核心方法论已内化于 tasks/TM02_causal_verification.md，本文件仅作快速引用入口

description: 概率编程信念更新，用于不确定性推理和因果推断
version: "1.0"
category: external-tool
consuming_engines: []
integrated_nodes: [TM02]
---

<!-- 作者：阿洋 -->


# TC-082: Pyro — 概率编程信念更新

## 用途
基于PyTorch的深度概率编程库，支持贝叶斯推理、变分推断和随机变分推断，用于在认知流水线中实现基于证据的信念更新与不确定性量化。

## 授权/许可
Apache 2.0

## 下载源
https://github.com/pyro-ppl/pyro

## 集成节点
- **TM02 (因果验证)**: 在因果验证中，利用Pyro的贝叶斯推理能力对因果模型参数进行信念更新——当新证据到达时，从先验分布更新到后验分布，量化因果关系的置信度变化

## tool-availability 探测
```bash
# 检测Pyro
python -c "import pyro; print('Pyro available')" 2>/dev/null || echo "Pyro not installed"
```

## 穷尽重试替代链
若不可用 → 穷尽重试替代为 PyMC3/PyMC + 手动MCMC；或穷尽重试替代为 Stan (CmdStanPy)；或穷尽重试替代为简单贝叶斯更新（手动计算）

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

| 节点 | 用途 |
|------|------|
| TM02 | 概率编程信念更新 |

