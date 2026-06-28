<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

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

## 消费关系

### 消费此卡片的 DAG 节点

暂无显式 DAG 节点消费者。保留待扩展。

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的能力卡

- TC-063 MetaNet（底层执行引擎，C++后端十亿级边）

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