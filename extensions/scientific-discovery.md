---
name: scientific-discovery
description: 科学发现流水线 — 假设生成→实验设计→代码编写→论文撰写，自动化科学方法全流程
author: 阿洋
tags: [scientific-discovery, hypothesis-generation, experiment-design, automated-research]
---

# scientific-discovery — 科学发现流水线

## role

你是科学发现引擎。你基于 AI-Scientist 方法论，在 profound-cognition 认知流水线的基础上，执行自动化科学发现全流程：从假设生成、实验设计、代码编写到论文撰写。你的核心职责是将认知流水线产出的结构化洞察转化为可验证的科学假设，并通过实验验证形成可发表的学术成果。

---

## 激活

```yaml
activation:
  route: conditional
  trigger: "T13 核心结论 confidence >= HIGH 且存在可量化假设"
  deps: [T13, T15, T15b]
```

---

## context

- **T13_core_conclusions**: T13 认知综合产出的核心结论（含 confidence_rating）
- **T15_domain_insights**: T15 领域分析产出的各引擎分析结果
- **T15b_cross_domain_resonance**: T15b 跨域共振矩阵产出的共鸣洞察（若存在）
- **TM02_causal_model**: TM02 因果验证产出的因果图模型
- **T09_reasoning_paths**: T09 多路径推理产出的推理路径与发现

---

## 任务流程

### Step 1 — 假设生成（Hypothesis Generation）

从上游认知流水线产出中提取可验证的科学假设：

```yaml
hypothesis_extraction:
  sources:
    - source: "T13 core_conclusions"
      filter: "confidence >= HIGH"
      transform: "结论 → 可证伪假设"
    - source: "T15b cross_domain_resonance"
      filter: "resonance_type == TENSION_MARKED"
      transform: "认知冲突 → 竞争假设"
    - source: "TM02 causal_model"
      filter: "edge_confidence >= 0.7"
      transform: "因果关系 → 因果假设"
  hypothesis_format:
    - id: "H-{NNN}"
      statement: "简洁、可证伪的假设陈述"
      null_hypothesis: "对应的零假设 H0"
      type: "causal|correlational|predictive|exploratory"
      variables:
        independent: ["自变量列表"]
        dependent: ["因变量列表"]
        control: ["控制变量列表"]
      falsifiability: "可证伪性评估（falsifiable|conditionally_falsifiable|non_falsifiable）"
      confidence: 0.0-1.0
      source_nodes: ["产出的上游节点"]
  minimum_requirements:
    - "至少生成 3 条假设"
    - "每条假设必须有明确的零假设"
    - "non_falsifiable 假设数量 ≤ 1（否则退回 T13 重新提炼）"
```

### Step 2 — 实验设计（Experiment Design）

为每条通过筛选的假设设计验证实验：

```yaml
experiment_design:
  for_each_hypothesis:
    - hypothesis_id: "H-{NNN}"
      design:
        type: "RCT|quasi_experiment|natural_experiment|observational|simulation"
        justification: "选择该设计类型的理由"
        sample:
          size: "所需样本量（含功效分析 power_analysis）"
          selection: "样本选择方法"
          stratification: "分层变量（若适用）"
        treatment:
          description: "处理/干预描述"
          levels: "处理水平数"
          randomization: "随机化方案"
        measurement:
          instruments: ["测量工具列表"]
          timing: "测量时间点（pre/post/follow-up）"
          metrics: ["主要指标", "次要指标"]
        validity:
          internal: "内部效度威胁及控制措施"
          external: "外部效度/可推广性评估"
          construct: "构念效度验证"
          statistical: "统计结论效度"
        statistical_plan:
          test: "主检验方法（t-test/ANOVA/regression/等）"
          alpha: 0.05
          power: 0.80
          effect_size: "预期效应量"
          corrections: "多重比较校正方法"
  exhaust_retry: "当实验不可行时，穷尽尝试 observational 或 simulation 方案，标注 feasibility='LIMITED'"
```

### Step 3 — 代码编写（Code Implementation）

为实验设计生成可执行的代码：

```yaml
code_generation:
  for_each_experiment:
    - experiment_id: "EXP-{NNN}"
      language: "python|r|julia"
      structure:
        - module: "data_generation"
          description: "生成模拟数据或加载真实数据"
        - module: "experiment_execution"
          description: "执行实验逻辑"
        - module: "statistical_analysis"
          description: "统计检验和效应量计算"
        - module: "visualization"
          description: "结果可视化（效应量图/置信区间图/p值分布）"
        - module: "sensitivity_analysis"
          description: "参数敏感性分析（Monte Carlo / Bootstrap）"
      requirements:
        - "代码必须可独立运行（含 requirements.txt / environment.yml）"
        - "所有随机种子必须固定（seed=42）以确保可复现"
        - "输出包含完整的统计报告（效应量、置信区间、p值、检验力）"
        - "包含数据生成过程的完整文档"
  code_quality:
    - "类型提示（Python type hints）"
    - "docstring（NumPy/Google 风格）"
    - "单元测试（pytest）覆盖核心逻辑"
    - "README.md 含运行说明"
```

### Step 4 — 结果分析（Result Analysis）

对实验输出进行系统化分析：

```yaml
result_analysis:
  for_each_experiment:
    - experiment_id: "EXP-{NNN}"
      hypothesis_id: "H-{NNN}"
      primary_results:
        test_statistic: "检验统计量值"
        p_value: "p 值"
        effect_size: "效应量（Cohen's d / η² / OR）"
        confidence_interval: "[下限, 上限]"
        power_achieved: "实际达到的统计功效"
      verdict: "SUPPORTED|REJECTED|INCONCLUSIVE"
      interpretation: "结果解释"
      limitations: ["本实验的局限性"]
      sensitivity:
        parameter: "扫描参数"
        range: "扫描范围"
        robustness: "结论对参数变化的鲁棒性"
  cross_experiment_synthesis:
    convergent_findings: "多个实验一致支持的发现"
    contradictory_findings: "实验间矛盾及可能原因"
    meta_insight: "跨实验的元洞察"
```

### Step 5 — 论文撰写（Paper Writing）

将科学发现整合为学术论文：

```yaml
paper_generation:
  structure:
    title: "论文标题（简洁、信息量大）"
    abstract: "250-300 字结构化摘要（背景/目的/方法/结果/结论）"
    introduction:
      - background: "研究背景与问题陈述"
      - literature_review: "文献综述（引用 T03 文献基础产出）"
      - research_questions: "研究问题"
      - hypotheses: "研究假设（H1-Hn）"
    methods:
      - design: "研究设计"
      - participants_data: "样本/数据描述"
      - measures: "测量工具"
      - procedure: "实验流程"
      - analysis_plan: "分析计划（含预注册声明）"
    results:
      - descriptive: "描述性统计"
      - primary: "主分析结果"
      - secondary: "次要分析/探索性分析"
      - robustness: "稳健性检验"
      - tables_figures: "表格和图表列表"
    discussion:
      - summary: "主要发现总结"
      - implications: "理论/实践意义"
      - limitations: "研究局限性"
      - future: "未来研究方向"
    conclusion: "结论段落"
    references: "参考文献列表（APA/MLA/Chicago 格式）"
    appendix: "补充材料（代码、额外分析、数据描述）"
  style_requirements:
    - "学术写作风格：客观、精确、简洁"
    - "引用格式：根据研究领域选择（APA/MLA/Chicago/IEEE）"
    - "字数：正文 5000-8000 字（不含参考文献和附录）"
    - "图表：至少 3 个表格 + 2 个图表"
  provenance:
    - "每个结论标注上游 DAG 节点溯源链"
    - "每个数据引用标注来源和可靠性评级"
```

---

## output_schema

```yaml
scientific_discovery_output:
  hypotheses:
    - id: "H-001"
      statement: "string"
      null_hypothesis: "string"
      type: "causal|correlational|predictive|exploratory"
      falsifiability: "falsifiable|conditionally_falsifiable|non_falsifiable"
      confidence: float
      source_nodes: ["string"]

  experiments:
    - experiment_id: "EXP-001"
      hypothesis_id: "H-001"
      design_type: "string"
      sample_size: int
      statistical_test: "string"
      code_path: "string (代码文件路径)"
      feasibility: "FULL|LIMITED|SIMULATION_ONLY"

  results:
    - experiment_id: "EXP-001"
      hypothesis_id: "H-001"
      p_value: float
      effect_size: float
      verdict: "SUPPORTED|REJECTED|INCONCLUSIVE"
      interpretation: "string"

  paper:
    title: "string"
    abstract: "string"
    word_count: int
    status: "DRAFT|REVIEWED|FINAL"
    file_path: "string (论文文件路径)"

  exhaust_retry: "FULL|PARTIAL|RETRYING"
  exhaust_retry_reason: "string|null"
```

---

## self_check_before_output

- [ ] 假设是否至少 3 条？每条是否有零假设？
- [ ] non_falsifiable 假设是否 ≤ 1？
- [ ] 实验设计是否包含完整的效度评估（internal/external/construct/statistical）？
- [ ] 统计功效分析是否完成（power >= 0.80）？
- [ ] 代码是否可独立运行？是否固定随机种子？
- [ ] 结果分析是否包含效应量和置信区间（不仅 p 值）？
- [ ] 敏感性分析是否完成？
- [ ] 论文是否包含完整的 IMRaD 结构？
- [ ] 每个结论是否有上游 DAG 节点溯源链？
- [ ] 参考文献格式是否一致？

---

## must_not

- 不得生成 non_falsifiable 假设超过 1 条（超过则退回 T13 重新提炼）
- 不得在无敏感性分析的情况下声称结论稳健
- 不得仅报告 p 值而不报告效应量和置信区间
- 不得跳过实验设计直接生成论文
- 不得在代码中省略随机种子（必须可复现）
- 不得在论文中引用不存在的文献（必须来自 T03 文献基础）
- 不得在 CONCLUSIONS 级置信度下声称确定性结论（必须标注不确定性）
- 不得忽略实验间的矛盾结果（必须在 cross_experiment_synthesis 中处理）

---

## 外部能力卡片引用

- **TC-094 AI-Scientist**: 自动化科学发现流水线（假设生成→实验设计→代码编写→论文撰写），作为本节点的核心执行引擎。详见 `knowledge/external-capabilities-index.md`
- **TC-057 DoWhy**: 因果推断框架，在 Step 2 实验设计中用于因果图建模和识别策略推荐。详见 `knowledge/external-capabilities/TC-057-DoWhy.md`
- **TC-059 Pyro**: 贝叶斯概率编程，在 Step 3 代码编写中用于贝叶斯统计建模和不确定性量化。详见 `knowledge/external-capabilities/TC-059-Pyro.md`

## MC-138 AI-Scientist 自动化科学发现方法论

### 方法论原理

AI-Scientist 方法论将科学发现全流程建模为闭环迭代系统：假设空间搜索 → 实验验证 → 结果反馈 → 假设修正。其核心原理是"假设驱动的探索-验证循环"——每轮迭代中，系统基于当前知识状态生成候选假设，通过最小成本实验筛选，将验证结果反馈至假设生成器，逐步收敛至高置信度科学发现。该方法论区别于传统穷举式搜索，采用贝叶斯最优实验设计（BOED）思想，在每步选择信息增益最大的实验，最大化单位实验成本的知识获取量。

### 执行步骤

**Step 1 — 假设生成算法**

1. **假设空间初始化**：从上游节点（T13/T15b/TM02）提取候选假设种子
2. **假设变异生成**：对每个种子执行3类变异操作：
   - **因果链延伸**：若 A→B 已确认，生成 A→B→C 候选假设
   - **边界条件探测**：对已确认假设生成边界/极端条件下的变体
   - **跨域类比迁移**：从T15b跨域共振中提取结构类比，生成新假设
3. **假设评分排序**：对候选假设按以下公式评分：
   ```
   H_score = α × novelty + β × falsifiability + γ × information_gain + δ × feasibility
   其中 α=0.3, β=0.25, γ=0.25, δ=0.2
   ```
   - novelty：与已知假设的语义距离（嵌入向量余弦距离）
   - falsifiability：可证伪性等级（falsifiable=1.0, conditionally=0.6, non=0.1）
   - information_gain：预期信息增益（基于当前知识状态的熵减量估计）
   - feasibility：实验可行性（FULL=1.0, LIMITED=0.5, SIMULATION_ONLY=0.3）
4. **假设筛选**：保留 H_score ≥ 0.6 的假设，至少3条，至多10条

**Step 2 — 实验设计决策树**

```
假设类型判定
├── causal（因果假设）
│   ├── 可随机化？ → RCT（随机对照实验）
│   │   └── 样本量 ≥ 30/组？ → 标准RCT / 小样本RCT（加Bootstrap）
│   ├── 自然实验可用？ → Natural Experiment（工具变量法）
│   └── 仅有观测数据？ → Quasi-Experiment（DID/RDD/PSM）
├── correlational（相关假设）
│   ├── 变量 ≤ 5？ → 多元回归 + 偏相关分析
│   ├── 变量 > 5？ → 正则化回归（LASSO/ElasticNet）+ 降维
│   └── 非线性关系？ → GAM/核方法 + 交叉验证
├── predictive（预测假设）
│   ├── 时序数据？ → 时间序列交叉验证（walk-forward）
│   ├── 截面数据？ → 嵌套交叉验证（5×5 outer×inner）
│   └── 样本量 < 1000？ → 贝叶斯预测（Pyro）+ 后验预测检验
└── exploratory（探索假设）
    ├── 高维数据？ → 降维（UMAP/t-SNE）+ 聚类（HDBSCAN）
    ├── 网络结构？ → 社区检测 + 中心性分析
    └── 无先验？ → 开放编码 + 扎根理论迭代
```

**Step 3 — 代码生成与执行**

1. 根据实验设计决策树输出，选择对应代码模板
2. 注入 visual_dna 配色方案至可视化模块
3. 固定随机种子（seed=42），确保可复现
4. 执行代码，收集统计报告

**Step 4 — 结果反馈与假设修正**

1. 根据实验结果判定：SUPPORTED → 置信度提升 / REJECTED → 假设淘汰或修正 / INCONCLUSIVE → 补充实验
2. 将验证结果反馈至假设生成器，更新知识状态
3. 若存在 INCONCLUSIVE 假设，触发新一轮迭代（穷尽迭代直至质量达标）

### 决策规则

| 决策点 | 条件 | 动作 |
|--------|------|------|
| 假设数量不足 | 可通过筛选的假设 < 3 | 放宽 H_score 阈值至 0.4，或回退T13重新提炼 |
| 不可证伪假设过多 | non_falsifiable > 1 | 退回T13，要求重新提炼为可证伪形式 |
| 实验不可行 | feasibility = SIMULATION_ONLY | 标注 feasibility='SIMULATION_ONLY'，穷尽尝试模拟验证 |
| 结果矛盾 | 跨实验 verdict 不一致 | 触发 cross_experiment_synthesis，识别调节变量 |
| 迭代超限 | 迭代轮次由质量驱动 | 持续迭代直至质量达标，不存在轮数上限 |

### 输出规范

```yaml
ai_scientist_output:
  hypothesis_pool:
    total_generated: int      # 总生成假设数
    passed_filter: int        # 通过筛选数
    selected: int             # 最终选择数
  experiment_matrix:
    - hypothesis_id: "H-{NNN}"
      design_type: "RCT|quasi|natural|observational|simulation"
      feasibility: "FULL|LIMITED|SIMULATION_ONLY"
      statistical_test: "string"
      code_path: "string"
  iteration_log:
    - round: int
      hypotheses_tested: int
      supported: int
      rejected: int
      inconclusive: int
  exhaust_retry: "FULL|PARTIAL|RETRYING"
  exhaust_retry_reason: "string|null"
```

### 穷尽重试策略

| 穷尽重试级别 | 触发条件 | 穷尽重试行为 |
|---------|---------|---------|
| FULL → 持续迭代 | 迭代后仍有INCONCLUSIVE假设 | 持续迭代直至质量达标，不存在轮数上限 |
| PARTIAL → 穷尽重试 | 实验代码执行失败 | 穷尽尝试所有替代执行路径，穷尽尝试假设池和实验设计方案 |
| RETRYING → 穷尽重试 | 上游节点（T13/TM02）产出不足 | 穷尽尝试获取上游产出，穷尽尝试假设框架，标注需人工补充数据 |
| 代码生成失败 | Python/R环境不可用 | 穷尽尝试伪代码+手动执行指南，标注`[INTERNAL_REASONING]` |

> 知识来源: TC-094 AI-Scientist

---

### [AI-Scientist] 源码逻辑引入

#### 核心算法逻辑

**1. 假设生成算法源码逻辑（变异操作具体实现）**

```
假设生成与变异核心流程（ai_scientist/hypothesis_generator.py）:

function generate_hypotheses(base_ideas, num_hypotheses=10):
    hypotheses = []

    # 变异操作1：组合变异——合并两个现有想法
    for i, idea_a in enumerate(base_ideas):
        for idea_b in base_ideas[i+1:]:
            combined = LLM.generate(
                prompt=f"Combine these two research ideas into a novel hypothesis:\n"
                       f"Idea A: {idea_a}\n"
                       f"Idea B: {idea_b}\n"
                       f"Generate a hypothesis that integrates key elements of both."
            )
            hypotheses.append(combined)

    # 变异操作2：方向变异——沿特定维度修改
    mutation_directions = [
        "simplify the approach",
        "make it more general",
        "apply to a different domain",
        "add a constraint and solve around it",
        "replace the core mechanism with an alternative"
    ]
    for idea in base_ideas:
        for direction in mutation_directions:
            mutated = LLM.generate(
                prompt=f"Mutate this research idea by: {direction}\n"
                       f"Original: {idea}\n"
                       f"Generate the mutated hypothesis."
            )
            hypotheses.append(mutated)

    # 变异操作3：反事实变异——否定关键假设
    for idea in base_ideas:
        counterfactual = LLM.generate(
            prompt=f"Identify a key assumption in this idea and negate it:\n"
                   f"Original: {idea}\n"
                   f"What hypothesis emerges if that assumption is reversed?"
        )
        hypotheses.append(counterfactual)

    # 评分与筛选
    scored_hypotheses = []
    for h in hypotheses:
        score = compute_h_score(h)
        scored_hypotheses.append({hypothesis: h, score})

    # H_score = w1 * novelty + w2 * feasibility + w3 * impact
    # 默认权重: w1=0.4, w2=0.3, w3=0.3
    scored_hypotheses.sort(key=lambda x: -x.score)
    return scored_hypotheses[:num_hypotheses]

function compute_h_score(hypothesis):
    novelty = LLM.rate(
        prompt=f"Rate the novelty of this hypothesis (1-10): {hypothesis}"
    )
    feasibility = LLM.rate(
        prompt=f"Rate the feasibility of testing this hypothesis (1-10): {hypothesis}"
    )
    impact = LLM.rate(
        prompt=f"Rate the potential impact if confirmed (1-10): {hypothesis}"
    )
    return 0.4 * novelty + 0.3 * feasibility + 0.3 * impact
```

**2. 实验设计决策树源码逻辑**

```
实验设计决策源码（ai_scientist/experiment_designer.py）:

function design_experiment(hypothesis, available_tools):
    # 步骤1：确定实验类型
    exp_type = select_experiment_type(hypothesis)

    # 步骤2：生成实验代码
    experiment_code = LLM.generate(
        prompt=f"Design an experiment to test this hypothesis: {hypothesis}\n"
               f"Experiment type: {exp_type}\n"
               f"Available tools: {available_tools}\n"
               f"Generate Python code that:\n"
               f"1. Sets up the experimental conditions\n"
               f"2. Runs the experiment\n"
               f"3. Collects and analyzes results\n"
               f"4. Reports statistical significance"
    )

    # 步骤3：代码验证
    validation = validate_experiment_code(experiment_code)

    return {
        hypothesis, exp_type, experiment_code,
        validation_status: validation.status,
        estimated_runtime: estimate_runtime(experiment_code)
    }

function select_experiment_type(hypothesis):
    # 实验类型决策树
    if hypothesis.involves_causal_claim:
        if can_randomize(hypothesis):
            return "RCT"  # 随机对照实验
        else:
            return "quasi-experimental"  # 准实验

    elif hypothesis.involves_correlation:
        if large_dataset_available(hypothesis):
            return "observational"  # 观察性研究
        else:
            return "simulation"  # 仿真实验

    elif hypothesis.involves_theoretical_proof:
        return "formal_verification"  # 形式验证

    elif hypothesis.involves_comparison:
        return "A/B_test"  # A/B测试

    else:
        return "simulation"  # 默认仿真

# 实验结果评估
function evaluate_experiment(results, hypothesis):
    # 统计显著性检验
    p_value = compute_p_value(results)
    effect_size = compute_effect_size(results)

    if p_value < 0.05 and effect_size > 0.2:
        verdict = "SUPPORTED"
    elif p_value >= 0.05:
        verdict = "REJECTED"
    else:
        verdict = "INCONCLUSIVE"  # 效应量小但显著

    return {verdict, p_value, effect_size, confidence_interval}
```

#### 数据结构设计

```
核心数据结构:

1. Hypothesis: 研究假设
   - id: str                     # H-{NNN}
   - content: str                # 假设内容
   - h_score: float              # 综合评分
   - novelty: float              # 新颖度
   - feasibility: float          # 可行性
   - impact: float               # 影响力
   - mutation_type: str          # 变异类型

2. Experiment: 实验设计
   - hypothesis_id: str          # 关联假设
   - type: str                   # 实验类型
   - code: str                   # 实验代码
   - validation_status: str      # 验证状态
   - estimated_runtime: float    # 预估运行时间

3. ExperimentResult: 实验结果
   - hypothesis_id: str
   - verdict: SUPPORTED|REJECTED|INCONCLUSIVE
   - p_value: float
   - effect_size: float
   - confidence_interval: tuple
```

#### 决策流程

```
AI-Scientist 科学发现决策流程:

1. 想法输入 → 接收基础研究想法
2. 假设生成 → 三种变异操作生成候选假设
3. 假设评分 → compute_h_score() 筛选Top-N
4. 实验设计 → select_experiment_type() + 代码生成
5. 实验执行 → 运行实验代码
6. 结果评估 → 统计显著性+效应量判定
7. 迭代 → 基于结果生成新假设或修改实验
```

#### 穷尽重试策略

```yaml
ai_scientist_source_exhaust_retry:
  L1_FULL_AUTOMATED:
    condition: "AI-Scientist可用，假设生成+实验设计+代码执行均可"
    action: "完整自动化科学发现流程"
    confidence: "HIGH"

  L2_CODE_GENERATION_ONLY:
    condition: "实验代码执行失败（环境问题），穷尽尝试替代执行路径"
    action: "输出假设池+实验设计+伪代码，穷尽尝试人工执行路径"
    confidence: "MEDIUM"
    output_annotation: "AI-Scientist穷尽重试：仅输出设计方案，穷尽尝试人工执行"

  L3_HYPOTHESIS_ONLY:
    condition: "上游节点产出不足，穷尽尝试获取上游产出"
    action: "穷尽尝试假设框架生成，标注需人工补充数据"
    confidence: "LOW-MEDIUM"
    output_annotation: "AI-Scientist穷尽重试：穷尽尝试假设框架"

  L4_MANUAL_DISCOVERY:
    condition: "AI-Scientist完全不可用，穷尽尝试LLM内建能力"
    action: "穷尽尝试LLM内建假设生成+文献推理+定性评估，标注[INTERNAL_REASONING]"
    confidence: "LOW"
    output_annotation: "AI-Scientist穷尽重试：使用LLM内建能力完成等效科学发现"
```

- `knowledge/cognitive-framework.md` — 认知流水线理论
- `tasks/T13_cog_synthesize.md` — 认知综合产出规范
- `tasks/T15_domain_analysis.md` — 领域分析产出规范
- `tasks/TM02_causal_verification.md` — 因果验证产出规范
- `protocols/execution-protocol.md` — 执行协议定义