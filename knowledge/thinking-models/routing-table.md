<!-- 作者：阿洋 -->
<!-- R5-01 思维模型路由表 — 22 个通用思维模型 + 8 决策/领域模型的适用条件映射 -->

# 思维模型路由表（Thinking Models Routing Table）

> **用途**：T00 研究大纲生成器根据问题特征查阅本表，将匹配的思维模型 ID 填入 `recommended_thinking_models[]`，通过 NRSF §ref 传递给 T08-T13 下游节点。下游节点在执行时读取推荐列表，标注 `applied_models` 字段记录实际应用的模型。

---

## 一、思维模型清单（30 个模型，3 大类）

### 1.1 通用思维模型（general/，22 个）

| # | model_id | 模型名称 | 适用条件 | 激活触发词 | 适用节点 |
|---|----------|---------|----------|-----------|----------|
| 1 | `general/abductive-reasoning` | 溯因推理 | 已观察现象需推导最佳解释；T01 识别"根因分析"类问题 | 为什么、原因、根源、最佳解释 | T08, T09 |
| 2 | `general/analogical-reasoning` | 类比推理 | 跨领域比较；T01 识别"跨领域比较"类问题 | 类比、相似、借鉴、跨领域 | T04, T15b |
| 3 | `general/cognitive-bias-scan` | 认知偏差扫描 | 涉及人类判断与决策；需识别认知偏差 | 偏见、偏差、判断、决策 | T10, T17 |
| 4 | `general/comparative-analysis` | 比较分析 | A/B 比较、多方案选择、差异归因 | 对比、区别、异同、哪个更好 | T04, T13 |
| 5 | `general/counterfactual-reasoning` | 反事实推理 | 评估"如果X不发生会怎样"；假设性场景推演 | 如果、假设、反事实、本来 | T06, T09 |
| 6 | `general/critical-thinking` | 批判性思维 | 对既有结论进行批判性评估；检验论证有效性 | 批判、评估、检验、质疑 | T10, T17, T18 |
| 7 | `general/cross-dimension-correlation` | 跨维度关联 | 多维度交叉分析；系统性问题 | 交叉、关联、系统性、多维 | T09, T13 |
| 8 | `general/dialectical-analysis` | 辩证分析 | 对立观点的调和；正反合推理 | 正反、矛盾、两难、辩证 | T09, T13 |
| 9 | `general/empowerment-substitution` | 赋能替代 | 评估技术/政策对人的赋能或替代效应 | 赋能、替代、技术影响、就业 | T09, T15 |
| 10 | `general/evidence-independence` | 证据独立性 | 多源证据交叉验证；评估证据可靠性 | 证据、验证、独立、交叉 | T05, T11 |
| 11 | `general/first-principles` | 第一性原理 | 根本原因/本质探究；从基本原理推导 | 本质、根本、第一性、原理 | T08, T09 |
| 12 | `general/layer-peeling` | 逐层剥开 | 表象简单但深层复杂；挖掘隐含假设 | 深层、本质、背后、假设 | T08, T09 |
| 13 | `general/mece-decomposition` | MECE 分解 | 问题拆解为互不重叠、完全穷尽的子问题 | 拆解、分解、MECE、穷尽 | T08 |
| 14 | `general/multidimensional-framework` | 多维框架 | 多维度交叉/系统性问题；需结构化分析框架 | 多维、框架、系统、结构 | T09, T13 |
| 15 | `general/narrative-analysis` | 叙事分析 | 分析叙事/话语/框架；理解故事如何塑造认知 | 叙事、话语、框架、故事 | T04, T13 |
| 16 | `general/norm-lifecycle` | 规范生命周期 | 分析社会规范的兴起、扩散、内化、衰退 | 规范、社会、扩散、内化 | T15, T17 |
| 17 | `general/robustness-testing` | 鲁棒性检验 | 检验结论在不同假设下的稳健性 | 鲁棒、稳健、敏感、压力测试 | T10, T12 |
| 18 | `general/steel-manning` | 钢铁人论证 | 构造最强版本的反方论证 | 反驳、钢铁人、最强论证 | T10, T13 |
| 19 | `general/structural-mapping` | 结构映射 | 跨域结构类比；识别同构关系 | 同构、映射、结构相似 | T04, T09 |
| 20 | `general/systems-thinking` | 系统思维 | 涉及反馈循环、系统抗性、反复失败的模式 | 系统、循环、反馈、涌现 | T09, T13 |
| 21 | `general/trigger-structure-coupling` | 触发-结构耦合 | 分析触发事件与结构条件的耦合效应 | 触发、耦合、事件、结构 | T09, T15 |
| 22 | `general/unintended-consequences` | 非意图后果 | 评估政策/行动的意外后果 | 意外、副作用、非意图、后果 | T15, T17 |

### 1.2 决策思维模型（decision/，4 个）

| # | model_id | 模型名称 | 适用条件 | 激活触发词 | 适用节点 |
|---|----------|---------|----------|-----------|----------|
| 23 | `decision/bayesian-updating` | 贝叶斯更新 | T01 识别"概率评估"类问题；需动态更新信念 | 概率、贝叶斯、更新、信念 | T05, T09 |
| 24 | `decision/decision-matrix` | 决策矩阵 | output_type == wechat_article 或问题涉及多方案决策 | 决策、方案、选择、矩阵 | T08, T09, T13 |
| 25 | `decision/game-theory` | 博弈论 | T01 识别"多方博弈"类问题；涉及策略互动 | 博弈、纳什、策略、均衡 | T05, T15 |
| 26 | `decision/scenario-simulator` | 情景模拟器 | 多情景推演；长期战略判断 | 情景、模拟、推演、战略 | T08, T09, T13 |

### 1.3 领域专用思维模型（domain-specific/，4 个）

| # | model_id | 模型名称 | 适用条件 | 激活触发词 | 适用节点 |
|---|----------|---------|----------|-----------|----------|
| 27 | `domain-specific/economic-policy-model` | 经济政策模型 | 问题涉及公共政策/政府监管 | 政策、监管、经济、政府 | T09, T15 |
| 28 | `domain-specific/geopolitical-analysis` | 地缘政治分析 | T01 识别"地缘政治"类问题 | 地缘、政治、国际、大国 | T15 |
| 29 | `domain-specific/social-change-model` | 社会变迁模型 | 问题涉及公共政策/政府监管；社会结构变迁 | 社会、变迁、结构、转型 | T09, T15 |
| 30 | `domain-specific/tech-disruption-model` | 技术颠覆模型 | 问题涉及技术颠覆/创新扩散 | 技术、颠覆、创新、扩散 | T09, T15 |

---

## 二、思维模板与领域引擎交叉映射矩阵（8 模板 × 39 引擎 = 312 组合）

> **用途**：T00 在匹配 `recommended_thinking_template` 时，同时参考领域引擎命中情况，从交叉映射矩阵中选取最适配的思维模板。
>
> **适配等级**：HIGH（强适配，优先选择）/ MEDIUM（中适配，可选）/ LOW（弱适配，不推荐）

### 2.1 因果链分析（causal-chain）× 39 领域引擎

| 领域引擎 | 适配等级 | 说明 |
|----------|---------|------|
| economics-engine | HIGH | 经济因果链分析是该领域的核心方法 |
| health-engine | HIGH | 疾病因果链是医学研究的核心 |
| history-engine | HIGH | 历史事件的因果归因是核心方法 |
| psychology-engine | HIGH | 心理因果机制分析是核心方法 |
| science-engine | HIGH | 科学因果推断是核心方法 |
| law-engine | HIGH | 法律因果责任判定是核心方法 |
| environment-climate-engine | HIGH | 气候变化的因果链分析是核心方法 |
| finance-quant-engine | MEDIUM | 金融市场因果分析常用 |
| political-engine | MEDIUM | 政治因果分析常用 |
| social-engine | MEDIUM | 社会现象因果分析常用 |
| business-engine | MEDIUM | 商业因果分析常用 |
| tech-engine | MEDIUM | 技术因果分析常用 |
| education-engine | MEDIUM | 教育因果分析常用 |
| engineering-engine | MEDIUM | 工程失效因果分析常用 |
| military-engine | MEDIUM | 军事因果分析常用 |
| national-power-engine | MEDIUM | 国力因果分析常用 |
| cognitive-science-engine | MEDIUM | 认知因果分析常用 |
| urban-planning-engine | MEDIUM | 城市因果分析常用 |
| anthropology-engine | LOW | 人类学因果分析较少 |
| architecture-engine | LOW | 建筑因果分析较少 |
| art-engine | LOW | 艺术因果分析较少 |
| culture-engine | LOW | 文化因果分析较少 |
| data-engine | LOW | 数据因果分析较少 |
| design-engine | LOW | 设计因果分析较少 |
| diplomacy-engine | LOW | 外交因果分析较少 |
| film-engine | LOW | 电影因果分析较少 |
| food-engine | LOW | 食品因果分析较少 |
| linguistics-engine | LOW | 语言学因果分析较少 |
| literature-engine | LOW | 文学因果分析较少 |
| mathematics-engine | LOW | 数学因果分析较少 |
| media-communication-engine | LOW | 媒体因果分析较少 |
| music-engine | LOW | 音乐因果分析较少 |
| philosophy-engine | LOW | 哲学因果分析较少 |
| religion-engine | LOW | 宗教因果分析较少 |
| sports-engine | LOW | 体育因果分析较少 |
| aerospace-engine | MEDIUM | 航空航天失效因果分析常用 |
| biotech-engine | HIGH | 生物因果机制是核心方法 |
| energy-engine | MEDIUM | 能源系统因果分析常用 |
| materials-engine | MEDIUM | 材料失效因果分析常用 |

### 2.2 对比分析（comparative-analysis）× 39 领域引擎

| 领域引擎 | 适配等级 | 说明 |
|----------|---------|------|
| political-engine | HIGH | 政治制度比较是核心方法 |
| economics-engine | HIGH | 经济体制比较是核心方法 |
| education-engine | HIGH | 教育体系比较是核心方法 |
| history-engine | HIGH | 历史比较是核心方法 |
| law-engine | HIGH | 法律体系比较是核心方法 |
| social-engine | HIGH | 社会制度比较是核心方法 |
| business-engine | HIGH | 商业模式比较是核心方法 |
| culture-engine | MEDIUM | 文化比较常用 |
| diplomacy-engine | MEDIUM | 外交比较常用 |
| health-engine | MEDIUM | 医疗体系比较常用 |
| urban-planning-engine | MEDIUM | 城市比较常用 |
| media-communication-engine | MEDIUM | 媒体比较常用 |
| tech-engine | MEDIUM | 技术比较常用 |
| finance-quant-engine | MEDIUM | 金融比较常用 |
| military-engine | MEDIUM | 军事比较常用 |
| national-power-engine | MEDIUM | 国力比较常用 |
| philosophy-engine | MEDIUM | 哲学比较常用 |
| psychology-engine | MEDIUM | 心理学派比较常用 |
| cognitive-science-engine | MEDIUM | 认知理论比较常用 |
| science-engine | MEDIUM | 科学理论比较常用 |
| anthropology-engine | LOW | 人类学比较较少 |
| architecture-engine | LOW | 建筑比较较少 |
| art-engine | LOW | 艺术比较较少 |
| data-engine | LOW | 数据比较较少 |
| design-engine | LOW | 设计比较较少 |
| engineering-engine | LOW | 工程比较较少 |
| environment-climate-engine | LOW | 气候比较较少 |
| film-engine | LOW | 电影比较较少 |
| food-engine | LOW | 食品比较较少 |
| linguistics-engine | LOW | 语言学比较较少 |
| literature-engine | LOW | 文学比较较少 |
| mathematics-engine | LOW | 数学比较较少 |
| music-engine | LOW | 音乐比较较少 |
| religion-engine | LOW | 宗教比较较少 |
| sports-engine | LOW | 体育比较较少 |
| aerospace-engine | LOW | 航空航天比较较少 |
| biotech-engine | MEDIUM | 生物技术比较常用 |
| energy-engine | MEDIUM | 能源体系比较常用 |
| materials-engine | MEDIUM | 材料体系比较常用 |

### 2.3 辩证综合（dialectical-synthesis）× 39 领域引擎

| 领域引擎 | 适配等级 | 说明 |
|----------|---------|------|
| philosophy-engine | HIGH | 哲学辩证是核心方法 |
| political-engine | HIGH | 政治辩证是核心方法 |
| social-engine | HIGH | 社会辩证是核心方法 |
| law-engine | HIGH | 法律辩证是核心方法 |
| economics-engine | HIGH | 经济辩证是核心方法 |
| history-engine | MEDIUM | 历史辩证常用 |
| culture-engine | MEDIUM | 文化辩证常用 |
| religion-engine | MEDIUM | 宗教辩证常用 |
| psychology-engine | MEDIUM | 心理辩证常用 |
| education-engine | MEDIUM | 教育辩证常用 |
| diplomacy-engine | MEDIUM | 外交辩证常用 |
| media-communication-engine | MEDIUM | 媒体辩证常用 |
| literature-engine | MEDIUM | 文学辩证常用 |
| art-engine | MEDIUM | 艺术辩证常用 |
| music-engine | MEDIUM | 音乐辩证常用 |
| anthropology-engine | LOW | 人类学辩证较少 |
| architecture-engine | LOW | 建筑辩证较少 |
| business-engine | LOW | 商业辩证较少 |
| cognitive-science-engine | LOW | 认知辩证较少 |
| data-engine | LOW | 数据辩证较少 |
| design-engine | LOW | 设计辩证较少 |
| engineering-engine | LOW | 工程辩证较少 |
| environment-climate-engine | LOW | 气候辩证较少 |
| film-engine | LOW | 电影辩证较少 |
| finance-quant-engine | LOW | 金融辩证较少 |
| food-engine | LOW | 食品辩证较少 |
| health-engine | LOW | 医学辩证较少 |
| linguistics-engine | LOW | 语言学辩证较少 |
| mathematics-engine | LOW | 数学辩证较少 |
| military-engine | LOW | 军事辩证较少 |
| national-power-engine | LOW | 国力辩证较少 |
| science-engine | LOW | 科学辩证较少 |
| sports-engine | LOW | 体育辩证较少 |
| aerospace-engine | LOW | 航空航天辩证较少 |
| biotech-engine | LOW | 生物辩证较少 |
| energy-engine | LOW | 能源辩证较少 |
| materials-engine | LOW | 材料辩证较少 |
| tech-engine | LOW | 技术辩证较少 |
| urban-planning-engine | LOW | 城市辩证较少 |

### 2.4 逐层剥开（layer-peeling）× 39 领域引擎

| 领域引擎 | 适配等级 | 说明 |
|----------|---------|------|
| philosophy-engine | HIGH | 哲学逐层探究是核心方法 |
| psychology-engine | HIGH | 心理深层分析是核心方法 |
| social-engine | HIGH | 社会深层分析是核心方法 |
| culture-engine | HIGH | 文化深层分析是核心方法 |
| anthropology-engine | HIGH | 人类学深层分析是核心方法 |
| religion-engine | HIGH | 宗教深层分析是核心方法 |
| literature-engine | MEDIUM | 文学深层分析常用 |
| art-engine | MEDIUM | 艺术深层分析常用 |
| history-engine | MEDIUM | 历史深层分析常用 |
| political-engine | MEDIUM | 政治深层分析常用 |
| economics-engine | MEDIUM | 经济深层分析常用 |
| education-engine | MEDIUM | 教育深层分析常用 |
| law-engine | MEDIUM | 法律深层分析常用 |
| linguistics-engine | MEDIUM | 语言学深层分析常用 |
| media-communication-engine | MEDIUM | 媒体深层分析常用 |
| cognitive-science-engine | MEDIUM | 认知深层分析常用 |
| music-engine | LOW | 音乐深层分析较少 |
| film-engine | LOW | 电影深层分析较少 |
| business-engine | LOW | 商业深层分析较少 |
| diplomacy-engine | LOW | 外交深层分析较少 |
| architecture-engine | LOW | 建筑深层分析较少 |
| science-engine | LOW | 科学深层分析较少 |
| health-engine | LOW | 医学深层分析较少 |
| urban-planning-engine | LOW | 城市深层分析较少 |
| environment-climate-engine | LOW | 气候深层分析较少 |
| military-engine | LOW | 军事深层分析较少 |
| national-power-engine | LOW | 国力深层分析较少 |
| tech-engine | LOW | 技术深层分析较少 |
| finance-quant-engine | LOW | 金融深层分析较少 |
| data-engine | LOW | 数据深层分析较少 |
| design-engine | LOW | 设计深层分析较少 |
| engineering-engine | LOW | 工程深层分析较少 |
| food-engine | LOW | 食品深层分析较少 |
| mathematics-engine | LOW | 数学深层分析较少 |
| sports-engine | LOW | 体育深层分析较少 |
| aerospace-engine | LOW | 航空航天深层分析较少 |
| biotech-engine | MEDIUM | 生物深层分析常用 |
| energy-engine | LOW | 能源深层分析较少 |
| materials-engine | MEDIUM | 材料深层结构分析常用 |

### 2.5 多利益相关方（multi-stakeholder）× 39 领域引擎

| 领域引擎 | 适配等级 | 说明 |
|----------|---------|------|
| political-engine | HIGH | 政治利益分析是核心方法 |
| business-engine | HIGH | 商业利益分析是核心方法 |
| economics-engine | HIGH | 经济利益分析是核心方法 |
| law-engine | HIGH | 法律利益分析是核心方法 |
| social-engine | HIGH | 社会利益分析是核心方法 |
| diplomacy-engine | HIGH | 外交利益分析是核心方法 |
| health-engine | HIGH | 医疗利益分析是核心方法 |
| environment-climate-engine | HIGH | 环境利益分析是核心方法 |
| urban-planning-engine | HIGH | 城市利益分析是核心方法 |
| education-engine | MEDIUM | 教育利益分析常用 |
| military-engine | MEDIUM | 军事利益分析常用 |
| national-power-engine | MEDIUM | 国力利益分析常用 |
| media-communication-engine | MEDIUM | 媒体利益分析常用 |
| finance-quant-engine | MEDIUM | 金融利益分析常用 |
| tech-engine | MEDIUM | 技术利益分析常用 |
| religion-engine | MEDIUM | 宗教利益分析常用 |
| history-engine | MEDIUM | 历史利益分析常用 |
| psychology-engine | LOW | 心理利益分析较少 |
| philosophy-engine | LOW | 哲学利益分析较少 |
| anthropology-engine | LOW | 人类学利益分析较少 |
| architecture-engine | LOW | 建筑利益分析较少 |
| art-engine | LOW | 艺术利益分析较少 |
| cognitive-science-engine | LOW | 认知利益分析较少 |
| culture-engine | LOW | 文化利益分析较少 |
| data-engine | LOW | 数据利益分析较少 |
| design-engine | LOW | 设计利益分析较少 |
| engineering-engine | LOW | 工程利益分析较少 |
| film-engine | LOW | 电影利益分析较少 |
| food-engine | LOW | 食品利益分析较少 |
| linguistics-engine | LOW | 语言学利益分析较少 |
| literature-engine | LOW | 文学利益分析较少 |
| mathematics-engine | LOW | 数学利益分析较少 |
| music-engine | LOW | 音乐利益分析较少 |
| science-engine | LOW | 科学利益分析较少 |
| sports-engine | LOW | 体育利益分析较少 |
| aerospace-engine | MEDIUM | 航空航天利益分析常用 |
| biotech-engine | MEDIUM | 生物伦理利益分析常用 |
| energy-engine | HIGH | 能源利益分析是核心方法 |
| materials-engine | LOW | 材料利益分析较少 |

### 2.6 规范分析（normative-analysis）× 39 领域引擎

| 领域引擎 | 适配等级 | 说明 |
|----------|---------|------|
| law-engine | HIGH | 法律规范分析是核心方法 |
| philosophy-engine | HIGH | 哲学规范分析是核心方法 |
| political-engine | HIGH | 政治规范分析是核心方法 |
| religion-engine | HIGH | 宗教规范分析是核心方法 |
| ethics-related | HIGH | 伦理规范分析是核心方法 |
| education-engine | HIGH | 教育规范分析是核心方法 |
| social-engine | HIGH | 社会规范分析是核心方法 |
| health-engine | HIGH | 医学伦理规范是核心方法 |
| economics-engine | MEDIUM | 经济规范分析常用 |
| business-engine | MEDIUM | 商业规范分析常用 |
| diplomacy-engine | MEDIUM | 外交规范分析常用 |
| military-engine | MEDIUM | 军事规范分析常用 |
| media-communication-engine | MEDIUM | 媒体规范分析常用 |
| environment-climate-engine | MEDIUM | 环境规范分析常用 |
| urban-planning-engine | MEDIUM | 城市规范分析常用 |
| tech-engine | MEDIUM | 技术规范分析常用 |
| psychology-engine | LOW | 心理规范分析较少 |
| history-engine | LOW | 历史规范分析较少 |
| anthropology-engine | LOW | 人类学规范分析较少 |
| architecture-engine | LOW | 建筑规范分析较少 |
| art-engine | LOW | 艺术规范分析较少 |
| cognitive-science-engine | LOW | 认知规范分析较少 |
| culture-engine | LOW | 文化规范分析较少 |
| data-engine | LOW | 数据规范分析较少 |
| design-engine | LOW | 设计规范分析较少 |
| engineering-engine | LOW | 工程规范分析较少 |
| film-engine | LOW | 电影规范分析较少 |
| finance-quant-engine | LOW | 金融规范分析较少 |
| food-engine | LOW | 食品规范分析较少 |
| linguistics-engine | LOW | 语言学规范分析较少 |
| literature-engine | LOW | 文学规范分析较少 |
| mathematics-engine | LOW | 数学规范分析较少 |
| music-engine | LOW | 音乐规范分析较少 |
| science-engine | LOW | 科学规范分析较少 |
| sports-engine | LOW | 体育规范分析较少 |
| aerospace-engine | LOW | 航空航天规范分析较少 |
| biotech-engine | HIGH | 生物伦理规范是核心方法 |
| energy-engine | MEDIUM | 能源规范分析常用 |
| materials-engine | LOW | 材料规范分析较少 |

### 2.7 系统动力学（system-dynamics）× 39 领域引擎

| 领域引擎 | 适配等级 | 说明 |
|----------|---------|------|
| economics-engine | HIGH | 经济系统动力学是核心方法 |
| environment-climate-engine | HIGH | 气候系统动力学是核心方法 |
| health-engine | HIGH | 公共卫生系统动力学是核心方法 |
| social-engine | HIGH | 社会系统动力学是核心方法 |
| urban-planning-engine | HIGH | 城市系统动力学是核心方法 |
| business-engine | HIGH | 商业系统动力学是核心方法 |
| finance-quant-engine | MEDIUM | 金融系统动力学常用 |
| political-engine | MEDIUM | 政治系统动力学常用 |
| education-engine | MEDIUM | 教育系统动力学常用 |
| military-engine | MEDIUM | 军事系统动力学常用 |
| national-power-engine | MEDIUM | 国力系统动力学常用 |
| tech-engine | MEDIUM | 技术系统动力学常用 |
| science-engine | MEDIUM | 科学系统动力学常用 |
| engineering-engine | MEDIUM | 工程系统动力学常用 |
| media-communication-engine | MEDIUM | 媒体系统动力学常用 |
| cognitive-science-engine | MEDIUM | 认知系统动力学常用 |
| psychology-engine | LOW | 心理系统动力学较少 |
| philosophy-engine | LOW | 哲学系统动力学较少 |
| anthropology-engine | LOW | 人类学系统动力学较少 |
| architecture-engine | LOW | 建筑系统动力学较少 |
| art-engine | LOW | 艺术系统动力学较少 |
| culture-engine | LOW | 文化系统动力学较少 |
| data-engine | LOW | 数据系统动力学较少 |
| design-engine | LOW | 设计系统动力学较少 |
| diplomacy-engine | LOW | 外交系统动力学较少 |
| film-engine | LOW | 电影系统动力学较少 |
| food-engine | LOW | 食品系统动力学较少 |
| history-engine | LOW | 历史系统动力学较少 |
| law-engine | LOW | 法律系统动力学较少 |
| linguistics-engine | LOW | 语言学系统动力学较少 |
| literature-engine | LOW | 文学系统动力学较少 |
| mathematics-engine | LOW | 数学系统动力学较少 |
| music-engine | LOW | 音乐系统动力学较少 |
| religion-engine | LOW | 宗教系统动力学较少 |
| sports-engine | LOW | 体育系统动力学较少 |
| aerospace-engine | HIGH | 航空航天系统动力学是核心方法 |
| biotech-engine | MEDIUM | 生物系统动力学常用 |
| energy-engine | HIGH | 能源系统动力学是核心方法 |
| materials-engine | MEDIUM | 材料系统动力学常用 |

### 2.8 趋势预测（trend-forecast）× 39 领域引擎

| 领域引擎 | 适配等级 | 说明 |
|----------|---------|------|
| tech-engine | HIGH | 技术趋势预测是核心方法 |
| economics-engine | HIGH | 经济趋势预测是核心方法 |
| finance-quant-engine | HIGH | 金融趋势预测是核心方法 |
| political-engine | HIGH | 政治趋势预测是核心方法 |
| environment-climate-engine | HIGH | 气候趋势预测是核心方法 |
| business-engine | HIGH | 商业趋势预测是核心方法 |
| national-power-engine | HIGH | 国力趋势预测是核心方法 |
| military-engine | MEDIUM | 军事趋势预测常用 |
| social-engine | MEDIUM | 社会趋势预测常用 |
| health-engine | MEDIUM | 医学趋势预测常用 |
| education-engine | MEDIUM | 教育趋势预测常用 |
| media-communication-engine | MEDIUM | 媒体趋势预测常用 |
| urban-planning-engine | MEDIUM | 城市趋势预测常用 |
| science-engine | MEDIUM | 科学趋势预测常用 |
| diplomacy-engine | MEDIUM | 外交趋势预测常用 |
| law-engine | MEDIUM | 法律趋势预测常用 |
| psychology-engine | LOW | 心理趋势预测较少 |
| philosophy-engine | LOW | 哲学趋势预测较少 |
| anthropology-engine | LOW | 人类学趋势预测较少 |
| architecture-engine | LOW | 建筑趋势预测较少 |
| art-engine | LOW | 艺术趋势预测较少 |
| cognitive-science-engine | LOW | 认知趋势预测较少 |
| culture-engine | LOW | 文化趋势预测较少 |
| data-engine | LOW | 数据趋势预测较少 |
| design-engine | LOW | 设计趋势预测较少 |
| engineering-engine | LOW | 工程趋势预测较少 |
| film-engine | LOW | 电影趋势预测较少 |
| food-engine | LOW | 食品趋势预测较少 |
| history-engine | LOW | 历史趋势预测较少 |
| linguistics-engine | LOW | 语言学趋势预测较少 |
| literature-engine | LOW | 文学趋势预测较少 |
| mathematics-engine | LOW | 数学趋势预测较少 |
| music-engine | LOW | 音乐趋势预测较少 |
| religion-engine | LOW | 宗教趋势预测较少 |
| sports-engine | LOW | 体育趋势预测较少 |
| aerospace-engine | HIGH | 航空航天趋势预测是核心方法 |
| biotech-engine | HIGH | 生物技术趋势预测是核心方法 |
| energy-engine | HIGH | 能源转型趋势预测是核心方法 |
| materials-engine | HIGH | 材料科学趋势预测是核心方法 |

---

## 三、路由规则

### 3.1 T00 路由流程

```yaml
t00_routing_flow:
  step_1: "T00 读取用户问题与 output_type"
  step_2: "扫描问题特征，匹配思维模板（8 选 1）"
  step_3: "查阅本路由表第一节，匹配思维模型（30 个候选）"
  step_4: "查阅本路由表第二节，根据命中的领域引擎选取适配度 HIGH 的思维模板"
  step_5: "将匹配结果填入 recommended_thinking_models[] 和 recommended_thinking_template"
  step_6: "通过 NRSF §ref 传递给 T08-T13 下游节点"
```

### 3.2 T08-T13 应用规则

```yaml
downstream_application_rule:
  step_1: "T08-T13 从 NRSF §ref:T00 读取 recommended_thinking_models"
  step_2: "节点执行时，实际应用的模型填入 applied_models[]"
  step_3: "applied_models 每条包含：model_id / application_scope / contribution"
  step_4: "若应用了推荐列表外的模型，需在 applied_models 中标注 [EXTRA] 前缀并说明理由"
  step_5: "若推荐列表中的模型未被应用，需在 applied_models 中标注 [SKIPPED] 前缀并说明理由"
```

### 3.3 一致性检查规则（check YAML）

```yaml
applied_models_consistency_check:
  check_1: "applied_models 字段是否存在且非空（至少 1 个模型被应用）"
  check_2: "applied_models 中每个条目是否包含 model_id / application_scope / contribution 三个字段"
  check_3: "applied_models 中标注 [EXTRA] 的模型是否有充分理由（≥20 字）"
  check_4: "recommended_thinking_models 中未被应用的模型是否标注 [SKIPPED] 并说明理由"
  check_5: "applied_models 中 model_id 是否在路由表（本文件第一节）的 30 个模型清单内"
```

---

## 四、统计汇总

| 统计项 | 数量 |
|--------|------|
| 通用思维模型（general/） | 22 |
| 决策思维模型（decision/） | 4 |
| 领域专用思维模型（domain-specific/） | 4 |
| **思维模型总计** | **30** |
| 思维模板（thinking-templates/） | 8 |
| 领域引擎（domains/） | 39 |
| **交叉映射组合总数** | **8 × 39 = 312** |

---

## 知识来源

- `knowledge/thinking-models/general/` — 22 个通用思维模型
- `knowledge/thinking-models/decision/` — 4 个决策思维模型
- `knowledge/thinking-models/domain-specific/` — 4 个领域专用思维模型
- `knowledge/thinking-templates/` — 8 个思维模板
- `knowledge/domains/` — 39 个领域引擎
