---
name: TC-077-XGI

> ★核心方法论已内化于 tasks/T03b_cross_axis_matrix.md，本文件仅作快速引用入口

description: 高阶网络超边分析库，用于复杂系统中的多体交互建模
version: "1.0"
category: external-tool
consuming_engines: []
integrated_nodes: [T03b]
---

<!-- 作者：阿洋 -->


# TC-077: XGI — 高阶网络超边

## 用途
基于Python的高阶网络（Hypergraph）分析库，支持超图构建、超边统计和复杂网络中的多体交互分析，突破传统图论仅能表示二元关系的局限。

## 授权/许可
BSD-3-Clause

## 下载源
https://github.com/xgi-org/xgi

## 集成节点
- **T03b (跨轴矩阵)**: 利用超边表示多维度的交叉关联——一个超边可以同时连接多个跨轴维度（如L1语义+L4因果+L7社会），超越传统二元关系矩阵的表示能力

## tool-availability 探测
```bash
# 检测XGI
python -c "import xgi; print('XGI available')" 2>/dev/null || echo "XGI not installed"
```

## 穷尽重试替代链
若不可用 → 穷尽重试替代为 NetworkX 超图（通过bipartite投影）+ 手动超边统计；或穷尽重试替代为 HyperNetX

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

| 节点 | 用途 |
|------|------|
| T03b | 高阶网络超边分析 |

