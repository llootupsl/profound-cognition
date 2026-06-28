<!-- 作者：阿洋 -->

## v5.1.0 Gate 门控检查维度

### Gate-α 检查维度

| 序号 | 检查项 | 通过条件 |
|------|--------|---------|
| 1 | 搜索覆盖率 | T02 搜索次数 ≥ 24，来源 ≥ 24，来源类型 ≥ 4 |
| 2 | 核心发现完整性 | T03 发现覆盖研究问题所有子维度 |
| 3 | 概念框架一致性 | T04 概念框架与 T03 发现无矛盾 |
| 4 | 证据层质量 | T05 引用数 ≥ 阈值，三角验证通过率 ≥ 0.70 |
| 5 | 铁律合规 | §0 铁律七条无违反 |
| 6 | NRSF 完整性 | §T02-§T06 均已追加到 NRSF-Full |

### Gate-β 检查维度

| 序号 | 检查项 | 通过条件 |
|------|--------|---------|
| 1 | I01 迭代深化 | 至少 2 轮，P0/P1 缺口全部闭合或标注 |
| 2 | 认知综合质量 | T13 综合叙事字数 ≥ 100000 |
| 3 | 反证充分性 | 反证段落数 / 总论断段落数 ≥ 0.10 |
| 4 | 铁律合规 | §0 铁律七条无违反 |
| 5 | NRSF 完整性 | §T08-§I01 均已追加到 NRSF-Full |

### Gate-γ 检查维度

| 序号 | 检查项 | 通过条件 |
|------|--------|---------|
| 1 | T19a 规则检查 | 6 项指标全部通过 |
| 2 | T19b LLM-as-Judge | 加权总分 ≥ 3.5 |
| 3 | 事实核查 | T17 无确认幻觉引用 |
| 4 | 偏见检测 | T18 无严重偏见倾向 |
| 5 | 铁律合规 | §0 铁律七条无违反 |
| 6 | NRSF 完整性 | §T15-§T19 均已追加到 NRSF-Full |

### Gate 失败处理

| Gate | 失败处理 |
|------|---------|
| Gate-α | 回退到失败维度对应的最早 Task，重新执行 |
| Gate-β | 回退到 I01，增加补研轮次 |
| Gate-γ | 回退到 T19，修复问题后重新自评（持续重试直至通过，无次数上限） |

### Persona 初始化完整性检查（Phase -1）

| 序号 | 检查项 | 通过条件 |
|------|--------|---------|
| 1 | persona_type 有效 | persona_type ∈ {researcher, wechat_author, educator} |
| 2 | researcher 必填字段完整 | expertise_domains / methodology_preference / writing_style / citation_style 全部非空 |
| 3 | **wechat_author 必填字段完整（7 项）** | identity / core_values / personal_stories / catchphrase / emotion_expression / target_audience / expected_tone 全部非空 |
| 4 | educator 必填字段完整 | teaching_style / target_level / pacing / assessment_style 全部非空 |
| 5 | wechat_author 枚举值有效 | core_values ∈ {开放, 保守, 批判, 建设, 中立, 激进, 务实, 理想}；emotion_expression ∈ {克制, 适度, 丰富, 强烈, 内敛, 外放, 层次, 爆发}；expected_tone ∈ {犀利批判, 温和启发, 幽默调侃, 严肃分析, 娓娓道来, 冷静克制} |
| 6 | wechat_article 人设阻塞校验 | 当 output_type == wechat_article 时，7 项必填字段未全部完成前，阻塞 T01d 及后续节点 |
