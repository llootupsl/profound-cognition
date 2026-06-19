<!-- 作者：阿洋 -->

# PubFig

## 基本信息
- **卡片编号**: #24
- **类型**: TC
- **优先级**: P1
- **层级**: L1

## 功能描述
PubFig 出版级图表生成工具，生成符合学术出版规范的图表。支持 IEEE/ACM/Nature/Science 等出版标准，提供精确的字体尺寸、线宽、颜色规范控制，自动生成图注和标签，适用于学术论文插图、会议海报、期刊投稿等场景。

## 调用指令

### 输入参数
- `description` (string, 图表的自然语言描述)
- `data` (object, 可选: 图表数据)
- `style` (string, 可选: 图表风格，如 ieee/acm/nature/science)
- `publication_standard` (string, 出版规范: ieee/acm/nature/science/springer)

### 输出格式
高分辨率 PNG(300dpi)/SVG/PDF

### 调用示例
```
pubfig_generate(description="双柱状图对比实验结果", data={"categories":["Method A","Method B","Method C"],"metric1":[85,92,78],"metric2":[90,88,95]}, style="nature", publication_standard="nature")
```

## 穷尽重试策略
- **穷尽重试替代路径**: PubFig → AutoFigure → Matplotlib
- **触发条件**: PubFig 服务不可用或出版规范不支持

## MCP 适配
- **MCP Tool 名称**: pubfig_generate
- **MCP 参数**: description, data, style, publication_standard

## 依赖
- PubFig 服务部署 + LaTeX 字体 + LLM 推理后端

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

暂无显式 DAG 节点消费者。保留待扩展。

