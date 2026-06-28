<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（能力卡补全版本治理元数据，D12.4.2）

# Tectonic

## 基本信息
- **卡片编号**: #12
- **类型**: TC
- **优先级**: P1
- **层级**: L1

## 功能描述
Tectonic LaTeX 编译引擎，自包含的 LaTeX 编译器，无需系统级 TeX 发行版安装。自动下载所需宏包，支持 XeTeX 后端，适用于学术论文和报告的 LaTeX 编译场景。

## 调用指令

### 输入参数
- `source_tex` (string, LaTeX 源码或 .tex 文件路径)
- `output_format` (string, 输出格式: pdf，默认 pdf)

### 输出格式
PDF

### 调用示例
```
tectonic.compile(source_tex="/output/research_master.tex", output_format="pdf")
```

## 穷尽重试策略
- **穷尽重试替代路径**: Tectonic → LuaTeX-CN → Typst
- **触发条件**: Tectonic 编译失败或二进制不可用

## MCP 适配
- **MCP Tool 名称**: tectonic_compile
- **MCP 参数**: source_tex, output_format

## 依赖
- Tectonic 二进制安装（自包含，无需 TeX Live）

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

暂无显式 DAG 节点消费者。保留待扩展。


## 效果度量

| 度量指标 | 定义 | 目标值 |
|----------|------|--------|
| 执行成功率 | 成功调用次数 / 总调用次数 | ≥ 0.95 |
| 平均延迟 | 单次调用平均耗时 | ≤ 5s |
| 输出质量分 | Supervisor 评分（0-1） | ≥ 0.8 |
| 穷尽重试触发率 | 触发降级的调用次数 / 总调用次数 | ≤ 0.1 |

效果度量写入 NRSF，供 T19 质量检查消费。