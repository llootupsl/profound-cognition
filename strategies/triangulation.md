<!-- 作者：阿洋 -->

# 三角验证策略

## 激活条件

```yaml
activation:
  condition: "T05/T06/T17 验证阶段 AND 存在需要验证的核心论断"
  trigger_rules:
    - "核心论断仅有一个来源支持"
    - "核心论断来自低权威度来源（权威度 < 0.7）"
    - "不同来源对同一论断存在矛盾"
    - "论断涉及关键决策或重大影响"
  priority: "必需 — 三角验证是研究可信度的核心保障"
```

---

## 1. 核心原则

关键事实必须 >= 2 个独立来源支持。独立来源定义为：不同作者、不同机构、不同方法论。

### 1.1 独立性判定规则

```yaml
independence_rules:
  rule_1_different_author:
    definition: "来源的作者无合作关系、无师生关系、无同一机构关系"
    verification: "检查作者机构和合作历史"

  rule_2_different_institution:
    definition: "来源的发表机构不同"
    verification: "检查机构名称和隶属关系"

  rule_3_different_methodology:
    definition: "来源使用不同的研究方法得出结论"
    verification: "检查研究方法描述"

  independence_scoring:
    3_dimensions_independent: "完全独立（最高可信度）"
    2_dimensions_independent: "部分独立（标准可信度）"
    1_dimension_independent: "弱独立（需补充验证）"
    0_dimensions_independent: "不独立（视为同一来源）"
```

---

## 2. 权威度评分

### 2.1 来源权威度
| 来源类型 | 权威度 | 示例 |
|---------|--------|------|
| 同行评审论文 | 0.95 | Nature, Science, 顶会论文 |
| 政府官方数据 | 0.90 | 统计局, WHO, UN |
| 国际组织报告 | 0.85 | World Bank, IMF, OECD |
| 知名媒体调查 | 0.75 | Reuters, BBC, 新华社 |
| 行业报告 | 0.70 | McKinsey, Gartner |
| 预印本/工作论文 | 0.65 | arXiv, SSRN |
| 博客/评论 | 0.40 | 个人博客, 专栏评论 |
| 社交媒体 | 0.30 | Twitter, 微博 |

### 2.2 加权计算
```
fact_confidence = sum(source_authority_i) / N
```

### 2.3 置信度分级

```yaml
confidence_levels:
  very_high:
    range: ">= 0.90"
    description: "多个高权威度独立来源一致支持"
    label: "高置信度"

  high:
    range: "0.75 - 0.89"
    description: "至少2个独立来源支持，权威度加权平均较高"
    label: "较高置信度"

  medium:
    range: "0.60 - 0.74"
    description: "有独立来源支持但权威度一般"
    label: "中等置信度"

  low:
    range: "0.40 - 0.59"
    description: "来源独立性和/或权威度不足"
    label: "低置信度"

  very_low:
    range: "< 0.40"
    description: "仅单一低权威度来源支持"
    label: "极低置信度"
```

---

## 3. 跨国/跨语言对比验证

### 3.1 验证规则
- 重要论断需跨语言来源验证
- 中文来源 + 英文来源为最低要求
- 按需添加第三语言来源

### 3.2 验证流程
1. 提取核心论断
2. 搜索中文来源
3. 搜索英文来源
4. 比较两个语言来源的一致性
5. 不一致时标注为"争议性论断"

### 3.3 跨语言一致性判定

```yaml
cross_language_consistency:
  consistent:
    condition: "中英文来源对同一论断得出一致结论"
    action: "标注为'跨语言验证通过'"
    confidence_bonus: "+0.1"

  partially_consistent:
    condition: "中英文来源方向一致但细节有差异"
    action: "标注为'部分一致'，记录差异点"
    confidence_bonus: "0"

  inconsistent:
    condition: "中英文来源对同一论断得出矛盾结论"
    action: "标注为'争议性论断'，记录各方论据"
    confidence_penalty: "-0.2"

  no_cross_language:
    condition: "仅有一种语言的来源"
    action: "标注为'单语言来源'，尝试搜索其他语言来源"
    confidence_penalty: "-0.1"
```

---

## 4. 三角验证通过率计算

### 4.1 计算方法
```
triangulation_pass_rate = (有 >= 2 独立来源的核心论断数) / (核心论断总数)
```

### 4.2 通过标准
- >= 0.70：通过
- 0.50-0.69：需补充
- < 0.50：严重不足

### 4.3 通过率与行动映射

```yaml
pass_rate_actions:
  ge_0_70:
    label: "通过"
    action: "继续后续研究阶段"
    report: "在NRSF中标注三角验证通过"

  range_0_50_0_69:
    label: "需补充"
    action: "触发I01补研，为未验证论断搜索补充来源"
    report: "在NRSF中标注需补充的论断列表"
    max_supplementary_rounds: 2

  lt_0_50:
    label: "严重不足"
    action: "触发I01补研，全面重新搜索核心论断来源"
    report: "在NRSF中标注严重不足警告"
    max_supplementary_rounds: 3
    escalation: "建议用户确认研究方向的可行性"
```

---

## 5. 未验证论断处理

### 5.1 处理规则
- 未通过三角验证的论断标注 [未验证]
- [未验证] 论断在 NRSF 中保留，但在最终输出中标注为"初步判断"
- [未验证] 论断超过 30% 时触发 I01 补研

### 5.2 未验证论断分级

```yaml
unverified_claim_handling:
  single_source:
    condition: "仅有一个来源支持"
    label: "[单源-未验证]"
    treatment: "标注为'初步判断'，在输出中标注来源数=1"
    action: "优先补研目标"

  low_authority:
    condition: "来源权威度 < 0.5"
    label: "[低权威-未验证]"
    treatment: "标注为'待验证判断'，在输出中标注权威度"
    action: "搜索高权威度替代来源"

  contradictory:
    condition: "不同来源存在矛盾"
    label: "[矛盾-未验证]"
    treatment: "标注为'争议性论断'，记录各方论据"
    action: "增加搜索轮次，寻找仲裁性来源"

  no_independent_source:
    condition: "多个来源但不独立"
    label: "[非独立-未验证]"
    treatment: "视为单源，标注为'初步判断'"
    action: "搜索独立来源"
```

---

## 6. 三角验证执行步骤

```yaml
triangulation_execution:
  step_1_extract_claims:
    method: "从NRSF中提取所有核心论断"
    output: "core_claims列表"

  step_2_source_audit:
    method: "审计每个论断的来源数量、权威度、独立性"
    output: "claim_source_audit列表"

  step_3_independence_check:
    method: "按独立性判定规则检查来源独立性"
    dimensions: [不同作者, 不同机构, 不同方法论]
    output: "independence_scores列表"

  step_4_cross_language_verify:
    method: "对重要论断执行跨语言验证"
    languages: ["中文", "英文"]
    output: "cross_language_results列表"

  step_5_calculate_pass_rate:
    method: "计算三角验证通过率"
    formula: "pass_rate = (有>=2独立来源的论断数) / (论断总数)"
    output: "pass_rate数值"

  step_6_action:
    method: "根据通过率执行对应行动"
    mapping: "pass_rate_actions"
    output: "行动列表"

  step_7_annotate:
    method: "在NRSF中标注验证结果"
    annotations: ["[已验证]", "[单源-未验证]", "[低权威-未验证]", "[矛盾-未验证]", "[非独立-未验证]"]
    output: "annotated_nrsf"
```

---

## 7. 与 profound-cognition Task 节点集成

```yaml
task_integration:
  T05_L6_L7_evidence:
    trigger: "证据边界层验证"
    strategy: "完整三角验证（7步执行）"
    pass_rate_threshold: 0.70
    annotation: "[triangulation] 标签标记验证结果"

  T06_L8_L9_counterfactual:
    trigger: "反事实搜索验证"
    strategy: "跨语言验证 + 矛盾论断标注"
    pass_rate_threshold: 0.50
    annotation: "[triangulation-counterfactual] 标签标记"

  T17_fact_check:
    trigger: "事实核查"
    strategy: "完整三角验证 + 置信度分级"
    pass_rate_threshold: 0.70
    annotation: "[triangulation-factcheck] 标签标记"

  I01_supplementary:
    trigger: "补研（未验证论断 > 30%）"
    strategy: "定向补研 + 重新验证"
    pass_rate_threshold: 0.70
    annotation: "[triangulation-supplement] 标签标记"
```

---

## 8. 输出规范

```yaml
triangulation_output:
  total_claims: int
  verified_claims: int
  unverified_claims: int
  pass_rate: float
  pass_level: "通过|需补充|严重不足"
  claims:
    - claim: str
      sources:
        - source: str
          authority: float
          institution: str
          methodology: str
          language: str
      independence_score: float
      confidence: float
      confidence_level: "高|较高|中等|低|极低"
      verification_status: "已验证|单源-未验证|低权威-未验证|矛盾-未验证|非独立-未验证"
      cross_language: "consistent|partially_consistent|inconsistent|no_cross_language"
  action_required: [str]
```

---

## 9. 穷尽重试策略

```yaml
exhaust_retry:
  rule_1_full_verify:
    condition: "所有搜索引擎可用 + 跨语言搜索正常"
    behavior: "完整三角验证 + 独立性3维检查 + 跨语言验证 + 置信度5级分级"

  rule_2_partial_verify:
    condition: "部分搜索引擎不可用 或 跨语言搜索受限"
    behavior: "可用来源验证 + 标注[PARTIAL-VERIFICATION] + 降低通过率阈值至0.60"

  rule_3_llm_verify:
    condition: "搜索引擎不可用，仅能使用LLM内建知识"
    behavior: "LLM知识交叉验证 + 标注[LLM-VERIFICATION] + 所有论断标注为'初步判断'"

  rule_4_no_verify:
    condition: "验证功能完全不可用"
    behavior: "所有论断标注[UNVERIFIED] + 警告研究可信度不足 + 建议人工验证"
```
