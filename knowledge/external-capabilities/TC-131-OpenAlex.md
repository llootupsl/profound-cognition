<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-27
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（Audit-7 Stage 2 补建，对应 v5.1.0 报告推荐项）

# TC-131: OpenAlex API — 开放学术元数据 API

## 基本信息
- **名称**: OpenAlex API
- **类别**: 开放学术元数据 API
- **语言**: Python（REST API）
- **版本要求**: >=1.0
- **许可证**: CC0
- **仓库**: https://github.com/ourresearch/openalex-api-tutorial
- **维护方**: OurResearch

## 核心能力
- 开放学术元数据检索（Works / Authors / Institutions / Concepts / Funders / Sources / Publishers / Topics）
- 跨实体关系遍历（works-authors-institutions-concepts-funders 多跳）
- 大规模学术图谱查询（≥2.5 亿 Works，全开放 CC0）
- 引用网络与影响力指标（cited_by_count / i10-index / h-index）

## 在 profound-cognition 中的用途
- **T02 研究底座**: T02 研究底座补充检索源；当前使用 PaperQA2 + Semantic Scholar API + OpenAlex API 组合，OpenAlex API 作为机构/概念/资助维度的补充元数据入口待激活
- **状态**: 待激活
- **对应 v5.1.0 报告项**: 第四章 4.3.12 节

## 消费节点
- T02 研究底座（待激活）

## 调用前置条件

- Python 3.9+ 运行环境（如需代码执行）
- 对应工具库已安装（详见「基本信息」字段）
- 网络连接可用（如需远程 API 或数据源）
- 上游节点产出已就绪（根据消费节点依赖关系）

## 失败回退策略

- **触发条件**: 工具不可用、调用超时、输出质量不达标、依赖缺失
- **回退路径**: 降级到 LLM 内建能力，标注 [INTERNAL_REASONING]
- **回退声明**: 回退后失去工具增强能力，但保证流程不中断（EXHAUST 铁律）
- **穷尽重试**: 按 L1_FULL → L2_PARTIAL → L3_TEXT_ONLY → L4_SERVICE_DOWN 逐级降级

## 效果度量

| 度量指标 | 定义 | 目标值 |
|----------|------|--------|
| 执行成功率 | 成功调用次数 / 总调用次数 | >= 0.95 |
| 平均延迟 | 单次调用平均耗时 | <= 5s |
| 输出质量分 | Supervisor 评分（0-1） | >= 0.8 |
| 穷尽重试触发率 | 触发降级的调用次数 / 总调用次数 | <= 0.1 |

## 替代关系
- **可被替代为**: Semantic Scholar API（TC-130）+ Crossref API 组合
- **替代说明**: 见 v5.1.0 报告第四章 4.3.12 节融入方案

## Audit-7 Stage 2 备注
- **核验状态**: ❌缺失 → ✅已补建（Audit-7 Stage 2）
- **对应 v5.1.0 报告项**: 4.3.12
- **核验日期**: 2026-06-27
- **审计员**: 独立审计子代理（Audit-7）
