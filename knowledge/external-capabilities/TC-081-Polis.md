---
name: TC-081-Polis

> ★核心方法论已内化于 tasks/T13_cog_synthesis.md，本文件仅作快速引用入口

description: 共识发现与意见可视化平台，用于大规模群体意见聚合
version: "1.0"
category: external-tool
consuming_engines: []
integrated_nodes: [TM03, T07b]
---

<!-- 作者：阿洋 -->


# TC-081: Pol.is — 共识发现

## 用途
基于实时意见聚合和可视化的共识发现平台，通过投票和意见分组算法识别群体中的共识区域和分歧线，支持大规模参与式决策。

## 授权/许可
AGPL-3.0

## 下载源
https://github.com/compdemocracy/polis

## 集成节点
- **TM03 (对抗综合)**: 在对抗综合中利用Pol.is的意见分组算法识别多方观点中的共识区域和不可调和的分歧线
- **T07b (跨轴检查)**: 在跨轴检查中，Pol.is帮助识别不同分析维度（如经济vs社会vs政治）上的意见一致性/冲突模式

## tool-availability 探测
```bash
# 检测Pol.is API
curl -s http://localhost:5000/api/v3/status 2>/dev/null || echo "Pol.is server not running"
# 或检测Python客户端
python -c "import polis; print('Polis Python available')" 2>/dev/null
```

## 穷尽重试替代链
若不可用 → 穷尽重试替代为 PCA/聚类分析 + 手动共识区域标注；或穷尽重试替代为 Delphi方法 + 结构化问卷

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

| 节点 | 用途 |
|------|------|
| TM03 | 共识发现 |
| T07b | 跨轴共识 |

