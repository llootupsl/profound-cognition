<!-- 作者：阿洋 -->

# 伦理标准参考文档

> **版本治理元数据 (D12.4.2)**:
> - version: 1.1
> - last_updated: 2026-06-25
> - maintainer: 阿洋
> - changelog:
>   - v1.0 初始版本（IEEE 7000/UNESCO/EU AI Act/GT-HarmBench）
>   - v1.1 补全版本治理元数据与交叉引用（D12.4.2-D12.4.3）

## 交叉引用

- **上游**: `knowledge/cognitive-framework.md`（认知流水线）
- **下游**: `tasks/T24_meta_dim_part1.md`（安全性分析）、`tasks/T26_meta_insight_cross.md`（伦理分析）
- **相关**: `knowledge/sensitivity-framework.md`（敏感度分级）、`knowledge/evidence-standards.md`（证据等级）
- **外部标准**: IEEE 7000-2021、UNESCO AI Ethics、EU AI Act、GT-HarmBench

## P-3 伦理分析参考框架

### IEEE 7000-2021
- 全称: IEEE Standard Model Process for Addressing Ethical Concern During System Design
- 核心内容: 系统设计中的伦理关切处理模型流程
- 适用: T24 Step 9 安全性分析、T26 Step 7 伦理分析
- 获取方式: https://standards.ieee.org/ieee/7000-2021/7080/

### UNESCO AI Ethics Recommendation
- 全称: Recommendation on the Ethics of Artificial Intelligence
- 核心内容: AI 伦理原则（透明性、公平性、问责制、隐私保护）
- 适用: T26 Step 7 伦理分析的五维框架参考
- 获取方式: https://www.unesco.org/en/artificial-intelligence/recommendation-ethics

### EU AI Act
- 全称: Regulation (EU) 2024/1689 (Artificial Intelligence Act)
- 核心内容: AI 系统风险分类、高风险系统要求、禁止实践
- 适用: T24 Step 9 安全性分析的风险分类参考
- 获取方式: https://artificialintelligenceact.eu/

### GT-HarmBench
- 性质: 评估基准数据集（非工具、非API）
- 核心内容: 有害输出模式分类、安全评估基准
- 适用: T24 Step 9 安全性分析 (P-3 伦理 Path A)
- 获取方式: https://harmbench.org/

## 伦理分析五维框架
1. **自主性 (Autonomy)**: 尊重用户/研究对象的自主决策权
2. **善行 (Beneficence)**: 确保研究产出促进福祉
3. **非恶意 (Non-maleficence)**: 避免有害输出和误用风险
4. **公正 (Justice)**: 确保公平性和无歧视
5. **可解释性 (Explainability)**: 确保研究过程和结论可解释

## Path A / Path B 独立性限制
- Path A (T24 GT-HarmBench 评估) 和 Path B (T26 伦理分析) 均依赖同一 LLM
- 独立性有限，不可视为完全独立的伦理审查
- 建议在关键场景下引入人工伦理审查
