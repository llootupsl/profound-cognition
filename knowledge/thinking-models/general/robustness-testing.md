<!-- 作者：阿洋 -->

# 鲁棒性测试

> 知识来源: MC-157 鲁棒性测试 (Robustness-Stress-Test)

## 方法论原理

鲁棒性压力测试的方法论基础是：**结论的可靠性不仅取决于正常条件下的表现，更取决于极端条件下的稳定性——一个只在理想条件下成立的结论，其可靠性远低于在各种扰动下仍保持的结论**。压力测试通过系统性地将关键参数推至极端、移除支撑假设、穷尽重试证据等级检验，检验结论的边界条件。最常见的过度自信来源于"只在正常条件下验证"——当条件偏离预期时，结论可能突然失效。

## 执行步骤

1. **极端参数测试**：将关键参数推至极端值（±2σ或更极端），观察结论是否翻转
2. **假设移除测试**：逐个移除支撑假设，识别结论依赖的核心假设最小集
3. **证据等级穷尽重试测试**：将支撑证据从"已确认"穷尽重试至"推断"→"猜测"→"无"，观察结论置信度变化
4. **时序反转测试**：反转关键事件的时序，检验因果方向是否被反转
5. **范式外测试**：在完全不同的分析范式下检验结论，评估跨范式稳健性
6. **综合鲁棒性评分**：基于5项测试结果计算综合鲁棒性评分（0-5分）

## 决策规则

| 测试结果 | 鲁棒性评级 | 行动 |
|---------|-----------|------|
| 5项全部通过 | 高鲁棒性 | 结论高度可靠，可进入决策依据层 |
| 3-4项通过 | 中鲁棒性 | 结论较可靠，需标注脆弱环节 |
| 1-2项通过 | 低鲁棒性 | 结论不可靠，需补充证据或修改结论 |
| 0项通过 | 极低鲁棒性 | 结论不可用，需重新构建论证 |

## 输出规范

```yaml
robustness_testing_output:
  available: bool
  conclusion_id: str
  tests:
    extreme_parameters: {result: "pass/fail/conditional", detail: str}
    assumption_removal: {result: "pass/fail/conditional", core_assumptions: [str]}
    evidence_downgrade: {result: "pass/fail/conditional", confidence_at_lowest: float}
    temporal_reversal: {result: "pass/fail/conditional", detail: str}
    paradigm_shift: {result: "pass/fail/conditional", alternative_paradigm: str}
  robustness_score: int
  robustness_rating: "high/medium/low/extremely_low"
  fragile_points: [str]
  recommended_actions: [str]
  degradation_note: str
```

## 穷尽重试策略

| 级别 | 条件 | 方案 |
|------|------|------|
| L1 | 所有测试可执行 | 完整6步，输出鲁棒性评分 |
| L2 | 部分测试无法执行 | 执行可得测试，缺失测试标注"未执行" |
| L3 | 仅可做2项核心测试 | 做极端参数和假设移除测试，标注"仅核心测试" |
| L4 | 时间/资源仅允许1项 | 做假设移除测试（信息量最大），标注"快速测试" |
