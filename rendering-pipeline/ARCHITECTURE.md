<!-- 作者：阿洋 -->

# 渲染管道架构 (Rendering Pipeline Architecture)

> 全局审美总控: Taste-Skill
> 容器底座: html-ppt-skill
> 所有绘图/图表/动效能力原子化挂载于此底座

## 13 个 Skills 分类层级

### 一、全局审美内核（品味总开关）
| Skill | 角色 | 消费节点 | 内化状态 |
|-------|------|---------|---------|
| Taste-Skill | 全局审美总控，生成视觉DNA，管控所有渲染输出 | T20a/T20b/T20c/T27 | ★核心算法已内化于 rendering-pipeline/taste-skill-consumer.md |

**Taste-Skill 内化规则摘要**（完整规则见 `taste-skill-consumer.md`）：

1. **三旋钮系统**：DESIGN_VARIANCE(1-10) / MOTION_INTENSITY(1-10) / VISUAL_DENSITY(1-10)，默认基线 8/6/4
   - DV 控制布局对称性（1=完美对称 → 10=艺术性混乱）
   - MI 控制动效强度（1=静态 → 10=电影级编排）
   - VD 控制信息密度（1=艺术画廊 → 10=驾驶舱）

2. **Brief Inference**：生成代码前必须先输出 Design Read 声明，提取6维信号（page_kind/vibe_words/reference_signals/audience/brand_assets/quiet_constraints）

3. **反Slop规则**（强制禁止）：
   - 禁止Inter字体用于Premium/Creative场景 → 替代: Geist/Outfit/Cabinet Grotesk/Satoshi
   - 禁止AI Purple/Blue审美（紫色光晕、霓虹渐变）
   - 禁止纯黑#000000 → 替代: Off-Black/Zinc-950
   - DV>4时禁止居中英雄区 → 替代: 分屏/不对称布局
   - 禁止h-screen → 替代: min-h-[100dvh]
   - 禁止width/height动画 → 仅允许transform+opacity
   - 禁止代码中emoji → 替代: Phosphor/Radix Icons
   - 禁止em-dash在标题中

4. **仲裁逻辑**：硬冲突以visual_dna原始值为准拒绝覆盖；软冲突取最接近值；优先级 output_type > content_theme > target_audience

5. **设计系统映射**：Microsoft→Fluent UI, UK公共服务→GOV.UK, Google→Material 3, Apple→HIG, 其他→原生CSS+Tailwind

**Taste-Skill 全局审美总控子模块**：

1. DLP 检索器（dlp-retriever.md）— 从 16 个 DLP 中检索最匹配的设计语言（DLP 库索引详见 `design-language-profiles/README.md`）
2. ASR 硬门（asr-hard-gate.md）— 44 条禁令的强制前置门禁
3. Golden Set 校验（golden-set-validator.md）— 48 个 Golden 样本的距离校验
4. 五维门禁审查（taste-validator.md）— 排版/审美/配图/语义一致性/品牌 DNA 一致性五维评分
5. 熔断机制（fuse-mechanism.md）— 满分追求 + 质量驱动终止（连续 2 次重试分数提升 < 1 分即终止，无硬性重试次数上限，符合 EXHAUST 模式四大铁律）+ 质量保持为最高分方案

**原子库（Atomic Libraries）**：

1. typography-atoms.md（TA 排版原子库）— 30 个原子，CSS+Typst 双轨
2. layout-atoms.md（LA 布局原子库）— 24 个原子，HTML+CSS/Typst 双轨
3. visual-creative-atoms.md（VCA 视觉创意原子库）— 26 个原子，SVG/Canvas/Matplotlib 模板

### 二、PPT 生成类
| Skill | 角色 | 消费节点 |
|-------|------|---------|
| guizang-ppt-skill | 代码化PPT设计，杂志/瑞士风顶级排版 | T20a (PPT子类型) |
| html-ppt-skill | HTML幻灯片容器底座，36套主题 | T20a (PPT子类型) |
| Anthropic PPTX Skill | 原生.pptx输出，含QA校验 | T20a (Office交付) |

### 三、学术手绘/结构化绘图类
| Skill | 角色 | 消费节点 |
|-------|------|---------|
| PaperBanana Skill | 顶刊级学术插图生成（**v2.0 代码生成版**，原专有 API 已废弃） | T27 (配图) |
| excalidraw-skill | 手绘风格示意图 | T27 (配图) |
| SketchAgent (MIT) | 序列手绘生成，逐笔动画 | T27 (配图) |

### 四、数据可视化类
| Skill | 角色 | 消费节点 |
|-------|------|---------|
| data-viz-plots Skill | Nature/Cell级学术图表 | T27 (配图) |
| Markdown Viewer Skills | 多引擎可视化，9500+图标 | T27 (配图) |

### 五、动效/动画类
| Skill | 角色 | 消费节点 |
|-------|------|---------|
| GSAP 官方 Skills | Web动效引擎，60fps丝滑 | T27 (动效) |
| vibe-motion/skills | 预调校动效包，直接调用 | T27 (动效) |
| Animotion MCP Skill | 745+ CSS动画 + 9500+ 图标 | T27 (动效) |

## 熔合方案
以 Taste-Skill 为全局审美总控，以 html-ppt-skill 为容器底座，所有绘图/图表/动效能力原子化挂载。
---

## 渲染文件分层按需加载策略（R6-01）

> **目的**：将渲染管道 14 个核心文件 + 16 个 DLP 文件的加载从"全量预载"改为"三层按需加载"，降低上下文窗口占用，提升渲染启动速度。加载决策由 output_type 与渲染需求驱动。

### 三层加载架构

| 层级 | 名称 | 加载时机 | 文件集 |
|------|------|---------|--------|
| **L0 必载层** | 每次渲染必载 | 渲染管道启动时无条件加载 | `visual-dna.md`、`ARCHITECTURE.md`（本文件） |
| **L1 类型层** | 按 output_type 加载 | T20a/T20b/T20c 节点启动时按成品类型加载 | 见下方 L1 类型层文件矩阵 |
| **L2 按需层** | 渲染需求驱动加载 | 渲染过程中触发特定需求时按需加载 | `motion-semantic-match.md`、`fuse-mechanism.md`、`golden-set-validator.md` |

### L0 必载层（每次渲染必载）

| 文件 | 用途 | 加载理由 |
|------|------|---------|
| `rendering-pipeline/ARCHITECTURE.md` | 渲染管道架构总览 | 全局架构参照，所有渲染节点的入口 |
| `rendering-pipeline/visual-dna.md` | 视觉DNA生成规范 | 配色/字体/栅格/线条/动效全量参数，所有渲染的视觉基线 |

### L1 类型层（按 output_type 加载）

#### research_report — 加载全部（全量集）

> research_report 为 EXHAUST 模式默认形态，渲染管道全部文件强制加载。

| 文件 | 用途 |
|------|------|
| `semantic-auto-detect.md` | 语义自动识别规则 |
| `layout-grid.md` | 统一12列栅格排版系统 |
| `taste-skill-consumer.md` | Taste-Skill 消费器（三旋钮系统） |
| `dlp-retriever.md` | DLP 检索器 |
| `asr-hard-gate.md` | ASR 硬门禁用清单 |
| `taste-validator.md` | 五维门禁审查器 |
| `typography-atoms.md` | TA 排版原子库 |
| `layout-atoms.md` | LA 布局原子库 |
| `visual-creative-atoms.md` | VCA 视觉创意原子库 |
| `design-language-profiles/` | DLP 设计语言画像库（16 DLP + README.md 索引） |

#### wechat_article — 加载精简集

> wechat_article 为轻量输出，跳过 DLP 检索与视觉创意原子库（公众号排版不需要学术级 DLP 匹配与高级视觉创意），保留核心排版与硬门能力。

| 文件 | 用途 |
|------|------|
| `semantic-auto-detect.md` | 语义自动识别规则 |
| `layout-grid.md` | 统一12列栅格排版系统 |
| `taste-skill-consumer.md` | Taste-Skill 消费器（三旋钮系统） |
| `asr-hard-gate.md` | ASR 硬门禁用清单 |
| `typography-atoms.md` | TA 排版原子库 |
| `layout-atoms.md` | LA 布局原子库 |

#### course_material — 加载教学集

> course_material 需要幻灯片排版与视觉创意（教学图示），但不需要五维门禁审查器（教学场景审美门槛低于学术报告）。

| 文件 | 用途 |
|------|------|
| `semantic-auto-detect.md` | 语义自动识别规则 |
| `layout-grid.md` | 统一12列栅格排版系统 |
| `taste-skill-consumer.md` | Taste-Skill 消费器（三旋钮系统） |
| `dlp-retriever.md` | DLP 检索器 |
| `typography-atoms.md` | TA 排版原子库 |
| `layout-atoms.md` | LA 布局原子库 |
| `visual-creative-atoms.md` | VCA 视觉创意原子库 |

### L2 按需层（渲染需求驱动加载）

| 文件 | 用途 | 加载触发条件 |
|------|------|-------------|
| `motion-semantic-match.md` | 动效语义匹配规则 | 渲染输出含动效需求（如 HTML 交互式幻灯片、Web 演示）时加载；纯静态 PDF/Markdown 输出不加载 |
| `fuse-mechanism.md` | 熔断机制（满分追求 + 质量驱动终止，无硬性重试次数上限） | 首次渲染完成后审美评分未达标、需要触发质量重试时加载；首次渲染即满分时不加载 |
| `golden-set-validator.md` | Golden Set 距离校验器（48 样本 × 4 维距离度量） | 需要金标准距离校验时加载（research_report 默认加载，wechat_article/course_material 按需加载） |

### 加载日志写入 execution_ledger

每次渲染管道加载文件时，必须向 `execution_ledger` 写入加载日志条目，记录加载层级、文件列表、加载时间戳，供审计追溯。

```yaml
rendering_load_log:
  node_id: "T20a"                    # 或 T20b/T20c
  output_type: "research_report"     # research_report | wechat_article | course_material
  load_timestamp: "2026-06-25T10:30:00+08:00"
  layers_loaded:
    L0_required:                     # L0 必载层
      - file: "rendering-pipeline/ARCHITECTURE.md"
        status: "loaded"
      - file: "rendering-pipeline/visual-dna.md"
        status: "loaded"
    L1_by_type:                      # L1 类型层（按 output_type 加载）
      - file: "rendering-pipeline/semantic-auto-detect.md"
        status: "loaded"
      - file: "rendering-pipeline/layout-grid.md"
        status: "loaded"
      # ... 其余 L1 文件
    L2_on_demand:                    # L2 按需层（按渲染需求加载）
      - file: "rendering-pipeline/motion-semantic-match.md"
        status: "loaded"             # loaded | skipped
        trigger: "motion_required"   # 加载触发原因（skipped 时为 "not_required"）
      - file: "rendering-pipeline/fuse-mechanism.md"
        status: "skipped"
        trigger: "not_required"      # 首次渲染即满分，无需熔断
      - file: "rendering-pipeline/golden-set-validator.md"
        status: "loaded"
        trigger: "research_report_default"
  total_files_loaded: 12             # 实际加载数
  total_files_skipped: 3             # 跳过加载数
  load_strategy: "R6-01 三层按需加载"
```

**日志写入规则**：
1. **写入时机**：渲染管道加载阶段完成后、渲染执行开始前，写入 execution_ledger
2. **写入位置**：execution_ledger 中对应渲染节点（T20a/T20b/T20c）的条目下
3. **L0 必载层**：始终记录为 `status: "loaded"`
4. **L1 类型层**：按 output_type 加载的文件记录为 `status: "loaded"`，未加载的文件不记录（仅记录实际加载的文件）
5. **L2 按需层**：无论加载与否均记录，`status: "loaded"` 或 `status: "skipped"`，并记录 `trigger` 原因
6. **审计追溯**：加载日志可用于追溯渲染过程中是否遗漏必要文件，以及按需层文件的加载决策依据

---

## 名片卡设计方法论

### LC-025 D3.js 设计方法论

#### 方法论原理
D3.js 是渲染管道中最高自由度的可视化引擎，采用数据绑定-DOM操作-过渡动画的声明式范式。其核心设计原理是数据驱动文档，通过 data().join() 模式将数据数组绑定到 DOM 元素选择集，自动处理 enter/update/exit 三种状态，实现数据变化到视觉变化的精确映射。D3.js 不提供预设图表类型，而是提供构建图表的原子化工具（比例尺、轴、形状生成器、地理投影），使渲染管道能够生成 ECharts/Plotly 无法覆盖的高级图表（力导向图、桑基图、旭日图、和弦图、自定义地理可视化）。

#### 执行步骤
1. 数据预处理：将原始数据转换为 D3 友好格式（JSON/CSV->d3.group/d3.rollup 聚合）
2. 比例尺选择：根据数据类型选择比例尺（定量->d3.scaleLinear/Log/Pow，序数->d3.scaleOrdinal/Band，时间->d3.scaleTime）
3. 布局计算：选择布局算法（力导向->d3.forceSimulation，层次->d3.hierarchy+d3.tree/cluster/partition，网络->d3.chord/sankey）
4. SVG 渲染：通过 data().join() 模式绑定数据到 SVG 元素
5. 交互绑定：添加 d3.brush/d3.zoom/d3.drag 交互行为
6. 过渡动画：使用 d3.transition() 实现数据更新时的平滑过渡

#### 决策规则
- 图表类型为力导向图/桑基图/旭日图/和弦图/自定义地理 -> D3.js
- 图表类型为标准折线/柱状/饼图/散点图 -> ECharts/Plotly（不使用D3）
- 数据规模节点 > 500 -> Canvas 渲染替代 SVG
- 交互需求需要拖拽/缩放/框选 -> D3.js（原生支持）
- 交互需求仅需悬停/提示 -> ECharts/Plotly（更便捷）

#### 输出规范
chart_type: force_directed|sankey|sunburst|chord|custom; data_binding: enter/update/exit counts; interaction: drag|zoom|brush|none; rendering: svg|canvas; visual_dna_compliance: FULL|PARTIAL

#### 穷尽重试策略
- D3.js -> ECharts：标准图表类型且无自定义需求
- ECharts -> 表格：渲染环境不可用
- SVG -> Canvas：数据量 > 500 节点
- Canvas -> 静态图：Canvas 不可用

> 知识来源: LC-025 D3.js

---

### LC-029 guizang-ppt-skill 设计方法论

#### 方法论原理
guizang-ppt-skill 是渲染管道中 PPT 输出的高端排版引擎，采用代码化设计范式，将 PPT 的每个视觉元素建模为代码对象，通过编程方式精确控制位置、大小、样式和动画。其核心设计原理是杂志/瑞士国际主义风格——强网格对齐、大字标题、高对比度、留白呼吸感、极简装饰。

#### 执行步骤
1. 内容解析：将 T22-T26 综合叙事产出解析为幻灯片结构
2. 版式选择：根据内容类型匹配瑞士/杂志风版式模板（全图型/左右分栏/大字标题/数据面板）
3. 栅格对齐：所有元素严格对齐 12 列栅格系统，间距遵循 4px 基准
4. 字体注入：从 visual_dna 读取字体方案，注入标题/正文字体
5. 配色注入：从 visual_dna 读取配色方案，生成幻灯片主题色
6. 代码生成：生成 PPTX 代码（python-pptx 或 HTML 幻灯片代码）
7. QA 校验：检查栅格对齐、字体一致性、配色合规性

#### 决策规则
- 需要杂志/瑞士风顶级排版 -> guizang-ppt-skill
- 需要36套主题快速切换 -> html-ppt-skill
- 需要原生.pptx Office交付 -> Anthropic PPTX Skill
- 需要HTML交互式幻灯片 -> html-ppt-skill
- 需要.pptx文件 -> guizang-ppt-skill 或 Anthropic PPTX

#### 输出规范
slide_count: int; style: swiss|magazine|minimal; grid_compliance: PASS|FAIL; visual_dna_compliance: FULL|PARTIAL; format: pptx|html

#### 穷尽重试策略
- guizang -> html-ppt-skill：python-pptx 环境不可用
- html-ppt-skill -> Markdown：HTML 渲染环境不可用
- 杂志风 -> 简约风：内容过于复杂无法适配杂志版式

> 知识来源: LC-029 guizang-ppt-skill

---

### LC-031 html-ppt-skill 设计方法论

#### 方法论原理
html-ppt-skill 是渲染管道的 PPT 容器底座，采用 HTML 幻灯片范式，将每张幻灯片渲染为一个 HTML 页面。其核心设计原理是容器+主题分离——html-ppt-skill 提供统一的幻灯片容器（页面切换、导航、全屏、进度条），而视觉风格由 36 套主题 CSS 完全控制。作为容器底座，html-ppt-skill 是其他渲染能力的挂载点。

#### 执行步骤
1. 主题选择：从 visual_dna 的配色方案映射到 36 套主题中最接近的一套
2. 容器初始化：创建 HTML 幻灯片容器，加载主题 CSS 和导航 JS
3. 内容分页：将文档内容按 H1/H2 标题分割为幻灯片
4. 组件挂载：将图表/插图/动效嵌入对应幻灯片
5. 栅格适配：所有组件对齐 16:9（1920x1080）栅格系统
6. 交互绑定：添加幻灯片切换、全屏、进度条等交互

#### 决策规则
- 需要交互式 Web 演示 -> html-ppt-skill
- 需要离线 .pptx 文件 -> Anthropic PPTX
- 需要杂志级排版 -> guizang-ppt-skill
- 主题选择由 visual_dna 配色方案自动匹配

#### 输出规范
slide_count: int; theme: string; components_mounted: list; navigation: keyboard|click|swipe; format: html

#### 穷尽重试策略
- html-ppt -> Anthropic PPTX：需要离线交付
- html-ppt -> Markdown 幻灯片：浏览器环境不可用
- 36 主题 -> 默认主题：主题匹配失败

> 知识来源: LC-031 html-ppt-skill

---

### LC-032 Anthropic-PPTX 设计方法论

#### 方法论原理
Anthropic-PPTX Skill 是渲染管道的原生 Office 交付引擎，采用 .pptx 原生输出范式，直接生成符合 Office Open XML 标准的 .pptx 文件。其核心设计原理是原生格式+QA校验——生成 .pptx 后自动执行质量校验（栅格对齐、字体嵌入、配色合规、幻灯片尺寸），确保输出文件在 PowerPoint/Keynote/WPS 中完美呈现。

#### 执行步骤
1. 内容解析：将文档内容解析为幻灯片结构
2. 模板选择：从 visual_dna 配色方案生成 .pptx 主题
3. 元素布局：使用 python-pptx 将文本框/图片/图表/表格精确定位
4. 字体嵌入：将 visual_dna 字体方案嵌入 .pptx 文件
5. 动画添加：添加 PowerPoint 原生切换动画
6. QA 校验：自动检查栅格对齐、字体一致性、配色合规、文件完整性
7. 文件输出：生成 .pptx 文件

#### 决策规则
- 需要离线 .pptx 文件 -> Anthropic-PPTX
- 需要 Web 交互演示 -> html-ppt-skill
- QA 校验不通过 -> 退回修正，持续重试直至通过
- 需要复杂 CSS/JS 动画 -> html-ppt-skill

#### 输出规范
file_path: string; slide_count: int; qa_result: PASS|FAIL; qa_issues: list; theme: string; format: pptx

#### 穷尽重试策略
- Anthropic-PPTX -> html-ppt-skill：python-pptx 不可用
- .pptx -> PDF：PowerPoint 兼容性问题
- QA 持续重试直至通过：输出带警告的 .pptx，标注已知问题

> 知识来源: LC-032 Anthropic-PPTX

---

### LC-034 Markdown-Viewer 设计方法论

#### 方法论原理
Markdown Viewer Skills 是渲染管道的多引擎可视化工具，采用 Markdown 原生渲染+图标增强范式。其核心设计原理是轻量级可视化——不需要 ECharts/D3 等重型可视化库，仅通过 Markdown 语法+9500+ 图标库（FontAwesome/Material Icons/Tabler Icons）+简单 CSS 即可实现高质量的可视化输出。

#### 执行步骤
1. Markdown 解析：将原始 Markdown 解析为 AST
2. 图标匹配：扫描文本关键词，自动匹配 9500+ 图标库中的语义图标
3. 样式注入：从 visual_dna 读取配色/字体方案，注入 CSS 变量
4. 组件渲染：渲染标题/段落/列表/表格/代码块/引用块
5. 图标嵌入：将匹配的图标以 SVG 方式嵌入对应位置
6. 输出格式化：生成格式化的 HTML/PDF/Markdown 输出

#### 决策规则
- 轻量级文档可视化+图标增强 -> Markdown Viewer
- 交互式数据图表 -> ECharts/Plotly
- 学术论文配图 -> data-viz-plots
- 需要 9500+ 图标库 -> Markdown Viewer

#### 输出规范
format: html|pdf|markdown; icons_used: int; visual_dna_compliance: FULL|PARTIAL; icon_libraries: fontawesome+material+tabler

#### 穷尽重试策略
- 图标增强 -> 纯 Markdown：图标库不可用
- HTML -> 纯文本：渲染环境不可用
- PDF -> HTML：PDF 生成失败

> 知识来源: LC-034 Markdown-Viewer


### TC-006 DeerFlow 并行编排方法论

**核心步骤**：
1. 任务分组：将DAG任务分配至4个并行组（G1-G4）
2. 并行执行：Orchestrator调度各并行组同时执行
3. 结果收集：收集各并行组的执行结果
4. 部分失败处理：对部分失败的任务执行穷尽尝试或重试

**决策规则**：DAG中存在可并行任务时使用DeerFlow；串行依赖链使用标准Orchestrator

**穷尽重试策略**：DeerFlow -> 串行Orchestrator -> 手动执行

> 知识来源: TC-006 DeerFlow



### TC-007 Typst 学术排版方法论

**核心步骤**：
1. 源码编写：使用Typst标记语言编写文档源码
2. 字体配置：指定中文字体路径确保中文排版
3. 编译输出：通过typst.compile()生成PDF/SVG/PNG
4. 质量校验：检查排版结果是否符合学术规范

**决策规则**：WeasyPrint不可用时使用Typst作为备选排版引擎；LaTeX需求使用Tectonic

**穷尽重试策略**：Typst -> WeasyPrint -> HTML

> 知识来源: TC-007 Typst



### TC-008 VMPrint 中文学术排版方法论

**核心步骤**：
1. 模板选择：选择中文学术出版模板（academic_cn等）
2. 排版配置：配置GB/T 7714引用格式、中文页眉页脚
3. 编译输出：生成符合中文学术规范的PDF/HTML
4. 规范校验：检查引用格式、目录生成、页眉页脚

**决策规则**：中文学术出版排版优先使用VMPrint；通用排版使用WeasyPrint

**穷尽重试策略**：VMPrint -> WeasyPrint -> HTML

> 知识来源: TC-008 VMPrint



### TC-012 Tectonic LaTeX编译方法论

**核心步骤**：
1. 源码编写：使用LaTeX语法编写文档源码
2. 自动下载：Tectonic自动下载所需LaTeX包
3. 编译输出：生成PDF文档
4. 错误处理：处理LaTeX编译错误和警告

**决策规则**：需要LaTeX排版时使用Tectonic；简单排版使用Typst

**穷尽重试策略**：Tectonic -> Typst -> WeasyPrint -> HTML

> 知识来源: TC-012 Tectonic



### TC-013 LuaTeX-CN 中文LaTeX方法论

**核心步骤**：
1. 源码编写：使用LaTeX+LuaTeX语法编写中文文档
2. 字体配置：配置中文字体和排版参数
3. 编译输出：使用LuaTeX引擎编译生成PDF
4. 中文优化：处理中文断行、标点挤压等特殊排版

**决策规则**：需要高级中文LaTeX排版时使用LuaTeX-CN；简单中文排版使用VMPrint

**穷尽重试策略**：LuaTeX-CN -> VMPrint -> Typst -> HTML

> 知识来源: TC-013 LuaTeX-CN



### TC-014 rxiv-maker 论文预印本制作方法论

**核心步骤**：
1. 内容组织：按论文结构组织内容（摘要/引言/方法/结果/讨论）
2. 模板选择：选择arXiv兼容的论文模板
3. 编译输出：生成符合预印本规范的PDF
4. 提交准备：生成arXiv提交所需的文件包

**决策规则**：需要制作arXiv预印本时使用rxiv-maker；一般论文使用Typst/LaTeX

**穷尽重试策略**：rxiv-maker -> Tectonic+手动模板 -> Typst -> Markdown

> 知识来源: TC-014 rxiv-maker



### TC-017 bm-md Markdown增强方法论

**核心步骤**：
1. Markdown编写：使用增强Markdown语法编写内容
2. 扩展解析：支持数学公式、图表、引用等扩展语法
3. 格式转换：将增强Markdown转换为HTML/PDF
4. 样式注入：从visual_dna注入排版样式

**决策规则**：需要增强Markdown功能时使用bm-md；标准Markdown使用原生解析

**穷尽重试策略**：bm-md -> 标准Markdown -> 纯文本

> 知识来源: TC-017 bm-md



### TC-022 AutoFigure 自动图表生成方法论

> **v2.0 重构说明**: AutoFigure 原依赖 LLM 推理后端生成图表，违反"代码生成优先"原则。现已重构为**纯代码生成**方式——由 LLM 直接书写 Mermaid / 内联 SVG / Observable Plot 代码生成图表。详见 [illustration-generator.md §0 核心铁律](../output/illustration-generator.md)。

**核心步骤**：
1. 数据提取：从文本中提取可可视化的数据
2. 图表类型推断：根据数据特征自动推断最佳图表类型
3. 代码生成：由 LLM 直接书写 Mermaid / 内联 SVG / Observable Plot 代码并渲染（禁止调用任何 AI 生图 API / LLM 推理后端）
4. 样式注入：从visual_dna注入配色和字体

**决策规则**：需要自动从文本生成图表时使用**代码生成**（Mermaid / 内联 SVG / Observable Plot）；手动指定图表使用ECharts/Plotly

**穷尽重试策略**：代码生成（Mermaid / SVG）-> ECharts手动配置 -> 表格（**禁止回落至 AI 生图 API / LLM 推理后端**）

> 知识来源: TC-022 AutoFigure



### TC-024 PubFig 出版级图表方法论

> **v2.0 重构说明**: PubFig 原依赖 LLM 推理后端生成图表，违反"代码生成优先"原则。现已重构为**纯代码生成**方式——由 LLM 直接书写 Matplotlib / 内联 SVG / Typst draw 代码生成出版级图表。详见 [illustration-generator.md §0 核心铁律](../output/illustration-generator.md)。

**核心步骤**：
1. 图表规范：按出版级标准设置图表尺寸和分辨率
2. 字体配置：使用出版级字体（Arial/Helvetica）
3. 配色注入：从visual_dna注入学术配色方案
4. 代码生成：由 LLM 直接书写 Matplotlib / 内联 SVG / Typst draw 代码生成高分辨率TIFF/EPS/PDF（禁止调用任何 AI 生图 API / LLM 推理后端）

**决策规则**：需要出版级图表输出时使用**代码生成**（Matplotlib / SVG / Typst draw）；Web展示使用ECharts/Plotly

**穷尽重试策略**：代码生成（Matplotlib / SVG）-> data-viz-plots -> Matplotlib -> 表格（**禁止回落至 AI 生图 API / LLM 推理后端**）

> 知识来源: TC-024 PubFig



### TC-026 PlantUML UML图生成方法论

**核心步骤**：
1. 图定义：使用PlantUML语法定义UML图
2. 图类型选择：类图/时序图/用例图/活动图/组件图
3. 渲染输出：通过PlantUML服务器或本地渲染生成SVG/PNG
4. 样式注入：从visual_dna注入配色方案

**决策规则**：需要UML标准图时使用PlantUML；流程图使用Mermaid

**穷尽重试策略**：PlantUML -> Mermaid -> ASCII图 -> 文字描述

> 知识来源: TC-026 PlantUML



### TC-027 TikZ LaTeX绘图方法论

**核心步骤**：
1. 绘图代码：使用TikZ语法定义图形
2. 编译渲染：通过LaTeX+TikZ编译生成PDF/SVG
3. 精确定位：使用TikZ坐标系统精确定位元素
4. 学术规范：确保图形符合学术出版规范

**决策规则**：需要LaTeX精确绘图时使用TikZ；简单示意图使用Mermaid/excalidraw

**穷尽重试策略**：TikZ -> Mermaid -> excalidraw -> 文字描述

> 知识来源: TC-027 TikZ



### TC-028 Pandoc 文档格式转换方法论

**核心步骤**：
1. 源格式识别：识别输入文档格式（Markdown/LaTeX/DOCX/HTML等）
2. 目标格式确定：确定输出格式需求
3. 转换执行：通过pandoc执行格式转换
4. 后处理：修复转换后的格式问题

**决策规则**：需要跨格式文档转换时使用Pandoc；单一格式使用专用工具

**穷尽重试策略**：Pandoc -> 专用转换工具 -> 手动复制

> 知识来源: TC-028 Pandoc



### TC-043 PaperBanana 顶刊插图方法论

> **v2.0 重构说明**: PaperBanana 原依赖 Google 专有 API（Nano Banana Pro / Gemini 3 Pro Image）生成插图，违反"代码生成优先"原则。现已重构为**纯代码生成**方式——通过内联 SVG / Canvas / Typst draw 代码生成顶刊级学术插图。详见 [illustration-generator.md §0 核心铁律](../output/illustration-generator.md)。

**核心步骤**：
1. 插图需求分析：确定插图类型（机制图/信号通路/架构图）
2. 配色注入：从visual_dna注入学术配色
3. 代码生成：由 LLM 直接书写内联 SVG / Canvas / Typst draw 代码生成顶刊级学术插图（禁止调用任何 AI 生图 API）
4. 质量校验：检查插图分辨率和学术规范性

**决策规则**：顶刊级学术插图使用**内联 SVG 代码生成**（PaperBanana 方法论·代码生成）；手绘风格使用excalidraw

**穷尽重试策略**：内联 SVG（PaperBanana 方法论）-> excalidraw -> Mermaid -> 文字描述（**禁止回落至 AI 生图 API**）

> 知识来源: TC-043 PaperBanana



### TC-044 PaperVizAgent 论文可视化代理方法论

> **v2.0 重构说明**: PaperVizAgent 原为专有 API 可视化代理，违反"代码生成优先"原则。现已重构为**纯代码生成**方式——通过 Observable Plot / ECharts / 内联 SVG 代码生成可视化图表。详见 [illustration-generator.md §0 核心铁律](../output/illustration-generator.md)。

**核心步骤**：
1. 论文解析：解析论文内容提取可视化需求
2. 图表规划：根据论文内容规划图表类型和布局
3. 代码生成：由 LLM 直接书写 Observable Plot / ECharts / 内联 SVG 代码生成图表（禁止调用任何 AI 生图 API）
4. 样式统一：确保所有图表风格统一

**决策规则**：需要批量生成论文图表时使用**代码生成**（Observable Plot / ECharts / 内联 SVG）；单图表使用ECharts/Plotly

**穷尽重试策略**：代码生成（Observable Plot / ECharts）-> data-viz-plots -> ECharts -> 表格（**禁止回落至 AI 生图 API**）

> 知识来源: TC-044 PaperVizAgent



### TC-074 WebWeaver Web内容生成方法论

**核心步骤**：
1. 内容结构化：将研究内容结构化为Web页面组件
2. 页面布局：使用12列栅格系统布局页面
3. 交互设计：添加导航、搜索、筛选等交互
4. 响应式适配：确保在不同设备上的显示效果

**决策规则**：需要生成Web交互内容时使用WebWeaver；静态文档使用Markdown/PDF

**穷尽重试策略**：WebWeaver -> html-ppt-skill -> Markdown -> PDF

> 知识来源: TC-074 WebWeaver

---

## 渲染管线流程

渲染管线新流程：

```
1. DLP 检索器（dlp-retriever.md）
   ↓ 输出 design_tokens
2. Visual DNA 生成（visual-dna.md）
   ↓ 生成 visual_dna 对象
3. 渲染（rendering-pipeline 各模块，从 TA/LA/VCA 原子库检索匹配原子）
   ↓ 渲染输出
4. ASR 硬门（asr-hard-gate.md）
   ↓ 通过/拒绝
5. Golden Set 距离校验（golden-set-validator.md）
   ↓ PASS/WARN/FAIL
6. 五维门禁审查（taste-validator.md）
   ↓ 五维评分
7. 熔断判定（fuse-mechanism.md）
   ↓ PASS/重试/质量保持
8. 导出（output 模块）
```

---

## 渲染管道穷尽重试策略

### L1: 完整渲染管道
Visual DNA生成 → 语义自动检测 → 布局栅格计算 → 动效语义匹配 → 容器渲染

### L2: Visual DNA生成失败
- 穷尽尝试默认主题（academic/business/creative三选一）
- 基于output_type自动选择：学术→academic, 商业→business, 创意→creative
- 跳过Taste-Skill仲裁，使用预设配色

### L3: 语义检测失败
- 穷尽尝试通用段落类型（全部标记为content）
- 使用默认布局规则（标题→全宽, 正文→单栏, 列表→双栏）
- 禁用语义驱动的动效匹配

### L4: 渲染引擎不可用
- 穷尽尝试Markdown输出
- 保留内容结构但无视觉样式
- 标记为穷尽重试渲染输出

### L5: 输出系统完全不可用
- 仅输出纯文本内容
- 无格式化、无排版
- 标注为穷尽重试输出

### L1-L5 与熔断机制的协同

- L1-L5 管渲染层重试：渲染失败时的技术重试（如渲染引擎崩溃、字体缺失等）
- 熔断管审美层重试：审美未满分时的质量重试（如配图不足、配色偏离等）
- 两者不冲突、不重复计数
- L1-L5 重试不计入熔断的质量驱动终止计数（连续 2 次重试分数提升 < 1 分的计数器，无硬性次数上限）
- 熔断重试不计入 L1-L5 的重试次数
- 执行顺序：先 L1-L5 技术重试（确保渲染成功），再熔断审美重试（确保审美达标）

---

## 复合渲染质量分 CRQS（R6-05）

> **目的**：为渲染管道提供一个统一的复合质量评分，整合 ASR 硬门合规性、Golden Set 金标准匹配度、Taste 品味分、Fuse 融合质量分四个维度，形成单一可比较的渲染质量指标。CRQS 用于渲染交付决策与重试触发。

### CRQS 公式

```
CRQS = ASR × 0.2 + GoldenSet × 0.3 + Taste × 0.4 + Fuse × 0.1
```

| 维度 | 权重 | 说明 |
|------|------|------|
| ASR | 0.2（20%） | ASR 硬门规则通过率 |
| GoldenSet | 0.3（30%） | 金标准匹配度 |
| Taste | 0.4（40%） | 品味分（权重最高，审美是核心） |
| Fuse | 0.1（10%） | 融合质量分 |

> **权重设计依据**：Taste 权重最高（0.4），因为审美是渲染管道的核心价值；GoldenSet 次之（0.3），确保与金标准对齐；ASR（0.2）作为硬门合规基线；Fuse（0.1）作为融合质量补充。四项权重之和为 1.0。

### 各维度分数计算方法

#### ASR（ASR Compliance Score）

```
ASR = (ASR 硬门规则通过数 / ASR 硬门规则总数) × 100
```

| 字段 | 说明 |
|------|------|
| 数据来源 | `asr-hard-gate.md` 中定义的 44 条禁令（8 类 × ≥5 条） |
| 通过数 | 渲染输出中未违反的 ASR 硬门规则数量 |
| 总数 | 44（ASR 硬门禁用清单全部规则） |
| 取值范围 | 0-100（100 = 全部 44 条规则通过，0 = 全部违反） |
| 计算时机 | 渲染管线流程第 4 步（ASR 硬门）执行后 |

#### GoldenSet（金标准匹配度）

```
GoldenSet = (1 - 平均距离) × 100
```

| 字段 | 说明 |
|------|------|
| 数据来源 | `golden-set-validator.md` 中定义的 48 个 Golden 样本 × 4 维距离度量 |
| 4 维距离 | 配色余弦距离、排版欧氏距离、间距曼哈顿距离、语义余弦距离 |
| 平均距离 | 4 维距离的归一化平均值（0-1，0 = 完全匹配，1 = 完全偏离） |
| 取值范围 | 0-100（100 = 与金标准完全匹配，0 = 完全偏离） |
| 计算时机 | 渲染管线流程第 5 步（Golden Set 距离校验）执行后 |

#### Taste（品味分）

```
Taste = 五维门禁审查平均分 × 100
```

| 字段 | 说明 |
|------|------|
| 数据来源 | `taste-validator.md` 中定义的五维门禁审查（每维 100 分） |
| 五维 | 排版 / 审美 / 配图 / 语义一致性 / 品牌 DNA 一致性 |
| 评分方式 | 人工评定或跨模型评定（如多模型投票取均值） |
| 取值范围 | 0-100（100 = 五维全部满分，0 = 五维全部零分） |
| 计算时机 | 渲染管线流程第 6 步（五维门禁审查）执行后 |

#### Fuse（融合质量分）

```
Fuse = 融合方案质量评分 × 100
```

| 字段 | 说明 |
|------|------|
| 数据来源 | `fuse-mechanism.md` 中熔断机制保留的最高分方案 |
| 评分依据 | 熔断过程中各次重试方案的审美评分，取最高分方案作为最终融合质量 |
| 取值范围 | 0-100（100 = 融合方案满分，0 = 融合方案零分） |
| 计算时机 | 渲染管线流程第 7 步（熔断判定）执行后；首次渲染即满分时 Fuse = 100 |

### CRQS 等级

| 等级 | 分数区间 | 含义 | 交付决策 |
|------|---------|------|---------|
| **A** | ≥ 90 | 优秀 | 直接交付，无需重试 |
| **B** | 80-89 | 良好 | 可交付，记录改进点供下次渲染优化 |
| **C** | 70-79 | 合格 | 可交付但附置信度标注，建议优化 |
| **D** | < 70 | 不合格 | 禁止交付，必须重试 |

### 重试触发规则

```
if CRQS < 80:
    trigger_retry()  # 触发渲染重试
elif CRQS < 70:
    block_delivery()  # 等级 D，禁止交付
```

| 规则 | 条件 | 动作 |
|------|------|------|
| **重试触发** | CRQS < 80（等级 C 或 D） | 触发渲染重试，重试次数受熔断机制限制（最大 3 次） |
| **禁止交付** | CRQS < 70（等级 D） | 禁止交付，必须重试直至 CRQS ≥ 70 |
| **可交付** | CRQS ≥ 80（等级 A 或 B） | 允许交付，等级 B 附改进点记录 |
| **最优交付** | CRQS ≥ 90（等级 A） | 直接交付，无需任何附加操作 |

**重试与熔断机制的协同**：
- CRQS < 80 触发重试时，重试次数计入熔断机制的 3 次限制
- 熔断机制保留最高分方案：即使 3 次重试后 CRQS 仍未达 80，也保留最高分方案作为最终输出（质量保持为最高分方案）
- 熔断后若最高分方案 CRQS ≥ 70（等级 C），允许交付但附置信度标注；若 < 70（等级 D），标记为"穷尽重试后仍不达标"，由 Orchestrator 决定是否接受

### CRQS 报告格式

CRQS 计算完成后，写入 execution_ledger 供审计追溯：

```yaml
crqs_report:
  node_id: "T20a"                    # 或 T20b/T20c
  output_type: "research_report"
  timestamp: "2026-06-25T10:35:00+08:00"
  scores:
    ASR: 95.5                        # ASR 硬门规则通过率 × 100
    GoldenSet: 88.0                  # 金标准匹配度 × 100
    Taste: 82.0                      # 品味分 × 100
    Fuse: 90.0                       # 融合质量分 × 100
  weights:
    ASR: 0.2
    GoldenSet: 0.3
    Taste: 0.4
    Fuse: 0.1
  CRQS: 87.35                        # = 95.5×0.2 + 88.0×0.3 + 82.0×0.4 + 90.0×0.1
  grade: "B"                         # A(≥90) | B(80-89) | C(70-79) | D(<70)
  delivery_decision: "deliverable"   # deliverable | retry | blocked
  retry_triggered: false             # CRQS ≥ 80，未触发重试
  retry_count: 0                     # 当前重试次数
  max_retries: 3                     # 熔断机制最大重试次数
```

---

## 渲染管线统一中间表示 IR（R9-01）

> **目的**：为 docx/html/typst 三条渲染链路定义统一的中间表示（Intermediate Representation, IR），使上游内容生成与下游格式渲染解耦。IR 是渲染管线的"通用语"，任何 output_type 的内容先生成 IR，再由各链路渲染器消费 IR 输出目标格式。

### IR 设计原则

1. **格式无关**：IR 不绑定任何具体渲染格式（docx/html/typst），仅描述内容结构与语义
2. **可序列化**：IR 可序列化为 JSON/YAML，便于跨节点传递与持久化
3. **可校验**：IR 有明确 schema，渲染前必须通过 schema 校验
4. **可追溯**：IR 的每个节点可追溯到上游 DAG 节点产出
5. **可扩展**：IR schema 支持版本化演进，向后兼容

### IR Schema 定义

```yaml
rendering_ir:
  schema_version: "1.0.0"
  metadata:
    output_type: "research_report|wechat_article|course_material"
    persona_type: "researcher|wechat_author|educator"
    visual_dna_ref: "visual_dna 对象的引用 ID"
    dlp_ref: "命中的 DLP 名称（如 DLP-nature）"
    source_nodes: ["T22", "T23", "T24", "T25", "T26"]  # 内容来源节点
    generated_at: "ISO 8601 时间戳"

  document:
    title: string
    subtitle: string | null
    abstract: string | null
    keywords: [string]
    authors: [string]                    # 来自 Persona 系统
    orcid: string | null                 # 来自 Persona 系统（学术合规）

  blocks:                                # 有序内容块列表
    - id: "block-001"                    # 块唯一 ID
      type: "heading|paragraph|list|table|figure|code_block|quote|callout|reference|page_break"
      level: int                         # heading 专用：1-6
      content: string                    # 文本内容
      children: [block_ref]              # 嵌套块（如 list 项）
      style:
        alignment: "left|center|right|justify"
        font_size: string | null         # 覆盖默认字号
        font_weight: "regular|bold|italic" | null
        color: string | null             # 覆盖默认颜色
      attributes:
        page_break_before: bool
        keep_with_next: bool
      source_ref: string | null          # 追溯到上游节点
      annotations:
        - key: string
          value: string

  figures:                               # 图表资源列表
    - id: "fig-001"
      type: "chart|illustration|screenshot|diagram"
      format: "svg|png|pdf|html"
      source: string                     # 文件路径或内联数据
      caption: string
      width: string                      # 如 "100%" 或 "600px"
      height: string | null
      alt_text: string                   # 无障碍描述
      render_engine: "mermaid|echarts|plotly|d3|matplotlib|typst_draw|inline_svg"
      source_node: string                # 生成该图表的节点

  tables:                                # 表格资源列表
    - id: "tbl-001"
      headers: [string]
      rows: [[string]]
      caption: string
      style: "striped|bordered|minimal"
      source_node: string

  references:                            # 引用列表
    - id: "ref-001"
      type: "inline|footnote|endnote|bibliography"
      citation_key: string
      citation_text: string
      url: string | null
      doi: string | null
      orcid: string | null               # 作者 ORCID（学术合规）

  style_tokens:                          # 从 visual_dna + DLP 注入的设计令牌
    color_scheme:
      primary: string
      secondary: string
      accent: string
      neutral: string
      background: string
      text: string
    font_scheme:
      heading_font: string
      body_font: string
      monospace_font: string
    typography:
      h1_size: string
      h2_size: string
      h3_size: string
      body_size: string
    spacing:
      base: string
      scale: [string]
    grid:
      columns: int | string
      margin: string
```

### IR 生成与消费流程

```
1. 上游节点（T22-T26）产出结构化内容
   ↓
2. IR 生成器（T20a/T20b/T20c 前置模块）
   - 读取上游内容
   - 读取 visual_dna + DLP 设计令牌
   - 读取 Persona 配置
   - 生成 rendering_ir 对象
   ↓
3. IR Schema 校验
   - 校验必填字段
   - 校验块类型合法性
   - 校验设计令牌完整性
   - 失败 → 触发 IR 校验错误处理
   ↓
4. 渲染器消费 IR
   - docx 渲染器：IR → python-docx → .docx
   - html 渲染器：IR → Jinja2 模板 → .html
   - typst 渲染器：IR → Typst 源码 → .pdf
   ↓
5. 三链路一致性校验（scripts/rendering-consistency-check.py）
   - 对比三链路输出的内容一致性
   - 对比三链路输出的视觉一致性
```

### IR 与三链路渲染器的映射

| IR 字段 | docx 渲染器 | html 渲染器 | typst 渲染器 |
|---------|------------|------------|-------------|
| blocks[type=heading] | paragraph.style=Heading{level} | `<h{level}>` | `= Heading` |
| blocks[type=paragraph] | paragraph | `<p>` | 普通段落 |
| blocks[type=list] | paragraph.style=ListBullet | `<ul><li>` | `- item` |
| blocks[type=table] | table | `<table>` | `#table()` |
| blocks[type=figure] | inline_image + caption | `<figure><img>` | `#figure(image())` |
| blocks[type=code_block] | paragraph.style=Code | `<pre><code>` | ```` ``` ```` |
| blocks[type=quote] | paragraph.style=Quote | `<blockquote>` | `#quote()` |
| blocks[type=page_break] | page_break | `<div style="page-break-after">` | `#pagebreak()` |
| style_tokens.color_scheme | run.font.color | CSS variable | `#set text(fill)` |
| style_tokens.font_scheme | run.font.name | font-family | `#set text(font)` |
| style_tokens.typography | paragraph.font.size | font-size | `#set text(size)` |

---

## 渲染管线性能基准（R9-02）

> **目的**：为渲染管线建立可量化的性能基准，覆盖延迟、内存、成功率三个维度，按 output_type 与渲染链路分别采集，用于性能退化检测与资源规划。

### 性能基准采集方法

- **采集周期**：每 30 天由 CI 自动执行一次基准测试
- **测试环境**：Linux Ubuntu 22.04, Python 3.11, 8 核 CPU, 16GB RAM
- **测试样本**：每种 output_type × 链路组合使用标准测试输入执行 50 次，取统计值
- **指标定义**：
  - **P50 延迟 (ms)**：50% 分位渲染延迟
  - **P95 延迟 (ms)**：95% 分位渲染延迟
  - **峰值内存 (MB)**：单次渲染峰值 RSS
  - **成功率**：50 次渲染中成功输出的比例

### 性能基准矩阵

#### research_report 链路

| 渲染链路 | P50 延迟 (ms) | P95 延迟 (ms) | 峰值内存 (MB) | 成功率 | 性能等级 |
|---------|--------------|--------------|--------------|--------|---------|
| typst | 3500 | 10000 | 250 | 0.95 | B |
| html | 2000 | 6000 | 180 | 0.97 | A |
| docx | 4500 | 13000 | 350 | 0.92 | C |

#### wechat_article 链路

| 渲染链路 | P50 延迟 (ms) | P95 延迟 (ms) | 峰值内存 (MB) | 成功率 | 性能等级 |
|---------|--------------|--------------|--------------|--------|---------|
| typst | 2000 | 6000 | 180 | 0.96 | B |
| html | 1200 | 4000 | 120 | 0.98 | A |
| docx | 3000 | 9000 | 280 | 0.93 | B |

#### course_material 链路

| 渲染链路 | P50 延迟 (ms) | P95 延迟 (ms) | 峰值内存 (MB) | 成功率 | 性能等级 |
|---------|--------------|--------------|--------------|--------|---------|
| typst | 3000 | 8500 | 220 | 0.94 | B |
| html | 1800 | 5500 | 160 | 0.97 | A |
| docx | 4000 | 12000 | 320 | 0.91 | C |

### 性能等级定义

| 等级 | P95 延迟 | 峰值内存 | 成功率 | 含义 |
|------|---------|---------|--------|------|
| **A** | ≤ 6000ms | ≤ 200MB | ≥ 0.97 | 优秀——快速、低耗、高可靠 |
| **B** | ≤ 10000ms | ≤ 300MB | ≥ 0.93 | 良好——可接受的开销与可靠性 |
| **C** | ≤ 15000ms | ≤ 400MB | ≥ 0.90 | 合格——开销较大，需关注资源占用 |
| **D** | > 15000ms | > 400MB | < 0.90 | 不合格——开销过大或可靠性不足 |

### 性能退化告警

| 指标 | 退化阈值 | 告警动作 |
|------|---------|---------|
| P95 延迟 | 较基线上升 > 50% | 标记为 performance_degraded，CI WARN |
| 峰值内存 | 较基线上升 > 30% | 标记为 memory_leak_suspect，CI WARN |
| 成功率 | 较基线下降 > 5% | 标记为 reliability_drop，CI ERROR 阻塞合并 |

### 性能基准与渲染链路选择的协同

- **html 链路**：性能最优，作为默认首选链路
- **typst 链路**：学术排版质量最高，research_report 优先使用
- **docx 链路**：Office 交付兼容性最高，但性能开销最大，仅在需要 .docx 输出时使用

### 性能基准报告格式

性能基准采集完成后，写入 execution_ledger 供审计追溯：

```yaml
rendering_performance_report:
  benchmark_id: "BENCH-2026-06-001"
  timestamp: "2026-06-25T10:30:00+08:00"
  environment:
    os: "Linux Ubuntu 22.04"
    python: "3.11"
    cpu: "8 cores"
    ram: "16GB"
  results:
    - output_type: "research_report"
      chain: "typst"
      p50_latency_ms: 3500
      p95_latency_ms: 10000
      peak_memory_mb: 250
      success_rate: 0.95
      grade: "B"
    - output_type: "research_report"
      chain: "html"
      p50_latency_ms: 2000
      p95_latency_ms: 6000
      peak_memory_mb: 180
      success_rate: 0.97
      grade: "A"
  summary:
    total_benchmarks: 9
    grade_a_count: 3
    grade_b_count: 4
    grade_c_count: 2
    grade_d_count: 0
```

---

## 渲染管线统一错误处理（R9-03）

> **目的**：为渲染管线定义统一的错误码体系与格式适配策略，确保任何渲染失败都有明确的处置路径，避免静默失败或无意义重试。

### 错误码体系

渲染管线错误码采用 `RERR-{类别}-{编号}` 格式，共 6 类：

| 错误码 | 类别 | 含义 | 严重程度 | 默认处置 |
|--------|------|------|---------|---------|
| RERR-IR-001 | IR 校验 | IR schema 校验失败（必填字段缺失） | CRITICAL | 退回 IR 生成器修复 |
| RERR-IR-002 | IR 校验 | IR 块类型非法 | CRITICAL | 退回 IR 生成器修复 |
| RERR-IR-003 | IR 校验 | IR 设计令牌不完整 | HIGH | 使用默认设计令牌补全 |
| RERR-DLP-001 | DLP 检索 | DLP 检索无匹配 | MEDIUM | 格式适配到 DLP-nature |
| RERR-DLP-002 | DLP 检索 | DLP 文件缺失 | HIGH | 格式适配到 DLP-nature 并告警 |
| RERR-VD-001 | Visual DNA | Visual DNA 生成失败 | HIGH | 格式适配到默认主题（academic/business/creative） |
| RERR-VD-002 | Visual DNA | Visual DNA 字段不完整 | MEDIUM | 使用默认值补全 |
| RERR-RENDER-001 | 渲染执行 | 渲染引擎不可用（如 typst 未安装） | CRITICAL | 切换到穷尽重试链下一渲染器 |
| RERR-RENDER-002 | 渲染执行 | 渲染超时（超过 P95 × 3） | HIGH | 终止当前渲染，切换渲染器 |
| RERR-RENDER-003 | 渲染执行 | 渲染输出为空 | CRITICAL | 退回 IR 校验，重新生成 IR |
| RERR-RENDER-004 | 渲染执行 | 渲染输出格式错误（如损坏的 PDF） | CRITICAL | 切换渲染器 |
| RERR-ASR-001 | ASR 硬门 | ASR 硬门规则违反 ≥ 3 条 | HIGH | 触发熔断重试 |
| RERR-ASR-002 | ASR 硬门 | ASR 硬门规则违反 1-2 条 | MEDIUM | 记录警告，允许交付 |
| RERR-CRQS-001 | CRQS | CRQS < 70（等级 D） | CRITICAL | 禁止交付，强制重试 |
| RERR-CRQS-002 | CRQS | CRQS 70-79（等级 C） | MEDIUM | 允许交付但附置信度标注 |

### 格式适配策略

渲染管线采用分层格式适配策略，每层失败后穷尽尝试下一层：

```
Layer 1: 主渲染链路（按 output_type 默认选择）
  ↓ 失败（RERR-RENDER-001/002/003/004）
Layer 2: 备用渲染链路（穷尽重试链 / 格式适配链）
  - typst 失败 → html
  - html 失败 → docx
  - docx 失败 → markdown
  ↓ 失败
Layer 3: 基础格式渲染（使用默认视觉风格，内容完整保留）
  - 跳过 DLP 检索，使用默认主题
  - 跳过动效，输出静态版本
  - 跳过图表渲染，输出表格替代
  ↓ 失败
Layer 4: 纯文本输出
  - 仅输出 IR 的文本内容
  - 保留内容结构但无视觉样式
  - 标注为穷尽重试渲染输出
  ↓ 失败
Layer 5: 错误报告
  - 输出结构化错误报告（含错误码、失败原因、格式适配链路）
  - 记录到 execution_ledger
  - 通知 Orchestrator 决定是否接受
```

> **R2-01 例外条款声明**：上述格式适配策略不视为降级——从 typst 到 html 到 docx 到 markdown 是格式变化，内容完整保留。Layer 3-4 虽使用基础视觉风格，但文本内容、数据、结论均完整保留，不构成内容降级。

### 错误处理与熔断机制的协同

| 错误类型 | 是否计入熔断 | 说明 |
|---------|------------|------|
| RERR-IR-* | 否 | IR 错误为上游内容问题，退回 IR 生成器修复，不计入渲染熔断 |
| RERR-DLP-* | 否 | DLP 错误由检索器格式适配处理，不影响渲染熔断 |
| RERR-VD-* | 否 | Visual DNA 错误由默认主题格式适配处理，不影响渲染熔断 |
| RERR-RENDER-* | 是 | 渲染执行错误计入熔断机制的质量驱动终止计数 |
| RERR-ASR-* | 是 | ASR 硬门违反触发熔断重试，计入质量驱动终止计数 |
| RERR-CRQS-* | 是 | CRQS 不达标触发熔断重试，计入质量驱动终止计数 |

### 错误日志格式

每次渲染错误记录到 execution_ledger.rendering_errors：

```yaml
rendering_errors:
  - error_id: "RERR-2026-001"
    timestamp: "2026-06-25T10:32:00+08:00"
    error_code: "RERR-RENDER-001"
    severity: "CRITICAL"
    node_id: "T20a"
    output_type: "research_report"
    chain: "typst"
    detail: "typst 引擎不可用：typst command not found"
    format_adaptation_action: "switch_to_html"
    format_adaptation_chain: ["typst", "html", "docx", "markdown"]
    retry_count: 1
    termination_condition: "quality_driven: consecutive_low_improvement >= 2"
    resolved: false
```

### 错误码与 HTTP 状态码的映射（供 API 调用参考）

| 错误码 | HTTP 状态码 | 含义 |
|--------|------------|------|
| RERR-IR-001/002 | 422 | Unprocessable Entity — IR 校验失败 |
| RERR-DLP-001/002 | 500 | Internal Server Error — DLP 检索失败 |
| RERR-VD-001/002 | 500 | Internal Server Error — Visual DNA 生成失败 |
| RERR-RENDER-001 | 503 | Service Unavailable — 渲染引擎不可用 |
| RERR-RENDER-002 | 504 | Gateway Timeout — 渲染超时 |
| RERR-RENDER-003/004 | 500 | Internal Server Error — 渲染输出异常 |
| RERR-ASR-001/002 | 200 | OK（附警告）— ASR 硬门违反但输出已生成 |
| RERR-CRQS-001 | 406 | Not Acceptable — CRQS 等级 D，禁止交付 |
| RERR-CRQS-002 | 200 | OK（附置信度标注）— CRQS 等级 C |
