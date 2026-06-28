<!-- 作者：阿洋 -->


> **版本治理元数据 (D12.4.2)**:
> - version: 1.0
> - last_updated: 2026-06-27
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（Wave 4 Step 4 补建，对应 v5.1.0 报告第四章 4.4.7 项）

# TC-120: scholarly — 学术搜索

## 基本信息
- **名称**: scholarly
- **类别**: 学术搜索
- **语言**: Python
- **版本要求**: >=0.1
- **许可证**: Unlicense
- **仓库**: https://github.com/scholarly-org/scholarly
- **维护方**: scholarly-org

## 核心能力
- Google Scholar 爬虫（无需 API key）
- 支持作者/关键词/引用检索
- 自动代理轮换

## 在 profound-cognition 中的用途
- **Google Scholar 爬虫**: 学术搜索辅助；当前 T02 使用 Semantic Scholar API + OpenAlex API，scholarly 作为 Google Scholar 爬虫备选待激活（注意：库内 'google_scholar' 10 处命中全部为 SearXNG 引擎参数引用，非 scholarly 库集成）
- **状态**: 待激活

## 消费节点
- Google Scholar 爬虫（待激活）

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
- **可被替代为**: Semantic Scholar API + OpenAlex API 组合
- **替代说明**: 见 v5.1.0 报告第四章 4.4.7 节融入方案

## Audit-6 Wave 4 备注
- **核验状态**: ❌缺失 → ✅已补建（Wave 4 Step 4 - W4-F1）
- **对应 v5.1.0 报告项**: 4.4.7
- **核验日期**: 2026-06-27
- **审计员**: 独立审计子代理（Audit-6）
