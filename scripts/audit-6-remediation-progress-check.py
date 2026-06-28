#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 作者：阿洋
"""audit-6-remediation-progress-check.py — Audit-6 Wave 5 修复进度检查脚本

检查 docs/audit-logs/Audit-6-remediation-log.md 中记录的修复项进度，
确保 P0 修复全部完成、P1 修复按计划推进，无遗漏或状态不一致。

检查内容：
  1. 解析修复日志中所有修复项（P0-x / P1-x / P2-x / P3-x）
  2. 统计各优先级的总数与已完成数
  3. 验证 P0 修复项全部为 ✅ 已执行（阻塞项）
  4. 输出进度报告

退出码:
  0 = P0 全部完成（P1/P2/P3 可有进行中项）
  1 = P0 存在未完成项（阻塞 v6.0.1 发布）
  2 = 解析错误或文件缺失

用法: python scripts/audit-6-remediation-progress-check.py
"""

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
REMEDIATION_LOG = PROJECT_ROOT / "docs" / "audit-logs" / "Audit-6-remediation-log.md"

# 修复项 ID 正则：匹配 #### P0-1, #### P1-7, #### P2-3 等
ITEM_PATTERN = re.compile(r"^####\s+(P[0-3])-(\d+)", re.MULTILINE)
# 修复状态正则：匹配 - **修复状态**：✅ 已执行 / ⏳ 待执行
STATUS_PATTERN = re.compile(r"\*\*修复状态\*\*[：:]\s*(✅\s*已执行|⏳\s*待执行|⏳\s*进行中)")


def parse_remediation_items(content):
    """解析修复日志，提取所有修复项及其状态。

    Args:
        content: 修复日志文件内容

    Returns:
        list of (priority, number, status) tuples
    """
    items = []
    # 按 #### 分割章节
    sections = re.split(r"(?=^####\s+P[0-3]-\d+)", content, flags=re.MULTILINE)

    for section in sections:
        header_match = ITEM_PATTERN.search(section)
        if not header_match:
            continue
        priority = header_match.group(1)
        number = int(header_match.group(2))

        status_match = STATUS_PATTERN.search(section)
        if status_match:
            status_raw = status_match.group(1)
            if status_raw.startswith("✅"):
                status = "done"
            else:
                status = "pending"
        else:
            status = "unknown"

        items.append((priority, number, status))

    return items


def main():
    print("=" * 60)
    print("Profound Cognition — Audit-6 Wave 5 修复进度检查")
    print("=" * 60)

    # 检查修复日志文件存在
    if not REMEDIATION_LOG.exists():
        print(f"\n❌ 错误: 修复日志文件不存在: {REMEDIATION_LOG}")
        print("=" * 60)
        sys.exit(2)

    print(f"\n[文件] {REMEDIATION_LOG.relative_to(PROJECT_ROOT)}")

    # 读取修复日志
    try:
        content = REMEDIATION_LOG.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        print(f"\n❌ 错误: 读取修复日志失败: {e}")
        print("=" * 60)
        sys.exit(2)

    # 解析修复项
    items = parse_remediation_items(content)

    if not items:
        print("\n❌ 错误: 未解析到任何修复项（P0/P1/P2/P3）")
        print("=" * 60)
        sys.exit(2)

    print(f"\n[解析] 共发现 {len(items)} 个修复项")

    # 按优先级分组统计
    priority_stats = {}
    for priority in ("P0", "P1", "P2", "P3"):
        priority_items = [(num, st) for p, num, st in items if p == priority]
        total = len(priority_items)
        done = sum(1 for _, st in priority_items if st == "done")
        pending = sum(1 for _, st in priority_items if st == "pending")
        unknown = sum(1 for _, st in priority_items if st == "unknown")
        priority_stats[priority] = {
            "total": total,
            "done": done,
            "pending": pending,
            "unknown": unknown,
            "items": priority_items,
        }

    # 输出统计
    print("\n[进度统计]")
    print("-" * 60)
    print(f"{'优先级':<10} {'总数':<8} {'已完成':<10} {'待执行':<10} {'未知':<8}")
    print("-" * 60)

    for priority in ("P0", "P1", "P2", "P3"):
        stats = priority_stats[priority]
        print(f"{priority:<10} {stats['total']:<8} {stats['done']:<10} {stats['pending']:<10} {stats['unknown']:<8}")

    print("-" * 60)

    total_items = len(items)
    total_done = sum(s["done"] for s in priority_stats.values())
    total_pending = sum(s["pending"] for s in priority_stats.values())
    print(f"{'合计':<10} {total_items:<8} {total_done:<10} {total_pending:<10}")

    # 列出待执行项
    pending_items = []
    for priority in ("P0", "P1", "P2", "P3"):
        for num, st in priority_stats[priority]["items"]:
            if st != "done":
                pending_items.append(f"{priority}-{num}")

    if pending_items:
        print(f"\n[待执行项] ({len(pending_items)} 项)")
        for item in pending_items:
            print(f"  ⏳ {item}")
    else:
        print("\n[待执行项] 无 — 全部完成")

    # 退出码判定
    # P0 阻塞项：必须全部完成
    p0_stats = priority_stats["P0"]
    print("\n" + "=" * 60)
    if p0_stats["total"] == 0:
        print("⚠ 警告: 未发现 P0 修复项（可能解析失败）")
        print("=" * 60)
        sys.exit(2)

    if p0_stats["pending"] > 0 or p0_stats["unknown"] > 0:
        pending_p0 = [
            f"P0-{num}" for num, st in p0_stats["items"] if st != "done"
        ]
        print(f"❌ 检查失败: P0 仍有 {len(pending_p0)} 项未完成")
        print(f"   未完成项: {pending_p0}")
        print("   P0 为阻塞项，必须全部完成后方可发布 v6.0.1")
        print("=" * 60)
        sys.exit(1)
    else:
        print(f"✅ 检查通过: P0 修复全部完成（{p0_stats['done']}/{p0_stats['total']}）")
        p1_stats = priority_stats["P1"]
        if p1_stats["total"] > 0:
            if p1_stats["pending"] > 0:
                print(f"   ⚠ P1 进度: {p1_stats['done']}/{p1_stats['total']}（{p1_stats['pending']} 项进行中）")
            else:
                print(f"   ✅ P1 进度: {p1_stats['done']}/{p1_stats['total']}（全部完成）")
        print("=" * 60)
        sys.exit(0)


if __name__ == "__main__":
    main()
