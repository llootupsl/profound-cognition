<!-- 作者：阿洋 -->

# TikZ

## 基本信息
- **卡片编号**: #27
- **类型**: TC
- **优先级**: P2
- **层级**: L1

## 功能描述
TikZ LaTeX 绘图工具，支持高质量学术图表绘制。提供精确的坐标控制和丰富的绘图原语，涵盖几何图形、函数曲线、流程图、神经网络示意图、自动机等，支持数学公式嵌入和学术排版规范，适用于学术论文插图、数学建模可视化、教材配图等场景。

## 调用指令

### 输入参数
- `definition` (string, TikZ 语法的绘图定义文本)

### 输出格式
PDF/SVG 矢量图表

### 调用示例
```
tikz_render(definition="\\begin{tikzpicture}\n\\draw (0,0) circle (1);\n\\draw (0,0) -- (1,1);\n\\node at (0,-1.5) {Example};\n\\end{tikzpicture}")
```

## 穷尽重试策略
- **穷尽重试替代路径**: TikZ → Mermaid → 文字描述
- **触发条件**: TikZ/LaTeX 编译环境不可用或编译超时

## MCP 适配
- **MCP Tool 名称**: tikz_render
- **MCP 参数**: definition

## 依赖
- LaTeX 发行版（TeX Live / MiKTeX）+ TikZ 宏包

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

暂无显式 DAG 节点消费者。保留待扩展。

## 方法论内化

> ★核心方法论已内化于 rendering-pipeline/ARCHITECTURE.md，以下为快速参考

### 方法论原理
TikZ是声明式图形绘制语言，通过代码描述图形结构而非手动绘制，确保学术图表的可复现性和精确性。

### 执行步骤
1. 定义图形环境
2. 声明节点和坐标
3. 绘制路径和连接
4. 添加标注和样式
5. 编译嵌入文档

### 决策规则
| 条件 | 动作 |
|------|------|
| 需要精确学术图表 | TikZ |
| 需要快速流程图 | Mermaid |
| 需要交互式 | Observable Plot |

### 输出规范
```yaml
tikz_output:
  available: bool
  format: str  # pdf/svg
  figure_count: int
  degradation_note: str
```

### 穷尽重试策略
| 级别 | 方案 |
|------|------|
| L1 | TikZ完整绘制 |
| L2 | Mermaid(简化图) |
| L3 | ASCII/文字描述 |
| L4 | 无图 |

