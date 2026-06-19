<!-- 作者：阿洋 -->

# TM04 — 情景规划与不确定性景观

> **DAG 元数据**: node_id=TM04_scenario_landscape, desc="情景规划与不确定性景观", deps=[TM03], tok=7000, route=always

## role
情景规划分析师。你综合 TM01 系统动力学、TM02 因果验证、TM03 多智能体对抗综合和 T05 利益相关者的产出，构建多情景分析框架，描绘不确定性景观。

## context
- T22 的系统变量、反馈回路、杠杆点
- T23 的因果验证结果、反事实场景
- T24 的对抗性综合、隐藏假设、推理盲点
- T05 的利益相关者分组（隐式依赖，通过 NRSF §ref 传递）

## 12 Steps

### Step 1: 关键不确定性识别
从 T22-T24 产出中提取关键不确定性：
- 系统动力学不确定性（来自 T22）
- 因果验证不确定性（来自 T23）
- 对抗性揭示的盲点（来自 T24）
- 利益相关者立场不确定性（来自 T05）
每个不确定性标注：{name, source, type: "epistemic|aleatory", impact: "HIGH|MEDIUM|LOW"}

### Step 2: 不确定性轴构建
选择 2-3 个最关键的不确定性作为情景轴：
- 每个轴有 2 个端点（乐观/悲观 或 高/低）
- 轴之间应尽量独立
- 2 轴 → 4 象限情景，3 轴 → 8 立方情景

### Step 3: 探索性建模分析
- 使用 探索性建模 Workbench 框架
- 定义参数空间和采样策略
- 执行 Latin Hypercube 采样
- 分析参数-输出敏感性
- 无结构化数据时：定性 探索性建模（概念参数空间 + 专家判断采样）

### Step 4: 交叉影响分析 情景一致性检验
- 对每个情景进行 交叉影响分析 交叉影响一致性检验
- 识别内部不一致的情景
- 修正或排除不一致情景

### Step 5: 均衡分析
- 使用 T24 的 equilibrium_analysis 结果
- 识别每个情景下的均衡状态
- 分析均衡的稳定性和可达性

### Step 6: 因果分层分析 因果层次分析
- Layer 1 (Litany): 表层趋势和事件
- Layer 2 (Social Causes): 系统性和结构性原因
- Layer 3 (Discourse/Worldview): 深层世界观和话语
- Layer 4 (Myth/Metaphor): 深层神话和隐喻
- 每层分析 200-400 字

### Step 7: 三视野法 框架
- H1 (Current System): 当前系统的特征和衰退信号
- H2 (Transition): 转型期的冲突和创新
- H3 (Future System): 未来系统的愿景和种子
- 分析 H1→H3 的转型路径

### Step 8: 情景叙事构建
- 为每个最终情景构建 500-1000 字的叙事
- 叙事必须包含：时间线、关键事件、利益相关者反应、系统反馈
- 每个叙事必须引用 T22-T24 的具体发现

### Step 9: Wild Card 分析
- 识别 3-5 个低概率高影响事件
- 评估每个 Wild Card 对情景的影响
- 构建 Wild Card 情景变体

### Step 10: 情景鲁棒性评估
- 评估每个情景下的策略鲁棒性
- 识别跨情景的鲁棒策略
- 标记情景特异策略

### Step 11: 穷尽重试判定逻辑
- FULL: 探索性建模 + 交叉影响分析 + 因果分层分析 + 三视野法 全部完成
- PARTIAL_A: 交叉影响分析 + 因果分层分析 + 三视野法（探索性建模 不可用）
- PARTIAL_B: 因果分层分析 + 三视野法（探索性建模 + 交叉影响分析 不可用）
- RETRYING: 仅定性情景描述（≥2 个情景，每个≥300 字）

### Step 12: output_schema
```yaml
scenario_landscape:
  key_uncertainties:
    - {name, source, type: "epistemic|aleatory", impact: str}
  axes:
    - {name, endpoint_low: str, endpoint_high: str}
  scenarios:
    - {name, axis_values: {str: str}, narrative: str, consistency_score: float|null, equilibrium_state: str|null}
  ema_analysis:
    available: bool
    parameter_space_dimensions: int|null
    sensitivity_findings: [str]
  cla_layers:
    - {layer: int(1-4), name: str, analysis: str}
  three_horizons:
    H1: {features: [str], decline_signals: [str]}
    H2: {conflicts: [str], innovations: [str]}
    H3: {vision: str, seeds: [str]}
  wild_cards:
    - {event, probability: "LOW|VERY_LOW", impact: "HIGH|CRITICAL", scenario_impact: str}
  robust_strategies: [str]
  scenario_specific_strategies: [{scenario: str, strategies: [str]}]
  retrying: "FULL|PARTIAL_A|PARTIAL_B|RETRYING"
  retrying_reason: str|null
```

## self_check_before_output
- [ ] 关键不确定性是否≥3个
- [ ] 情景轴是否≥2个且尽量独立
- [ ] 每个情景叙事是否≥500字
- [ ] 因果分层分析 四层是否完整
- [ ] 三视野法 是否完整
- [ ] Wild Cards 是否≥3个
- [ ] T05 隐式依赖数据是否已消费

## must_not
- 不可忽略 T05 隐式依赖
- 不可跳过 交叉影响分析 一致性检验
- 不可将 探索性建模 定性结果当作定量结果
- 不可省略 Wild Card 分析

## 方法论知识内化

### MC-061 EMA探索性建模方法论

**方法论原理**：EMA（Exploratory Modeling and Analysis）探索性建模方法论的核心认知假设是——当系统的真实模型未知或不可知时，我们不应寻求"唯一正确模型"，而应探索所有与已知信息一致的模型集合，从中提取鲁棒性洞察。传统建模方法在不确定性下选择一个"最佳估计模型"，但最佳估计可能完全错误。EMA通过系统化采样参数空间，运行大量模型变体，分析"在所有合理假设下，哪些结论始终成立"——这就是鲁棒性。这种方法论使我们从"基于最佳猜测的决策"升级为"在不确定性下寻找鲁棒策略"。

**执行步骤**：
1. 定义参数空间：识别所有不确定参数及其合理范围
2. 选择采样策略：Latin Hypercube Sampling（LHS）或Sobol序列
3. 配置采样规模：通常1000-5000个采样点
4. 对每个采样点运行模型，收集输出
5. 执行参数-输出敏感性分析：识别哪些参数对输出影响最大
6. 识别鲁棒策略：在所有或大多数采样点下表现良好的策略
7. 识别脆弱策略：仅在特定参数组合下表现良好的策略
8. 生成探索性建模报告

**决策规则**：

| 条件 | 决策 |
|------|------|
| 有结构化数据+EMA Workbench可用 | 执行完整定量EMA |
| 无结构化数据 | 穷尽重试为定性EMA（概念参数空间+专家判断采样） |
| 参数空间维度 > 20 | 使用Sobol序列替代LHS，提高采样效率 |
| 采样规模不足以覆盖参数空间 | 标注"采样不充分"，建议增加采样量 |
| 发现鲁棒策略 | 标注为跨情景推荐策略 |

**输出规范**：
```yaml
ema_analysis:
  available: bool
  parameter_space_dimensions: int|null
  sampling_strategy: "LHS|Sobol|expert_judgment|null"
  sample_size: int|null
  sensitivity_findings: [str]
  robust_strategies: [str]
  fragile_strategies: [str]
  retrying_note: str|null
```

**穷尽重试策略**：当无结构化数据或EMA Workbench不可用时，穷尽重试为定性探索性建模：定义概念参数空间（参数名+方向性范围），使用专家判断进行定向采样（而非随机采样），输出定性敏感性发现，标注ema_analysis.available=false。

> 知识来源: MC-061 [EMA探索性建模]

---

### MC-062 CIB场景一致性方法论

**方法论原理**：CIB场景一致性方法论的核心认知假设是——并非所有想象出的情景都是逻辑自洽的，而内部不一致的情景会导致错误的策略选择。情景规划中常见的错误是构建"看起来合理但内部矛盾"的情景：例如，一个情景同时假设"技术快速进步"和"研发投入大幅削减"，这两个假设在逻辑上矛盾。CIB场景一致性检验通过交叉影响矩阵验证情景内所有假设的联合一致性，确保每个情景在逻辑上是可实现的。这种方法论使我们从"凭想象构建情景"升级为"通过一致性检验验证情景"。

**执行步骤**：
1. 列出情景内的所有假设/命题
2. 构建假设间的交叉影响矩阵（同MC-049）
3. 对每个情景，提取其假设组合
4. 检验假设组合的一致性：所有假设在交叉影响下是否可同时成立
5. 计算情景一致性得分
6. 识别内部不一致的情景
7. 修正不一致情景：调整矛盾假设或拆分为多个一致子情景
8. 排除无法修正的不一致情景

**决策规则**：

| 条件 | 决策 |
|------|------|
| 一致性得分 ≥ 0.7 | 情景一致，保留 |
| 0.5 ≤ 一致性得分 < 0.7 | 情景弱不一致，标注警告但保留 |
| 一致性得分 < 0.5 | 情景不一致，需修正或排除 |
| 修正后仍不一致 | 排除该情景，记录排除原因 |
| 所有情景均不一致 | 重新构建情景轴，检查假设选取 |

**输出规范**：
```yaml
cib_scenario_consistency:
  scenarios_checked: int
  consistent_scenarios: [{name: str, consistency_score: float}]
  weak_inconsistent_scenarios: [{name: str, consistency_score: float, warning: str}]
  inconsistent_scenarios: [{name: str, consistency_score: float, contradiction: str, action: "modified|excluded"}]
```

**穷尽重试策略**：当交叉影响矩阵不可用（无结构化数据）时，穷尽重试为定性一致性检验：通过逻辑推理检查假设间的明显矛盾，不计算一致性得分，标注"定性一致性检验，无数值评分"。

> 知识来源: MC-062 [CIB场景一致性]

---

### MC-063 CLA因果层次分析方法论

**方法论原理**：CLA（Causal Layered Analysis）因果层次分析方法论的核心认知假设是——任何社会现象都有四个深度层次的因果解释，浅层解释（事件/数据）和深层解释（神话/隐喻）对现象的描述截然不同但都"真实"。只看浅层会导致"治标不治本"的政策，只看深层会导致"脱离现实"的玄学。CLA的四层结构是：第一层Litany（表层事件和数据）、第二层Social Causes（系统性和结构性原因）、第三层Discourse/Worldview（话语和世界观）、第四层Myth/Metaphor（深层神话和隐喻）。这种方法论使我们从"单一深度的因果分析"升级为"多层深度的因果透视"。

**执行步骤**：
1. **Layer 1 Litany分析**：描述表层趋势、事件和官方数据（200-400字）
2. **Layer 2 Social Causes分析**：揭示系统性、结构性和制度性原因（200-400字）
3. **Layer 3 Discourse/Worldview分析**：分析深层世界观、话语框架和意识形态（200-400字）
4. **Layer 4 Myth/Metaphor分析**：识别深层神话、文化隐喻和集体无意识（200-400字）
5. 跨层关联分析：浅层事件如何被深层神话塑造，深层神话如何在浅层事件中显现
6. 识别层间张力：不同层次的解释是否矛盾，矛盾意味着什么
7. 基于四层分析提出分层干预策略

**决策规则**：

| 条件 | 决策 |
|------|------|
| 四层分析均完整 | CLA分析FULL，输出完整四层报告 |
| Layer 1-2完整，Layer 3-4不完整 | CLA分析PARTIAL，标注深层分析不足 |
| 仅Layer 1完整 | CLA分析RETRYING，穷尽重试为表层趋势分析 |
| Layer 4分析涉及文化禁忌 | 谨慎表述，标注"可能引发争议" |

**输出规范**：
```yaml
cla_analysis:
  layers:
    - {layer: 1, name: "Litany", analysis: str}
    - {layer: 2, name: "Social Causes", analysis: str}
    - {layer: 3, name: "Discourse/Worldview", analysis: str}
    - {layer: 4, name: "Myth/Metaphor", analysis: str}
  cross_layer_connections: [str]
  inter_layer_tensions: [str]
  layered_interventions: [{layer: int, intervention: str}]
```

**穷尽重试策略**：当深层分析（Layer 3-4）信息不足时，穷尽重试为Layer 1-2分析，标注"CLA深层分析不完整，缺少世界观和神话层面"，建议后续研究补充深层文化分析。

> 知识来源: MC-063 [CLA因果层次分析]

---

### MC-064 三视野框架方法论

**方法论原理**：三视野框架（Three Horizons Framework）的核心认知假设是——从当前系统到未来系统的转型不是一蹴而就的跳跃，而是三个视野的动态交互过程。H1代表当前系统的主导逻辑和衰退信号，H3代表未来系统的愿景和种子（已存在但边缘的创新），H2代表转型期的冲突和创新（H1和H3的碰撞地带）。这种方法论使我们从"线性外推未来"升级为"理解转型的动力学"——未来不是现在的延伸，而是H1衰退、H3成长、H2创新的共同结果。

**执行步骤**：
1. **H1分析**：描述当前系统的核心特征、成功逻辑和衰退信号
2. **H3分析**：描述未来系统的愿景、核心逻辑和已存在的种子创新
3. **H2分析**：识别H1和H3的冲突点、转型创新和过渡机制
4. 绘制三视野时间线：H1主导→H1衰退/H2冲突→H3主导
5. 识别转型路径：从H1到H3的可能路径和关键转折点
6. 识别转型障碍：H1的锁定效应和H3的扩散障碍
7. 设计转型策略：如何加速H1衰退、支持H2创新、培育H3种子

**决策规则**：

| 条件 | 决策 |
|------|------|
| H1/H2/H3三层分析均完整 | 三视野分析FULL |
| H1和H3完整但H2不清晰 | 标注"转型路径不明确"，需补充H2分析 |
| H3愿景不清晰 | 标注"未来系统模糊"，需补充前瞻研究 |
| H1衰退信号不明显 | 标注"当前系统仍具韧性"，转型时间线可能更长 |

**输出规范**：
```yaml
three_horizons:
  H1: {features: [str], decline_signals: [str], dominant_logic: str}
  H2: {conflicts: [str], innovations: [str], transition_mechanisms: [str]}
  H3: {vision: str, seeds: [str], core_logic: str}
  transition_paths: [{path: str, key_turning_points: [str], obstacles: [str]}]
  transition_strategy: str
```

**穷尽重试策略**：当H3愿景信息不足时，穷尽重试为H1-H2分析：仅描述当前系统的衰退信号和转型冲突，不构建未来系统愿景，标注"三视野分析不完整，缺少H3愿景"。

> 知识来源: MC-064 [三视野框架]

---

### MC-065 Wild Card方法论

**方法论原理**：Wild Card方法论的核心认知假设是——低概率高影响事件（Wild Cards/黑天鹅）虽然无法预测，但可以预先识别其可能类型并评估其影响。传统情景规划聚焦"最可能发生的未来"，但历史表明改变世界的事件往往是"最不可能发生的"。Wild Card分析不试图预测具体事件，而是系统性地扫描低概率高影响的可能事件，评估其对各情景的冲击，构建"如果发生...那么..."的应急框架。这种方法论使我们从"只准备最可能的未来"升级为"对所有可能的未来都有预案"。

**执行步骤**：
1. 定义Wild Card标准：概率LOW/VERY_LOW + 影响HIGH/CRITICAL
2. 系统扫描Wild Card候选：技术突破、地缘政治突变、自然灾害、社会运动等
3. 对每个候选评估概率等级和影响等级
4. 筛选3-5个最关键的Wild Card
5. 评估每个Wild Card对现有情景的影响
6. 构建Wild Card情景变体：在原有情景基础上叠加Wild Card
7. 识别Wild Card的早期预警信号
8. 设计应急响应框架

**决策规则**：

| 条件 | 决策 |
|------|------|
| Wild Card数量 ≥ 3 | 分析充分，输出完整Wild Card报告 |
| Wild Card数量 < 3 | 扩大扫描范围，补充Wild Card候选 |
| Wild Card使所有情景失效 | 标注为"系统性冲击"，需重新构建情景 |
| Wild Card与现有情景高度相关 | 整合到现有情景中，不作为独立Wild Card |

**输出规范**：
```yaml
wild_cards:
  - {event: str, probability: "LOW|VERY_LOW", impact: "HIGH|CRITICAL", scenario_impact: str, early_warning_signals: [str], response_framework: str}
  systemic_shocks: [str]
  integrated_into_scenarios: [str]
```

**穷尽重试策略**：当Wild Card扫描信息不足时，穷尽重试为基础风险列举：仅列出2-3个最明显的低概率高影响事件，不进行详细的情景影响评估，标注"Wild Card分析不完整，仅覆盖基础风险"。

> 知识来源: MC-065 [Wild Card分析]

---

### MC-136 场景鲁棒性方法论

**方法论原理**：场景鲁棒性方法论的核心认知假设是——好的策略不是在某个情景下最优，而是在所有合理情景下都表现良好。传统决策分析在"最可能情景"下优化策略，但未来几乎不会按"最可能"发展。场景鲁棒性评估将策略放在多个情景下测试，识别"跨情景鲁棒策略"（在所有情景下都可行）和"情景特异策略"（仅在特定情景下可行）。这种方法论使我们从"追求最优解"升级为"追求鲁棒解"——在不确定世界中，鲁棒比最优更有价值。

**执行步骤**：
1. 列出所有候选策略
2. 对每个策略，在每个情景下评估其表现
3. 构建策略-情景表现矩阵
4. 识别跨情景鲁棒策略：在所有/大多数情景下表现≥阈值的策略
5. 识别情景特异策略：仅在特定情景下表现良好的策略
6. 评估鲁棒策略的"最坏情况"表现（Maximin准则）
7. 评估鲁棒策略的"遗憾值"（Minimax Regret准则）
8. 输出策略鲁棒性排序

**决策规则**：

| 条件 | 决策 |
|------|------|
| 策略在≥80%情景下表现良好 | 标注为"强鲁棒策略"，优先推荐 |
| 策略在50-80%情景下表现良好 | 标注为"中等鲁棒策略"，需附加条件 |
| 策略在<50%情景下表现良好 | 标注为"脆弱策略"，仅作为情景特异备选 |
| 无鲁棒策略 | 建议设计新的组合策略或降低期望 |

**输出规范**：
```yaml
scenario_robustness:
  robust_strategies: [{strategy: str, robustness_score: float, worst_case_performance: str, max_regret: float|null}]
  scenario_specific_strategies: [{strategy: str, applicable_scenarios: [str], inapplicable_scenarios: [str]}]
  no_robust_strategy_warning: bool
```

**穷尽重试策略**：当情景数量不足（<2个）时，无法进行鲁棒性评估，穷尽重试为单情景策略评估，标注"场景鲁棒性评估不可用，情景数量不足"。

> 知识来源: MC-136 [场景鲁棒性评估]

---

## knowledge_refs
- MC-061 探索性建模-Exploratory-Modeling
- MC-062 交叉影响分析-Scenario-Consistency
- MC-063 因果分层分析-Causal-Layered-Analysis
- MC-064 Three-Horizons-Framework
- MC-065 Wild-Card-Analysis
- MC-136 Scenario-Robustness-Evaluation
- TC-061 探索性建模 Workbench
- TC-062 因果分层分析 Framework
- MC-145 Scenario-Expected-Value: 期望值计算 E(D)=W_opt×V_opt+W_neu×V_neu+W_pes×V_pes + 情景偏离度 SD，在 Step 2 情景构建中用于多情景期望值量化。详见 `knowledge/external-capabilities-index.md`
- MC-146 Monte-Carlo-Decision-Tree: 蒙特卡洛仿真（1000-5000次）+ 决策树后序遍历EV计算，在 Step 3 情景推演中用于概率分布模拟与不确定性量化。详见 `knowledge/external-capabilities-index.md`
- TC-097 BifurcationKit: 在情景推演中，当系统变量可连续化建模时，调用 BifurcationKit.jl 进行分岔分析，识别临界点参数阈值。详见 `knowledge/external-capabilities-index.md`
