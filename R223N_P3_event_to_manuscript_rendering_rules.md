# R223N-P3 Event To Manuscript Rendering Rules

```text
stage_id=1013R_R223N_P3_TEACHER_MANUSCRIPT_GRAMMAR_ALIGNMENT
source_stage_id=1013R_R223N_P2_TEACHER_LANGUAGE_HUMANIZATION_AND_LABEL_DETECHNICALIZATION
standard_id=GOLDEN_CLASSROOM_EVENT_EXPANSION_STANDARD_V0.1_LOCK_CANDIDATE
status=event_to_manuscript_rules
preview_only=true
teacher_confirmed=false
formal_apply_allowed=false
R97B / UI / runtime / prompt / model / db = untouched
```

## 一、核心原则

P3 不把课堂事件字段直接铺给老师。后端字段仍完整留在 review ledger，教师默认稿只看文稿结果。事件链进入教师稿时，需要被转译为：活动步骤、教师话术、学生活动、课堂调控、小结、【设计意图】、素材和评价证据。

## 二、字段转译表

| 后端字段 | 教师稿位置 | 渲染规则 |
| --- | --- | --- |
| teaching_responsibility | 环节导语或【设计意图】 | 不作为固定字段标题反复出现 |
| student_problem | 设计意图中的问题意识，或正文中的教师提醒 | 只露出教师需要抓住的教学风险 |
| task_release | 教师话术 | 直接写成“教师：……” |
| expected_student_responses | 学生活动和学生可能回答 | 自然嵌入，不列完整清单 |
| likely_misconceptions_or_failures | “若学生……”的课堂调控句 | 只保留高频偏差 |
| teacher_follow_up_questions | 教师追问 | 写进正文，不另做追问矩阵 |
| teacher_rescue_strategy | 教师调整 / 小支架 | 在学生卡住处自然补入 |
| screen_trigger | 大屏可出示…… | 只写和本环节相关的 1 句 |
| component_trigger | 课堂动作 | 默认稿不写组件名，转成两图对比、摸猜、步骤拆解、圈画等动作 |
| learning_sheet_trigger | 学习单记录 | 写成学生留下什么记录 |
| evidence_trigger | 评价证据 | 进入环节收束或评价设计 |
| transition_chain | 过渡语 | 帮助教师知道下一步为何自然发生 |

## 三、默认稿与审核稿分层

- 默认教师稿：连续教案文稿，不显示完整 event_id、组件矩阵和控制点矩阵。
- 审核视图：保留 event_id、组件触发、screen_trigger、learning_sheet_trigger、evidence_trigger 和 source_anchor。
- 评价视图：只抽取“可观察证据”和“学习单记录”，不把全部推理链塞入正文。

## 四、禁止

- 不把 R223N-P2 的固定标题继续作为每个环节主结构；
- 不把组件名作为工具清单显示在教师稿；
- 不把大屏、学习单、评价证据堆成卡片墙；
- 不把《我为文具代言》的文具内容迁移到《有趣的纸印》。
