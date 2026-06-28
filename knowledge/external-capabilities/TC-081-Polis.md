---
name: TC-081-Polis

> ★核心方法论已内化于 tasks/T13_cog_synthesis.md，本文件仅作快速引用入口

description: 共识发现与意见可视化平台，用于大规模群体意见聚合
version: "1.0"
category: external-tool
consuming_engines: []
integrated_nodes: [TM03, T07b]

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

