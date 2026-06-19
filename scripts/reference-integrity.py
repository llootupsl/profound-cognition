#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 作者：阿洋
"""reference-integrity.py — Profound Cognition v5.1.0 参考完整性校验脚本

校验项目:
  1. DAG 节点名 = 文件名 = deps 引用三者一致
  2. 孤儿任务文件（在 tasks/ 中但不在 DAG 中）
  3. 零引用能力卡片（在 external-capabilities/ 中但无 DAG 节点引用）
  4. Supervisor check 文件与任务文件一一对应
  5. T20x token 预算与目标长度一致性验证

用法: python scripts/reference-integrity.py
退出码: 0=全部通过, 1=有异常
"""

import os
import re
import sys
from pathlib import Path

# 跨平台 UTF-8 输出兼容（修复 Windows GBK 编码崩溃）
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Windows 控制台 UTF-8 代码页设置（修复 PowerShell 管道中文乱码）
if sys.platform == "win32":
    import ctypes
    try:
        ctypes.windll.kernel32.SetConsoleOutputCP(65001)
        ctypes.windll.kernel32.SetConsoleCP(65001)
    except Exception:
        pass

PROJECT_ROOT = Path(__file__).parent.parent
V2_DIR = PROJECT_ROOT
TASKS_DIR = V2_DIR / "tasks"
CHECKS_DIR = V2_DIR / "supervisors" / "checks"
CAPABILITIES_DIR = V2_DIR / "knowledge" / "external-capabilities"
SKILL_MD = V2_DIR / "SKILL.md"


def parse_file_index(skill_md_path):
    """从 SKILL.md 的文件索引表中解析 node_id → task_file_stem 映射"""
    mapping = {}
    if not skill_md_path.exists():
        return mapping

    content = skill_md_path.read_text(encoding="utf-8")

    # Match lines like: | `tasks/T00_outline.md` | 研究大纲生成 ...
    pattern = re.compile(
        r'\|\s*`tasks/(?P<file>[^`]+\.md)`\s*\|',
        re.MULTILINE
    )

    for match in pattern.finditer(content):
        filename = match.group("file")
        stem = filename.replace(".md", "")
        mapping[stem] = stem

    return mapping


def parse_dag_nodes(skill_md_path):
    """从 SKILL.md 中解析 DAG 节点定义，返回 {node_name: {deps, file_stem, ...}}"""
    nodes = {}
    if not skill_md_path.exists():
        print(f"[ERROR] SKILL.md not found: {skill_md_path}")
        return nodes

    content = skill_md_path.read_text(encoding="utf-8")

    # Parse node blocks from the YAML DAG definition.
    # Each node block starts with "- node_id:" and contains "dependencies:".
    node_blocks = re.split(r'\n\s*(?=- node_id:)', content)

    for block in node_blocks:
        node_match = re.search(r'node_id:\s*"?(?P<id>\S+?)"?(?:\s|$)', block)
        if not node_match:
            continue
        node_id = node_match.group("id")

        deps_match = re.search(r'dependencies:\s*\[([^\]]*)\]', block)
        deps = []
        if deps_match:
            deps_raw = deps_match.group(1).strip()
            if deps_raw:
                deps = [d.strip().strip('"') for d in deps_raw.split(",") if d.strip()]

        nodes[node_id] = {"deps": deps}

        tok_match = re.search(r'tok:\s*(?P<tok>\d+)', block)
        if tok_match:
            nodes[node_id]["tok"] = int(tok_match.group("tok"))

    # Build file index mapping and attach to nodes
    file_index = parse_file_index(skill_md_path)

    # For each node, try to find its task file in the index
    for node_id in nodes:
        # 1) 精确匹配
        if node_id in file_index:
            nodes[node_id]["file_stem"] = node_id
            continue
        # 2) "node_id_" / "node_id." 前缀匹配（优先，避免 T00 误配 T00a_time_anchor）
        found = None
        for stem in file_index:
            if stem.startswith(node_id + "_") or stem.startswith(node_id + "."):
                found = stem
                break
        # 3) 仅当前缀无果时，再退化到 node_id 子串匹配（处理 node_id 较短的命名）
        if not found:
            for stem in file_index:
                if node_id in stem and stem.startswith(node_id[0]):
                    found = stem
                    break
        nodes[node_id]["file_stem"] = found

    return nodes


def check_dag_file_consistency(nodes):
    """校验 1: DAG 节点名 = deps 引用 = 任务文件名 三者一致"""
    errors = []
    task_files = {f.stem: f for f in TASKS_DIR.glob("*.md")} if TASKS_DIR.exists() else {}

    for node_id, info in nodes.items():
        file_stem = info.get("file_stem", "")

        # Check file exists
        if file_stem and file_stem not in task_files:
            errors.append(f"节点 {node_id} 引用的文件 tasks/{file_stem}.md 不存在")
        elif not file_stem:
            errors.append(f"节点 {node_id} 在文件索引中未找到对应的任务文件")

        # Check deps reference valid nodes
        deps = info.get("deps", [])
        for dep in deps:
            if dep not in nodes:
                errors.append(f"节点 {node_id} 的依赖 {dep} 不在 DAG 中")

    return errors


def check_orphan_tasks(nodes):
    """校验 2: 扫描 tasks/ 中的孤儿文件"""
    errors = []
    if not TASKS_DIR.exists():
        return errors

    dag_files = set()
    for info in nodes.values():
        file_stem = info.get("file_stem", "")
        if file_stem:
            dag_files.add(file_stem)

    for task_file in TASKS_DIR.glob("*.md"):
        if task_file.stem not in dag_files:
            errors.append(f"孤儿任务文件: tasks/{task_file.name}（不在 DAG 中）")

    return errors


def check_zero_ref_capabilities(nodes):
    """校验 3: 零引用能力卡片扫描

    仅当卡片在全部项目文件中均未被引用时才报告。
    引用方式包括：frontmatter integrated_nodes、consuming_engines、
    消费此卡片的 DAG 节点/领域引擎 章节、以及简单名称引用。

    注意：能力卡片作为框架的储备能力库，零引用不代表错误——
    仅当卡片在 external-capabilities-index.md 中也未被索引时才报告。
    """
    errors = []
    if not CAPABILITIES_DIR.exists():
        return errors

    # 读取能力卡片索引文件
    index_path = V2_DIR / "knowledge" / "external-capabilities-index.md"
    index_content = ""
    if index_path.exists():
        index_content = index_path.read_text(encoding="utf-8")

    # 收集所有项目文件内容
    all_content = ""
    for task_file in TASKS_DIR.glob("*.md"):
        all_content += task_file.read_text(encoding="utf-8") + "\n"

    knowledge_dir = V2_DIR / "knowledge"
    if knowledge_dir.exists():
        for md_file in knowledge_dir.rglob("*.md"):
            all_content += md_file.read_text(encoding="utf-8") + "\n"

    if SKILL_MD.exists():
        all_content += SKILL_MD.read_text(encoding="utf-8") + "\n"
    protocols_dir = V2_DIR / "protocols"
    if protocols_dir.exists():
        for proto_file in protocols_dir.glob("*.md"):
            all_content += proto_file.read_text(encoding="utf-8") + "\n"

    for card_file in CAPABILITIES_DIR.glob("*.md"):
        card_name = card_file.stem
        card_content = card_file.read_text(encoding="utf-8")

        has_consumers = False

        # 方式 1: YAML frontmatter
        fm_match = re.match(r'^---\s*\n(.*?)\n---', card_content, re.DOTALL)
        if fm_match:
            fm = fm_match.group(1)
            if re.search(r'integrated_nodes:\s*\[.*\S.*\]', fm):
                has_consumers = True
            if re.search(r'consuming_engines:\s*\[.*\S.*\]', fm):
                has_consumers = True

        # 方式 2: markdown 章节
        if not has_consumers:
            if re.search(r'消费此卡片的\s*DAG\s*节点', card_content):
                dag_section = re.search(
                    r'消费此卡片的\s*DAG\s*节点.*?\n(.*?)(?=\n##|\n---|\Z)',
                    card_content, re.DOTALL
                )
                if dag_section:
                    body = dag_section.group(1)
                    data_rows = [l for l in body.split('\n') if l.strip().startswith('|') and not l.strip().startswith('|---') and not l.strip().startswith('|--') and '节点' not in l and '---' not in l]
                    if data_rows:
                        has_consumers = True

        if not has_consumers:
            if re.search(r'消费此卡片的\s*领域引擎', card_content):
                eng_section = re.search(
                    r'消费此卡片的\s*领域引擎.*?\n(.*?)(?=\n##|\n---|\Z)',
                    card_content, re.DOTALL
                )
                if eng_section:
                    body = eng_section.group(1)
                    data_rows = [l for l in body.split('\n') if l.strip().startswith('|') and not l.strip().startswith('|---') and not l.strip().startswith('|--') and '引擎' not in l and '---' not in l]
                    if data_rows:
                        has_consumers = True

        # 方式 3: 在项目文件中按名称引用
        if not has_consumers:
            if card_name in all_content:
                has_consumers = True

        # 方式 4: 在能力卡片索引中被收录（检查卡片编号前缀）
        if not has_consumers:
            if card_name in index_content:
                has_consumers = True
            else:
                # 尝试匹配卡片编号前缀（如 LC-018-ECharts → LC-018）
                prefix_match = re.match(r'^([A-Z]+-\d+)', card_name)
                if prefix_match:
                    prefix = prefix_match.group(1)
                    if prefix in index_content:
                        has_consumers = True

        if not has_consumers:
            errors.append(f"零引用能力卡片: {card_file.name}")

    return errors


def check_supervisor_task_pairs(nodes):
    """校验 4: Supervisor check 文件与任务文件一一对应"""
    errors = []
    if not CHECKS_DIR.exists():
        return errors

    # Non-task supervisor check files (legitimate exceptions)
    NON_TASK_CHECKS = {"persona-check", "checkpoint"}

    task_nodes = set(nodes.keys())

    for f in CHECKS_DIR.glob("*.yml"):
        stem = f.stem
        if stem in NON_TASK_CHECKS or stem.replace("_check", "") in NON_TASK_CHECKS:
            continue

        # Try to match check file to a DAG node.
        # Strategy 1: Remove _check suffix and check if result is a DAG node.
        # Strategy 2: Check if stem starts with a known DAG node ID.
        # Strategy 3: Check if any DAG node ID starts with the stem (after _check removal).
        base = stem
        if base.endswith("_check"):
            base = base[:-len("_check")]

        matched = False

        # Direct match
        if base in task_nodes:
            matched = True

        # Check if stem starts with a known DAG node ID
        if not matched:
            for node_id in sorted(task_nodes, key=len, reverse=True):
                if stem.startswith(node_id + "_") or stem == node_id:
                    matched = True
                    break

        # Check if any DAG node ID starts with the base
        if not matched:
            for node_id in task_nodes:
                if node_id.startswith(base) or base.startswith(node_id):
                    matched = True
                    break

        if not matched:
            errors.append(f"Supervisor check {f.name} 对应的任务节点不存在（推断节点: {base}）")

    return errors


def check_dead_code(nodes):
    """校验 6: 死代码扫描 — 未被任何引用链可达的文件

    扫描范围：
      - tasks/ 中的孤儿文件（已在 check_orphan_tasks 中覆盖）
      - knowledge/external-capabilities/ 中的零引用卡片（已在 check_zero_ref_capabilities 中覆盖）
      - protocols/ 中未被引用的协议
      - supervisors/ 中未被引用的监督器
      - tests/ 中未被引用的测试文件
      - knowledge/ 中未被引用的知识文件

    引用判定：文件在 SKILL.md 或任何任务文件中被引用（名称或路径）即视为已引用。
    """
    errors = []
    all_content = ""

    # 收集所有任务文件内容
    if TASKS_DIR.exists():
        for task_file in TASKS_DIR.glob("*.md"):
            all_content += task_file.read_text(encoding="utf-8") + "\n"

    # 收集 SKILL.md 内容
    if SKILL_MD.exists():
        all_content += SKILL_MD.read_text(encoding="utf-8") + "\n"

    # 收集所有 protocol 文件内容（协议间可能互相引用）
    protocols_dir = V2_DIR / "protocols"
    if protocols_dir.exists():
        for proto_file in protocols_dir.glob("*.md"):
            all_content += proto_file.read_text(encoding="utf-8") + "\n"

    def is_referenced(file_stem, file_relpath):
        """检查文件是否在项目中被引用"""
        # 直接名称匹配
        if file_stem in all_content:
            return True
        # 相对路径匹配
        if file_relpath in all_content:
            return True
        # 文件名匹配（含扩展名）
        if file_stem + ".md" in all_content or file_stem + ".yml" in all_content:
            return True
        # 父目录匹配（如 knowledge/domains/ 目录级引用）
        parent_dir = "/".join(file_relpath.split("/")[:-1]) + "/"
        if parent_dir in all_content:
            return True
        return False

    # 扫描 protocols/ 目录
    if protocols_dir.exists():
        for proto_file in protocols_dir.glob("*.md"):
            if not is_referenced(proto_file.stem, f"protocols/{proto_file.name}"):
                errors.append(f"死代码 - 协议文件未被引用: protocols/{proto_file.name}")

    # 扫描 supervisors/ 目录（非 check 文件）
    supervisors_dir = V2_DIR / "supervisors"
    if supervisors_dir.exists():
        for sup_file in supervisors_dir.rglob("*.md"):
            if "checks" in sup_file.parts:
                continue
            rel = str(sup_file.relative_to(V2_DIR)).replace("\\", "/")
            if not is_referenced(sup_file.stem, rel):
                errors.append(f"死代码 - 监督器文件未被引用: {rel}")

    # 扫描 knowledge/ 目录（排除 external-capabilities/，由 check_zero_ref_capabilities 处理）
    # 也排除 tool-availability/（工具可用性验证文件，属于基础设施）
    knowledge_dir = V2_DIR / "knowledge"
    if knowledge_dir.exists():
        for kn_file in knowledge_dir.rglob("*.md"):
            if "external-capabilities" in kn_file.parts:
                continue
            if "tool-availability" in kn_file.parts:
                continue
            rel = str(kn_file.relative_to(V2_DIR)).replace("\\", "/")
            if not is_referenced(kn_file.stem, rel):
                errors.append(f"死代码 - 知识文件未被引用: {rel}")

    # 扫描 tests/ 目录（测试基础设施，不纳入死代码检测）
    # 测试文件属于开发/QA 基础设施，不需要在任务文件或 SKILL.md 中被显式引用
    tests_dir = V2_DIR / "tests"
    # 跳过 tests/ 目录的死代码扫描

    return errors


def check_t20_token_budgets(nodes):
    """校验 5: T20x token 预算与目标长度一致性验证"""
    errors = []

    # T20x 节点的预算约束（来自 SKILL.md DAG）。
    # T20a 为长文渲染节点：token 不设上限（tok=null），正文长度由 min_length 约束。
    T20_NODES = {
        "T20a": {"uncapped": True, "min_length": 100000, "label": "深度研究报告渲染"},
        "T20b": {"min_tok": 8000, "label": "公众号文章渲染"},
        "T20c": {"min_tok": 12800, "label": "课程材料渲染"},
        "T20_output_guard": {"min_tok": 200, "label": "输出卫士"},
        "T20d_cross_media_review": {"min_tok": 150, "label": "跨媒介审查"},
    }

    # Parse task file metadata tok values
    task_file_toks = {}
    if TASKS_DIR.exists():
        for task_file in TASKS_DIR.glob("*.md"):
            content = task_file.read_text(encoding="utf-8")
            # Match DAG metadata lines like: tok=6000 or tok=8000
            tok_match = re.search(r'tok[=:]\s*(\d+)', content)
            if tok_match:
                task_file_toks[task_file.stem] = int(tok_match.group(1))

    for node_id, config in T20_NODES.items():
        label = config["label"]

        if node_id not in nodes:
            errors.append(f"T20x 节点 {node_id} ({label}) 不在 DAG 中")
            continue

        file_stem = nodes[node_id].get("file_stem", "")

        # 不设 token 上限的长文渲染节点：跳过 token 下限校验，改为校验 min_length
        if config.get("uncapped"):
            min_length = config["min_length"]
            ml_ok = False
            if TASKS_DIR.exists() and file_stem:
                tf = TASKS_DIR / f"{file_stem}.md"
                if tf.exists():
                    m = re.search(r'min_length:\s*(\d+)', tf.read_text(encoding="utf-8"))
                    if m and int(m.group(1)) >= min_length:
                        ml_ok = True
            if not ml_ok:
                errors.append(
                    f"节点 {node_id} ({label}) 未声明 min_length ≥ {min_length}"
                    f"（不设 token 上限的长文渲染节点须以 min_length 约束正文长度）"
                )
            continue

        min_tok = config["min_tok"]

        # Check 1: DAG tok field exists and meets minimum
        dag_tok = nodes[node_id].get("tok", 0)
        if dag_tok < min_tok:
            errors.append(
                f"节点 {node_id} ({label}) DAG tok={dag_tok} 低于最低要求 {min_tok}"
            )

        # Check 2: Task file tok matches DAG tok
        if file_stem and file_stem in task_file_toks:
            file_tok = task_file_toks[file_stem]
            if file_tok != dag_tok:
                errors.append(
                    f"节点 {node_id} ({label}) DAG tok={dag_tok} 与任务文件 "
                    f"tasks/{file_stem}.md tok={file_tok} 不一致"
                )
        elif file_stem and file_stem not in task_file_toks:
            errors.append(
                f"节点 {node_id} ({label}) 任务文件 tasks/{file_stem}.md 中未找到 tok 声明"
            )

    return errors


def main():
    print("=" * 60)
    print("Profound Cognition v5.1.0 — 参考完整性校验")
    print("=" * 60)

    nodes = parse_dag_nodes(SKILL_MD)
    print(f"\n[DAG] 解析到 {len(nodes)} 个节点")

    all_errors = []

    print("\n[校验 1] DAG 节点名 = 文件名 = deps 引用一致...")
    errors = check_dag_file_consistency(nodes)
    all_errors.extend(errors)
    if errors:
        for e in errors:
            print(f"  ✗ {e}")
    else:
        print("  ✓ 全部通过")

    print("\n[校验 2] 孤儿任务文件扫描...")
    errors = check_orphan_tasks(nodes)
    all_errors.extend(errors)
    if errors:
        for e in errors:
            print(f"  ✗ {e}")
    else:
        print("  ✓ 全部通过")

    print("\n[校验 3] 零引用能力卡片扫描...")
    errors = check_zero_ref_capabilities(nodes)
    all_errors.extend(errors)
    if errors:
        for e in errors:
            print(f"  ✗ {e}")
    else:
        print("  ✓ 全部通过")

    print("\n[校验 4] Supervisor check 与任务文件对应...")
    errors = check_supervisor_task_pairs(nodes)
    all_errors.extend(errors)
    if errors:
        for e in errors:
            print(f"  ✗ {e}")
    else:
        print("  ✓ 全部通过")

    print("\n[校验 5] T20x token 预算与目标长度一致性...")
    errors = check_t20_token_budgets(nodes)
    all_errors.extend(errors)
    if errors:
        for e in errors:
            print(f"  ✗ {e}")
    else:
        print("  ✓ 全部通过")

    print("\n[校验 6] 死代码扫描...")
    errors = check_dead_code(nodes)
    all_errors.extend(errors)
    if errors:
        for e in errors:
            print(f"  ✗ {e}")
    else:
        print("  ✓ 全部通过")

    print("\n" + "=" * 60)
    if all_errors:
        print(f"校验失败: {len(all_errors)} 个问题")
        sys.exit(1)
    else:
        print("全部校验通过 ✓")
        sys.exit(0)


if __name__ == "__main__":
    main()