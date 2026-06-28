<!-- 作者：阿洋 -->
<!-- output_type_restriction: [research_report, wechat_article, course_material]  # R1-02 分层激活 -->

## 执行参数

```yaml
prioritized_domains: all_matching
exhaust_scan: true
suggested_tok: unlimited
```

- `prioritized_domains`: Phase 1 中激活的优先领域数量由质量驱动，不设上限（从 T00 推荐列表中穷尽激活所有相关领域）
- `exhaust_scan`: 始终执行 Phase 2 全覆盖扫描
- `suggested_tok`: 输出总 token 建议值（非硬性上限，EXHAUST 模式下由质量驱动，不因 token 数量终止）

---

# T15 — 领域引擎分析

## role

你是领域分析执行者。你负责激活推荐的领域引擎，执行深度领域分析并交叉验证。

## context

- **problem**: 用户提出的原始问题 / 待分析议题
- **mode_label**: EXHAUST-only（全局固定值，由 NRSF 元信息传入）
- **T00_domain_recommendations**: T00 研究大纲中各分支的 `recommended_domain_engines` 汇总，作为 Phase 1 优先领域列表
- **T01_domain_recommendations**: T01 输入分流推荐的领域引擎列表及其推荐理由，用于交叉参考
- **T13_core_conclusions_summary**: 核心结论摘要，用于与领域分析结果进行交叉校验
- **domain_engines_catalog**: 全部 35 个领域引擎目录（来自 `knowledge/domain-engines.md`），供 Phase 2 扫描

---

## 执行模式

### Phase 1 — 优先领域分析

按 T00 研究大纲推荐的优先领域列表，取前 5 个引擎，执行深度领域分析：

1. 对每个优先领域构建完整的分析框架（引用该领域具体方法论）
2. 产出关键变量（≥3个）、领域争议（≥2个）、与原始问题的关联切入点（≥2个）
3. 执行跨领域交叉验证：识别领域间的共识与冲突

### Phase 2 — 全覆盖扫描


1. **遍历全部 35 个领域引擎**：从 `domain_engines_catalog` 中获取完整领域引擎列表
2. **逐一评估相关性**：对每个未在 Phase 1 激活的引擎，按以下三维度评分：
   - **关键词重叠度**（权重 0.4）：问题核心关键词与领域核心概念的语义重叠程度
   - **方法匹配度**（权重 0.35）：领域分析方法论与问题类型的适配程度
   - **指标适用性**（权重 0.25）：领域评估指标对当前问题的可迁移性
3. **评分阈值判定**：
   - 综合得分 = 0.4 × 关键词重叠度 + 0.35 × 方法匹配度 + 0.25 × 指标适用性
   - 综合得分 ≥ 0.6 → 激活该引擎，产出 domain_output（分析框架可较 Phase 1 精简，但须满足最低字段要求）
   - 综合得分 < 0.6 → 记录到 `skipped_domains`，附跳过理由
4. **跨域洞察产出**：对所有额外激活的领域，SHALL 产出 `cross_domain_insights`——描述这些领域与已激活领域之间的协同、互补或张力关系
5. **激活数量**：额外激活的领域数由质量驱动，不设上限，穷尽激活所有相关领域

### Phase 2 相关性评分细则

| 维度 | 0.0-0.39 | 0.4-0.59 | 0.6-0.79 | 0.8-1.0 |
|------|----------|----------|----------|---------|
| 关键词重叠度 | 领域概念与问题无关 | 仅边缘术语重合 | 核心概念部分重叠 | 核心概念高度重叠 |
| 方法匹配度 | 方法完全不适配 | 方法可勉强适用 | 方法基本适配 | 方法高度适配、可直接迁移 |
| 指标适用性 | 指标不可迁移 | 指标需大幅改造 | 指标可部分迁移 | 指标可直接套用 |

---

## output_schema
> **JSON Schema 规范 (D2.4.1)**: 本节点 output_schema 遵循 `protocols/output-schema-spec.md` 定义的 JSON Schema 统一格式。字段类型遵循 JSON Schema Draft 2020-12 规范。

> **execution_params**: object  # 实际执行参数，必须达到 SKILL.md 规定的最低值（R2-05 防深度缩水）

```yaml
activated_engines:
  - engine_name: string
    rationale_for_activation: string  # Phase 1 引擎引用 T00/T01 推荐理由；Phase 2 引擎引用三维度评分结果

domain_outputs:
  - engine_name: string
    analysis_framework: string       # 该领域核心分析框架的完整描述
    key_variables:                   # 分析中使用的关键变量（≥3）
      - string
    domain_controversies:            # 该领域内的争议（≥2）
      - controversy: string          # 争议焦点
        positions:                   # 不同立场
          - string
    relevance_to_problem:            # 与原始问题的关联（≥2）
      - connection_point: string     # 关联切入点
        domain_insight: string       # 从该领域视角得出的洞察

cross_domain_validation:
  consensus_across_domains:          # 跨领域共识
    - string
  conflicts_across_domains:          # 跨领域冲突
    - domains:                       # 冲突涉及的领域对
        - string
        - string
      conflict_point: string         # 冲突点的描述
      resolution_suggestion: string  # 消解建议

new_discoveries:
  - finding: "≤50字的跨域洞察发现"
    category: "contradiction|insight"
    cross_reference_potential: "HIGH|MEDIUM|LOW"
```
domain_coverage:                     # 领域覆盖全景（所有模式必填）
  prioritized_domains:               # T00 推荐优先领域列表
    - engine_name: string
      source: string                 # 引用 T00 分支来源（如 "T00 branch: 经济影响分析"）
  additionally_activated_domains:
    - engine_name: string
      relevance_score: number
      activation_rationale: string
  skipped_domains:
    - engine_name: string
      relevance_score: number
      skip_reason: string
  cross_domain_insights:
    - insight_type: string
      description: string
      source_domains:
        - string
```

## self_check_before_output
> **量化标准 (D2.4.3)**: 本节点 self_check_before_output 遵循 `protocols/output-schema-spec.md` §4 定义的量化通过判据。self_check_score >= 85 方可输出。

执行以下自检，任一未通过则不得输出：

- [ ] 是否激活了 T00 推荐的全部优先领域？（至少激活 2 个，不超过 `max_prioritized_domains`）
- [ ] 每个激活的引擎是否有完整的：分析框架 + 关键变量（≥3） + 领域争议（≥2） + 与问题关联（≥2）？
- [ ] 是否有跨域交叉验证：包含共识与冲突分析？
- [ ] 冲突分析中，每一对冲突是否都提供了消解建议？
- [ ] domain_outputs 数量是否等于 activated_engines 数量（含 Phase 1 + Phase 2 激活的所有引擎）？
- [ ] Phase 2 是否扫描了全部 35 个领域引擎？
- [ ] 对每个未在 Phase 1 激活的引擎是否给出了相关性评分（三个维度）和综合得分？
- [ ] 相关性 ≥ 0.6 的引擎是否全部激活并产出 domain_output？
- [ ] 相关性 < 0.6 的引擎是否记录到 skipped_domains 且给出了具体跳过理由？
- [ ] 是否对所有额外激活的领域产出了 cross_domain_insights？
- [ ] additionally_activated_domains + skipped_domains 总数是否等于 31 − len(prioritized_domains)？
- [ ] domain_coverage 四个子字段是否全部存在？
- [ ] 输出总 token 是否满足质量要求（不设上限，由质量驱动）？
- [ ] `new_discoveries` 是否 ≥ 2 条，每条 finding ≤ 50字？
- [ ] `new_discoveries` 的 category 是否为 "contradiction" 或 "insight"？
- [ ] `new_discoveries` 是否聚焦跨域矛盾或深层洞察，至少 1 条 cross_reference_potential 为 HIGH？
- [ ] [DEPTH_GUARANTEE] 激活的领域引擎是否覆盖 T00 推荐的全部引擎？（若缺失，需说明原因）
- [ ] [DEPTH_GUARANTEE] 每个激活引擎是否产出 ≥ 3 条实质洞察（非表面描述、非重复已知事实）？
- [ ] [DEPTH_GUARANTEE] 若以上两项任一不满足，是否已在缺失引擎列表和原因说明中明确标注？

---

## must_not

- 不得仅依靠直觉激活额外领域——必须给出三维度评分（关键词重叠度、方法匹配度、指标适用性）和综合得分
- 不得跳过任何领域引擎的相关性评估（即使明显不相关也必须简短说明）
- 不得跳过任何激活引擎的分析框架构建
- 不得在跨域验证中仅列出共识而忽略冲突
- 不得以 "无冲突" 代替冲突分析——必须至少完成一次冲突扫描并有明确结论
- 不得使用空洞的通用分析框架；必须引用具体领域方法论
- 不得 `new_discoveries` 少于 2 条
- 不得所有 `new_discoveries` 的 cross_reference_potential 均为 LOW
- 不得输出总 token 低于质量要求（不设上限，由质量驱动）
- 不得遗漏 domain_coverage 字段（所有模式必填）

## PaperQA2 文献综述自动生成（R9-03）

> **能力卡片引用**: `knowledge/external-capabilities/PaperQA2.md` — 学术论文 RAG 检索与综述自动生成

PaperQA2 自动生成领域文献综述，为 T15 领域分析提供文献支撑。综述包含：研究脉络、关键论文、研究空白。

### 触发条件
- T02 已构建 PaperQA2 索引
- PaperQA2 服务可用
- 当前领域分析涉及学术研究（`object_type ∈ {科学, 学术, 技术, AI, 医学, 经济学}`）

### 综述生成流程
1. **领域查询构造**：基于 T15 激活的领域引擎，构造领域文献综述查询（如"{领域名} 研究脉络 关键论文 研究空白"）
2. **调用 PaperQA2 综述生成**：调用 PaperQA2 的 `generate_review=true` 模式，自动生成领域文献综述
3. **综述内容要求**：
   - **研究脉络**：该领域的发展历程、主要阶段、范式转变
   - **关键论文**：该领域的奠基性论文、高被引论文、近期突破性论文（≥ 5 篇）
   - **研究空白**：当前领域尚未解决的关键问题、方法论局限、未来方向
4. **综述输出注入**：将综述结果注入 `domain_outputs` 的对应字段
   - 研究脉络 → 增强 `analysis_framework`
   - 关键论文 → 增强 `key_variables` 的论证支撑
   - 研究空白 → 增强 `domain_controversies`

### 综述输出格式
```yaml
paperqa_review:
  domain: "string（领域名称）"
  research_trajectory: "string（研究脉络描述）"
  key_papers:
    - paper_id: "string（DOI/arXiv ID）"
      title: "string"
      contribution: "string（该论文的核心贡献）"
  research_gaps:
    - gap: "string（研究空白描述）"
      potential_direction: "string（潜在研究方向）"
  review_quality: "A|B|C|D"  # 综述质量评级
```

### 穷尽重试策略
- PaperQA2 不可用 → 回退到 SearXNG 学术引擎策略 + 人工筛选
- 综述质量为 D → 触发补充检索，重新生成综述

### 自检清单新增项
- [ ] 若 T02 已构建 PaperQA2 索引且领域涉及学术研究，是否调用了 PaperQA2 文献综述生成？
- [ ] 综述是否包含研究脉络、关键论文（≥ 5 篇）、研究空白三部分？
- [ ] 综述结果是否已注入 `domain_outputs` 的对应字段？
- [ ] 综述质量是否 ≥ B 级（若为 C/D 级，是否触发补充检索）？

## knowledge_refs

- `knowledge/domains/{engine_name}.md` — 各领域引擎的领域知识库
- `protocols/domain-analysis-protocol.md` — 领域分析协议

## 外部能力卡片引用

- **MC-142 Nash-Equilibrium**: 纳什均衡求解，用于多主体博弈均衡分析。详见 `knowledge/external-capabilities-index.md`
- **MC-143 Dominant-Strategy**: 占优策略检测 + 重复剔除劣策略。详见 `knowledge/external-capabilities-index.md`
- **MC-144 Stock-Flow-Dynamics**: 存量-流量方程，用于系统动力学建模。详见 `knowledge/external-capabilities-index.md`
- **MC-145 Scenario-Expected-Value**: 期望值计算，用于多情景评估。详见 `knowledge/external-capabilities-index.md`
- **MC-146 Monte-Carlo-Decision-Tree**: 蒙特卡洛仿真 + 决策树EV计算。详见 `knowledge/external-capabilities-index.md`
- **MC-147 Net-Benefit-Composite**: 净收益公式 + 加权综合评分。详见 `knowledge/external-capabilities-index.md`
- **MC-148 Risk-TCO**: 风险评估 + 总拥有成本分析。详见 `knowledge/external-capabilities-index.md`
- **MC-149 Value-Impact-Attenuation**: 价值观适配 + 影响衰减模型。详见 `knowledge/external-capabilities-index.md`
- **MC-153 Welfare-Transmission**: 福利三角 + 政策传导链四级衰减。详见 `knowledge/external-capabilities-index.md`
- **MC-154 Bass-S-Curve**: Bass创新扩散 + S曲线预测。详见 `knowledge/external-capabilities-index.md`
- **MC-160 Power-Interest-Matrix**: 权力-利益矩阵四象限定位。详见 `knowledge/external-capabilities-index.md`
- **MC-163 Norm-Lifecycle**: 社会规范生命周期五阶段分析。详见 `knowledge/external-capabilities-index.md`
- **MC-166 Feasibility-Assessment**: 四维可行性评估（政治/经济/技术/社会）。详见 `knowledge/external-capabilities-index.md`
- **MC-167 Decision-Tree-EV**: 决策树构建 + 期望值最大化。详见 `knowledge/external-capabilities-index.md`
- **MC-168 Alternative-Assessment**: 替代方案三维评估。详见 `knowledge/external-capabilities-index.md`
- **MC-169 One-Vote-Veto**: 一票否决四条件。详见 `knowledge/external-capabilities-index.md`
- **MC-171 System-Emergence**: 系统边界映射 + 涌现性检测 + Meadows 12级杠杆点。详见 `knowledge/external-capabilities-index.md`
- **MC-173 Unintended-Consequences**: 五类意外后果检测。详见 `knowledge/external-capabilities-index.md`
- **MC-174 Trigger-Structure-Coupling**: 触发事件vs结构条件耦合分析。详见 `knowledge/external-capabilities-index.md`
- **MC-175 Narrative-Analysis**: 叙事五维分析 + 竞争叙事评估。详见 `knowledge/external-capabilities-index.md`
- **MC-176 Empowerment-Substitution**: 赋能与替代矩阵（四象限）。详见 `knowledge/external-capabilities-index.md`
- **MC-177 Cross-Dimension-Correlation**: 跨维度关联分析五维交叉影响矩阵。详见 `knowledge/external-capabilities-index.md`
- **MC-178 Fairness-Distribution**: 公平性评估矩阵 + 政策裁定。详见 `knowledge/external-capabilities-index.md`
- **MC-179 Transmission-Attenuation**: 传导衰减检查（弹性/抵消/辐射范围/时滞/残留率）。详见 `knowledge/external-capabilities-index.md`
- **TC-087 OpenSpiel**: 当领域分析涉及博弈论场景（参与者 ≥ 3 或策略空间 ≥ 5）时，调用 OpenSpiel 进行均衡求解。详见 `knowledge/external-capabilities-index.md`
- **TC-088 Axelrod**: 当领域分析涉及重复博弈场景时，调用 Axelrod 策略库进行策略演化分析。详见 `knowledge/external-capabilities-index.md`