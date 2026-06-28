# 规范分析 — 从应然标准到可行路径的三层递进推理

> **模块标识**: `knowledge/thinking-templates/normative-analysis`
> **设计依据**: 基于全域深度认知框架三层推理架构设计——规范分析遵循"应然标准锚定→实然差距诊断→可然路径设计"三步递进逻辑
> **依赖**: `knowledge/cognitive-framework`、`knowledge/research-methods`
> **骨架类型**: 规范分析 (Normative Analysis)
>
> **版本治理元数据 (D12.4.2)**:
> - version: 1.1
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（应然→实然→可然三层递进）
>   - v1.1 补全版本治理元数据与交叉引用（D12.4.2-D12.4.3）

## 交叉引用

- **上游**: `knowledge/cognitive-framework.md`、`knowledge/research-methods.md`
- **下游**: `tasks/T09_cog_reason.md`（认知推理，应用规范分析模板）、`tasks/T19b_prescription_gate.md`（处方门控，规范分析产出处方）
- **相关**: `knowledge/ethics-references.md`（伦理标准，应然标准参考）、`knowledge/thinking-templates/multi-stakeholder.md`（多利益相关方模板）、`knowledge/thinking-models/routing-table.md`（思维模型路由表）

---

## 模板与模型的边界（D6.4.1）

> 本节明确「思维模板」（骨架级）与「思维模型」（方法论级）的边界与协作关系。

| 维度 | 思维模板（本文件） | 思维模型（thinking-models/） |
|------|------------------|---------------------------|
| **层级** | 骨架级（Skeleton-level） | 方法论级（Methodology-level） |
| **职责** | 提供"如何执行"的步骤流程 | 提供"为什么这样执行"的理论背景 |
| **内容** | 可执行伪代码 + 输入输出 schema + 失败模式闭环 | 理论渊源 + 假设体系 + 适用条件 + 局限性 |
| **抽象度** | 中（直接可调用） | 高（需模板将其落地为具体步骤） |
| **调用关系** | 模板调用模型的方法论指导 | 模型为模板提供理论支撑和边界条件 |

**本模板对应的方法论级模型**：
- `knowledge/ethics-references.md`（伦理标准 — 应然标准的参考体系）
- `knowledge/thinking-models/general/critical-thinking.md`（批判性思维 — 价值判断审视的逻辑工具）

**边界声明**：本模板提供三步规范分析的执行流程（应然锚定→实然诊断→可然设计的伪代码），不重复阐述伦理学理论体系或批判性思维的哲学基础。当需要理论依据时，调用上述模型文件。本模板面向跨域政策分析，区别于 philosophy-engine 面向纯伦理问题的义务论/后果论/德性论推理。

---

## 1. 定义

规范分析是一种系统化回答"应该怎么做"的推理方法。它不同于实然分析（追问"是什么"和"为什么"），也不同于哲学伦理思辨（追问"什么是好的"），而是在"应然标准 → 实然差距 → 可然路径"三层递进中，揭示标准的定义权归属、差距的结构性成因、以及改进路径的约束条件与合法性来源。

规范分析承认一个核心前提：在大多数现实问题中，"好"的定义本身就是争议性的。因此，规范分析不是输出一个"正确"的价值判断，而是呈现应然标准的多元竞争格局，并在此基础上评估各条改进路径的可行性和合法性。

**核心法则**: 好的规范分析不输出道德判断句，而是揭示应然标准的定义权归属、实然差距的结构性成因、以及可行路径的约束条件与合法性来源。分析者本人的价值偏好应被显性标注为"alternative_normative_frameworks"而非伪装为域内共识。

**与 philosophy-engine 的区别**：philosophy-engine 面向哲学伦理问题，使用义务论/后果论/德性论的经典框架（如"撒谎是错的"类推理）。本模板面向跨域政策分析、商业伦理、技术监管、社会规范等实际决策问题——在这些问题中，核心任务不是"这个行为在道德上对不对"，而是"在多个相互竞争的应然标准中，当前差距的结构性成因是什么，最可行的改进路径是什么"。

---

## 2. 核心概念

| 概念 | 定义 | 分析要点 |
|------|------|----------|
| **应然标准 (Normative Standard)** | 该领域中"好/正确"的判定标准 | 标准的定义权归属、合法性来源、是否被普遍接受抑或存在争议 |
| **实然差距 (Descriptive Gap)** | 当前状态与应然标准之间的偏离 | 差距的度量方式（定量优先）、差距扩大/缩小/稳定的趋势判断、结构性成因 |
| **可然路径 (Feasible Pathway)** | 在现有约束下可行的改进方案 | 政治可行性、经济成本、技术可达性、社会接受度的四维评估 |
| **合法性来源 (Source of Legitimacy)** | 标准或路径的正当性根基 | 法律授权、专业共识、民主程序、伦理原则、市场效率——每种来源有不同的适用范围和强度 |
| **价值冲突 (Value Conflict)** | 不可调和的价值目标矛盾 | 区分真正的零和冲突（安全 vs 自由）与伪冲突（通过方案设计可同时实现的目标） |
| **规范竞争 (Normative Contestation)** | 不同应然标准之间的竞争 | 哪个标准正在主导制度设计？哪个标准被边缘化？边缘化是正当的还是不公正的？ |

---

## 3. 三步分析流程

```
步骤1: 应然标准锚定
  ├─ 识别问题域中存在的应然标准（通常多个且互相冲突）
  ├─ 每个标准需回答：谁定义了这个标准？定义者为何有定义权？
  ├─ 合法性来源分类：法律授权 / 专业共识 / 民主程序 / 伦理原则 / 市场效率
  ├─ 判断各标准的接受范围：域内共识 / 多数接受 / 有争议 / 少数主张
  ├─ 标注不可调和的标准冲突（如安全优先 vs 效率优先）
  └─ 输出：领域应然标准地图（含冲突标注与定义权归属）

步骤2: 实然差距诊断
  ├─ 度量当前状态：定量优先（如覆盖率%、合规率%），不可量化时用定性刻度（严重/中等/轻微偏离）
  ├─ 计算差距：当前状态相对于每条应然标准的偏离方向和程度
  ├─ 趋势判断：差距在扩大/缩小/稳定？（需至少一个时间序列数据点支持）
  ├─ 结构性成因分析：
  │    ├─ 差距为何存在？（直接驱动因素）
  │    ├─ 谁从中获益？（既得利益结构）
  │    └─ 什么机制维持了差距？（制度锁定、激励错位、认知偏差）
  └─ 输出：差距诊断报告（含趋势箭头与结构性成因）

步骤3: 可然路径设计
  ├─ 生成候选改进路径（至少3条，每条对应不同的应然标准侧重或利益偏好）
  ├─ 四维可行性评估：
  │    ├─ 政治可行性：是否有足够的政治意愿和支持联盟？
  │    ├─ 经济可行性：成本多少？谁承担？收益是否超过成本？
  │    ├─ 技术可行性：所需技术是否成熟？部署周期多长？
  │    └─ 社会可行性：公众接受度如何？是否会引发社会反弹？
  ├─ 标注每条路径的合法性来源和实施后可能面临的系统性抵抗
  ├─ 区分"真正可行的路径" vs "理论上成立但实践中受阻的路径"，说明受阻原因
  └─ 输出：可行路径矩阵（含排序与理由，优先推荐综合可行性最高的路径）
```

### 3.1 可执行伪代码（D6.4.3）

```python
def normative_analysis(domain, problem_statement):
    """
    规范分析模板 - 可执行伪代码（D6.4.3）
    输入: domain(分析领域标识), problem_statement(规范性问题)
    输出: normative_analysis YAML（见 §5 输出模板）
    """
    # ===== 步骤1: 应然标准锚定 =====
    standards = identify_normative_standards(domain, problem_statement)
    # 通常多个且互相冲突
    for std in standards:
        std["defined_by"] = identify_definer(std)  # 谁定义了这个标准？
        std["source_of_legitimacy"] = classify_legitimacy(std)
        # legal_authority | professional_consensus | democratic_process | ethical_principle | market_efficiency
        std["acceptance"] = assess_acceptance(std)
        # domain_consensus | majority | contested | minority
        std["competing_with"] = identify_competing_standards(std, standards)

    # 标注不可调和的标准冲突
    conflicts = []
    for s1, s2 in combinations(standards, 2):
        conflict = analyze_standard_conflict(s1, s2)
        if conflict:
            conflicts.append({
                "standards": [s1["id"], s2["id"]],
                "nature": conflict.nature,  # zero_sum | partial_overlap | pseudo_conflict
                "description": conflict.description
            })

    # ===== 步骤2: 实然差距诊断 =====
    current_state = measure_current_state(domain)  # 定量优先
    gaps = []
    for std in standards:
        gap = calculate_gap(current_state, std)
        gaps.append({
            "against_standard": std["id"],
            "degree": gap.degree,  # 偏离方向和程度
            "measurement": gap.measurement_method,
            "trend": assess_trend(gap),  # widening | stable | narrowing
            "data_source": gap.data_source
        })

    # 结构性成因分析
    structural_causes = []
    for gap in gaps:
        causes = analyze_structural_causes(gap)
        structural_causes.append({
            "description": causes.description,
            "beneficiaries": causes.beneficiaries,  # 谁从中获益？
            "sustaining_mechanism": causes.sustaining_mechanism  # 什么机制维持了差距？
        })

    # ===== 步骤3: 可然路径设计 =====
    # 生成候选改进路径（至少3条）
    candidate_pathways = generate_candidate_pathways(standards, gaps, structural_causes)
    assert len(candidate_pathways) >= 3, "需至少3条候选路径"

    feasible_pathways = []
    for i, pathway in enumerate(candidate_pathways):
        # 四维可行性评估
        feasibility = {
            "political": assess_political_feasibility(pathway),  # 政治意愿和支持联盟？
            "economic": assess_economic_feasibility(pathway),    # 成本多少？谁承担？
            "technical": assess_technical_feasibility(pathway),  # 技术成熟度？部署周期？
            "social": assess_social_feasibility(pathway)         # 公众接受度？社会反弹？
        }
        # 标注合法性来源和系统性抵抗
        pathway["id"] = f"FP-{i+1:02d}"
        pathway["aligned_with_standard"] = identify_aligned_standard(pathway, standards)
        pathway["feasibility"] = feasibility
        pathway["systemic_resistance_expected"] = predict_resistance(pathway)
        pathway["legitimacy"] = identify_legitimacy_source(pathway)
        # 区分真正可行 vs 理论成立但实践受阻
        pathway["rank"] = rank_feasibility(pathway)
        feasible_pathways.append(pathway)

    # 优先推荐综合可行性最高的路径
    feasible_pathways.sort(key=lambda p: p["rank"])

    # ===== 元反思 =====
    meta_reflection = {
        "alternative_normative_frameworks": identify_alternative_frameworks(standards),
        "irreconcilable_conflicts": [c for c in conflicts if c["nature"] == "zero_sum"],
        "caveats": declare_analysis_limitations(domain, standards, gaps)
    }

    return {
        "domain": domain,
        "problem_statement": problem_statement,
        "normative_landscape": {"standards": standards, "conflicts": conflicts},
        "descriptive_gap": {"current_state": current_state, "gaps": gaps,
                           "structural_causes": structural_causes},
        "feasible_pathways": feasible_pathways,
        "meta_reflection": meta_reflection
    }
```

---

## 4. 常见陷阱

| 陷阱 | 表现 | 纠正方案 |
|------|------|----------|
| **用哲学框架替代政策框架** | 对政策问题输出"义务论认为应尊重人的自主性、后果论认为应最大化社会福利"等哲学化论述，而非分析谁定义了监管标准、现行框架与标准的差距是什么 | 第一步先问"在这个领域，谁定义了'好的结果/正确的做法'？"，而非"这个行为在道德上对不对"。philosophy-engine 是为纯伦理问题设计的，本模板是为决策分析设计的 |
| **应然标准单一化** | 只呈现一种应然标准（通常是分析者认为"对"的那个），忽略该领域中事实上存在的标准竞争——如只讲"安全第一"不讲"效率优先" | 主动追问："还有谁在定义这个领域的标准？他们的标准是什么？为什么他们的标准没有被采纳？"确保至少呈现2-3个竞争性的应然标准 |
| **路径脱离约束** | 提出理想化方案（"政府应出台更严格的法规"、"行业应建立自律机制"）但未评估任何可行性维度 | 每条路径必须过四维可行性检查：政治能否推动？经济是否可持续？技术是否可达？社会是否接受？任何一维不可行就需标注并说明原因 |
| **混淆应然与偏好** | 将分析者自身的价值偏好包装为"域内共识"或"唯一合理的标准"，如将"我支持减少监管"等同于"减少监管是正确方向" | 区分"域内公认的应然标准"（有文献/制度/调查证据支持）与"分析者个人认为的标准"。后者放入 `meta_reflection.alternative_normative_frameworks` 并显性标注 |

---

## 5. 输出模板

```yaml
normative_analysis:
  domain: "分析领域标识"
  problem_statement: "需要回答的规范性问题（一句话）"

  normative_landscape:
    standards:
      - id: "NS-01"
        name: "应然标准名称"
        definition: "标准的具体定义"
        defined_by: "该标准的定义者（机构/群体/学派）"
        source_of_legitimacy: "legal_authority|professional_consensus|democratic_process|ethical_principle|market_efficiency"
        acceptance: "domain_consensus|majority|contested|minority"
        competing_with: ["与之竞争的应然标准ID列表"]
    conflicts:
      - standards: ["NS-01", "NS-02"]
        nature: "zero_sum|partial_overlap|pseudo_conflict"
        description: "冲突的本质"

  descriptive_gap:
    current_state: "当前实际状态（尽量量化）"
    gaps:
      - against_standard: "NS-01"
        degree: "偏离方向和程度"
        measurement: "度量方式"
        trend: "widening|stable|narrowing"
        data_source: "度量数据来源"
    structural_causes:
      - description: "结构性成因描述"
        beneficiaries: ["从该差距中获益的主体"]
        sustaining_mechanism: "维持该差距的制度/激励/认知机制"

  feasible_pathways:
    - id: "FP-01"
      description: "路径描述"
      aligned_with_standard: "该路径主要服务于哪个应然标准"
      feasibility:
        political: "政治可行性评估（含推动力量与阻力）"
        economic: "经济可行性评估（含成本估算与承担方）"
        technical: "技术可行性评估（含成熟度与部署周期）"
        social: "社会可行性评估（含公众接受度与潜在反弹）"
      systemic_resistance_expected: ["实施后预计会遇到的系统性抵抗"]
      legitimacy: "路径本身的合法性来源"
      rank: "综合可行性排名（1=最可行）"

  meta_reflection:
    alternative_normative_frameworks: ["分析者认知但域内未成为主流的替代框架"]
    irreconcilable_conflicts: ["当前条件下不可调和的价值冲突"]
    caveats: "分析的局限性和适用边界"
```

---

## 6. 快速调用指南

当问题包含以下特征时，优先使用本骨架：

- 问题形式为"X 应该怎么做？""正确的标准是什么？""谁有责任/义务做 Y？"
- 涉及政策方案评估（"哪个政策方案更好？为什么？"）
- 涉及伦理边界划定（"这种行为是否应当被允许？由谁判断？"）
- 涉及合规与监管问题（"当前监管是否充分？哪里存在缺口？"）
- 涉及价值冲突（"在安全和效率之间如何权衡？"）
- 触发关键词：应该、应当、规范、伦理、合规、合法性、正当性、标准、责任、义务、监管、底线

---

## 附录：跨域应用示例

### 示例 1：政策分析 — AI 监管政策

**问题**："生成式 AI 应该如何监管？"

**应然标准地图**：
- NS-01（安全底线）：由政府和公共安全机构定义，合法性来源为法律授权。确保 AI 不造成大规模伤害。
- NS-02（创新空间）：由科技企业和创新倡导者定义，合法性来源为市场效率。确保监管不扼杀技术进步和产业竞争力。
- NS-03（公平竞争）：由中小企业和反垄断机构定义，合法性来源为法律授权+市场效率。确保大企业不利用监管壁垒形成垄断。
- 冲突：NS-01 与 NS-02 之间存在零和冲突——更严格的审查必然增加创新成本。

**实然差距**：现行《生成式人工智能服务管理暂行办法》提供了原则性框架但缺乏细则，执行力度因地区而异。中小企业在合规成本上面临不成比例的压力（安全底线与公平竞争的次要冲突）。

**可然路径矩阵**：
- FP-01（分层监管）：按风险等级分层，高风险应用严格许可、低风险应用备案即用。政治可行性高（与现行框架兼容），经济成本中等。
- FP-02（沙盒机制）：设立监管沙盒，允许在受控环境中测试创新应用。技术可行性高，但需设计退出沙盒后的合规衔接机制。
- FP-03（算法审计）：强制第三方算法审计。政治可行性中等（业界阻力大），但透明度效益显著。

### 示例 2：商业伦理 — 平台算法透明度

**问题**："电商平台的推荐算法应该向用户披露到什么程度？"

**应然标准地图**：
- NS-01（用户知情权）：由消费者保护机构和用户倡导者定义，合法性来源为伦理原则。用户有权知道为什么看到这个推荐。
- NS-02（商业机密保护）：由平台企业定义，合法性来源为市场效率。算法是核心竞争力，过度披露将削弱竞争优势。
- NS-03（防止操纵）：由监管机构定义，合法性来源为法律授权。算法不得用于操纵消费决策。
- 冲突：NS-01 与 NS-02 在披露程度上存在零和冲突。

**实然差距**：当前主流平台仅提供泛化的"基于您的浏览历史"说明，不披露权重因子、排序逻辑或付费推广与非付费结果的区分。欧盟 DSA 已开始要求超大型平台提供算法透明度报告，但亚太地区的披露水平仍较低。

**可然路径矩阵**：
- FP-01（分级披露）：对普通用户提供简明版说明（"为什么看到这个"），对研究者提供 API 审计接口。平衡知情权与商业机密。
- FP-02（标签制度）：对算法推荐内容添加"推荐"标签，对广告内容添加"广告"标签。社会可行性高、成本低。
- FP-03（用户控制面板）：允许用户查看和调整影响推荐的因素（兴趣标签、价格偏好等）。技术可行性中等。

### 示例 3：技术监管 — 人脸识别技术部署

**问题**："公共场所的人脸识别技术应该在什么条件下被允许部署？"

**应然标准地图**：
- NS-01（公共安全）：由执法和安全机构定义，合法性来源为法律授权。人脸识别是预防和侦破犯罪的有效工具。
- NS-02（隐私保护）：由隐私倡导者和公民社会组织定义，合法性来源为伦理原则+法律授权。大规模无差别人脸采集侵犯基本隐私权。
- NS-03（技术可靠性）：由技术标准机构定义，合法性来源为专业共识。技术本身存在偏见（对某些族群识别准确率低），部署可能加剧歧视。
- 冲突：NS-01 与 NS-02 是经典的零和冲突——更强的安全监控必然削弱隐私保护。

**实然差距**：中国在公共场所已大规模部署人脸识别，覆盖率全球领先，但法规层面（《个人信息保护法》）对公共场所生物特征采集的规定仍在细化阶段。英国和欧盟已出台较严格的限制框架（仅在严重犯罪调查中使用）。技术层面的偏见问题已有大量研究证据但在中国的监管讨论中涉及较少。

**可然路径矩阵**：
- FP-01（场景化授权）：区分"重大安全场景"（反恐、追逃——可部署）与"一般管理场景"（交通违章、市容管理——需更高门槛）。政治可行性高，是现行政策中的主流讨论方向。
- FP-02（独立审计+影响评估）：任何部署前强制完成隐私影响评估和算法偏见审计。技术可行性中等（需要成熟的审计标准体系）。
- FP-03（时限+用途限制）：采集数据仅可在指定时间内用于指定目的，到期强制删除。与现行《个人信息保护法》的最小必要原则兼容。
- FP-04（公众知情+退出机制）：部署区域明确标识、提供非人脸识别的替代通道。社会接受度改进效果显著但增加实施成本。

---

## 7. 失败模式闭环清单（D6.4.4）

> 本节提供「失败模式 → 检测信号 → 恢复策略」三列结构，配套检测伪代码，确保规范分析的常见失败模式可被自动识别与修复。

| 失败模式 | 检测信号 | 恢复策略 |
|---------|---------|---------|
| **用哲学框架替代政策框架** | 输出包含"义务论认为/后果论认为/德性论认为"但缺少"谁定义了监管标准/现行框架与标准的差距" | 切换到政策分析视角：第一步先问"在这个领域，谁定义了'好的结果'？"，调用 `identify_normative_standards()` 重新锚定应然标准 |
| **应然标准单一化** | `standards` 列表长度 < 2 或所有标准的 `defined_by` 相同 | 主动追问"还有谁在定义这个领域的标准？"，强制生成至少 2-3 个竞争性应然标准，调用 `identify_competing_standards()` |
| **路径脱离约束** | `feasible_pathways` 中存在 `feasibility` 字段为空或四维评估不完整的路径 | 对每条路径强制执行四维可行性检查（政治/经济/技术/社会），任何一维不可行就标注并说明原因 |
| **混淆应然与偏好** | `meta_reflection.alternative_normative_frameworks` 为空，但 `standards` 中存在 `acceptance=minority` 的标准被当作 `domain_consensus` | 区分"域内公认的应然标准"与"分析者个人认为的标准"，后者放入 `alternative_normative_frameworks` 并显性标注 |
| **差距度量不可量化** | `gaps[].measurement` 为空或仅用"严重/中等/轻微"等定性刻度，且 `data_source` 为空 | 优先寻找定量度量（覆盖率%/合规率%），无定量数据时标注 `measurement=qualitative` 并声明数据缺口 |
| **趋势判断无数据** | `gaps[].trend` 字段存在但 `data_source` 为空，或趋势判断无时间序列数据支持 | 强制要求至少一个时间序列数据点支持趋势判断，无数据时标注 `trend=unknown` 并声明数据不足 |
| **合法性来源误判** | `source_of_legitimacy` 字段值与实际定义者不符（如政府机构定义的标准标注为 `market_efficiency`） | 重新审视定义者身份与合法性来源的对应关系：法律授权→政府/监管机构，专业共识→专业组织/学术机构，民主程序→民选机构，伦理原则→伦理委员会/公民社会，市场效率→企业/市场参与者 |
| **可行性评估缺失** | `feasible_pathways` 中某条路径的 `feasibility` 四维中任一维度为空或仅写"可行/不可行"无理由 | 对每个维度强制提供理由：政治可行性→推动力量与阻力；经济可行性→成本估算与承担方；技术可行性→成熟度与部署周期；社会可行性→公众接受度与潜在反弹 |
| **价值冲突伪冲突** | `conflicts[].nature` 标注为 `zero_sum` 但未检验是否存在通过方案设计可同时实现的伪冲突 | 对每个 `zero_sum` 冲突追问"是否存在方案设计能同时满足两个标准？"若存在则改标为 `pseudo_conflict` 并记录方案 |
| **路径排序无理由** | `feasible_pathways` 的 `rank` 字段存在但无排序依据，或所有路径 `rank=1` | 强制按四维可行性综合评分排序，记录排序理由（哪一维度决定了排名差异） |

### 7.1 失败模式检测伪代码

```python
def detect_and_recover_normative_failures(analysis_result):
    """
    规范分析失败模式检测与恢复（D6.4.4）
    输入: analysis_result（normative_analysis YAML 输出）
    输出: failure_report + recovered_analysis
    """
    failures = []

    # FM-01: 用哲学框架替代政策框架
    if contains_philosophy_frameworks(analysis_result) and \
       not has_policy_analysis_elements(analysis_result):
        failures.append({
            "mode": "philosophy_substitution",
            "signal": "输出包含义务论/后果论/德性论但缺少应然标准地图",
            "recovery": "切换到政策分析视角，调用 identify_normative_standards() 重新锚定"
        })

    # FM-02: 应然标准单一化
    standards = analysis_result["normative_landscape"]["standards"]
    if len(standards) < 2 or len(set(s["defined_by"] for s in standards)) < 2:
        failures.append({
            "mode": "standard_monoculture",
            "signal": f"应然标准数量={len(standards)}（<2）或定义者单一",
            "recovery": "强制生成至少2-3个竞争性应然标准，调用 identify_competing_standards()"
        })

    # FM-03: 路径脱离约束
    for pathway in analysis_result["feasible_pathways"]:
        feas = pathway.get("feasibility", {})
        if not all(k in feas and feas[k] for k in ["political", "economic", "technical", "social"]):
            failures.append({
                "mode": "pathway_without_constraints",
                "signal": f"路径 {pathway['id']} 四维可行性评估不完整",
                "recovery": "强制执行四维可行性检查，任何一维不可行就标注并说明原因"
            })

    # FM-04: 混淆应然与偏好
    meta = analysis_result.get("meta_reflection", {})
    if not meta.get("alternative_normative_frameworks"):
        minority_stds = [s for s in standards if s["acceptance"] == "minority"]
        if minority_stds:
            failures.append({
                "mode": "preference_disguised_as_norm",
                "signal": "alternative_normative_frameworks 为空但存在 minority 标准",
                "recovery": "将分析者个人标准移入 alternative_normative_frameworks 并显性标注"
            })

    # FM-05: 差距度量不可量化
    for gap in analysis_result["descriptive_gap"]["gaps"]:
        if not gap.get("measurement") or not gap.get("data_source"):
            failures.append({
                "mode": "unquantifiable_gap",
                "signal": f"差距 {gap['against_standard']} 缺少量化度量或数据来源",
                "recovery": "优先寻找定量度量，无数据时标注 measurement=qualitative 并声明数据缺口"
            })

    # FM-06: 趋势判断无数据
    for gap in analysis_result["descriptive_gap"]["gaps"]:
        if gap.get("trend") and gap["trend"] != "unknown" and not gap.get("data_source"):
            failures.append({
                "mode": "trend_without_data",
                "signal": f"差距 {gap['against_standard']} 趋势判断无数据支持",
                "recovery": "强制要求时间序列数据点，无数据时标注 trend=unknown"
            })

    # FM-07: 合法性来源误判
    legitimacy_map = {
        "government": "legal_authority",
        "regulator": "legal_authority",
        "professional_body": "professional_consensus",
        "academic_institution": "professional_consensus",
        "elected_body": "democratic_process",
        "ethics_committee": "ethical_principle",
        "civil_society": "ethical_principle",
        "enterprise": "market_efficiency"
    }
    for std in standards:
        expected = legitimacy_map.get(std["defined_by"].lower())
        if expected and std["source_of_legitimacy"] != expected:
            failures.append({
                "mode": "legitimacy_misattribution",
                "signal": f"标准 {std['id']} 定义者={std['defined_by']} 但合法性来源={std['source_of_legitimacy']}",
                "recovery": f"应改为 {expected}"
            })

    # FM-08: 可行性评估缺失
    for pathway in analysis_result["feasible_pathways"]:
        feas = pathway.get("feasibility", {})
        for dim in ["political", "economic", "technical", "social"]:
            val = feas.get(dim, "")
            if not val or len(val) < 10:  # 仅写"可行/不可行"无理由
                failures.append({
                    "mode": "feasibility_missing",
                    "signal": f"路径 {pathway['id']} 的 {dim} 可行性评估缺失或无理由",
                    "recovery": f"强制为 {dim} 维度提供理由（推动力量/成本/成熟度/接受度）"
                })

    # FM-09: 价值冲突伪冲突
    for conflict in analysis_result["normative_landscape"]["conflicts"]:
        if conflict["nature"] == "zero_sum":
            if not conflict.get("pseudo_conflict_checked"):
                failures.append({
                    "mode": "pseudo_conflict_unchecked",
                    "signal": f"冲突 {conflict['standards']} 标注为 zero_sum 但未检验伪冲突",
                    "recovery": "追问'是否存在方案设计能同时满足两个标准？'若存在则改标为 pseudo_conflict"
                })

    # FM-10: 路径排序无理由
    pathways = analysis_result["feasible_pathways"]
    if len(pathways) > 1:
        ranks = [p.get("rank") for p in pathways]
        if not all(r is not None and r != 1 for r in ranks) or \
           not any(p.get("rank_rationale") for p in pathways):
            failures.append({
                "mode": "ranking_without_rationale",
                "signal": "路径排序无理由或所有路径 rank=1",
                "recovery": "强制按四维可行性综合评分排序，记录排序理由"
            })

    return {
        "failure_count": len(failures),
        "failures": failures,
        "recovery_actions": [f["recovery"] for f in failures]
    }
```

---

© 阿洋