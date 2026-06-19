<!-- 作者：阿洋 -->

# MECE分解

> 知识来源: MC-159 MECE分解 (MECE-Prioritization)

## 方法论原理

MECE优先级排序的方法论基础是：**分析的质量不仅取决于"想到了什么"，更取决于"先想什么、后想什么、忽略什么"**。MECE（Mutually Exclusive, Collectively Exhaustive）递归分解确保分析覆盖的完备性和不重叠性，而优先级排序确保有限认知资源被分配到最有价值的分析方向。最常见的分析失败不是"没想到"，而是"想到了但没来得及深入"——在有限时间内平均分配精力导致所有方向都浅尝辄止。八维分析矩阵为MECE分解提供了维度框架，优先级公式 P = I × (11-U) 为排序提供了量化标准。

## 执行步骤

1. **定义核心问题**：将分析目标表述为明确的疑问句，确保问题边界清晰
2. **MECE递归分解**：按八维矩阵（D-POL, D-ECO, D-SOC, D-TEC, D-ENV, D-LEG, D-ETH, D-PSY）分解为子问题，检验互斥性和穷尽性，递归深度通常2-3层
3. **影响度评估**：对每个叶子子问题评估解释力 I（1-10分）
4. **不确定度评估**：对每个叶子子问题评估证据充分程度 U（1-10分）
5. **优先级计算**：P = I × (11 - U)，高分=影响力大且信息不足，最优先处理
6. **排序与资源分配**：按优先级排序，80%资源分配给前20%高优先级子问题（帕累托原则）
7. **动态调整**：随新证据获取更新I和U值，重新计算优先级

## 决策规则

| 优先级区间 | 分类 | 资源分配 | 处理方式 |
|-----------|------|---------|---------|
| P ≥ 70 | 关键优先 | 分配40%资源 | 必须深入分析，产出确定性结论 |
| 40 ≤ P < 70 | 重要优先 | 分配30%资源 | 需要分析但可接受部分不确定性 |
| 20 ≤ P < 40 | 一般优先 | 分配20%资源 | 快速扫描，标注关键发现 |
| P < 20 | 低优先 | 分配10%资源 | 仅做定性标注，不深入分析 |

| MECE检验结果 | 判定 | 行动 |
|-------------|------|------|
| 互斥性失败 | 分解不干净 | 合并重叠子问题或重新定义边界 |
| 穷尽性失败 | 分解不完整 | 补充遗漏维度的子问题 |
| 两者均通过 | MECE合格 | 继续优先级评估 |

## 输出规范

```yaml
mece_decomposition_output:
  available: bool
  core_question: str
  decomposition:
    depth: int
    mece_check:
      mutual_exclusivity: "pass/fail/approximate"
      collective_exhaustiveness: "pass/fail/approximate"
    leaf_nodes:
      - id: str
        question: str
        dimension: str
        impact_score: int
        uncertainty_score: int
        priority_score: int
        priority_tier: str
  resource_allocation:
    critical_priority: str
    important_priority: str
  degradation_note: str
```

## 穷尽重试策略

| 级别 | 条件 | 方案 |
|------|------|------|
| L1 | 八维均可评估且有足够信息 | 完整执行7步，输出量化优先级排序 |
| L2 | 部分维度信息不足 | 对有信息的维度做量化评估，其余标注"信息不足" |
| L3 | 无量化信息但可做定性判断 | 对I和U做定性评估（高/中/低），转化为数值后计算 |
| L4 | 问题过于复杂无法做MECE分解 | 列举已知子问题但不保证MECE，标注"非MECE列举" |
