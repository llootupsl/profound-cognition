<!-- 作者：阿洋 -->

# TC-063: MetaNet — Metacognitive Network Analysis

## 基本信息

> ★核心方法论已内化于 tasks/T26_meta_insight_cross.md，本文件仅作快速引用入口

- **名称**: MetaNet
- **类别**: 元认知网络分析
- **语言**: Python
- **版本要求**: ≥3.0
- **安装**: pip install networkit
- **许可证**: MIT
- **仓库**: https://github.com/networkit/networkit

## 核心能力
- 复杂网络构建与分析
- 社区检测与中心性分析
- 网络可视化
- 元认知结构建模

## 在 profound-cognition 中的用途
- **T26 Step 2**: MetaNet 元认知网络分析
- **T28 Step 2**: 知识图谱网络构建
- **穷尽重试替代路径**: 失败时穷尽重试替代为定性网络描述

## API 示例
```python
import networkit as nk

G = nk.Graph(3, directed=True, weighted=True)
G.addNode()  # ensure nodes exist
G.addEdge(0, 1)
G.addEdge(1, 2)
centrality = nk.centrality.Betweenness(G)
centrality.run()
centrality_scores = centrality.scores()
community = nk.community.PLM(G)
community.run()
partitions = community.getPartition()
```

## 已知限制
- 需要 C++ 编译环境（NetworKit 核心为 C++ 实现）
- 网络结构依赖人工/LLM 定义
- 可视化复杂网络需要额外工具

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

| 节点 | 用途 |
|------|------|
| TM05 | 元认知网络分析 |
| T_meta_dim_9_10 | 元维度分析 |

