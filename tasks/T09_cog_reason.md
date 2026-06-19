<!-- 作者：阿洋 -->

# T09 — 多路径推理

## role

你是认知流水线第二步：多路径推理者。你开启 8 条独立推理路径（A/B/C/D/E/F/G/H，含 NS-Engine 路径 H），以 Multi-Path Exploration with Branch Pruning（MPEP）驱动路径选择与探索，每条路径使用不同的分析维度视角，并对各路径结论进行对比。

---

## 路径配置

推理路径固定配置如下（EXHAUST-only，全局不可变）：

```yaml
path_config:
  paths: 8
  min_steps: 7
  tok_budget: 8000
  layers_used: ["structural", "stakeholder", "temporal", "causal", "counterfactual", "systemic", "normative", "neurosymbolic"]
```

- `paths`: 并行推理路径数量（8 条，含新增 NS-Engine 神经符号推理路径）
- `min_steps`: 每条路径推理链的最低步数（7 步，与 SKILL.md 执行参数一致）
- `tok_budget`: 推理输出的 token 预算上限（NS-Engine 路径额外 2000 预算用于 Datalog 规则展开）
- `layers_used`: 可用的分析维度列表，每条推理路径选取唯一的 analysis_layer

### NS-Engine 推理路径（第 8 路径：neurosymbolic）

> **能力卡**: MC-183 Scallop

第 8 条路径（路径 H）采用神经符号推理范式（Neuro-Symbolic Reasoning），在 Pyro（纯概率推理）和 OpenNARS（非公理推理）之间建立第三种推理范式：

```yaml
ns_engine_path:
  path_id: "路径H"
  analysis_layer: "neurosymbolic"
  paradigm: "Datalog规则 + 神经网络概率输出"
  workflow:
    - step: "将核心问题转化为 Datalog 规则集合（事实 + 推理规则）"
    - step: "为每条规则附加神经网络输出的概率权重（Scallop 概率化 Datalog）"
    - step: "执行前向链推理（Forward Chaining），生成所有可推导结论"
    - step: "反向传播概率，计算每条结论的边际概率分布"
    - step: "提取高置信度结论（P > 0.8）及对应的规则支持链"
  output:
    high_confidence_conclusions: ["概率 > 0.8 的结论"]
    rule_support_chains: ["每条结论的规则推导链"]
    contrasting_paths: ["与路径 A-G 的结论对比：共性/差异/互补"]
```

#### Scallop Datalog 规则编写规范

Datalog 规则格式遵循 Scallop 概率化扩展语法：

```yaml
datalog_rule_spec:
  fact_format:
    syntax: "relation_name(arg1, arg2, ...) :: probability"
    example: "causes(inflation, price_rise) :: 0.85"
    constraints:
      - "概率值 ∈ [0.0, 1.0]"
      - "参数必须是原子值（字符串/数字/枚举）"
      - "关系名必须为 snake_case"

  rule_format:
    syntax: "conclusion(args) :- premise1(args), premise2(args), ..."
    example: "leads_to(X, Z) :- causes(X, Y), leads_to(Y, Z)"
    constraints:
      - "每条规则最多 5 个前提（premise）"
      - "变量名必须大写开头，常量小写"
      - "禁止否定即失败（negation as failure），使用概率 < 0.3 替代"
      - "递归深度不超过 3 层"

  probability_propagation:
    - "合取（AND）: P(A ∧ B) = P(A) × P(B)（独立假设）"
    - "析取（OR）: P(A ∨ B) = P(A) + P(B) - P(A) × P(B)"
    - "条件: P(A|B) 通过 Scallop 编译器自动推导"

  rule_quality_checklist:
    - "规则是否覆盖了核心问题的所有关键变量？"
    - "概率赋值是否有依据（文献/数据/专家判断）？"
    - "是否存在循环依赖？"
    - "递归规则是否有明确的终止条件？"
```

#### Scallop 输出 yaml 规范

```yaml
scallop_ns_engine_output:
  rule_set:
    - rule_id: "R-001"
      type: "fact|rule"
      statement: "Datalog 规则文本"
      probability: 0.0-1.0
      source: "literature|data|expert|inferred"
  forward_chaining_results:
    - conclusion: "推导出的结论"
      probability: 0.0-1.0
      supporting_rules: ["R-001", "R-003"]
      derivation_depth: int
  high_confidence_conclusions:
    - conclusion: "概率 > 0.8 的结论"
      probability: 0.0-1.0
      rule_chain: ["完整规则推导链"]
  marginal_probabilities:
    - variable: "变量名"
      distribution: {P_true: 0.0-1.0, P_false: 0.0-1.0}
  path_contrast:
    consensus_with_other_paths: ["与路径A-G的共识"]
    unique_insights: ["路径H独有的结论"]
    conflicts_with_other_paths: ["与其他路径的分歧"]
```

#### Scallop 穷尽重试策略

```yaml
scallop_retrying:
  RETRYING_SCALLOP:
    trigger: "Scallop 运行时不可用或 Datalog 规则编译失败"
    exhaust-retry: "使用纯 Prolog 风格逻辑推理（无概率），规则概率权重改为确定性布尔标记"
    output_annotation: "NS-Engine穷尽重试：Scallop不可用，使用确定性逻辑推理替代概率化Datalog"
    confidence_adjustment: "所有结论置信度上限降为 MEDIUM"

  RETRYING_RULE_ENCODING:
    trigger: "核心问题无法有效编码为 Datalog 规则（问题过于模糊或非结构化）"
    exhaust-retry: "将问题拆解为可编码子集 + 不可编码残余，子集走 Scallop，残余走纯文本推理"
    output_annotation: "NS-Engine部分穷尽重试：问题部分可编码，残余走文本推理"

  RETRYING_PROBABILITY:
    trigger: "概率传播计算失败（规则间依赖过于复杂）"
    exhaust-retry: "使用独立概率假设（忽略规则间依赖），每条结论概率单独计算"
    output_annotation: "NS-Engine概率穷尽重试：使用独立概率假设，忽略规则间依赖"

  FULL_EXHAUST_RETRY:
    trigger: "神经符号推理完全不可用（Scallop + Prolog 均失败）"
    exhaust-retry: "路径H穷尽重试为纯文本逻辑推理，使用三段论+假言推理，无概率量化"
    output_annotation: "NS-Engine穷尽重试保底：路径H使用纯文本逻辑推理，无概率量化"
    confidence_adjustment: "路径H overall_confidence 上限为 0.6"
```

> 知识来源: MC-183 [Scallop]

#### Scallop 神经符号推理三范式选择决策树

> **能力卡**: MC-183 [Scallop]

Scallop 提供三种神经符号推理范式，不同范式适用于不同类型的推理任务。以下决策树用于在 T09 路径 H 中选择最优范式：

**三范式定义**：

| 范式 | 名称 | 核心机制 | 适用场景 |
|------|------|---------|---------|
| 范式1 | **概率化Datalog推理** | Datalog规则 + 神经网络概率输出 + 前向链推理 | 规则可显式编码、推理链可枚举 |
| 范式2 | **可微Datalog推理** | Datalog规则嵌入可微计算图，端到端训练 | 需要从数据中学习规则权重 |
| 范式3 | **神经关系推理** | 神经网络学习关系表示 + Datalog约束推理 | 关系结构复杂、规则难以手工编码 |

**三范式选择决策树**：

```
问题输入
  │
  ├─ Q1: 核心问题能否用明确的逻辑规则（IF-THEN）表述？
  │   ├─ YES → Q2
  │   └─ NO → 范式3（神经关系推理）
  │            理由：规则不可显式编码时，需神经网络学习关系表示
  │
  ├─ Q2: 规则中的概率/权重是否已知（来自文献/数据/专家）？
  │   ├─ YES → 范式1（概率化Datalog推理）
  │   │         理由：规则和概率均已知，直接前向链推理
  │   └─ NO → Q3
  │
  ├─ Q3: 是否有标注数据可用于学习规则权重？
  │   ├─ YES → 范式2（可微Datalog推理）
  │   │         理由：规则结构已知但权重未知，端到端训练学习权重
  │   └─ NO → 范式1（概率化Datalog推理）
  │            理由：无标注数据时，使用均匀先验概率+前向链推理
  │            穷尽重试标注：概率赋值基于启发式判断，confidence上限MEDIUM
  │
  └─ 特殊情况处理：
      ├─ 规则可编码但存在递归（深度>3）→ 范式1 + 递归深度限制3层
      ├─ 规则可编码但规则数>50 → 范式1 + 分块推理（按功能组拆分）
      └─ 关系结构复杂且有标注数据 → 范式2+3混合（先用范式3学习关系，再用范式2精调权重）
```

**范式选择与 profound-cognition Layer 对照映射**：

| 范式选择步骤 | 对应Layer | 映射说明 |
|------------|----------|---------|
| Q1 规则可编码性判定 | Layer2 分解 | 分解问题判断逻辑结构 |
| Q2 概率已知性判定 | Layer3 证据 | 证据是否提供概率信息 |
| Q3 标注数据可用性 | Layer3 证据 | 证据是否包含标注数据 |
| 范式1 前向链推理 | Layer4 推理 | 确定性规则驱动的推理 |
| 范式2 可微训练 | Layer4 推理+Layer6 因果 | 数据驱动的权重学习+因果约束 |
| 范式3 关系学习 | Layer1 感知+Layer4 推理 | 从原始信号学习关系+推理 |

**范式选择穷尽重试策略**：

```yaml
paradigm_selection_retrying:
  L1_FULL:
    condition: "三范式均可选，决策树正常执行"
    action: "按决策树选择最优范式"
    confidence: "HIGH"

  L2_ALTERNATIVE_PARADIGM:
    condition: "最优范式不可用（如范式2需要梯度计算但环境不支持）"
    action: "穷尽重试到次优范式（范式2→范式1，范式3→范式1）"
    confidence: "MEDIUM"
    output_annotation: "Scallop范式穷尽重试：使用次优范式替代"

  L3_RULE_ONLY:
    condition: "仅范式1可用（无神经网络支持）"
    action: "使用纯Datalog推理（无概率），规则权重改为确定性布尔标记"
    confidence: "LOW-MEDIUM"
    output_annotation: "Scallop穷尽重试：仅使用确定性Datalog推理"

  L4_TEXT_REASONING:
    condition: "Scallop完全不可用"
    action: "路径H穷尽重试为纯文本逻辑推理，使用三段论+假言推理"
    confidence: "LOW"
    output_annotation: "Scallop穷尽重试保底：路径H使用纯文本逻辑推理"
```

---

## MPEP 路径选择与探索机制

T09 采用 Multi-Path Exploration with Branch Pruning（MPEP）驱动 7 条推理路径的选择与探索，四阶段循环如下：

```yaml
mpep_config:
  selection: "UCB1 上置信界选择——计算每条路径 UCB = avg_confidence + c * sqrt(ln(N) / n)，选择 UCB 最高的节点优先展开推理链"
  expansion: "从选中节点展开新的推理步骤，每条路径最终生成完整推理链（≥ min_steps 步）"
  simulation: "对每条路径进行轻量 rollout（深度 3 步），使用启发式规则估算路径终端置信度"
  backpropagation: "将 simulation 结果反向传播，更新各步骤 confidence，累积全局路径统计以驱动下轮 selection"
  c_exploration: 1.414
  rollout_depth: 3
```

> **实现说明**：以下 MPEP 流程为单次上下文内的启发式模拟，而非多次独立采样后再行汇总的真正树搜索。其核心价值在于强制 LLM 按树搜索的决策逻辑组织推理过程（方向展开 → 多维评估 → 最优选择 → 回溯剪枝），即使未执行并行子树独立采样，这一结构化的推理组织方式本身也能显著提升推理质量和结论的可追溯性。

### MPEP 四阶段详解

| 阶段 | 操作 | 输出 |
|------|------|------|
| **Selection** | 在 8 个 analysis_layer 中，基于 UCB1 公式计算各层探索价值，优先选择高潜力低访问次数的层 | 选中展开的 path_id |
| **Expansion** | 对选中层展开完整推理链（≥7 步），每步生成 conclusion + confidence，层间独立不交叉 | reasoning_chain |
| **Simulation** | 以轻量 rollout（3 步）快速评估路径潜在结论质量，估算 terminal confidence | 模拟置信度 |
| **Backpropagation** | 将模拟结果沿路径回溯至根节点，更新各步骤 confidence，为 selection 积累统计信息 | 修正后置信度分布 |

### MPEP 与路径配置的关系

- 8 个 analysis_layer 构成 MPEP 根节点的 8 个可扩展分支
- 每条路径的 overall_confidence 经 backpropagation 修正后，作为 selection 阶段的 UCB 输入
- `c_exploration = 1.414` 平衡探索（exploration）与利用（exploitation），确保低置信度但高潜力的路径不被过早剪枝
- rollout 阶段的模拟不替代完整推理链，仅用于辅助路径排序与资源分配

### AGoT 推理路径图结构化

- 推理路径组织遵循 AGoT（Adaptive Graph of Thought）图结构化范式
- 推理路径以有向无环图（DAG）组织，节点为推理步骤，边为逻辑依赖
- 安全限制：最大分支数 5、最大深度 3、预算追踪 20 单位
- 超限穷尽重试：穷尽尝试 LLM 原生推理（CoT/ToT）
- MPEP（Multi-Path Exploration with Branch Pruning）为 AGoT 的具体实现策略
- 详细定义见 knowledge/external-capabilities/MC-033-AGoT.md

#### AGoT 方法论原理

AGoT 将推理过程建模为动态有向无环图（DAG），核心思想是：推理不是线性的，而是图结构的——推理步骤之间存在分支、合并和依赖关系。AGoT 通过预算控制机制防止推理爆炸，同时保持推理路径的多样性和完整性。

**核心机制**：
1. **节点生成**：每个推理步骤生成一个节点，节点包含推理内容、置信度和资源消耗
2. **边构建**：节点间的逻辑依赖关系形成有向边，支持分支（一对多）和合并（多对一）
3. **预算追踪**：每个节点消耗预算单位，总预算不超过上限（默认20）
4. **深度控制**：推理深度由质量驱动，不设上限，持续深化直至推理充分
5. **分支控制**：分支数由质量驱动，不设上限，防止遗漏关键推理路径

#### AGoT 决策规则（if-then 表格）

| 条件 (if) | 动作 (then) | 理由 |
|-----------|------------|------|
| 当前分支数 < max_branches 且预算剩余 > 5 | 允许新分支展开 | 资源充足，可探索新方向 |
| 当前分支数 ≥ max_branches | 禁止新分支，对已有分支执行剪枝 | 防止组合爆炸 |
| 当前深度 ≥ max_depth | 停止向下展开，输出当前路径结论 | 防止无限递归 |
| 预算剩余 ≤ 5 | 仅保留 top-2 置信度路径，其余剪枝 | 资源紧张，聚焦最优路径 |
| 节点置信度 < 0.3 且无新证据支持 | 标记为 dead_end，回溯到父节点 | 低置信度路径不值得继续 |
| 两条路径结论一致且推理链重叠 > 70% | 合并为一条路径，预算释放 | 消除冗余 |
| 预算耗尽 | 立即终止所有展开，输出已有结论 | 硬性约束 |
| 所有路径置信度 > 0.8 | 提前终止，进入综合阶段 | 已达高质量收敛 |

#### AGoT 输出 yaml 规范

```yaml
agot_graph:
  metadata:
    total_nodes: int
    total_edges: int
    budget_used: int
    budget_remaining: int
    max_depth_reached: int
    branches_created: int
    branches_pruned: int
  nodes:
    - node_id: "N-001"
      depth: 0
      content: "推理步骤内容"
      confidence: 0.0-1.0
      budget_consumed: int
      status: "expanded|dead_end|selected|pruned"
      parent: null
      children: ["N-002", "N-003"]
  edges:
    - from: "N-001"
      to: "N-002"
      relation: "logical_dependency|branch|merge"
      strength: 0.0-1.0
  selected_paths:
    - path: ["N-001", "N-002", "N-005"]
      overall_confidence: 0.0-1.0
      conclusion: "路径最终结论"
  pruned_report:
    - node_id: "N-003"
      reason: "低置信度/预算不足/冗余合并"
      original_confidence: 0.0-1.0
```

#### AGoT 穷尽重试策略

```yaml
agot_retrying:
  RETRYING_BRANCH_LIMIT:
    trigger: "分支数达到上限(max_branches=5)但仍有高潜力方向未探索"
    exhaust-retry: "记录未探索方向到 deferred_branches 字段，后续迭代中优先展开"
    output_annotation: "AGoT分支受限：部分高潜力方向延迟探索"

  RETRYING_BUDGET:
    trigger: "预算耗尽(budget=0)但推理未收敛"
    exhaust-retry: "输出当前最高置信度路径作为临时结论，标注 confidence_upper_bound 为估计值"
    output_annotation: "AGoT预算受限：结论置信度为下界估计"

  RETRYING_DEPTH:
    trigger: "达到最大深度(max_depth=3)但关键问题未完全解答"
    exhaust-retry: "将未解答的子问题标记为 deferred_questions，建议后续独立推理"
    output_annotation: "AGoT深度受限：部分子问题延迟处理"

  FULL_EXHAUST_RETRY:
    trigger: "AGoT图结构服务完全不可用"
    exhaust-retry: "穷尽尝试 LLM 原生推理（Chain-of-Thought / Tree-of-Thought），8条路径按线性序列独立执行"
    output_annotation: "AGoT穷尽重试保底：使用LLM原生推理替代图结构推理"
```

> 知识来源: MC-033 [AGoT]

---

## context

- **problem**: 用户提出的原始问题
- **T08_summary**: 上一步子问题分解与假设挖掘的输出摘要
- **mother_hypotheses**: T00 产出的母假设候选列表，参考 NRSF §T00_* 中高相关母假设，将其作为推理路径的潜在方向
- **discovery_log_full**: discovery_log 完整内容（不压缩，直通传递），无数据时为空数组 `[]`
- **critical_findings_refs**: 跨节点直通的关键发现 §ref 索引（`cross_reference_potential = HIGH` 的发现，上限 10 条）
- **layer_specific_data**: 每条路径对应的分析层完整原始数据，无数据时为空对象 `{}`
  - **structural**: T03 `variable_list` 完整字段（变量名 + 交互关系 + 阈值效应）
  - **stakeholder**: T05 `L7_stakeholder_map` 完整字段（利益相关方角色 + 权力 + 利益 + 立场）
  - **temporal**: T02 `L2_timeline_table` 完整字段（关键时间节点 + 趋势转折 + 速率变化）
  - **causal**: T06 `causal_chain_graph` 完整字段（因果链节点 + 方向 + 强度 + 反馈回路）
  - **counterfactual**: T04 `counterfactual_branches` 完整字段（反事实假设 + 分支条件 + 预期结果差异）
  - **systemic**: T01 `system_boundary_emergence` 完整字段（系统边界定义 + 子系统互动 + 涌现属性）
  - **normative**: T07 `value_framework` 完整字段（价值判断维度 + 伦理约束 + 规范性优先级）
  - **neurosymbolic**: 通过 Scallop 概率化 Datalog 规则引擎处理核心命题，NS-Engine 路径专用，无需上游直通数据

---

## 变量分类驱动的资源分配（递归剪枝规则）

T08 将变量分为五类（root_variable / explanatory_variable / auxiliary_variable / counter_variable / noise_variable），T09 在构建推理路径时 SHALL 按以下规则分配资源：

```yaml
variable_driven_allocation:
  root_variable:
    action: "分配最多推理路径资源"
    path_allocation: "至少 2 条独立推理路径（不同 analysis_layer 视角）"
    token_multiplier: 2.0
    reasoning_depth: "deep"

  explanatory_variable:
    action: "分配标准推理路径"
    path_allocation: "1 条推理路径"
    token_multiplier: 1.0
    reasoning_depth: "standard"

  auxiliary_variable:
    action: "分配聚焦推理路径"
    path_allocation: "1 条聚焦路径（min_steps 按辅助变量相关性调整）"
    token_multiplier: 0.5
    reasoning_depth: "focused"

  counter_variable:
    action: "分配对抗推理路径"
    path_allocation: "1 条对抗路径（从反面视角推理）"
    token_multiplier: 1.2
    reasoning_depth: "adversarial"

  noise_variable:
    action: "直接剪枝，不分配任何推理路径"
    path_allocation: 0
    token_multiplier: 0
    reasoning_depth: "eliminated"
```

**剪枝执行规则**：
1. T09 在执行推理前，先读取 T08 的 `variable_classification[].var_type`
2. `noise_variable` 类型的变量直接从推理范围中移除（不产生推理路径，不在 consensus_divergence_matrix 中出现）
3. `root_variable` 获得 2.0 倍 token 预算，`auxiliary_variable` 获得 0.5 倍
4. 剪枝后的总路径数仍必须满足 `path_config.paths`（8 条）的要求——若 noise 剪枝导致路径不足，从 root/explanatory 中追加路径补足
5. 在 output_schema 中新增 `pruning_report` 字段记录剪枝决策

---

## output_schema

```yaml
reasoning_paths:
  - path_id: "路径A"    # 路径A/B/C/D/E/F/G/H，共8条
    analysis_layer: "structural | stakeholder | temporal | causal | counterfactual | systemic | normative | neurosymbolic"
    meta_assumption: "该路径的核心预设（区别于其他路径的根本前提）"
    reasoning_chain:
      - step: "推理步骤描述"
        conclusion: "该步结论"
        confidence: 0.0-1.0
    key_insights:
      - "该路径独有的关键洞察"
    overall_confidence: 0.0-1.0

consensus_divergence_matrix:
  consensus_points:
    - "所有路径共同认可的结论"
  divergence_points:
    - point: "分歧主题"
      path_views:
        - path_id: "路径A"
          view: "路径A的观点"
        - path_id: "路径B"
          view: "路径B的观点"
        - path_id: "路径C"
          view: "路径C的观点"
        - path_id: "路径D"
          view: "路径D的观点"
        - path_id: "路径E"
          view: "路径E的观点"
        - path_id: "路径F"
          view: "路径F的观点"
        - path_id: "路径G"
          view: "路径G的观点"
      analysis: "分歧原因分析与评估"

recommended_path:
  path_id: "推荐路径标识"
  rationale: "推荐理由"

mpep_trace:
  root_nodes:
    - node_id: "root_1"
      direction: "推理方向描述"
      children:
        - node_id: "root_1_child_1"
          evaluation: {novelty: 0.0-1.0, logical_strength: 0.0-1.0, evidence_feasibility: 0.0-1.0}
          status: "expanded | dead_end | selected"
          children: []
  search_summary:
    total_nodes_visited: N
    dead_ends_encountered: N
    selected_final_path: "node_id"

pruning_report:
  noise_variables_eliminated: ["被剪枝的noise变量列表"]
  root_variables_expanded: ["获得额外路径的root变量列表"]
  paths_redistributed: integer

causal_graph_for_dynamics:
  variables:
    - name: "变量名称"
      type: "stock|flow|exogenous|parameter"
      definition: "变量定义描述"
  edges:
    - from: "源变量"
      to: "目标变量"
      strength: 0.0-1.0
      direction: "+|-"
  confidence: "HIGH|MEDIUM|LOW"
  data_source: "empirical|pseudo_dataset|literature_based"
```

### 推理路径设计要求

| 要求 | 说明 |
|------|------|
| 路径独立性 | 每条路径须有不同的meta_assumption和analysis_layer，由此产生实质性推理分化 |
| 推理链完整性 | 每条路径至少 7 步推理（由 path_config.min_steps 指定），每步有明确的conclusion与confidence |
| 置信度量化 | overall_confidence为0-1浮点数，不可全为相同值 |
| 分歧必要性 | divergence_points至少1项，不可所有路径完全一致 |

new_discoveries:
  - finding: "推理阶段发现的意外洞察或高价值跨层发现（≤50字）"
    discovered_at: "T09"
    cross_reference_potential: "HIGH|MEDIUM|LOW"
    category: "reasoning"

---

## 自一致性独立性约束

每条推理路径 SHALL 独立执行，遵守以下规则：

1. **禁止交叉参照**：在生成路径 N 时，禁止参考已生成的路径 1...(N-1) 的结论、中间步骤或推理方向
2. **独立上下文**：每条路径仅使用 T08 解构结果 + 原始问题作为输入，不接收其他路径的中间产物
3. **交叉仅限 T13**：路径间的对比、交叉验证和综合仅在 T13（认知综合）阶段进行
4. **违规标记**：若任一路径中发现引用其他路径的迹象（如"如路径A所述"），该路径标记为 INVALID 并重新生成

---

## self_check_before_output

### M10 逼退函数（L4 毕业条件）
> **铁律**：逼退函数是毕业条件，未通过则不得进入下一层 T13。
> - [ ] **M3 递归分支剪枝**：是否已执行变量分类（主根/强解释/辅助/反证/噪声）？主根变量 ≤ 1？
> - [ ] **M9 主线竞争择优**：是否已执行五维加权评分？主线得分 ≥ 60 分？主线与第二名分差 ≥ 5 分？

在输出前，逐项自检以下清单：

- [ ] 推理路径数是否为 8 条（A/B/C/D/E/F/G/H），与 path_config.paths 一致？
- [ ] 每条路径是否都有独特的meta_assumption（核心预设），且与其他路径的前提存在实质性差异？
- [ ] 每条路径的reasoning_chain是否至少 7 步，每步有conclusion和confidence？
- [ ] 所有路径的结论是否存在实质性差异（而非表面措辞不同）？
- [ ] consensus_divergence_matrix是否真实反映了路径间的共识与分歧？
- [ ] recommended_path是否基于矩阵分析给出了有说服力的理由？
- [ ] 每条路径 reasoning_chain 步数 ≥ path_config.min_steps（7 步）？
- [ ] divergence_points ≥ 1？
- [ ] 各路径是否严格遵守独立性约束（无跨路径引用）？
- [ ] 【深度保底】所有路径是否满足最低质量门槛？
- [ ] new_discoveries 是否至少包含1条 cross_reference_potential == HIGH 的发现？
- [ ] new_discoveries 中的发现是否标注了正确的 category（T09 推理层发现使用 "reasoning"）？
- [ ] 每条路径的 analysis_layer 是否从 path_config.layers_used 中选取且无重复？
- [ ] pruning_report.paths_redistributed 是否满足 path_config.paths（8 条）要求？noise_variables_eliminated 是否与 variable_classification 中的 noise_variable 列表一致？
- [ ] gCastle 数据管线中间步骤是否已执行（如适用）
- [ ] 算法适用性标注是否与实际数据类型匹配
- [ ] causal_graph_for_dynamics 字段是否完整（供 T22 消费）
- [ ] 伪数据集方法是否已标注 "定性参考" 警告
- [ ] 至少 3 种算法交叉验证是否通过

---

## MPEP 推理流程

T09 采用 MPEP（Multi-Path Exploration with Branch Pruning）驱动路径选择与探索：

**Step 1 — 根节点生成：** 从问题出发，生成 3-5 个候选推理方向（根节点），每个根节点代表一种根本不同的分析框架。

**Step 2 — 子节点展开：** 每个方向展开 3 个子节点，对应该方向的不同推理分支。

**Step 3 — 节点评估：** 对每个子节点进行三维度评估：
- `novelty`（新颖性 0-1）：该推理分支是否提供了独特视角而非重复已知结论
- `logical_strength`（逻辑强度 0-1）：推理链内的一致性和说服力
- `evidence_feasibility`（证据可行性 0-1）：该推理方向在现实中能否找到支撑证据

**Step 4 — 选择与展开：** 选择综合评分最高的子节点继续展开，形成深层推理链。

**Step 5 — 回溯剪枝：** 当某个方向的所有子节点综合评分 < 0.5 时，标记该方向为 dead_end 并回溯到上一级节点重新选择。

**Step R — 递归分支剪枝（M3）：**

每完成一轮推理路径展开后，对每个分支强制分类：

| 分类 | 判据 | 处理策略 |
|------|------|---------|
| **主根变量** | 解释力最广、能串联最多现象的核心变量 | 继续深挖，作为后续递归的锚点 |
| **强解释变量** | 有直接因果证据链、覆盖 ≥3 个现象 | 核心展开，与主根变量形成解释网络 |
| **辅助变量** | 有调节/中介作用但非根因 | 压缩为一段，标注"辅助" |
| **反证变量** | 与主流解释矛盾但证据充分 | 进红队阶段（T13） |
| **噪声变量** | 仅相关无因果、或证据等级 < C | 删除或归入"待观察"附录 |

**约束**：最多 1 主根 + 2-3 强解释 + 3-5 辅助 + 3-5 反证

**禁止令**：真正的深度是找到最能解释全局的根系，不是挖一堆地道。

**输出要求：** 须附加 `mpep_trace` 字段记录完整的树搜索踪迹。

---

### Step S：主线竞争择优（M9）

在完成 M3 递归分支剪枝后，对保留的候选路径执行主线竞争择优：

1. **候选路径筛选**：从剪枝后的路径中选取 3-5 条最强路径，每条路径独立发展核心论证
2. **五维加权评分**（总分 100）：
   - 证据强度（25%）：路径所依赖的证据质量、可验证性、多元来源一致性
   - 解释力（25%）：路径对核心现象的解释覆盖面和因果穿透力
   - 反证容忍度（20%）：路径在面对已知反证时的稳健性，是否能用同一框架解释反例
   - 新颖性（15%）：路径是否提供了超越常识/现有文献的新洞察
   - 可扩展性（15%）：路径是否可推广至关联问题域，是否支撑后续层级展开
3. **排名与分配**：
   - Rank 1 → 主线（mainline），必须 ≥ 60 分
   - Rank 2-3 → 子线（sublines），作为主线补充
   - Rank 4-5 → 反证材料（counterfactual material），用于检验主线稳健性
4. **铁律**：
   - 不得平均分配分数，每项评分必须有具体理由（基于实际证据和论证质量，非主观偏好）
   - 主线得分必须 ≥ 60 分，不达标则退回 Step A 重新构造推理路径
   - 主线与第二条路径的得分差距应 ≥ 5 分，否则说明路径区分度不足，需重新审视路径独立性

---

## gCastle 数据管线中间步骤

当使用 gCastle 进行因果发现时，由于 gCastle 需要结构化数值数据作为输入，而认知推理的产出通常是概念性的，因此需要以下中间步骤：

1. **概念变量提取**: 从 T09 推理产出中提取所有因果相关变量（概念名称）
2. **变量编码映射**: 为每个概念变量创建编码映射表（变量名 → 数值编码）
3. **伪数据集构造**: 基于因果方向和强度，使用 LLM 生成模拟数据集（N≥100 行）
4. **数据质量验证**: 检查伪数据集的基本统计特性（分布、相关性方向与因果假设一致性）
5. **gCastle 算法选择**: 从 30+ 种算法中选择 5-8 种代表性算法：
   - PC (约束式)
   - GES (评分式)
   - LiNGAM (函数式，需非高斯假设)
   - NOTEARS (连续优化式)
   - DirectLiNGAM (直接法)
   - MMHC (混合式)
   - ICA-LiNGAM (独立成分分析)
   - GOLEM (无环约束优化)
6. **结果交叉验证**: 至少 3 种算法结果一致时才接受因果边

注意：伪数据集方法仅提供定性参考，不可作为定量因果推断的依据。输出必须标注 "基于伪数据集的定性因果分析"。

### 算法适用性标注

| 算法类别 | 代表算法 | 适用场景 | 文本研究适用性 |
|----------|----------|----------|----------------|
| 约束式 | PC, FCI | 有条件独立检验 | 中（需伪数据集） |
| 评分式 | GES, MMHC | 有评分函数 | 中（需伪数据集） |
| 函数式 | LiNGAM, ICA-LiNGAM | 非高斯连续数据 | 低（假设难满足） |
| 连续优化 | NOTEARS, GOLEM | 可微分评分 | 中（需伪数据集） |
| 混合式 | MMHC | 离散+连续混合 | 中（需伪数据集） |

纯文本研究场景推荐：PC + GES + NOTEARS（3 种交叉验证）
有结构化数据场景推荐：PC + GES + LiNGAM + NOTEARS + GOLEM（5 种交叉验证）

---

## gCastle 穷尽重试状态

当因果发现库出现故障时，按以下规则穷尽重试：

```yaml
retrying_states:
  RETRYING_GCASTLE:
    trigger: "gCastle 导入失败或伪数据集构造失败"
    exhaust-retry: "使用 pgmpy + lingam + 时序因果发现 替代（不含 gCastle）"
    output_annotation: "因果发现穷尽重试：gCastle 不可用，使用替代库"

  RETRYING_CAUSAL:
    trigger: "所有因果发现库均不可用（gCastle + pgmpy + lingam + 时序因果发现 全部失败）"
    exhaust-retry: "纯定性因果分析，基于文献推理"
    output_annotation: "因果发现穷尽重试保底：仅提供定性因果分析，无算法验证"
```

穷尽重试执行规则：
1. 优先尝试 gCastle 全量流程
2. gCastle 失败时，切换到 RETRYING_GCASTLE，使用 pgmpy + lingam + 时序因果发现
3. 所有库均失败时，切换到 RETRYING_CAUSAL，输出纯定性因果分析
4. 穷尽重试状态必须在 `causal_graph_for_dynamics.data_source` 中标注
5. RETRYING_CAUSAL 状态下，`causal_graph_for_dynamics.confidence` 上限为 LOW

---

## must_not

- 不得生成结论雷同的"伪独立"路径
- 不得跳过meta_assumption——每条路径必须声明其核心预设
- 不得在divergence_points为空时声称路径间存在分歧
- 不得使用相同或几乎相同的overall_confidence值
- 推荐路径的理由不得是"直觉"或"明显"，必须基于矩阵分析
- 不得在路径生成时参考同一轮中已完成的任何其他路径
- 不得产出推理步数低于 7 步的路径
- 不得跳过 MPEP Selection 阶段——必须对所有 8 个 analysis_layer 计算 UCB 值后确定展开顺序
- 不得在 UCB 计算中忽略 exploration 项（c_exploration ≠ 0），防止仅凭 exploitation 导致低探索路径过早收敛

---

### TC-073 OpenNARS非公理推理方法论

**方法论原理**：OpenNARS非公理推理方法论的核心认知假设是——在知识不完全和资源受限的条件下，推理系统必须容忍矛盾而非崩溃，必须在不完全证据下做出"最佳当前判断"而非等待完美信息。传统逻辑系统（一阶逻辑、描述逻辑）遇到矛盾就失效，OpenNARS基于非公理逻辑（NAL）则将矛盾视为常态：每条信念带有真值（频率f+置信度c），矛盾信念共存但真值降低。这种方法论使认知推理从"追求逻辑一致性"升级为"在矛盾中持续推理"——当证据冲突时输出置信度而非真假二值，当资源受限时输出"最佳当前答案"而非拒绝回答。

**执行步骤**：
1. **非公理推理三原则应用**：(a) 经验性——所有知识来自经验（观察+推理），无先天确定真理；(b) 可修正性——新证据可修正旧信念，真值动态更新；(c) 资源适应性——推理深度和广度受可用资源约束
2. **真值函数计算**：为每条推理结论计算真值——(a) 频率f=正面证据数/总证据数（0-1）；(b) 置信度c=正面证据数/(正面证据数+先验常数k)（0-1）；(c) 真值=(f,c)，如(0.8,0.6)表示80%频率+60%置信度
3. **前向推理规则表应用**：从已知前提推导新结论——(a) 演绎规则：若A→B且B→C则A→C，真值由前提真值函数计算；(b) 归纳规则：若A→B观察到多次则归纳A→B，真值随观察次数增加；(c) 溯因规则：若A→B且观察到B则假设A，真值较低（溯因不确定性高）
4. **后向推理规则表应用**：从目标反推需要的前提——(a) 若目标B且已知A→B则子目标A；(b) 若目标B且已知B→C则目标C可能满足
5. **矛盾容忍处理**：当发现矛盾信念A和¬A时——(a) 不删除任一信念；(b) 降低矛盾双方的置信度；(c) 标注矛盾关系供后续推理参考
6. **资源受限推理**：在时间/内存约束下——(a) 优先处理高置信度+高相关性的信念；(b) 限制推理深度（最大链长度）；(c) 输出"最佳当前答案"而非等待完整推理

**决策规则**：

| 条件 | 决策 |
|------|------|
| 证据一致且充分 | 使用演绎推理，输出高置信度结论 |
| 证据部分冲突 | 使用加权推理，输出中等置信度结论，标注矛盾 |
| 证据严重矛盾 | 降低双方置信度，标注为"待解决矛盾" |
| 推理资源充足 | 执行完整推理链，输出多候选结论 |
| 推理资源受限 | 执行浅层推理，输出"最佳当前答案" |
| 置信度c>0.8 | 结论可信，可作为下游输入 |
| 0.5≤置信度c≤0.8 | 结论中等可信，标注不确定性 |
| 置信度c<0.5 | 结论低可信，仅作为假设参考 |
| OpenNARS不可用 | 穷尽重试为概率推理+手动矛盾标记 |

**输出规范**：
```yaml
opennars_reasoning:
  available: bool
  principles_applied: {experiential: bool, revisable: bool, resource_adaptive: bool}
  truth_values:
    - {statement: str, frequency: float, confidence: float, evidence_count: int}
  forward_rules_applied: [{rule: str, premises: [str], conclusion: str, truth: {f: float, c: float}}]
  backward_rules_applied: [{rule: str, goal: str, sub_goals: [str]}]
  contradictions: [{belief_a: str, belief_b: str, resolution: str}]
  best_current_answer: {statement: str, truth: {f: float, c: float}}
  resource_constraints: {depth_limit: int, time_budget: str}
  retrying_note: str|null
```

**穷尽重试策略**：当OpenNARS不可用时，按L1→L2→L3→L4逐级穷尽重试：L1 OpenNARS完整非公理推理（真值函数+前后向推理+矛盾容忍）→L2 概率推理（Pyro/贝叶斯网络替代，手动标注矛盾）→L3 模糊逻辑规则（手动定义隶属度函数+规则表）→L4 定性矛盾标注（手动识别矛盾并标注"待解决"，无真值计算）。

> 知识来源: TC-073 OpenNARS

---

## knowledge_refs

## NRSF 追加指令

T09 完成后，将散文式研究笔记追加到 NRSF-Full §T09：
- 每段 150-300 字，段落级引用
- 包含认知推理、逻辑推演、结论推导
- 遵循 nrsf-protocol.md 的散文式笔记格式

## 双阶段输出格式

### 阶段 A：结构化分析

原有的 output_schema 格式输出，用于 Supervisor 检查。

### 阶段 B：散文式研究笔记

追加到 NRSF-Full §T09 的散文式笔记，供下游消费。

## 外部能力卡片引用

- **TC-074 WebWeaver**: 当 depth_signal 触发深递归时，可用 WebWeaver 的动态大纲功能自动生成递归研究的大纲并迭代补充知识点。详见 `knowledge/external-capabilities/TC-074-WebWeaver.md`
- **MC-033 AGoT**: 自适应思维图推理，将推理路径组织为有向无环图结构。详见 `knowledge/external-capabilities/MC-033-AGoT.md`
- **MC-140 Bayesian-Inference**: 贝叶斯公式 + 全概率展开，P(H|E)=P(E|H)×P(H)/P(E)，动态后验更新。详见 `knowledge/external-capabilities-index.md`
- **MC-141 Bayes-Factor-Convergence**: 贝叶斯因子 BF=P(E|H)/P(E|¬H) + 收敛判定（连续3条证据ΔP<0.05）。详见 `knowledge/external-capabilities-index.md`
- **MC-142 Nash-Equilibrium**: 纳什均衡求解，纯策略与混合策略均衡判定。详见 `knowledge/external-capabilities-index.md`
- **MC-143 Dominant-Strategy**: 占优策略检测 + 重复剔除劣策略。详见 `knowledge/external-capabilities-index.md`
- **MC-144 Stock-Flow-Dynamics**: 存量-流量方程，反馈回路增益计算。详见 `knowledge/external-capabilities-index.md`
- **MC-145 Scenario-Expected-Value**: 期望值计算 E(D)=W_opt×V_opt+W_neu×V_neu+W_pes×V_pes。详见 `knowledge/external-capabilities-index.md`
- **MC-146 Monte-Carlo-Decision-Tree**: 蒙特卡洛仿真（1000-5000次）+ 决策树后序遍历EV计算。详见 `knowledge/external-capabilities-index.md`
- **MC-147 Net-Benefit-Composite**: 净收益公式 TR/TC + 加权综合评分。详见 `knowledge/external-capabilities-index.md`
- **MC-148 Risk-TCO**: 风险分 R=P×I（1-25）+ 总拥有成本 TCO。详见 `knowledge/external-capabilities-index.md`
- **MC-149 Value-Impact-Attenuation**: 价值观适配度 VAF + 影响衰减模型 I(t)=I_0×e^(-λt)+I_base。详见 `knowledge/external-capabilities-index.md`
- **MC-150 IBE-Abductive**: 最佳解释推断 IBE=0.45×E+0.30×S+0.25×C。详见 `knowledge/external-capabilities-index.md`
- **MC-151 Structural-Mapping**: 结构映射三原则（关系优先/系统性/一一对应）。详见 `knowledge/external-capabilities-index.md`
- **MC-152 Causal-Effect-Confounding**: 因果效应量（Cohen's d/β/OR）+ 混淆变量识别。详见 `knowledge/external-capabilities-index.md`
- **MC-153 Welfare-Transmission**: 福利三角 ΔTS=ΔCS+ΔPS+ΔGR+ΔEXT + 政策传导链四级衰减。详见 `knowledge/external-capabilities-index.md`
- **MC-154 Bass-S-Curve**: Bass创新扩散 n(t)=[p+q×N(t)/m]×[m-N(t)] + S曲线预测。详见 `knowledge/external-capabilities-index.md`
- **MC-155 Assumption-Counterfactual**: 三层假设挖掘（显性/隐性/深层）+ 七种反事实推演。详见 `knowledge/external-capabilities-index.md`
- **MC-156 Bias-Socratic-Scan**: 11类认知偏误全扫描 + 苏格拉底式诘问5条追问链。详见 `knowledge/external-capabilities-index.md`
- **MC-157 Robustness-Stress-Test**: 五类鲁棒性压力测试。详见 `knowledge/external-capabilities-index.md`
- **MC-158 Axiom-Verification**: 公理验证四标准 + 递归拆解锚定验证。详见 `knowledge/external-capabilities-index.md`
- **MC-159 MECE-Prioritization**: MECE递归分解 + 问题优先级排序 I×(11-U)。详见 `knowledge/external-capabilities-index.md`
- **MC-160 Power-Interest-Matrix**: 权力-利益矩阵四象限定位 + 动机四层级。详见 `knowledge/external-capabilities-index.md`
- **MC-161 Aufheben-Synthesis**: 扬弃操作（否定/保留/提升）+ 合题质量七标准。详见 `knowledge/external-capabilities-index.md`
- **MC-162 Layer-Peeling**: 五层剥开架构L0-L4 + 每层触发/终止条件判定。详见 `knowledge/external-capabilities-index.md`
- **MC-163 Norm-Lifecycle**: 社会规范生命周期五阶段。详见 `knowledge/external-capabilities-index.md`
- **MC-164 Comparison-Significance**: 异同矩阵构造 + 差异显著性评估 + 根因追溯。详见 `knowledge/external-capabilities-index.md`
- **MC-165 STEEP-Scenario**: STEEP五维驱动力分解 + 多情景构建。详见 `knowledge/external-capabilities-index.md`
- **MC-166 Feasibility-Assessment**: 四维可行性评估（政治/经济/技术/社会）。详见 `knowledge/external-capabilities-index.md`
- **MC-167 Decision-Tree-EV**: 决策树构建 + 后序遍历期望值最大化。详见 `knowledge/external-capabilities-index.md`
- **MC-168 Alternative-Assessment**: 替代方案三维评估：综合分=0.35×新颖度+0.35×可行性+0.30×协同度。详见 `knowledge/external-capabilities-index.md`
- **MC-169 One-Vote-Veto**: 一票否决四条件。详见 `knowledge/external-capabilities-index.md`
- **MC-170 Evidence-Independence**: 证据独立性检查四问。详见 `knowledge/external-capabilities-index.md`
- **MC-171 System-Emergence**: 系统边界映射 + 涌现性检测 + Meadows 12级杠杆点。详见 `knowledge/external-capabilities-index.md`
- **MC-172 Steelmanning**: 钢化论证六标准（逐命题攻击/精度提升/边界明确/不确定性标注/替代排除/博弈稳定）。详见 `knowledge/external-capabilities-index.md`
- **MC-173 Unintended-Consequences**: 五类意外后果检测。详见 `knowledge/external-capabilities-index.md`
- **MC-174 Trigger-Structure-Coupling**: 触发事件vs结构条件耦合分析 + "火花-湿木"类比判定。详见 `knowledge/external-capabilities-index.md`
- **MC-175 Narrative-Analysis**: 叙事五维分析（角色/时间/因果/情绪/省略）+ 竞争叙事评估。详见 `knowledge/external-capabilities-index.md`
- **MC-176 Empowerment-Substitution**: 赋能与替代矩阵（四象限）。详见 `knowledge/external-capabilities-index.md`
- **MC-177 Cross-Dimension-Correlation**: 跨维度关联分析五维交叉影响矩阵。详见 `knowledge/external-capabilities-index.md`
- **MC-178 Fairness-Distribution**: 公平性评估矩阵（收入五等分）+ 进步性/倒退性/中性政策裁定。详见 `knowledge/external-capabilities-index.md`
- **MC-179 Transmission-Attenuation**: 传导衰减检查（弹性/抵消/辐射范围/时滞/残留率）。详见 `knowledge/external-capabilities-index.md`
- **MC-183 Scallop**: 神经符号推理（Datalog规则+神经网络概率输出），NS-Engine第8推理路径，在Pyro与OpenNARS之间建立第三种推理范式。详见 `knowledge/external-capabilities-index.md`
- **TC-087 OpenSpiel**: 在路径 C（博弈推理）中，当参与者 ≥ 3 或策略空间 ≥ 5 时，调用 OpenSpiel 进行算法化均衡求解。详见 `knowledge/external-capabilities-index.md`
- **TC-088 Axelrod**: 在路径 C（博弈推理）中，当重复博弈场景（互动次数 ≥ 5）时，调用 Axelrod 策略库进行策略匹配与锦标赛模拟。详见 `knowledge/external-capabilities-index.md`
- **MC-184 ABLkit-CBRkit**: 在路径 F（类比推理）中，当源域与目标域各含 ≥ 5 个结构化关系时，调用 ABLkit 的 SME/FAM 算法进行量化结构映射；当存在历史案例库时，调用 CBRkit 执行案例推理四步循环。详见 `knowledge/external-capabilities-index.md`

---

### [Scallop] 源码逻辑引入

#### 核心算法逻辑

**1. Datalog 推理引擎前向链推理算法源码逻辑**

```
前向链推理核心流程（scallop/core/forward_chaining.py）:

function forward_chaining(rules, facts, max_iterations=100):
    # rules: Datalog规则集合
    # facts: 初始事实集合（EDB，外延数据库）

    derived_facts = copy(facts)  # 已知事实+推导事实

    for iteration in 1..max_iterations:
        new_facts = set()

        for rule in rules:
            # Datalog规则格式: head :- body1, body2, ..., bodyN
            # 例: ancestor(X, Z) :- parent(X, Y), ancestor(Y, Z)

            # 步骤1：模式匹配——找到规则体中所有谓词的匹配
            bindings = match_body(rule.body, derived_facts)
            # bindings: 变量绑定列表 [{X: alice, Y: bob}, ...]

            # 步骤2：对每个绑定生成头部事实
            for binding in bindings:
                head_fact = instantiate_head(rule.head, binding)
                if head_fact not in derived_facts:
                    new_facts.add(head_fact)

        # 步骤3：合并新推导的事实
        if len(new_facts) == 0:
            break  # 不动点到达——无新事实可推导
        derived_facts = derived_facts ∪ new_facts

    return derived_facts

function match_body(body_atoms, facts):
    # 逐原子匹配，逐步约束变量绑定
    # 类似关系数据库的join操作
    bindings = [{}]  # 初始空绑定

    for atom in body_atoms:
        # atom格式: predicate(arg1, arg2, ...)
        new_bindings = []
        for binding in bindings:
            # 在facts中查找匹配atom的元组
            for fact in facts:
                if fact.predicate == atom.predicate:
                    new_binding = unify(atom, fact, binding)
                    if new_binding is not None:
                        new_bindings.append(new_binding)
        bindings = new_bindings

    return bindings

# 否定处理（stratified negation）:
# Scallop使用分层否定——按依赖图分层，每层内不允许递归否定
function stratify(rules):
    # 构建谓词依赖图
    # 否定边标记为"负"边
    # 按拓扑排序分层
    # 若存在负边环 → 报错"不可分层"
    strata = topological_sort_by_negative_edges(rules)
    return strata
```

**2. 神经符号融合架构概率传播计算源码逻辑**

```
概率传播核心流程（scallop/probabilistic/provenance.py）:

function probabilistic_forward_chaining(rules, probabilistic_facts):
    # probabilistic_facts: Dict[fact, probability]
    # 例: {sunny(t): 0.8, rain(t): 0.3}

    # 使用证明追踪（provenance）计算推导事实的概率
    provenance_graph = build_provenance_graph(rules, probabilistic_facts)

    for iteration in 1..max_iterations:
        for rule in rules:
            for binding in match_body(rule.body, probabilistic_facts):
                head_fact = instantiate_head(rule.head, binding)

                # 计算头部事实的概率
                # 使用证明追踪的半环（semiring）计算
                body_prob = compute_body_probability(
                    rule.body, binding, probabilistic_facts
                )
                head_prob = body_prob  # Datalog蕴含保持概率

                # 更新头部事实概率（取最大值——disjunctive证明）
                if head_fact in probabilistic_facts:
                    probabilistic_facts[head_fact] = max(
                        probabilistic_facts[head_fact], head_prob
                    )
                else:
                    probabilistic_facts[head_fact] = head_prob

    return probabilistic_facts

function compute_body_probability(body, binding, prob_facts):
    # 合取概率：P(A ∧ B) = P(A) × P(B)（独立性假设）
    # 析取概率：P(A ∨ B) = 1 - (1-P(A)) × (1-P(B))

    if body is conjunction:
        prob = 1.0
        for atom in body:
            fact = instantiate(atom, binding)
            prob *= prob_facts[fact]  # 合取=乘积
        return prob

    elif body is disjunction:
        prob = 0.0
        for atom in body:
            fact = instantiate(atom, binding)
            prob = 1 - (1 - prob) * (1 - prob_facts[fact])  # 析取=De Morgan
        return prob

# 神经网络-符号桥接:
# 1. 神经网络输出概率化感知结果（如目标检测置信度）
# 2. 概率化结果作为probabilistic_facts输入Datalog引擎
# 3. Datalog推导产生概率化推理结果
# 4. 概率化结果可反馈到神经网络训练（可微分）
```

#### 数据结构设计

```
核心数据结构:

1. Rule: Datalog规则
   - head: Atom               # 头部原子
   - body: list[Atom]         # 体部原子列表（合取）
   - is_negated: Dict[Atom, bool]  # 否定标记

2. Atom: 谓词原子
   - predicate: str           # 谓词名
   - arguments: list[Term]    # 参数（变量或常量）

3. ProbabilisticFact: 概率化事实
   - fact: Atom               # 事实原子
   - probability: float       # 概率值 [0, 1]
   - provenance: list[Rule]   # 证明追踪（推导路径）

4. ProvenanceGraph: 证明图
   - nodes: set[Fact]         # 事实节点
   - edges: set[(Rule, Fact)] # 推导边
```

#### 决策流程

```
Scallop 神经符号推理决策流程:

1. 输入解析 → 将问题编码为Datalog规则+概率化事实
2. 分层检查 → stratify() 确保规则可分层
3. 前向链推理 → forward_chaining() 推导新事实
4. 概率传播 → probabilistic_forward_chaining() 计算概率
5. 结果提取 → 从推导事实中提取答案及置信度
6. 反馈训练（可选）→ 可微分概率传播支持端到端训练
```

#### 穷尽重试策略

```yaml
scallop_source_retrying:
  L1_FULL_NEUROSYMBOLIC:
    condition: "Scallop可用，Datalog推理+概率传播均可执行"
    action: "完整神经符号推理：规则编码+前向链+概率传播"
    confidence: "HIGH"

  L2_SYMBOLIC_ONLY:
    condition: "概率传播不可用（无神经网络输出）"
    action: "仅使用确定性Datalog推理（布尔事实），无概率"
    confidence: "MEDIUM"
    output_annotation: "Scallop穷尽重试：确定性符号推理，无概率传播"

  L3_MANUAL_DATALOG:
    condition: "Scallop不可用，但可手动编写Datalog规则"
    action: "手动前向链推理——逐步应用规则推导"
    confidence: "LOW-MEDIUM"
    output_annotation: "Scallop穷尽重试：手动Datalog推理"

  L4_NATURAL_REASONING:
    condition: "Datalog形式化不可行"
    action: "自然语言逻辑推理，标注'无形式化验证'"
    confidence: "LOW"
    output_annotation: "Scallop穷尽重试保底：自然语言逻辑推理"
```
