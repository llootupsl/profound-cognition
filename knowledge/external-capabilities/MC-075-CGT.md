---
name: MC-075-CGT

> ★核心方法论已内化于 tasks/TM07_ontology_export.md，本文件仅作快速引用入口

description: 范畴论对抗形式化框架，用于结构化对抗论证的数学表示
version: "1.0"
category: external-tool
consuming_engines: []
integrated_nodes: [T13, TM03]
---

<!-- 作者：阿洋 -->


# MC-075: CGT — 范畴论对抗形式化

## 用途
基于范畴论（Category Theory）的对抗论证形式化框架，将对抗性命题和反驳结构化为范畴中的对象和态射，利用函子、自然变换和极限概念进行结构化对抗分析。

## 授权/许可
MIT

## 下载源
https://github.com/user/CGT (Category-Theoretic Argumentation，待确认)

## 集成节点
- **T13 (认知综合)**: 将不同视角的论证结构化为范畴，通过函子映射发现视角间的结构对应与差异
- **TM03 (对抗综合)**: 利用范畴论的极限/余极限概念实现多视角对抗论点的结构化综合，生成超越单一视角的元视角

## tool-availability 探测
```bash
# 检测CGT形式化工具
python -c "import cgt; print('CGT available')" 2>/dev/null || echo "CGT not installed"
# 备选：使用Catlab进行范畴论计算
python -c "import catlab; print('Catlab available')" 2>/dev/null
```

## 穷尽重试替代链
若不可用 → 穷尽重试替代为 Catlab (TC-076) 范畴论计算 + 手动对抗结构映射；或穷尽重试替代为论证图（Argumentation Framework）+ Dung语义

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

| 节点 | 用途 |
|------|------|
| T13 | 范畴论对抗形式化 |
| TM03 | 对抗综合 |

