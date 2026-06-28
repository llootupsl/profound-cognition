#!/usr/bin/env python3
# 作者：阿洋
"""protocol-deps-check.py — 协议依赖图检查（D1.4.2/D3.4.1）

解析 protocols/ 下所有协议文件的依赖关系，检测：
  1. 循环依赖（非设计性双向引用）
  2. 孤立协议（无被引用也无引用其他）

设计性双向引用（如 execution ↔ handoff）通过白名单豁免，不视为循环依赖。

用法: python scripts/protocol-deps-check.py
退出码: 0=全部通过（孤立协议为 WARNING 不阻塞）, 1=检测到循环依赖
"""

import re
import sys
from collections import defaultdict
from pathlib import Path

# 跨平台 UTF-8 输出兼容
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

if sys.platform == "win32":
    import ctypes
    try:
        ctypes.windll.kernel32.SetConsoleOutputCP(65001)
        ctypes.windll.kernel32.SetConsoleCP(65001)
    except Exception:
        pass

PROJECT_ROOT = Path(__file__).parent.parent
PROTOCOLS_DIR = PROJECT_ROOT / "protocols"

# 设计性双向引用白名单（不视为循环依赖）
# 每个元组表示一对允许的双向引用 (A, B)
# 当循环中包含至少一条白名单边时，整个循环被视为设计意图，不报错
BIDIRECTIONAL_WHITELIST = {
    ("execution-protocol", "handoff-protocol"),
    ("output-expansion-protocol", "write-while-research-protocol"),
    ("checkpoint-protocol", "context-budget-protocol"),
    ("output-rendering-protocol", "illustration-generation-protocol"),
    # v6.0 审计补充：以下双向引用为设计性紧耦合，职责边界声明互相引用
    ("checkpoint-protocol", "cross-session-memory-protocol"),
    ("nrsf-protocol", "output-expansion-protocol"),
}

# 设计性多节点循环白名单（以 frozenset 表示循环涉及的节点集合）
# 这些循环是核心协议间紧耦合的设计意图，非有害循环依赖
CYCLE_WHITELIST = {
    frozenset({"handoff-protocol", "nrsf-protocol", "output-rendering-protocol"}),
}


def parse_protocol_dependencies(protocol_path):
    """解析单个协议文件中对其他协议的依赖引用。

    匹配模式:
      - [xxx-protocol.md](./xxx-protocol.md)  — Markdown 链接
      - ./xxx-protocol.md                      — 直接路径引用
      - xxx-protocol.md                        — 在 knowledge_refs 等列表中
    """
    content = protocol_path.read_text(encoding="utf-8")
    # 匹配所有 xxx-protocol.md 引用（不含路径前缀）
    pattern = re.compile(r'([a-z][a-z0-9-]*-protocol)\.md')
    matches = set(pattern.findall(content))
    # 排除自身
    self_name = protocol_path.stem  # 如 "nrsf-protocol"
    matches.discard(self_name)
    return matches


def build_dependency_graph():
    """构建协议依赖图。

    Returns:
        protocols: set of all protocol names
        deps: dict {protocol_name: set of dependency names}
    """
    protocols = set()
    deps = defaultdict(set)

    if not PROTOCOLS_DIR.exists():
        return protocols, deps

    for f in sorted(PROTOCOLS_DIR.glob("*.md")):
        # 仅扫描文件名以 -protocol.md 结尾的文件，跳过 output-schema-spec.md 等规范类文件。
        # 注意：protocol-version-check.py 扫描所有 *.md 文件（22 个），本脚本仅扫描 -protocol.md（21 个），
        # 因此两脚本协议计数差 1。这是设计上的有意取舍——
        # protocol-version-check.py 关注"版本号一致性"（所有规范文件都应有版本号），
        # 本脚本关注"协议间依赖关系"（仅 -protocol.md 文件有 deps 字段，规范类文件无 deps）。
        # 详见 Audit-6 F9 修复记录。
        if not f.name.endswith("-protocol.md"):
            continue
        name = f.stem  # 如 "nrsf-protocol"
        protocols.add(name)
        dep_names = parse_protocol_dependencies(f)
        # 只保留存在的协议
        deps[name] = dep_names

    return protocols, deps


def _is_whitelisted_edge(src, dst):
    """检查一条边是否为白名单双向引用。"""
    return (
        (src, dst) in BIDIRECTIONAL_WHITELIST
        or (dst, src) in BIDIRECTIONAL_WHITELIST
    )


def detect_cycles(protocols, deps):
    """检测循环依赖（使用 DFS 三色标记法）。

    白名单中的双向引用不视为循环依赖。当循环中包含至少一条白名单边时，
    整个循环被视为设计意图，不报错。
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {p: WHITE for p in protocols}
    cycles = []

    def dfs(node, path):
        color[node] = GRAY
        path.append(node)
        for neighbor in sorted(deps.get(node, [])):
            if neighbor not in protocols:
                continue
            if color[neighbor] == WHITE:
                dfs(neighbor, path)
            elif color[neighbor] == GRAY:
                # 发现循环
                cycle_start = path.index(neighbor)
                cycle = path[cycle_start:] + [neighbor]
                # 检查循环中是否包含白名单边
                has_whitelisted = False
                for i in range(len(cycle) - 1):
                    if _is_whitelisted_edge(cycle[i], cycle[i + 1]):
                        has_whitelisted = True
                        break
                if has_whitelisted:
                    continue
                # 检查是否为白名单多节点循环
                cycle_nodes = frozenset(cycle)
                if cycle_nodes in CYCLE_WHITELIST:
                    continue
                cycles.append(cycle)
        path.pop()
        color[node] = BLACK

    for p in sorted(protocols):
        if color[p] == WHITE:
            dfs(p, [])

    return cycles


def detect_orphans(protocols, deps):
    """检测孤立协议（无被引用也无引用其他）。"""
    # 收集所有被引用的协议
    referenced = set()
    for dep_set in deps.values():
        referenced.update(dep_set)

    orphans = []
    for p in sorted(protocols):
        has_outgoing = len(deps.get(p, set())) > 0
        has_incoming = p in referenced
        if not has_outgoing and not has_incoming:
            orphans.append(p)
    return orphans


def main():
    errors = []
    warnings = []

    protocols, deps = build_dependency_graph()

    if not protocols:
        errors.append("protocols/ 目录不存在或无协议文件")
        print("FAIL: 无协议文件")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    # 检测循环依赖
    cycles = detect_cycles(protocols, deps)
    for cycle in cycles:
        errors.append(
            f"检测到循环依赖: {' → '.join(cycle)}"
        )

    # 检测孤立协议
    orphans = detect_orphans(protocols, deps)
    for orphan in orphans:
        warnings.append(
            f"孤立协议: {orphan}（无被引用也无引用其他协议）"
        )

    # 输出
    print("=" * 60)
    print("协议依赖图检查（D1.4.2/D3.4.1）")
    print("=" * 60)
    print(f"  协议总数:       {len(protocols)}")
    print(f"  依赖关系数:     {sum(len(v) for v in deps.values())}")
    print(f"  循环依赖数:     {len(cycles)}")
    print(f"  孤立协议数:     {len(orphans)}")
    print(f"  白名单双向引用: {len(BIDIRECTIONAL_WHITELIST)} 对")

    # 打印依赖关系
    print("\n--- 依赖关系 ---")
    for p in sorted(protocols):
        dep_list = sorted(deps.get(p, set()))
        if dep_list:
            print(f"  {p} → {', '.join(dep_list)}")
        else:
            print(f"  {p} → (无)")

    if warnings:
        print("\n--- WARNINGS ---")
        for w in warnings:
            print(f"  ⚠ {w}")

    if errors:
        print("\n--- ERRORS ---")
        for e in errors:
            print(f"  ✗ {e}")

    # 退出码判定：循环依赖 → 退出码 1；孤立协议 → 仅警告，不阻塞
    if errors:
        print(f"\nFAIL: 检测到 {len(errors)} 个循环依赖")
        sys.exit(1)

    if warnings:
        print(f"\nPASS (with {len(warnings)} warnings)")

    print("\n全部校验通过 ✓")
    sys.exit(0)


if __name__ == "__main__":
    main()
