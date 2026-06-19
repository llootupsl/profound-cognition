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
5. 熔断机制（fuse-mechanism.md）— 满分追求 + 最大重试 3 次 + 质量保持为最高分方案

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
| PaperBanana Skill | 顶刊级学术插图生成 | T27 (配图) |
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

**核心步骤**：
1. 数据提取：从文本中提取可可视化的数据
2. 图表类型推断：根据数据特征自动推断最佳图表类型
3. 图表生成：自动生成图表代码并渲染
4. 样式注入：从visual_dna注入配色和字体

**决策规则**：需要自动从文本生成图表时使用AutoFigure；手动指定图表使用ECharts/Plotly

**穷尽重试策略**：AutoFigure -> ECharts手动配置 -> 表格

> 知识来源: TC-022 AutoFigure



### TC-024 PubFig 出版级图表方法论

**核心步骤**：
1. 图表规范：按出版级标准设置图表尺寸和分辨率
2. 字体配置：使用出版级字体（Arial/Helvetica）
3. 配色注入：从visual_dna注入学术配色方案
4. 输出格式：生成高分辨率TIFF/EPS/PDF

**决策规则**：需要出版级图表输出时使用PubFig；Web展示使用ECharts/Plotly

**穷尽重试策略**：PubFig -> data-viz-plots -> Matplotlib -> 表格

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

**核心步骤**：
1. 插图需求分析：确定插图类型（机制图/信号通路/架构图）
2. 配色注入：从visual_dna注入学术配色
3. 插图生成：PaperBanana生成顶刊级学术插图
4. 质量校验：检查插图分辨率和学术规范性

**决策规则**：顶刊级学术插图使用PaperBanana；手绘风格使用excalidraw

**穷尽重试策略**：PaperBanana -> excalidraw -> Mermaid -> 文字描述

> 知识来源: TC-043 PaperBanana



### TC-044 PaperVizAgent 论文可视化代理方法论

**核心步骤**：
1. 论文解析：解析论文内容提取可视化需求
2. 图表规划：根据论文内容规划图表类型和布局
3. 图表生成：自动生成论文所需的图表
4. 样式统一：确保所有图表风格统一

**决策规则**：需要批量生成论文图表时使用PaperVizAgent；单图表使用ECharts/Plotly

**穷尽重试策略**：PaperVizAgent -> data-viz-plots -> ECharts -> 表格

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
- L1-L5 重试不计入熔断的 3 次限制
- 熔断重试不计入 L1-L5 的重试次数
- 执行顺序：先 L1-L5 技术重试（确保渲染成功），再熔断审美重试（确保审美达标）
