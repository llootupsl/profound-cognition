---
name: TC-071-CozoDB

> ★核心方法论已内化于 tasks/TM07_ontology_export.md，本文件仅作快速引用入口

description: Datalog传递推理图数据库，支持递归规则和时态图查询
version: "1.0"
category: external-tool
consuming_engines: []
integrated_nodes: [TM07, T15b]
---

<!-- 作者：阿洋 -->


# TC-071: CozoDB — Datalog传递推理

## 用途
基于Datalog的嵌入式图数据库，支持递归规则查询，用于知识图谱中的传递闭包推理和多跳关系推导。

## 授权/许可
Apache 2.0 / AGPL-3.0 (双许可)

## 下载源
https://github.com/cozodb/cozo

## 集成节点
- **TM07 (本体导出)**: 作为知识图谱的持久化后端，利用Datalog递归规则进行本体一致性检查和传递推理
- **T15b (跨域矩阵)**: 存储和查询跨域知识图谱，利用Datalog规则发现隐含的跨域关系

## tool-availability 探测
```bash
# 检测CozoDB是否安装
python -c "import pycozo; print('CozoDB available')" 2>/dev/null || echo "CozoDB not installed"
# 或检测Docker部署
docker ps | grep cozo
```

## 穷尽重试替代链
若不可用 → 穷尽重试替代为 NetworkX 传递闭包 + 手动递归查询；或穷尽重试替代为 SQLite 递归 CTE

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

| 节点 | 用途 |
|------|------|
| TM07 | Datalog传递推理 |
| T15b | 跨域知识图谱 |

