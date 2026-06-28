---
name: TC-076-Catlab

> ★核心方法论已内化于 tasks/T03b_cross_axis_matrix.md，本文件仅作快速引用入口

description: 范畴论计算库，支持同构类比和函子映射
version: "1.0"
category: external-tool
consuming_engines: []
integrated_nodes: [T15b]

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

