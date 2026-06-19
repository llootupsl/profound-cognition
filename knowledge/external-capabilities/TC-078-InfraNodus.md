---
name: TC-078-InfraNodus

> ★核心方法论已内化于 tasks/T03b_cross_axis_matrix.md，本文件仅作快速引用入口

description: 文本网络分析工具，用于结构洞发现和知识空白识别
version: "1.0"
category: external-tool
consuming_engines: []
integrated_nodes: [T15b]
---

<!-- 作者：阿洋 -->


# TC-078: InfraNodus — 结构洞发现

## 用途
基于文本网络分析的知识图谱工具，通过识别概念网络中的结构洞（structural gaps）来发现知识空白和潜在的创新连接点，支持知识图谱的完整性评估。

## 授权/许可
AGPL-3.0

## 下载源
https://github.com/noduslabs/infranodus

## 集成节点
- **T15b (跨域矩阵)**: 在跨域知识图谱中识别结构洞——即两个或多个知识域之间缺乏连接的区域，发现潜在的跨域创新机会

## tool-availability 探测
```bash
# 检测InfraNodus
python -c "import infranodus; print('InfraNodus available')" 2>/dev/null || echo "InfraNodus not installed"
# 或检测API端点
curl -s http://localhost:3000/api/status 2>/dev/null || echo "InfraNodus server not running"
```

## 穷尽重试替代链
若不可用 → 穷尽重试替代为 NetworkX 中心性分析 + 社区检测（Louvain/Girvan-Newman）；或手动结构洞识别

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

| 节点 | 用途 |
|------|------|
| T15b | 结构洞发现 |

