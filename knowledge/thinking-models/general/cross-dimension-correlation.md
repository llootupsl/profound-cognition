<!-- 作者：阿洋 -->

# 交叉维度关联

> 知识来源: MC-177 交叉维度关联 (Cross-Dimension-Correlation)

## 方法论原理

跨维度关联分析的方法论基础是：**全息框架的各维度之间不是独立的，而是存在复杂的交叉影响——一个维度的变化会通过直接和间接路径影响其他维度**。8×8交叉影响矩阵量化了每对维度之间的影响方向和强度，揭示了关键影响路径、反馈回路和枢纽维度。这一方法论之所以必要，是因为最常见的分析错误是"维度孤立"——在每个维度内部分析得很深入，但忽略了维度间的传导效应和反馈回路，导致对系统性风险的低估。

## 执行步骤

1. **维度定义**：确认全息框架的8个维度（D-POL, D-ECO, D-SOC, D-TEC, D-ENV, D-LEG, D-ETH, D-PSY）
2. **直接影响评估**：对每对维度 (D_i, D_j)，评估 D_i 对 D_j 的直接影响方向（增强/减弱/无关）和强度（1-5分）
3. **间接影响追踪**：通过矩阵乘法计算间接影响路径
4. **敏感性排名**：计算每个维度的敏感性得分（被影响程度）和影响力得分（影响他人程度）
5. **关键路径识别**：识别3-5条最强的跨维度影响路径
6. **反馈回路检测**：识别正反馈和负反馈回路
7. **枢纽维度定位**：识别高敏感+高影响力的枢纽维度

## 决策规则

| 敏感性/影响力模式 | 维度类型 | 分析重点 |
|-----------------|---------|---------|
| 高敏感+高影响力 | 枢纽维度 | 最关键的分析焦点，变化会传导到所有维度 |
| 高敏感+低影响力 | 接收维度 | 主要受其他维度影响，需关注上游变化 |
| 低敏感+高影响力 | 驱动维度 | 是其他维度变化的源头，需重点监控 |
| 低敏感+低影响力 | 边缘维度 | 对系统影响有限，可降低分析优先级 |

| 反馈回路类型 | 判定 | 行动 |
|------------|------|------|
| 正反馈回路 | 自强化循环，可能导致系统失衡 | 识别回路中的阻断点，评估失衡风险 |
| 负反馈回路 | 自稳定循环，有助于系统均衡 | 评估回路的稳定效能是否充足 |

## 输出规范

```yaml
cross_dimension_correlation_output:
  available: bool
  dimensions: [str]
  influence_matrix:
    - from_dimension: str
      to_dimension: str
      direction: "enhance/weaken/neutral"
      strength: int
  sensitivity_ranking:
    - dimension: str
      sensitivity_score: float
      rank: int
      primary_influences_from: [str]
  influence_ranking:
    - dimension: str
      influence_score: float
      rank: int
      primary_influences_to: [str]
  critical_paths:
    - path: [str]
      cumulative_strength: float
      description: str
  feedback_loops:
    - loop: [str]
      type: "positive/negative"
      strength: str
      description: str
  key_hub_dimensions: [str]
  degradation_note: str
```

## 穷尽重试策略

| 级别 | 条件 | 方案 |
|------|------|------|
| L1 | 所有64个交叉影响可评估 | 完整执行7步，输出精确矩阵和排名 |
| L2 | 部分维度间关系不可评估 | 评估可得关系，不可评估标注"未评估" |
| L3 | 无法构建完整矩阵但可识别关键路径 | 仅识别3-5条最关键跨维度路径 |
| L4 | 无量化数据 | 对每对维度做定性影响判断，不做强度量化 |
