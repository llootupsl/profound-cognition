<!-- 作者：阿洋 -->

# 触发-结构耦合

> 知识来源: MC-174 触发-结构耦合 (Trigger-Structure-Coupling)

## 方法论原理

触发事件-结构条件耦合分析的方法论基础是：**社会变革从来不是单一因素驱动的，而是"触发事件"（火花）与"结构条件"（干柴）的耦合结果**。没有结构条件的触发事件只是火花落在湿木上——瞬间闪烁后熄灭；没有触发事件的结构条件是充满沼气的空间但无人点火——潜在能量巨大但无法释放。对变革最常见的误判是"触发事件过度归因"——将长期累积的结构变化归因于最近的轰动事件，或反过来"结构决定论"——认为结构条件成熟后变革必然发生而忽略触发事件的必要性。耦合分析强制要求同时评估两个维度及其交互强度。

## 执行步骤

1. **触发事件分类**：将触发事件分为危机型、丑闻型、技术型、象征型、外部型五类，评估可见性和情绪冲击
2. **结构条件评估（5层）**：评估经济结构层、制度结构层、社会结构层、文化结构层、技术结构层的成熟度（未成熟/部分成熟/高度成熟）
3. **耦合强度判定**：评估触发事件与结构条件的耦合强度（弱耦合/中耦合/强耦合/超耦合）
4. **变革路径预测**：基于耦合强度和结构条件成熟度，预测变革的可能路径和时间窗口
5. **反向运动评估**：评估结构条件中是否存在反对变革的强固结构，以及触发事件是否同时激活了反向运动

## 决策规则

| 耦合强度 | 结构成熟度 | 变革预测 | 策略建议 |
|---------|-----------|---------|---------|
| 超耦合 | 高度成熟 | 变革已不可逆 | 顺应变革，参与新秩序构建 |
| 强耦合 | 高度成熟 | 快速变革即将发生 | 积极准备，抢占变革先机 |
| 强耦合 | 部分成熟 | 不完全变革，可能停滞 | 推动结构条件成熟，防止变革被收编 |
| 中耦合 | 高度成熟 | 等待更强触发 | 创造或等待触发事件，保持结构压力 |
| 中耦合 | 部分成熟 | 缓慢渐进变革 | 持续积累结构条件，不急于求成 |
| 弱耦合 | 任意 | 无实质变革 | 不做变革预期，关注结构条件变化 |
| 任意 | 未成熟 | 变革条件不具备 | 首先推动结构条件成熟 |

## 输出规范

```yaml
trigger_structure_coupling_output:
  available: bool
  trigger_events:
    - event: str
      type: "crisis/scandal/technology/symbolic/external"
      visibility: str
      emotional_impact: str
  structural_conditions:
    economic: {maturity: str, evidence: str}
    institutional: {maturity: str, evidence: str}
    social: {maturity: str, evidence: str}
    cultural: {maturity: str, evidence: str}
    technological: {maturity: str, evidence: str}
    overall_maturity: str
  coupling_assessment:
    strength: "weak/medium/strong/super"
    mechanism: str
    feedback_loop: str
  change_path_prediction:
    path_type: str
    timeline: str
    confidence: float
  degradation_note: str
```

## 穷尽重试策略

| 级别 | 条件 | 方案 |
|------|------|------|
| L1 | 触发事件和结构条件均可评估 | 完整执行5步，输出精确耦合判定 |
| L2 | 部分结构层数据不可得 | 评估可得层，缺失层标注"未评估" |
| L3 | 仅触发事件可分析 | 仅做触发事件分类，标注"结构条件未知" |
| L4 | 无明确触发事件 | 仅做结构条件5层评估，标注"触发事件缺失" |
