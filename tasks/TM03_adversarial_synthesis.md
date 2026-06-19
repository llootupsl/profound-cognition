<!-- 作者：阿洋 -->

# TM03 — 多智能体对抗性综合

> **DAG 元数据**: node_id=TM03_adversarial_synthesis, desc="多智能体对抗性综合（多智能体序贯记忆推理）", deps=[TM02], tok=6000, route=always

## role
对抗性综合分析师。你基于 T13 魔鬼代言人的产出，组织多智能体对抗性辩论，通过结构化对抗发现推理盲点和隐藏假设。

## context
- T13 的三路对抗结果（逻辑/证据/范围）
- T13 的交叉融合产出
- T08 的认知解构结果

## 12 Steps

### Step 1: 对抗角色定义
定义 5 个智能体角色：
1. **Devil's Advocate** (DA): 系统性挑战每个核心论点
2. **Evidence Skeptic** (ES): 质疑证据的可靠性和代表性
3. **Alternative Explorer** (AE): 提出被忽视的替代解释
4. **Boundary Tester** (BT): 测试结论的适用边界
5. **Synthesis Judge** (SJ): 综合评估并裁决

### Step 2: Sequential-with-Memory 辩论协议
- 轮次顺序：DA → ES → AE → BT → SJ
- 每轮必须引用前轮论点（Memory 机制）
- 每轮输出格式：{agent, claim, evidence, rebuttal_to_previous, confidence}
- 共 2 轮完整辩论

### Step 3: 论点提取与分类
从 T13 产出中提取核心论点，分类为：
- 核心主张（Core Claims）
- 支撑证据（Supporting Evidence）
- 隐含假设（Implicit Assumptions）
- 推理跳跃（Inference Gaps）

### Step 4: 第一轮对抗辩论
每个 Agent 对分类后的论点进行攻击/防御：
- DA: 挑战核心主张的逻辑链
- ES: 质疑支撑证据的方法论
- AE: 提出至少 2 个替代解释
- BT: 识别结论的适用边界
- SJ: 初步综合，识别共识与分歧

### Step 5: 第二轮深化辩论
基于第一轮的 Memory，深化对抗：
- DA: 针对第一轮防御中的薄弱点
- ES: 追问证据的因果推断强度
- AE: 评估替代解释的似然度
- BT: 测试边界条件的极端情况
- SJ: 最终综合裁决

### Step 6: 共识与分歧映射
- 标记所有论点的共识度（1-5 级）
- 识别关键分歧点
- 评估分歧对结论的影响

### Step 7: 隐藏假设挖掘
- 从辩论中提取被揭示的隐藏假设
- 评估每个隐藏假设的合理性
- 标记高风险隐藏假设

### Step 8: 推理盲点识别
- 标记辩论中暴露的推理盲点
- 评估盲点对整体论证的影响
- 提出弥补方案

### Step 9: 安全性分析 (P-3 伦理 Path A)
- 基于 GT-HarmBench 评估基准框架进行安全分析
- 识别潜在的有害输出模式
- 评估研究结论的伦理风险
- 标记需要伦理审查的论点

### Step 10: 对抗结果综合
- 综合两轮辩论结果
- 生成修订后的论点列表（含置信度调整）
- 标记被削弱/被强化的论点

### Step 11: 穷尽重试判定逻辑
- FULL: 5 Agent × 2 轮完整辩论
- PARTIAL_A: 3 Agent × 2 轮（DA + ES + SJ）
- PARTIAL_B: 2 Agent × 1 轮（DA + SJ）
- RETRYING: 单 Agent 自我对抗（仅 DA 角色）

### Step 12: output_schema
```yaml
adversarial_synthesis:
  agents: [{name, role, claims_made: int, challenges_made: int}]
  rounds_completed: int
  core_claims:
    - {claim, original_confidence: float, revised_confidence: float, consensus_level: int(1-5)}
  hidden_assumptions:
    - {assumption, revealed_by: str, reasonability: "HIGH|MEDIUM|LOW", risk: "HIGH|MEDIUM|LOW"}
  reasoning_blindspots:
    - {blindspot, impact: "CRITICAL|HIGH|MEDIUM|LOW", mitigation: str}
  safety_analysis:
    harm_patterns: [str]
    ethical_risks: [str]
    gt_harmbench_alignment: bool
  equilibrium_analysis:
    equilibrium_type: "Nash|Pareto|Stackelberg|none"
    stability: "stable|unstable|metastable"
    conditions: [str]
    note: str
  consensus_map:
    full_consensus: [str]
    partial_consensus: [str]
    key_disagreements: [str]
  retrying: "FULL|PARTIAL_A|PARTIAL_B|RETRYING"
  retrying_reason: str|null
```

## self_check_before_output
- [ ] 5 个 Agent 角色是否全部参与
- [ ] 每轮是否引用前轮论点（Memory 机制）
- [ ] 共识度是否已映射
- [ ] 隐藏假设是否已挖掘
- [ ] 安全性分析是否基于 GT-HarmBench 评估基准
- [ ] 置信度调整是否合理
- [ ] equilibrium_analysis 包含 equilibrium_type/stability/conditions 三个必填字段

## must_not
- 不可跳过 Memory 机制
- 不可忽略安全性分析
- 不可将 GT-HarmBench 描述为工具（它是评估基准框架）
- 不可省略隐藏假设挖掘

## 方法论知识内化

### MC-057 RSI多智能体辩论方法论

**方法论原理**：RSI（Reasoning via Structured Interaction）多智能体辩论方法论的核心认知假设是——单一推理者的盲点无法通过"更努力地思考"来消除，只能通过外部视角的碰撞来暴露。每个推理者都有隐含的认知框架和假设，这些框架在自我反思中是透明的（因为反思本身就在同一框架内），但在与持不同框架的推理者交互时就会变得可见。RSI通过结构化的多轮序贯辩论，让每个智能体必须引用前轮论点（Memory机制），迫使推理从"各自为战"升级为"在对抗中逼近真理"。Memory机制是关键创新——没有它，辩论沦为并行独白；有了它，辩论成为递归深化的集体推理。

**执行步骤**：
1. 定义智能体角色：为每个Agent分配明确的对抗角色（DA/ES/AE/BT/SJ）
2. 建立辩论协议：确定轮次顺序、输出格式、Memory引用规则
3. 第一轮辩论：每个Agent按序发言，必须引用前轮论点
4. 提取第一轮产出：论点、证据、反驳、置信度
5. 第二轮深化辩论：基于第一轮Memory，针对薄弱点深化攻击
6. 提取第二轮产出：修订论点、新暴露的盲点、调整后的置信度
7. 综合裁决：Synthesis Judge基于两轮辩论产出综合裁决
8. 输出结构化结果：共识、分歧、隐藏假设、推理盲点

**决策规则**：

| 条件 | 决策 |
|------|------|
| 5 Agent × 2 轮完整执行 | FULL，输出完整对抗结果 |
| 3 Agent × 2 轮（DA+ES+SJ） | PARTIAL_A，缺少AE和BT视角 |
| 2 Agent × 1 轮（DA+SJ） | PARTIAL_B，仅基础对抗 |
| 单Agent自我对抗 | RETRYING，仅DA角色 |
| Agent未引用前轮论点 | 标注Memory机制违规，要求补充 |

**输出规范**：
```yaml
rsi_debate:
  agents: [{name: str, role: str, claims_made: int, challenges_made: int}]
  rounds_completed: int
  memory_references: [{from_agent: str, to_agent: str, round: int, referenced_claim: str}]
  core_claims:
    - {claim: str, original_confidence: float, revised_confidence: float, consensus_level: int(1-5)}
  retrying: "FULL|PARTIAL_A|PARTIAL_B|RETRYING"
```

**穷尽重试策略**：当Agent数量不足时，按FULL→PARTIAL_A→PARTIAL_B→RETRYING逐级穷尽重试，每级减少Agent角色和辩论轮次，最低保障DA角色的自我对抗。

> 知识来源: MC-057 [RSI多智能体辩论]

---

### MC-058 魔鬼代言人方法论

**方法论原理**：魔鬼代言人（Devil's Advocate）方法论的核心认知假设是——人类思维天然偏向确认偏误（confirmation bias），倾向于寻找支持自己观点的证据而忽略反对证据。魔鬼代言人通过系统性挑战每个核心论点，强制推理者面对自己最不愿意面对的反驳。这不是"为了反对而反对"，而是"为了发现盲点而反对"——魔鬼代言人的价值不在于赢得辩论，而在于暴露原论证中未被检验的假设和逻辑跳跃。这种方法论使我们从"自我确认的推理"升级为"经受过刻意挑战的推理"。

**执行步骤**：
1. 从论点列表中提取核心主张
2. 对每个核心主张，构造最强反驳（steel man而非straw man）
3. 识别支撑证据的方法论弱点（样本偏差、选择性引用、因果推断强度不足等）
4. 检验逻辑链的每一步推理是否存在跳跃
5. 评估结论的适用边界：在什么条件下结论不成立
6. 标记被削弱的论点和被强化的论点
7. 计算置信度调整量
8. 输出结构化挑战结果

**决策规则**：

| 条件 | 决策 |
|------|------|
| 核心主张逻辑链完整且证据充分 | 挑战结果为"论点稳健"，置信度微调（±0.05） |
| 逻辑链存在跳跃但可修补 | 挑战结果为"论点需修订"，置信度下调0.1-0.2 |
| 证据存在方法论弱点 | 挑战结果为"证据不足"，置信度下调0.2-0.3 |
| 核心假设被有效反驳 | 挑战结果为"论点被削弱"，置信度下调≥0.3 |
| 无法构造有效反驳 | 标注为"论点极稳健"，置信度不变或微升 |

**输出规范**：
```yaml
devils_advocate:
  challenges:
    - {target_claim: str, challenge_type: "logic_gap|evidence_weakness|assumption_invalid|boundary_violation", challenge_description: str, strength: "strong|moderate|weak", confidence_adjustment: float}
  weakened_claims: [str]
  strengthened_claims: [str]
  overall_assessment: str
```

**穷尽重试策略**：当无法构造有效反驳时，不强行挑战，标注为"论点极稳健，未发现有效反驳点"，避免为了挑战而制造虚假争议。

> 知识来源: MC-058 [魔鬼代言人]

---

### MC-059 共识映射方法论

**方法论原理**：共识映射方法论的核心认知假设是——多方观点之间的共识与分歧不是简单的"多数vs少数"，而是具有结构性的知识拓扑。不同观点之间可能存在部分重叠的共识区域、不可调和的分歧线、以及尚未被讨论的空白地带。共识映射通过可视化这些结构，使我们能够识别：哪些共识是真实的（基于相同理由达成一致）、哪些是虚假的（基于不同理由达成相同结论）、哪些分歧是原则性的（不可调和）、哪些是信息性的（可通过补充证据解决）。

**执行步骤**：
1. 收集所有参与方的观点和论据
2. 提取每个观点的核心主张和支撑理由
3. 识别观点间的共识区域：相同主张+相同理由=强共识；相同主张+不同理由=弱共识
4. 识别观点间的分歧线：不同主张的分歧类型（事实分歧/价值分歧/方法论分歧）
5. 评估分歧的可调和性：信息性分歧（可调和）vs原则性分歧（不可调和）
6. 识别未讨论的空白地带
7. 绘制共识-分歧拓扑图
8. 为每个共识/分歧分配共识度评分（1-5级）

**决策规则**：

| 条件 | 决策 |
|------|------|
| 共识度5（完全共识） | 标记为full_consensus，纳入最终结论 |
| 共识度3-4（部分共识） | 标记为partial_consensus，标注分歧细节 |
| 共识度1-2（关键分歧） | 标记为key_disagreement，分析分歧类型 |
| 分歧为信息性 | 标注"可通过补充证据解决" |
| 分歧为原则性 | 标注"不可调和，需条件化结论" |

**输出规范**：
```yaml
consensus_map:
  full_consensus: [str]
  partial_consensus: [{claim: str, agreement_reason: "same_reason|different_reason", dissent_detail: str}]
  key_disagreements: [{claim: str, disagreement_type: "factual|value|methodological", resolvability: "resolvable|irreconcilable"}]
  blank_areas: [str]
```

**穷尽重试策略**：当参与方观点信息不足时，穷尽重试为二元共识标注（同意/反对），不进行共识结构分析，标注"共识映射不完整，缺少理由层面分析"。

> 知识来源: MC-059 [共识映射]

---

### MC-060 隐藏假设挖掘方法论

**方法论原理**：隐藏假设挖掘方法论的核心认知假设是——任何论证都建立在未明说的假设之上，而这些隐藏假设往往是论证最脆弱的环节。显式假设可以被检验和修正，但隐藏假设在未被意识到的情况下持续影响推理，形成"看不见的风险"。隐藏假设挖掘不是简单的"找漏洞"，而是系统性地将论证的隐含前提暴露出来，评估其合理性，识别高风险假设。这种方法论使我们从"基于未检验假设的推理"升级为"基于已检验假设的推理"。

**执行步骤**：
1. 从论点中提取显式前提和结论
2. 对每个推理步骤，追问"这个推理隐含了什么前提？"
3. 识别四类隐藏假设：事实假设（关于世界状态的假设）、逻辑假设（关于推理规则的假设）、价值假设（关于好坏判断的假设）、范围假设（关于适用范围的假设）
4. 评估每个隐藏假设的合理性：HIGH（有强证据支撑）/MEDIUM（有弱证据支撑）/LOW（无证据支撑或与已知矛盾）
5. 标记高风险隐藏假设：合理性为LOW且对结论影响大的假设
6. 评估隐藏假设对结论的影响：如果该假设不成立，结论如何变化
7. 提出假设检验建议：如何验证或证伪高风险隐藏假设
8. 输出结构化隐藏假设清单

**决策规则**：

| 条件 | 决策 |
|------|------|
| 隐藏假设合理性HIGH | 标注为低风险，不影响结论 |
| 隐藏假设合理性MEDIUM | 标注为中风险，需在结论中条件化 |
| 隐藏假设合理性LOW | 标注为高风险，结论需附加警告 |
| 高风险假设≥3个 | 整体论证可信度下调，建议补充证据 |
| 高风险假设使核心结论不成立 | 标注为CRITICAL，建议重新构建论证 |

**输出规范**：
```yaml
hidden_assumptions:
  - {assumption: str, type: "factual|logical|value|scope", revealed_by: str, reasonability: "HIGH|MEDIUM|LOW", risk: "HIGH|MEDIUM|LOW", impact_if_invalid: str, verification_suggestion: str}
  critical_assumptions: [str]
  overall_argument_strength: "strong|moderate|weak|critical"
```

**穷尽重试策略**：当论点信息不足以进行深层假设挖掘时，穷尽重试为表层假设列举：仅识别最明显的隐含前提，不进行合理性评估和风险标注，标注"隐藏假设挖掘不完整，仅覆盖表层假设"。

> 知识来源: MC-060 [隐藏假设挖掘]

---

### MC-135 安全评估方法论（GT-HarmBench）

**方法论原理**：GT-HarmBench安全评估方法论的核心认知假设是——研究结论可能产生非意图的有害后果，而这种风险不能仅靠研究者的善意来防范，需要系统化的安全评估框架。GT-HarmBench不是工具，而是一个评估基准框架，定义了有害输出模式的分类体系和检测标准。安全评估与伦理分析（MC-071）的区别在于：安全评估关注"输出可能造成什么伤害"，伦理分析关注"研究过程和结论的伦理正当性"。这种方法论使我们从"假设研究无害"升级为"主动检测潜在伤害"。

**执行步骤**：
1. 识别研究结论的潜在输出模式：信息型输出、建议型输出、预测型输出
2. 对每种输出模式，评估可能的有害使用场景
3. 使用GT-HarmBench分类体系标注有害模式类型：误导性信息、歧视性建议、隐私泄露、激化冲突等
4. 评估每种有害模式的严重性和可能性
5. 标记需要伦理审查的论点
6. 评估研究结论的伦理风险等级
7. 提出风险缓解建议
8. 输出结构化安全评估报告

**决策规则**：

| 条件 | 决策 |
|------|------|
| 未发现有害模式 | 安全评估通过，标注gt_harmbench_alignment=true |
| 发现低严重性有害模式 | 标注警告，建议添加使用限制声明 |
| 发现高严重性有害模式 | 标注为伦理风险，建议修改结论表述 |
| 发现CRITICAL级有害模式 | 建议限制输出范围或重新评估研究结论 |

**输出规范**：
```yaml
safety_evaluation:
  harm_patterns: [str]
  ethical_risks: [str]
  risk_levels: [{pattern: str, severity: "LOW|MEDIUM|HIGH|CRITICAL", likelihood: "LOW|MEDIUM|HIGH"}]
  gt_harmbench_alignment: bool
  mitigation_suggestions: [str]
```

**穷尽重试策略**：当GT-HarmBench框架不可用时，穷尽重试为基础安全检查：仅检测最明显的有害模式（歧视性表述、隐私泄露等），不使用完整分类体系，标注"安全评估不完整，仅覆盖基础检查"。

> 知识来源: MC-135 [GT-HarmBench安全评估]

---

### TC-079 GenerativeAgents社会涌现模拟方法论

**方法论原理**：GenerativeAgents方法论的核心认知假设是——社会涌现现象（观点极化、共识形成、信息级联）无法通过静态分析预测，只能通过让异质智能体在时间维度上持续互动来观察。其关键创新在于三层认知架构：记忆流（Memory Stream）提供经验的时间连续性，反思（Reflection）机制从经验中提取高层抽象，计划（Plan）生成将抽象意图转化为具体行动序列。在对抗综合场景中，这意味着每个Agent不是简单地"持有立场"，而是通过记忆积累和反思调整动态演化其立场——这种动态演化过程本身就是对抗综合需要捕捉的核心数据。对话策略则确保互动不是随机噪声，而是有方向性的社会影响力博弈。

**执行步骤**：
1. 定义Agent群体：为每个Agent设定身份特征（背景、价值观、初始立场）、社会关系网络、环境感知范围
2. 构建记忆流：初始化每个Agent的记忆流，包含初始观察和背景知识，设定记忆检索函数（相关性×近期性×重要性加权）
3. 配置反思触发：设定反思触发条件（累积重要性阈值或固定时间间隔），反思从记忆流中提取高层洞察并写入记忆
4. 生成行动计划：基于当前记忆和反思，让Agent生成日计划→小时计划→即时行动的三层计划树
5. 执行沙盒互动：Agent按计划行动，在共享环境中产生观察事件，触发其他Agent的记忆更新
6. 对话交互：当Agent相遇时，基于双方记忆和当前意图生成对话，对话内容写入双方记忆流
7. 追踪涌现指标：持续监测观点分布变化、信息传播路径、子群体形成、极化/收敛趋势
8. 提取对抗综合数据：从涌现过程中提取说服事件链、立场转变轨迹、关键影响节点

**决策规则**：

| 条件 | 决策 |
|------|------|
| Agent ≥ 5 且互动 ≥ 50轮 | FULL，完整社会涌现模拟 |
| Agent 3-4 且互动 ≥ 30轮 | PARTIAL_A，子群体涌现可能不完整 |
| Agent 2 且互动 ≥ 20轮 | PARTIAL_B，仅双人说服博弈 |
| 单Agent + 模拟对手 | RETRYING，穷尽重试：转为自我对抗 |
| 反思机制未触发 | 标注"反思层缺失，Agent行为可能缺乏深度调整" |
| 记忆流检索失败 | 穷尽重试为最近N条记忆直接访问，标注"记忆检索穷尽重试" |

**输出规范**：
```yaml
generative_agents_simulation:
  agents: [{id: str, identity: str, initial_stance: float, final_stance: float, stance_shift: float}]
  memory_stream_stats: {total_observations: int, reflections_triggered: int, avg_retrieval_depth: int}
  emergence_metrics:
    opinion_polarization: float  # 观点极化指数
    information_cascade_events: [{source: str, path: [str], reach: int}]
    subgroup_formation: [{members: [str], cohesion: float}]
    consensus_zones: [{topic: str, agreement_level: float}]
  persuasion_events: [{persuader: str, persuadee: str, mechanism: str, stance_delta: float}]
  retrying: "FULL|PARTIAL_A|PARTIAL_B|RETRYING"
```

**穷尽重试策略**：当GenerativeAgents框架不可用时：L1→使用Mesa ABM（TC-055）+ LLM角色扮演替代，保留Agent/Model/Schedule结构但用LLM生成对话；L2→使用纯LLM多角色辩论（MC-057 RSI），省略记忆流和反思层；L3→使用手动角色扮演，人类模拟不同立场Agent的互动；L4→使用静态立场分析，仅分析各方立场差异不做动态模拟，标注"社会涌现模拟不可用，仅提供静态对抗分析"。

> 知识来源: TC-079 [GenerativeAgents]

---

### [GenerativeAgents] 源码逻辑引入

#### 核心算法逻辑

**1. 记忆流数据结构源码逻辑**

```
记忆流核心结构（generative_agents/memory.py）:

class MemoryStream:
    # 记忆流：按时间排序的记忆列表
    memories: list[Memory]

    def add(self, content, timestamp, importance):
        memory = Memory(
            content=content,           # 记忆文本描述
            timestamp=timestamp,       # 创建时间
            importance=importance,     # 重要性评分(1-10)
            last_accessed=timestamp,   # 最后访问时间
            embedding=embed(content)   # 语义嵌入向量
        )
        self.memories.append(memory)

    def retrieve(self, query, top_k=10):
        # 三维检索评分: 相关性 × 近因性 × 重要性
        scores = []
        for memory in self.memories:
            relevance = cosine_similarity(embed(query), memory.embedding)
            recency = decay_function(current_time - memory.last_accessed)
              # recency = 0.99 ^ (hours_since_access)
              # 每小时衰减1%，约3天后衰减至约50%
            importance = memory.importance / 10.0  # 归一化到0-1

            # 综合评分（默认等权重）
            score = relevance + recency + importance
            scores.append((memory, score))

        # 返回top_k个最高评分记忆
        return sorted(scores, key=lambda x: -x[1])[:top_k]

class Memory:
    content: str              # 记忆内容
    timestamp: datetime       # 创建时间
    importance: float         # 重要性(1-10)
    last_accessed: datetime   # 最后访问时间
    embedding: list[float]    # 语义嵌入
```

**2. 反思触发逻辑源码逻辑**

```
反思触发机制（generative_agents/reflection.py）:

function should_reflect(agent, current_time):
    # 反思阈值：当Agent的近期记忆重要性总和超过阈值时触发反思
    recent_memories = agent.memory_stream.retrieve(
        query="recent events",
        top_k=100
    )

    # 计算近期记忆的重要性总和
    importance_sum = sum(m.importance for m in recent_memories
                         if (current_time - m.timestamp).hours < 8)

    # 阈值判定（默认阈值=150）
    if importance_sum > REFLECTION_THRESHOLD:
        return True
    return False

function generate_reflection(agent, current_time):
    # 步骤1：检索近期重要记忆
    recent_memories = agent.memory_stream.retrieve(
        query="what has been happening recently",
        top_k=100
    )

    # 步骤2：生成反思问题
    reflection_questions = LLM.generate(
        prompt=f"Given these recent events: {recent_memories}, "
               f"generate 3 high-level questions about the agent's experiences."
    )

    # 步骤3：对每个问题检索相关记忆并生成洞察
    insights = []
    for question in reflection_questions:
        related_memories = agent.memory_stream.retrieve(
            query=question, top_k=20
        )
        insight = LLM.generate(
            prompt=f"Based on these memories: {related_memories}, "
                   f"answer the question: {question}"
        )
        insights.append(insight)

    # 步骤4：将反思洞察作为高重要性记忆存入记忆流
    for insight in insights:
        agent.memory_stream.add(
            content=insight,
            timestamp=current_time,
            importance=8  # 反思记忆默认高重要性
        )

    return insights
```

**3. 计划生成算法源码逻辑**

```
计划生成与执行（generative_agents/plan.py）:

function generate_daily_plan(agent, current_date):
    # 步骤1：基于Agent身份和近期反思生成日计划
    identity = agent.identity  # 姓名、年龄、特质、当前状态
    recent_reflections = agent.memory_stream.retrieve(
        query="reflections about life", top_k=5
    )

    daily_plan = LLM.generate(
        prompt=f"Agent {identity.name} is a {identity.age}-year-old "
               f"with traits: {identity.traits}. "
               f"Recent reflections: {recent_reflections}. "
               f"Plan their day in broad strokes (5-8 activities)."
    )

    # 步骤2：将日计划分解为小时级计划
    hourly_plans = []
    for activity in daily_plan:
        hour_plan = LLM.generate(
            prompt=f"Decompose '{activity}' into specific hourly actions "
                   f"from {activity.start_time} to {activity.end_time}."
        )
        hourly_plans.append(hour_plan)

    # 步骤3：将计划存入记忆流
    for plan in hourly_plans:
        agent.memory_stream.add(
            content=f"Plan: {plan.description}",
            timestamp=current_date + plan.start_time,
            importance=5
        )

    return hourly_plans

function execute_plan_step(agent, current_time):
    # 获取当前应执行的计划步骤
    current_plan = agent.get_current_plan(current_time)

    # 检查是否需要重新规划（环境变化或社交中断）
    if needs_replan(agent, current_time):
        new_plan = LLM.generate(
            prompt=f"Agent was planning '{current_plan}' but "
                   f"{agent.get_recent_interruption()}. "
                   f"Generate a new plan for the rest of the hour."
        )
        return new_plan

    return current_plan

function needs_replan(agent, current_time):
    # 重新规划触发条件:
    # 1. 被其他Agent发起对话中断
    # 2. 当前计划已完成
    # 3. 环境发生重大变化
    recent_events = agent.memory_stream.retrieve(
        query="interruptions and changes", top_k=5
    )
    for event in recent_events:
        if "conversation" in event.content or "interruption" in event.content:
            if (current_time - event.timestamp).minutes < 30:
                return True
    return False
```

#### 数据结构设计

```
核心数据结构:

1. MemoryStream: 记忆流
   - memories: list[Memory]          # 按时间排序的记忆列表
   - add(content, timestamp, importance): 添加记忆
   - retrieve(query, top_k): 三维检索

2. Memory: 单条记忆
   - content: str                    # 记忆内容
   - timestamp: datetime             # 创建时间
   - importance: float (1-10)        # 重要性评分
   - last_accessed: datetime         # 最后访问时间
   - embedding: list[float]          # 语义嵌入向量

3. Plan: 计划条目
   - description: str                # 计划描述
   - start_time: datetime            # 开始时间
   - end_time: datetime              # 结束时间
   - location: str                   # 执行地点
   - status: PENDING|ACTIVE|COMPLETED|INTERRUPTED

4. Reflection: 反思洞察
   - question: str                   # 反思问题
   - insight: str                    # 生成洞察
   - source_memories: list[Memory]   # 来源记忆
   - importance: float (默认8)       # 反思记忆高重要性
```

#### 决策流程

```
GenerativeAgents 行为决策流程:

1. 环境感知 → 检索记忆流中与当前情境相关的记忆
2. 反思检查 → should_reflect() 判断是否触发反思
   ├─ 重要性总和 > 阈值 → generate_reflection() 生成高层洞察
   └─ 未达阈值 → 继续
3. 计划执行 → execute_plan_step() 执行当前计划步骤
   ├─ 需要重新规划 → LLM生成新计划
   └─ 按计划执行 → 执行当前步骤
4. 社交互动 → 检测附近Agent，触发对话生成
5. 记忆更新 → 将新经历存入记忆流
```

#### 穷尽重试策略

```yaml
generative_agents_source_retrying:
  L1_FULL_FRAMEWORK:
    condition: "GenerativeAgents框架可用，记忆流+反思+计划均可执行"
    action: "完整记忆流检索+反思触发+计划生成+社交涌现"
    confidence: "HIGH"

  L2_MESA_LLM:
    condition: "GenerativeAgents不可用，但Mesa+LLM可用"
    action: "使用Mesa ABM框架+LLM角色扮演替代，保留Agent/Model/Schedule结构"
    confidence: "MEDIUM"
    output_annotation: "GenerativeAgents穷尽重试：Mesa ABM + LLM角色扮演"

  L3_LLM_DEBATE:
    condition: "Mesa不可用，但LLM可用"
    action: "纯LLM多角色辩论（MC-057 RSI），省略记忆流和反思层"
    confidence: "LOW-MEDIUM"
    output_annotation: "GenerativeAgents穷尽重试：纯LLM多角色辩论"

  L4_STATIC_ANALYSIS:
    condition: "LLM不可用或资源不足"
    action: "静态立场分析，仅分析各方立场差异不做动态模拟"
    confidence: "LOW"
    output_annotation: "GenerativeAgents穷尽重试保底：静态立场分析"
```

---

## knowledge_refs
- MC-057 递归序贯推理-Multi-Agent-Debate
- MC-058 Devils-Advocate-Framework
- MC-059 Consensus-Mapping
- MC-060 Hidden-Assumption-Mining
- MC-135 GT-HarmBench-Safety-Evaluation
- TC-060 递归序贯推理 (Reasoning via Structured Interaction)
- TC-079 GenerativeAgents: 部署多个持不同立场的生成式智能体在沙盒中互动，观察观点碰撞、说服、妥协和极化的社会涌现过程。详见 `knowledge/external-capabilities/TC-079-GenerativeAgents.md`
- TC-081 Pol.is: 利用意见分组算法识别多方观点中的共识区域和不可调和的分歧线。详见 `knowledge/external-capabilities/TC-081-Polis.md`
- MC-075 CGT: 利用范畴论极限/余极限实现多视角对抗论点的结构化综合，生成超越单一视角的元视角。详见 `knowledge/external-capabilities/MC-075-CGT.md`
- MC-142 Nash-Equilibrium: 纳什均衡求解（纯策略与混合策略均衡 + 互为最优响应判定），在 Step 2 多智能体博弈仿真中用于求解各Agent策略的均衡状态，识别是否存在稳定策略组合。详见 `knowledge/external-capabilities-index.md`
- TC-087 OpenSpiel: 在多智能体博弈仿真中，当参与者 ≥ 3 或策略空间 ≥ 5 时，调用 OpenSpiel 进行算法化均衡求解，验证各 Agent 策略的均衡状态。详见 `knowledge/external-capabilities-index.md`


### TC-081 Pol.is 共识发现方法论

**方法论原理**：Pol.is基于"共识发现不需要对话而需要统计聚合"的认知假设——传统共识形成依赖对话，但对话易被强势声音主导。Pol.is通过让参与者对陈述进行同意/反对投票，再用PCA降维可视化意见分布，使沉默多数和少数派意见同时可见。这种方法论将共识发现从"对话协商"升级为"统计聚合+可视化"——不需要各方达成口头一致，只需识别出所有群体都同意的陈述（共识区域）和将群体分开的陈述（分歧线），从而在保留分歧的前提下找到可行动的共识基础。

**核心步骤**：
1. 意见采集：通过投票机制采集多方意见
2. 意见分组：使用PCA降维和聚类算法识别意见分组
3. 共识区域识别：识别所有组都同意的陈述（共识区域）
4. 分歧线识别：识别将不同组分开的陈述（分歧线）
5. 可视化呈现：生成交互式意见地图

**决策规则**：需要大规模群体共识发现时使用Pol.is；小规模使用共识映射(MC-059)

**输出规范**：
```yaml
polis_consensus:
  available: bool
  participant_count: int
  statement_count: int
  opinion_groups:
    - {group_id: int, size: int, pca_centroid: [float], key_positions: [str]}
  consensus_areas:
    - {statement: str, agreement_ratio: float, groups_agreeing: [int]}
  division_lines:
    - {statement: str, group_a_position: str, group_b_position: str, divisiveness_score: float}
  pca_visualization: {available: bool, dimensions: int, explained_variance: [float]}
  retrying_note: str|null
```

**穷尽重试策略**：Pol.is → PCA/聚类分析+手动共识标注 → Delphi方法+结构化问卷

> 知识来源: TC-081 Polis
