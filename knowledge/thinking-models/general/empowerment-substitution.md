<!-- 作者：阿洋 -->

# 赋能-替代

> 知识来源: MC-176 赋能-替代 (Empowerment-Substitution)

## 方法论原理

赋能-替代分析的方法论基础是：**技术对社会的效应不是单一的"好"或"坏"，而是同时包含赋能（创造新能力/新市场/新岗位）和替代（消灭旧方案/旧岗位/旧市场）两个维度**。将这两个维度交叉形成四象限矩阵：破坏性重构（高赋能+高替代）、就业摧毁（低赋能+高替代）、生产力提升（高赋能+低替代）、边际改良（低赋能+低替代）。这一方法论之所以必要，是因为对技术效应最常见的误判是"单向思维"——只看到赋能忽略替代（技术乐观主义），或只看到替代忽略赋能（技术悲观主义）。

## 执行步骤

1. **技术范围界定**：明确目标技术及其影响的行业和岗位
2. **赋能效应评估**：识别新能力、新市场、效率提升，量化新增岗位和市场价值
3. **替代效应评估**：识别被替代方案、岗位和市场，量化消失岗位和萎缩市场价值
4. **象限定位**：基于赋能得分和替代得分，在四象限矩阵中定位
5. **分配分析**：评估受益群体与受损群体的重叠程度，识别分配断裂和弱势群体影响
6. **策略推荐**：基于象限位置和分配分析，推荐主动转型/社会保障/技能升级/维持现状

## 决策规则

| 象限 | 赋能强度 | 替代强度 | 特征 | 策略 |
|------|---------|---------|------|------|
| 破坏性重构 | 高（E > 中位） | 高（S > 中位） | 旧秩序瓦解，新秩序建立 | 主动转型+社会保障并行 |
| 就业摧毁 | 低（E ≤ 中位） | 高（S > 中位） | 岗位消失但无新岗位替代 | 社会保障+技能升级 |
| 生产力提升 | 高（E > 中位） | 低（S ≤ 中位） | 效率提升但就业基本稳定 | 技能升级+效率红利分享 |
| 边际改良 | 低（E ≤ 中位） | 低（S ≤ 中位） | 增量有限，行业基本不变 | 维持现状，关注潜在升级 |

| 分配条件 | 判定 | 行动 |
|---------|------|------|
| 受益群体与受损群体高度重叠 | 自我补偿 | 重点提供过渡支持 |
| 受益群体与受损群体不重叠 | 分配断裂 | 需要显式再分配机制 |
| 受损群体为弱势群体 | 公平风险 | 必须设计针对性保护措施 |
| 受益群体为强势群体 | 权力集中风险 | 需反垄断和开放政策 |

## 输出规范

```yaml
empowerment_substitution_output:
  available: bool
  technology_scope:
    name: str
    affected_industries: [str]
    affected_occupations: [str]
  empowerment_effects:
    new_capabilities: [str]
    new_markets: [str]
    efficiency_gains: [str]
    empowerment_strength: "high/medium/low"
  substitution_effects:
    replaced_solutions: [str]
    replaced_occupations: [str]
    replaced_markets: [str]
    substitution_strength: "high/medium/low"
  quadrant_position:
    quadrant: "disruptive_reconstruction/job_destruction/productivity_enhancement/marginal_improvement"
    empowerment_score: float
    substitution_score: float
  distribution_analysis:
    benefit_groups: [str]
    harm_groups: [str]
    overlap: str
    distribution_fracture: bool
  strategy_recommendation:
    primary_strategy: str
    distribution_mechanism: str
  degradation_note: str
```

## 穷尽重试策略

| 级别 | 条件 | 方案 |
|------|------|------|
| L1 | 赋能和替代效应均可量化 | 完整执行6步，输出精确象限定位 |
| L2 | 仅部分效应可量化 | 量化可量化部分，其余定性评估，标注"半定量" |
| L3 | 无量化数据但可知技术方向 | 基于技术特征做定性象限判定，标注"定性推断" |
| L4 | 无本技术数据但有类似技术先例 | 引用类似技术的赋能-替代历史，标注"类比推断" |
