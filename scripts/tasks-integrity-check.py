#!/usr/bin/env python3
# 作者：阿洋
"""tasks-integrity-check.py — tasks/ 目录健康检查

防止 tasks/ 目录被误删或精简安装时分发不完整导致的静默失败。
本脚本是鲁班慢刨阶段沉淀的验证资产（对应 SKILL.md §0.1 A 节点执行契约）。

校验项:
  1. tasks/ 目录存在
  2. tasks/ 下 .md 文件数量 ≥ 58（DAG 节点数，含 TM06b）
  3. SKILL.md 文件索引表中声明的每个 tasks/{node_id}.md 都真实存在
  4. tasks/ 中无孤儿文件（在 tasks/ 但不在 SKILL.md 索引中）

用法: python scripts/tasks-integrity-check.py
退出码: 0=全部通过, 1=有异常
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
TASKS_DIR = PROJECT_ROOT / "tasks"
SKILL_MD = PROJECT_ROOT / "SKILL.md"

EXPECTED_MIN_TASK_FILES = 58


def parse_skill_md_task_index(skill_md_path):
    """从 SKILL.md 的文件索引表中解析所有声明的 tasks/*.md 文件名

    只匹配真实文件名（形如 tasks/T01_xxx.md），排除说明性文字中的
    通配符引用（如 tasks/*.md、tasks/{node_id}.md）。
    """
    if not skill_md_path.exists():
        return set()

    content = skill_md_path.read_text(encoding="utf-8")
    # 只匹配反引号包裹的、不含通配符的真实文件路径
    pattern = re.compile(r'`tasks/(?P<file>[A-Za-z0-9_\-]+\.md)`')
    return {m.group("file") for m in pattern.finditer(content)}


def main():
    errors = []
    warnings = []

    # 校验 1: tasks/ 目录存在
    if not TASKS_DIR.exists():
        errors.append(
            "tasks/ 目录不存在。SKILL.md §0.1 A 节点执行契约要求：若 tasks/ 缺失，"
            "必须按自足契约就地执行——但 tasks/ 缺失本身是分发缺陷，应修复。"
        )
        print("FAIL: tasks/ 目录不存在")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    # 校验 2: 文件数量
    task_files = sorted(TASKS_DIR.glob("*.md"))
    actual_count = len(task_files)
    if actual_count < EXPECTED_MIN_TASK_FILES:
        errors.append(
            f"tasks/ 下 .md 文件数量 {actual_count} < 预期最小值 {EXPECTED_MIN_TASK_FILES}。"
            f"可能存在文件丢失或精简分发。"
        )
    elif actual_count > EXPECTED_MIN_TASK_FILES:
        warnings.append(
            f"tasks/ 下 .md 文件数量 {actual_count} > 预期 {EXPECTED_MIN_TASK_FILES}，"
            f"请确认是否新增节点未同步更新 EXPECTED_MIN_TASK_FILES。"
        )

    # 校验 3: SKILL.md 声明的文件都存在
    declared_files = parse_skill_md_task_index(SKILL_MD)
    actual_filenames = {f.name for f in task_files}
    missing = declared_files - actual_filenames
    if missing:
        errors.append(
            f"SKILL.md 文件索引声明了 {len(missing)} 个不存在的 tasks/ 文件: "
            f"{sorted(missing)}"
        )

    # 校验 4: 孤儿文件
    orphans = actual_filenames - declared_files
    if orphans:
        warnings.append(
            f"tasks/ 中有 {len(orphans)} 个孤儿文件（不在 SKILL.md 索引中）: "
            f"{sorted(orphans)}"
        )

    # 输出
    print(f"tasks/ 目录健康检查:")
    print(f"  目录存在: ✓")
    print(f"  .md 文件数: {actual_count} (预期最小 {EXPECTED_MIN_TASK_FILES})")
    print(f"  SKILL.md 声明文件数: {len(declared_files)}")
    print(f"  缺失文件: {len(missing)}")
    print(f"  孤儿文件: {len(orphans)}")

    if warnings:
        print("\nWARNINGS:")
        for w in warnings:
            print(f"  ⚠ {w}")

    if errors:
        print("\nFAIL:")
        for e in errors:
            print(f"  ✗ {e}")
        sys.exit(1)

    print("\n全部校验通过 ✓")
    sys.exit(0)


if __name__ == "__main__":
    main()
