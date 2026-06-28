# 辩证分析 — 正反合统一与多主体博弈

> **模块标识**: `knowledge/thinking-models/general/dialectical-analysis`
> **来源**: TM-005 (多智能体辩论)、TM-006 (魔鬼代言人)、TM-009 (共识生成器)、TM-030 (钢化论证生成)、TM-042 (多智能体博弈)、TM-023 (博弈论框架)
> **依赖**: `knowledge/research-methods`、`knowledge/cognitive-framework`
> **父模型**: `knowledge/thinking-models/general/critical-thinking`

---

## 1. 定义

辩证分析是一种通过正反意见的对抗性交锋来检验命题可靠性的思维方法。它不满足于单方面的论证，而是通过系统化的"建设性支持者"与"严格批评者"之间的结构化辩论，暴露论证的薄弱环节，最终在更高层次上形成整合性结论。在此基础上，融入多主体博弈视角，分析多方利益主体的策略互动。

**核心法则**: 如果没有人试图推翻你的结论，你就不配持有它。

---

## 2. 核心概念

| 概念 | 定义 | 执行方式 |
|------|------|---------|
| **人格化角色** | 将不同分析视角人格化为独立角色 | 每个角色有明确的立场、知识范围和动机 |
| **独立推理轮** | 每个角色在不受其他角色影响下独立分析 | 角色间信息隔离，避免一个角色的推理污染另一个 |
| **交叉批评轮** | 角色间相互攻击论证的弱点和盲区 | 每个角色必须对至少一个其他角色的论证提出实质性挑战 |
| **收敛综合轮** | 基于辩论结果整合为稳健结论 | 共识/争议/未解决问题三分类输出 |
| **钢化论证** | 经受住魔鬼代言人攻击后修正的论证 | 输出不是初始论证，是经过攻击后存活的修正版 |
| **纳什均衡分析** | 多主体博弈中谁也无法单方面改善的状态 | 在涉及多方利益的决策中识别均衡点 |

---

## 3. 三阶段辩证流程

```
阶段一: 正题建立（建设性支持者）
  │
  ├─ 目标: 为命题构建最强支持论证
  ├─ 行为: 收集证据、建立因果链、回应已知反对
  │
  ▼
阶段二: 反题攻击（严格批评者 + 多角色博弈）
  │
  ├─ 角色1 魔鬼代言人: 寻找逻辑漏洞、反例、证据薄弱点
  ├─ 角色2 多Agent博弈: 迭代推演对立立场的策略互动
  ├─ 角色3 偏见检测: 识别论证中的认知偏误
  ├─ 角色4 证据核查: 验证关键声明的可核验性
  │
  ▼
阶段三: 合题升华（收敛综合）
  │
  ├─ 输出1: 经受住攻击的钢化论证
  ├─ 输出2: 在攻击中被削弱的论证（标注削弱原因）
  ├─ 输出3: 被攻击推翻的论证（标注推翻证据）
  ├─ 输出4: 博弈均衡点（如在多主体情境中）
  └─ 输出5: 未解决争议（标注无法解决的原因）
```

---

## 4. 结构化辩论规则

### 4.1 独立推理轮规则

- 每个角色使用独立的分析框架和知识范围
- 角色之间在第一轮不分享推理过程
- 禁止"我知道另一个角色会说什么所以..."
- 每个角色产出的论证必须自包含且可独立评估

### 4.2 交叉批评轮规则

- 批评必须指向具体论证环节，不得笼统攻击
- 每个批评必须附带"如果被批评方是对的，需要什么证据？"的探测问题
- 批评方也必须声明自己论证中最薄弱的环节（对称性义务）
- 禁止人身攻击式批评（"这个论证太愚蠢了"）

### 4.3 收敛综合轮规则

- 共识以"双方同意的最高限度"而非"最低共同点"为准
- 争议点必须具体化：不是说"我们有分歧"，而是"在X条件下对Y问题的Z判断上我们有分歧"
- 未解决问题必须标注无法解决的原因：证据不足/逻辑不可判定/价值观差异/未知未知
- 收敛不追求消灭所有分歧，追求最大化可操作共识

---

## 5. 钢化论证标准

一个论证经过辩证分析后，只有满足以下全部条件才能称为"钢化论证"：

1. 魔鬼代言人已对每个核心命题发起至少1次攻击
2. 攻击后的论证版本明显比原始版本更精确（范围更窄、条件更明确）
3. 攻击揭示了论证的真正边界——在什么条件下论证成立、什么条件下不成立
4. 剩余的不确定性已被明确标注而非隐含
5. 替代解释已被认真检验并合理排除
6. **博弈稳定**: 论证经受住多主体博弈的交替迭代

---

## 6. 多主体博弈分析

### 6.1 适用范围
问题涉及多方决策主体（>= 2方），且各方之间存在策略性互动（一方的选择影响另一方的收益）。

### 6.2 分析流程

```
识别参与方 → 定义策略空间 → 构建收益矩阵 → 寻找纳什均衡 → 演化稳定性分析
```

- **识别参与方**: >= 3 方，标注势力对比和偏好顺序
- **定义策略空间**: 每方的可选行动和行动顺序
- **构建收益矩阵**: 对所有策略组合标注收益值
- **寻找纳什均衡**: 纯策略和混合策略均衡
- **演化稳定性**: 均衡在动态扰动下是否稳定

---

## 7. 常见陷阱

1. **稻草人辩论**: 批评方攻击的是一个被弱化的、真实的论证更强于的版本。**纠正**: 批评前的第一步是"我理解的对吗？请确认这就是你的主张"。
2. **假辩证真偏袒**: 表面上进行了正反辩论，实际上给"正方"更多篇幅和资源，"反方"只是走过场。**纠正**: 正反方使用对称的分析资源和对等的篇幅。
3. **无收敛辩论**: 辩论后不整合，停留在"双方各有道理"的模糊状态。**纠正**: 辩论必须产出可操作的收敛综合——哪怕结论是"当前无法判定"也需要具体说明无法判定的原因。
4. **人格化角色失实**: 角色不代表真实的利益方，而是分析者的单一视角投射。**纠正**: 检查每个角色的立场是否代表了真实存在的、可在现实中找到对应群体的利益。
5. **博弈过度简化**: 将复杂博弈简化为零和博弈或囚徒困境。**纠正**: 先检查博弈是否为零和，大多数实际博弈有合作空间。

---

## 8. 输出模板

```yaml
dialectical_analysis:
  thesis:
    - conclusion_id: "CON-001"
      strongest_evidence: ["最强支持证据"]
      weakest_link: "最薄弱环节"
  antithesis:
    attacks:
      - target: "CON-001"
        attack_type: "logic_flaw/evidence_gap/counter_example/scope_overreach/bias"
        severity: "critical/significant/minor"
        rebuttal: "被攻击方的回应"
        attacker_concession: "攻击方承认的对立方优势"
  game_theory:
    players:
      - name: "参与方名称"
        preferences: ["偏好排序"]
        strategies: ["可选策略"]
    nash_equilibria: ["纳什均衡点"]
    evolutionary_stability: "演化稳定性分析"
  synthesis:
    steelmanned_arguments: ["钢化论证清单"]
    weakened_arguments: ["被削弱的论证清单"]
    refuted_arguments: ["被推翻的论证清单"]
    unresolved_controversies: ["未解决争议及其原因"]
    consensus_maximum: "最可能达成共识的结论"
  aafs_formal_verification:
    description: "pygarg 形式化论证计算（v3 新增）"
    capability_card: "TC-085 pygarg"
    framework: "AAFs (Abstract Argumentation Frameworks)"
    argument_set: ["论证A1: ...", "论证A2: ...", "论证A3: ..."]
    attack_relations: [["A1", "A2"], ["A2", "A3"]]  # A1攻击A2, A2攻击A3
    semantics:
      admissible: ["可容许论证集合"]
      complete: ["完备论证集合"]
      preferred: ["优先论证集合"]
      stable: ["稳定论证集合"]
    verdict: "四种语义下的数学判定结果，替代纯LLM论证评估"
```

---

## 9. pygarg 形式化论证计算（v3 新增）

> **能力卡**: TC-085 pygarg

在输出 `steelmanned_arguments` 之前，对论证结构执行 AAFs（Abstract Argumentation Frameworks）形式化计算：

### 9.1 AAFs 语义判定

将辩证分析的论证映射为抽象论证框架：

```
AAF = ⟨Args, Att⟩
其中:
  Args = {A1, A2, ..., An}  — 论证集合
  Att ⊆ Args × Args         — 攻击关系（Ai 攻击 Aj）
```

### 9.2 四种语义数学判定

| 语义 | 定义 | 判据 |
|------|------|------|
| **admissible（可容许）** | 集合 S 内部无冲突且能防御所有外部攻击 | S 无冲突 ∧ ∀a∈Args, 若 a 攻击 S 中某元素则 S 中有元素攻击 a |
| **complete（完备）** | 可容许且包含所有被防御的论证 | admissible(S) ∧ ∀a∈Args, 若 S 防御 a 则 a∈S |
| **preferred（优先）** | 最大完备集合 | complete(S) ∧ 不存在 complete(S') 且 S⊂S' |
| **stable（稳定）** | 攻击所有不在集合中的论证 | 无冲突 ∧ ∀a∉S, ∃b∈S 使得 b 攻击 a |

### 9.3 在辩证分析中的应用

- 将"正方论证"和"反方攻击"映射为 AAFs 的论证与攻击关系
- 计算四种语义下的外延（extension），判定哪些论证是"可容许的"、"完备的"、"优先的"、"稳定的"
- 将判定结果写入 `aafs_formal_verification` 字段
- 若四种语义下结论一致 → 高置信度结论；若不一致 → 标注语义分歧及原因

---

## 10. 辩证分析决策规则

| 条件 | 判定 | 行动 |
|------|------|------|
| 正方论证经受住所有反方攻击 | 钢化论证 | 输出为高置信度结论 |
| 正方论证被部分削弱但未推翻 | 条件性论证 | 标注削弱原因和条件边界 |
| 正方论证被推翻 | 无效论证 | 不输出该结论，分析推翻原因 |
| 存在未解决争议 | 开放问题 | 标注争议原因（证据不足/逻辑不可判定/价值观差异） |
| AAFs四种语义一致 | 高置信度 | 可作为强推理依据 |
| AAFs四种语义不一致 | 语义分歧 | 标注分歧原因，降低结论置信度 |
| 博弈均衡为帕累托最优 | 合作解 | 推荐合作策略 |
| 博弈均衡为囚徒困境 | 非合作解 | 评估改变博弈结构的可能性 |
| 正反方使用不对称资源 | 假辩证风险 | 强制对称化资源分配 |

> 知识来源: MC-161 Aufheben-Synthesis / MC-172 Steelmanning

---

## 11. 辩证分析穷尽重试策略

| 重试层级 | 条件 | 替代方案 |
|---------|------|---------|
| L1 完整三阶段辩证+AAFs | 正反方可独立推理、pygarg可用 | 完整正题-反题-合题+AAFs形式化验证 |
| L2 三阶段辩证无AAFs | pygarg不可用 | 完整正题-反题-合题，标注"无形式化验证" |
| L3 正反方辩论 | 无法做收敛综合 | 做正反方辩论，标注"无收敛综合" |
| L4 单方论证+自我批评 | 无法构造独立反方 | 做单方论证+自我批评，标注"无独立反方" |

> 知识来源: MC-161 Aufheben-Synthesis / MC-172 Steelmanning

---

## 12. 内化方法论：扬弃综合法（MC-161 Aufheben-Synthesis）

### 方法论原理

扬弃综合法的方法论基础是：**辩证分析的终极目标不是"正方赢了"或"反方赢了"，而是在更高层次上实现"扬弃"（Aufheben）——同时保留正反方的合理内核、抛弃各自的片面性、在新的综合中超越对立**。扬弃不是折中（各取一半），而是质变——综合后的结论是正反方都不曾达到的新层次。这一方法论之所以必要，是因为最常见的辩证分析失败是"假综合"——看似综合，实则是"正方说了A，反方说了B，所以A和B都有道理"的模糊折中，而非真正的超越性综合。

### 执行步骤

1. **提取正方合理内核**：从正方论证中提取经受住攻击的核心论点
2. **提取反方合理内核**：从反方攻击中提取揭示的真问题
3. **识别对立根源**：正反方为什么对立？是事实分歧、价值分歧还是框架分歧？
4. **超越性重构**：在更高层次上重新定义问题框架，使正反方的合理内核在新框架中不再对立
5. **综合验证**：检验综合结论是否同时容纳了正反方的合理内核，且超越了原始对立

### 决策规则

| 对立根源 | 综合策略 | 综合质量判定 |
|---------|---------|------------|
| 事实分歧 | 补充证据，以事实裁定 | 若证据可得→高质综合；若不可得→标注"事实待定" |
| 价值分歧 | 识别价值前提，做条件性综合 | 若可找到共同价值前提→条件性综合；若不可→标注"价值不可调和" |
| 框架分歧 | 在元层次重构框架 | 若可重构→高质综合；若不可→标注"框架不可通约" |
| 规模分歧（正方适用大尺度，反方适用小尺度） | 分尺度综合 | 在不同尺度上分别成立，标注"分尺度综合" |

### 输出规范

```yaml
aufheben_synthesis:
  thesis_core: "正方合理内核"
  antithesis_core: "反方合理内核"
  opposition_root: "事实分歧/价值分歧/框架分歧/规模分歧"
  synthesis:
    higher_framework: "更高层次的问题框架"
    preserved_from_thesis: ["保留的正方内核"]
    preserved_from_antithesis: ["保留的反方内核"]
    transcended_opposition: "超越的对立点"
    new_insight: "综合产生的新洞见"
  verification:
    accommodates_thesis_core: true|false
    accommodates_antithesis_core: true|false
    transcends_original_opposition: true|false
  synthesis_quality: "high/conditional/failed"
```

### 穷尽重试策略

| 重试层级 | 条件 | 替代方案 |
|---------|------|---------|
| L1 完整扬弃综合 | 正反方合理内核可提取、对立根源可识别 | 完整5步，输出超越性综合 |
| L2 条件性综合 | 对立根源可识别但无法完全超越 | 做条件性综合，标注"条件性成立" |
| L3 折中综合 | 无法做超越性综合 | 做折中（各取合理部分），标注"折中非扬弃" |
| L4 并列呈现 | 正反方无法综合 | 并列呈现正反方论证，标注"无法综合" |

> 知识来源: MC-161 Aufheben-Synthesis

---

## 13. 内化方法论：钢化论证法（MC-172 Steelmanning）

### 方法论原理

钢化论证法的方法论基础是：**真正有力的论证不是从未被攻击的论证，而是经受住最严厉攻击后仍然存活的论证**。"钢化"（Steelmanning）与"稻草人"相反——不是弱化对手的论证以便攻击，而是强化对手的论证至其最强版本后再检验自己的论证能否抵御。这一方法论之所以必要，是因为最常见的论证自满是"只与弱版对手辩论"——攻击一个被弱化的对手当然能赢，但这不证明自己的论证真的可靠。只有与最强版对手辩论并存活，论证才值得信赖。

### 执行步骤

1. **识别对手论证**：准确陈述对手的论证（不弱化、不歪曲）
2. **强化对手论证**：将对手论证强化至其最强版本——补充缺失前提、修正逻辑漏洞、添加最强证据
3. **自我论证攻击**：用强化后的对手论证攻击自己的论证
4. **存活检验**：自己的论证在攻击后是否仍然成立？
5. **修正与钢化**：若论证被削弱，修正后重新接受攻击；若论证存活，输出为钢化论证

### 决策规则

| 攻击结果 | 判定 | 行动 |
|---------|------|------|
| 论证在最强攻击下完整存活 | 钢化论证 | 输出为高置信度结论 |
| 论证被部分削弱但核心成立 | 半钢化论证 | 修正薄弱环节，标注条件边界 |
| 论证被推翻 | 未钢化论证 | 重新构建论证或接受对手论证 |
| 无法构造对手的最强版本 | 对手论证不可强化 | 标注"对手论证本身薄弱，钢化测试不适用" |

### 输出规范

```yaml
steelmanning_analysis:
  original_argument: "原始论证陈述"
  opponent_argument:
    original: "对手原始论证"
    strengthened: "强化后的对手论证"
    strengthening_steps: ["强化步骤"]
  attack_results:
    - attack_point: "攻击点"
      defense: "自我论证的防御"
      outcome: "survived/weakened/defeated"
  steelmanned_argument:
    statement: "钢化后的论证陈述"
    conditions: ["成立条件"]
    boundaries: ["论证边界"]
    remaining_vulnerabilities: ["残余脆弱点"]
  confidence: "high/medium/low"
```

### 穷尽重试策略

| 重试层级 | 条件 | 替代方案 |
|---------|------|---------|
| L1 完整钢化论证 | 对手论证可识别和强化 | 完整5步，输出钢化论证 |
| L2 部分钢化 | 对手论证仅可部分强化 | 对可强化部分做钢化，标注"部分钢化" |
| L3 自我批评 | 无法构造对手论证 | 做自我批评式攻击，标注"无对手钢化" |
| L4 论证陈述 | 无法做任何攻击 | 仅陈述论证和已知弱点，标注"无钢化测试" |

> 知识来源: MC-172 Steelmanning

---

## 14. 内化方法论：pygarg AAFs 形式化论证计算（TC-085）

> **能力卡**: TC-085 pygarg

### 14.1 核心原理

pygarg 是抽象论证框架（Abstract Argumentation Frameworks, AAFs）的计算工具，将辩证分析中的论证和攻击关系形式化为数学结构，通过四种标准语义（admissible/complete/preferred/stable）判定论证的可接受性。与第9节的概述不同，本节提供完整的执行步骤和判定算法。

**AAFs 形式化定义**：
```
AAF = ⟨Args, Att⟩
其中:
  Args = {A1, A2, ..., An}  — 论证集合（有限集）
  Att ⊆ Args × Args         — 攻击关系（二元关系）
  (Ai, Aj) ∈ Att 表示 Ai 攻击 Aj
```

### 14.2 四种语义判定步骤

**步骤1：admissible（可容许）语义判定**

```
判定算法:
1. 构造攻击图：对每个论证Ai，列出所有攻击Ai的论证集合 Att^{-1}(Ai)
2. 检查无冲突：候选集合S中不存在 (Ai, Aj) ∈ Att
3. 检查防御性：对S中每个Ai，若存在Aj攻击Ai（(Aj, Ai) ∈ Att），
   则S中必须存在Ak攻击Aj（(Ak, Aj) ∈ Att）
4. 若2和3均满足 → S是admissible外延

判定规则:
- 空集 ∅ 总是admissible的（无冲突且无需防御）
- 单元素集 {Ai} admissible ⟺ Ai无攻击者，或Ai的每个攻击者都被S中某元素攻击
```

**步骤2：complete（完备）语义判定**

```
判定算法:
1. 从admissible外延出发
2. 对每个admissible外延S，检查：是否存在论证Ai ∉ S，
   使得S防御Ai（即Ai的所有攻击者都被S中元素攻击）
3. 若不存在这样的Ai → S是complete外延
4. 若存在 → 将Ai加入S，重新检查

判定规则:
- complete外延 = 最大的"只包含被自身防御的论证"的admissible集
- 每个complete外延都是admissible的，但反之不然
```

**步骤3：preferred（优先）语义判定**

```
判定算法:
1. 枚举所有complete外延
2. 按集合包含关系排序
3. 选择最大的complete外延（不存在真包含它的complete外延）
4. 这些最大complete外延即为preferred外延

判定规则:
- preferred外延 ⊆ complete外延 ⊆ admissible外延
- 至少存在一个preferred外延（保证性定理）
- preferred外延可能不唯一
```

**步骤4：stable（稳定）语义判定**

```
判定算法:
1. 对候选集合S，检查无冲突：S中不存在 (Ai, Aj) ∈ Att
2. 检查攻击外部：对每个Aj ∉ S，存在Ai ∈ S使得 (Ai, Aj) ∈ Att
3. 若1和2均满足 → S是stable外延

判定规则:
- stable外延攻击所有不在集合中的论证
- 每个stable外延都是preferred的，但反之不然
- stable外延可能不存在（当论证框架有自攻击或奇数循环时）
```

### 14.3 四种语义的关系与判定优先级

```
语义包含关系:
stable ⊆ preferred ⊆ complete ⊆ admissible

判定优先级:
1. 先判定stable（最强语义，结论最确定）
2. stable不存在时，判定preferred（次强语义）
3. 需要完整分析时，判定complete（包含所有可防御论证）
4. 需要最宽松接受时，判定admissible（最小约束）

一致性检验:
- 若四种语义下结论一致 → 高置信度（标注"四语义一致"）
- 若stable不存在但preferred存在 → 中等置信度（标注"无stable外延"）
- 若preferred不唯一 → 低置信度（标注"多preferred外延，需聚焦机制"）
```

### 14.4 pygarg 与 profound-cognition Layer 对照映射

| pygarg步骤 | 对应Layer | 映射说明 |
|-----------|----------|---------|
| AAF构建 | Layer2 分解 | 将论证分解为形式化结构 |
| admissible判定 | Layer4 推理 | 基本逻辑推理判定 |
| complete判定 | Layer6 因果 | 完整因果链防御检查 |
| preferred判定 | Layer7 综合 | 选择最优综合方案 |
| stable判定 | Layer8 决策 | 最终决策级判定 |
| 一致性检验 | Layer5 反事实 | 反事实检验语义一致性 |

### 14.5 pygarg 穷尽重试策略

```yaml
pygarg_exhaust_retry:
  L1_FULL:
    condition: "pygarg可用，AAF可构建，四种语义均可判定"
    action: "完整4步语义判定+一致性检验"
    confidence: "HIGH"

  L2_PREFERRED_ONLY:
    condition: "stable外延不存在（自攻击或奇数循环）"
    action: "使用preferred语义作为最强判定，标注'无stable外延'"
    confidence: "MEDIUM"
    output_annotation: "pygarg穷尽重试替代：无stable外延，使用preferred语义"

  L3_MANUAL_AAF:
    condition: "pygarg不可用，但论证结构可手动形式化"
    action: "手动构建AAF并执行admissible/complete判定"
    confidence: "LOW-MEDIUM"
    output_annotation: "pygarg穷尽重试替代：手动AAFs形式化验证"

  L4_NATURAL_DIALECTIC:
    condition: "AAFs形式化不可行（论证过于模糊或非结构化）"
    action: "使用自然语言辩证分析，标注'无形式化验证'"
    confidence: "LOW"
    output_annotation: "pygarg完全穷尽重试：使用自然语言辩证分析"
```

> 知识来源: TC-085 [pygarg]

---

### [pygarg] 源码逻辑引入

#### 核心算法逻辑

**1. AAFs 四种语义判定算法源码级伪代码**

```
抽象论证框架（AAF）核心结构:

AAF = (Args, Attacks)
  Args: set[Argument]         # 论证集合
  Attacks: set[(Arg, Arg)]    # 攻击关系集合 (a, b) = a攻击b

# 基本判定函数
function is_acceptable(arg, S, Attacks):
    # arg在集合S中是可接受的 ⟺ S防御arg的所有攻击者
    for attacker in {a | (a, arg) ∈ Attacks}:
        # 检查S中是否有成员反击attacker
        if not any((s, attacker) ∈ Attacks for s in S):
            return False  # 存在未被反击的攻击者
    return True

# 语义1：admissible（可容纳）语义
function compute_admissible(AAF):
    # S是admissible ⟺ S是冲突自由的且S中每个论证都是可接受的
    admissible_extensions = []

    for S in subsets(AAF.Args):
        # 条件1：冲突自由——S中无互相攻击
        conflict_free = not any((a, b) in AAF.Attacks
                                for a in S for b in S)
        if not conflict_free:
            continue

        # 条件2：每个成员可接受
        all_acceptable = all(is_acceptable(arg, S, AAF.Attacks)
                             for arg in S)
        if all_acceptable:
            admissible_extensions.append(S)

    return admissible_extensions

# 语义2：complete（完备）语义
function compute_complete(AAF):
    # S是complete ⟺ S是admissible且S包含所有对S可接受的论证
    admissible = compute_admissible(AAF)
    complete_extensions = []

    for S in admissible:
        # 找出所有对S可接受的论证
        all_acceptable_to_S = {arg for arg in AAF.Args
                               if is_acceptable(arg, S, AAF.Attacks)}
        # S必须恰好等于所有对S可接受的论证集合
        if set(S) == all_acceptable_to_S:
            complete_extensions.append(S)

    return complete_extensions

# 语义3：preferred（优先）语义
function compute_preferred(AAF):
    # S是preferred ⟺ S是极大admissible扩展（集合包含意义下的极大）
    admissible = compute_admissible(AAF)
    preferred_extensions = []

    # 按集合大小降序排列
    sorted_adm = sorted(admissible, key=lambda s: -len(s))

    for S in sorted_adm:
        # 检查S是否被任何已选preferred扩展真包含
        is_maximal = not any(set(S) < set(P)
                             for P in preferred_extensions)
        if is_maximal:
            preferred_extensions.append(S)

    return preferred_extensions
    # 性质：每个AAF至少有一个preferred扩展（即使为空集）

# 语义4：stable（稳定）语义
function compute_stable(AAF):
    # S是stable ⟺ S是冲突自由的且S攻击所有不在S中的论证
    stable_extensions = []

    for S in subsets(AAF.Args):
        # 条件1：冲突自由
        conflict_free = not any((a, b) in AAF.Attacks
                                for a in S for b in S)
        if not conflict_free:
            continue

        # 条件2：攻击所有非成员
        attacks_all_outside = all(
            any((s, arg) in AAF.Attacks for s in S)
            for arg in AAF.Args if arg not in S
        )
        if attacks_all_outside:
            stable_extensions.append(S)

    return stable_extensions
    # 注意：stable扩展可能不存在（自攻击或奇数循环时）
```

**2. 语义间关系判定源码逻辑**

```
四种语义的包含关系:

stable ⊆ preferred ⊆ complete ⊆ admissible

function verify_semantic_relations(AAF):
    stable = compute_stable(AAF)
    preferred = compute_preferred(AAF)
    complete = compute_complete(AAF)
    admissible = compute_admissible(AAF)

    # 验证包含关系
    assert set(stable) ⊆ set(preferred)
    assert set(preferred) ⊆ set(complete)
    assert set(complete) ⊆ set(admissible)

    # 判定逻辑:
    # 如果stable非空 → 使用stable（最强语义）
    # 如果stable为空但preferred非空 → 使用preferred
    # 如果preferred仅为空集 → 标注"论证框架无可信扩展"

    return {
        stable, preferred, complete, admissible,
        strongest_semantic: select_strongest(stable, preferred, complete)
    }

function select_strongest(stable, preferred, complete):
    if len(stable) > 0:
        return ("stable", stable)
    elif len(preferred) > 0 and preferred != [set()]:
        return ("preferred", preferred)
    elif len(complete) > 0 and complete != [set()]:
        return ("complete", complete)
    else:
        return ("none", [])  # 无可信扩展
```

**3. 论证状态标注源码逻辑**

```
论证状态判定:

function label_arguments(AAF, extensions):
    # 基于扩展集合标注每个论证的状态
    labels = {}

    for arg in AAF.Args:
        in_some_extension = any(arg in ext for ext in extensions)
        in_all_extensions = all(arg in ext for ext in extensions)
        out_all_extensions = not any(arg in ext for ext in extensions)

        if in_all_extensions:
            labels[arg] = "SKEPTICALLY_ACCEPTED"  # 怀疑地接受
        elif in_some_extension:
            labels[arg] = "CREDULOUSLY_ACCEPTED"  # 轻信地接受
        else:
            labels[arg] = "REJECTED"              # 被拒绝

    return labels

# 辩证分析应用:
# SKEPTICALLY_ACCEPTED → 高置信度论证（所有扩展都接受）
# CREDULOUSLY_ACCEPTED → 有条件接受（部分扩展接受）
# REJECTED → 不可信论证（无扩展接受）
```

#### 数据结构设计

```
核心数据结构:

1. AAF: 抽象论证框架
   - Args: set[Argument]          # 论证集合
   - Attacks: set[tuple(Arg, Arg)] # 攻击关系

2. Argument: 论证节点
   - id: str                      # 唯一标识
   - content: str                 # 论证内容
   - source: str                  # 来源标注

3. Extension: 语义扩展
   - arguments: set[Argument]     # 扩展中的论证集合
   - semantic_type: "admissible"|"complete"|"preferred"|"stable"
   - label: Dict[Arg, "SKEPTICALLY_ACCEPTED"|"CREDULOUSLY_ACCEPTED"|"REJECTED"]
```

#### 决策流程

```
pygarg AAFs 辩证分析决策流程:

1. 论证提取 → 从分析内容中提取论证和攻击关系
2. AAF构建 → 构建AAF=(Args, Attacks)
3. 四种语义计算 → 依次计算admissible→complete→preferred→stable
4. 最强语义选择 → select_strongest()
   ├─ stable非空 → 使用stable（最强）
   ├─ stable为空 → 使用preferred
   └─ preferred仅为空集 → 标注"无可信扩展"
5. 论证标注 → label_arguments() 标注各论证状态
6. 输出辩证结论 → 基于最强语义和论证标注
```

#### 穷尽重试策略

```yaml
pygarg_source_exhaust_retry:
  L1_FULL_SEMANTICS:
    condition: "pygarg可用，四种语义均可判定"
    action: "完整4步语义判定+一致性检验+论证标注"
    confidence: "HIGH"

  L2_PREFERRED_ONLY:
    condition: "stable外延不存在（自攻击或奇数循环）"
    action: "使用preferred语义作为最强判定，标注'无stable外延'"
    confidence: "MEDIUM"
    output_annotation: "pygarg穷尽重试替代：无stable外延，使用preferred语义"

  L3_MANUAL_AAF:
    condition: "pygarg不可用，但论证结构可手动形式化"
    action: "手动构建AAF并执行admissible/complete判定"
    confidence: "LOW-MEDIUM"
    output_annotation: "pygarg穷尽重试替代：手动AAFs形式化验证"

  L4_NATURAL_DIALECTIC:
    condition: "AAFs形式化不可行"
    action: "使用自然语言辩证分析，标注'无形式化验证'"
    confidence: "LOW"
    output_annotation: "pygarg完全穷尽重试：使用自然语言辩证分析"
```

© 阿洋