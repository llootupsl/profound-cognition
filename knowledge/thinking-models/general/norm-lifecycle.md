<!-- 作者：阿洋 -->

# 规范生命周期

> 知识来源: MC-163 规范生命周期 (Norm-Lifecycle)

## 方法论原理

社会规范生命周期的方法论基础是：**社会规范不是静态的规则，而是经历从禁忌→争议→主流化→制度化→理所当然的动态演化过程**。每个阶段有独特的特征指标和转换条件，理解规范所处的阶段可以预测其演化方向和速度。这一方法论之所以必要，是因为对规范最常见的误判是"将当前状态视为永恒"——将制度化规范视为理所当然而忽视其历史偶然性，或将争议期规范视为不可能改变而忽视其演化趋势。

## 执行步骤

1. **规范定义**：明确目标规范的内容、类型（禁止性/倡导性）和边界
2. **五指标评估**：评估媒体话语、法律地位、多数态度、违反成本、代际差异五个指标，每个指标标注所处阶段
3. **阶段定位**：基于五指标的综合评估，确定规范当前所处阶段（禁忌/争议/主流化/制度化/理所当然）
4. **转换条件分析**：分析从当前阶段到下一阶段的触发条件满足程度
5. **变革速度预测**：基于触发条件的满足程度，预测阶段转换的时间窗口
6. **反向运动分析**：识别并评估反对规范变革的反向运动的规模、资源和叙事

## 决策规则

| 当前阶段 | 下一阶段触发条件满足度 | 预测 | 行动 |
|---------|---------------------|------|------|
| 禁忌 | 触发条件满足 < 30% | 长期停滞在禁忌期 | 不预期短期变化，关注潜在触发事件 |
| 禁忌 | 触发条件满足 30%-70% | 即将进入争议期 | 密切监测精英分裂和可视性事件 |
| 争议 | 触发条件满足 < 30% | 长期停留在争议期 | 关注代际更替进程和替代叙事出现 |
| 争议 | 触发条件满足 30%-70% | 即将进入主流化 | 准备主流化后的制度设计 |
| 争议 | 触发条件满足 > 70% | 快速进入主流化 | 加速制度准备，防止制度化滞后 |
| 主流化 | 触发条件满足 > 50% | 即将制度化 | 推动立法/政策进程 |
| 制度化 | 触发条件满足 > 50% | 逐步成为理所当然 | 维护制度，防止倒退 |
| 任意阶段 | 反向运动强度 > 推动力 | 可能阶段倒退 | 评估倒退风险，制定防御策略 |

## 输出规范

```yaml
norm_lifecycle_output:
  available: bool
  target_norm:
    description: str
    norm_type: "prohibitive/advocatory"
  stage_assessment:
    media_discourse: {indicator: str, evidence: str}
    legal_status: {indicator: str, evidence: str}
    majority_attitude: {indicator: str, evidence: str}
    violation_cost: {indicator: str, evidence: str}
    generational_difference: {indicator: str, evidence: str}
    current_stage: str
    inconsistent_indicators: [str]
  transition_conditions:
    next_stage: str
    overall_satisfaction: str
    estimated_transition_time: str
  backlash_movement:
    exists: bool
    strength: str
    regression_risk: str
  degradation_note: str
```

## 穷尽重试策略

| 级别 | 条件 | 方案 |
|------|------|------|
| L1 | 所有指标数据可得 | 完整执行6步，输出精确阶段定位 |
| L2 | 部分指标数据不可得 | 用可得指标评估，缺失指标标注"未评估" |
| L3 | 仅有一个指标可得 | 基于该指标做阶段推断，标注"单指标推断，置信度低" |
| L4 | 无本规范数据但有类似规范先例 | 引用类似规范的演化历史，标注"类比推断" |
