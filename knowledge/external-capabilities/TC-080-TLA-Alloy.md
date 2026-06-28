---
name: TC-080-TLA-Alloy

> ★核心方法论已内化于 tasks/TM02_causal_verification.md，本文件仅作快速引用入口

description: 形式化模型检查工具，用于系统规范验证和一致性检查
version: "1.0"
category: external-tool
consuming_engines: []
integrated_nodes: [TM01, TM06]

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

# TC-080: TLA+/Alloy — 形式化模型检查

## 用途
TLA+（Temporal Logic of Actions）和Alloy是形式化规范语言和模型检查工具，用于验证系统设计的一致性和安全性属性，确保认知流水线的逻辑正确性。

## 授权/许可
MIT (TLA+) / MIT (Alloy)

## 下载源
- TLA+: https://github.com/tlaplus/tlaplus
- Alloy: https://github.com/AlloyTools/org.alloytools.alloy

## 集成节点
- **TM01 (系统动力学)**: 使用TLA+形式化验证系统动力学模型中的状态转换逻辑，确保反馈循环和因果链的一致性
- **TM06 (元层验证)**: 使用Alloy对认知流水线的元层规范进行模型检查，验证无死锁、无活锁等安全性属性

## tool-availability 探测
```bash
# 检测TLA+
java -jar tla2tools.jar -version 2>/dev/null || echo "TLA+ not available"
# 检测Alloy
java -jar alloy.jar -version 2>/dev/null || echo "Alloy not available"
# 或Python封装
python -c "import alloy; print('Alloy Python available')" 2>/dev/null
```

## 穷尽重试替代链
若不可用 → 穷尽重试替代为手动状态机验证 + 不变式标注；或穷尽重试替代为 P 语言 (p-org.github.io/P)

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

| 节点 | 用途 |
|------|------|
| TM01 | 形式化模型检查 |
| TM06 | 元层验证 |

