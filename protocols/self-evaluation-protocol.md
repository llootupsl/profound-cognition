<!-- 作者：阿洋 -->

# T19 交付守卫与质量判定协议 (T19 Quality Delivery & Judgment Protocol) v3.0

## 1. 概述

T19 自评拆分为 T19a（规则检查，不依赖 LLM）和 T19b（LLM-as-judge，强制批评提示词）两个子阶段。T19a 所有 6 项通过才进入 T19b。

**触发条件**：T17（事实核查）和 T18（格式审查）完成后自动触发。

## 2. T19a 规则检查

### 2.1 概述
T19a 不依赖 LLM 判分，直接从 NRSF 元数据和统计数据中提取指标。

### 2.2 六项指标详细定义

#### 指标 1：citation_count（引用数量）
- **method**：正则匹配 NRSF-Full 中的 `[来源:...]` 标记，统计总数
- **threshold**：≥ NRSF 总字数 × 5 / 1000（即每 1000 字至少 5 个引用）
- **pass**：count ≥ threshold
- **不通过穷尽尝试**：T05/T06（补充证据搜索）

#### 指标 2：source_diversity（来源多样性）
- **method**：提取所有引用的域名，去重计数
- **threshold**：≥ 15 个不同域名
- **pass**：unique_domains ≥ 15
- **不通过穷尽尝试**：T03/T04（扩展研究广度）

#### 指标 3：source_type_coverage（来源类型覆盖）
- **method**：统计引用来源类型：
  - 学术（arxiv.org, semanticscholar.org, scholar.google.com, doi.org, researchgate.net 等）
  - 官方（gov.cn, gov, org, europa.eu, who.int 等）
  - 媒体（news, reuters.com, bbc.com, nytimes.com 等）
  - 社区（reddit.com, stackoverflow.com, forum, zhihu.com 等）
  - 文化（文化类来源）
  计算覆盖类型数
- **threshold**：≥ 3 种类型
- **pass**：covered_types ≥ 3
- **不通过穷尽尝试**：T03/T04（扩展来源类型）

#### 指标 4：counter_evidence_ratio（反证比率）
- **method**：统计 NRSF 中标记为「反证」或「对立」的段落数 / 总论点段落数
- **threshold**：≥ 0.10（至少 10% 的论点段落包含反证）
- **pass**：ratio ≥ 0.10
- **不通过穷尽尝试**：T10/T11/T12（加强对抗分析）

#### 指标 5：triangulation_pass_rate（三角验证通过率）
- **method**：对每个核心论断，检查是否有 ≥ 2 个独立来源支持，统计通过率
- **threshold**：≥ 0.70（70% 以上的核心论断有三角验证）
- **pass**：pass_rate ≥ 0.70
- **不通过穷尽尝试**：T17（加强事实核查）

#### 指标 6：hallucination_check（幻觉检查）
- **method**：提取所有 `[来源:URL]` 标记，验证 URL 是否可达且内容与引用描述一致。若无法联网验证则标记为"待验证"
- **threshold**：0 个确认幻觉引用（"待验证"不计入幻觉，但需在 T19b 报告中标注）
- **pass**：hallucination_count == 0
- **不通过穷尽尝试**：T05（重新搜索验证）

### 2.3 T19a 执行流程
1. 读取 NRSF-Full
2. 逐项计算 6 个指标
3. 生成 T19a 结果报告（YAML 格式）
4. 所有 6 项通过 → 进入 T19b
5. 任一不通过 → 穷尽尝试回到对应阶段补充

### 2.4 T19a 结果报告格式
```yaml
t19a_results:
  citation_count:
    value: {N}
    threshold: {N}
    pass: {true|false}
  source_diversity:
    value: {N}
    threshold: 15
    pass: {true|false}
  source_type_coverage:
    value: {N}
    types_covered: [{academic}, {official}, {media}, {community}, {cultural}]
    threshold: 3
    pass: {true|false}
  counter_evidence_ratio:
    value: {ratio}
    threshold: 0.10
    pass: {true|false}
  triangulation_pass_rate:
    value: {ratio}
    threshold: 0.70
    pass: {true|false}
  hallucination_check:
    confirmed_hallucinations: {N}
    pending_verification: {N}
    threshold: 0
    pass: {true|false}
  overall_pass: {true|false}
  exhaust-retry_target: "{task_id or null}"
```

## 3. T19b LLM-as-Judge

### 3.1 强制批评提示词
```
你是一个严格的学术评审人。你的任务是找出研究报告中的问题，而非确认其正确性。

**强制批评规则**：
1. 你必须找出至少 3 个问题。如果找不到，说明你审得不够仔细。
2. 对每个论断，先假设它是错的，再找证据反驳它。
3. 偏好确定性表述的文本不等于好文本——检查是否有过度简化。
4. 长文本不等于深文本——检查是否有灌水段落。
5. 不要因为文本"看起来专业"就给高分——检查逻辑链是否实际闭合。

**评分锚定案例**：
- 1 分（不合格）：逻辑断裂，证据虚无，大段无引用的主观判断
- 3 分（及格）：逻辑基本通顺，每条核心论断有至少 1 个引用，无反证
- 5 分（优秀）：逻辑严密，每条论断有 2+ 独立来源，反证充分，边界清晰

**分歧处理**：如果对该给 3 分还是 4 分犹豫，给 3 分（宁可偏严）。
```

### 3.2 六个评估维度

#### 维度 1：semantic_quality（权重 0.35）
- 论证完整性：核心论证链是否从前提走到结论无跳跃
- 逻辑连贯：段落间是否有逻辑连接非简单罗列
- 证据质量：证据是否"根系完整"含推理+引用+出处

#### 维度 2：topical_focus（权重 0.20）
- 主题聚焦度：是否有偏离研究问题的段落
- 偏离惩罚：每发现一个偏离段落扣 0.5 分

#### 维度 3：retrieval_trustworthiness（权重 0.15）
- 引用可追溯性
- 来源权威度
- 三角验证通过率

#### 维度 4：accuracy（权重 0.15）
- 事实准确率
- 幻觉引用检出率

#### 维度 5：completeness（权重 0.10）
- 覆盖广度：研究问题所有子维度是否都已覆盖
- 缺口坦诚度：未闭合链是否被坦诚标注非隐藏

#### 维度 6：objectivity（权重 0.05）
- 反证比率
- 偏见倾向检测

### 3.3 评分方法
- 逐维评分 1-5
- 加权平均计算总分
- 总分 = semantic_quality × 0.35 + topical_focus × 0.20 + retrieval_trustworthiness × 0.15 + accuracy × 0.15 + completeness × 0.10 + objectivity × 0.05
- 加权总分 ≥ 3.5 为通过

### 3.4 T19b 输出格式
```markdown
## T19b 评审结果

### 强制发现问题（至少 3 个）
1. {问题描述} — {影响} — {建议修复}
2. {问题描述} — {影响} — {建议修复}
3. {问题描述} — {影响} — {建议修复}

### 各维度评分
| 维度 | 得分 | 评语 |
|------|------|------|
| semantic_quality | {1-5} | {简短评语} |
| topical_focus | {1-5} | {简短评语} |
| retrieval_trustworthiness | {1-5} | {简短评语} |
| accuracy | {1-5} | {简短评语} |
| completeness | {1-5} | {简短评语} |
| objectivity | {1-5} | {简短评语} |

### 加权总分: {x.x}/5

### 是否通过: {pass/fail}
```

### 3.5 不通过穷尽尝试规则
- 穷尽尝试回到问题最严重的阶段（通常 I01 或 T05）
- 补充研究后重新进入 T19
- 质量驱动持续重试

### 3.6 评估框架参考
- **Rigorous Bench**：语义质量基准，用于校准 semantic_quality 维度评分
- **DRACO**：深度研究评估框架，用于校准 retrieval_trustworthiness 和 completeness 维度
- **DeepResearch Bench**：研究深度评估，用于校准 topical_focus 和 accuracy 维度
- **DeepScholarBench**：学术质量评估，用于校准 objectivity 维度和整体评分锚定

## 4. T19a→T19b 流程

### 4.1 流程图
```
T17 + T18 完成
    ↓
T19a 规则检查
    ↓
全部 6 项通过？
    ├─ 是 → T19b LLM-as-Judge
    └─ 否 → 穷尽尝试回到对应阶段补充 → 重新 T19a

T19b LLM-as-Judge
    ↓
加权总分 ≥ 3.5？
    ├─ 是 → T19 通过 → 进入 T20
    └─ 否 → 穷尽尝试回到问题最严重阶段 → 补充研究 → 重新 T19（质量驱动）
```

### 4.2 双阶段输出格式
- **阶段 A**（结构化分析）：
  - T19a 结果报告（YAML 格式，见 §2.4）
  - T19b 评审结果（Markdown 格式，见 §3.4）

- **阶段 B**（散文式 NRSF 笔记）：
  - 散文式评估报告追加到 §T19
  - 包含评估过程描述、发现的问题、修复建议


## 5. ORCHESTRATOR 三维度评分（最终判定）

### 5.1 概述

T19a（规则检查）和 T19b（LLM 评分）完成后，进入 ORCHESTRATOR 三维度评分阶段，作为最终质量判定。三套评分体系执行顺序：

```
T19a（规则检查）→ T19b（LLM 评分）→ 三维度评分（最终判定）
```

### 5.2 三维度定义

| 维度 | 权重 | 评分范围 | 说明 |
|------|------|---------|------|
| **内洽度** (Coherence) | 40% | 1-10 | 报告内部逻辑一致性、章节间无矛盾、论证链闭合、§1-§8 结构完整性 |
| **创新度** (Novelty) | 30% | 1-10 | 见解原创性、非显而易见结论、跨域映射创新、元维度扩展深度 |
| **实用度** (Utility) | 30% | 1-10 | 可操作性、决策支持价值、现实适用性、读者可落地程度 |

### 5.3 综合评分公式

```
ORCHESTRATOR_Score = 0.40 × Coherence + 0.30 × Novelty + 0.30 × Utility
```

### 5.4 GREEN/YELLOW/RED 判定标准

| 判定 | 条件 | 处理 |
|------|------|------|
| **GREEN** | 三维度均 ≥ 7 且 ORCHESTRATOR_Score ≥ 7.5 | 通过，进入交付 |
| **YELLOW** | 任一维度 5-6 或 ORCHESTRATOR_Score 6.0-7.4 | 退回 Phase 1 补强弱项维度，重试后重新评分 |
| **RED** | 任一维度 < 5 或 ORCHESTRATOR_Score < 6.0 | 强制退回 Phase 1 重执行，标记问题节点重执行 |

### 5.5 三维度评分输出格式

```yaml
orchestrator_final_verdict:
  coherence:
    score: {1-10}
    rationale: "内洽度评语"
  novelty:
    score: {1-10}
    rationale: "创新度评语"
  utility:
    score: {1-10}
    rationale: "实用度评语"
  weighted_score: {x.x}
  verdict: "GREEN|YELLOW|RED"
  action: "通过|退回补强|强制重执行"
  weak_dimensions: ["{维度名}"]
```

### 5.6 与 T19a/T19b 的关系

- **T19a**（规则检查）：客观指标门控，不通过不进入后续阶段
- **T19b**（LLM 评分）：六维度学术质量评审，加权总分 ≥ 3.5 为通过
- **三维度评分**（最终判定）：ORCHESTRATOR 层面的交付决策，GREEN 才允许交付

三套评分体系层层递进：T19a 过滤基础质量问题，T19b 评估学术质量，三维度评分做最终交付决策。任一阶段不通过均触发穷尽重试。

---

## 6. 异常处理与穷尽重试

| 异常场景 | 处理策略 |
|---------|---------|
| T19a某项指标无法计算（如NRSF元数据缺失） | 该指标标记为"无法评估"，不纳入通过判定，但需在报告中说明原因 |
| T19a不通过 | 持续重试T19a直至通过，不设重试上限，通过后进入T19b |
| T19b LLM-as-Judge服务不可用 | 持续重试T19b直至服务可用，不设重试上限，质量保持为T19a+T19b完整双轨 |
| T19b评审超时 | 持续重试T19b直至全部维度评审完成，不设超时上限，不按及格线计入 |
| T19b评审结果与T19a严重矛盾 | 以T19a规则检查为准，T19b结果标注"与规则检查矛盾，需人工复核" |
| 持续重试直至质量达标 | 不设重试上限 |

---

## 穷尽重试策略

### L1: 完整自评估
T19a质量门控 + T19b偏差扫描 + 量化评分

### L2: 部分评估工具不可用
- T19a可用但T19b不可用：持续重试T19b直至可用，不设重试上限，不跳过偏差扫描
- 标记评估为部分评估

### L3: 评估工具完全不可用
- 持续重试T19a和T19b直至全部可用，不设重试上限，不使用简化评估维度
- 标记为穷尽重试评估

### L4: 评估系统完全失败
- 评估系统完全失败时持续重试，不跳过自评估步骤，标注"评估系统异常-持续重试中"
- 不设重试上限


---

## 测试用例 (D3.4.4)

### 测试用例 1：自评通过

**给定输入**：节点 T09 执行完成，self_check 清单全部通过，self_check_score=90。

**应产出**：自评通过，允许输出，score 写入 execution_ledger。

### 测试用例 2：自评未通过

**给定输入**：节点 T09 执行完成，self_check 清单中 2 项未通过，self_check_score=70。

**应产出**：自评未通过（< 85 阈值），触发重试，retry_feedback 包含未通过项的改进建议。

### 测试用例 3：跨模型自评

**给定输入**：Gate-终（T28）执行跨模型审计，模型 A 评分 88，模型 B 评分 82。

**应产出**：两模型评分分歧 > 5 分，触发第三模型裁定或人工介入。
