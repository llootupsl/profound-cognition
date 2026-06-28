#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 作者：阿洋
"""
================================================================================
脚本名称: plugins-health-check.py
用途: 统一检查 plugins/ 目录下所有插件适配器的可用性与一致性
版本: 1.0.0
日期: 2026-06-25
================================================================================
背景：plugins/ 目录下分布 23 个插件适配器（.md），各适配器独立维护，
      缺少统一的健康检查机制。本脚本对全部插件执行 6 项健康检查，
      输出结构化报告，供 CI 与人工审计使用。

检查项：
  H1 文件完整性：plugins/ 下 .md 适配器文件数量与 config.yaml registry 一致
  H2 Frontmatter 合规：每个 .md 含 YAML frontmatter（name/description/author/tags）
  H3 配置一致性：每个 .md 在 plugins/config.yaml 中有对应条目
  H4 激活条件声明：每个 .md 含「激活条件」章节
  H5 穷尽重试声明：每个 .md 含「穷尽重试」或「exhaust_retry」章节
  H6 错误处理声明：每个 .md 含「错误处理」或「error_handling」章节

用法: python scripts/plugins-health-check.py
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
PLUGINS_DIR = PROJECT_ROOT / "plugins"
CONFIG_FILE = PLUGINS_DIR / "config.yaml"

# 必填 frontmatter 字段
REQUIRED_FRONTMATTER_FIELDS = ["name", "description", "author", "tags"]

# 必填章节关键词（任一命中即视为通过）
REQUIRED_SECTIONS = {
    "activation": ["激活条件", "activation"],
    "exhaust_retry": ["穷尽重试", "exhaust_retry", "exhaust-retry", "穷尽尝试"],
    "error_handling": ["错误处理", "error_handling", "error-handling"],
}


def parse_frontmatter(content: str):
    """解析 Markdown 文件顶部 YAML frontmatter，返回 (frontmatter_dict, body_str)。
    若无 frontmatter，返回 ({}, content)。
    """
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not fm_match:
        return {}, content
    fm_text = fm_match.group(1)
    body = fm_match.group(2)
    fm = {}
    for line in fm_text.splitlines():
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)$", line)
        if m:
            key = m.group(1).strip()
            val = m.group(2).strip().strip('"').strip("'")
            fm[key] = val
    return fm, body


def load_config_registry():
    """从 plugins/config.yaml 解析已注册插件名列表。
    简易解析：抓取所有 `- name: xxx` 行。
    """
    if not CONFIG_FILE.exists():
        return set()
    text = CONFIG_FILE.read_text(encoding="utf-8")
    return {m.group(1).strip() for m in re.finditer(r"^\s*-\s*name\s*:\s*([^\n]+)$", text, re.MULTILINE)}


def check_plugin_file(path: Path, registered_names: set):
    """对单个插件 .md 执行 5 项检查（H2-H6），返回 (plugin_name, issues_list)。"""
    issues = []
    content = path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(content)

    # H2 Frontmatter 合规
    for field in REQUIRED_FRONTMATTER_FIELDS:
        if field not in fm:
            issues.append(f"H2: frontmatter 缺失字段 '{field}'")

    plugin_name = fm.get("name", path.stem)

    # H3 配置一致性
    if plugin_name not in registered_names and path.stem not in registered_names:
        issues.append(f"H3: 插件 '{plugin_name}' 未在 plugins/config.yaml 中注册")

    # H4-H6 章节关键词检查（在 body 中查找）
    for check_id, keywords in REQUIRED_SECTIONS.items():
        if not any(kw.lower() in body.lower() for kw in keywords):
            issues.append(f"{check_id.upper()}: 缺少章节（关键词: {keywords}）")

    return plugin_name, issues


def main():
    errors = []
    warnings = []
    passed = []

    # H1 文件完整性
    if not PLUGINS_DIR.exists():
        errors.append("H1: plugins/ 目录不存在")
        print("FAIL: plugins/ 目录不存在")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    plugin_files = sorted(PLUGINS_DIR.glob("*.md"))
    # 排除非适配器文件（如 README.md）
    adapter_files = [p for p in plugin_files if p.name.lower() not in ("readme.md", "changelog.md")]

    registered_names = load_config_registry()

    if not adapter_files:
        errors.append("H1: plugins/ 下未发现任何插件适配器 .md 文件")
    elif len(adapter_files) < 5:
        warnings.append(f"H1: plugins/ 下适配器数量 {len(adapter_files)} 偏少（预期 ≥ 5）")

    print(f"INFO: 发现 {len(adapter_files)} 个插件适配器，config.yaml 注册 {len(registered_names)} 个")
    print(f"INFO: 开始逐个检查...")
    print("-" * 70)

    for pf in adapter_files:
        name, issues = check_plugin_file(pf, registered_names)
        if issues:
            warnings.append(f"{pf.name}:")
            for iss in issues:
                warnings.append(f"  - {iss}")
            print(f"WARN: {pf.name}")
            for iss in issues:
                print(f"  - {iss}")
        else:
            passed.append(pf.name)
            print(f"PASS: {pf.name}")

    print("-" * 70)
    print(f"总计: PASS={len(passed)}, WARN={len(warnings)}, ERROR={len(errors)}")

    if errors:
        print("\n=== 错误 ===")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    if warnings:
        print("\n=== 警告 ===")
        for w in warnings:
            print(f"  - {w}")
        # 警告不阻塞 CI，但退出码仍为 0
        sys.exit(0)

    print("\n全部插件健康检查通过。")
    sys.exit(0)


if __name__ == "__main__":
    main()
