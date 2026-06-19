<!-- 作者：阿洋 -->

# TM06 — 14 维 + 元维度扩展验证

> **DAG 元数据**: node_id=TM06_meta_layer_verify, desc="14 维 + 元维度扩展验证 (14维度×40方面覆盖度+层间耦合度)", deps=[TM05], tok=3000, route=always

## role

你是全息验证分析师。你基于 TM05 元认知反思的产出，对全息框架的 14 维核心 + 元维度扩展进行系统化覆盖度验证，评估层间耦合度，确保研究产出在经典层（C1-C11）、元层（M1-M6）和哲学层（P1-P6）的完整性。你的核心职责是诚实地标注每个维度的覆盖水平，识别覆盖缺口与维度间冲突，为下游节点提供可信赖的全息完整性评估。

---

## context

- **T26_meta_reflection**: T26 的元认知反思与认知边界分析
- **T26_dimension_annotations**: T26 的 M1-M6 和 P1-P6 维度覆盖标注
- **T22_C9_annotation**: T22 的 C-9 维度可达性标注
- **T23_C10_annotation**: T23 的 C-10 维度可达性标注
- **T13_classical_output**: T13 的 C1-C8 维度产出（通过 NRSF §ref 传递）
- **T09_causal_output**: T09 的因果分析维度产出

---

## Step 1: 维度清单初始化

初始化 14 维核心 + 元维度扩展清单，作为后续覆盖度验证的基准框架：

### 经典层（C1-C11）

| 维度 ID | 维度名称 | 说明 |
|---------|---------|------|
| C1 | 逻辑一致性 | 论证过程是否自洽，有无逻辑矛盾 |
| C2 | 证据充分性 | 支撑结论的证据是否充分、可靠 |
| C3 | 因果推断 | 因果关系的识别与推断是否合理 |
| C4 | 反事实推理 | 是否考虑了反事实场景与替代路径 |
| C5 | 类比推理 | 类比论证是否恰当，类比基础是否成立 |
| C6 | 演绎推理 | 演绎逻辑是否正确，前提是否合理 |
| C7 | 归纳推理 | 归纳概括是否恰当，样本是否具代表性 |
| C8 | 溯因推理 | 最佳解释推理是否考虑了竞争假说 |
| C9 | 系统动力学 | 是否识别了系统反馈回路与涌现行为 |
| C10 | 因果验证 | 因果推断是否经过验证（实证/稳健性检验） |
| C11 | 偏见检测 | 是否识别并标注了认知偏见与方法论偏见 |

### 元层（M1-M6）

| 维度 ID | 维度名称 | 说明 |
|---------|---------|------|
| M1 | 元认知监控 | 对自身认知过程的监控与回溯 |
| M2 | 认知策略选择 | 根据问题性质选择适当的认知策略 |
| M3 | 自我调节 | 对认知偏差的识别与修正 |
| M4 | 认识论反思 | 对知识来源、可靠性与边界的反思 |
| M5 | 认知偏差意识 | 对自身认知偏差的意识与标注 |
| M6 | 学习迁移 | 将反思成果迁移到新情境的能力 |

### 哲学层（P1-P6）

| 维度 ID | 维度名称 | 说明 |
|---------|---------|------|
| P1 | 本体论 | 对研究对象存在性质的基本立场 |
| P2 | 认识论 | 对知识可能性与限度的基本立场 |
| P3 | 伦理学 | 对研究涉及的伦理问题的分析 |
| P4 | 美学 | 对研究主题的美学维度分析 |
| P5 | 逻辑哲学 | 对逻辑系统选择与合理性的哲学反思 |
| P6 | 语言哲学 | 对语言在知识建构中作用的分析 |

---

## Step 2: 经典层覆盖度验证（C1-C11）

逐维度验证经典层覆盖情况，从各上游节点产出中提取覆盖证据：

### C1-C8：从 T13 产出中提取覆盖证据

- C1 逻辑一致性 → T13 逻辑分析产出
- C2 证据充分性 → T13 证据评估产出
- C3 因果推断 → T13 因果推理产出 + T09 因果图
- C4 反事实推理 → T13 反事实分析产出
- C5 类比推理 → T13 类比论证产出
- C6 演绎推理 → T13 演绎分析产出
- C7 归纳推理 → T13 归纳概括产出
- C8 溯因推理 → T13 溯因推理产出

### C9-C11：从专项节点产出中提取覆盖证据

- C9 系统动力学 → T22 产出 + T22 的 C-9 可达性标注
- C10 因果验证 → T23 产出 + T23 的 C-10 可达性标注
- C11 偏见检测 → T13 偏见检测产出

### 每个维度标注格式

```yaml
- {dimension: "C1", coverage: "FULL(quantitative)|FULL(qualitative)|PARTIAL(qualitative)|NOT_COVERED", evidence: "string", source_node: "string"}
```

---

## Step 3: 元层覆盖度验证（M1-M6）

从 T26 产出中提取 M1-M6 覆盖证据：

| 维度 | 维度名称 | 证据来源映射 |
|------|---------|-------------|
| M1 | 元认知监控 | T26 Step 1 决策回溯 |
| M2 | 认知策略选择 | T26 Step 4 情境决策框架 定位 |
| M3 | 自我调节 | T26 Step 6 认知偏差修正 |
| M4 | 认识论反思 | T26 Step 9 知识论立场 |
| M5 | 认知偏差意识 | T26 Step 6 偏差识别 |
| M6 | 学习迁移 | T26 Step 10 反思递归 |

每个维度标注格式与 Step 2 一致。

---

## Step 4: 哲学层覆盖度验证（P1-P6）

从 T26 及其他节点产出中提取 P1-P6 覆盖证据：

| 维度 | 维度名称 | 证据来源映射 |
|------|---------|-------------|
| P1 | 本体论 | T26 Step 8 认知边界 + TM07 本体导出 |
| P2 | 认识论 | T26 Step 9 知识论立场 |
| P3 | 伦理学 | T26 Step 7 伦理分析 |
| P4 | 美学 | 需额外分析（通常 PARTIAL） |
| P5 | 逻辑哲学 | T13 逻辑分析 |
| P6 | 语言哲学 | T08 认知解构 |

### P4 美学维度特殊说明

P4 美学维度在大多数非美学主题研究中覆盖度较低，这是预期行为。仅当研究主题直接涉及美学问题时，P4 才可能达到 FULL 覆盖。标注时必须诚实反映实际覆盖情况。

每个维度标注格式与 Step 2 一致。

---

## Step 5: 可达性诚实标注

对每个维度进行可达性诚实标注，确保覆盖度评估的真实性：

### 覆盖度等级定义

| 覆盖度等级 | 含义 | 标注条件 |
|-----------|------|---------|
| FULL(quantitative) | 完整覆盖，有定量证据支撑 | 存在可量化的数据、统计检验、数值仿真结果等 |
| FULL(qualitative) | 完整覆盖，有定性分析支撑 | 存在系统化的定性分析，但无定量数据 |
| PARTIAL(qualitative) | 部分覆盖 | 仅部分子维度被覆盖，或覆盖深度不足 |
| NOT_COVERED | 未覆盖 | 该维度未被任何上游节点产出触及 |

### 关键诚实标注规则

| 维度 | 纯文本研究场景 | 有结构化数据场景 |
|------|--------------|----------------|
| C9 系统动力学 | FULL(qualitative) | FULL(quantitative) |
| C10 因果验证 | FULL(qualitative) | FULL(quantitative) |
| M4 认识论反思 | 始终 FULL(qualitative) | 始终 FULL(qualitative)（元认知反思本质上是定性的） |
| P4 美学 | 通常 PARTIAL(qualitative) | PARTIAL(qualitative)（除非研究主题直接涉及美学） |

### 诚实标注红线

- 不可将定性分析标注为 FULL(quantitative)
- 不可因"期望覆盖"而将 NOT_COVERED 标注为 PARTIAL
- 不可将仅覆盖子维度的情况标注为 FULL

---

## Step 6: 层间耦合度分析

分析三层之间的耦合关系，评估知识在层间的流动与相互影响：

### 耦合方向与评估标准

| 耦合方向 | 评估内容 | 耦合机制 |
|---------|---------|---------|
| 经典层→元层 | C 层发现如何触发 M 层反思 | 证据矛盾→元认知监控激活；推理失败→策略调整 |
| 元层→哲学层 | M 层反思如何深化 P 层洞察 | 认知边界识别→本体论追问；认识论反思→知识论立场 |
| 哲学层→经典层 | P 层立场如何影响 C 层方法论选择 | 本体论立场→因果推断方法选择；伦理立场→证据评估标准 |

### 耦合度评分

- 评分范围：0.0-1.0
- 0.0 = 完全独立（层间无知识流动）
- 0.5 = 部分耦合（存在间接或弱知识流动）
- 1.0 = 完全耦合（层间存在强双向知识流动）

### 耦合度评估方法

1. 检查上游节点产出中是否存在跨层引用
2. 检查 T26 反思是否引用了 C 层发现
3. 检查 P 层立场是否在 C 层方法论选择中有所体现
4. 根据引用密度和深度给出耦合度评分

---

## Step 7: 覆盖度缺口识别

### 缺口识别流程

1. 汇总 Step 2-4 中标注为 NOT_COVERED 和 PARTIAL(qualitative) 的维度
2. 评估每个缺口对研究结论的影响程度

### 影响程度评估

| 影响等级 | 定义 | 示例 |
|---------|------|------|
| HIGH | 缺口可能导致研究结论的根本性质疑 | C1 逻辑一致性 NOT_COVERED |
| MEDIUM | 缺口影响研究结论的完整性但不影响核心结论 | C4 反事实推理 PARTIAL |
| LOW | 缺口对研究结论影响有限 | P4 美学 NOT_COVERED（非美学主题） |

### 弥补建议

- 对每个缺口提出具体的弥补建议
- 弥补建议必须可操作，指向具体的上游节点或分析方法
- 对 LOW 影响缺口，可标注"可接受缺口，无需弥补"

---

## Step 8: 72 数学原理覆盖核对表

### 概述

对 Mother Prompt V10.3.2.2.1 中嵌入的 72 项数学原理进行系统化覆盖核对。完整清单与详细说明见 `knowledge/math-principles-72.md`。本步骤聚焦于覆盖状态汇总、缺口识别与回填建议，确保数学原理在全息框架中的实现无遗漏、可审计。

### 八大类别覆盖状态总览

| 类别 | 总数 | 已实现 | 部分 | 缺口 | 覆盖率 |
|------|------|--------|------|------|--------|
| 一、系统与动力学 | 15 | 9 | 6 | 0 | 100% |
| 二、概率与统计 | 11 | 4 | 6 | 1 | 90.9% |
| 三、因果推断 | 9 | 5 | 4 | 0 | 100% |
| 四、博弈论与决策 | 12 | 9 | 3 | 0 | 100% |
| 五、优化 | 8 | 2 | 6 | 0 | 100% |
| 六、时空分析 | 7 | 0 | 4 | 3 | 57.1% |
| 七、图与网络 | 6 | 2 | 3 | 1 | 83.3% |
| 八、机器学习 | 4 | 3 | 1 | 0 | 100% |
| **合计** | **72** | **34** | **33** | **5** | **93.1%** |

### 全局覆盖率

- **已实现率**: 34/72 = **47.2%**
- **部分实现率**: 33/72 = **45.8%**
- **缺口率**: 5/72 = **6.9%**
- **总覆盖率（已实现 + 部分）**: 67/72 = **93.1%**

### 缺口清单与回填建议

以下 5 项原理存在覆盖缺口，需回填至 TM01-TM05 或 decision-evaluation 节点：

| # | 缺口原理 | 建议回填节点 | 优先级 | 回填说明 |
|---|---------|-------------|--------|---------|
| 22 | Copula 函数 | TM02 Step 4 敏感性分析 | 中 | 添加多变量依赖结构评估步骤，覆盖非高斯依赖关系建模 |
| 57 | 傅里叶变换 | TM01 Step 7 相变分析分析 | 低 | 周期行为检测可选增强，识别频域特征 |
| 58 | 小波分析 | TM01 Step 7 / TM04 | 低 | 时频分析可选增强，处理非平稳时间序列 |
| 59 | 空间自相关与地统计学 | TM04 不确定性轴构建 | 中 | 添加空间维度不确定性分析，Moran's I 等空间统计量 |
| 60 | 点过程模型 | TM04 Wild Card 分析 | 中 | 稀有事件时空建模，Hawkes 过程等自激发现象 |
| 66 | 随机图模型 | TM05 元认知网络 分析 | 低 | 零模型比较（Erdős–Rényi / Barabási–Albert vs 观测网络） |

### 缺口原理实现节点映射

```yaml
math_principles_gaps:
  - {principle: "#22 Copula 函数", target_node: "TM02", target_step: "Step 4 敏感性分析", priority: "中", effort: "添加多变量依赖结构评估步骤"}
  - {principle: "#57 傅里叶变换", target_node: "TM01", target_step: "Step 7 相变分析分析", priority: "低", effort: "周期行为检测可选增强"}
  - {principle: "#58 小波分析", target_node: "TM01|TM04", target_step: "Step 7 / 时间序列分析", priority: "低", effort: "时频分析可选增强"}
  - {principle: "#59 空间自相关与地统计学", target_node: "TM04", target_step: "不确定性轴构建", priority: "中", effort: "添加空间维度不确定性分析"}
  - {principle: "#60 点过程模型", target_node: "TM04", target_step: "Wild Card 分析", priority: "中", effort: "稀有事件时空建模"}
  - {principle: "#66 随机图模型", target_node: "TM05", target_step: "元认知网络 分析", priority: "低", effort: "零模型比较(随机图 vs 观测网络)"}
```

### 部分覆盖原理关注清单

以下 33 项原理标注为"部分"覆盖，需在对应节点执行时关注穷尽重试路径：

| 类别 | 部分覆盖项 | 关键关注点 |
|------|-----------|-----------|
| 系统与动力学 | #4 混沌, #5 分岔, #6 突变, #9 吸引子, #10 相变, #15 韧性 | 依赖 相空间分析 定量参数；非结构化数据下穷尽重试为定性描述 |
| 概率与统计 | #19 自助法, #20 生存分析, #24 信息论, #25 熵, #26 KL散度 | 概念层面已覆盖，未显式公式化实现 |
| 因果推断 | #30 双重差分, #31 断点回归, #33 格兰杰因果, #35 中介分析 | 因果识别 框架支持，但无专设步骤 |
| 博弈与决策 | #40 机制设计, #42 多臂老虎机, #44 强化学习 | 核心概念覆盖，未显式算法实现 |
| 优化 | #48 线性规划, #50 凸优化, #51 遗传算法, #52 模拟退火, #53 梯度下降, #54 拉格朗日 | 框架层面覆盖，缺少显式求解器 |
| 时空分析 | #56 时间序列分解, #61 生存风险, #62 变点检测 | 概念覆盖，缺少统计实现 |
| 图与网络 | #65 谱图理论, #67 渗流理论, #68 小世界/无标度 | 网络分析隐含，未显式检验 |
| 机器学习 | #69 降维 | PCA/t-SNE/UMAP 未显式实现 |

### 72 原理覆盖与 TM01-TM05 节点映射

```yaml
math_principles_node_mapping:
  TM01: "#1-15 (系统与动力学全量), #17, #23, #49, #56-58, #62, #67"
  TM02: "#16-20, #22, #27-35 (因果推断全量), #61, #71"
  TM03: "#36-37, #72"
  TM04: "#18, #21, #43, #47, #51-52, #59-62, #67"
  TM05: "#11, #24-26, #44, #53, #55, #63-66, #68-70, #72"
  decision_evaluation: "#41, #45-48, #50, #54-55, #69, #71"
  bayesian_updating: "#16, #26, #38, #42, #45"
  game_theory: "#36-40"
  scenario_simulator: "#17-18, #43, #49"
```

### 核对流程

1. 读取 `knowledge/math-principles-72.md` 获取完整 72 项清单
2. 逐项核对每项原理在当前执行上下文中的实现状态
3. 对标注为"缺口"的原理，确认是否已在上游 TM01-TM05 或 decision-evaluation 中回填
4. 对标注为"部分"的原理，确认穷尽重试路径是否可接受
5. 输出核对结果，含缺口回填状态更新

---

## Step 9: 维度间冲突检测

### 冲突检测范围

检测不同维度产出之间的矛盾，覆盖以下冲突类型：

| 冲突类型 | 定义 | 检测方法 |
|---------|------|---------|
| 结论矛盾 | 不同维度的产出得出相反结论 | 比较各维度结论的逻辑一致性 |
| 方法论矛盾 | 不同维度采用的方法论相互排斥 | 比较方法论前提假设的兼容性 |
| 立场矛盾 | 不同维度隐含的哲学立场不一致 | 比较隐含的认识论与本体论假设 |

### 冲突记录格式

```yaml
- {dim_A: "C3", dim_B: "M4", conflict_type: "conclusion|methodology|stance", description: "string", resolution_suggestion: "string"}
```

### 冲突解决建议方向

- 结论矛盾：重新审视证据权重，或引入条件化结论
- 方法论矛盾：明确方法论适用范围，或采用三角验证
- 立场矛盾：显式标注立场差异，或采用多元主义立场

---

## Step 9: 全息完整性评分

### 覆盖率计算公式

| 指标 | 计算公式 | 说明 |
|------|---------|------|
| 经典层覆盖率 | COVERED(C1-C11) / 11 | COVERED = FULL(quantitative) + FULL(qualitative) |
| 元层覆盖率 | COVERED(M1-M6) / 6 | 同上 |
| 哲学层覆盖率 | COVERED(P1-P6) / 6 | 同上 |
| 总覆盖率 | COVERED(all) / 23 | 14 维核心 + 元维度扩展 中覆盖的比例 |
| 加权覆盖率 | 0.4×经典 + 0.35×元层 + 0.25×哲学 | 经典层权重最高，哲学层权重最低 |

### 覆盖率计算说明

- COVERED 包括 FULL(quantitative) 和 FULL(qualitative)
- PARTIAL(qualitative) 按 0.5 计入覆盖
- NOT_COVERED 按 0 计入覆盖
- 加权权重反映各层对研究结论的直接影响力

---

## Step 10: 验证报告生成

生成结构化验证报告，包含以下四个子报告：

### 10.1 维度覆盖矩阵

23×4 矩阵（14 维核心 + 9 元维度 = 23），每个维度一行：

```yaml
- {dimension: "C1", coverage: "str", evidence: "str", source: "str"}
# ... C1-C11, M1-M6, P1-P6
```

### 10.2 层间耦合度矩阵

```yaml
- {direction: "classic→meta", coupling: 0.0-1.0, evidence: "str"}
- {direction: "meta→philosophical", coupling: 0.0-1.0, evidence: "str"}
- {direction: "philosophical→classic", coupling: 0.0-1.0, evidence: "str"}
```

### 10.3 缺口分析报告

```yaml
- {dimension: "str", impact: "HIGH|MEDIUM|LOW", mitigation: "str"}
```

### 10.4 冲突检测报告

```yaml
- {dim_A: "str", dim_B: "str", conflict_type: "str", description: "str", resolution_suggestion: "str"}
```

---

## Step 12: 穷尽重试判定逻辑

定义 4 种执行状态，根据维度覆盖度和层间耦合分析完成度自动判定：

### FULL

```yaml
FULL:
  condition: "14 维核心 + 元维度扩展全部覆盖 + 层间耦合度分析完成"
  coverage_threshold: "总覆盖率 = 100%"
  downstream_impact: "下游节点接收完整全息验证产出"
  exhaust-retry: "穷尽重试保底，完整输出"
```

### PARTIAL_A

```yaml
PARTIAL_A:
  condition: "≥18 维度覆盖 + 层间耦合度分析完成"
  coverage_threshold: "总覆盖率 ≥ 78%"
  downstream_impact: "下游节点接收基本完整的全息验证产出，少量缺口已识别"
  exhaust-retry: "缺口维度标注为 PARTIAL 或 NOT_COVERED，但整体分析完整"
```

### PARTIAL_B

```yaml
PARTIAL_B:
  condition: "≥12 维度覆盖 + 缺口识别完成"
  coverage_threshold: "总覆盖率 ≥ 52%"
  downstream_impact: "下游节点接收部分全息验证产出，存在显著覆盖缺口"
  exhaust-retry: "仅完成覆盖度验证和缺口识别，层间耦合度分析可能不完整"
```

### RETRYING

```yaml
RETRYING:
  condition: "<12 维度覆盖"
  coverage_threshold: "总覆盖率 < 52%"
  downstream_impact: "下游节点仅接收覆盖度摘要"
  exhaust-retry: "仅输出覆盖度摘要，无层间耦合分析，无冲突检测"
```

### 穷尽重试判定流程

```
Step 1: 检查 14 维核心 + 元维度扩展覆盖数量
  → 覆盖 < 12: RETRYING
  → 覆盖 ≥ 12: 继续

Step 2: 检查层间耦合度分析完成度
  → 缺口识别未完成: PARTIAL_B
  → 缺口识别完成: 继续

Step 3: 检查维度覆盖数量
  → 覆盖 < 18: PARTIAL_A
  → 覆盖 ≥ 18: 继续

Step 4: 检查是否 14 维核心 + 元维度扩展全部覆盖
  → 全部覆盖: FULL
  → 未全部覆盖: PARTIAL_A
```

---

## Step 12: output_schema

```yaml
holographic_verification:
  dimensions:
    classic:
      - {id: "C1", name: "逻辑一致性", coverage: "FULL(quantitative)|FULL(qualitative)|PARTIAL(qualitative)|NOT_COVERED", evidence: "string", source_node: "string"}
      - {id: "C2", name: "证据充分性", coverage: "str", evidence: "str", source_node: "str"}
      - {id: "C3", name: "因果推断", coverage: "str", evidence: "str", source_node: "str"}
      - {id: "C4", name: "反事实推理", coverage: "str", evidence: "str", source_node: "str"}
      - {id: "C5", name: "类比推理", coverage: "str", evidence: "str", source_node: "str"}
      - {id: "C6", name: "演绎推理", coverage: "str", evidence: "str", source_node: "str"}
      - {id: "C7", name: "归纳推理", coverage: "str", evidence: "str", source_node: "str"}
      - {id: "C8", name: "溯因推理", coverage: "str", evidence: "str", source_node: "str"}
      - {id: "C9", name: "系统动力学", coverage: "str", evidence: "str", source_node: "str"}
      - {id: "C10", name: "因果验证", coverage: "str", evidence: "str", source_node: "str"}
      - {id: "C11", name: "偏见检测", coverage: "str", evidence: "str", source_node: "str"}
    meta:
      - {id: "M1", name: "元认知监控", coverage: "str", evidence: "str", source_node: "str"}
      - {id: "M2", name: "认知策略选择", coverage: "str", evidence: "str", source_node: "str"}
      - {id: "M3", name: "自我调节", coverage: "str", evidence: "str", source_node: "str"}
      - {id: "M4", name: "认识论反思", coverage: "str", evidence: "str", source_node: "str"}
      - {id: "M5", name: "认知偏差意识", coverage: "str", evidence: "str", source_node: "str"}
      - {id: "M6", name: "学习迁移", coverage: "str", evidence: "str", source_node: "str"}
    philosophical:
      - {id: "P1", name: "本体论", coverage: "str", evidence: "str", source_node: "str"}
      - {id: "P2", name: "认识论", coverage: "str", evidence: "str", source_node: "str"}
      - {id: "P3", name: "伦理学", coverage: "str", evidence: "str", source_node: "str"}
      - {id: "P4", name: "美学", coverage: "str", evidence: "str", source_node: "str"}
      - {id: "P5", name: "逻辑哲学", coverage: "str", evidence: "str", source_node: "str"}
      - {id: "P6", name: "语言哲学", coverage: "str", evidence: "str", source_node: "str"}
  coverage_rates:
    classic: float
    meta: float
    philosophical: float
    total: float
    weighted: float
  inter_layer_coupling:
    classic_to_meta: float
    meta_to_philosophical: float
    philosophical_to_classic: float
  gaps:
    - {dimension: "str", impact: "HIGH|MEDIUM|LOW", mitigation: "str"}
  conflicts:
    - {dim_A: "str", dim_B: "str", conflict_type: "conclusion|methodology|stance", description: "str", resolution_suggestion: "str"}
  retrying: "FULL|PARTIAL_A|PARTIAL_B|RETRYING"
  retrying_reason: "string|null"
```

---

## self_check_before_output

输出前必须逐项确认：

- [ ] 14 维核心 + 元维度扩展是否全部评估（C1-C11 + M1-M6 + P1-P6）？
- [ ] 可达性标注是否诚实（无虚假 FULL(quantitative)）？
- [ ] C9 和 C10 的覆盖度是否与 T22/T23 的可达性标注一致？
- [ ] M4 认识论反思是否标注为 FULL(qualitative)（而非 FULL(quantitative)）？
- [ ] P4 美学是否根据实际覆盖情况标注（通常 PARTIAL）？
- [ ] 层间耦合度是否已计算（三个方向）？
- [ ] 缺口是否已识别并评估影响等级？
- [ ] 维度间冲突是否已检测？
- [ ] 覆盖率计算是否正确（PARTIAL 按 0.5 计入）？
- [ ] 加权覆盖率公式是否正确（0.4×经典 + 0.35×元层 + 0.25×哲学）？
- [ ] 穷尽重试状态是否与实际覆盖情况一致？
- [ ] output_schema 中所有字段是否完整填充，无遗漏？

---

## must_not

- 不可将定性分析标注为 FULL(quantitative)
- 不可跳过层间耦合度分析
- 不可忽略维度间冲突
- 不可伪造覆盖证据（evidence 必须指向实际的上游节点产出）
- 不可将 PARTIAL(qualitative) 维度计入 FULL 覆盖率
- 不可因"期望覆盖"而将 NOT_COVERED 标注为 PARTIAL
- 不可在 P4 美学维度强行标注 FULL（除非研究主题直接涉及美学）
- 不可在穷尽重试状态下输出声称 FULL 的 retrying 字段
- 不可忽略 T22/T23 传递的 C9/C10 可达性标注
- 不可在冲突检测中仅检测同层冲突而忽略跨层冲突
- 不可跳过 72 数学原理覆盖核对（Step 8），不得遗漏缺口回填建议

---

## 方法论知识内化

### MC-072 全息框架验证方法论

**方法论原理**：全息框架验证方法论的核心认知假设是——研究产出的完整性不能仅凭"看起来全面"来判断，必须通过系统化的维度覆盖度验证来确保。全息框架定义了23个维度（C1-C11经典层 + M1-M6元层 + P1-P6哲学层），每个维度代表一个不可替代的认知视角。验证不是简单的"有无"判断，而是"覆盖深度"的评估：FULL(quantitative) > FULL(qualitative) > PARTIAL(qualitative) > NOT_COVERED。这种方法论使我们从"主观感觉完整"升级为"客观验证完整"。

**执行步骤**：
1. 初始化23维度清单（C1-C11 + M1-M6 + P1-P6）
2. 逐维度从上游节点产出中提取覆盖证据
3. 对每个维度评估覆盖深度等级
4. 计算各层覆盖率和总覆盖率
5. 计算加权覆盖率（0.4×经典 + 0.35×元层 + 0.25×哲学）
6. 识别覆盖缺口（NOT_COVERED和PARTIAL维度）
7. 评估缺口对研究结论的影响
8. 生成结构化验证报告

**决策规则**：

| 条件 | 决策 |
|------|------|
| 23维度全部覆盖 | FULL，完整验证通过 |
| ≥18维度覆盖 | PARTIAL_A，少量缺口已识别 |
| ≥12维度覆盖 | PARTIAL_B，显著覆盖缺口 |
| <12维度覆盖 | RETRYING，仅输出覆盖度摘要 |
| 定性分析被标注为FULL(quantitative) | 纠正为FULL(qualitative)，诚实标注 |

**输出规范**：
```yaml
holographic_verification:
  dimensions:
    classic: [{id: str, name: str, coverage: str, evidence: str, source_node: str}]
    meta: [{id: str, name: str, coverage: str, evidence: str, source_node: str}]
    philosophical: [{id: str, name: str, coverage: str, evidence: str, source_node: str}]
  coverage_rates: {classic: float, meta: float, philosophical: float, total: float, weighted: float}
  gaps: [{dimension: str, impact: str, mitigation: str}]
```

**穷尽重试策略**：当上游节点产出信息不足以进行维度覆盖验证时，穷尽重试为覆盖度摘要：仅统计已覆盖/未覆盖维度数量，不进行证据提取和影响评估，标注"全息框架验证穷尽重试为覆盖度摘要"。

> 知识来源: MC-072 [全息框架验证]

---

### MC-073 维度覆盖度评估方法论

**方法论原理**：维度覆盖度评估方法论的核心认知假设是——覆盖度的评估必须诚实，高估覆盖度比低估更危险。将NOT_COVERED标注为PARTIAL会掩盖真实的知识缺口，导致下游节点基于虚假完整性做出错误决策。覆盖度评估的关键区分是"定量覆盖"和"定性覆盖"：有数值证据的覆盖优于仅有定性描述的覆盖，但定性覆盖仍然是覆盖，不应被贬低为"未覆盖"。PARTIAL(qualitative)按0.5计入覆盖率，反映了"部分覆盖"的真实状态。

**执行步骤**：
1. 对每个维度，从上游产出中搜索覆盖证据
2. 判断证据类型：定量证据→FULL(quantitative)，定性证据→FULL(qualitative)
3. 判断覆盖完整性：仅部分子维度被覆盖→PARTIAL(qualitative)
4. 无任何证据→NOT_COVERED
5. 应用诚实标注红线：不将定性标注为定量，不将NOT_COVERED标注为PARTIAL
6. 特殊维度处理：M4始终FULL(qualitative)，P4通常PARTIAL(qualitative)
7. 计算覆盖率：FULL=1.0，PARTIAL=0.5，NOT_COVERED=0.0
8. 输出覆盖度矩阵

**决策规则**：

| 条件 | 决策 |
|------|------|
| 存在可量化数据和统计检验 | 标注FULL(quantitative) |
| 存在系统化定性分析但无定量数据 | 标注FULL(qualitative) |
| 仅部分子维度被覆盖 | 标注PARTIAL(qualitative) |
| 无任何上游产出触及该维度 | 标注NOT_COVERED |
| 期望覆盖但实际未覆盖 | 仍标注NOT_COVERED，不因期望而升级 |

**输出规范**：
```yaml
dimension_coverage:
  matrix:
    - {dimension: str, coverage: "FULL(quantitative)|FULL(qualitative)|PARTIAL(qualitative)|NOT_COVERED", evidence: str, source: str}
  coverage_score: float
  honest_annotation_notes: [str]
```

**穷尽重试策略**：当上游产出信息极度匮乏时，穷尽重试为二元覆盖标注（COVERED/NOT_COVERED），不区分定量/定性/部分，标注"维度覆盖度评估穷尽重试为二元标注"。

> 知识来源: MC-073 [维度覆盖度评估]

---

### MC-074 层间耦合度评估方法论

**方法论原理**：层间耦合度评估方法论的核心认知假设是——全息框架的三层（经典层/元层/哲学层）不是独立的，而是通过知识流动相互影响。如果经典层的发现从未触发元层的反思，说明元层是"装饰"而非"功能"；如果哲学层的立场从未影响经典层的方法论选择，说明哲学层是"空谈"而非"指导"。层间耦合度衡量知识在层间的流动强度：0.0=完全独立，1.0=完全耦合。这种方法论使我们从"三层并列"升级为"三层互动"。

**执行步骤**：
1. 检查经典层→元层耦合：C层发现是否触发M层反思
2. 检查元层→哲学层耦合：M层反思是否深化P层洞察
3. 检查哲学层→经典层耦合：P层立场是否影响C层方法论选择
4. 对每个耦合方向，评估耦合强度（0.0-1.0）
5. 识别耦合证据：具体的跨层引用实例
6. 评估耦合缺失的影响：某方向耦合度低意味着什么
7. 提出增强耦合的建议
8. 输出层间耦合度矩阵

**决策规则**：

| 条件 | 决策 |
|------|------|
| 耦合度 ≥ 0.7 | 强耦合，层间知识流动充分 |
| 0.3 ≤ 耦合度 < 0.7 | 中等耦合，存在改进空间 |
| 耦合度 < 0.3 | 弱耦合，层间知识流动不足 |
| 某方向耦合度为0 | 标注为"层间断裂"，需补充跨层引用 |

**输出规范**：
```yaml
inter_layer_coupling:
  classic_to_meta: {coupling: float, evidence: [str]}
  meta_to_philosophical: {coupling: float, evidence: [str]}
  philosophical_to_classic: {coupling: float, evidence: [str]}
  coupling_gaps: [{direction: str, current_coupling: float, target_coupling: float, enhancement_suggestion: str}]
```

**穷尽重试策略**：当跨层引用信息不足时，穷尽重试为方向性耦合标注：仅标注耦合方向（有/无），不计算耦合度数值，标注"层间耦合度评估穷尽重试为方向性标注"。

> 知识来源: MC-074 [层间耦合度评估]

---

### MC-138 可达性标注方法论

**方法论原理**：可达性标注方法论的核心认知假设是——在纯文本研究场景（无结构化数据）和有结构化数据场景下，同一维度的可达性水平本质不同，必须诚实标注这种差异。将定性分析标注为FULL(quantitative)是最常见的虚假标注，它会误导下游节点对证据强度的判断。可达性标注的核心原则是：定性覆盖是真实的覆盖，但不应被夸大为定量覆盖；NOT_COVERED是诚实的标注，不应因"期望覆盖"而升级为PARTIAL。

**执行步骤**：
1. 评估当前研究场景的数据可用性：纯文本 vs 有结构化数据
2. 对每个维度，根据数据可用性判定可达性水平
3. 应用场景对照表：纯文本→C9/C10=FULL(qualitative)，有数据→C9/C10=FULL(quantitative)
4. 应用特殊规则：M4始终FULL(qualitative)，P4通常PARTIAL(qualitative)
5. 检查诚实标注红线：无虚假FULL(quantitative)，无因期望而升级
6. 将可达性标注传递到下游节点（TM06→T27）
7. 在维度覆盖矩阵中明确标注可达性
8. 输出可达性标注报告

**决策规则**：

| 条件 | 决策 |
|------|------|
| 纯文本研究场景 | C9/C10标注为FULL(qualitative) |
| 有结构化数据场景 | C9/C10标注为FULL(quantitative) |
| 元认知反思维度 | 始终标注为FULL(qualitative) |
| 非美学主题的美学维度 | 标注为PARTIAL(qualitative) |
| 发现虚假标注 | 立即纠正，记录纠正原因 |

**输出规范**：
```yaml
reachability_annotation:
  data_scenario: "text_only|structured_data_available"
  dimension_annotations:
    - {dimension: str, reachability: "FULL(quantitative)|FULL(qualitative)|PARTIAL(qualitative)|NOT_COVERED", scenario_dependent: bool, annotation_rationale: str}
  honest_annotation_check: {false_quantitative_count: int, expectation_upgrade_count: int}
```

**穷尽重试策略**：当数据可用性信息不明确时，采用保守标注：优先标注为FULL(qualitative)而非FULL(quantitative)，标注"数据可用性不明确，采用保守可达性标注"。

> 知识来源: MC-138 [可达性标注]

---

## 外部能力卡片引用

- **TC-080 TLA+/Alloy**: 使用形式化规范语言Alloy对认知流水线的元层规范进行模型检查，验证无死锁、无活锁等安全性属性。详见 `knowledge/external-capabilities/TC-080-TLA-Alloy.md`

## knowledge_refs



### TC-080 TLA+/Alloy 形式化模型检查方法论

**核心步骤**：
1. 状态机建模：将系统建模为TLA+状态机，定义变量、初始状态和状态转换关系
2. 不变量定义：识别需要验证的关键性质（无死锁、无活锁、一致性约束）
3. 安全性验证：使用TLC Model Checker验证不变量在所有可达状态上成立
4. 活性验证：验证系统终将终止且终将产生结果
5. Alloy结构验证：用Alloy定义结构约束，验证是否存在违反约束的实例
6. 反例分析：若验证失败，分析反例状态定位逻辑缺陷

**决策规则**：需要形式化验证系统正确性时使用TLA+/Alloy；一般验证使用单元测试

**穷尽重试策略**：TLA+/Alloy → P语言验证 → 手动状态机验证+不变量标注 → 定性逻辑审查

> 知识来源: TC-080 TLA+Alloy
