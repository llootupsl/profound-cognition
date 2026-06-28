<!-- 作者：阿洋 -->

# Supervisor 检查项覆盖度矩阵 (Supervisor Coverage Matrix)

> **定位**: supervisors/checks/ 目录下 61 个 check YAML 文件的覆盖度矩阵，确保每个 DAG 节点、每个检查维度、每个宪法条款都有对应的检查项。
> **配套**: `supervisors/supervisor_protocol.md`、`scripts/supervisor-check-tests.py`
> **最后更新**: 2026-06-25

---

## 一、检查文件清单（61 个）

### 1.1 完整清单

| # | 检查文件 | 关联节点 | 节点类型 | 检查项数（约） | critical_path |
|---|---------|---------|---------|--------------|--------------|
| 1 | I01_check.yml | I01 | 迭代深化 | 4 | false |
| 2 | T00_check.yml | T00 | 初始化 | 5 | false |
| 3 | T00a_check.yml | T00a | 初始化 | 4 | false |
| 4 | T00b_check.yml | T00b | 初始化 | 4 | false |
| 5 | T01_check.yml | T01 | 输入分诊 | 6 | true |
| 6 | T01b_check.yml | T01b | 人设校准 | 5 | false |
| 7 | T01d_check.yml | T01d | 人设深化 | 4 | false |
| 8 | T02_check.yml | T02 | 研究底座 | 8 | true |
| 9 | T03_check.yml | T03 | 搜索执行 | 7 | true |
| 10 | T03b_check.yml | T03b | 搜索补充 | 5 | false |
| 11 | T04_check.yml | T04 | 来源筛选 | 6 | true |
| 12 | T05_check.yml | T05 | 来源验证 | 7 | true |
| 13 | T06_check.yml | T06 | NRSF 写入 | 6 | true |
| 14 | T07_check.yml | T07 | Gate-α | 6 | true |
| 15 | T07b_check.yml | T07b | Gate-α 补充 | 4 | false |
| 16 | T08_check.yml | T08 | 认知解构 | 7 | true |
| 17 | T09_check.yml | T09 | 认知框架 | 6 | true |
| 18 | T10_check.yml | T10 | 维度展开 | 7 | true |
| 19 | T11_check.yml | T11 | 跨维度连接 | 5 | true |
| 20 | T12_check.yml | T12 | 推理链构建 | 6 | true |
| 21 | T12b_check.yml | T12b | 推理链补充 | 4 | false |
| 22 | T13_check.yml | T13 | 综合判断 | 7 | true |
| 23 | T13b_check.yml | T13b | 综合补充 | 4 | false |
| 24 | T14_check.yml | T14 | Gate-β | 5 | true |
| 25 | T15_check.yml | T15 | 事实核查 | 6 | true |
| 26 | T15b_check.yml | T15b | 核查补充 | 4 | false |
| 27 | T16_check.yml | T16 | Gate-γ | 6 | true |
| 28 | T17_check.yml | T17 | 幻觉检测 | 5 | true |
| 29 | T18_check.yml | T18 | 冲突处置 | 5 | true |
| 30 | T19_check.yml | T19 | 认知综合 | 7 | true |
| 31 | T19b_prescription_gate_check.yml | T19b | 处方门控 | 4 | true |
| 32 | T20_check.yml | T20 | 输出总控 | 5 | true |
| 33 | T20_output_guard_check.yml | T20 | 输出守卫 | 4 | true |
| 34 | T20a_research_render_check.yml | T20a | 研究渲染 | 6 | true |
| 35 | T20b_wechat_render_check.yml | T20b | 公众号渲染 | 5 | true |
| 36 | T20c_check.yml | T20c | 课程渲染 | 5 | true |
| 37 | T20d_check.yml | T20d | 跨媒介审查 | 6 | true |
| 38 | T21_check.yml | T21 | 去重验证 | 4 | true |
| 39 | T22_nrsf_synthesize_check.yml | T22 | NRSF 综合 | 6 | true |
| 40 | T23_meta_dim_part1_check.yml | T23 | 元维度 1-4 | 5 | true |
| 41 | T24_meta_dim_part2_check.yml | T24 | 元维度 5-8 | 5 | true |
| 42 | T25_meta_dim_part3_check.yml | T25 | 元维度 9-14 | 5 | true |
| 43 | T26_meta_insight_cross_check.yml | T26 | 元洞察交叉 | 6 | true |
| 44 | T27_meta_visual_map_check.yml | T27 | 元视觉图谱 | 5 | true |
| 45 | T28_gate_final_check.yml | T28 | Gate-终 | 9 | true |
| 46 | TM01_system_dynamics_check.yml | TM01 | 系统动力学 | 5 | true |
| 47 | TM02_causal_verification_check.yml | TM02 | 因果验证 | 5 | true |
| 48 | TM03_adversarial_synthesis_check.yml | TM03 | 对抗综合 | 5 | true |
| 49 | TM04_scenario_landscape_check.yml | TM04 | 情景景观 | 4 | true |
| 50 | TM05_meta_reflection_check.yml | TM05 | 元反思 | 4 | true |
| 51 | TM06_meta_layer_verify_check.yml | TM06 | 元层验证 | 5 | true |
| 52 | TM06b_check.yml | TM06b | 元层补充 | 3 | false |
| 53 | TM07_ontology_export_check.yml | TM07 | 本体导出 | 4 | true |
| 54 | T_env_probe_check.yml | T_env | 环境探测 | 3 | false |
| 55 | T_gate_delta_check.yml | T_gate_delta | Gate-δ | 7 | true |
| 56 | T_meta_dim_11_12_check.yml | T_meta_11_12 | 元维度 11-12 | 4 | false |
| 57 | T_meta_dim_13_14_check.yml | T_meta_13_14 | 元维度 13-14 | 4 | false |
| 58 | T_meta_dim_9_10_check.yml | T_meta_9_10 | 元维度 9-10 | 4 | false |
| 59 | T_philosophical_core_check.yml | T_phil | 哲学核心 | 5 | true |
| 60 | checkpoint_check.yml | CHECKPOINT | 检查点 | 4 | false |
| 61 | persona-check.yml | PERSONA | 人设初始化 | 30 | true |

### 1.2 统计摘要

| 指标 | 数值 |
|------|------|
| 检查文件总数 | 61 |
| critical_path 节点检查文件数 | 42 |
| 非 critical_path 节点检查文件数 | 19 |
| 检查项总数（估算） | ~320 |
| CRITICAL 严重级别检查项数（估算） | ~180 |
| MAJOR 严重级别检查项数（估算） | ~90 |
| MINOR 严重级别检查项数（估算） | ~50 |

---

## 二、检查维度覆盖度矩阵

### 2.1 检查维度定义

每个 check YAML 文件可包含以下维度的检查项：

| 维度 | YAML 键 | 说明 |
|------|---------|------|
| 结构检查 | structural_checks | 字段完整性、Schema 合规性 |
| 深度检查 | depth_checks | 内容深度、模糊词扫描、量化阈值 |
| 完整性检查 | integrity_checks | 来源标注、数据一致性 |
| 宪法检查 | constitution_checks | P1-P6 宪法条款合规 |
| 检索检查 | retrieval_checks | 强制检索触发器覆盖 |
| 一致性检查 | consistency_checks | 跨字段、跨类型一致性 |
| 禁止项检查 | must_not | 不可出现的字段或行为 |

### 2.2 维度覆盖度矩阵

| 检查文件 | structural | depth | integrity | constitution | retrieval | consistency | must_not |
|---------|-----------|-------|-----------|-------------|-----------|------------|----------|
| T01_check.yml | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| T02_check.yml | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| T03_check.yml | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| T05_check.yml | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| T08_check.yml | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| T13_check.yml | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| T15_check.yml | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| T19_check.yml | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| T20a_check.yml | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| T28_check.yml | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| persona-check.yml | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| ...（其余文件类似） | | | | | | | |

> **图例**: ✅ 包含该维度 | ❌ 不包含该维度 | 完整矩阵见各 check YAML 文件

### 2.3 维度覆盖度统计

| 维度 | 包含该维度的文件数 | 覆盖率 |
|------|------------------|--------|
| structural_checks | 61 | 100% |
| depth_checks | 45 | 73.8% |
| integrity_checks | 42 | 68.9% |
| constitution_checks | 55 | 90.2% |
| retrieval_checks | 8 | 13.1% |
| consistency_checks | 3 | 4.9% |
| must_not | 5 | 8.2% |

### 2.4 覆盖度缺口分析

| 缺口 | 影响 | 缓解方案 |
|------|------|---------|
| retrieval_checks 仅 8 个文件包含 | 搜索类节点（T02/T03/T05）已覆盖，其他节点不强制检索 | 按需扩展，非搜索节点不需要检索检查 |
| consistency_checks 仅 3 个文件包含 | persona-check 已覆盖人设一致性 | 渲染节点（T20a/b/c）建议新增跨链路一致性检查 |
| must_not 仅 5 个文件包含 | persona-check 已覆盖人设禁止项 | 关键节点（T28/T19）建议新增 must_not 检查 |

---

## 三、宪法条款覆盖度

### 3.1 宪法条款与检查项映射

| 宪法条款 | 条款内容 | 对应检查维度 | 覆盖文件数 | 覆盖率 |
|---------|---------|------------|-----------|--------|
| P1 | 禁止模糊词 ≥3 → RETRYING | constitution_checks.C01 | 55 | 90.2% |
| P2 | 必填字段缺失 → RETRYING | constitution_checks.C02 | 55 | 90.2% |
| P3 | 无来源+常识冲突 → RETRYING | constitution_checks.C03 | 55 | 90.2% |
| P4 | 穷尽重试直至达标 | constitution_checks.C04 | 50 | 82.0% |
| P5 | 不得对已修正项重复 RETRYING | constitution_checks.C05 | 50 | 82.0% |
| P6 | SKIPPED==COMPLETED | （隐式覆盖，无独立检查项） | 61 | 100% |

### 3.2 宪法条款覆盖度结论

- P1-P3 覆盖率 90.2%，未覆盖的 6 个文件为非 critical_path 节点（如 T00a/T00b/T03b 等补充节点），可接受
- P4-P5 覆盖率 82.0%，未覆盖的 11 个文件为初始化与补充节点，不涉及重试场景，可接受
- P6 为隐式规则，由 Orchestrator 在节点状态判定时执行，无需独立检查项

---

## 四、DAG 节点覆盖度

### 4.1 DAG 节点与检查文件映射

| Phase | DAG 节点 | 检查文件 | 覆盖状态 |
|-------|---------|---------|---------|
| Phase 0 | T00/T00a/T00b/T01/T01b/T01d | 7 个检查文件 | ✅ 完全覆盖 |
| Phase 1 | T02/T03/T03b/T04/T05/T06/T07/T07b | 8 个检查文件 | ✅ 完全覆盖 |
| Phase 2 | T08/T09/T10/T11/T12/T12b/T13/T13b/T14 | 9 个检查文件 | ✅ 完全覆盖 |
| Phase 3 | T15/T15b/T16/T17/T18/T19/T19b | 7 个检查文件 | ✅ 完全覆盖 |
| Phase 4 | T20/T20a/T20b/T20c/T20d/T21 | 6 个检查文件 | ✅ 完全覆盖 |
| Phase 5 | T22/T23/T24/T25/T26/T27/T28 | 7 个检查文件 | ✅ 完全覆盖 |
| Phase 6 | TM01-TM07/TM06b | 8 个检查文件 | ✅ 完全覆盖 |
| 跨 Phase | I01/checkpoint/persona/T_env/T_gate_delta/T_meta_dim_*/T_phil | 9 个检查文件 | ✅ 完全覆盖 |

### 4.2 DAG 节点覆盖度结论

- 所有 DAG 节点（含主节点与补充节点）均有对应的检查文件
- 终局 Gate（T28/T_gate_delta）检查项数最多（9/7 项），符合终局门控的严格性要求
- persona-check 检查项数最多（30 项），覆盖 12 字段系统的完整枚举校验

---

## 五、检查项量化标准统一

### 5.1 严重级别定义

| 级别 | 含义 | 处置规则 | 量化阈值 |
|------|------|---------|---------|
| CRITICAL | 关键检查——违反即 RETRYING | 任一 CRITICAL 失败 → verdict=RETRYING | 通过率 = 100% |
| MAJOR | 主要检查——影响输出质量 | MAJOR 通过率 < 80% → verdict=RETRYING | 通过率 ≥ 80% |
| MINOR | 次要检查——格式与规范性 | MINOR 通过率 < 60% → verdict=RETRYING | 通过率 ≥ 60% |

### 5.2 量化标准与 Gate 权重的协同

本节量化标准与 `supervisor_protocol.md` 中「Gate 检查项权重化（R7-02）」的权重体系对齐：

| 本节级别 | R7-02 权重级别 | 权重值 | 处置规则一致性 |
|---------|--------------|--------|--------------|
| CRITICAL | blocking | 5 | ✅ 一致——违反即 FAIL |
| MAJOR | major | 3 | ✅ 一致——通过率 < 80% 则 FAIL |
| MINOR | minor | 1 | ✅ 一致——通过率 < 60% 则 FAIL |

---

## 六、维护与治理

### 6.1 新增检查文件流程

1. 在 `supervisors/checks/` 下创建 `{node_id}_check.yml`
2. 在本文件 §1.1 清单中登记
3. 在 §2.2 维度覆盖度矩阵中登记维度覆盖情况
4. 在 §4.1 DAG 节点映射中登记
5. 运行 `python scripts/supervisor-check-tests.py` 验证通过

### 6.2 检查项变更流程

1. 修改对应 check YAML 文件
2. 更新本文件 §1.1 中的检查项数
3. 运行 `python scripts/supervisor-check-tests.py` 验证通过

---

## 七、变更日志

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| v1.0.0 | 2026-06-25 | 初始发布：61 检查文件清单 + 维度覆盖度矩阵 + 宪法条款覆盖度 + DAG 节点覆盖度 + 量化标准统一 |
