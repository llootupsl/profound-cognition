<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

# TC-088: Axelrod — 囚徒困境策略演化

> ★核心方法论已内化于 knowledge/thinking-models/decision/game-theory.md

## 基本信息
- **名称**: Axelrod
- **类别**: 博弈论/演化模拟
- **语言**: Python
- **许可证**: MIT
- **仓库**: https://github.com/Axelrod-Python/Axelrod

## 核心能力
- 230+策略库（TFT/GTFT/WSLS/Zero-Determinant等）
- 锦标赛模拟（Tournament）
- Moran过程种群演化
- 策略匹配与对抗分析
- 重复博弈策略分析

## 在 profound-cognition 中的用途
- **T09**: 重复博弈策略分析
- **T15**: 策略演化模拟

## 消费节点
- T09
- T15

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