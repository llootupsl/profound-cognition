#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
脚本名称: encoding-compatibility-check.py
用途: 检查所有 Python 脚本是否包含跨平台 UTF-8 输出兼容代码
作者: 阿洋
版本: 5.1.0
日期: 2026-06-17
================================================================================
背景：Windows 上 Python 3 默认 stdout 编码为 GBK，无法编码 Unicode 符号
      （如 ✓ ✅ ✗），导致脚本崩溃 UnicodeEncodeError。
      本脚本扫描仓库内所有 .py 文件，检查是否包含 UTF-8 reconfigure 代码。

检查规则：
  1. 扫描 scripts/ 和 assets/ 目录下所有 .py 文件
  2. 每个文件必须包含 sys.stdout.reconfigure 调用
  3. 排除本脚本自身（检查器不需要检查自己）

退出码：
  0 = 全部通过
  1 = 有文件缺少 UTF-8 兼容代码
================================================================================
"""

import os
import re
import sys
from pathlib import Path

# ----------------------------------------------------------------------------
# 跨平台 UTF-8 输出兼容（修复 Windows GBK 编码崩溃）
# ----------------------------------------------------------------------------
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

# ----------------------------------------------------------------------------
# 配置
# ----------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent

# 需要检查的目录（相对于 skill 根目录）
CHECK_DIRS = ["scripts", "assets"]

# 排除的文件名（自身）
EXCLUDE_FILES = {"encoding-compatibility-check.py"}

# 检查模式：sys.stdout.reconfigure
RECONFIGURE_PATTERN = re.compile(
    r"sys\.stdout\.reconfigure\s*\(\s*encoding\s*=\s*[\"']utf-8[\"']",
    re.IGNORECASE,
)


def find_python_files():
    """查找需要检查的 Python 文件"""
    py_files = []
    for check_dir_name in CHECK_DIRS:
        check_dir = SKILL_ROOT / check_dir_name
        if not check_dir.exists():
            continue
        for py_file in check_dir.rglob("*.py"):
            if py_file.name in EXCLUDE_FILES:
                continue
            py_files.append(py_file)
    return py_files


def check_file(file_path):
    """
    检查单个文件是否包含 UTF-8 reconfigure 代码。
    返回: (bool, str) — (是否通过, 原因)
    """
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        return False, "读取失败: {}".format(e)

    if RECONFIGURE_PATTERN.search(content):
        return True, "包含 UTF-8 reconfigure 代码"
    else:
        return False, "缺少 sys.stdout.reconfigure(encoding='utf-8') 兼容代码"


def main():
    print("=" * 60)
    print("编码兼容性检查 v5.1.0")
    print("=" * 60)
    print()
    print("检查规则: 所有 Python 脚本必须包含 UTF-8 reconfigure 代码")
    print("检查目录: {}".format(", ".join(CHECK_DIRS)))
    print()

    py_files = find_python_files()

    if not py_files:
        print("⚠ 未找到任何 Python 文件需要检查")
        print("  如果这是预期的，请忽略此警告。")
        return 0

    print("找到 {} 个 Python 文件:".format(len(py_files)))
    for f in py_files:
        print("  - {}".format(f.relative_to(SKILL_ROOT)))
    print()

    passed = 0
    failed = 0
    failed_files = []

    for py_file in py_files:
        rel_path = py_file.relative_to(SKILL_ROOT)
        ok, reason = check_file(py_file)
        if ok:
            print("  ✓ {} — {}".format(rel_path, reason))
            passed += 1
        else:
            print("  ✗ {} — {}".format(rel_path, reason))
            failed += 1
            failed_files.append((rel_path, reason))

    print()
    print("-" * 60)
    print("检查结果:")
    print("  通过: {} / {}".format(passed, len(py_files)))
    print("  失败: {} / {}".format(failed, len(py_files)))

    if failed > 0:
        print()
        print("✗ 编码兼容性检查未通过！")
        print()
        print("以下文件缺少 UTF-8 reconfigure 兼容代码:")
        for rel_path, reason in failed_files:
            print("  - {}: {}".format(rel_path, reason))
        print()
        print("修复方法: 在文件 import 之后添加以下代码:")
        print()
        print("  # 跨平台 UTF-8 输出兼容（修复 Windows GBK 编码崩溃）")
        print('  if hasattr(sys.stdout, "reconfigure"):')
        print('      sys.stdout.reconfigure(encoding="utf-8", errors="replace")')
        print('  if hasattr(sys.stderr, "reconfigure"):')
        print('      sys.stderr.reconfigure(encoding="utf-8", errors="replace")')
        return 1
    else:
        print()
        print("✓ 全部通过")
        return 0


if __name__ == "__main__":
    sys.exit(main())
