> **作者**: 阿洋

# Markmap 思维导图生成规范

> **模块标识**: `output/mindmap-renderer`
> **职责**: 将结构化大纲和研究结论转换为交互式思维导图，使用 Markmap（Markdown → 思维导图）实现零配置渲染
> **CLI 命令**: `npx markmap-cli input.md -o output.html`
> **依赖**: 无

---

## 一、Markmap 基础

### 1.1 原理

Markmap 将 Markdown 的层级结构（`#` / `##` / `###` / `-` 缩进列表）转换为可交互的思维导图，支持缩放、折叠、展开。

```
Markdown 层级文本
  ↓ markmap 解析
  ↓
交互式 SVG/HTML 思维导图
```

### 1.2 输入格式

Markmap 的输入就是标准的 Markdown 文件，层级关系由标题级别和列表缩进决定：

```markdown
# 根节点
## 一级分支 A
- 叶子节点 A1
- 叶子节点 A2
## 一级分支 B
- 叶子节点 B1
  - 子节点 B1a
  - 子节点 B1b
- 叶子节点 B2
## 一级分支 C
```

### 1.3 渲染方式

```bash
# CLI 生成交互式 HTML
npx markmap-cli mindmap.md --output mindmap.html

# 在浏览器中打开
open mindmap.html

# 生成离线包（含依赖）
npx markmap-cli mindmap.md --output mindmap.html --no-open
```

---

## 二、标准思维导图模板

### 2.1 研究报告大纲导图

```markdown
---
title: 深度研究 — 思维导图
markmap:
  colorFreezeLevel: 2
  maxWidth: 300
  initialExpandLevel: 2
---

# [研究主题]

## 背景与问题
- 核心问题定义
- 研究动机
- 已有研究局限
- 本研究定位

## 研究方法
- 研究设计
  - 定性分析
  - 定量分析
- 数据来源
  - 一手数据
  - 二手数据
- 分析框架
  - L1 基础事实层
  - L2 时间演化层
  - L3 结构变量层

## 关键发现
- 发现一：...
  - 证据 A
  - 证据 B
- 发现二：...
  - 证据 C
- 发现三：...

## 结论与建议
- 主要结论
- 行动建议
- 未来展望
```

### 2.2 认知层级导图（L1-L9 框架）

```markdown
---
title: 九层认知框架
markmap:
  colorFreezeLevel: 1
  maxWidth: 280
---

# 九层深度认知

## L1 基础事实
- 已确认事实
- 可验证数据
- 公开信息

## L2 时间演化
- 历史脉络
- 关键转折点
- 趋势方向

## L3 结构变量
- 核心驱动力
- 交互矩阵
- 反馈循环

## L4 比较参照
- 同类案例
- 异业参照
- 国际视角

## L5 感受叙事
- 参与者视角
- 情绪温度
- 文化语境

## L6 证据边界
- 证据等级
- 可信度评估
- 不确定性

## L7 利益相关者
- 各方立场
- 利益冲突
- 权力地图

## L8 反事实
- "如果...会怎样"
- 替代路径
- 关键节点模拟

## L9 知识边界
- 已知未知
- 未知未知
- 研究限制
```

---

## 三、Markmap 配置选项

### 3.1 YAML Frontmatter 配置

```yaml
---
markmap:
  colorFreezeLevel: 2          # 冻结颜色的层级深度
  maxWidth: 300                # 节点最大宽度（px）
  initialExpandLevel: 2        # 初始展开层级（-1 为全部展开）
  duration: 500                # 动画持续时间（ms）
  extraJs: []                  # 额外 JS
  extraCss: []                 # 额外 CSS
  zoom: true                   # 是否启用缩放
  pan: true                    # 是否启用平移
  fitRatio: 0.95               # 适应比例
  nodeMinHeight: 16            # 节点最小高度
  spacingVertical: 10          # 垂直间距
  spacingHorizontal: 80        # 水平间距
  autoFit: true                # 自动适应容器
  color: d3.schemeCategory10   # 颜色方案
---
```

### 3.2 节点内联样式

```markdown
# 根节点 <!-- markmap: foldAll -->
## 默认展开的分支
- 这是一个普通节点
- <span style="color: red;">红色节点</span>
- **加粗节点**
- *斜体节点*
- `代码节点`
```

---

## 四、高级用法

### 4.1 自定义颜色方案

```yaml
---
markmap:
  colorFreezeLevel: 3
  color:
    - "#2196F3"
    - "#4CAF50"
    - "#FF9800"
    - "#9C27B0"
    - "#F44336"
    - "#00BCD4"
    - "#FFEB3B"
    - "#795548"
---
```

### 4.2 嵌入已有页面

```html
<div id="mindmap-container" style="width: 100%; height: 600px;"></div>

<script src="https://cdn.jsdelivr.net/npm/markmap-autoloader"></script>
<script>
  const { markmap } = window;
  const { Markmap, loadCSS, loadJS, Transformer } = markmap;

  const transformer = new Transformer();
  const markdown = `
# 思维导图
## 分支 A
- 叶节点 1
- 叶节点 2
## 分支 B
`;

  const { root } = transformer.transform(markdown);
  const mm = Markmap.create('#mindmap-container', null, root);
</script>
```

### 4.3 在 HTML 报告中内嵌思维导图

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>研究报告 — 思维导图</title>
  <style>
    #mindmap { width: 100%; height: 100vh; }
  </style>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/markmap-toolbar/dist/style.css">
</head>
<body>
  <div id="mindmap"></div>

  <script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
  <script src="https://cdn.jsdelivr.net/npm/markmap-view"></script>
  <script src="https://cdn.jsdelivr.net/npm/markmap-toolbar"></script>
  <script>
    (async () => {
      const { Transformer } = window.markmap;
      const { Markmap, loadCSS, loadJS } = window.markmap;

      const markdown = await fetch('./mindmap.md').then(r => r.text());
      const { root, features } = new Transformer().transform(markdown);

      const { el } = Markmap.create('#mindmap', {
        autoFit: true,
        colorFreezeLevel: 2,
        maxWidth: 280,
        initialExpandLevel: 2,
      }, root);

      window.mm = Markmap;
    })();
  </script>
</body>
</html>
```

### 4.4 动态更新导图

```javascript
const mm = Markmap.create('#mindmap', options, root);

// 切换全部展开/折叠
mm.toggleAll();

// 展开到指定层级
mm.expandDepth(3);

// 缩放到适应
mm.fit();

// 更新数据
const { root: newRoot } = transformer.transform(newMarkdown);
mm.setData(newRoot);
```

---

## 五、质量检查清单

### 5.1 结构检查

- [ ] 只有一个根节点（`#` 一级标题）
- [ ] 分支数量合理（一级分支不超过 7 个）
- [ ] 层级深度不超过 5 层（避免过于深嵌套）
- [ ] 叶子节点名称简洁（不超过 30 字）
- [ ] 同级节点逻辑并列

### 5.2 视觉检查

- [ ] 颜色方案与文档主题协调
- [ ] 节点文字大小适中
- [ ] 间距合理，无重叠
- [ ] 缩放和平移功能正常
- [ ] 折叠/展开动画流畅

### 5.3 内容检查

- [ ] 与研究报告结论一致
- [ ] 关键发现全部呈现
- [ ] 逻辑链路完整
- [ ] 无遗漏关键节点

---

## 穷尽尝试输出规范

当 Markmap 环境不可用时，穷尽尝试 **Markdown 结构化文本**，保留全部信息层级。

### 穷尽尝试触发条件

1. Node.js 环境不可用（无法运行 `npx markmap-cli`）
2. 浏览器环境无法加载 CDN 资源
3. 目标输出为纯文本格式

### 穷尽尝试模板

```markdown
# [研究主题] — 思维导图（文本版）

## 一、背景与问题
- 核心问题定义
- 研究动机
- 已有研究局限
- 本研究定位

## 二、研究方法
- 研究设计
  - 定性分析
  - 定量分析
- 数据来源
  - 一手数据
  - 二手数据

## 三、关键发现
- 发现一：...
- 发现二：...
- 发现三：...

## 四、结论与建议
- 主要结论
- 行动建议
- 未来展望
```

### 穷尽尝试质量要求

- 层级结构通过标题级别（`#` → `##` → `###`）和列表缩进表达
- 同级节点数量保持一致
- 叶子节点信息完整
- 保留全部逻辑链路


---
© 阿洋