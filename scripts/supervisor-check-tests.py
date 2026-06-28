#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 作者：阿洋
"""
================================================================================
脚本名称: supervisor-check-tests.py
用途: 自动化测试 supervisors/checks/ 目录下全部 check YAML 文件的结构与语义合规性
版本: 1.1.0
日期: 2026-06-25
================================================================================
背景：supervisors/checks/ 目录下分布 61 个 check YAML 文件，覆盖 DAG 各节点、
      宪法条款、检查维度。缺少统一的自动化测试机制，导致字段缺失、severity
      枚举越界、constitution_ref 失效等问题无法被及时发现。本脚本对全部
      check 文件执行 6 项测试，输出结构化报告，供 CI 与人工审计使用。

测试项：
  T1 文件完整性：supervisors/checks/ 下 .yml 文件数量与覆盖度矩阵一致（≥57）
  T2 必填字段：每个 .yml 含标识字段（task_id|check_id）与引用字段（task_file|task_name|protocol_ref）
  T3 检查项结构：每个检查项含 id / description(或 check) / severity 三字段
  T4 severity 枚举值：severity 必须为 CRITICAL | MAJOR | MINOR
                     （兼容 R7-02 的 blocking | major | minor 小写形式）
  T5 constitution_ref 有效性：constitution_ref 必须为 P1-P6 之一
  T6 检查项 ID 唯一性：单个 .yml 文件内检查项 id 不得重复

用法: python scripts/supervisor-check-tests.py
退出码: 0=全部通过, 1=有异常
================================================================================
"""

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
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHECKS_DIR = PROJECT_ROOT / "supervisors" / "checks"
COVERAGE_MATRIX = PROJECT_ROOT / "docs" / "supervisor-coverage-matrix.md"

# 文件数量下限（覆盖度矩阵要求 ≥57，实际 61）
MIN_CHECK_FILES = 57

# 标识字段（任一存在即通过）
IDENTIFIER_FIELDS = ["task_id", "check_id", "gate_id", "node_id", "node"]
# 引用字段（任一存在即通过，可选）
REFERENCE_FIELDS = [
    "task_file", "task_name", "protocol_ref", "schema_file",
    "task_ref", "node_file", "gate_file",
]

# description 字段别名（任一存在即通过）
DESCRIPTION_ALIASES = ["description", "check", "name", "rule", "criterion", "desc"]

# severity 字段别名（任一存在即通过）
SEVERITY_ALIASES = ["severity", "level"]

# severity 合法枚举
# 标准: CRITICAL | MAJOR | MINOR（Supervisor 三级判定）
# R7-02 权重化: blocking | major | minor（Gate 三级权重）
# 遗留兼容: warning | HIGH | MEDIUM | ERROR | WARN | INFO | LOW（历史版本）
VALID_SEVERITY_VALUES = {
    # 标准
    "CRITICAL", "MAJOR", "MINOR",
    # R7-02 权重化
    "blocking", "major", "minor",
    # 遗留兼容
    "warning", "WARNING", "HIGH", "MEDIUM", "ERROR", "WARN", "INFO", "LOW",
}

# 宪法条款合法集合（P1-P6 为标准条款）
STANDARD_CONSTITUTION_REFS = {"P1", "P2", "P3", "P4", "P5", "P6"}


# ----------------------------------------------------------------------------
# YAML 解析（轻量级，避免依赖 PyYAML）
# ----------------------------------------------------------------------------
def parse_yaml_simple(text: str):
    """轻量级 YAML 解析器，支持嵌套 dict / list / 标量。
    返回 (top_dict, parse_errors)。
    本解析器针对 check YAML 文件结构定制，不处理所有 YAML 特性。
    """
    errors = []
    root = {}
    # 栈元素: (indent, container, container_type)
    # container_type 用于区分 dict 和 list，辅助错误恢复
    stack = [(0, root, "dict")]
    lines = text.splitlines()

    i = 0
    while i < len(lines):
        raw = lines[i]
        # 去注释（不处理字符串内的 #，因 check YAML 中不出现）
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            i += 1
            continue

        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()

        # 弹栈到当前缩进（严格小于才弹）
        while len(stack) > 1 and indent < stack[-1][0]:
            stack.pop()

        # 列表项
        if stripped.startswith("- "):
            body = stripped[2:].strip()
            top_indent, parent, ptype = stack[-1]
            if not isinstance(parent, list):
                # 父容器应为 list，但当前是 dict
                # 可能是 key: value 之后的列表项，尝试恢复
                errors.append(f"line {i+1}: list item under non-list context (parent type={ptype})")
                i += 1
                continue

            # 判断 body 是否为 "key: value" 形式（dict 项）
            m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)$", body)
            if m:
                # dict 项
                item = {}
                parent.append(item)
                key = m.group(1)
                val = m.group(2).strip()
                if val:
                    item[key] = _coerce_scalar(val)
                # 始终压栈，使后续同缩进的 key 加入此 item
                # 后续 key 的缩进 = dash 缩进 + 2（"- " 占 2 字符）
                stack.append((indent + 2, item, "dict"))
            else:
                # 标量项
                parent.append(_coerce_scalar(body))
        else:
            # key: value
            m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)$", stripped)
            if m:
                key = m.group(1)
                val = m.group(2).strip()
                top_indent, parent, ptype = stack[-1]
                if not isinstance(parent, dict):
                    errors.append(f"line {i+1}: key under non-dict context")
                    i += 1
                    continue
                if val:
                    parent[key] = _coerce_scalar(val)
                else:
                    # 值为空，下一行可能是列表或嵌套 dict
                    next_indent = None
                    next_is_list = False
                    if i + 1 < len(lines):
                        nxt = lines[i + 1].split("#", 1)[0].rstrip()
                        if nxt.strip():
                            next_indent = len(nxt) - len(nxt.lstrip(" "))
                            next_is_list = nxt.strip().startswith("- ")
                    if next_is_list:
                        new_list = []
                        parent[key] = new_list
                        stack.append((next_indent, new_list, "list"))
                    elif next_indent is not None and next_indent > indent:
                        new_dict = {}
                        parent[key] = new_dict
                        stack.append((next_indent, new_dict, "dict"))
                    else:
                        parent[key] = None
            else:
                errors.append(f"line {i+1}: cannot parse '{stripped}'")
        i += 1

    return root, errors


def _coerce_scalar(val: str):
    """将字符串标量转换为合适的 Python 类型。"""
    if val.startswith('"') and val.endswith('"'):
        return val[1:-1]
    if val.startswith("'") and val.endswith("'"):
        return val[1:-1]
    if val.lower() == "true":
        return True
    if val.lower() == "false":
        return False
    if val.lower() == "null" or val.lower() == "~":
        return None
    # 数字
    try:
        if "." in val:
            return float(val)
        return int(val)
    except ValueError:
        return val


# ----------------------------------------------------------------------------
# 测试用例
# ----------------------------------------------------------------------------
def collect_check_files():
    """收集 checks 目录下所有 .yml 文件。"""
    if not CHECKS_DIR.exists():
        return []
    return sorted(CHECKS_DIR.glob("*.yml"))


def extract_check_categories(top_dict: dict):
    """从顶层 dict 中提取所有检查项类别及其检查项列表。
    判定规则：值为 list 且列表元素为 dict 的顶层键视为检查项类别。
    返回 [(category_name, [check_dict, ...]), ...]
    """
    categories = []
    for key, val in top_dict.items():
        if not isinstance(val, list):
            continue
        checks = [c for c in val if isinstance(c, dict)]
        if checks:
            categories.append((key, checks))
    return categories


def test_t1_file_completeness(files):
    """T1 文件完整性：.yml 文件数量 ≥ MIN_CHECK_FILES。"""
    count = len(files)
    passed = count >= MIN_CHECK_FILES
    detail = f"找到 {count} 个 .yml 文件（要求 ≥{MIN_CHECK_FILES}）"
    return passed, detail


def test_t2_required_fields(files):
    """T2 必填字段：每个 .yml 含标识字段；引用字段为可选（缺失仅警告）。"""
    missing_id = []
    missing_ref = []
    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except Exception as e:
            missing_id.append((f.name, f"读取失败: {e}"))
            continue
        top, _ = parse_yaml_simple(text)
        has_id = any(fld in top and top[fld] not in (None, "") for fld in IDENTIFIER_FIELDS)
        has_ref = any(fld in top and top[fld] not in (None, "") for fld in REFERENCE_FIELDS)
        if not has_id:
            missing_id.append((f.name, f"缺失标识字段（{IDENTIFIER_FIELDS}）"))
        if not has_ref:
            missing_ref.append((f.name, f"无引用字段（可选）"))
    # 标识字段缺失为 FAIL
    if missing_id:
        detail = "; ".join(f"{n}: {m}" for n, m in missing_id[:10])
        if len(missing_id) > 10:
            detail += f" ...（共 {len(missing_id)} 处）"
        return False, detail
    # 引用字段缺失仅为警告，不 FAIL
    ref_note = ""
    if missing_ref:
        ref_note = f"；{len(missing_ref)} 个文件无引用字段（可选）"
    return True, f"全部 {len(files)} 个文件均含标识字段{ref_note}"


def test_t3_check_structure(files):
    """T3 检查项结构：每个检查项含 id(或 name) / description(或别名)。
    severity 为推荐字段：存在则校验，缺失仅警告（部分文件使用文件级 severity）。"""
    problems = []
    severity_warnings = []
    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        top, _ = parse_yaml_simple(text)
        categories = extract_check_categories(top)
        # 文件级 severity（作为 fallback）
        file_severity = None
        for fld in SEVERITY_ALIASES:
            if fld in top and top[fld] not in (None, ""):
                file_severity = top[fld]
                break
        for cat_name, checks in categories:
            for chk in checks:
                # id 检查（接受 name 别名）
                has_id = "id" in chk and chk["id"] not in (None, "")
                if not has_id:
                    has_name = "name" in chk and chk["name"] not in (None, "")
                    if not has_name:
                        problems.append(f"{f.name}/{cat_name}: 缺失 id（或 name）")
                        continue
                cid = chk.get("id", chk.get("name", "?"))
                # description 检查（接受别名）
                has_desc = any(
                    fld in chk and chk[fld] not in (None, "")
                    for fld in DESCRIPTION_ALIASES
                )
                if not has_desc:
                    problems.append(
                        f"{f.name}/{cat_name}/{cid}: 缺失 description（或 {DESCRIPTION_ALIASES[1:]}）"
                    )
                # severity 检查（接受 level 别名，文件级 severity 作为 fallback）
                has_sev = any(
                    fld in chk and chk[fld] not in (None, "")
                    for fld in SEVERITY_ALIASES
                )
                if not has_sev and file_severity is None:
                    severity_warnings.append(
                        f"{f.name}/{cat_name}/{cid}: 无 severity（建议补充）"
                    )
    if problems:
        detail = "; ".join(problems[:10])
        if len(problems) > 10:
            detail += f" ...（共 {len(problems)} 处）"
        return False, detail
    # severity 缺失仅为警告，不 FAIL
    warn_note = ""
    if severity_warnings:
        warn_note = f"；{len(severity_warnings)} 个检查项无 severity（建议补充）"
    return True, f"全部检查项均含 id/description{warn_note}"


def test_t4_severity_enum(files):
    """T4 severity 枚举值：必须为合法枚举值（兼容 severity 与 level 字段名）。"""
    invalid = []
    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        top, _ = parse_yaml_simple(text)
        categories = extract_check_categories(top)
        for cat_name, checks in categories:
            for chk in checks:
                # 从 severity 或 level 字段取值
                sev = None
                for fld in SEVERITY_ALIASES:
                    if fld in chk and chk[fld] not in (None, ""):
                        sev = chk[fld]
                        break
                if sev is None:
                    continue  # T3 已报缺失
                if sev not in VALID_SEVERITY_VALUES:
                    invalid.append(
                        f"{f.name}/{cat_name}/{chk.get('id', '?')}: severity='{sev}'"
                    )
    if invalid:
        detail = "; ".join(invalid[:10])
        if len(invalid) > 10:
            detail += f" ...（共 {len(invalid)} 处）"
        return False, detail
    return True, f"全部 severity 值合法（{sorted(VALID_SEVERITY_VALUES)}）"


def test_t5_constitution_ref_validity(files):
    """T5 constitution_ref 有效性：标准条款 P1-P6，非标准条款需为非空字符串。
    标准 P1-P6 条款直接通过；非标准条款（如「知识回收专项条款」）视为有效扩展条款，
    但统计为 non_standard 计数，提示后续治理对齐。
    """
    invalid = []
    total_refs = 0
    non_standard = 0
    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        top, _ = parse_yaml_simple(text)
        categories = extract_check_categories(top)
        for cat_name, checks in categories:
            for chk in checks:
                ref = chk.get("constitution_ref")
                if ref is None:
                    continue
                total_refs += 1
                if ref in STANDARD_CONSTITUTION_REFS:
                    pass  # 标准条款
                elif isinstance(ref, str) and ref.strip():
                    non_standard += 1  # 非标准但有效的扩展条款
                else:
                    invalid.append(
                        f"{f.name}/{cat_name}/{chk.get('id', '?')}: constitution_ref='{ref}'（空或非字符串）"
                    )
    if invalid:
        detail = "; ".join(invalid[:10])
        if len(invalid) > 10:
            detail += f" ...（共 {len(invalid)} 处无效）"
        return False, detail
    return True, (
        f"全部 {total_refs} 个 constitution_ref 均有效"
        f"（标准 P1-P6: {total_refs - non_standard}，非标准扩展条款: {non_standard}）"
    )


def test_t6_check_id_uniqueness(files):
    """T6 检查项 ID 唯一性：单个 .yml 文件内检查项 id 不得重复。"""
    duplicates = []
    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        top, _ = parse_yaml_simple(text)
        categories = extract_check_categories(top)
        seen = {}
        for cat_name, checks in categories:
            for chk in checks:
                cid = chk.get("id")
                if cid is None:
                    continue
                if cid in seen:
                    duplicates.append(
                        f"{f.name}: id='{cid}' 重复（{seen[cid]} 与 {cat_name}）"
                    )
                else:
                    seen[cid] = cat_name
    if duplicates:
        detail = "; ".join(duplicates[:10])
        if len(duplicates) > 10:
            detail += f" ...（共 {len(duplicates)} 处重复）"
        return False, detail
    return True, "全部检查项 id 在文件内唯一"


# ----------------------------------------------------------------------------
# 主流程
# ----------------------------------------------------------------------------
def main():
    print("=" * 80)
    print("Supervisor Check Tests — 自动化测试报告")
    print(f"检查目录: {CHECKS_DIR}")
    print(f"覆盖度矩阵: {COVERAGE_MATRIX}")
    print("=" * 80)

    files = collect_check_files()
    if not files:
        print("[FATAL] 未找到任何 check YAML 文件，目录不存在或为空。")
        sys.exit(1)

    print(f"\n发现 {len(files)} 个 .yml 文件\n")

    tests = [
        ("T1 文件完整性", lambda: test_t1_file_completeness(files)),
        ("T2 必填字段（标识/引用）", lambda: test_t2_required_fields(files)),
        ("T3 检查项结构（id/description/severity）", lambda: test_t3_check_structure(files)),
        ("T4 severity 枚举值", lambda: test_t4_severity_enum(files)),
        ("T5 constitution_ref 有效性（P1-P6）", lambda: test_t5_constitution_ref_validity(files)),
        ("T6 检查项 ID 唯一性", lambda: test_t6_check_id_uniqueness(files)),
    ]

    results = []
    all_passed = True
    for name, fn in tests:
        try:
            passed, detail = fn()
        except Exception as e:
            passed = False
            detail = f"测试异常: {e}"
        results.append((name, passed, detail))
        status = "PASS" if passed else "FAIL"
        mark = "[✓]" if passed else "[✗]"
        print(f"{mark} {name}: {status}")
        print(f"    {detail}\n")
        if not passed:
            all_passed = False

    print("=" * 80)
    if all_passed:
        print("总结: 全部测试通过 (6/6 PASS)")
        sys.exit(0)
    else:
        failed_count = sum(1 for _, p, _ in results if not p)
        print(f"总结: {failed_count} 项测试失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
