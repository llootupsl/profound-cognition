---
name: TC-079-GenerativeAgents
description: 生成式智能体社会涌现沙盒，模拟多智能体社会互动
version: "1.0"
category: external-tool
consuming_engines: []
integrated_nodes: [TM03]
---

<!-- 作者：阿洋 -->


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

