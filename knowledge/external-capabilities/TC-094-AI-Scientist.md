<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

# TC-094: AI-Scientist — 科学发现流水线

> ★核心方法论已内化于 extensions/scientific-discovery.md

## 基本信息
- **名称**: AI-Scientist
- **类别**: 科学发现
- **语言**: Python
- **许可证**: MIT
- **仓库**: https://github.com/SakanaAI/AI-Scientist

## 核心能力
- 假设生成（三种变异操作：组合/方向/反事实）
- H_score假设评估（0.4×新颖度 + 0.3×可行性 + 0.3×影响力）
- 实验类型决策树（RCT/quasi-experimental/observational/simulation/formal_verification/A/B_test）
- 实验评估（p_value<0.05 且 effect_size>0.2→SUPPORTED）
- 自动化科学方法全流程（假设→实验→代码→论文）

## 在 profound-cognition 中的用途
- **scientific-discovery.md**: 科学发现核心执行引擎

## 消费节点
- scientific-discovery.md

## 消费关系

### 消费此卡片的 DAG 节点

暂无显式 DAG 节点消费者。保留待扩展。

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的扩展模块

- extensions/scientific-discovery.md（科学发现核心执行引擎）

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