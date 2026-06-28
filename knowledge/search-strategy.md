<!-- 作者：阿洋 -->

# 搜索方法论

> **版本治理元数据 (D12.4.2)**:
> - version: 1.1
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（多引擎聚合 + 查询重写 + 三角验证）
>   - v1.1 补全版本治理元数据与交叉引用（D12.4.2-D12.4.3）

## 交叉引用

- **上游**: `knowledge/research-methods.md`（九层研究底座）
- **下游**: `tasks/T02_L1_L2_research.md`（研究底座执行搜索）、`tasks/I01_iterative_deepening.md`（迭代深化补研搜索）
- **相关**: `knowledge/evidence-standards.md`（证据等级，搜索结果分级）、`knowledge/source-verification.md`（来源核实）、`knowledge/knowledge-graph-integration.md`（KG 集成，搜索补充）
- **能力卡**: TC-001-SearXNG、TC-002-Whoogle、TC-029-STORM、TC-030-GPT-Researcher、TC-032-Perplexica
- **插件**: `plugins/searxng-adapter.md`、`plugins/whoogle-adapter.md`、`plugins/duckduckgo-adapter.md`

## 1. 多引擎聚合规则

### 1.1 搜索引擎
| 引擎 | 类型 | 适用场景 |
|------|------|---------|
| SearXNG | 元搜索 | 通用搜索，聚合多引擎结果 |
| Whoogle | Google 代理 | 需要 Google 质量结果时 |
| LLM 内置搜索 | 模型搜索 | 快速概览、实时信息 |

### 1.2 聚合规则
- 跨引擎结果去重：URL 级别去重，保留最早来源
- 质量评分：域名权威度 × 内容相关性 × 时效性
- 来源标注：每条结果标注来源引擎

## 2. 查询重写规则

### 2.1 Perplexica 多角度重写
- 将原始查询重写为 3-5 个不同角度的子查询
- 每个子查询覆盖不同的语义维度

### 2.2 STORM 多视角提问
- 从不同专家视角生成提问
- 覆盖支持、反对、边界三种立场

### 2.3 反事实查询
- 搜索与核心假设相反的证据
- 格式："NOT {假设关键词}" 或 "{对立观点关键词}"

## 3. 去重标注规则

- 跨引擎结果按 URL 去重
- 保留最早来源，标注重复来源数
- 语义去重：相似度 > 0.8 的结果合并

## 4. 迭代补缺搜索规则

1. 缺口识别：从 NRSF 中识别未闭合论证链
2. 定向搜索：针对缺口生成定向查询
3. 追加 NRSF：搜索结果追加到对应 § 节
4. 循环：直到缺口闭合或质量达标

## 5. 搜索量化标准表

| 研究阶段 | 最低搜索次数 | 最低来源数 | 最低来源类型数 |
|---------|------------|-----------|-------------|
| T02 L1+L2 | 8×3=24 | 24 | 4 |
| T03 L3 | 5×3=15 | 15 | 3 |
| T04 L4+L5 | 5×3=15 | 15 | 3 |
| T05 L6+L7 | 8×3=24 | 24 | 4 |
| T06 L8+L9 | 3×3=9 | 9 | 2 |
| I01 补研 | 5×3=15 | 15 | 3 |
| T20 补研 | 2×2=4 | 4 | 1 |

## 6. 多语言搜索规则

- 默认：中文 + 英文双语搜索
- 按需第三语言：根据研究主题添加（如日语/韩语/德语/法语）
- 翻译查询：将中文查询翻译为目标语言后搜索
- 结果统一：搜索结果统一以中文记录到 NRSF

## 7. 多引擎并发搜索策略 (v3 新增)

### 7.1 并发引擎列表
同查询同时发所有可用引擎：
- SearXNG（TC-001，元搜索引擎）
- Whoogle（TC-002，隐私搜索）
- DuckDuckGo Instant Answer（即时搜索，插件适配器）
- Firecrawl（Web爬虫，插件适配器）
- GPT-Researcher（TC-030，AI搜索）
- Perplexica（TC-032，AI搜索）
- Crawl4AI（TC-003，网页抓取）

### 7.2 结果去重算法
1. URL 完全匹配 → 去重，保留最先返回的结果
2. 标题相似度 > 0.8（Levenshtein 或 Jaccard）→ 去重，保留更完整的结果
3. 正文前 200 字相似度 > 0.7 → 标记为"可能重复"，保留两者但降权

### 7.3 权威性排序规则
1. 学术来源（.edu、arxiv、scholar）→ 权重 1.0
2. 官方机构（.gov、UN、WHO）→ 权重 0.95
3. 权威媒体（Reuters、BBC、新华社）→ 权重 0.85
4. 行业报告（McKinsey、Gartner）→ 权重 0.80
5. 个人博客/论坛 → 权重 0.50

### 7.4 最少搜索轮次
- 默认 3 轮（v3 从 1 轮提高至 3 轮）
- 每轮搜索后去重并排序
- 第 3 轮仍无新结果 → 自动结束搜索阶段

---

## 8. 元搜索方法论 (TC-001 SearXNG)

### 8.1 方法论原理

元搜索的核心认知假设是——单一搜索引擎的索引覆盖率和排序算法存在系统性偏差，任何单一引擎都无法提供"全视角"的信息检索结果。SearXNG作为元搜索聚合层，将多个搜索引擎（Google/Bing/DuckDuckGo/Wikipedia等）的结果并行检索、交叉聚合，通过去重和权威性排序生成"去偏差"的综合结果集。这种方法论使我们从"信任单一引擎的排序"升级为"多引擎共识排序"——被多个引擎同时返回的结果具有更高的可信度。

> 知识来源: TC-001 [SearXNG]

### 8.2 执行步骤

1. **查询分发**：将用户查询同时发送至所有配置的搜索引擎（Google/Bing/DuckDuckGo/Qwant等），设置`categories`参数匹配查询类型（general/science/news/images）
2. **结果收集**：并行收集各引擎返回的结果，记录每条结果的来源引擎（`engine`字段）和引擎内排名（`score`字段）
3. **三级去重**：
   - L1 URL完全匹配去重：保留最早返回的结果，标注重复来源数
   - L2 标题相似度去重（Levenshtein/Jaccard > 0.8）：保留更完整的结果
   - L3 正文前200字相似度去重（> 0.7）：标记为"可能重复"，保留两者但降权
4. **权威性5级排序**：
   - Level 1（权重1.0）：学术来源（.edu、arxiv.org、scholar.google.com）
   - Level 2（权重0.95）：官方机构（.gov、un.org、who.int）
   - Level 3（权重0.85）：权威媒体（reuters.com、bbc.com、xinhuanet.com）
   - Level 4（权重0.80）：行业报告（mckinsey.com、gartner.com）
   - Level 5（权重0.50）：个人博客/论坛
5. **综合评分**：`final_score = authority_weight × relevance_score × recency_factor × engine_consensus_bonus`，其中`engine_consensus_bonus`为被N个引擎同时返回时的加成系数（N≥3: +0.3, N=2: +0.15, N=1: 0）

> 知识来源: TC-001 [SearXNG]

### 8.3 决策规则

| 条件 | 决策 |
|------|------|
| 查询涉及学术/科学主题 | 设置`categories=science`，优先触发学术搜索引擎 |
| 查询涉及实时新闻 | 设置`categories=news`，限制时间范围为最近7天 |
| 查询为多语言关键词 | 设置`language=all`，分别以中文和英文查询后合并去重 |
| SearXNG服务不可用 | 穷尽重试到Whoogle（TC-002）单引擎搜索 |
| 返回结果 < 5条 | 扩展查询词（使用同义词/上位词），重新搜索 |
| engine_consensus ≥ 3 | 结果标注为"高可信度"，优先纳入证据链 |

> 知识来源: TC-001 [SearXNG]

### 8.4 输出规范

```yaml
searxng_search_result:
  query: str
  categories: str
  total_results: int
  results:
    - title: str
      url: str
      snippet: str
      engines: [str]
      authority_level: 1-5
      final_score: float
      consensus_count: int
  dedup_stats:
    l1_url_dedup: int
    l2_title_dedup: int
    l3_content_dedup: int
```

> 知识来源: TC-001 [SearXNG]

### 8.5 穷尽重试策略

| 穷尽重试路径 | 触发条件 | 行为 |
|---------|---------|------|
| SearXNG → Whoogle | SearXNG服务超时或不可用 | 切换到Whoogle单引擎搜索，标注`exhaust-retry=whoogle` |
| Whoogle → LLM内置搜索 | Whoogle也不可用 | 使用LLM内置搜索能力，标注`exhaust-retry=llm_search, confidence_penalty=-0.3` |
| 全引擎无结果 | 所有引擎返回空 | 扩展查询词后重试1次，仍无结果则标注`search_exhausted=true` |

> 知识来源: TC-001 [SearXNG]

---

## 9. Google搜索优化方法论 (TC-002 Whoogle)

### 9.1 方法论原理

Google搜索优化的核心认知假设是——搜索引擎的查询语言是一种"受限自然语言"，通过结构化的查询重写可以显著提高检索精度。Whoogle作为Google的隐私代理层，不仅提供无追踪的搜索通道，更重要的是允许我们系统性地应用查询优化策略：将模糊的自然语言查询转化为精确的搜索指令，利用Google的高级搜索语法（site:/filetype:/intitle:/inurl:等）实现定向检索。这种方法论使我们从"自然语言提问"升级为"搜索语言编程"。

> 知识来源: TC-002 [Whoogle]

### 9.2 执行步骤

1. **查询重写5规则**：
   - 规则1（精确匹配）：将核心术语用双引号包裹 → `"大语言模型" 幻觉`
   - 规则2（站点限定）：对权威来源使用`site:`限定 → `site:arxiv.org "LLM hallucination"`
   - 规则3（排除噪声）：用`-`排除不相关结果 → `"AI安全" -"人工智能安全" -游戏`
   - 规则4（文件类型）：对学术文献使用`filetype:pdf` → `"transformer attention" filetype:pdf`
   - 规则5（标题限定）：对核心概念使用`intitle:` → `intitle:"知识图谱" 建模`
2. **时间范围过滤**：根据研究阶段设置时间范围
   - T02 L1事实收集：近1年
   - T03 L3结构分析：近3年
   - T05 L6证据层：不限时间
3. **学术搜索模式切换**：当查询涉及学术概念时，自动切换到Google Scholar模式
   - 使用scholar.google.com替代普通搜索
   - 启用引用追踪：从核心论文出发追踪前向引用和后向引用
   - 启用相关文章发现：利用Scholar的"相关文章"功能扩展文献网络

> 知识来源: TC-002 [Whoogle]

### 9.3 决策规则

| 条件 | 决策 |
|------|------|
| 查询包含学术术语 | 启用学术搜索模式，使用Google Scholar |
| 需要最新数据/新闻 | 设置时间范围为近1个月 |
| 需要历史性证据 | 不设时间限制，优先返回高引用文献 |
| 普通搜索结果质量低 | 应用查询重写规则1-5，重新搜索 |
| 需要特定格式文献 | 使用`filetype:pdf`限定 |
| Whoogle服务不可用 | 穷尽重试到LLM内置搜索 |

> 知识来源: TC-002 [Whoogle]

### 9.4 输出规范

```yaml
whoogle_search_result:
  query_original: str
  query_rewritten: str
  time_range: "year|month|week|all"
  scholar_mode: bool
  results:
    - title: str
      url: str
      snippet: str
      is_pdf: bool
      citation_count: int|null
```

> 知识来源: TC-002 [Whoogle]

### 9.5 穷尽重试策略

| 穷尽重试路径 | 触发条件 | 行为 |
|---------|---------|------|
| Whoogle → LLM内置搜索 | Whoogle服务不可用 | 使用LLM内置搜索，标注`exhaust-retry=llm_search` |
| Google Scholar → 普通搜索 | Scholar接口异常 | 使用普通搜索+`filetype:pdf`替代，标注`scholar_exhaust-retry=true` |
| 查询重写失败 | 重写后结果更差 | 穷尽尝试到原始查询，标注`rewrite_aborted=true` |

> 知识来源: TC-002 [Whoogle]

---

## 10. Web爬取方法论 (TC-003 Crawl4AI)

### 10.1 方法论原理

Web爬取的核心认知假设是——搜索引擎的摘要（snippet）仅包含网页内容的冰山一角，深度信息获取必须通过直接访问和解析原始网页。Crawl4AI作为智能爬取层，需要解决三个核心问题：(1)页面结构识别——区分导航/广告/正文/侧边栏，(2)正文提取——从复杂HTML中提取核心内容，(3)反爬策略——绕过网站的反自动化机制。这种方法论使我们从"依赖搜索摘要"升级为"直接获取全文"。

> 知识来源: TC-003 [Crawl4AI]

### 10.2 执行步骤

1. **页面结构识别算法**：
   - DOM树分析：识别`<article>`/`<main>`/`<section>`等语义标签，优先提取
   - 密度启发式：计算各DOM节点的文本密度（文字量/标签量），文本密度最高的区域为正文候选
   - 重复模式消除：识别并移除导航栏、页脚、侧边栏等重复出现的DOM结构
2. **正文提取规则**：
   - 优先提取`<article>`标签内容
   - 次选提取`role="main"`区域
   - 兜底使用文本密度算法提取最大文本块
   - 保留标题层级（h1-h6）、列表结构（ul/ol）、表格结构（table）
   - 移除`<script>`/`<style>`/`<nav>`/`<footer>`/`<aside>`标签
3. **反爬策略5维**：
   - 维度1（User-Agent轮换）：维护UA池，每次请求随机选择
   - 维度2（请求间隔）：随机延迟2-5秒，模拟人类浏览节奏
   - 维度3（JavaScript渲染）：启用`js_rendering=true`处理SPA页面
   - 维度4（Cookie处理）：自动处理会话Cookie和CSRF令牌
   - 维度5（代理轮换）：当IP被封时切换代理节点

> 知识来源: TC-003 [Crawl4AI]

### 10.3 决策规则

| 条件 | 决策 |
|------|------|
| 目标页面为SPA/动态渲染 | 启用JavaScript渲染，设置`js_rendering=true` |
| 目标页面为静态HTML | 禁用JavaScript渲染，提高爬取速度 |
| 爬取超时（>30s） | 穷尽重试到requests+BeautifulSoup，仅提取纯文本 |
| 页面需要登录 | 标注`auth_required=true`，跳过该页面 |
| 返回403/429 | 触发反爬策略，增加延迟，轮换UA和代理 |
| 正文提取质量低 | 标注`extraction_quality=low`，提示人工审核 |

> 知识来源: TC-003 [Crawl4AI]

### 10.4 输出规范

```yaml
crawl4ai_result:
  url: str
  status_code: int
  content_type: "article|list|table|mixed"
  title: str
  body_markdown: str
  extraction_quality: "high|medium|low"
  js_rendered: bool
  fetch_duration_ms: int
```

> 知识来源: TC-003 [Crawl4AI]

### 10.5 穷尽重试策略

| 穷尽重试路径 | 触发条件 | 行为 |
|---------|---------|------|
| Crawl4AI → requests+BS4 | Crawl4AI服务不可用 | 使用requests获取HTML+BeautifulSoup解析，标注`exhaust-retry=bs4` |
| requests+BS4 → LLM内置fetch | requests也无法获取 | 使用LLM内置URL获取能力，标注`exhaust-retry=llm_fetch` |
| JS渲染失败 | 页面需要JS但渲染超时 | 返回未渲染的HTML文本，标注`js_rendering_failed=true` |

> 知识来源: TC-003 [Crawl4AI]

---

## 11. 文档阅读方法论 (TC-004 Jina-Reader/MarkItDown)

### 11.1 方法论原理

文档阅读的核心认知假设是——长文档的信息密度不均匀，关键信息往往集中在特定段落（摘要、结论、方法、数据表），而非均匀分布。Jina-Reader和MarkItDown作为文档解析层，需要解决三个核心问题：(1)长文档分段——将超长文档切分为语义连贯的段落，(2)关键信息提取——从每个段落中识别和提取核心论点、数据、方法，(3)跨文档对比——在多个文档间建立信息对应关系，发现共识和分歧。这种方法论使我们从"通读全文"升级为"定向提取+结构化对比"。

> 知识来源: TC-004 [Jina-Reader/MarkItDown]

### 11.2 执行步骤

1. **长文档分段策略**：
   - 按标题层级分段：以H1/H2/H3标题为分段边界
   - 段落长度控制：每段不超过2000字（约500 tokens），保持语义完整性
   - 特殊段落识别：摘要（Abstract）、结论（Conclusion）、方法（Methodology）作为独立段落保留
   - 表格和图表单独提取，保留标题和注释
2. **关键信息提取规则**：
   - 论点提取：识别"我们认为/本研究表明/结果显示"等论点标记词
   - 数据提取：识别数值、百分比、统计指标，保留单位和上下文
   - 方法提取：识别实验设计、样本量、分析方法
   - 引用提取：识别参考文献编号和引用关系
   - 不确定性标注：识别"可能/表明/暗示/需要进一步研究"等不确定性标记
3. **跨文档对比方法**：
   - 主题对齐：按研究主题将不同文档的对应段落对齐
   - 共识识别：多个文档在相同主题上得出一致结论 → 标注为"共识"
   - 分歧识别：不同文档在相同主题上得出矛盾结论 → 标注为"分歧"，记录各方论据
   - 补充识别：某文档提供了其他文档未覆盖的信息 → 标注为"补充"

> 知识来源: TC-004 [Jina-Reader/MarkItDown]

### 11.3 决策规则

| 条件 | 决策 |
|------|------|
| 文档为PDF/DOCX/PPTX | 使用MarkItDown转换为Markdown后再处理 |
| 文档为网页URL | 使用Jina-Reader直接获取结构化内容 |
| 文档长度 > 10000字 | 启用分段策略，按标题层级切分 |
| 文档长度 < 2000字 | 整篇处理，不切分 |
| 需要对比3+篇文档 | 建立主题对齐矩阵，逐主题对比 |
| 文档格式转换失败 | 穷尽重试到纯文本提取，标注`format_loss=true` |

> 知识来源: TC-004 [Jina-Reader/MarkItDown]

### 11.4 输出规范

```yaml
document_reading_result:
  source: str
  format: "pdf|docx|html|url"
  total_length: int
  segments:
    - heading: str
      content: str
      key_findings: [str]
      data_points: [{metric: str, value: str, context: str}]
      uncertainty_markers: [str]
  cross_document_analysis:
    consensus_points: [str]
    divergence_points: [{topic: str, positions: [{source: str, position: str}]}]
    supplementary_points: [str]
```

> 知识来源: TC-004 [Jina-Reader/MarkItDown]

### 11.5 穷尽重试策略

| 穷尽重试路径 | 触发条件 | 行为 |
|---------|---------|------|
| Jina-Reader → MarkItDown | Jina-Reader服务不可用 | 先下载文档再用MarkItDown本地转换 |
| MarkItDown → pandoc | MarkItDown转换失败 | 使用pandoc作为备选转换工具 |
| pandoc → 手动解析 | pandoc也失败 | 提取纯文本，标注`extraction_method=manual, quality=low` |
| 格式转换丢失结构 | 转换后表格/图表丢失 | 标注`format_loss=true`，保留可提取的文本内容 |

> 知识来源: TC-004 [Jina-Reader/MarkItDown]


### TC-005 Mem0 记忆管理方法论

**核心步骤**：
1. 记忆写入：通过 mem0.add() 将研究片段写入记忆库，附带 task_id/timestamp/research_id 元数据
2. 记忆检索：通过 mem0.search() 语义查询相关记忆片段，top_k 默认10
3. 记忆更新：通过 mem0.update() 修正已有记忆，需提供 memory_id
4. 图增强（Mem0g）：启用实体关系图模式，提取实体和关系构建知识图谱

**决策规则**：NRSF-Summary增量管理优先使用Mem0；跨会话记忆持久化使用Mem0g图增强版

**穷尽重试策略**：Mem0 -> 本地JSON存储 -> 无记忆模式

> 知识来源: TC-005 Mem0



### TC-032 Perplexica 开源AI搜索引擎方法论

**核心步骤**：
1. 查询提交：将研究问题提交至 Perplexica 搜索引擎
2. 结果聚合：Perplexica 聚合多源搜索结果并AI摘要
3. 来源验证：对返回结果进行来源可靠性评估
4. 结果整合：将验证后的结果整合至研究上下文

**决策规则**：需要AI增强搜索摘要时使用Perplexica；纯元搜索使用SearXNG

**穷尽重试策略**：Perplexica -> SearXNG -> Whoogle -> LLM内置搜索

> 知识来源: TC-032 Perplexica



### TC-045 Crawl4AI-MCP MCP爬取方法论

**核心步骤**：
1. URL提交：通过MCP协议提交目标URL至Crawl4AI
2. 页面获取：Crawl4AI执行页面获取和渲染
3. 正文提取：自动识别页面结构并提取正文内容
4. 格式输出：返回Markdown格式清洗后内容

**决策规则**：MCP环境可用时优先使用Crawl4AI-MCP；非MCP环境使用Crawl4AI CLI

**穷尽重试策略**：Crawl4AI-MCP -> Crawl4AI CLI -> Jina-Reader -> requests+BeautifulSoup

> 知识来源: TC-045 Crawl4AI-MCP



### TC-046 MarkItDown-MCP MCP文档转换方法论

**核心步骤**：
1. 文件提交：通过MCP协议提交文档文件至MarkItDown
2. 格式识别：自动识别文档格式（PDF/DOCX/PPTX/XLSX）
3. 内容转换：将文档内容转换为Markdown格式
4. 结构保留：保留标题层级、表格、列表等结构信息

**决策规则**：MCP环境可用时优先使用MarkItDown-MCP；非MCP环境使用MarkItDown CLI

**穷尽重试策略**：MarkItDown-MCP -> MarkItDown CLI -> Jina-Reader -> 手动提取

> 知识来源: TC-046 MarkItDown-MCP

---

## 12. 跨平台多步搜索方法论 (TC-098 last30days-skill + TC-099 Agent-Reach)

> **职责边界**：本节整合 last30days-skill 的跨平台评分排序算法和 Agent-Reach 的多步搜索+可达性评估。
> last30days-skill 详细算法见 knowledge/external-capabilities/last30days-skill-consumer.md。
> Agent-Reach 详细策略见 strategies/agent-reach-consumer.md。

### 12.1 方法论原理

跨平台多步搜索的核心认知假设是——**单一搜索引擎和单一信息源都存在系统性偏差，社交媒体/专业论坛/预测市场等"围墙花园"内的信息无法通过传统搜索引擎获取，必须通过专用渠道直接访问**。last30days-skill 提供跨平台评分排序算法（30天衰减+四阶段评分+收敛检测），Agent-Reach 提供多平台搜索能力（14+渠道+多步搜索+可达性评估），两者互补形成完整的跨平台搜索方法论。

### 12.2 执行步骤

1. **渠道诊断**：执行 Agent-Reach doctor 诊断所有渠道可用性
2. **广度扫描**：在所有可用渠道并行搜索，收集初步结果
3. **时效性衰减**：对结果应用30天指数衰减模型 `score × exp(-λ × days_old)`
4. **四阶段评分**：本地相关性(55%+25%+20%) → 加权RRF融合 → LLM语义重排 → 最终评分(70%+25%+5%)
5. **定向深挖**：从广度结果提取关键实体，在特定渠道定向搜索
6. **可达性评估**：对每条结果评估可达性等级(A/B/C/D/F)，应用置信度惩罚
7. **收敛检测**：识别跨平台共识（≥3平台+0.3加成），标注高可信度
8. **缺口补全**：识别未覆盖维度，在未使用渠道中定向搜索

### 12.3 决策规则

| 条件 | 决策 |
|------|------|
| 需要实时社交讨论 | Twitter/X → Reddit（Agent-Reach渠道） |
| 需要中文社区观点 | 小红书 → 微博 → B站 → 微信公众号 |
| 需要技术深度 | GitHub → HN → YouTube |
| 内容>30天 | 标注EXPIRED，排除出报告 |
| 内容21-30天 | 标注STALE，降低权重 |
| ≥3平台共识 | 标注高可信度，优先纳入 |
| LLM不可用 | 穷尽重试替代为三信号评分（相关性70%+时效20%+来源10%） |
| 特定渠道不可用 | 切换替代渠道，标注partial_search |

### 12.4 输出规范

```yaml
cross_platform_search_output:
  channels:
    available: [str]
    partial: [str]
    unavailable: [str]
  search_depth: "L1|L2|L3|L4"
  results:
    - title: str
      url: str
      source_platform: str
      freshness: "FRESH|RECENT|NORMAL|STALE|EXPIRED"
      accessibility: "A|B|C|D|F"
      final_score: float
      consensus_count: int
  trend_analysis:
    direction: "rising|peaking|declining|stable"
    platform_convergence: [str]
```

### 12.5 穷尽重试策略

| 穷尽重试路径 | 触发条件 | 行为 |
|-------------|---------|------|
| 完整四阶段评分 → 穷尽重试替代三信号 | LLM不可用 | 使用exhaust_retry_score |
| 全渠道搜索 → 部分渠道 | 某渠道不可用 | 跳过不可用渠道，标注partial_search |
| Agent-Reach → SearXNG聚合 | Agent-Reach不可用 | 穷尽重试替代到现有搜索策略 |
| Jina Reader → Camoufox → 手动提取 | 网页读取失败 | 逐级穷尽重试替代读取策略 |
| 全渠道无结果 → LLM内建知识 | 所有外部渠道失败 | 标注internal_reasoning=true, confidence_penalty=-0.3 |

> 知识来源: TC-098 last30days-skill + TC-099 Agent-Reach
