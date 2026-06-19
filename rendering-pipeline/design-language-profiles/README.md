<!-- 作者：阿洋 -->

# 设计语言画像库 (Design Language Profiles, DLP)

> **定位**: Visual DNA 审美进化层。将 Visual DNA 中枢从"抽象描述符"升级为"具象参考"——每个 DLP 锚定一个真实世界的设计语言实体（Nature 正刊 / Linear UI / Economist 排版等），为 `visual_dna` 生成提供可追溯、可复现的具象锚点。
> **强制规则**: DLP 检索器在 Taste-Skill 生成 `visual_dna` 前必须命中一个 DLP，未命中时回退到 `DLP-nature`（学术严谨默认锚点）。

---

## 一、DLP 库总览

DLP 库共收录 **16 个具名设计语言画像**，按视觉基因相似度归为 **4 族**。每个 DLP 锚定一个真实世界的设计实体，所有配色、字体、栅格参数均来自该实体的公开版式规范，禁止 AI 凭空生成。

| 族 (Family) | DLP 数量 | 族特征 | 族默认锚点 |
|-------------|---------|--------|-----------|
| academic-journal | 4 | 衬线正文、双栏栅格、低饱和配色、印刷媒介、零动效 | DLP-nature |
| interface-brand | 4 | 无衬线字体、单栏响应式、品牌色驱动、微动效、圆角阴影 | DLP-linear |
| publication-typesetting | 4 | 杂志级排版、强字体层级、图文混排、叙事动效 | DLP-economist |
| data-visualization | 4 | 图表优先、数据色板、Tufte 纪律、图表字体 | DLP-economist-chart |

### 1.1 DLP 完整清单

| DLP 名称 | 族 | 锚定实体 | 主色 | 辅色 | 文件 |
|---------|-----|---------|------|------|------|
| DLP-nature | academic-journal | Nature 正刊 2024 年版式 | #000000 | #E60012 | DLP-nature.md |
| DLP-science | academic-journal | Science 正刊 2024 年版式 | #1A1A1A | #F47C20 | DLP-science.md |
| DLP-ieee | academic-journal | IEEE/ACM 正刊 2024 年版式 | #000000 | #00629B | DLP-ieee.md |
| DLP-springer | academic-journal | Springer Nature 期刊 2024 年版式 | #1A1A1A | #005CAB | DLP-springer.md |
| DLP-linear | interface-brand | Linear App 2024 界面 | #5E6AD2 | #26282D | DLP-linear.md |
| DLP-aesop | interface-brand | Aesop 官网 2024 界面 | #455A64 | #D4C5B9 | DLP-aesop.md |
| DLP-stripe-press | interface-brand | Stripe Press 2024 界面 | #635BFF | #0A2540 | DLP-stripe-press.md |
| DLP-gov-uk | interface-brand | GOV.UK Design System 2024 | #1D70B8 | #003078 | DLP-gov-uk.md |
| DLP-economist | publication-typesetting | The Economist 2024 版式 | #E3120B | #1A1A1A | DLP-economist.md |
| DLP-ted | publication-typesetting | TED 演讲幻灯片 2024 版式 | #E62B1E | #000000 | DLP-ted.md |
| DLP-newyorker | publication-typesetting | The New Yorker 2024 版式 | #1A1A1A | #C8102E | DLP-newyorker.md |
| DLP-kami | publication-typesetting | Kami 纸质美学 2024 版式 | #2C2C2C | #B8956A | DLP-kami.md |
| DLP-economist-chart | data-visualization | Economist 图表规范 2024 | #E3120B | #006BA2 | DLP-economist-chart.md |
| DLP-scienceplots | data-visualization | SciencePlots Python 库风格 | #0AA398 | #E69F00 | DLP-scienceplots.md |
| DLP-nature-figure | data-visualization | Nature 图表规范 2024 | #0066CC | #E60012 | DLP-nature-figure.md |
| DLP-plotivy | data-visualization | Plotly 美学模板 2024 | #636EFA | #EF553B | DLP-plotivy.md |

> **注**: 本批次创建文件 1-5（README + 4 个 academic-journal 族 DLP）。其余 12 个 DLP 文件由后续批次补全，清单先行登记以锁定命名空间与配色占位。

---

## 二、族分类总览

### 2.1 academic-journal 族（学术期刊族）

**族特征**:
- **媒介**: 印刷优先（PDF/纸质），数字为辅
- **栅格**: 双栏为主（Nature/Science/IEEE），单栏为辅（Springer 预印本）
- **字体**: 衬线正文（Times New Roman / Latin Modern Roman），中文 fallback 宋体
- **配色**: 极简（黑+品牌色+链接蓝），饱和度低，零渐变
- **圆角阴影**: 全直角（0px），零阴影
- **动效**: N/A（印刷媒介无动效）
- **字号单位**: pt 为主（印刷点），px 为辅（数字渲染）

**族成员**: DLP-nature / DLP-science / DLP-ieee / DLP-springer

**族适用场景**: 学术论文、期刊投稿、同行评审、预印本、工程研究、科学研究

### 2.2 interface-brand 族（界面品牌族）

**族特征**:
- **媒介**: 数字优先（Web/App），响应式
- **栅格**: 单栏响应式，12 列栅格，断点驱动
- **字体**: 无衬线为主（Inter / Söhne / Helvetica Neue），几何感强
- **配色**: 品牌色驱动，中性色丰富（zinc/slate 灰阶），暗色模式支持
- **圆角阴影**: 中等圆角（6-12px），柔和阴影（elevation 分层）
- **动效**: 微动效（150-300ms），ease-out 为主

**族成员**: DLP-linear / DLP-aesop / DLP-stripe-press / DLP-gov-uk

**族适用场景**: SaaS 产品、品牌官网、设计系统、政府公共服务、电商

### 2.3 publication-typesetting 族（出版物排版族）

**族特征**:
- **媒介**: 混合（印刷+数字），长文阅读优先
- **栅格**: 多栏（2-3 栏），基线网格严格
- **字体**: 强字体层级（Display + Body + Caption），衬线/无衬线混排
- **配色**: 编辑色板（红/黑/米白），低饱和高对比
- **圆角阴影**: 直角为主，零阴影（印刷感）
- **动效**: 叙事动效（滚动驱动、视差），600-1000ms

**族成员**: DLP-economist / DLP-ted / DLP-newyorker / DLP-kami

**族适用场景**: 新闻杂志、深度报道、演讲幻灯片、文学出版物、品牌叙事

### 2.4 data-visualization 族（数据可视化族）

**族特征**:
- **媒介**: 图表优先（SVG/Canvas），嵌入文档
- **栅格**: 图表内栅格（坐标轴网格），无页面栅格
- **字体**: 数据字体（无衬线小字号），轴标签 8-10pt
- **配色**: 数据色板（8-12 色序数色），色盲安全，Tufte 纪律
- **圆角阴影**: 直角（数据精确性优先），零阴影
- **动效**: 入场动效（400-800ms），数据标记逐点绘制

**族成员**: DLP-economist-chart / DLP-scienceplots / DLP-nature-figure / DLP-plotivy

**族适用场景**: 数据图表、统计可视化、学术配图、交互式仪表盘

---

## 三、DLP 元规范（12 字段强制 schema）

每个 DLP 文件**必须**包含以下 12 个字段，字段值**必须具象**（十六进制色值 / px / rem / pt / cm / inch 等可量化单位），禁止使用形容词（如"优雅的""现代的"）。

### 3.1 字段定义

| 序号 | 字段名 | 类型 | 说明 | 示例 |
|-----|--------|------|------|------|
| 1 | `name` | string | DLP 唯一标识，格式 `DLP-{entity}` | `DLP-nature` |
| 2 | `anchor` | string | 锚定真实世界实体的描述（含年份） | `"Nature 正刊 2024 年版式"` |
| 3 | `family` | enum | 族分类，4 选 1 | `academic-journal` |
| 4 | `color_palette` | object | 6 色板（主/辅/强调/中性/背景/文本），全部十六进制 | `{primary: "#000000", ...}` |
| 5 | `typography_scale` | object | 字号阶梯（h1-h4/body/caption/footnote），含 px/rem/pt | `{h1: "24px/1.5rem", ...}` |
| 6 | `font_stack` | object | 字体栈（西文/中文/等宽），含 fallback | `{western: '"Times New Roman", serif', ...}` |
| 7 | `font_weight_pairing` | object | 字重配对（标题/正文/强调） | `{heading: "bold(700)", ...}` |
| 8 | `spacing_system` | object | 间距系统（基准+阶梯） | `{base: "4px", scale: "4/8/12/16/24/32px"}` |
| 9 | `grid_system` | object | 栅格系统（栏数/列宽/槽宽/页边距/断点） | `{columns: "双栏", ...}` |
| 10 | `radius_shadow` | object | 圆角与阴影 | `{radius: "0px", shadow: "none"}` |
| 11 | `motion_curve` | object | 动效曲线（印刷媒介填 N/A） | `{easing: "N/A", ...}` |
| 12 | `applicable_scenarios` | array | 适用场景列表 | `["学术论文", "期刊投稿"]` |

### 3.2 字段值约束

1. **color_palette**: 6 个色值全部为 6 位十六进制（`#RRGGBB`），禁止 3 位缩写、禁止 `rgba()`、禁止 CSS 变量名
2. **typography_scale**: 字号必须同时给出 px 和 pt/rem 换算（`10pt/13.33px`），行高必须给出（`1.5`）
3. **font_stack**: 必须包含中文 fallback（`"宋体", "SimSun", serif` 或 `"黑体", "SimHei", sans-serif`），西文字体在前
4. **grid_system**: 印刷媒介用 cm/inch，数字媒介用 px，断点印刷媒介填 `N/A`
5. **motion_curve**: 印刷媒介填 `N/A(印刷媒介)`，数字媒介必须给出 cubic-bezier 值
6. **applicable_scenarios**: 至少 2 个场景，中文描述

### 3.3 YAML frontmatter 模板

每个 DLP 文件**必须**以 YAML frontmatter 开头，包含 12 字段完整定义：

```yaml
---
name: "DLP-{entity}"
anchor: "{锚定实体} {年份} 年版式"
family: "{academic-journal|interface-brand|publication-typesetting|data-visualization}"

color_palette:
  primary: "#RRGGBB"       # 主色
  secondary: "#RRGGBB"     # 辅色
  accent: "#RRGGBB"        # 强调色
  neutral: "#RRGGBB"       # 中性色
  background: "#RRGGBB"    # 背景色
  text: "#RRGGBB"          # 文本色

typography_scale:
  h1: "{px}/{rem}"
  h2: "{px}/{rem}"
  h3: "{px}/{rem}"
  h4: "{px}/{rem}"
  body: "{pt}/{px}"
  caption: "{pt}/{px}"
  footnote: "{pt}/{px}"

font_stack:
  western: '"{西文字体}", fallback, serif|sans-serif'
  chinese: '"{中文字体}", "SimSun"|"SimHei", serif|sans-serif'
  monospace: '"{等宽字体}", "Courier New", monospace'

font_weight_pairing:
  heading: "bold(700)"
  body: "regular(400)"
  emphasis: "italic(400)"

spacing_system:
  base: "4px"
  scale: "4/8/12/16/24/32px"

grid_system:
  columns: "{单栏|双栏|三栏|12列}"
  column_width: "{cm|inch|px}"
  gutter: "{cm|inch|px|N/A}"
  margin: "{cm|inch|px}"
  breakpoint: "{N/A|sm:640px/md:768px/lg:1024px/xl:1280px}"

radius_shadow:
  radius: "{px}"
  shadow: "none|{box-shadow值}"

motion_curve:
  easing: "N/A(印刷媒介)|cubic-bezier(...)"
  duration: "N/A|{ms}"

applicable_scenarios:
  - "{场景1}"
  - "{场景2}"
---
```

---

## 四、DLP 检索规范

DLP 检索器是 Taste-Skill 的前置模块，负责从 16 个 DLP 中选择最匹配当前任务的 DLP，作为 `visual_dna` 生成的具象锚点。

### 4.1 检索输入

DLP 检索器接收 3 个输入参数（与 Taste-Skill 的 3 参数控制对齐）：

| 参数 | 取值范围 | 权重 |
|------|---------|------|
| `content_theme` | 任意文本描述 | 40% |
| `output_type` | research_report / wechat_article / course_material | 35% |
| `target_audience` | academic / general / professional / youth | 25% |

### 4.2 检索算法

```
输入: content_theme + output_type + target_audience
  ↓
Step 1: 族预筛选
  - output_type == research_report AND target_audience == academic
    → 候选族 = [academic-journal, data-visualization]
  - output_type == wechat_article AND target_audience IN [general, youth]
    → 候选族 = [interface-brand, publication-typesetting]
  - output_type == course_material
    → 候选族 = [interface-brand, publication-typesetting]
  ↓
Step 2: 族内 DLP 匹配
  - 在候选族内，按 content_theme 关键词匹配 DLP 的 applicable_scenarios
  - 匹配度 = 关键词命中率 × 0.6 + 族权重 × 0.4
  ↓
Step 3: 冲突裁决
  - 多个 DLP 匹配度相同时，按族优先级裁决:
    academic-journal > data-visualization > publication-typesetting > interface-brand
  - 仍无法裁决时，使用族默认锚点
  ↓
Step 4: 输出
  - 返回命中的 DLP 名称（如 "DLP-nature"）
  - 未命中时回退到 DLP-nature（学术严谨默认锚点）
```

### 4.3 检索映射表

| content_theme | output_type | target_audience | 命中 DLP |
|--------------|-------------|-----------------|---------|
| 学术论文/期刊投稿/同行评审 | research_report | academic | DLP-nature |
| 跨学科研究/科学前沿 | research_report | academic | DLP-science |
| 工程研究/计算机科学/电子工程 | research_report | academic | DLP-ieee |
| 预印本/arXiv | research_report | academic | DLP-springer |
| SaaS 产品/项目管理/开发者工具 | wechat_article | professional | DLP-linear |
| 奢侈品/护肤/极简品牌 | wechat_article | general | DLP-aesop |
| 金融科技/支付/开发者文档 | wechat_article | professional | DLP-stripe-press |
| 政府公共服务/政策解读 | wechat_article | general | DLP-gov-uk |
| 新闻杂志/深度报道/全球议题 | wechat_article | general | DLP-economist |
| 演讲/分享/灵感/创意 | course_material | youth | DLP-ted |
| 文学/散文/长篇叙事 | wechat_article | general | DLP-newyorker |
| 纸质美学/手作/日式极简 | wechat_article | general | DLP-kami |
| 数据图表/统计可视化/经济数据 | research_report | academic | DLP-economist-chart |
| 科研绘图/Python/Matplotlib | research_report | academic | DLP-scienceplots |
| 学术配图/Nature/Cell 级图表 | research_report | academic | DLP-nature-figure |
| 交互式图表/仪表盘/Plotly | research_report | professional | DLP-plotivy |

### 4.4 检索回退策略

| 条件 | 回退动作 |
|------|---------|
| 3 参数均未提供 | 使用 DLP-nature（学术严谨默认锚点） |
| 族预筛选无匹配 | 使用 DLP-nature |
| 族内 DLP 匹配度均为 0 | 使用族默认锚点 |
| content_theme 为空 | 按 output_type + target_audience 检索 |
| 多 DLP 匹配度并列最高 | 按族优先级裁决 |

### 4.5 检索输出规范

```yaml
dlp_retriever_output:
  matched_dlp: "DLP-{entity}"
  matched_family: "{family}"
  match_score: 0.85
  exhaust_retry_used: false
  exhaust_retry_reason: null
  candidate_dlps:
    - dlp: "DLP-nature"
      score: 0.85
    - dlp: "DLP-springer"
      score: 0.72
  visual_dna_anchor: "DLP-{entity} 的 12 字段将作为 visual_dna 生成的具象锚点"
```

---

## 五、融入 brand-identity-skill 元规则

brand-identity-skill 是统一品牌视觉语言的元规则集，DLP 库作为其具象锚点层，提供可追溯的真实世界参考。两者关系：**brand-identity-skill 定义"如何统一品牌视觉"，DLP 库提供"统一成什么样"的具象样本**。

### 5.1 brand-identity-skill 消费 DLP 的 3 条元规则

#### 元规则 1: 配色锚定规则

brand-identity-skill 在生成品牌配色时，**必须**从命中的 DLP 的 `color_palette` 6 色板中提取基色，按以下映射注入 `visual_dna.color_scheme`：

| DLP color_palette 字段 | visual_dna.color_scheme 字段 | 映射规则 |
|------------------------|------------------------------|---------|
| `primary` | `--color-primary` | 直接映射，作为标题/重点强调色 |
| `secondary` | `--color-secondary` | 直接映射，作为次要强调/数据高亮色 |
| `accent` | `--color-accent` | 直接映射，作为关键警示/CTA 色 |
| `neutral` | `--color-text-secondary` | 直接映射，作为次要文字/图注色 |
| `background` | `--color-bg` | 直接映射，作为页面主背景 |
| `text` | `--color-text` | 直接映射，作为正文主文字色 |

**禁止行为**: brand-identity-skill 不得凭空生成未在 DLP `color_palette` 中定义的色值；如需扩展色板（语义色），必须基于 DLP 6 色板派生（调亮/调暗 10-20%），并记录派生链。

#### 元规则 2: 字体栈继承规则

brand-identity-skill 在生成品牌字体方案时，**必须**完整继承命中的 DLP 的 `font_stack` 三栈（西文/中文/等宽），按以下映射注入 `visual_dna.font_scheme`：

| DLP font_stack 字段 | visual_dna.font_scheme 字段 | 映射规则 |
|---------------------|----------------------------|---------|
| `western` | 标题/正文字体族（西文部分） | 作为 font-family 的首选字体 |
| `chinese` | 标题/正文字体族（中文部分） | 作为 font-family 的中文 fallback |
| `monospace` | 代码字体族 | 作为 code/pre 的 font-family |

**字体栈拼接规则**: `font-family: {western}, {chinese};`（西文在前，中文在后，确保西文字符优先用西文字体渲染）

**字号阶梯规则**: brand-identity-skill 必须采用 DLP 的 `typography_scale` 字号阶梯，不得自行调整字号比例；如需适配数字媒介，可按 1pt = 1.333px 换算。

#### 元规则 3: 图形规范继承规则

brand-identity-skill 在生成品牌图形规范时，**必须**继承命中的 DLP 的以下字段：

| DLP 字段 | brand-identity-skill 消费点 | 映射规则 |
|---------|----------------------------|---------|
| `grid_system` | 品牌栅格系统 | 列数/列宽/槽宽/页边距直接继承 |
| `spacing_system` | 品牌间距系统 | 基准+阶梯直接继承 |
| `radius_shadow` | 品牌圆角阴影 | 圆角值+阴影值直接继承 |
| `motion_curve` | 品牌动效曲线 | 缓动函数+时长直接继承（印刷媒介则禁用动效） |

**禁止行为**: brand-identity-skill 不得在 DLP `radius_shadow` 为 `0px/none` 时为元素添加圆角或阴影（学术期刊族强制直角零阴影）。

### 5.2 brand-identity-skill 与 DLP 的协作流程

```
任务输入: content_theme + output_type + target_audience
  ↓
Step 1: DLP 检索器命中 DLP-{entity}
  ↓
Step 2: brand-identity-skill 读取 DLP-{entity} 的 12 字段
  ↓
Step 3: brand-identity-skill 按 3 条元规则将 DLP 字段注入 visual_dna
  - 元规则 1: color_palette → visual_dna.color_scheme
  - 元规则 2: font_stack + typography_scale → visual_dna.font_scheme
  - 元规则 3: grid_system + spacing_system + radius_shadow + motion_curve → visual_dna.grid_system / line_style / motion_profile
  ↓
Step 4: Taste-Skill 接收带 DLP 锚点的 visual_dna，执行审美等级判定与设计语言匹配
  ↓
Step 5: 渲染管道消费 visual_dna，所有渲染输出可追溯到 DLP-{entity} 的具象参数
```

### 5.3 品牌视觉语言统一性校验

brand-identity-skill 在完成 visual_dna 注入后，必须执行以下校验：

| 校验项 | 校验规则 | 失败处理 |
|--------|---------|---------|
| 配色可追溯性 | visual_dna.color_scheme 的每个色值必须能在 DLP color_palette 中找到源色或派生链 | 拒绝注入，回退到 DLP 原始色值 |
| 字体栈完整性 | visual_dna.font_scheme 的 font-family 必须包含 DLP font_stack 的西文+中文 fallback | 补全缺失的 fallback |
| 字号阶梯一致性 | visual_dna.font_scheme 的字号比例必须与 DLP typography_scale 一致（允许 1pt=1.333px 换算误差） | 调整为 DLP 字号阶梯 |
| 圆角阴影合规性 | visual_dna 的圆角/阴影不得超出 DLP radius_shadow 的定义（DLP 为 0px 时禁止圆角） | 强制回退到 DLP 值 |
| 动效合规性 | DLP motion_curve 为 N/A 时，visual_dna 不得包含动效定义 | 清空动效参数 |

---

## 六、DLP 库扩展规范

### 6.1 新增 DLP 流程

1. **锚定真实实体**: 必须锚定一个真实世界的设计语言实体（期刊/品牌/出版物/可视化库），含年份
2. **族归属判定**: 按 4 族特征归入对应族，无法归类时新建族（需更新本 README）
3. **12 字段填写**: 按元规范完整填写 12 字段，字段值必须具象
4. **配色可追溯**: 配色必须来自锚定实体的公开版式规范，附来源说明
5. **字体栈含中文 fallback**: 西文字体在前，中文 fallback 在后
6. **检索映射登记**: 在本 README §4.3 检索映射表中登记 content_theme → DLP 映射
7. **brand-identity-skill 元规则兼容**: 新 DLP 必须兼容 §5 的 3 条元规则

### 6.2 DLP 命名规范

- 格式: `DLP-{entity}`
- entity 用小写英文，多词用连字符（如 `DLP-stripe-press`）
- 文件名: `DLP-{entity}.md`
- 不得使用中文、空格、下划线

### 6.3 DLP 版本管理

- DLP 锚定实体的年份版本（如 "Nature 正刊 2024 年版式"）在 `anchor` 字段中记录
- 锚定实体更新版式时，新建 DLP 文件（如 `DLP-nature-2025.md`），旧 DLP 保留
- 不得直接修改已发布 DLP 的 12 字段（破坏可追溯性）

---

## 七、与 Visual DNA 的关系

### 7.1 定位差异

| 维度 | Visual DNA | DLP 库 |
|------|-----------|--------|
| 抽象层级 | 抽象描述符（变量名+色值） | 具象参考（真实实体锚点） |
| 生成时机 | 渲染管道启动时生成 | 预先定义，检索时命中 |
| 可追溯性 | 参数来自 Taste-Skill 算法 | 参数来自真实世界实体 |
| 数量 | 每次渲染生成 1 个 | 16 个预设 DLP |
| 可变性 | 渲染过程中不可变 | 锚定实体更新时新增 DLP |

### 7.2 协作流程

```
DLP 库（16 个预设具象锚点）
  ↓ DLP 检索器命中
DLP-{entity}（1 个具象参考）
  ↓ brand-identity-skill 注入
visual_dna（带 DLP 锚点的抽象描述符）
  ↓ Taste-Skill 仲裁
渲染管道消费（所有输出可追溯到 DLP-{entity}）
```

### 7.3 审美进化意义

DLP 库将 Visual DNA 中枢从"抽象描述符"升级为"具象参考"：

1. **可追溯**: 每个 visual_dna 参数可追溯到真实世界实体（如"这个配色来自 Nature 正刊 2024 年版式"）
2. **可复现**: 相同输入必命中相同 DLP，生成相同 visual_dna，确保渲染结果可复现
3. **可对标**: 渲染输出可与锚定实体直接对标（如"这个 PDF 版式是否符合 Nature 正刊规范"）
4. **可扩展**: 新增 DLP 即可扩展审美覆盖面，无需修改 Visual DNA 生成算法

> 知识来源: Visual DNA 审美进化项目 / brand-identity-skill 元规则 / Taste-Skill 全局审美总控
