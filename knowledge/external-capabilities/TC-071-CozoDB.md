---
name: TC-071-CozoDB

> ★核心方法论已内化于 tasks/TM07_ontology_export.md，本文件仅作快速引用入口

description: Datalog传递推理图数据库，支持递归规则和时态图查询
version: "1.0"
category: external-tool
consuming_engines: []
integrated_nodes: [TM07, T15b]

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

