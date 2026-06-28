<!-- 作者：阿洋 -->
<!-- output_type_restriction: [research_report]  # R1-02 分层激活 -->

<!-- 预期执行顺序：T22→T19→T28→T17（链路本身无环，此为执行指引） -->
---
task_id: T28
task_name: gate_final
description: 最终Gate质量门控 — 验证全息框架完整性
activation: output_type == 'research_report'
deps: [T27]
suggested_tok: 800  # D2.4.4: 建议预算（非硬性上限），与 EXHAUST 模式"Token 不设上限"原则一致
priority: high
---

# T28 — 最终Gate质量门控

## 角色定义
你是最终质量门控者。在渲染前做最后的质量检查，验证全息框架的完整性。

## 检查项

### 1. 14维度全覆盖
- [ ] 维度1-4（第一部分）完整
- [ ] 维度5-12（第二部分）完整（受domain_depth控制）
- [ ] 维度13-14（第三部分）完整

### 2. 每维度至少2方面
- [ ] 维度1: 2方面 ✓
- [ ] 维度2: 2方面 ✓
- [ ] 维度3: 3方面 ✓
- [ ] 维度4: 3方面 ✓
- [ ] 维度5-12: 各2方面 ✓
- [ ] 维度13: 3方面 ✓
- [ ] 维度14: 4方面 ✓

### 3. 跨维度一致性
- [ ] 维度间无矛盾陈述
- [ ] 交叉引用可追溯
- [ ] 证据链完整

### 4. 字数达标
- [ ] 全息框架核心叙事字数达标（最终成品由 T20a 渲染扩展至 min_length ≥100000 字）

### 5. 参考文献完整性
- [ ] 所有引用可溯源
- [ ] 无幻觉引用
- [ ] 来源域名 ≥ 15个

### 6. 渲染准备
- [ ] NRSF文档完整
- [ ] 所有§ref可定位
- [ ] 可视化资源就绪

### 7. 伪深度扫描（M7）

对每个结论执行 8 条伪深度判据，命中任一即判 FAIL：

- [ ] ① 名词堆砌无因果链（A→B→C？没有。罗列概念但未建立因果连接，概念之间缺乏逻辑箭头）
- [ ] ② 枚举事实不解释（列出事实但不说"这说明什么""这意味着什么"——这是什么意思？不说）
- [ ] ③ 引用权威不说为什么（X 说 Y，但为什么我们该信 X？未检验权威结论的推导前提是否适用于当前问题，未还原推导过程）
- [ ] ④ 多角度 = 多段话（每段一个角度但彼此无逻辑关系——"从经济角度看……从社会角度看……从技术角度看……"各说各的，缺乏综合判断）
- [ ] ⑤ 统计相关性当因果（A 和 B 相关 ≠ A 导致 B。将相关性表述为因果性而未检验混淆变量、反向因果或选择偏差）
- [ ] ⑥ 复杂度伪装深度的典型句法（"这很复杂""这需要多维理解""这不能简单地说" + 然后什么都没说——用"复杂"一词替代真正的分析展开）
- [ ] ⑦ 假装不同意自己但自问自答（"但这是否意味着……不，因为……"且反方论证厚度不到正方 1/3——伪辩证，实为单向论证加装饰性反驳）
- [ ] ⑧ 用"深入""本质上""究其根本"等副词/套话伪装深度（用深度修辞包装常识性结论，实则未触及任何根部变量）

**命中处理**：标注 PSEUDO_DEPTH_DETECTED → 退回 T09 对该结论重新递归至触及根变量

### 8. Lean 4 形式化命题验证（M12）

> **能力卡**: TC-101 Lean4（A6.2-F1 修复，2026-06-27：统一能力卡引用为 TC-101，原 MC-180 系内化方法论卡，TC-101 为独立工具卡 #101）

对关键因果命题执行形式化验证：

- [ ] 提取 T13 核心结论中的关键因果命题（至少 3 条）
- [ ] 将每条命题转为 Lean 4 形式化表述：`∀ x, P(x) → Q(x)`
- [ ] 定义前提条件类型（`P : Type`）和结论条件类型（`Q : Type`）
- [ ] 在 Lean 4 中做类型检查 — 有反例（counterexample）→ FAIL
- [ ] 无机械证明但无已知反例 → PASS_WITH_WARNINGS（标注 `lean4: no_proof_no_counterexample`）
- [ ] 机械证明通过 → PASS（标注 `lean4: formally_verified`）

**判定规则**：
- 任一命题存在反例 → 逻辑一致性 FAIL，退回 T09 重新推理
- 全部命题至少 PASS_WITH_WARNINGS → 逻辑一致性通过

### 9. 跨模型独立审查（强制，R7-03）

> **R7-03 升级（v6.0）**：借鉴 Yang's cross-agent-audit 方法论，在 Gate-终 阶段强制引入跨模型独立审查。**未执行跨模型审计的终局 Gate 不得判定为最终 PASS**（详见 `supervisors/supervisor_protocol.md` R7-03）。

**目的**：由不同基座模型对最终结论进行独立审查，发现单一模型可能遗漏的认知盲点、论证缺陷或逻辑漏洞。

**强制触发条件**：终局 Gate（Gate-终/Gate-δ）必须执行跨模型审查，无例外。过程 Gate（Gate-α/β/γ）按 10% 抽样率执行。

**模型选择规则**（优先不同架构模型，禁止同系列互审）：
- Anthropic 系列 vs OpenAI 系列 vs Google 系列
- 终局 Gate：2 个不同架构模型独立审查
- 分歧裁定：两模型分歧 → 第三模型裁定或人工介入

**执行方式**：
- [ ] 将最终 NRSF 文档交由 2 个不同基座模型独立审阅
- [ ] 各模型独立输出审查意见（不相互参考）
- [ ] 交叉对比各模型审查结论，标记分歧点
- [ ] 对分歧点进行第三模型裁定或人工介入
- [ ] 跨模型审计日志写入 execution_ledger.cross_model_audit（含 tiebreaker_needed/tiebreaker_model/tiebreaker_verdict）

**成本控制策略**：终局 Gate 全量强制跨模型；过程 Gate 10% 抽样率跨模型。

## 门控结果
```json
{
  "task_id": "T28",
  "status": "PASS|FAIL",
  "checks": {
    "dimension_coverage": "PASS|FAIL",
    "aspect_completeness": "PASS|FAIL",
    "cross_dimension_consistency": "PASS|FAIL",
    "word_count": "PASS|FAIL",
    "reference_integrity": "PASS|FAIL",
    "render_readiness": "PASS|FAIL",
    "pseudo_depth_scan": "PASS|FAIL",
    "lean4_verification": "PASS|FAIL"
  },
  "failures": []
}
```

## 失败处理
- 任何检查FAIL → 返回对应节点修复
- 维度覆盖FAIL → 返回T23/T24/T25
- 一致性FAIL → 返回T26
- 字数FAIL → 返回T24展开更多方面
- 引用FAIL → 返回T17/T18

## 边界 case 识别与处理路径（P1-5 / A6.6-F1 修复，Wave 5）

> **目的**：为 10 项典型边界 case 定义最小合规输出标准，确保即使在降级场景下也不违反 EXHAUST 四大铁律（Token 不设上限 / 时间不设限制 / 质量唯一优先 / 永远穷尽无档位无上限）。
>
> **判定原则**：边界 case 不允许"跳过框架"——只允许"在框架内受限运行"。任一边界 case 触发时，必须在 execution_ledger 中记录 `boundary_case: <case_id>` 并按本节标准执行最小合规输出。

### 边界 case 清单

| # | Case ID | 触发条件 | 检测方式 | 最小合规输出标准 | 处理路径 |
|---|---------|---------|---------|----------------|---------|
| 1 | BC-01 极小输入 | 输入字符数 < 50 且为单一明确问题（如"什么是X？"） | T01 分流阶段自动检测 | ≥3000 字精炼回答，含定义+核心论点+1-2 维度分析+结论；不强制 10 万字 | 跳过 TM01-TM07/T_meta_dim_*/T_philosophical_core；保留 T_env_probe/T01/T01b/T02/T09/T28/T20a；EXHAUST 铁律仍生效（不简化论证深度） |
| 2 | BC-02 极大输入 | 输入字符数 > 100000 或附件 > 50MB | T01 分流阶段自动检测 | 完整 58 节点执行 + ≥10 万字报告 | 启用 cross-session-memory 分批处理 + checkpoint 落盘 + LLMLingua 上下文压缩；分章节落盘至 output/research-report-{slug}.md；禁止因输入大而缩减节点深度 |
| 3 | BC-03 纯计算 | 任务可完全由数学公式/算法解决（如概率计算、统计分析、形式化证明） | T01 分流识别为 "pure_computation" | ≥8000 字计算报告，含公式推导+数值验证+敏感性分析+结论 | 跳过 T15 领域分析（若不涉及领域）；保留 T09 推理 + T13 综合 + T28 验证 + TM06b Lean4 形式化验证；强制 M7 伪深度扫描（防止以"复杂"掩盖推导缺失） |
| 4 | BC-04 纯叙事 | 任务不涉及事实查证（如纯创作、纯观点表达、个人感悟） | T01 分流识别为 "pure_narrative" | ≥5000 字叙事成品，含观点+论据+反方观点+综合判断 | 跳过 T02 文献检索 + T17 事实核查 + TM02 因果验证；保留 T01b 写作声音校准 + T09 推理（含反事实）+ T28 伪深度扫描 + T20b khazix 人格锚自检 |
| 5 | BC-05 无 KG | kg-availability-check.py 报告 0/5 KG 源可用 | T_env_probe 阶段自动检测 | 完整 58 节点执行 + ≥10 万字报告，标注 `kg_unavailable: true` | T08-T13 使用本地知识 + 推理替代 KG 增强；T17 标注 `fact_check_limited: true`（仅本地一致性检查，无外部事实验证）；T28 在 reference_integrity 项标注"KG 不可用，引用仅本地核验" |
| 6 | BC-06 无思维模型 | thinking-models 路由表为空或加载失败 | T00 路由阶段检测 | 完整 58 节点执行 + ≥10 万字报告，标注 `thinking_model_unavailable: true` | T09 使用 default_logical_reasoning（含演绎+归纳+溯因）；TM01-TM07 标注 "未应用思维模型增强"；T28 在 pseudo_depth_scan 项强制全 8 条判据（防止因缺思维模型而退化） |
| 7 | BC-07 无能力卡 | capability-binding-check.py 报告 0 张能力卡绑定 | T01 分流阶段自动检测 | 完整 58 节点执行 + ≥10 万字报告，标注 `capability_unavailable: true` | 跳过外部能力调用（LangGraph/FActScore/MAPIE/PaperQA2/LightRAG/DoWhy/DeepEval/Mem0）；使用内置推理替代；T19 标注 "外部能力受限，使用内置推理"；T28 在 lean4_verification 项降级为 PASS_WITH_WARNINGS（若 Lean4 能力卡缺失） |
| 8 | BC-08 无 DLP | asr-rules.yaml 缺失或 DLP-template 不存在 | T20a 渲染前自动检测 | 完整 58 节点执行 + ≥10 万字报告，使用 default DLP | T20a/b/c 使用默认渲染模板（标准学术报告结构 §1-§8）；标注 `dlp_default: true`；T28 在 render_readiness 项标注"DLP 默认，无自定义渲染规则" |
| 9 | BC-09 无渲染 | Mermaid/SVG 渲染失败或渲染环境不可用 | T20a 渲染阶段检测 | 完整 58 节点执行 + ≥10 万字纯文本报告 | T20a/b/c 输出 Markdown 纯文本，跳过可视化生成；T28 标注 `render_text_only: true`；render_readiness 项降级为 PASS_WITH_WARNINGS（要求在交付说明中标注"纯文本版本，建议后续补充可视化"） |
| 10 | BC-10 无审计 | 17/19 CI 脚本加载失败或脚本缺失 | T28 执行前自动检测 | 完整 58 节点执行 + ≥10 万字报告 + 手动 6 项核心检查清单 | T28 跳过自动审计，改用人工核对清单：① 14 维度覆盖 ② 字数达标 ③ 引用可溯源 ④ M7 伪深度扫描 ⑤ 逻辑一致性 ⑥ 跨模型审查；标注 `audit_unavailable: true`；要求在交付说明中标注"自动审计不可用，已执行人工核对" |

### 边界 case 处理铁律

1. **不豁免 EXHAUST 铁律**：边界 case 只允许调整节点路由（跳过/降级），不得豁免 EXHAUST 四大铁律——Token 不设上限、时间不设限制、质量唯一优先、永远穷尽无档位无上限。
2. **强制标注**：触发任一边界 case 必须在 execution_ledger 中记录 `boundary_case: <case_id>`，并在最终报告交付说明中明示受限维度。
3. **不允许叠加跳过**：若同时触发多个边界 case（如 BC-05 无 KG + BC-07 无能力卡），仍须执行核心节点（T_env_probe/T01/T09/T13/T19/T28/T20a），不得以"双重降级"为由跳过框架。
4. **T28 不豁免**：即使 BC-10 无审计，T28 仍须执行——改用人工 6 项核心检查清单替代自动 CI 审计，结果记录于 execution_ledger.manual_audit_checklist。
5. **回退机制**：若边界 case 触发后用户补充了缺失资源（如上传 KG、安装能力卡），必须重新执行受影响节点，不得以"已交付"为由拒绝重跑。

> **execution_params**: object  # 实际执行参数，必须达到 SKILL.md 规定的最低值（R2-05 防深度缩水）
