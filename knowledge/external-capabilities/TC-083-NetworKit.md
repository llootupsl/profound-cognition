<!-- 作者：阿洋 -->

# TC-083: NetworKit — 高性能复杂网络引擎

> ★核心方法论已内化于 tasks/T26_meta_insight_cross.md

## 基本信息
- **名称**: NetworKit
- **类别**: 复杂网络分析
- **语言**: C++/Python
- **许可证**: MIT
- **仓库**: https://github.com/networkit/networkit

## 核心能力
- 5种中心性算法（degree/betweenness/closeness/PageRank/eigenvector）
- 4种社区检测算法（Louvain/PLM/LabelPropagation/Spectral）
- C++后端支持十亿级边
- 替换NetworkX解决>5000节点性能瓶颈

## 在 profound-cognition 中的用途
- **TC-063 MetaNet**: 底层执行引擎，C++后端十亿级边

## 消费节点
- TC-063 MetaNet
