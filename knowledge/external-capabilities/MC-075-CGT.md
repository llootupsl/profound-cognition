---
name: MC-075-CGT

> ★核心方法论已内化于 tasks/TM07_ontology_export.md，本文件仅作快速引用入口

description: 范畴论对抗形式化框架，用于结构化对抗论证的数学表示
version: "1.0"
category: external-tool
consuming_engines: []
integrated_nodes: [T13, TM03]

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

