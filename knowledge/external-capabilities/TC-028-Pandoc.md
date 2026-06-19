<!-- 作者：阿洋 -->

# Pandoc

## 基本信息
- **卡片编号**: #28
- **类型**: TC
- **优先级**: P2
- **层级**: L1

## 功能描述
Pandoc 文档格式转换工具，支持数十种文档格式互转。涵盖 Markdown、HTML、LaTeX、Word(docx)、PDF、EPUB、reStructuredText、Org-mode、Jupyter Notebook 等格式，支持自定义模板、过滤器(Lua/Filters)和引用管理，适用于文档格式迁移、多格式发布、学术写作工作流等场景。

## 调用指令

### 输入参数
- `source` (string, 源文档内容或文件路径)
- `input_format` (string, 输入格式: markdown/html/latex/docx/rst/org 等)
- `output_format` (string, 输出格式: pdf/docx/html/epub/latex 等)

### 输出格式
目标格式文件

### 调用示例
```
pandoc_convert(source="/docs/report.md", input_format="markdown", output_format="pdf")
```

## 穷尽重试策略
- **穷尽重试替代路径**: Pandoc → 手动转换
- **触发条件**: Pandoc 未安装或目标格式不支持

## MCP 适配
- **MCP Tool 名称**: pandoc_convert
- **MCP 参数**: source, input_format, output_format

## 依赖
- Pandoc 命令行工具 + LaTeX 引擎（PDF 输出时需要）

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

暂无显式 DAG 节点消费者。保留待扩展。

