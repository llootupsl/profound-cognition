<!-- 作者：阿洋 -->

# 学术合规协议 (Academic Compliance Protocol) v3.0

> **状态**: 正式发布 (v3.0)
> **适用范围**: Profound Cognition — research_report / course_material 产品的学术合规声明自动生成
> **最后更新**: 2026-06-25
> **依赖**: `persona/persona-schema.yaml`（ORCID 字段）、`tasks/T26_meta_insight_cross.md`（伦理交叉洞察）、`tasks/TM05_meta_reflection.md`（伦理分析）、`tasks/T24_meta_dim_part2.md`（法律伦理维度）、`protocols/nrsf-protocol.md`（数据源追溯）
> **职责边界**: 本协议定义学术合规声明的**自动生成规则、数据来源、输出格式与覆盖机制**。不替代人工伦理审查，仅基于研究流程中已产出的伦理分析结果生成声明。

---

## 1. 协议概述

### 1.1 目的

AcademicComplianceProtocol 定义 Profound Cognition 中四类学术合规声明的自动生成机制，确保研究输出符合学术出版规范：

1. **ORCID 集成**（D15.4.1）—— Persona 系统新增 ORCID 字段，引用时自动附加
2. **数据可用性声明**（D15.4.2）—— 基于研究过程中使用的数据源自动生成
3. **伦理审查声明**（D15.4.3）—— 基于 T26/TM05 伦理分析结果自动生成
4. **利益冲突声明**（D15.4.4）—— 默认「无利益冲突」，用户可覆盖
5. **作者贡献声明**（D15.4.5）—— 基于 Persona 系统自动生成

### 1.2 核心设计原则

- **自动生成优先**：所有声明默认自动生成，无需用户手动编写
- **可追溯**：每条声明必须标注数据来源（NRSF §ref 或节点 ID）
- **可覆盖**：用户可逐条覆盖自动生成的声明内容
- **保守声明**：当数据不足时，生成保守声明（如"本研究未涉及人类受试者"而非"已通过伦理审查"）
- **不替代人工审查**：伦理审查声明仅基于流程内分析结果，不替代正式的机构伦理委员会审查

### 1.3 触发条件

```yaml
trigger:
  condition: "output_type IN [research_report, course_material]"
  description: "研究报告与课程材料需生成学术合规声明；公众号文章不触发"
  generation_node: "T20a_research_render / T20c_course_render"
  always_trigger: true  # 只要触发条件满足即自动生成
```

### 1.4 与其他协议的关系

| 文档 | 职责 | 与本协议的关系 |
|------|------|--------------|
| `persona/persona-schema.yaml` | ORCID 字段定义 | 本协议读取 `researcher.orcid` 字段 |
| `persona/persona-init-protocol.md` | ORCID 采集流程 | 本协议引用其采集结果 |
| `protocols/nrsf-protocol.md` | 数据源记录格式 | 本协议从 NRSF 提取数据源清单 |
| `tasks/T26_meta_insight_cross.md` | 跨维度伦理洞察 | 本协议引用其法律伦理交叉洞察 |
| `tasks/TM05_meta_reflection.md` | 伦理深度分析 | 本协议引用其 ethics_analysis 输出 |
| `tasks/T24_meta_dim_part2.md` | 法律伦理维度分析 | 本协议引用其 dim_10 伦理考量 |

---

## 2. ORCID 集成与引用附加（D15.4.1）

### 2.1 ORCID 字段定义

ORCID（Open Researcher and Contributor ID）是研究者的持久数字标识符。Persona 系统在 `researcher` 类型中新增 `orcid` 字段：

```yaml
# persona-schema.yaml
researcher:
  orcid:
    type: string
    pattern: '^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$'  # XXXX-XXXX-XXXX-XXXX
    required: false
    description: "ORCID iD，引用时自动附加到研究报告署名"
```

### 2.2 ORCID 采集流程

ORCID 在 Phase 0 人设初始化时采集（详见 `persona-init-protocol.md` §3.1 q5）：

```yaml
orcid_collection:
  timing: "Phase 0 人设初始化"
  question: "（可选，可跳过）您的 ORCID iD 是什么？（格式：XXXX-XXXX-XXXX-XXXX）"
  required: false
  validation:
    pattern: '^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$'
    checksum: "ISO 7064 11-2 校验算法"
    on_invalid: "提示格式错误，不阻塞流程"
    on_skip: "orcid 字段设为 null，不附加 ORCID"
  storage: "写入 persona_context.researcher.orcid"
```

### 2.3 ORCID 校验算法

ORCID iD 的末位是校验位，采用 ISO 7064 11-2 模 11 算法：

```python
def validate_orcid_checksum(orcid: str) -> bool:
    """校验 ORCID iD 的末位校验位"""
    digits = orcid.replace('-', '').replace('X', '10')[:-1]
    total = 0
    for d in digits:
        total = (total + int(d)) * 2
    remainder = total % 11
    check = (12 - remainder) % 11
    check_char = 'X' if check == 10 else str(check)
    return orcid[-1] == check_char
```

### 2.4 ORCID 自动附加规则

当 `researcher.orcid` 非 null 时，在研究报告署名处自动附加 ORCID：

```yaml
orcid_auto_append:
  trigger: "T20a_research_render 渲染研究报告署名时"
  condition: "persona_context.researcher.orcid != null"
  format:
    inline: "{author_name} (ORCID: {orcid})"
    footnote: "{author_name}¹ ¹ ORCID: https://orcid.org/{orcid}"
    reference_list: "Corresponding author: {author_name}, ORCID: {orcid}"
  selection_rule: "按 citation_style 选择格式：inline→inline，footnote→footnote，apa/chicago→reference_list"
  on_null: "不附加 ORCID，仅显示作者名"
```

### 2.5 ORCID 隐私保护

```yaml
orcid_privacy:
  storage: "ORCID 仅存储在 persona_context 中，不写入公开日志"
  display: "仅在研究报告署名处显示，不在过程日志中暴露"
  user_control: "用户可随时通过 T01b 校准清除 ORCID"
  cross_session: "跨会话持久化时保留 ORCID（属于 persona 配置）"
```

---

## 3. 数据可用性声明自动生成（D15.4.2）

### 3.1 数据来源识别

数据可用性声明基于研究过程中使用的数据源自动生成。数据源从 NRSF 中提取：

```yaml
data_source_extraction:
  source: "NRSF.metadata.data_sources + NRSF.evidence_pool"
  extraction_node: "T22_nrsf_synthesize（NRSF 综合节点）"
  extracted_fields:
    - source_id: "数据源唯一标识"
    - source_type: "数据源类型（见 §3.2）"
    - source_url: "数据源 URL（如有）"
    - access_date: "访问日期"
    - license: "许可证类型（如有）"
    - evidence_level: "证据等级 L0-L3"
```

### 3.2 数据源类型分类

| 数据源类型 | 标识 | 可用性声明模板 |
|-----------|------|--------------|
| 公开数据集 | `public_dataset` | "本研究使用的公开数据集可从 {source_url} 获取" |
| 学术文献 | `academic_literature` | "本研究引用的学术文献可通过 DOI 或出版社网站获取" |
| 政府数据 | `government_data` | "本研究使用的政府数据来自 {source_url}，公开可访问" |
| 企业数据 | `enterprise_data` | "本研究使用的部分数据由企业提供，受 NDA 约束，不可公开" |
| 原始数据 | `raw_data` | "本研究生成的原始数据可从 {repository_url} 获取" |
| API 数据 | `api_data` | "本研究通过 {api_name} API 获取数据，访问条件见 {source_url}" |
| 受限数据 | `restricted_data` | "本研究使用的部分数据受访问限制，需申请权限" |

### 3.3 声明生成规则

```yaml
data_availability_generation:
  trigger: "T20a_research_render / T20c_course_render 渲染前"
  input: "NRSF 中提取的数据源清单"
  rules:
    - condition: "全部数据源为 public_dataset / academic_literature / government_data"
      template: "本研究使用的全部数据来自公开来源，可从相应公开渠道获取。具体数据源清单见附录 {appendix_ref}。"
    
    - condition: "存在 enterprise_data 或 restricted_data"
      template: "本研究使用的部分数据受访问限制（{restricted_count} 项），不可公开获取。其余公开数据可从相应渠道获取。受限数据详情见附录 {appendix_ref}。"
    
    - condition: "存在 raw_data（研究过程中生成）"
      template: "本研究生成的原始数据已上传至 {repository_url}，可公开获取。引用数据集请使用：{citation}。"
    
    - condition: "数据源清单为空"
      template: "本研究为理论分析/文献综述，未使用原始数据集。"
    
    - condition: "混合数据源"
      template: "本研究使用的数据来源多样：{public_count} 项公开数据、{restricted_count} 项受限数据。公开数据可从相应渠道获取，受限数据需申请权限。数据源完整清单见附录 {appendix_ref}。"
  
  appendix_ref: "附录 A：数据源清单"
  citation_format: "Data available from {repository_url} (accessed {access_date})"
```

### 3.4 数据源清单附录格式

```yaml
data_source_appendix:
  title: "附录 A：数据源清单"
  format: "表格"
  columns:
    - 序号
    - 数据源名称
    - 类型
    - URL / 获取方式
    - 访问日期
    - 许可证
    - 证据等级
  sorting: "按证据等级降序排列（L0 优先）"
```

### 3.5 用户覆盖

```yaml
data_availability_override:
  trigger: "用户明确要求修改数据可用性声明"
  action: "用用户提供的声明替换自动生成的声明"
  scope: "仅替换声明文本，数据源清单附录仍自动生成"
  log: "记录覆盖事件到 execution_ledger.academic_compliance.data_availability_override"
```

---

## 4. 伦理审查声明自动生成（D15.4.3）

### 4.1 伦理分析数据来源

伦理审查声明基于研究流程中已产出的伦理分析结果。Profound Cognition 有三个伦理分析来源：

| 来源节点 | 分析类型 | 输出字段 | 说明 |
|---------|---------|---------|------|
| T24（维度10） | 法律伦理维度分析 | `dim_10.aspects: ["法律合规分析", "伦理考量"]` | Path A：基于 GT-HarmBench 评估 |
| T26（跨维度洞察） | 法律伦理交叉洞察 | `cross_insights` 中 dimensions 含 "法律伦理" 的条目 | 跨维度伦理关联 |
| TM05（Step 7） | 伦理深度分析 | `ethics_analysis: {dimensions, dilemmas, recommendations}` | Path B：自主性/beneficence/非恶意/公正/可解释性 |

### 4.2 伦理风险等级判定

基于三个来源的伦理分析结果，判定研究的伦理风险等级：

```yaml
ethics_risk_assessment:
  inputs:
    - t24_ethics: "T24 dim_10 伦理考量"
    - t26_ethics_insights: "T26 法律伦理交叉洞察"
    - tm05_ethics: "TM05 ethics_analysis"
  
  risk_levels:
    NONE:
      condition: "三个来源均无伦理风险标识"
      statement_template: "本研究未涉及人类受试者、动物实验或可识别个人信息，不涉及伦理审查事项。"
    
    LOW:
      condition: "存在伦理考量但无困境/张力"
      statement_template: "本研究在分析过程中识别了伦理维度（{ethics_dimensions}），经评估未发现显著伦理风险。伦理考量详情见附录 {appendix_ref}。"
    
    MEDIUM:
      condition: "存在伦理困境或张力，但有明确建议"
      statement_template: "本研究识别了 {dilemma_count} 项伦理困境/张力，涉及 {ethics_dimensions}。已提出 {recommendation_count} 项伦理建议。伦理分析详情见附录 {appendix_ref}。"
    
    HIGH:
      condition: "存在高严重性伦理风险"
      statement_template: "本研究识别了高严重性伦理风险，涉及 {risk_details}。建议在正式发布前提交机构伦理委员会审查。伦理风险详情见附录 {appendix_ref}。"
  
  independence_limitation: "Path A (T24) 和 Path B (TM05) 均依赖同一 LLM，独立性有限。本声明不替代正式的机构伦理委员会审查。"
```

### 4.3 声明生成规则

```yaml
ethics_statement_generation:
  trigger: "T20a_research_render / T20c_course_render 渲染前"
  input: "T24 dim_10 + T26 cross_insights + TM05 ethics_analysis"
  
  flow:
    step_1: "从 T24 提取 dim_10.aspects 中的伦理考量"
    step_2: "从 T26 提取 dimensions 含 '法律伦理' 的 cross_insights"
    step_3: "从 TM05 提取 ethics_analysis（dimensions/dilemmas/recommendations）"
    step_4: "按 §4.2 判定伦理风险等级（NONE/LOW/MEDIUM/HIGH）"
    step_5: "按风险等级选择声明模板"
    step_6: "填充模板变量（ethics_dimensions/dilemma_count 等）"
    step_7: "附加独立性限制声明"
  
  appendix_ref: "附录 B：伦理分析详情"
  
  mandatory_disclaimer: |
    注：本伦理审查声明基于 Profound Cognition 流程内的自动化伦理分析（T24 维度分析 + T26 跨维度洞察 + TM05 元认知反思），不构成正式的机构伦理委员会审查。如研究涉及人类受试者、动物实验或敏感个人信息，应另行提交机构伦理委员会审批。
```

### 4.4 伦理分析详情附录格式

```yaml
ethics_appendix:
  title: "附录 B：伦理分析详情"
  sections:
    - section: "B.1 法律伦理维度分析（T24）"
      content: "T24 dim_10 完整输出"
    - section: "B.2 跨维度伦理洞察（T26）"
      content: "T26 中 dimensions 含 '法律伦理' 的 cross_insights 列表"
    - section: "B.3 伦理深度分析（TM05）"
      content: "TM05 ethics_analysis 完整输出（dimensions/dilemmas/recommendations）"
    - section: "B.4 独立性限制声明"
      content: "Path A 和 Path B 均依赖同一 LLM，独立性有限"
```

### 4.5 用户覆盖

```yaml
ethics_statement_override:
  trigger: "用户明确要求修改伦理审查声明"
  action: "用用户提供的声明替换自动生成的声明"
  scope: "仅替换声明文本，伦理分析详情附录仍自动生成"
  warning: "覆盖高风险伦理声明时，提示用户确认已通过正式伦理审查"
  log: "记录覆盖事件到 execution_ledger.academic_compliance.ethics_override"
```

---

## 5. 利益冲突声明自动生成（D15.4.4）

### 5.1 默认声明

利益冲突声明默认为「无利益冲突」：

```yaml
conflict_of_interest_default:
  template: "作者声明：本研究无利益冲突。"
  condition: "默认声明，无需用户输入"
```

### 5.2 用户覆盖机制

用户可在任何阶段声明利益冲突，覆盖默认声明：

```yaml
conflict_of_interest_override:
  trigger: "用户明确声明存在利益冲突"
  collection:
    timing: "Phase 0 人设初始化时询问（可选）/ T01b 校准时补充 / 渲染前确认"
    question: "（可选，可跳过）本研究是否存在需要声明的利益冲突？（如：资助方关系、个人经济利益、学术竞争关系）"
    type: "free_text"
    required: false
  
  override_templates:
    financial:
      condition: "用户声明存在财务利益冲突"
      template: "作者声明：本研究存在以下利益冲突——{user_provided_details}。"
    
    affiliation:
      condition: "用户声明存在机构从属关系冲突"
      template: "作者声明：本研究存在以下机构从属关系——{user_provided_details}。"
    
    personal:
      condition: "用户声明存在个人关系冲突"
      template: "作者声明：本研究存在以下个人关系利益冲突——{user_provided_details}。"
    
    custom:
      condition: "用户提供自定义声明"
      template: "{user_provided_statement}"
  
  confirmation: "覆盖默认声明时需用户明确确认"
  log: "记录覆盖事件到 execution_ledger.academic_compliance.coi_override"
```

### 5.3 利益冲突检测提示

```yaml
coi_detection_hint:
  trigger: "研究过程中检测到潜在利益冲突信号"
  signals:
    - "数据源中存在 enterprise_data 且用户声明与该企业有从属关系"
    - "Persona 中 expertise_domains 与研究结论直接相关，可能存在学术立场冲突"
    - "T26 跨维度洞察中识别利益相关方维度的高风险信号"
  action: "提示用户确认是否需要声明利益冲突"
  non_blocking: "检测提示不阻塞流程，仅建议用户确认"
```

---

## 6. 作者贡献声明自动生成（D15.4.5）

### 6.1 基于 Persona 系统生成

作者贡献声明基于 Persona 系统的 `persona_type` 和字段配置自动生成：

```yaml
author_contribution_generation:
  source: "persona_context"
  trigger: "T20a_research_render / T20c_course_render 渲染前"
  
  templates:
    researcher:
      condition: "persona_type == 'researcher'"
      template: |
        作者贡献声明：
        {author_name}（{orcid_or_affiliation}）作为本研究的主要研究者，完成了以下工作：
        - 研究设计与问题定义
        - {methodology_preference}方法论的执行
        - 数据收集与分析（涉及领域：{expertise_domains}）
        - 报告撰写与{writing_style}风格呈现
        - 结论论证与{citation_style}引注规范执行
      variables:
        author_name: "用户提供的作者名（默认：研究者）"
        orcid_or_affiliation: "ORCID（如有）或专业领域标识"
        methodology_preference: "persona_context.researcher.methodology_preference"
        expertise_domains: "persona_context.researcher.expertise_domains"
        writing_style: "persona_context.researcher.writing_style"
        citation_style: "persona_context.researcher.citation_style"
    
    educator:
      condition: "persona_type == 'educator'"
      template: |
        作者贡献声明：
        {author_name} 作为本课程材料的开发者，完成了以下工作：
        - 课程内容设计与{teaching_style}教学策略制定
        - 知识体系构建（目标学员水平：{target_level}）
        - 教学节奏规划（{pacing}）
        - 评估方式设计（{assessment_style}）
      variables:
        author_name: "用户提供的作者名（默认：教育者）"
        teaching_style: "persona_context.educator.teaching_style"
        target_level: "persona_context.educator.target_level"
        pacing: "persona_context.educator.pacing"
        assessment_style: "persona_context.educator.assessment_style"
    
    wechat_author:
      condition: "persona_type == 'wechat_author'"
      template: |
        作者贡献声明：
        {author_name}（{identity}）作为本文作者，完成了以下工作：
        - 选题策划与视角构建
        - 内容创作与{style_ref}叙事呈现
        - 个人经历素材提供（{story_count} 个故事）
        - {expected_tone}语气的把控与表达
      variables:
        author_name: "用户提供的作者名（默认：作者）"
        identity: "persona_context.wechat_author.identity"
        style_ref: "persona_context.wechat_author.style_ref"
        story_count: "persona_context.wechat_author.personal_stories 的数量"
        expected_tone: "persona_context.wechat_author.expected_tone"
```

### 6.2 多作者场景

```yaml
multi_author_scenario:
  trigger: "用户声明存在多位作者"
  collection:
    question: "（可选）是否有其他作者需要声明贡献？请提供每位作者的姓名与贡献描述。"
    type: "free_text"
    required: false
  
  template: |
    作者贡献声明：
    {primary_author}（{primary_contribution}）
    {secondary_authors_list}
  
  format:
    secondary_authors_list: "每行一位作者：{name}（{contribution}）"
  
  default: "未声明多作者时，默认单作者贡献声明"
```

### 6.3 CRediT 分类法对齐

作者贡献声明可对齐 CRediT（Contributor Roles Taxonomy）标准分类：

```yaml
credit_alignment:
  mapping:
    researcher:
      "研究设计与问题定义": "Conceptualization"
      "数据收集与分析": "Data curation, Investigation, Formal analysis"
      "报告撰写": "Writing – original draft"
      "结论论证": "Validation"
      "引注规范执行": "Writing – review & editing"
    educator:
      "课程内容设计": "Conceptualization"
      "知识体系构建": "Methodology"
      "教学节奏规划": "Project administration"
      "评估方式设计": "Validation"
    wechat_author:
      "选题策划": "Conceptualization"
      "内容创作": "Writing – original draft"
      "个人经历素材提供": "Resources"
      "语气把控": "Writing – review & editing"
  
  optional: "CRediT 对齐为可选，用户可选择是否采用 CRediT 标签"
```

### 6.4 用户覆盖

```yaml
author_contribution_override:
  trigger: "用户明确要求修改作者贡献声明"
  action: "用用户提供的声明替换自动生成的声明"
  scope: "完全替换声明文本"
  log: "记录覆盖事件到 execution_ledger.academic_compliance.author_contribution_override"
```

---

## 7. 声明集成与输出位置

### 7.1 声明在研究报告中的位置

```yaml
statement_placement:
  research_report:
    orcid: "署名处（标题下方，作者名后）"
    data_availability: "正文末尾，参考文献之前"
    ethics_review: "正文末尾，数据可用性声明之后"
    conflict_of_interest: "正文末尾，伦理审查声明之后"
    author_contribution: "正文末尾，利益冲突声明之后"
  
  course_material:
    orcid: "课程封面或讲师信息处"
    data_availability: "课程材料附录"
    ethics_review: "课程材料附录（如有伦理考量）"
    conflict_of_interest: "课程材料附录"
    author_contribution: "课程材料附录"
  
  wechat_article:
    trigger: "不触发（公众号文章不生成学术合规声明）"
```

### 7.2 声明章节格式

```yaml
statement_section_format:
  title: "学术合规声明"
  subsections:
    - "数据可用性声明"
    - "伦理审查声明"
    - "利益冲突声明"
    - "作者贡献声明"
  numbering: "连续编号（如：声明 1、声明 2、声明 3、声明 4）"
  language: "与研究报告主体语言一致"
```

### 7.3 声明写入 NRSF

```yaml
nrsf_integration:
  section: "nrsf.metadata.academic_compliance"
  format:
    academic_compliance:
      orcid: " researcher.orcid 或 null"
      data_availability:
        statement: "自动生成的声明文本"
        source_count: int
        restricted_count: int
        overridden: false
      ethics_review:
        statement: "自动生成的声明文本"
        risk_level: "NONE|LOW|MEDIUM|HIGH"
        sources: ["T24", "T26", "TM05"]
        overridden: false
      conflict_of_interest:
        statement: "默认或用户覆盖的声明文本"
        overridden: false
      author_contribution:
        statement: "自动生成的声明文本"
        persona_type: "researcher|educator|wechat_author"
        credit_aligned: false
        overridden: false
  write_timing: "T20a/T20c 渲染完成后写入 NRSF"
```

---

## 8. 校验与审计

### 8.1 声明完整性校验

```yaml
statement_completeness_check:
  trigger: "Gate-终（T28）最终检查时"
  checks:
    - id: "AC-01"
      check: "research_report 输出包含全部 4 项声明"
      severity: "MAJOR"
      rule: "data_availability + ethics_review + conflict_of_interest + author_contribution 均非空"
    
    - id: "AC-02"
      check: "ORCID 格式校验（如提供）"
      severity: "MINOR"
      rule: "orcid 字段为 null 或匹配 ^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$"
    
    - id: "AC-03"
      check: "数据可用性声明引用的数据源清单与 NRSF 一致"
      severity: "MAJOR"
      rule: "声明中 source_count == NRSF.metadata.data_sources 的长度"
    
    - id: "AC-04"
      check: "伦理审查声明引用的伦理分析来源可追溯"
      severity: "MAJOR"
      rule: "声明中 sources 字段引用的节点 ID 在 NRSF 中存在"
    
    - id: "AC-05"
      check: "利益冲突声明非空"
      severity: "CRITICAL"
      rule: "conflict_of_interest.statement 非空"
    
    - id: "AC-06"
      check: "作者贡献声明与 Persona 类型一致"
      severity: "MAJOR"
      rule: "author_contribution.persona_type == persona_context.persona_type"
    
    - id: "AC-07"
      check: "覆盖事件已记录"
      severity: "MINOR"
      rule: "所有 overridden=true 的声明在 execution_ledger 中有对应覆盖日志"
```

### 8.2 审计日志格式

```yaml
academic_compliance_audit:
  timestamp: "ISO 8601"
  output_type: "research_report"
  persona_type: "researcher"
  statements_generated:
    - type: "data_availability"
      auto_generated: true
      overridden: false
      source_count: 12
      restricted_count: 2
    - type: "ethics_review"
      auto_generated: true
      overridden: false
      risk_level: "LOW"
      sources: ["T24", "T26", "TM05"]
    - type: "conflict_of_interest"
      auto_generated: true
      overridden: false
      default_used: true
    - type: "author_contribution"
      auto_generated: true
      overridden: false
      persona_type: "researcher"
      credit_aligned: false
  orcid_provided: true
  orcid_valid: true
  completeness_check: "PASS"
```

### 8.3 与 Gate-终 的集成

```yaml
gate_final_integration:
  gate: "T28 Gate-终"
  check_ids: ["AC-01", "AC-02", "AC-03", "AC-04", "AC-05", "AC-06", "AC-07"]
  blocking_rules:
    AC-05: "CRITICAL — 利益冲突声明为空时 Gate-终 FAIL"
    AC-01: "MAJOR — 缺失任一声明时 Gate-终 PASS_WITH_WARNINGS（C 级以下，不降低 EXHAUST 质量标准，仅降级 Gate 判定等级）"
    AC-03: "MAJOR — 数据源清单不一致时 Gate-终 PASS_WITH_WARNINGS（不降低 EXHAUST 质量标准）"
    AC-04: "MAJOR — 伦理来源不可追溯时 Gate-终 PASS_WITH_WARNINGS（不降低 EXHAUST 质量标准）"
    AC-06: "MAJOR — Persona 类型不一致时 Gate-终 PASS_WITH_WARNINGS（不降低 EXHAUST 质量标准）"
    AC-02: "MINOR — ORCID 格式错误时 WARNING"
    AC-07: "MINOR — 覆盖日志缺失时 WARNING"
  exhaust_compliance_note: |
    注：本协议中的"Gate-终 PASS_WITH_WARNINGS"是 T28 三态判定（PASS/PASS_WITH_WARNINGS/FAIL）
    的中间态，表示 Gate 判定等级降级，**不构成 EXHAUST 模式质量标准降级**。
    EXHAUST 四大铁律之"质量唯一优先"在所有 Gate 判定中均严格生效。
    受限运行模式下，仅可降低输出体积，不得降低质量标准（含 14 维度覆盖率/字数下限/参考文献完整性）。
```

---

## 9. 边界与限制

### 9.1 不替代正式审查

```yaml
limitations:
  ethics_review: |
    本协议生成的伦理审查声明基于流程内自动化伦理分析（T24/T26/TM05），
    不构成正式的机构伦理委员会（IRB/REC）审查。
    涉及人类受试者、动物实验或敏感个人信息的研究，
    必须另行提交机构伦理委员会审批。
  
  conflict_of_interest: |
    本协议默认「无利益冲突」声明，不主动检测用户未声明的利益冲突。
    利益冲突检测提示（§5.3）仅为辅助信号，不替代用户的主动声明义务。
  
  author_contribution: |
    本协议基于 Persona 系统自动生成作者贡献声明，
    反映的是 Persona 配置中的角色定位，不替代实际贡献的核实。
    多作者场景下，各作者的实际贡献应由作者团队自行确认。
```

### 9.2 适用范围限制

```yaml
scope_limitations:
  research_report: "完全适用——生成全部 4 项声明 + ORCID 附加"
  course_material: "部分适用——生成数据可用性/伦理审查/利益冲突/作者贡献，ORCID 可选"
  wechat_article: "不适用——公众号文章不生成学术合规声明"
  analysis_report: "部分适用——同 research_report，但可简化"
  press_commentary: "不适用——新闻评论不生成学术合规声明"
  decision_memo: "不适用——决策备忘录不生成学术合规声明"
```

---

## 10. 测试用例

### 10.1 ORCID 集成测试

```yaml
test_case_orcid:
  tc_1:
    name: "有效 ORCID"
    input: "0000-0002-1825-0097"
    expected: "校验通过，附加到署名"
  
  tc_2:
    name: "无效格式 ORCID"
    input: "0000-0002-1825-009"
    expected: "校验失败，提示格式错误，不阻塞流程"
  
  tc_3:
    name: "校验位错误 ORCID"
    input: "0000-0002-1825-0090"
    expected: "校验失败，提示校验位错误"
  
  tc_4:
    name: "ORCID 为 null"
    input: null
    expected: "不附加 ORCID，仅显示作者名"
```

### 10.2 数据可用性声明测试

```yaml
test_case_data_availability:
  tc_1:
    name: "全部公开数据源"
    input: "12 项公开数据源，0 项受限"
    expected: "生成「全部数据来自公开来源」声明"
  
  tc_2:
    name: "混合数据源"
    input: "10 项公开，2 项受限"
    expected: "生成「部分数据受访问限制」声明"
  
  tc_3:
    name: "无数据源"
    input: "数据源清单为空"
    expected: "生成「理论分析/文献综述，未使用原始数据集」声明"
```

### 10.3 伦理审查声明测试

```yaml
test_case_ethics:
  tc_1:
    name: "无伦理风险"
    input: "T24/T26/TM05 均无伦理风险标识"
    expected: "风险等级 NONE，生成「不涉及伦理审查事项」声明"
  
  tc_2:
    name: "中等伦理风险"
    input: "TM05 识别 2 项伦理困境，3 项建议"
    expected: "风险等级 MEDIUM，生成含困境数与建议数的声明"
  
  tc_3:
    name: "高伦理风险"
    input: "TM05 识别高严重性伦理风险"
    expected: "风险等级 HIGH，建议提交机构伦理委员会"
```

### 10.4 利益冲突声明测试

```yaml
test_case_coi:
  tc_1:
    name: "默认无利益冲突"
    input: "用户未声明利益冲突"
    expected: "生成默认「无利益冲突」声明"
  
  tc_2:
    name: "用户覆盖"
    input: "用户声明存在财务利益冲突"
    expected: "生成含用户提供的冲突详情的声明"
```

### 10.5 作者贡献声明测试

```yaml
test_case_author_contribution:
  tc_1:
    name: "researcher persona"
    input: "persona_type=researcher, methodology=mixed_methods, expertise=[经济学, AI]"
    expected: "生成含方法论与领域的贡献声明"
  
  tc_2:
    name: "educator persona"
    input: "persona_type=educator, teaching_style=Systematic"
    expected: "生成含教学策略的贡献声明"
  
  tc_3:
    name: "多作者场景"
    input: "用户声明 2 位作者"
    expected: "生成含主作者与次作者的贡献声明"
```

---

## 附录：变更记录

| 版本 | 日期 | 变更内容 |
|------|------|---------|
| v3.0 | 2026-06-25 | 初版发布：ORCID 集成（D15.4.1）、数据可用性声明（D15.4.2）、伦理审查声明（D15.4.3）、利益冲突声明（D15.4.4）、作者贡献声明（D15.4.5） |
