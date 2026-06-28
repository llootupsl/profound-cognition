<!-- 作者：阿洋 -->

# 动效语义匹配规则 (Motion Semantic Match Rules)

> **定位**: 渲染管道的动效引擎，根据内容语义自动匹配动效类型，确保动效服务于内容表达而非装饰。
> **强制规则**: 动效时长和缓动曲线全局统一，不随内容类型变化。

---

## 一、语义 → 动效匹配表

### 1.1 结论 → 高亮动效

**触发条件**: 段落包含结论性、总结性、关键性陈述。

| 触发关键词 | 动效类型 | 动效参数 |
|-----------|---------|---------|
| `(总之\|综上所述\|结论\|核心发现\|关键洞察\|归根结底)` | fadeIn + scale | opacity 0→1, scale 0.95→1.0, duration 800ms, easing ease-out |
| `(重要\|关键\|核心\|本质\|根本)` | glowPulse (发光脉冲) | box-shadow 0→8px→0, duration 1200ms, easing ease-in-out, loop 1 |
| `(值得注意的是\|尤其\|特别\|尤为)` | highlightBG (背景高亮) | background-color 透明→淡黄→透明, duration 1500ms, easing ease-in-out |

### 1.2 流程 → 动线动效

**触发条件**: 段落包含步骤、流程、时序描述。

| 触发关键词 | 动效类型 | 动效参数 |
|-----------|---------|---------|
| 步骤序号/时序词 | staggerFadeIn (逐项淡入) | stagger 150ms/item, opacity 0→1, translateY 10px→0, duration 400ms/item |
| 箭头/流向/传递 | motionPath (路径动画) | SVG path 描边动画, stroke-dashoffset 100%→0, duration 1000ms |
| 循环/反馈/闭环 | rotateLoop (循环旋转) | SVG 循环路径, rotation 0→360°, duration 3000ms, infinite |

### 1.3 数据 → 递进动效

**触发条件**: 段落包含数值、统计、变化趋势描述。

| 触发关键词 | 动效类型 | 动效参数 |
|-----------|---------|---------|
| 数值/百分比/增长 | countUp (数字递增) | 从 0 递增至目标值, duration 1500ms, easing ease-out, 千分位格式化 |
| 排名/对比 | stagger + countUp | 逐项数字递增, stagger 200ms, 每项 duration 1000ms |
| 趋势/变化 | barGrow (柱状图生长) | height 0→目标值, duration 1000ms, easing ease-out, stagger 150ms |
| 占比/分布 | pieReveal (饼图展开) | SVG 扇形角度 0→目标值, duration 1200ms, easing ease-out |

### 1.4 概念 → 揭示动效

**触发条件**: 段落包含概念定义、分类、层级关系。

| 触发关键词 | 动效类型 | 动效参数 |
|-----------|---------|---------|
| 定义/是指 | fadeIn + slideUp (淡入上滑) | opacity 0→1, translateY 20px→0, duration 600ms, easing ease-out |
| 分类/包含 | staggerReveal (逐项揭示) | stagger 200ms, opacity 0→1, scale 0.9→1.0, duration 500ms/item |
| 层级/层次 | cascadeReveal (层级展开) | 父→子逐层, 每层 delay 300ms, duration 500ms/层 |

---

## 二、动效时长规范表

### 2.1 全局统一时长

| 动效级别 | 时长范围 | 典型值 | 适用场景 |
|---------|---------|--------|---------|
| 微动效 (Micro) | 300-500ms | 400ms | 悬停反馈、图标切换、颜色过渡、聚焦态 |
| 标准动效 (Standard) | 600-1000ms | 800ms | 元素入场、卡片展开、段落切换、图表渲染 |
| 大型动效 (Macro) | 1000-2000ms | 1500ms | 页面转场、全屏动画、滚动叙事、封面动画 |

### 2.2 时长使用约束

| 约束项 | 规则 |
|--------|------|
| 同一页面内动效数量 | ≤ 5 个同时播放的动效 |
| 入场动效总时长 | ≤ 3000ms（所有入场动效串联完成） |
| 循环动效 | 仅限 1 个循环动效同时存在，避免视觉污染 |
| 数据动效 | 图表类动效仅首次渲染时播放，刷新不重播 |

---

## 三、缓动曲线全局统一

### 3.1 标准缓动曲线（全局统一）

| 缓动名称 | CSS easing | cubic-bezier | 使用场景 | 不可变 |
|---------|-----------|-------------|---------|--------|
| **入场缓动** | ease-out | `cubic-bezier(0.25, 0.1, 0.25, 1.0)` | 所有元素入场动画（fadeIn, slideUp, scale, stagger 等） | ✓ |
| **循环缓动** | ease-in-out | `cubic-bezier(0.42, 0.0, 0.58, 1.0)` | 所有循环/往复动画（pulse, rotate, breathe 等） | ✓ |
| **出场缓动** | ease-in | `cubic-bezier(0.42, 0.0, 1.0, 1.0)` | 所有元素出场动画（fadeOut, slideDown 等） | ✓ |

### 3.2 缓动曲线不可变规则

```
入场 ≠ 循环 ≠ 出场（三者缓动曲线不同，但各自全局统一）

入场:  cubic-bezier(0.25, 0.1, 0.25, 1.0)  ← 永远不变
循环:  cubic-bezier(0.42, 0.0, 0.58, 1.0)   ← 永远不变
出场:  cubic-bezier(0.42, 0.0, 1.0, 1.0)    ← 永远不变
```

---

## 四、动效 CSS 实现参考

### 4.1 入场动效（ease-out）

```css
/* 淡入 + 缩放 */
@keyframes fadeInScale {
  from { opacity: 0; transform: scale(0.95); }
  to   { opacity: 1; transform: scale(1.0); }
}
.animate-fade-in-scale {
  animation: fadeInScale 800ms cubic-bezier(0.25, 0.1, 0.25, 1.0) both;
}

/* 淡入 + 上滑 */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
.animate-fade-in-up {
  animation: fadeInUp 600ms cubic-bezier(0.25, 0.1, 0.25, 1.0) both;
}

/* 逐项淡入 */
.stagger-fade-in > * {
  opacity: 0;
  animation: fadeInUp 400ms cubic-bezier(0.25, 0.1, 0.25, 1.0) forwards;
}
.stagger-fade-in > *:nth-child(1) { animation-delay: 0ms; }
.stagger-fade-in > *:nth-child(2) { animation-delay: 150ms; }
.stagger-fade-in > *:nth-child(3) { animation-delay: 300ms; }
.stagger-fade-in > *:nth-child(4) { animation-delay: 450ms; }
.stagger-fade-in > *:nth-child(5) { animation-delay: 600ms; }
```

### 4.2 循环动效（ease-in-out）

```css
/* 脉冲 */
@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50%      { transform: scale(1.05); }
}
.animate-pulse {
  animation: pulse 2000ms cubic-bezier(0.42, 0.0, 0.58, 1.0) infinite;
}

/* 发光脉冲 */
@keyframes glowPulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(26, 86, 219, 0.4); }
  50%      { box-shadow: 0 0 0 8px rgba(26, 86, 219, 0); }
}
.animate-glow-pulse {
  animation: glowPulse 2000ms cubic-bezier(0.42, 0.0, 0.58, 1.0) 1;
}
```

### 4.3 数据动效（countUp）

```css
/* 数字递增 - CSS 无法直接实现，需 JS 辅助 */
/* 参考实现: 使用 requestAnimationFrame 逐帧插值 */
```

```javascript
// countUp 数字递增 JS 实现
function countUp(el, target, duration = 1500) {
  const start = 0;
  const startTime = performance.now();
  function update(now) {
    const elapsed = now - startTime;
    const progress = Math.min(elapsed / duration, 1);
    // ease-out cubic-bezier(0.25, 0.1, 0.25, 1.0) 近似
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = Math.round(start + (target - start) * eased);
    el.textContent = current.toLocaleString();
    if (progress < 1) requestAnimationFrame(update);
  }
  requestAnimationFrame(update);
}
```

### 4.4 SVG 描边动画（motionPath）

```css
/* SVG 路径描边动画 */
.animate-draw-svg {
  stroke-dasharray: var(--path-length);
  stroke-dashoffset: var(--path-length);
  animation: drawPath 1000ms cubic-bezier(0.25, 0.1, 0.25, 1.0) forwards;
}
@keyframes drawPath {
  to { stroke-dashoffset: 0; }
}
```

---

## 五、动效禁用与穷尽重试

### 5.1 禁用条件

| 条件 | 行为 |
|------|------|
| `prefers-reduced-motion: reduce` | 所有动效禁用，元素直接显示最终状态 |
| 打印模式 (`@media print`) | 所有动效禁用 |
| 低性能设备 (CPU ≤ 2 核) | 仅保留 fadeIn，禁用复杂动效（motionPath, countUp, stagger） |
| 静态输出（PDF/DOCX） | 所有动效穷尽重试为静态样式（如用静态颜色替代 glowPulse） |

### 5.2 穷尽重试 CSS

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

@media print {
  .animate-fade-in-scale,
  .animate-fade-in-up,
  .animate-pulse,
  .animate-glow-pulse,
  .animate-draw-svg {
    animation: none !important;
    opacity: 1 !important;
    transform: none !important;
  }
}
```

---

## 六、强制规则

1. **缓动曲线全局统一**: 入场 `cubic-bezier(0.25, 0.1, 0.25, 1.0)`、循环 `cubic-bezier(0.42, 0.0, 0.58, 1.0)`、出场 `cubic-bezier(0.42, 0.0, 1.0, 1.0)` — 永远不变，不随内容类型变化。
2. **动效时长全局统一**: 微动效 300-500ms、标准动效 600-1000ms、大型动效 1000-2000ms — 不随内容类型变化。
3. **语义驱动**: 动效类型由内容语义自动匹配，不是设计师手动选择，确保一致性。
4. **无障碍优先**: 检测到 `prefers-reduced-motion` 时必须禁用所有动效。
5. **静态输出穷尽重试**: 非交互式输出（PDF/Print）中动效必须穷尽重试为静态样式，不影响信息传达。
6. **动效不抢内容**: 动效服务于内容表达，不因动效华丽而分散读者注意力。同一页面内同时播放的动效不超过 5 个。
---

## 七、LC-037 Animotion-MCP 动效库设计方法论

### 7.1 方法论原理
Animotion MCP Skill 是渲染管道的 CSS 动效库引擎，采用预构建动画+图标库范式——提供 745+ 预构建 CSS 动画和 9500+ 图标，通过 MCP 协议直接调用。其核心设计原理是动画即数据——每个动画被建模为可参数化的数据对象（名称、时长、缓动、迭代次数），而非代码片段。Animotion-MCP 不生成自定义动画代码，而是从预构建库中匹配最合适的动画，确保动画质量的一致性和可预测性。与 GSAP（自定义时间线编排）和 vibe-motion（预调校动效包）形成三级动效体系：Animotion-MCP 负责标准 CSS 动画，vibe-motion 负责预调校组合动效，GSAP 负责精确时间线控制。

### 7.2 执行步骤
1. 语义匹配：从 motion-semantic-match 规则表获取目标动效类型（fadeIn/slideUp/glowPulse等）
2. 动画检索：在 745+ 动画库中检索匹配的 CSS 动画
3. 参数注入：从 visual_dna.motion_profile 注入时长和缓动参数
4. 配色注入：从 visual_dna.color_scheme 注入颜色参数
5. 图标匹配：如需图标增强，从 9500+ 图标库中检索语义图标
6. CSS 输出：生成标准 CSS @keyframes + class 定义

### 7.3 决策规则
- 需要 745+ 预构建 CSS 动画 -> Animotion-MCP
- 需要预调校组合动效包 -> vibe-motion
- 需要精确时间线编排 -> GSAP
- 需要 9500+ 图标 -> Animotion-MCP
- 需要自定义贝塞尔曲线 -> GSAP

### 7.4 输出规范
animation_name: string; duration: ms; easing: string; iterations: int; icon_used: string|null; visual_dna_compliance: FULL|PARTIAL

### 7.5 穷尽重试策略
- Animotion-MCP -> vibe-motion：预构建动画不满足需求
- vibe-motion -> GSAP：预调校包不满足需求
- GSAP -> CSS Animation：GSAP 环境不可用
- CSS Animation -> 静态样式：prefers-reduced-motion 或打印模式

> 知识来源: LC-037 Animotion-MCP
