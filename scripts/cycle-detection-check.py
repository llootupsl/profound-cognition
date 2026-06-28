#!/usr/bin/env python3
# 作者：阿洋
"""cycle-detection-check.py — DAG 拓扑环检测脚本（R1-04）

解析 SKILL.md 的 DAG 拓扑定义（58 节点），使用 Kahn's algorithm（拓扑排序）
检测是否存在环。

检测逻辑：
  1. 从 SKILL.md 解析全部节点及其 dependencies
  2. 构建邻接表（dependency → node 的有向图）
  3. Kahn's algorithm：入度为 0 的节点入队，逐步移除并减少后继入度
     - 全部节点处理完毕 → 无环，退出码 0
     - 仍有节点未处理 → 存在环，用 DFS 定位环路径并打印，退出码 1

与 execution-protocol.md §3.5「运行时循环检测」配合：
  - 本脚本（编译期）：CI 流水线中检测静态拓扑环
  - LangGraph（运行期）：递归上限 + 状态指纹检测动态执行环

用法: python scripts/cycle-detection-check.py
退出码: 0=无环, 1=有环或解析错误
"""

import re
import sys
from collections import deque
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
SKILL_MD = PROJECT_ROOT / "SKILL.md"


def parse_dag_nodes(skill_md_path):
    """从 SKILL.md 解析 DAG 节点定义，返回 {node_id: [dep_id, ...]}

    解析逻辑与 reference-integrity.py 的 parse_dag_nodes 一致：
    按 "- node_id:" 分割块，正则提取 node_id 和 dependencies。
    """
    if not skill_md_path.exists():
        print(f"[ERROR] SKILL.md not found: {skill_md_path}")
        return {}

    content = skill_md_path.read_text(encoding="utf-8")

    # 仅在 DAG 拓扑 YAML 块内解析（避免误匹配其他章节）
    # DAG 拓扑块以 "## DAG 拓扑" 开头，到下一个 "## " 或 "### " 结束
    dag_section_match = re.search(
        r'## DAG 拓扑.*?\n(.*?)(?=\n## |\n### |\Z)',
        content,
        re.DOTALL,
    )
    if not dag_section_match:
        print("[ERROR] 未在 SKILL.md 中找到「DAG 拓扑」章节")
        return {}

    dag_content = dag_section_match.group(1)

    nodes = {}

    # 按 "- node_id:" 分割节点块
    node_blocks = re.split(r'\n\s*(?=- node_id:)', dag_content)

    for block in node_blocks:
        node_match = re.search(r'node_id:\s*"?(?P<id>\S+?)"?(?:\s|$)', block)
        if not node_match:
            continue
        node_id = node_match.group("id")

        deps = []
        deps_match = re.search(r'dependencies:\s*\[([^\]]*)\]', block)
        if deps_match:
            deps_raw = deps_match.group(1).strip()
            if deps_raw:
                deps = [d.strip().strip('"') for d in deps_raw.split(",") if d.strip()]

        nodes[node_id] = deps

    return nodes


def kahn_topological_sort(nodes):
    """Kahn's algorithm 拓扑排序。

    Args:
        nodes: {node_id: [dep_id, ...]}

    Returns:
        (sorted_order, remaining_nodes):
          - sorted_order: 拓扑排序结果（无环时包含全部节点）
          - remaining_nodes: 未处理的节点集合（非空则存在环）
    """
    # 构建邻接表和入度表
    # 边方向：dependency → node（dependency 完成后才能执行 node）
    adj = {node_id: [] for node_id in nodes}
    in_degree = {node_id: 0 for node_id in nodes}

    for node_id, deps in nodes.items():
        for dep in deps:
            if dep in adj:
                adj[dep].append(node_id)
                in_degree[node_id] += 1
            else:
                print(f"[WARN] 节点 {node_id} 的依赖 {dep} 不在 DAG 节点集中，已跳过")

    # 入度为 0 的节点入队
    queue = deque([node_id for node_id, deg in in_degree.items() if deg == 0])
    sorted_order = []

    while queue:
        current = queue.popleft()
        sorted_order.append(current)
        for successor in adj[current]:
            in_degree[successor] -= 1
            if in_degree[successor] == 0:
                queue.append(successor)

    remaining_nodes = {node_id for node_id in nodes if node_id not in sorted_order}
    return sorted_order, remaining_nodes


def find_cycle_path(nodes, remaining_nodes):
    """用 DFS（三色标记法）在剩余节点中定位环路径。

    Args:
        nodes: {node_id: [dep_id, ...]}
        remaining_nodes: Kahn's algorithm 未处理的节点集合

    Returns:
        环路径列表（如 [A, B, C, A]），未找到则返回空列表
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {node_id: WHITE for node_id in remaining_nodes}
    parent = {}

    def dfs(node_id):
        color[node_id] = GRAY
        for dep in nodes.get(node_id, []):
            if dep not in remaining_nodes:
                continue
            if color[dep] == WHITE:
                parent[dep] = node_id
                result = dfs(dep)
                if result:
                    return result
            elif color[dep] == GRAY:
                # 找到环：从 dep 到 node_id 回溯
                cycle = [dep, node_id]
                current = node_id
                while current != dep and current in parent:
                    current = parent[current]
                    cycle.append(current)
                cycle.reverse()
                cycle.append(cycle[0])  # 闭合环
                return cycle
        color[node_id] = BLACK
        return None

    for node_id in remaining_nodes:
        if color[node_id] == WHITE:
            result = dfs(node_id)
            if result:
                return result

    return []


def main():
    print("=" * 60)
    print("DAG 拓扑环检测（Kahn's algorithm）— R1-04")
    print("=" * 60)

    # Step 1: 解析 SKILL.md DAG 拓扑
    nodes = parse_dag_nodes(SKILL_MD)
    if not nodes:
        print("[ERROR] 未能从 SKILL.md 解析出任何 DAG 节点")
        sys.exit(1)

    print(f"\n[1] 解析 DAG 拓扑: {len(nodes)} 个节点")
    for node_id, deps in nodes.items():
        dep_str = ", ".join(deps) if deps else "(无依赖)"
        print(f"    {node_id}: deps=[{dep_str}]")

    # Step 2: Kahn's algorithm 拓扑排序
    print(f"\n[2] 执行 Kahn's algorithm 拓扑排序...")
    sorted_order, remaining_nodes = kahn_topological_sort(nodes)

    print(f"    已排序节点数: {len(sorted_order)}")
    print(f"    剩余未排序节点数: {len(remaining_nodes)}")

    # Step 3: 判定是否有环
    if not remaining_nodes:
        print(f"\n[3] ✓ 无环检测通过 — 全部 {len(nodes)} 个节点完成拓扑排序")
        print(f"    拓扑序: {' → '.join(sorted_order)}")
        print("\n" + "=" * 60)
        print("结果: PASS (无环)")
        print("=" * 60)
        sys.exit(0)
    else:
        print(f"\n[3] ✗ 检测到环 — {len(remaining_nodes)} 个节点无法排序:")
        for node_id in remaining_nodes:
            print(f"    {node_id}")

        # 定位环路径
        cycle_path = find_cycle_path(nodes, remaining_nodes)
        if cycle_path:
            print(f"\n    环路径: {' → '.join(cycle_path)}")
        else:
            print("\n    [WARN] 未能定位具体环路径（可能存在自引用或复杂环）")

        print("\n" + "=" * 60)
        print("结果: FAIL (存在环)")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
