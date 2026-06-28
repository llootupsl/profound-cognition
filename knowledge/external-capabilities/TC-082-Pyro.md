---
name: TC-082-Pyro

> ★核心方法论已内化于 tasks/TM02_causal_verification.md，本文件仅作快速引用入口

description: 概率编程信念更新，用于不确定性推理和因果推断
version: "1.0"
category: external-tool
consuming_engines: []
integrated_nodes: [TM02]

## 调用前置条件

- Python 3.9+ 运行环境（如需代码执行）
- 对应工具库已安装（详见卡片「安装」或「基本信息」字段）
- 网络连接可用（如需远程 API 或数据源）
- 上游节点产出已就绪（根据消费节点依赖关系）

## 失败回退策略

- **触发条件**: 工具不可用、调用超时、输出质量不达标、依赖缺失
- **回退路径**: 降级到 LLM 内建能力，标注 [INTERNAL_REASONING]
- **回退声明**: 回退后失去工具增强能力，但保证流程不中断（EXHAUST 铁律）
- **穷尽重试**: 按 L1_FULL → L2_PARTIAL → L3_TEXT_ONLY → L4_SERVICE_DOWN 逐级降级

## 效果度量

| 度量指标 | 定义 | 目标值 |
|----------|------|--------|
| 执行成功率 | 成功调用次数 / 总调用次数 | ≥ 0.95 |
| 平均延迟 | 单次调用平均耗时 | ≤ 5s |
| 输出质量分 | Supervisor 评分（0-1） | ≥ 0.8 |
| 穷尽重试触发率 | 触发降级的调用次数 / 总调用次数 | ≤ 0.1 |

效果度量写入 NRSF，供 T19 质量检查消费。
---

<!-- 作者：阿洋 -->



> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

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

