<!-- 作者：阿洋 -->

# VMPrint

## 基本信息
- **卡片编号**: #8
- **类型**: TC
- **优先级**: P0
- **层级**: L1

## 功能描述
中文排版引擎，专注于中文学术出版排版规范，支持 GB/T 7714 引用格式、中文页眉页脚、自动目录生成。

## 调用指令

### 输入参数
- `source` (string, 源文件)
- `template` (string, 模板名称)
- `output_format` (string, pdf/html)
- `config` (object, 排版配置)

### 输出格式
PDF/HTML

### 调用示例
```
vmprint.render(source="report.md", template="academic_cn", output_format="pdf", config={"citation_style":"gbt7714","toc_levels":3})
```

## 穷尽重试策略
- **穷尽重试替代路径**: VMPrint → WeasyPrint → HTML
- **触发条件**: VMPrint 渲染失败

## MCP 适配
- **MCP Tool 名称**: vmprint_render
- **MCP 参数**: source, template, output_format, config

## 依赖
- VMPrint 服务部署 + 中文字体

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

暂无显式 DAG 节点消费者。保留待扩展。

