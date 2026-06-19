<!-- 作者：阿洋 -->

# Panelizer Adapter — TUI 图片排版

## 适配器配置
- role: Panelizer TUI 图片排版工具
- activation: 有配图时的 wechat_article
- description: 在终端中排版图片，支持3:4/4:5/3:2比例模板和Instagram-ready轮播图格式

## 3种比例模板

### 3:4 竖版模板
- 用途：公众号封面图、人物介绍图
- 尺寸：1080×1440px
- 布局：标题在上1/3 + 内容在下2/3

### 4:5 竖版模板
- 用途：Instagram帖子、信息图
- 尺寸：1080×1350px
- 布局：标题在上1/4 + 主体内容在中2/4 + 落款在下1/4

### 3:2 横版模板
- 用途：公众号头图、横幅图
- 尺寸：900×600px
- 布局：左图右文 / 左文右图

## Instagram-ready 轮播图格式
- 尺寸：1080×1080px（正方形）
- 格式：PNG（无损压缩）
- 轮播：最多10张
- 排列：导航图+内容图+总结图

---

## 激活条件

```yaml
activation:
  condition: "output_type == 'wechat_article' AND 有配图需求"
  priority: "首选公众号图片排版引擎 — 3种比例模板+Instagram轮播"
  exhaust-retry: "若 Panelizer 不可用，穷尽尝试到 Moka 卡片排版 → 纯HTML内联样式"
```

---

## 模板选择策略规则

```yaml
template_selection:
  rule_1_cover_image:
    trigger: "公众号封面图/人物介绍"
    template: "3:4 竖版模板"
    size: "1080x1440px"
    layout: "标题在上1/3 + 内容在下2/3"
    reason: "封面图需要竖版高冲击力布局"

  rule_2_infographic:
    trigger: "信息图/Instagram帖子"
    template: "4:5 竖版模板"
    size: "1080x1350px"
    layout: "标题在上1/4 + 主体内容在中2/4 + 落款在下1/4"
    reason: "信息图需要均衡的内容分布"

  rule_3_banner:
    trigger: "公众号头图/横幅图"
    template: "3:2 横版模板"
    size: "900x600px"
    layout: "左图右文 / 左文右图"
    reason: "横幅图需要横向布局"

  rule_4_carousel:
    trigger: "Instagram轮播/多图系列"
    template: "Instagram-ready 轮播图格式"
    size: "1080x1080px"
    max_slides: 10
    layout: "导航图+内容图+总结图"
    reason: "轮播需要正方形统一格式"
```

---

## 与 profound-cognition Task 节点集成

```yaml
task_integration:
  T20_output_rendering:
    trigger: "输出渲染 — wechat_article 配图排版"
    strategy: "按模板选择策略规则选择模板"
    output: "排版图片嵌入 T20 渲染输出"
    annotation: "[panelizer] 标签标记图片排版"

  T13_cog_synthesize:
    trigger: "认知综合 — 可视化卡片生成"
    strategy: "rule_2_infographic"
    output: "信息图卡片注入综合分析"
    annotation: "[panelizer-infographic] 标签标记信息图"
```

---

## 错误处理

```yaml
error_handling:
  tool_not_available:
    action: "穷尽重试到 Moka 卡片排版"
    log: "记录 Panelizer 不可用事件"

  image_too_large:
    action: "自动压缩到模板尺寸"
    log: "记录图片过大事件"

  template_not_found:
    action: "使用默认3:4竖版模板"
    log: "记录模板未找到事件"

  render_failure:
    action: "穷尽重试到纯HTML内联样式排版"
    log: "记录渲染失败事件"
```

---

## 穷尽重试策略

```yaml
exhaust_retry:
  L1_FULL:
    condition: "Panelizer 可用"
    behavior: "完整3种比例模板 + Instagram轮播格式"

  L2_PARTIAL_DATA:
    condition: "Panelizer 可用但部分模板异常"
    behavior: "可用模板排版 + 标注[PARTIAL-TEMPLATE]"

  L3_TEXT_ONLY:
    condition: "Panelizer 不可用"
    behavior: "穷尽尝试到 Moka 卡片排版 + 标注[MOKA-INTERNAL_REASONING]"

  L4_SERVICE_DOWN:
    condition: "所有图片排版工具不可用"
    behavior: "纯HTML内联样式 + 标注[HTML-ONLY]"
```
