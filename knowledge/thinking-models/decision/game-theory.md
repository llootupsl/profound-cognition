# 博弈论分析框架 — 多方策略互动的分析框架

> **模块标识**: `knowledge/thinking-models/decision/game-theory`
> **职责**: 作为决策分析系统的策略互动引擎，接收多方利益相关者信息，通过博弈论模型分析各方策略选择、均衡状态和稳定性，输出策略建议与风险预警
> **依赖**: `knowledge/thinking-models/decision/decision-matrix`、`knowledge/thinking-models/decision/bayesian-updating`、`knowledge/thinking-models/general/critical-thinking`、`knowledge/research-methods`
> **核心能力**: 参与者识别、策略空间构建、收益矩阵计算、均衡求解、稳定性分析、重复博弈演化分析

---

## 一、模块定位

### 1.1 在框架架构中的角色

```
┌─────────────────────────────────────────────────────────────────┐
│                    策略互动分析流水线                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  多方问题识别 ──▶ 参与者提取 ──▶ 策略互动判定 ──▶ 本模块触发    │
│                                          │                      │
│                                          ▼                      │
│                        ┌─────────────────────┐                 │
│                        │    game-theory      │                 │
│                        │  (博弈论分析引擎)    │                 │
│                        └────────┬────────────┘                 │
│                                 │                              │
│            ┌────────────────────┼────────────────────┐         │
│            ▼                    ▼                    ▼         │
│       均衡状态输出        策略建议输出          稳定性判定        │
│       (T05使用)          (T13使用)            (T15使用)        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 触发条件

当问题涉及以下场景时自动触发：

- 多个决策主体之间存在策略互动
- 一方的最优选择取决于其他方的选择
- 存在利益冲突或合作可能
- 需要分析"如果对方这样做，我该怎么办"

---

## 二、核心概念

### 2.1 基本博弈类型

| 博弈类型 | 定义 | 典型场景 | 均衡特征 |
|---------|------|---------|---------|
| **囚徒困境** | 个体理性导致集体非最优 | 价格战、军备竞赛、公地悲剧 | 唯一纳什均衡为帕累托劣解 |
| **零和博弈** | 一方收益等于另一方损失 | 竞争性投标、领土争端 | 混合策略均衡，无合作空间 |
| **协调博弈** | 双方有共同最优但需协调 | 技术标准选择、货币统一 | 多重均衡，需聚焦机制 |
| **胆小鬼博弈** | 退让者输但碰撞双输 | 极限施压、贸易谈判 | 混合策略均衡，高风险 |
| **重复博弈** | 同一博弈多次进行 | 长期合作、行业竞争 | 合作可成为子博弈精炼均衡 |

### 2.2 核心解概念

| 解概念 | 定义 | 适用条件 |
|--------|------|---------|
| **纳什均衡** | 没有任何一方有动力单方面偏离的策略组合 | 通用，但可能存在多重均衡 |
| **占优策略** | 无论对方如何选择都是最优的策略 | 强解，但不总是存在 |
| **帕累托最优** | 无法在不损害他人的情况下改善任何一方 | 效率标准，但不保证公平 |
| **子博弈精炼均衡** | 在每个子博弈上都构成纳什均衡 | 适用于动态/重复博弈 |
| **混合策略均衡** | 以概率分布随机选择纯策略 | 当纯策略均衡不存在时 |

---

## 三、分析步骤

### 3.1 步骤一：识别参与者

```
参与者识别清单:
1. 谁是决策主体？（直接参与者）
2. 谁受结果影响但无决策权？（利益相关者）
3. 谁有能力改变博弈规则？（规则制定者）
4. 是否存在隐性参与者？（幕后影响者）
5. 参与者之间的信息对称性如何？（完全信息/不完全信息）

参与者画像:
- 参与者ID
- 目标函数（最大化什么？）
- 约束条件（资源、信息、时间限制）
- 风险偏好（风险厌恶/中性/偏好）
- 时间偏好（短期导向/长期导向）
```

### 3.2 步骤二：定义策略空间

```
策略空间构建:
1. 每个参与者的可选行动集合
2. 行动的时序（同时/序贯）
3. 信息结构（完美信息/不完美信息）
4. 策略的不可逆性（可撤回/不可撤回）
5. 策略的可见性（公开/隐蔽）

策略空间约束:
- 策略数量: 至少2个（否则不构成博弈）
- 策略互斥: 每个参与者在同一时点只能选择一个策略
- 策略可行: 每个策略必须在参与者的资源和能力范围内
```

### 3.3 步骤三：构建收益矩阵

```
收益矩阵构建规则:
1. 对每个策略组合，评估每个参与者的收益
2. 收益量化: 优先使用可量化指标（利润、市场份额等）
3. 不可量化收益: 使用相对评分（-5 到 +5）
4. 收益必须反映参与者的真实目标函数（非分析者的判断）

收益矩阵格式（2人博弈示例）:
                参与者B
              策略B1    策略B2
参与  策略A1  (3,2)    (0,4)
者A   策略A2  (4,0)    (1,1)
              (A收益, B收益)
```

### 3.4 步骤四：求解均衡

```
均衡求解流程:
1. 检查占优策略: 每个参与者是否有占优策略？
2. 重复剔除劣策略: 逐步剔除严格劣策略
3. 寻找纯策略纳什均衡: 互为最优响应的策略组合
4. 若无纯策略均衡: 求解混合策略均衡
5. 动态博弈: 使用逆向归纳法求解子博弈精炼均衡
6. 多重均衡处理: 使用聚焦机制（历史惯例、显性信号、第三方协调）选择
```

### 3.5 步骤五：分析稳定性

```
稳定性分析维度:
1. 均衡的鲁棒性: 收益小幅变化是否改变均衡？
2. 参与者偏离动机: 偏离均衡的收益差是多少？
3. 信息不完全的影响: 如果参与者误判对方收益，均衡是否改变？
4. 重复博弈的演化: 长期互动中均衡是否稳定？
5. 外部冲击: 新参与者加入或规则改变时均衡如何移动？

稳定性评级:
- 高稳定: 均衡在多种扰动下保持不变
- 中稳定: 均衡在部分扰动下改变，但有恢复机制
- 低稳定: 均衡在小扰动下即改变，缺乏恢复机制
- 不稳定: 均衡仅在严格条件下成立
```

---

## 四、重复博弈与演化分析

### 4.1 重复博弈框架

```
单次博弈 vs 重复博弈:
- 单次博弈: 参与者只互动一次 → 背叛可能是理性选择
- 有限重复: 互动N次（N已知） → 逆向归纳导致合作崩溃
- 无限重复: 互动持续（或N未知） → 合作可成为均衡

合作条件（Folk Theorem）:
如果 δ (贴现因子) 足够大，即参与者足够重视未来：
  δ > (背叛诱惑收益 - 合作收益) / (背叛诱惑收益 - 惩罚收益)
则合作可以作为子博弈精炼均衡被维持
```

### 4.2 常见策略评估

| 策略 | 描述 | 适用场景 | 弱点 |
|------|------|---------|------|
| **一报还一报（TFT）** | 第一轮合作，之后模仿对方上一轮行为 | 重复博弈初期 | 对噪声敏感，可能陷入报复循环 |
| **宽容TFT** | 以一定概率原谅对方的背叛 | 有噪声/误判的环境 | 可能被系统性剥削 |
| **始终合作** | 无论对方如何选择都合作 | 极长期关系 | 被背叛者剥削 |
| **始终背叛** | 无论对方如何选择都背叛 | 单次博弈 | 无法获得合作收益 |
| **触发策略** | 一旦对方背叛，永远背叛 | 需要强威慑 | 过于严厉，无法恢复合作 |

---

## 五、与任务节点的协同

### 5.1 与 T05（假设管理）的集成

利益相关者分析时使用博弈论分析各方策略选择：

```
T05-博弈论联动:
1. T05 识别利益相关者 → 作为博弈参与者输入
2. 博弈论分析各方策略选择 → 生成"策略互动假设"
3. 纳什均衡结果 → 作为假设的置信度参考
4. 均衡稳定性 → 作为假设的鲁棒性评估
5. 新证据影响收益矩阵 → 触发贝叶斯更新（bayesian-updating）
```

### 5.2 与 T15（领域分析）的集成

领域分析时使用博弈论分析行业竞争格局：

```
T15-博弈论联动:
1. T15 识别行业参与者 → 作为博弈参与者
2. 行业竞争格局 → 构建收益矩阵
3. 博弈均衡 → 预测行业演化方向
4. 重复博弈分析 → 评估长期竞争/合作趋势
5. 规则改变（政策/技术） → 分析新均衡
```

### 5.3 与 bayesian-updating 的集成

- 参与者的类型不确定时，使用贝叶斯更新推断参与者类型
- 收益矩阵中的不确定参数使用贝叶斯后验概率
- 均衡稳定性分析结合置信度区间

---

## 六、输出模板

```yaml
game_theory_analysis:
  players:
    - id: "P-001"
      name: "参与者名称"
      type: "decision_maker/stakeholder/rule_setter/hidden"
      objective: "目标函数描述"
      constraints: ["约束条件"]
      risk_preference: "averse/neutral/seeking"
      information: "complete/incomplete"
  strategy_space:
    - player_id: "P-001"
      strategies: ["策略1", "策略2"]
      timing: "simultaneous/sequential"
      reversibility: "reversible/irreversible"
      observability: "public/private"
  payoff_matrix:
    - strategy_profile: ["P-001:策略1", "P-002:策略1"]
      payoffs: {P-001: 0, P-002: 0}
  equilibrium:
    type: "nash_dominant/nash_pure/nash_mixed/subgame_perfect/pareto"
    strategy_profile: ["均衡策略组合"]
    stability: "high/medium/low/unstable"
    robustness: "收益小幅变化下均衡是否改变"
  repeated_game_analysis:
    applicable: true/false
    discount_factor: 0.0-1.0
    cooperation_sustainable: true/false
    recommended_strategy: "推荐策略"
  key_findings:
    - "核心发现1: 均衡状态描述"
    - "核心发现2: 稳定性评估"
    - "核心发现3: 策略建议"
  risks:
    - "风险1: 均衡可能被打破的条件"
    - "风险2: 信息不对称的影响"
  strategic_recommendations:
    - target_player: "P-001"
      recommendation: "策略建议"
      rationale: "建议依据"
```

---

## 七、质量自检清单

### 博弈结构完整性
- 参与者数量 >= 2
- 每个参与者至少2个策略
- 收益矩阵覆盖所有策略组合
- 收益反映参与者真实目标函数

### 均衡求解正确性
- 占优策略检查已完成
- 劣策略剔除已执行
- 纳什均衡已正确识别
- 多重均衡已标注并分析

### 稳定性分析充分性
- 鲁棒性检验已完成
- 参与者偏离动机已评估
- 信息不完全影响已分析
- 重复博弈演化已考虑（如适用）

### 实用性检查
- 收益矩阵数据有来源依据
- 策略建议针对具体参与者
- 风险条件具体可操作
- 未将博弈论结论当作确定性预测

---
## 八、外部能力卡片引用（v3 新增）

### 8.1 OpenSpiel 博弈求解引擎

> **能力卡**: TC-087 OpenSpiel

在均衡求解步骤（步骤四）中，当博弈结构复杂（参与者 ≥ 3 或策略空间 ≥ 5）时，调用 OpenSpiel 进行算法化均衡求解：

```yaml
openspiel_integration:
  trigger: "参与者 ≥ 3 或策略空间 ≥ 5"
  workflow:
    - step: "将博弈结构编码为 OpenSpiel Game 定义（normal_form / extensive_form）"
    - step: "选择求解算法：Nash（LCP/LP）、Correlated（LP）、Quantal Response（Logit）"
    - step: "执行求解，输出均衡策略组合及对应收益"
    - step: "验证均衡：检查偏离动机（regret < 0.001）"
  exhaust-retry: "博弈结构简单（2人 × ≤4策略）时，使用手动推理求解，标注 solver='manual'"
  capabilities:
    - "70+ 博弈环境（矩阵博弈、扩展式博弈、马尔可夫博弈、贝叶斯博弈等）"
    - "30+ 求解算法（Nash/Correlated/Quantal Response/NFSP/Deep CFR/PSRO等）"
    - "支持不完全信息博弈和动态博弈"
```

### 8.2 Axelrod 重复博弈策略库

> **能力卡**: TC-088 Axelrod

在重复博弈与演化分析（第四节）中，当分析长期互动策略选择时，调用 Axelrod 策略库进行策略匹配与锦标赛模拟：

```yaml
axelrod_integration:
  trigger: "重复博弈场景（互动次数 ≥ 5 或无限重复）"
  workflow:
    - step: "将参与者的行为模式编码为 Axelrod 策略或匹配已有策略库（230+ 策略）"
    - step: "配置锦标赛参数：轮数（≥ 200）、噪声率（0-0.05）、参与者数量"
    - step: "运行锦标赛模拟，输出各策略的平均得分和排名"
    - step: "分析策略演化：使用 Moran Process 模拟策略种群演化"
    - step: "推荐最优策略：综合锦标赛排名 + 对抗不同策略的鲁棒性"
  strategy_categories:
    - "Cooperative（合作型）：TitForTat, GenerousTFT, HardTFT"
    - "Defecting（背叛型）：Defector, Alternator, DoubleCrosser"
    - "Grudger（记仇型）：Grudger, Retaliate, Punisher"
    - "Memory-based（记忆型）：TFT家族（1-3步记忆）, WinStayLoseShift"
    - "Zero-Determinant（零行列式）：ZD-Extortion, ZD-Generous, ZD-GTFT"
  exhaust-retry: "单次博弈或非囚徒困境结构时，不调用 Axelrod，使用手动分析"
```

### 8.3 能力卡调用声明

| 能力卡 | 调用位置 | 触发条件 | 穷尽重试策略 |
|--------|---------|---------|---------|
| TC-087 OpenSpiel | 步骤四：均衡求解 | 参与者 ≥ 3 或策略空间 ≥ 5 | 穷尽重试为手动推理，标注 solver='manual' |
| TC-088 Axelrod | 第四节：重复博弈分析 | 互动次数 ≥ 5 或无限重复 | 穷尽重试为手动策略评估，标注 strategy_src='manual' |

---

## 九、博弈分析决策规则（MC-142 Nash-Equilibrium / MC-143 Dominant-Strategy）

| 条件 | 判定 | 行动 |
|------|------|------|
| 存在占优策略（MC-143） | 强解 | 直接推荐占优策略，标注"占优策略均衡" |
| 存在纯策略纳什均衡（MC-142） | 稳定均衡 | 推荐均衡策略，分析偏离动机 |
| 仅存在混合策略纳什均衡 | 不完全稳定 | 推荐混合策略，标注"概率化选择" |
| 存在多重纳什均衡 | 均衡不确定性 | 使用聚焦机制选择，标注"多重均衡需协调" |
| 无纳什均衡 | 博弈不稳定 | 建议改变博弈结构或引入重复博弈框架 |
| 均衡稳定性评级为"高稳定" | 可信预测 | 均衡结果可作为高置信度预测 |
| 均衡稳定性评级为"低稳定/不稳定" | 不可信预测 | 均衡结果仅作参考，需动态监测 |
| 重复博弈 δ > 阈值 | 合作可持续 | 推荐合作策略（TFT/宽容TFT） |
| 重复博弈 δ < 阈值 | 合作不可持续 | 接受非合作均衡，评估改变δ的可能性 |
| 参与者 ≥ 3 或策略空间 ≥ 5 | 复杂博弈 | 触发OpenSpiel算法化求解 |
| 信息不完全 | 不完全信息博弈 | 使用贝叶斯纳什均衡，结合bayesian-updating推断类型 |

> 知识来源: MC-142 Nash-Equilibrium / MC-143 Dominant-Strategy

---

## 十、博弈分析穷尽重试策略

| 重试层级 | 条件 | 替代方案 |
|---------|------|---------|
| L1 完整博弈分析 | 收益矩阵可量化、参与者可识别 | 完整执行5步分析+均衡求解+稳定性评估 |
| L2 部分量化博弈 | 收益仅可部分量化 | 对可量化部分做均衡分析，不可量化部分用相对评分（-5到+5），标注"部分量化" |
| L3 定性博弈分析 | 收益完全不可量化 | 做定性策略互动分析（谁占优、谁弱势、合作/冲突倾向），标注"定性分析" |
| L4 博弈结构识别 | 仅知参与者身份和关系 | 仅识别博弈类型（囚徒困境/零和/协调等），标注"仅结构识别" |

> 知识来源: MC-142 Nash-Equilibrium / MC-143 Dominant-Strategy

---

## 十一、权力-利益矩阵分析（MC-160 Power-Interest-Matrix）

### 方法论原理

权力-利益矩阵的方法论基础是：**在多方博弈中，不同利益相关者对决策结果的影响力和关注度不同，有效的策略必须根据各方的权力-利益位置差异化对待**。将利益相关者映射到权力（Power）和利益（Interest）两个维度上，形成四个象限，每个象限对应不同的管理策略。这一方法论之所以必要，是因为最常见的利益相关者管理失败是"平均对待"——对所有利益方投入同等精力，导致高权力高利益方关注不足而低权力低利益方浪费资源。

### 执行步骤

1. **识别利益相关者**：列出所有受决策影响或能影响决策的主体
2. **权力评估**：对每个利益方评估其权力水平（1-10）：强制力、资源控制力、信息控制力、合法性权威
3. **利益评估**：对每个利益方评估其利益水平（1-10）：直接利益程度、受影响强度、关注主动性
4. **矩阵定位**：将各利益方映射到权力-利益四象限
5. **策略制定**：根据象限位置制定差异化策略

### 决策规则

| 象限 | 权力 | 利益 | 策略 | 精力分配 |
|------|------|------|------|---------|
| A 关键方 | 高(≥7) | 高(≥7) | 密切管理：主动沟通、优先满足核心诉求 | 40% |
| B 保持满意 | 高(≥7) | 低(<7) | 保持满意：定期沟通、防止利益上升 | 20% |
| C 保持告知 | 低(<7) | 高(≥7) | 保持告知：充分沟通、利用其舆论影响力 | 25% |
| D 监测 | 低(<7) | 低(<7) | 最少努力：定期监测、防止权力或利益上升 | 15% |

### 输出规范

```yaml
power_interest_matrix:
  stakeholders:
    - id: "SH-001"
      name: "利益方名称"
      power_score: 1-10
      interest_score: 1-10
      quadrant: "A-关键方/B-保持满意/C-保持告知/D-监测"
      strategy: "管理策略描述"
      effort_allocation: "百分比"
  matrix_summary:
    key_players: ["A象限利益方"]
    keep_satisfied: ["B象限利益方"]
    keep_informed: ["C象限利益方"]
    monitor: ["D象限利益方"]
  power_dynamics:
    potential_shifts: ["权力/利益可能变化的利益方"]
    coalition_risks: ["潜在联盟风险"]
```

### 穷尽重试策略

| 重试层级 | 条件 | 替代方案 |
|---------|------|---------|
| L1 完整权力-利益矩阵 | 权力和利益均可量化评估 | 完整执行5步，输出四象限矩阵和策略 |
| L2 定性矩阵 | 权力和利益仅可定性评估 | 使用高/中/低三级评估，标注"定性评估" |
| L3 利益方清单 | 仅可识别利益方但无法评估权力/利益 | 列出利益方清单和基本关系，标注"无矩阵定位" |
| L4 利益方识别 | 仅知部分利益方 | 列出已知利益方，标注"利益方识别不完整" |

> 知识来源: MC-160 Power-Interest-Matrix

---

## 十二、OpenSpiel+Axelrod 博弈求解方法论（TC-087/TC-088）

> **能力卡**: TC-087 OpenSpiel / TC-088 Axelrod

### 12.1 核心原理

OpenSpiel 和 Axelrod 是博弈论求解的两大工具：
- **OpenSpiel**（TC-087）：Google DeepMind 开发的博弈论环境库，支持2人零和到多人一般和博弈，内置多种均衡求解算法（CFR、 fictitious play、alpha-zero风格搜索等）
- **Axelrod**（TC-088）：重复囚徒困境策略演化库，内置200+策略，支持策略锦标赛和演化模拟

### 12.2 OpenSpiel 环境分类与算法选择

**环境分类**：

| 环境类型 | 代表博弈 | 参与者数 | 信息结构 | 推荐算法 |
|---------|---------|---------|---------|---------|
| **2人零和完全信息** | 囚徒困境、匹配硬币 | 2 | 完全 | CFR、CFR+、MCCFR |
| **2人零和不完全信息** | 德州扑克、Kuhn扑克 | 2 | 不完全 | CFR+、Deep CFR、PSRO |
| **2人一般和** | 协调博弈、性别战 | 2 | 完全/不完全 | fictitious play、replicator dynamics |
| **多人博弈** | 公共物品博弈、投票 | ≥3 | 完全/不完全 | NashConv、alpha-zero风格搜索 |
| **序列博弈** | 扩展式博弈、谈判 | 2+ | 完全/不完全 | 后向归纳、子博弈求解 |

**算法选择决策树**：

```
博弈环境输入
  │
  ├─ Q1: 参与者数量？
  │   ├─ 2人 → Q2
  │   └─ ≥3人 → NashConv + alpha-zero风格搜索
  │
  ├─ Q2: 博弈类型？
  │   ├─ 零和 → Q3
  │   └─ 一般和 → fictitious play + replicator dynamics
  │
  ├─ Q3: 信息结构？
  │   ├─ 完全信息 → CFR（反事实遗憾最小化）
  │   └─ 不完全信息 → Q4
  │
  ├─ Q4: 状态空间大小？
  │   ├─ 小（<10^6 状态）→ CFR+（加速版CFR）
  │   ├─ 中（10^6-10^9）→ MCCFR（蒙特卡洛CFR）
  │   └─ 大（>10^9）→ Deep CFR（神经网络近似CFR）
  │
  └─ 默认推荐：
      2人零和完全信息 → CFR
      2人零和不完全信息 → MCCFR
      多人博弈 → NashConv评估 + PSRO策略优化
```

### 12.3 Axelrod 策略演化分析

**策略分类**：

| 策略类别 | 代表策略 | 核心特征 | 适应场景 |
|---------|---------|---------|---------|
| **合作型** | Cooperator, TitForTat, Grudger | 初始合作，回应合作 | 长期重复博弈 |
| **背叛型** | Defector, AlwaysDefect | 始终背叛 | 单次/短期博弈 |
| **条件型** | TFT, GTFT, Pavlov, Random | 根据对手行为调整 | 不确定环境 |
| **复杂型** | FSM策略, LookupTable, Neural | 复杂状态机/学习 | 高噪声/不确定环境 |
| **检测型** | Detective, Prober | 先试探再决定 | 未知对手类型 |

**演化分析执行步骤**：

```
步骤1: 策略选择
  ├─ 从200+策略中选择5-10种代表性策略
  ├─ 确保覆盖5个类别（合作/背叛/条件/复杂/检测）
  └─ 输出：策略列表

步骤2: 锦标赛模拟
  ├─ 每对策略进行N轮重复囚徒困境（N=200默认）
  ├─ 计算每对策略的收益矩阵
  ├─ 计算各策略的总得分和排名
  └─ 输出：锦标赛排名

步骤3: 演化模拟
  ├─ 初始种群：各策略等比例
  ├─ 每代：按收益比例更新种群比例（replicator dynamics）
  │   x_i(t+1) = x_i(t) × f_i / Σ x_j(t) × f_j
  │   其中 f_i = 策略i的适应度（平均收益）
  ├─ 运行100代，记录种群演化轨迹
  └─ 输出：演化稳定策略（ESS）

步骤4: 鲁棒性检验
  ├─ 噪声测试：在5%/10%/20%噪声下重复锦标赛
  ├─ 种群扰动：引入5%突变策略，检验ESS稳定性
  └─ 输出：策略鲁棒性报告
```

### 12.4 OpenSpiel+Axelrod 与 profound-cognition Layer 对照映射

| 博弈求解步骤 | 对应Layer | 映射说明 |
|------------|----------|---------|
| 环境分类 | Layer2 分解 | 分解博弈结构特征 |
| 算法选择 | Layer4 推理 | 选择推理算法 |
| 均衡求解 | Layer4 推理 | 执行博弈推理 |
| 策略演化 | Layer6 因果 | 因果分析策略演化动力 |
| 鲁棒性检验 | Layer5 反事实 | 反事实检验策略稳定性 |
| 策略建议 | Layer8 决策 | 输出策略决策建议 |

### 12.5 OpenSpiel+Axelrod 穷尽重试策略

```yaml
game_solving_exhaust_retry:
  L1_FULL:
    condition: "OpenSpiel和Axelrod均可用"
    action: "OpenSpiel求解均衡+Axelrod演化模拟+鲁棒性检验"
    confidence: "HIGH"

  L2_OPENSPIEL_ONLY:
    condition: "Axelrod不可用（非重复博弈场景）"
    action: "仅使用OpenSpiel求解均衡，跳过演化分析"
    confidence: "MEDIUM"
    output_annotation: "博弈求解穷尽重试：仅均衡求解，无演化分析"

  L3_ANALYTICAL_NASH:
    condition: "OpenSpiel不可用，但博弈结构简单（2人2策略）"
    action: "手动求解纳什均衡（最佳回应法/划线法）"
    confidence: "LOW-MEDIUM"
    output_annotation: "博弈求解穷尽重试：手动纳什均衡求解"

  L4_QUALITATIVE_GAME:
    condition: "博弈工具完全不可用"
    action: "定性博弈分析——识别博弈类型+策略互动方向+合作/冲突倾向"
    confidence: "LOW"
    output_annotation: "博弈求解完全穷尽重试：定性博弈分析"
```

> 知识来源: TC-087 [OpenSpiel] / TC-088 [Axelrod]

---

## 十三、源码逻辑引入

### [OpenSpiel] 源码逻辑引入

#### 核心算法逻辑

**1. 博弈环境类层次与加载机制**

```
Game 类层次（open_spiel/python/spiel.py）:
  Game (抽象基类)
    ├─ type() → GameType  # 返回博弈元信息
    │   ├─ dynamics: SEQUENTIAL | SIMULTANEOUS
    │   ├─ chance_mode: DETERMINISTIC | EXPLICIT_STOCHASTIC | EXPLICIT_SAMPLED
    │   ├─ information: PERFECT | IMPERFECT
    │   ├─ utility: ZERO_SUM | GENERAL_SUM | IDENTICAL
    │   └─ max_num_players, min_num_players
    ├─ new_initial_state() → State  # 创建初始状态
    └─ num_distinct_actions() → int

  State (抽象基类)
    ├─ is_chance_node() → bool      # 是否为机会节点
    ├─ is_terminal() → bool         # 是否为终止节点
    ├─ legal_actions(player) → list # 当前合法动作
    ├─ apply_action(action)         # 执行动作，状态转移
    ├─ returns() → list[float]      # 终止时各玩家收益
    └─ information_state_string() → str  # 信息集标识

加载流程:
  load_game(game_name, params) → Game
    ├─ 从 game_name 查找注册表
    ├─ 合并默认参数与用户参数
    ├─ 实例化具体 Game 子类
    └─ 返回 Game 对象
```

**2. CFR（反事实遗憾最小化）算法源码逻辑**

```
CFR 求解器核心循环（open_spiel/algorithms/cfr.py）:

function CFR_Solver(game, iterations):
    root = game.new_initial_state()
    info_state_values = {}  # Dict[info_state_str, float[]]

    for t in 1..iterations:
        # 遍历所有玩家
        for player in 0..game.num_players()-1:
            # 递归遍历博弈树，计算反事实遗憾
            root_value = traverse_tree(root, player, reach_prob, info_state_values)

            # 更新遗憾和累积策略
            for info_state in info_state_values:
                current_strategy = regret_matching(info_state.regret)
                info_state.cum_strategy += reach_prob * current_strategy

    # 返回平均策略（累积策略归一化）
    return average_strategy(info_state_values)

function regret_matching(regret):
    # 遗憾匹配：正遗憾按比例分配，零遗憾均匀分配
    positive_regret = max(regret[a], 0) for each action a
    sum_positive = sum(positive_regret)
    if sum_positive > 0:
        return positive_regret / sum_positive
    else:
        return uniform_distribution(num_actions)

function traverse_tree(state, player, reach_prob, info_state_values):
    if state.is_terminal():
        return state.returns()[player]  # 返回当前玩家收益

    if state.is_chance_node():
        # 机会节点：按概率加权遍历所有可能动作
        value = 0
        for action, prob in state.chance_outcomes():
            child = state.child(action)
            value += prob * traverse_tree(child, player, reach_prob, ...)
        return value

    info_state = state.information_state_string()
    legal_actions = state.legal_actions()

    # 计算当前策略
    current_strategy = regret_matching(info_state_values[info_state].regret)

    # 遍历所有合法动作
    action_values = []
    for action in legal_actions:
        child = state.child(action)
        new_reach = reach_prob.copy()
        new_reach[player] *= current_strategy[action]
        action_value = traverse_tree(child, player, new_reach, ...)
        action_values.append(action_value)

    # 计算反事实值和遗憾
    state_value = sum(current_strategy[a] * action_values[a] for a in legal_actions)
    for a in legal_actions:
        counterfactual_value = action_values[a] - state_value
        info_state_values[info_state].regret[a] += counterfactual_value * reach_prob[opponent]

    return state_value
```

**3. 求解算法选择源码逻辑**

```
算法选择决策函数（伪代码）:

function select_solver(game):
    game_type = game.type()

    # 第一层：参与者数量判断
    if game.num_players() >= 3:
        # 多人博弈：使用 NashConv 评估 + PSRO 策略优化
        return PSRO_Solver(game, meta_strategy=NashConv)

    # 第二层：零和 vs 一般和
    if game_type.utility == ZERO_SUM:
        # 第三层：信息结构
        if game_type.information == PERFECT:
            # 完全信息零和：CFR
            return CFR_Solver(game)
        else:
            # 不完全信息零和：按状态空间大小选择
            state_space = estimate_state_space(game)
            if state_space < 1e6:
                return CFRPlus_Solver(game)   # 加速版CFR
            elif state_space < 1e9:
                return MCCFR_Solver(game)     # 蒙特卡洛CFR
            else:
                return DeepCFR_Solver(game)   # 神经网络近似
    else:
        # 一般和博弈：虚构博弈 + 复制子动力学
        return FictitiousPlay_Solver(game)
```

**4. 均衡验证源码逻辑**

```
均衡验证函数（open_spiel/algorithms/nash_conv.py 简化）:

function verify_equilibrium(game, policy):
    # 计算 NashConv：各玩家最大可改进收益之和
    nash_conv = 0
    for player in 0..game.num_players()-1:
        # 计算当前策略下该玩家的收益
        current_value = compute_value(game, policy, player)

        # 计算该玩家的最佳响应收益（其他玩家策略不变）
        best_response_value = compute_best_response(game, policy, player)

        # 遗憾 = 最佳响应收益 - 当前收益
        regret = best_response_value - current_value
        nash_conv += regret

    # NashConv < ε 视为近似均衡
    # 典型阈值：ε = 0.001
    is_equilibrium = nash_conv < 0.001

    return {nash_conv, is_equilibrium, per_player_regret}
```

#### 数据结构设计

```
核心数据结构:

1. GameType: 博弈元信息结构
   - dynamics: SEQUENTIAL | SIMULTANEOUS
   - chance_mode: DETERMINISTIC | EXPLICIT_STOCHASTIC
   - information: PERFECT | IMPERFECT
   - utility: ZERO_SUM | GENERAL_SUM | IDENTICAL
   - max_num_players, min_num_players: int

2. InfoStateValues: 信息集累积值
   - regret: Dict[action, float]         # 累积遗憾值
   - cum_strategy: Dict[action, float]   # 累积策略
   - current_strategy: Dict[action, float] # 当前策略（遗憾匹配结果）

3. Policy: 策略表示
   - info_state_to_action_probs: Dict[info_state_str, Dict[action, probability]]
   - 支持均匀随机策略、表格策略、神经网络策略

4. NashConvResult: 均衡验证结果
   - nash_conv: float          # 总纳什偏离度
   - per_player_regret: list   # 各玩家遗憾
   - is_equilibrium: bool      # 是否为近似均衡
```

#### 决策流程

```
OpenSpiel 博弈求解决策流程:

1. 博弈输入 → load_game() 加载博弈环境
2. GameType 分析 → 判断博弈类别（零和/一般和、完全/不完全信息）
3. 算法选择 → select_solver(game) 选择求解器
4. 求解执行 → solver.run(iterations) 迭代求解
5. 均衡验证 → verify_equilibrium(game, policy)
   ├─ NashConv < 0.001 → 均衡可信，输出策略
   ├─ 0.001 ≤ NashConv < 0.01 → 均衡近似，标注"近似均衡"
   └─ NashConv ≥ 0.01 → 增加迭代次数或切换算法
6. 策略输出 → average_strategy 作为最终推荐
```

#### 穷尽重试策略

```yaml
openspiel_source_exhaust_retry:
  L1_CFR_FULL:
    condition: "OpenSpiel可用，CFR系列算法可执行"
    action: "按算法选择逻辑执行CFR/MCCFR/DeepCFR + NashConv验证"
    confidence: "HIGH"

  L2_FICTITIOUS_PLAY:
    condition: "CFR系列不可用（内存不足或博弈树过大）"
    action: "穷尽重试为虚构博弈（Fictitious Play），迭代至收敛"
    confidence: "MEDIUM"
    output_annotation: "OpenSpiel穷尽重试：使用虚构博弈替代CFR"

  L3_MANUAL_NASH:
    condition: "OpenSpiel不可用，但博弈结构简单（2人≤4策略）"
    action: "手动求解纳什均衡（最佳回应法/划线法）"
    confidence: "LOW-MEDIUM"
    output_annotation: "OpenSpiel穷尽重试：手动纳什均衡求解"

  L4_QUALITATIVE:
    condition: "OpenSpiel不可用且博弈结构复杂"
    action: "定性博弈分析——识别博弈类型+策略互动方向"
    confidence: "LOW"
    output_annotation: "OpenSpiel完全穷尽重试：定性博弈分析"
```

---

### [Axelrod] 源码逻辑引入

#### 核心算法逻辑

**1. 策略类层次与交互机制**

```
Strategy 类层次（axelrod/strategies/）:

  Strategy (抽象基类, axelrod/player.py)
    ├─ name: str              # 策略名称
    ├─ classifier: Dict       # 分类标签
    │   ├─ stochastic: bool   # 是否随机策略
    │   ├─ memory_depth: int  # 记忆深度（-1=无限）
    │   ├─ makes_use_of: list # 使用的特殊信息
    │   └─ inspects_source: bool  # 是否检查对手源码
    ├─ strategy(opponent: Player) → Action
    │   # 核心方法：根据对手历史决定当前动作
    └─ _history: list[Action]  # 自身历史动作

  主要策略子类:
    ├─ Cooperator          # 始终合作
    ├─ Defector            # 始终背叛
    ├─ TitForTat           # 一报还一报
    │   └─ strategy(): return opponent.history[-1]
    ├─ GenerousTFT         # 宽容TFT（以概率p原谅背叛）
    │   └─ strategy(): if opponent_last == D: return C with prob p
    ├─ Grudger             # 记仇（一旦背叛永远背叛）
    │   └─ strategy(): if D in opponent.history: return D
    ├─ WinStayLoseShift    # 赢了保持，输了切换
    ├─ ZDExtortion         # 零行列式勒索策略
    └─ MetaPlayer          # 元策略（组合多个子策略）

交互机制:
  Match.play():
    for turn in 1..turns:
      action_p1 = player1.strategy(player2)
      action_p2 = player2.strategy(player1)
      player1.history.append(action_p1)
      player2.history.append(action_p2)
      scores = compute_scores(action_p1, action_p2)
      # 收益矩阵: (C,C)=(3,3), (C,D)=(0,5), (D,C)=(5,0), (D,D)=(1,1)
```

**2. 锦标赛执行源码逻辑**

```
Tournament 执行流程（axelrod/tournament.py）:

function run_tournament(players, turns=200, repetitions=50, noise=0):
    results = TournamentResults()

    for rep in 1..repetitions:
        # 每对策略进行比赛
        for p1, p2 in combinations(players, 2):
            match = Match(p1, p2, turns, noise)
            match.play()
            results.record(match)

        # 每个策略也与自己比赛
        for player in players:
            match = Match(player, clone(player), turns, noise)
            match.play()
            results.record(match)

    # 计算排名
    rankings = compute_rankings(results)
    # 计算收益矩阵
    payoff_matrix = compute_payoff_matrix(results)
    # 计算获胜次数
    wins = compute_wins(results)

    return {rankings, payoff_matrix, wins, cooperation_rates}

噪声机制:
  if noise > 0:
    # 每个动作以概率 noise 被翻转
    actual_action = flip(action) with probability noise
```

**3. Moran Process 种群演化源码逻辑**

```
Moran Process 源码逻辑（axelrod/moran.py）:

function moran_process(players, turns=200, mutation_rate=0):
    # 初始化种群：每种策略等比例
    population = initialize_population(players, population_size=N)

    generation = 0
    while not fixated(population):
        generation += 1

        # 步骤1：计算适应度
        fitness = {}
        for strategy in unique_strategies(population):
            # 适应度 = 该策略与种群中所有策略对战的平均收益
            total_score = 0
            for opponent_strategy in unique_strategies(population):
                count = population.count(opponent_strategy)
                avg_score = play_match(strategy, opponent_strategy, turns)
                total_score += count * avg_score
            fitness[strategy] = total_score / len(population)

        # 步骤2：选择（按适应度比例选择一个个体繁殖）
        reproducer = weighted_random_choice(population, fitness)

        # 步骤3：变异（以概率 mutation_rate 替换为随机策略）
        if random() < mutation_rate:
            offspring = random_strategy(players)
        else:
            offspring = clone(reproducer)

        # 步骤4：替换（随机移除一个个体，加入后代）
        removed = random_choice(population)
        population.remove(removed)
        population.append(offspring)

        # 步骤5：检查是否固定
        if all_same_strategy(population):
            return {fixated_strategy, generation, trajectory}

    return {trajectory: population_history_over_generations}

function fixated(population):
    # 种群中只剩一种策略时固定
    return len(set(p.strategy for p in population)) == 1
```

**4. 策略分类体系源码结构**

```
230+ 策略分类（axelrod/strategies/ 目录结构）:

strategies/
  ├─ cooperator.py       # 合作型 (~15策略)
  │   └─ Cooperator, AllCooperator, ...
  ├─ defector.py         # 背叛型 (~10策略)
  │   └─ Defector, AllDefector, ...
  ├─ titfortat.py        # TFT家族 (~20策略)
  │   └─ TitForTat, GenerousTFT, HardTFT, ...
  ├─ grudger.py          # 记仇型 (~15策略)
  │   └─ Grudger, Punisher, ...
  ├─ memoryone.py        # 一步记忆 (~25策略)
  │   └─ WinStayLoseShift, SoftJoss, ...
  ├─ memorytwo.py        # 两步记忆 (~10策略)
  ├─ finitestatemachine.py  # 有限状态机 (~20策略)
  ├─ neural.py           # 神经网络策略 (~5策略)
  ├─ zero_determinant.py # 零行列式策略 (~10策略)
  │   └─ ZDExtortion, ZDGenerous, ...
  ├─ meta.py             # 元策略 (~15策略)
  │   └─ MetaMajority, MetaHunter, ...
  └─ ...                 # 其他 (~100+策略)

策略分类器 classifier 字段:
  stochastic: bool       # 是否随机
  memory_depth: int      # 记忆深度 (-1=无限, 0=无记忆, 1=一步...)
  makes_use_of: list     # 使用的特殊能力
  long_run_time: bool    # 是否耗时
  inspects_source: bool  # 是否检查对手源码
  manipulates_source: bool  # 是否修改对手源码
  manipulates_state: bool   # 是否修改对手状态
```

#### 数据结构设计

```
核心数据结构:

1. Action: 枚举类型
   - C = Cooperation (合作)
   - D = Defection (背叛)

2. MatchResult: 比赛结果
   - scores: (float, float)     # 双方总得分
   - cooperation_rates: (float, float)  # 双方合作率
   - normalised_scores: (float, float)  # 归一化得分

3. TournamentResults: 锦标赛结果
   - rankings: list[list[int]]  # 每次重复的排名
   - payoff_matrix: np.ndarray  # 策略×策略收益矩阵
   - wins: dict[int, int]       # 各策略获胜次数
   - cooperation_rates: dict    # 各策略合作率

4. MoranProcessResult: 演化结果
   - winning_strategy_name: str  # 固定策略
   - fixation_generation: int    # 固定所需代数
   - trajectory: list[dict]      # 种群比例变化轨迹
```

#### 决策流程

```
Axelrod 策略演化分析决策流程:

1. 场景识别 → 判断是否为重复博弈（互动次数 ≥ 5）
2. 策略匹配 → 从230+策略库中匹配参与者行为模式
   ├─ 直接匹配已有策略（classifier字段比对）
   └─ 无匹配 → 使用MetaPlayer组合或自定义策略
3. 锦标赛配置 → 设定轮数(≥200)、噪声率(0-0.05)、重复次数(≥50)
4. 锦标赛执行 → run_tournament()
5. 演化模拟 → moran_process() 种群演化
   ├─ 固定于单一策略 → ESS（演化稳定策略）
   └─ 多态平衡 → 标注"多态均衡"
6. 鲁棒性检验 → 噪声测试(5%/10%/20%) + 突变测试(5%)
7. 策略推荐 → 综合锦标赛排名 + 演化稳定性 + 鲁棒性
```

#### 穷尽重试策略

```yaml
axelrod_source_exhaust_retry:
  L1_FULL_TOURNAMENT:
    condition: "Axelrod可用，锦标赛和Moran Process均可执行"
    action: "完整锦标赛(≥50重复) + Moran Process演化 + 鲁棒性检验"
    confidence: "HIGH"

  L2_TOURNAMENT_ONLY:
    condition: "Moran Process不可用（种群规模过大或计算资源不足）"
    action: "仅执行锦标赛排名，使用replicator dynamics公式手动计算演化趋势"
    confidence: "MEDIUM"
    output_annotation: "Axelrod穷尽重试：仅锦标赛排名，手动演化分析"

  L3_MANUAL_STRATEGY:
    condition: "Axelrod不可用，但可手动评估策略"
    action: "手动策略评估——识别策略类别+定性比较+收益矩阵手动计算"
    confidence: "LOW-MEDIUM"
    output_annotation: "Axelrod穷尽重试：手动策略评估"

  L4_QUALITATIVE:
    condition: "Axelrod不可用且无法手动量化"
    action: "定性策略分析——识别合作/背叛倾向+长期趋势判断"
    confidence: "LOW"
    output_annotation: "Axelrod完全穷尽重试：定性策略分析"
```

---

© 阿洋
