<!-- 作者：阿洋 -->

# 字段依赖图（Field Dependency Graph）

> **强制规则**：任何字段被新增或改名时，MUST 检查此图上所有依赖该字段的文件并同步修改。违反此规则导致的跨文件不一致 SHALL 视为 P0 级 Bug。
>
> **SSOT 原则**：SKILL.md 是 DAG 拓扑的唯一真实源（Single Source of Truth）。本文档中的节点定义、名称、依赖关系均从 SKILL.md DAG 拓扑派生，不得独立定义。若本文档与 SKILL.md 冲突，以 SKILL.md 为准。

---

## 1. 三种产品类型路由

```
T01_input_triage（output_type 判定）
  │
  ├─→ research_report
  │     ├─→ T00_outline（学术研究大纲，≥100000字目标）
  │     ├─→ SearXNG 引擎策略：学术研究（arxiv, google_scholar, pubmed, crossref, semantic_scholar）
  │     ├─→ T20a 主渲染器（Typst → WeasyPrint 研究报告版式）
  │     ├─→ Persona 系统：researcher（persona-init-protocol.md 自动推断）
  │     └─→ Gate-终 检查：学术规范、引用完整性、方法论述评
  │
  ├─→ wechat_article
  │     ├─→ T00_outline（公众号文章大纲，≥3000字目标，5阶段叙事结构）
  │     ├─→ SearXNG 引擎策略：综合信息（google, duckduckgo, bing, wikipedia, wikidata）
  │     ├─→ T20b_wechat_render 独立渲染器（5阶段叙事 + 钩子开头 + 互动结尾）
  │     ├─→ Persona 系统激活（wechat_author 人格注入）
  │     └─→ Gate-终 检查：可读性、传播性、钩子质量、合规性
  │
  └─→ course_material
        ├─→ T00_outline（课程材料大纲，按模块数量弹性）
        ├─→ SearXNG 引擎策略：学术研究 + 综合信息（两者合并）
        ├─→ T20c 渲染器（Marp 幻灯片 / Typst PDF）
        ├─→ Persona 系统激活（educator 人格注入）
        └─→ Gate-终 检查：教学逻辑、模块衔接、习题完整性
```

## 2. NRSF 全链路（T02-T16 → T22-T28 + TM01-TM07）

> **SSOT 参照**：本节所有节点定义、名称、依赖关系均从 SKILL.md DAG 拓扑派生。完整拓扑见 SKILL.md "DAG 拓扑 — 唯一真实源" 区块。

```
NRSF-Full（叙事研究状态文件 —— 全量笔记）
  │
  ├─→ Phase 1: 研究底座（T02-T06）
  │     ├─→ T02（L1+L2）产出 → NRSF-Full §T02
  │     ├─→ T03（L3）产出 → NRSF-Full §T03
  │     ├─→ T04（L4+L5）产出 → NRSF-Full §T04
  │     ├─→ T05（L6+L7）产出 → NRSF-Full §T05
  │     └─→ T06（L8+L9）产出 → NRSF-Full §T06
  │
  ├─→ Phase 2: 认知流水线（T08-T13）
  │     ├─→ T08（认知解构）产出 → NRSF-Full §T08
  │     ├─→ T09（多路径推理）产出 → NRSF-Full §T09
  │     ├─→ T10（逻辑攻击）产出 → NRSF-Full §T10
  │     ├─→ T11（证据攻击）产出 → NRSF-Full §T11
  │     ├─→ T12（范围攻击）产出 → NRSF-Full §T12
  │     └─→ T13（认知综合）产出 → NRSF-Full §T13
  │
  ├─→ Phase 3: 领域分析（T15-T16）
  │     ├─→ T15（领域引擎分析）产出 → NRSF-Full §T15
  │     └─→ T16（Gate-γ 门控）产出 → NRSF-Full §T16
  │
  ├─→ Phase 5: 元维度引擎（T22-T28）—— 仅 research_report
  │     ├─→ T22（NRSF叙事综合）消费 NRSF-Full §T02-§T19 → 产出 → NRSF-Full §T22
  │     ├─→ T23（全息框架第一部分-问题认知与定义）消费 NRSF-Full §T22 → 产出 → NRSF-Full §T23
  │     ├─→ T24（全息框架第二部分-全维全域分析）消费 NRSF-Full §T23 → 产出 → NRSF-Full §T24
  │     ├─→ T25（全息框架第三部分-极限决策推理）消费 NRSF-Full §T24 → 产出 → NRSF-Full §T25
  │     ├─→ T26（跨维度洞察抽取）消费 NRSF-Full §T25 → 产出 → NRSF-Full §T26
  │     ├─→ T27（14维度关系可视化）消费 NRSF-Full §T26 → 产出 → NRSF-Full §T27
  │     └─→ T28（Gate-终 最终质量门控）消费 NRSF-Full §T27 → 产出 → 门控判定
  │
  ├─→ Phase 5: 科学层（TM01-TM07）—— 仅 research_report + system_dynamics_required
  │     ├─→ TM01（系统动力学仿真与反馈回路建模）消费 T28 通过 → 产出 → TM01 输出
  │     ├─→ TM02（因果验证 DoWhy/EconML/Pyro）消费 TM01 完成 → 产出 → TM02 输出
  │     ├─→ TM03（多智能体对抗性综合）消费 TM02 完成 → 产出 → TM03 输出  ┐
  │     ├─→ TM04（场景规划 EMA+CIB+CLA+3Horizons）消费 TM02 完成 → 产出 → TM04 输出  ├ R4-01 并行（deps: [TM02]）
  │     ├─→ TM05（元认知反思 MetaNet+ENA+Cynefin）消费 TM02 完成 → 产出 → TM05 输出  ┘
  │     ├─→ TM06（14 维 + 元维度扩展验证）消费 TM03+TM04+TM05 全部完成 → 产出 → TM06 输出  # R4-01 汇聚并行
  │     └─→ TM07（知识图谱导出 OWLAPY+SSSOM+PyKEEN+Neo4j）消费 TM06 完成 → 产出 → TM07 输出
  │
  └─→ NRSF-Summary（叙事研究摘要 —— ≤ 8000 字）
        ├─→ Mem0 存储（原子添加，语义 + 关键词 + 实体三路检索）
        ├─→ 各 Gate 节点消费 NRSF-Summary 进行完整性/深度检查
        ├─→ Context 窗口不足时作为代理加载
        └─→ nrsf-protocol.md（并发写入协议：tmp 文件 + Orchestrator 合并）
```

## 3. Phase 5 节点定义速查（从 SKILL.md DAG 派生）

> **SSOT 参照**：完整节点定义（node_id、dependencies、tok、route、executor 等 9 字段）见 SKILL.md "DAG 拓扑 — 唯一真实源" 区块。本节仅提供字段消费/产出速查。

### 3.1 元维度引擎（T22-T28）

| 节点ID | SSOT 名称 | 消费字段 | 产出字段 |
|--------|----------|---------|---------|
| T22 | NRSF叙事综合（全息框架3部分） | NRSF-Full §T02-§T19, context_package | NRSF-Full §T22, nrsf_append |
| T23 | 全息框架第一部分-问题认知与定义（4维度） | NRSF-Full §T22 | NRSF-Full §T23, nrsf_append |
| T24 | 全息框架第二部分-全维全域分析（8维度） | NRSF-Full §T23 | NRSF-Full §T24, nrsf_append |
| T25 | 全息框架第三部分-极限决策推理（2维度） | NRSF-Full §T24 | NRSF-Full §T25, nrsf_append |
| T26 | 跨维度洞察抽取（14维交叉） | NRSF-Full §T25 | NRSF-Full §T26, nrsf_append |
| T27 | 14维度关系可视化（3种图表） | NRSF-Full §T26 | NRSF-Full §T27, nrsf_append |
| T28 | Gate-终 最终质量门控（8项检查） | NRSF-Full §T27 | 门控判定（PASS/FAIL） |

### 3.2 科学层（TM01-TM07）

> **R4-01 依赖重构（v6.0）**：TM03/TM04/TM05 改为并行（均 deps: [TM02]），TM06 deps: [TM03, TM04, TM05] 汇聚三路并行结果。关键路径从 7 节点缩短为 4 节点。TM06b（Lean4）与 TM07 保持 deps: [TM06] 不变。

| 节点ID | SSOT 名称 | 消费字段 | 产出字段 |
|--------|----------|---------|---------|
| TM01 | 系统动力学仿真与反馈回路建模 | T28 门控通过 | TM01 输出 |
| TM02 | 因果验证（DoWhy/EconML/Pyro） | TM01 输出 | TM02 输出 |
| TM03 | 多智能体对抗性综合 | TM02 输出 | TM03 输出 |
| TM04 | 场景规划（EMA+CIB+CLA+3Horizons） | TM02 输出 | TM04 输出 |
| TM05 | 元认知反思（MetaNet+ENA+Cynefin） | TM02 输出 | TM05 输出 |
| TM06 | 14 维 + 元维度扩展验证 | TM03+TM04+TM05 输出 | TM06 输出 |
| TM06b | Lean4 形式化验证（v6.0 新增） | TM06 输出 | lean4_verification_report |
| TM07 | 知识图谱导出（OWLAPY+SSSOM+PyKEEN+Neo4j） | TM06 输出 | TM07 输出 |
| T_gate_delta | Gate-δ 科学层门控 | TM07 + TM06b + T_philosophical_core + T_meta_dim 节点 | 门控判定（PASS/FAIL） |

### 3.3 哲学与元维度扩展节点

| 节点ID | SSOT 名称 | 路由状态 |
|--------|----------|---------|
| T_philosophical_core | 哲学三元组审查（本体论/认识论/价值论） | research_report (always) |
| T_meta_dim_9_10 | 元维度9-10：无知之学+认知神经心理学 | research_report (always) |
| T_meta_dim_11_12 | 元维度11-12：二阶方法论+深度时间思维 | research_report (always) |
| T_meta_dim_13_14 | 元维度13-14：悲剧性智慧+知识生命体化 | research_report (always) |

## 4. 三路渲染输出

```
T20_output_render（输出渲染 —— 路由分发）
  │
  ├─→ T20a（research_report 渲染）
  │     ├─→ 消费：NRSF-Full §T02-§T28 + T13 core_conclusions
  │     ├─→ 渲染引擎：Typst 0.13+ → WeasyPrint PDF
  │     ├─→ 版式：学术研究报告（≥100000字，含摘要、方法、结果、讨论、参考文献）
  │     ├─→ 插图：illustration-generator.md + chart-renderer.md（Observable Plot + ECharts）
  │     ├─→ 美学增强：aesthetic-enhancer.md
  │     └─→ 输出：PDF 研究报告
  │
  ├─→ T20b_wechat_render（wechat_article 渲染）
  │     ├─→ 消费：NRSF-Full §T02-§T28 + T13 core_conclusions
  │     ├─→ 渲染引擎：独立渲染器（5阶段叙事结构）
  │     ├─→ 叙事结构：钩子开头 → 问题展开 → 深度分析 → 观点升华 → 互动结尾
  │     ├─→ Persona 注入：wechat_author 人格（口语化、故事化、互动化）
  │     ├─→ 版式：微信公众号兼容格式（≥3000字）
  │     └─→ 输出：Markdown 公众号文章
  │
  └─→ T20c（course_material 渲染）
        ├─→ 消费：NRSF-Full §T02-§T28 + T13 core_conclusions
        ├─→ 渲染引擎：Marp 幻灯片 / Typst PDF
        ├─→ 结构：模块化课程（按 T00 大纲模块拆分）
        ├─→ Persona 注入：educator 人格（教学化、渐进式、互动式）
        ├─→ 版式：幻灯片 + 讲义 + 习题集
        └─→ 输出：Marp HTML / Typst PDF

T20_output_guard（输出卫士）
  ├─→ 正则/关键词扫描元数据泄露
  └─→ T20d_cross_media_review 消费

T20d_cross_media_review（跨媒体审校）
  ├─→ 排版渲染 + 成品打包
  ├─→ 字体穷尽尝试链（霞鹜文楷 → 未来荧黑 → Fusion Pixel → 系统字体）
  └─→ SHA-256 哈希（研究完整性防伪）
```

## 5. Gate 门控链路

```
Gate-α（研究底座门控） → T07_gate_alpha
  │
  ├─→ 检查对象：T02-T06 NRSF 完整性
  ├─→ 检查维度：
  │     ├─→ 来源多样性（L0/L1/L2/L3 覆盖度）
  │     ├─→ 搜索合规性（SearXNG 多引擎聚合、Meilisearch 历史检索）
  │     ├─→ 事实完整性（factual_checklist ≥ 25、timeline_table ≥ 10）
  │     └─→ 数据缺口诚实度（data_gaps_marked 非空）
  ├─→ 失败 → 穷尽尝试 T02-T06 对应节点重执行
  └─→ 通过 → 放行至 T08 认知流水线

Gate-β（认知流水线门控） → T14_gate_beta
  │
  ├─→ 检查对象：T08-T13 NRSF 完整性 + I01 迭代深化
  ├─→ 检查维度：
  │     ├─→ 推理深度（7 条路径独立性、推理链步数 ≥ 7）
  │     ├─→ 对抗充分性（T10/T11/T12 攻击向量覆盖率）
  │     ├─→ 认知综合质量（CL1-CL6 跃迁记录、C1-C7 收敛清单）
  │     └─→ 深度信号处理（depth_signal.triggered 是否正确响应）
  ├─→ 失败 → 穷尽尝试 I01/T10-T12 对应节点重执行
  └─→ 通过 → 放行至 T15 领域分析

Gate-γ（领域分析门控） → T16_gate_gamma
  │
  ├─→ 检查对象：T15 领域引擎分析
  ├─→ 检查维度：
  │     ├─→ 领域-认知一致性（T15 各引擎结论 vs T13 核心结论）
  │     ├─→ 领域覆盖度（T01 推荐引擎全部激活、关键领域无遗漏）
  │     └─→ 跨领域交叉验证（≥ 2 对交叉比对、矛盾已调和）
  ├─→ 失败 → 穷尽尝试 T15 重执行
  └─→ 通过 → 放行至 T17 质量保障

Gate-δ（科学层门控） → T_gate_delta
  │
  ├─→ 检查对象：TM01-TM07 + TM06b（Lean4 形式化验证，proved_rate ≥ 0.8）+ T_philosophical_core + T_meta_dim 节点
  ├─→ 检查维度：
  │     ├─→ 科学层全面验证（系统动力学、因果链、多智能体、场景规划）
  │     ├─→ 哲学审查完备性（本体论/认识论/价值论）
  │     ├─→ 元维度一致性（无知之学、认知神经心理学、二阶方法论等）
  │     ├─→ 因果链正确性（DoWhy/EconML/Pyro 验证通过）
  │     ├─→ 场景规划有效性（EMA+CIB+CLA+3Horizons 覆盖）
  │     ├─→ 元认知自洽性（MetaNet+ENA+Cynefin 一致性）
  │     └─→ 知识图谱完整性（OWLAPY+SSSOM+PyKEEN+Neo4j 导出）
  ├─→ 失败 → 穷尽尝试对应失败层，持续退回重试直至通过
  └─→ 通过 → 放行至 T20/T21 输出渲染

Gate-终（最终输出门控） → T28
  │
  ├─→ 检查对象：T20 渲染输出
  ├─→ 检查维度：
  │     ├─→ research_report：学术规范、引用完整性、方法论述评
  │     ├─→ wechat_article：可读性、传播性、钩子质量、合规性
  │     └─→ course_material：教学逻辑、模块衔接、习题完整性
  ├─→ 失败 → 穷尽尝试 T20 对应渲染器重执行
  └─→ 通过 → 交付最终产品
```

## 6. Persona 系统（覆盖全部 3 种 output_type）

> **SSOT 参照**：Persona 系统由 SKILL.md §0.0 前置执行（Step -1）统一初始化，配置文件为 `persona/persona-init-protocol.md` + `persona/persona-schema.yaml`。

```
Persona 初始化（Phase -1，所有 output_type 强制激活）
  │
  ├─→ output_type = research_report
  │     ├─→ Persona 类型：researcher（persona-init-protocol.md 自动推断）
  │     ├─→ 注入节点：无（学术中立风格，不注入口语化 persona）
  │     └─→ 配置文件：persona/persona-init-protocol.md + persona-schema.yaml
  │
  ├─→ output_type = wechat_article
  │     ├─→ Persona 类型：wechat_author（persona-init-protocol.md 自动推断）
  │     ├─→ 注入节点：T20b_wechat_render
  │     ├─→ 特征：
  │     │     ├─→ 口语化表达（"你"、"咱们"、"说实话"）
  │     │     ├─→ 故事化叙事（案例引入 → 冲突展开 → 洞察揭示）
  │     │     ├─→ 互动式结尾（提问、投票、留言引导）
  │     │     └─→ 钩子开头（前 3 句抓住注意力）
  │     └─→ 配置文件：persona/persona-init-protocol.md + persona-schema.yaml
  │
  └─→ output_type = course_material
        ├─→ Persona 类型：educator（persona-init-protocol.md 自动推断）
        ├─→ 注入节点：T20c
        ├─→ 特征：
        │     ├─→ 教学化语言（"我们先来看"、"请思考"、"小结一下"）
        │     ├─→ 渐进式结构（概念 → 案例 → 练习 → 总结）
        │     ├─→ 互动式设计（思考题、讨论题、课后作业）
        │     └─→ 模块化组织（每模块含学习目标、核心内容、检验题）
        └─→ 配置文件：persona/persona-init-protocol.md + persona-schema.yaml
```

## 7. DAG 节点链路

见 SKILL.md DAG 拓扑定义（58 节点完整 YAML 块）。

## 8. 质量保障链路

```
T17_quality_factcheck（CoVe 级联事实核查）
  ├─→ 输出 confidence_summary + requires_annotation
  └─→ T19_quality_delivery 消费

T18_quality_bias（偏见检测 + 风格检查）
  └─→ T19_quality_delivery 消费

T19_quality_delivery（交付守卫）
  └─→ T19b_prescription_gate → T20_output_render
```

## 变更检查清单

当修改以下字段时，必须同步更新所有消费该字段的文件：

| 字段名 | 定义位置 | 消费位置 |
|--------|---------|---------|
| output_type | T01_input_triage.md, SKILL.md | T00_outline.md, tasks/T20a_research_render.md, T20b_wechat_render.md, tasks/T20c_course_render.md, handoff-protocol.md, searxng-adapter.md |
| context_package | handoff-protocol.md | 所有 DAG 节点 |
| confidence_summary | T17_quality_factcheck.md, T19_quality_delivery.md | tasks/T20a_research_render.md |
| NRSF-Summary | nrsf-protocol.md | Gate checks, I01, T20 |
| persona_config | persona/persona-init-protocol.md, persona/persona-schema.yaml | T20b_wechat_render.md, tasks/T20c_course_render.md |
| nrsf_append | T02-T06, T08-T13, T15, T16 | NRSF-Full, nrsf-protocol.md |
| 备注 | | |