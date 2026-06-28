---
name: markitdown-adapter
description: MarkItDown 适配器 — 将用户上传的各类文档（PDF/DOCX/PPTX/XLSX 等）自动转换为 Markdown 格式，注入 T02 研究底座
author: 阿洋
tags: [markitdown, document-conversion, adapter, t02, markdown]
---

# MarkItDown 适配器

## 概述

本模块为 T02（研究底座）节点提供 MarkItDown 文档转换适配器，将用户上传的各类文档（PDF、DOCX、PPTX、XLSX、HTML、图片等）自动转换为 Markdown 格式，作为 T02 研究底座的输入。MarkItDown 由 Microsoft 开源，支持多种文档格式的统一转换，是用户文档自动化的核心引擎。

---

## 激活条件

```yaml
activation:
  condition: "用户上传文档 AND T02_L1_L2_research.route == always"
  priority: "必需 — 用户上传文档必须转换为 Markdown 才能进入研究管线"
  exhaust-retry: "若 MarkItDown 不可用，尝试 Pandoc 转换 → 手动提取文本 → 提示用户上传 Markdown 格式"
```

---

## 安装与调用

### 安装

```bash
pip install markitdown
```

### CLI 调用

```bash
# 转换 PDF
markitdown path/to/file.pdf

# 转换 DOCX
markitdown path/to/file.docx

# 转换 PPTX
markitdown path/to/file.pptx

# 转换 XLSX
markitdown path/to/file.xlsx

# 转换 HTML
markitdown path/to/file.html

# 输出到文件
markitdown path/to/file.pdf > output.md
```

### Python API 调用

```python
from markitdown import MarkItDown

md = MarkItDown()

def convert_document(file_path: str) -> dict:
    result = md.convert(file_path)
    return {
        "file_path": file_path,
        "markdown": result.text_content,
        "title": result.title if hasattr(result, "title") else None,
        "success": True,
    }
```

---

## 支持的文档格式

```yaml
supported_formats:
  documents:
    - extension: ".pdf"
      description: "PDF 文档"
      quality: "高（保留段落结构和表格）"
    - extension: ".docx"
      description: "Microsoft Word 文档"
      quality: "高（完整保留格式）"
    - extension: ".pptx"
      description: "Microsoft PowerPoint 演示文稿"
      quality: "中（提取幻灯片文本和备注）"
    - extension: ".xlsx"
      description: "Microsoft Excel 电子表格"
      quality: "中（转换为 Markdown 表格）"
    - extension: ".html"
      description: "HTML 网页"
      quality: "高（保留语义结构）"
    - extension: ".csv"
      description: "CSV 数据文件"
      quality: "高（转换为 Markdown 表格）"
    - extension: ".json"
      description: "JSON 数据文件"
      quality: "中（格式化输出）"
    - extension: ".xml"
      description: "XML 数据文件"
      quality: "中（提取文本内容）"
    - extension: ".zip"
      description: "ZIP 压缩包"
      quality: "中（遍历内部文件逐一转换）"
    - extension: ".txt"
      description: "纯文本文件"
      quality: "高（直接输出）"
    - extension: ".md"
      description: "Markdown 文件"
      quality: "高（直接透传）"
```

---

## 数据格式适配

### MarkItDown → T02 标准格式

```yaml
adapter_pipeline:
  step_1_convert:
    method: "调用 MarkItDown 将上传文档转换为 Markdown"
    input: "用户上传文件路径"
    output: "markdown_content"
    format: "标准 Markdown 文本"

  step_2_structure:
    method: "解析 Markdown 结构，提取标题层级、段落、表格、列表"
    extraction_rules:
      - "H1-H4 标题映射为 T02 事实层级"
      - "表格数据提取为结构化事实条目"
      - "列表项提取为独立事实条目"
      - "段落文本提取为描述性事实"
    output: "structured_facts"

  step_3_transform:
    method: "将结构化事实转换为 T02 标准 research_item 格式"
    output: "T02_compatible_research_items"
    mapping:
      research_item:
        source_file: "原始文件名"
        source_type: "文件扩展名"
        content: "Markdown 转换后的文本内容"
        content_type: "document_upload"
        extraction_method: "markitdown"
        title: "文档标题（从 H1 或元数据提取）"
        relevance_score: "基于研究问题计算的相关性评分（0-1）"
        credibility_flag: "needs_review（用户上传文档需验证）"
```

---

## 与 T02 的集成：用户上传文档自动转 Markdown

### 集成流程

```yaml
T02_integration:
  trigger: "用户上传文档到研究项目"
  step_1_detect:
    method: "检测上传文件的格式"
    supported: "PDF/DOCX/PPTX/XLSX/HTML/CSV/JSON/XML/TXT/MD"
    unsupported: "提示用户转换为支持的格式"

  step_2_convert:
    method: "调用 MarkItDown 将文档转换为 Markdown"
    command: "markitdown {file_path}"
    output: "markdown_content"

  step_3_inject:
    method: "将 Markdown 内容注入 T02 L1 事实收集流程"
    injection_point: "T02_L1_L2_research.fact_collection"
    annotation: "[markitdown] 标签标记来源为用户上传文档"

  step_4_validate:
    method: "对转换后的内容进行质量检查"
    checks:
      - "文本完整性：关键段落是否完整提取"
      - "表格准确性：数值数据是否正确转换"
      - "结构保留：标题层级是否正确映射"
```

### T02 context 扩展

```yaml
T02_context:
  document_upload:
    enabled: true
    supported_formats: ["pdf", "docx", "pptx", "xlsx", "html", "csv", "json", "xml", "txt", "md"]
    conversion_method: "markitdown"
    auto_inject: true
    inject_target: "L1 基础事实层"
    annotation: "[markitdown] 标签标记文档转换来源"
    credibility_default: "needs_review"
```

---

## 转换质量规范

```yaml
quality_standards:
  text_integrity:
    requirement: "关键段落完整提取，不丢失核心内容"
    validation: "对比原文和转换结果的字数差异，差异 > 20% 需警告"

  table_accuracy:
    requirement: "表格数据正确转换，数值无误差"
    validation: "检查 Markdown 表格行列数与原文一致"

  structure_preservation:
    requirement: "标题层级正确映射（H1→H1, H2→H2...）"
    validation: "检查标题层级不跳级"

  encoding:
    requirement: "UTF-8 编码，BOM 禁止"
    validation: "检查输出文件编码"

  metadata:
    requirement: "保留文档元数据（标题、作者、日期）"
    validation: "检查 YAML frontmatter 中的元数据字段"
```

---

## 错误处理

```yaml
error_handling:
  library_not_available:
    action: "穷尽重试到 Pandoc 转换"
    log: "记录 MarkItDown 不可用事件，标注 exhaust-retry_reason=markitdown_not_installed"
    exhaust_retry_chain: "MarkItDown → Pandoc → 手动提取文本 → 提示用户上传 Markdown"

  unsupported_format:
    action: "提示用户转换为支持的格式"
    log: "记录不支持的格式事件，标注 unsupported_format={extension}"

  conversion_failure:
    action: "尝试 Pandoc 转换，若仍失败则提示用户"
    log: "记录转换失败事件，标注 failed_file={file_path}"

  empty_output:
    action: "警告用户文档可能为空或为扫描版 PDF"
    log: "记录空输出事件，标注 empty_file={file_path}"

  encoding_error:
    action: "尝试多种编码（UTF-8, GBK, GB2312, Big5）重新读取"
    log: "记录编码错误事件，标注 exhaust-retry_encoding={encoding}"

  file_too_large:
    action: "分块处理大文件"
    log: "记录文件过大事件，标注 file_size={size}"
    max_size: "50MB"
```

---

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| v1.0 | 2026-05-28 | 初始发布：MarkItDown 适配器 + T02 集成方案 + 格式支持列表 |

---

© 阿洋


---

## 穷尽重试策略

```yaml
exhaust_retry:
  L1_FULL:
    condition: "MarkItDown 可用 + 所有格式支持正常"
    behavior: "完整文档→Markdown转换 + 结构保留 + 元数据提取"

  L2_PARTIAL_DATA:
    condition: "MarkItDown 可用但部分格式转换质量低"
    behavior: "可用格式正常转换 + 低质量格式穷尽重试到Pandoc + 标注[PARTIAL-FORMAT]"

  L3_TEXT_ONLY:
    condition: "MarkItDown 不可用"
    behavior: "穷尽尝试到 Pandoc转换/手动提取 + 标注[PANDOC-INTERNAL_REASONING]"

  L4_SERVICE_DOWN:
    condition: "所有文档转换工具不可用"
    behavior: "提示用户上传Markdown格式 + 标注[MANUAL-CONVERSION]"
```
