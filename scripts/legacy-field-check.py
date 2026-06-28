#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 作者：阿洋
"""legacy-field-check.py — LEGACY 字段名残留扫描脚本

扫描全项目所有 .md/.yml/.yaml/.json/.py 文件，检测 LEGACY A-J 字段别名
（A_core_identity, B_communication_style, ... J_self_deprecation_style）
以及 'ABCDEFGHIJ' 迭代模式的残留引用。

v6.0 Stage 0 Task 0.5 已将所有 LEGACY 字段名替换为语义化字段名
（identity, communication_style, knowledge_zones, core_values, catchphrase,
emotional_baseline, reader_name, style_ref, emotion_expression, self_deprecation）。
本脚本确保后续不会再引入 LEGACY 字段名。

排除规则（不视为违规）：
  - 本脚本自身（scripts/legacy-field-check.py）
  - CHANGELOG.md（记录历史变更，引用旧名是合法的）
  - 处于"已移除/已替换/已废弃/已弃用"等否定/历史上下文中的引用

用法: python scripts/legacy-field-check.py
退出码: 0=无残留, 1=有残留
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

# 扫描的文件扩展名
SCAN_EXTENSIONS = {".md", ".yml", ".yaml", ".json", ".py"}

# 排除的目录（不扫描）
EXCLUDE_DIRS = {
    ".git",
    ".github",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "build",
    "dist",
}

# LEGACY 字段名 -> 语义化字段名映射
LEGACY_FIELD_MAP = {
    "A_core_identity": "identity",
    "B_communication_style": "communication_style",
    "C_expertise_domains": "knowledge_zones",
    "D_value_stance": "core_values",
    "E_signature_phrases": "catchphrase",
    "F_emotional_baseline": "emotional_baseline",
    "G_audience_distance": "reader_name",
    "H_narrative_preference": "style_ref",
    "I_emotional_expressions": "emotion_expression",
    "J_self_deprecation_style": "self_deprecation",
}

# 'ABCDEFGHIJ' 迭代模式（用于 validation 表达式中遍历 10 个字段）
LEGACY_ITERATION_PATTERN = re.compile(r"""['"]ABCDEFGHIJ['"]""")

# 否定/历史上下文标记（出现这些标记的行不视为违规）
# 这些标记表示该行是在描述"已移除/已替换"的历史变更，而非使用 LEGACY 字段名
ALLOWED_CONTEXT_MARKERS = [
    "已移除",
    "已替换",
    "已废弃",
    "已弃用",
    "已删除",
    "已重命名",
    "移除",
    "替换",
    "废弃",
    "弃用",
    "删除",
    "重命名",
    "→",
    "改为",
    "原",
    "旧",
    "LEGACY",
    "legacy",
    "BREAKING",
    "破坏性变更",
    "Stage 0",
    "Task 0.5",
]


def is_in_allowed_context(line_content):
    """检查行是否处于允许的上下文中（历史变更说明/否定表述）。

    当行中包含"已移除""已替换""→"等标记时，说明是在描述 LEGACY 字段名
    的移除/替换历史，而非实际使用，因此不视为违规。
    """
    for marker in ALLOWED_CONTEXT_MARKERS:
        if marker in line_content:
            return True
    return False


def scan_file(file_path):
    """扫描单个文件，返回违规列表。

    返回: [(line_number, term, line_content), ...]
    """
    violations = []
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception:
        # 编码错误等，跳过该文件
        return violations

    lines = content.split("\n")

    for line_idx, line in enumerate(lines, start=1):
        # 检查是否处于允许的上下文中（历史变更说明）
        if is_in_allowed_context(line):
            continue

        # 检查 LEGACY 字段名
        for legacy_name in LEGACY_FIELD_MAP:
            if legacy_name in line:
                violations.append((line_idx, legacy_name, line.rstrip()))

        # 检查 'ABCDEFGHIJ' 迭代模式
        if LEGACY_ITERATION_PATTERN.search(line):
            violations.append((line_idx, "'ABCDEFGHIJ'", line.rstrip()))

    return violations


def should_scan_file(file_path):
    """判断文件是否应被扫描。"""
    # 检查扩展名
    if file_path.suffix.lower() not in SCAN_EXTENSIONS:
        return False

    # 检查是否在排除目录中
    try:
        rel = file_path.relative_to(PROJECT_ROOT)
    except ValueError:
        return False

    parts = rel.parts
    for part in parts:
        if part in EXCLUDE_DIRS:
            return False

    # 排除本脚本自身
    if file_path.name == "legacy-field-check.py" and "scripts" in parts:
        return False

    # 排除 CHANGELOG.md（记录历史变更，引用旧名是合法的）
    if file_path.name == "CHANGELOG.md" and file_path.parent == PROJECT_ROOT:
        return False

    return True


def collect_files():
    """收集所有需要扫描的文件。"""
    files = []
    for root, dirs, filenames in os.walk(PROJECT_ROOT):
        # 过滤排除目录
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for filename in filenames:
            file_path = Path(root) / filename
            if should_scan_file(file_path):
                files.append(file_path)
    return files


def main():
    print("=" * 60)
    print("Profound Cognition — LEGACY 字段名残留扫描")
    print("=" * 60)

    if not PROJECT_ROOT.exists():
        print(f"[ERROR] 项目根目录不存在: {PROJECT_ROOT}")
        sys.exit(2)

    files = collect_files()
    print(f"\n[扫描] 共发现 {len(files)} 个待扫描文件")

    all_violations = []
    files_with_violations = 0

    for file_path in files:
        try:
            rel_path = file_path.relative_to(PROJECT_ROOT)
        except ValueError:
            rel_path = file_path

        violations = scan_file(file_path)
        if violations:
            files_with_violations += 1
            all_violations.append((rel_path, violations))

    print(f"\n[结果] 扫描完成")
    print(f"  扫描文件数: {len(files)}")
    print(f"  违规文件数: {files_with_violations}")
    total_violations = sum(len(v) for _, v in all_violations)
    print(f"  违规总数: {total_violations}")

    if all_violations:
        print("\n" + "-" * 60)
        print("违规详情:")
        print("-" * 60)
        for rel_path, violations in all_violations:
            print(f"\n📄 {rel_path}")
            for v in violations:
                line_no, term, line_content = v
                display_line = line_content.strip()
                if len(display_line) > 120:
                    display_line = display_line[:117] + "..."
                semantic_name = LEGACY_FIELD_MAP.get(term, "?")
                hint = f"（应替换为: {semantic_name}）" if semantic_name != "?" else ""
                print(f"  L{line_no} [{term}]{hint}: {display_line}")

        print("\n" + "=" * 60)
        print(f"❌ 扫描未通过: {total_violations} 处 LEGACY 字段名残留")
        print("=" * 60)
        sys.exit(1)
    else:
        print("\n" + "=" * 60)
        print("✅ 扫描通过: 无 LEGACY 字段名残留")
        print("=" * 60)
        sys.exit(0)


if __name__ == "__main__":
    main()
