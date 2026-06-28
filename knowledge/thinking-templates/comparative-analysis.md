# 对比分析 — 多对象多维度结构化比较与根因追溯

> **模块标识**: `knowledge/thinking-templates/comparative-analysis`
> **设计依据**: 基于全域深度认知框架三层推理架构设计——对比分析遵循"维度锚定→差异度量→归因分析→优劣判断"四步递进逻辑
> **依赖**: `knowledge/research-methods`、`knowledge/cognitive-framework`
> **骨架类型**: 对比分析 (Comparative Analysis)
>
> **版本治理元数据 (D12.4.2)**:
> - version: 1.1
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（对比分析四步递进）
>   - v1.1 补全版本治理元数据与交叉引用（D12.4.2-D12.4.3）

## 交叉引用

- **上游**: `knowledge/research-methods.md`（九层研究底座）、`knowledge/cognitive-framework.md`（认知流水线）
- **下游**: `tasks/T04_L4_L5_compare.md`（L4 比较参照层）、`tasks/T09_cog_reason.md`（认知推理，应用对比分析模板）
- **相关**: `knowledge/thinking-models/general/comparative-analysis.md`（对比分析模型）、`knowledge/thinking-models/general/cross-dimension-correlation.md`（跨维度关联）、`knowledge/thinking-models/routing-table.md`（思维模型路由表）

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
- `knowledge/thinking-models/general/comparative-analysis.md`（对比分析模型 — 比较方法论的类型学基础）
- `knowledge/thinking-models/general/cross-dimension-correlation.md`（跨维度关联 — 多维度交叉分析的理论框架）

**边界声明**：本模板提供五步对比分析的执行流程（步骤1-5的伪代码），不重复阐述比较方法论的类型学理论或跨维度关联的认识论基础。当需要理论依据时，调用上述模型文件。

---

## 1. 定义

对比分析是一种通过系统化比较两个或多个对象在多个维度上的异同，进而追溯差异根因的推理方法。它不仅是"列出不同点"，而是要求在每个维度上追问"为什么相同？""为什么不同？"，从而揭示被比较对象各自的本质特征、结构性约束和演化路径。对比分析的终点是形成对每个对象独立而深刻的认知，而非仅停留在差异描述层面。

**核心法则**: 对比的价值不在差异本身，而在差异背后指向的结构性原因。

---

## 2. 核心概念

| 概念 | 定义 | 执行标准 |
|------|------|----------|
| **比较维度** | 用于对比的抽象分析切面 | 每个维度必须可被独立定义和测量 |
| **可比性条件** | 两个对象在某一维度上具备有意义的可比性的前提 | 若条件不满足，标注为"不可比"而非强行比较 |
| **异同矩阵** | 以维度为行、对象为列的差异记录矩阵 | 每格必须包含"是什么"和"为什么" |
| **差异显著性** | 差异的大小和对结论的重要性 | 区分关键差异与边际差异 |
| **同构性** | 两个表面上不同的对象在深层结构上的一致性 | 揭示不同表象下的共同机制 |
| **异质性** | 两个表面上相似的对象在深层结构上的分歧 | 揭示相似表象下的不同本质 |
| **根因追溯** | 从差异描述到差异成因的因果推断 | 每项差异归因必须锚定于至少一个因果链 |

---

## 3. 五步对比分析流程

```
步骤1: 对比维度定义
  ├─ 核心维度: 直接关联分析目标的维度（3-5个）
  ├─ 结构维度: 反映对象本质结构的维度（2-3个）
  ├─ 时间维度: 反映对象演化路径的维度（1-2个）
  ├─ 维度独立性检验: 维度之间是否互斥？是否有隐含的层级关系？
  └─ 维度完备性检验: 是否存在遗漏的关键分析切面？
        │
步骤2: 各维度数据收集
  ├─ 对每个对象 × 每个维度，收集可比的数据
  ├─ 标准化数据口径: 确保不同对象的数据具有可比性
  ├─ 标注数据等级: L0（一手数据）到 L3（结构分析）
  └─ 识别数据缺口: 标注无法获取数据的维度
        │
步骤3: 异同点矩阵
  ├─ 构建 n×m 矩阵（n=维度数，m=对象数）
  ├─ 每格填充: 该对象在该维度的状态 + 数据来源
  ├─ 横向比较（同行）: 不同对象在同一维度上的异同
  ├─ 纵向比较（同列）: 同一对象在不同维度上的表现模式
  └─ 标注: 相同点（=）、显著差异（≠）、不可比（∅）
        │
步骤4: 根因分析
  ├─ 对每项显著差异追问"为什么不同？"
  ├─ 差异归因分层:
  │    L1 直接原因: 什么直接导致了该差异？
  │    L2 结构原因: 什么制度/结构约束导致了该差异？
  │    L3 机制原因: 什么深层机制维持了该差异？
  │    L4 范式原因: 什么信念/价值观/世界观导致了该差异？
  ├─ 对每项相同点追问"为什么相同？"——揭示共性背后的同构压力
  └─ 交叉验证: 不同维度的归因是否一致？是否存在矛盾？
        │
步骤5: 综合判断
  ├─ 提炼核心洞见: 通过对比获得的对每个对象的本质认知
  ├─ 共性总结: 跨对象的共同规律或约束
  ├─ 差异性结论: 差异产生的根本原因和可改变性评估
  └─ 不可比项声明: 标注无法有效比较的维度及原因
```

### 3.1 可执行伪代码（D6.4.3）

```python
def comparative_analysis(objects, analysis_goal):
    """
    对比分析模板 - 可执行伪代码（D6.4.3）
    输入: objects(待比较对象列表), analysis_goal(分析目标)
    输出: comparative_analysis YAML（见 §6 输出模板）
    """
    # ===== 步骤1: 对比维度定义 =====
    core_dimensions = select_core_dimensions(analysis_goal)  # 3-5个核心维度
    structural_dimensions = select_structural_dimensions(objects)  # 2-3个结构维度
    temporal_dimensions = select_temporal_dimensions(objects)  # 1-2个时间维度
    dimensions = core_dimensions + structural_dimensions + temporal_dimensions

    # 维度独立性检验
    for d1, d2 in combinations(dimensions, 2):
        assert is_independent(d1, d2), f"维度 {d1} 与 {d2} 不互斥"
    # 维度完备性检验
    assert check_completeness(dimensions, analysis_goal), "存在遗漏的关键分析切面"

    # ===== 步骤2: 各维度数据收集 =====
    data_matrix = {}
    for obj in objects:
        for dim in dimensions:
            data = collect_data(obj, dim)
            data = standardize_data(data)  # 标准化数据口径
            data_matrix[(obj, dim)] = {
                "value": data,
                "evidence_level": classify_evidence_level(data),  # L0-L3
                "source": data.source
            }
    data_gaps = identify_data_gaps(data_matrix)  # 标注无法获取数据的维度

    # ===== 步骤3: 异同点矩阵 =====
    comparison_matrix = build_matrix(dimensions, objects)  # n×m 矩阵
    for dim in dimensions:
        values = {obj: data_matrix[(obj, dim)]["value"] for obj in objects}
        for obj_pair in combinations(objects, 2):
            verdict = compare_values(values[obj_pair[0]], values[obj_pair[1]])
            # verdict: "=" 相同 | "≠" 显著差异 | "∅" 不可比
            comparison_matrix.set(dim, obj_pair, verdict)

    # ===== 步骤4: 根因分析 =====
    difference_analysis = []
    for dim in dimensions:
        for obj_pair in combinations(objects, 2):
            if comparison_matrix.get(dim, obj_pair) == "≠":
                root_causes = trace_root_causes(dim, obj_pair, data_matrix)
                # 差异归因分层: L1直接/L2结构/L3机制/L4范式
                difference_analysis.append({
                    "dimension": dim,
                    "objects": obj_pair,
                    "root_cause_chain": root_causes,
                    "changeability": assess_changeability(root_causes)
                })
            elif comparison_matrix.get(dim, obj_pair) == "=":
                # 对相同点追问"为什么相同？"——揭示共性背后的同构压力
                common_pattern = analyze_commonality(dim, obj_pair, data_matrix)
                difference_analysis.append({
                    "dimension": dim,
                    "objects": obj_pair,
                    "common_pattern": common_pattern
                })

    # 交叉验证: 不同维度的归因是否一致？
    cross_validate_attributions(difference_analysis)

    # ===== 步骤5: 综合判断 =====
    return {
        "core_insights": [  # 核心洞见
            {"for": obj, "insight": extract_insight(obj, difference_analysis)}
            for obj in objects
        ],
        "cross_cutting_themes": identify_cross_cutting_themes(difference_analysis),  # 共性总结
        "difference_conclusions": difference_analysis,  # 差异性结论
        "incommensurable_dimensions": [  # 不可比项声明
            {"dimension": dim, "reason": "数据口径不一致" or "维度对某些对象不适用"}
            for dim in dimensions if has_incommensurable(dim, objects)
        ],
        "generalizability": assess_generalizability(objects, difference_analysis)
    }
```

---

## 4. 对比维度的选择原则

### 4.1 维度分类体系

| 维度类别 | 说明 | 示例 |
|---------|------|------|
| 功能维度 | 对象"做什么" | 生产效率、服务范围、覆盖人群 |
| 结构维度 | 对象"是什么构成的" | 组织架构、资源构成、权力分布 |
| 过程维度 | 对象"如何运作" | 决策流程、反馈机制、学习曲线 |
| 环境维度 | 对象"在什么条件下" | 外部约束、资源可得性、竞争格局 |
| 输出维度 | 对象"产出什么" | 产品质量、社会影响、外部性 |
| 时间维度 | 对象"如何演化" | 生命周期阶段、增长速率、拐点 |

### 4.2 维度筛选标准

每条选定的维度必须满足：
- **可操作性**: 该维度能否被明确定义和测量？
- **区分度**: 该维度上对象之间是否存在有意义的差异？
- **解释力**: 该维度的差异是否有助于理解对象的核心特征？
- **非冗余**: 该维度是否与其他维度重叠（相关性 > 0.7 时合并或删除）？

---

## 5. 常见陷阱

1. **苹果与橙子**: 比较了本质上不可比的对象。**纠正**: 先定义可比性条件，不满足时标注为"不可比"并说明原因。
2. **维度不对称**: 选择的维度对某些对象有意义但对其他对象不适用。**纠正**: 对每个维度检验"对所有对象的适用性"，不适用时标注 ∅。
3. **差异归因跳跃**: 将差异归因于"文化差异"或"国情不同"等笼统解释。**纠正**: 每个归因必须满足因果链的可追溯性，追溯至至少一个具体的结构因素。
4. **共性过度推广**: 从有限对象的共性中得出过泛的规律。**纠正**: 共性结论必须标注"基于 N 个对象的观察，推广性受限于..."
5. **选择性比较**: 只列出支持预设结论的差异，忽略同等重要的相同点。**纠正**: 异同矩阵必须对称——对相同点和不同点给予同等的记录和分析深度。
6. **静态比较**: 只比较当前状态，忽略演化趋势的差异。**纠正**: 必须包含至少一个时间维度的比较。

---

## 6. 输出模板

```yaml
comparative_analysis:
  objects:
    - id: "OBJ-A"
      name: "对象A名称"
      scope: "分析范围界定"
    - id: "OBJ-B"
      name: "对象B名称"
      scope: "分析范围界定"

  dimensions:
    - id: "DIM-01"
      name: "维度名称"
      category: "functional|structural|process|environmental|output|temporal"
      definition: "维度的可操作化定义"
      comparability_check: "所有对象在此维度上的可比性确认"

  comparison_matrix:
    rows:
      - dimension: "DIM-01"
        values:
          OBJ-A: "对象A在该维度的状态"
          OBJ-B: "对象B在该维度的状态"
        verdict: "= | ≠ | ∅"
        evidence_level: "L0|L1|L2|L3"
        evidence_source: "数据来源"

  similarity_analysis:
    - dimensions: ["相同的维度"]
      common_pattern: "共性模式描述"
      root_cause_of_similarity: "共性的结构性原因"
      significance: "该共性对分析的意义"

  difference_analysis:
    - dimensions: ["差异的维度"]
      difference_description: "差异的具体描述"
      root_cause_chain:
        - level: "L1_direct|L2_structural|L3_mechanism|L4_paradigm"
          cause: "该层原因"
          evidence: "支撑证据"
      changeability: "high|medium|low（该差异的可改变程度）"

  synthesis:
    core_insights:
      - for: "OBJ-A"
        insight: "通过对比揭示的关于对象A的本质认知"
      - for: "OBJ-B"
        insight: "通过对比揭示的关于对象B的本质认知"
    cross_cutting_themes: ["跨对象的共同主题"]
    incommensurable_dimensions: ["不可比维度及原因"]
    generalizability: "结论的可推广性评估"
```

---

## 7. 快速调用指南

当问题包含以下特征时，优先使用本骨架：
- 问题形式为"A 和 B 有何异同？为什么？"
- 涉及多方案/多对象/多路径的选择和评估
- 需要从差异中提取本质规律
- 问题涉及"最佳实践"的适用性评估（需要对比情境差异）
- 需要揭示表面上不同对象的深层同构性或表面上相似的深层异质性

---

## 8. 失败模式闭环清单（D6.4.4）

> 本节为对比分析模板的「失败模式 → 检测信号 → 恢复策略」闭环清单。当检测到失败模式时，必须执行对应的恢复策略。

| 失败模式 | 检测信号 | 恢复策略 |
|---------|---------|---------|
| **苹果与橙子** | 比较了本质上不可比的对象（如不同量级、不同范畴） | 先定义可比性条件：对象在核心维度上必须有共同的分析锚点；不满足时标注为"不可比"并说明原因 |
| **维度不对称** | 选择的维度对某些对象有意义但对其他对象不适用 | 对每个维度检验"对所有对象的适用性"，不适用时标注 ∅（不可比）而非强行比较 |
| **差异归因跳跃** | 将差异归因于"文化差异"或"国情不同"等笼统解释 | 每个归因必须满足因果链的可追溯性，追溯至至少一个具体的结构因素（L1-L4分层） |
| **共性过度推广** | 从有限对象的共性中得出过泛的规律 | 共性结论必须标注"基于 N 个对象的观察，推广性受限于..."，声明样本量和边界条件 |
| **选择性比较** | 只列出支持预设结论的差异，忽略同等重要的相同点 | 异同矩阵必须对称——对相同点和不同点给予同等的记录和分析深度 |
| **静态比较** | 只比较当前状态，忽略演化趋势的差异 | 强制包含至少一个时间维度的比较，标注各对象的历史轨迹差异 |
| **维度冗余** | 两个或多个维度高度相关（相关性>0.7），导致重复计算 | 合并或删除冗余维度，保留解释力最强的维度；在维度独立性检验阶段拦截 |
| **数据口径不一致** | 不同对象的同一维度数据来自不同口径，导致虚假差异 | 标准化数据口径：确保不同对象的数据具有可比性；无法标准化时标注 ∅ |
| **根因层次混淆** | 将L1直接原因与L4范式原因混为一谈，导致归因层次不清 | 强制分层归因：对每项差异执行 L1→L2→L3→L4 四层追溯，标注每层原因 |
| **交叉验证失败** | 不同维度的归因相互矛盾，无法形成一致的解释 | 重新审视矛盾维度的归因，寻找更深层的统一解释；若无法统一，标注为"多维张力" |

### 8.1 失败模式检测与恢复的执行伪代码

```python
def detect_and_recover_comparative_failures(dimensions, objects, comparison_matrix, difference_analysis):
    """
    对比分析失败模式检测与恢复（D6.4.4）
    """
    failures = []

    # 检测1: 苹果与橙子（不可比对象）
    for obj_pair in combinations(objects, 2):
        if not check_comparability(obj_pair[0], obj_pair[1]):
            failures.append({
                "failure_mode": "apples_and_oranges",
                "objects": obj_pair,
                "recovery": mark_incomparable(obj_pair, reason="核心维度无共同分析锚点")
            })

    # 检测2: 维度不对称
    for dim in dimensions:
        for obj in objects:
            if not dim.applicable_to(obj):
                failures.append({
                    "failure_mode": "dimension_asymmetry",
                    "dimension": dim,
                    "object": obj,
                    "recovery": mark_incomparable(dim, obj, reason="维度对该对象不适用")
                })

    # 检测3: 差异归因跳跃
    for diff in difference_analysis:
        if diff.root_cause_chain and diff.root_cause_chain[-1]["level"] < "L2":
            failures.append({
                "failure_mode": "attribution_jump",
                "dimension": diff.dimension,
                "recovery": deepen_attribution(diff, target_level="L4")
            })

    # 检测4: 共性过度推广
    if len(objects) < 3:
        for common in difference_analysis:
            if common.get("common_pattern") and common.get("generalized", False):
                failures.append({
                    "failure_mode": "over_generalization",
                    "recovery": add_sample_size_caveat(common, sample_size=len(objects))
                })

    # 检测5: 选择性比较
    similarity_count = sum(1 for d in difference_analysis if d.get("common_pattern"))
    difference_count = sum(1 for d in difference_analysis if d.get("root_cause_chain"))
    if similarity_count == 0 or difference_count == 0:
        failures.append({
            "failure_mode": "selective_comparison",
            "recovery": force_symmetric_analysis(difference_analysis)
        })

    # 检测6: 静态比较
    if not any(d.category == "temporal" for d in dimensions):
        failures.append({
            "failure_mode": "static_comparison",
            "recovery": add_temporal_dimension(dimensions, objects)
        })

    # 检测7: 维度冗余
    for d1, d2 in combinations(dimensions, 2):
        if correlation(d1, d2) > 0.7:
            failures.append({
                "failure_mode": "dimension_redundancy",
                "dimensions": (d1, d2),
                "recovery": merge_or_delete_dimension(d1, d2)
            })

    # 检测8: 交叉验证失败
    if not cross_validate_attributions(difference_analysis):
        failures.append({
            "failure_mode": "cross_validation_failure",
            "recovery": find_unified_explanation(difference_analysis) or
                       mark_multidimensional_tension(difference_analysis)
        })

    return failures
```

---

© 阿洋