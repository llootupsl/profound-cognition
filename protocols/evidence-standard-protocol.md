<!-- 作者：阿洋 -->

# 证据标准协议 (Evidence Standard Protocol) v3.0

> **状态**: 正式发布 (v3.0)
> **适用范围**: Profound Cognition — 全部需要证据等级判定的任务节点
> **最后更新**: 2026-06-25
> **依赖**: `knowledge/evidence-standards.md`（L0-L3 基础分级标准）
> **职责边界**: 本协议定义证据等级的**升级/降级规则、动态调整机制与验证流程闭环**。基础分级标准（L0-L3 定义、判定标准、示例）仍由 `knowledge/evidence-standards.md` 定义，本协议在其之上增加动态治理层。

---

## 1. 协议概述

### 1.1 目的

EvidenceStandardProtocol 定义 Profound Cognition 中证据等级的动态治理机制。基础分级标准（`knowledge/evidence-standards.md`）定义了 L0-L3 四级证据的静态判定规则；本协议在此基础上增加五个动态维度：

1. **证据等级与验证流程闭环**（D13.4.1）—— 从证据等级判定到验证执行的完整闭环
2. **升级/降级规则**（D13.4.2）—— 3 个独立 L1 可升级为 L0
3. **时效性维度**（D13.4.3）—— L0 超 5 年降为 L1
4. **地域性维度**（D13.4.4）—— 跨地域证据降级
5. **利益相关方维度**（D13.4.5）—— 企业赞助研究降一级

### 1.2 核心设计原则

- **静态分级 + 动态调整**：基础等级由 `evidence-standards.md` 静态判定，本协议根据上下文动态调整
- **可追溯**：每次升级/降级必须记录原因、触发条件、调整前后等级
- **保守降级**：当不确定是否升级时，保持原等级；当不确定是否降级时，执行降级
- **多维度叠加**：多个降级因素叠加时，取最低等级；多个升级因素叠加时，最多升一级

### 1.3 与基础标准的关系

| 文档 | 职责 | 适用场景 |
|------|------|---------|
| `knowledge/evidence-standards.md` | L0-L3 静态分级标准、判定规则、示例 | 初始证据等级判定 |
| `protocols/evidence-standard-protocol.md`（本协议） | 升级/降级规则、动态调整、验证闭环 | 证据等级动态治理 |

---

## 2. 证据等级与验证流程闭环（D13.4.1）

### 2.1 闭环流程

```
┌──────────────────────────────────────────────────────────┐
│  证据等级与验证流程闭环                                    │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  1. 初始分级                                              │
│     └─ 基于 evidence-standards.md 静态判定 → L0/L1/L2/L3 │
│                                                          │
│  2. 动态调整                                              │
│     ├─ 升级检查（§3）                                     │
│     ├─ 时效性降级（§4）                                   │
│     ├─ 地域性降级（§5）                                   │
│     └─ 利益相关方降级（§6）                               │
│                                                          │
│  3. 验证执行                                              │
│     ├─ L0/L1: 强制三角验证（≥2 个独立来源）              │
│     ├─ L2: 建议三角验证                                  │
│     └─ L3: 标注"可靠性需进一步验证"                      │
│                                                          │
│  4. 验证结果反馈                                          │
│     ├─ 验证通过 → 确认最终等级                            │
│     ├─ 验证部分通过 → 降一级                              │
│     └─ 验证失败 → 降两级或标记为不可用                    │
│                                                          │
│  5. 最终等级写入 NRSF                                     │
│     └─ evidence_level: L0|L1|L2|L3 + adjustment_history  │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### 2.2 验证流程规范

```yaml
evidence_verification:
  initial_level: "L0|L1|L2|L3"           # 基于 evidence-standards.md 的初始分级
  adjustment_history:
    - dimension: "upgrade|time|region|stakeholder|verification"
      trigger: "触发条件描述"
      before: "L0|L1|L2|L3"
      after: "L0|L1|L2|L3"
      reason: "调整原因"
  verification_status: "passed|partial|failed|skipped"
  final_level: "L0|L1|L2|L3"             # 最终确认等级
  verification_evidence:
    - source_ref: "§ref:T02:source_001"
      independent: bool                   # 是否独立来源
      corroborates: bool                  # 是否佐证原结论
```

### 2.3 闭环触发条件

| 触发点 | 执行动作 |
|--------|---------|
| T02 研究底座完成 | 对所有收集的来源执行初始分级 + 动态调整 |
| T05 证据层完成 | 对核心论据执行三角验证 |
| T17 事实核查 | 验证证据等级与实际可靠性是否一致 |
| Gate-α/β/γ | 抽样检查证据等级调整记录的完整性 |

---

## 3. 证据等级升级/降级规则（D13.4.2）

### 3.1 升级规则

#### 3.1.1 L1 → L0 升级规则

**核心规则**：3 个独立 L1 来源交叉验证同一事实时，可将该事实的证据等级升级为 L0。

**判定条件**（全部满足方可升级）：
1. **数量条件**：≥3 个 L1 级别来源报道同一事实
2. **独立性条件**：3 个来源必须满足以下独立性要求
   - 不同作者（无共同作者）
   - 不同机构（无母子公司关系）
   - 不同方法论（如不同数据源、不同分析框架）
3. **一致性条件**：3 个来源对核心事实的描述一致（允许细节差异）
4. **时效条件**：3 个来源中最旧的来源发布时间 ≤ 2 年
5. **无利益冲突**：3 个来源均无企业赞助或利益相关方嫌疑（见 §6）

**升级记录格式**：
```yaml
upgrade_record:
  original_level: L1
  upgraded_level: L0
  rule: "3-independent-L1-upgrade"
  sources:
    - {ref: "§ref:T02:src_001", author: "...", institution: "...", method: "..."}
    - {ref: "§ref:T02:src_002", author: "...", institution: "...", method: "..."}
    - {ref: "§ref:T02:src_003", author: "...", institution: "...", method: "..."}
  independence_verified: true
  consistency_check: "核心事实一致，细节差异：..."
  oldest_source_date: "2024-06-15"
```

#### 3.1.2 L2 → L1 升级规则

**核心规则**：2 个独立 L2 来源（同行评审论文）交叉验证同一结论，且被 ≥1 个 L1 权威报道引用时，可升级为 L1。

**判定条件**：
1. ≥2 个 L2 来源（不同期刊、不同作者团队）
2. ≥1 个 L1 权威报道引用该结论
3. 结论一致性 ≥ 0.85（语义相似度）

#### 3.1.3 L3 → L2 升级规则

**核心规则**：L3 来源（博客/论坛）引用了 L0/L1/L2 原始来源时，应追溯至原始来源并标注原始等级（此规则已在 `evidence-standards.md` 跨级判定规则 §2 定义）。本协议补充：若无法追溯原始来源，但 ≥3 个独立 L3 来源一致且被 ≥1 个 L2 来源佐证，可升级为 L2。

### 3.2 降级规则

#### 3.2.1 验证失败降级

| 验证状态 | 降级幅度 |
|---------|---------|
| 验证通过（≥2 个独立来源佐证） | 不降级 |
| 验证部分通过（1 个独立来源佐证） | 降一级（L0→L1, L1→L2, L2→L3） |
| 验证失败（无独立来源佐证） | 降两级或标记为不可用 |
| 验证矛盾（独立来源给出相反结论） | 标记为 CONTROVERSIAL，降一级 |

#### 3.2.2 冲突降级

当不同级别来源对同一事实存在矛盾时：
1. 优先采信更高级别来源（依据 `evidence-standards.md` 跨级判定规则 §3）
2. 在输出中注明争议
3. 较低级别来源标记为 `disputed`
4. 若高级别来源无法解决争议，整体降一级

### 3.3 升级/降级决策树

```yaml
evidence_level_adjustment:
  step_1_initial: "基于 evidence-standards.md 判定初始等级"
  step_2_upgrade_check:
    - if L1 and count(independent_L1_sources) >= 3:
        if all_conditions_met:
          upgrade_to: L0
    - if L2 and count(independent_L2_sources) >= 2 and has_L1_corroboration:
        if consistency >= 0.85:
          upgrade_to: L1
  step_3_time_decay: "见 §4"
  step_4_region_check: "见 §5"
  step_5_stakeholder_check: "见 §6"
  step_6_verification: "执行三角验证，依据 §3.2.1 调整"
  step_7_final: "写入 NRSF"
```

---

## 4. 时效性维度（D13.4.3）

### 4.1 时效性降级规则

**核心规则**：证据等级随时间衰减。L0 级别来源超过 5 年未更新，降为 L1。

| 原始等级 | 时效阈值 | 降级后等级 | 说明 |
|---------|---------|-----------|------|
| L0 | > 5 年 | L1 | 政府/国际组织数据超 5 年可能已被修订 |
| L0 | > 10 年 | L2 | 超 10 年的原始数据可能已严重过时 |
| L1 | > 3 年 | L2 | 主流媒体报道超 3 年可能已被后续报道修正 |
| L1 | > 7 年 | L3 | 超 7 年的媒体报道参考价值显著降低 |
| L2 | > 5 年 | L3 | 学术论文超 5 年可能已被后续研究修正（与 `evidence-standards.md` L2 使用原则一致） |
| L3 | 不降级 | L3 | L3 已是最低等级 |

### 4.2 时效性计算

```python
# 时效性降级计算伪代码
def time_decay_evidence_level(original_level, publication_date, reference_date):
    age_years = (reference_date - publication_date).days / 365.25

    decay_rules = {
        "L0": [(5, "L1"), (10, "L2")],
        "L1": [(3, "L2"), (7, "L3")],
        "L2": [(5, "L3")],
        "L3": [],  # 不降级
    }

    rules = decay_rules.get(original_level, [])
    for threshold, new_level in rules:
        if age_years > threshold:
            return new_level, f"时效降级：{original_level} → {new_level}（{age_years:.1f} 年 > {threshold} 年阈值）"

    return original_level, None
```

### 4.3 时效性例外

以下类型的来源不受时效性降级约束：
1. **历史档案**：如历史事件的一手档案（年代久远是固有属性）
2. **法律条文**：现行有效的法律条文（只要未被废止）
3. **基础科学原理**：如牛顿运动定律等基础科学原理
4. **经典著作**：学术领域的奠基性著作（标注为 `classic`）

例外标注格式：
```yaml
time_decay_exception:
  reason: "historical_archive|legal_statute|scientific_principle|classic_work"
  note: "该来源为历史档案，时效性降级不适用"
```

### 4.4 时效性记录

```yaml
time_decay_record:
  original_level: "L0"
  publication_date: "2018-06-15"
  reference_date: "2026-06-25"
  age_years: 8.03
  decayed_level: "L1"
  decay_rule: "L0 > 5 years → L1"
  exception_applied: false
```

---

## 5. 地域性维度（D13.4.4）

### 5.1 地域性降级规则

**核心规则**：证据的地域适用性影响其等级。跨地域使用证据时，需评估地域适配性，必要时降级。

### 5.2 地域适配性矩阵

| 证据来源地域 | 适用地域 | 适配等级 | 调整建议 |
|-------------|---------|---------|---------|
| 中国大陆 | 中国大陆 | FULL | 不调整 |
| 中国大陆 | 港澳台 | PARTIAL | 降一级（制度差异） |
| 中国大陆 | 海外 | LIMITED | 降一级（文化/制度差异） |
| 美国/欧洲 | 美国/欧洲 | FULL | 不调整 |
| 美国/欧洲 | 中国 | PARTIAL | 降一级（制度/文化差异） |
| 任何地域 | 全球通用 | FULL | 不调整（如基础科学） |

### 5.3 地域性降级条件

**降级触发条件**（满足任一即降级）：
1. **制度差异**：证据来源地的政治/法律/经济制度与研究目标地显著不同
2. **文化差异**：证据涉及文化敏感领域（如社会行为、消费习惯、价值观），且来源地与目标地文化差异显著
3. **经济差异**：证据涉及经济指标（如收入水平、消费能力），且来源地与目标地经济发展水平差异 > 2 倍
4. **数据覆盖缺失**：证据来源地不包含研究目标地的数据

### 5.4 地域性记录

```yaml
region_adjustment_record:
  source_region: "USA"
  target_region: "China"
  compatibility: "PARTIAL"
  adjustment: "L1 → L2"
  reasons:
    - "制度差异：美国市场经济 vs 中国社会主义市场经济"
    - "数据覆盖缺失：来源仅含美国数据，未覆盖中国"
  exception_applied: false
```

### 5.5 地域性例外

以下情况不受地域性降级约束：
1. **基础科学研究**：如物理、化学、生物等基础科学实验结果（地域无关）
2. **全球性统计**：如 WHO 全球疾病负担数据、World Bank 全球经济指标
3. **跨国比较研究**：研究本身覆盖多个地域
4. **技术标准**：如 ISO/IEEE 等国际技术标准

---

## 6. 利益相关方维度（D13.4.5）

### 6.1 利益相关方降级规则

**核心规则**：企业赞助研究的证据等级降一级。利益相关方可能影响研究的客观性。

### 6.2 利益相关方识别

**利益相关方类型**：

| 类型 | 识别信号 | 降级幅度 |
|------|---------|---------|
| 企业赞助研究 | 研究经费来自相关企业、企业员工参与作者团队 | 降一级 |
| 行业协会赞助 | 研究经费来自相关行业协会 | 降一级 |
| 政府赞助（争议领域） | 政府赞助且研究主题涉及该政府利益 | 降一级（仅争议领域） |
| 利益相关方引用 | 研究被利益相关方选择性引用且未标注 | 降一级 |
| 作者利益冲突 | 作者持有相关企业股权/专利/顾问关系 | 降一级 |

### 6.3 利益相关方降级规则

```yaml
stakeholder_adjustment:
  original_level: "L2"
  adjusted_level: "L3"
  stakeholder_type: "corporate_sponsored"
  evidence:
    - "研究经费来自 XYZ 公司（见致谢部分）"
    - "通讯作者为 XYZ 公司员工"
    - "研究结论有利于 XYZ 公司产品"
  conflict_of_interest_declared: false  # 是否声明利益冲突
  adjustment_reason: "企业赞助研究且未声明利益冲突，降一级"
```

### 6.4 利益相关方例外

以下情况不执行利益相关方降级：
1. **已声明且无冲突**：作者明确声明无利益冲突，且研究主题与赞助方无直接利益关系
2. **独立第三方验证**：研究结论已被独立第三方（无利益相关）验证
3. **政府基础统计**：政府统计部门发布的常规统计数据（非争议领域）
4. **同行评审通过**：经过严格同行评审且评审专家无利益冲突

### 6.5 利益相关方检测清单

对每条 L0/L1/L2 证据执行以下检测：

- [ ] 研究经费来源是否公开？
- [ ] 作者是否声明利益冲突？
- [ ] 研究结论是否有利于赞助方？
- [ ] 研究是否被利益相关方选择性引用？
- [ ] 是否存在独立第三方验证？

任一检测项异常 → 执行降级。

---

## 7. 多维度叠加规则

### 7.1 叠加原则

当多个维度同时触发调整时：
1. **升级与降级叠加**：先执行升级，再执行降级。若升级后立即被降级，则保持原等级。
2. **多个降级叠加**：取最低等级（而非逐级降级）。例如 L0 同时触发时效降级（→L1）和利益相关方降级（→L1），最终为 L1 而非 L2。
3. **多个升级叠加**：最多升一级。例如 L2 同时满足"3 个独立 L1 升级"和"L2→L1 升级"条件，最终为 L1 而非 L0。

### 7.2 叠加决策树

```yaml
multi_dimension_adjustment:
  step_1_upgrade: "执行升级检查（§3.1）"
  step_2_time_decay: "执行时效性降级（§4）"
  step_3_region: "执行地域性降级（§5）"
  step_4_stakeholder: "执行利益相关方降级（§6）"
  step_5_aggregate:
    if upgrade_triggered and downgrade_triggered:
      final = original  # 升级与降级抵消
    elif multiple_downgrades:
      final = min(all_downgraded_levels)  # 取最低
    elif multiple_upgrades:
      final = original + 1  # 最多升一级
    else:
      final = last_adjusted_level
  step_6_verification: "执行验证（§2.2）"
  step_7_final: "写入 NRSF"
```

### 7.3 叠加示例

**示例 1**：L0 来源，发布于 6 年前（时效降级 → L1），由企业赞助（利益相关方降级 → L1）
- 叠加结果：L1（取最低，非 L2）

**示例 2**：L1 来源，3 个独立 L1 交叉验证（升级 → L0），但发布于 4 年前（时效不降级，L0 阈值是 5 年）
- 叠加结果：L0

**示例 3**：L2 论文，2 个独立 L2 + 1 个 L1 引用（升级 → L1），但作者持有专利（利益相关方降级 → L2）
- 叠加结果：L2（升级与降级抵消）

---

## 8. 输出规范

### 8.1 证据等级调整报告

```yaml
evidence_level_report:
  source_ref: "§ref:T02:source_001"
  source_url: "https://..."
  source_title: "..."
  initial_level: "L0"
  adjustments:
    - dimension: "upgrade"
      triggered: false
      details: null
    - dimension: "time"
      triggered: true
      before: "L0"
      after: "L1"
      reason: "发布于 2018-06-15，距今 8.03 年，超过 5 年阈值"
    - dimension: "region"
      triggered: false
      details: "来源地域与目标地域一致"
    - dimension: "stakeholder"
      triggered: true
      before: "L1"
      after: "L2"
      reason: "研究经费来自 XYZ 公司，未声明利益冲突"
    - dimension: "verification"
      triggered: true
      before: "L2"
      after: "L2"
      reason: "三角验证通过（2 个独立来源佐证）"
  final_level: "L2"
  adjustment_summary: "L0 → L1（时效）→ L2（利益相关方）→ L2（验证通过）"
```

### 8.2 NRSF 写入格式

```yaml
nrsf_evidence_entry:
  - source_ref: "§ref:T02:source_001"
    evidence_level: "L2"
    initial_level: "L0"
    adjustment_history:
      - {dimension: "time", from: "L0", to: "L1", reason: "..."}
      - {dimension: "stakeholder", from: "L1", to: "L2", reason: "..."}
    verification_status: "passed"
    last_verified: "2026-06-25"
```

---

## 9. 与其他协议的关系

| 协议 | 关系 |
|------|------|
| `knowledge/evidence-standards.md` | 上游：提供 L0-L3 静态分级标准 |
| `protocols/nrsf-protocol.md` | 下游：证据等级调整结果写入 NRSF |
| `protocols/self-evaluation-protocol.md` | 协同：自评时检查证据等级调整记录 |
| `protocols/exhaust-retry-protocol.md` | 协同：证据等级验证失败时触发穷尽重试 |
| `tasks/T02_L1_L2_research.md` | 消费：研究底座执行初始分级 |
| `tasks/T05_L6_L7_evidence.md` | 消费：证据层执行三角验证 |
| `tasks/T17_quality_factcheck.md` | 消费：事实核查验证证据等级 |
| `tasks/T19b_prescription_gate.md` | 消费：处方门控追溯证据链 |

---

## 10. 测试用例

### 测试用例 1：L1 → L0 升级

**给定输入**：3 个独立 L1 来源（Reuters、AP、新华社）报道同一事实，作者不同、机构不同、方法论不同，最旧来源发布于 2024-06-15（< 2 年），无利益冲突。

**应产出**：证据等级升级为 L0，`upgrade_record.rule = "3-independent-L1-upgrade"`，`independence_verified = true`。

### 测试用例 2：L0 时效降级

**给定输入**：L0 来源（国家统计局 2018 年数据），当前日期 2026-06-25，距今 8.03 年。

**应产出**：证据等级降为 L1，`time_decay_record.decay_rule = "L0 > 5 years → L1"`，`age_years = 8.03`。

### 测试用例 3：利益相关方降级

**给定输入**：L2 学术论文，研究经费来自 XYZ 公司，通讯作者为 XYZ 公司员工，研究结论有利于 XYZ 公司产品，未声明利益冲突。

**应产出**：证据等级降为 L3，`stakeholder_adjustment.stakeholder_type = "corporate_sponsored"`，`conflict_of_interest_declared = false`。

### 测试用例 4：多维度叠加

**给定输入**：L0 来源，发布于 6 年前（时效降级），由企业赞助（利益相关方降级），3 个独立 L1 交叉验证（升级）。

**应产出**：最终等级为 L1。升级（L0→L0，已是最高的 L0 来源不需要升级）+ 时效降级（L0→L1）+ 利益相关方降级（L1→L1，取最低），最终 L1。

### 测试用例 5：地域性降级

**给定输入**：L1 来源（美国主流媒体 Reuters 报道美国消费者行为数据），研究目标为中国消费者行为，制度差异显著且数据覆盖缺失。

**应产出**：证据等级降为 L2，`region_adjustment_record.compatibility = "PARTIAL"`，`reasons` 包含制度差异和数据覆盖缺失。
