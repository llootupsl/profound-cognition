#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 作者：阿洋
"""version-consistency-check.py — Profound Cognition 版本号一致性校验脚本

扫描全仓库中承载版本号的文件，提取版本号并检测是否全部一致。
真相源版本号取自 SKILL.md frontmatter 的 version 字段。

扫描的文件与提取模式：
  1. SKILL.md                        — YAML frontmatter `version: X.Y.Z`
  2. README.md                       — badge URL `version-X.Y.Z-blueviolet`
  3. persona/persona-init-protocol.md — 标题 `vX.Y.Z`
  4. persona/persona-schema.yaml     — 注释 `vX.Y.Z`
  5. .claude-plugin/marketplace.json — JSON `"version": "X.Y.Z"`（2 处）

用法: python scripts/version-consistency-check.py
退出码: 0=全部一致, 1=存在不一致
"""

import json
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

# Semver 正则（可选 v 前缀）
SEMVER_RE = re.compile(r"v?(\d+\.\d+\.\d+)")


def _norm(version_str):
    """归一化版本号：去除 v 前缀，返回 X.Y.Z。"""
    m = SEMVER_RE.search(version_str)
    if m:
        return m.group(1)
    return version_str.strip().lstrip("v")


def extract_skill_md_version(path):
    """从 SKILL.md YAML frontmatter 提取 version 字段。"""
    if not path.exists():
        return None, "文件不存在"
    text = path.read_text(encoding="utf-8")
    # frontmatter 在首对 --- 之间
    m = re.search(r"^---\s*\n(.*?)\n---\s*$", text, re.MULTILINE | re.DOTALL)
    if not m:
        return None, "未找到 YAML frontmatter"
    fm = m.group(1)
    vm = re.search(r"^version:\s*(\S+)\s*$", fm, re.MULTILINE)
    if not vm:
        return None, "frontmatter 中未找到 version 字段"
    return _norm(vm.group(1)), None


def extract_readme_badge_version(path):
    """从 README.md badge URL 提取版本号。"""
    if not path.exists():
        return None, "文件不存在"
    text = path.read_text(encoding="utf-8")
    # 匹配 version-X.Y.Z-blueviolet
    m = re.search(r"badge/version-([0-9]+\.[0-9]+\.[0-9]+)-", text)
    if not m:
        return None, "未找到 version badge"
    return _norm(m.group(1)), None


def extract_header_vversion(path):
    """从文件标题提取 vX.Y.Z 形式版本号。"""
    if not path.exists():
        return None, "文件不存在"
    text = path.read_text(encoding="utf-8")
    # 取前 5 行查找 vX.Y.Z
    head = "\n".join(text.split("\n")[:5])
    m = re.search(r"v([0-9]+\.[0-9]+\.[0-9]+)", head)
    if not m:
        return None, "前 5 行未找到 vX.Y.Z"
    return _norm(m.group(1)), None


def extract_marketplace_versions(path):
    """从 marketplace.json 提取所有 version 字段值。"""
    if not path.exists():
        return [], "文件不存在"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return [], f"JSON 解析失败: {e}"
    versions = []
    # metadata.version
    meta = data.get("metadata", {})
    if isinstance(meta, dict) and "version" in meta:
        versions.append(("metadata.version", _norm(str(meta["version"]))))
    # plugins[].version
    plugins = data.get("plugins", [])
    if isinstance(plugins, list):
        for i, p in enumerate(plugins):
            if isinstance(p, dict) and "version" in p:
                versions.append((f"plugins[{i}].version", _norm(str(p["version"]))))
    return versions, None


def main():
    print("=" * 60)
    print("Profound Cognition — 版本号一致性校验")
    print("=" * 60)

    # 真相源：SKILL.md
    skill_md = PROJECT_ROOT / "SKILL.md"
    readme = PROJECT_ROOT / "README.md"
    persona_init = PROJECT_ROOT / "persona" / "persona-init-protocol.md"
    persona_schema = PROJECT_ROOT / "persona" / "persona-schema.yaml"
    marketplace = PROJECT_ROOT / ".claude-plugin" / "marketplace.json"

    canonical, err = extract_skill_md_version(skill_md)
    if err:
        print(f"[ERROR] 无法从 SKILL.md 提取真相源版本号: {err}")
        sys.exit(2)
    print(f"\n[真相源] SKILL.md version = {canonical}")

    findings = []  # (file, location, version, ok)
    findings.append(("SKILL.md", "frontmatter.version", canonical, True))

    # README.md
    v, e = extract_readme_badge_version(readme)
    if e:
        print(f"[WARN] README.md: {e}")
        findings.append(("README.md", "badge", "N/A", False))
    else:
        findings.append(("README.md", "badge", v, v == canonical))

    # persona-init-protocol.md
    v, e = extract_header_vversion(persona_init)
    if e:
        print(f"[WARN] persona-init-protocol.md: {e}")
        findings.append(("persona/persona-init-protocol.md", "header", "N/A", False))
    else:
        findings.append(("persona/persona-init-protocol.md", "header", v, v == canonical))

    # persona-schema.yaml
    v, e = extract_header_vversion(persona_schema)
    if e:
        print(f"[WARN] persona-schema.yaml: {e}")
        findings.append(("persona/persona-schema.yaml", "header", "N/A", False))
    else:
        findings.append(("persona/persona-schema.yaml", "header", v, v == canonical))

    # marketplace.json
    versions, e = extract_marketplace_versions(marketplace)
    if e:
        print(f"[WARN] marketplace.json: {e}")
        findings.append((".claude-plugin/marketplace.json", "json", "N/A", False))
    else:
        for loc, v in versions:
            findings.append((".claude-plugin/marketplace.json", loc, v, v == canonical))

    # 输出结果
    print(f"\n[扫描] 共检查 {len(findings)} 处版本号声明")
    print("-" * 60)
    inconsistent = []
    for file, loc, ver, ok in findings:
        status = "✅" if ok else "❌"
        print(f"  {status} {file:45s} {loc:25s} = {ver}")
        if not ok:
            inconsistent.append((file, loc, ver))

    print("-" * 60)
    if inconsistent:
        print(f"\n❌ 版本号不一致: {len(inconsistent)} 处与真相源 ({canonical}) 不符")
        for file, loc, ver in inconsistent:
            print(f"   - {file} [{loc}]: {ver} (应为 {canonical})")
        print("\n" + "=" * 60)
        sys.exit(1)
    else:
        print(f"\n✅ 版本号一致性校验通过: 全部为 {canonical}")
        print("=" * 60)
        sys.exit(0)


if __name__ == "__main__":
    main()
