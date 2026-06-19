---
name: TC-076-Catlab

> ★核心方法论已内化于 tasks/T03b_cross_axis_matrix.md，本文件仅作快速引用入口

description: 范畴论计算库，支持同构类比和函子映射
version: "1.0"
category: external-tool
consuming_engines: []
integrated_nodes: [T15b]
---

<!-- 作者：阿洋 -->


# TC-076: Catlab — 范畴论同构类比

## 用途
基于Julia的范畴论科学计算库，提供范畴、函子、自然变换等范畴论抽象的计算实现，支持跨域知识结构的同构类比发现。

## 授权/许可
MIT

## 下载源
https://github.com/AlgebraicJulia/Catlab.jl

## 集成节点
- **T15b (跨域矩阵)**: 利用Catlab的范畴论工具发现不同领域之间的结构同构——两个领域看似不同的知识结构可能共享相同的范畴论骨架，从而支持类比迁移

## tool-availability 探测
```bash
# 检测Julia和Catlab
julia -e 'using Catlab; println("Catlab available")' 2>/dev/null || echo "Julia/Catlab not installed"
# 或Python替代
python -c "import catlab; print('Catlab Python available')" 2>/dev/null
```

## 穷尽重试替代链
若不可用 → 穷尽重试替代为 NetworkX 图同构检测 + 手动结构映射；或穷尽重试替代为 Python 范畴论库（如 discopy）

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

| 节点 | 用途 |
|------|------|
| T15b | 范畴论同构类比 |

