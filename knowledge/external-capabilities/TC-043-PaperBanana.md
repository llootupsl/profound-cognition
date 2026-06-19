<!-- 作者：阿洋 -->

# PaperBanana

## 基本信息
- **卡片编号**: #43
- **类型**: TC
- **优先级**: P2
- **层级**: L1

## 功能描述
PaperBanana 专有 API 图表生成工具，使用 Nano Banana Pro (Gemini 3 Pro Image) 模型生成高质量学术图表。支持多种图表风格和输出格式，适用于论文插图、数据可视化和学术报告中的专业图表制作。

## 调用指令

### 输入参数
- `description` (string, 图表描述)
- `style` (string, 可选: academic/infographic/minimal, 图表风格，默认 academic)
- `output_format` (string, 可选: png/svg, 输出格式，默认 png)

### 输出格式
高质量图表文件（PNG/SVG）

### 调用示例
```
paperbanana_generate.generate(description="中国GDP增长率折线图 2015-2025", style="academic", output_format="png")
```

## 穷尽重试策略
- **穷尽重试替代路径**: PaperBanana → AutoFigure → Mermaid
- **触发条件**: Google 专有 API 不可用（开源环境不可用）

## MCP 适配
- **MCP Tool 名称**: paperbanana_generate
- **MCP 参数**: description, style, output_format

## 依赖
- Google 专有 API（开源环境不可用）

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

暂无显式 DAG 节点消费者。保留待扩展。

## 方法论内化

> ★核心方法论已内化于 rendering-pipeline/ARCHITECTURE.md，以下为快速参考

### 方法论原理
PaperBanana通过AI自动生成论文图表，解决了研究者图表制作耗时且设计质量不一致的问题。

### 执行步骤
1. 解析论文数据段
2. 识别数据类型(时序/分类/关系)
3. 选择图表类型
4. 生成图表代码
5. 渲染输出

### 决策规则
| 条件 | 动作 |
|------|------|
| 需要自动图表 | PaperBanana |
| 需要精确控制 | AutoFigure |
| 需要简单图 | Mermaid |

### 输出规范
```yaml
paperbanana_output:
  available: bool
  chart_format: str  # png/svg
  chart_type: str
  degradation_note: str
```

### 穷尽重试策略
| 级别 | 方案 |
|------|------|
| L1 | PaperBanana完整AI图表生成 |
| L2 | AutoFigure(代码模板) |
| L3 | Mermaid(简化图) |
| L4 | 文字描述 |

