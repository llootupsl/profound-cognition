<!-- 作者：阿洋 -->

# Agent-Reach 核心算法消费文件

> **文件**: `strategies/agent-reach-consumer.md`
> **来源项目**: [Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach)
> **能力卡编号**: TC-099
> **消费节点**: T02 研究底座、I01 补研、knowledge/search-strategy.md
> **内化日期**: 2026-06-14

---

## 一、方法论原理

Agent-Reach 是 AI Agent 的"互联网能力中间层"，其核心认知假设是——**AI Agent 的瓶颈不在推理能力，而在信息可达性。大多数 Agent 失败不是因为模型不够聪明，而是因为模型没有稳定的外部信息入口**。

Agent-Reach 的设计哲学是"脚手架而非框架"——它不参与数据流，而是提供：
1. **安装器**：一键安装所有渠道的上游工具
2. **配置器**：自动配置认证和环境
3. **诊断器**：检测所有渠道的可用状态

其核心算法可提炼为三条：
1. **多步搜索策略**：从广度发现到深度定向的渐进式搜索
2. **信息可达性评估**：14+平台渠道的可用性诊断与穷尽重试替代路由
3. **搜索深度控制规则**：根据信息缺口动态调整搜索深度

---

## 二、执行步骤

### 步骤1：渠道可用性诊断（Channel Availability Diagnosis）

```
agent-reach doctor 命令执行流程:

FOR EACH channel IN channels:
  1. 检测上游工具是否已安装
  2. 检测认证配置是否完成
  3. 执行测试查询验证功能
  4. 记录状态: AVAILABLE | PARTIAL | UNAVAILABLE

14+渠道诊断清单:
  | 渠道            | 上游工具          | 认证需求     | 诊断方法                    |
  |----------------|------------------|-------------|---------------------------|
  | Web网页         | Jina Reader      | 无          | 读取测试URL                |
  | Twitter/X      | xreach CLI       | Cookie/API  | xreach search "test"      |
  | YouTube        | yt-dlp           | 无          | 搜索测试视频               |
  | B站            | yt-dlp + bili-cli| Cookie(推荐) | 搜索测试视频              |
  | GitHub         | gh CLI           | Token       | gh search repos "test"    |
  | Reddit         | rdt-cli          | Cookie      | rdt search "test"         |
  | 小红书          | mcporter MCP     | Cookie      | 搜索测试笔记               |
  | 抖音            | mcporter MCP     | 无          | 解析测试链接               |
  | 微信公众号      | miku_ai+Camoufox | 无          | 搜索测试文章               |
  | 微博            | Jina Reader      | 无          | 读取测试URL                |
  | LinkedIn       | mcporter MCP     | Cookie      | 搜索测试档案               |
  | RSS            | feedparser       | 无          | 解析测试Feed               |
  | 全网搜索        | Exa Search       | API Key     | 搜索测试查询               |
  | 任意网页        | Jina Reader      | 无          | 读取测试URL                |

输出: 诊断报告
  ✅ AVAILABLE:  渠道名 (工具版本)
  ⚠️ PARTIAL:    渠道名 (缺失: 认证/配置)
  ❌ UNAVAILABLE: 渠道名 (原因: 工具未安装/认证失败)
```

### 步骤2：多步搜索策略（Multi-Step Search Strategy）

```
搜索策略分三步递进:

Step 1: 广度扫描（Broad Scan）
  目标: 快速获取主题概览
  执行:
    - Exa Search: 语义搜索，获取高质量文章
    - Jina Reader: 读取Top-5文章全文
    - Web搜索: 补充博客/新闻/教程
  输出: 主题概览 + 关键实体列表 + 初步来源集

Step 2: 定向深挖（Targeted Deep Dive）
  目标: 针对Step 1发现的关键实体进行深度搜索
  执行:
    - 从Step 1提取关键人物/组织/产品名
    - Twitter/X: 搜索关键人物的最新观点
    - Reddit: 搜索关键产品的社区讨论
    - GitHub: 搜索关键项目的代码和Issue
    - YouTube/B站: 搜索关键主题的视频教程
  输出: 深度证据集 + 多角度观点

Step 3: 缺口补全（Gap Completion）
  目标: 识别并填补信息缺口
  执行:
    - 分析已有证据的覆盖度
    - 识别未覆盖的维度/观点/来源
    - 针对缺口生成定向查询
    - 在未使用的渠道中搜索
  输出: 完整证据集 + 缺口闭合报告

搜索深度控制:
  | 信息缺口程度 | 搜索深度 | 行为                          |
  |------------|---------|-------------------------------|
  | 无缺口      | L1-浅层  | 仅Step 1广度扫描               |
  | 少量缺口    | L2-中层  | Step 1 + Step 2定向深挖        |
  | 大量缺口    | L3-深层  | Step 1 + Step 2 + Step 3补全  |
  | 关键缺口    | L4-穷尽  | L3 + 跨语言搜索 + 反事实搜索   |
```

### 步骤3：信息可达性评估（Information Accessibility Assessment）

```
对每条搜索结果评估其可达性等级:

可达性5级评估:
  | 等级 | 标签         | 条件                           | 置信度惩罚 |
  |-----|-------------|-------------------------------|-----------|
  | A   | FULL_ACCESS | 全文可读，无需认证，格式完整     | 0         |
  | B   | PARTIAL     | 部分可读，需登录查看完整内容     | -0.1      |
  | C   | SNIPPET     | 仅摘要/片段可读                 | -0.2      |
  | D   | METADATA    | 仅元数据（标题/日期/作者）可读   | -0.3      |
  | F   | BLOCKED     | 完全不可达（付费墙/地理封锁）    | -0.5      |

可达性提升策略:
  | 阻塞类型     | 提升策略                                    |
  |-------------|-------------------------------------------|
  | 付费墙       | 搜索相同信息的免费来源（预印本/博客/新闻）    |
  | 地理封锁     | 使用Jina Reader代理 / 配置代理节点           |
  | 登录墙       | 使用Cookie认证 / mcporter MCP               |
  | 反爬虫       | 使用Camoufox浏览器模拟 / 增加延迟            |
  | JavaScript渲染| 使用yt-dlp / Jina Reader JS渲染模式         |
  | 格式不兼容   | 使用MarkItDown转换 / 手动提取关键信息        |
```

### 步骤4：平台特定搜索协议

```
Twitter/X搜索协议:
  1. 搜索: xreach search "{query}" -n 20 --type latest --json
  2. 读推文: xreach tweet "{url}" --json
  3. 用户时间线: xreach tweets @{handle} -n 50 --json
  4. 完整线程: xreach thread "{thread_id}" --json
  认证: xreach auth set --auth-token TOKEN --ct0 CT0
        xreach auth extract --browser chrome

YouTube/B站搜索协议:
  1. 视频元数据: yt-dlp --dump-json "{url}"
  2. 字幕下载: yt-dlp --write-sub --write-auto-sub --sub-lang "zh-Hans,zh,en" --skip-download -o "/tmp/%(id)s" "{url}"
  3. 搜索: yt-dlp --dump-json "ytsearch5:{query}"
  B站特殊: --cookies-from-browser chrome（避免412）

GitHub搜索协议:
  1. 仓库搜索: gh search repos "{query}" --sort stars --limit 10
  2. 代码搜索: gh search code "{query}" --language python
  3. Issue查看: gh issue view {id} -R {repo}
  4. Issue列表: gh issue list -R {repo} --state open

小红书搜索协议:
  1. 搜索笔记: mcporter call 'xiaohongshu.search_feeds(keyword: "{query}")'
  2. 读取详情: mcporter call 'xiaohongshu.get_feed_detail(feed_id: "{id}", xsec_token: "{token}", load_all_comments: true)'

Reddit搜索协议:
  1. 搜索: rdt search "{query}" --sort hot --limit 20
  2. 读帖子: rdt read "{url}" --comments
  认证: rdt login（Cookie方式）

微信公众号搜索协议:
  1. 搜索文章: miku_ai.get_wexin_article('{query}', count=5)
  2. 读取全文: Camoufox浏览器模拟（绕过反爬虫）
  注意: 唯一可靠的反爬虫绕过方案，Jina Reader/curl都会失败

全网语义搜索协议:
  1. Exa Search: mcporter call 'exa.search_and_contents(query: "{query}", num_results: 10)'
  优势: AI优化的语义搜索，结果质量高于关键词搜索
```

### 步骤5：结果聚合与标准化

```
将异构平台结果标准化为统一格式:

标准化Schema:
  {
    "source": "twitter|youtube|github|reddit|xiaohongshu|bilibili|wechat|weibo|linkedin|rss|exa|web",
    "id": "平台唯一标识",
    "title": "标题",
    "url": "原始链接",
    "content": "正文内容（Markdown格式）",
    "author": "作者/发布者",
    "date": "发布日期（ISO 8601）",
    "engagement": {
      "views": int|null,
      "likes": int|null,
      "comments": int|null,
      "shares": int|null
    },
    "accessibility": "A|B|C|D|F",
    "metadata": {
      "platform_specific": object
    }
  }

去重规则:
  1. URL完全匹配 → 去重，保留最早来源
  2. 标题相似度 > 0.8 → 合并，保留更完整的结果
  3. 正文前200字相似度 > 0.7 → 标记可能重复，保留但降权
```

---

## 三、决策规则

### 3.1 渠道路由决策

| 条件 | 决策 | 说明 |
|------|------|------|
| 需要实时观点/讨论 | Twitter/X → Reddit | 社交平台实时性最强 |
| 需要技术深度 | GitHub → HN → YouTube | 技术社区信息密度最高 |
| 需要中文社区观点 | 小红书 → 微博 → B站 → 微信公众号 | 中文平台优先 |
| 需要学术文献 | Exa Search → Web → RSS | 学术搜索优先 |
| 需要视频内容 | YouTube → B站 | 视频平台优先 |
| 需要预测/情绪 | Polymarket → Twitter/X | 预测市场+社交媒体 |
| 目标URL已知 | Jina Reader 直接读取 | 最快路径 |

### 3.2 搜索深度决策

| 条件 | 搜索深度 | 行为 |
|------|---------|------|
| 主题为热门话题，信息丰富 | L1-浅层 | 仅广度扫描，3-5个来源 |
| 主题为中等热度，部分信息缺失 | L2-中层 | 广度+定向，10-15个来源 |
| 主题为冷门/专业领域 | L3-深层 | 广度+定向+补全，15-25个来源 |
| 主题为前沿/争议领域 | L4-穷尽 | 全渠道+跨语言+反事实，25+来源 |
| Step 1已获得足够信息 | 穷尽重试替代至L1 | 节省搜索成本 |
| Step 3仍有大量缺口 | 升级至L4 | 确保信息完整性 |

### 3.3 可达性穷尽重试替代决策

| 可达性等级 | 决策 |
|-----------|------|
| A (FULL_ACCESS) | 直接使用，无惩罚 |
| B (PARTIAL) | 使用可读部分，标注缺失内容，搜索替代来源 |
| C (SNIPPET) | 仅作为线索，必须搜索完整来源 |
| D (METADATA) | 仅用于来源发现，不作为证据 |
| F (BLOCKED) | 放弃该来源，穷尽重试替代渠道 |

### 3.4 认证配置决策

| 平台 | 认证方式 | 优先级 |
|------|---------|--------|
| Twitter/X | Cookie（auth_token+ct0）> xAI API Key | Cookie优先（免费） |
| Reddit | Cookie（rdt login）> ScrapeCreators API | Cookie优先 |
| GitHub | gh auth login（OAuth/Token） | 必须 |
| 小红书 | Cookie（Cookie-Editor导出）> mcporter | Cookie优先 |
| YouTube | 无需认证 | — |
| B站 | Cookie推荐（避免412） | 推荐 |
| 微信公众号 | 无需认证（Camoufox绕过） | — |

---

## 四、输出规范

```yaml
agent_reach_output:
  diagnosis:
    channels_available: int
    channels_partial: int
    channels_unavailable: int
    channel_details:
      - name: str
        status: "AVAILABLE|PARTIAL|UNAVAILABLE"
        tool_version: str|null
        auth_status: "configured|missing|failed"

  search_strategy:
    depth_level: "L1|L2|L3|L4"
    steps_completed: ["broad_scan", "targeted_dive", "gap_completion"]
    channels_used: [str]

  results:
    - source: str
      id: str
      title: str
      url: str
      content: str
      author: str|null
      date: str|null
      engagement:
        views: int|null
        likes: int|null
        comments: int|null
        shares: int|null
      accessibility: "A|B|C|D|F"
      confidence_penalty: float

  gap_analysis:
    identified_gaps: [str]
    closed_gaps: [str]
    remaining_gaps: [str]
    depth_upgrade_recommended: bool

  dedup_stats:
    url_dedup: int
    title_dedup: int
    content_dedup: int
```

---

## 五、与 profound-cognition 搜索策略集成

### 5.1 与 search-strategy.md 的关系

本消费文件是 `knowledge/search-strategy.md` 的深度内化补充：
- search-strategy.md 定义了多引擎聚合规则（SearXNG/Whoogle/DuckDuckGo等）
- 本消费文件补充了**社交媒体平台**的搜索能力（Twitter/Reddit/小红书/抖音/B站等）
- 本消费文件补充了**多步搜索策略**（广度→定向→补全）
- 本消费文件补充了**信息可达性评估**框架

### 5.2 渠道扩展映射

| search-strategy.md 现有渠道 | Agent-Reach 扩展渠道 | 集成方式 |
|---------------------------|---------------------|---------|
| SearXNG（元搜索） | Exa Search（语义搜索） | 并行搜索，Exa优先用于语义查询 |
| Whoogle（Google代理） | Jina Reader（网页读取） | Whoogle发现URL → Jina读取全文 |
| Crawl4AI（网页抓取） | Camoufox（反爬虫浏览器） | Crawl4AI失败 → Camoufox兜底 |
| — | Twitter/X（xreach） | 新增渠道 |
| — | Reddit（rdt-cli） | 新增渠道 |
| — | GitHub（gh CLI） | 新增渠道 |
| — | YouTube/B站（yt-dlp） | 新增渠道 |
| — | 小红书（mcporter） | 新增渠道 |
| — | 微信公众号（miku_ai） | 新增渠道 |

### 5.3 搜索深度与搜索轮次映射

| Agent-Reach 搜索深度 | profound-cognition 搜索轮次 | 来源数要求 |
|---------------------|---------------------------|-----------|
| L1-浅层 | 1轮 | 5-10 |
| L2-中层 | 2轮 | 10-15 |
| L3-深层 | 3轮（默认） | 15-25 |
| L4-穷尽 | 3+轮（穷尽重试） | 25+ |

### 5.4 穷尽重试策略

| 穷尽重试路径 | 触发条件 | 行为 |
|-------------|---------|------|
| Agent-Reach全渠道 → SearXNG聚合 | Agent-Reach不可用 | 穷尽重试替代到现有搜索策略 |
| 特定平台不可用 → 替代平台 | 某平台认证失败/被封 | 切换到功能相近的替代平台 |
| Jina Reader → Camoufox → 手动提取 | 网页读取失败 | 逐级穷尽重试替代网页读取策略 |
| Cookie认证 → API Key → 无认证 | 认证方式不可用 | 逐级穷尽重试替代认证方式，功能递减 |
| 全渠道无结果 → LLM内建知识 | 所有外部渠道失败 | 使用LLM知识，标注`internal_reasoning=true` |

> 知识来源: TC-099 Agent-Reach (Panniantong/Agent-Reach)
