---
name: crawl4ai-adapter
description: Crawl4AI 适配器 — 将深度网页爬取与内容提取能力注入 T02/T05 节点，替代通用 Web Search 实现更精准的信息采集
author: 阿洋
tags: [crawl4ai, web-crawl, adapter, t02, t05, markdown]
---

# Crawl4AI 适配器

## 概述

本模块为 T02（研究底座）和 T05（来源验证）节点提供 Crawl4AI 网页爬取适配器，将 Crawl4AI 的深度内容提取能力转换为 T02/T05 可消费的标准化格式。Crawl4AI 输出结构化 Markdown，相比通用 Web Search 能获取更完整、更精准的页面内容，特别适合深度研究场景中的全文提取需求。

---

## 激活条件

```yaml
activation:
  condition: "always（EXHAUST-only） AND (T02_L1_L2_research.route == always OR T05_L6_L7_evidence.route == always)"
  priority: "可选增强 — 替代通用 Web Search 步骤，提供更精准的网页内容提取"
  exhaust-retry: "若 Crawl4AI 不可用，自动穷尽尝试至通用 Web Search（Bing/Google）"
```

---

## 安装与调用

### 安装

```bash
pip install crawl4ai
```

### Python API 调用

```python
from crawl4ai import AsyncWebCrawler

async def crawl_url(url: str) -> dict:
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)
        return {
            "url": result.url,
            "markdown": result.markdown,
            "html": result.html,
            "metadata": result.metadata,
            "success": result.success,
            "status_code": result.status_code,
            "error_message": result.error_message if not result.success else None,
        }
```

### 输出格式

Crawl4AI 输出标准 Markdown 格式，保留页面结构：

```yaml
output_format:
  primary: "Markdown（结构化全文）"
  secondary: "HTML（原始页面）"
  metadata:
    - title: "页面标题"
    - description: "页面描述"
    - language: "页面语言"
    - content_type: "内容类型"
```

---

## 数据格式适配

### Crawl4AI → T02 标准格式

```yaml
adapter_pipeline:
  step_1_crawl:
    method: "调用 Crawl4AI AsyncWebCrawler 爬取目标 URL"
    input: "URL 列表（来自搜索结果或用户指定）"
    output: "crawl4ai_raw_results"
    format: "每个 URL 对应一个 Markdown 全文 + 元数据"

  step_2_extract:
    method: "从 Markdown 全文中提取与研究问题相关的内容段落"
    filter_rules:
      - "基于研究问题关键词匹配相关段落"
      - "排除导航栏、页脚、广告等噪声内容（Crawl4AI 已自动清洗）"
      - "保留结构化内容：标题层级、列表、表格、代码块"
    output: "crawl4ai_extracted_content"

  step_3_transform:
    method: "将提取的内容转换为 T02 标准 research_item 格式"
    output: "T02_compatible_research_items"
    mapping:
      research_item:
        source_url: "crawl4ai.result.url"
        title: "crawl4ai.result.metadata.title"
        content: "crawl4ai.result.markdown（相关段落）"
        content_type: "full_text"
        extraction_method: "crawl4ai"
        language: "crawl4ai.result.metadata.language"
        relevance_score: "基于研究问题计算的相关性评分（0-1）"
        credibility_flag: "verified|unverified|needs_review"
```

### Crawl4AI → T05 标准格式

```yaml
adapter_pipeline_t05:
  step_1_crawl:
    method: "对 T05 待验证来源 URL 执行深度爬取"
    input: "T05 证据链中的来源 URL"
    output: "crawl4ai_source_content"

  step_2_verify:
    method: "将爬取的全文内容与待验证断言进行匹配"
    verification_rules:
      - "在全文中搜索断言关键短语"
      - "提取上下文段落（前后各 200 字）"
      - "判断断言是否被原文支持/反驳/无关"
    output: "T05_verification_results"
    mapping:
      verification_result:
        claim: "待验证断言"
        source_url: "crawl4ai.result.url"
        source_content: "匹配的上下文段落"
        verdict: "supported|refuted|unverifiable|out_of_context"
        confidence: "验证置信度（0-1）"
        extraction_method: "crawl4ai"
```

---

## 与 T02 的集成：替代 "Web Search" 步骤

### T02 context 扩展

```yaml
T02_context:
  research_query: "用户研究问题"
  web_search:
    default_engine: "Bing/Google"
    crawl4ai_boost:
      enabled: " ∈ {DEEP, EXHAUST}"
      trigger: "搜索结果中存在高价值 URL 需要深度提取"
      data: "Crawl4AI 适配后的全文内容"
      merge_strategy: "替换 — Crawl4AI 全文内容替代搜索引擎摘要"
      annotation: "[crawl4ai] 标签标记来源，表明内容为深度提取而非搜索摘要"
```

### 集成流程

```
T02 L1 事实收集
  → Web Search 获取 URL 列表
  → Crawl4AI 深度爬取高价值 URL
  → 全文内容替代搜索摘要
  → 标注 [crawl4ai] 来源标签
```

---

## 与 T05 的集成：替代 "来源验证" 步骤

### T05 context 扩展

```yaml
T05_context:
  evidence_verification:
    default_method: "URL 访问 + 人工摘要比对"
    crawl4ai_boost:
      enabled: " ∈ {DEEP, EXHAUST}"
      trigger: "证据链中包含需要全文验证的 URL 来源"
      data: "Crawl4AI 爬取的全文内容 + 自动匹配验证结果"
      merge_strategy: "增强 — Crawl4AI 全文验证补充摘要比对"
      annotation: "[crawl4ai-verify] 标签标记验证方式"
```

### 集成流程

```
T05 L6 证据边界层
  → 证据链来源 URL 提取
  → Crawl4AI 深度爬取来源页面
  → 全文内容与断言自动匹配
  → 生成验证结果（supported/refuted/unverifiable）
  → 标注 [crawl4ai-verify] 验证方式
```

---

## 与通用 Web Search 的对比增强

```yaml
crawl4ai_enhancement:
  dimension_depth:
    description: "Crawl4AI 提取页面完整 Markdown 全文，而非搜索引擎摘要"
    advantage_over_search: "搜索引擎仅返回摘要片段，Crawl4AI 返回结构化全文——获取更完整的信息"

  dimension_structure:
    description: "Crawl4AI 保留页面的标题层级、列表、表格等结构"
    advantage_over_search: "搜索引擎摘要丢失结构信息，Crawl4AI 保留完整文档结构——便于后续分析"

  dimension_verification:
    description: "Crawl4AI 可直接爬取来源页面全文进行断言验证"
    advantage_over_search: "搜索引擎无法提供原文上下文，Crawl4AI 提供完整上下文——验证更精准"

  dimension_noise_reduction:
    description: "Crawl4AI 自动清洗导航栏、广告、页脚等噪声"
    advantage_over_search: "减少人工筛选噪声的时间，直接获取核心内容"
```

---

## 输出注入

适配后的内容注入 T02/T05 的标准数据结构：

```yaml
research_items:
  standard_source: "基于 Bing/Google 搜索的摘要结果"
  crawl4ai_supplement:
    enabled: true
    format: "Markdown 全文 + 元数据"
    merge_strategy: "替换 — 若同一 URL 同时有搜索摘要和 Crawl4AI 全文，选择 Crawl4AI 版本（更完整）"
    annotation: "[crawl4ai] 标签标记来源，方便 T05/T16 事实核查时区分来源优先级"
```

---

## API 接口约定

```yaml
crawl4ai_api:
  method: "Python AsyncWebCrawler API"
  params:
    url: "目标 URL（必需）"
    headless: true
    verbose: false
    bypass_cache: false
  rate_limit: "10 concurrent requests"
  timeout: 30000  # ms
  retry:
    max_attempts: 2
    backoff: "exponential"
```

> **注意**：Crawl4AI 需要浏览器引擎支持（Playwright/Chromium）。首次运行会自动下载浏览器，可能需要较长时间。

---

## 错误处理

```yaml
error_handling:
  library_not_available:
    action: "穷尽重试到通用 Web Search，不阻塞 T02/T05 流程"
    log: "记录 Crawl4AI 不可用事件，标注 exhaust-retry_reason=crawl4ai_not_installed"

  crawl_timeout:
    action: "跳过该 URL，继续处理下一个，不阻塞整体流程"
    log: "记录 URL 超时事件，标注 exhaust-retry_reason=crawl4ai_timeout"

  crawl_failure:
    action: "穷尽重试到通用 Web Search 获取该 URL 的摘要信息"
    log: "记录爬取失败事件，标注 exhaust-retry_reason=crawl4ai_crawl_failed"

  empty_content:
    action: "跳过该 URL，返回空内容，不合并到 research_items"
    log: "记录空内容事件（可能是动态页面或反爬策略）"

  browser_engine_missing:
    action: "穷尽重试到通用 Web Search，提示用户安装浏览器引擎"
    log: "记录浏览器引擎缺失事件，标注 exhaust-retry_reason=crawl4ai_no_browser"
```

---

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| v1.0 | 2026-05-28 | 初始发布：Crawl4AI 适配器 + T02/T05 集成方案 |

---

© 阿洋


---

## 穷尽重试策略

```yaml
exhaust_retry:
  L1_FULL:
    condition: "Crawl4AI 可用 + 浏览器引擎正常"
    behavior: "完整深度网页爬取 + Markdown全文 + 结构保留 + 噪声清洗"

  L2_PARTIAL_DATA:
    condition: "Crawl4AI 可用但部分URL爬取失败"
    behavior: "可用URL深度提取 + 失败URL穷尽重试到搜索摘要 + 标注[PARTIAL-CRAWL]"

  L3_TEXT_ONLY:
    condition: "Crawl4AI 不可用"
    behavior: "穷尽尝试到通用Web Search摘要 + 标注[SEARCH-SUMMARY]"

  L4_SERVICE_DOWN:
    condition: "所有爬取工具不可用"
    behavior: "LLM内建知识 + 标注[INTERNAL_REASONING]"
```
