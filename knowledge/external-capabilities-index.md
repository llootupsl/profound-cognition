# 外部能力卡片逆向索引 (External Capabilities Reverse Index)

> **文件**: `knowledge/external-capabilities-index.md`
> **用途**: 卡片→消费节点的反向索引，用于追踪每张能力卡片的集成状态和死代码检测
> **更新日期**: 2026-06-05

---

## 一、激活卡片（有消费节点）

| 卡片编号 | 卡片名称 | 消费节点 | 用途简述 |
|---------|---------|---------|---------|
| TC-009 | Wikidata | data-engine | 实体属性验证、事实核查、数据溯源 | ★核心方法论已内化于 knowledge/domains/data-engine.md
| TC-010 | ConceptNet | cognitive-science-engine | 常识知识图谱、心智模型构建 | ★核心方法论已内化于 knowledge/domains/cognitive-science-engine.md
| TC-029 | STORM | literature-engine | 跨文本综合、文献综述生成 | ★核心方法论已内化于 knowledge/domains/literature-engine.md |
| TC-030 | GPT-Researcher | science-engine | 文献检索、实验方案设计 | ★核心方法论已内化于 knowledge/domains/science-engine.md
| TC-055 | Mesa | TM01 | ABM仿真框架 | ★核心方法论已内化于 tasks/TM01_system_dynamics.md |
| TC-056 | PyCX | TM01 | 相平面分析工具 | ★核心方法论已内化于 tasks/TM01_system_dynamics.md
| TC-057 | DoWhy | TM02 | 因果推断 | ★核心方法论已内化于 tasks/TM02_causal_verification.md |
| TC-058 | EconML | TM02 | 异质性处置效应估计 |
| TC-059 | Pyro | TM02 | 概率编程 | ★核心方法论已内化于 tasks/TM02_causal_verification.md
| TC-060 | RSI | TM03 | 结构化交互推理 |
| TC-061 | EMA Workbench | TM04 | 探索性建模分析 |
| TC-062 | CLA Framework | TM04 | 因果层次分析 |
| TC-063 | MetaNet | TM05, T_meta_dim_9_10 | 元认知网络分析（底层引擎：NetworKit TC-083，C++后端十亿级边，替换NetworkX以支持>5000节点） | ★核心方法论已内化于 tasks/T26_meta_insight_cross.md
| TC-064 | ENA | TM05, T_meta_dim_9_10 | 认知网络分析 | ★核心方法论已内化于 tasks/T26_meta_insight_cross.md
| TC-065 | Cynefin | TM05 | 复杂决策框架 | ★核心方法论已内化于 tasks/TM05_meta_reflection.md |
| TC-066 | MCDA | TM05 | 多准则决策分析（底层执行引擎：pyDecision TC-089，46种方法） | ★核心方法论已内化于 knowledge/thinking-models/decision/decision-matrix.md
| TC-067 | OWLAPY | TM07 | OWL本体构建 | ★核心方法论已内化于 tasks/TM07_ontology_export.md
| TC-068 | SSSOM | TM07 | 语义映射标准 | ★核心方法论已内化于 tasks/TM07_ontology_export.md
| TC-069 | PyKEEN | TM07 | 知识图谱嵌入 | ★核心方法论已内化于 tasks/TM07_ontology_export.md
| TC-070 | Neo4j | TM07 | 图数据库 | ★核心方法论已内化于 tasks/TM07_ontology_export.md
| TC-071 | CozoDB | TM07, T15b | Datalog传递推理 | ★核心方法论已内化于 tasks/TM07_ontology_export.md
| TC-072 | TypeDB | TM07 | 强类型知识图谱 |
| TC-073 | OpenNARS | T10, T11, T12 | 非公理矛盾容忍推理 | ★核心方法论已内化于 tasks/T09_cog_reason.md
| TC-074 | WebWeaver | T02, T09 | 动态大纲深度研究合成 |
| TC-076 | Catlab | T15b | 范畴论同构类比 | ★核心方法论已内化于 tasks/T03b_cross_axis_matrix.md
| TC-077 | XGI | T03b | 高阶网络超边分析 | ★核心方法论已内化于 tasks/T03b_cross_axis_matrix.md
| TC-078 | InfraNodus | T15b | 结构洞发现 | ★核心方法论已内化于 tasks/T03b_cross_axis_matrix.md
| TC-079 | GenerativeAgents | TM03 | 社会涌现沙盒 | ★核心方法论已内化于 tasks/TM03_adversarial_synthesis.md |
| TC-080 | TLA+/Alloy | TM01, TM06 | 形式化模型检查 | ★核心方法论已内化于 tasks/TM02_causal_verification.md
| TC-081 | Pol.is | TM03, T07b | 共识发现 | ★核心方法论已内化于 tasks/T13_cog_synthesis.md
| TC-082 | Pyro-Probabilistic | TM02 | 概率编程信念更新 | ★核心方法论已内化于 tasks/TM02_causal_verification.md
| MC-033 | AGoT | T08, T09 | 思维图推理 | ★核心方法论已内化于 tasks/T09_cog_reason.md
| MC-075 | CGT | T13, TM03 | 范畴论对抗形式化 | ★核心方法论已内化于 tasks/TM07_ontology_export.md
| TC-001 | SearXNG | T02 | 研究搜索（元搜索引擎） | ★核心方法论已内化于 knowledge/search-strategy.md
| TC-002 | Whoogle | T02 | 隐私搜索（SearXNG备选） | ★核心方法论已内化于 knowledge/search-strategy.md
| TC-003 | Crawl4AI | T02 | 网页抓取 | ★核心方法论已内化于 knowledge/search-strategy.md
| TC-004 | MarkItDown | T20a | 内容格式转换 | ★核心方法论已内化于 knowledge/search-strategy.md
| TC-007 | Typst | T20a | 排版渲染 |
| TC-008 | VMPrint | T20a | 虚拟打印 |
| TC-012 | Tectonic | T20a | 排版引擎 |
| TC-013 | LuaTeX-CN | T20a | 中文排版 |
| TC-014 | rxiv-maker | T20a | 预印本生成 |
| TC-017 | bm-md | T20a | 书签markdown转换 |
| LC-018 | ECharts | T27 | 可视化渲染 | ★核心方法论已内化于 rendering-pipeline/visual-dna.md
| LC-019 | Plotly | T27 | 交互式图表 | ★核心方法论已内化于 rendering-pipeline/visual-dna.md
| LC-020 | Observable-Plot | T27 | 声明式可视化 | ★核心方法论已内化于 rendering-pipeline/visual-dna.md
| LC-021 | Mermaid | T27 | 流程图渲染 | ★核心方法论已内化于 rendering-pipeline/ARCHITECTURE.md
| TC-022 | AutoFigure | T27 | 图表自动生成 |
| LC-023 | Markmap | T27 | 思维导图渲染 | ★核心方法论已内化于 rendering-pipeline/ARCHITECTURE.md
| TC-024 | PubFig | T27 | 学术图表标准 |
| LC-025 | d3js | T27 | 自定义可视化 | ★核心方法论已内化于 rendering-pipeline/visual-dna.md
| TC-026 | PlantUML | T27 | UML图渲染 |
| TC-027 | TikZ | T27 | 学术绘图 |
| TC-028 | Pandoc | T20a | 格式转换 |
| TC-031 | PaperQA2 | T02 | 学术论文QA |
| TC-032 | Perplexica | T02 | AI搜索引擎 |
| TC-036 | OpenAI-Deep-Research | T02 | 深度研究 |
| TC-037 | Gemini-Deep-Research | T02 | 深度研究(备选) |
| TC-043 | PaperBanana | T02 | 论文解析 |
| TC-044 | PaperVizAgent | T20a | 论文可视化 |
| TC-045 | Crawl4AI-MCP | T02 | MCP网页抓取 |
| TC-046 | MarkItDown-MCP | T20a | MCP格式转换 |
| LC-026 | Taste-Skill | T20a, T20b, T20c, T27 | 全局审美总控，视觉DNA生成，管控所有渲染输出 | ★核心方法论已内化于 rendering-pipeline/visual-dna.md
| LC-029 | guizang-ppt-skill | T20a | 代码化PPT设计，杂志/瑞士风顶级排版 | ★核心方法论已内化于 rendering-pipeline/ARCHITECTURE.md
| LC-031 | html-ppt-skill | T20a | HTML幻灯片容器底座，36套主题 | ★核心方法论已内化于 rendering-pipeline/ARCHITECTURE.md
| LC-032 | Anthropic-PPTX-Skill | T20a | 原生.pptx输出，含QA校验 | ★核心方法论已内化于 rendering-pipeline/ARCHITECTURE.md
| LC-033 | PaperBanana-Skill | T27 | 顶刊级学术插图生成 | ★核心方法论已内化于 rendering-pipeline/visual-dna.md
| LC-035 | excalidraw-skill | T27 | 手绘风格示意图 | ★核心方法论已内化于 rendering-pipeline/ARCHITECTURE.md
| LC-036 | SketchAgent-MIT | T27 | 序列手绘生成，逐笔动画 | ★核心方法论已内化于 rendering-pipeline/ARCHITECTURE.md
| LC-030 | data-viz-plots-skill | T27 | Nature/Cell级学术图表 |
| LC-034 | Markdown-Viewer-Skills | T27 | 多引擎可视化，9500+图标 | ★核心方法论已内化于 rendering-pipeline/ARCHITECTURE.md
| LC-027 | GSAP-Skills | T27 | Web动效引擎，60fps丝滑 | ★核心方法论已内化于 rendering-pipeline/visual-dna.md
| LC-028 | vibe-motion-skills | T27 | 预调校动效包，直接调用 | ★核心方法论已内化于 rendering-pipeline/visual-dna.md
| LC-037 | Animotion-MCP-Skill | T27 | 745+ CSS动画 + 9500+ 图标 | ★核心方法论已内化于 rendering-pipeline/visual-dna.md
| FE-001 | Softmax-Attention | T12b, T13 | 动态注意力加权，路径/证据强度得分归一化 |
| FE-002 | Logistic-Adjudication | T10 | Logistic 胜负判定，攻击/辩护强度映射为连续攻击成功率 |
| FE-003 | Info-Decay | I01, context-budget-protocol | 指数边际收益衰减，动态判断迭代终止 |
| FE-004 | Sigmoid-Calibration | supervisor protocol | Sigmoid 置信度校准，压缩极端值拉伸中间区域 |
| MC-140 | Bayesian-Inference | T09, T13, TM02, T05 | 贝叶斯公式 + 全概率展开：P(H\|E)=P(E\|H)×P(H)/P(E)，动态后验更新 | ★核心方法论已内化于 knowledge/thinking-models/decision/bayesian-updating.md
| MC-141 | Bayes-Factor-Convergence | T09, T13, T05 | 贝叶斯因子 BF=P(E\|H)/P(E\|¬H) + 收敛判定（连续3条证据ΔP<0.05） | ★核心方法论已内化于 knowledge/thinking-models/decision/bayesian-updating.md
| MC-142 | Nash-Equilibrium | T09, T13, T15, TM03 | 纳什均衡求解：纯策略与混合策略均衡，互为最优响应判定 | ★核心方法论已内化于 knowledge/thinking-models/decision/game-theory.md
| MC-143 | Dominant-Strategy | T09, T13, T15 | 占优策略检测 + 重复剔除劣策略 + Folk Theorem 合作条件 | ★核心方法论已内化于 knowledge/thinking-models/decision/game-theory.md
| MC-144 | Stock-Flow-Dynamics | T09, TM01, T15 | 存量-流量方程：存量变化率=流入-流出，反馈回路增益计算 | ★核心方法论已内化于 knowledge/thinking-templates/system-dynamics.md
| MC-145 | Scenario-Expected-Value | T09, T13, TM04, T15 | 期望值计算 E(D)=W_opt×V_opt+W_neu×V_neu+W_pes×V_pes + 情景偏离度 SD | ★核心方法论已内化于 knowledge/thinking-models/decision/scenario-simulator.md
| MC-146 | Monte-Carlo-Decision-Tree | TM04, T09, T15 | 蒙特卡洛仿真（1000-5000次）+ 决策树后序遍历EV计算 | ★核心方法论已内化于 knowledge/thinking-models/decision/scenario-simulator.md
| MC-147 | Net-Benefit-Composite | T09, T13, T15 | 净收益公式 TR/TC + 加权综合评分 CS=0.25×S1+0.25×S2+0.20×S3+0.15×S4+0.15×S5 | ★核心方法论已内化于 knowledge/thinking-models/decision/decision-matrix.md
| MC-148 | Risk-TCO | T09, T15 | 风险分 R=P×I（1-25）+ 总拥有成本 TCO=直接成本+机会成本+隐性成本 | ★核心方法论已内化于 knowledge/thinking-models/decision/decision-matrix.md
| MC-149 | Value-Impact-Attenuation | T09, T15 | 价值观适配度 VAF + 影响衰减模型 I(t)=I_0×e^(-λt)+I_base，CI(T)=∫[I_pos-I_neg]dt | ★核心方法论已内化于 knowledge/thinking-models/decision/decision-matrix.md
| MC-150 | IBE-Abductive | T08, T09, T13 | 最佳解释推断 IBE=0.45×E+0.30×S+0.25×C；E=覆盖度×机制明确度；S=1/(1+额外假设数) | ★核心方法论已内化于 knowledge/thinking-models/general/abductive-reasoning.md
| MC-151 | Structural-Mapping | T09, T15b, T04 | 结构映射三原则（关系优先/系统性/一一对应）+ 映射有效性三层验证 | ★核心方法论已内化于 knowledge/thinking-models/general/structural-mapping.md
| MC-152 | Causal-Effect-Confounding | T09, TM02, T08 | 因果效应量（Cohen's d/β/OR）+ 混淆变量识别与中介/调节分析 | ★核心方法论已内化于 knowledge/thinking-templates/causal-chain.md
| MC-153 | Welfare-Transmission | T15, T09 | 福利三角 ΔTS=ΔCS+ΔPS+ΔGR+ΔEXT + 政策传导链四级衰减分析 | ★核心方法论已内化于 knowledge/thinking-models/decision/decision-matrix.md
| MC-154 | Bass-S-Curve | T15, T09, TM04 | Bass创新扩散 n(t)=[p+q×N(t)/m]×[m-N(t)] + S曲线预测（性能极限比） | ★核心方法论已内化于 knowledge/thinking-templates/trend-forecast.md
| MC-155 | Assumption-Counterfactual | T08, T10, T11, T12 | 三层假设挖掘（显性/隐性/深层）+ 七种反事实推演 + criticality×uncertainty矩阵 | ★核心方法论已内化于 knowledge/thinking-models/general/counterfactual-reasoning.md
| MC-156 | Bias-Socratic-Scan | T08, T18, T10 | 11类认知偏误全扫描 + 苏格拉底式诘问5条追问链 + 范式质疑三层框架 | ★核心方法论已内化于 knowledge/thinking-models/general/cognitive-bias-scan.md
| MC-157 | Robustness-Stress-Test | T12, T13, T06 | 五类鲁棒性压力测试（极端参数/假设移除/证据穷尽重试替代/时序反转/范式外） | ★核心方法论已内化于 knowledge/thinking-models/general/robustness-testing.md
| MC-158 | Axiom-Verification | T08, TM02, T09 | 公理验证四标准（广泛性/稳定性/可证伪性/不可再分性）+ 递归拆解锚定验证 | ★核心方法论已内化于 knowledge/thinking-templates/causal-chain.md
| MC-159 | MECE-Prioritization | T08, T09, T01 | MECE递归分解 + 问题优先级排序 I×(11-U)；八维分析矩阵敏感性映射 | ★核心方法论已内化于 knowledge/thinking-models/general/mece-decomposition.md
| MC-160 | Power-Interest-Matrix | T09, T15, T05 | 权力-利益矩阵四象限定位 + 动机四层级（L1物质/L2制度/L3身份/L4价值） | ★核心方法论已内化于 knowledge/thinking-models/decision/decision-matrix.md
| MC-161 | Aufheben-Synthesis | T13, T12b, T09 | 扬弃操作（否定/保留/提升）+ 合题质量七标准（超越性/不可逆性/精确性等） | ★核心方法论已内化于 knowledge/thinking-models/general/dialectical-analysis.md
| MC-162 | Layer-Peeling | T08, T13, T09 | 五层剥开架构L0-L4 + 每层触发/终止条件判定 + 不可跳跃/不可混淆纪律规则 | ★核心方法论已内化于 knowledge/thinking-models/general/layer-peeling.md
| MC-163 | Norm-Lifecycle | T15, T09, T13 | 社会规范生命周期五阶段（禁忌→争议→主流化→制度化→理所当然）+ 跃迁加速器 | ★核心方法论已内化于 knowledge/thinking-models/general/norm-lifecycle.md
| MC-164 | Comparison-Significance | T04, T09, T13 | 异同矩阵构造 + 差异显著性评估 + 根因追溯L1-L4四层级归因 | ★核心方法论已内化于 knowledge/thinking-models/general/comparative-analysis.md
| MC-165 | STEEP-Scenario | T09, T13, TM04 | STEEP五维驱动力分解 + 驱动力权重矩阵（高影响×高确定性→情景轴）+ 多情景构建 | ★核心方法论已内化于 knowledge/thinking-models/decision/scenario-simulator.md
| MC-166 | Feasibility-Assessment | T09, T13, T15 | 四维可行性评估（政治/经济/技术/社会）+ 合法性来源五分类 | ★核心方法论已内化于 knowledge/thinking-models/decision/decision-matrix.md
| MC-167 | Decision-Tree-EV | T09, TM04, T15 | 决策树构建（□决策/○机会/△结果节点）+ 后序遍历期望值最大化 | ★核心方法论已内化于 knowledge/thinking-models/decision/scenario-simulator.md
| MC-168 | Alternative-Assessment | T09, T13, T15 | 替代方案三维评估：综合分=0.35×新颖度+0.35×可行性+0.30×协同度 | ★核心方法论已内化于 knowledge/thinking-models/decision/decision-matrix.md
| MC-169 | One-Vote-Veto | T09, T15, T19 | 一票否决四条件（致命风险/核心价值冲突/成本不可承受/长期影响严重负面） | ★核心方法论已内化于 knowledge/thinking-models/decision/decision-matrix.md
| MC-170 | Evidence-Independence | T09, T11, T05 | 证据独立性检查四问（同源/因果依赖/共因/独立证据权重加倍） | ★核心方法论已内化于 knowledge/thinking-models/general/evidence-independence.md
| MC-171 | System-Emergence | T09, TM01, T15 | 系统边界映射 + 涌现性检测（移除测试）+ Meadows 12级杠杆点排序 | ★核心方法论已内化于 knowledge/thinking-templates/system-dynamics.md
| MC-172 | Steelmanning | T10, T11, T12, T12b | 钢化论证六标准（逐命题攻击/精度提升/边界明确/不确定性标注/替代排除/博弈稳定） | ★核心方法论已内化于 knowledge/thinking-models/general/steel-manning.md
| MC-173 | Unintended-Consequences | T15, T09, T06 | 五类意外后果检测（回弹/替代/挤出/补偿/软预算约束）+ 寻租检测预防清单 | ★核心方法论已内化于 knowledge/thinking-models/general/unintended-consequences.md
| MC-174 | Trigger-Structure-Coupling | T09, T15, T13 | 触发事件vs结构条件耦合分析 + "火花-湿木"类比判定框架 | ★核心方法论已内化于 knowledge/thinking-models/general/trigger-structure-coupling.md
| MC-175 | Narrative-Analysis | T15, T09, T13 | 叙事五维分析（角色/时间/因果/情绪/省略）+ 竞争叙事评估 | ★核心方法论已内化于 knowledge/thinking-models/general/narrative-analysis.md
| MC-176 | Empowerment-Substitution | T15, T09, T13 | 赋能与替代矩阵（四象限：破坏性重构/就业摧毁/生产力提升/边际改良） | ★核心方法论已内化于 knowledge/thinking-models/general/empowerment-substitution.md
| MC-177 | Cross-Dimension-Correlation | T15, T15b, T09 | 跨维度关联分析五维交叉影响矩阵 + 硬地缘/软地缘/路径锁定三驱动判定 | ★核心方法论已内化于 knowledge/thinking-models/general/cross-dimension-correlation.md
| MC-178 | Fairness-Distribution | T15, T09, T05 | 公平性评估矩阵（收入五等分）+ 进步性/倒退性/中性政策裁定 | ★核心方法论已内化于 knowledge/thinking-models/decision/decision-matrix.md
| MC-179 | Transmission-Attenuation | T15, T09, TM01 | 传导衰减检查（弹性/抵消/辐射范围/时滞/残留率）+ 三级传导残留率<30%预警 | ★核心方法论已内化于 knowledge/thinking-templates/system-dynamics.md
| MC-180 | Lean4 | T28 | Lean 4 形式化命题验证，将关键因果命题转为 ∀x, P(x)→Q(x) 类型检查，有反例→FAIL |
| MC-181 | AutoTRIZ | engineering-engine, design-engine | 系统化创新方法论（40发明原则+矛盾矩阵+ARIZ-85C），注入工程/设计引擎核心工具箱 | ★核心方法论已内化于 knowledge/domains/engineering-engine.md |
| MC-182 | ActiveInference | supervisor protocol | pymdp/ActiveInference.jl 主动推理框架，自由能原理驱动"信息增益 vs 时间成本"动态平衡 | ★核心方法论已内化于 knowledge/cognitive-framework.md |
| MC-183 | Scallop | T09, T13 | 神经符号推理（Datalog规则+神经网络），NS-Engine推理路径，Pyro与OpenNARS之间第三种范式 | ★核心方法论已内化于 tasks/T09_cog_reason.md |
| TC-083 | NetworKit | TC-063 MetaNet | 高性能复杂网络引擎（C++后端，十亿级边），替换NetworkX解决>5000节点性能瓶颈 | ★核心方法论已内化于 tasks/T26_meta_insight_cross.md |
| TC-084 | PyMC | TM02, bayesian-updating.md | 贝叶斯概率编程（先验+观测数据→MCMC采样→后验分布），与Pyro TC-059互补 | ★核心方法论已内化于 knowledge/thinking-models/decision/bayesian-updating.md |
| TC-085 | pygarg | T13, dialectical-analysis.md | 形式化论证计算（AAFs语义判定：admissible/complete/preferred/stable），替代纯LLM论证评估 | ★核心方法论已内化于 knowledge/thinking-models/general/dialectical-analysis.md |
| TC-086 | causal-learn | TM02, causal-chain.md | 因果发现算法（30+算法从数据学习因果图），送入DoWhy TC-057估计因果效应 | ★核心方法论已内化于 knowledge/thinking-templates/causal-chain.md |
| TC-087 | OpenSpiel | T09, T15, TM03 | 博弈求解引擎（70+博弈环境+30+求解算法），纳什均衡/子博弈精炼均衡/相关均衡求解执行层 | ★核心方法论已内化于 knowledge/thinking-models/decision/game-theory.md |
| TC-088 | Axelrod | T09, T15 | 囚徒困境策略演化（230+策略库），重复博弈策略分析：TFT/GTFT/WSLS/Zero-Determinant等策略匹配与锦标赛模拟 | ★核心方法论已内化于 knowledge/thinking-models/decision/game-theory.md |
| TC-089 | pyDecision | TC-066 MCDA | 多准则决策方法库（46种MCDA方法），替换MCDA纯方法论为pyDecision执行层：TOPSIS/AHP/PROMETHEE/VIKOR/ELECTRE等 |
| TC-090 | pgmpy | TM02, T09 | 贝叶斯网络结构学习（DAG结构学习+参数估计+精确/近似推理），HillClimbing/PC/MMHC算法 | ★核心方法论已内化于 tasks/TM02_causal_verification.md
| TC-091 | BFO-SUMO | knowledge-graph-integration.md | 顶层本体统一概念分类框架（BFO 2.0 + SUMO），本体对齐根节点，提供通用实体类型和公理体系 | ★核心方法论已内化于 knowledge/knowledge-graph-integration.md
| TC-092 | FCA | T15b, TM07 | 形式概念分析（FCA/pyRDM），概念格构建+关联规则挖掘+概念稳定性度量，跨域概念簇发现 | ★核心方法论已内化于 tasks/T03b_cross_axis_matrix.md
| TC-093 | KGHeartBeat | T21, TM07 | 知识图谱质量监控（一致性约束/完整性检查/时效性扫描/冲突检测），自动诊断报告生成 | ★核心方法论已内化于 tasks/TM07_ontology_export.md
| TC-094 | AI-Scientist | scientific-discovery.md | 科学发现流水线（假设生成→实验设计→代码编写→论文撰写），自动化科学方法全流程 | ★核心方法论已内化于 extensions/scientific-discovery.md |
| TC-095 | Shadow-Loom | literature-engine, film-engine | 叙事因果推理引擎（fabula/syuzhet分离+Pearl因果阶梯+反事实微积分），分析叙事事件间因果依赖与假设变更影响 |
| TC-096 | PySD | TM01, system-dynamics.md | 系统动力学仿真引擎（因果回路图→存量-流量模型，Vensim模型兼容），微分方程数值求解+参数敏感性扫描 |
| TC-097 | BifurcationKit | TM01, TM04 | 分岔分析引擎（Julia后端，Fold/Hopf/Pitchfork/Transcritical分岔检测），临界点定位+分岔图生成 |
| TC-098 | last30days-skill | T02, I01, search-strategy | 跨平台趋势情报采集与排序（30天衰减模型+四阶段评分+意图感知重排+收敛检测） | ★核心方法论已内化于 knowledge/external-capabilities/last30days-skill-consumer.md
| TC-099 | Agent-Reach | T02, I01, search-strategy | AI Agent互联网能力中间层（14+平台多步搜索+可达性评估+搜索深度控制） | ★核心方法论已内化于 strategies/agent-reach-consumer.md
| MC-184 | ABLkit-CBRkit | T09, T15b | 类比推理（SME/FAM结构映射算法）+案例推理（四步循环：检索/复用/修正/保留），类比推理算法化执行层 |

---
## 二、保留待扩展卡片（无消费节点）

以下卡片已完成基础文档编写，但尚未通过消费节点集成激活。标签 `保留待扩展` 表示其具备潜在整合价值，待后续任务明确后再挂载。

| 卡片编号 | 卡片名称 | 状态 | 潜在整合方向 |
|---------|---------|------|-------------|
| TC-005 | Mem0 | 保留待扩展 | 记忆存储层 |
| TC-006 | DeerFlow | 保留待扩展 | 工作流编排 |
| TC-011 | LightRAG | 保留待扩展 | 知识检索增强 |
| TC-015 | OpenAgents | 保留待扩展 | 多智能体框架 |
| TC-016 | AIHot | 保留待扩展 | 热点话题追踪 |
| MC-034 | FoT | 保留待扩展 | T13综合推理增强 |
| MC-035 | FoFR-Decider | 保留待扩展 | T13决策融合 |
| TC-038 | DeepSeek-R1 | 保留待扩展 | T09推理增强 |
| TC-039 | xAI-Grok | 保留待扩展 | 实时信息推理 |
| TC-040 | Claude-Extended-Thinking | 保留待扩展 | T09深度推理 |
| MC-041 | Google-ADK | 保留待扩展 | 智能体开发框架 |
| MC-042 | SERA | 保留待扩展 | 安全评估框架 |
| TC-047 | LightRAG-MCP | 保留待扩展 | MCP知识检索 |

---

## 三、方法论卡片引用（无独立文件）

以下卡片在任务文件中被引用但尚未创建独立的能力卡片文件（可能位于 `knowledge/methodology-cards/` 或以其他形式存在）：

| 卡片编号 | 引用位置 | 用途 |
|---------|---------|------|
| MC-048 | TM01 | 系统动力学建模方法论 | ★核心方法论已内化于 tasks/TM01_system_dynamics.md
| MC-049 | TM01 | CIB交叉影响平衡分析 | ★核心方法论已内化于 tasks/TM01_system_dynamics.md
| MC-050 | TM01 | Mesa ABM仿真框架 | ★核心方法论已内化于 tasks/TM01_system_dynamics.md
| MC-051 | TM01 | 9种系统基模 | ★核心方法论已内化于 tasks/TM01_system_dynamics.md
| MC-052 | TM01 | Meadows 12级杠杆点 | ★核心方法论已内化于 tasks/TM01_system_dynamics.md
| MC-053 | TM01 | PyCX相平面分析 | ★核心方法论已内化于 tasks/TM01_system_dynamics.md
| MC-054 | TM02 | DoWhy因果推断 | ★核心方法论已内化于 tasks/TM02_causal_verification.md
| MC-055 | TM02 | EconML异质性效应 | ★核心方法论已内化于 tasks/TM02_causal_verification.md
| MC-056 | TM02 | Pyro概率编程 | ★核心方法论已内化于 tasks/TM02_causal_verification.md
| MC-057 | TM03 | RSI多智能体辩论 | ★核心方法论已内化于 tasks/TM03_adversarial_synthesis.md
| MC-058 | TM03 | 魔鬼代言人框架 | ★核心方法论已内化于 tasks/TM03_adversarial_synthesis.md
| MC-059 | TM03 | 共识映射 | ★核心方法论已内化于 tasks/TM03_adversarial_synthesis.md
| MC-060 | TM03 | 隐藏假设挖掘 | ★核心方法论已内化于 tasks/TM03_adversarial_synthesis.md
| MC-061 | TM04 | EMA探索性建模 | ★核心方法论已内化于 tasks/TM04_scenario_landscape.md
| MC-062 | TM04 | CIB场景一致性 | ★核心方法论已内化于 tasks/TM04_scenario_landscape.md
| MC-063 | TM04 | CLA因果层次分析 | ★核心方法论已内化于 tasks/TM04_scenario_landscape.md
| MC-064 | TM04 | 三视野框架 | ★核心方法论已内化于 tasks/TM04_scenario_landscape.md
| MC-065 | TM04 | Wild Card分析 | ★核心方法论已内化于 tasks/TM04_scenario_landscape.md
| MC-066 | TM05 | MetaNet元认知网络 | ★核心方法论已内化于 tasks/TM05_meta_reflection.md
| MC-067 | TM05 | ENA认知网络分析 | ★核心方法论已内化于 tasks/TM05_meta_reflection.md
| MC-068 | TM05 | Cynefin框架 | ★核心方法论已内化于 tasks/TM05_meta_reflection.md
| MC-069 | TM05 | MCDA多准则决策 | ★核心方法论已内化于 tasks/TM05_meta_reflection.md
| MC-070 | TM05 | 认知偏差目录 | ★核心方法论已内化于 tasks/TM05_meta_reflection.md
| MC-071 | TM05 | 伦理分析框架 | ★核心方法论已内化于 tasks/TM05_meta_reflection.md
| MC-072 | TM06 | 全息框架验证 | ★核心方法论已内化于 tasks/TM06_meta_layer_verify.md
| MC-073 | TM06 | 维度覆盖度分析 | ★核心方法论已内化于 tasks/TM06_meta_layer_verify.md
| MC-074 | TM06 | 层间耦合度测量 | ★核心方法论已内化于 tasks/TM06_meta_layer_verify.md
| MC-075-OWLAPY | TM07 | OWLAPY本体构建 |
| MC-076-SSSOM | TM07 | SSSOM语义映射 | ★核心方法论已内化于 tasks/TM07_ontology_export.md
| MC-077-PyKEEN | TM07 | PyKEEN知识图谱嵌入 | ★核心方法论已内化于 tasks/TM07_ontology_export.md
| MC-078-Neo4j | TM07 | Neo4j图数据库 | ★核心方法论已内化于 tasks/TM07_ontology_export.md
| MC-131 | T20/T20b | 中文修辞术方法论 | ★核心方法论已内化于 tasks/T20b_wechat_render.md
| MC-133 | TM01 | 增强型交叉影响分析 | ★核心方法论已内化于 tasks/TM01_system_dynamics.md
| MC-134 | TM02 | 反事实分析框架 | ★核心方法论已内化于 tasks/TM02_causal_verification.md
| MC-135 | TM03 | GT-HarmBench安全评估 | ★核心方法论已内化于 tasks/TM03_adversarial_synthesis.md
| MC-136 | TM04 | 场景鲁棒性评估 | ★核心方法论已内化于 tasks/TM04_scenario_landscape.md
| MC-137 | TM05 | 元认知递归协议 | ★核心方法论已内化于 tasks/TM05_meta_reflection.md
| MC-138 | TM06 | 可达性诚实标注协议 | ★核心方法论已内化于 tasks/TM06_meta_layer_verify.md
| MC-139 | TM07 | 本体验证协议 | ★核心方法论已内化于 tasks/TM07_ontology_export.md

---

## 四、借鉴技术分类处置（Task 4.6）

> 以下为借鉴/借用技术目录的分类处置，明确每项技术在当前架构中的激活状态和消费路径。

### Category 28 图标符号类

| 技术名称 | 状态 | 消费节点/处置说明 |
|---------|------|-----------------|
| Iconify | **激活** | T20a 排版模块（aesthetic-enhancer §13）、T27 配图模块；插件 `plugins/iconify-adapter.md` |
| Tabler Icons | **激活** | Iconify 默认图标集，同 Iconify 消费路径 |
| Feather Icons | **deprecated** | 已被 Iconify + Tabler Icons 完全覆盖，不单独维护 |
| OpenMoji | **deprecated** | 已被 Iconify 覆盖，emoji 场景由 Unicode 符号替代 |
| 3dicons | **deprecated** | 3D 图标非核心需求，已被 内联 Mermaid/SVG 图生成 手绘风格统一替代 |

### Category 30 艺术装饰类

| 技术名称 | 状态 | 消费节点/处置说明 |
|---------|------|-----------------|
| uiGradients | **激活** | T20a 排版模块（aesthetic-enhancer §3 配色系统 + §10 主题预设），CSS 渐变已内化 |
| 分割线 | **激活** | T20a 排版模块（aesthetic-enhancer §5 §7，Typst `line` / CSS `hr` 已模板化） |
| 水印 | **deprecated** | 研究报告默认不加水印，版权声明通过页脚 © 阿洋 实现 |
| 二维码 | **deprecated** | 当前产品类型无扫码场景，若未来需移动端传播可重新激活 |
| 签名 | **deprecated** | 已由页脚 © 阿洋 版权声明替代，数字签名场景暂不需要 |

### Category 31 专业领域配图类

| 技术名称 | 状态 | 消费节点/处置说明 |
|---------|------|-----------------|
| SDXL | **激活** | illustration-generation-protocol（Stable Diffusion 3.5 穷尽重试链）；消费节点 T27 |
| MONAI | **deprecated** | 医学影像专用框架，当前全息框架 31 域中 health-engine 已覆盖医学分析，不依赖 MONAI 生成影像 |
| 金融领域配图 | **激活** | illustration-generation-protocol；消费节点 T27 |
| 历史领域配图 | **激活** | illustration-generation-protocol；消费节点 T27 |
| 科学领域配图 | **激活** | illustration-generation-protocol + PubFig 学术图表；消费节点 T27 |
| 设计领域配图 | **激活** | illustration-generation-protocol + aesthetic-enhancer §10.4 创意主题；消费节点 T27 |

### Category 32-34 学术排版工具类

| 技术名称 | 状态 | 消费节点/处置说明 |
|---------|------|-----------------|
| PaperSpine | **deprecated** | 未在项目中找到引用，Typst + Pandoc + WeasyPrint 排版链已完全覆盖学术排版需求 |
| nature skill | **deprecated** | 未在项目中找到引用，学术排版风格由 aesthetic-enhancer §10.2 academic 主题 + Typst 模板实现 |
| 内联 Mermaid/SVG 图生成 | **激活** | T27 14维度关系可视化（首选）、illustration-generation-protocol §6（13步子代理工作流）；插件 `plugins/paper-figure-adapter.md` |

---
## 五、统计概览

- **激活卡片**: 140 张（含新增 MC-140~MC-184 共 45 张数学公式/认知增强能力卡，含 TC-083~TC-099 共 17 张认知增强工具卡，含 FE-001~FE-004 共 4 张公式引擎能力卡）
- **保留待扩展**: 13 张
- **方法论引用（无独立文件）**: 39 项
- **借鉴技术激活**: 10 项
- **借鉴技术 deprecated**: 9 项
- **总计**: 192 项卡片 + 19 项借鉴技术