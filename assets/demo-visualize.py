#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
脚本名称: demo-visualize.py
用途: 跨平台可视化 profound-cognition 的 58 节点 DAG 执行流程
作者: 阿洋
版本: 6.0.0
日期: 2026-06-25
================================================================================
本脚本是 demo-record.sh 的跨平台补充版本（Windows 无 bash 时使用）。
产物:
  1. assets/dag-topology.mmd      — Mermaid DAG 拓扑图（可嵌入 README/GitHub）
  2. assets/execution-timeline.md — 执行时间线卡片（Markdown 表格）
  3. assets/demo-summary.json     — 执行摘要 JSON（机器可读）
零依赖：仅使用 Python 标准库，无需 pip install。
================================================================================
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ----------------------------------------------------------------------------
# 跨平台 UTF-8 输出兼容（修复 Windows GBK 编码崩溃）
# ----------------------------------------------------------------------------
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ----------------------------------------------------------------------------
# 常量定义
# ----------------------------------------------------------------------------
VERSION = "6.0.0"
SKILL_NAME = "profound-cognition"
DEMO_PROMPT = "穷尽分析中国新能源汽车产业的竞争格局与供应链韧性"

# 脚本所在目录的父目录 = skill 根目录
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
ASSETS_DIR = SCRIPT_DIR  # 本脚本位于 assets/ 下

# ----------------------------------------------------------------------------
# 58 节点 DAG 拓扑定义（与 SKILL.md SSOT 严格对齐）
# 格式: (node_id, phase, 中文名称, 类型)
# 类型: node / gate / hard_gate
# 节点总数: 58（Phase1=15 + Phase2=9 + Phase3=8 + Phase4=6 + Phase5=20，含 TM06b）
# 注: G1-G6 为交付前硬门控，不属于 DAG 节点，单独列出用于可视化
# ----------------------------------------------------------------------------
DAG_NODES = [
    # ===== Phase 1 — 研究底座层 (15 nodes) =====
    ("T_env_probe", "P1", "运行环境与模型能力探测", "node"),
    ("T00a", "P1", "时间锚定", "node"),
    ("T01", "P1", "输入分流", "node"),
    ("T01b", "P1", "写作声音校准", "node"),
    ("T00b", "P1", "输入情绪基调提取", "node"),
    ("T01d", "P1", "人设故事解析", "node"),
    ("T00", "P1", "研究大纲+母假设路由", "node"),
    ("T02", "P1", "L1+L2研究底座", "node"),
    ("T03", "P1", "L3结构变量", "node"),
    ("T03b", "P1", "横纵交叉矩阵分析", "node"),
    ("T04", "P1", "L4+L5比较叙事", "node"),
    ("T05", "P1", "L6+L7证据利益", "node"),
    ("T06", "P1", "L8+L9反事实边界", "node"),
    ("T07", "P1", "Gate-α 研究底座门控", "gate"),
    ("T07b", "P1", "纵横交汇分析", "node"),

    # ===== Phase 2 — 认知流水线层 (9 nodes) =====
    ("T08", "P2", "认知解构", "node"),
    ("T09", "P2", "多路径推理（7条+分支剪枝）", "node"),
    ("T10", "P2", "魔鬼代言人-逻辑攻击", "node"),
    ("T11", "P2", "魔鬼代言人-证据攻击", "node"),
    ("T12", "P2", "魔鬼代言人-范围攻击", "node"),
    ("T12b", "P2", "三路对抗交叉融合", "node"),
    ("T13", "P2", "认知综合+深度信号扫描+3轮递归", "node"),
    ("I01", "P2", "迭代深化补研循环", "node"),
    ("T14", "P2", "Gate-β 认知流水线门控", "gate"),

    # ===== Phase 3 — 领域分析与质量保障层 (8 nodes) =====
    ("T15", "P3", "领域引擎分析", "node"),
    ("T15b", "P3", "跨域共振矩阵", "node"),
    ("T16", "P3", "Gate-γ 领域分析门控", "gate"),
    ("T13b", "P3", "二次综合修正", "node"),
    ("T17", "P3", "CoVe级联事实核查", "node"),
    ("T18", "P3", "偏见检测+风格检查", "node"),
    ("T19", "P3", "交付守卫", "node"),
    ("T19b", "P3", "处方门控", "node"),

    # ===== Phase 4 — 输出渲染与交付层 (6 nodes) =====
    ("T20a", "P4", "深度研究报告渲染", "node"),
    ("T20b", "P4", "公众号文章渲染", "node"),
    ("T20c", "P4", "课程材料渲染", "node"),
    ("T20_output_guard", "P4", "输出卫士", "node"),
    ("T20d_cross_media_review", "P4", "跨媒介审查", "node"),
    ("T21", "P4", "知识回收", "node"),

    # ===== Phase 5 — 元维度引擎 + 科学层 (20 nodes，含 TM06b) =====
    ("T22", "P7", "NRSF叙事综合（全息框架3部分）", "node"),
    ("T23", "P7", "全息框架第一部分-问题认知与定义（4维度）", "node"),
    ("T24", "P7", "全息框架第二部分-全维全域分析（8维度）", "node"),
    ("T25", "P7", "全息框架第三部分-极限决策推理（2维度）", "node"),
    ("T26", "P7", "跨维度洞察抽取（14维交叉）", "node"),
    ("T27", "P7", "14维度关系可视化（3种图表）", "node"),
    ("T28", "P7", "Gate-终 最终质量门控", "gate"),
    ("T_philosophical_core", "P7", "哲学三元组审查（本体论/认识论/价值论）", "node"),
    ("T_meta_dim_9_10", "P7", "元维度9-10：无知之学+认知神经心理学", "node"),
    ("T_meta_dim_11_12", "P7", "元维度11-12：二阶方法论+深度时间思维", "node"),
    ("T_meta_dim_13_14", "P7", "元维度13-14：悲剧性智慧+知识生命体化", "node"),
    ("TM01", "P7", "系统动力学仿真与反馈回路建模", "node"),
    ("TM02", "P7", "因果验证与反事实推断", "node"),
    ("TM03", "P7", "多智能体对抗性综合", "node"),
    ("TM04", "P7", "情景规划与不确定性景观", "node"),
    ("TM05", "P7", "元认知反思与认知边界", "node"),
    ("TM06", "P7", "14维+元维度扩展验证", "node"),
    ("TM06b", "P7", "Lean4 形式化验证（v6.0 新增）", "node"),
    ("TM07", "P7", "知识图谱本体导出", "node"),
    ("T_gate_delta", "P7", "Gate-δ 科学层门控", "gate"),
]

# 交付前硬门控 G1-G6（不属于 DAG 节点，单独列出用于可视化）
HARD_GATES = [
    ("G1", "字数下限校验（≥10万字）"),
    ("G2", "14维覆盖完整性校验"),
    ("G3", "科学层8模块落地校验（含 Lean4 形式化验证）"),
    ("G4", "哲学三元组存在性校验"),
    ("G5", "引用与事实可溯源校验"),
    ("G6", "EXHAUST穷尽性终审校验"),
]

# 阶段名称映射
STAGE_NAMES = {
    "P1": "Phase 1：研究底座层（15节点）",
    "P2": "Phase 2：认知流水线层（9节点）",
    "P3": "Phase 3：领域分析与质量保障层（8节点）",
    "P4": "Phase 4：输出渲染与交付层（6节点）",
    "P7": "Phase 5：元维度引擎+科学层（20节点，含 TM06b）",
}

# DAG 边定义（关键依赖关系，用于 Mermaid 图）
DAG_EDGES = [
    # Phase 1
    ("T_env_probe", "T00a"),
    ("T_env_probe", "T01"),
    ("T01", "T01b"),
    ("T01b", "T01d"),
    ("T01b", "T00"),
    ("T00a", "T00"),
    ("T00", "T00b"),
    ("T00", "T02"),
    ("T02", "T03"),
    ("T03", "T03b"),
    ("T03b", "T04"),
    ("T02", "T04"),
    ("T04", "T05"),
    ("T05", "T06"),
    ("T06", "T07"),
    ("T07", "T07b"),
    # Phase 2
    ("T07", "T08"),
    ("T08", "T09"),
    ("T09", "T10"),
    ("T09", "T11"),
    ("T09", "T12"),
    ("T10", "T12b"),
    ("T11", "T12b"),
    ("T12", "T12b"),
    ("T12b", "T13"),
    ("T13", "I01"),
    ("I01", "T14"),
    ("T13", "T14"),
    # Phase 3
    ("T14", "T15"),
    ("T15", "T15b"),
    ("T15b", "T16"),
    ("T15", "T16"),
    ("T13", "T13b"),
    ("T15b", "T13b"),
    ("T16", "T17"),
    ("T16", "T18"),
    ("T17", "T19"),
    ("T18", "T19"),
    ("T19", "T19b"),
    # Phase 5（T22 依赖多个 Phase 2/3 节点）
    ("T13", "T22"),
    ("T13b", "T22"),
    ("T14", "T22"),
    ("T15", "T22"),
    ("T15b", "T22"),
    ("T16", "T22"),
    ("T19", "T22"),
    ("T22", "T23"),
    ("T23", "T24"),
    ("T24", "T25"),
    ("T25", "T26"),
    ("T26", "T27"),
    ("T27", "T28"),
    ("T28", "T_philosophical_core"),
    ("T28", "T_meta_dim_9_10"),
    ("T28", "T_meta_dim_11_12"),
    ("T28", "T_meta_dim_13_14"),
    ("T28", "TM01"),
    ("TM01", "TM02"),
    ("TM02", "TM03"),
    ("TM03", "TM04"),
    ("TM04", "TM05"),
    ("TM05", "TM06"),
    ("TM06", "TM06b"),
    ("TM06", "TM07"),
    ("TM06b", "T_gate_delta"),
    ("TM07", "T_gate_delta"),
    ("T_philosophical_core", "T_gate_delta"),
    ("T_meta_dim_9_10", "T_gate_delta"),
    ("T_meta_dim_11_12", "T_gate_delta"),
    ("T_meta_dim_13_14", "T_gate_delta"),
    # Phase 4（渲染依赖 Phase 5 产出）
    ("T_gate_delta", "T20a"),
    ("T19b", "T20a"),
    ("T19", "T20a"),
    ("T01b", "T20a"),
    ("T01b", "T20b"),
    ("T19b", "T20b"),
    ("T19", "T20b"),
    ("T01b", "T20c"),
    ("T19", "T20c"),
    ("T20a", "T20_output_guard"),
    ("T20b", "T20_output_guard"),
    ("T20c", "T20_output_guard"),
    ("T20_output_guard", "T20d_cross_media_review"),
    ("T20_output_guard", "T21"),
]


def generate_mermaid_dag():
    """生成 Mermaid DAG 拓扑图"""
    lines = [
        "```mermaid",
        "graph TD",
        "    %% Profound Cognition 58-Node DAG Topology v6.0.0",
        "    %% 生成时间: {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        "",
        "    %% ===== 节点定义 =====",
    ]

    # 按阶段分组定义节点
    current_stage = None
    for node_id, stage, desc, node_type in DAG_NODES:
        if stage != current_stage:
            current_stage = stage
            stage_name = STAGE_NAMES.get(stage, stage)
            lines.append("    %% --- {} ---".format(stage_name))

        # 节点形状按类型区分
        if node_type == "gate":
            shape_open, shape_close = "{{", "}}"
        elif node_type == "hard_gate":
            shape_open, shape_close = "[[", "]]"
        else:
            shape_open, shape_close = "[", "]"

        # Mermaid 节点 ID 不能含特殊字符，做映射
        safe_id = node_id.replace("_", "_")
        lines.append('    {}{}"{}"{}'.format(safe_id, shape_open, desc, shape_close))

    lines.append("")
    lines.append("    %% ===== 边定义（关键依赖） =====")

    for src, dst in DAG_EDGES:
        safe_src = src.replace("_", "_")
        safe_dst = dst.replace("_", "_")
        lines.append("    {} --> {}".format(safe_src, safe_dst))

    # 并行节点标注
    lines.append("")
    lines.append("    %% ===== 并行节点标注 =====")
    lines.append("    %% T10/T11/T12 三路对抗并行")
    lines.append("    %% T17/T18 事实核查与偏见检测并行")

    # 样式
    lines.append("")
    lines.append("    %% ===== 样式 =====")
    lines.append("    classDef gate fill:#f9f,stroke:#333,stroke-width:2px;")
    lines.append("    classDef hardgate fill:#fdd,stroke:#c00,stroke-width:3px;")
    lines.append("    classDef normal fill:#dfd,stroke:#333,stroke-width:1px;")

    # 应用样式
    gate_ids = []
    hard_gate_ids = []
    node_ids = []
    for node_id, stage, desc, node_type in DAG_NODES:
        safe_id = node_id.replace("_", "_")
        if node_type == "gate":
            gate_ids.append(safe_id)
        elif node_type == "hard_gate":
            hard_gate_ids.append(safe_id)
        else:
            node_ids.append(safe_id)

    if gate_ids:
        lines.append("    class {} gate;".format(",".join(gate_ids)))
    if hard_gate_ids:
        lines.append("    class {} hardgate;".format(",".join(hard_gate_ids)))
    if node_ids:
        lines.append("    class {} normal;".format(",".join(node_ids)))

    lines.append("```")
    return "\n".join(lines)


def generate_timeline_md():
    """生成执行时间线 Markdown 卡片"""
    lines = [
        "# Profound Cognition 执行时间线",
        "",
        "> Demo Prompt: `{}`".format(DEMO_PROMPT),
        "> 版本: {}".format(VERSION),
        "> 生成时间: {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        "",
        "## DAG 节点执行序列（58 节点全量激活）",
        "",
        "| 序号 | 节点ID | 阶段 | 中文名称 | 类型 |",
        "|------|--------|------|----------|------|",
    ]

    for idx, (node_id, stage, desc, node_type) in enumerate(DAG_NODES, 1):
        stage_name = STAGE_NAMES.get(stage, stage)
        type_label = {
            "node": "⚪ 节点",
            "gate": "🟪 Gate",
            "hard_gate": "🟥 硬门控",
        }.get(node_type, node_type)
        lines.append("| {} | `{}` | {} | {} | {} |".format(
            idx, node_id, stage_name, desc, type_label
        ))

    # 统计
    node_count = sum(1 for _, _, _, t in DAG_NODES if t == "node")
    gate_count = sum(1 for _, _, _, t in DAG_NODES if t == "gate")
    hard_gate_count = len(HARD_GATES)
    total = len(DAG_NODES)

    lines.extend([
        "",
        "## 统计摘要",
        "",
        "| 指标 | 数值 |",
        "|------|------|",
        "| DAG 节点总数 | {} |".format(total),
        "| 普通节点 | {} |".format(node_count),
        "| Gate 门控 | {} |".format(gate_count),
        "| 硬门控 G1-G6 | {} |".format(hard_gate_count),
        "| DAG 边数 | {} |".format(len(DAG_EDGES)),
        "| Phase 数 | {} |".format(len(STAGE_NAMES)),
        "",
        "## 并行执行点",
        "",
        "1. **T10/T11/T12** — 三路对抗验证（逻辑攻击/证据攻击/范围攻击）同时启动",
        "2. **T17/T18** — 事实核查与偏见检测并行执行",
        "3. **T_philosophical_core / T_meta_dim_9_10 / T_meta_dim_11_12 / T_meta_dim_13_14 / TM01** — Gate-终后并行启动",
        "",
        "## 五道 Gate 门控",
        "",
        "| Gate | 节点 | 检查内容 |",
        "|------|------|----------|",
        "| Gate-α | T07 | 研究底座九层覆盖完整性 |",
        "| Gate-β | T14 | 认知深度与收敛性 |",
        "| Gate-γ | T16 | 领域适配与知识注入 |",
        "| Gate-终 | T28 | 全息框架14维完整性终审 |",
        "| Gate-δ | T_gate_delta | 哲学三元组与元维度门控 |",
        "",
        "## 交付前硬门控 G1-G6",
        "",
        "| 硬门控 | 检查内容 |",
        "|--------|----------|",
    ])

    for gate_id, gate_desc in HARD_GATES:
        lines.append("| {} | {} |".format(gate_id, gate_desc))

    lines.append("")

    return "\n".join(lines)


def generate_summary_json():
    """生成执行摘要 JSON"""
    node_count = sum(1 for _, _, _, t in DAG_NODES if t == "node")
    gate_count = sum(1 for _, _, _, t in DAG_NODES if t == "gate")
    hard_gate_count = len(HARD_GATES)

    summary = {
        "skill_name": SKILL_NAME,
        "version": VERSION,
        "demo_prompt": DEMO_PROMPT,
        "generated_at": datetime.now().isoformat(),
        "topology": {
            "dag_nodes_total": len(DAG_NODES),
            "normal_nodes": node_count,
            "gate_nodes": gate_count,
            "hard_gates": hard_gate_count,
            "edges": len(DAG_EDGES),
            "phases": len(STAGE_NAMES),
            "phase_distribution": {
                "P1": sum(1 for _, p, _, _ in DAG_NODES if p == "P1"),
                "P2": sum(1 for _, p, _, _ in DAG_NODES if p == "P2"),
                "P3": sum(1 for _, p, _, _ in DAG_NODES if p == "P3"),
                "P4": sum(1 for _, p, _, _ in DAG_NODES if p == "P4"),
                "P7": sum(1 for _, p, _, _ in DAG_NODES if p == "P7"),
            },
        },
        "gates": [
            {"name": "Gate-α", "node": "T07", "check": "研究底座九层覆盖完整性"},
            {"name": "Gate-β", "node": "T14", "check": "认知深度与收敛性"},
            {"name": "Gate-γ", "node": "T16", "check": "领域适配与知识注入"},
            {"name": "Gate-终", "node": "T28", "check": "全息框架14维完整性终审"},
            {"name": "Gate-δ", "node": "T_gate_delta", "check": "哲学三元组与元维度门控"},
        ],
        "hard_gates": [
            {"name": gate_id, "check": gate_desc}
            for gate_id, gate_desc in HARD_GATES
        ],
        "parallel_points": [
            {"nodes": ["T10", "T11", "T12"], "desc": "三路对抗验证（逻辑攻击/证据攻击/范围攻击）"},
            {"nodes": ["T17", "T18"], "desc": "事实核查与偏见检测"},
            {"nodes": ["T_philosophical_core", "T_meta_dim_9_10", "T_meta_dim_11_12", "T_meta_dim_13_14", "TM01"], "desc": "Gate-终后并行启动（哲学核心+元维度+科学层M1）"},
        ],
        "nodes": [
            {
                "id": node_id,
                "phase": stage,
                "phase_name": STAGE_NAMES.get(stage, stage),
                "description": desc,
                "type": node_type,
            }
            for node_id, stage, desc, node_type in DAG_NODES
        ],
        "edges": [
            {"source": src, "target": dst}
            for src, dst in DAG_EDGES
        ],
    }
    return json.dumps(summary, ensure_ascii=False, indent=2)


def main():
    print("=" * 60)
    print("Profound Cognition Demo Visualizer v{}".format(VERSION))
    print("=" * 60)
    print()

    # 产物路径
    mermaid_path = ASSETS_DIR / "dag-topology.mmd"
    timeline_path = ASSETS_DIR / "execution-timeline.md"
    json_path = ASSETS_DIR / "demo-summary.json"

    # 生成 Mermaid DAG 图
    print("[1/3] 生成 Mermaid DAG 拓扑图...")
    mermaid_content = generate_mermaid_dag()
    mermaid_path.write_text(mermaid_content, encoding="utf-8")
    print("      -> {}".format(mermaid_path))

    # 生成时间线 Markdown
    print("[2/3] 生成执行时间线 Markdown...")
    timeline_content = generate_timeline_md()
    timeline_path.write_text(timeline_content, encoding="utf-8")
    print("      -> {}".format(timeline_path))

    # 生成摘要 JSON
    print("[3/3] 生成执行摘要 JSON...")
    json_content = generate_summary_json()
    json_path.write_text(json_content, encoding="utf-8")
    print("      -> {}".format(json_path))

    # 统计
    node_count = sum(1 for _, _, _, t in DAG_NODES if t == "node")
    gate_count = sum(1 for _, _, _, t in DAG_NODES if t == "gate")
    hard_gate_count = len(HARD_GATES)

    print()
    print("=" * 60)
    print("可视化产物生成完成")
    print("=" * 60)
    print("Mermaid DAG 图    : {}".format(mermaid_path))
    print("执行时间线 MD     : {}".format(timeline_path))
    print("执行摘要 JSON     : {}".format(json_path))
    print("-" * 60)
    print("DAG 节点总数      : {}".format(len(DAG_NODES)))
    print("  普通节点        : {}".format(node_count))
    print("  Gate 门控       : {}".format(gate_count))
    print("  硬门控 G1-G6    : {}".format(hard_gate_count))
    print("DAG 边数          : {}".format(len(DAG_EDGES)))
    print("Phase 数          : {}".format(len(STAGE_NAMES)))
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
