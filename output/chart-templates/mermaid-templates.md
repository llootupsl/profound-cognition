<!-- 作者：阿洋 -->

# Mermaid 图表模板库

以下为常用图表类型的 Mermaid.js 标准模板。所有模板均可直接粘贴到 Markdown 中的 ````mermaid` 代码块中。

## 1. 流程图 (Flowchart)

```mermaid
graph TD
    A[起点] --> B{判断条件}
    B -->|是| C[执行路径A]
    B -->|否| D[执行路径B]
    C --> E[结果]
    D --> E
```

## 2. 时序图 (Sequence Diagram)

```mermaid
sequenceDiagram
    participant A as 角色A
    participant B as 角色B
    A->>B: 请求
    B-->>A: 响应
    Note over A,B: 说明文字
```

## 3. 甘特图 (Gantt Chart)

```mermaid
gantt
    title 项目时间线
    dateFormat  YYYY-MM-DD
    section 阶段一
    任务A           :a1, 2024-01-01, 30d
    任务B           :after a1, 20d
    section 阶段二
    任务C           :2024-02-15, 45d
```

## 4. 饼图 (Pie Chart)

```mermaid
pie title 数据分布
    "类别A" : 45
    "类别B" : 30
    "类别C" : 15
    "其他" : 10
```

## 5. 思维导图 (Mindmap)

```mermaid
mindmap
  root((核心主题))
    子主题A
      细节A1
      细节A2
    子主题B
      细节B1
      细节B2
    子主题C
```

## 6. 状态图 (State Diagram)

```mermaid
stateDiagram-v2
    [*] --> 状态A
    状态A --> 状态B : 事件触发
    状态B --> 状态C : 条件满足
    状态C --> [*]
```

## 7. 类图 (Class Diagram)

```mermaid
classDiagram
    class 类名 {
        +属性1
        -属性2
        +方法1()
        -方法2()
    }
    类A <|-- 类B : 继承
    类A *-- 类C : 组合
```

## 使用说明

1. 选择最接近目标结构的模板
2. 替换模板中的占位文字（起点、角色A、类别A 等）
3. 在 Mermaid 代码块中渲染：````mermaid {模板内容} ````
4. 若外部渲染工具不可用，HTML 穷尽尝试层已内嵌 Mermaid.js CDN 将自动渲染图表