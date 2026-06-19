<!-- 作者：阿洋 -->

# ASR 硬门禁用清单 (Anti-Slop Rule Set — Hard Gate)

> **定位**: 渲染管道所有输出的强制前置门禁。任何渲染产物（HTML/CSS/图片/图表/排版）在输出前必须通过本清单全量检查。
> **执行强度**: 硬门——违反即拒。任一禁令触发即返回违规清单并拒绝输出，触发穷尽重试（计入熔断计数）。
> **设计理念**: 融入 Impeccable 的禁用清单驱动理念——系统性剔除廉价渐变、光晕、模板化布局等 AI 设计通病，细节精度对标资深设计师，输出高完成度界面。
> **知识来源**: LC-026 Taste-Skill 反 Slop 规则（深度扩展）+ Impeccable 禁用清单驱动理念

---

## 〇、门禁总览

| 维度 | 值 |
|------|-----|
| 禁令总数 | 44 条（8 类别） |
| 执行模式 | 硬门（HARD GATE） |
| 违规处理 | 违反即拒 + 返回违规清单 + 触发重试 |
| 检查时机 | 渲染输出前（visual_dna 生成之后、最终产物落地之前） |
| 检查范围 | CSS / HTML / 图片元数据 / 图表代码 / 排版参数 |
| 与 visual_dna 关系 | 本清单为 visual_dna 的强制约束层，visual_dna 生成的参数不得违反本清单 |

### 禁令类别索引

| 类别 | 前缀 | 条数 | 核心目标 |
|------|------|------|---------|
| 字体禁令 | ASR-FONT | 6 | 剔除通用化字体选择，强制审美品位 |
| 配色禁令 | ASR-COLOR | 6 | 剔除 AI 配色通病（紫/黑/白/默认蓝） |
| 布局禁令 | ASR-LAYOUT | 6 | 剔除模板化布局（居中英雄/等宽卡片） |
| 动效禁令 | ASR-MOTION | 5 | 剔除性能杀手与廉价动效 |
| 装饰禁令 | ASR-DECO | 5 | 剔除 emoji/em-dash/光晕等装饰噪音 |
| 配图禁令 | ASR-IMAGE | 5 | 剔除低质图片与无障碍缺陷 |
| 排版禁令 | ASR-TYPO | 6 | 剔除可读性杀手与层级混乱 |
| 数据可视禁令 | ASR-VIZ | 5 | 剔除默认配色与误导性图表 |

---

## 一、字体禁令（ASR-FONT-001 ~ 006）

> **来源**: LC-026 Taste-Skill 反 Slop 排版禁令扩展
> **原理**: Inter/Roboto/Arial 等"安全字体"是 LLM 训练数据统计平均的产物，缺乏设计意图。Premium 产出必须使用有审美主张的字体。

### ASR-FONT-001: 禁 Inter 作为 Premium 产出字体

| 字段 | 内容 |
|------|------|
| **检测规则** | 正则 `font-family.*Inter` 且 `产出类型 == Premium`（含 research_report / wechat_article 中 vibe_words 含 premium/creative） |
| **违规示例** | `font-family: "Inter", sans-serif;`（Premium 场景） |
| **修复建议** | 替换为 Geist / Outfit / Cabinet Grotesk / Satoshi。示例：`font-family: "Geist", "Outfit", sans-serif;` |
| **来源标注** | LC-026 Taste-Skill 反 Slop 规则·排版禁令 |

### ASR-FONT-002: 禁 Roboto 作为品牌字体

| 字段 | 内容 |
|------|------|
| **检测规则** | 正则 `font-family.*Roboto` 且 `产出类型 == Brand`（含品牌标识/Logo/品牌主视觉） |
| **违规示例** | `font-family: "Roboto", sans-serif;`（品牌标题） |
| **修复建议** | 替换为 Satoshi / Cabinet Grotesk / General Sans。品牌字体须具备独特字怀和笔画特征。 |
| **来源标注** | LC-026 Taste-Skill 反 Slop 规则·排版禁令（扩展） |

### ASR-FONT-003: 禁 Arial 作为正文字体

| 字段 | 内容 |
|------|------|
| **检测规则** | 正则 `font-family.*Arial` 且 `role == body`（正文段落） |
| **违规示例** | `font-family: "Arial", sans-serif;`（正文） |
| **修复建议** | 西文正文替换为 Source Serif 4 / Fraunces（Editorial 感）或 Geist（UI 感）；中文正文使用思源宋体/思源黑体。 |
| **来源标注** | LC-026 Taste-Skill 反 Slop 规则·排版禁令（扩展） |

### ASR-FONT-004: 禁默认无衬线字体用于学术正文

| 字段 | 内容 |
|------|------|
| **检测规则** | 学术场景（`output_type == research_report` 且 `target_audience == academic`）+ 正则 `font-family.*sans-serif` 且 `role == body` |
| **违规示例** | 学术论文正文使用 `font-family: sans-serif;` |
| **修复建议** | 学术正文必须使用衬线字体：Source Serif 4 / Noto Serif SC / STSong。学术场景衬线正文是出版规范要求。 |
| **来源标注** | visual-dna.md §三 字体方案 + LC-026 学术严谨设计语言 |

### ASR-FONT-005: 禁混合 3 种以上字体族

| 字段 | 内容 |
|------|------|
| **检测规则** | AST 检查：提取所有 `font-family` 声明，去重后字体族 count > 3（标题/正文/代码 3 族为上限） |
| **违规示例** | 同时使用 Inter（标题）+ Source Serif（正文）+ JetBrains Mono（代码）+ Outfit（强调）= 4 族 |
| **修复建议** | 最多保留 3 个字体族：1 标题族 + 1 正文族 + 1 代码族。强调需求通过字重/字号变化实现，不引入第 4 族。 |
| **来源标注** | Impeccable 禁用清单驱动理念·字体一致性约束 |

### ASR-FONT-006: 禁通用衬线字体用于 Editorial 场景

| 字段 | 内容 |
|------|------|
| **检测规则** | 正则 `font-family.*(Times New Roman|Georgia|Garamond)` 且 `vibe_words 含 editorial` |
| **违规示例** | `font-family: "Times New Roman", serif;`（Editorial 场景） |
| **修复建议** | 替换为 Fraunces / Gambarino / Editorial New / Instrument Serif。通用衬线字体缺乏 Editorial 气质。 |
| **来源标注** | LC-026 Taste-Skill 反 Slop 规则·排版禁令 |

---

## 二、配色禁令（ASR-COLOR-001 ~ 006）

> **来源**: LC-026 Taste-Skill 反 Slop 配色禁令 + Impeccable 禁用清单驱动理念
> **原理**: AI Purple/Blue、纯黑纯白、Tailwind 默认蓝是 AI 生成内容最显著的"统计平均色"，一眼可辨。高饱和度渐变是廉价感的标志。

### ASR-COLOR-001: 禁 AI 紫 #7C3AED 系

| 字段 | 内容 |
|------|------|
| **检测规则** | 色值检测：十六进制色值转 HSL，判断是否在 #7C3AED ±10% 范围内（H ∈ [250°, 280°], S > 60%, L ∈ [40%, 60%]）。覆盖 `#7C3AED`/`#8B5CF6`/`#6D28D9`/`#A78BFA` 等 AI 紫色系。 |
| **违规示例** | `--color-primary: #7C3AED;` 或 `background: linear-gradient(to right, #8B5CF6, #6D28D9);` |
| **修复建议** | 替换为有色彩主张的色值。学术蓝 `#1A56DB`、暖调人文 `#B45309`、科技青 `#06B6D4`。如需紫色，使用低饱和度薰衣草灰 `#9C8DB8`。 |
| **来源标注** | LC-026 Taste-Skill 反 Slop 规则·配色禁令（AI Purple/Blue 审美） |

### ASR-COLOR-002: 禁纯黑 #000000 作为大面积背景

| 字段 | 内容 |
|------|------|
| **检测规则** | 正则 `background.*#000000` 或 `background.*rgb\(0,\s*0,\s*0\)` 或 `background.*#000`（大面积背景场景） |
| **违规示例** | `body { background: #000000; }` |
| **修复建议** | 使用 Off-Black / Zinc-950 / Charcoal：`#0A0A0A`（Zinc-950）/ `#18181B`（Zinc-900）/ `#1C1C1E`（Charcoal）。纯黑在 OLED 屏幕上产生过强对比，缺乏层次。 |
| **来源标注** | LC-026 Taste-Skill 反 Slop 规则·配色禁令（禁止纯黑） |

### ASR-COLOR-003: 禁纯白 #FFFFFF 作为大面积背景

| 字段 | 内容 |
|------|------|
| **检测规则** | 正则 `background.*#FFFFFF` 或 `background.*rgb\(255,\s*255,\s*255\)` 且背景面积 > 50%（通过布局区域占比计算） |
| **违规示例** | `body { background: #FFFFFF; }`（占满全屏） |
| **修复建议** | 使用暖白/冷白替代：`#FAFAFA`（Zinc-50）/ `#F9FAFB`（Gray-50）/ `#FDFDFC`（暖白）。纯白背景缺乏温度感，资深设计师极少使用。 |
| **来源标注** | Impeccable 禁用清单驱动理念·配色温度约束 |

### ASR-COLOR-004: 禁 Tailwind 默认蓝 #3B82F6 作为主色

| 字段 | 内容 |
|------|------|
| **检测规则** | 正则 `--primary.*#3B82F6` 或 `--color-primary.*#3B82F6` 或 `background.*#3B82F6`（主色用途） |
| **违规示例** | `--color-primary: #3B82F6;`（Tailwind blue-500） |
| **修复建议** | 替换为有品牌主张的蓝色：学术蓝 `#1A56DB`、深海蓝 `#1E40AF`、钢蓝 `#075985`。Tailwind 默认蓝是"未做设计决策"的标志。 |
| **来源标注** | LC-026 Taste-Skill 反 Slop 规则·配色禁令（扩展）+ Impeccable 禁用清单 |

### ASR-COLOR-005: 禁高饱和度渐变

| 字段 | 内容 |
|------|------|
| **检测规则** | 解析 `linear-gradient`/`radial-gradient` 两端色值，转 HSL 后判断两端饱和度是否均 > 80%。正则匹配 `gradient.*` 后提取色值。 |
| **违规示例** | `background: linear-gradient(135deg, #FF006E, #8338EC);`（两端饱和度均 >90%） |
| **修复建议** | 降低渐变端点饱和度至 60% 以下，或使用同色系明度渐变（如 `#1A56DB` → `#3B82F6` 同色系深浅渐变）。高饱和渐变是 AI 设计最显著的廉价标志。 |
| **来源标注** | LC-026 Taste-Skill 反 Slop 规则·配色禁令（霓虹渐变）+ Impeccable 禁用清单 |

### ASR-COLOR-006: 禁暖冷灰波动

| 字段 | 内容 |
|------|------|
| **检测规则** | AST 检查：提取所有灰色系色值（S < 10%），转 HSL 后判断色相 H 是否统一。若文档内存在暖灰（H ∈ [20°, 50°]）与冷灰（H ∈ [200°, 240°]）混用即违规。 |
| **违规示例** | `--color-border: #E5E7EB;`（冷灰 H=220°）与 `--color-bg-alt: #F5F0EB;`（暖灰 H=30°）同时出现 |
| **修复建议** | 全文档统一一种灰调。学术/科技场景用冷灰（Zinc 系），人文/品牌场景用暖灰（Stone 系）。 |
| **来源标注** | LC-026 Taste-Skill 反 Slop 规则·配色禁令（禁止暖冷灰波动） |

---

## 三、布局禁令（ASR-LAYOUT-001 ~ 006）

> **来源**: LC-026 Taste-Skill 反 Slop 布局禁令 + Impeccable 禁用清单驱动理念
> **原理**: 居中英雄区、等宽三列卡片、h-screen 全屏占位是 LLM 生成前端代码的三大模板化标志。资深设计师通过不对称布局和栅格约束创造视觉节奏。

### ASR-LAYOUT-001: 禁居中英雄区（DV>4 时）

| 字段 | 内容 |
|------|------|
| **检测规则** | CSS 选择器组合检测：`text-align: center` + (`min-height: 100vh` 或 `min-height: 100dvh`) 且 `DESIGN_VARIANCE > 4`。同时检查父容器是否为 flex 居中（`justify-content: center` + `align-items: center`）。 |
| **违规示例** | `<section class="hero" style="text-align:center; min-height:100vh; display:flex; justify-content:center; align-items:center;">` |
| **修复建议** | DV>4 时使用分屏布局（左对齐内容 + 右对齐资产）或不对称留白布局。示例：`grid-template-columns: 7fr 5fr;` 左侧内容左对齐，右侧视觉资产。 |
| **来源标注** | LC-026 Taste-Skill 反 Slop 规则·布局禁令（DV>4 禁止居中英雄区） |

### ASR-LAYOUT-002: 禁 h-screen 全屏占位

| 字段 | 内容 |
|------|------|
| **检测规则** | 正则 `height:\s*100vh` 或 `min-height:\s*100vh` 或 Tailwind 类 `h-screen`。排除 `min-height: 100dvh`（允许）。 |
| **违规示例** | `<div class="h-screen">` 或 `section { height: 100vh; }` |
| **修复建议** | 替换为 `min-h-[100dvh]`（CSS：`min-height: 100dvh;`）。`dvh`（dynamic viewport height）防止 iOS Safari 地址栏伸缩导致的布局跳动。 |
| **来源标注** | LC-026 Taste-Skill 反 Slop 规则·布局禁令（禁止 h-screen） |

### ASR-LAYOUT-003: 禁 3 列等宽卡片网格

| 字段 | 内容 |
|------|------|
| **检测规则** | 正则 `grid-template-columns:\s*1fr\s+1fr\s+1fr` 且 AST 检查三个网格子元素内容结构无差异（相同标签结构 + 相同 class 模式）。 |
| **违规示例** | `<div style="display:grid; grid-template-columns: 1fr 1fr 1fr;">` 内含 3 个结构相同的卡片 |
| **修复建议** | 使用非对称栅格 `grid-template-columns: 2fr 1fr 1fr` 或 `grid-template-columns: 1fr 1.5fr 1fr`，或改为 2 列 + 1 全宽的混合布局。等宽三列是 AI 生成最模板化的布局模式。 |
| **来源标注** | LC-026 Taste-Skill 反 Slop 规则·布局禁令（扩展）+ Impeccable 禁用清单 |

### ASR-LAYOUT-004: 禁默认 Tailwind 间距阶梯

| 字段 | 内容 |
|------|------|
| **检测规则** | 正则检测 Tailwind 默认间距类：`\b(p|m|gap|space)-(4|8|12|16)\b` 出现频率 > 60%（占所有间距类比例）。Tailwind 默认 `p-4`/`m-4`/`gap-4` 是未做间距设计的标志。 |
| **违规示例** | 大量使用 `<div class="p-4 m-4 gap-4">` 而无自定义间距变量 |
| **修复建议** | 基于 visual_dna 的 4px 栅格系统定义语义化间距变量：`--space-xs: 4px; --space-sm: 8px; --space-md: 16px;`，使用 CSS 变量替代 Tailwind 默认类。 |
| **来源标注** | Impeccable 禁用清单驱动理念·栅格约束 + visual-dna.md §四 4px 基准栅格系统 |

### ASR-LAYOUT-005: 禁无栅格约束的自由布局

| 字段 | 内容 |
|------|------|
| **检测规则** | AST 检查：页面主布局容器无 `display: grid` 或 `display: flex` 声明，且子元素使用绝对定位（`position: absolute`）占比 > 30%。 |
| **违规示例** | 所有子元素使用 `position: absolute; top: Xpx; left: Ypx;` 手动定位 |
| **修复建议** | 主布局必须使用 grid 或 flex 约束。绝对定位仅用于叠加层（overlay/tooltip/modal）。引入 12 列栅格系统：`grid-template-columns: repeat(12, 1fr);`。 |
| **来源标注** | Impeccable 禁用清单驱动理念·栅格约束 |

### ASR-LAYOUT-006: 禁卡片滥用（高密度场景）

| 字段 | 内容 |
|------|------|
| **检测规则** | AST 检查：`VISUAL_DENSITY > 7`（驾驶舱密度）时，`box-shadow` + `border-radius` 组合的卡片元素占比 > 50%。高密度场景应使用分割线替代卡片。 |
| **违规示例** | VD=8 的仪表盘中每个数据块都包裹在带阴影圆角的卡片内 |
| **修复建议** | VD>7 时用 `border-top` 分割线或负空间（margin）替代卡片阴影。仅在有层级提升需求时使用卡片。 |
| **来源标注** | LC-026 Taste-Skill 反 Slop 规则·组件禁令（卡片仅在有层级提升需求时使用） |

---

## 四、动效禁令（ASR-MOTION-001 ~ 005）

> **来源**: LC-026 Taste-Skill 反 Slop 动效规则 + Impeccable 禁用清单驱动理念
> **原理**: width/height 动画触发重排（reflow）是性能杀手；linear 缓动缺乏自然感；弹跳动画用于正式产出显得轻浮。资深设计师仅动画 transform + opacity（GPU 加速）。

### ASR-MOTION-001: 禁 width/height 动画

| 字段 | 内容 |
|------|------|
| **检测规则** | 正则 `transition:\s*.*width` 或 `transition:\s*.*height` 或 `@keyframes` 内含 `width:` / `height:` 属性变化。 |
| **违规示例** | `transition: width 0.3s ease;` 或 `@keyframes expand { from { width: 0; } to { width: 100%; } }` |
| **修复建议** | 仅动画 `transform` 和 `opacity`（GPU 加速，不触发重排）。宽度变化用 `transform: scaleX()`，高度变化用 `transform: scaleY()`。 |
| **来源标注** | LC-026 Taste-Skill 反 Slop 规则·动效禁令（仅允许 transform+opacity） |

### ASR-MOTION-002: 禁 linear 缓动

| 字段 | 内容 |
|------|------|
| **检测规则** | 正则 `transition-timing-function:\s*linear` 或 `animation-timing-function:\s*linear` 或 `cubic-bezier\(0,\s*0,\s*1,\s*1\)`（linear 的贝塞尔表达）。 |
| **违规示例** | `transition: all 0.3s linear;` |
| **修复建议** | 使用自然缓动曲线：入场 `ease-out`（`cubic-bezier(0.25, 0.1, 0.25, 1.0)`）、出场 `ease-in`（`cubic-bezier(0.42, 0, 1.0, 1.0)`）、循环 `ease-in-out`。linear 缓动在物理世界不存在。 |
| **来源标注** | visual-dna.md §六 动效速率规范 + Impeccable 禁用清单 |

### ASR-MOTION-003: 禁旋转动画用于非加载场景

| 字段 | 内容 |
|------|------|
| **检测规则** | 正则 `transform:\s*rotate` 或 `animation.*spin` 或 `@keyframes.*rotate` 且上下文非 loading/spinner（AST 检查父元素 class 不含 `loading`/`spinner`/`loader`）。 |
| **违规示例** | 按钮悬停时 `transform: rotate(180deg);`（非加载场景） |
| **修复建议** | 旋转动画仅用于加载指示器（spinner）。非加载场景的强调动效用 `transform: scale()` 或 `opacity` 变化。 |
| **来源标注** | Impeccable 禁用清单驱动理念·动效语义约束 |

### ASR-MOTION-004: 禁弹跳动画用于正式产出

| 字段 | 内容 |
|------|------|
| **检测规则** | 正则 `animation:\s*.*bounce` 或 `cubic-bezier` 参数中 y 值超出 [0, 1] 范围（如 `cubic-bezier(0.34, 1.56, 0.64, 1.0)` 中 1.56 > 1 表示弹跳）。且 `产出类型 ∈ {research_report, wechat_article}`（正式产出）。 |
| **违规示例** | `animation: bounce 0.5s;` 或 `transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1.0);`（正式报告） |
| **修复建议** | 正式产出使用克制缓动：`cubic-bezier(0.25, 0.1, 0.25, 1.0)`（标准 ease-out）。弹跳动画仅允许在 course_material 的趣味交互场景。 |
| **来源标注** | Impeccable 禁用清单驱动理念·动效正式性约束 |

### ASR-MOTION-005: 禁自动播放动画

| 字段 | 内容 |
|------|------|
| **检测规则** | 正则 `animation:\s*.*\d+s.*infinite`（无限循环自动播放）且无 `animation-play-state:\s*paused` 声明，且非 loading 指示器上下文。 |
| **违规示例** | `animation: pulse 2s infinite;`（无暂停控制） |
| **修复建议** | 动画须提供用户控制（hover 触发 / scroll 触发 / 点击触发）。如需持续动画，添加 `prefers-reduced-motion` 媒体查询适配：`@media (prefers-reduced-motion: reduce) { animation: none; }`。 |
| **来源标注** | Impeccable 禁用清单驱动理念·无障碍动效约束 |

---

## 五、装饰禁令（ASR-DECO-001 ~ 005）

> **来源**: LC-026 Taste-Skill 反 Slop 内容/组件禁令 + Impeccable 禁用清单驱动理念
> **原理**: emoji、em-dash、霓虹光晕、毛玻璃堆叠是 AI 生成内容最易暴露的装饰噪音。资深设计师用图标系统替代 emoji，用排版节奏替代装饰符号。

### ASR-DECO-001: 禁 emoji 作为装饰

| 字段 | 内容 |
|------|------|
| **检测规则** | Unicode 范围检测：正则 `[\u{1F600}-\u{1F64F}]|[\u{1F300}-\u{1F5FF}]|[\u{1F680}-\u{1F6FF}]|[\u{1F700}-\u{1F77F}]|[\u{2600}-\u{26FF}]|[\u{2700}-\u{27BF}]`（覆盖表情/符号/交通/炼金术/杂项符号/装饰符号）。 |
| **违规示例** | `<h2>🚀 快速开始</h2>` 或 `<p>状态：✅ 已完成</p>` |
| **修复建议** | 替换为图标系统：Phosphor Icons / Radix Icons / Tabler Icons。示例：`<h2><PhosphorIcon name="rocket-launch" /> 快速开始</h2>`。图标具备一致的线宽和视觉权重，emoji 不具备。 |
| **来源标注** | LC-026 Taste-Skill 反 Slop 规则·内容禁令（禁止代码中使用 emoji） |

### ASR-DECO-002: 禁 em-dash（—）作为分隔符

| 字段 | 内容 |
|------|------|
| **检测规则** | 正则 `—`（U+2014 EM DASH）用于分隔上下文（前后均有文字且非引文标注场景）。AST 检查标题节点内含 `—`。 |
| **违规示例** | `<h1>性能优化 — 从理论到实践</h1>` 或 `<p>前端工程化 — 构建工具篇</p>` |
| **修复建议** | 标题中使用冒号 `:` 或竖线 `|` 替代。正文中使用破折号 `——`（中文双破折号）仅用于引文标注，不用于标题分隔。 |
| **来源标注** | LC-026 Taste-Skill 反 Slop 规则·内容禁令（禁止 em-dash 在标题中） |

### ASR-DECO-003: 禁阴影堆叠超过 3 层

| 字段 | 内容 |
|------|------|
| **检测规则** | AST 检查 `box-shadow` 属性值，按逗号分隔计数 shadow 层级 > 3 组。正则 `box-shadow:\s*.*,.+,.+,.+`（4 组及以上）。 |
| **违规示例** | `box-shadow: 0 1px 2px rgba(0,0,0,0.1), 0 2px 4px rgba(0,0,0,0.1), 0 4px 8px rgba(0,0,0,0.1), 0 8px 16px rgba(0,0,0,0.1);`（4 层） |
| **修复建议** | 最多保留 3 层阴影，且阴影须着色到背景色调（tinted shadows）。示例：`box-shadow: 0 1px 2px rgba(26,86,219,0.05), 0 4px 8px rgba(26,86,219,0.08);`（2 层着色阴影）。 |
| **来源标注** | LC-026 Taste-Skill 反 Slop 规则·组件禁令（卡片阴影着色）+ Impeccable 禁用清单 |

### ASR-DECO-004: 禁毛玻璃效果用于正文区域

| 字段 | 内容 |
|------|------|
| **检测规则** | 正则 `backdrop-filter:\s*blur` 且 AST 检查应用元素 `role == body`（正文段落容器）。 |
| **违规示例** | `article { backdrop-filter: blur(10px); background: rgba(255,255,255,0.5); }`（正文区域） |
| **修复建议** | 毛玻璃效果仅用于导航栏/侧边栏/浮层等非正文区域。正文区域使用实色背景或轻微透明度（`rgba(255,255,255,0.95)`）确保可读性。 |
| **来源标注** | Impeccable 禁用清单驱动理念·可读性优先约束 |

### ASR-DECO-005: 禁霓虹发光效果

| 字段 | 内容 |
|------|------|
| **检测规则** | AST 检查 `box-shadow` 值：含 `0 0` 模式（无偏移阴影）且 blur > 10px 且颜色饱和度 > 70%（HSL 中 S > 0.7）。正则 `box-shadow:\s*0\s+0\s+\d{2,}px.*hsl\(\d+,\s*[7-9]\d%` 或对应 hex 高饱和色。 |
| **违规示例** | `box-shadow: 0 0 20px #FF006E;`（无偏移 + 大模糊 + 高饱和） |
| **修复建议** | 移除发光效果，改用着色阴影（tinted shadow）：`box-shadow: 0 4px 12px rgba(255,0,110,0.15);`（有偏移 + 低透明度）。霓虹发光是 AI Purple/Blue 审美的典型装饰。 |
| **来源标注** | LC-026 Taste-Skill 反 Slop 规则·配色禁令（AI Purple/Blue 审美·霓虹渐变）+ Impeccable 禁用清单 |

---

## 六、配图禁令（ASR-IMAGE-001 ~ 005）

> **来源**: Impeccable 禁用清单驱动理念 + visual-dna.md 配图规范
> **原理**: AI 生成图片直接使用、低分辨率图片、无 Alt 文本、图片变形是配图质量的四大缺陷。资深设计师对每张图片做风格化处理、分辨率校验、无障碍标注。

### ASR-IMAGE-001: 禁 AI 生成图片直接使用

| 字段 | 内容 |
|------|------|
| **检测规则** | 图片元数据检测：EXIF/metadata 含 AI 生成标记（`Software: Midjourney`/`Software: DALL-E`/`Software: Stable Diffusion`/`generator` 字段）且无风格化处理（无滤镜/无色调调整/无裁切痕迹）。 |
| **违规示例** | 直接嵌入 Midjourney 生成的图片，未做任何后处理 |
| **修复建议** | AI 生成图片须经过风格化处理：色调调整（匹配 visual_dna 配色）、裁切构图优化、添加纹理/噪点统一质感。或使用 PaperBanana/excalidraw 生成与文档风格统一的插图。 |
| **来源标注** | Impeccable 禁用清单驱动理念·配图风格统一约束 |

### ASR-IMAGE-002: 禁低分辨率图片

| 字段 | 内容 |
|------|------|
| **检测规则** | 图片元数据检测：印刷场景 DPI < 300 或图片宽度 < 2480px（A4@300dpi）；Web 场景图片宽度 < 1920px（全宽图）或 < 800px（内容区图）。 |
| **违规示例** | 印刷报告中使用 72dpi 的 Web 图片；全宽 Banner 使用 800px 宽图片 |
| **修复建议** | 印刷场景：图片 ≥ 300dpi，A4 全宽 ≥ 2480px。Web 场景：全宽图 ≥ 1920px，内容区图 ≥ 1200px。提供 `srcset` 多分辨率适配。 |
| **来源标注** | Impeccable 禁用清单驱动理念·配图分辨率约束 + visual-dna.md 配图规范 |

### ASR-IMAGE-003: 禁无 Alt 文本的图片

| 字段 | 内容 |
|------|------|
| **检测规则** | AST 检查 `<img>` 标签：无 `alt` 属性，或 `alt=""`（空 alt，仅装饰图允许），且图片非纯装饰用途（AST 判断图片在内容流中而非背景层）。 |
| **违规示例** | `<img src="chart.png">`（无 alt）或 `<img src="diagram.png" alt="">`（内容图空 alt） |
| **修复建议** | 所有内容图片必须提供描述性 alt：`<img src="chart.png" alt="2024年Q1-Q4营收增长趋势图，从1.2亿增长至1.8亿">`。装饰图可使用 `alt=""` 但须添加 `role="presentation"`。 |
| **来源标注** | Impeccable 禁用清单驱动理念·无障碍约束 |

### ASR-IMAGE-004: 禁图片拉伸变形

| 字段 | 内容 |
|------|------|
| **检测规则** | CSS 检查 `object-fit:\s*fill` 或 AST 检查图片显示宽高比与原始宽高比偏差 > 5%（`displayRatio / naturalRatio` 偏差 > 0.05）。 |
| **违规示例** | `<img src="photo.jpg" style="width:100%; height:200px; object-fit:fill;">`（强制拉伸） |
| **修复建议** | 使用 `object-fit: cover`（裁切填充）或 `object-fit: contain`（完整显示）。确保容器宽高比与图片原始比例一致，使用 `aspect-ratio` CSS 属性。 |
| **来源标注** | Impeccable 禁用清单驱动理念·配图比例约束 |

### ASR-IMAGE-005: 禁图片与正文无间距

| 字段 | 内容 |
|------|------|
| **检测规则** | AST 检查 `<img>` 紧邻 `<p>`/`<h1>`-`<h6>`/`<li>` 等文本元素，且图片元素无 `margin`/`margin-bottom`/`margin-top` 声明（或值为 0）。 |
| **违规示例** | `<img src="figure.png"><p>如图所示...</p>`（无 margin） |
| **修复建议** | 图片与正文间须有明确间距：`img { margin-bottom: var(--space-md); }`（16px）。图注与图片间距 `margin-top: var(--space-xs);`（4px）。遵循 visual_dna 4px 栅格间距系统。 |
| **来源标注** | visual-dna.md §四 4px 基准栅格系统 + Impeccable 禁用清单 |

---

## 七、排版禁令（ASR-TYPO-001 ~ 006）

> **来源**: visual-dna.md §三 字体方案 + Impeccable 禁用清单驱动理念
> **原理**: 行长过长、行高过低、段落间距等于行高、标题层级过深、无段首缩进是中文排版的五大可读性杀手。资深设计师严格遵循中文排版规范。

### ASR-TYPO-001: 禁行长超过 75 个中文字符

| 字段 | 内容 |
|------|------|
| **检测规则** | 文本内容检测：每行中文字符数 > 75（含标点）。通过 `text-content` 提取 + 按容器宽度估算每行字符数，或直接检测 `max-width` / `width` 对应字符容量。 |
| **违规示例** | 正文容器宽度允许每行 80+ 中文字符 |
| **修复建议** | 限制正文容器宽度：中文正文每行 30-75 字符为宜。设置 `max-width: 42em;`（约 42 个中文字符宽度）或使用 visual_dna 栅格系统约束内容栏宽度。 |
| **来源标注** | Impeccable 禁用清单驱动理念·中文排版可读性约束 |

### ASR-TYPO-002: 禁行高低于 1.5（正文）

| 字段 | 内容 |
|------|------|
| **检测规则** | CSS 检查 `line-height` 值：正文字体（`role == body`）`line-height < 1.5`。无单位值和带单位值均检测。 |
| **违规示例** | `p { line-height: 1.3; }`（正文行高 1.3） |
| **修复建议** | 正文行高 ≥ 1.5，推荐 1.75（visual_dna 默认值）。中文排版因字符高度一致，行高需比西文更大。标题行高可降至 1.2-1.4。 |
| **来源标注** | visual-dna.md §三 字号阶梯（Body 行高 1.75）+ Impeccable 禁用清单 |

### ASR-TYPO-003: 禁段落间距等于行高

| 字段 | 内容 |
|------|------|
| **检测规则** | CSS 检查：`margin-bottom`（段落间距）== `line-height * font-size`（行高值）。段落间距与行高相同时，段落边界消失，可读性下降。 |
| **违规示例** | `p { font-size: 16px; line-height: 1.75; margin-bottom: 28px; }`（28px = 16px × 1.75，段落间距等于行高） |
| **修复建议** | 段落间距须明显大于行高：`margin-bottom: calc(var(--line-height) * 1.5);` 或使用 visual_dna 间距系统 `margin-bottom: var(--space-lg);`（24px）。段落间距 ≥ 行高 × 1.3。 |
| **来源标注** | Impeccable 禁用清单驱动理念·排版节奏约束 |

### ASR-TYPO-004: 禁标题层级超过 4 级

| 字段 | 内容 |
|------|------|
| **检测规则** | AST 检查 HTML 中出现 `<h5>` 或 `<h6>` 标签。标题层级超过 4 级（H1-H4）意味着信息结构过深，读者迷失。 |
| **违规示例** | `<h4>4.1.2.3 子节标题</h4>` 后跟 `<h5>4.1.2.3.1 更深层级</h5>` |
| **修复建议** | 超过 4 级的标题改用粗体段落或列表项替代：`<p><strong>4.1.2.3.1 更深层级</strong></p>`。重构信息结构，将深层级内容拆分为独立小节。 |
| **来源标注** | Impeccable 禁用清单驱动理念·信息层级约束 |

### ASR-TYPO-005: 禁无段首缩进的中文正文（学术场景除外）

| 字段 | 内容 |
|------|------|
| **检测规则** | AST 检查：中文正文段落（`lang="zh"` 或内容含中文字符 > 50%）+ 无 `text-indent` 声明 + `产出类型 != research_report`（学术场景使用西式顶格段落）。 |
| **违规示例** | 微信公众号文章中文正文段落无 `text-indent`，每段顶格 |
| **修复建议** | 中文正文段落添加段首缩进：`p { text-indent: 2em; }`（缩进 2 个字符宽度）。学术报告（research_report）可使用顶格 + 段间空行格式。 |
| **来源标注** | Impeccable 禁用清单驱动理念·中文排版规范约束 |

### ASR-TYPO-006: 禁数字使用比例字体（高密度场景）

| 字段 | 内容 |
|------|------|
| **检测规则** | CSS 检查：`VISUAL_DENSITY > 7`（高密度场景）时，数字内容（`<td>` 含数字/`<span class="number">`）未使用等宽字体（`font-variant-numeric: tabular-nums` 或 `font-family` 含 mono）。 |
| **违规示例** | VD=8 的仪表盘中数字使用比例字体，列对齐错乱 |
| **修复建议** | 高密度场景所有数字使用 `font-variant-numeric: tabular-nums;`（等宽数字）或等宽字体族（JetBrains Mono / Geist Mono）。确保数字列对齐。 |
| **来源标注** | LC-026 Taste-Skill 反 Slop 规则·排版禁令（VD>7 时所有数字必须使用等宽字体） |

---

## 八、数据可视禁令（ASR-VIZ-001 ~ 005）

> **来源**: Impeccable 禁用清单驱动理念 + visual-dna.md §九 LC 卡片对接规则
> **原理**: Matplotlib 默认配色、3D 饼图、无坐标轴标签、图例遮挡数据、彩虹色板误用是数据可视化的五大误导性缺陷。资深设计师遵循 Tufte 数据墨水比原则。

### ASR-VIZ-001: 禁默认 Matplotlib 配色

| 字段 | 内容 |
|------|------|
| **检测规则** | 图表代码检测：正则 `tab:blue|tab:orange|tab:green|tab:red|tab:purple|tab:brown|tab:pink|tab:gray|tab:olive|tab:cyan`（Matplotlib 默认 tab 色板）或未设置 `color`/`colormap` 参数（使用默认 `C0`-`C9` 循环色）。 |
| **违规示例** | `plt.plot(x, y)`（未指定 color，使用默认 tab:blue） |
| **修复建议** | 从 visual_dna 读取配色方案注入图表：`plt.plot(x, y, color='#1A56DB')`（学术蓝主色）。或使用 Nature/Cell 级学术配色包（data-viz-plots）。 |
| **来源标注** | Impeccable 禁用清单驱动理念·数据可视化配色约束 + visual-dna.md §九 LC-030 data-viz-plots 对接 |

### ASR-VIZ-002: 禁 3D 饼图

| 字段 | 内容 |
|------|------|
| **检测规则** | 图表代码检测：正则 `projection\s*=\s*['\"]3d['\"]` 且图表类型为 pie（`ax.pie(` 或 `plt.pie(`）。3D 饼图因透视畸变严重扭曲面积感知，是数据可视化的经典反模式。 |
| **违规示例** | `ax = fig.add_subplot(111, projection='3d'); ax.pie(sizes, labels=labels)` |
| **修复建议** | 使用 2D 饼图或更优的条形图/树状图替代。饼图仅适用于 ≤5 个分类且需展示占比关系的场景。分类 > 5 时改用水平条形图。 |
| **来源标注** | Impeccable 禁用清单驱动理念·数据可视化准确性约束 |

### ASR-VIZ-003: 禁无坐标轴标签的图表

| 字段 | 内容 |
|------|------|
| **检测规则** | 图表代码 AST 检查：Matplotlib 图表缺少 `ax.set_xlabel()` / `ax.set_ylabel()`；ECharts 图表缺少 `xAxis.name` / `yAxis.name`；Plotly 图表缺少 `xaxis.title` / `yaxis.title`。 |
| **违规示例** | `plt.plot(x, y); plt.show()`（无轴标签） |
| **修复建议** | 所有图表必须标注坐标轴：Matplotlib `ax.set_xlabel('时间（月）'); ax.set_ylabel('营收（亿元）')`。轴标签须含单位。饼图/桑基图等无坐标轴图表除外。 |
| **来源标注** | Impeccable 禁用清单驱动理念·数据可视化完整性约束 |

### ASR-VIZ-004: 禁图例遮挡数据

| 字段 | 内容 |
|------|------|
| **检测规则** | 图表渲染检测：图例 bounding box 与数据点/数据线 bounding box 重叠面积 > 5%。通过图表渲染后的坐标计算判断。Matplotlib 检查 `loc` 参数是否为默认值（`best` 可能遮挡）。 |
| **违规示例** | 图例默认放置在图表右上角，遮挡了该区域的数据峰值 |
| **修复建议** | 将图例放置在图表外部：Matplotlib `ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')`；ECharts `legend.top: 'bottom'`。或使用直接标注法（direct labeling）替代图例。 |
| **来源标注** | Impeccable 禁用清单驱动理念·数据可视化可读性约束 |

### ASR-VIZ-005: 禁彩虹色板用于顺序数据

| 字段 | 内容 |
|------|------|
| **检测规则** | 图表代码检测：正则 `cmap\s*=\s*['\"](jet|rainbow|hsv)['\"]` 且数据类型为 sequential（顺序型，如时间序列/温度/排名）。彩虹色板在顺序数据上制造虚假的分类边界。 |
| **违规示例** | `plt.scatter(x, y, c=values, cmap='jet')`（values 为连续温度数据） |
| **修复建议** | 顺序数据使用顺序型色板：`cmap='viridis'`（感知均匀）/ `cmap='Blues'`（单色渐变）/ `cmap='YlOrRd'`（黄-橙-红渐变）。分类数据才使用定性色板（`Set1`/`Set2`）。 |
| **来源标注** | Impeccable 禁用清单驱动理念·数据可视化色彩科学约束 |

---

## 九、硬门执行逻辑

### 9.1 执行流程

```
渲染输出产物（HTML/CSS/图片/图表代码/排版参数）
  ↓
步骤1: 扫描所有待检代码与资源
  - CSS: 提取所有样式声明
  - HTML: 构建 AST 树
  - 图片: 读取元数据与 EXIF
  - 图表: 解析图表库配置代码
  - 排版: 计算行长/行高/间距参数
  ↓
步骤2: 逐条检查 44 条禁令（ASR-FONT/COLOR/LAYOUT/MOTION/DECO/IMAGE/TYPO/VIZ）
  - 每条禁令独立检测，记录违规项
  - 检测顺序: FONT → COLOR → LAYOUT → MOTION → DECO → IMAGE → TYPO → VIZ
  ↓
步骤3: 违规判定
  IF 违规数 == 0:
    → 门禁通过，允许输出
  ELSE:
    → 门禁拒绝，返回违规清单
    → 触发穷尽重试（计入熔断计数）
  ↓
步骤4: 违规清单输出（格式见 §9.2）
```

### 9.2 违规清单格式

每条违规按以下格式输出：

```
[ASR-XXXX-NNN] 禁令描述
  ├─ 违规代码: <检测到的具体代码/值>
  ├─ 检测规则: <触发的检测规则说明>
  └─ 修复建议: <具体的修复方案>
```

**违规清单示例**：

```
[ASR-FONT-001] 禁 Inter 作为 Premium 产出字体
  ├─ 违规代码: font-family: "Inter", sans-serif; (research_report 场景)
  ├─ 检测规则: font-family.*Inter 且 产出类型=Premium
  └─ 修复建议: 替换为 Geist / Outfit / Cabinet Grotesk / Satoshi

[ASR-COLOR-001] 禁 AI 紫 #7C3AED 系
  ├─ 违规代码: --color-primary: #7C3AED;
  ├─ 检测规则: 色值在 #7C3AED ±10% 范围内 (H=263°, S=84%, L=58%)
  └─ 修复建议: 替换为学术蓝 #1A56DB 或暖调人文 #B45309

门禁结果: 拒绝输出（2 条违规）
重试状态: 已计入熔断计数（当前 1/3）
```

### 9.3 熔断机制

| 熔断状态 | 触发条件 | 行为 |
|---------|---------|------|
| 正常 | 重试次数 < 3 | 返回违规清单，触发重试 |
| 熔断 | 重试次数 >= 3 | 质量保持为最高分方案（详见 fuse-mechanism.md），ASR 硬门在质量保持方案上仍执行核心禁令检查（ASR-COLOR-001/002 + ASR-FONT-001），确保质量保持方案不违反最基础的审美底线 |

> **与 fuse-mechanism.md 一致性说明**: 本表熔断条件"重试次数 >= 3"与 fuse-mechanism.md 伪代码 `while attempt < 3`（最多 3 次尝试后质量保持）完全一致。质量保持策略统一为"选择最高分方案"，ASR 硬门在此质量保持方案上额外执行核心禁令检查（ASR-COLOR-001/002 + ASR-FONT-001），确保质量保持方案不违反最基础的审美底线。

> **质量保持后核心禁令复查失败处理**: 质量保持方案在 ASR 硬门核心禁令复查（ASR-COLOR-001/002 + ASR-FONT-001）中仍失败时，返回 `[FUSE-FAILED]` 错误，需人工介入。此场景意味着即使质量保持为最高分方案，其配色和字体仍违反最基础审美底线，无法自动修复，必须人工审查并调整渲染参数。

### 9.4 与 visual_dna 的关系

```
visual_dna 生成 → ASR 硬门检查 visual_dna 参数
  ├─ 通过: visual_dna 参数合法，继续渲染
  └─ 拒绝: visual_dna 参数违规，重新生成 visual_dna

渲染产物生成 → ASR 硬门检查渲染产物
  ├─ 通过: 允许输出
  └─ 拒绝: 返回违规清单，触发重试
```

> **注意**: ASR 硬门是 visual_dna 的强制约束层。visual_dna 生成的参数（配色/字体/布局/动效）本身不得违反 ASR 禁令。若 visual_dna 参数违规，须在 visual_dna 生成阶段即拦截。

---

## 十、融入 Impeccable 禁用清单驱动理念

> **来源技能标注**: Impeccable 禁用清单驱动理念（系统性剔除 AI 设计通病的方法论）

### 10.1 理念融入说明

Impeccable 的核心方法论是**禁用清单驱动**——通过系统性枚举并禁止 AI 设计的常见通病，倒逼生成高完成度界面。本 ASR 硬门禁用清单是这一理念在 profound-cognition 渲染管道中的具体实现：

| Impeccable 理念 | ASR 硬门实现 |
|----------------|-------------|
| 系统性剔除廉价渐变 | ASR-COLOR-005（禁高饱和度渐变）+ ASR-DECO-005（禁霓虹发光） |
| 系统性剔除光晕 | ASR-DECO-005（禁霓虹发光效果）+ ASR-DECO-003（禁阴影堆叠 >3 层） |
| 系统性剔除模板化布局 | ASR-LAYOUT-001（禁居中英雄区）+ ASR-LAYOUT-003（禁等宽三列卡片） |
| 细节精度对标资深设计师 | 全部 44 条禁令的检测规则均基于资深设计师的审查清单 |
| 输出高完成度界面 | 硬门执行逻辑确保零违规才允许输出 |

### 10.2 细节精度对标

ASR 硬门的每条禁令均对标资深设计师的审查维度：

| 资深设计师审查维度 | 对应 ASR 禁令 |
|-------------------|-------------|
| 字体选择是否有审美主张 | ASR-FONT-001~006 |
| 配色是否避开 AI 统计平均色 | ASR-COLOR-001~006 |
| 布局是否有栅格节奏 | ASR-LAYOUT-001~006 |
| 动效是否遵循物理直觉 | ASR-MOTION-001~005 |
| 装饰是否克制无噪音 | ASR-DECO-001~005 |
| 配图是否高清无障碍 | ASR-IMAGE-001~005 |
| 排版是否遵循中文规范 | ASR-TYPO-001~006 |
| 数据可视化是否准确无误导 | ASR-VIZ-001~005 |

### 10.3 高完成度界面保障

ASR 硬门通过"零违规才输出"的硬门机制保障高完成度：

1. **前置拦截**: 渲染产物落地前全量检查，违规即拒
2. **违规可追溯**: 每条违规附检测规则与修复建议，支持精准修复
3. **熔断质量保持**: 3 次尝试后熔断，质量保持为最高分方案（详见 fuse-mechanism.md），ASR 硬门在质量保持方案上仍执行核心禁令检查（ASR-COLOR-001/002 + ASR-FONT-001），确保质量保持方案不违反最基础的审美底线
4. **与 visual_dna 联动**: visual_dna 参数本身受 ASR 约束，从源头杜绝违规

---

## 十一、禁令统计与来源溯源

### 11.1 禁令统计

| 类别 | 前缀 | 条数 | 编号范围 |
|------|------|------|---------|
| 字体禁令 | ASR-FONT | 6 | 001-006 |
| 配色禁令 | ASR-COLOR | 6 | 001-006 |
| 布局禁令 | ASR-LAYOUT | 6 | 001-006 |
| 动效禁令 | ASR-MOTION | 5 | 001-005 |
| 装饰禁令 | ASR-DECO | 5 | 001-005 |
| 配图禁令 | ASR-IMAGE | 5 | 001-005 |
| 排版禁令 | ASR-TYPO | 6 | 001-006 |
| 数据可视禁令 | ASR-VIZ | 5 | 001-005 |
| **总计** | — | **44** | — |

### 11.2 来源溯源

| 来源 | 贡献禁令 | 标注方式 |
|------|---------|---------|
| LC-026 Taste-Skill 反 Slop 规则 | ASR-FONT-001/002/003/006, ASR-COLOR-001/002/006, ASR-LAYOUT-001/002/003/006, ASR-MOTION-001, ASR-DECO-001/002/003/005, ASR-TYPO-006 | `LC-026 Taste-Skill 反 Slop 规则·XXX` |
| Impeccable 禁用清单驱动理念 | ASR-FONT-005, ASR-COLOR-003/004/005, ASR-LAYOUT-004/005, ASR-MOTION-002/003/004/005, ASR-DECO-004/005, ASR-IMAGE-001/002/003/004/005, ASR-TYPO-001/003/004/005, ASR-VIZ-001/002/003/004/005 | `Impeccable 禁用清单驱动理念·XXX` |
| visual-dna.md 渲染管道规范 | ASR-FONT-004, ASR-LAYOUT-004, ASR-MOTION-002, ASR-IMAGE-005, ASR-TYPO-002/005, ASR-VIZ-001 | `visual-dna.md §X XXX` |

---

> 知识来源: LC-026 Taste-Skill (Leonxlnx/taste-skill) 反 Slop 规则 + Impeccable 禁用清单驱动理念 + visual-dna.md 渲染管道规范
