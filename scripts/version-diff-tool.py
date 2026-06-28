#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 作者：阿洋
"""version-diff-tool.py — Profound Cognition 版本对比工具

对比两个 Git Tag（或提交）之间的文件变更，自动生成 Diff 报告（YAML 格式），
自动判定变更类型（PATCH/MINOR/MAJOR），并将 Diff 报告写入 docs/version_history/。

四类变更分类：
  - added（新增）：新增的文件
  - modified（修改）：修改了内容但文件仍存在
  - removed（删除）：删除的文件
  - unchanged（未变）：文件未发生变更

变更类型判定规则：
  - MAJOR：存在删除文件 或 存在破坏性变更（字段删除/语义变更）
  - MINOR：存在新增文件 或 存在修改文件（但无删除）
  - PATCH：仅修改文件内容（无新增/删除）

用法:
  python scripts/version-diff-tool.py --from v6.0.0 --to v6.1.0
  python scripts/version-diff-tool.py --from commit_a --to commit_b
  python scripts/version-diff-tool.py --from latest --to working
  python scripts/version-diff-tool.py --from v6.0.0 --to v6.1.0 --output docs/version_history/v6.1.0_diff.md

退出码:
  0 = 成功，无破坏性变更
  1 = 成功，但存在破坏性变更（需人工确认 MAJOR 版本递增）
  2 = 工具执行错误
"""

import argparse
import datetime
import os
import re
import subprocess
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
VERSION_HISTORY_DIR = PROJECT_ROOT / "docs" / "version_history"

# 扫描范围：仅对比以下目录与文件（排除 .git、node_modules、__pycache__ 等）
SCAN_PATTERNS = [
    "protocols/*.md",
    "tasks/*.md",
    "knowledge/external-capabilities/*.md",
    "knowledge/domains/*.md",
    "knowledge/thinking-models/**/*.md",
    "knowledge/*.md",
    "output/*.md",
    "plugins/*.md",
    "persona/*.md",
    "persona/*.yaml",
    "scripts/*.py",
    "docs/**/*.md",
    "SKILL.md",
    "README.md",
    "CHANGELOG.md",
    "FIELD-DEPENDENCY-GRAPH.md",
    "asr-rules.yaml",
]

# 排除模式
EXCLUDE_PATTERNS = [
    ".git/",
    "node_modules/",
    "__pycache__/",
    "*.pyc",
    ".DS_Store",
    "docs/version_history/*_diff.md",  # 排除历史 Diff 报告自身
]


def run_git(args, cwd=PROJECT_ROOT):
    """执行 git 命令并返回输出。"""
    try:
        result = subprocess.run(
            ["git"] + args,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if result.returncode != 0:
            print(f"[git 错误] {' '.join(args)}: {result.stderr}", file=sys.stderr)
            return None
        return result.stdout.strip()
    except FileNotFoundError:
        print("[错误] 未找到 git 命令，请确保 git 已安装并在 PATH 中", file=sys.stderr)
        return None
    except Exception as e:
        print(f"[git 异常] {e}", file=sys.stderr)
        return None


def resolve_ref(ref):
    """将引用解析为 Git commit hash。

    支持：
    - Tag 名（v6.0.0）
    - commit hash（短或长）
    - "latest"：最新 Tag
    - "working"：当前工作区
    """
    if ref == "working":
        return "working"
    if ref == "latest":
        # 获取最新 Tag
        latest = run_git(["describe", "--tags", "--abbrev=0"])
        if latest is None:
            # 无 Tag 时使用 HEAD
            return run_git(["rev-parse", "HEAD"])
        return latest
    # 验证 ref 是否存在
    verify = run_git(["rev-parse", "--verify", ref])
    if verify is None:
        print(f"[错误] 无法解析引用: {ref}", file=sys.stderr)
        return None
    return ref


def get_file_list_at_ref(ref):
    """获取指定 ref 处的文件列表（仅扫描范围内的文件）。"""
    if ref == "working":
        # 工作区：使用 git ls-files
        output = run_git(["ls-files"])
    else:
        # 指定 ref：使用 git ls-tree
        output = run_git(["ls-tree", "-r", "--name-only", ref])

    if output is None:
        return set()

    files = set()
    for line in output.splitlines():
        line = line.strip()
        if not line:
            continue
        # 检查是否在扫描范围内
        if _matches_scan_pattern(line) and not _matches_exclude_pattern(line):
            files.add(line)
    return files


def _matches_scan_pattern(filepath):
    """检查文件是否匹配扫描范围。"""
    for pattern in SCAN_PATTERNS:
        # 简单的 glob 匹配
        if _glob_match(pattern, filepath):
            return True
    return False


def _glob_match(pattern, filepath):
    """简化的 glob 匹配（支持 * 和 **）。"""
    # 将 glob 模式转为正则
    regex = pattern
    regex = regex.replace(".", "\\.")
    regex = regex.replace("**/", "(.*/)?")
    regex = regex.replace("*", "[^/]*")
    regex = "^" + regex + "$"
    return re.match(regex, filepath) is not None


def _matches_exclude_pattern(filepath):
    """检查文件是否匹配排除模式。"""
    for pattern in EXCLUDE_PATTERNS:
        if _glob_match(pattern, filepath):
            return True
    return False


def get_file_content_at_ref(ref, filepath):
    """获取指定 ref 处的文件内容。"""
    if ref == "working":
        path = PROJECT_ROOT / filepath
        if not path.exists():
            return None
        try:
            return path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            return None
    else:
        output = run_git(["show", f"{ref}:{filepath}"])
        return output


def compute_diff(from_ref, to_ref):
    """对比两个 ref 的文件变更，返回 Diff 结果。"""
    from_files = get_file_list_at_ref(from_ref)
    to_files = get_file_list_at_ref(to_ref)

    added = sorted(to_files - from_files)
    removed = sorted(from_files - to_files)
    common = sorted(from_files & to_files)

    modified = []
    unchanged = []

    for filepath in common:
        from_content = get_file_content_at_ref(from_ref, filepath)
        to_content = get_file_content_at_ref(to_ref, filepath)

        if from_content is None and to_content is None:
            continue
        elif from_content is None or to_content is None:
            # 一侧无法读取，视为修改
            modified.append(filepath)
        elif from_content != to_content:
            modified.append(filepath)
        else:
            unchanged.append(filepath)

    return {
        "added": added,
        "modified": modified,
        "removed": removed,
        "unchanged": unchanged,
    }


def detect_breaking_changes(diff_result, from_ref, to_ref):
    """检测破坏性变更。

    破坏性变更判定规则：
    1. 删除了文件（removed 非空）
    2. 删除了协议章节（需对比文件内容，检测章节标题消失）
    3. 字段语义变更（需人工确认，工具仅基于文件删除判定）
    """
    breaking = []

    # 规则 1：删除文件
    for filepath in diff_result["removed"]:
        breaking.append({
            "path": filepath,
            "type": "file",
            "description": f"删除文件: {filepath}",
            "reason": "文件删除属于破坏性变更",
            "migration": "需确认是否有下游依赖，提供迁移方案",
        })

    # 规则 2：检测章节删除（对比修改文件的章节标题）
    for filepath in diff_result["modified"]:
        from_content = get_file_content_at_ref(from_ref, filepath)
        to_content = get_file_content_at_ref(to_ref, filepath)
        if from_content is None or to_content is None:
            continue

        from_sections = _extract_section_headers(from_content)
        to_sections = _extract_section_headers(to_content)

        removed_sections = from_sections - to_sections
        for section in removed_sections:
            breaking.append({
                "path": f"{filepath}#{section}",
                "type": "section",
                "description": f"删除章节: {section}（文件: {filepath}）",
                "reason": "章节删除可能属于破坏性变更",
                "migration": "需确认章节内容是否迁移到其他位置",
            })

    return breaking


def _extract_section_headers(content):
    """从 Markdown 内容中提取章节标题（## 和 ### 级别）。"""
    sections = set()
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("## ") or line.startswith("### "):
            # 去除 Markdown 标记和锚点
            section = line.lstrip("#").strip()
            sections.add(section)
    return sections


def determine_change_type(diff_result, breaking_changes):
    """判定变更类型（PATCH/MINOR/MAJOR）。

    判定规则：
    - MAJOR：存在破坏性变更（删除文件或删除章节）
    - MINOR：存在新增文件（但无破坏性变更）
    - PATCH：仅修改文件内容（无新增/删除）
    """
    if breaking_changes:
        return "MAJOR"
    if diff_result["added"]:
        return "MINOR"
    if diff_result["modified"]:
        return "PATCH"
    return "PATCH"  # 默认


def generate_diff_report(from_ref, to_ref, diff_result, breaking_changes, change_type):
    """生成 Diff 报告（YAML 格式）。"""
    now = datetime.datetime.now().isoformat()

    # 生成变更摘要
    summary_parts = []
    if diff_result["added"]:
        summary_parts.append(f"新增 {len(diff_result['added'])} 个文件")
    if diff_result["modified"]:
        summary_parts.append(f"修改 {len(diff_result['modified'])} 个文件")
    if diff_result["removed"]:
        summary_parts.append(f"删除 {len(diff_result['removed'])} 个文件")
    release_notes = "；".join(summary_parts) if summary_parts else "无变更"

    # 构建 YAML
    lines = [
        "version_diff_report:",
        f"  from_version: \"{from_ref}\"",
        f"  to_version: \"{to_ref}\"",
        f"  change_type: \"{change_type}\"",
        f"  release_date: \"{now}\"",
        f"  release_notes: \"{release_notes}\"",
        "",
        "  summary:",
        f"    total_files_changed: {len(diff_result['added']) + len(diff_result['modified']) + len(diff_result['removed'])}",
        f"    added: {len(diff_result['added'])}",
        f"    modified: {len(diff_result['modified'])}",
        f"    removed: {len(diff_result['removed'])}",
        f"    unchanged: {len(diff_result['unchanged'])}",
        "",
        "  changes:",
    ]

    # added
    lines.append("    added:")
    for filepath in diff_result["added"]:
        lines.append(f"      - path: \"{filepath}\"")
        lines.append(f"        type: \"file\"")
        lines.append(f"        description: \"新增文件: {filepath}\"")
        lines.append(f"        related_requirement: \"\"")

    # modified
    lines.append("    modified:")
    for filepath in diff_result["modified"]:
        lines.append(f"      - path: \"{filepath}\"")
        lines.append(f"        type: \"file\"")
        lines.append(f"        description: \"修改文件: {filepath}\"")
        lines.append(f"        related_requirement: \"\"")

    # removed
    lines.append("    removed:")
    for filepath in diff_result["removed"]:
        lines.append(f"      - path: \"{filepath}\"")
        lines.append(f"        type: \"file\"")
        lines.append(f"        description: \"删除文件: {filepath}\"")
        lines.append(f"        reason: \"需确认删除原因\"")
        lines.append(f"        migration: \"需提供迁移方案\"")

    # unchanged（仅列出关键文件，非全部列举）
    lines.append("    unchanged:")
    # 仅列出关键配置文件
    key_files = ["SKILL.md", "README.md", "CHANGELOG.md"]
    for filepath in diff_result["unchanged"]:
        if filepath in key_files:
            lines.append(f"      - path: \"{filepath}\"")
            lines.append(f"        type: \"file\"")
            lines.append(f"        description: \"未修改\"")

    # breaking_changes
    lines.append("")
    lines.append("  breaking_changes:")
    if breaking_changes:
        for bc in breaking_changes:
            lines.append(f"      - path: \"{bc['path']}\"")
            lines.append(f"        description: \"{bc['description']}\"")
            lines.append(f"        reason: \"{bc['reason']}\"")
            lines.append(f"        migration: \"{bc['migration']}\"")
    else:
        lines.append("    []  # 无破坏性变更")

    # audit
    lines.append("")
    lines.append("  audit:")
    lines.append(f"    generated_by: \"version-diff-tool.py\"")
    lines.append(f"    timestamp: \"{now}\"")

    return "\n".join(lines)


def print_console_summary(diff_result, breaking_changes, change_type):
    """打印控制台摘要。"""
    print("=" * 60)
    print("版本对比结果摘要")
    print("=" * 60)
    print(f"\n变更类型判定: {change_type}")
    print(f"\n变更统计:")
    print(f"  新增文件: {len(diff_result['added'])}")
    print(f"  修改文件: {len(diff_result['modified'])}")
    print(f"  删除文件: {len(diff_result['removed'])}")
    print(f"  未变文件: {len(diff_result['unchanged'])}")

    if diff_result["added"]:
        print(f"\n新增文件列表:")
        for f in diff_result["added"]:
            print(f"  + {f}")

    if diff_result["modified"]:
        print(f"\n修改文件列表:")
        for f in diff_result["modified"]:
            print(f"  ~ {f}")

    if diff_result["removed"]:
        print(f"\n删除文件列表:")
        for f in diff_result["removed"]:
            print(f"  - {f}")

    if breaking_changes:
        print(f"\n⚠️  破坏性变更警告（{len(breaking_changes)} 项）:")
        for bc in breaking_changes:
            print(f"  ⚠ {bc['description']}")
        print(f"\n建议: 本次变更包含破坏性变更，建议递增 MAJOR 版本号。")

    print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Profound Cognition 版本对比工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python scripts/version-diff-tool.py --from v6.0.0 --to v6.1.0
  python scripts/version-diff-tool.py --from latest --to working
  python scripts/version-diff-tool.py --from v6.0.0 --to v6.1.0 --output custom_diff.md
        """,
    )
    parser.add_argument(
        "--from",
        dest="from_ref",
        required=True,
        help='起始版本/提交（Tag名、commit hash、"latest"=最新Tag、"working"=工作区）',
    )
    parser.add_argument(
        "--to",
        dest="to_ref",
        required=True,
        help='目标版本/提交（Tag名、commit hash、"latest"=最新Tag、"working"=工作区）',
    )
    parser.add_argument(
        "--output",
        dest="output",
        default=None,
        help="输出文件路径（默认: docs/version_history/{to_ref}_diff.md）",
    )

    args = parser.parse_args()

    # 解析引用
    from_ref = resolve_ref(args.from_ref)
    to_ref = resolve_ref(args.to_ref)

    if from_ref is None:
        print(f"[错误] 无法解析 --from 引用: {args.from_ref}", file=sys.stderr)
        return 2
    if to_ref is None:
        print(f"[错误] 无法解析 --to 引用: {args.to_ref}", file=sys.stderr)
        return 2

    print(f"[信息] 对比: {from_ref} → {to_ref}")

    # 计算差异
    diff_result = compute_diff(from_ref, to_ref)

    # 检测破坏性变更
    breaking_changes = detect_breaking_changes(diff_result, from_ref, to_ref)

    # 判定变更类型
    change_type = determine_change_type(diff_result, breaking_changes)

    # 生成 Diff 报告
    diff_report = generate_diff_report(from_ref, to_ref, diff_result, breaking_changes, change_type)

    # 确定输出路径
    if args.output:
        output_path = PROJECT_ROOT / args.output
    else:
        # 默认输出到 docs/version_history/
        VERSION_HISTORY_DIR.mkdir(parents=True, exist_ok=True)
        # 清理 to_ref 中的特殊字符作为文件名
        safe_name = re.sub(r"[^a-zA-Z0-9._-]", "_", str(to_ref))
        output_path = VERSION_HISTORY_DIR / f"{safe_name}_diff.md"

    # 写入文件
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(diff_report, encoding="utf-8")
        print(f"[信息] Diff 报告已写入: {output_path}")
    except Exception as e:
        print(f"[错误] 写入 Diff 报告失败: {e}", file=sys.stderr)
        return 2

    # 打印控制台摘要
    print_console_summary(diff_result, breaking_changes, change_type)

    # 返回退出码
    if breaking_changes:
        return 1  # 破坏性变更
    return 0


if __name__ == "__main__":
    sys.exit(main())
