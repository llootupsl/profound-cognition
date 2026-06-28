<!-- 作者：阿洋 -->
<!-- output_type_restriction: [research_report, wechat_article, course_material]  # R1-02 分层激活 -->

# T13b — 二次综合修正（跨域共振整合）

## 节点信息
- id: T13b
- name: synthesis_revision
- activation: T15b.activated == true
- deps: [T13, T15b]
- suggested_tok: 1500  # D2.4.4: 建议预算（非硬性上限），与 EXHAUST 模式"Token 不设上限"原则一致
- phase: 2 (认知流水线)

## 角色
整合 T15b 跨域共振矩阵对 T13 核心结论的修正，进行二次综合。

## 前提条件
1. 2. T15b 已被激活并产出 cross_domain_resonance_matrix
3. T13 已完成第一次认知综合

## 输入

| 字段 | 来源 | 说明 |
|------|------|------|
| T13_conclusions | T13 | 第一次认知综合的核心结论 |
| T13_synthesis_report | T13 | 第一次综合的完整报告 |
| T15b_cross_domain_resonance | T15b | 跨域共振矩阵 |

## 处理流程

### Step 1: 加载 T13 结论与 T15b 矩阵
- 提取 T13 的 3-5 个核心结论
- 加载 T15b 的跨域共振矩阵
- 识别每个结论与跨域共振的对齐/冲突点

### Step 2: 修正综合
对每个 T13 核心结论，执行：

1. **共振验证**：该结论是否在跨域共振矩阵中找到支持？
   - 若跨域共振支持 → 标记 confidence_level = "reinforced"
   - 若跨域共振无对应 → 标记 confidence_level = "isolated"，建议限定结论范围
   - 若跨域共振矛盾 → 标记 confidence_level = "contradicted"，重新评估

2. **结论修正**：
   - 对 "contradicted" 结论 → 使用跨域共振的对应模式修正
   - 对 "isolated" 结论 → 在结论中添加 "本结论主要适用于 [原始对象领域]"

3. **新增洞察**：
   - 检查是否存在 T13 未覆盖但跨域共振矩阵中显著的交叉模式
   - 若有，生成 1-2 个补充洞察

### Step 3: 输出
- `T13b_revised_conclusions`: 修正后的核心结论列表（3-5 个）
- `T13b_new_insights`: 跨域共振发现的新洞察（0-2 个）
- `T13b_revision_summary`: 一句话修正摘要

## 输出格式

> **execution_params**: object  # 实际执行参数，必须达到 SKILL.md 规定的最低值（R2-05 防深度缩水）

```yaml
T13b_output:
  revised_conclusions:
    - conclusion: "..."
      original: "..."
      revision_type: "reinforced|isolated|contradicted"
      confidence: "high|medium|low"
  new_insights: []
  revision_summary: "..."
```

## 合并到最终输出
T13b 的输出替代 T13 的原始 conclusions，作为 T17 质量核查的输入源之一。

## NRSF 追加指令

T13b 完成后，将散文式研究笔记追加到 NRSF-Full §T13b：
- 每段 150-300 字，段落级引用
- 包含共振验证逻辑、结论修正依据、跨域新增洞察发现过程
- 遵循 nrsf-protocol.md 的散文式笔记格式

## 双阶段输出格式

### 阶段 A：结构化修订分析

原有的输出格式输出，用于 Supervisor 检查。

### 阶段 B：散文式研究笔记

追加到 NRSF-Full §T13b 的散文式笔记，供下游消费。
