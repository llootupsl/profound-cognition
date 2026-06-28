<!-- 作者：阿洋 -->

# taste-skill 核心算法消费文件

> **文件**: `rendering-pipeline/taste-skill-consumer.md`
> **来源项目**: [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill)
> **能力卡编号**: LC-026（已存在，本次为深度内化补充）
> **消费节点**: T20a/T20b/T20c/T27, rendering-pipeline/visual-dna.md
> **内化日期**: 2026-06-14

---

## 一、方法论原理

taste-skill 是 AI Agent 的"设计品位外挂"，其核心认知假设是——**LLM 在生成前端代码时存在系统性审美偏差（AI Slop），表现为：居中英雄区、紫色渐变、Inter字体、三列卡片、圆角阴影等"平均化"模式。这些模式源于训练数据的统计平均，而非有意识的设计决策**。

taste-skill 的破局思路不是提供模板或组件库，而是注入**约束原则**——让 AI 自己推断出适合当前项目的设计语言。其核心机制是"三旋钮控制 + 反Slop规则 + 设计语言推断"三层防御体系：

1. **三旋钮（Three Dials）**：DESIGN_VARIANCE / MOTION_INTENSITY / VISUAL_DENSITY 三个连续参数，控制全局设计方向
2. **反Slop规则（Anti-Slop Rules）**：显式禁止 LLM 最常犯的审美错误，详见 `asr-hard-gate.md`（硬门执行，违反即拒）
3. **设计语言推断（Brief Inference）**：从用户需求中提取6维信号，推断设计方向，在写代码之前先输出"Design Read"

---

## 二、执行步骤

### 步骤1：Brief Inference（需求推断）

```
输入: 用户需求描述
输出: 6维信号 + Design Read 声明

6维信号提取:
  1. page_kind: 页面类型（landing/dashboard/editor/docs/portfolio/blog）
  2. vibe_words: 情绪词（premium/minimal/brutalist/soft/editorial/tech）
  3. reference_signals: 参考信号（品牌/产品/网站引用）
  4. audience: 受众（consumer/enterprise/developer/creative/student）
  5. brand_assets: 品牌资产（logo/配色/字体/图标）
  6. quiet_constraints: 隐性约束（无障碍/性能/SEO/国际化）

Design Read 声明（强制输出）:
  格式: "Design Read: {page_kind} for {audience}, {vibe_words} vibe, {design_system} foundation"
  示例: "Design Read: Landing for enterprise, premium vibe, Fluent UI foundation"

  目的: 强制 AI 在生成任何代码之前先提交设计方向，
       防止默认到通用模式（default-to-generic behavior）
```

### 步骤2：三旋钮配置（Three Dials Configuration）

```
三个连续参数，范围1-10:

  DESIGN_VARIANCE (设计方差):
    1-3: 完美对称，保守布局，网格对齐
    4-7: 偏移不对称，有节奏的变化
    8-10: 艺术性混乱，实验性布局

  MOTION_INTENSITY (动效强度):
    1-3: 静态克制，仅CSS过渡
    4-7: 流畅CSS动画，Framer Motion基础
    8-10: 电影级编排，弹簧物理，视差滚动

  VISUAL_DENSITY (视觉密度):
    1-3: 艺术画廊/空灵，大量留白
    4-7: 日常应用/均衡，标准信息密度
    8-10: 驾驶舱/密集，信息密集型

默认基线: DESIGN_VARIANCE=8, MOTION_INTENSITY=6, VISUAL_DENSITY=4

旋钮推断表（根据Brief信号自动配置）:
  | Brief类型              | DV | MI | VD |
  |------------------------|----|----|-----|
  | 极简编辑类网站          | 3  | 2  | 2  |
  | 信任优先公共服务        | 2  | 1  | 5  |
  | 高端消费品牌            | 9  | 7  | 3  |
  | SaaS仪表盘             | 4  | 4  | 7  |
  | 创意作品集              | 10 | 8  | 3  |
  | 技术文档                | 2  | 1  | 6  |
  | 新闻编辑               | 5  | 3  | 6  |
```

### 步骤3：设计系统映射（Design System Map）

```
根据Brief信号选择设计系统基础:

  | Brief信号                    | 设计系统               |
  |-----------------------------|----------------------|
  | Microsoft企业产品            | Fluent UI            |
  | UK公共服务                   | GOV.UK Frontend      |
  | Google产品                   | Material Design 3    |
  | Apple生态                    | Apple HIG            |
  | 审美方向（非正式系统）        | 原生CSS + Tailwind    |

诚实规则（Honesty Rule）:
  - 如果真实的设计系统包存在，必须使用真实包
  - 禁止手写CSS模仿设计系统
  - 借鉴灵感 vs 官方材料必须明确标注
```

### 步骤4：反Slop规则执行（Anti-Slop Rules）

Anti-Slop 规则详见 asr-hard-gate.md，执行强度为硬门：违反即拒。
ASR 硬门包含 8 个类别 44 条禁令：字体禁令、配色禁令、布局禁令、动效禁令、装饰禁令、配图禁令、排版禁令、数据可视禁令。

### 步骤5：Hero区设计（Hero Section Design）

```
Hero区是第一印象，必须创意性、醒目、非通用:

  签名创意技术——内联图片排版（Inline Image Typography）:
    在标题文字之间嵌入小型上下文图片，图片位于文字行内高度，
    圆角处理，充当视觉标点符号

  强制规则:
    - 文字不得与图片或其他文字重叠
    - 每个元素占据自己干净的空间区域
    - 禁止填充文本和滚动提示
    - DESIGN_VARIANCE > 4 时禁止居中布局
    - 最多1个主CTA，无次要"Learn more"链接
```

### 步骤6：组件样式定义（Component Stylings）

```
按钮:
  - 按下状态有触觉反馈（tactile push feedback）
  - 无霓虹外发光
  - 无自定义鼠标光标

卡片:
  - 仅当elevation传达层级时使用
  - 阴影着色到背景色调
  - 高密度布局用border-top分割线或负空间替代

输入框/表单:
  - 标签始终可见（不用浮动标签）
  - 聚焦状态用ring而非border变化
  - 错误状态用语义色标记

数据展示:
  - 表格用水平线分割，不用全边框
  - 数字右对齐，使用tabular-nums
  - 空状态有明确引导，非空白
```

### 步骤7：动效哲学（Motion Philosophy）

```
动效引擎选择:
  - 简单CSS过渡: CSS transition/animation
  - 声明式动画: Framer Motion
  - 高精度时间线: GSAP + ScrollTrigger
  - 弹簧物理: Framer Motion spring()

动效规则:
  - 仅动画 transform 和 opacity（GPU加速）
  - 禁止 width/height/layout 动画
  - 微交互: 150-300ms
  - 标准入场: 300-500ms
  - 大型转场: 600-1000ms
  - 永久微交互（呼吸/脉冲）: 2-4秒周期

MOTION_INTENSITY映射:
  | MI  | 动效策略                                   |
  |-----|-------------------------------------------|
  | 1-3 | CSS过渡，无JS动画，hover/focus微反馈        |
  | 4-7 | Framer Motion入场/出场，视差滚动            |
  | 8-10| GSAP时间线编排，弹簧物理，电影级编排         |
```

### 步骤8：Taste-Skill 仲裁逻辑

```
当多个渲染模块对同一视觉参数产生冲突时:

1. 冲突检测: 收集所有模块对visual_dna各字段的写入请求

2. 冲突分类:
   - 硬冲突: 同一字段被多个模块写入不同值（如配色方案冲突）
   - 软冲突: 同一字段被多个模块写入兼容值（如间距微调）

3. 仲裁规则:
   - 硬冲突: 以Taste-Skill生成的原始visual_dna值为准，拒绝所有覆盖
   - 软冲突: 取最接近visual_dna原始值的写入请求

4. 仲裁日志: 记录所有冲突及裁决结果

5. 三旋钮优先级: output_type > content_theme > target_audience
```

---

## 三、决策规则

### 3.1 技能选择决策

| 场景 | 选择技能 | 说明 |
|------|---------|------|
| 新项目默认 | taste-skill v2 | 主力技能，推断设计语言，调节三旋钮 |
| GPT/Codex环境 | gpt-tasteskill | 严格变体，强化GSAP动效 |
| 图片→代码 | image-to-code-skill | 图片分析→风格提取→代码生成 |
| 改造现有UI | redesign-skill | 6类诊断→完整改造方案 |
| 品牌体系搭建 | brandkit skill | Logo+配色+字体+品牌规范 |
| 极简风格 | minimalist-skill | Notion/Linear编辑风格 |
| 粗野主义 | brutalist-skill | 瑞士排版+CRT终端美学 |
| Google Stitch | stitch-skill | DESIGN.md兼容 |

### 3.2 配色决策

| 条件 | 决策 |
|------|------|
| 需要Premium感 | 禁止Inter，使用Geist/Outfit/Cabinet Grotesk/Satoshi |
| 需要Editorial感 | 仅允许Fraunces/Gambarino/Editorial New/Instrument Serif |
| Dashboard/软件UI | 完全禁止衬线字体，使用Geist+Geist Mono或Satoshi+JetBrains Mono |
| VD > 7 | 所有数字必须等宽 |
| 需要强调色 | 最多1个，饱和度<80% |
| 需要暗色主题 | 使用Off-Black(Zinc-950)，禁止纯黑 |

### 3.3 布局决策

| 条件 | 决策 |
|------|------|
| DV > 4 | 禁止居中英雄区，使用分屏/不对称布局 |
| DV ≤ 3 | 允许居中布局，但需有独特元素 |
| VD ≤ 3 | 大量留白，艺术画廊感 |
| VD > 7 | 信息密集，驾驶舱感，用分割线替代卡片 |
| 需要全高区域 | 使用min-h-[100dvh]，禁止h-screen |

### 3.4 动效决策

| 条件 | 决策 |
|------|------|
| MI ≤ 3 | 仅CSS过渡，hover/focus微反馈 |
| MI 4-7 | Framer Motion入场/出场动画 |
| MI ≥ 8 | GSAP时间线编排+弹簧物理 |
| 任何MI值 | 仅动画transform+opacity |
| 需要滚动驱动 | GSAP ScrollTrigger |
| 需要预调校包 | vibe-motion直接调用 |

---

## 四、输出规范

```yaml
taste_skill_consumer_output:
  design_read:
    page_kind: "landing|dashboard|editor|docs|portfolio|blog"
    vibe_words: [str]
    reference_signals: [str]
    audience: "consumer|enterprise|developer|creative|student"
    brand_assets: {logo: str|null, colors: [str]|null, fonts: [str]|null}
    quiet_constraints: [str]

  three_dials:
    DESIGN_VARIANCE: int  # 1-10
    MOTION_INTENSITY: int  # 1-10
    VISUAL_DENSITY: int    # 1-10

  design_system:
    name: "fluent_ui|gov_uk|material_3|apple_hig|native_css_tailwind"
    is_official: bool
    honesty_note: str|null

  anti_slop_compliance:
    fonts_banned: [str]        # 被禁止的字体列表
    fonts_used: [str]          # 实际使用的字体列表
    colors_banned: [str]       # 被禁止的配色列表
    layout_rules_applied: [str]
    content_rules_applied: [str]

  visual_dna:
    color_scheme:
      primary: str
      secondary: str
      accent: str
      background: str
      text: str
    font_scheme:
      heading: str
      body: str
      code: str
    motion_profile:
      micro_duration_ms: int
      standard_duration_ms: int
      large_duration_ms: int
      easing_standard: str
      easing_spring: str|null

  arbitration_log:
    - conflict_type: "hard|soft"
      field: str
      requester: str
      resolution: str
```

---

## 五、与 profound-cognition 渲染管道集成

### 5.1 与现有 visual-dna.md 的关系

本消费文件是 `rendering-pipeline/visual-dna.md` §八"Taste-Skill 全局审美总控方法论"的深度内化补充：
- visual-dna.md §八 定义了3参数控制规则（content_theme/output_type/target_audience）
- 本消费文件补充了 taste-skill 原项目的**三旋钮系统**（DESIGN_VARIANCE/MOTION_INTENSITY/VISUAL_DENSITY）
- Anti-Slop 规则（反Slop规则）已移出至 `asr-hard-gate.md`，作为硬门独立执行（8 类别 44 条禁令）
- 本消费文件补充了**Brief Inference**的6维信号提取流程

### 5.2 参数映射

| taste-skill 原项目参数 | profound-cognition visual-dna 参数 | 映射关系 |
|----------------------|----------------------------------|---------|
| DESIGN_VARIANCE | 审美等级 L1/L2/L3 | DV 1-3→L1, DV 4-7→L2, DV 8-10→L3 |
| MOTION_INTENSITY | motion_profile 动效时长 | MI 1-3→微动效200ms, MI 4-7→标准400ms, MI 8-10→大型800ms |
| VISUAL_DENSITY | 栅格系统间距 | VD 1-3→3xl间距, VD 4-7→lg间距, VD 8-10→sm间距 |
| vibe_words | content_theme | 直接映射 |
| audience | target_audience | 直接映射 |
| page_kind | output_type | 需转换映射 |

### 5.3 穷尽重试策略

| 穷尽重试路径 | 触发条件 | 行为 |
|-------------|---------|------|
| taste-skill v2 → v1 | v2规则导致渲染异常 | 穷尽重试替代到v1可预测行为 |
| taste-skill → minimalist-skill | 审美推断失败 | 使用极简风格兜底 |
| 三旋钮推断 → 默认基线 | Brief信号不足 | 使用DV=8/MI=6/VD=4默认值 |
| ASR 硬门 → 宽松模式 | 规则过于严格导致无法生成 | 详见 asr-hard-gate.md 的质量保持策略，保留核心禁令 |

---

## taste-skill soft/minimalist 分支

当 DESIGN_VARIANCE (DV) ≤ 4 时，启用柔和留白模式：
- 间距 ×1.5（所有间距值乘以 1.5）
- 圆角 ×1.2（所有圆角值乘以 1.2）
- 阴影减弱 50%（阴影透明度减半）
- 动效减弱 30%（动效持续时间缩短 30%）

此分支融入 taste-skill 的 soft/minimalist 风格，主打柔和留白与产品级极简，避开通用款的同质化问题，间距、动效、排版舒适度极高。

---

## DLP 对接规则

三旋钮值（DV/MI/VD）作为 DLP 适配器的微调参数（DLP 检索器实现详见 `dlp-retriever.md`，DLP 库索引详见 `design-language-profiles/README.md`）：

### DV（DESIGN_VARIANCE）与 DLP 配色
- DV=8 时：允许 DLP 配色的 ±10% 色相偏移
- DV=6 时：允许 DLP 配色的 ±5% 色相偏移
- DV=4 时：不允许色相偏移（严格遵循 DLP 配色）
- DV=2 时：不允许色相偏移 + 启用 soft/minimalist 分支

### MI（MOTION_INTENSITY）与 DLP 动效
- MI=8 时：允许 DLP 动效曲线的 ±20% 持续时间调整
- MI=6 时：严格遵循 DLP 动效曲线
- MI=4 时：动效持续时间 ×0.7
- MI=2 时：动效持续时间 ×0.5

### VD（VISUAL_DENSITY）与 DLP 间距
- VD=8 时：允许 DLP 间距的 -20% 压缩
- VD=6 时：严格遵循 DLP 间距
- VD=4 时：DLP 间距 ×1.2
- VD=2 时：DLP 间距 ×1.5

> 知识来源: LC-026 Taste-Skill (Leonxlnx/taste-skill)
