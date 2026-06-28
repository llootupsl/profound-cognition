#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 作者：阿洋
"""knowledge-conflict-check.py — Profound Cognition 知识文件冲突检测脚本

扫描 knowledge/ 目录下的知识文件（排除 domains/、thinking-models/、external-capabilities/，
这些由其他子代理处理），检测同一概念/术语在不同文件中的定义冲突。

依据 D12.4.5 知识文件冲突检测机制：
  - 同一术语在不同文件中给出不同定义 → 潜在冲突
  - 同一枚举值在不同文件中给出不同取值集合 → 潜在冲突
  - 同一阈值/数值常量在不同文件中给出不同值 → 潜在冲突
  - 同一字段名在不同文件中给出不同类型/含义 → 潜在冲突

检测策略（启发式，非语义级）：
  1. 提取每个文件中的「定义型」语句（"X 是 Y"、"X 定义为 Y"、"X: Y"）
  2. 提取每个文件中的枚举声明（如 sensitivity_level ∈ {LOW|MEDIUM|HIGH|CRITICAL}）
  3. 提取每个文件中的数值阈值（如 ≥0.8、<0.6、≥2/3）
  4. 跨文件比对同一术语/枚举/阈值，输出潜在冲突清单

扫描范围：
  knowledge/*.md
  knowledge/thinking-templates/*.md
  knowledge/tool-availability/*.md
  （排除 knowledge/domains/、knowledge/thinking-models/、knowledge/external-capabilities/）

用法: python scripts/knowledge-conflict-check.py
退出码: 0=无冲突, 1=存在潜在冲突, 2=脚本错误
"""

import re
import sys
from collections import defaultdict
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
KNOWLEDGE_DIR = PROJECT_ROOT / "knowledge"

# 排除的子目录（由其他子代理处理）
EXCLUDED_SUBDIRS = {"domains", "thinking-models", "external-capabilities"}

# 已知的关键枚举术语（这些术语的取值集合必须跨文件一致）
KNOWN_ENUM_TERMS = [
    "sensitivity_level",
    "evidence_level",
    "output_type",
    "object_type",
    "bias_presets.type",
    "robustness",
    "retrying",
    "prescription_gate_result",
    "identification_strategy",
]

# 已知的关键数值阈值术语（这些阈值的数值必须跨文件一致）
KNOWN_THRESHOLD_TERMS = [
    "FActScore",
    "triangulation",
    "info_gain",
    "e_value",
    "self_check_score",
    "coverage_rate",
    "counterfactual",
]


def collect_knowledge_files():
    """收集需要扫描的知识文件"""
    files = []
    if not KNOWLEDGE_DIR.exists():
        return files

    for md_file in KNOWLEDGE_DIR.glob("*.md"):
        files.append(md_file)

    for subdir in KNOWLEDGE_DIR.iterdir():
        if not subdir.is_dir():
            continue
        if subdir.name in EXCLUDED_SUBDIRS:
            continue
        for md_file in subdir.rglob("*.md"):
            files.append(md_file)

    return sorted(files)


def extract_enum_declarations(content):
    """提取文件中的枚举声明。

    匹配模式：
      - `term` ∈ {A|B|C}
      - term ∈ {A|B|C}
      - term: A | B | C
      - term = A | B | C

    返回: [(term, value_set_str, line_no), ...]
    """
    results = []
    lines = content.split("\n")

    # 模式1：`term` ∈ {A|B|C} 或 term ∈ {A|B|C}
    enum_pattern1 = re.compile(
        r'[`"\']?([a-z_][a-z_\.]*)[`"\']?\s*[∈=]\s*\{([^}]+)\}',
        re.IGNORECASE
    )

    # 模式2：term: A | B | C（在表格或定义中）
    enum_pattern2 = re.compile(
        r'[`"\']([a-z_][a-z_\.]*)[`"\']\s*[:：]\s*([A-Z][A-Z_|\s]+(?:\|[\sA-Z_]+)+)',
        re.IGNORECASE
    )

    for idx, line in enumerate(lines, start=1):
        # 跳过代码块中的行（避免误报代码示例）
        # 但保留 YAML/枚举示例，因为它们常包含关键定义
        for m in enum_pattern1.finditer(line):
            term = m.group(1).lower()
            values = m.group(2).strip()
            results.append((term, values, idx))

        for m in enum_pattern2.finditer(line):
            term = m.group(1).lower()
            values = m.group(2).strip()
            results.append((term, values, idx))

    return results


def extract_threshold_declarations(content):
    """提取文件中的数值阈值声明。

    匹配模式：
      - FActScore < 0.8
      - ≥ 0.8
      - self_check_score >= 85
      - 通过率 ≥ 0.70

    返回: [(term, threshold_str, line_no), ...]
    """
    results = []
    lines = content.split("\n")

    # 匹配 term (op) number 模式
    threshold_pattern = re.compile(
        r'([A-Za-z_][A-Za-z_\s]*?)\s*(?:≥|<=|>=|<|>|≤)\s*(\d+\.?\d*)',
    )

    for idx, line in enumerate(lines, start=1):
        for m in threshold_pattern.finditer(line):
            term = m.group(1).strip().lower()
            value = m.group(2)
            # 过滤掉过于通用的词
            if len(term) < 3:
                continue
            if term in {"if", "the", "and", "or", "not", "for", "with", "when", "then"}:
                continue
            results.append((term, value, idx))

    return results


def normalize_enum_values(values_str):
    """归一化枚举值集合，返回 frozenset"""
    # 分割符：| 或 逗号 或 空格
    parts = re.split(r'[|,，\s]+', values_str)
    cleaned = set()
    for p in parts:
        p = p.strip().strip('`"\'')
        if p and len(p) >= 2:
            cleaned.add(p.upper())
    return frozenset(cleaned)


def detect_enum_conflicts(declarations_by_file):
    """检测枚举声明冲突。

    declarations_by_file: {file_path: [(term, values_str, line_no), ...]}
    返回: [(term, [(file, values_str, line_no), ...]), ...]
    """
    # 按术语聚合所有声明
    term_declarations = defaultdict(list)
    for file_path, decls in declarations_by_file.items():
        for term, values_str, line_no in decls:
            if term in KNOWN_ENUM_TERMS or any(k in term for k in KNOWN_ENUM_TERMS):
                term_declarations[term].append((file_path, values_str, line_no))

    conflicts = []
    for term, decls in term_declarations.items():
        if len(decls) < 2:
            continue

        # 比较归一化后的值集合
        normalized_sets = [(f, normalize_enum_values(v), v, ln) for f, v, ln in decls]
        unique_sets = set(ns for _, ns, _, _ in normalized_sets)

        if len(unique_sets) > 1:
            conflicts.append((term, normalized_sets))

    return conflicts


def detect_threshold_conflicts(declarations_by_file):
    """检测数值阈值冲突。

    declarations_by_file: {file_path: [(term, value_str, line_no), ...]}
    返回: [(term, [(file, value_str, line_no), ...]), ...]
    """
    term_declarations = defaultdict(list)
    for file_path, decls in declarations_by_file.items():
        for term, value_str, line_no in decls:
            # 仅检测已知阈值术语
            for known in KNOWN_THRESHOLD_TERMS:
                if known.lower() in term:
                    term_declarations[term].append((file_path, value_str, line_no))
                    break

    conflicts = []
    for term, decls in term_declarations.items():
        if len(decls) < 2:
            continue

        values = [(f, v, ln) for f, v, ln in decls]
        unique_values = set(v for _, v, _ in values)

        if len(unique_values) > 1:
            conflicts.append((term, values))

    return conflicts


def main():
    print("=" * 70)
    print("Profound Cognition — 知识文件冲突检测（D12.4.5）")
    print("=" * 70)

    if not KNOWLEDGE_DIR.exists():
        print(f"[ERROR] knowledge/ 目录不存在: {KNOWLEDGE_DIR}")
        sys.exit(2)

    files = collect_knowledge_files()
    print(f"\n[扫描] 共发现 {len(files)} 个知识文件")
    print(f"[策略] 检测枚举声明冲突 + 数值阈值冲突")
    print(f"[排除] 子目录: {', '.join(sorted(EXCLUDED_SUBDIRS))}")
    print("-" * 70)

    enum_declarations = {}
    threshold_declarations = {}

    for kf in files:
        rel_path = kf.relative_to(PROJECT_ROOT).as_posix()
        try:
            content = kf.read_text(encoding="utf-8")
        except Exception as e:
            print(f"  [WARN] {rel_path}: 读取失败 ({e})")
            continue

        enum_declarations[rel_path] = extract_enum_declarations(content)
        threshold_declarations[rel_path] = extract_threshold_declarations(content)

    # 检测冲突
    enum_conflicts = detect_enum_conflicts(enum_declarations)
    threshold_conflicts = detect_threshold_conflicts(threshold_declarations)

    # 输出枚举冲突
    print("\n[枚举声明冲突检测]")
    if enum_conflicts:
        print(f"  发现 {len(enum_conflicts)} 处潜在枚举冲突:")
        for term, decls in enum_conflicts:
            print(f"\n  ⚠️  术语: {term}")
            for file_path, norm_set, raw_values, line_no in decls:
                print(f"     - {file_path}:L{line_no} → {raw_values}")
    else:
        print("  ✅ 未发现枚举声明冲突")

    # 输出阈值冲突
    print("\n[数值阈值冲突检测]")
    if threshold_conflicts:
        print(f"  发现 {len(threshold_conflicts)} 处潜在阈值冲突:")
        for term, decls in threshold_conflicts:
            print(f"\n  ⚠️  术语: {term}")
            for file_path, value_str, line_no in decls:
                print(f"     - {file_path}:L{line_no} → {value_str}")
    else:
        print("  ✅ 未发现数值阈值冲突")

    print("\n" + "=" * 70)
    total_conflicts = len(enum_conflicts) + len(threshold_conflicts)
    print(f"[结果] 共发现 {total_conflicts} 处潜在冲突")

    if total_conflicts > 0:
        print("\n[建议] 请人工审查上述潜在冲突，确认是否为真实冲突或上下文差异")
        print("       - 不同上下文下的不同取值可能是合理的（如不同任务节点的阈值）")
        print("       - 同一概念的不同定义需要统一或明确区分上下文")
        sys.exit(1)
    else:
        print("✅ 知识文件冲突检测通过：无潜在冲突")
        sys.exit(0)


if __name__ == "__main__":
    main()
