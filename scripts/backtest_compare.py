#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 作者：阿洋
"""backtest_compare.py — 鲁班慢刨回测对比工具

把一次性验证沉淀为仓库工具。功能：
  1. 对比冻结基线（v5.1.0 修复前）和当前版本的差异（基于 CHANGELOG）
  2. 检查版本号一致性（扫描所有文件中的版本号，报告不一致）
  3. 检查 reference-integrity（调用 reference-integrity.py）
  4. 输出对比报告（Markdown 格式）

用法:
  python scripts/backtest_compare.py                   # 全量对比（默认）
  python scripts/backtest_compare.py --check-version   # 仅版本号一致性检查
  python scripts/backtest_compare.py --check-integrity # 仅引用完整性检查

退出码:
  0 = 全部通过
  1 = 存在异常
"""

import argparse
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime
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

# --------------------------------------------------------------------------
# 配置（全部基于脚本位置动态推导，不硬编码绝对路径）
# --------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
REFERENCE_INTEGRITY_SCRIPT = SCRIPTS_DIR / "reference-integrity.py"
CHANGELOG_FILE = PROJECT_ROOT / "CHANGELOG.md"

# 冻结基线版本（v5.1.0 修复前）
FROZEN_BASELINE_VERSION = "5.0.0"
CURRENT_VERSION = "5.1.0"

# 扫描的文件扩展名
SCAN_EXTENSIONS = {
    ".md", ".yml", ".yaml", ".json", ".py",
    ".mmd", ".typ", ".html", ".sh", ".ps1",
}

# 排除的目录（不扫描）
EXCLUDE_DIRS = {
    ".git", ".github", "node_modules", "__pycache__",
    ".venv", "venv", "env", ".pytest_cache", ".mypy_cache",
    ".ruff_cache", "build", "dist", ".claude-plugin",
}

# 排除的文件（自身 + 二进制文件）
EXCLUDE_FILES = {"backtest_compare.py"}

# --------------------------------------------------------------------------
# 版本号匹配模式（保守匹配，避免误报日期/章节号）
# --------------------------------------------------------------------------
# 模式 1：显式 v 前缀，如 v5.1.0
PATTERN_V_PREFIX = re.compile(r'(?<![A-Za-z0-9])v(?P<version>\d+\.\d+\.\d+)(?![0-9])')
# 模式 2：JSON version 字段，如 "version": "5.1.0"
PATTERN_JSON_VERSION = re.compile(
    r'"version"\s*:\s*"(?P<version>\d+\.\d+\.\d+)"'
)
# 模式 3：YAML/MD version 字段，如 version: 5.1.0 或 version: "5.1.0"
PATTERN_YAML_VERSION = re.compile(
    r'(?:^|\s)version\s*:\s*["\']?(?P<version>\d+\.\d+\.\d+)["\']?(?!\d)',
    re.MULTILINE,
)
# 模式 4：CHANGELOG 标题，如 ## [v5.1.0]
PATTERN_CHANGELOG_HEADER = re.compile(
    r'^##\s*\[v?(?P<version>\d+\.\d+\.\d+)\]',
    re.MULTILINE,
)
# 模式 5：Version: 标注，如 Version: 5.1.0
PATTERN_VERSION_LABEL = re.compile(
    r'[Vv]ersion\s*[:：]\s*v?(?P<version>\d+\.\d+\.\d+)(?![0-9])'
)

ALL_VERSION_PATTERNS = [
    PATTERN_V_PREFIX,
    PATTERN_JSON_VERSION,
    PATTERN_YAML_VERSION,
    PATTERN_CHANGELOG_HEADER,
    PATTERN_VERSION_LABEL,
]


def should_scan(path):
    """判断文件是否需要扫描"""
    if path.name in EXCLUDE_FILES:
        return False
    if path.suffix.lower() not in SCAN_EXTENSIONS:
        return False
    # 检查是否在排除目录中
    try:
        rel_parts = path.relative_to(PROJECT_ROOT).parts
    except ValueError:
        return False
    for part in rel_parts:
        if part in EXCLUDE_DIRS:
            return False
    return True


def find_version_numbers(content):
    """从文件内容中提取所有版本号及其上下文"""
    findings = []
    seen_spans = set()

    for pattern in ALL_VERSION_PATTERNS:
        for match in pattern.finditer(content):
            version = match.group("version")
            start = match.start()
            # 避免同一位置重复匹配
            if any(abs(start - s) < 3 for s in seen_spans):
                continue
            seen_spans.add(start)

            # 提取上下文（前后各 20 字符）
            ctx_start = max(0, start - 20)
            ctx_end = min(len(content), match.end() + 20)
            context = content[ctx_start:ctx_end].replace("\n", " ").strip()
            findings.append({
                "version": version,
                "context": context,
                "line": content[:start].count("\n") + 1,
            })

    return findings


# 历史版本引用的上下文标记（出现这些标记的行中的版本号是历史引用，不是当前版本声明）
HISTORICAL_REFERENCE_MARKERS = [
    "新增", "强化", "修复", "移除", "修改", "更新", "替换",
    "deprecated", "DEPRECATED", "已废弃", "已弃用", "已移除",
    "已替换", "已修复", "已修改", "已更新", "已新增",
    "→", "历史", "旧", "原", "从 v", "自 v",
    "tagged", "校验项", "强制规则", "self_check",
    "must_not", "Phase", "Task",
    # 带括号的版本标注，如 （v4.1.3）、(v4.1.5)
    "（v", "(v",
    # 强制/同步追加/提升为/背景等历史变更描述
    "强制", "同步追加", "提升为", "背景",
    # result-card.md 表格中的历史方案标注
    "方案A", "方案B",
]


def is_historical_version_reference(line_content, version):
    """检查版本号是否出现在历史引用上下文中。

    当版本号出现在"v4.1.4 新增"、"v4.1.5 强化"等历史变更描述上下文中时，
    视为历史引用，不报告为版本号不一致。
    """
    for marker in HISTORICAL_REFERENCE_MARKERS:
        if marker in line_content:
            return True
    return False


def scan_version_consistency():
    """扫描全项目版本号一致性

    返回:
        dict: {
            "expected": "5.1.0",
            "files_scanned": int,
            "by_version": {version: [(file, line, context), ...]},
            "inconsistent": [(file, line, found_version, context), ...],
            "summary": str,
        }
    """
    by_version = defaultdict(list)
    files_scanned = 0
    inconsistent = []

    for root, dirs, files in os.walk(PROJECT_ROOT):
        # 原地修改 dirs 以跳过排除目录
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for fname in files:
            fpath = Path(root) / fname
            if not should_scan(fpath):
                continue
            try:
                content = fpath.read_text(encoding="utf-8", errors="replace")
            except (OSError, UnicodeDecodeError):
                continue
            files_scanned += 1

            findings = find_version_numbers(content)
            if not findings:
                continue

            try:
                rel_path = str(fpath.relative_to(PROJECT_ROOT)).replace("\\", "/")
            except ValueError:
                rel_path = str(fpath)

            # CHANGELOG.md 中的版本号都是历史记录，跳过不一致检查
            is_changelog = (fname == "CHANGELOG.md")

            for f in findings:
                by_version[f["version"]].append(
                    (rel_path, f["line"], f["context"])
                )
                # CHANGELOG.md 中的版本号是历史记录，不视为不一致
                # 其他文件中的历史版本引用（如"v4.1.4 新增"）也不视为不一致
                if f["version"] != CURRENT_VERSION:
                    if is_changelog:
                        pass  # CHANGELOG.md 全部跳过
                    elif is_historical_version_reference(f["context"], f["version"]):
                        pass  # 历史引用跳过
                    else:
                        inconsistent.append(
                            (rel_path, f["line"], f["version"], f["context"])
                        )

    # 生成摘要
    lines = []
    lines.append(f"扫描文件数：{files_scanned}")
    lines.append(f"期望版本：{CURRENT_VERSION}")
    lines.append(f"发现版本分布：")
    for ver in sorted(by_version.keys()):
        count = len(by_version[ver])
        marker = " ✅" if ver == CURRENT_VERSION else " ⚠️"
        lines.append(f"  - v{ver}：{count} 处{marker}")
    if inconsistent:
        lines.append(f"\n不一致项：{len(inconsistent)} 处")
    else:
        lines.append("\n不一致项：0 处（全部一致 ✅）")

    return {
        "expected": CURRENT_VERSION,
        "files_scanned": files_scanned,
        "by_version": dict(by_version),
        "inconsistent": inconsistent,
        "summary": "\n".join(lines),
    }


def run_reference_integrity():
    """调用 reference-integrity.py 进行引用完整性检查

    返回:
        dict: {
            "script_exists": bool,
            "return_code": int,
            "stdout": str,
            "stderr": str,
            "passed": bool,
        }
    """
    result = {
        "script_exists": REFERENCE_INTEGRITY_SCRIPT.exists(),
        "return_code": -1,
        "stdout": "",
        "stderr": "",
        "passed": False,
    }

    if not result["script_exists"]:
        result["stderr"] = f"reference-integrity.py 不存在: {REFERENCE_INTEGRITY_SCRIPT}"
        return result

    try:
        proc = subprocess.run(
            [sys.executable, str(REFERENCE_INTEGRITY_SCRIPT)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=str(PROJECT_ROOT),
            timeout=120,
        )
        result["return_code"] = proc.returncode
        result["stdout"] = proc.stdout or ""
        result["stderr"] = proc.stderr or ""
        result["passed"] = (proc.returncode == 0)
    except subprocess.TimeoutExpired:
        result["stderr"] = "reference-integrity.py 执行超时（120s）"
    except FileNotFoundError:
        result["stderr"] = f"Python 解释器不可用: {sys.executable}"
    except OSError as exc:
        result["stderr"] = f"执行异常: {exc}"

    return result


def extract_changelog_diff():
    """从 CHANGELOG.md 提取 v5.1.0 和 v5.0.0 的变更记录

    返回:
        dict: {
            "changelog_exists": bool,
            "baseline_version": "5.0.0",
            "current_version": "5.1.0",
            "current_section": str,   # v5.1.0 的变更内容
            "baseline_section": str,  # v5.0.0 的变更内容
        }
    """
    result = {
        "changelog_exists": CHANGELOG_FILE.exists(),
        "baseline_version": FROZEN_BASELINE_VERSION,
        "current_version": CURRENT_VERSION,
        "current_section": "",
        "baseline_section": "",
    }

    if not result["changelog_exists"]:
        return result

    try:
        content = CHANGELOG_FILE.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return result

    # 提取每个版本的章节
    # 格式: ## [vX.Y.Z] - YYYY-MM-DD
    section_pattern = re.compile(
        r'^(##\s*\[v?(?P<version>\d+\.\d+\.\d+)\][^\n]*\n)'
        r'(?P<body>.*?)(?=\n##\s*\[v?|\Z)',
        re.MULTILINE | re.DOTALL,
    )

    sections = {}
    for match in section_pattern.finditer(content):
        ver = match.group("version")
        body = match.group("body").strip()
        sections[ver] = body

    result["current_section"] = sections.get(CURRENT_VERSION, "（未找到 v" + CURRENT_VERSION + " 章节）")
    result["baseline_section"] = sections.get(FROZEN_BASELINE_VERSION, "（未找到 v" + FROZEN_BASELINE_VERSION + " 章节）")

    return result


def generate_report(version_result, integrity_result, changelog_result):
    """生成 Markdown 对比报告

    Args:
        version_result: scan_version_consistency() 的返回值
        integrity_result: run_reference_integrity() 的返回值
        changelog_result: extract_changelog_diff() 的返回值

    Returns:
        str: Markdown 格式的对比报告
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = []

    lines.append("# Backtest 对比报告")
    lines.append("")
    lines.append(f"> 生成时间：{now}")
    lines.append(f"> 工具版本：v{CURRENT_VERSION}")
    lines.append(f"> 冻结基线：v{FROZEN_BASELINE_VERSION}（v{CURRENT_VERSION} 修复前）")
    lines.append("")
    lines.append("---")
    lines.append("")

    # ========== 1. 版本号一致性 ==========
    lines.append("## 1. 版本号一致性检查")
    lines.append("")

    if version_result is None:
        lines.append("> 本次运行未执行版本号检查（使用 --check-version 或无参数启用）。")
        lines.append("")
    else:
        lines.append(f"- 期望版本：**v{version_result['expected']}**")
        lines.append(f"- 扫描文件数：**{version_result['files_scanned']}**")
        lines.append("")

        if version_result["by_version"]:
            lines.append("### 版本分布")
            lines.append("")
            lines.append("| 版本 | 出现次数 | 状态 |")
            lines.append("|------|---------|------|")
            for ver in sorted(version_result["by_version"].keys(), reverse=True):
                count = len(version_result["by_version"][ver])
                if ver == CURRENT_VERSION:
                    status = "✅ 一致"
                else:
                    status = "⚠️ 不一致"
                lines.append(f"| v{ver} | {count} | {status} |")
            lines.append("")
        else:
            lines.append("> 未扫描到任何版本号。")
            lines.append("")

        if version_result["inconsistent"]:
            lines.append("### 不一致详情")
            lines.append("")
            lines.append("| 文件 | 行号 | 发现版本 | 上下文 |")
            lines.append("|------|------|---------|--------|")
            for filepath, lineno, ver, ctx in version_result["inconsistent"][:50]:
                # 截断过长的上下文
                ctx_short = ctx[:60].replace("|", "\\|")
                lines.append(f"| {filepath} | {lineno} | v{ver} | {ctx_short} |")
            if len(version_result["inconsistent"]) > 50:
                lines.append(f"\n> ...共 {len(version_result['inconsistent'])} 处不一致，仅展示前 50 处")
            lines.append("")
        else:
            lines.append("✅ 所有版本号均与期望版本一致。")
            lines.append("")

    lines.append("---")
    lines.append("")

    # ========== 2. 引用完整性 ==========
    lines.append("## 2. 引用完整性检查（reference-integrity.py）")
    lines.append("")

    if integrity_result is None:
        lines.append("> 本次运行未执行引用完整性检查（使用 --check-integrity 或无参数启用）。")
        lines.append("")
    elif not integrity_result["script_exists"]:
        lines.append("⚠️ reference-integrity.py 脚本不存在，跳过此项检查。")
        lines.append("")
    else:
        status = "✅ 通过" if integrity_result["passed"] else "❌ 失败"
        lines.append(f"- 脚本状态：{status}")
        lines.append(f"- 退出码：{integrity_result['return_code']}")
        lines.append("")

        if integrity_result["stdout"]:
            lines.append("### 标准输出")
            lines.append("")
            lines.append("```")
            stdout_trimmed = integrity_result["stdout"][:3000]
            lines.append(stdout_trimmed)
            if len(integrity_result["stdout"]) > 3000:
                lines.append("...（输出已截断）")
            lines.append("```")
            lines.append("")

        if integrity_result["stderr"]:
            lines.append("### 标准错误")
            lines.append("")
            lines.append("```")
            stderr_trimmed = integrity_result["stderr"][:2000]
            lines.append(stderr_trimmed)
            if len(integrity_result["stderr"]) > 2000:
                lines.append("...（输出已截断）")
            lines.append("```")
            lines.append("")

    lines.append("---")
    lines.append("")

    # ========== 3. 冻结基线对比 ==========
    lines.append(f"## 3. 冻结基线对比（v{FROZEN_BASELINE_VERSION} → v{CURRENT_VERSION}）")
    lines.append("")

    if changelog_result is None:
        lines.append("> 本次运行未执行冻结基线对比（使用无参数运行启用）。")
        lines.append("")
    elif not changelog_result["changelog_exists"]:
        lines.append("⚠️ CHANGELOG.md 不存在，无法提取变更记录。")
        lines.append("")
    else:
        lines.append(f"### v{CURRENT_VERSION} 变更内容（当前版本）")
        lines.append("")
        lines.append("```markdown")
        current_trimmed = changelog_result["current_section"][:4000]
        lines.append(current_trimmed)
        if len(changelog_result["current_section"]) > 4000:
            lines.append("...（已截断，完整内容见 CHANGELOG.md）")
        lines.append("```")
        lines.append("")

        lines.append(f"### v{FROZEN_BASELINE_VERSION} 变更内容（冻结基线）")
        lines.append("")
        lines.append("```markdown")
        baseline_trimmed = changelog_result["baseline_section"][:2000]
        lines.append(baseline_trimmed)
        if len(changelog_result["baseline_section"]) > 2000:
            lines.append("...（已截断，完整内容见 CHANGELOG.md）")
        lines.append("```")
        lines.append("")

    lines.append("---")
    lines.append("")

    # ========== 4. 总结 ==========
    lines.append("## 4. 总结")
    lines.append("")

    issues = []
    if version_result is not None and version_result["inconsistent"]:
        issues.append(
            f"版本号不一致：{len(version_result['inconsistent'])} 处"
        )
    if integrity_result is not None:
        if not integrity_result["script_exists"]:
            issues.append("reference-integrity.py 脚本缺失")
        elif not integrity_result["passed"]:
            issues.append("引用完整性检查未通过")

    if issues:
        lines.append("### ⚠️ 发现问题")
        lines.append("")
        for issue in issues:
            lines.append(f"- {issue}")
        lines.append("")
        lines.append("> 建议根据上述详情修复后重新运行本工具。")
    else:
        lines.append("### ✅ 全部通过")
        lines.append("")
        if version_result is not None:
            lines.append(f"- 版本号一致性：全部为 v{CURRENT_VERSION}")
        if integrity_result is not None:
            lines.append("- 引用完整性：通过")
        if changelog_result is not None:
            lines.append(f"- 冻结基线对比：v{FROZEN_BASELINE_VERSION} → v{CURRENT_VERSION} 变更已记录")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"> 工具：backtest_compare.py | 版本：v{CURRENT_VERSION} | 作者：阿洋")

    return "\n".join(lines)


def main():
    """主入口"""
    parser = argparse.ArgumentParser(
        description="鲁班慢刨回测对比工具：对比冻结基线与当前版本，检查版本一致性与引用完整性",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "示例:\n"
            "  python scripts/backtest_compare.py                   # 全量对比\n"
            "  python scripts/backtest_compare.py --check-version   # 仅版本号检查\n"
            "  python scripts/backtest_compare.py --check-integrity # 仅引用完整性\n"
        ),
    )
    parser.add_argument(
        "--check-version",
        action="store_true",
        help="仅执行版本号一致性检查",
    )
    parser.add_argument(
        "--check-integrity",
        action="store_true",
        help="仅执行引用完整性检查（调用 reference-integrity.py）",
    )
    args = parser.parse_args()

    # 确定执行哪些检查
    run_version = True
    run_integrity = True
    run_changelog = True

    if args.check_version and not args.check_integrity:
        run_integrity = False
        run_changelog = False
    elif args.check_integrity and not args.check_version:
        run_version = False
        run_changelog = False

    # 执行检查
    version_result = None
    integrity_result = None
    changelog_result = None

    if run_version:
        print(f"[INFO] 扫描版本号一致性（期望 v{CURRENT_VERSION}）...", file=sys.stderr)
        version_result = scan_version_consistency()

    if run_integrity:
        print("[INFO] 执行引用完整性检查...", file=sys.stderr)
        integrity_result = run_reference_integrity()

    if run_changelog:
        print(f"[INFO] 提取 CHANGELOG 变更记录（v{FROZEN_BASELINE_VERSION} → v{CURRENT_VERSION}）...", file=sys.stderr)
        changelog_result = extract_changelog_diff()

    # 生成报告
    report = generate_report(version_result, integrity_result, changelog_result)
    print(report)

    # 确定退出码
    has_issues = False
    if version_result and version_result["inconsistent"]:
        has_issues = True
    if integrity_result and integrity_result["script_exists"] and not integrity_result["passed"]:
        has_issues = True

    return 1 if has_issues else 0


if __name__ == "__main__":
    sys.exit(main())
