---
node_id: "T01d"
name: "人设故事解析"
phase: 1
deps: ["T01b"]
route: always
condition: "wechat_article 且用户提供个人故事"
tok: 800
---

<!-- 作者：阿洋 -->


# T01d — 人设故事解析（Persona Story Parse）

## Step 1：从用户故事中抽取人设字段
- identity（你是谁/做什么的）
- core_values（你相信什么/在乎什么）
- catchphrase（标志性口头禅/表达习惯）
- emotion_expression（情绪表达方式）
- 同步 A-J 别名

## Step 2：故事结构化存储
- 每个故事存入 personal_stories[]：{原始文本, 场景, 情绪, 转折, 清晰度评分}
- 故事清晰度 = 有场景 + 有情绪 + 有转折 → 3/3 = 清晰

## Step 3：清晰度追问（最多 2 轮）
- 对每个 required 字段检查清晰度
- 缺失或模糊 → 追问（如"你说的那个场景，具体是什么时候？当时你什么感受？"）
- 2 轮后仍不清晰 → 标 [待补充]

## Step 4：输出人设卡
- 写入 NRSF §persona_card-{timestamp}
- 包含 12 字段 + story_clarity_status

## Step 5：HKR 选题质检
- Happy（愉悦度）：读者读完会感到愉悦/有趣吗？1-5分
- Knowledge（知识增量）：读者能学到新东西吗？1-5分
- Resonance（共鸣度）：读者会产生"我也是"的感觉吗？1-5分
- S 级：三项兼备（≥4/5每项）
- 及格：≥两项（≥3/5）
- 仅一项：提示用户调整选题方向

## HKR 误判回退机制
- 故事 < 2 → HKR 穷尽重试替代为仅供参考
- 故事 ≥ 2 但模糊 → 附加素材充分度标注
- 任一维度素材不足 → 附带"[素材不足]"标记
- HKR 不阻断流程（建议性质检）

## self_check_before_output
- [ ] 12 字段是否全部填充（含 [待补充] 标记）
- [ ] A-J 别名是否同步
- [ ] personal_stories 数组非空且包含清晰度评分
- [ ] HKR 三项均已打分（1-5分）
- [ ] 故事清晰度已评定
- [ ] NRSF §persona_card-{timestamp} 是否写入成功