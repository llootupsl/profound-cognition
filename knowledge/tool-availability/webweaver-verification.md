<!-- 作者：阿洋 -->

# WebWeaver 可用性验证

> **版本治理元数据 (D12.4.2)**:
> - version: 1.1
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（WebWeaver 不可用，采用 STORM + GPT-Researcher 替代）
>   - v1.1 补全版本治理元数据与交叉引用（D12.4.2-D12.4.3）

## 交叉引用

- **上游**: `knowledge/external-capabilities-index.md`（外部能力索引）
- **下游**: 无直接消费（验证结果记录文件）
- **相关**: `knowledge/search-strategy.md`（搜索方法论，STORM/GPT-Researcher 用于搜索）、`knowledge/research-methods.md`（研究方法）
- **替代能力卡**: TC-029-STORM、TC-030-GPT-Researcher（替代 WebWeaver）

## 验证结果
WebWeaver 不可用（未找到可用的 Python 包或 API）

## 替代方案
采用 STORM + GPT-Researcher 作为替代：

### STORM (Stanford)
- 功能: 学术写作辅助、大纲生成、文献综述
- 安装: pip install knowledge-storm
- 状态: ✅ 可用
- 用途: research_master 输出类型的文献综述章节辅助

### GPT-Researcher
- 功能: 深度网络搜索、多源信息聚合
- 安装: pip install gpt-researcher
- 状态: ✅ 可用
- 用途: 补充 T02 研究底座的网络信息搜索

## 决策
采用 STORM + GPT-Researcher 替代 WebWeaver，功能覆盖更全面。
