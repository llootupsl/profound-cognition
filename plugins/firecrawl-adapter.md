---
name: firecrawl-adapter
description: Firecrawl 网页抓取适配器 — 将网页内容转换为 Markdown 格式
author: 阿洋
tags: [firecrawl, crawling, adapter, web-scraping]
---

<!-- 作者：阿洋 -->

# Firecrawl 适配器 (Firecrawl Adapter)

> 工具: Firecrawl (Web Crawler)
> 类型: 网页爬虫
> 配置: 零配置、零 API Key

## 反爬策略
### User-Agent 轮换
轮换列表（至少 5 个 UA）：
- Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0
- Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0
- Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0
- Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/17.2
- Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Edg/120.0.0.0
每次请求随机选择一个 UA。

### 请求间隔随机化
- 基础间隔: 2-5 秒随机
- 高负载目标: 5-10 秒随机

### 指数退避重试
- 首次失败: 等待 1 秒
- 第二次失败: 等待 2 秒
- 第三次失败: 等待 4 秒
- 第四次失败: 等待 8 秒
- 第五次失败: 放弃该 URL

### Referrer 模拟
- 搜索引擎来源: https://www.google.com/
- 社交媒体来源: https://t.co/
- 直接来源: 留空

### Cookie 管理
- 每次新会话清除 Cookie
- 不接受第三方 Cookie

---

## 激活条件

```yaml
activation:
  condition: "T02/T05 深度网页内容提取 AND Firecrawl 已安装"
  priority: "可选增强 — 替代通用 Web Search 步骤，提供更精准的网页内容提取"
  exhaust-retry: "若 Firecrawl 不可用，穷尽尝试到 Crawl4AI → 通用 Web Search"
```

---

## 爬取优先级规则

```yaml
crawl_priority:
  rule_1_academic:
    pattern: "*.edu, *.ac.*, arxiv.org, doi.org, scholar.google.com"
    priority: "高 — 学术来源优先深度提取"
    max_depth: 2

  rule_2_government:
    pattern: "*.gov, *.gov.cn, *.org"
    priority: "高 — 官方来源优先深度提取"
    max_depth: 2

  rule_3_news:
    pattern: "新闻类URL（含/news/、/article/、/report/路径）"
    priority: "中 — 新闻来源标准提取"
    max_depth: 1

  rule_4_general:
    pattern: "其他URL"
    priority: "低 — 通用来源按需提取"
    max_depth: 1

  rule_5_skip:
    pattern: "登录页面、PDF直链、视频页面、社交媒体主页"
    priority: "跳过 — 不适合爬取"
    action: "穷尽重试到搜索引擎摘要"
```

---

## 与 profound-cognition Task 节点集成

```yaml
task_integration:
  T02_L1_L2_research:
    trigger: "研究底座事实收集 — 搜索结果中存在高价值URL"
    strategy: "按爬取优先级规则选择性深度提取"
    output: "full_text_content 替代搜索摘要"
    annotation: "[firecrawl] 标签标记深度提取来源"

  T05_L6_L7_evidence:
    trigger: "证据验证 — 需要全文验证的URL来源"
    strategy: "爬取来源页面全文 + 断言匹配验证"
    output: "verification_results 注入 T05 证据层"
    annotation: "[firecrawl-verify] 标签标记验证方式"
```

---

## 错误处理

```yaml
error_handling:
  library_not_available:
    action: "穷尽重试到 Crawl4AI，若仍不可用则穷尽重试到通用 Web Search"
    log: "记录 Firecrawl 不可用事件"
    exhaust_retry_chain: "Firecrawl → Crawl4AI → Web Search → LLM内建知识"

  crawl_blocked:
    action: "切换 User-Agent 重试，穷尽重试直至成功"
    log: "记录反爬拦截事件，标注 blocked_url={url}"

  crawl_timeout:
    action: "跳过该URL，继续处理下一个"
    log: "记录超时事件，标注 timeout_url={url}"
    timeout: 30000  # ms

  empty_content:
    action: "穷尽重试到搜索引擎摘要"
    log: "记录空内容事件（可能是动态页面）"

  rate_limit:
    action: "指数退避重试（2s→4s→8s）"
    log: "记录限流事件"
```

---

## 穷尽重试策略

```yaml
exhaust_retry:
  L1_FULL:
    condition: "Firecrawl 可用 + 反爬策略正常"
    behavior: "完整深度爬取 + UA轮换 + 请求间隔随机化"

  L2_PARTIAL_DATA:
    condition: "Firecrawl 可用 + 部分URL被拦截"
    behavior: "可用URL深度提取 + 被拦截URL穷尽重试到搜索摘要"

  L3_TEXT_ONLY:
    condition: "Firecrawl 不可用"
    behavior: "穷尽尝试到 Crawl4AI/Web Search 搜索摘要 + 标注[SEARCH-SUMMARY]"

  L4_SERVICE_DOWN:
    condition: "所有爬取工具不可用"
    behavior: "使用 LLM 内建知识 + 标注[INTERNAL_REASONING]"
```
