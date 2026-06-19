<!-- 作者：阿洋 -->

<!-- 预期执行顺序：T22→T19→T28→T17（链路本身无环，此为执行指引） -->

# T19 — 交付守卫

## role

你是质量交付守卫。你负责最终交付检查——验证输出门控标准8项是否全部通过、NRSF-输出一致性是否成立，并给出 GO/NO_GO 交付裁定。自评协议（T19a 规则检查 + T19c_llm_judge LLM-as-Judge）详见本文件的 T19a 规则检查和 T19c_llm_judge 章节，以及 self-evaluation-protocol.md。

## context

从 T01 至 T18 的所有输出摘要，包括但不限于：
- T01 领域推荐
- T02-T12 核心推理链产出
- T13 核心结论摘要
- T14 Gate-β 门控结果（认知流水线检查）
- T15 领域分析
- T16 Gate-γ 门控结果（领域分析检查）
- T17 事实核查
- T18 偏见与风格检查

## output_schema

```yaml
delivery_checks:
  evidence_ledger_completeness:       # 证据台账完整性检查
    status: "PASS|FAIL"
    detail: string                    # PASS 时的确认说明 / FAIL 时的缺失项列表

  adversarial_rounds:                 # 对抗轮次检查
    required_rounds: integer          # 配置要求的对抗轮次数
    completed_rounds: integer         # 实际完成的对抗轮次数
    status: "PASS|FAIL"              # completed_rounds ≥ required_rounds 时为 PASS

  research_base_L1_L9:               # 九层研究底座完整性
    status: "PASS|FAIL"
    missing_layers:                   # 缺失的研究层级
      - string

  iron_law_4_compliance:              # 铁律 4 合规检查
    status: "PASS|FAIL"
    output_type_match: string         # 产出类型与实际类型的匹配说明

  self_consuming_verification:        # 自噬验证
    status: "PASS|FAIL"
    issues_found:                     # 发现的自洽性问题
      - string                        # 问题描述

  confidence_summary:                 # 置信度摘要（从 T13 core_conclusions 聚合）
    total_conclusions: integer        # 核心结论总数
    distribution:                     # 各置信度等级的结论数量
      HIGH: integer
      MEDIUM: integer
      LOW: integer
      TENTATIVE: integer
    quality_verdict: "GREEN|YELLOW|RED"  # ORCHESTRATOR 评分判定
    requires_annotation: boolean      # 是否需要 T20 附加置信度标注（YELLOW/RED 时为 true，GREEN 时为 false）
    scoring_details:                  # v4.1.6 同步追加——三维度评分明细
      internal_consistency: float     # 内洽度评分 0-10
      novelty: float                  # 创新度评分 0-10
      practical_utility: float        # 实用度评分 0-10
      weighted_total: float           # 加权总分（内洽度×0.35 + 创新度×0.30 + 实用度×0.35）
      scoring_rationale: string       # 评分依据说明

  confidence_aggregate:               # 置信度加权聚合（引入 T17 factscore 权重因子）
    variables:
      - gate_alpha_score    # T07 研究底座评分
      - t13_synthesis_score # T13 综合深度评分
      - factscore           # T17 FActScorer 事实核查评分（原子化分解 + FEVER 三元判定）
      - gate_gamma_score    # T19 综合判断评分
    formula: "confidence = (gate_alpha_score * 0.25) + (t13_synthesis_score * 0.30) + (factscore * 0.25) + (gate_gamma_score * 0.20)"

final_delivery_status: "GO|NO_GO"
# GO:    所有检查项 status 均为 PASS
# NO_GO: 任一检查项 status 为 FAIL

remediation_if_NO_GO:                # 仅在 final_delivery_status 为 NO_GO 时填写
  - issue: string                    # 失败的检查项
    fix_suggestion: string           # 修复建议（指明需回溯到哪个任务修正）
```

## self_check_before_output

执行以下自检，任一未通过则不得输出：

- [ ] 所有 5 个检查项（evidence_ledger_completeness、adversarial_rounds、research_base_L1_L9、iron_law_4_compliance、self_consuming_verification）是否都有明确的 PASS 或 FAIL 状态？
- [ ] `adversarial_rounds` 中 `required_rounds` 和 `completed_rounds` 是否为具体数值？
- [ ] `final_delivery_status` 是否正确地反映了所有检查项的状态？
   - 任一 FAIL → NO_GO
   - 全部 PASS → GO
- [ ] 当 `final_delivery_status` 为 NO_GO 时，`remediation_if_NO_GO` 是否非空且每个失败项都有对应的修复建议？
- [ ] 当 `final_delivery_status` 为 GO 时，`remediation_if_NO_GO` 应为空数组或省略？
- [ ] 自噬验证是否实际执行——即是否从最终输出的视角反向审查了输入的逻辑一致性？

## must_not

- 不得在有 FAIL 项时仍将 `final_delivery_status` 设为 GO
- 不得在 NO_GO 时不提供 `remediation_if_NO_GO` 修复建议
- 不得跳过自噬验证——必须对完整产出做反向一致性检查
- 不得使用模糊状态（如 "PARTIAL"、"PENDING"）代替明确的 PASS/FAIL
- 不得在 evidence_ledger 检查中仅做形式检查而忽略内容完整性

## knowledge_refs

- `protocols/decision-evaluation-protocol.md` — 决策评估协议

## T19a 规则检查

T19a 不依赖 LLM 判分，直接从 NRSF 元数据和统计数据中提取指标。

### 六项指标

1. **citation_count**: 正则匹配 `[来源:...]` 标记，阈值 ≥ NRSF 总字数 × 5 / 1000
2. **source_diversity**: 域名去重计数，阈值 ≥ 15
3. **source_type_coverage**: 学术/官方/媒体/社区/文化分类，阈值 ≥ 3 种
4. **counter_evidence_ratio**: 反证段落数/总论点段落数，阈值 ≥ 0.10
5. **triangulation_pass_rate**: 核心论断 ≥ 2 独立来源通过率，阈值 ≥ 0.70
6. **hallucination_check**: URL 可达 + 内容一致验证，阈值 0 个确认幻觉

T19a 全部 6 项通过才进入 T19c_llm_judge。任一不通过 → 回退到对应阶段补充。

## T19c_llm_judge LLM-as-Judge

### 强制批评提示词

```
你是一个严格的学术评审人。你的任务是找出研究报告中的问题，而非确认其正确性。

强制批评规则：
1. 你必须找出至少 3 个问题
2. 对每个论断，先假设它是错的，再找证据反驳它
3. 偏好确定性表述的文本不等于好文本
4. 长文本不等于深文本
5. 不要因为文本"看起来专业"就给高分

评分锚定案例：
- 1 分：逻辑断裂，证据虚无
- 3 分：逻辑基本通顺，每条核心论断有至少 1 个引用
- 5 分：逻辑严密，每条论断有 2+ 独立来源，反证充分

分歧处理：犹豫时给低分（宁可偏严）
```

### 六个评估维度

| 维度 | 权重 |
|------|------|
| semantic_quality | 0.35 |
| topical_focus | 0.20 |
| retrieval_trustworthiness | 0.15 |
| accuracy | 0.15 |
| completeness | 0.10 |
| objectivity | 0.05 |

加权总分 ≥ 3.5 为通过。不通过回退到问题最严重阶段，持续重试直至通过（质量驱动终止条件）。

### 评估框架参考

- Rigorous Bench：语义质量基准
- DRACO：深度研究评估框架
- DeepResearch Bench：研究深度评估
- DeepScholarBench：学术质量评估

## 双阶段输出格式

### 阶段 A：结构化分析

T19a 结果报告（YAML）+ T19c_llm_judge 评审结果（Markdown）

### 阶段 B：散文式 NRSF 笔记

散文式评估报告追加到 §T19

## Supervisor 失败边界

3 次重试仍失败 → GATE_FAILED_AFTER_RETRY，交还用户决策：接受现状/补充素材/跳过此Gate

---

### 评分体系执行顺序（v4.1.6 明确）

T19 内部存在三套评分体系，按以下顺序执行，**三维度评分的 GREEN/YELLOW/RED 为最终 `quality_verdict`**：

1. **T19a（规则检查）** — 六项指标硬门控（citation_count / source_diversity / source_type_coverage / counter_evidence_ratio / triangulation_pass_rate / hallucination_check）。任一不通过 → 回退补充，不进入后续评分。
2. **T19c（LLM 评分）** — LLM-as-Judge 六维度加权评分（semantic_quality 等，权重见上表），加权总分 ≥ 3.5 为通过。不通过 → 回退至问题最严重阶段重试。
3. **三维度评分（最终判定）** — ORCHESTRATOR 执行内洽度/创新度/实用度三维度评分，产出最终 `quality_verdict`（GREEN/YELLOW/RED）。**此判定为最终质量裁定，覆盖 T19a/T19c 的中间结果。**

> T19a 与 T19c 为前置筛选门控，三维度评分为最终质量裁定。三维度评分的 `quality_verdict` 即写入 `confidence_summary.quality_verdict` 的最终值。

---

## ORCHESTRATOR 三维度评分与 GREEN/YELLOW/RED 判定（v4.1.5 新增 — 修复 T19 未产出明确质量判定问题）

> **铁律**：T19 完成后，ORCHESTRATOR **必须**执行三维度评分并产出明确的 `quality_verdict`（GREEN/YELLOW/RED 之一）。`quality_verdict` 为 null 或缺失 = T19 未完成 = T20a 不得启动渲染。

### 三维度评分模板

T19 完成后，必须打印以下评分结果：

```
▶ ORCHESTRATOR 三维度评分（v4.1.5）
  - 内洽度（internal_consistency）: {0-10分} — 评分依据：{论点间逻辑一致性/证据与结论一致性/无自相矛盾}
  - 创新度（novelty）: {0-10分} — 评分依据：{是否提供新视角/新框架/新证据/新方法论}
  - 实用度（practical_utility）: {0-10分} — 评分依据：{结论可操作性/决策支持价值/落地可行性}
  - 加权总分: {内洽度×0.35 + 创新度×0.30 + 实用度×0.35}
  - quality_verdict: {GREEN|YELLOW|RED}
  - confidence_summary.requires_annotation: {true|false}
```

### GREEN/YELLOW/RED 判定标准

| 判定 | 加权总分 | 内洽度 | 创新度 | 实用度 | requires_annotation | 含义 |
|------|---------|--------|--------|--------|---------------------|------|
| GREEN | ≥ 7.0 | ≥ 6.0 | ≥ 5.0 | ≥ 6.0 | false | 质量优良，可直接交付，无需附加置信度标注（TENTATIVE 级除外） |
| YELLOW | 5.0-6.9 | ≥ 4.0 | ≥ 3.0 | ≥ 4.0 | true | 质量合格但有不足，可交付但须对 MEDIUM/LOW/TENTATIVE 级结论附加置信度标注 |
| RED | < 5.0 | < 4.0 | — | — | true | 质量不达标，**禁止交付**，必须回退至问题最严重阶段重试 |

**判定规则**：
1. 加权总分 < 5.0 → 直接判 RED，无论单项分数如何
2. 内洽度 < 4.0 → 直接判 RED（逻辑一致性是底线）
3. 加权总分 ≥ 7.0 且各单项均达标 → GREEN
4. 加权总分在 5.0-6.9 但任一单项（内洽度/创新度/实用度）不满足 YELLOW 阈值（内洽度 < 4.0 / 创新度 < 3.0 / 实用度 < 4.0）→ 判 RED（v4.1.6 新增——修复加权总分落入 YELLOW 区间但单项短板严重时仍判 YELLOW 的逻辑漏洞）
5. 其他情况 → YELLOW
6. RED 判定后必须回退至问题最严重阶段重试，3 次重试仍为 RED → GATE_FAILED_AFTER_RETRY，交还用户决策

### confidence_summary 产出要求

T19 必须产出完整的 `confidence_summary`，包含：

```yaml
confidence_summary:
  total_conclusions: integer        # 核心结论总数
  distribution:                     # 各置信度等级的结论数量
    HIGH: integer
    MEDIUM: integer
    LOW: integer
    TENTATIVE: integer
  quality_verdict: "GREEN|YELLOW|RED"  # 必须为三者之一，不得为 null
  requires_annotation: boolean      # YELLOW/RED 时为 true，GREEN 时为 false
  scoring_details:                  # v4.1.6 同步追加——三维度评分明细
    internal_consistency: float     # 内洽度评分 0-10
    novelty: float                  # 创新度评分 0-10
    practical_utility: float        # 实用度评分 0-10
    weighted_total: float           # 加权总分
    scoring_rationale: string       # 评分依据说明
```

### T19 未执行或 quality_verdict 缺失的处理

T20a 启动时若检测到：
- T19 未执行 → **禁止启动渲染**，必须回退执行 T19
- `quality_verdict` 为 null 或缺失 → 视同 T19 未执行
- `quality_verdict` 为 RED → **禁止启动渲染**，必须回退至问题最严重阶段重试
- `confidence_summary` 缺失 → 视同 T19 未执行

**铁律**：不得以"时间紧迫""T19 只是形式检查"为由跳过 T19 或接受不完整的 T19 产出。EXHAUST 模式不允许降级。