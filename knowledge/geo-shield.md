# 地缘防护盾 — 偏见检测规则

> **模块标识**: `knowledge/geo-shield`
> **作者**: 阿洋
> **依赖**: `knowledge/cognitive-framework`, `knowledge/research-methods`
> **核心能力**: 五类偏见预设检测 + 信号词扫描 + 分级处理策略 + 交叉偏见消解
> **上游调用**: T01 输入分流器（`bias_presets.type` 枚举对齐）
> **下游协同**: T18 偏见检测 + 风格检查（认知偏见层面）、sensitivity-framework（敏感度分级）

---

## 1. 总则

地缘防护盾（geo-shield）是 Profound Cognition 输入分流阶段的核心偏见扫描机制。它在 T01 执行时对用户原始问题进行五类偏见预设的系统性检测，输出结构化的 `bias_presets` 数组，并为下游敏感度分级与处理策略提供判定依据。

### 1.1 核心原则

1. **全覆盖扫描**: 每次输入必须逐类扫描全部五种偏见类型，不得跳过任何一类
2. **证据绑定**: 任何 `detected` 判定必须引用用户原文片段作为证据
3. **clean 有据**: 任何 `clean` 判定必须简要说明为何未检出（非空判定理由）
4. **类型严格对齐**: 五类偏见枚举值必须与 T01 `output_schema.bias_presets.type` 完全一致：`geo_bias | cultural_bias | position_preset | frame_preset | narrative_preset`
5. **敏感度联动**: 偏见检测结果直接驱动 `sensitivity_level` 判定——至少2类 `detected` 方可评定 HIGH 及以上

### 1.2 检测输出格式

```json
{
  "type": "geo_bias|cultural_bias|position_preset|frame_preset|narrative_preset",
  "detection_result": "detected|clean",
  "evidence": "string（引用问题原文片段或说明 clean 判定理由）"
}
```

---

## 2. 五类偏见预设定义与检测规则

---

### 2.1 geo_bias（地域偏见）

#### 2.1.1 定义

地域偏见是指在问题表述中隐含了对特定国家、地区、地域群体的刻板印象、优越性/劣等性框架或本质主义归因。它表现为将复杂的地域现象简化为地域本质属性，或以某一地域为中心视角评判其他地域，从而在问题输入阶段即预判了分析方向与结论倾向。

#### 2.1.2 检测信号词库

| 编号 | 中文信号词/短语 | 英文信号词/短语 |
|------|----------------|----------------|
| 1 | 西方中心 | Western-centric / Eurocentric |
| 2 | 东方中心 | Eastern-centric / Asiacentric |
| 3 | 发达国家总是 | developed countries always |
| 4 | 发展中国家就是 | developing countries are just |
| 5 | 某国天生 | inherently / born to |
| 6 | 劣等/低等 | inferior / substandard |
| 7 | 优越/高等 | superior / dominant |
| 8 | 他们那种人 | those people / their kind |
| 9 | 某地人都是 | people from X are all |
| 10 | 落后地区 | backward region / underdeveloped |
| 11 | 文明/野蛮 | civilized / barbaric |
| 12 | 民族劣根性 | national character flaws |
| 13 | 某国特色 | X-style (derogatory) |
| 14 | 地域决定 | geographically determined |
| 15 | 血统/基因决定 | bloodline / genetically determined |
| 16 | 永远不可能 | will never be able to |
| 17 | 本质上就是 | essentially just |
| 18 | 某国模式唯一 | the only model |
| 19 | 地域宿命 | geographic destiny |
| 20 | 不配/没资格 | doesn't deserve / not qualified |
| 21 | 穷国/富国 | poor countries / rich countries (essentializing) |
| 22 | 第三世界就是 | the Third World is just |
| 23 | 地域基因 | regional DNA (metaphorical essentializing) |
| 24 | 与生俱来 | innate / inborn (applied to regions) |
| 25 | 某地永远 | X will always |

#### 2.1.3 检测流程

1. **地域实体提取**: 扫描问题文本，识别所有地域指代实体（国家名、地区名、洲名、民族名、文化圈名）
2. **评价性修饰语匹配**: 对每个地域实体，检查其前后是否附带评价性修饰语（信号词库匹配 + 语义扩展）
3. **归因方向判定**: 判定评价性修饰语的归因方向——是归因于地域本质（偏见信号强）还是归因于具体历史/制度条件（偏见信号弱）
4. **中心-边缘结构识别**: 检测问题是否隐含"中心-边缘"或"核心-附属"的地缘等级结构
5. **综合判定**: 若步骤2-4中任一步检出偏见信号，则 `detection_result: "detected"`，否则 `"clean"` 并注明"问题中地域实体均为中性指代，未发现评价性归因或等级结构"

#### 2.1.4 分级处理策略

| 敏感度 | 处理策略 |
|--------|----------|
| LOW | 标注检出项，在分析中补充对地域刻板印象的消解说明，保持分析中立 |
| MEDIUM | 标注检出项，激活多地域视角平衡输出，至少补充2个不同地域的对照视角 |
| HIGH | 标注检出项并高亮警示，强制执行至少3个地域视角的平衡呈现，每个结论必须标注地域适用范围，禁止将单一地域经验泛化为普遍规律 |
| CRITICAL | 标注检出项并升级为首要约束，仅输出事实陈述与多地域中立分析，明确声明不持地域立场，所有地域相关判断必须附带反地域本质主义的限定声明 |

---

### 2.2 cultural_bias（文化偏见）

#### 2.2.1 定义

文化偏见是指在问题表述中以某一种文化标准作为隐含的普遍尺度来评判其他文化，或假定文化之间存在"先进/落后"的等级秩序。它表现为文化本质主义表述、文化优越感暗示、以及将特定文化实践去语境化后进行跨文化比较时的标准预设。

#### 2.2.2 检测信号词库

| 编号 | 中文信号词/短语 | 英文信号词/短语 |
|------|----------------|----------------|
| 1 | 文明冲突 | clash of civilizations |
| 2 | 先进文化 | advanced culture / progressive culture |
| 3 | 落后文化 | backward culture / primitive culture |
| 4 | 普世价值 | universal values (as cultural imposition) |
| 5 | 文化劣根 | cultural flaws / cultural inferiority |
| 6 | 不开化 | uncivilized / unenlightened |
| 7 | 文化入侵 | cultural invasion (one-directional framing) |
| 8 | 纯正/纯正性 | purity / cultural purity |
| 9 | 同化 | assimilation (as normative goal) |
| 10 | 文化沙漠 | cultural desert / cultural wasteland |
| 11 | 愚昧/迷信 | ignorant / superstitious (cultural labeling) |
| 12 | 文化等级 | cultural hierarchy / cultural ladder |
| 13 | 现代化=西化 | modernization = Westernization |
| 14 | 传统=落后 | traditional = backward |
| 15 | 他们不懂 | they don't understand (cultural condescension) |
| 16 | 文化宿命 | cultural destiny |
| 17 | 野蛮习俗 | barbaric custom |
| 18 | 文化基因决定 | cultural DNA determines |
| 19 | 不符合文明标准 | doesn't meet civilized standards |
| 20 | 文化断层 | cultural fault line (essentializing) |
| 21 | 高等/低等文化 | higher/lower culture |
| 22 | 文化同质化必然 | cultural homogenization is inevitable |
| 23 | 某文化天生 | X culture is inherently |
| 24 | 文化进化 | cultural evolution (unilinear) |
| 25 | 普遍标准 | universal standard (cultural) |

#### 2.2.3 检测流程

1. **文化实体提取**: 扫描问题文本，识别所有文化指代实体（文化名、宗教名、传统名、习俗名、文明圈名）
2. **等级性修饰语匹配**: 对每个文化实体，检查是否存在"先进/落后""高等/低等""文明/野蛮"等等级性修饰
3. **标准预设识别**: 检测问题是否隐含将某一文化标准作为评判其他文化的默认尺度（如以"现代化"隐含"西化"标准）
4. **本质主义归因判定**: 判定文化差异的归因方式——是归因于文化本质（偏见信号强）还是归因于历史/社会/经济条件（偏见信号弱）
5. **综合判定**: 若步骤2-4中任一步检出偏见信号，则 `detection_result: "detected"`，否则 `"clean"` 并注明"问题中文化实体均为描述性指代，未发现等级性修饰或本质主义归因"

#### 2.2.4 分级处理策略

| 敏感度 | 处理策略 |
|--------|----------|
| LOW | 标注检出项，在分析中补充文化相对性说明，指出评判标准的文化依赖性 |
| MEDIUM | 标注检出项，激活多文化视角平衡输出，至少补充2个不同文化传统的对照视角，明确标注评判标准的文化来源 |
| HIGH | 标注检出项并高亮警示，强制执行至少3个文化视角的平衡呈现，每个文化判断必须标注标准来源与适用边界，禁止将单一文化标准泛化为普遍规范 |
| CRITICAL | 标注检出项并升级为首要约束，仅输出事实陈述与多文化中立分析，明确声明不持文化立场，所有文化相关判断必须附带反文化本质主义的限定声明，禁止任何文化等级排序 |

---

### 2.3 position_preset（立场预设）

#### 2.3.1 定义

立场预设是指在问题表述中已经隐含了某一方政治、意识形态或价值立场，使得问题本身不是开放探究而是预设了结论方向。它表现为问题中嵌入了立场性判断词（如"失败""成功""正确""错误"），或以"为什么X是Y"的句式预设了X确实是Y，从而将分析引向对预设立场的论证而非对问题本身的开放考察。

#### 2.3.2 检测信号词库

| 编号 | 中文信号词/短语 | 英文信号词/短语 |
|------|----------------|----------------|
| 1 | 为什么X失败了 | why did X fail |
| 2 | 为什么X是错的 | why is X wrong |
| 3 | X的弊端 | the drawbacks of X (presupposed) |
| 4 | 显然X是不对的 | obviously X is incorrect |
| 5 | X必然导致 | X inevitably leads to |
| 6 | 谁都知道X不好 | everyone knows X is bad |
| 7 | X的危害 | the harm of X (presupposed) |
| 8 | 为什么X会崩溃 | why will X collapse |
| 9 | X注定 | X is doomed / destined to |
| 10 | 证明X是正确的 | prove that X is right |
| 11 | X的阴谋 | X's conspiracy |
| 12 | X在欺骗 | X is deceiving |
| 13 | X的真相 | the truth about X (implying hidden) |
| 14 | 反对X的理由 | reasons to oppose X (presupposed) |
| 15 | 支持X的证据 | evidence supporting X (cherry-picking) |
| 16 | X的问题在于 | the problem with X is |
| 17 | X已经证明了 | X has already proven |
| 18 | 不容置疑 | beyond doubt / unquestionable |
| 19 | 历史已经判定 | history has judged |
| 20 | X的必然结果 | the inevitable result of X |
| 21 | 为什么X总是 | why does X always |
| 22 | X的本质就是 | the essence of X is (negative) |
| 23 | 站在X一边 | taking X's side |
| 24 | X的虚伪 | X's hypocrisy |
| 25 | 不证自明 | self-evident (ideological) |

#### 2.3.3 检测流程

1. **立场性判断词扫描**: 扫描问题文本，匹配信号词库中的立场性判断词和句式模式
2. **预设结论提取**: 识别问题中隐含的预设结论（如"为什么X失败"→预设"X失败"）
3. **开放性检验**: 将问题改写为开放形式，检验原问题是否排除了与预设结论相反的可能性
4. **立场来源追溯**: 判定预设立场的来源——是用户有意识表达还是问题表述中无意识嵌入
5. **综合判定**: 若步骤1-3中任一步检出立场预设信号，则 `detection_result: "detected"`，否则 `"clean"` 并注明"问题为开放探究形式，未发现预设立场或预设结论"

#### 2.3.4 分级处理策略

| 敏感度 | 处理策略 |
|--------|----------|
| LOW | 标注检出项，在分析中将预设结论转化为待检验假设，补充对立立场视角 |
| MEDIUM | 标注检出项，将预设结论显式标注为"待验证假设"，强制补充至少2个对立立场视角，确保分析不围绕预设结论展开 |
| HIGH | 标注检出项并高亮警示，将预设结论拆解为正反两个待验证假设，强制执行至少3个立场视角的平衡呈现，每个结论必须标注立场来源与替代立场 |
| CRITICAL | 标注检出项并升级为首要约束，将预设结论完全悬置，仅输出事实陈述与多立场中立分析，明确声明不持任何政治/意识形态立场，所有立场相关判断必须附带"此为某方立场表述，不代表分析者认同"的标注 |

---

### 2.4 frame_preset（框架预设）

#### 2.4.1 定义

框架预设是指在问题表述中已经选定了特定的理论框架、分析范式或概念体系来封装问题，从而在分析开始之前即限定了可能的结论空间。它表现为问题中嵌入了特定的理论视角（如"从新自由主义视角看""用博弈论分析"），或以特定框架的概念体系构建问题（如"X的成本-收益分析"预设了理性选择框架），使得其他可能更有解释力的框架被排除在视野之外。

#### 2.4.2 检测信号词库

| 编号 | 中文信号词/短语 | 英文信号词/短语 |
|------|----------------|----------------|
| 1 | 从X视角看 | from the perspective of X |
| 2 | 用X理论分析 | analyze using X theory |
| 3 | X框架下 | under the X framework |
| 4 | 按X的逻辑 | following X's logic |
| 5 | X模型表明 | the X model shows |
| 6 | 成本-收益分析 | cost-benefit analysis (as sole frame) |
| 7 | 零和博弈 | zero-sum game (as preset frame) |
| 8 | 阶级斗争视角 | class struggle perspective |
| 9 | 文明冲突框架 | clash of civilizations framework |
| 10 | 现实主义视角 | realist perspective (IR) |
| 11 | 自由主义框架 | liberal framework |
| 12 | 结构主义分析 | structuralist analysis |
| 13 | X范式 | the X paradigm |
| 14 | 用X的方法论 | using X's methodology |
| 15 | X学派认为 | the X school argues (as frame lock) |
| 16 | 唯物史观下 | under historical materialism |
| 17 | 制度经济学视角 | institutional economics perspective |
| 18 | 社会达尔文主义 | Social Darwinism (as frame) |
| 19 | 依附理论 | dependency theory (as sole frame) |
| 20 | X决定论 | X determinism |
| 21 | 只能从X理解 | can only be understood through X |
| 22 | X是唯一解释 | X is the only explanation |
| 23 | 本质上是X问题 | essentially an X problem |
| 24 | X的规律 | the law of X (as universal) |
| 25 | 归根结底是X | ultimately it's X (frame reduction) |

#### 2.4.3 检测流程

1. **框架标识词扫描**: 扫描问题文本，匹配信号词库中的框架标识词和句式模式
2. **框架排他性检验**: 判定问题中指定的框架是否排除了其他框架的可能性（"只能""唯一""归根结底"为强排他信号）
3. **框架适配性评估**: 评估指定框架与研究对象的适配程度——是否为最合适的分析框架，还是窄化了问题视野
4. **替代框架识别**: 尝试识别至少1个可能同样具有解释力的替代框架，若无法识别则框架预设风险较低
5. **综合判定**: 若步骤1-3中任一步检出框架预设信号，则 `detection_result: "detected"`，否则 `"clean"` 并注明"问题未指定特定理论框架，或指定框架为开放性参考而非排他性限定"

#### 2.4.4 分级处理策略

| 敏感度 | 处理策略 |
|--------|----------|
| LOW | 标注检出项，在分析中补充至少1个替代框架视角，说明不同框架可能产生不同结论 |
| MEDIUM | 标注检出项，将指定框架显式标注为"参考框架之一"，强制补充至少2个替代框架视角，对比不同框架的解释力与局限 |
| HIGH | 标注检出项并高亮警示，将指定框架穷尽重试替代为"多个可选框架之一"，强制执行至少3个框架的对比分析，每个结论必须标注其框架依赖性，明确说明换用其他框架可能得出不同结论 |
| CRITICAL | 标注检出项并升级为首要约束，完全悬置指定框架，从问题本身出发重新选择最适配的分析框架（至少3个），明确声明不绑定任何理论框架，所有框架相关判断必须附带"此结论依赖于X框架，换用Y框架可能得出不同结论"的标注 |

---

### 2.5 narrative_preset（叙事预设）

#### 2.5.1 定义

叙事预设是指在问题表述中已经嵌入了特定的叙事结构或情节模板，使得分析尚未开始即被引导向某种戏剧化、目的论或二元对立的解释路径。它表现为问题中隐含"崛起/衰落""危机/机遇""进步/倒退""光明/黑暗"等叙事弧线，或以"转折点""分水岭""终局"等叙事节点构建问题，从而将复杂的非线性过程简化为特定叙事模板下的情节展开。

#### 2.5.2 检测信号词库

| 编号 | 中文信号词/短语 | 英文信号词/短语 |
|------|----------------|----------------|
| 1 | 崛起 | rise / rising (narrative arc) |
| 2 | 衰落 | decline / fall (narrative arc) |
| 3 | 危机 | crisis (as narrative device) |
| 4 | 机遇 | opportunity (binary with crisis) |
| 5 | 转折点 | turning point |
| 6 | 分水岭 | watershed / dividing line |
| 7 | 终局 | endgame / final chapter |
| 8 | 复兴 | renaissance / revival (teleological) |
| 9 | 崩溃 | collapse (dramatic arc) |
| 10 | 黎明 | dawn (progress narrative) |
| 11 | 黑暗 | dark age (decline narrative) |
| 12 | 觉醒 | awakening (teleological) |
| 13 | 没落 | waning / decline (inevitable) |
| 14 | 伟大复兴 | great rejuvenation (teleological) |
| 15 | 百年变局 | century-scale change (dramatic) |
| 16 | 历史必然 | historical inevitability |
| 17 | 不可逆转 | irreversible / unstoppable |
| 18 | 命运抉择 | fateful choice |
| 19 | 最后的机会 | last chance (urgency narrative) |
| 20 | 新时代 | new era (epochal narrative) |
| 21 | 旧秩序瓦解 | old order crumbling |
| 22 | 历史的终结 | end of history |
| 23 | 文明的兴衰 | rise and fall of civilizations |
| 24 | 大变局 | great transformation (dramatic) |
| 25 | 末日/终末 | doomsday / end times (narrative) |

#### 2.5.3 检测流程

1. **叙事弧线词扫描**: 扫描问题文本，匹配信号词库中的叙事弧线词和情节模板词
2. **叙事结构识别**: 判定问题是否嵌入了特定的叙事结构——线性进步叙事、循环兴衰叙事、危机-转机叙事、末世叙事等
3. **戏剧化程度评估**: 评估问题表述的戏剧化程度——是否将复杂过程简化为戏剧性转折，是否赋予事件以目的论意义
4. **替代叙事识别**: 尝试识别至少1种替代叙事结构来解释同一现象，若现象确实只能用当前叙事解释则叙事预设风险较低
5. **综合判定**: 若步骤1-3中任一步检出叙事预设信号，则 `detection_result: "detected"`，否则 `"clean"` 并注明"问题为描述性/分析性表述，未发现叙事弧线或戏剧化结构嵌入"

#### 2.5.4 分级处理策略

| 敏感度 | 处理策略 |
|--------|----------|
| LOW | 标注检出项，在分析中补充对叙事结构的反思说明，指出叙事简化可能遗漏的复杂性 |
| MEDIUM | 标注检出项，将叙事预设显式标注为"叙事简化"，强制补充至少2种替代叙事或非叙事性分析视角，对比叙事解释与结构性解释的差异 |
| HIGH | 标注检出项并高亮警示，将叙事预设拆解为"叙事层"与"事实层"，强制执行叙事去戏剧化处理，每个结论必须区分"叙事性解释"与"结构性解释"，禁止以叙事逻辑替代因果分析 |
| CRITICAL | 标注检出项并升级为首要约束，完全悬置叙事预设，仅输出事实陈述与结构性分析，明确声明不采用任何叙事模板，所有时间性判断必须附带"此为阶段性观察，不构成叙事弧线推断"的限定声明 |

---

## 3. 交叉偏见检测规则

### 3.1 交叉偏见定义

当同一输入文本中同时检出2种及以上偏见类型时，称为交叉偏见。交叉偏见不是各偏见的简单叠加，而是偏见之间的相互强化、嵌套或伪装关系，其风险等级可能高于单一偏见的加总。

### 3.2 交叉偏见组合识别

| 组合模式 | 风险特征 | 典型表现 |
|----------|----------|----------|
| geo_bias + cultural_bias | 地域-文化双重本质化 | 将地域特征归因为文化基因，形成"地域决定文化、文化决定命运"的双重锁定 |
| geo_bias + position_preset | 地域-立场双重预设 | 以地域标签替代立场论证，如"某国当然反对X"将立场归因为地域属性 |
| geo_bias + narrative_preset | 地域-叙事双重简化 | 将地域发展嵌入"崛起/衰落"叙事，如"东方崛起、西方衰落"的二元叙事 |
| cultural_bias + frame_preset | 文化-框架双重锁定 | 以文化本质主义框架分析问题，如"用文明冲突框架分析X"将文化差异固化为文明对立 |
| cultural_bias + position_preset | 文化-立场双重预设 | 将文化差异等同于立场对立，如"X文化天然反对Y" |
| cultural_bias + narrative_preset | 文化-叙事双重戏剧化 | 将文化变迁嵌入"觉醒/没落"叙事，如"传统文化的复兴/消亡" |
| position_preset + frame_preset | 立场-框架双重预设 | 选择与立场一致的理论框架，如"用批判理论证明X的不公正" |
| position_preset + narrative_preset | 立场-叙事双重引导 | 以叙事结构强化立场预设，如"X的衰落证明了Y的正确" |
| frame_preset + narrative_preset | 框架-叙事双重限定 | 理论框架与叙事结构互相强化，如"用周期理论解释文明的兴衰" |
| 三重及以上 | 系统性偏见锁定 | 地域/文化/立场/框架/叙事中三种及以上同时检出，形成封闭的偏见论证回路 |

### 3.3 交叉偏见处理规则

1. **升级规则**: 交叉偏见的敏感度等级取各单一偏见敏感度等级的最大值，并向上提升一级（但不超过 CRITICAL）。例如：geo_bias=MEDIUM + cultural_bias=LOW → 交叉敏感度=HIGH
2. **解耦优先**: 交叉偏见必须先解耦再处理——识别各偏见的独立贡献与交互效应，分别制定消解策略
3. **强化证据要求**: 交叉偏见的 `evidence` 字段必须分别标注每种偏见的独立证据和交叉证据
4. **循环检测**: 当三重及以上偏见同时检出时，必须检测是否存在"偏见论证回路"（A偏见支撑B偏见，B偏见支撑C偏见，C偏见又支撑A偏见），若存在则标记为 CRITICAL 并触发全量悬置处理
5. **穷尽重试替代条件**: 仅当交叉偏见的交互效应经检验为弱（各偏见独立存在且不互相强化）时，方可按独立偏见的最高等级处理而不升级

### 3.4 交叉偏见输出格式

```json
{
  "type": "geo_bias",
  "detection_result": "detected",
  "evidence": "原文片段（独立证据）[交叉:与cultural_bias交互——地域标签与文化本质主义互相强化]"
}
```

---

## 4. 处理策略矩阵

以下矩阵覆盖5种偏见类型 × 4种敏感度等级 = 20个策略单元。每个单元包含：处理动作、视角补充要求、标注要求、禁止事项。

### 4.1 完整矩阵

| 偏见类型 | 敏感度 | 处理动作 | 视角补充 | 标注要求 | 禁止事项 |
|----------|--------|----------|----------|----------|----------|
| **geo_bias** | LOW | 标注检出项，补充地域刻板印象消解说明 | 补充1个不同地域对照视角 | 标注地域偏见的检出位置与信号词 | 禁止将单一地域经验泛化为普遍规律 |
| **geo_bias** | MEDIUM | 标注检出项，激活多地域视角平衡输出 | 补充至少2个不同地域对照视角 | 标注地域偏见的检出位置、信号词与消解措施 | 禁止地域本质主义归因；禁止单一地域视角主导分析 |
| **geo_bias** | HIGH | 标注检出项并高亮警示，强制多地域平衡 | 强制至少3个地域视角平衡呈现 | 标注地域偏见的检出位置、信号词、消解措施与每个结论的地域适用范围 | 禁止地域本质主义归因；禁止单一地域视角主导；禁止将地域经验泛化 |
| **geo_bias** | CRITICAL | 标注检出项并升级为首要约束，仅输出事实与多地域中立分析 | 强制至少3个地域视角，每个结论附带反地域本质主义限定 | 声明不持地域立场；每个地域判断附带反本质主义限定声明 | 禁止任何地域等级排序；禁止地域本质主义归因；禁止隐含地域优越性 |
| **cultural_bias** | LOW | 标注检出项，补充文化相对性说明 | 补充1个不同文化传统对照视角 | 标注文化偏见的检出位置与信号词 | 禁止将单一文化标准泛化为普遍规范 |
| **cultural_bias** | MEDIUM | 标注检出项，激活多文化视角平衡输出 | 补充至少2个不同文化传统对照视角，标注评判标准的文化来源 | 标注文化偏见的检出位置、信号词与评判标准来源 | 禁止文化本质主义归因；禁止以单一文化标准评判其他文化 |
| **cultural_bias** | HIGH | 标注检出项并高亮警示，强制多文化平衡 | 强制至少3个文化视角平衡呈现 | 标注文化偏见的检出位置、信号词、评判标准来源与每个文化判断的适用边界 | 禁止文化本质主义归因；禁止文化等级排序；禁止单一文化标准泛化 |
| **cultural_bias** | CRITICAL | 标注检出项并升级为首要约束，仅输出事实与多文化中立分析 | 强制至少3个文化视角，每个判断附带反文化本质主义限定 | 声明不持文化立场；每个文化判断附带反本质主义限定声明 | 禁止任何文化等级排序；禁止文化本质主义归因；禁止隐含文化优越性 |
| **position_preset** | LOW | 标注检出项，将预设结论转化为待检验假设 | 补充1个对立立场视角 | 标注立场预设的检出位置与预设结论 | 禁止围绕预设结论展开分析 |
| **position_preset** | MEDIUM | 标注检出项，将预设结论显式标注为"待验证假设" | 补充至少2个对立立场视角 | 标注立场预设的检出位置、预设结论与替代立场 | 禁止围绕预设结论展开分析；禁止忽略与预设结论矛盾的证据 |
| **position_preset** | HIGH | 标注检出项并高亮警示，将预设结论拆解为正反两个待验证假设 | 强制至少3个立场视角平衡呈现 | 标注立场预设的检出位置、预设结论、替代立场与每个结论的立场来源 | 禁止围绕预设结论展开；禁止忽略矛盾证据；禁止立场性结论无来源标注 |
| **position_preset** | CRITICAL | 标注检出项并升级为首要约束，将预设结论完全悬置 | 仅输出事实陈述与多立场中立分析 | 声明不持任何政治/意识形态立场；每个立场判断附带"此为某方立场表述"标注 | 禁止任何立场性结论；禁止隐含立场倾向；禁止将立场包装为事实 |
| **frame_preset** | LOW | 标注检出项，补充替代框架视角 | 补充至少1个替代框架视角 | 标注框架预设的检出位置与指定框架 | 禁止将指定框架作为唯一分析工具 |
| **frame_preset** | MEDIUM | 标注检出项，将指定框架穷尽重试替代为"参考框架之一" | 补充至少2个替代框架视角，对比解释力与局限 | 标注框架预设的检出位置、指定框架与替代框架 | 禁止框架排他性锁定；禁止忽略框架外的解释路径 |
| **frame_preset** | HIGH | 标注检出项并高亮警示，将指定框架穷尽重试替代为"多个可选框架之一" | 强制至少3个框架的对比分析 | 标注框架预设的检出位置、指定框架、替代框架与每个结论的框架依赖性 | 禁止框架排他性锁定；禁止忽略框架外解释；禁止结论无框架依赖标注 |
| **frame_preset** | CRITICAL | 标注检出项并升级为首要约束，完全悬置指定框架 | 从问题本身出发重新选择至少3个适配框架 | 声明不绑定任何理论框架；每个结论附带框架依赖性标注 | 禁止任何框架排他性声明；禁止框架决定论；禁止隐含框架优越性 |
| **narrative_preset** | LOW | 标注检出项，补充叙事结构反思说明 | 补充1种替代叙事或非叙事性分析视角 | 标注叙事预设的检出位置与叙事类型 | 禁止以叙事逻辑替代因果分析 |
| **narrative_preset** | MEDIUM | 标注检出项，将叙事预设显式标注为"叙事简化" | 补充至少2种替代叙事或非叙事性分析视角 | 标注叙事预设的检出位置、叙事类型与替代叙事 | 禁止以叙事逻辑替代因果分析；禁止戏剧化表述替代结构性解释 |
| **narrative_preset** | HIGH | 标注检出项并高亮警示，将叙事预设拆解为"叙事层"与"事实层" | 强制叙事去戏剧化处理，至少3种分析视角 | 标注叙事预设的检出位置、叙事类型、替代叙事与每个结论的"叙事/结构"分类 | 禁止以叙事逻辑替代因果分析；禁止戏剧化表述；禁止目的论推断 |
| **narrative_preset** | CRITICAL | 标注检出项并升级为首要约束，完全悬置叙事预设 | 仅输出事实陈述与结构性分析 | 声明不采用任何叙事模板；每个时间性判断附带"阶段性观察，不构成叙事弧线推断"限定 | 禁止任何叙事模板嵌入；禁止目的论推断；禁止戏剧化表述；禁止"历史必然"类断言 |

### 4.2 矩阵速查规则

- **行定位**: 根据偏见类型定位行
- **列定位**: 根据敏感度等级定位列
- **优先级**: CRITICAL > HIGH > MEDIUM > LOW（当同一偏见类型在不同上下文中可能对应不同敏感度时，取较高等级）
- **叠加规则**: 当多种偏见同时检出时，执行各偏见对应策略的并集（取最严格约束）

---

## 5. 检测执行协议

### 5.1 执行顺序

```
输入文本 → 逐类扫描（geo_bias → cultural_bias → position_preset → frame_preset → narrative_preset）
         → 交叉偏见检测
         → 敏感度联动判定
         → 输出 bias_presets 数组
```

### 5.2 扫描完整性校验

输出前必须确认以下校验项全部通过：

- [ ] 五类偏见是否**全部**扫描（geo_bias、cultural_bias、position_preset、frame_preset、narrative_preset）？
- [ ] 每个 `detection_result: "detected"` 的项是否引用了用户原文片段作为 `evidence`？
- [ ] 每个 `detection_result: "clean"` 的项是否给出了判定理由（非空）？
- [ ] 交叉偏见是否已检测（2种及以上 `detected` 时）？
- [ ] 敏感度等级是否与偏见扫描结果一致（至少2类 `detected` 方可评定 HIGH 及以上）？

### 5.3 禁止事项

- 禁止跳过任何一类偏见的扫描
- 禁止在 `evidence` 字段中使用模糊表述（必须引用原文或给出明确理由）
- 禁止将 `sensitivity_level` 默认设为 LOW（需有充分理由）
- 禁止在偏见扫描阶段输出分析结论或价值判断（仅报告"是否检测到"及"依据"）
- 禁止将交叉偏见的处理简化为单一偏见的处理（必须执行解耦分析）

---

## 6. 与 T01 output_schema 的对齐映射

| geo-shield 输出 | T01 output_schema 字段 | 对齐说明 |
|-----------------|----------------------|----------|
| 偏见类型枚举 | `bias_presets[].type` | 严格对齐：geo_bias \| cultural_bias \| position_preset \| frame_preset \| narrative_preset |
| 检测结果 | `bias_presets[].detection_result` | 对齐：detected \| clean |
| 证据/理由 | `bias_presets[].evidence` | 对齐：引用原文片段或 clean 判定理由 |
| 敏感度等级 | `sensitivity_level` | 联动：偏见检测结果驱动敏感度分级 |
| 交叉偏见标记 | `bias_presets[].evidence` 内嵌 | 在 evidence 字段中以 [交叉:...] 标注交互效应 |

---

© 阿洋
