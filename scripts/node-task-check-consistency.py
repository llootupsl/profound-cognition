#!/usr/bin/env python3
# 作者：阿洋
"""node-task-check-consistency.py — 节点-任务-检查三方一致性校验（D1.4.1）

校验 SKILL.md DAG 拓扑中的节点、tasks/ 目录下的任务文件、supervisors/checks/ 下的
检查 YAML 三方一致性，防止新增/删除节点时遗漏任务文件或检查文件。

校验项:
  P0 (CRITICAL): DAG 节点在 tasks/ 下无对应任务文件
  P1 (WARNING):  DAG 节点在 supervisors/checks/ 下无对应检查 YAML
  P2 (INFO):     tasks/ 或 checks/ 中存在孤儿文件（不对应任何 DAG 节点）

用法: python scripts/node-task-check-consistency.py
退出码: 0=全部通过, 1=存在 P0 或 P1 不一致
"""

import re
import sys
from pathlib import Path

# 跨平台 UTF-8 输出兼容（修复 Windows GBK 编码崩溃）
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Windows 控制台 UTF-8 代码页设置
if sys.platform == "win32":
    import ctypes
    try:
        ctypes.windll.kernel32.SetConsoleOutputCP(65001)
        ctypes.windll.kernel32.SetConsoleCP(65001)
    except Exception:
        pass

PROJECT_ROOT = Path(__file__).parent.parent
SKILL_MD = PROJECT_ROOT / "SKILL.md"
TASKS_DIR = PROJECT_ROOT / "tasks"
CHECKS_DIR = PROJECT_ROOT / "supervisors" / "checks"

# 已知的检查文件缩写名别名（node_id → 缩写 check 文件名）
# 当检查文件使用缩写名而非完整 node_id 时，通过此映射匹配
CHECK_ALIASES = {
    "T20d_cross_media_review": "T20d_check.yml",
    "T20_output_guard": "T20_check.yml",
}


def parse_dag_nodes(skill_md_path):
    """从 SKILL.md 的 DAG 拓扑 YAML 块中解析全部 node_id。

    DAG YAML 块位于 ```yaml ... ``` 之间，以 `dag_topology:` 开头。
    每个节点以 `- node_id: "XXX"` 形式声明。
    """
    if not skill_md_path.exists():
        return []

    content = skill_md_path.read_text(encoding="utf-8")

    # 定位 DAG YAML 块（```yaml ... ```）
    yaml_blocks = re.findall(
        r'```yaml\n(.*?)```', content, re.DOTALL
    )

    node_ids = []
    for block in yaml_blocks:
        # 只处理包含 dag_topology 的块
        if 'dag_topology' not in block:
            continue
        # 匹配 - node_id: "XXX" 或 - node_id:       "XXX"
        matches = re.findall(
            r'-\s*node_id:\s+"([^"]+)"', block
        )
        node_ids.extend(matches)

    return node_ids


def find_task_file(node_id, task_files):
    """查找节点对应的任务文件。

    匹配规则:
      - 文件名 == {node_id}.md
      - 文件名以 {node_id}_ 开头（如 T01_input_triage.md）
    """
    for f in task_files:
        name = f.name
        if name == f"{node_id}.md":
            return f
        if name.startswith(f"{node_id}_") and name.endswith(".md"):
            return f
    return None


def find_check_file(node_id, check_files):
    """查找节点对应的检查 YAML。

    匹配规则（按优先级）:
      1. 别名映射（CHECK_ALIASES）——处理已知的缩写名
      2. 文件名 == {node_id}_check.yml
      3. 文件名以 {node_id}_ 开头且以 _check.yml 结尾
        （如 T19b_prescription_gate_check.yml, T20a_research_render_check.yml）
    """
    # 1. 别名映射
    alias = CHECK_ALIASES.get(node_id)
    if alias:
        for f in check_files:
            if f.name == alias:
                return f
    # 2-3. 常规匹配
    for f in check_files:
        name = f.name
        if name == f"{node_id}_check.yml":
            return f
        if name.startswith(f"{node_id}_") and name.endswith("_check.yml"):
            return f
    return None


def find_orphan_task_files(node_ids, task_files):
    """查找 tasks/ 中的孤儿文件（不对应任何 DAG 节点）。"""
    orphans = []
    for f in task_files:
        name = f.name
        if not name.endswith(".md"):
            continue
        matched = False
        for node_id in node_ids:
            if name == f"{node_id}.md" or name.startswith(f"{node_id}_"):
                matched = True
                break
        if not matched:
            orphans.append(f)
    return orphans


def find_orphan_check_files(node_ids, check_files):
    """查找 checks/ 中的孤儿文件（不对应任何 DAG 节点）。"""
    orphans = []
    # 排除非节点级检查文件（如 checkpoint_check.yml, persona-check.yml）
    NON_NODE_CHECKS = {"checkpoint_check.yml", "persona-check.yml"}
    # 收集所有别名文件名，这些文件已通过别名映射匹配到节点
    aliased_names = set(CHECK_ALIASES.values())
    for f in check_files:
        name = f.name
        if name in NON_NODE_CHECKS:
            continue
        if name in aliased_names:
            continue
        if not name.endswith("_check.yml"):
            continue
        # 去掉 _check.yml 后缀得到 base name
        base = name[:-len("_check.yml")]
        matched = False
        for node_id in node_ids:
            if base == node_id or base.startswith(f"{node_id}_"):
                matched = True
                break
        if not matched:
            orphans.append(f)
    return orphans


def main():
    errors = []
    warnings = []
    info_items = []

    # 解析 DAG 节点
    node_ids = parse_dag_nodes(SKILL_MD)
    if not node_ids:
        errors.append(
            "无法从 SKILL.md 解析 DAG 节点。请检查 SKILL.md 中 dag_topology YAML 块是否存在。"
        )
        print("FAIL: 无法解析 DAG 节点")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    # 加载任务文件和检查文件
    task_files = sorted(TASKS_DIR.glob("*.md")) if TASKS_DIR.exists() else []
    check_files = sorted(CHECKS_DIR.glob("*.yml")) if CHECKS_DIR.exists() else []

    # P0: 节点无任务文件
    nodes_without_task = []
    for node_id in node_ids:
        task_file = find_task_file(node_id, task_files)
        if task_file is None:
            nodes_without_task.append(node_id)

    if nodes_without_task:
        for nid in nodes_without_task:
            errors.append(
                f"[P0] 节点 {nid} 在 tasks/ 下无对应任务文件"
            )

    # P1: 节点无检查 YAML
    nodes_without_check = []
    for node_id in node_ids:
        check_file = find_check_file(node_id, check_files)
        if check_file is None:
            nodes_without_check.append(node_id)

    if nodes_without_check:
        for nid in nodes_without_check:
            warnings.append(
                f"[P1] 节点 {nid} 在 supervisors/checks/ 下无对应检查 YAML"
            )

    # P2: 孤儿文件
    orphan_tasks = find_orphan_task_files(node_ids, task_files)
    orphan_checks = find_orphan_check_files(node_ids, check_files)

    for f in orphan_tasks:
        info_items.append(
            f"[P2] tasks/ 中存在孤儿文件: {f.name}（不对应任何 DAG 节点）"
        )
    for f in orphan_checks:
        info_items.append(
            f"[P2] supervisors/checks/ 中存在孤儿文件: {f.name}（不对应任何 DAG 节点）"
        )

    # 输出
    print("=" * 60)
    print("节点-任务-检查三方一致性校验（D1.4.1）")
    print("=" * 60)
    print(f"  DAG 节点数:          {len(node_ids)}")
    print(f"  tasks/ 文件数:       {len(task_files)}")
    print(f"  supervisors/checks/ 文件数: {len(check_files)}")
    print(f"  P0 节点无任务文件:   {len(nodes_without_task)}")
    print(f"  P1 节点无检查 YAML:  {len(nodes_without_check)}")
    print(f"  P2 孤儿任务文件:     {len(orphan_tasks)}")
    print(f"  P2 孤儿检查文件:     {len(orphan_checks)}")

    if errors:
        print("\n--- P0 CRITICAL ---")
        for e in errors:
            print(f"  ✗ {e}")

    if warnings:
        print("\n--- P1 WARNING ---")
        for w in warnings:
            print(f"  ⚠ {w}")

    if info_items:
        print("\n--- P2 INFO ---")
        for i in info_items:
            print(f"  ℹ {i}")

    # 退出码判定：P0 或 P1 存在则退出码 1
    if errors or warnings:
        print(f"\nFAIL: 存在 {len(errors)} 个 P0 问题, {len(warnings)} 个 P1 问题")
        sys.exit(1)

    print("\n全部校验通过 ✓")
    sys.exit(0)


if __name__ == "__main__":
    main()
