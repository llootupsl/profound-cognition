---
name: TC-074-WebWeaver
description: 动态大纲深度研究合成引擎，支持多轮迭代式搜索与综合
version: "1.0"
category: external-tool
consuming_engines: []
integrated_nodes: [T02, I01]
---

<!-- 作者：阿洋 -->


# TC-074: WebWeaver — 动态大纲深度研究合成

## 用途
基于动态大纲生成和迭代深化的研究合成引擎，通过多轮搜索→提取→综合的循环生成结构化研究报告，自动发现知识空白并填补。

## 授权/许可
MIT

## 下载源
https://github.com/user/WebWeaver (待确认官方仓库)

## 集成节点
- **T02 (L1-L2研究)**: 作为研究助手，自动生成研究大纲并迭代收集语义和逻辑层信息
- **I01 (迭代深化)**: 与迭代深化协议协同，WebWeaver在每轮迭代中扩展大纲并补充新发现的知识点

## tool-availability 探测
```bash
# 检测WebWeaver
python -c "import webweaver; print('WebWeaver available')" 2>/dev/null || echo "WebWeaver not installed"
```

## 穷尽重试替代链
若不可用 → 穷尽重试替代为 GPT-Researcher (TC-030) + 手动大纲生成；或穷尽重试替代为 STORM (TC-029)

## 消费关系

### 消费此卡片的领域引擎

暂无显式领域引擎消费者。

### 消费此卡片的 DAG 节点

| 节点 | 用途 |
|------|------|
| T02 | 动态大纲研究合成 |
| T09 | 迭代深化 |

