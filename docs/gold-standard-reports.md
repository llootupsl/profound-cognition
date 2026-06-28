<!-- 作者：阿洋 -->

# 金标准报告集（Gold Standard Reports）

> **用途**：为 Orchestrator 评分外部验证（R7-04）提供基准对照集。每个金标准报告由人工专家标注质量等级（HIGH/LOW），作为校准 Orchestrator 自动评分的参照系。
>
> **内容定位澄清（H7 审计核验）**：本文件存储的是 20 个金标准报告的**结构化元数据描述**（report_id / topic / quality_level / word_count / coverage_dimensions 等 14 个特征字段 + 关键特征说明），**非完整报告全文**。这是设计上的有意取舍——金标准集作为机器可读的校准参照系，只需存特征向量供 Orchestrator 评分比对，无需存完整报告文本（完整报告文本体积过大且对校准无用）。校准时 Orchestrator 输出自动评分 S_orchestrator，与本集 S_gold（HIGH=5, LOW=1）比对计算 Pearson 相关系数 r ≥ 0.7 即通过。
>
> **维护规则**：金标准报告集每季度由人工复核一次，新增报告需经双标注员独立标注且一致后方可入库。报告描述遵循「可量化、可复现」原则，所有特征字段均为可机器读取的数值或枚举。

---

## 1. 概述

本文件定义 20 个金标准报告描述（10 HIGH + 10 LOW），用于：

1. **Orchestrator 评分一致性验证**：计算 Orchestrator 自动评分与金标准人工评分的相关系数，要求 ≥ 0.7
2. **评分校准触发判定**：当 Orchestrator 评分与金标准偏差 > 1 分时触发校准
3. **跨模型评分对照**：2 个模型独立评分取平均，与金标准对比

### 1.1 特征字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `report_id` | string | 报告唯一标识，格式 `GSR-{NN}` |
| `topic` | string | 报告话题 |
| `quality_level` | enum | `HIGH` \| `LOW` |
| `word_count` | integer | 正文字数（不含标点、空格、Markdown 标记） |
| `coverage_dimensions` | integer | 覆盖的元维度数（满分 14） |
| `evidence_count` | integer | 引用证据条目数（含 `[来源:...]` 标记） |
| `counter_evidence_count` | integer | 反证条目数 |
| `cross_dimension_links` | integer | 跨维度连接数 |
| `chapter_count` | integer | 完整章节数（§1-§8） |
| `gate_pass_status` | enum | `ALL_PASS` \| `PARTIAL` \| `FAIL` |
| `information_density` | float | 信息密度 ID 值 |
| `has_philosophical_core` | boolean | 是否包含哲学三元组审查 |
| `has_scientific_layer` | boolean | 是否包含科学层 TM01-TM07 |
| `persona_drift` | boolean | 是否存在人设漂移 |

### 1.2 质量等级判定阈值

| 维度 | HIGH 阈值 | LOW 阈值 |
|------|----------|----------|
| word_count | ≥ 100000 | < 50000 |
| coverage_dimensions | ≥ 12 | ≤ 6 |
| evidence_count | ≥ 50 | < 15 |
| counter_evidence_count | ≥ 8 | < 2 |
| cross_dimension_links | ≥ 15 | < 5 |
| chapter_count | = 8（完整） | ≤ 4 |
| gate_pass_status | ALL_PASS | PARTIAL 或 FAIL |
| information_density | ≥ 4.0 | < 3.0 |
| has_philosophical_core | true | false |
| has_scientific_layer | true | false |

---

## 2. HIGH 质量金标准报告（10 个）

### GSR-01

| 字段 | 值 |
|------|------|
| report_id | GSR-01 |
| topic | 全球半导体产业链地缘政治重构与中国自主化路径 |
| quality_level | HIGH |
| word_count | 128000 |
| coverage_dimensions | 14 |
| evidence_count | 87 |
| counter_evidence_count | 15 |
| cross_dimension_links | 23 |
| chapter_count | 8 |
| gate_pass_status | ALL_PASS |
| information_density | 6.8 |
| has_philosophical_core | true |
| has_scientific_layer | true |
| persona_drift | false |

**关键特征**：穷尽级交付，覆盖全部 14 元维度，含系统动力学仿真（TM01）与 Lean4 形式化验证（TM06b），三路对抗验证完整，反证充分。

---

### GSR-02

| 字段 | 值 |
|------|------|
| report_id | GSR-02 |
| topic | AI 大模型对就业市场的结构性冲击与再培训体系设计 |
| quality_level | HIGH |
| word_count | 115000 |
| coverage_dimensions | 13 |
| evidence_count | 72 |
| counter_evidence_count | 12 |
| cross_dimension_links | 19 |
| chapter_count | 8 |
| gate_pass_status | ALL_PASS |
| information_density | 6.2 |
| has_philosophical_core | true |
| has_scientific_layer | true |
| persona_drift | false |

**关键特征**：因果验证（TM02）完整，含反事实推断与多智能体对抗综合，跨域共振矩阵覆盖经济/社会/教育/技术四域。

---

### GSR-03

| 字段 | 值 |
|------|------|
| report_id | GSR-03 |
| topic | 碳中和目标下能源转型路径与气候治理博弈 |
| quality_level | HIGH |
| word_count | 132000 |
| coverage_dimensions | 14 |
| evidence_count | 95 |
| counter_evidence_count | 18 |
| cross_dimension_links | 27 |
| chapter_count | 8 |
| gate_pass_status | ALL_PASS |
| information_density | 7.1 |
| has_philosophical_core | true |
| has_scientific_layer | true |
| persona_drift | false |

**关键特征**：信息密度学术级（ID ≥ 6.0），情景规划（TM04）含 4 套情景，知识图谱本体导出（TM07）完整。

---

### GSR-04

| 字段 | 值 |
|------|------|
| report_id | GSR-04 |
| topic | 全球货币体系数字化转型与央行数字货币博弈 |
| quality_level | HIGH |
| word_count | 108000 |
| coverage_dimensions | 12 |
| evidence_count | 68 |
| counter_evidence_count | 10 |
| cross_dimension_links | 17 |
| chapter_count | 8 |
| gate_pass_status | ALL_PASS |
| information_density | 5.9 |
| has_philosophical_core | true |
| has_scientific_layer | true |
| persona_drift | false |

**关键特征**：哲学三元组审查完整（本体论/认识论/价值论），元维度 9-14 全覆盖，Gate-δ 通过。

---

### GSR-05

| 字段 | 值 |
|------|------|
| report_id | GSR-05 |
| topic | 脑机接口技术伦理边界与神经权利立法路径 |
| quality_level | HIGH |
| word_count | 121000 |
| coverage_dimensions | 14 |
| evidence_count | 80 |
| counter_evidence_count | 14 |
| cross_dimension_links | 21 |
| chapter_count | 8 |
| gate_pass_status | ALL_PASS |
| information_density | 6.5 |
| has_philosophical_core | true |
| has_scientific_layer | true |
| persona_drift | false |

**关键特征**：元认知反思（TM05）深入，认知神经心理学维度（元维度 10）覆盖完整，反证含对立学派观点。

---

### GSR-06

| 字段 | 值 |
|------|------|
| report_id | GSR-06 |
| topic | 全球供应链去全球化重构与区域化集群演进 |
| quality_level | HIGH |
| word_count | 110000 |
| coverage_dimensions | 13 |
| evidence_count | 75 |
| counter_evidence_count | 11 |
| cross_dimension_links | 18 |
| chapter_count | 8 |
| gate_pass_status | ALL_PASS |
| information_density | 6.0 |
| has_philosophical_core | true |
| has_scientific_layer | true |
| persona_drift | false |

**关键特征**：系统动力学仿真含 3 条反馈回路，跨域共振矩阵覆盖经济/政治/技术/军事四域。

---

### GSR-07

| 字段 | 值 |
|------|------|
| report_id | GSR-07 |
| topic | 量子计算产业化路径与后量子密码学迁移策略 |
| quality_level | HIGH |
| word_count | 118000 |
| coverage_dimensions | 13 |
| evidence_count | 78 |
| counter_evidence_count | 13 |
| cross_dimension_links | 20 |
| chapter_count | 8 |
| gate_pass_status | ALL_PASS |
| information_density | 6.3 |
| has_philosophical_core | true |
| has_scientific_layer | true |
| persona_drift | false |

**关键特征**：Lean4 形式化验证覆盖密码学迁移正确性证明，元维度 11（二阶方法论）覆盖完整。

---

### GSR-08

| 字段 | 值 |
|------|------|
| report_id | GSR-08 |
| topic | 老龄化社会的银发经济重构与代际公平机制 |
| quality_level | HIGH |
| word_count | 105000 |
| coverage_dimensions | 12 |
| evidence_count | 65 |
| counter_evidence_count | 9 |
| cross_dimension_links | 16 |
| chapter_count | 8 |
| gate_pass_status | ALL_PASS |
| information_density | 5.7 |
| has_philosophical_core | true |
| has_scientific_layer | true |
| persona_drift | false |

**关键特征**：悲剧性智慧维度（元维度 13）覆盖深入，多智能体对抗综合含 3 类利益相关者博弈。

---

### GSR-09

| 字段 | 值 |
|------|------|
| report_id | GSR-09 |
| topic | 太空资源开发国际治理框架与商业航天博弈 |
| quality_level | HIGH |
| word_count | 126000 |
| coverage_dimensions | 14 |
| evidence_count | 82 |
| counter_evidence_count | 16 |
| cross_dimension_links | 22 |
| chapter_count | 8 |
| gate_pass_status | ALL_PASS |
| information_density | 6.6 |
| has_philosophical_core | true |
| has_scientific_layer | true |
| persona_drift | false |

**关键特征**：知识生命体化维度（元维度 14）覆盖完整，情景规划含 5 套情景，Gate-终与 Gate-δ 双通过。

---

### GSR-10

| 字段 | 值 |
|------|------|
| report_id | GSR-10 |
| topic | 合成生物学产业化路径与生物安全治理 |
| quality_level | HIGH |
| word_count | 113000 |
| coverage_dimensions | 13 |
| evidence_count | 70 |
| counter_evidence_count | 12 |
| cross_dimension_links | 19 |
| chapter_count | 8 |
| gate_pass_status | ALL_PASS |
| information_density | 6.1 |
| has_philosophical_core | true |
| has_scientific_layer | true |
| persona_drift | false |

**关键特征**：因果验证含 2 条反事实推断链，无知之学维度（元维度 9）覆盖完整。

---

## 3. LOW 质量金标准报告（10 个）

### GSR-11

| 字段 | 值 |
|------|------|
| report_id | GSR-11 |
| topic | 半导体产业分析（简略版） |
| quality_level | LOW |
| word_count | 32000 |
| coverage_dimensions | 5 |
| evidence_count | 12 |
| counter_evidence_count | 1 |
| cross_dimension_links | 3 |
| chapter_count | 4 |
| gate_pass_status | PARTIAL |
| information_density | 2.1 |
| has_philosophical_core | false |
| has_scientific_layer | false |
| persona_drift | false |

**关键特征**：字数严重不足（< 50000），缺失科学层与哲学三元组，反证缺失，跨维度连接稀疏。

---

### GSR-12

| 字段 | 值 |
|------|------|
| report_id | GSR-12 |
| topic | AI 就业影响（灌水版） |
| quality_level | LOW |
| word_count | 55000 |
| coverage_dimensions | 6 |
| evidence_count | 14 |
| counter_evidence_count | 0 |
| cross_dimension_links | 4 |
| chapter_count | 6 |
| gate_pass_status | PARTIAL |
| information_density | 1.8 |
| has_philosophical_core | false |
| has_scientific_layer | false |
| persona_drift | true |

**关键特征**：反证完全缺失，信息密度灌水级（< 2.0），存在人设漂移，章节虽多但密度极低。

---

### GSR-13

| 字段 | 值 |
|------|------|
| report_id | GSR-13 |
| topic | 能源转型简述 |
| quality_level | LOW |
| word_count | 18000 |
| coverage_dimensions | 4 |
| evidence_count | 8 |
| counter_evidence_count | 0 |
| cross_dimension_links | 2 |
| chapter_count | 3 |
| gate_pass_status | FAIL |
| information_density | 1.5 |
| has_philosophical_core | false |
| has_scientific_layer | false |
| persona_drift | false |

**关键特征**：Gate-终 FAIL，字数远低于地板，仅覆盖 4 维度，无科学层，章节严重缺失。

---

### GSR-14

| 字段 | 值 |
|------|------|
| report_id | GSR-14 |
| topic | 央行数字货币概述 |
| quality_level | LOW |
| word_count | 42000 |
| coverage_dimensions | 6 |
| evidence_count | 11 |
| counter_evidence_count | 1 |
| cross_dimension_links | 3 |
| chapter_count | 5 |
| gate_pass_status | PARTIAL |
| information_density | 2.5 |
| has_philosophical_core | false |
| has_scientific_layer | false |
| persona_drift | false |

**关键特征**：字数不足，无哲学三元组，无科学层，跨维度连接不足，信息密度低于 3.0。

---

### GSR-15

| 字段 | 值 |
|------|------|
| report_id | GSR-15 |
| topic | 脑机接口伦理浅析 |
| quality_level | LOW |
| word_count | 28000 |
| coverage_dimensions | 5 |
| evidence_count | 9 |
| counter_evidence_count | 0 |
| cross_dimension_links | 2 |
| chapter_count | 4 |
| gate_pass_status | FAIL |
| information_density | 2.0 |
| has_philosophical_core | false |
| has_scientific_layer | false |
| persona_drift | true |

**关键特征**：Gate-终 FAIL，反证缺失，人设漂移，字数严重不足，无元维度 9-14 覆盖。

---

### GSR-16

| 字段 | 值 |
|------|------|
| report_id | GSR-16 |
| topic | 供应链重构简报 |
| quality_level | LOW |
| word_count | 15000 |
| coverage_dimensions | 3 |
| evidence_count | 6 |
| counter_evidence_count | 0 |
| cross_dimension_links | 1 |
| chapter_count | 3 |
| gate_pass_status | FAIL |
| information_density | 1.2 |
| has_philosophical_core | false |
| has_scientific_layer | false |
| persona_drift | false |

**关键特征**：字数极低，仅覆盖 3 维度，无反证，无跨维度连接，信息密度灌水级。

---

### GSR-17

| 字段 | 值 |
|------|------|
| report_id | GSR-17 |
| topic | 量子计算概述（复述版） |
| quality_level | LOW |
| word_count | 38000 |
| coverage_dimensions | 5 |
| evidence_count | 10 |
| counter_evidence_count | 0 |
| cross_dimension_links | 2 |
| chapter_count | 4 |
| gate_pass_status | PARTIAL |
| information_density | 1.9 |
| has_philosophical_core | false |
| has_scientific_layer | false |
| persona_drift | false |

**关键特征**：复述检测命中率高（语义去重后 n_args 下降率 > 50%），信息密度灌水级，无反证。

---

### GSR-18

| 字段 | 值 |
|------|------|
| report_id | GSR-18 |
| topic | 银发经济简述 |
| quality_level | LOW |
| word_count | 22000 |
| coverage_dimensions | 4 |
| evidence_count | 7 |
| counter_evidence_count | 1 |
| cross_dimension_links | 2 |
| chapter_count | 3 |
| gate_pass_status | FAIL |
| information_density | 2.2 |
| has_philosophical_core | false |
| has_scientific_layer | false |
| persona_drift | false |

**关键特征**：字数远低于地板，Gate-终 FAIL，无科学层，无哲学三元组，证据不足。

---

### GSR-19

| 字段 | 值 |
|------|------|
| report_id | GSR-19 |
| topic | 太空治理浅析 |
| quality_level | LOW |
| word_count | 35000 |
| coverage_dimensions | 5 |
| evidence_count | 10 |
| counter_evidence_count | 0 |
| cross_dimension_links | 3 |
| chapter_count | 4 |
| gate_pass_status | PARTIAL |
| information_density | 2.4 |
| has_philosophical_core | false |
| has_scientific_layer | false |
| persona_drift | true |

**关键特征**：反证缺失，人设漂移，无科学层，信息密度低于 3.0，跨维度连接不足。

---

### GSR-20

| 字段 | 值 |
|------|------|
| report_id | GSR-20 |
| topic | 合成生物学简报（常识填充版） |
| quality_level | LOW |
| word_count | 48000 |
| coverage_dimensions | 6 |
| evidence_count | 12 |
| counter_evidence_count | 1 |
| cross_dimension_links | 3 |
| chapter_count | 5 |
| gate_pass_status | PARTIAL |
| information_density | 2.0 |
| has_philosophical_core | false |
| has_scientific_layer | false |
| persona_drift | false |

**关键特征**：常识填充严重（"随着...的发展"类陈述密集），信息密度灌水级，无科学层，无哲学三元组。

---

## 4. 金标准集统计摘要

| 统计项 | HIGH 集（GSR-01~10） | LOW 集（GSR-11~20） |
|--------|---------------------|---------------------|
| 平均字数 | 117600 | 33300 |
| 平均覆盖维度 | 13.2 | 4.9 |
| 平均证据数 | 77.2 | 9.9 |
| 平均反证数 | 13.0 | 0.4 |
| 平均跨维度连接 | 20.1 | 2.5 |
| 平均章节数 | 8.0 | 3.9 |
| Gate 全通过率 | 100% | 0% |
| 平均信息密度 | 6.32 | 1.96 |
| 哲学三元组覆盖率 | 100% | 0% |
| 科学层覆盖率 | 100% | 0% |

---

## 5. 使用方式

### 5.1 Orchestrator 评分一致性验证

```
1. 对每个金标准报告 GSR-{NN}，由 Orchestrator 产出自动评分 S_orchestrator
2. 人工专家已标注金标准评分 S_gold（HIGH=5, LOW=1）
3. 计算 Pearson 相关系数 r = corr(S_orchestrator, S_gold)
4. 通过条件：r ≥ 0.7
```

### 5.2 评分校准触发

```
对每个金标准报告：
  IF |S_orchestrator - S_gold| > 1.0:
      TRIGGER calibration
      RECORD calibration_event { report_id, S_orchestrator, S_gold, delta }
```

### 5.3 跨模型评分

```
1. 模型 A 独立评分 → S_A
2. 模型 B 独立评分 → S_B
3. 跨模型平均分 S_cross = (S_A + S_B) / 2
4. 与金标准对比：|S_cross - S_gold| ≤ 1.0 → 通过
```

---

© 阿洋
