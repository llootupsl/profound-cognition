<!-- 作者：阿洋 -->

# 反事实推理

> 知识来源: MC-155 反事实推理 (Assumption-Counterfactual)
> **完整方法论已在 `knowledge/thinking-models/general/critical-thinking.md` §11 中内化，本文为独立参考**

## 方法论原理

假设-反事实推演的方法论基础是：**论证的可靠性取决于其关键假设的可靠性，而检验假设最有效的方法是构造反事实——如果该假设不成立，结论会发生什么变化**。这一方法论将假设挖掘和反事实推演整合为统一流程：先挖掘假设，再对每个关键假设构造反事实，最后评估反事实对结论的影响。单独的假设挖掘容易流于"列举仪式"，而单独的反事实推演容易脱离论证结构——两者结合才能精确识别论证的脆弱环节。

## 执行步骤

1. **假设挖掘**：使用三层假设挖掘框架，识别显性/隐性/深层假设
2. **假设排序**：按 criticality × uncertainty 排序，聚焦红色假设（高关键性+高不确定性）
3. **反事实构造**：对每个红色假设，构造"如果该假设为假"的反事实场景
4. **反事实推演**：对每个反事实，推演至少3步因果链
5. **影响评估**：评估反事实对原始结论的影响（翻转/削弱/不变/加强）
6. **鲁棒性判定**：若任一红色假设的反事实翻转结论 → 标注"结论脆弱"

## 决策规则

| 反事实影响 | 判定 | 行动 |
|-----------|------|------|
| 结论被翻转 | 致命脆弱 | 必须验证该假设，否则结论不可信 |
| 结论被显著削弱 | 重要脆弱 | 需验证该假设，降低结论置信度 |
| 结论基本不变 | 鲁棒 | 该假设非关键支撑，可接受不确定性 |
| 多个反事实均翻转结论 | 极度脆弱 | 重新构建论证体系 |

## 输出规范

```yaml
counterfactual_reasoning_output:
  available: bool
  assumptions:
    - id: str
      statement: str
      layer: "explicit/implicit/hidden"
      criticality: "high/medium/low"
      uncertainty: "high/medium/low"
      risk_label: "red/yellow/green/gray"
  counterfactuals:
    - assumption_id: str
      counterfactual: str
      causal_chain: [str]
      impact: "conclusion_flipped/conclusion_weakened/conclusion_unchanged/conclusion_strengthened"
  robustness_verdict: "robust/moderately_fragile/fragile/extremely_fragile"
  critical_assumptions_to_verify: [str]
  degradation_note: str
```

## 穷尽重试策略

| 级别 | 条件 | 方案 |
|------|------|------|
| L1 | 假设可挖掘、反事实可推演 | 完整6步，输出鲁棒性判定 |
| L2 | 部分假设无法构造反事实 | 对可推演假设做反事实，其余标注"反事实不可构造" |
| L3 | 反事实无法推演因果链 | 做假设挖掘+定性影响判断，标注"定性反事实" |
| L4 | 无法构造反事实 | 仅做假设挖掘和排序，标注"无反事实推演" |
