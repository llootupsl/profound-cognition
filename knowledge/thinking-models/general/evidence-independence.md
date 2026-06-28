<!-- 作者：阿洋 -->

# 证据独立性

> 知识来源: MC-170 证据独立性 (Evidence-Independence)

## 方法论原理

证据独立性检验的方法论基础是：**多条独立证据的联合支持力远大于多条相关证据——因为相关证据可能共享同一错误来源，导致"虚假的强支持"**。当多条证据实际上来自同一信息源或受同一混淆因素影响时，它们看起来各自独立支持结论，但实际上只提供了一次支持。最常见的过度自信来源于"证据数量幻觉"——看到5条支持证据就认为结论很可靠，但若5条证据都来自同一来源，实际支持力只有1条。

## 执行步骤

1. **证据来源追溯**：对每条证据，追溯其原始来源（数据源、研究团队、方法论）
2. **同源检测**：检查是否有证据共享同一原始来源
3. **依赖检测**：检查是否有证据因果依赖于另一条证据
4. **共因检测**：检查是否有证据受同一混淆因素驱动
5. **独立性评分**：对每条证据标注独立性等级（独立/部分独立/依赖/同源）
6. **有效证据计数**：仅计独立证据数量，重新评估结论支持度

## 决策规则

| 独立性等级 | 判定 | 处理方式 |
|-----------|------|---------|
| 独立 | 不同来源、不同方法 | 全部计入有效证据 |
| 部分独立 | 部分共享来源或方法 | 计为0.5条有效证据 |
| 依赖 | 一条证据因果依赖另一条 | 合并为1条复合证据 |
| 同源 | 来自同一原始来源 | 合并为1条证据，标注"同源" |

## 输出规范

```yaml
evidence_independence_output:
  available: bool
  evidence_list:
    - id: str
      source: str
      independence_level: "independent/partially_independent/dependent/co_sourced"
      related_evidence: [str]
      relationship_type: "same_source/causal_dependency/common_cause/none"
  effective_evidence_count: int
  raw_evidence_count: int
  independence_ratio: float
  adjusted_conclusion_support: str
  degradation_note: str
```

## 穷尽重试策略

| 级别 | 条件 | 方案 |
|------|------|------|
| L1 | 证据来源可追溯 | 完整6步，输出有效证据计数 |
| L2 | 部分证据来源不可追溯 | 对可追溯证据做检验，不可追溯标注"来源未知" |
| L3 | 仅可做同源检测 | 检查是否有明显同源证据，标注"仅同源检查" |
| L4 | 无法做任何独立性分析 | 标注原始证据数量，警告"未检验独立性" |
