# R223N-P3 Review Ledger Preservation Note

```text
stage_id=1013R_R223N_P3_TEACHER_MANUSCRIPT_GRAMMAR_ALIGNMENT
source_stage_id=1013R_R223N_P2_TEACHER_LANGUAGE_HUMANIZATION_AND_LABEL_DETECHNICALIZATION
standard_id=GOLDEN_CLASSROOM_EVENT_EXPANSION_STANDARD_V0.1_LOCK_CANDIDATE
status=review_ledger_preservation_note
preview_only=true
teacher_confirmed=false
formal_apply_allowed=false
R97B / UI / runtime / prompt / model / db = untouched
```

## 一、分层原则

P3 默认教师稿不显示完整 event_id、组件触发矩阵和控制点矩阵，但这些信息没有被删除。它们继续作为 review ledger 和后续大屏、学习单、评价证据生成的依据。

## 二、Ledger 保留摘要

| event_id | 事件 | 组件触发（审核层） | 大屏触发 | 学习单字段 | 最小证据 |
| --- | --- | --- | --- | --- | --- |
| paper_print_event_01_task_entry | 任务入场：走进版画车间坊 | 比一比 | 版画车间坊任务语 + 画出来/印出来对比图 + 记录句式 | 入场记录 | 能说出一个印痕观察点。 |
| paper_print_event_02_material_texture_observation | 摸一摸：纸材肌理观察 | 材料盲盒 | 纸材观察词库 + 侧光肌理照片 + 一句预测格式 | 纸材预测 | 每组至少一条带理由的纸材预测。 |
| paper_print_event_03_texture_making | 变一变：制造纸的新肌理 | 技法拆解 | 刻/剪/撕/拼贴/揉/卷/折方法图 + 小块试验提醒 | 改造方法 | 每组保留一个改造小样。 |
| paper_print_event_04_first_print_trial | 试一试：第一次转印 | 圈一圈 | 少量上色、均匀压印、慢揭纸三步图 + 清楚/糊印对比 | 试印记录 | 每组至少一张有圈画和一句调整计划的试印记录。 |
| paper_print_event_05_print_method_comparison | 比一比：干印、湿印与油印 | 比一比 | 同版不同印法对照图 + 清晰边缘/灰层/肌理保留观察角度 | 印法比较 | 每组至少一组同版不同印法对照。 |
| paper_print_event_06_artwork_creation_with_print_marks | 做一做：用印痕完成作品 | 中途看一看 | 一主一辅画面提示 + 印痕过多/重点清楚作品对比 + 清理提示 | 作品取舍 | 作品中至少有一处可说明来源的印痕。 |
| paper_print_event_07_gallery_reflection | 说一说：印痕展评与车间收束 | 作品画廊 | 展示句式 + 纸材/印法/印痕/画面四类评价词 + 证据归档提醒 | 展评归档 | 每组至少一份作品与试印证据配套归档。 |

## 三、边界

默认稿可以把组件转成课堂动作，例如“两图对比”“摸猜材料”“步骤拆解”“圈画印痕”。审核层仍保留组件名和 component_id，供后续系统检查；正式 UI、R97B、runtime 和数据库仍然不接入。
