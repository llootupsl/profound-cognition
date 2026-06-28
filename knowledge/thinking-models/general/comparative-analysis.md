<!-- 作者：阿洋 -->

# 比较分析

> 知识来源: MC-164 比较分析 (Comparison-Significance)

## 方法论原理

比较-显著性分析的方法论基础是：**类比推理的有效性不仅取决于结构同构性，还取决于比较的统计显著性——两个领域的相似性是否超出了随机期望**。当类比基于大量特征比较时，需要区分"系统性相似"（超出随机期望的结构性对应）和"偶然相似"（随机产生的表面重合）。最常见的类比错误是"过度解读偶然相似"——将随机重合的特征当作深层结构同构的证据。

## 执行步骤

1. **特征枚举**：列出源域和目标域的所有可比特征
2. **相似特征计数**：统计两个领域中相似的特征数量
3. **随机期望计算**：在零假设下，计算随机产生该相似度的期望值
4. **显著性判定**：若实际相似度显著高于随机期望 → 结构性相似；否则 → 偶然相似
5. **异同矩阵构造**：构建系统性的异同对比矩阵
6. **差异显著性评估**：评估差异是否具有统计显著性
7. **根因追溯**：对显著差异进行L1-L4四层级归因（表面差异/结构差异/机制差异/范式差异）

## 决策规则

| 显著性水平 | 判定 | 行动 |
|-----------|------|------|
| p < 0.01 | 高度显著相似 | 类比推理可靠，可作为强推理依据 |
| p < 0.05 | 显著相似 | 类比推理较可靠，可作为中等推理依据 |
| p < 0.10 | 边缘显著 | 类比推理弱，仅作启发参考 |
| p ≥ 0.10 | 不显著 | 相似性可能为偶然，禁止类比推理 |

## 输出规范

```yaml
comparative_analysis_output:
  available: bool
  source_domain: str
  target_domain: str
  features_compared: int
  similar_features: int
  random_expectation: float
  significance_level: str
  conclusion: "highly_significant/significant/marginal/not_significant"
  analogical_strength: "strong/moderate/weak/unreliable"
  difference_matrix:
    - feature: str
      source_value: str
      target_value: str
      difference_type: "surface/structural/mechanistic/paradigmatic"
  root_cause_attribution: [str]
  degradation_note: str
```

## 穷尽重试策略

| 级别 | 条件 | 方案 |
|------|------|------|
| L1 | 特征可枚举、随机期望可计算 | 完整7步，输出显著性水平 |
| L2 | 随机期望无法精确计算 | 使用近似估计，标注"近似显著性" |
| L3 | 仅可做特征计数 | 统计相似特征比例，标注"无显著性检验" |
| L4 | 无法枚举特征 | 做定性相似判断，标注"定性比较" |
