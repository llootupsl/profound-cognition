<!-- 作者：阿洋 -->

# 视觉 DNA 生成规范 (Visual DNA Specification)

> **定位**: 渲染管道第一步，生成唯一视觉DNA，后续所有渲染动作必须读取并遵循此DNA。
> **强制规则**: 任何元素不得偏离视觉DNA定义。

---

## 一、视觉DNA 生成流程

### 1.1 生成时机
渲染管道启动时，第一步生成唯一 `visual_dna_id`，格式为 `VDNA-{timestamp}-{hash8}`。

### 1.2 生成逻辑
```
输入: 内容主题 + 产品类型 + 目标受众
  ↓
Taste-Skill 审美分析 → 生成视觉DNA
  ↓
输出: visual_dna 对象（含配色/字体/栅格/线条/动效全量参数）
```

### 1.3 视觉DNA 结构
```yaml
visual_dna:
  dna_id: "VDNA-20260613-a1b2c3d4"
  generated_at: "2026-06-13T00:00:00Z"
  content_theme: "主题描述"
  output_type: "research_report | wechat_article | course_material"

  color_scheme: { ... }    # 见 §二
  font_scheme: { ... }     # 见 §三
  grid_system: { ... }     # 见 §四
  line_style: { ... }      # 见 §五
  motion_profile: { ... }  # 见 §六
```

---

## 二、配色方案 (Color Scheme)

### 2.1 五色板定义

| 色板角色 | 变量名 | 示例值（DLP-nature） | 说明 |
|---------|--------|-----------------|------|
| 主色 Primary | `--color-primary` | `#000000` | 标题、重点强调、链接 |
| 辅色 Secondary | `--color-secondary` | `#E60012` | 次要强调、数据高亮、图表辅色 |
| 强调色 Accent | `--color-accent` | `#0066CC` | 关键警示、CTA按钮、异常标注 |
| 背景色 Background | `--color-bg` | `#FFFFFF` | 页面主背景 |
| 文字色 Text | `--color-text` | `#1A1A1A` | 正文主文字色 |

### 2.2 扩展色板（语义色）

| 变量名 | 示例值 | 用途 |
|--------|--------|------|
| `--color-bg-alt` | `#F9FAFB` | 交替背景（表格斑马纹、代码块） |
| `--color-border` | `#E5E7EB` | 边框、分割线 |
| `--color-text-secondary` | `#6B7280` | 次要文字、图注、脚注 |
| `--color-success` | `#059669` | 正向指标、通过标记 |
| `--color-warning` | `#D97706` | 警告标记、需注意 |
| `--color-error` | `#DC2626` | 错误标记、高风险 |
| `--color-info` | `#2563EB` | 信息标记、中性提示 |

### 2.3 配色方案来源

配色方案不再使用预设色板，改由 DLP 检索器命中的 DLP 的 `color_palette` 字段提供 6 色板具象值（primary/secondary/accent/neutral/background/text）。所有配色参数可追溯到 DLP 锚定实体（如 Nature 正刊、Linear App、The Economist 等）。详见 `design-language-profiles/` 目录与 `dlp-retriever.md` §六适配器输出。

---

## 三、字体方案 (Font Scheme)

### 3.1 字体族定义

| 用途 | 西文字体 | 中文字体 | CSS font-family | 备选穷尽尝试 |
|------|---------|---------|----------------|---------|
| 标题 Heading | Inter | 思源黑体 / 阿里巴巴普惠体 | `"Inter", "Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif` | Arial + 微软雅黑 |
| 正文 Body | Source Serif 4 | 思源宋体 / 方正书宋 | `"Source Serif 4", "Noto Serif SC", "STSong", "SimSun", serif` | Georgia + 宋体 |
| 代码 Code | JetBrains Mono | — | `"JetBrains Mono", "Cascadia Code", "Fira Code", "Consolas", monospace` | Courier New |

### 3.2 字号阶梯（基于 4px 栅格）

| 层级 | 用途 | 字号 | 行高 | 字重 |
|------|------|------|------|------|
| H1 | 文档主标题 | 32px | 1.2 | 700 |
| H2 | 章节标题 | 24px | 1.3 | 600 |
| H3 | 小节标题 | 20px | 1.4 | 600 |
| H4 | 子节标题 | 16px | 1.5 | 600 |
| Body | 正文 | 16px | 1.75 | 400 |
| Small | 图注/脚注 | 14px | 1.6 | 400 |
| Caption | 表格标题/元数据 | 12px | 1.5 | 400 |
| Code | 代码块 | 14px | 1.6 | 400 |

---

## 四、4px 基准栅格系统

### 4.1 栅格基准
所有间距、圆角、尺寸均以 **4px** 为最小基准单位，确保像素对齐。

### 4.2 圆角规范

| 元素类型 | 圆角值 | 说明 |
|---------|--------|------|
| 卡片/Card | 8px (2×4) | 内容卡片、信息面板 |
| 按钮/Button | 6px (1.5×4) | 交互按钮 |
| 输入框/Input | 6px (1.5×4) | 表单输入 |
| 图片/Image | 4px (1×4) | 插图圆角 |
| 标签/Tag | 4px (1×4) | 状态标签、分类标签 |
| 代码块/Code | 4px (1×4) | 代码区域 |

### 4.3 间距规范

| 间距类型 | 值 | 用途 |
|---------|-----|------|
| xs | 4px | 图标与文字间距、紧密元素 |
| sm | 8px | 列表项间距、标签内边距 |
| md | 16px | 段落间距、卡片内边距 |
| lg | 24px | 章节间距、区块间距 |
| xl | 32px | 大标题下方间距、主要区块分隔 |
| 2xl | 48px | 页面级区块分隔 |
| 3xl | 64px | 文档级大分隔 |

---

## 五、线条质感规范

### 5.1 线条参数

| 用途 | 粗细 | 颜色 | 端点样式 | 连接样式 |
|------|------|------|---------|---------|
| 分割线/水平线 | 1px | `--color-border` | — | — |
| 表格边框 | 1px | `--color-border` | — | — |
| 图表轴线 | 1.5px | `--color-text-secondary` | — | — |
| 数据线（折线图） | 2px | `--color-primary` | round | round |
| 强调边框 | 2px | `--color-primary` | — | — |
| 流程图连线 | 1.5px | `--color-text-secondary` | round | round |
| 虚线（辅助线） | 1px | `--color-border` | — | — |
| 手绘风格线 | 1.5px | `--color-primary` | round | round |

### 5.2 虚线模式

| 模式 | dasharray | 用途 |
|------|-----------|------|
| 短虚线 | `4, 4` | 辅助参考线 |
| 长虚线 | `8, 4` | 边界分隔 |
| 点线 | `2, 4` | 投影线、引导线 |

---

## 六、动效速率规范

### 6.1 标准缓动曲线

| 用途 | CSS easing | cubic-bezier | 说明 |
|------|-----------|-------------|------|
| 入场（标准） | ease-out | `cubic-bezier(0.25, 0.1, 0.25, 1.0)` | 元素出现、淡入、上滑 |
| 出场（标准） | ease-in | `cubic-bezier(0.42, 0.0, 1.0, 1.0)` | 元素消失、淡出 |
| 循环/往复 | ease-in-out | `cubic-bezier(0.42, 0.0, 0.58, 1.0)` | 持续动画、脉冲、呼吸 |
| 弹性回弹 | — | `cubic-bezier(0.34, 1.56, 0.64, 1.0)` | 强调出现、弹入 |
| 减速停止 | — | `cubic-bezier(0.0, 0.0, 0.2, 1.0)` | Material Design 标准缓出 |

### 6.2 动效时长规范

| 动效类型 | 时长范围 | 典型值 | 适用场景 |
|---------|---------|--------|---------|
| 微动效 | 150-300ms | 200ms | 悬停反馈、图标切换、颜色过渡 |
| 标准动效 | 300-500ms | 400ms | 元素入场、卡片展开、切换 |
| 大型动效 | 600-1000ms | 800ms | 页面转场、全屏动画、滚动叙事 |
| PPT 动效 | 500-1500ms | 800ms | 幻灯片切换、逐条展示、图表动画 |

---

## 七、强制规则

1. **DNA 优先**: 渲染管道启动后，第一步必须生成 `visual_dna`，后续所有渲染步骤从 `visual_dna` 读取参数。
2. **熔断可控偏离**: 在熔断机制允许的范围内（最大重试 3 次），允许对五维门禁未满分维度进行定向修复；已满分维度保持不动，避免"修一处坏一处"的回退风险。超过最大重试次数后质量保持为最高分方案，不再追求满分。
3. **全局统一**: 同一文档内所有页面、所有组件共享同一份 `visual_dna`，风格强制统一。
4. **DNA 版本锁定**: 渲染过程中 `visual_dna` 不可修改；如需调整，需终止当前渲染、重新生成 DNA、重新渲染。
5. **Taste-Skill 仲裁**: 当多个渲染模块对同一参数有冲突定义时，以 Taste-Skill 生成的 `visual_dna` 为准。

### 7.1 四道门禁

渲染输出在落地前必须依次通过以下 4 道门禁，前序失败不计入后续评分历史：

| 门禁序号 | 门禁名称 | 执行强度 | 判定标准 | 违规处理 | 规范文件 |
|---------|---------|---------|---------|---------|---------|
| Gate-1 | ASR 硬门 | 硬门（违反即拒） | 44 条禁令（8 类别：字体/配色/布局/动效/装饰/配图/排版/数据可视）全量检查 | 任一禁令触发即返回违规清单并拒绝输出，触发重试（计入熔断计数） | `asr-hard-gate.md` |
| Gate-2 | Golden Set 距离校验 | 距离门（距离 > 0.5 即拒） | 待校验输出与 48 个 Golden 样本（16 DLP × 3 样本）的多维距离度量（配色/排版/间距/语义），综合距离 ≤ 0.5 方为通过 | 距离 > 0.5 即拒绝，返回偏离维度与修复建议，触发重试 | `golden-set-validator.md` |
| Gate-3 | 五维门禁审查 | 满分门（任一维度未满分即打回） | 5 个维度（排版/审美/配图/语义一致性/品牌 DNA 一致性）独立评分，每维度 100 分，五维总分 500 分，均达 100 分方为通过 | 任一维度未达 100 分即打回，仅修复未满分维度，触发重试 | `taste-validator.md` |
| Gate-4 | 熔断机制 | 重试上限（超过即质量保持） | 最大重试次数 3 次，3 次内未达五维全满分即质量保持为历史最高分方案 | 超过 3 次质量保持为最高分方案，标注 `[FUSE-EXHAUST-RETRY]`，不再追求满分 | `fuse-mechanism.md` |

**门禁执行顺序**：ASR 硬门 → Golden Set 距离校验 → 五维门禁审查 → 熔断机制兜底。三者顺序不可调换，前序失败不计入五维评分历史。

**熔断质量保持安全网**：质量保持方案必须通过 ASR 硬门（因未通过 ASR 的方案不会进入得分历史），保证质量保持不会降到违反硬门的方案。

---

## 八、Taste-Skill 全局审美总控方法论

### 8.1 方法论原理

Taste-Skill 是渲染管道的审美决策中枢，负责在渲染启动时生成唯一的 `visual_dna` 对象，并在渲染全流程中充当最终仲裁者。其核心原理是"3参数控制+审美等级判定+DLP 检索"三层决策模型：

1. **3参数控制**：内容主题（content_theme）、产品类型（output_type）、目标受众（target_audience）三个输入参数唯一确定视觉DNA
2. **审美等级判定**：根据内容语义深度将审美需求分为3个等级，每个等级对应不同的视觉复杂度
3. **DLP 检索**：调用 DLP 检索器（`dlp-retriever.md`）从 16 个具象 DLP 中检索最匹配的 1 个主 DLP，将 DLP 的 12 字段规范适配为 `design_tokens` 对象，确保视觉输出与内容语义一致且可追溯

Taste-Skill 不是简单的参数映射器，而是具备审美判断力的决策引擎——它需要理解内容的情感基调、学术深度、受众预期，并据此做出超越模板化的审美决策。

### 8.2 3参数控制规则

| 参数 | 取值范围 | 影响范围 | 决策权重 |
|------|---------|---------|---------|
| `content_theme` | 任意文本描述 | 配色方案、字体风格、线条质感 | 40% |
| `output_type` | research_report / wechat_article / course_material | 栅格系统、动效强度、页面尺寸 | 35% |
| `target_audience` | academic / general / professional / youth | 字号阶梯、信息密度、视觉复杂度 | 25% |

**参数组合→DLP 族映射**：

配色方案不再使用预设色板，改由 DLP 检索器根据参数组合映射到 DLP 族，并在族内打分命中具体 DLP，由 DLP 的 `color_palette` 字段提供 6 色板具象值。

| content_theme | output_type | target_audience | 默认 DLP 族 | 族默认 DLP |
|--------------|-------------|-----------------|------------|-----------|
| 科技/数据/AI | research_report | academic | academic-journal | DLP-nature |
| 人文/社会/文化 | wechat_article | general | publication-typesetting | DLP-economist |
| 教育/培训/课程 | course_material | professional | interface-brand | DLP-linear |
| 商业/市场/金融 | research_report | professional | academic-journal | DLP-nature |
| 医疗/健康/生物 | research_report | academic | academic-journal | DLP-nature |
| 创意/设计/艺术 | wechat_article | youth | publication-typesetting | DLP-economist |

> 注：上表为质量保持策略的默认映射，正常检索时由 DLP 检索器根据语义信号 + 任务类型 + 族内打分动态命中，详见 `dlp-retriever.md`。

### 8.3 审美等级判定规则表

| 等级 | 判定条件 | 视觉复杂度 | 配色策略 | 动效策略 | 信息密度 |
|------|---------|-----------|---------|---------|---------|
| L1-极简 | 内容为数据摘要/指标面板/简报 | 低（2色） | 主色+背景色 | 无动效 | 高密度 |
| L2-标准 | 内容为研究报告/分析文章/课程材料 | 中（3-5色） | 五色板完整 | 微动效+标准动效 | 标准密度 |
| L3-沉浸 | 内容为叙事长文/品牌故事/深度专题 | 高（5色+渐变） | 五色板+渐变+纹理 | 标准+大型动效 | 低密度（留白多） |

**等级判定算法**：
```
IF output_type == "research_report" AND target_audience == "academic":
    level = L2-标准
ELIF output_type == "wechat_article" AND content_theme IN ["叙事", "故事", "品牌"]:
    level = L3-沉浸
ELIF word_count < 500 OR format == "dashboard":
    level = L1-极简
ELSE:
    level = L2-标准
```

### 8.4 DLP 检索器算法

Taste-Skill 不再维护抽象设计语言描述符，改为调用 DLP 检索器（`dlp-retriever.md`）从 16 个具象 DLP 中检索最匹配的 1 个主 DLP + 1 个备选 DLP，并将 DLP 的 12 字段规范适配为 `design_tokens` 对象供下游消费。设计语言由 16 个 DLP 提供，详见 `design-language-profiles/` 目录。

**检索流程**：

```
输入: UIR v2.0 文档（§1-§8 全息框架）+ 任务类型 + 用户偏好
  ↓
Step 1: 语义信号提取（从 §1-§8 提取内容主题/领域/受众）
  ↓
Step 2: 任务类型映射（4 种任务类型 → 4 族优先级）
  ↓
Step 3: 族内打分（目标族内 4 个 DLP 按场景标签匹配度打分）
  ↓
Step 4: 适配器输出（DLP 12 字段 → design_tokens 对象）
  ↓
输出: 主 DLP + 备选 DLP + design_tokens 对象 + 置信度
```

**四阶段决策范式**：

| 阶段 | 输入 | 输出 | 核心逻辑 |
|------|------|------|---------|
| 语义信号提取 | UIR v2.0 §1-§8 | semantic_signals（content_theme/domain/target_audience） | 从摘要层/背景层提取主题，从方法层/分析层提取领域，从讨论层/结论层推断受众 |
| 任务类型映射 | semantic_signals + 显式任务类型 | task_type_mapping（primary_family/secondary_family） | 4 种任务类型 → 4 族优先级：research_report→academic-journal, wechat_article→publication-typesetting, course_material→interface-brand, data_visualization→data-visualization |
| 族内打分 | target_family + semantic_signals | scored_dlps（按场景标签匹配度排序） | 完全匹配 +1.0，部分匹配 +0.5，不匹配 0；归一化得分 = Σ匹配分值/场景标签数 × 100% |
| 适配器输出 | primary_dlp（12 字段完整定义） | design_tokens 对象 | DLP 12 字段 → design_tokens 具象值，供 visual_dna 消费 |

**design_tokens 输出对象（含 DLP 的 12 字段具象值）**：

```yaml
design_tokens:
  # ---- 可追溯锚点 ----
  dlp_anchor: "DLP-nature"                          # 命中的 DLP 名称
  dlp_anchor_description: "Nature 正刊 2024 年版式"  # 锚定实体描述
  dlp_family: "academic-journal"                     # 族分类
  dlp_scenarios: ["学术论文", "期刊投稿", "科学研究"] # 场景标签

  # ---- 配色方案（6 色板，来自 DLP color_palette 字段）----
  color_palette:
    primary: "#000000"       # 主色
    secondary: "#E60012"     # 辅色
    accent: "#0066CC"        # 强调色
    neutral: "#6C757D"       # 中性色
    background: "#FFFFFF"    # 背景色
    text: "#1A1A1A"          # 文本色

  # ---- 字体方案（来自 DLP typography_scale/font_stack/font_weight_pairing 字段）----
  typography:
    scale: { h1, h2, h3, h4, body, caption, footnote }
    font_stack: { western, chinese, monospace }
    weight_pairing: { heading, body, emphasis }

  # ---- 间距系统（来自 DLP spacing_system 字段）----
  spacing: { base, scale }

  # ---- 栅格系统（来自 DLP grid_system 字段）----
  grid: { columns, gutter, margin, breakpoints }

  # ---- 圆角与阴影（来自 DLP radius_shadow 字段）----
  radius: { card, button, input }
  shadow: { light, medium }

  # ---- 动效（来自 DLP motion_curve 字段）----
  motion: { duration, easing }
```

**质量保持策略**：当检索置信度 < 0.6 时，回退到任务类型映射的默认族默认 DLP；语义信号提取失败时使用全局默认 DLP-nature。详见 `dlp-retriever.md` §七质量保持策略。

**匹配冲突解决**：当语义信号指向不同族时，按 `task_type > content_theme > target_audience` 优先级裁决族归属，族内打分仍按场景标签匹配度客观排序。

### 8.5 Taste-Skill 仲裁逻辑

当渲染管道中多个模块对同一 visual_dna 参数产生冲突定义时，Taste-Skill 执行以下仲裁流程：

1. **冲突检测**：收集所有渲染模块对 visual_dna 各字段的写入请求
2. **冲突分类**：
   - **硬冲突**：同一字段被多个模块写入不同值（如配色方案冲突）
   - **软冲突**：同一字段被多个模块写入兼容值（如间距微调）
3. **仲裁规则**：
   - 硬冲突：以 Taste-Skill 生成的原始 visual_dna 值为准，拒绝所有覆盖
   - 软冲突：取最接近 visual_dna 原始值的写入请求
4. **仲裁日志**：记录所有冲突及裁决结果，供调试审查

### 8.6 执行步骤

1. **接收3参数**：从渲染管道入口获取 content_theme、output_type、target_audience
2. **审美等级判定**：根据8.3规则表确定审美等级（L1/L2/L3）
3. **DLP 检索**：调用 DLP 检索器（`dlp-retriever.md`）进行语义信号提取 → 任务类型映射 → 族内打分 → 适配器输出 design_tokens
4. **配色方案注入**：从 design_tokens.color_palette 读取 6 色板具象值，注入 visual_dna.color_scheme
5. **字体方案注入**：从 design_tokens.typography 读取字号阶梯/字体栈/字重配对，注入 visual_dna.font_scheme
6. **栅格参数注入**：从 design_tokens.grid 读取列数/槽宽/页边距，注入 visual_dna.grid_system
7. **线条质感注入**：从 design_tokens.radius/shadow 读取圆角/阴影规范，注入 visual_dna.line_style
8. **动效配置注入**：从 design_tokens.motion 读取动效时长/缓动（印刷媒介为 N/A 时禁用动效），注入 visual_dna.motion_profile
9. **组装 visual_dna 对象**：将以上参数组装为完整的 visual_dna 对象
10. **签发 visual_dna_id**：生成唯一标识 `VDNA-{timestamp}-{hash8}`

### 8.7 决策规则

| 决策点 | 条件 | 动作 |
|--------|------|------|
| 参数缺失 | 3参数中任一未提供 | 使用默认值：content_theme="通用", output_type=research_report, target_audience=academic |
| DLP 检索置信度不足 | 检索置信度 < 0.6 | 回退到任务类型映射的默认族默认 DLP（详见 `dlp-retriever.md` §七质量保持策略） |
| 审美等级冲突 | 内容特征同时满足L1和L3条件 | 取较高等级（L3），确保视觉表现力 |
| 配色方案冲突 | 多个参数指向不同 DLP 族 | 按 output_type 对应的默认族为准，族内打分客观排序 |
| 渲染模块覆盖请求 | 下游模块请求修改 visual_dna | 拒绝，要求终止当前渲染并重新生成 |

### 8.8 输出规范

```yaml
taste_skill_output:
  visual_dna_id: "VDNA-{timestamp}-{hash8}"
  aesthetic_level: "L1-极简|L2-标准|L3-沉浸"
  dlp_anchor: "DLP-nature"                    # 命中的主 DLP 名称
  dlp_family: "academic-journal"              # 命中的 DLP 族
  design_tokens: object                       # DLP 12 字段适配后的具象值（见 §8.4）
  control_params:
    content_theme: "string"
    output_type: "string"
    target_audience: "string"
  arbitration_log:
    - conflict_type: "hard|soft"
      field: "string"
      requester: "string"
      resolution: "string"
  retry_logic: "FULL|PARTIAL|RETRYING|FUSE-EXHAUST-RETRY"
```

> 知识来源: LC-026 Taste-Skill

---

## 九、LC 卡片 visual_dna 对接规则

> 每张 LC 渲染卡片必须从 `visual_dna` 读取参数，不得硬编码视觉值。以下定义各卡片与 visual_dna 的对接映射。
>
> **DLP 对接说明**：`visual_dna` 的所有视觉参数（配色/字体/栅格/线条/动效）均由 DLP 检索器（`dlp-retriever.md`）命中的 DLP 适配为 `design_tokens` 对象后注入（详见 §8.4）。LC 卡片消费的 `visual_dna` 字段可追溯到 DLP 锚定实体的 12 字段规范，设计语言由 16 个 DLP 提供，详见 `design-language-profiles/` 目录。LC 卡片不再对接抽象设计语言描述符，而是对接 DLP 具象锚点。
>
> **对接链路**：DLP 12 字段 → `design_tokens`（`dlp-retriever.md` §六适配器）→ `visual_dna`（本文件 §8.6 执行步骤）→ LC 卡片消费（本节 §9.1-§9.11）

### 9.1 LC-018 ECharts 对接规则

**消费 visual_dna 字段**（源自 DLP `design_tokens`，可追溯至 DLP 锚定实体）：`color_scheme`（五色板→ECharts color 数组）、`font_scheme`（字体族→textStyle.fontFamily）、`line_style`（数据线粗细→series.lineStyle.width）、`motion_profile`（动效时长→animationDuration）

**对接映射**：

| visual_dna 字段 | ECharts 配置项 | 映射规则 |
|----------------|---------------|---------|
| `--color-primary` | `color[0]` | 主色作为系列1颜色 |
| `--color-secondary` | `color[1]` | 辅色作为系列2颜色 |
| `--color-accent` | `color[2]` | 强调色作为系列3颜色 |
| `--color-bg` | `backgroundColor` | 背景色直接映射 |
| `--color-border` | `splitLine.lineStyle.color` | 分割线颜色 |
| `--color-text` | `textStyle.color` | 全局文字颜色 |
| H1字号 32px | `title.textStyle.fontSize` | 标题字号映射 |
| 数据线 2px | `series.lineStyle.width` | 折线粗细 |
| 标准动效 400ms | `animationDuration` | 入场动画时长 |

**决策规则**：ECharts 图表类型由 semantic-auto-detect 的数据段检测决定，ECharts 仅负责渲染，不参与图表类型选择。

> 知识来源: LC-018 ECharts

### 9.2 LC-019 Plotly 对接规则

**消费 visual_dna 字段**（源自 DLP `design_tokens`，可追溯至 DLP 锚定实体）：`color_scheme`（→layout.colorway）、`font_scheme`（→layout.font.family）、`grid_system`（→layout.margin/width/height）、`line_style`（→trace.line.width）

**对接映射**：

| visual_dna 字段 | Plotly 配置项 | 映射规则 |
|----------------|-------------|---------|
| `--color-primary/secondary/accent` | `layout.colorway` | 三色映射为 colorway 数组 |
| `--color-bg` | `layout.paper_bgcolor` | 画布背景色 |
| `--color-bg-alt` | `layout.plot_bgcolor` | 绘图区背景色 |
| `--color-text` | `layout.font.color` | 全局字体颜色 |
| `--color-text-secondary` | `layout.xaxis.tickfont.color` | 轴刻度颜色 |
| 标题字体 | `layout.title.font.family` | 标题字体族 |
| 正文字体 | `layout.font.family` | 全局字体族 |
| 数据线 2px | `trace.line.width` | 折线/曲线粗细 |
| 标准动效 400ms | `layout.transition.duration` | 过渡动画时长 |

**决策规则**：3D图表、统计图表（箱线图/小提琴图/热力图）优先使用 Plotly 而非 ECharts；科研数据可视化场景优先 Plotly。

> 知识来源: LC-019 Plotly

### 9.3 LC-020 Observable-Plot 对接规则

**消费 visual_dna 字段**（源自 DLP `design_tokens`，可追溯至 DLP 锚定实体）：`color_scheme`（→plot.color 颜色比例尺）、`font_scheme`（→plot.style 字体）、`line_style`（→mark 线宽）

**对接映射**：

| visual_dna 字段 | Observable Plot 配置项 | 映射规则 |
|----------------|---------------------|---------|
| `--color-primary/secondary/accent` | `color` 通道 | 声明式颜色比例尺映射 |
| `--color-bg` | SVG 容器背景 | 通过 CSS 设置 |
| `--color-text` | `plot.style.color` | 全局文字颜色 |
| 标题字号 | `title.fontSize` | 标题字号 |
| 数据线 2px | `strokeWidth` | 线宽 |

**决策规则**：轻量级数据探索场景优先使用 Observable Plot（声明式API更简洁）；需要复杂交互或3D时切换至 Plotly/ECharts。

> 知识来源: LC-020 Observable-Plot

### 9.4 LC-021 Mermaid 对接规则

**消费 visual_dna 字段**（源自 DLP `design_tokens`，可追溯至 DLP 锚定实体）：`color_scheme`（→themeVariables.primaryColor/secondaryColor等）、`font_scheme`（→themeVariables.fontFamily）、`line_style`（→edge 线条样式）

**对接映射**：

| visual_dna 字段 | Mermaid 配置项 | 映射规则 |
|----------------|--------------|---------|
| `--color-primary` | `themeVariables.primaryColor` | 节点主色 |
| `--color-secondary` | `themeVariables.secondaryColor` | 节点辅色 |
| `--color-accent` | `themeVariables.tertiaryColor` | 第三色/决策节点 |
| `--color-bg` | `themeVariables.mainBkg` | 节点背景 |
| `--color-text` | `themeVariables.primaryTextColor` | 节点文字色 |
| `--color-border` | `themeVariables.lineColor` | 连线颜色 |
| 标题字体 | `themeVariables.fontFamily` | 全局字体 |
| 流程图连线 1.5px | `themeVariables.lineWidth` | 连线粗细 |

**决策规则**：流程图/时序图/甘特图/类图/状态图/ER图统一使用 Mermaid；思维导图使用 Markmap（LC-023）。

> 知识来源: LC-021 Mermaid

### 9.5 LC-023 Markmap 对接规则

**消费 visual_dna 字段**（源自 DLP `design_tokens`，可追溯至 DLP 锚定实体）：`color_scheme`（→markmap colorFreezeLevel 颜色映射）、`font_scheme`（→CSS font-family 注入）

**对接映射**：

| visual_dna 字段 | Markmap 配置项 | 映射规则 |
|----------------|--------------|---------|
| `--color-primary` | 根节点颜色 | 中心主题节点色 |
| `--color-secondary` | 一级分支色 | 第一层分支颜色 |
| `--color-accent` | 二级分支色 | 第二层分支颜色 |
| `--color-text` | 全局文字色 | SVG text fill |
| 标题字体 | CSS font-family 注入 | 节点字体 |
| 标准动效 400ms | `duration` | 节点展开/折叠动画时长 |

**决策规则**：概念段检测中"分类列表"和"层级关键词"触发的思维导图使用 Markmap；流程图使用 Mermaid。

> 知识来源: LC-023 Markmap

### 9.6 LC-027 GSAP 对接规则

**消费 visual_dna 字段**（源自 DLP `design_tokens`，可追溯至 DLP 锚定实体）：`motion_profile`（→GSAP tween 时长和缓动）、`color_scheme`（→GSAP 颜色动画目标值）

**对接映射**：

| visual_dna 字段 | GSAP 配置项 | 映射规则 |
|----------------|-----------|---------|
| 入场缓动 ease-out | `gsap.ease` = "power2.out" | 对应 cubic-bezier(0.25,0.1,0.25,1.0) |
| 循环缓动 ease-in-out | `gsap.ease` = "power2.inOut" | 对应 cubic-bezier(0.42,0,0.58,1.0) |
| 出场缓动 ease-in | `gsap.ease` = "power2.in" | 对应 cubic-bezier(0.42,0,1.0,1.0) |
| 微动效 200ms | `duration: 0.2` | 悬停反馈等 |
| 标准动效 400ms | `duration: 0.4` | 元素入场等 |
| 大型动效 800ms | `duration: 0.8` | 页面转场等 |
| `--color-primary` | 颜色动画目标 | gsap.to({color: primary}) |

**决策规则**：需要精确时间线控制（Timeline）、多元素编排、滚动驱动动画时使用 GSAP；简单CSS动画使用 vibe-motion 预调校包。

> 知识来源: LC-027 GSAP

### 9.7 LC-028 vibe-motion 对接规则

**消费 visual_dna 字段**（源自 DLP `design_tokens`，可追溯至 DLP 锚定实体）：`motion_profile`（→预调校动效包参数）、`color_scheme`（→动效颜色参数）

**对接映射**：

| visual_dna 字段 | vibe-motion 配置项 | 映射规则 |
|----------------|------------------|---------|
| 入场缓动 | 预设包 easing 选择 | 匹配最接近的预调校缓动 |
| 标准动效 400ms | 预设包 duration | 直接映射 |
| `--color-primary` | 动效颜色参数 | 高亮/强调动效颜色 |

**决策规则**：标准入场/出场/悬停动效优先使用 vibe-motion 预调校包（开箱即用）；需要自定义时间线编排时切换至 GSAP。

> 知识来源: LC-028 vibe-motion

### 9.8 LC-030 data-viz-plots 对接规则

**消费 visual_dna 字段**（源自 DLP `design_tokens`，可追溯至 DLP 锚定实体）：`color_scheme`（→Nature/Cell级图表配色）、`font_scheme`（→学术字体）、`line_style`（→图表线条规范）

**对接映射**：

| visual_dna 字段 | data-viz-plots 配置项 | 映射规则 |
|----------------|---------------------|---------|
| `--color-primary/secondary/accent` | 图表系列颜色 | 学术级配色映射 |
| `--color-text` | 轴标签/图例文字色 | 全局文字色 |
| `--color-text-secondary` | 刻度标签/注释色 | 辅助文字色 |
| 正文字体 | 轴标签字体 | 学术字体族 |
| 数据线 2px | 数据线粗细 | 折线/曲线 |
| 图表轴线 1.5px | 坐标轴线粗细 | X/Y轴 |

**决策规则**：学术论文配图（Nature/Cell级别）优先使用 data-viz-plots；交互式数据探索使用 ECharts/Plotly。

> 知识来源: LC-030 data-viz-plots

### 9.9 LC-033 PaperBanana 对接规则

**消费 visual_dna 字段**（源自 DLP `design_tokens`，可追溯至 DLP 锚定实体）：`color_scheme`（→学术插图配色）、`font_scheme`（→插图标注字体）、`line_style`（→插图线条风格）

**对接映射**：

| visual_dna 字段 | PaperBanana 配置项 | 映射规则 |
|----------------|------------------|---------|
| `--color-primary` | 插图主色调 | 关键元素着色 |
| `--color-secondary` | 插图辅色调 | 辅助元素着色 |
| `--color-text` | 标注文字色 | 图注/标签 |
| `--color-border` | 插图边框/连线色 | 连接线/边框 |
| 正文字体 | 标注字体 | 图内文字 |
| 流程图连线 1.5px | 连线粗细 | 示意图连线 |

**决策规则**：顶刊级学术插图（机制图/信号通路/系统架构图）使用 PaperBanana；手绘风格示意图使用 excalidraw。

> 知识来源: LC-033 PaperBanana

### 9.10 LC-035 excalidraw 对接规则

**消费 visual_dna 字段**（源自 DLP `design_tokens`，可追溯至 DLP 锚定实体）：`color_scheme`（→手绘风格配色）、`line_style`（→手绘线条参数）

**对接映射**：

| visual_dna 字段 | excalidraw 配置项 | 映射规则 |
|----------------|-----------------|---------|
| `--color-primary` | 元素主色 | 手绘元素描边/填充 |
| `--color-secondary` | 元素辅色 | 辅助元素 |
| `--color-text` | 文字色 | 手绘文字 |
| `--color-border` | 连线色 | 手绘箭头/连线 |
| 手绘风格线 1.5px | strokeWidth | 手绘线条粗细 |
| round 端点 | strokeSharpness: "round" | 手绘圆角端点 |

**决策规则**：概念示意图/白板风格/非正式说明图使用 excalidraw；正式学术插图使用 PaperBanana。

> 知识来源: LC-035 excalidraw

### 9.11 LC-036 SketchAgent 对接规则

**消费 visual_dna 字段**（源自 DLP `design_tokens`，可追溯至 DLP 锚定实体）：`color_scheme`（→逐笔动画颜色）、`line_style`（→笔画粗细和端点）、`motion_profile`（→逐笔绘制速度）

**对接映射**：

| visual_dna 字段 | SketchAgent 配置项 | 映射规则 |
|----------------|-------------------|---------|
| `--color-primary` | 笔画主色 | 主要笔画颜色 |
| `--color-secondary` | 笔画辅色 | 辅助笔画颜色 |
| `--color-border` | 连线色 | 连接笔画 |
| 手绘风格线 1.5px | stroke width | 笔画粗细 |
| round 端点 | stroke cap: round | 笔画端点 |
| 标准动效 400ms/项 | 绘制速度 | 每笔画绘制时长 |

**决策规则**：需要逐笔绘制动画效果（如教学演示/过程展示）使用 SketchAgent；静态手绘示意图使用 excalidraw。

> 知识来源: LC-036 SketchAgent

---

## 十、LC 卡片卡级设计决策补全

> 以下为 11 张部分内化 LC 卡的卡级设计决策补全，涵盖方法论原理、执行步骤、决策规则、输出规范四要素。

### 10.1 LC-018 ECharts 卡级设计决策

**方法论原理**：ECharts 是渲染管道中覆盖面最广的交互式图表引擎，采用配置驱动-声明式渲染范式。其核心设计原理是"数据→配置→渲染"的单向数据流：将数据数组映射为 ECharts option 对象，option 中的 series/type 决定图表类型，option 中的 style 属性从 visual_dna 读取，ECharts 引擎负责从 option 到 Canvas/SVG 的渲染。ECharts 的优势在于开箱即用的 30+ 图表类型、丰富的交互组件（tooltip/dataZoom/legend）和双渲染引擎（Canvas 大数据量/SVG 高清输出）。

**执行步骤**：
1. 图表类型确定：由 semantic-auto-detect 的数据段检测决定图表类型
2. 数据预处理：将原始数据转换为 ECharts 数据格式（dataset 或 series.data）
3. option 构建：构建 ECharts option 对象，series/type 由步骤1决定
4. visual_dna 注入：从 visual_dna 读取配色/字体/线宽/动效参数，注入 option
5. 交互配置：添加 tooltip/legend/dataZoom 等交互组件
6. 渲染引擎选择：数据量 > 10000 → Canvas；需要高清导出 → SVG
7. 初始化渲染：调用 echarts.init() + setOption() 渲染图表

**决策规则**：

| 条件 | 决策 |
|------|------|
| 标准图表类型（折线/柱状/饼/散点/雷达/热力） | 使用 ECharts |
| 3D 图表 | 切换至 Plotly |
| 力导向图/桑基图/旭日图 | 切换至 D3.js |
| 数据量 > 10000 | 使用 Canvas 渲染 |
| 需要高清 SVG 导出 | 使用 SVG 渲染 |
| 需要学术出版级静态图 | 切换至 data-viz-plots |

**输出规范**：
```yaml
echarts_output:
  chart_type: str
  rendering_engine: "canvas|svg"
  option: object
  visual_dna_compliance: "FULL|PARTIAL"
  interaction_components: [str]
  data_points: int
```

> 知识来源: LC-018 ECharts

---

### 10.2 LC-019 Plotly 卡级设计决策

**方法论原理**：Plotly 是渲染管道中面向科研数据的交互式可视化引擎，采用 Figure 对象-Trace 布局范式。其核心设计原理是"数据→Trace→Figure"的分层架构：Trace 定义数据映射（x/y/z/颜色/大小），Layout 定义视觉样式（配色/字体/轴/注释），Figure = Trace + Layout。Plotly 的优势在于 3D 可视化（3D 散点/曲面/网格）、统计图表（箱线图/小提琴图/直方图/热力图）和 Python/JS 双语言支持。

**执行步骤**：
1. 图表类型确定：3D/统计图表优先 Plotly
2. Trace 构建：根据图表类型创建对应的 Trace 对象（go.Scatter/go.Bar/go.Box 等）
3. Layout 构建：配置轴标签/标题/图例/注释
4. visual_dna 注入：从 visual_dna 读取配色/字体/线宽，注入 Layout
5. 交互配置：添加 hoverinfo/clickmode/dragmode 交互
6. Figure 组装：Figure = Trace[] + Layout
7. 渲染输出：fig.show() 或 fig.to_html()/fig.to_image()

**决策规则**：

| 条件 | 决策 |
|------|------|
| 3D 图表（散点/曲面/网格） | 使用 Plotly |
| 统计图表（箱线图/小提琴图/直方图） | 使用 Plotly |
| 科研数据可视化 | 使用 Plotly |
| 标准折线/柱状/饼图 | 使用 ECharts（更轻量） |
| 力导向图/桑基图 | 使用 D3.js |
| 需要学术出版级静态图 | 使用 data-viz-plots |

**输出规范**：
```yaml
plotly_output:
  chart_type: str
  trace_types: [str]
  layout_config: object
  visual_dna_compliance: "FULL|PARTIAL"
  export_format: "html|png|svg|pdf"
  3d_enabled: bool
```

> 知识来源: LC-019 Plotly

---

### 10.3 LC-021 Mermaid 卡级设计决策

**方法论原理**：Mermaid 是渲染管道中覆盖面最广的结构化图引擎，采用文本定义-自动布局范式。其核心设计原理是"文本即图"：用简洁的文本语法描述图结构（节点+边+关系），Mermaid 引擎自动计算布局和渲染。Mermaid 支持 8 种图表类型（flowchart/sequence/class/state/ER/gantt/pie/mindmap），覆盖了大部分结构化可视化需求。其优势在于文本可维护性（版本控制友好）和自动布局（无需手动调整位置）。

**执行步骤**：
1. 图表类型确定：根据内容语义选择 Mermaid 图表类型
2. 文本定义编写：使用 Mermaid 语法编写图定义文本
3. visual_dna 注入：从 visual_dna 读取配色/字体/线宽，注入 Mermaid 主题变量
4. 主题配置：设置 themeVariables 对象
5. 渲染输出：调用 mermaid.render() 生成 SVG

**决策规则**：

| 内容语义 | 图表类型 |
|---------|---------|
| 流程/决策/算法 | flowchart |
| 交互/通信/协议 | sequence |
| 类/继承/接口 | class |
| 状态/转换/生命周期 | state |
| 实体/关系/数据库 | er |
| 时间线/里程碑 | gantt |
| 比例/占比 | pie |
| 分类/层级 | mindmap（或 Markmap） |

**输出规范**：
```yaml
mermaid_output:
  diagram_type: str
  definition_text: str
  theme: str
  visual_dna_compliance: "FULL|PARTIAL"
  node_count: int
  edge_count: int
```

> 知识来源: LC-021 Mermaid

---

### 10.4 LC-023 Markmap 卡级设计决策

**方法论原理**：Markmap 是渲染管道中专门用于思维导图的渲染引擎，采用 Markdown 标题层级-树形映射范式。其核心设计原理是"Markdown 即思维导图"：将 Markdown 的标题层级（#/##/###）自动映射为思维导图的树形结构，标题文本映射为节点文本，标题层级映射为树的深度。Markmap 的优势在于从已有 Markdown 内容零成本生成思维导图，无需额外编辑。

**执行步骤**：
1. Markdown 输入：接收 Markdown 格式的内容
2. 层级解析：解析 Markdown 标题层级（#/##/###/####）
3. 树形构建：将标题层级映射为树形结构
4. visual_dna 注入：从 visual_dna 读取配色/字体/动效，注入 Markmap 配置
5. 布局计算：计算节点位置和分支角度
6. SVG 渲染：生成思维导图 SVG
7. 交互绑定：添加节点展开/折叠交互

**决策规则**：

| 条件 | 决策 |
|------|------|
| 内容为分类列表/层级关键词 | 使用 Markmap |
| 内容为流程/决策 | 使用 Mermaid flowchart |
| 内容为实体关系 | 使用 Mermaid ER |
| 已有 Markdown 内容需快速可视化 | 使用 Markmap |
| 需要精细控制节点样式 | 使用 D3.js 自定义 |

**输出规范**：
```yaml
markmap_output:
  source_markdown: str
  node_count: int
  max_depth: int
  visual_dna_compliance: "FULL|PARTIAL"
  interactive: bool
```

> 知识来源: LC-023 Markmap

---

### 10.5 LC-026 Taste-Skill 卡级设计决策

**方法论原理**：Taste-Skill 是渲染管道的全局审美总控，采用3参数-审美等级-DLP 检索三层决策范式。其核心设计原理是"内容决定形式"：通过 content_theme（内容主题）、output_type（输出类型）、target_audience（目标受众）三个参数，自动判定审美等级（L1极简/L2标准/L3沉浸），并调用 DLP 检索器（`dlp-retriever.md`）从 16 个具象 DLP 中检索最匹配的 1 个主 DLP，将 DLP 的 12 字段规范适配为 `design_tokens` 对象，最终生成 visual_dna 参数集供所有下游 LC 卡片消费。设计语言由 16 个 DLP 提供，详见 `design-language-profiles/` 目录。Taste-Skill 不直接渲染任何视觉元素，而是通过 visual_dna 间接控制所有渲染输出。

**执行步骤**：
1. 参数采集：从任务上下文提取 content_theme/output_type/target_audience
2. 审美等级判定：根据3参数组合判定 L1/L2/L3
3. DLP 检索：调用 DLP 检索器进行语义信号提取 → 任务类型映射 → 族内打分 → 适配器输出 design_tokens
4. visual_dna 生成：根据审美等级 + design_tokens 生成完整 visual_dna 参数集
5. 冲突仲裁：处理硬冲突（报错）和软冲突（加权投票）
6. 参数下发：将 visual_dna 下发给所有下游 LC 卡片

**决策规则**：

| 参数组合 | 审美等级 | 默认 DLP 族 | 族默认 DLP |
|---------|---------|------------|-----------|
| 学术论文+论文+学者 | L1极简 | academic-journal | DLP-nature |
| 人文叙事+文章+公众 | L2标准 | publication-typesetting | DLP-economist |
| 科技报告+演示+专家 | L3沉浸 | academic-journal | DLP-nature |
| 教育内容+课件+学生 | L2标准 | interface-brand | DLP-linear |

> 注：上表为质量保持策略的默认映射，正常检索时由 DLP 检索器动态命中，详见 `dlp-retriever.md`。

**输出规范**：
```yaml
taste_skill_output:
  parameters: {content_theme: str, output_type: str, target_audience: str}
  aesthetic_level: "L1|L2|L3"
  dlp_anchor: str           # 命中的主 DLP 名称
  dlp_family: str           # 命中的 DLP 族
  design_tokens: object     # DLP 12 字段适配后的具象值
  visual_dna: object
  confidence: "FULL|PARTIAL|RETRYING|FUSE-EXHAUST-RETRY"
```

> 知识来源: LC-026 Taste-Skill

---

### 10.6 LC-027 GSAP 卡级设计决策

**方法论原理**：GSAP 是渲染管道中最高精度的动效引擎，采用 Timeline-多元素编排-滚动驱动范式。其核心设计原理是"时间线即动画"：通过 gsap.timeline() 创建时间线对象，将多个 tween（补间动画）按时间轴编排，实现多元素的精确时序控制。GSAP 的优势在于亚像素级精度（60fps）、滚动驱动动画（ScrollTrigger）、和跨浏览器一致性。

**执行步骤**：
1. 动效需求分析：确定动效类型（入场/出场/悬停/滚动/循环）
2. Timeline 创建：gsap.timeline() 创建时间线
3. Tween 编排：将多个 gsap.to()/from()/fromTo() 按时序添加到时间线
4. visual_dna 注入：从 visual_dna 读取动效时长/缓动/颜色参数
5. ScrollTrigger 配置（如需滚动驱动）：设置触发位置/起始/结束
6. 性能优化：使用 will-change/gpu 加速，避免布局抖动
7. 渲染执行：启动时间线播放

**决策规则**：

| 条件 | 决策 |
|------|------|
| 需要多元素时序编排 | 使用 GSAP Timeline |
| 需要滚动驱动动画 | 使用 GSAP ScrollTrigger |
| 需要亚像素精度动效 | 使用 GSAP |
| 简单入场/悬停动效 | 使用 vibe-motion 预调校包 |
| 仅需 CSS 过渡 | 使用 CSS Animation |

**输出规范**：
```yaml
gsap_output:
  timeline_count: int
  tween_count: int
  scroll_trigger: bool
  visual_dna_compliance: "FULL|PARTIAL"
  fps_target: int
  easing_functions: [str]
```

> 知识来源: LC-027 GSAP

---

### 10.7 LC-028 vibe-motion 卡级设计决策

**方法论原理**：vibe-motion 是渲染管道中的预调校动效包，采用预设-直接调用范式。其核心设计原理是"开箱即用的动效"：将常用的动效模式（入场/出场/悬停/强调）封装为预调校的动效包，开发者无需理解缓动函数/时长/延迟等底层参数，直接调用预设名称即可。vibe-motion 的优势在于零配置、一致性和可预测性——所有动效都经过审美调校，确保视觉体验的一致性。

**执行步骤**：
1. 动效模式选择：从预设包中选择动效模式（fadeIn/fadeOut/slideIn/scaleUp/highlight 等）
2. visual_dna 注入：从 visual_dna 读取动效时长/缓动，匹配最接近的预调校包
3. 目标元素选择：指定动效作用的目标 DOM 元素
4. 动效触发配置：配置触发条件（页面加载/滚动进入/悬停/点击）
5. 执行动效：调用预调校包执行动效

**决策规则**：

| 条件 | 决策 |
|------|------|
| 标准入场/出场/悬停动效 | 使用 vibe-motion 预调校包 |
| 需要自定义时间线编排 | 切换至 GSAP |
| 需要滚动驱动动画 | 切换至 GSAP ScrollTrigger |
| 需要大量 CSS 动画 | 使用 Animotion MCP |

**输出规范**：
```yaml
vibe_motion_output:
  preset_name: str
  target_elements: [str]
  trigger: "load|scroll|hover|click"
  visual_dna_compliance: "FULL|PARTIAL"
```

> 知识来源: LC-028 vibe-motion

---

### 10.8 LC-030 data-viz-plots 卡级设计决策

**方法论原理**：data-viz-plots 是渲染管道中面向学术出版的静态图表引擎，采用 Nature/Cell 级规范-精确控制范式。其核心设计原理是"学术出版级图表"：图表的每个视觉元素（轴线粗细/刻度间距/字体大小/配色方案/图例位置）都严格遵循 Nature/Cell 等顶刊的图表规范，确保输出图表无需后处理即可直接用于论文投稿。

**执行步骤**：
1. 图表规范选择：根据目标期刊选择图表规范（Nature/Cell/Science/IEEE）
2. 数据预处理：将数据转换为图表所需的格式
3. 图表类型确定：根据数据特征和期刊规范确定图表类型
4. visual_dna 注入：从 visual_dna 读取学术配色/字体/线宽
5. 精确绘制：按期刊规范精确控制每个视觉元素
6. 分辨率输出：生成 300+ DPI 的高分辨率图表
7. 格式导出：导出为 TIFF/EPS/PDF/SVG 格式

**决策规则**：

| 条件 | 决策 |
|------|------|
| 学术论文配图（Nature/Cell 级别） | 使用 data-viz-plots |
| 交互式数据探索 | 使用 ECharts/Plotly |
| Web 展示 | 使用 ECharts |
| 需要出版级分辨率 | 使用 data-viz-plots |
| 简单快速图表 | 使用 Matplotlib |

**输出规范**：
```yaml
data_viz_plots_output:
  journal_standard: str
  chart_type: str
  dpi: int
  format: "tiff|eps|pdf|svg"
  visual_dna_compliance: "FULL|PARTIAL"
  colorblind_safe: bool
```

> 知识来源: LC-030 data-viz-plots

---

### 10.9 LC-033 PaperBanana 卡级设计决策

**方法论原理**：PaperBanana 是渲染管道中面向顶刊学术插图的生成引擎，采用语义描述-AI生成-学术规范范式。其核心设计原理是"文字即插图"：通过自然语言描述插图内容（如"Wnt信号通路示意图"、"系统架构图"），PaperBanana 自动生成符合学术规范的顶刊级插图。与 ECharts/Plotly 的数据驱动图表不同，PaperBanana 生成的是概念性插图（机制图/信号通路/架构图），而非数据图表。

**执行步骤**：
1. 插图需求分析：确定插图类型（机制图/信号通路/架构图/流程示意图）
2. 语义描述编写：用自然语言描述插图内容和元素关系
3. visual_dna 注入：从 visual_dna 读取学术配色/字体/线宽
4. AI 生成：PaperBanana 根据语义描述生成插图
5. 学术规范校验：检查插图是否符合学术出版规范
6. 格式导出：导出为 SVG/PNG 格式

**决策规则**：

| 条件 | 决策 |
|------|------|
| 顶刊级学术插图（机制图/信号通路） | 使用 PaperBanana |
| 手绘风格示意图 | 使用 excalidraw |
| 数据图表 | 使用 ECharts/Plotly/data-viz-plots |
| UML 标准图 | 使用 PlantUML |
| 流程图 | 使用 Mermaid |

**输出规范**：
```yaml
paperbanana_output:
  illustration_type: str
  semantic_description: str
  format: "svg|png"
  dpi: int
  visual_dna_compliance: "FULL|PARTIAL"
  academic_standard: bool
```

> 知识来源: LC-033 PaperBanana

---

### 10.10 LC-035 excalidraw 卡级设计决策

**方法论原理**：excalidraw 是渲染管道中的手绘风格示意图引擎，采用手绘渲染-白板风格范式。其核心设计原理是"手绘即沟通"：通过模拟手绘线条的不规则性（抖动/粗细变化/圆角端点），创造非正式、亲和力强的视觉风格，适合概念解释、白板讨论和快速原型。excalidraw 与 PaperBanana 的区别在于风格定位——excalidraw 是"白板讨论级"，PaperBanana 是"顶刊出版级"。

**执行步骤**：
1. 示意图需求分析：确定示意图类型（概念图/流程草图/架构白板）
2. 元素规划：规划矩形/椭圆/箭头/文字等元素
3. visual_dna 注入：从 visual_dna 读取手绘配色/线宽/端点样式
4. 手绘参数配置：设置抖动幅度/粗细变化/圆角端点
5. 元素绘制：绘制手绘风格的元素和连线
6. 文字标注：添加手绘风格的文字标注
7. 导出输出：导出为 SVG/PNG 格式

**决策规则**：

| 条件 | 决策 |
|------|------|
| 概念示意图/白板风格/非正式说明 | 使用 excalidraw |
| 正式学术插图 | 使用 PaperBanana |
| 流程图/时序图 | 使用 Mermaid |
| 需要逐笔绘制动画 | 使用 SketchAgent |
| UML 标准图 | 使用 PlantUML |

**输出规范**：
```yaml
excalidraw_output:
  sketch_type: str
  element_count: int
  hand_drawn_style: bool
  visual_dna_compliance: "FULL|PARTIAL"
  format: "svg|png|excalidraw"
```

> 知识来源: LC-035 excalidraw

---

### 10.11 LC-036 SketchAgent 卡级设计决策

**方法论原理**：SketchAgent 是渲染管道中的逐笔绘制动画引擎，采用笔画序列-时序动画范式。其核心设计原理是"过程即内容"：不仅展示最终的示意图结果，更展示绘制过程本身——每一笔的绘制顺序、速度和节奏都传递信息。SketchAgent 与 excalidraw 的区别在于动态性——excalidraw 输出静态手绘图，SketchAgent 输出逐笔绘制动画。这种"过程可视化"特别适合教学演示和概念解释场景。

**执行步骤**：
1. 绘制需求分析：确定绘制内容和笔画序列
2. 笔画路径规划：规划每个笔画的路径（起点→终点/曲线控制点）
3. visual_dna 注入：从 visual_dna 读取笔画颜色/粗细/端点/绘制速度
4. 时序编排：编排笔画的绘制顺序和时间间隔
5. 动画生成：生成逐笔绘制的 SVG/Canvas 动画
6. 交互配置：添加播放/暂停/重放控制
7. 导出输出：导出为 SVG 动画/GIF/视频格式

**决策规则**：

| 条件 | 决策 |
|------|------|
| 需要逐笔绘制动画（教学/过程展示） | 使用 SketchAgent |
| 静态手绘示意图 | 使用 excalidraw |
| 正式学术插图 | 使用 PaperBanana |
| 流程图 | 使用 Mermaid |
| 需要复杂动效编排 | 使用 GSAP |

**输出规范**：
```yaml
sketchagent_output:
  stroke_count: int
  total_duration_ms: int
  visual_dna_compliance: "FULL|PARTIAL"
  format: "svg_animation|gif|video"
  playback_controls: bool
```

> 知识来源: LC-036 SketchAgent
