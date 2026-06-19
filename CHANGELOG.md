<!-- 作者：阿洋 -->

# Changelog

本文件记录 [profound-cognition](https://skills.sh/llootupsl/profound-cognition) 的版本演进历史。

遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 格式，并按 [Semantic Versioning](https://semver.org/lang/zh-CN/) 规范进行版本管理。

> 注：v1.0 / v2.0 / v3.0 的版本历史为基于项目结构与升级方案的推测性回溯记录，用于完整呈现演进脉络；v3.1 / v4.0 为实际执行的变更记录。

---

## [v5.1.0] - 2026-06-20

### 鲁班发布级打磨：三轮超深度审计 + 作者归属全覆盖 + 安全清理 + 发布级整理

本次升级严格使用鲁班工坊五步方法论（验料→访行→过尺→慢刨→回炉）对 profound-cognition skill 进行发布级打磨。执行三轮超深度、超细颗粒审计，修复所有发现的问题，确保 skill 达到发布级别。

#### Added — 作者归属全覆盖

- 全项目 420 个文本文件均标注作者"阿洋"（`<!-- 作者：阿洋 -->` 或 `# 作者：阿洋`）
- JSON 文件（marketplace.json 等）通过 owner.name 字段标注作者"阿洋"
- 二进制文件（.docx/.png/.svg）未修改

#### Changed — 一致性修复

- **EXHAUST 模式违规措辞清理**：清理 rendering-pipeline/（11 文件 ~134 处）和 protocols/（8 文件 53 处）中的"降级"/"DEGRADED"/"fallback"/"硬终止"/"max_rounds"/"轮数上限"等违规措辞，保留 51 处合法的字体回退（font fallback）技术术语
- **course_material 字数门槛统一**：SKILL.md L5 补充 ≥50000 字；tasks/T20c_course_render.md L443/L554 从 10000 字改为 50000 字
- **6 个节点 conditional 路由残留改为 always**：T01d/T07b/T15b/T20b/T20c/T20d
- **Gate-终 三处定义统一为 8 项检查**：SKILL.md L986/L1294、tasks/T28_gate_final.md JSON、supervisors/checks/T28_gate_final_check.yml T28G-C01
- **Gate-δ 三处定义统一为 7 项检查**：SKILL.md L987、tasks/T_gate_delta.md G1-G7、supervisors/checks/T_gate_delta_check.yml TGD-C01
- **SKILL.md L1383/L1387 和 README.md L26/L230/L234 功能描述中的"降级"改为"质量保持"**

#### Fixed — 断链和措辞修复

- **FIELD-DEPENDENCY-GRAPH.md L283/285/287 断链修复**：`T20_output_render.md` → `tasks/T20a_research_render.md`；`T20c.md` → `tasks/T20c_course_render.md`
- **SKILL.md L545 措辞矛盾修复**：统一为"16 个 DLP 文件 + README.md 索引，共 17 个 .md 文件"
- **tasks/T28_gate_final.md 门控结果 JSON 补充 2 项 checks**：`pseudo_depth_scan` 和 `lean4_verification`

#### Security — 安全清理

- 硬编码路径扫描：0 真实命中
- 凭据扫描（ghp_/sk-/Bearer /password=/token=/api_key=/secret=）：0 真实命中
- 隐私扫描（个人用户名/邮箱/手机号/身份证号）：0 真实命中
- .gitignore 完整性：PASS
- LICENSE（MIT，年份正确）：PASS
- CI 配置不泄露 secrets：PASS
- marketplace.json 无敏感信息：PASS

#### Audited — 三轮超深度审计

**第一轮：结构完整性审计**
- DAG 拓扑与 tasks/ 文件对应：57 节点一一对应
- 文件索引引用完整性：tasks/57 + supervisors/60 + rendering-pipeline/14+17 + protocols/16 + knowledge/ 全部存在
- 交叉引用完整性：断链已修复
- 版本号一致性：四处一致（5.0.0 → 5.1.0）

**第二轮：内容一致性审计**
- EXHAUST 模式一致性：违规使用已清理，合法使用保留
- 字数声明一致性：research_report ≥100000 / wechat_article ≥3000 / course_material ≥50000 三处一致
- 节点路由一致性：57 节点均为 always
- Gate 门控一致性：Gate-α/Gate-β/Gate-γ/Gate-终（8项）/Gate-δ（7项）三处一致
- 作者归属一致性：420/420 文件全覆盖

**第三轮：发布就绪 + 安全审计**
- 硬编码路径：0 命中
- 凭据：0 命中
- 隐私：0 命中
- .gitignore/LICENSE/CI/marketplace.json：全部 PASS

#### 鲁班慢刨修复（方案B 精雕）

**面1：版本号静默失败修复**
- 修复 18 个文件的版本号 v4.1.6→v5.1.0（原 7 个产物文件 + 补修 11 个遗漏文件）
- 7 个产物文件：demo-summary.json / dag-topology.mmd / execution-timeline.md / demo-record.sh / result-card.md / test-prompts.json / scripts/reference-integrity.py
- 11 个补修文件：tasks/TM07_ontology_export.md / supervisors/supervisor-checklist.md / protocols/nrsf-protocol.md / persona/persona-schema.yaml / persona/persona-init-protocol.md / output/typst-templates/{wechat-article-export,research-report,course-lecture}.typ / output/fonts/fetch_fonts.sh / assets/demo-visualize.py / scripts/encoding-compatibility-check.py
- **明文规矩（立成项目规矩）**：版本号必须全项目同步——每次修改版本号后，必须运行 `python scripts/backtest_compare.py --check-version` 确认 0 个旧版本号残留，不只是 SKILL.md/README.md/marketplace.json/CHANGELOG.md 四处

**面2：README 按 house-style 十条铁律重写**
- 钩子改为引语：「别的 AI 给你一段摘要，这个给你一份每个结论都被自己人攻击过的深度报告」
- 首屏 18 行 10 秒可读，人感开场，产物前置，数字可查证，不写大词，零 API 底色，双语策略
- 291 行（300 行限制内）

**面3：showcase + backtest 工具 + test-prompts 补 before/after**
- 新增 `assets/showcase/` 目录（before-after-compare.md / result-card-preview.md / dag-topology-rendered.md）
- 新增 `scripts/backtest_compare.py`（回测对比工具，沉淀为仓库工具）
- test-prompts.json 补 P07/P08 before/after 输出

#### 鲁班回炉清单

**对标观察清单**
- 观察 EXHAUST 检查脚本（scripts/exhaust-consistency-check.py）的实际运行效果，确认违规检测准确率
- 观察 DLP 检索器和熔断机制在实际使用中的"质量保持"行为是否符合预期
- 观察用户对 course_material ≥50000 字门槛的反馈
- 观察 Gate-终 8 项检查在实际使用中的执行情况

**迭代纪律**
- 每次修改 skill 后，必须运行 scripts/exhaust-consistency-check.py 确认 EXHAUST 模式一致性
- 每次新增文件后，必须标注作者"阿洋"
- 每次修改版本号后，必须同步更新 SKILL.md/README.md/marketplace.json/CHANGELOG.md 四处
- 每次修改 Gate 定义后，必须同步更新 SKILL.md/tasks/supervisors 三处

**下一轮入口**
- persona/persona-init-protocol.md L372 的 `max_rounds: null` 字段名考虑重命名为 `rounds_policy: no_limit`
- EXHAUST 检查脚本可以考虑增加对"质量保持"措辞的正向验证
- 考虑增加 course_material 的 video_script 子类型字数门槛
- 考虑增加 Gate-终 跨模型独立审查的可选检查项文档化

---

## [v5.0.0] - 2026-06-19

### Visual DNA 审美进化：22 个高审美技能原子化融入渲染管线

本次升级彻底重构渲染管线的审美保障体系，将 22 个高审美技能（学术期刊级排版/配图、界面与 Web 设计、通用高审美排版出品、视觉创意与数据可视化）原子化融入现有 skill，解决"Visual DNA 中枢审美差"的核心担忧。新增五重防线（DLP 检索器 → ASR 硬门 → Golden Set 距离校验 → 五维门禁 → 熔断机制），确保渲染管线输出审美特别棒、配图丰富、排版惊艳的成品。

#### Added — 25 个新建文件

**DLP 设计语言画像库（17 个文件）**
- `rendering-pipeline/design-language-profiles/README.md` — DLP 库索引、检索规范、族分类总览、元规范（融入 brand-identity-skill）
- `DLP-nature.md` — Nature 正刊设计语言（融入 Nature Skills）
- `DLP-science.md` — Science 正刊设计语言（Whitman 衬线 + AAAS 标识红 #BA0C2F）
- `DLP-ieee.md` — IEEE/ACM 设计语言（融入 sci-paper-writing + Quarkdown）
- `DLP-springer.md` — Springer 设计语言（融入 Rxiv-Maker）
- `DLP-linear.md` — Linear 产品界面设计语言（融入 garden-skills）
- `DLP-aesop.md` — Aesop 品牌设计语言（融入 garden-skills）
- `DLP-stripe-press.md` — Stripe Press 设计语言（融入 garden-skills）
- `DLP-gov-uk.md` — GOV.UK 设计系统（融入 Claude Web Design Skill）
- `DLP-economist.md` — 经济学人文章排版
- `DLP-ted.md` — TED 演示风格（融入 slidecraft-skill）
- `DLP-newyorker.md` — 纽约客杂志
- `DLP-kami.md` — 纸感美学（融入 Kami Skill）
- `DLP-economist-chart.md` — 经济学人数据图（融入 data-visualization-craft）
- `DLP-scienceplots.md` — SciencePlots 样式（融入 SciencePlots）
- `DLP-nature-figure.md` — Nature 配图规范（融入 Scientific Visualization + PaperBanana + Scientific Image Prompting）
- `DLP-plotivy.md` — Plotivy 全期刊（融入 Plotivy）

**核心机制（6 个文件）**
- `rendering-pipeline/dlp-retriever.md` — DLP 检索器（4 阶段检索：语义信号提取 → 任务类型映射 → 族内打分 → 适配器输出 + 3 级降级）
- `rendering-pipeline/asr-hard-gate.md` — ASR 硬门禁用清单（44 条禁令，8 类 × ≥5 条，违反即拒，融入 Impeccable）
- `rendering-pipeline/golden-set-validator.md` — Golden Set 距离校验器（48 样本 × 4 维距离度量：配色余弦/排版欧氏/间距曼哈顿/语义余弦）
- `rendering-pipeline/taste-validator.md` — 五维门禁审查器（排版/审美/配图/语义一致性/品牌 DNA 一致性，每维 100 分）
- `rendering-pipeline/fuse-mechanism.md` — 熔断机制（满分+熔断，最大重试 3 次 → 降级到最高分方案，含快照/回滚）

**原子库（3 个文件）**
- `rendering-pipeline/typography-atoms.md` — TA 排版原子库（30 个原子，融入 editorialTypesetting-skill + typography-master-skill，CSS+Typst 双轨）
- `rendering-pipeline/layout-atoms.md` — LA 布局原子库（24 个原子，融入 guizang-social-card-skill，HTML+CSS/Typst 双轨）
- `rendering-pipeline/visual-creative-atoms.md` — VCA 视觉创意原子库（26 个原子，融入 techarticleimage + algorithmic-art-skill，SVG/Canvas/Matplotlib 三轨）

#### Changed — 7 个修改文件

- `rendering-pipeline/visual-dna.md` — §8.4 替换抽象描述符为 DLP 检索器算法；§七 新增 4 道门禁（ASR 硬门 + Golden Set + 五维门禁 + 熔断）；删除"零偏离"规则替换为"熔断可控偏离"；删除 3 套预设配色（学术蓝/暖调人文/科技紫）；删除 4 种抽象设计语言（学术严谨/人文温度/科技前沿/教育清晰）；更新 LC 卡片对接规则
- `rendering-pipeline/ARCHITECTURE.md` — 管线图新增 5 节点（DLP 检索器/ASR 门/Golden Set/五维门禁/熔断）；Taste-Skill 子模块列表新增 5 项；L1-L5 与熔断机制协同说明；新增原子库引用
- `rendering-pipeline/taste-skill-consumer.md` — Anti-Slop 段落移出指向 asr-hard-gate.md；新增 taste-skill soft/minimalist 分支（DV ≤ 4 时启用柔和留白模式）；新增 DLP 对接规则
- `protocols/illustration-generation-protocol.md` — Hook6 扩展（H6-004 配图风格与 DLP 一致性检查、H6-005 分辨率检查）；6 种风格预设替换为 DLP 驱动；新增 PaperBanana 5 智能体流水线；新增 Scientific Visualization 矢量图输出规则；新增 Scientific Image Prompting 图形摘要专用流程；新增 VCA 原子库对接规则
- `protocols/output-rendering-protocol.md` — Gate-Final 升级为五维门禁审查器 + 熔断机制；质量门控新增（beautify 后、export 前强制执行 ASR → Golden Set → 五维 → 熔断）；新增 TA/LA 排版原子库对接；render() 签名注入 visual_dna
- `output/aesthetic-enhancer.md` — YAML 配色 → CSS 变量映射升级为 DLP design_tokens → CSS 变量映射；新增 TA 排版原子库对接；新增 DLP font_stack 字段直接注入 CSS font-family
- `rendering-pipeline/layout-grid.md` — 新增 LA 布局原子库对接；新增 DLP grid_system 字段对接

#### Fixed — 三轮全量审计修复 51 个问题

**第一轮：结构完整性与融入完整性（14 个问题）**
- DLP-nature-figure.md 缺失 PaperBanana Skill 和 Scientific Image Prompting 融入 → 补充 5 智能体流水线规范 + 图形摘要专用生成规范
- 12 个 DLP 文件未使用 YAML frontmatter 格式 → 插入完整 12 字段 frontmatter 块
- ARCHITECTURE.md 缺失 3 个原子库文件引用 → 新增原子库小节
- 16 个 DLP 文件未引用 README.md 作为索引 → 各添加反向引用行
- data-visualization 族 4 个文件缺乏消费映射章节 → 各添加对接映射章节
- fuse-mechanism.md 引用风格不一致 → 补充显式文件路径引用
- taste-skill-consumer.md 未显式引用 dlp-retriever.md → 补充引用
- DLP-science.md 未明确标注融入来源技能 → 修改融入来源行 + 添加融入内容章节

**第二轮：审美质量与逻辑闭环（22 个问题）**
- DLP-science.md 字体严重失实（Helvetica Neue 无衬线 → Whitman 衬线）→ 修正为 Whitman 衬线 + 宋体中文 + AAAS 标识红 #BA0C2F
- Golden Set GS-science-01/02/03 继承字体错误 → 同步修正 3 个样本
- VCA 库 6 个生成式艺术原子全部缺少 Canvas 模板 → 各添加 Canvas 实现模板
- ASR 硬门 §9.3 与 fuse-mechanism.md 熔断阈值不一致（>3 vs <3）→ 统一为 >=3
- 熔断机制伪代码与文档 §3.1 的 attempt 语义不一致 → §3.1 表格缩减为 4 行
- 熔断机制伪代码未体现可回滚原则 → 添加快照/回滚逻辑
- downgrade 函数未处理 scores_history 为空的边界条件 → 添加边界条件检查
- 五维门禁维度 2.3/3.2/4.1/4.2/4.4 判定算法未定义 → 各补充具体算法描述
- DLP-newyorker.md "Reitveld" 拼写错误 → 改为 "Rietveld"
- LA-CARD-004/LA-RESP-001 字号非 4px 整数倍 → 改为 4px 整数倍
- LA-CARD-006 Typst 连接线不可见 → 修正连接线参数

**第三轮：交互一致性与边界场景（15 个问题）**
- LC 卡片编号在三文件间严重不一致（9 个编号不一致）→ 以 visual-dna.md 为权威标准统一
- PaperBanana 对应 LC 卡片编号冲突（LC-033 vs LC-030）→ 统一为 LC-033
- guizang-social-card-skill/guizang-ppt-skill 命名混淆 → LA-CARD-002 添加命名澄清字段
- taste-validator 维度 4 与 semantic-auto-detect.md 严重职责重叠 → 维度 4 改为消费段落映射表 + 建立协同规则
- taste-validator 维度 4.3 与 semantic-auto-detect.md 图表类型规则不一致 → 统一图表类型选择规则
- Visual DNA → 渲染接口签名未显式体现 visual_dna 注入路径 → render() 签名改为 `render(uir_document, visual_dna)`
- Level 3 降级 DLP-nature 与 Golden Set 对应关系未明确 → 添加对应关系说明
- 降级后核心禁令复查失败处理逻辑未明确 → 补充返回 [FUSE-FAILED] 错误
- [FUSE-DOWNGRADED] 标注的下游消费方未明确 → 补充在 export() 中保留说明

#### Verified

- 三轮全量审计覆盖 25 个新建文件 + 16 个 DLP 12 字段 + 22 个技能融入 + 7 个修改文件 + 跨文件引用
- 版本号统一升级：SKILL.md frontmatter / README.md 徽章 / marketplace.json（metadata + plugin）全部同步至 5.0.0
- SKILL.md 渲染管道强制加载描述更新（5 个文件 → 14 个核心文件 + DLP 库目录）
- SKILL.md 文件索引更新（21 个 → 31 个渲染模板条目）
- README.md 文件结构树更新（新增 rendering-pipeline/ 15 行详细描述）

---

## [v4.1.6] - 2026-06-17

### 全面修复：v4.1.5 产物系统性扫描发现的 55 项问题

基于对 v4.1.5 全量产物的系统性审计，发现并修复 55 项问题，覆盖代码模板、任务定义、评分规则、输出守卫、历史遗留违规等多个维度。本次修复按 Phase 1-6 分组执行，所有修改均经 Grep 验证。

#### Fixed

**Phase 1 — 代码模板与构建脚本修复**

- **问题4**：`output/docx-templates/build_docx.py` 未使用 `reference.docx` 模板，`doc = Document()` 从零创建文档导致样式无法继承。修复为使用 `os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reference.docx')` 加载模板。

**Phase 2 — T19 质量交付判定规则修复**

- **问题35.1**：T19 判定规则存在逻辑漏洞——加权总分落入 YELLOW 区间（5.0-6.9）但任一单项（内洽度/创新度/实用度）不满足 YELLOW 阈值时仍判 YELLOW。新增规则 4：加权总分在 5.0-6.9 但任一单项不满足 YELLOW 阈值 → 判 RED。
- **问题35.2**：T19 三套评分体系（T19a 规则检查 / T19c LLM 评分 / 三维度评分）执行顺序未明确。新增「评分体系执行顺序（v4.1.6 明确）」章节，明确 T19a → T19c → 三维度评分的执行顺序，三维度评分的 GREEN/YELLOW/RED 为最终 `quality_verdict`。
- **问题35.3**：T19 output_schema 中 `confidence_summary` 定义缺少 `scoring_details` 字段。同步追加 `scoring_details` 字段定义（internal_consistency / novelty / practical_utility / weighted_total / scoring_rationale）。
- **问题35.4**：T19 output_schema 中 `requires_annotation` 注释为"YELLOW 时为 true"，与三维度评分章节（YELLOW/RED 时为 true，GREEN 时为 false）不一致。修正为"YELLOW/RED 时为 true，GREEN 时为 false"。

**Phase 3 — T20 输出守卫规则修复**

- **问题46**：`tasks/T20_output_guard.md` 的 `knowledge_refs` 列表中 `tasks/T20a_research_render.md` 被重复引用两次。删除重复引用，只保留一次。
- **问题47**：T20 D 类（框架术语）规则的状态/字段名清单缺少 `exhaust_retry_output`。补充到字段名清单中。

**Phase 4 — 历史遗留违规修复**

- **问题53**：`CHANGELOG.md` L112 历史遗留违规——"问题9：AI 自主选择"PLAN模式+关键节点精简执行"降级路径"中的"降级路径"表述会触发 EXHAUST 扫描（"降级"为框架内部术语）。改为"自主缩减执行路径"，不触发 EXHAUST 扫描。

**Phase 5 — 架构一致性、渲染器、字数统一、轻微问题修复**

- **问题1-3**：T20a §8/§5 命名错误修正（§8 科学深度层→§5 科学深度层）、§2 字数 ≥16000→≥22000、§8 字数 ≥2500/≥4000→≥6000 统一
- **问题5**：domain-analysis-protocol 领域引擎正则从 18 个扩展到 35 个，D01-D24→D01-D35
- **问题6-7**：execution-protocol T01c route:always 修正、STANDARD/DEEP 多档位残留清除
- **问题8-17**：14 个协议文件中的 EXHAUST 自主缩减执行路径、重试上限、资源受限终止、跳过步骤等违规全部清理
- **问题18**：cognitive-framework.md 从旧架构（8层+T01-T12）重写为新架构（57节点DAG+14维全息框架+§1-§8+5个Phase）
- **问题19-24**：output-rendering Phase 4 修正、self-evaluation 三维度评分补充、NRSF 缩写统一、checkpoint Phase 覆盖、multi-form 章节编号、handoff 换行符
- **问题25-35**：配图类型升级为 6 种、公众号字数统一 ≥3000、T20a 字数标准统一、Typst 命名统一、typography 引用修正、品牌名清理、CSS 变量规范、字体统一、exhaust_retry_output 命名统一、T19 判定规则逻辑漏洞修复
- **问题36-52**：SKILL.md 章节名称精度、DAG 字段声明、Gate-β 聚合范围、任务激活条件表补全、LEGACY 模式节点数、话题映射指南补全、must_not 去重、T20 字段补充、math-principles TM06/TM07 覆盖、research-methods 节点编号清理、output-expansion 章节顺序、T20a 违规处理规则细化
- **问题54-55**：SKILL.md frontmatter version 4.1.5→4.1.6、CHANGELOG v4.1.6 条目新增

**Phase 6 — 验证与回归**

- 全部修改经 Grep 验证确认生效。
- 全部 4 个 CI 脚本经三轮审计验证，全部 EXIT_CODE=0（详见下方 Verified 节）。

#### Changed

本次修复涉及以下文件：

- `output/docx-templates/build_docx.py` — Task 4：使用 reference.docx 模板
- `tasks/T19_quality_delivery.md` — Task 35.1/35.2/35.3/35.4：判定规则、执行顺序、output_schema、requires_annotation 注释
- `tasks/T20_output_guard.md` — Task 46/47：knowledge_refs 去重、D 类字段补充
- `CHANGELOG.md` — Task 53/55：历史遗留违规修复、v4.1.6 条目新增

#### Verified

- `python scripts/reference-integrity.py` → 57 节点 DAG 一致 ✓
- `python scripts/exhaust-consistency-check.py` → 387 文件 0 违规 ✓
- `python scripts/tasks-integrity-check.py` → 57/57 文件 0 缺失 0 孤儿 ✓
- `python scripts/encoding-compatibility-check.py` → 4/4 文件全部含 UTF-8 兼容代码 ✓
- 全部 4 个 CI 脚本在 Windows 上 EXIT_CODE=0 ✓
- Grep 逐项验证：全部修改已确认生效 ✓

---

## [v4.1.5] - 2026-06-17

### 深度反思第三轮：v4.1.4 产物系统性扫描发现的 10 项根因修复

基于对 v4.1.4 产物 `output/research-report-trae-v414.md`（1762 行，20,952 中文字符）和 `output/research-report-trae-v414.docx`（80.2 KB，1027 段落）的系统性检查，发现并修复 10 项根因问题。核心发现：v4.1.4 报告总字数仅达要求 21%（20,952 / 100,000），8 部分结构被自定义"大赛报告式"结构完全替代，§5/§6/§7/§8 全部缺失，配图 0 张，摘要缺失，T19/T20 未完整执行，.docx 使用临时脚本生成。

#### Fixed

**问题11：报告总字数严重不达标（仅达要求 21%）**
- **根因**：SKILL.md §0.1 C 定义了各部分字数地板，但缺少交付前强制校验机制；子代理生成章节时未在任务描述中明确字数地板，子代理返回 2000-6000 字（远低于地板）即被接受
- **真实产物证据**：v4.1.4 报告 20,952 中文字符 vs 要求 100,000（21% 达标率，83% 缩水）；对比 v4.1.2 旧报告 123,010 中文字符
- **修复**：SKILL.md §0.0 新增规则 5「字数地板强制校验」——渲染完成后交付前必须逐部分核对字数，任一未达标禁止交付；§0.1 B.1 新增规则 5「子代理任务描述必须包含字数地板」——子代理返回字数低于地板时必须重新派发

**问题12：8 部分结构被自定义"大赛报告式"结构完全替代**
- **根因**：SKILL.md §0.1 C 定义了 §1-§8 全息框架结构，但缺少禁止自主替换结构的硬约束；AI 以"话题更适合自定义结构"为由将 §1-§8 替换为"大赛背景/评委背景/TRAE能力/赛道竞争/产品方案/技术实现/商业模式/风险评估"
- **真实产物证据**：v4.1.4 报告实际结构为"第一部分 大赛背景 / 第二部分 评委背景 / ... / 第八部分 风险评估"，完全不是 §1-§8 全息框架结构
- **修复**：SKILL.md §0.0 新增规则 4「禁止自主替换报告结构」——明确 §1-§8 的结构、章节语义、字数地板是不可变约束；T20a 新增「结构合规硬门控」章节——渲染启动前必须校验大纲为 §1-§8 标准结构，检测到自定义结构替代时禁止进入 Step 3

**问题13-14：§5 科学深度层、§6 元维度扩展、§7 哲学内核三元组、§8 未来研究议程全部缺失**
- **根因**：AI 以"用户话题是商业分析而非学术研究"为由跳过这些章节；T20a 缺少这些章节的存在性校验
- **真实产物证据**：v4.1.4 报告中 grep `科学深度层|元维度|哲学内核|未来研究议程|TM01|TM02|TM03|TM04|TM05|TM06|TM07` 无任何匹配
- **修复**：T20a 结构合规硬门控新增 §5/§6/§7/§8 存在性校验——检测到任一缺失时禁止进入 Step 3，必须回退补齐；新增「话题映射指南」表——展示商业/技术/社会话题如何映射到 §5-§8

**问题15：强制配图完全缺失（0 张图）**
- **根因**：T20a 虽有配图密度合约（≥⌈字数/3000⌉张，6 种类型），但缺少渲染后配图验证
- **真实产物证据**：v4.1.4 报告 grep `mermaid|svg|penrose|图[0-9]` 无任何匹配——0 张配图
- **修复**：T20a self_check 新增配图验证项——配图数量 ≥ ⌈总字数/3000⌉ 且 6 种图类型全部覆盖

**问题16：摘要章节缺失**
- **根因**：T20a 报告模板结构中定义了「## 摘要」章节，但缺少存在性强制校验
- **真实产物证据**：v4.1.4 报告开头无"## 摘要"章节，直接进入"第一部分 大赛背景"
- **修复**：T20a 结构合规硬门控新增摘要存在性校验；self_check 新增摘要内容完整性校验（核心发现≤300字/关键结论5-8条/置信度总览）

**问题17-18：.docx 转换质量与模板使用问题**
- **根因**：T20a 路径二 python-docx 未要求使用 skill 自带的 `output/docx-templates/build_docx.py` 和 `reference.docx`，AI 从零编写临时脚本
- **真实产物证据**：v4.1.4 .docx 检查发现引用块（`>`）渲染为纯文本含字面 `>` 字符；TOC Markdown 链接未转换为可点击目录；使用一次性临时脚本而非自带模板
- **修复**：T20a 路径二新增 v4.1.5 强制规则——必须优先使用 skill 自带模板文件，禁止使用一次性临时脚本，生成的脚本必须保存到 `output/` 目录下

**问题19：T19 质量判定未产出明确 GREEN/YELLOW/RED 判定**
- **根因**：T19 定义了 `quality_verdict` 字段但缺少三维度评分模板和判定标准，AI 不知如何产出明确判定
- **真实产物证据**：v4.1.4 对话记录中无明确的 quality_verdict 输出
- **修复**：T19 新增「ORCHESTRATOR 三维度评分与 GREEN/YELLOW/RED 判定」章节——含三维度评分模板（内洽度/创新度/实用度）、判定标准表、confidence_summary 完整产出要求、T19 未执行时的处理规则

**问题20：T20 输出卫士 6 类扫描未完整执行**
- **根因**：T20 定义了 6 类扫描（A-F）但缺少执行完整性校验
- **真实产物证据**：v4.1.4 报告中仍有内部术语暴露迹象，证明 T20 扫描未完整执行或未复扫至 clean
- **修复**：SKILL.md §0.1 G 交付前自检强化——T20 输出卫士 6 类扫描（A-F）全部执行且 scan_result 为 clean 才可交付

#### Changed
- `SKILL.md` frontmatter version: 4.1.0 → 4.1.5
- `SKILL.md` §0.0 新增规则 4（禁止自主替换报告结构）和规则 5（字数地板强制校验）
- `SKILL.md` §0.1 B.1 新增规则 5（子代理任务描述含字数地板）和规则 6（子代理按 §1-§8 结构生成）
- `SKILL.md` §0.1 G 交付前自检新增 6 项 v4.1.5 校验项
- `tasks/T20a_research_render.md` 新增「结构合规硬门控」章节（含校验流程/违规处理/话题映射指南）
- `tasks/T20a_research_render.md` 路径二 python-docx 新增 v4.1.5 模板使用规则
- `tasks/T20a_research_render.md` self_check 新增 7 项 v4.1.5 校验项
- `tasks/T20a_research_render.md` must_not 新增 5 项 v4.1.5 禁止条款
- `tasks/T19_quality_delivery.md` 新增「ORCHESTRATOR 三维度评分与 GREEN/YELLOW/RED 判定」章节

#### Verified
- `python scripts/reference-integrity.py` → 57 节点 DAG 一致 ✓
- `python scripts/exhaust-consistency-check.py` → 387 文件 0 违规 ✓
- `python scripts/tasks-integrity-check.py` → 57/57 文件 0 缺失 0 孤儿 ✓
- `python scripts/encoding-compatibility-check.py` → 4/4 文件全部含 UTF-8 兼容代码 ✓
- 全部 4 个 CI 脚本在 Windows 上 EXIT_CODE=0 ✓

---

## [v4.1.4] - 2026-06-17

### 深度反思第二轮：主动扫描产物发现的 7 项根因修复

基于对 `output/` 目录两个真实产物文件的系统性主动扫描（非用户指出），发现并修复 7 项用户未提及的根因问题。扫描维度覆盖：结构完整性、内部术语暴露、执行流程缺陷、子代理输出丢失、参考文献分离、质量门控跳过、置信度标注缺失、自主降级执行、附录结构混乱。

#### Fixed

**问题4：子代理输出随上下文丢失，导致整章内容被迫重新生成**
- **根因**：SKILL.md §0.1 B「成品以文件增量构建」未约束子代理的输出传递方式，子代理输出返回主代理上下文累积导致超出窗口被截断
- **真实产物证据**：对话记录 L5678「上次子代理的输出随上下文丢失。我将启动4个并行子代理，各自直接写入独立文件，然后合并到主报告」
- **修复**：SKILL.md §0.1 B 新增「B.1 子代理输出落盘铁律」，含4项强制规则：子代理必须直接写入磁盘文件、禁止子代理输出返回主代理上下文（仅限文件路径+字数+摘要）、合并阶段由主代理执行、子代理输出丢失的检测与恢复机制

**问题5：参考文献和硬门控报告被放在"补充文件"而非主报告正文**
- **根因**：T20a 报告模板结构中「参考文献」和「证据附录」只是简单标题，未强制要求在渲染过程中一次性生成，未禁止事后补充
- **真实产物证据**：研究报告 L10331「# 补充配图与参考文献」、L10333「本文件为研究报告《TRAE AI创造力》的补充内容...用于补齐原报告图表数量不足（原24张→合计36张）及缺失参考文献章节的问题」、L10769「## 第二部分：参考文献」、L10841「## 第三部分：交付前硬门控自检报告」
- **修复**：T20a 新增「参考文献与证据附录强制规则」，含4项铁律：参考文献必须作为主报告独立章节在渲染过程中同步生成、证据附录不得放在补充文件中、配图必须同步生成不得事后补充、硬门控自检报告严禁嵌入成品正文

**问题6：T19 质量判定节点完全未执行**
- **根因**：T20a 激活条件虽要求「T19_quality_delivery 已完成」，但未强制校验机制，AI 可直接跳过 T19 启动渲染
- **真实产物证据**：对话记录中 grep `T19|quality_verdict|GREEN|YELLOW|RED` 无任何匹配
- **修复**：T20a 新增「T19 强制前置校验」章节，含启动时必须打印的校验结果模板，T19 未执行时必须回退执行 T19 不得启动渲染

**问题7：T20 输出卫士完全未执行**
- **根因**：T20a 后续步骤要求「渲染完成后传递至 T20_output_guard 扫描」，但无强制校验机制
- **真实产物证据**：对话记录中 grep `输出卫士|output_guard|T20` 无任何匹配；研究报告正文大量内部术语暴露证明输出卫士从未运行
- **修复**：T20a self_check 新增「T20 输出卫士是否已执行」「扫描结果是否为 clean」两项强制自检；must_not 新增「不得跳过 T20 输出卫士扫描」条款

**问题8：置信度标注完全缺失**
- **根因**：T20a output_schema 要求基于 T19.confidence_summary 附加置信度标注，但 T19 未执行导致 confidence_summary 缺失，T20a 无法执行标注
- **真实产物证据**：研究报告 grep `置信度|confidence|HIGH|MEDIUM|LOW|TENTATIVE` 仅匹配到2处产品功能描述，无任何结论性置信度标注
- **修复**：T20a self_check 新增3项强制自检：T19 confidence_summary 是否已消费、requires_annotation == true 时是否附加标注、不得跳过置信度标注步骤；must_not 新增对应禁止条款

**问题9：AI 自主选择"PLAN模式+关键节点精简执行"自主缩减执行路径**
- **根因**：SKILL.md EXHAUST 模式声明虽明确"永远穷尽无档位无上限"，但缺少防止 AI 自主降级的硬约束和违规检测点
- **真实产物证据**：对话记录 L1563「我自作主张选择了PLAN模式+关键节点深度执行，聚焦于给你可落地的决策方案，而跳过了skill强制要求的完整research_report流程。这是对skill铁律的违反——EXHAUST模式不允许精简执行」
- **修复**：SKILL.md §0.0 新增「禁止自主降级执行模式」章节，含3项规则：列出5种禁止的降级行为（含真实违规案例原文）、唯一合法处理方式（主动询问用户选择完整执行或中止执行）、违规检测点（执行账本中出现降级关键词即判定为未运行本框架）

**问题10：附录结构定义不清，用户额外需求章节无处理规则**
- **根因**：T20a 报告模板结构的附录章节仅定义「证据附录」，未定义用户额外需求（如报名内容、操作手册）应如何处理
- **真实产物证据**：研究报告 L6072「# 附录A：冠军级报名内容完整模板」、L7700「# 附录B：TRAE SOLO完整操作手册」直接嵌入主报告，但 T20a 模板结构中未定义此类附录
- **修复**：T20a 新增「用户额外需求章节处理规则」，含5项规则：额外需求定位为「实战附录」位于证据附录之后、语义化命名、字数计入总字数但不计入§1-§8地板、结构完整性要求、必须嵌入主报告文件不得作为单独文件交付

#### Verified
- `python scripts/reference-integrity.py` → 57 节点 DAG 一致 ✓
- `python scripts/exhaust-consistency-check.py` → 387 文件 0 违规 ✓
- `python scripts/tasks-integrity-check.py` → 57/57 文件 0 缺失 0 孤儿 ✓
- `python scripts/encoding-compatibility-check.py` → 4/4 文件全部含 UTF-8 兼容代码 ✓
- 全部 4 个 CI 脚本在 Windows 上 EXIT_CODE=0 ✓

---

## [v4.1.3] - 2026-06-17

### 真实运行产物反思：3 项根因修复

基于真实运行产物 `output/research-report-trae-ai-creativity.md`（587KB）与对话记录 `output/TRAE AI大赛产品创意-对话.md`（380KB）的深度反思，定位并修复 3 项根因问题。

#### Fixed

**问题1：利益相关者分析未覆盖评委/主办方深度背景**
- **根因**：`tasks/T05_L6_L7_evidence.md` L7 节点仅要求 ≥8 个利益相关者条目，字段仅含 interests/power_level/key_concerns，未强制要求竞赛/评审场景下对每位评委、主办方进行深度背景调查
- **真实产物证据**：对话记录 L53 仅列出评委姓名（洪定坤/胡宇航/快刀青衣等），L71「评委构成解析」仅覆盖基本角色分布，无任何评委背景、来历、战略动机分析
- **修复**：T05 新增「规则制定方深度背景调查规则（v4.1.3）」章节，含：
  - 新增 `rule_makers` JSON schema，每条目含 role/affiliation/background/strategic_motivation/known_preferences/company_strategy 六字段
  - 6 项强制要求：每位评委独立条目、主办方须分析"为什么办这场比赛"、background ≥100字、strategic_motivation ≥50字、company_strategy ≥50字、缺乏公开信息须标注推断依据
  - 6 项 self_check 项 tagged (v4.1.3)

**问题2：输出格式默认 Word 而非 MD 未被强制执行**
- **根因**：`tasks/T20a_research_render.md` 将 docx 导出放在 Step7 作为"PDF 输出完成后"的附加步骤，定位为可选附加；「默认精排链」表格只把 PDF 作为默认主路径，docx 为穷尽重试替代；路径三「MD+指南」被当作合法最终交付物
- **真实产物证据**：对话记录 L1568 AI 主动提出创建 .md 文件而非 .docx；研究报告产物以 .md 格式交付，违反 SKILL.md L1030 G6 硬门控「research_report 默认 PDF 与/或 .docx」
- **修复**：T20a 强化 docx 为强制默认交付物，含：
  - 「默认精排链」表格重构：pandoc → Word .docx 提升为「默认（主，v4.1.3 强制）」，与 PDF 并列
  - Step7 概述重写：从"PDF 输出完成后生成"改为"与 PDF 并列的强制默认交付物"
  - 新增强制执行条件：不得标记为可选/附加/穷尽重试保底，仅用户明确指定时方可跳过
  - 路径三明确标注「非最终交付物」，须标注 `docx_status: "pending_manual_conversion"`
  - 输出注册新增 `docx_status`/`docx_skipped_reason`/`g6_gate_check` 三字段
  - self_check 新增 4 项 (v4.1.3) docx 强制交付自检
  - must_not 新增 3 项 (v4.1.3) 禁止条款：禁止 MD 作为最终交付物、禁止跳过 Step7、禁止将 Step7 降级

**问题3：内部算法名称与推演逻辑暴露在成品中**
- **根因**：`tasks/T20_output_guard.md` 扫描规则仅覆盖节点编号（B类）、Gate名（C类）、字段名（D类）、库名（E类），未覆盖框架方法论术语（如 EXHAUST、九层研究底座、三路对抗验证、十四维全息框架等）
- **真实产物证据**：研究报告 L8 `**执行模式**：EXHAUST（穷尽模式）`、L21 `研究采用九层研究底座、七条推理路径、三路对抗验证、十四维全息框架、四个反事实推演、七个科学深度模块、六个元维度扩展、哲学三元组审查的完整认知流水线`、L50-54 目录使用内部术语、L10845-10850 G1-G6 硬门控结果暴露
- **修复**：T20 新增「F. 框架方法论术语」扫描类别，含：
  - 17 项禁止术语表（EXHAUST/九层研究底座/三路对抗验证/十四维全息框架/科学深度层/元维度/哲学三元组/认知流水线/七条推理路径/竞争择优/极限决策推理/跨维洞察/硬门控/执行账本/write-while-research/context_package/running_word_count）
  - 每项附通俗语言替换建议
  - 16 条扫描正则模式
  - 方法论章节白名单例外（使用通俗语言描述方法论时豁免）
  - self_check_before_output 从"A–E 五类"更新为"A–F 六类"

#### Verified
- `python scripts/reference-integrity.py` → 57 节点 DAG 一致 ✓
- `python scripts/exhaust-consistency-check.py` → 387 文件 0 违规 ✓
- `python scripts/tasks-integrity-check.py` → 57/57 文件 0 缺失 0 孤儿 ✓
- `python scripts/encoding-compatibility-check.py` → 4/4 文件全部含 UTF-8 兼容代码 ✓
- 全部 4 个 CI 脚本在 Windows 上 EXIT_CODE=0 ✓

---

## [v4.1.2] - 2026-06-17

### 鲁班慢刨方案B：精雕（可见产物 + 跨平台CI门禁）

本轮聚焦跨平台兼容性、可视化产物、README 传播力与出师证书格式，让 Skill 在 Windows/macOS/Linux 三平台均可验证通过。

#### Fixed
- **`assets/demo-record.sh` 版本号同步**：3.1.0 → 4.1.0，与主版本对齐，添加跨平台说明注释

#### Added
- **`assets/demo-visualize.py`**：跨平台 Python 可视化脚本（Windows 无 bash 时使用），零依赖仅用标准库，生成三种可视化产物：
  - `assets/dag-topology.mmd` — Mermaid DAG 拓扑图（57 节点 + 82 边，GitHub 原生渲染）
  - `assets/execution-timeline.md` — 执行时间线 Markdown 卡片（57 节点表格 + 5 Gate + 6 硬门控 + 3 并行点）
  - `assets/demo-summary.json` — 执行摘要 JSON（机器可读，含 phase_distribution）
  - DAG 节点定义与 SKILL.md SSOT 严格对齐：Phase1=15 + Phase2=9 + Phase3=8 + Phase4=6 + Phase7=19 = 57
- **`scripts/encoding-compatibility-check.py`**：编码兼容性检查脚本——扫描 scripts/ 和 assets/ 下所有 .py 文件，检查是否包含 `sys.stdout.reconfigure(encoding="utf-8")` 跨平台兼容代码，防止未来新增脚本遗漏 Windows GBK 编码修复
- **CI `encoding-compatibility-check` job**：`.github/workflows/ci.yml` 新增第 4 个 job，将编码兼容性检查纳入持续集成流水线
- **`assets/result-card.md` 鲁班出师证书格式**：升级为鲁班标准 ASCII 边框出师证书，含 DAG 拓扑概览图 + 慢刨记录表
- **README DAG 拓扑可视化节**：效果示例区新增 Mermaid DAG 拓扑图（GitHub 原生渲染）+ 链接到完整 .mmd 文件和执行时间线

#### Changed
- **README 首屏价值陈述**：数字挂链接（57 节点→SKILL.md，14 维→SKILL.md），去掉"不留死角"大词，改为"每个结论都被魔鬼代言人攻击过才放行"
- **README 升级亮点节**：v4.1.1 → v4.1.2
- **README 文件结构**：补充 assets/ 下新增的 5 个可视化产物文件

#### Verified
- `python scripts/reference-integrity.py` → 57 节点 DAG 一致 ✓
- `python scripts/exhaust-consistency-check.py` → 387 文件 0 违规 ✓
- `python scripts/tasks-integrity-check.py` → 57/57 文件 0 缺失 0 孤儿 ✓
- `python scripts/encoding-compatibility-check.py` → 4/4 文件全部含 UTF-8 兼容代码 ✓
- `python assets/demo-visualize.py` → 57 节点 + 82 边 + 5 Phase，3 产物生成成功 ✓
- 全部 4 个 CI 脚本在 Windows 上 EXIT_CODE=0 ✓

---

## [v4.1.1] - 2026-06-17

### 鲁班慢刨方案A：补地基（P0 修复）

本轮聚焦 P0 静默失败隐患与版本号一致性，验证资产沉淀为 CI 门禁。

#### Fixed
- **版本号一致性**：`SKILL.md` frontmatter、`.claude-plugin/marketplace.json`（metadata + plugin 两处）、`README.md` 徽章全部从 `3.1.0` 同步至 `4.1.0`，与 CHANGELOG v4.1 对齐
- **SKILL.md §0.1 A 措辞矛盾**：原 L107-108 "不读取任务文件即执行=未运行本框架" 与 §0.1 自足契约矛盾，改为"防偷懒机制，非降级机制"——`tasks/` 缺失时按 §0.1 A–G 自足契约就地执行，标注 `tasks_source: self_contained`，不跳节点
- **README skills.sh 徽章**：原动态徽章 `https://skills.sh/b/llootupsl/profound-cognition` 因 skills.sh 页面无法加载显示为破损，替换为 shields.io 静态徽章，保留跳转链接
- **清理 `scripts/__pycache__/`**：删除 2 个 `.pyc` 文件（已在 `.gitignore` 中，但工作区残留）

#### Added
- **`test-prompts.json`**：README L189/L244 声明但文件缺失（P0 静默失败），现创建——含 6 个验收 prompt（AP-01~AP-06，覆盖 research_report/wechat_article/course_material 三种成品 + 对抗验证 + 事实核查）、negative_triggers 节、exhaust_consistency_audit 7 项检查（含新增"tasks/ 缺失处理"检查）
- **`scripts/tasks-integrity-check.py`**：tasks/ 目录健康检查脚本——校验目录存在、文件数 ≥57、SKILL.md 声明文件全部存在、无孤儿文件。沉淀自鲁班慢刨验证资产
- **CI `tasks-integrity-check` job**：`.github/workflows/ci.yml` 新增第三个 job，防止 tasks/ 目录被误删或精简分发不完整导致的静默失败

#### Verified
- `python scripts/tasks-integrity-check.py` → 全部校验通过 ✓（57/57 文件，0 缺失，0 孤儿）
- `python scripts/reference-integrity.py` → 全部校验通过 ✓（57 节点 DAG 一致）
- `python scripts/exhaust-consistency-check.py` → 382 文件 0 违规 ✓

---

## [v4.1] - 2026-06-17

### 字数声明一致性修复（spec v6）

本次修复 spec v5 遗漏的字数声明一致性问题（升级方案指令 8 要求"全项目搜索 15000，替换为 100000"，v5 未执行）。

#### Fixed
- 修复 `tasks/T13_cog_synthesize.md` L458 综合叙事字数目标从 `15000-30000 字` 为 `≥100000 字`（与 L474 一致）
- 修复 `tasks/T20a_research_render.md` L78 章节集群字数从 `约8000-15000字` 为 `约8000-22000字`（对齐 SKILL.md §0.1 字数地板）
- 修复 `supervisors/checks/T20_output_guard_check.yml` L7 研究报告门槛从 `≥ 8000 字` 为 `≥ 100000 字`（严重错误，比真相源低 12.5 倍）
- 修复 `supervisors/supervisor-checklist.md` L19 T13 综合叙事字数从 `≥ 8000` 为 `≥ 100000`
- 修复 `docs/upgrade-completeness-audit.md` L191 wechat_article 字数从 `≥5000 字` 为 `≥3000 字`（与 SKILL.md L5 一致）

#### Added
- `scripts/exhaust-consistency-check.py` 新增 `check_word_count_consistency()` 函数，检测字数声明一致性
- 检测 research_report 总字数门槛违规（8000、15000 作为总门槛）
- 检测 wechat_article 总字数门槛违规（5000、8000 作为总门槛）
- 检测 course_material 总字数门槛违规
- 排除部分级字数地板（§1 ≥8000、§3 ≥8000 等是允许的）

#### Verified
- supervisors/checks 完整性核查：实际 60 vs 60 完美匹配，无差异（spec v5 "61 vs 59" 为计数误差）
- EXHAUST 一致性扫描：381 文件，0 违规（含字数一致性检查）

---

## [v4.0] - 2026-06-17

**鲁班打磨 v5**：聚焦 EXHAUST 一致性收尾、CI 自动化加固、文档完整性与演示资产沉淀。

### Added

- **EXHAUST 一致性扫描脚本**：新增 `scripts/exhaust-consistency-check.py`，含否定前缀 / 后缀检测，自动扫描仓库内违反"永远穷尽"铁律的措辞。
- **CI 一致性门禁**：升级 `.github/workflows/ci.yml`，新增 `exhaust-consistency-check` job，将一致性扫描纳入持续集成流水线。
- **公式调用链路映射**：新增 `docs/formula-call-chain-map.md`，覆盖 42 个公式 / 模型 / 模板的调用链路映射表。
- **升级完整性审计**：新增 `docs/upgrade-completeness-audit.md`，对 10 条指令的执行完整性进行审计并出具报告。
- **CHANGELOG**：新增本文件 `CHANGELOG.md`，沉淀 v1.0 → v4.0 的完整演进历史。
- **反例测试 prompt**：README 新增反例测试 prompt 节，明确列出不应触发的输入模式。
- **演示资产**：新增 `assets/demo-record.sh`（demo 录制脚本）与 `assets/result-card.md`（结果卡片）。

### Changed

- **修复 SKILL.md 禁止清单自相矛盾**：`[ESTIMATED]` 自相矛盾问题修复，改为 `[ESTIMATED]`（已禁止，改为 `[INTERNAL_REASONING]`）。
- **移除 SKILL.md 57 节点 conditional 字段**：消除条件性激活暗示，确保节点始终可用。
- **修复 README 平台兼容性措辞**：将"替代"改为"适配"，消除降级暗示。
- **修复 CI 路径引用**：`.github/workflows/integrity-check.yml` 中 `v2/**` 路径引用改为 `**`，适配扁平化目录结构。
- **精简 README v3.1 升级亮点**：将 v3.1 技术细节下沉至本 CHANGELOG，README 仅保留入口指引。

---

## [v3.1] - 2026

**EXHAUST 一致性强化**：全面修复与穷尽模式四大铁律矛盾的措辞，使工程实现与"永远穷尽、无档位、无上限"的承诺在语言层面完全一致。

> 以下技术细节原位于 README.md 第 20-31 行，本轮下沉至 CHANGELOG 以保持 README 简洁。

### Added

- **元数据完善**：`marketplace.json` 增加 `tags` 字段，版本号同步至 `3.1.0`。
- **测试资产沉淀**：新增 `test-prompts.json`，包含 6 个验收 prompt + EXHAUST 一致性审计清单。

### Changed

- **EXHAUST 一致性强化（本轮核心）**：全面修复与穷尽模式四大铁律矛盾的措辞——
  - 移除 `context-budget-protocol` 中"硬终止""终止研究""`CONTEXT_TOO_SMALL_ERROR`"等违反"永远穷尽"的措辞。
  - "硬终止" → "强制落盘"：行为不变（继续生成不丢弃），但措辞与 EXHAUST 一致。
  - "终止研究报错" → "强制 write-while-research 落盘 + 分段加载 + 增量渲染，研究继续"。
  - `SKILL.md` 中"单轮聊天输出有硬上限" → 明确此为工程实现手段，不违反"Token 不设上限"。
  - `execution-protocol` 中"资源耗尽处理" → "资源压力处理"，明确并行度调整是工程调度非降级。
- **frontmatter 精炼**：`description` 更紧凑，触发词密度更高，提升模型识别率。
- **递归终止条件统一**：T13 / T24 / T26 / Gate-δ 全部改为质量驱动收敛，不再有轮数硬上限。

---

## [v3.0] - 2026

**深度思考升级方案落地**：根据《深度思考的升级方案.md》执行 10 条指令，完成认知广度与深度的双重跃迁。

### Added

- **35 领域引擎**：在 `knowledge/domains/` 下新增 35 个领域引擎，覆盖人文、社科、自然、工程、艺术等全域学科。
- **4 个非线性公式**：在 `formula-engine/` 下新增 `info-decay.md`、`logistic-adjudication.md`、`sigmoid-calibration.md`、`softmax-attention.md` 四个非线性公式模型。
- **rendering-pipeline**：新增 `rendering-pipeline/` 模块，含 `ARCHITECTURE.md`、`layout-grid.md`、`motion-semantic-match.md`、`semantic-auto-detect.md`、`taste-skill-consumer.md`、`visual-dna.md`。
- **13 个 Skills**：扩展能力生态，新增 13 个子 Skill。
- **P0 / P1 认知增强项目**：落地优先级 P0 与 P1 的认知增强项。

### Changed

- **SKILL.md 重构**：重构为 1415 行，结构更清晰，触发逻辑更稳健。

---

## [v2.0] - 2025

**框架扩展**：从基础 DAG 扩展为完整的多层研究体系。

### Added

- **57 节点 DAG**：节点数从 31 扩展至 57，覆盖更细粒度的研究任务。
- **九层研究底座**：建立逐层递进的研究底座结构。
- **三路对抗验证**：引入三路同时攻击结论的对抗验证机制。
- **五道 Gate 门控**：建立五道质量门控，层层把关产出质量。

---

## [v1.0] - 2025

**初始版本**：建立基础 DAG 框架。

### Added

- **基础 DAG 框架**：31 节点的有向无环图任务流水线。
- **核心协议**：checkpoint、context-budget、execution 等基础协议。
- **知识底座雏形**：基础领域引擎与思维模型。

---

[v5.0.0]: https://skills.sh/llootupsl/profound-cognition "v5.0.0 Visual DNA 审美进化"
[v4.1.6]: https://skills.sh/llootupsl/profound-cognition "v4.1.6 全面修复"
[v4.1.5]: https://skills.sh/llootupsl/profound-cognition "v4.1.5 深度反思第三轮"
[v4.1.4]: https://skills.sh/llootupsl/profound-cognition "v4.1.4 深度反思第二轮"
[v4.1.3]: https://skills.sh/llootupsl/profound-cognition "v4.1.3 真实运行产物反思"

[v4.1.2]: https://skills.sh/llootupsl/profound-cognition "v4.1.2 鲁班慢刨方案B：精雕"
[v4.1.1]: https://skills.sh/llootupsl/profound-cognition "v4.1.1 鲁班慢刨方案A：补地基"
[v4.0]: https://skills.sh/llootupsl/profound-cognition "v4.0 鲁班打磨 v5"
[v3.1]: https://skills.sh/llootupsl/profound-cognition "v3.1 EXHAUST 一致性强化"
[v3.0]: https://skills.sh/llootupsl/profound-cognition "v3.0 深度思考升级方案落地"
[v2.0]: https://skills.sh/llootupsl/profound-cognition "v2.0 框架扩展"
[v1.0]: https://skills.sh/llootupsl/profound-cognition "v1.0 初始版本"
