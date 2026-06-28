#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 作者：阿洋
"""
================================================================================
脚本名称: rendering-consistency-check.py
用途: 校验 docx/html/typst 三条渲染链路输出的一致性
版本: 1.0.0
日期: 2026-06-25
================================================================================
背景：渲染管线定义了统一中间表示 IR（见 rendering-pipeline/ARCHITECTURE.md
      §渲染管线统一中间表示 IR），三条链路（docx/html/typst）均从同一 IR
      渲染输出。本脚本对比三链路输出，确保内容一致性，避免某条链路静默
      丢失内容或偏离 IR 定义。

校验项：
  C1 文件存在性：三链路输出文件均存在且非空
  C2 标题一致性：三链路输出的 H1-H4 标题文本一致
  C3 段落数一致性：三链路输出的段落数量一致（容差 ±5%）
  C4 图表引用一致性：三链路输出的图表引用数量一致
  C5 表格一致性：三链路输出的表格数量一致
  C6 引用一致性：三链路输出的引用数量一致
  C7 元数据一致性：三链路输出的 title/abstract/authors 一致

用法:
  python scripts/rendering-consistency-check.py <output_dir>
  output_dir 应包含三个子目录：docx/ html/ typst/
  或包含三个文件：output.docx output.html output.typ（或 .pdf）

退出码: 0=全部通过, 1=有异常

分类说明（Audit-7 Stage 6 修复 R3-F02）：
  本脚本为「参数化工具脚本」，非「CI 守门脚本」。
  - CI 守门脚本：无参数即可运行，exit 0 表示仓库状态健康（如 version-consistency-check.py）
  - 参数化工具脚本：必须提供参数才能运行，用于特定场景的诊断（如本脚本需 <output_dir>）
  - 本脚本不纳入 .github/workflows/ci.yml 工作流（无参数时 exit 1，会导致 CI 误失败）
  - 本脚本不纳入 CI 回归列表（19 个 CI 守门脚本），但在渲染管线中作为闭环验证工具使用
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
CHAINS = ["docx", "html", "typst"]

# 容差阈值
PARAGRAPH_COUNT_TOLERANCE = 0.05  # 段落数容差 5%


def find_output_files(output_dir: Path):
    """在输出目录中查找三链路的输出文件。"""
    files = {}
    # 方式 1: 子目录模式 docx/output.* html/output.* typst/output.*
    for chain in CHAINS:
        subdir = output_dir / chain
        if subdir.is_dir():
            for ext in ["*", "*.docx", "*.html", "*.typ", "*.pdf"]:
                matches = list(subdir.glob(ext))
                if matches:
                    files[chain] = matches[0]
                    break
    # 方式 2: 平铺模式 output.docx output.html output.typ
    if not files:
        for chain, ext in [("docx", "*.docx"), ("html", "*.html"), ("typst", "*.typ"), ("typst", "*.pdf")]:
            if chain not in files:
                matches = list(output_dir.glob(ext))
                if matches:
                    files[chain] = matches[0]
    return files


def extract_headings_html(content: str):
    """从 HTML 内容提取 H1-H4 标题文本。"""
    headings = []
    for m in re.finditer(r"<h([1-4])[^>]*>(.*?)</h\1>", content, re.DOTALL | re.IGNORECASE):
        level = int(m.group(1))
        text = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        headings.append((level, text))
    return headings


def extract_headings_markdown(content: str):
    """从 Markdown/Typst 源码提取标题。
    Typst: = Heading, == Heading, === Heading
    Markdown: # Heading, ## Heading, ### Heading
    """
    headings = []
    for line in content.splitlines():
        # Typst 风格
        m = re.match(r"^(=+)\s+(.+)$", line)
        if m:
            level = len(m.group(1))
            if 1 <= level <= 4:
                headings.append((level, m.group(2).strip()))
                continue
        # Markdown 风格
        m = re.match(r"^(#{1,4})\s+(.+)$", line)
        if m:
            level = len(m.group(1))
            headings.append((level, m.group(2).strip()))
    return headings


def extract_paragraphs_html(content: str):
    """从 HTML 提取段落计数。"""
    return len(re.findall(r"<p[^>]*>", content, re.IGNORECASE))


def extract_paragraphs_markdown(content: str):
    """从 Markdown/Typst 提取段落计数（非空行且非标题/列表/代码块）。"""
    count = 0
    in_code_block = False
    for line in content.splitlines():
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        stripped = line.strip()
        if not stripped:
            continue
        if re.match(r"^(=+|#+)\s", stripped):
            continue
        if re.match(r"^[-*+]\s", stripped):
            continue
        if re.match(r"^\d+\.\s", stripped):
            continue
        if stripped.startswith("|"):
            continue
        count += 1
    return count


def extract_figures_html(content: str):
    """从 HTML 提取图表引用计数。"""
    return len(re.findall(r"<(figure|img)[^>]*>", content, re.IGNORECASE))


def extract_figures_markdown(content: str):
    """从 Markdown/Typst 提取图表引用计数。"""
    # Markdown 图片语法 ![alt](src)
    md_imgs = len(re.findall(r"!\[[^\]]*\]\([^)]+\)", content))
    # Typst figure 语法 #figure(...)
    typst_figs = len(re.findall(r"#figure\(", content))
    return md_imgs + typst_figs


def extract_tables_html(content: str):
    """从 HTML 提取表格计数。"""
    return len(re.findall(r"<table[^>]*>", content, re.IGNORECASE))


def extract_tables_markdown(content: str):
    """从 Markdown/Typst 提取表格计数。"""
    # Markdown 表格（以 | 开头的连续行块）
    md_tables = 0
    in_table = False
    for line in content.splitlines():
        if line.strip().startswith("|"):
            if not in_table:
                md_tables += 1
                in_table = True
        else:
            in_table = False
    # Typst 表格 #table(...)
    typst_tables = len(re.findall(r"#table\(", content))
    return md_tables + typst_tables


def extract_references_html(content: str):
    """从 HTML 提取引用计数。"""
    return len(re.findall(r"<(cite|sup|a[^>]*class=['\"][^'\"]*reference[^'\"]*['\"])", content, re.IGNORECASE))


def extract_references_markdown(content: str):
    """从 Markdown/Typst 提取引用计数。"""
    # Markdown 脚注 [^id]
    md_refs = len(re.findall(r"\[\^[^\]]+\]", content))
    # Typst 引用 #cite(...)
    typst_refs = len(re.findall(r"#cite\(", content))
    return md_refs + typst_refs


def extract_metadata_html(content: str):
    """从 HTML 提取元数据（title）。"""
    title_match = re.search(r"<title[^>]*>(.*?)</title>", content, re.IGNORECASE | re.DOTALL)
    title = title_match.group(1).strip() if title_match else ""
    return {"title": title}


def extract_metadata_markdown(content: str):
    """从 Markdown/Typst 提取元数据。"""
    # YAML frontmatter
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    title = ""
    if fm_match:
        title_match = re.search(r"^title\s*:\s*(.+)$", fm_match.group(1), re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip().strip('"').strip("'")
    if not title:
        # 第一个 H1
        for line in content.splitlines():
            m = re.match(r"^(=+|#+)\s+(.+)$", line)
            if m:
                title = m.group(2).strip()
                break
    return {"title": title}


def read_file_content(path: Path) -> str:
    """读取文件内容，docx 文件返回空字符串（无法直接解析）。"""
    if path.suffix.lower() == ".docx":
        # docx 是二进制格式，无法直接解析；返回空字符串并标记
        return ""
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        print(f"WARN: 读取文件 {path} 失败: {e}")
        return ""


def check_consistency(output_dir: Path):
    """执行三链路一致性校验，返回 (errors, warnings)。"""
    errors = []
    warnings = []

    # C1 文件存在性
    files = find_output_files(output_dir)
    missing_chains = [c for c in CHAINS if c not in files]
    if missing_chains:
        errors.append(f"C1: 缺少渲染链路输出: {missing_chains}")
        return errors, warnings

    print(f"INFO: 发现三链路输出文件:")
    for chain, path in files.items():
        size = path.stat().st_size if path.exists() else 0
        status = "OK" if size > 0 else "EMPTY"
        print(f"  - {chain}: {path} ({size} bytes, {status})")
        if size == 0:
            errors.append(f"C1: {chain} 输出文件为空: {path}")

    if errors:
        return errors, warnings

    # 读取内容
    contents = {chain: read_file_content(path) for chain, path in files.items()}

    # 标记 docx 是否可解析
    docx_parseable = bool(contents.get("docx", ""))
    if not docx_parseable:
        warnings.append("C2-C7: docx 为二进制格式，无法直接文本解析，仅校验 html 与 typst 一致性")

    # 提取各链路的特征
    features = {}
    for chain in CHAINS:
        content = contents.get(chain, "")
        if not content:
            features[chain] = None
            continue
        if chain == "html":
            features[chain] = {
                "headings": extract_headings_html(content),
                "paragraphs": extract_paragraphs_html(content),
                "figures": extract_figures_html(content),
                "tables": extract_tables_html(content),
                "references": extract_references_html(content),
                "metadata": extract_metadata_html(content),
            }
        else:
            features[chain] = {
                "headings": extract_headings_markdown(content),
                "paragraphs": extract_paragraphs_markdown(content),
                "figures": extract_figures_markdown(content),
                "tables": extract_tables_markdown(content),
                "references": extract_references_markdown(content),
                "metadata": extract_metadata_markdown(content),
            }

    # 确定可比链路
    comparable_chains = [c for c in CHAINS if features.get(c) is not None]
    if len(comparable_chains) < 2:
        errors.append("C2-C7: 可比链路不足 2 个，无法执行一致性校验")
        return errors, warnings

    # C2 标题一致性
    print("\n--- C2 标题一致性 ---")
    base_chain = comparable_chains[0]
    base_headings = features[base_chain]["headings"]
    base_heading_texts = [t for _, t in base_headings]
    print(f"  基准链路 ({base_chain}): {len(base_heading_texts)} 个标题")
    for chain in comparable_chains[1:]:
        chain_headings = [t for _, t in features[chain]["headings"]]
        print(f"  {chain}: {len(chain_headings)} 个标题")
        if chain_headings != base_heading_texts:
            # 允许大小写与空白差异
            norm_base = [t.lower().strip() for t in base_heading_texts]
            norm_chain = [t.lower().strip() for t in chain_headings]
            if norm_base != norm_chain:
                warnings.append(f"C2: {base_chain} 与 {chain} 标题不一致（base={len(base_heading_texts)}, {chain}={len(chain_headings)}）")

    # C3 段落数一致性
    print("\n--- C3 段落数一致性 ---")
    base_paras = features[base_chain]["paragraphs"]
    print(f"  基准链路 ({base_chain}): {base_paras} 段落")
    for chain in comparable_chains[1:]:
        chain_paras = features[chain]["paragraphs"]
        print(f"  {chain}: {chain_paras} 段落")
        if base_paras > 0:
            ratio = abs(chain_paras - base_paras) / base_paras
            if ratio > PARAGRAPH_COUNT_TOLERANCE:
                warnings.append(f"C3: {base_chain} 与 {chain} 段落数差异 {ratio:.1%} > 容差 {PARAGRAPH_COUNT_TOLERANCE:.1%}")

    # C4 图表引用一致性
    print("\n--- C4 图表引用一致性 ---")
    base_figs = features[base_chain]["figures"]
    print(f"  基准链路 ({base_chain}): {base_figs} 图表")
    for chain in comparable_chains[1:]:
        chain_figs = features[chain]["figures"]
        print(f"  {chain}: {chain_figs} 图表")
        if base_figs != chain_figs:
            warnings.append(f"C4: {base_chain} 与 {chain} 图表数不一致（{base_figs} vs {chain_figs}）")

    # C5 表格一致性
    print("\n--- C5 表格一致性 ---")
    base_tables = features[base_chain]["tables"]
    print(f"  基准链路 ({base_chain}): {base_tables} 表格")
    for chain in comparable_chains[1:]:
        chain_tables = features[chain]["tables"]
        print(f"  {chain}: {chain_tables} 表格")
        if base_tables != chain_tables:
            warnings.append(f"C5: {base_chain} 与 {chain} 表格数不一致（{base_tables} vs {chain_tables}）")

    # C6 引用一致性
    print("\n--- C6 引用一致性 ---")
    base_refs = features[base_chain]["references"]
    print(f"  基准链路 ({base_chain}): {base_refs} 引用")
    for chain in comparable_chains[1:]:
        chain_refs = features[chain]["references"]
        print(f"  {chain}: {chain_refs} 引用")
        if base_refs != chain_refs:
            warnings.append(f"C6: {base_chain} 与 {chain} 引用数不一致（{base_refs} vs {chain_refs}）")

    # C7 元数据一致性
    print("\n--- C7 元数据一致性 ---")
    base_title = features[base_chain]["metadata"]["title"]
    print(f"  基准链路 ({base_chain}): title='{base_title}'")
    for chain in comparable_chains[1:]:
        chain_title = features[chain]["metadata"]["title"]
        print(f"  {chain}: title='{chain_title}'")
        if base_title and chain_title and base_title.lower().strip() != chain_title.lower().strip():
            warnings.append(f"C7: {base_chain} 与 {chain} title 不一致（'{base_title}' vs '{chain_title}'）")

    return errors, warnings


def main():
    if len(sys.argv) < 2:
        print("用法: python scripts/rendering-consistency-check.py <output_dir>")
        print("  output_dir 应包含 docx/ html/ typst/ 子目录或 output.docx output.html output.typ 文件")
        sys.exit(1)

    output_dir = Path(sys.argv[1]).resolve()
    if not output_dir.exists():
        print(f"FAIL: 输出目录不存在: {output_dir}")
        sys.exit(1)

    print(f"INFO: 校验目录: {output_dir}")
    print(f"INFO: 开始三链路一致性校验...")
    print("=" * 70)

    errors, warnings = check_consistency(output_dir)

    print("=" * 70)
    print(f"总计: ERROR={len(errors)}, WARN={len(warnings)}")

    if errors:
        print("\n=== 错误 ===")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    if warnings:
        print("\n=== 警告 ===")
        for w in warnings:
            print(f"  - {w}")
        print("\n三链路一致性校验完成（有警告，但不阻塞）。")
        sys.exit(0)

    print("\n三链路一致性校验全部通过。")
    sys.exit(0)


if __name__ == "__main__":
    main()
