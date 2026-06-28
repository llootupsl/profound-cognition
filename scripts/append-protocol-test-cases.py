#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""append-protocol-test-cases.py — 一次性为 15 个协议追加测试用例章节

排除：context-budget-protocol.md、user-feedback-protocol.md（由其他子代理处理）
排除：evidence-standard-protocol.md（已包含测试用例）
"""

import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROTOCOLS_DIR = Path(__file__).parent.parent / "protocols"

SKIP_FILES = {
    "context-budget-protocol.md",
    "user-feedback-protocol.md",
    "evidence-standard-protocol.md",
}

# 每个协议的测试用例内容
TEST_CASES = {
    "checkpoint-protocol.md": """

---

## 测试用例 (D3.4.4)

### 测试用例 1：Phase 级检查点保存

**给定输入**：Phase 1（研究底座）完成，T01-T06 全部节点状态为 completed，核心结论摘要为"全球经济秩序重建的核心叙事"。

**应产出**：检查点保存 phase_id=Phase 1，node_completion_status 包含 T01-T06 全部 completed，core_conclusions 非空（≤500 字），nrsf_position 指向当前 NRSF 写入位置。

### 测试用例 2：断点恢复

**给定输入**：用户再次触发同等任务，存在最近 checkpoint（phase_id=Phase 2，T07-T13 部分完成）。

**应产出**：从 Phase 2 起点恢复执行，T07-T13 中已完成的节点标记为 CACHED 不重新执行，未完成节点继续执行。

### 测试用例 3：时间衰减权重

**给定输入**：来源 A 发布于 10 天前，来源 B 发布于 200 天前，λ=0.01。

**应产出**：来源 A 权重 w=exp(-0.01×10)≈0.905，来源 B 权重 w=exp(-0.01×200)≈0.135。来源 B 权重 < 0.37 阈值，标注"检查点较旧"。

### 测试用例 4：跨会话检查点衰减

**给定输入**：跨会话检查点年龄 45 天，未标注"永久保存"。

**应产出**：衰减权重 0.02-0.14，标注"弱检查点"，恢复前向用户确认。
""",
    "decision-evaluation-protocol.md": """

---

## 测试用例 (D3.4.4)

### 测试用例 1：决策方案评分

**给定输入**：3 个决策方案，每个方案在 5 个准则下的评分矩阵（方案 A: [8,7,9,6,8]，方案 B: [7,9,8,7,7]，方案 C: [9,6,7,9,9]），准则权重 [0.3,0.2,0.2,0.2,0.1]。

**应产出**：方案 A 加权得分 7.7，方案 B 加权得分 7.7，方案 C 加权得分 7.8。推荐方案 C，但需标注与方案 A/B 差距 < 0.1 属于统计噪声。

### 测试用例 2：敏感性分析

**给定输入**：决策方案评分中准则 1 的权重从 0.3 扰动到 0.5（其他权重等比缩放）。

**应产出**：输出权重扰动后的方案排名变化，若排名翻转则标注"决策对准则 1 权重敏感"。

### 测试用例 3：帕累托最优检查

**给定输入**：4 个方案在 3 个准则下的评分，方案 A 在准则 1 最优但准则 2/3 最劣。

**应产出**：识别方案 A 为非帕累托最优（被方案 B/D 支配），标注"方案 A 被支配"。
""",
    "domain-analysis-protocol.md": """

---

## 测试用例 (D3.4.4)

### 测试用例 1：领域引擎激活

**给定输入**：object_type=technology，主题为"大语言模型对就业市场的影响"。

**应产出**：激活 tech-engine（技术演化路径）+ economics-engine（劳动力市场）+ social-engine（社会变迁）+ psychology-engine（认知影响），输出领域引擎激活清单。

### 测试用例 2：跨领域冲突识别

**给定输入**：tech-engine 认为"AI 提升生产力"（正面），social-engine 认为"AI 加剧不平等"（负面）。

**应产出**：识别跨领域视角冲突，输出冲突描述 + 两个领域的证据等级 + 建议的综合结论方向。

### 测试用例 3：领域覆盖度检查

**给定输入**：研究报告涉及 8 个维度，但仅激活了 3 个领域引擎。

**应产出**：标注"领域覆盖度不足（3/8）"，列出未覆盖的维度对应的推荐领域引擎。
""",
    "execution-protocol.md": """

---

## 测试用例 (D3.4.4)

### 测试用例 1：DAG 就绪节点识别

**给定输入**：DAG 中 T01 无依赖，T02 deps=[T01]，T03 deps=[T01]，T04 deps=[T02,T03]。当前 T01 已完成。

**应产出**：find_ready_nodes() 返回 [T02, T03]（并行就绪），T04 不在就绪列表中（依赖未满足）。

### 测试用例 2：Gate 失败回退

**给定输入**：Gate-α 检查 T01-T06 产出，发现 T03 的 self_check_score=70（< 85 阈值），判定为 fail。

**应产出**：触发 T03 回退，重新执行 T03；T04/T05/T06（依赖 T03）状态清理为 pending；回退日志记录触发节点=T03、影响范围=[T04,T05,T06]。

### 测试用例 3：并行节点执行

**给定输入**：T10/T11/T12 三个对抗节点 deps=[T09]，T09 已完成。

**应产出**：T10/T11/T12 同时进入就绪状态，并行执行，结果在 T12b 汇聚。

### 测试用例 4：循环检测

**给定输入**：DAG 中存在 A→B→C→A 的循环依赖。

**应产出**：拓扑排序检测到循环，输出错误"Cycle detected: A→B→C→A"，拒绝执行。
""",
    "exhaust-retry-protocol.md": """

---

## 测试用例 (D3.4.4)

### 测试用例 1：穷尽重试触发

**给定输入**：节点 T05 第一次执行 self_check_score=60（< 85），触发重试。

**应产出**：节点状态变为 RETRYING，retry_feedback 注入 context_package，重试次数 +1。

### 测试用例 2：连续 3 次重试未通过

**给定输入**：节点 T05 连续 3 次重试，self_check_score 分别为 60/65/70（均 < 85）。

**应产出**：触发升级处理，调用更强模型或人工介入，标注"3 次重试未通过"。

### 测试用例 3：穷尽重试替代路径

**给定输入**：DoWhy 因果推断不可用（库未安装）。

**应产出**：按 L1→L2→L3→L4 逐级穷尽重试：L1 完整 DoWhy → L2 手动后门准则 → L3 因果图+识别策略声明 → L4 纯文字因果结构分析。最终执行 L4，标注"穷尽重试 L4"。

### 测试用例 4：重试成功

**给定输入**：节点 T05 第一次失败（score=70），第二次重试改进了证据覆盖度，score=88。

**应产出**：节点状态变为 completed，retry_count=1，记录"重试改进点：补充了 2 个 L1 来源"。
""",
    "handoff-protocol.md": """

---

## 测试用例 (D3.4.4)

### 测试用例 1：Context Package 标准格式

**给定输入**：T02 完成执行，产出包含 task_id、output、nrsf_refs、execution_params。

**应产出**：Context Package 包含 task_id=T02、output（JSON Schema 校验通过）、nrsf_refs（≥1 条 §ref）、execution_params（非空），格式符合 handoff-protocol 规范。

### 测试用例 2：上游引用解析

**给定输入**：T09 的 context_package 引用 §ref:T02:main_narrative 和 §ref:T05:evidence_summary。

**应产出**：Orchestrator 解析两个 §ref，从 NRSF 中提取对应叙事片段，注入 T09 的 context_package.upstream_refs。

### 测试用例 3：§ref 不存在报错

**给定输入**：T09 引用 §ref:T02:nonexistent_narrative（该 narrative_id 不存在于 NRSF）。

**应产出**：报错"§ref:T02:nonexistent_narrative not found in NRSF"，不静默跳过。
""",
    "illustration-generation-protocol.md": """

---

## 测试用例 (D3.4.4)

### 测试用例 1：图表类型选择

**给定输入**：研究报告中需要展示"全球 GDP 增长率 2010-2025 时间序列"。

**应产出**：选择折线图（时间序列数据），标注 x 轴=年份、y 轴=GDP 增长率，生成 Mermaid 或 ECharts 代码。

### 测试用例 2：Penrose 因果回路图生成

**给定输入**：TM01 系统动力学产出包含增强回路 R1（投资→产能→收入→投资）。

**应产出**：生成 Penrose DSL 代码，包含 R1 节点和正反馈边，标注回路类型为"增强回路"。

### 测试用例 3：图表质量检查

**给定输入**：生成的图表缺少标题、轴标签和图例。

**应产出**：质量检查失败，标注"缺少 title/x_label/y_label/legend"，触发重试。
""",
    "iterative-deepening-protocol.md": """

---

## 测试用例 (D3.4.4)

### 测试用例 1：缺口识别与排级

**给定输入**：T13 综合叙事中存在 3 个缺口（A 类论证链不闭合、B 类缺少直接证据、C 类缺少反证）。

**应产出**：识别 3 个缺口，排级为 P0（A 类）、P1（B 类）、P1（C 类），执行补研。

### 测试用例 2：收敛判据满足

**给定输入**：连续 2 轮迭代，ΔInfo < 0.05，所有 P0/P1 缺口已闭合。

**应产出**：满足收敛判据（质量条件 + 信息增益条件），终止迭代，输出迭代报告。

### 测试用例 3：人工检查点

**给定输入**：已执行 5 轮迭代，仍有 2 个 P0 缺口未闭合。

**应产出**：触发人工检查点，向用户展示进度（已闭合缺口数、剩余缺口数、信息增益曲线），等待用户确认。

### 测试用例 4：补研执行

**给定输入**：P0 缺口"X 导致 Y 但缺少因果机制"。

**应产出**：执行定向搜索（≥15 次、≥15 个来源、≥3 种来源类型），补研结果追加到 NRSF-Full §I01。
""",
    "multi-form-delivery-protocol.md": """

---

## 测试用例 (D3.4.4)

### 测试用例 1：多格式输出路由

**给定输入**：output_type=research_report，研究报告已完成。

**应产出**：路由到 T20a_research_render，生成 Typst PDF（首选）或 WeasyPrint HTML（备选），包含完整 §1-§8 结构。

### 测试用例 2：跨媒介一致性检查

**给定输入**：同一研究报告生成了 PDF 版本和公众号版本。

**应产出**：T20d 跨媒介审查执行 6 项检查（事实一致性/证据等级匹配/语气适配性/核心结论一致/引用完整性/品牌标识一致），输出审查报告。

### 测试用例 3：格式适配链触发

**给定输入**：Typst 渲染失败（缺少字体）。

**应产出**：触发格式适配链，降级到 WeasyPrint HTML，标注"格式适配：Typst→WeasyPrint"，内容完整保留。
""",
    "nrsf-protocol.md": """

---

## 测试用例 (D3.4.4)

### 测试用例 1：§ref 标记格式校验

**给定输入**：节点产出包含 §ref:T02:main_narrative:v1。

**应产出**：§ref 解析成功，node_id=T02、narrative_id=main_narrative、version=v1，从 NRSF 中提取对应叙事片段。

### 测试用例 2：NRSF 只追加不删除

**给定输入**：T13 修订了之前的叙事片段 main_narrative（v1→v2）。

**应产出**：NRSF 保留 v1（不删除），追加 v2，下游节点默认引用 v2，可在 context_package 指定引用 v1。

### 测试用例 3：并发写入冲突

**给定输入**：T10/T11/T12 并行执行，同时向 NRSF 写入叙事片段。

**应产出**：并发写入协议生效，每个节点写入独立的 narrative_id（path_10/path_11/path_12），无冲突。

### 测试用例 4：NRSF 写入失败穷尽重试

**给定输入**：NRSF 写入失败（磁盘满）。

**应产出**：按 L1→L2→L3→L4 穷尽重试：L1 完整写入 → L2 部分写入重试 → L3 内存暂存 → L4 输出系统完全不可用时持续重试。
""",
    "output-expansion-protocol.md": """

---

## 测试用例 (D3.4.4)

### 测试用例 1：字数地板检查

**给定输入**：research_report 最终成品字数为 80000 字（< 100000 字地板）。

**应产出**：触发字数不足警告，标注"未达字数地板（80000/100000）"，要求补充展开。

### 测试用例 2：信息密度计算

**给定输入**：某章节 5000 字，包含 10 个独立论点、15 个证据、5 个反证、8 个跨维度连接。

**应产出**：信息密度 = (10×15×5×8)/5000×1000 = 1200/5000×1000 = 240... 实际公式 (10×15×5×8)/5000×1000 = 6000/5 = 1200。密度等级 ≥6.0 高密度。

### 测试用例 3：灌水警告

**给定输入**：某章节 3000 字，仅 2 个独立论点、3 个证据、0 个反证、1 个跨维度连接。

**应产出**：信息密度 = (2×3×0×1)/3000×1000 = 0（反证数为 0 导致密度为 0）。触发灌水警告，标注"低密度章节，缺少反证"。

### 测试用例 4：分批交付触发

**给定输入**：最终成品预估 60000 字（> 50000 字阈值）。

**应产出**：触发分批交付，每批至少 1 个完整章节，批次标识格式正确。
""",
    "output-rendering-protocol.md": """

---

## 测试用例 (D3.4.4)

### 测试用例 1：格式净化

**给定输入**：研究报告中包含内部标记（如 §ref:T02:main_narrative、[DEBUG:...]）。

**应产出**：格式净化后移除所有内部标记，§ref 转换为可读引用格式（如"参见 T02 主叙事第 3 段"），[DEBUG:...] 标记删除。

### 测试用例 2：渲染引擎选择

**给定输入**：output_type=research_report，目标格式=PDF。

**应产出**：首选 Typst 渲染，生成 PDF；若 Typst 不可用，降级到 WeasyPrint，标注"格式适配链：Typst→WeasyPrint"。

### 测试用例 3：渲染质量检查

**给定输入**：渲染后的 PDF 中存在字体缺失（显示为方框）。

**应产出**：渲染质量检查失败，标注"字体缺失：霞鹜文楷"，触发格式适配链降级到系统字体。
""",
    "output-schema-spec.md": """

---

## 测试用例 (D3.4.4)

### 测试用例 1：JSON Schema 校验通过

**给定输入**：节点 T02 的 output 符合 JSON Schema 规范（包含 task_id、output、nrsf_refs、execution_params 字段，类型正确）。

**应产出**：JSON Schema 校验通过，允许输出。

### 测试用例 2：JSON Schema 校验失败

**给定输入**：节点 T02 的 output 缺少 execution_params 字段。

**应产出**：JSON Schema 校验失败，错误信息"missing required field: execution_params"，触发重试。

### 测试用例 3：self_check 量化标准

**给定输入**：节点 T13 的 self_check_score=88（≥ 85 阈值）。

**应产出**：self_check 通过，允许输出。

### 测试用例 4：self_check 未达阈值

**给定输入**：节点 T13 的 self_check_score=80（< 85 阈值）。

**应产出**：self_check 未通过，触发重试，retry_feedback 注入 context_package。
""",
    "self-evaluation-protocol.md": """

---

## 测试用例 (D3.4.4)

### 测试用例 1：自评通过

**给定输入**：节点 T09 执行完成，self_check 清单全部通过，self_check_score=90。

**应产出**：自评通过，允许输出，score 写入 execution_ledger。

### 测试用例 2：自评未通过

**给定输入**：节点 T09 执行完成，self_check 清单中 2 项未通过，self_check_score=70。

**应产出**：自评未通过（< 85 阈值），触发重试，retry_feedback 包含未通过项的改进建议。

### 测试用例 3：跨模型自评

**给定输入**：Gate-终（T28）执行跨模型审计，模型 A 评分 88，模型 B 评分 82。

**应产出**：两模型评分分歧 > 5 分，触发第三模型裁定或人工介入。
""",
    "write-while-research-protocol.md": """

---

## 测试用例 (D3.4.4)

### 测试用例 1：边研究边写作

**给定输入**：T02 研究底座完成 L1-L3 层，已收集 20 个来源。

**应产出**：触发边研究边写作，将 L1-L3 层发现写入 NRSF-Full 的散文式笔记，不等待全部研究完成。

### 测试用例 2：研究笔记与最终输出分离

**给定输入**：T02 产出的研究笔记包含原始数据、中间推理过程。

**应产出**：研究笔记写入 NRSF-Full（内部使用），最终输出仅引用结论性叙事片段（通过 §ref），不暴露中间推理过程。

### 测试用例 3：增量写作

**给定输入**：T05 完成 L6 证据层，补充了 5 个新证据。

**应产出**：增量追加到 NRSF-Full 的 L6 章节，不重写已有内容，标注"增量追加：+5 证据"。
""",
}


def main():
    print("=" * 60)
    print("为 15 个协议追加测试用例章节（D3.4.4）")
    print("=" * 60)

    success = 0
    skipped = 0
    failed = 0

    for proto_file in sorted(PROTOCOLS_DIR.glob("*.md")):
        name = proto_file.name
        if name in SKIP_FILES:
            print(f"  [SKIP] {name}")
            skipped += 1
            continue

        if name not in TEST_CASES:
            print(f"  [WARN] {name}: 无测试用例定义")
            failed += 1
            continue

        # 检查是否已有测试用例章节
        try:
            content = proto_file.read_text(encoding="utf-8")
        except Exception as e:
            print(f"  [ERROR] {name}: 读取失败 ({e})")
            failed += 1
            continue

        if "测试用例 (D3.4.4)" in content:
            print(f"  [EXISTS] {name}: 已有测试用例章节")
            success += 1
            continue

        # 追加测试用例
        test_case_content = TEST_CASES[name]
        try:
            with open(proto_file, "a", encoding="utf-8") as f:
                f.write(test_case_content)
            print(f"  [OK] {name}: 追加测试用例")
            success += 1
        except Exception as e:
            print(f"  [ERROR] {name}: 写入失败 ({e})")
            failed += 1

    print("-" * 60)
    print(f"[结果] 成功={success}, 跳过={skipped}, 失败={failed}")
    print("=" * 60)


if __name__ == "__main__":
    main()
