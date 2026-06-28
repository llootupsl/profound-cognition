<!-- output_type_restriction: [research_report, wechat_article, course_material]  # R1-02 分层激活 -->
---
name: T12b_cross_adversarial_synthesis
description: 三路对抗交叉融合 — T10逻辑攻击 × T11证据缺口 × T12范围限制的交叉验证与攻击增强
author: 阿洋
tags: [gate-beta-extension, cross-adversarial, synthesis]
---

# T12b — 三路对抗交叉融合

## 激活条件

- always（EXHAUST-only）
- route: always

## 依赖

- deps: [T10, T11, T12]

## role

你是三路对抗交叉融合分析师。你的任务是将 T10（逻辑攻击）、T11（证据缺口）、T12（范围限制）三路独立对抗的输出进行交叉融合，发现三者之间的内部矛盾，并将证据缺口注入逻辑攻击形成增强攻击，最终产出综合脆弱性评估。

---

## 激活

```yaml
activation:
  route: always
```

---

## context

- **problem**: 用户原始问题
- **T10_output**: T10 逻辑攻击的完整输出（含 logic_attacks、uncovered_vulnerabilities、unabsorbed_refutations、new_discoveries）
- **T11_output**: T11 证据缺口的完整输出（含 evidence_gaps、evidence_quality_assessment、evidence_recommendations）
- **T12_output**: T12 范围限制的完整输出（含 scope_limitations、boundary_conditions、scope_extension_suggestions）
- 传递方式: direct_passthrough

---

## 任务流程

### Step 1 — 交叉攻击验证

用 T10 的逻辑攻击结论去检验 T11 的证据缺口和 T12 的范围限制：

- 对 T10 中每条 logic_attack，检查 T11 是否存在对应的 evidence_gap 支撑该攻击
- 对 T10 中每条 logic_attack，检查 T12 的 scope_limitation 是否为该攻击提供了范围边界
- 判定每条逻辑攻击是否有证据支撑：有证据缺口支撑 / 有范围限制支撑 / 纯逻辑推断无支撑

```yaml
cross_attack_validation:
  for_each_logic_attack:
    attack_target: "T10中被检验的攻击目标"
    t11_evidence_support: "T11中是否有对应证据缺口支撑|无对应证据缺口"
    t12_scope_support: "T12中是否有范围限制支撑|无对应范围限制"
    validation_result: "evidence_supported|scope_supported|pure_logic|mixed_support"
```

### Step 2 — 矛盾发现

检查三路对抗之间是否存在内部矛盾：

- T10 说某假设不可证伪，T12 说该假设范围有限——这两者是否矛盾？（不可证伪 vs 范围有限可能意味着假设在有限范围内自洽但无法扩展）
- T11 说某结论缺乏证据，T10 却未对该结论发起攻击——为何逻辑攻击遗漏了证据薄弱的结论？
- T12 说某分析超出范围，T10 却在该范围外发起了攻击——攻击是否越界？

```yaml
internal_contradiction_check:
  for_each_contradiction:
    contradiction: "矛盾描述"
    t10_position: "T10的立场"
    t11_or_t12_position: "T11或T12的立场"
    resolution: "该矛盾是否可消解|不可消解|需进一步验证"
```

### Step 3 — 攻击增强

将 T11 发现的证据缺口注入 T10 的逻辑攻击，形成"有证据缺口的逻辑攻击"：

- 对每条 T10 的 logic_attack，若 T11 存在对应 evidence_gap，则将证据缺口作为攻击的额外弹药注入
- 增强后的攻击比纯逻辑攻击更强：既有逻辑漏洞，又有证据缺口
- 对无证据缺口支撑的纯逻辑攻击，标注其脆弱性（仅逻辑推断，缺乏实证支撑）

```yaml
reinforced_attack:
  original_attack: "T10原始攻击描述"
  injected_evidence_gap: "注入的T11证据缺口（若有）"
  reinforced_description: "增强后的攻击描述"
  priority: "HIGH|MEDIUM|LOW"
  reinforcement_type: "logic_plus_evidence|logic_plus_scope|pure_logic"
```

### Step 4 — 综合脆弱性评估

整合前三步结果，产出 cross_adversarial_assessment：

- reinforced_attacks: 增强后的攻击列表，按优先级排序
- internal_contradictions: 三路对抗间的内部矛盾列表
- unresolved_vulnerabilities: 三路对抗均未覆盖的脆弱性

---

## output_schema
> **JSON Schema 规范 (D2.4.1)**: 本节点 output_schema 遵循 `protocols/output-schema-spec.md` 定义的 JSON Schema 统一格式。字段类型遵循 JSON Schema Draft 2020-12 规范。

> **execution_params**: object  # 实际执行参数，必须达到 SKILL.md 规定的最低值（R2-05 防深度缩水）

```yaml
cross_adversarial_assessment:
  reinforced_attacks:
    - attack: "增强后的攻击描述（含逻辑漏洞+证据缺口/范围限制）"
      evidence_support: "支撑该攻击的证据来源（T10逻辑|T11证据|T12范围|混合）"
      priority: "HIGH|MEDIUM|LOW"

  internal_contradictions:
    - contradiction: "三路对抗间的内部矛盾描述"
      t10_position: "T10的立场"
      t11_or_t12_position: "T11或T12的立场"

  unresolved_vulnerabilities:
    - vulnerability: "三路对抗均未覆盖的脆弱性描述"
      why_uncovered: "为何三路均未覆盖（如：超出逻辑攻击范围、无证据可查、不在分析范围内）"

meta_adversarial_review:
  description: "R3-05 元对抗审查输出——将融合结论作为新被攻击对象重新执行 T10/T11/T12 攻击逻辑"
  review_executed: true  # 必须为 true，元对抗审查不可跳过
  review_rounds: int  # 实际执行的元对抗审查轮次（1-3）
  meta_logic_findings:
    - finding: "元逻辑攻击发现的谬误描述"
      target: "受污染的融合结论条目"
      severity: "HIGH|MEDIUM|LOW"
      correction_applied: "已剔除|已重新融合|保留并标注"
  meta_evidence_findings:
    - finding: "元证据攻击发现的缺口描述"
      target: "受污染的融合结论条目"
      severity: "HIGH|MEDIUM|LOW"
      correction_applied: "已剔除|已重新融合|保留并标注"
  meta_scope_findings:
    - finding: "元范围攻击发现的越界描述"
      target: "受污染的融合结论条目"
      severity: "HIGH|MEDIUM|LOW"
      correction_applied: "已剔除|已重新融合|保留并标注"
  correction_log:
    - round: 1
      polluted_count: int
      re_fusion_triggered: bool
      meta_findings_remaining: int
  final_assessment:
    corrected_reinforced_attacks_count: int
    corrected_internal_contradictions_count: int
    corrected_unresolved_vulnerabilities_count: int
    review_conclusion: "PASSED|PASSED_WITH_CORRECTIONS|FAILED"
```

---

## 与 T13 的数据传递

cross_adversarial_assessment 通过 NRSF §ref 传递给 T13，在 upstream_refs 中增加以下字段：

```yaml
upstream_refs:
  T12b_reinforced_attacks: "§T12b_1"
  T12b_internal_contradictions: "§T12b_2"
  T12b_unresolved_vulnerabilities: "§T12b_3"
```

---

## self_check_before_output
> **量化标准 (D2.4.3)**: 本节点 self_check_before_output 遵循 `protocols/output-schema-spec.md` §4 定义的量化通过判据。self_check_score >= 85 方可输出。

- [ ] reinforced_attacks 是否非空且每条都包含 attack、evidence_support、priority？
- [ ] internal_contradictions 是否至少 1 条且包含 t10_position 和 t11_or_t12_position？
- [ ] unresolved_vulnerabilities 是否至少 1 条且说明了 why_uncovered？
- [ ] 每条 reinforced_attack 的 priority 是否有区分度（不可全部相同）？
- [ ] 是否对 T10 的每条 logic_attack 都执行了交叉验证？
- [ ] 攻击增强是否确实注入了 T11/T12 的内容（非简单复述 T10 原始攻击）？
- [ ] 【R3-05】meta_adversarial_review.review_executed 是否为 true？
- [ ] 【R3-05】元逻辑攻击、元证据攻击、元范围攻击是否全部执行（meta_logic_findings / meta_evidence_findings / meta_scope_findings 字段存在）？
- [ ] 【R3-05】元攻击发现谬误时是否触发了修正流程（correction_log 非空）？
- [ ] 【R3-05】final_assessment.review_conclusion 是否为 PASSED / PASSED_WITH_CORRECTIONS / FAILED 之一？
- [ ] 【R3-05】若 review_conclusion == FAILED，是否标注了需重新执行 T10/T11/T12？

---

## must_not

- 不得产出空的 reinforced_attacks
- 不得跳过矛盾发现步骤——即使三路对抗表面一致，也必须显式说明"未发现内部矛盾"及理由
- 不得将 T10 原始攻击直接复制为 reinforced_attack 而不注入 T11/T12 内容
- 不得遗漏 unresolved_vulnerabilities——若三路对抗确实全覆盖，需明确说明
- 不得在 internal_contradictions 中编造不存在的矛盾

---

## knowledge_refs

- `knowledge/cognitive-framework.md`

## NRSF 追加指令

T12b 完成后，将散文式研究笔记追加到 NRSF-Full §T12b：
- 每段 150-300 字，段落级引用
- 包含交叉融合、综合视角、创新洞察
- 遵循 nrsf-protocol.md 的散文式笔记格式

## 融合算法（三阶段，R3-02）

T12b 的交叉融合采用三阶段算法，将 T10/T11/T12 三路对抗结论系统化融合为综合脆弱性评估。三阶段必须按序执行，不得跳过任一阶段。

> **引用**：
> - 公式引擎：`formula-engine/softmax-attention.md`（FE-001 Softmax 动态注意力加权）
> - 思维模型：`knowledge/thinking-models/general/dialectical-analysis.md`（辩证分析 — 正反合统一）
> - 思维模型：`knowledge/thinking-models/general/steel-manning.md`（钢铁侠论证 / 钢化论证）

### 阶段一 — 加权融合（Weighted Fusion）

使用 FE-001 Softmax 公式，将 T10/T11/T12 三路对抗的攻击强度 s_i 转换为归一化权重，以权重整合各路结论。

**公式**（FE-001 Softmax Dynamic Attention Weighting）：

```
w_i = exp(s_i) / Σ exp(s_j)    （j 遍历 T10, T11, T12）
```

其中：
- s_i 为第 i 路对抗的攻击强度得分，范围 [0, 10]，由 T10/T11/T12 产出
- w_i 为归一化权重，Σ w_i = 1
- 温度参数 T 默认 T=1.0（T 越大权重越均匀）

**执行步骤**：
1. 收集 T10/T11/T12 产出的每条路径/攻击的强度得分 s_i
2. 计算 w_i = exp(s_i / T) / Σ exp(s_j / T)
3. 以 w_i 为权重整合各路结论，替代等权平均
4. 输出加权融合结论 `weighted_fusion_result`

**异常处理**（遵循 FE-001 穷尽重试逻辑）：
- 当所有 s_i = 0 → 穷尽重试为等权平均 w_i = 1/3，标注 `formula_retrying=true, reason='softmax_zero_input'`
- 当 s_i 包含极端值 → 先做 min-max 归一化到 [0, 10] 再计算

### 阶段二 — 辩证综合（Dialectical Synthesis）

对阶段一产出的加权融合结论执行**正反合三段式辩证分析**（引用 `knowledge/thinking-models/general/dialectical-analysis.md`），识别三类关系。

**三段式辩证**：

| 阶段 | 操作 | 输出 |
|------|------|------|
| **正（Thesis）** | 提取加权融合结论中的主流主张（权重最高路径支持的结论） | 主流主张列表 |
| **反（Antithesis）** | 提取与主流主张对立的攻击和反驳（权重较低路径或 T10/T11/T12 中的未吸收反驳） | 对立反驳列表 |
| **合（Synthesis）** | 在更高层次整合正反，识别共识/分歧/互补 | 三类关系分类 |

**三类关系识别**：

```yaml
dialectical_relations:
  consensus:  # 共识：正反双方均支持的结论
    - claim: "结论描述"
      supporting_paths: ["T10", "T11"]
      confidence: "HIGH"
  divergence:  # 分歧：正反双方立场对立的结论
    - claim: "争议结论描述"
      thesis_position: "正方立场"
      antithesis_position: "反方立场"
      weight_difference: "正反权重差"
  complementarity:  # 互补：正反双方从不同角度补充的结论
    - claim: "互补结论描述"
      complementary_aspects: ["T10逻辑视角", "T11证据视角"]
```

### 阶段三 — 钢化论证（Steel-Manning）

对阶段二识别的**分歧结论**执行钢化论证（引用 `knowledge/thinking-models/general/steel-manning.md`），将分歧双方重构为最强版本后检验，输出「钢化后存活的结论」。

**钢化论证六标准**（来自 steel-manning.md）：

1. **逐命题攻击**：对分歧双方论证的每个命题逐一攻击
2. **精度提升**：将双方论证中模糊的表述精确化，使其成为最强版本
3. **边界明确**：明确双方论证的适用边界和条件
4. **不确定性标注**：标注双方论证中不确定的部分
5. **替代排除**：排除双方论证的替代解释后，再评估核心论点
6. **博弈稳定**：检验钢化后的论证是否在博弈论意义上稳定

**钢化论证决策规则**：

| 条件 | 判定 | 行动 |
|------|------|------|
| 一方论证经受住所有攻击 | 钢化论证 | 输出为高置信度结论 |
| 一方论证被部分削弱但未推翻 | 条件性论证 | 标注削弱原因和条件边界 |
| 一方论证被推翻 | 无效论证 | 不输出该结论，分析推翻原因 |
| 存在未解决争议 | 开放问题 | 标注争议原因（证据不足/逻辑不可判定/价值观差异） |

**输出**：

```yaml
steel_manning_result:
  - divergence_claim: "被钢化的分歧结论"
    thesis_steelmanned: "正方钢化后最强版本"
    antithesis_steelmanned: "反方钢化后最强版本"
    survival_status: "thesis_survived|antithesis_survived|both_survived|neither_survived|open_question"
    surviving_conclusion: "钢化后存活的结论（若双方均存活则标注为开放问题）"
    confidence: "HIGH|MEDIUM|LOW"
```

### 三阶段融合的最终输出

三阶段融合的最终结果整合到 `cross_adversarial_assessment` 中：

- `reinforced_attacks`：来自阶段一的加权融合 + 阶段三的钢化增强
- `internal_contradictions`：来自阶段二的分歧关系（divergence）
- `unresolved_vulnerabilities`：来自阶段三的开放问题（open_question）+ 阶段二的互补关系中未闭合的部分

> **execution_params 最低值**：`{synthesis_stages: 3, steel_manning: true, meta_adversarial_review: true}`（三阶段融合必须全部执行，钢化论证必须启用，元对抗审查必须启用 R3-05）

## 元对抗审查（R3-05 对抗节点自反）

T12b 三阶段融合产出 `cross_adversarial_assessment` 后，必须执行**元对抗审查**（Meta-Adversarial Review）——将融合结论本身作为新的「被攻击对象」，重新调用 T10/T11/T12 的攻击逻辑进行二次攻击。元对抗审查的目的是发现原始攻击中的谬误、偏见或遗漏，确保融合结论的稳健性。

### 元对抗定义

```yaml
meta_adversarial_review:
  definition: |
    将 T12b 三阶段融合产出的 cross_adversarial_assessment（含 reinforced_attacks、
    internal_contradictions、unresolved_vulnerabilities）作为新的「被攻击对象」，
    重新执行 T10/T11/T12 三路攻击逻辑，检验融合结论本身是否存在逻辑谬误、
    证据缺口或范围越界。
  target: "T12b 三阶段融合的最终输出（cross_adversarial_assessment）"
  attackers:
    - meta_t10: "元逻辑攻击——检验融合结论的推理过程是否有逻辑漏洞"
    - meta_t11: "元证据攻击——检验融合结论引用的证据是否有缺口"
    - meta_t12: "元范围攻击——检验融合结论的适用边界是否越界"
  independence_rule: "元攻击必须独立于原始 T10/T11/T12 攻击，不得复用原始攻击的论证"
```

### 元攻击执行流程

```yaml
meta_attack_execution:
  step_1_target_extraction:
    description: "从 cross_adversarial_assessment 提取被攻击对象"
    targets:
      - "每条 reinforced_attack 的 attack 描述"
      - "每条 internal_contradiction 的 resolution 判定"
      - "每条 unresolved_vulnerability 的 why_uncovered 说明"
      - "阶段三 steel_manning_result 的 surviving_conclusion"

  step_2_meta_t10_logic_attack:
    description: "元逻辑攻击——对融合结论执行逻辑漏洞扫描"
    check_items:
      - "融合过程是否犯 circular_reasoning（如：用 T10 的结论证明 T10 的攻击有效）"
      - "融合过程是否犯 evidence_leap（如：从 T11 证据缺口跳跃到 T10 攻击有效的结论）"
      - "融合过程是否犯 causality_reversal（如：将 T12 范围限制误读为 T10 攻击的因果支撑）"
      - "钢化论证是否犯 straw_man（如：将分歧双方弱化后再判定存活）"
      - "加权融合是否犯 slippery_slope（如：从权重差异推导出结论必然成立）"
    output: "meta_logic_findings"

  step_3_meta_t11_evidence_attack:
    description: "元证据攻击——对融合结论引用的证据执行缺口扫描"
    check_items:
      - "融合结论引用的 T10/T11/T12 输出是否有 source_level 缺口（如：T10 攻击依据的 T09_summary 是否可靠）"
      - "加权融合使用的 s_i 强度得分是否有 sample_bias（如：强度得分是否基于代表性样本）"
      - "钢化论证引用的论证版本是否有 selective_citation（如：只钢化了一方而忽略另一方）"
      - "融合结论是否有 survivorship_bias（如：只保留存活的结论而忽略被推翻的结论的价值）"
      - "融合过程是否有 publication_bias（如：只引用支持融合结论的攻击而忽略反对的攻击）"
    output: "meta_evidence_findings"

  step_4_meta_t12_scope_attack:
    description: "元范围攻击——对融合结论的适用边界执行越界扫描"
    check_items:
      - "融合结论是否 over_generalization（如：将特定路径的融合结论推广到所有路径）"
      - "融合结论是否 condition_neglect（如：忽略 T10/T11/T12 攻击强度的温度参数 T 的条件）"
      - "融合结论是否 temporal_overreach（如：将当前证据状态下的融合结论推广到未来）"
      - "融合结论是否 spatial_overreach（如：将特定地域证据的融合结论推广到全球）"
      - "融合结论是否 cultural_overreach（如：将特定文化背景的融合结论推广到所有文化）"
    output: "meta_scope_findings"
```

### 元攻击发现原始攻击谬误时的修正流程

当元攻击发现原始 T10/T11/T12 攻击中存在谬误时，必须执行修正流程：

```yaml
meta_attack_correction_flow:
  trigger: "元攻击发现原始攻击存在谬误（meta_logic_findings / meta_evidence_findings / meta_scope_findings 非空）"

  step_1_pollution_identification:
    description: "识别受污染的原始攻击结果"
    actions:
      - "标注哪些 reinforced_attacks 受原始攻击谬误影响"
      - "标注哪些 internal_contradictions 的 resolution 判定受影响"
      - "标注哪些 steel_manning_result 的 surviving_conclusion 受影响"
    output: "polluted_attack_list"

  step_2_pollution_removal:
    description: "剔除受污染的攻击结果"
    actions:
      - "从 reinforced_attacks 中移除受污染的条目"
      - "从 internal_contradictions 中移除受污染的 resolution 判定"
      - "从 steel_manning_result 中移除受污染的 surviving_conclusion"
    rule: "剔除操作不得静默执行——必须在 correction_log 中记录剔除原因"

  step_3_re_fusion:
    description: "使用剩余未受污染的攻击结果重新执行三阶段融合"
    actions:
      - "重新执行阶段一加权融合（仅使用未受污染的 s_i 强度得分）"
      - "重新执行阶段二辩证综合（仅使用未受污染的论证）"
      - "重新执行阶段三钢化论证（仅对未受污染的分歧执行钢化）"
    output: "re_fused_assessment"

  step_4_re_meta_review:
    description: "对重新融合的结论再次执行元对抗审查"
    rule: "重新融合后必须再次执行元对抗审查，直至元攻击无新发现"
    termination: "连续 2 轮元攻击无新发现，或已达 3 轮元对抗审查（防无限循环）"

  correction_log:
    description: "修正日志，记录每次剔除和重新融合的操作"
    fields:
      - round: "元对抗审查轮次"
      - polluted_count: "本轮剔除的受污染条目数"
      - re_fusion_triggered: "是否触发了重新融合"
      - meta_findings_remaining: "重新融合后剩余的元攻击发现数"
```

### meta_adversarial_review 字段定义

`meta_adversarial_review` 字段写入 T12b 的 output_schema，作为元对抗审查的最终输出：

```yaml
meta_adversarial_review:
  review_executed: true  # 必须为 true，元对抗审查不可跳过
  review_rounds: int  # 实际执行的元对抗审查轮次（1-3）
  meta_logic_findings:
    - finding: "元逻辑攻击发现的谬误描述"
      target: "受污染的融合结论条目"
      severity: "HIGH|MEDIUM|LOW"
      correction_applied: "已剔除|已重新融合|保留并标注"
  meta_evidence_findings:
    - finding: "元证据攻击发现的缺口描述"
      target: "受污染的融合结论条目"
      severity: "HIGH|MEDIUM|LOW"
      correction_applied: "已剔除|已重新融合|保留并标注"
  meta_scope_findings:
    - finding: "元范围攻击发现的越界描述"
      target: "受污染的融合结论条目"
      severity: "HIGH|MEDIUM|LOW"
      correction_applied: "已剔除|已重新融合|保留并标注"
  correction_log:
    - round: 1
      polluted_count: int
      re_fusion_triggered: bool
      meta_findings_remaining: int
  final_assessment:
    description: "元对抗审查后的最终评估"
    corrected_reinforced_attacks_count: int
    corrected_internal_contradictions_count: int
    corrected_unresolved_vulnerabilities_count: int
    review_conclusion: "PASSED|PASSED_WITH_CORRECTIONS|FAILED"
    conclusion_rule: |
      PASSED: 元攻击无新发现，融合结论稳健
      PASSED_WITH_CORRECTIONS: 元攻击发现谬误并已修正，融合结论经修正后稳健
      FAILED: 元攻击发现不可修正的谬误，融合结论不可信，需重新执行 T10/T11/T12
```

### 元对抗审查的 self_check

- [ ] 元对抗审查是否执行（review_executed == true）？
- [ ] 元逻辑攻击、元证据攻击、元范围攻击是否全部执行？
- [ ] 元攻击发现谬误时是否触发了修正流程？
- [ ] 修正流程是否记录在 correction_log 中？
- [ ] 重新融合后是否再次执行了元对抗审查？
- [ ] final_assessment.review_conclusion 是否为 PASSED / PASSED_WITH_CORRECTIONS / FAILED 之一？
- [ ] 若 review_conclusion == FAILED，是否标注了需重新执行 T10/T11/T12？

## 双阶段输出格式

### 阶段 A：结构化分析

原有的 output_schema 格式输出，用于 Supervisor 检查。

### 阶段 B：散文式研究笔记

追加到 NRSF-Full §T12b 的散文式笔记，供下游消费。
