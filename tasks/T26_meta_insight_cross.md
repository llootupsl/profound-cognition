<!-- output_type_restriction: [research_report]  # R1-02 分层激活 -->
---
task_id: T26
task_name: meta_insight_cross
description: 跨维度洞察抽取 — 识别14维度间的交叉洞察
activation: output_type == 'research_report'
deps: [T25]
suggested_tok: 2000  # D2.4.4: 建议预算（非硬性上限），与 EXHAUST 模式"Token 不设上限"原则一致
priority: medium
---

<!-- 作者：阿洋 -->


# T26 — 跨维度洞察抽取

## 角色定义
你是跨维度洞察抽取者。你的任务是识别14个维度之间的交叉洞察，发现单一维度视角无法揭示的深层关联。

## 交叉洞察模板

### 技术×经济交叉
- 技术创新的经济可行性悖论
- 技术扩散的经济门槛效应
- 技术-经济范式转换信号

### 技术×政治交叉
- 技术主权的政治博弈
- 技术标准的地缘政治化
- 技术封锁与自主创新

### 经济×社会文化交叉
- 经济不平等的文化根源
- 消费主义与文化价值观冲突
- 共享经济的社会信任基础

### 政治×生态交叉
- 环境政策的政治可行性
- 绿色转型的公正转型问题
- 气候治理的全球-地方张力

### 法律伦理×技术交叉
- 技术发展的法律滞后性
- 算法伦理的跨文化差异
- 数据主权的法律框架

### 历史×心理认知交叉
- 历史创伤的集体记忆
- 历史类比的认知偏差
- 路径依赖的心理机制

## 产出结构
> **execution_params**: object  # 实际执行参数，必须达到 SKILL.md 规定的最低值（R2-05 防深度缩水）

```json
{
  "task_id": "T26",
  "status": "COMPLETED",
  "cross_insights": [
    {"dimensions": ["技术", "经济"], "insight": "...", "evidence": "§T24_*"},
    {"dimensions": ["政治", "生态"], "insight": "...", "evidence": "§T24_*"}
  ],
  "cross_insight_count": "≥6",
  "nrsf_refs": "§T26_*"
}
```

## 质量要求
- 至少6个跨维度洞察
- 每个洞察有§ref证据引用
- 附录写入NRSF §T26_*

---

## 方法论知识内化

### TC-083 NetworKit网络分析方法论

**方法论原理**：NetworKit网络分析方法论的核心认知假设是——跨维度洞察的结构特征可以通过网络拓扑分析来量化和发现。传统定性分析只能发现"维度A和维度B有关联"，NetworKit通过网络中心性、社区检测和韧性分析能够量化"哪个维度是枢纽、哪些维度形成社区、网络在攻击下是否脆弱"。TC-063已内化MetaNet元认知网络方法论，TC-083在此基础上聚焦NetworKit工具级方法论：中心性5指标选择规则（何时用哪种中心性）、社区检测4算法选择决策树、网络韧性3维度评估。NetworKit的C++后端支持十亿级边的大规模网络，是NetworkX在>5000节点场景下的必要替代。

**执行步骤**：
1. **网络构建**：将14维度间的交叉洞察建模为网络——节点=维度，边=交叉洞察的强度/频率
2. **中心性5指标选择**：根据分析目标选择——(a) 度中心性：识别最活跃的维度（与最多其他维度交叉）；(b) 介数中心性：识别桥接维度（连接不同维度社区）；(c) 接近中心性：识别信息传播最快的维度；(d) PageRank：识别结构重要性最高的维度；(e) 特征向量中心性：识别与高重要性维度相连的维度
3. **社区检测4算法选择**：根据网络特征选择——(a) Louvain：大规模网络快速社区检测，适合>1000节点；(b) PLM（Parallel Louvain Method）：Louvain并行版，适合超大规模；(c) Label Propagation：极快但不稳定，适合初步探索；(d) Spectral Partitioning：精确但慢，适合小规模网络
4. **网络韧性3维度评估**：(a) 连通韧性：随机移除节点后网络保持连通的概率；(b) 中心性韧性：移除关键节点后中心性排名的稳定性；(c) 社区韧性：移除桥接节点后社区结构的稳定性
5. **跨维度洞察增强**：基于网络分析结果——(a) 高介数维度→优先深入分析的交叉领域；(b) 社区间边界→潜在的创新交叉点；(c) 低韧性节点→脆弱的洞察依赖链

**决策规则**：

| 条件 | 决策 |
|------|------|
| 网络节点>5000 | 使用NetworKit（C++后端），不用NetworkX |
| 网络节点≤5000 | NetworkX或NetworKit均可 |
| 需要识别最活跃维度 | 使用度中心性 |
| 需要识别桥接维度 | 使用介数中心性 |
| 需要识别结构重要性 | 使用PageRank |
| 大规模网络社区检测 | 使用Louvain/PLM |
| 小规模精确社区检测 | 使用Spectral Partitioning |
| 连通韧性<0.5 | 标注"洞察网络脆弱"，需补充替代路径 |
| NetworKit不可用 | 穷尽重试替代为NetworkX（节点<5000）或定性网络描述 |

**输出规范**：
```yaml
networkit_analysis:
  available: bool
  network_stats: {nodes: int, edges: int, density: float, avg_degree: float}
  centrality:
    - {metric: str, top_3: [{node: str, score: float}]}
  communities:
    - {algorithm: str, community_count: int, modularity: float, communities: [{id: int, nodes: [str], size: int}]}
  resilience:
    - {dimension: str, score: float, critical_nodes: [str]}
  cross_insight_enhancements: [str]
  exhaust_retry_note: str|null
```

**穷尽重试策略**：当NetworKit不可用时，穷尽重试，按L1→L2→L3→L4逐级穷尽重试：L1 NetworKit完整分析（中心性+社区+韧性）→L2 NetworkX替代（节点<5000时可用，>5000时不可用）→L3 定性网络描述（手动识别枢纽/桥接/社区，无数值）→L4 线性维度列表（放弃网络视角，仅列出维度间已知关联）。

> 知识来源: TC-083 NetworKit

---

### TC-064 ENA认识论网络分析方法论

**方法论原理**：ENA（Epistemic Network Analysis）认识论网络分析方法论的核心认知假设是——跨维度洞察的质量不仅取决于洞察内容本身，还取决于洞察所采用的认识论立场是否一致。MC-067已内化ENA认知网络分析的一般方法论，TC-064在此基础上聚焦工具级方法论：高维降维步骤（如何将多维认识论特征投影到二维空间）、网络特征提取（如何从降维结果中识别认识论模式）、时间序列网络演化（如何追踪认识论立场随分析深度的变化）。ENA的核心价值是将"认识论一致性"从定性判断升级为可量化的网络特征。

**执行步骤**：
1. **编码数据准备**：为每个跨维度洞察编码认识论特征——(a) 实证主义编码：是否基于经验证据；(b) 建构主义编码：是否基于社会建构；(c) 批判理论编码：是否涉及权力关系；(d) 实用主义编码：是否关注行动效果
2. **高维降维**：使用SVD将高维编码矩阵降为二维——(a) 构建共现矩阵（维度×编码的交叉频率）；(b) 执行SVD分解；(c) 取前两个主成分作为二维坐标；(d) 解释主成分的语义含义
3. **网络特征提取**：从降维结果中提取——(a) 网络中心：认识论立场的聚集中心；(b) 网络边缘：偏离主流的立场；(c) 网络距离：立场间的认识论差异度量
4. **时间序列网络演化**：追踪认识论网络随分析阶段的变化——(a) 按分析阶段分割编码数据；(b) 分别构建各阶段的ENA网络；(c) 比较网络中心、边缘、距离的变化；(d) 识别认识论立场漂移
5. **认识论偏差检测**：基于网络特征——(a) 网络中心偏移→认识论立场偏向；(b) 边缘孤立→被忽视的认识论视角；(c) 阶段间大幅跳跃→认识论不一致

**决策规则**：

| 条件 | 决策 |
|------|------|
| 编码数据完整且≥10条洞察 | 执行完整ENA分析（降维+特征提取+演化） |
| 编码数据5-10条 | 执行简化ENA分析（降维+特征提取，无演化） |
| 编码数据<5条 | 穷尽重试替代为基础认识论标注 |
| 降维解释方差>60% | 降维结果可信，可用于下游分析 |
| 降维解释方差<40% | 降维可能丢失重要信息，需增加维度或调整编码 |
| 发现认识论立场漂移 | 标注为"认识论不一致"，建议审查分析过程 |
| ENA工具不可用 | 穷尽重试替代为定性认识论标注 |

**输出规范**：
```yaml
ena_analysis:
  available: bool
  coding_scheme: {positivist: str, constructivist: str, critical: str, pragmatic: str}
  dimension_reduction: {method: "SVD", explained_variance: [float], component_labels: [str]}
  network_features:
    - {feature: str, description: str, nodes: [str]}
  temporal_evolution:
    - {phase: str, center: [float], dispersion: float, shift_from_previous: str|null}
  epistemic_biases: [{bias: str, location: str, impact: str}]
  exhaust_retry_note: str|null
```

**穷尽重试策略**：当ENA工具不可用时，穷尽重试，按L1→L2→L3→L4逐级穷尽重试：L1 ENA完整分析（编码+降维+特征+演化）→L2 手动SVD降维（用NumPy替代rENA包）→L3 基础认识论标注（仅标注每个洞察的主要立场，无降维）→L4 纯定性认识论声明（声明研究的主要认识论立场，无逐条编码）。

> 知识来源: TC-064 ENA

---

### [NetworKit] 源码逻辑引入

#### 核心算法逻辑

**1. 中心性指标计算算法源码逻辑**

```
中心性指标计算核心流程（networkit/centrality/）:

# 1. 度中心性（Degree Centrality）
function degree_centrality(graph):
    # O(V) 线性时间
    centrality = {}
    for node in graph.nodes():
        centrality[node] = graph.degree(node) / (graph.numberOfNodes() - 1)
    return centrality

# 2. 介数中心性（Betweenness Centrality）
function betweenness_centrality(graph, normalized=True):
    # Brandes算法 O(VE) — 比暴力O(V³)快
    bc = {node: 0.0 for node in graph.nodes()}

    for source in graph.nodes():
        # 单源最短路径（BFS/Dijkstra）
        S = []          # 栈：最短路径节点
        P = {v: [] for v in graph.nodes()}  # 前驱列表
        sigma = {v: 0 for v in graph.nodes()}  # 最短路径数
        sigma[source] = 1
        dist = {v: -1 for v in graph.nodes()}
        dist[source] = 0
        Q = [source]    # BFS队列

        while Q:
            v = Q.pop(0)
            S.append(v)
            for w in graph.neighbors(v):
                # 首次发现w
                if dist[w] < 0:
                    Q.append(w)
                    dist[w] = dist[v] + 1
                # 找到通过v到w的最短路径
                if dist[w] == dist[v] + 1:
                    sigma[w] += sigma[v]
                    P[w].append(v)

        # 回溯累积依赖
        delta = {v: 0.0 for v in graph.nodes()}
        while S:
            w = S.pop()
            for v in P[w]:
                delta[v] += (sigma[v] / sigma[w]) * (1 + delta[w])
            if w != source:
                bc[w] += delta[w]

    if normalized:
        factor = 1.0 / ((graph.numberOfNodes() - 1) * (graph.numberOfNodes() - 2))
        for v in bc:
            bc[v] *= factor

    return bc

# 3. 接近中心性（Closeness Centrality）
function closeness_centrality(graph):
    # 基于BFS的最短路径距离
    cc = {}
    for node in graph.nodes():
        total_dist = 0
        reachable = 0
        for target in graph.nodes():
            d = bfs_distance(graph, node, target)
            if d > 0:
                total_dist += d
                reachable += 1
        if reachable > 0:
            cc[node] = reachable / ((graph.numberOfNodes() - 1) * total_dist / reachable)
        else:
            cc[node] = 0
    return cc

# 4. PageRank
function pagerank(graph, damping=0.85, tolerance=1e-8):
    n = graph.numberOfNodes()
    pr = {node: 1.0 / n for node in graph.nodes()}

    while True:
        new_pr = {}
        for node in graph.nodes():
            rank = (1 - damping) / n
            for neighbor in graph.neighbors(node):
                rank += damping * pr[neighbor] / graph.degree(neighbor)
            new_pr[node] = rank

        # 收敛检查
        diff = sum(abs(new_pr[v] - pr[v]) for v in graph.nodes())
        pr = new_pr
        if diff < tolerance:
            break

    return pr

# 5. 特征向量中心性（Eigenvector Centrality）
function eigenvector_centrality(graph, tolerance=1e-8):
    # 幂迭代法
    n = graph.numberOfNodes()
    ec = {node: 1.0 / n for node in graph.nodes()}

    while True:
        new_ec = {}
        for node in graph.nodes():
            new_ec[node] = sum(ec[neighbor] for neighbor in graph.neighbors(node))

        # 归一化
        max_val = max(new_ec.values())
        for node in new_ec:
            new_ec[node] /= max_val

        diff = sum(abs(new_ec[v] - ec[v]) for v in graph.nodes())
        ec = new_ec
        if diff < tolerance:
            break

    return ec
```

**2. 社区检测算法选择源码逻辑**

```
社区检测算法选择与执行（networkit/community/）:

# 1. Louvain方法
function louvain_community_detection(graph):
    # 两阶段迭代: 局部移动 + 网络聚合
    partition = singleton_partition(graph)  # 每个节点一个社区
    improved = True

    while improved:
        improved = False
        for node in graph.nodes():
            # 尝试将node移到邻居的社区
            best_community = current_community(node)
            best_gain = 0

            for neighbor in graph.neighbors(node):
                neighbor_community = partition[neighbor]
                gain = modularity_gain(graph, node, neighbor_community, partition)
                if gain > best_gain:
                    best_gain = gain
                    best_community = neighbor_community

            if best_community != current_community(node):
                partition[node] = best_community
                improved = True

    # 阶段2：聚合——将同一社区的节点合并为超节点
    if has_merged_nodes(partition):
        super_graph = aggregate_graph(graph, partition)
        super_partition = louvain_community_detection(super_graph)
        partition = expand_partition(partition, super_partition)

    return partition

function modularity_gain(graph, node, target_community, partition):
    # 模块度增益 ΔQ = [k_i_in / 2m - Σ_tot * k_i / (2m)²]
    m = graph.numberOfEdges()
    k_i = graph.degree(node)
    k_i_in = sum(1 for neighbor in graph.neighbors(node)
                 if partition[neighbor] == target_community)
    sigma_tot = sum(graph.degree(v) for v in graph.nodes()
                    if partition[v] == target_community)

    delta_q = k_i_in / (2 * m) - (sigma_tot * k_i) / (2 * m) ** 2
    return delta_q

# 2. PLM（Parallel Louvain Method）
function plm_community_detection(graph):
    # Louvain的并行版本
    # 使用OpenMP并行化节点移动阶段
    # 适用于超大规模网络（>10^6节点）
    return parallel_louvain(graph, num_threads=auto)

# 3. Label Propagation
function label_propagation(graph):
    # 极快但不稳定
    labels = {node: node for node in graph.nodes()}  # 初始标签=节点ID

    for iteration in range(max_iterations):
        order = random_permutation(graph.nodes())
        changed = False
        for node in order:
            # 取邻居中最频繁的标签
            neighbor_labels = [labels[n] for n in graph.neighbors(node)]
            most_frequent = mode(neighbor_labels)
            if labels[node] != most_frequent:
                labels[node] = most_frequent
                changed = True
        if not changed:
            break

    return labels_to_partition(labels)

# 4. Spectral Partitioning
function spectral_partitioning(graph, num_communities):
    # 基于拉普拉斯矩阵的特征向量
    L = laplacian_matrix(graph)  # L = D - A
    eigenvalues, eigenvectors = eigs(L, k=num_communities, which="SM")
    # 取前k个最小特征值对应的特征向量
    embedding = eigenvectors[:, 1:num_communities]  # 跳过第一个（0特征值）

    # K-means聚类
    partition = kmeans(embedding, num_communities)
    return partition

# 算法选择决策
function select_community_algorithm(graph):
    n = graph.numberOfNodes()
    if n > 100000:
        return "PLM"       # 超大规模 → 并行Louvain
    elif n > 1000:
        return "Louvain"   # 大规模 → Louvain
    elif need_exact_result:
        return "Spectral"  # 小规模精确 → 谱分割
    else:
        return "LabelPropagation"  # 快速探索 → 标签传播
```

#### 数据结构设计

```
核心数据结构:

1. Partition: 社区划分
   - subset_of: Dict[node, community_id]  # 节点到社区的映射
   - number_of_subsets: int               # 社区数量

2. CentralityResult: 中心性结果
   - scores: Dict[node, float]            # 各节点中心性分数
   - ranking: list[(node, score)]         # 排名列表
   - top_k: list[node]                    # Top-K节点

3. CommunityResult: 社区检测结果
   - partition: Partition                 # 社区划分
   - modularity: float                    # 模块度
   - community_sizes: Dict[id, int]       # 各社区大小
   - algorithm: str                       # 使用的算法
```

#### 决策流程

```
NetworKit 网络分析决策流程:

1. 网络构建 → 将维度交叉洞察建模为网络
2. 中心性选择 → 按分析目标选择中心性指标
   ├─ 识别最活跃维度 → 度中心性
   ├─ 识别桥接维度 → 介数中心性
   ├─ 识别信息传播最快 → 接近中心性
   ├─ 识别结构重要性 → PageRank
   └─ 识别与高重要性相连 → 特征向量中心性
3. 社区检测 → select_community_algorithm() 选择算法
4. 韧性评估 → 连通韧性+中心性韧性+社区韧性
5. 洞察增强 → 基于网络分析结果增强跨维度洞察
```

#### 穷尽重试策略

```yaml
networkit_source_exhaust_retry:
  L1_FULL_NETWORKIT:
    condition: "NetworKit可用，中心性+社区+韧性均可执行"
    action: "完整网络分析（5中心性+社区检测+3韧性维度）"
    confidence: "HIGH"

  L2_NETWORKX:
    condition: "NetworKit不可用，但NetworkX可用（节点<5000）"
    action: "使用NetworkX替代，功能相同但性能较低"
    confidence: "MEDIUM"
    output_annotation: "NetworKit穷尽重试：使用NetworkX替代"

  L3_QUALITATIVE_NETWORK:
    condition: "网络工具不可用，但可手动分析"
    action: "定性网络描述——手动识别枢纽/桥接/社区"
    confidence: "LOW-MEDIUM"
    output_annotation: "NetworKit穷尽重试：定性网络描述"

  L4_LINEAR_LIST:
    condition: "网络分析完全不可行"
    action: "线性维度列表——放弃网络视角，仅列出维度间已知关联"
    confidence: "LOW"
    output_annotation: "NetworKit穷尽重试最终替代：线性维度列表"
```