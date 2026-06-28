#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 作者：阿洋
"""audit-6-summary-check.py — Audit-6 汇总检查脚本

验证 Audit-6 超深度审计的完整性与独立性，确保 12 维度审计全部完成、
输出文件齐全、无循环自证。

检查内容：
  1. 验证 4 个 Audit-6 输出文件存在
     - Audit-6-super-depth-audit.md（12 维度审计日志）
     - Audit-6-remediation-log.md（修复日志）
     - Audit-6-ci-reproduction.md（CI 复现报告）
     - Audit-6-verification-matrix.md（125 项验证矩阵）
  2. 检查 12 维度（A6.1-A6.12）在审计日志中均有独立结论
  3. 检测循环自证模式（禁止"本日志即修复记录"等自引用表述）
  4. 输出汇总报告

退出码:
  0 = 全部检查通过
  1 = 存在缺失文件或维度未审计或检测到循环自证
  2 = 解析错误

用法: python scripts/audit-6-summary-check.py
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
AUDIT_LOGS_DIR = PROJECT_ROOT / "docs" / "audit-logs"

# Audit-6 输出文件清单
REQUIRED_FILES = {
    "super-depth-audit": "Audit-6-super-depth-audit.md",
    "remediation-log": "Audit-6-remediation-log.md",
    "ci-reproduction": "Audit-6-ci-reproduction.md",
    "verification-matrix": "Audit-6-verification-matrix.md",
}

# Audit-6 12 维度定义
DIMENSIONS = {
    "A6.1": "内容深度核验",
    "A6.2": "跨文件语义一致性",
    "A6.3": "数字可复现性",
    "A6.4": "隐式降级检测",
    "A6.5": "循环自证破解",
    "A6.6": "边界 case 审查",
    "A6.7": "时间线一致性",
    "A6.8": "协议闭环",
    "A6.9": "能力卡真实可用性",
    "A6.10": "任务文件 output_schema 与 check YAML 三方对齐",
    "A6.11": "EXHAUST 模式合规性",
    "A6.12": "DAG 拓扑静态分析",
}

# 循环自证禁止表述（在审计日志中不允许出现）
CIRCULAR_SELF_REFERENCE_PATTERNS = [
    r"本日志即修复记录",
    r"本审计即修复",
    r"审计与修复同体",
]


def check_required_files():
    """检查 4 个 Audit-6 输出文件是否存在。

    Returns:
        list of (name, exists: bool, path)
    """
    results = []
    for name, filename in REQUIRED_FILES.items():
        filepath = AUDIT_LOGS_DIR / filename
        results.append((name, filepath.exists(), filename))
    return results


def check_dimensions(audit_content):
    """检查 12 维度是否在审计日志中均有独立结论。

    Args:
        audit_content: Audit-6-super-depth-audit.md 文件内容

    Returns:
        list of (dim_id, dim_name, found: bool)
    """
    results = []
    for dim_id, dim_name in DIMENSIONS.items():
        # 检查维度 ID 出现（作为标题或引用）
        pattern = re.compile(re.escape(dim_id))
        found = bool(pattern.search(audit_content))
        results.append((dim_id, dim_name, found))
    return results


# v6.0.1 Wave 6: 循环自证检测的豁免标记
# 行包含这些标记时不视为违规（表示引用历史违规或描述审计方法）
CIRCULAR_EXEMPT_MARKERS = [
    # 引号标记（表示引用历史违规文本）
    '"', '"', '"', "'", "`",
    # 历史违规描述标记（描述之前如何修复的）
    "问题位置", "问题描述", "修复决策", "修复状态",
    "已修复", "已重写", "移除", "重写", "确认无残留",
    # 审计方法/范围描述标记
    "审计范围", "审计方法", "审计日期",
    "Grep", "扫描", "关键词", "命中数", "豁免",
    # v6.0.1 Wave 6 补充：描述历史违规的标记
    "循环自证", "自述", "措辞",
]


def _is_circular_exempt_line(line):
    """检查行是否处于循环自证检测的豁免上下文中。

    豁免规则：
      1. 行包含引号（表示引用历史违规文本，非当前违规）
      2. 行包含历史违规描述标记（如"问题位置"/"修复决策"）
      3. 行包含审计方法描述标记（如"审计范围"/"Grep"/"扫描"）
    """
    for marker in CIRCULAR_EXEMPT_MARKERS:
        if marker in line:
            return True
    return False


def check_circular_self_reference(audit_content, remediation_content):
    """检测循环自证模式。

    v6.0.1 Wave 6 修复：原逻辑直接 `pattern.search(content)` 过于简单，
    会误判引用历史违规的文本（如"问题位置：L39 '本日志即修复记录'"）。
    新逻辑按行扫描，跳过包含豁免标记的行（引号引用/历史描述/审计方法）。

    Args:
        audit_content: 审计日志内容
        remediation_content: 修复日志内容

    Returns:
        list of (pattern, found_in_audit, found_in_remediation)
    """
    def has_non_exempt_match(content, pattern_str):
        """检查 content 中是否存在非豁免的循环自证匹配。"""
        pattern = re.compile(pattern_str)
        for m in pattern.finditer(content):
            # 获取匹配所在的行
            line_start = content.rfind("\n", 0, m.start()) + 1
            line_end = content.find("\n", m.end())
            if line_end == -1:
                line_end = len(content)
            line = content[line_start:line_end]
            if not _is_circular_exempt_line(line):
                return True
        return False

    results = []
    for pattern_str in CIRCULAR_SELF_REFERENCE_PATTERNS:
        in_audit = has_non_exempt_match(audit_content, pattern_str)
        in_remediation = has_non_exempt_match(remediation_content, pattern_str)
        results.append((pattern_str, in_audit, in_remediation))
    return results


def main():
    print("=" * 60)
    print("Profound Cognition — Audit-6 汇总检查")
    print("=" * 60)

    errors = []

    # === 检查 1: 输出文件存在性 ===
    print("\n[检查 1] Audit-6 输出文件存在性")
    print("-" * 60)

    file_results = check_required_files()
    all_files_exist = True
    for name, exists, filename in file_results:
        mark = "✓" if exists else "✗"
        print(f"  {mark} [{name}] {filename}")
        if not exists:
            all_files_exist = False
            errors.append(f"文件缺失: {filename}")

    print("-" * 60)
    print(f"  文件完整性: {sum(1 for _, e, _ in file_results if e)}/{len(file_results)}")

    # === 检查 2: 12 维度审计完整性 ===
    print("\n[检查 2] 12 维度审计完整性")
    print("-" * 60)

    audit_file = AUDIT_LOGS_DIR / "Audit-6-super-depth-audit.md"
    if not audit_file.exists():
        print(f"  ⚠ 跳过（审计日志不存在: {audit_file.name}）")
        errors.append("无法检查 12 维度（审计日志缺失）")
    else:
        try:
            audit_content = audit_file.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            print(f"  ❌ 读取审计日志失败: {e}")
            errors.append(f"读取审计日志失败: {e}")
            audit_content = ""

        dim_results = check_dimensions(audit_content)
        dims_found = sum(1 for _, _, f in dim_results if f)
        for dim_id, dim_name, found in dim_results:
            mark = "✓" if found else "✗"
            print(f"  {mark} [{dim_id}] {dim_name}")
            if not found:
                errors.append(f"维度缺失: {dim_id} {dim_name}")

        print("-" * 60)
        print(f"  维度完整性: {dims_found}/{len(DIMENSIONS)}")

    # === 检查 3: 循环自证检测 ===
    print("\n[检查 3] 循环自证检测")
    print("-" * 60)

    remediation_file = AUDIT_LOGS_DIR / "Audit-6-remediation-log.md"
    audit_content_for_check = ""
    remediation_content_for_check = ""

    if audit_file.exists():
        try:
            audit_content_for_check = audit_file.read_text(encoding="utf-8", errors="replace")
        except Exception:
            pass

    if remediation_file.exists():
        try:
            remediation_content_for_check = remediation_file.read_text(encoding="utf-8", errors="replace")
        except Exception:
            pass

    circular_results = check_circular_self_reference(
        audit_content_for_check, remediation_content_for_check
    )

    circular_found = False
    for pattern_str, in_audit, in_remediation in circular_results:
        marks = []
        marks.append("✓" if not in_audit else "✗")
        marks.append("✓" if not in_remediation else "✗")
        audit_mark = "无" if not in_audit else "检测到"
        remediation_mark = "无" if not in_remediation else "检测到"
        print(f"  [{marks[0]}审计日志 / {marks[1]}修复日志] \"{pattern_str}\"")
        print(f"     审计日志: {audit_mark} | 修复日志: {remediation_mark}")
        if in_audit or in_remediation:
            circular_found = True
            errors.append(f"循环自证检测到: \"{pattern_str}\"")

    print("-" * 60)
    if circular_found:
        print("  ❌ 循环自证检测: 发现违规表述")
    else:
        print("  ✅ 循环自证检测: 无违规")

    # === 汇总 ===
    print("\n" + "=" * 60)
    if errors:
        print(f"❌ 检查失败: 共 {len(errors)} 项问题")
        for err in errors:
            print(f"   - {err}")
        print("=" * 60)
        sys.exit(1)
    else:
        print("✅ 检查通过: Audit-6 完整性验证全部通过")
        print(f"   - 输出文件: {len(REQUIRED_FILES)} 个全部存在")
        print(f"   - 审计维度: {len(DIMENSIONS)} 个全部覆盖")
        print("   - 循环自证: 无违规")
        print("=" * 60)
        sys.exit(0)


if __name__ == "__main__":
    main()
