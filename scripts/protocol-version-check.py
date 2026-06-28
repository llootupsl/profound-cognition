#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 作者：阿洋
"""protocol-version-check.py — Profound Cognition 协议版本号一致性校验脚本

扫描 protocols/ 目录下所有 .md 协议文件，提取 YAML 代码块中的 version 字段，
检测是否全部统一为 v3.0。

依据 docs/protocol-version-governance.md 治理规范：
  - 所有协议文件的 version 字段必须为 "3.0"
  - 协议标题中的版本号（如 (v3.0)）也需统一为 v3.0

扫描模式：
  1. YAML 代码块中的 `version: "X.Y"` 或 `version: "X"` 声明
  2. 协议标题行中的 `vX.Y` 或 `vX` 版本号

用法: python scripts/protocol-version-check.py
退出码: 0=全部一致, 1=存在不一致, 2=脚本错误
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
PROTOCOLS_DIR = PROJECT_ROOT / "protocols"

# 期望的协议版本号（依据 docs/protocol-version-governance.md）
EXPECTED_VERSION = "3.0"

# YAML version 字段正则（匹配 version: "3.0" / version: "3" / version: 3.0 等）
YAML_VERSION_RE = re.compile(r'^\s*version:\s*"?(\d+(?:\.\d+)*)"?', re.MULTILINE)

# 标题中的版本号正则（匹配 (v3.0) / (v3) / (v2 适配) 等）
TITLE_VERSION_RE = re.compile(r'\(v(\d+(?:\.\d+)*)\s*[^)]*\)')


def extract_yaml_versions(content):
    """从文件内容中提取所有 YAML version 字段声明。

    返回: [(line_number, raw_value, normalized_value), ...]
    """
    results = []
    lines = content.split("\n")
    for idx, line in enumerate(lines, start=1):
        m = re.match(r'^\s*version:\s*"?(\d+(?:\.\d+)*)"?', line)
        if m:
            raw = m.group(1)
            # 归一化：确保是 X.Y 格式
            if "." in raw:
                normalized = raw
            else:
                # 单数字版本号如 "3" → "3.0"
                normalized = raw + ".0"
            results.append((idx, raw, normalized))
    return results


def extract_title_version(content):
    """从文件标题（前 10 行）提取协议版本号。

    注意：仅识别纯协议版本号声明如 (v3.0)，排除框架适配说明如 (v2 适配)。
    依据 docs/protocol-version-governance.md，框架版本引用不受协议版本约束。

    返回: (line_number, raw_value, normalized_value) 或 None
    """
    lines = content.split("\n")[:10]
    for idx, line in enumerate(lines, start=1):
        # 匹配 (v3.0) / (v3) 等纯版本号声明
        # 排除 (v2 适配) / (v3 适配) 等框架适配说明（"适配"关键字表示框架引用）
        m = re.search(r'\(v(\d+(?:\.\d+)*)\s*[^)]*\)', line)
        if m:
            # 检查括号内是否含"适配"关键字——这是框架版本引用，跳过
            full_match = m.group(0)
            if "适配" in full_match:
                continue
            raw = m.group(1)
            if "." in raw:
                normalized = raw
            else:
                normalized = raw + ".0"
            return (idx, raw, normalized)
    return None


def scan_protocol_file(file_path):
    """扫描单个协议文件，返回版本号声明列表。

    返回: {
        'yaml_versions': [(line_no, raw, normalized), ...],
        'title_version': (line_no, raw, normalized) 或 None,
    }
    """
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        return {'error': str(e), 'yaml_versions': [], 'title_version': None}

    return {
        'yaml_versions': extract_yaml_versions(content),
        'title_version': extract_title_version(content),
    }


def main():
    print("=" * 60)
    print("Profound Cognition — 协议版本号一致性校验")
    print("=" * 60)

    if not PROTOCOLS_DIR.exists():
        print(f"[ERROR] protocols/ 目录不存在: {PROTOCOLS_DIR}")
        sys.exit(2)

    # 收集所有 .md 协议文件
    # 注意：本脚本扫描 protocols/*.md（全部 .md 文件，含 output-schema-spec.md 等非 -protocol.md 后缀的文件），
    # 因此本脚本的协议计数（22）会高于 protocol-deps-check.py 的协议计数（21）。
    # 差异原因：protocol-deps-check.py 仅扫描文件名以 -protocol.md 结尾的文件，
    #          而本脚本扫描所有 .md 文件（含 output-schema-spec.md 等规范类文件）。
    # 两脚本对"协议"的定义不同，但各自逻辑自洽。详见 Audit-6 F9 修复记录。
    protocol_files = sorted(PROTOCOLS_DIR.glob("*.md"))
    print(f"\n[扫描] 共发现 {len(protocol_files)} 个协议文件（含非 -protocol.md 后缀的规范文件，如 output-schema-spec.md）")
    print(f"[期望] 全部版本号应为 v{EXPECTED_VERSION}")
    print("-" * 60)

    findings = []  # (file, location, version, ok)
    inconsistent = []

    for pf in protocol_files:
        rel_name = pf.name
        result = scan_protocol_file(pf)

        if 'error' in result:
            print(f"  [WARN] {rel_name}: 读取失败 ({result['error']})")
            findings.append((rel_name, "read_error", "N/A", False))
            continue

        # 检查 YAML version 字段
        for line_no, raw, normalized in result['yaml_versions']:
            ok = (normalized == EXPECTED_VERSION)
            loc = f"L{line_no} version:"
            findings.append((rel_name, loc, raw, ok))
            if not ok:
                inconsistent.append((rel_name, loc, raw, EXPECTED_VERSION))

        # 检查标题版本号
        tv = result['title_version']
        if tv:
            line_no, raw, normalized = tv
            ok = (normalized == EXPECTED_VERSION)
            loc = f"L{line_no} title(v)"
            findings.append((rel_name, loc, raw, ok))
            if not ok:
                inconsistent.append((rel_name, loc, raw, EXPECTED_VERSION))

    # 输出结果
    for file, loc, ver, ok in findings:
        status = "✅" if ok else "❌"
        print(f"  {status} {file:45s} {loc:20s} = {ver}")

    print("-" * 60)
    print(f"[结果] 共检查 {len(findings)} 处版本号声明")

    if inconsistent:
        print(f"\n❌ 协议版本号不一致: {len(inconsistent)} 处与期望值 (v{EXPECTED_VERSION}) 不符")
        for file, loc, ver, expected in inconsistent:
            print(f"   - {file} [{loc}]: {ver} (应为 {expected})")
        print("\n" + "=" * 60)
        sys.exit(1)
    else:
        print(f"\n✅ 协议版本号一致性校验通过: 全部为 v{EXPECTED_VERSION}")
        print("=" * 60)
        sys.exit(0)


if __name__ == "__main__":
    main()
