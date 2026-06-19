<!-- 作者：阿洋 -->

# 布局原子库 (Layout Atoms)

> **定位**: 渲染管道的空间布局原子化能力库，为所有渲染模块提供可复用的栅格/卡片/页面/响应式/特殊布局原子。
> **强制规则**: 所有渲染模块的布局结构必须从本原子库选取原子，不得自行声明布局数值；所有间距值必须是 4px 的整数倍（4px 基准系统）。
> **layout-grid.md 对接**: 每个原子通过 4px 基准系统与 `layout-grid.md` 的 12 列栅格系统对接，栅格列宽、槽宽、边距均从 `--grid-gutter` / `--page-margin-*` 变量派生。
> **融入来源**: guizang-social-card-skill — 竖版图文卡片排版能力，对标杂志视觉逻辑，摒弃通用模板的同质化廉价感。

---

## 方法论原理

布局原子库基于"原子化设计"理论：将空间布局系统分解为最小不可分割的原子单元（栅格/卡片/页面/响应式/特殊），每个原子封装 HTML+CSS 与 Typst 双轨实现，确保跨引擎布局一致性。原子库融入了 guizang-social-card-skill 的竖版图文卡片排版能力——以 375px iPhone 标准宽度为基准，对标杂志视觉逻辑，建立视觉重心、留白节奏、字体层级三位一体的杂志级排版，摒弃通用模板"图片+文字"简单堆叠的同质化廉价感。

### 4px 基准系统对接规则

所有布局原子的间距值（margin/padding/gap/width/height）必须是 4px 的整数倍，与 `layout-grid.md` 第七章强制规则第 3 条对齐。对接逻辑：

- **栅格槽宽**：从 `--grid-gutter`（默认 16px = 4×4px）派生
- **页面边距**：从 `--page-margin-*` 变量派生，所有值对齐 4px
- **卡片内边距**：从 `--padding-card`（默认 24px = 6×4px）派生
- **段间距**：从 `--spacing-para`（默认 16px = 4×4px）派生

### 融入 guizang-social-card-skill 核心理念

> **来源技能**: guizang-social-card-skill
> **融入点**: LA-CARD-002 竖版卡片（375px 宽，图片 16:9 比例，标题/正文/标签三级层级）
> **杂志视觉逻辑**: 卡片不是简单的"图片+文字"堆叠，而是有视觉重心（图片占视觉权重 60%）、留白节奏（图片下沿 16px 呼吸空间）、字体层级（标题 20px semibold / 正文 14px regular / 标签 12px medium）的杂志级排版。

---

## 一、栅格布局原子（LA-GRID）

> **融入来源**: layout-grid.md 12 列栅格系统 + guizang-social-card-skill 竖版卡片栅格
> **对接规则**: 每个栅格原子通过 `--grid-columns` / `--grid-gutter` 变量与 layout-grid.md 对接，所有槽宽和边距对齐 4px 基准。

### LA-GRID-001: 12 列栅格

- **原子 ID**: LA-GRID-001
- **适用场景**: 标准 Web 布局、桌面端页面、复杂多栏内容排版，支持 2/3/4/6 整除灵活性
- **HTML+CSS 实现**:
  ```html
  <div class="la-grid-12">
    <div class="la-col la-col-12">12/12 全宽</div>
    <div class="la-col la-col-8">8/12 主内容</div>
    <div class="la-col la-col-4">4/12 侧边栏</div>
    <div class="la-col la-col-6">6/12 半宽</div>
    <div class="la-col la-col-6">6/12 半宽</div>
  </div>
  ```
  ```css
  .la-grid-12 {
    display: grid;
    grid-template-columns: repeat(12, 1fr);
    column-gap: 24px;   /* 6×4px，槽宽 */
    row-gap: 24px;      /* 6×4px，行间距 */
    padding: 32px;      /* 8×4px，页面边距 */
    box-sizing: border-box;
  }
  .la-col { box-sizing: border-box; }
  .la-col-12 { grid-column: span 12; }
  .la-col-8  { grid-column: span 8; }
  .la-col-6  { grid-column: span 6; }
  .la-col-4  { grid-column: span 4; }
  .la-col-3  { grid-column: span 3; }
  .la-col-2  { grid-column: span 2; }

  /* 响应式：窄屏折叠为单列 */
  @media (max-width: 767px) {
    .la-grid-12 { grid-template-columns: 1fr; padding: 16px; }
    .la-col-12, .la-col-8, .la-col-6, .la-col-4, .la-col-3, .la-col-2 {
      grid-column: span 1;
    }
  }
  ```
- **Typst 实现**:
  ```typst
  #let la-grid-12(
    columns: 12,
    gutter: 24pt,
    margin: 32pt,
    body
  ) = {
    set page(margin: (left: margin, right: margin, top: margin, bottom: margin))
    // 12 列栅格通过 grid 函数实现
    grid(
      columns: (1fr,) * columns,
      column-gutter: gutter,
      row-gutter: gutter,
      ..body
    )
  }

  // 列占用辅助函数
  #let la-col(span, body) = gridcell(colspan: span, body)

  // 使用示例
  #la-grid-12(
    columns: 12,
    gutter: 24pt,
    margin: 32pt
  )[
    #gridcell(colspan: 12)[12/12 全宽]
    #gridcell(colspan: 8)[8/12 主内容]
    #gridcell(colspan: 4)[4/12 侧边栏]
  ]
  ```
- **与 layout-grid.md 对接规则**: 直接映射 layout-grid.md 第一章 12 列栅格系统。`column-gap: 24px` 对应 layout-grid.md 的 `--grid-gutter` 变量（本原子采用 24px 而非默认 16px，用于 Web 布局的更宽松呼吸感，仍为 4px 整数倍）。`padding: 32px` 对应 `--page-margin-*` 变量。列占用规则完全遵循 layout-grid.md 第 1.2 节列占用表。

---

### LA-GRID-002: 6 列栅格

- **原子 ID**: LA-GRID-002
- **适用场景**: 紧凑布局、仪表盘面板、移动端横屏、信息密度较高的数据展示
- **HTML+CSS 实现**:
  ```html
  <div class="la-grid-6">
    <div class="la-col-6">6/6 全宽</div>
    <div class="la-col-3">3/6 半宽</div>
    <div class="la-col-3">3/6 半宽</div>
    <div class="la-col-2">2/6 三分之一</div>
    <div class="la-col-2">2/6 三分之一</div>
    <div class="la-col-2">2/6 三分之一</div>
  </div>
  ```
  ```css
  .la-grid-6 {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    column-gap: 16px;   /* 4×4px，紧凑槽宽 */
    row-gap: 16px;      /* 4×4px */
    padding: 24px;      /* 6×4px，紧凑边距 */
    box-sizing: border-box;
  }
  .la-col-6 { grid-column: span 6; }
  .la-col-3 { grid-column: span 3; }
  .la-col-2 { grid-column: span 2; }

  @media (max-width: 639px) {
    .la-grid-6 { grid-template-columns: 1fr; padding: 16px; }
    .la-col-6, .la-col-3, .la-col-2 { grid-column: span 1; }
  }
  ```
- **Typst 实现**:
  ```typst
  #let la-grid-6(
    gutter: 16pt,
    margin: 24pt,
    body
  ) = {
    set page(margin: (left: margin, right: margin, top: margin, bottom: margin))
    grid(
      columns: (1fr,) * 6,
      column-gutter: gutter,
      row-gutter: gutter,
      ..body
    )
  }

  // 使用示例
  #la-grid-6(gutter: 16pt, margin: 24pt)[
    #gridcell(colspan: 6)[6/6 全宽]
    #gridcell(colspan: 3)[3/6 半宽]
    #gridcell(colspan: 3)[3/6 半宽]
  ]
  ```
- **与 layout-grid.md 对接规则**: 作为 layout-grid.md 12 列栅格的简化变体，6 列栅格是 12 列的子集（每 2 列合并为 1 列）。`column-gap: 16px` 严格对齐 layout-grid.md 默认 `--grid-gutter: 16px`。`padding: 24px` 对应 layout-grid.md 第 2.1 节手机竖屏边距。适用于 layout-grid.md 第 4.1 节中需要紧凑排版的场景。

---

### LA-GRID-003: 黄金分割栅格

- **原子 ID**: LA-GRID-003
- **适用场景**: 主内容 + 侧边栏布局、编辑型页面、博客文章页、品牌叙事页
- **HTML+CSS 实现**:
  ```html
  <div class="la-grid-golden">
    <main class="la-golden-main">
      主内容区（61.8%）
    </main>
    <aside class="la-golden-aside">
      侧边栏（38.2%）
    </aside>
  </div>
  ```
  ```css
  .la-grid-golden {
    display: grid;
    grid-template-columns: 61.8fr 38.2fr;
    column-gap: 32px;   /* 8×4px，宽松槽宽 */
    padding: 32px;      /* 8×4px */
    box-sizing: border-box;
  }
  .la-golden-main,
  .la-golden-aside {
    box-sizing: border-box;
    min-width: 0;       /* 防止内容溢出栅格 */
  }

  @media (max-width: 1023px) {
    .la-grid-golden {
      grid-template-columns: 1fr;
      column-gap: 0;
      row-gap: 24px;    /* 6×4px */
    }
  }
  ```
- **Typst 实现**:
  ```typst
  #let la-grid-golden(
    gutter: 32pt,
    margin: 32pt,
    main-body,
    aside-body
  ) = {
    set page(margin: (left: margin, right: margin, top: margin, bottom: margin))
    grid(
      columns: (61.8fr, 38.2fr),
      column-gutter: gutter,
      row-gutter: gutter,
      main-body,
      aside-body
    )
  }

  // 使用示例
  #la-grid-golden(
    gutter: 32pt,
    margin: 32pt,
    main-body: [主内容区（61.8%）],
    aside-body: [侧边栏（38.2%）]
  )
  ```
- **与 layout-grid.md 对接规则**: 对应 layout-grid.md 第 4.2 节"主内容 + 侧边栏"模式（8/12 + 4/12 ≈ 66.7% + 33.3%）的审美优化变体，将比例调整为黄金分割 61.8%/38.2%。`column-gap: 32px`（8×4px）比 layout-grid.md 默认槽宽更宽松，用于编辑型内容的呼吸感。窄屏折叠规则遵循 layout-grid.md 第 5.2 节断点切换规则。

---

### LA-GRID-004: 杂志双栏

- **原子 ID**: LA-GRID-004
- **适用场景**: 杂志风格长文排版、A4 打印文档双栏、学术报告正文、编辑型内容
- **HTML+CSS 实现**:
  ```html
  <div class="la-grid-magazine-2">
    <div class="la-mag-col">
      左栏内容
    </div>
    <div class="la-mag-col">
      右栏内容
    </div>
  </div>
  ```
  ```css
  .la-grid-magazine-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    column-gap: 24px;   /* 6×4px */
    padding: 40px;      /* 10×4px，杂志宽边距 */
    box-sizing: border-box;
  }
  .la-mag-col {
    box-sizing: border-box;
    min-width: 0;
  }

  @media (max-width: 767px) {
    .la-grid-magazine-2 {
      grid-template-columns: 1fr;
      column-gap: 0;
      row-gap: 24px;
      padding: 24px;
    }
  }
  ```
- **Typst 实现**:
  ```typst
  #let la-grid-magazine-2(
    gutter: 24pt,
    margin: 40pt,
    body
  ) = {
    set page(margin: (left: margin, right: margin, top: margin, bottom: margin))
    // 杂志双栏通过 columns 函数实现
    set columns(2, gutter: gutter)
    body
  }

  // 使用示例
  #la-grid-magazine-2(gutter: 24pt, margin: 40pt)[
    左栏内容

    #colbreak()

    右栏内容
  ]
  ```
- **与 layout-grid.md 对接规则**: 对应 layout-grid.md 第 4.1 节 Word/PDF (A4) 双栏模式（6/12 + 6/12）。`padding: 40px`（10×4px）比 layout-grid.md A4 边距（25mm ≈ 94px）更紧凑，适用于数字杂志而非打印。Typst 实现使用原生 `columns` 函数，`gutter: 24pt` 对齐 layout-grid.md `--grid-gutter` 变量。

---

### LA-GRID-005: 杂志三栏

- **原子 ID**: LA-GRID-005
- **适用场景**: 杂志三栏排版、新闻门户、特性对比页、三步流程展示
- **HTML+CSS 实现**:
  ```html
  <div class="la-grid-magazine-3">
    <div class="la-mag3-col">第一栏</div>
    <div class="la-mag3-col">第二栏</div>
    <div class="la-mag3-col">第三栏</div>
  </div>
  ```
  ```css
  .la-grid-magazine-3 {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    column-gap: 20px;   /* 5×4px */
    padding: 32px;      /* 8×4px */
    box-sizing: border-box;
  }
  .la-mag3-col {
    box-sizing: border-box;
    min-width: 0;
  }

  @media (max-width: 1023px) {
    .la-grid-magazine-3 {
      grid-template-columns: 1fr 1fr;
    }
  }
  @media (max-width: 639px) {
    .la-grid-magazine-3 {
      grid-template-columns: 1fr;
      column-gap: 0;
      row-gap: 20px;
      padding: 20px;
    }
  }
  ```
- **Typst 实现**:
  ```typst
  #let la-grid-magazine-3(
    gutter: 20pt,
    margin: 32pt,
    body
  ) = {
    set page(margin: (left: margin, right: margin, top: margin, bottom: margin))
    grid(
      columns: (1fr,) * 3,
      column-gutter: gutter,
      row-gutter: gutter,
      ..body
    )
  }

  // 使用示例
  #la-grid-magazine-3(gutter: 20pt, margin: 32pt)[
    #gridcell[第一栏]
    #gridcell[第二栏]
    #gridcell[第三栏]
  ]
  ```
- **与 layout-grid.md 对接规则**: 对应 layout-grid.md 第 4.2 节"三栏卡片"模式（4/12 × 3 ≈ 33.3% × 3）。`column-gap: 20px`（5×4px）介于 layout-grid.md 默认槽宽 16px 与 LA-GRID-001 的 24px 之间，三栏布局需要更紧凑的槽宽以避免单栏过窄。响应式断点遵循 layout-grid.md 第 5.1 节 md/lg 断点定义。

---

### LA-GRID-006: 竖版卡片栅格

- **原子 ID**: LA-GRID-006
- **适用场景**: 社交媒体卡片、移动端 H5 长图、微信公众号图文、iPhone 标准宽度内容
- **融入来源**: guizang-social-card-skill — 375px iPhone 标准宽度栅格，专为竖版图文卡片设计
- **HTML+CSS 实现**:
  ```html
  <div class="la-grid-card-vertical">
    <article class="la-card-vertical-item">
      <!-- 卡片内容 -->
    </article>
  </div>
  ```
  ```css
  .la-grid-card-vertical {
    width: 375px;       /* iPhone 标准宽度 */
    margin: 0 auto;
    padding: 16px;      /* 4×4px，移动端边距 */
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    gap: 16px;          /* 4×4px，卡片间距 */
  }
  .la-card-vertical-item {
    box-sizing: border-box;
    width: 100%;
  }

  /* 响应式：小于 375px 时全宽自适应 */
  @media (max-width: 374px) {
    .la-grid-card-vertical {
      width: 100%;
      padding: 12px;    /* 3×4px */
    }
  }
  ```
- **Typst 实现**:
  ```typst
  #let la-grid-card-vertical(
    width: 375pt,
    margin: 16pt,
    gap: 16pt,
    body
  ) = {
    set page(
      width: width,
      margin: (left: margin, right: margin, top: margin, bottom: margin)
    )
    // 竖版卡片栅格通过 stack 垂直排列
    stack(
      spacing: gap,
      ..body
    )
  }

  // 使用示例
  #la-grid-card-vertical(width: 375pt, margin: 16pt, gap: 16pt)[
    #rect(width: 100%, height: auto, inset: 16pt)[卡片内容 1]
    #rect(width: 100%, height: auto, inset: 16pt)[卡片内容 2]
  ]
  ```
- **与 layout-grid.md 对接规则**: 对应 layout-grid.md 第 3.1 节"手机竖屏 375px"尺寸和第 2.1 节手机竖屏边距（左右 16px = 4×4px）。此栅格是 layout-grid.md 12 列栅格在移动端的单栏特化（12/12 全宽），遵循 layout-grid.md 第 4.1 节手机竖屏 1 栏全宽策略。`gap: 16px` 对齐 `--spacing-para` 变量。

---

## 二、卡片布局原子（LA-CARD）

> **融入来源**: guizang-social-card-skill — 竖版图文卡片排版能力，杂志视觉逻辑
> **对接规则**: 每个卡片原子通过 `--padding-card` 变量与 layout-grid.md 对接，卡片内边距默认 24px（6×4px）。

### LA-CARD-001: 横版卡片

- **原子 ID**: LA-CARD-001
- **适用场景**: 列表页内容卡片、博客文章列表、产品展示卡片、搜索结果项
- **HTML+CSS 实现**:
  ```html
  <article class="la-card-horizontal">
    <div class="la-card-h-image">
      <img src="cover.jpg" alt="封面图" />
    </div>
    <div class="la-card-h-content">
      <h3 class="la-card-h-title">卡片标题</h3>
      <p class="la-card-h-desc">卡片描述文字，简要概述内容要点。</p>
      <div class="la-card-h-meta">
        <span class="la-card-h-tag">标签</span>
        <time class="la-card-h-time">2026-06-19</time>
      </div>
    </div>
  </article>
  ```
  ```css
  .la-card-horizontal {
    display: flex;
    height: 200px;          /* 固定高度 */
    background: #ffffff;
    border-radius: 8px;     /* 2×4px */
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  }
  .la-card-h-image {
    flex: 0 0 40%;           /* 图片占 40% */
    overflow: hidden;
  }
  .la-card-h-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  .la-card-h-content {
    flex: 1;
    padding: 24px;           /* 6×4px */
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-sizing: border-box;
  }
  .la-card-h-title {
    font-size: 20px;         /* 5×4px */
    font-weight: 600;
    line-height: 1.3;
    margin: 0 0 8px 0;       /* 2×4px */
  }
  .la-card-h-desc {
    font-size: 14px;
    line-height: 1.6;
    color: #555555;
    margin: 0;
    flex: 1;
  }
  .la-card-h-meta {
    display: flex;
    align-items: center;
    gap: 12px;               /* 3×4px */
    margin-top: 12px;        /* 3×4px */
  }
  .la-card-h-tag {
    font-size: 12px;         /* 3×4px */
    padding: 4px 8px;        /* 1×4px, 2×4px */
    background: #f0f0f0;
    border-radius: 4px;      /* 1×4px */
  }
  .la-card-h-time {
    font-size: 12px;
    color: #999999;
  }
  ```
- **Typst 实现**:
  ```typst
  #let la-card-horizontal(
    image-src,
    title,
    desc,
    tag: "",
    time: "",
  ) = {
    block(
      width: 100%,
      height: 200pt,
      clip: true,
    )[
      #grid(
        columns: (40%, 1fr),
        column-gutter: 0pt,
        // 图片列
        rect(width: 100%, height: 100%, fill: image(image-src, width: 100%, height: 100%)),
        // 内容列
        pad(x: 24pt, y: 24pt)[
          #text(size: 20pt, weight: "semibold")[#title]
          #v(8pt)
          #text(size: 14pt, fill: rgb("#555555"))[#desc]
          #v(1fr)
          #grid(
            columns: (auto, auto),
            column-gutter: 12pt,
            text(size: 12pt)[#tag],
            text(size: 12pt, fill: rgb("#999999"))[#time],
          )
        ]
      )
    ]
  }
  ```
- **与 layout-grid.md 对接规则**: 卡片内边距 `padding: 24px` 对齐 layout-grid.md `--padding-card` 变量（6×4px）。`height: 200px`（50×4px）为固定高度，对应 layout-grid.md 卡片内边距规范。图片占 40% 对应 layout-grid.md 第 4.2 节"图文混排（左图右文）"5/12 + 7/12 模式的简化变体。所有间距值（8px/12px/24px）均为 4px 整数倍。

---

### LA-CARD-002: 竖版卡片

- **原子 ID**: LA-CARD-002
- **适用场景**: 社交媒体卡片、移动端内容流、微信公众号图文卡片、信息流广告
- **融入来源**: guizang-social-card-skill — 核心融入点，375px iPhone 标准宽度，杂志级图文排版
- **命名澄清**: guizang-social-card-skill 是 guizang 系列技能的社交卡片分支，与 guizang-ppt-skill（LC-029，PPT 生成分支）是同一作者的不同技能。guizang-social-card-skill 无独立 LC 卡片编号，作为设计语言来源内化到 LA-CARD-002，不应强行关联到 LC-029（guizang-ppt-skill）。
- **杂志视觉逻辑**: 视觉重心（图片 16:9 占视觉权重 60%）+ 留白节奏（图片下沿 16px 呼吸空间）+ 字体层级（标题 20px semibold / 正文 14px regular / 标签 12px medium）
- **HTML+CSS 实现**:
  ```html
  <article class="la-card-vertical">
    <div class="la-card-v-image">
      <img src="cover.jpg" alt="封面图" />
    </div>
    <div class="la-card-v-content">
      <h3 class="la-card-v-title">杂志级排版标题</h3>
      <p class="la-card-v-body">
        正文内容，以杂志视觉逻辑组织信息层级，
        摒弃通用模板的同质化廉价感。
      </p>
      <div class="la-card-v-tags">
        <span class="la-card-v-tag">设计</span>
        <span class="la-card-v-tag">排版</span>
      </div>
      <div class="la-card-v-footer">
        <span class="la-card-v-author">作者名</span>
        <time class="la-card-v-time">2026-06-19</time>
      </div>
    </div>
  </article>
  ```
  ```css
  .la-card-vertical {
    width: 375px;            /* iPhone 标准宽度 */
    background: #ffffff;
    border-radius: 8px;      /* 2×4px */
    overflow: hidden;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
    box-sizing: border-box;
  }
  .la-card-v-image {
    width: 100%;
    height: 210px;           /* 16:9 比例：375 × 9/16 ≈ 211px，取 210px 对齐 4px */
    overflow: hidden;
  }
  .la-card-v-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  .la-card-v-content {
    padding: 16px;           /* 4×4px，紧凑内边距 */
    box-sizing: border-box;
  }
  .la-card-v-title {
    font-size: 20px;         /* 5×4px，semibold 层级 */
    font-weight: 600;
    line-height: 1.3;
    margin: 0 0 8px 0;       /* 2×4px */
    color: #1a1a1a;
  }
  .la-card-v-body {
    font-size: 14px;         /* regular 层级 */
    line-height: 1.6;
    color: #444444;
    margin: 0 0 12px 0;      /* 3×4px */
  }
  .la-card-v-tags {
    display: flex;
    gap: 8px;                /* 2×4px */
    margin-bottom: 12px;     /* 3×4px */
  }
  .la-card-v-tag {
    font-size: 12px;         /* 3×4px，medium 层级 */
    font-weight: 500;
    padding: 4px 8px;        /* 1×4px, 2×4px */
    background: #f5f5f5;
    border-radius: 4px;      /* 1×4px */
    color: #666666;
  }
  .la-card-v-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 12px;       /* 3×4px */
    border-top: 1px solid #eeeeee;
  }
  .la-card-v-author {
    font-size: 12px;
    color: #999999;
  }
  .la-card-v-time {
    font-size: 12px;
    color: #999999;
  }
  ```
- **Typst 实现**:
  ```typst
  #let la-card-vertical(
    image-src,
    title,
    body,
    tags: (),
    author: "",
    time: "",
  ) = {
    block(
      width: 375pt,
      clip: true,
      fill: rgb("#ffffff"),
      stroke: (paint: rgb("#000000"), thickness: 0pt),
    )[
      // 图片区：16:9 比例
      #image(image-src, width: 375pt, height: 210pt, fit: "cover")

      // 内容区
      #pad(x: 16pt, y: 16pt)[
        // 标题层：20pt semibold
        #text(size: 20pt, weight: "semibold", fill: rgb("#1a1a1a"))[#title]
        #v(8pt)

        // 正文层：14pt regular
        #text(size: 14pt, fill: rgb("#444444"), leading: 0.9em)[#body]
        #v(12pt)

        // 标签层：12pt medium
        #if tags.len() > 0 {
          grid(
            columns: tags.map(t => auto),
            column-gutter: 8pt,
            ..tags.map(t => box(
              inset: (x: 8pt, y: 4pt),
              fill: rgb("#f5f5f5"),
              radius: 4pt,
              text(size: 12pt, weight: "medium", fill: rgb("#666666"))[#t]
            ))
          )
          v(12pt)
        }

        // 页脚：作者 + 时间
        #line(length: 100%, stroke: 0.5pt + rgb("#eeeeee"))
        #v(8pt)
        #grid(
          columns: (1fr, 1fr),
          text(size: 12pt, fill: rgb("#999999"))[#author],
          align(right, text(size: 12pt, fill: rgb("#999999"))[#time]),
        )
      ]
    ]
  }
  ```
- **与 layout-grid.md 对接规则**: 此原子是 guizang-social-card-skill 的核心融入点。`width: 375px` 对应 layout-grid.md 第 3.1 节手机竖屏尺寸。`padding: 16px`（4×4px）对应 layout-grid.md 第 2.1 节手机竖屏左右边距。图片高度 `210px`（16:9 比例，对齐 4px 基准）建立视觉重心。字体层级（20px/14px/12px）均为 4px 整数倍，与 typography-atoms.md 的字号阶梯对接。卡片间距遵循 `--spacing-para: 16px`。

---

### LA-CARD-003: 图文并排卡片

- **原子 ID**: LA-CARD-003
- **适用场景**: 特性展示、产品对比、教程步骤、图文交替排列的杂志风格内容
- **HTML+CSS 实现**:
  ```html
  <div class="la-card-alternating">
    <article class="la-card-alt la-card-alt-left">
      <div class="la-card-alt-image"><img src="1.jpg" alt="" /></div>
      <div class="la-card-alt-text">
        <h3>特性一</h3>
        <p>描述文字</p>
      </div>
    </article>
    <article class="la-card-alt la-card-alt-right">
      <div class="la-card-alt-image"><img src="2.jpg" alt="" /></div>
      <div class="la-card-alt-text">
        <h3>特性二</h3>
        <p>描述文字</p>
      </div>
    </article>
  </div>
  ```
  ```css
  .la-card-alternating {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;               /* 6×4px */
    padding: 32px;           /* 8×4px */
    box-sizing: border-box;
  }
  .la-card-alt {
    display: flex;
    align-items: center;
    background: #ffffff;
    border-radius: 8px;      /* 2×4px */
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
  }
  .la-card-alt-image {
    flex: 0 0 48%;
  }
  .la-card-alt-image img {
    width: 100%;
    height: 120px;          /* 30×4px */
    object-fit: cover;
    display: block;
  }
  .la-card-alt-text {
    flex: 1;
    padding: 16px;          /* 4×4px */
    box-sizing: border-box;
  }
  .la-card-alt-text h3 {
    font-size: 16px;        /* 4×4px */
    font-weight: 600;
    margin: 0 0 8px 0;      /* 2×4px */
  }
  .la-card-alt-text p {
    font-size: 14px;
    line-height: 1.5;
    color: #555555;
    margin: 0;
  }
  /* 交替排列：偶数卡片图片在右 */
  .la-card-alt-right {
    flex-direction: row-reverse;
  }

  @media (max-width: 767px) {
    .la-card-alternating {
      grid-template-columns: 1fr;
      gap: 16px;
      padding: 16px;
    }
  }
  ```
- **Typst 实现**:
  ```typst
  #let la-card-alt(
    image-src,
    title,
    desc,
    reverse: false,
  ) = {
    let cols = if reverse { (1fr, 48%) } else { (48%, 1fr) }
    let img-cell = rect(width: 100%, height: 120pt, fill: image(image-src, width: 100%, height: 100%, fit: "cover"))
    let text-cell = pad(x: 16pt, y: 16pt)[
      #text(size: 16pt, weight: "semibold")[#title]
      #v(8pt)
      #text(size: 14pt, fill: rgb("#555555"))[#desc]
    ]
    grid(
      columns: cols,
      column-gutter: 0pt,
      if reverse { text-cell } else { img-cell },
      if reverse { img-cell } else { text-cell },
    )
  }

  // 使用示例
  #grid(
    columns: (1fr, 1fr),
    column-gutter: 24pt,
    row-gutter: 24pt,
    la-card-alt("1.jpg", "特性一", "描述文字"),
    la-card-alt("2.jpg", "特性二", "描述文字", reverse: true),
  )
  ```
- **与 layout-grid.md 对接规则**: 对应 layout-grid.md 第 4.2 节"图文混排"模式的双栏变体。外层 `grid-template-columns: 1fr 1fr` 对应 6/12 + 6/12 双栏。卡片内边距 `16px`（4×4px）比 layout-grid.md 默认 `--padding-card: 24px` 更紧凑，适配并排卡片的有限空间。`gap: 24px` 对齐 `--grid-gutter` 变量。

---

### LA-CARD-004: 引用卡片

- **原子 ID**: LA-CARD-004
- **适用场景**: 名人名言、用户评价、专家观点、编辑评论、杂志侧边栏引用
- **HTML+CSS 实现**:
  ```html
  <blockquote class="la-card-quote">
    <div class="la-card-quote-band"></div>
    <div class="la-card-quote-content">
      <p class="la-card-quote-text">
        "好的设计不是让你觉得它有多好，而是让你觉得它本该如此。"
      </p>
      <footer class="la-card-quote-source">
        <cite class="la-card-quote-author">—— 设计师姓名</cite>
        <span class="la-card-quote-role">职位 / 机构</span>
      </footer>
    </div>
  </blockquote>
  ```
  ```css
  .la-card-quote {
    display: flex;
    background: #f5f5f5;
    border-radius: 8px;        /* 2×4px */
    overflow: hidden;
    margin: 24px 0;            /* 6×4px */
    box-sizing: border-box;
  }
  .la-card-quote-band {
    flex: 0 0 4px;             /* 1×4px，左侧色带 */
    background: #1a1a1a;
  }
  .la-card-quote-content {
    flex: 1;
    padding: 24px;             /* 6×4px */
    box-sizing: border-box;
  }
  .la-card-quote-text {
    font-size: 20px;           /* 5×4px，引用文字略大 */
    line-height: 1.6;
    font-style: italic;
    color: #333333;
    margin: 0 0 16px 0;        /* 4×4px */
  }
  .la-card-quote-source {
    display: flex;
    flex-direction: column;
    gap: 4px;                  /* 1×4px */
  }
  .la-card-quote-author {
    font-size: 14px;
    font-weight: 600;
    font-style: normal;
    color: #1a1a1a;
  }
  .la-card-quote-role {
    font-size: 12px;           /* 3×4px */
    color: #888888;
  }
  ```
- **Typst 实现**:
  ```typst
  #let la-card-quote(
    quote-text,
    author,
    role: "",
  ) = {
    block(
      width: 100%,
      fill: rgb("#f5f5f5"),
      radius: 8pt,
      clip: true,
    )[
      #grid(
        columns: (4pt, 1fr),
        column-gutter: 0pt,
        // 左侧色带
        rect(width: 100%, height: 100%, fill: rgb("#1a1a1a")),
        // 内容区
        pad(x: 24pt, y: 24pt)[
          #text(size: 20pt, style: "italic", fill: rgb("#333333"))[#quote-text]
          #v(16pt)
          #text(size: 14pt, weight: "semibold", fill: rgb("#1a1a1a"))[#author]
          #v(4pt)
          #text(size: 12pt, fill: rgb("#888888"))[#role]
        ]
      )
    ]
  }
  ```
- **与 layout-grid.md 对接规则**: 背景色 `#f5f5f5` 对应 layout-grid.md 引用块规范。`padding: 24px` 对齐 `--padding-card` 变量。左侧色带 `4px`（1×4px）是最小 4px 基准单位。`margin: 24px 0` 对齐 layout-grid.md 第 2.2 节图片上下间距 `--spacing-image: 24px`。引用文字 20px 介于标题与正文之间，建立视觉层级。

---

### LA-CARD-005: 数据卡片

- **原子 ID**: LA-CARD-005
- **适用场景**: 数据仪表盘、KPI 指标展示、统计报告、数据驱动型内容卡片
- **HTML+CSS 实现**:
  ```html
  <div class="la-card-data">
    <div class="la-card-data-value">
      <span class="la-card-data-number">12,847</span>
      <span class="la-card-data-trend la-card-data-trend-up">↑ 12.5%</span>
    </div>
    <div class="la-card-data-label">月活跃用户</div>
    <div class="la-card-data-desc">较上月增长 1,423 人</div>
  </div>
  ```
  ```css
  .la-card-data {
    background: #ffffff;
    border-radius: 8px;        /* 2×4px */
    padding: 24px;             /* 6×4px */
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
    box-sizing: border-box;
  }
  .la-card-data-value {
    display: flex;
    align-items: baseline;
    gap: 12px;                 /* 3×4px */
    margin-bottom: 8px;        /* 2×4px */
  }
  .la-card-data-number {
    font-size: 48px;           /* 12×4px，大字号 */
    font-weight: 600;          /* semibold */
    line-height: 1;
    color: #1a1a1a;
    letter-spacing: -0.02em;
  }
  .la-card-data-trend {
    font-size: 16px;           /* 4×4px */
    font-weight: 500;
  }
  .la-card-data-trend-up {
    color: #16a34a;
  }
  .la-card-data-trend-down {
    color: #dc2626;
  }
  .la-card-data-label {
    font-size: 14px;
    color: #555555;
    margin-bottom: 4px;        /* 1×4px */
  }
  .la-card-data-desc {
    font-size: 12px;           /* 3×4px */
    color: #999999;
  }
  ```
- **Typst 实现**:
  ```typst
  #let la-card-data(
    number,
    trend: "",
    trend-up: true,
    label,
    desc: "",
  ) = {
    block(
      width: 100%,
      fill: rgb("#ffffff"),
      radius: 8pt,
      inset: 24pt,
    )[
      #grid(
        columns: (auto, auto),
        column-gutter: 12pt,
        align(baseline,
          text(size: 48pt, weight: "semibold", fill: rgb("#1a1a1a"), tracking: -1pt)[#number]
        ),
        align(baseline,
          text(
            size: 16pt,
            weight: "medium",
            fill: if trend-up { rgb("#16a34a") } else { rgb("#dc2626") }
          )[#trend]
        ),
      )
      #v(8pt)
      #text(size: 14pt, fill: rgb("#555555"))[#label]
      #v(4pt)
      #text(size: 12pt, fill: rgb("#999999"))[#desc]
    ]
  }
  ```
- **与 layout-grid.md 对接规则**: `padding: 24px` 对齐 `--padding-card` 变量。数字字号 `48px`（12×4px）对应 typography-atoms.md 的 h1 层级，建立数据卡片的视觉焦点。趋势箭头颜色（绿色 #16a34a / 红色 #dc2626）遵循数据可视化语义色规范。所有间距值（4px/8px/12px/24px）均为 4px 整数倍。

---

### LA-CARD-006: 时间线卡片

- **原子 ID**: LA-CARD-006
- **适用场景**: 发展历程、项目里程碑、事件时间轴、教程步骤序列
- **HTML+CSS 实现**:
  ```html
  <div class="la-card-timeline">
    <div class="la-timeline-item">
      <div class="la-timeline-dot"></div>
      <div class="la-timeline-content">
        <time class="la-timeline-time">2026-06</time>
        <h4 class="la-timeline-title">里程碑事件</h4>
        <p class="la-timeline-desc">事件描述文字</p>
      </div>
    </div>
    <div class="la-timeline-item">
      <div class="la-timeline-dot"></div>
      <div class="la-timeline-content">
        <time class="la-timeline-time">2026-03</time>
        <h4 class="la-timeline-title">另一个事件</h4>
        <p class="la-timeline-desc">事件描述文字</p>
      </div>
    </div>
  </div>
  ```
  ```css
  .la-card-timeline {
    position: relative;
    padding-left: 32px;        /* 8×4px，为时间线留空间 */
  }
  /* 垂直连接线 */
  .la-card-timeline::before {
    content: '';
    position: absolute;
    left: 12px;               /* 3×4px，圆点中心位置 */
    top: 8px;
    bottom: 8px;
    width: 2px;               /* 连接线宽度 2px */
    background: #e0e0e0;
  }
  .la-timeline-item {
    position: relative;
    padding-bottom: 32px;     /* 8×4px */
    display: flex;
    gap: 16px;                /* 4×4px */
  }
  .la-timeline-item:last-child {
    padding-bottom: 0;
  }
  .la-timeline-dot {
    position: absolute;
    left: -26px;              /* 对齐连接线 */
    top: 4px;
    width: 12px;             /* 3×4px */
    height: 12px;
    border-radius: 50%;
    background: #1a1a1a;
    border: 2px solid #ffffff;
    box-sizing: border-box;
  }
  .la-timeline-content {
    flex: 1;
  }
  .la-timeline-time {
    font-size: 12px;          /* 3×4px */
    color: #999999;
    display: block;
    margin-bottom: 4px;       /* 1×4px */
  }
  .la-timeline-title {
    font-size: 16px;          /* 4×4px */
    font-weight: 600;
    margin: 0 0 8px 0;        /* 2×4px */
  }
  .la-timeline-desc {
    font-size: 14px;
    line-height: 1.6;
    color: #555555;
    margin: 0;
  }
  ```
- **Typst 实现**:
  ```typst
  #let la-card-timeline(items) = {
    let n = items.len()
    for (i, item) in items.enumerate() {
      // 时间点圆点
      place(dx: 0pt, dy: 4pt,
        circle(radius: 6pt, fill: rgb("#1a1a1a"), stroke: 2pt + white)
      )
      // 连接线（非最后一项）
      if i < n - 1 {
        place(dx: 5pt, dy: 16pt,
          line(length: 32pt, angle: 90deg, stroke: 2pt + rgb("#e0e0e0"))
        )
      }
      // 内容
      block(inset: (left: 24pt, bottom: 32pt))[
        #text(size: 12pt, fill: rgb("#999999"))[#item.time]
        #v(4pt)
        #text(size: 16pt, weight: "semibold")[#item.title]
        #v(8pt)
        #text(size: 14pt, fill: rgb("#555555"))[#item.desc]
      ]
    }
  }

  // 使用示例
  #la-card-timeline((
    (time: "2026-06", title: "里程碑事件", desc: "事件描述文字"),
    (time: "2026-03", title: "另一个事件", desc: "事件描述文字"),
  ))
  ```
- **与 layout-grid.md 对接规则**: `padding-left: 32px`（8×4px）为时间线留出空间，对齐 layout-grid.md `--spacing-heading-top` 变量。连接线 `2px` 是 layout-grid.md 中表格边框的标准宽度。圆点 `12px`（3×4px）和间距值均对齐 4px 基准。时间线项间距 `32px`（8×4px）建立垂直节奏感。

---

## 三、页面布局原子（LA-PAGE）

> **对接规则**: 每个页面原子通过 `--page-width` / `--page-height` / `--page-margin-*` 变量与 layout-grid.md 对接，页面尺寸从 layout-grid.md 第 3.1 节标准页面尺寸表选取。

### LA-PAGE-001: 落地页布局

- **原子 ID**: LA-PAGE-001
- **适用场景**: 产品落地页、营销活动页、SaaS 首页、品牌官网首页
- **HTML+CSS 实现**:
  ```html
  <div class="la-page-landing">
    <section class="la-landing-hero">
      <h1>产品名称</h1>
      <p>一句话价值主张</p>
      <button>立即开始</button>
    </section>
    <section class="la-landing-features">
      <h2>核心特性</h2>
      <div class="la-landing-features-grid">
        <!-- 特性卡片 -->
      </div>
    </section>
    <section class="la-landing-cta">
      <h2>准备好开始了吗？</h2>
      <button>免费试用</button>
    </section>
    <footer class="la-landing-footer">
      <!-- 页脚内容 -->
    </footer>
  </div>
  ```
  ```css
  .la-page-landing {
    width: 100vw;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    box-sizing: border-box;
  }
  .la-landing-hero {
    width: 100%;
    min-height: 480px;        /* 120×4px */
    padding: 80px 32px;       /* 20×4px, 8×4px */
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    box-sizing: border-box;
  }
  .la-landing-hero h1 {
    font-size: 48px;          /* 12×4px */
    font-weight: 700;
    margin: 0 0 16px 0;       /* 4×4px */
  }
  .la-landing-hero p {
    font-size: 20px;          /* 5×4px */
    color: #555555;
    margin: 0 0 32px 0;       /* 8×4px */
  }
  .la-landing-features {
    width: 100%;
    max-width: 1200px;        /* 300×4px */
    margin: 0 auto;
    padding: 64px 32px;       /* 16×4px, 8×4px */
    box-sizing: border-box;
  }
  .la-landing-features h2 {
    font-size: 32px;          /* 8×4px */
    text-align: center;
    margin: 0 0 48px 0;       /* 12×4px */
  }
  .la-landing-features-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;                /* 6×4px */
  }
  .la-landing-cta {
    width: 100%;
    padding: 64px 32px;       /* 16×4px, 8×4px */
    text-align: center;
    background: #f9f9f9;
    box-sizing: border-box;
  }
  .la-landing-footer {
    width: 100%;
    padding: 32px;            /* 8×4px */
    background: #1a1a1a;
    color: #ffffff;
    box-sizing: border-box;
  }
  ```
- **Typst 实现**:
  ```typst
  #let la-page-landing(
    hero-title,
    hero-desc,
    features: (),
    cta-title,
    footer-body,
  ) = {
    set page(width: 100%, margin: 0pt)

    // Hero 区
    block(width: 100%, height: 480pt, fill: rgb("#ffffff"))[
      #align(center + horizon)[
        #pad(x: 32pt, y: 80pt)[
          #text(size: 48pt, weight: "bold")[#hero-title]
          #v(16pt)
          #text(size: 20pt, fill: rgb("#555555"))[#hero-desc]
          #v(32pt)
          #rect(inset: (x: 32pt, y: 12pt), fill: rgb("#1a1a1a"), radius: 8pt)[
            #text(size: 16pt, fill: white)[立即开始]
          ]
        ]
      ]
    ]

    // 特性区
    block(width: 100%, inset: (x: 32pt, y: 64pt))[
      #align(center)[#text(size: 32pt, weight: "bold")[核心特性]]
      #v(48pt)
      #grid(
        columns: (1fr,) * 3,
        column-gutter: 24pt,
        row-gutter: 24pt,
        ..features.map(f => f)
      )
    ]

    // CTA 区
    block(width: 100%, fill: rgb("#f9f9f9"), inset: (x: 32pt, y: 64pt))[
      #align(center)[
        #text(size: 32pt, weight: "bold")[#cta-title]
        #v(32pt)
        #rect(inset: (x: 32pt, y: 12pt), fill: rgb("#1a1a1a"), radius: 8pt)[
          #text(size: 16pt, fill: white)[免费试用]
        ]
      ]
    ]

    // 页脚
    block(width: 100%, fill: rgb("#1a1a1a"), inset: 32pt)[
      #text(size: 14pt, fill: white)[#footer-body]
    ]
  }
  ```
- **与 layout-grid.md 对接规则**: `width: 100vw` 对应 layout-grid.md 全宽布局（12/12）。`max-width: 1200px`（300×4px）对应 layout-grid.md 第 5.1 节 xl 断点（1200px）。`padding: 80px 32px` 中 80px（20×4px）为 Hero 区垂直留白，32px（8×4px）对齐 `--page-margin-*` 变量。特性区 3 列网格对应 layout-grid.md 第 4.2 节"三栏卡片"模式（4/12 × 3）。

---

### LA-PAGE-002: 文章页布局

- **原子 ID**: LA-PAGE-002
- **适用场景**: 博客文章页、新闻详情页、技术文档页、长文阅读页
- **HTML+CSS 实现**:
  ```html
  <div class="la-page-article">
    <header class="la-article-header">
      <h1>文章标题</h1>
      <div class="la-article-meta">
        <span>作者</span>
        <time>2026-06-19</time>
        <span>阅读时长 5 分钟</span>
      </div>
    </header>
    <div class="la-article-body">
      <main class="la-article-main">
        <!-- 正文内容 -->
      </main>
      <aside class="la-article-sidebar">
        <!-- 侧边栏：目录、相关文章 -->
      </aside>
    </div>
  </div>
  ```
  ```css
  .la-page-article {
    max-width: 1200px;        /* 300×4px */
    margin: 0 auto;
    padding: 32px;            /* 8×4px */
    box-sizing: border-box;
  }
  .la-article-header {
    margin-bottom: 48px;      /* 12×4px */
    padding-bottom: 24px;     /* 6×4px */
    border-bottom: 1px solid #eeeeee;
  }
  .la-article-header h1 {
    font-size: 36px;          /* 9×4px */
    font-weight: 700;
    line-height: 1.2;
    margin: 0 0 16px 0;       /* 4×4px */
  }
  .la-article-meta {
    display: flex;
    gap: 16px;                /* 4×4px */
    font-size: 14px;
    color: #888888;
  }
  .la-article-body {
    display: grid;
    grid-template-columns: 65% 35%;
    column-gap: 32px;         /* 8×4px */
  }
  .la-article-main {
    font-size: 16px;          /* 4×4px */
    line-height: 1.8;
    color: #333333;
  }
  .la-article-main p {
    margin: 0 0 24px 0;       /* 6×4px */
  }
  .la-article-sidebar {
    padding-left: 24px;       /* 6×4px */
    border-left: 1px solid #eeeeee;
  }

  @media (max-width: 1023px) {
    .la-article-body {
      grid-template-columns: 1fr;
      column-gap: 0;
      row-gap: 32px;
    }
    .la-article-sidebar {
      padding-left: 0;
      border-left: none;
    }
  }
  ```
- **Typst 实现**:
  ```typst
  #let la-page-article(
    title,
    author,
    time,
    read-time,
    main-body,
    sidebar-body,
  ) = {
    set page(margin: (left: 32pt, right: 32pt, top: 32pt, bottom: 32pt))

    // 标题区
    block(width: 100%)[
      #text(size: 36pt, weight: "bold")[#title]
      #v(16pt)
      #grid(
        columns: (auto, auto, auto),
        column-gutter: 16pt,
        text(size: 14pt, fill: rgb("#888888"))[#author],
        text(size: 14pt, fill: rgb("#888888"))[#time],
        text(size: 14pt, fill: rgb("#888888"))[阅读时长 #read-time],
      )
      #v(24pt)
      #line(length: 100%, stroke: 0.5pt + rgb("#eeeeee"))
      #v(48pt)
    ]

    // 正文 + 侧边栏
    grid(
      columns: (65%, 35%),
      column-gutter: 32pt,
      // 正文
      block(width: 100%)[
        #set text(size: 12pt, leading: 1.5em)
        #main-body
      ],
      // 侧边栏
      block(width: 100%, inset: (left: 24pt))[
        #line(length: 100%, stroke: 0.5pt + rgb("#eeeeee"))
        #v(8pt)
        #sidebar-body
      ]
    )
  }
  ```
- **与 layout-grid.md 对接规则**: 正文 65% + 侧边栏 35% 对应 layout-grid.md 第 4.2 节"主内容 + 侧边栏"模式（8/12 + 4/12 ≈ 66.7% + 33.3%）的微调变体。`column-gap: 32px`（8×4px）对齐 `--page-margin-*` 变量。`max-width: 1200px` 对应 layout-grid.md xl 断点。段间距 `24px`（6×4px）对齐 `--padding-card` 变量。

---

### LA-PAGE-003: 报告页布局

- **原子 ID**: LA-PAGE-003
- **适用场景**: 学术报告 PDF、年度报告、白皮书、A4 打印文档
- **HTML+CSS 实现**:
  ```html
  <div class="la-page-report">
    <section class="la-report-cover">
      <h1>报告标题</h1>
      <p>副标题</p>
      <p>机构名称 · 2026</p>
    </section>
    <section class="la-report-toc">
      <h2>目录</h2>
      <ol class="la-report-toc-list">
        <li>第一章 概述</li>
        <li>第二章 分析</li>
      </ol>
    </section>
    <section class="la-report-body">
      <header class="la-report-header">
        <span>报告标题</span>
        <span>第 1 页</span>
      </header>
      <div class="la-report-content">
        <!-- 双栏正文 -->
      </div>
      <footer class="la-report-footer">
        <span>机构名称</span>
        <span>2026</span>
      </footer>
    </section>
  </div>
  ```
  ```css
  .la-page-report {
    width: 210mm;             /* A4 宽度 */
    min-height: 297mm;        /* A4 高度 */
    margin: 0 auto;
    background: #ffffff;
    box-sizing: border-box;
  }
  .la-report-cover {
    width: 100%;
    height: 297mm;
    padding: 80px 64px;       /* 20×4px, 16×4px */
    display: flex;
    flex-direction: column;
    justify-content: center;
    box-sizing: border-box;
    page-break-after: always;
  }
  .la-report-cover h1 {
    font-size: 48px;          /* 12×4px */
    font-weight: 700;
    margin: 0 0 16px 0;
  }
  .la-report-toc {
    padding: 64px 48px;       /* 16×4px, 12×4px */
    page-break-after: always;
    box-sizing: border-box;
  }
  .la-report-toc h2 {
    font-size: 24px;          /* 6×4px */
    margin: 0 0 32px 0;       /* 8×4px */
  }
  .la-report-toc-list li {
    font-size: 14px;
    line-height: 2;
  }
  .la-report-body {
    padding: 48px 40px;       /* 12×4px, 10×4px */
    box-sizing: border-box;
  }
  .la-report-header {
    display: flex;
    justify-content: space-between;
    padding-bottom: 16px;     /* 4×4px */
    border-bottom: 1px solid #eeeeee;
    font-size: 12px;          /* 3×4px */
    color: #888888;
    margin-bottom: 32px;      /* 8×4px */
  }
  .la-report-content {
    column-count: 2;
    column-gap: 24px;         /* 6×4px */
    font-size: 14px;
    line-height: 1.8;
  }
  .la-report-footer {
    display: flex;
    justify-content: space-between;
    padding-top: 16px;        /* 4×4px */
    border-top: 1px solid #eeeeee;
    font-size: 12px;
    color: #888888;
    margin-top: 32px;         /* 8×4px */
  }
  ```
- **Typst 实现**:
  ```typst
  #let la-page-report(
    title,
    subtitle,
    org,
    year,
    toc-items,
    body,
  ) = {
    set page(width: 210mm, height: 297mm, margin: (left: 40pt, right: 40pt, top: 48pt, bottom: 48pt))

    // 封面
    #page(margin: (left: 64pt, right: 64pt, top: 80pt, bottom: 80pt))[
      #v(1fr)
      #text(size: 48pt, weight: "bold")[#title]
      #v(16pt)
      #text(size: 20pt, fill: rgb("#555555"))[#subtitle]
      #v(1fr)
      #text(size: 16pt, fill: rgb("#888888"))[#org · #year]
    ]

    // 目录
    #page[
      #text(size: 24pt, weight: "bold")[目录]
      #v(32pt)
      #for item in toc-items {
        text(size: 14pt)[#item]
        linebreak()
      }
    ]

    // 正文双栏
    #set page(
      header: align(right)[
        #text(size: 12pt, fill: rgb("#888888"))[#title]
        #line(length: 100%, stroke: 0.5pt + rgb("#eeeeee"))
      ],
      footer: align(center)[
        #line(length: 100%, stroke: 0.5pt + rgb("#eeeeee"))
        #text(size: 12pt, fill: rgb("#888888"))[#org · #year]
      ]
    )
    #set columns(2, gutter: 24pt)
    #set text(size: 12pt, leading: 1.5em)
    #body
  }
  ```
- **与 layout-grid.md 对接规则**: `width: 210mm` / `height: 297mm` 严格对应 layout-grid.md 第 3.1 节 A4 纵向尺寸。`padding: 48px 40px` 对应 layout-grid.md 第 2.1 节 A4 打印边距（20mm ≈ 76px 上下，25mm ≈ 94px 左右）的数字适配变体。双栏 `column-gap: 24px` 对应 layout-grid.md `--grid-gutter` 变量。页眉页脚遵循 layout-grid.md 表格单元格内边距规范。

---

### LA-PAGE-004: 演示页布局

- **原子 ID**: LA-PAGE-004
- **适用场景**: PPT 演示文稿、全屏演讲幻灯片、会议展示页、16:9 演示
- **HTML+CSS 实现**:
  ```html
  <div class="la-page-presentation">
    <div class="la-presentation-slide">
      <div class="la-presentation-content">
        <h1>幻灯片标题</h1>
        <p>幻灯片内容</p>
      </div>
    </div>
  </div>
  ```
  ```css
  .la-page-presentation {
    width: 100vw;
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #000000;
    box-sizing: border-box;
  }
  .la-presentation-slide {
    width: 100%;
    max-width: 1920px;        /* 16:9 宽度 */
    height: 100%;
    max-height: 1080px;       /* 16:9 高度 */
    aspect-ratio: 16 / 9;
    padding: 64px;            /* 16×4px */
    display: flex;
    align-items: center;
    justify-content: center;
    background: #ffffff;
    box-sizing: border-box;
  }
  .la-presentation-content {
    width: 100%;
    max-width: 1280px;        /* 320×4px，内容最大宽度 */
    text-align: center;
  }
  .la-presentation-content h1 {
    font-size: 48px;          /* 12×4px */
    font-weight: 700;
    margin: 0 0 24px 0;       /* 6×4px */
  }
  .la-presentation-content p {
    font-size: 24px;          /* 6×4px */
    line-height: 1.5;
    color: #555555;
    margin: 0;
  }
  ```
- **Typst 实现**:
  ```typst
  #let la-page-presentation(
    title,
    body,
  ) = {
    set page(
      width: 1920pt,
      height: 1080pt,
      margin: 64pt,
    )
    align(center + horizon)[
      #block(width: 100%)[
        #text(size: 48pt, weight: "bold")[#title]
        #v(24pt)
        #text(size: 24pt, fill: rgb("#555555"))[#body]
      ]
    ]
  }

  // 使用示例
  #la-page-presentation(
    title: "幻灯片标题",
    body: "幻灯片内容",
  )
  ```
- **与 layout-grid.md 对接规则**: `max-width: 1920px` / `max-height: 1080px` 严格对应 layout-grid.md 第 3.1 节 16:9 幻灯片尺寸。`padding: 64px`（16×4px）对应 layout-grid.md 第 2.1 节 16:9 幻灯片边距（80px 上下，120px 左右）的居中简化变体。`aspect-ratio: 16 / 9` 确保比例一致。内容最大宽度 `1280px`（320×4px）确保可读性。

---

## 四、响应式布局原子（LA-RESP）

> **对接规则**: 每个响应式原子通过 layout-grid.md 第 5.1 节断点定义表对接，断点值严格遵循 layout-grid.md 的 xs/sm/md/lg/xl 断点规范。

### LA-RESP-001: 移动端断点

- **原子 ID**: LA-RESP-001
- **适用场景**: 手机端布局适配（< 640px）、移动端 H5 页面、竖版卡片流
- **HTML+CSS 实现**:
  ```html
  <div class="la-resp-mobile">
    <div class="la-resp-mobile-item">内容块 1</div>
    <div class="la-resp-mobile-item">内容块 2</div>
    <div class="la-resp-mobile-item">内容块 3</div>
  </div>
  ```
  ```css
  .la-resp-mobile {
    display: flex;
    flex-direction: column;
    gap: 16px;                /* 4×4px */
    padding: 16px;            /* 4×4px */
    box-sizing: border-box;
  }
  .la-resp-mobile-item {
    width: 100%;
    box-sizing: border-box;
  }
  /* 移动端字号对齐 4px 基准系统 */
  .la-resp-mobile {
    font-size: 16px;          /* 4×4px，基准 16px（对齐 4px 基准系统） */
  }
  .la-resp-mobile h1 {
    font-size: 32px;          /* 8×4px */
  }
  .la-resp-mobile h2 {
    font-size: 24px;          /* 6×4px */
  }

  /* 仅在 < 640px 时生效 */
  @media (max-width: 639px) {
    .la-resp-mobile {
      padding: 16px;
    }
  }
  ```
- **Typst 实现**:
  ```typst
  #let la-resp-mobile(
    body,
    base-font-size: 12pt,    // 移动端基准字号（桌面 14pt × 0.9 ≈ 12.6pt ≈ 12pt）
  ) = {
    set page(width: 375pt, margin: (left: 16pt, right: 16pt, top: 16pt, bottom: 16pt))
    set text(size: base-font-size)
    // 移动端单栏
    set columns(1)
    body
  }

  // 使用示例
  #la-resp-mobile(base-font-size: 12pt)[
    #text(size: 24pt, weight: "bold")[移动端标题]
    #v(16pt)
    内容块 1
    #v(16pt)
    内容块 2
  ]
  ```
- **与 layout-grid.md 对接规则**: 对应 layout-grid.md 第 5.1 节 xs/sm 断点（0-767px）。`padding: 16px`（4×4px）对齐 layout-grid.md 第 2.1 节手机竖屏边距（左右 16px）。字号对齐 4px 基准系统（16px/24px/32px）对应 layout-grid.md 第 5.2 节"窄屏下页面边距减半"的字号适配策略。单列布局遵循 layout-grid.md 第 5.2 节"多栏布局强制折叠为 1 栏"规则。

---

### LA-RESP-002: 平板断点

- **原子 ID**: LA-RESP-002
- **适用场景**: 平板端布局适配（640px-1024px）、iPad 横屏、小平板竖屏
- **HTML+CSS 实现**:
  ```html
  <div class="la-resp-tablet">
    <div class="la-resp-tablet-item">内容块 1</div>
    <div class="la-resp-tablet-item">内容块 2</div>
    <div class="la-resp-tablet-item">内容块 3</div>
    <div class="la-resp-tablet-item">内容块 4</div>
  </div>
  ```
  ```css
  .la-resp-tablet {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;                /* 6×4px */
    padding: 24px;            /* 6×4px */
    box-sizing: border-box;
  }
  .la-resp-tablet-item {
    box-sizing: border-box;
  }

  /* 仅在 640px-1024px 时生效 */
  @media (min-width: 640px) and (max-width: 1023px) {
    .la-resp-tablet {
      grid-template-columns: repeat(2, 1fr);
    }
  }
  ```
- **Typst 实现**:
  ```typst
  #let la-resp-tablet(
    body,
    page-width: 768pt,       // 平板基准宽度
  ) = {
    set page(width: page-width, margin: (left: 24pt, right: 24pt, top: 24pt, bottom: 24pt))
    // 平板端 2 栏
    grid(
      columns: (1fr, 1fr),
      column-gutter: 24pt,
      row-gutter: 24pt,
      ..body
    )
  }

  // 使用示例
  #la-resp-tablet(page-width: 768pt)[
    #gridcell[内容块 1]
    #gridcell[内容块 2]
    #gridcell[内容块 3]
    #gridcell[内容块 4]
  ]
  ```
- **与 layout-grid.md 对接规则**: 对应 layout-grid.md 第 5.1 节 md 断点（768px-991px）及 sm 断点上限。`grid-template-columns: repeat(2, 1fr)` 对应 layout-grid.md 第 5.1 节 md 断点"最多 2 栏"策略。`padding: 24px`（6×4px）对齐 layout-grid.md 第 2.1 节公众号边距。`gap: 24px` 对齐 `--grid-gutter` 变量。

---

### LA-RESP-003: 桌面断点

- **原子 ID**: LA-RESP-003
- **适用场景**: 桌面端布局适配（1024px-1280px）、笔记本屏幕、标准显示器
- **HTML+CSS 实现**:
  ```html
  <div class="la-resp-desktop">
    <div class="la-resp-desktop-item">内容块 1</div>
    <div class="la-resp-desktop-item">内容块 2</div>
    <div class="la-resp-desktop-item">内容块 3</div>
    <div class="la-resp-desktop-item">内容块 4</div>
    <div class="la-resp-desktop-item">内容块 5</div>
    <div class="la-resp-desktop-item">内容块 6</div>
  </div>
  ```
  ```css
  .la-resp-desktop {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 32px;                /* 8×4px */
    padding: 32px;            /* 8×4px */
    box-sizing: border-box;
  }
  .la-resp-desktop-item {
    box-sizing: border-box;
  }

  /* 仅在 1024px-1280px 时生效 */
  @media (min-width: 1024px) and (max-width: 1279px) {
    .la-resp-desktop {
      grid-template-columns: repeat(3, 1fr);
    }
  }
  ```
- **Typst 实现**:
  ```typst
  #let la-resp-desktop(
    body,
    page-width: 1024pt,      // 桌面基准宽度
  ) = {
    set page(width: page-width, margin: (left: 32pt, right: 32pt, top: 32pt, bottom: 32pt))
    // 桌面端 3-4 栏
    grid(
      columns: (1fr, 1fr, 1fr),
      column-gutter: 32pt,
      row-gutter: 32pt,
      ..body
    )
  }

  // 使用示例
  #la-resp-desktop(page-width: 1024pt)[
    #gridcell[内容块 1]
    #gridcell[内容块 2]
    #gridcell[内容块 3]
    #gridcell[内容块 4]
    #gridcell[内容块 5]
    #gridcell[内容块 6]
  ]
  ```
- **与 layout-grid.md 对接规则**: 对应 layout-grid.md 第 5.1 节 lg 断点（992px-1199px）。`grid-template-columns: repeat(3, 1fr)` 对应 layout-grid.md 第 5.1 节 lg 断点"最多 3 栏"策略。`padding: 32px`（8×4px）对齐 layout-grid.md `--page-margin-*` 变量。`gap: 32px`（8×4px）比默认 `--grid-gutter: 16px` 更宽松，适用于桌面端的呼吸感。

---

### LA-RESP-004: 超宽屏断点

- **原子 ID**: LA-RESP-004
- **适用场景**: 超宽屏布局适配（> 1280px）、4K 显示器、超宽显示器、大屏展示
- **HTML+CSS 实现**:
  ```html
  <div class="la-resp-wide">
    <div class="la-resp-wide-container">
      <div class="la-resp-wide-item">内容块 1</div>
      <div class="la-resp-wide-item">内容块 2</div>
      <div class="la-resp-wide-item">内容块 3</div>
      <div class="la-resp-wide-item">内容块 4</div>
    </div>
  </div>
  ```
  ```css
  .la-resp-wide {
    width: 100%;
    display: flex;
    justify-content: center;
    box-sizing: border-box;
  }
  .la-resp-wide-container {
    width: 100%;
    max-width: 1440px;        /* 360×4px，最大宽度居中 */
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 32px;                /* 8×4px */
    padding: 48px;            /* 12×4px */
    box-sizing: border-box;
  }
  .la-resp-wide-item {
    box-sizing: border-box;
  }

  /* 仅在 > 1280px 时生效 */
  @media (min-width: 1280px) {
    .la-resp-wide-container {
      grid-template-columns: repeat(4, 1fr);
    }
  }
  ```
- **Typst 实现**:
  ```typst
  #let la-resp-wide(
    body,
    page-width: 1440pt,      // 超宽屏最大宽度
  ) = {
    set page(width: page-width, margin: (left: 48pt, right: 48pt, top: 48pt, bottom: 48pt))
    // 超宽屏 4 栏
    grid(
      columns: (1fr, 1fr, 1fr, 1fr),
      column-gutter: 32pt,
      row-gutter: 32pt,
      ..body
    )
  }

  // 使用示例
  #la-resp-wide(page-width: 1440pt)[
    #gridcell[内容块 1]
    #gridcell[内容块 2]
    #gridcell[内容块 3]
    #gridcell[内容块 4]
  ]
  ```
- **与 layout-grid.md 对接规则**: 对应 layout-grid.md 第 5.1 节 xl 断点（1200px+）。`max-width: 1440px`（360×4px）限制内容最大宽度，避免超宽屏下内容过度拉伸。`grid-template-columns: repeat(4, 1fr)` 对应 layout-grid.md 第 5.1 节 xl 断点"最多 4 栏"策略。`padding: 48px`（12×4px）为超宽屏提供更宽松的边距。`gap: 32px`（8×4px）对齐 `--page-margin-*` 变量。

---

## 五、特殊布局原子（LA-SPEC）

> **对接规则**: 每个特殊原子通过 layout-grid.md 的间距变量对接，特殊布局不绕过栅格系统，而是在栅格框架内实现特殊排版效果。

### LA-SPEC-001: 首字下沉布局

- **原子 ID**: LA-SPEC-001
- **适用场景**: 杂志风格长文开头、编辑型内容、叙事性文章、品牌故事
- **HTML+CSS 实现**:
  ```html
  <div class="la-spec-dropcap">
    <p class="la-spec-dropcap-text">
      <span class="la-spec-dropcap-letter">好</span>的设计不是让你觉得它有多好，
      而是让你觉得它本该如此。这是对设计本质的深刻理解，
      也是对用户尊重的体现。
    </p>
  </div>
  ```
  ```css
  .la-spec-dropcap-text {
    font-size: 16px;          /* 4×4px */
    line-height: 1.8;
    color: #333333;
    margin: 0;
  }
  .la-spec-dropcap-letter {
    float: left;
    font-size: 56px;          /* 14×4px，3-4 行高 */
    font-weight: 700;
    line-height: 1;
    margin-right: 8px;        /* 2×4px */
    margin-top: 4px;          /* 1×4px，微调垂直对齐 */
    color: #1a1a1a;
  }
  /* 清除浮动 */
  .la-spec-dropcap-text::after {
    content: '';
    display: table;
    clear: both;
  }
  ```
- **Typst 实现**:
  ```typst
  #let la-spec-dropcap(
    first-char,
    body,
  ) = {
    // Typst 通过 place + float 实现首字下沉
    place(float: true, dx: 0pt, dy: 4pt,
      text(size: 56pt, weight: "bold", fill: rgb("#1a1a1a"))[#first-char]
    )
    // 正文
    set text(size: 12pt, leading: 1.5em)
    body
  }

  // 使用示例
  #la-spec-dropcap(
    "好",
    [的设计不是让你觉得它有多好，而是让你觉得它本该如此。]
  )
  ```
- **与 layout-grid.md 对接规则**: 首字 `font-size: 56px`（14×4px）约为正文 16px 的 3.5 倍，对应 3-4 行高。`margin-right: 8px`（2×4px）对齐 layout-grid.md `--spacing-list-item` 变量。正文 `font-size: 16px` / `line-height: 1.8` 遵循 layout-grid.md 段落间距规范。首字下沉不绕过栅格系统，而是在文本流内通过 float 实现。

---

### LA-SPEC-002: 图文绕排布局

- **原子 ID**: LA-SPEC-002
- **适用场景**: 杂志图文混排、新闻配图、教程插图、编辑型内容图文穿插
- **HTML+CSS 实现**:
  ```html
  <div class="la-spec-wrap">
    <img class="la-spec-wrap-image la-spec-wrap-left" src="image.jpg" alt="配图" />
    <p class="la-spec-wrap-text">
      这是图文绕排的文字内容。图片浮动在左侧，
      文字自动环绕图片排列，形成杂志风格的图文混排效果。
      当文字内容足够多时，会在图片下方继续流动排列。
    </p>
  </div>
  ```
  ```css
  .la-spec-wrap {
    box-sizing: border-box;
  }
  .la-spec-wrap-image {
    width: 240px;             /* 60×4px */
    height: auto;
    margin: 0 16px 8px 0;    /* 4×4px, 2×4px 右下边距 */
    border-radius: 8px;       /* 2×4px */
  }
  .la-spec-wrap-left {
    float: left;
  }
  .la-spec-wrap-right {
    float: right;
    margin: 0 0 8px 16px;    /* 2×4px 下，4×4px 左 */
  }
  .la-spec-wrap-text {
    font-size: 16px;          /* 4×4px */
    line-height: 1.8;
    color: #333333;
    margin: 0;
  }
  /* 清除浮动 */
  .la-spec-wrap::after {
    content: '';
    display: table;
    clear: both;
  }
  ```
- **Typst 实现**:
  ```typst
  #let la-spec-wrap(
    image-src,
    body,
    align-side: left,        // left 或 right
  ) = {
    let dx = if align-side == left { 0pt } else { 0pt }
    place(
      float: true,
      alignment: if align-side == left { left } else { right },
      dx: dx,
      image(image-src, width: 180pt)
    )
    // 图文绕排通过 place float 实现
    set text(size: 12pt, leading: 1.5em)
    body
  }

  // 使用示例
  #la-spec-wrap(
    "image.jpg",
    [这是图文绕排的文字内容。图片浮动在左侧，文字自动环绕图片排列。],
    align-side: left,
  )
  ```
- **与 layout-grid.md 对接规则**: 图片宽度 `240px`（60×4px）约为 layout-grid.md 12 列栅格中 4/12 列的宽度。`margin: 0 16px 8px 0` 中 16px（4×4px）对齐 `--grid-gutter` 变量，8px（2×4px）对齐 `--spacing-list-item` 变量。图文绕排通过 float 实现，不绕过 layout-grid.md 第七章强制规则第 5 条"栅格不可覆盖"。

---

### LA-SPEC-003: 脚注边栏布局

- **原子 ID**: LA-SPEC-003
- **适用场景**: 学术文档脚注、报告注释、术语解释、杂志侧边栏注释
- **HTML+CSS 实现**:
  ```html
  <div class="la-spec-footnote">
    <div class="la-spec-footnote-main">
      <p>正文内容，包含需要注释的术语<sup class="la-spec-footnote-ref">1</sup>。</p>
    </div>
    <aside class="la-spec-footnote-sidebar">
      <ol class="la-spec-footnote-list">
        <li>术语的详细解释和来源说明。</li>
      </ol>
    </aside>
  </div>
  ```
  ```css
  .la-spec-footnote {
    display: grid;
    grid-template-columns: 1fr 240px;  /* 主内容 + 侧边栏 240px（60×4px） */
    column-gap: 32px;         /* 8×4px */
    box-sizing: border-box;
  }
  .la-spec-footnote-main {
    font-size: 16px;          /* 4×4px */
    line-height: 1.8;
    color: #333333;
  }
  .la-spec-footnote-ref {
    font-size: 12px;          /* 3×4px */
    vertical-align: super;
    color: #1a1a1a;
  }
  .la-spec-footnote-sidebar {
    padding: 16px;            /* 4×4px */
    background: #f9f9f9;
    border-radius: 8px;       /* 2×4px */
    align-self: start;
  }
  .la-spec-footnote-list {
    margin: 0;
    padding-left: 20px;       /* 5×4px */
    font-size: 12px;          /* 3×4px，脚注字号 */
    line-height: 1.6;
    color: #666666;
  }
  .la-spec-footnote-list li {
    margin-bottom: 8px;       /* 2×4px */
  }

  @media (max-width: 1023px) {
    .la-spec-footnote {
      grid-template-columns: 1fr;
      column-gap: 0;
      row-gap: 16px;
    }
  }
  ```
- **Typst 实现**:
  ```typst
  #let la-spec-footnote(
    main-body,
    notes: (),
  ) = {
    grid(
      columns: (1fr, 240pt),
      column-gutter: 32pt,
      // 主内容
      block(width: 100%)[
        #set text(size: 12pt, leading: 1.5em)
        #main-body
      ],
      // 脚注边栏
      block(width: 100%, inset: 16pt, fill: rgb("#f9f9f9"), radius: 8pt)[
        #set text(size: 9pt, fill: rgb("#666666"))
        #for (i, note) in notes.enumerate() {
          [#(i + 1). #note]
          linebreak()
        }
      ]
    )
  }

  // 使用示例
  #la-spec-footnote(
    main-body: [正文内容，包含需要注释的术语],
    notes: ("术语的详细解释和来源说明。",),
  )
  ```
- **与 layout-grid.md 对接规则**: 侧边栏宽度 `240px`（60×4px）对应 layout-grid.md 12 列栅格中 4/12 列宽度。`column-gap: 32px`（8×4px）对齐 `--page-margin-*` 变量。脚注字号 `12px`（3×4px）是 layout-grid.md 表格单元格内边距规范中的最小可读字号。`padding: 16px`（4×4px）对齐 `--grid-gutter` 变量。

---

### LA-SPEC-004: 页眉页脚布局

- **原子 ID**: LA-SPEC-004
- **适用场景**: 文档页眉页脚、报告固定头尾、Web 应用顶部导航 + 底部信息栏
- **HTML+CSS 实现**:
  ```html
  <div class="la-spec-header-footer">
    <header class="la-spec-header">
      <div class="la-spec-header-left">品牌名称</div>
      <nav class="la-spec-header-nav">
        <a href="#">首页</a>
        <a href="#">关于</a>
        <a href="#">联系</a>
      </nav>
    </header>
    <main class="la-spec-main">
      <!-- 页面主体内容 -->
    </main>
    <footer class="la-spec-footer">
      <div class="la-spec-footer-left">© 2026 公司名称</div>
      <div class="la-spec-footer-right">隐私政策 · 服务条款</div>
    </footer>
  </div>
  ```
  ```css
  .la-spec-header-footer {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    box-sizing: border-box;
  }
  .la-spec-header {
    position: sticky;
    top: 0;
    z-index: 100;
    height: 64px;             /* 16×4px，页眉高度 */
    padding: 0 32px;          /* 8×4px */
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #ffffff;
    border-bottom: 1px solid #eeeeee;
    box-sizing: border-box;
  }
  .la-spec-header-left {
    font-size: 20px;          /* 5×4px */
    font-weight: 700;
    color: #1a1a1a;
  }
  .la-spec-header-nav {
    display: flex;
    gap: 24px;                /* 6×4px */
  }
  .la-spec-header-nav a {
    font-size: 14px;
    color: #555555;
    text-decoration: none;
  }
  .la-spec-main {
    flex: 1;
    padding: 32px;            /* 8×4px */
    box-sizing: border-box;
  }
  .la-spec-footer {
    height: 48px;             /* 12×4px，页脚高度 */
    padding: 0 32px;          /* 8×4px */
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #1a1a1a;
    color: #ffffff;
    box-sizing: border-box;
  }
  .la-spec-footer-left,
  .la-spec-footer-right {
    font-size: 12px;          /* 3×4px */
  }
  ```
- **Typst 实现**:
  ```typst
  #let la-spec-header-footer(
    header-left,
    header-nav: (),
    main-body,
    footer-left,
    footer-right,
  ) = {
    set page(
      header: block(width: 100%, height: 64pt, inset: (x: 32pt, y: 0pt))[
        #grid(
          columns: (1fr, 1fr),
          align(left, text(size: 20pt, weight: "bold")[#header-left]),
          align(right,
            grid(
              columns: header-nav.map(n => auto),
              column-gutter: 24pt,
              ..header-nav.map(n => text(size: 14pt, fill: rgb("#555555"))[#n])
            )
          )
        )
        #line(length: 100%, stroke: 0.5pt + rgb("#eeeeee"))
      ],
      footer: block(width: 100%, height: 48pt, fill: rgb("#1a1a1a"), inset: (x: 32pt, y: 0pt))[
        #grid(
          columns: (1fr, 1fr),
          align(left, text(size: 12pt, fill: white)[#footer-left]),
          align(right, text(size: 12pt, fill: white)[#footer-right]),
        )
      ],
      margin: (top: 96pt, bottom: 80pt, left: 32pt, right: 32pt),
    )
    main-body
  }

  // 使用示例
  #la-spec-header-footer(
    header-left: "品牌名称",
    header-nav: ("首页", "关于", "联系"),
    main-body: [页面主体内容],
    footer-left: "© 2026 公司名称",
    footer-right: "隐私政策 · 服务条款",
  )
  ```
- **与 layout-grid.md 对接规则**: 页眉高度 `64px`（16×4px）和页脚高度 `48px`（12×4px）均为 4px 整数倍。`padding: 0 32px`（8×4px）对齐 layout-grid.md `--page-margin-*` 变量。页眉 `position: sticky` 实现固定顶部，不绕过 layout-grid.md 第七章强制规则第 5 条——sticky 定位仍遵循文档流，不使用绝对定位硬编码坐标。页脚字号 `12px`（3×4px）对齐 layout-grid.md 表格单元格内边距规范中的最小字号。

---

## 穷尽重试策略

### 穷尽尝试完整布局原子库
24 个布局原子（6 栅格 + 6 卡片 + 4 页面 + 4 响应式 + 4 特殊）+ HTML+CSS/Typst 双轨实现 + 4px 基准对接

### 布局原子库部分不可用时穷尽尝试简化原子
- 穷尽尝试仅使用 LA-GRID-001（12 列栅格）+ LA-CARD-002（竖版卡片）
- 禁用响应式断点原子
- 使用固定布局原子组合

### 布局原子库不可用时穷尽尝试 layout-grid.md 原生栅格
- 穷尽尝试 layout-grid.md 的 12 列栅格系统
- 无卡片/页面/特殊原子，仅保留栅格
- 标注为穷尽重试布局

### layout-grid.md 不可用时穷尽尝试 Flexbox 布局
- 穷尽尝试 CSS Flexbox 布局
- 无栅格系统，仅保留 flex-direction + gap
- 使用固定边距和间距（均对齐 4px 基准）
- 标注为穷尽重试布局
