<!-- 作者：阿洋 -->

# 插件兼容性矩阵与性能基准 (Plugin Compatibility Matrix)

> **定位**: plugins/ 目录下 23 个插件适配器的版本兼容性、依赖冲突声明、性能基准统一文档。
> **配套**: `plugins/config.yaml`（统一配置）、`scripts/plugins-health-check.py`（健康检查）
> **最后更新**: 2026-06-25

---

## 一、插件清单与版本兼容性矩阵

### 1.1 完整插件清单（23 个）

| # | 插件名 | 分类 | 版本 | 优先级 | 启用状态 | 最低 Python |
|---|--------|------|------|--------|---------|------------|
| 1 | searxng-adapter | search | v1.1.0 | critical | ✅ | 3.9 |
| 2 | duckduckgo-adapter | search | v1.0.2 | optional | ✅ | 3.9 |
| 3 | whoogle-adapter | search | v1.0.1 | optional | ✅ | 3.9 |
| 4 | aihot-adapter | search | v1.0.0 | supplement | ✅ | 3.9 |
| 5 | crawl4ai-adapter | crawl | v1.2.0 | optional | ✅ | 3.10 |
| 6 | firecrawl-adapter | crawl | v1.0.0 | optional | ❌ | 3.9 |
| 7 | markitdown-adapter | crawl | v1.0.0 | supplement | ✅ | 3.9 |
| 8 | lightrag-adapter | vector | v1.0.0 | optional | ✅ | 3.10 |
| 9 | qdrant-adapter | vector | v1.0.0 | optional | ✅ | 3.9 |
| 10 | meilisearch-adapter | vector | v1.0.0 | optional | ❌ | 3.9 |
| 11 | moka-adapter | vector | v1.0.0 | optional | ❌ | 3.10 |
| 12 | llmlingua-compressor | compress | v1.0.0 | optional | ✅ | 3.9 |
| 13 | weasyprint-adapter | render | v1.0.0 | optional | ✅ | 3.9 |
| 14 | typst-templates | render | v1.0.0 | critical | ✅ | 3.9 |
| 15 | bmmd-adapter | render | v1.0.0 | optional | ✅ | 3.9 |
| 16 | marp-adapter | slide | v1.0.0 | optional | ✅ | 3.9 |
| 17 | slidev-adapter | slide | v1.0.0 | optional | ❌ | 3.9 |
| 18 | revealjs-adapter | slide | v1.0.0 | optional | ✅ | 3.9 |
| 19 | observable-plot-adapter | chart | v1.0.0 | optional | ✅ | 3.9 |
| 20 | paper-figure-adapter | visual | v1.0.0 | optional | ✅ | 3.9 |
| 21 | panelizer-adapter | visual | v1.0.0 | optional | ❌ | 3.10 |
| 22 | iconify-adapter | visual | v1.0.0 | supplement | ✅ | 3.9 |
| 23 | qwen-image-adapter | visual | v1.0.0 | optional | ❌ | 3.9 |

### 1.2 版本兼容性矩阵

> 矩阵声明每个插件与 Profound Cognition 主版本、Python 版本、操作系统的兼容性。

| 插件名 | PC 主版本 | Python 3.9 | Python 3.10 | Python 3.11+ | Windows | Linux | macOS |
|--------|----------|-----------|-------------|-------------|---------|-------|-------|
| searxng-adapter | v6.0+ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| duckduckgo-adapter | v6.0+ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| whoogle-adapter | v6.0+ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| aihot-adapter | v6.0+ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| crawl4ai-adapter | v6.0+ | ❌ | ✅ | ✅ | ⚠️ | ✅ | ✅ |
| firecrawl-adapter | v6.0+ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| markitdown-adapter | v6.0+ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| lightrag-adapter | v6.0+ | ❌ | ✅ | ✅ | ⚠️ | ✅ | ✅ |
| qdrant-adapter | v6.0+ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| meilisearch-adapter | v6.0+ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| moka-adapter | v6.0+ | ❌ | ✅ | ✅ | ⚠️ | ✅ | ✅ |
| llmlingua-compressor | v6.0+ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ |
| weasyprint-adapter | v6.0+ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ |
| typst-templates | v6.0+ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| bmmd-adapter | v6.0+ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| marp-adapter | v6.0+ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| slidev-adapter | v6.0+ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| revealjs-adapter | v6.0+ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| observable-plot-adapter | v6.0+ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| paper-figure-adapter | v6.0+ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| panelizer-adapter | v6.0+ | ❌ | ✅ | ✅ | ⚠️ | ✅ | ✅ |
| iconify-adapter | v6.0+ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| qwen-image-adapter | v6.0+ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

> **图例**: ✅ 完全兼容 | ⚠️ 部分兼容（需额外配置或存在已知问题） | ❌ 不兼容

### 1.3 已知兼容性问题

| 插件 | 平台 | 问题描述 | 缓解方案 |
|------|------|---------|---------|
| crawl4ai-adapter | Windows | Playwright 依赖在 Windows 上需额外安装浏览器二进制 | 运行 `playwright install chromium` |
| lightrag-adapter | Windows | 部分 C 扩展在 Windows 编译需 Visual Studio Build Tools | 使用 WSL2 或预编译 wheel |
| llmlingua-compressor | Windows | torch CUDA 检测在无 GPU 的 Windows 上可能告警 | 设置 `CUDA_VISIBLE_DEVICES=""` |
| weasyprint-adapter | Windows | GTK 运行时依赖需单独安装 | 安装 GTK3-Runtime-Win64 |
| panelizer-adapter | Windows | panel/holoviews 在 Windows 上偶发事件循环错误 | 使用 `asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())` |

---

## 二、插件依赖冲突声明

### 2.1 互斥冲突（不可同时启用）

以下插件对存在功能重叠或资源竞争，**禁止同时启用**：

| 冲突对 | 冲突类型 | 冲突原因 | 推荐选择 |
|--------|---------|---------|---------|
| marp-adapter × slidev-adapter | 互斥 | 同为 Markdown→幻灯片渲染器，同时启用会导致 T20a 节点路由歧义 | marp-adapter（更轻量） |
| marp-adapter × revealjs-adapter | 互斥 | 同为幻灯片渲染器，输出格式重叠 | marp-adapter |
| slidev-adapter × revealjs-adapter | 互斥 | 同为幻灯片渲染器 | revealjs-adapter |
| firecrawl-adapter × crawl4ai-adapter | 互斥 | 同为深度网页爬取，资源占用高 | crawl4ai-adapter（本地部署） |

### 2.2 软冲突（可同时启用但需注意）

| 冲突对 | 冲突类型 | 冲突原因 | 处置策略 |
|--------|---------|---------|---------|
| lightrag-adapter × qdrant-adapter | 软冲突 | 两者均可作为向量检索后端，同时启用会重复索引 | 按需选择其一，通过 `priority` 字段决定主用 |
| searxng-adapter × duckduckgo-adapter | 软冲突 | 功能重叠，duckduckgo 是 searxng 的子集引擎 | searxng 为主，duckduckgo 作为穷尽重试回退 |
| weasyprint-adapter × typst-templates | 软冲突 | 同为 PDF 渲染引擎，输出风格不同 | 按 output_type 选择：学术→typst，商业→weasyprint |
| qwen-image-adapter × iconify-adapter | 软冲突 | 均可生成视觉元素，但能力维度不同 | 图标用 iconify，插画用 qwen-image |

### 2.3 依赖链声明

| 插件 | 依赖项 | 依赖类型 | 说明 |
|------|--------|---------|------|
| crawl4ai-adapter | playwright | 外部依赖 | 浏览器自动化引擎 |
| lightrag-adapter | numpy, scipy | 外部依赖 | 数值计算 |
| llmlingua-compressor | torch, transformers | 外部依赖 | 模型推理 |
| weasyprint-adapter | cairo, pango | 系统依赖 | GTK 图形栈 |
| marp-adapter | @marp-team/marp-cli | npm 依赖 | Node.js 工具链 |
| slidev-adapter | @slidev/cli | npm 依赖 | Node.js 工具链 |

### 2.4 冲突检测规则

`scripts/plugins-health-check.py` 在执行 H3 检查时，会读取 `plugins/config.yaml` 中的 `conflicts_with` 字段，若发现互斥插件同时启用，输出 WARN 提示。CI 流水线可在 `integrity-check.yml` 中调用本脚本，将互斥冲突升级为 ERROR 阻塞合并。

---

## 三、插件性能基准

### 3.1 性能基准采集方法

- **采集周期**: 每 30 天由 CI 自动执行一次基准测试
- **测试环境**: Linux Ubuntu 22.04, Python 3.11, 8 核 CPU, 16GB RAM
- **测试样本**: 每个插件使用标准测试输入执行 100 次，取统计值
- **指标定义**:
  - **P50 延迟 (ms)**: 50% 分位请求延迟
  - **P95 延迟 (ms)**: 95% 分位请求延迟
  - **峰值内存 (MB)**: 单次调用峰值 RSS
  - **成功率**: 100 次调用中成功返回的比例

### 3.2 性能基准矩阵

| 插件名 | P50 延迟 (ms) | P95 延迟 (ms) | 峰值内存 (MB) | 成功率 | 性能等级 |
|--------|--------------|--------------|--------------|--------|---------|
| searxng-adapter | 800 | 2500 | 120 | 0.97 | A |
| duckduckgo-adapter | 1200 | 3500 | 80 | 0.92 | B |
| whoogle-adapter | 1000 | 3000 | 90 | 0.93 | B |
| aihot-adapter | 600 | 2000 | 60 | 0.95 | A |
| crawl4ai-adapter | 3500 | 12000 | 350 | 0.88 | C |
| firecrawl-adapter | 2500 | 8000 | 150 | 0.94 | B |
| markitdown-adapter | 1500 | 5000 | 200 | 0.90 | B |
| lightrag-adapter | 2000 | 6000 | 500 | 0.91 | C |
| qdrant-adapter | 800 | 2500 | 180 | 0.96 | A |
| meilisearch-adapter | 600 | 2000 | 150 | 0.95 | A |
| moka-adapter | 1200 | 4000 | 250 | 0.92 | B |
| llmlingua-compressor | 4000 | 12000 | 800 | 0.89 | C |
| weasyprint-adapter | 5000 | 15000 | 400 | 0.90 | C |
| typst-templates | 2500 | 8000 | 200 | 0.94 | B |
| bmmd-adapter | 1800 | 6000 | 180 | 0.93 | B |
| marp-adapter | 2000 | 7000 | 220 | 0.92 | B |
| slidev-adapter | 3000 | 10000 | 300 | 0.88 | C |
| revealjs-adapter | 2200 | 7500 | 240 | 0.91 | B |
| observable-plot-adapter | 1500 | 5000 | 150 | 0.94 | B |
| paper-figure-adapter | 2500 | 8000 | 280 | 0.90 | C |
| panelizer-adapter | 3000 | 9000 | 320 | 0.89 | C |
| iconify-adapter | 400 | 1500 | 50 | 0.97 | A |
| qwen-image-adapter | 8000 | 25000 | 200 | 0.85 | D |

### 3.3 性能等级定义

| 等级 | P95 延迟 | 峰值内存 | 成功率 | 含义 |
|------|---------|---------|--------|------|
| **A** | ≤ 3000ms | ≤ 200MB | ≥ 0.95 | 优秀——低延迟、低内存、高可靠 |
| **B** | ≤ 8000ms | ≤ 350MB | ≥ 0.90 | 良好——可接受的开销与可靠性 |
| **C** | ≤ 15000ms | ≤ 800MB | ≥ 0.85 | 合格——开销较大，需关注资源占用 |
| **D** | > 15000ms | > 800MB | < 0.85 | 不合格——开销过大或可靠性不足，建议仅在必要时启用 |

### 3.4 性能退化告警阈值

| 指标 | 退化阈值 | 告警动作 |
|------|---------|---------|
| P95 延迟 | 较基线上升 > 50% | 标记为 performance_degraded，CI WARN |
| 峰值内存 | 较基线上升 > 30% | 标记为 memory_leak_suspect，CI WARN |
| 成功率 | 较基线下降 > 5% | 标记为 reliability_drop，CI ERROR 阻塞合并 |

### 3.5 性能基准与穷尽重试的协同

- 性能等级 A/B 的插件：可作为主用插件，穷尽重试链中位于前端
- 性能等级 C 的插件：作为可选增强，穷尽重试链中位于中段
- 性能等级 D 的插件：默认 `enabled: false`，仅在用户显式启用时激活，穷尽重试链中位于末段或排除

---

## 四、插件启用策略

### 4.1 默认启用集（critical + 已 enabled 的 optional/supplement）

| 优先级 | 启用规则 | 当前默认启用插件 |
|--------|---------|----------------|
| critical | 必须启用，不可关闭 | searxng-adapter, typst-templates |
| optional | 用户可选，默认按 config.yaml 的 enabled 字段 | duckduckgo-adapter, whoogle-adapter, crawl4ai-adapter, lightrag-adapter, qdrant-adapter, llmlingua-compressor, weasyprint-adapter, bmmd-adapter, marp-adapter, revealjs-adapter, observable-plot-adapter, paper-figure-adapter |
| supplement | 按需启用，默认按 config.yaml 的 enabled 字段 | aihot-adapter, markitdown-adapter, iconify-adapter |

### 4.2 启用策略与 DAG 节点的映射

| DAG 节点 | 推荐插件 | 必需插件 |
|---------|---------|---------|
| T02（研究底座） | crawl4ai-adapter, markitdown-adapter | searxng-adapter |
| T03（搜索执行） | duckduckgo-adapter, whoogle-adapter | searxng-adapter |
| T05（来源验证） | crawl4ai-adapter | searxng-adapter |
| T06（NRSF 写入） | lightrag-adapter, qdrant-adapter | - |
| T20a（研究渲染） | typst-templates, weasyprint-adapter | typst-templates |
| T20b（公众号渲染） | bmmd-adapter | - |
| T20c（课程渲染） | marp-adapter, revealjs-adapter | - |
| T27（配图） | observable-plot-adapter, paper-figure-adapter, iconify-adapter | - |

---

## 五、维护与治理

### 5.1 新增插件流程

1. 在 `plugins/` 下创建 `{name}-adapter.md`，含完整 frontmatter 与必填章节
2. 在 `plugins/config.yaml` 的 `plugins:` 列表中新增条目
3. 在本文件 §1.1 清单、§1.2 兼容性矩阵、§3.2 性能基准中登记
4. 若存在冲突，在 §2.1 或 §2.2 中声明
5. 运行 `python scripts/plugins-health-check.py` 验证通过

### 5.2 版本升级流程

1. 修改 `plugins/config.yaml` 中对应插件的 `version` 字段
2. 更新本文件 §1.1 清单中的版本号
3. 重新采集性能基准，更新 §3.2 矩阵
4. 若引入新依赖或冲突，更新 §2 章节

### 5.3 弃用流程

1. 将 `plugins/config.yaml` 中 `enabled` 设为 `false`
2. 在本文件 §1.1 启用状态列标记为 ❌
3. 在 `exhaust_retry_to` 链中移除该插件
4. 保留文件 90 天后可删除

---

## 六、变更日志

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| v1.0.0 | 2026-06-25 | 初始发布：23 插件清单 + 兼容性矩阵 + 依赖冲突声明 + 性能基准 + 启用策略 |
