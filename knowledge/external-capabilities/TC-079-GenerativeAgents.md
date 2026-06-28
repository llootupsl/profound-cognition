---
name: TC-079-GenerativeAgents
description: 生成式智能体社会涌现沙盒，模拟多智能体社会互动
version: "1.0"
category: external-tool
consuming_engines: []
integrated_nodes: [TM03]

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

# TC-079: GenerativeAgents — 社会涌现沙盒

> ★核心方法论已内化于 tasks/TM03_adversarial_synthesis.md

## 用途
基于斯坦福Smallville研究的生成式智能体框架，通过LLM驱动的多智能体在社会沙盒中互动，观察社会涌现现象（如信息传播、群体极化、共识形成），用于对抗性社会模拟。

## 授权/许可
MIT

## 下载源
https://github.com/joonspk-research/generative_agents

## 集成节点
- **TM03 (对抗综合)**: 在对抗综合阶段，部署多个持不同立场的生成式智能体在沙盒中互动，观察观点碰撞、说服、妥协和极化的社会涌现过程，为对抗综合提供模拟数据

## tool-availability 探测
```bash
# 检测GenerativeAgents
python -c "import generative_agents; print('GenerativeAgents available')" 2>/dev/null || echo "GenerativeAgents not installed"
# 检测Mesa作为备选
python -c "import mesa; print('Mesa available')" 2>/dev/null
```

## 穷尽重试替代链
若不可用 → 穷尽重试替代为 Mesa (TC-055) 多智能体模拟 + LLM角色扮演；或穷尽重试替代为手动角色辩论

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

| 节点 | 用途 |
|------|------|
| TM03 | 社会涌现沙盒 |

