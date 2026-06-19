<!-- 作者：阿洋 -->

# MarkItDown

## 基本信息

> ★核心方法论已内化于 knowledge/search-strategy.md，本文件仅作快速引用入口

- **卡片编号**: #4
- **类型**: TC
- **优先级**: P0
- **层级**: L1

## 功能描述
文档格式转换工具，支持 PDF/DOCX/PPTX/XLSX → Markdown 转换，保留结构和格式

## 调用指令

### 输入参数
- `file_path` (string, 文件路径或 URL)
- `output_format` (string, 默认 markdown)
- `preserve_images` (boolean, 默认 true)

### 输出格式
Markdown（保留标题层级、表格、列表）

### 调用示例
```
markitdown.convert(file_path="report.pdf", output_format="markdown", preserve_images=true)
```

## 穷尽重试策略
- **穷尽重试替代路径**: MarkItDown → pandoc → 手动解析
- **触发条件**: MarkItDown 转换失败

## MCP 适配
- **MCP Tool 名称**: markitdown_convert
- **MCP 参数**: file_path, output_format, preserve_images

## 依赖
- MarkItDown 库安装

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

暂无显式 DAG 节点消费者。保留待扩展。

