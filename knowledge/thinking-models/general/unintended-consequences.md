<!-- 作者：阿洋 -->

# 非预期后果

> 知识来源: MC-173 非预期后果 (Unintended-Consequences)

## 方法论原理

非预期后果检测的方法论基础是：**任何干预都会产生超出预期的影响——效率提高可能引发回弹、规制可能引发替代、公共支出可能挤出私人投资**。五类意外后果（回弹/替代/挤出/补偿/软预算约束）覆盖了政策和技术干预中最常见的非预期效应模式。这一方法论之所以必要，是因为最常见的政策失败不是"没想到目标"，而是"没想到副作用"——干预的直接效果往往符合预期，但间接效应和长期效应常常偏离甚至逆转预期。

## 执行步骤

1. **回弹效应检测**：检验长期弹性是否显著大于短期弹性，计算回弹率 R = (ε_l - ε_s) / ε_s × 100%
2. **替代效应检测**：列出被规制行为的所有可替代方案（至少5个），评估每个替代方案的风险等级，计算替代风险指数 SRI
3. **挤出效应检测**：检验总支出（公共+私人）是增加还是仅转移，计算挤出率
4. **补偿行为检测**：识别安全措施改变的风险感知，估算风险补偿弹性，计算净安全效应
5. **软预算约束检测**：识别是否存在"无法退出"的救助机制，计算软预算约束指数 SBCI = 补贴金额/经营亏损
6. **寻租检测**：执行寻租检测五问清单

## 决策规则

| 后果类型 | 检测阈值 | 判定 | 行动 |
|---------|---------|------|------|
| 回弹率 R < 20% | 政策有效 | 回弹可忽略 | 继续执行 |
| 回弹率 20% ≤ R < 50% | 政策部分有效 | 需补充需求侧措施 | 调整政策组合 |
| 回弹率 R ≥ 50% | 政策效果存疑 | 必须同时实施需求控制 | 重新设计政策 |
| SRI < 被规制行为风险 | 替代效应可控 | 继续执行 | 监测替代行为 |
| SRI ≥ 被规制行为风险 | 替代效应严重 | 扩大规制覆盖面 | 修订政策 |
| 净安全效应 > 0 | 安全措施总体有效 | 继续执行 | — |
| 净安全效应 ≤ 0 | 安全措施被补偿行为抵消 | 需配套行为约束 | 重新设计 |
| SBCI > 0.5 且持续 ≥ 3年 | 软预算约束确认 | 需强制破产/重组机制 | 制度改革 |

## 输出规范

```yaml
unintended_consequences_output:
  available: bool
  intervention: str
  rebound_effect:
    detected: bool
    rebound_rate: float
    severity: "negligible/partial/severe/backfire"
  substitution_effect:
    detected: bool
    alternative_count: int
    substitution_risk_index: float
    severity: "controllable/moderate/severe"
  crowding_out:
    detected: bool
    crowding_rate: float
  compensation_behavior:
    detected: bool
    net_safety_effect: float
  soft_budget_constraint:
    detected: bool
    sbci: float
    duration_years: int
  rent_seeking_risk: "high/medium/low"
  overall_assessment: str
  degradation_note: str
```

## 穷尽重试策略

| 级别 | 条件 | 方案 |
|------|------|------|
| L1 | 五类后果均可量化检测 | 完整6步，输出精确检测指标 |
| L2 | 部分后果可量化 | 量化可量化部分，其余定性评估，标注"半定量" |
| L3 | 仅可做定性后果列举 | 基于五类框架做定性风险判断，标注"定性推断" |
| L4 | 无本干预数据但有类似先例 | 引用类似干预的后果历史，标注"类比推断" |
