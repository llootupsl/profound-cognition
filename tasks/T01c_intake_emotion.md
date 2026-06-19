---
task_id: T01c
task_name: intake_emotion
description: 输入情绪基调提取与风格偏好识别
activation: always（所有output_type和所有模式）
deps: [T00]
tok_budget: 500
priority: high
---

<!-- 作者：阿洋 -->


# T01c — 输入情绪基调提取

## 角色定义
你是输入分析者。你的任务是从用户的原始输入中提取情绪基调、隐式风格偏好，并产出生效控制信号。

## 执行流程

### Step 1: emotional_tone 提取
分析用户输入中的情绪基调：
- urgency: "calm" | "concerned" | "urgent" | "critical"
- stance: "neutral" | "optimistic" | "skeptical" | "critical" | "curious"
- intensity: 1-5（情绪强度评分）

```json
{{
  "emotional_tone": {{
    "urgency": "calm|concerned|urgent|critical",
    "stance": "neutral|optimistic|skeptical|critical|curious",
    "intensity": 3
  }}
}}
```

### Step 2: stylistic_hints 提取
识别用户隐式表达的风格偏好：
- formality: "academic" | "business" | "casual" | "popular"
- depth_preference: "surface" | "moderate" | "deep" | "exhaustive"
- visual_preference: "text_only" | "light_visuals" | "rich_visuals"
- length_tolerance: "concise" | "moderate" | "long" | "unlimited"

```json
{{
  "stylistic_hints": {{
    "formality": "academic|business|casual|popular",
    "depth_preference": "exhaustive",
    "visual_preference": "rich_visuals",
    "length_tolerance": "unlimited"
  }}
}}
```

### Step 3: persona_init_trigger
判断是否触发人设初始化（Phase -1）：
- wechat_article → ALWAYS true
- research_report → true（若检测到风格偏好）
- course_material → true（若检测到教学方法偏好）

```json
{{
  "persona_init_trigger": true
}}
```

### Step 4: depth_scan_priority 产出
根据用户输入推断 domain_depth 建议值和优先维度：
```json
{{
  "depth_scan_priority": {{
    "suggested_domain_depth": 5,
    "priority_dimensions": ["技术", "经济", "社会文化"],
    "rationale": "用户关注技术创新的经济和社会影响"
  }}
}}
```

## 产出结构
```json
{{
  "task_id": "T01c",
  "status": "COMPLETED",
  "emotional_tone": {{...}},
  "stylistic_hints": {{...}},
  "persona_init_trigger": true|false,
  "depth_scan_priority": {{...}},
  "emotion_curve_target": {{
    "segment_1": {{ "position": "开头 0-10%", "target_emotion": "好奇/悬念", "intensity": 3, "technique_hint": "反直觉钩子 / 场景开场" }},
    "segment_2": {{ "position": "引入 10-20%", "target_emotion": "共鸣/认同", "intensity": 2, "technique_hint": "个人经验锚 / 对话感" }},
    "segment_3": {{ "position": "展开 20-30%", "target_emotion": "认知冲突", "intensity": 3, "technique_hint": "对比张力 / 疑问句刹车" }},
    "segment_4": {{ "position": "深入 30-40%", "target_emotion": "专注/思考", "intensity": 2, "technique_hint": "数据具象化" }},
    "segment_5": {{ "position": "转折 40-50%", "target_emotion": "意外/震撼", "intensity": 4, "technique_hint": "转折叙事 / 反直觉" }},
    "segment_6": {{ "position": "解释 50-60%", "target_emotion": "恍然大悟", "intensity": 2, "technique_hint": "知识随手掏" }},
    "segment_7": {{ "position": "展开 60-70%", "target_emotion": "信任/追随", "intensity": 2, "technique_hint": "弱点暴露 / 自嘲" }},
    "segment_8": {{ "position": "高潮 70-80%", "target_emotion": "共鸣/感动", "intensity": 4, "technique_hint": "文化映射 / 情绪递进" }},
    "segment_9": {{ "position": "收束 80-90%", "target_emotion": "启发/思考", "intensity": 3, "technique_hint": "留白与悬念" }},
    "segment_10": {{ "position": "结尾 90-100%", "target_emotion": "余温/行动欲", "intensity": 2, "technique_hint": "金句收尾 / 人称带入" }}
  }}
}}
```

## 产出：emotion_curve_target（10 段目标情绪曲线）

| 段落 | 位置 | 目标情绪 | 强度 | 技法提示 |
|------|------|---------|------|---------|
| 1 | 开头 0-10% | 好奇/悬念 | ⭐⭐⭐ | 反直觉钩子 / 场景开场 |
| 2 | 引入 10-20% | 共鸣/认同 | ⭐⭐ | 个人经验锚 / 对话感 |
| 3 | 展开 20-30% | 认知冲突 | ⭐⭐⭐ | 对比张力 / 疑问句刹车 |
| 4 | 深入 30-40% | 专注/思考 | ⭐⭐ | 数据具象化 |
| 5 | 转折 40-50% | 意外/震撼 | ⭐⭐⭐⭐ | 转折叙事 / 反直觉 |
| 6 | 解释 50-60% | 恍然大悟 | ⭐⭐ | 知识随手掏 |
| 7 | 展开 60-70% | 信任/追随 | ⭐⭐ | 弱点暴露 / 自嘲 |
| 8 | 高潮 70-80% | 共鸣/感动 | ⭐⭐⭐⭐ | 文化映射 / 情绪递进 |
| 9 | 收束 80-90% | 启发/思考 | ⭐⭐⭐ | 留白与悬念 |
| 10 | 结尾 90-100% | 余温/行动欲 | ⭐⭐ | 金句收尾 / 人称带入 |

## 质量要求
- emotional_tone 不可为空
- persona_init_trigger 必须为布尔值
- depth_scan_priority.suggested_domain_depth 范围 1-5
- tok_budget 严格控制在 500 以内