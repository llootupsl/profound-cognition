<!-- 作者：阿洋 -->

# MarkItDown MCP

## 基本信息
- **卡片编号**: #46
- **类型**: TC
- **优先级**: P2
- **层级**: L1

## 功能描述
MarkItDown MCP 适配器，将 MarkItDown 文档格式转换工具封装为 MCP Tool，使其可通过 MCP 协议统一调用。保留 MarkItDown 的全部功能，支持 PDF/DOCX/PPT/XLS 等多种格式转换为 Markdown，同时获得 MCP 生态的标准化调用能力。

## 调用指令

### 输入参数
- 同 MarkItDown（file_path, output_format 等）

### 输出格式
同 MarkItDown（Markdown 文本）

### 调用示例
```
markitdown_mcp_convert.convert(file_path="/data/report.docx")
```

## 穷尽重试策略
- **穷尽重试替代路径**: MarkItDown MCP → MarkItDown 直接调用
- **触发条件**: MCP Server 不可用或协议通信失败

## MCP 适配
- **MCP Tool 名称**: markitdown_mcp_convert
- **MCP 参数**: 同 MarkItDown 参数

## 依赖
- MarkItDown + MCP Server

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

暂无显式 DAG 节点消费者。保留待扩展。

