#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 作者：阿洋
"""knowledge-expiry-check.py — Profound Cognition 知识文件过期检测脚本

扫描 knowledge/ 目录下的知识文件（排除 domains/、thinking-models/、external-capabilities/，
这些由其他子代理处理），提取版本治理元数据中的 last_updated 字段，
检测超过 2 年未更新的文件并标记为「待复审」。

依据 D12.4.4 知识文件过期检测机制：
  - 知识文件必须包含版本治理元数据（version/last_updated/maintainer/changelog）
  - last_updated 字段格式：YYYY-MM-DD
  - 超过 730 天（2 年）未更新的文件标记为 STALE_REVIEW_REQUIRED
  - 超过 365 天（1 年）未更新的文件标记为 AGING_NOTICE

扫描范围：
  knowledge/*.md
  knowledge/thinking-templates/*.md
  knowledge/tool-availability/*.md
  （排除 knowledge/domains/、knowledge/thinking-models/、knowledge/external-capabilities/）

用法: python scripts/knowledge-expiry-check.py
退出码: 0=全部在有效期内, 1=存在过期文件, 2=脚本错误
"""

import re
import sys
from datetime import datetime, date
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

# 过期阈值（天）
AGING_THRESHOLD_DAYS = 365      # 1 年：老化提醒
STALE_THRESHOLD_DAYS = 730      # 2 年：待复审

# last_updated 字段正则（匹配 last_updated: 2026-06-05 等格式）
# 支持 YAML front matter 和正文中的元数据块
LAST_UPDATED_RE = re.compile(
    r'last_updated["\']?\s*[:：]\s*["\']?(\d{4}-\d{2}-\d{2})["\']?',
    re.IGNORECASE
)

# 备用：从「最后更新」字段提取（中文）
LAST_UPDATED_CN_RE = re.compile(
    r'最后更新["\']?\s*[:：]\s*["\']?(\d{4}-\d{2}-\d{2})["\']?',
    re.IGNORECASE
)

# 备用：从「更新日期」字段提取（中文）
UPDATE_DATE_CN_RE = re.compile(
    r'更新日期["\']?\s*[:：]\s*["\']?(\d{4}-\d{2}-\d{2})["\']?',
    re.IGNORECASE
)


def collect_knowledge_files():
    """收集需要扫描的知识文件（排除 domains/、thinking-models/、external-capabilities/）"""
    files = []
    if not KNOWLEDGE_DIR.exists():
        return files

    # 1. knowledge/ 根目录下的 .md 文件
    for md_file in KNOWLEDGE_DIR.glob("*.md"):
        files.append(md_file)

    # 2. knowledge/ 下的子目录（排除指定目录）
    for subdir in KNOWLEDGE_DIR.iterdir():
        if not subdir.is_dir():
            continue
        if subdir.name in EXCLUDED_SUBDIRS:
            continue
        for md_file in subdir.rglob("*.md"):
            files.append(md_file)

    return sorted(files)


def extract_last_updated(content):
    """从文件内容中提取 last_updated 日期。

    返回: (date_obj, raw_string) 或 (None, None)
    """
    # 优先匹配 last_updated
    m = LAST_UPDATED_RE.search(content)
    if not m:
        m = LAST_UPDATED_CN_RE.search(content)
    if not m:
        m = UPDATE_DATE_CN_RE.search(content)
    if not m:
        return None, None

    raw = m.group(1)
    try:
        d = datetime.strptime(raw, "%Y-%m-%d").date()
        return d, raw
    except ValueError:
        return None, raw


def days_since(date_obj, reference_date):
    """计算从 date_obj 到 reference_date 的天数差"""
    return (reference_date - date_obj).days


def main():
    print("=" * 70)
    print("Profound Cognition — 知识文件过期检测（D12.4.4）")
    print("=" * 70)

    if not KNOWLEDGE_DIR.exists():
        print(f"[ERROR] knowledge/ 目录不存在: {KNOWLEDGE_DIR}")
        sys.exit(2)

    files = collect_knowledge_files()
    print(f"\n[扫描] 共发现 {len(files)} 个知识文件")
    print(f"[阈值] AGING ≥ {AGING_THRESHOLD_DAYS} 天（1 年），STALE ≥ {STALE_THRESHOLD_DAYS} 天（2 年）")
    print(f"[排除] 子目录: {', '.join(sorted(EXCLUDED_SUBDIRS))}")
    print("-" * 70)

    today = date.today()
    findings = []  # (rel_path, last_updated, days_old, status)
    missing_metadata = []
    stale_files = []
    aging_files = []

    for kf in files:
        rel_path = kf.relative_to(PROJECT_ROOT).as_posix()
        try:
            content = kf.read_text(encoding="utf-8")
        except Exception as e:
            print(f"  [WARN] {rel_path}: 读取失败 ({e})")
            findings.append((rel_path, None, None, "READ_ERROR"))
            continue

        last_updated, raw = extract_last_updated(content)
        if last_updated is None:
            findings.append((rel_path, None, None, "MISSING_METADATA"))
            missing_metadata.append(rel_path)
            continue

        days_old = days_since(last_updated, today)
        if days_old >= STALE_THRESHOLD_DAYS:
            status = "STALE_REVIEW_REQUIRED"
            stale_files.append((rel_path, last_updated.isoformat(), days_old))
        elif days_old >= AGING_THRESHOLD_DAYS:
            status = "AGING_NOTICE"
            aging_files.append((rel_path, last_updated.isoformat(), days_old))
        else:
            status = "FRESH"

        findings.append((rel_path, last_updated.isoformat(), days_old, status))

    # 输出结果
    for rel_path, last_updated, days_old, status in findings:
        if status == "READ_ERROR":
            print(f"  ❌ {rel_path:55s} [读取失败]")
        elif status == "MISSING_METADATA":
            print(f"  ⚠️  {rel_path:55s} [缺少 last_updated 元数据]")
        elif status == "STALE_REVIEW_REQUIRED":
            print(f"  🔴 {rel_path:55s} last_updated={last_updated} ({days_old} 天前) → 待复审")
        elif status == "AGING_NOTICE":
            print(f"  🟡 {rel_path:55s} last_updated={last_updated} ({days_old} 天前) → 老化提醒")
        else:
            print(f"  ✅ {rel_path:55s} last_updated={last_updated} ({days_old} 天前)")

    print("-" * 70)
    print(f"[结果] 共检查 {len(findings)} 个文件")
    print(f"   - FRESH (在有效期内): {sum(1 for _, _, _, s in findings if s == 'FRESH')}")
    print(f"   - AGING_NOTICE (1-2 年): {len(aging_files)}")
    print(f"   - STALE_REVIEW_REQUIRED (>2 年): {len(stale_files)}")
    print(f"   - MISSING_METADATA (缺少元数据): {len(missing_metadata)}")

    if missing_metadata:
        print(f"\n[警告] 以下文件缺少 last_updated 元数据（需补全版本治理元数据）:")
        for f in missing_metadata:
            print(f"   - {f}")

    if stale_files:
        print(f"\n[待复审] 以下文件超过 2 年未更新，需立即复审:")
        for f, d, days in stale_files:
            print(f"   - {f} (last_updated={d}, {days} 天前)")

    if aging_files:
        print(f"\n[老化提醒] 以下文件 1-2 年未更新，建议安排复审:")
        for f, d, days in aging_files:
            print(f"   - {f} (last_updated={d}, {days} 天前)")

    print("=" * 70)

    # 退出码：存在过期文件或缺少元数据则返回 1
    if stale_files or missing_metadata:
        sys.exit(1)
    else:
        print("✅ 知识文件过期检测通过：无过期文件，无缺失元数据")
        sys.exit(0)


if __name__ == "__main__":
    main()
