# R223N-P3 Gold Manuscript Grammar Analysis

```text
stage_id=1013R_R223N_P3_TEACHER_MANUSCRIPT_GRAMMAR_ALIGNMENT
source_stage_id=1013R_R223N_P2_TEACHER_LANGUAGE_HUMANIZATION_AND_LABEL_DETECHNICALIZATION
standard_id=GOLDEN_CLASSROOM_EVENT_EXPANSION_STANDARD_V0.1_LOCK_CANDIDATE
status=gold_manuscript_grammar_analysis
preview_only=true
teacher_confirmed=false
formal_apply_allowed=false
R97B / UI / runtime / prompt / model / db = untouched
```

## 一、判断

《我为文具代言》的价值不在于简单“表格多”或“正文长”，而在于它形成了稳定的教师文稿秩序：先总览，再结构，再流程，再细节，再评价。每一种形态都有角色，表格负责总览，结构图负责关系，正文负责上课过程，【设计意图】负责解释为什么，图片和学习单负责素材证据，评价表负责学习证据。

## 二、Gold Grammar

| 文稿部件 | 承担的角色 | 对 R223N-P3 的启发 |
| --- | --- | --- |
| 单元总表 | 把主题、学科、年级、大观念、基本问题、目标、学情和重难点放在一张总览里 | 教师先知道这节课从哪里来，不被细节淹没 |
| 单元评价方案 | 表现性任务和评价要点单列 | 评价不是课后附加，而是从任务开始就有方向 |
| 单元结构表 | 阶段、学习任务、小问题、学习活动、学习评价并列呈现 | 让阶段责任和活动关系先被压清楚 |
| 单元结构图 | 用图表达四阶段关系 | 帮助教师快速抓住整体推进，不把单课孤立出来 |
| 教学过程摘要 | 按阶段写活动名和简要过程 | 先看流程骨架，再进入具体课堂 |
| 具体教学过程 | 活动名、教师话术、学生活动、小结、设计意图、素材和学习单 | 正文承担上课过程，不承担完整后端 ledger |
| 【设计意图】 | 把推理链压成教师能接受的一小段理由 | 解释为什么这样教，但不把控制点逐项外露 |
| 图片 / 学习单 / 评价表 | 素材、记录和评价单独承担证据角色 | 让视觉材料和学习证据有位置，不挤进正文 |

## 三、对 R223N 的修正

R223N-P2 已经把字段味降下来，但仍然把课堂事件 ledger 的节奏直接排成教师稿。P3 要做的是第二次转译：把后端事件结构转成教师文稿结构。默认稿不再一环一环重复“这一环节要解决什么 / 如果学生卡住 / 下游影响”等标题，而是使用教师熟悉的教案文法：

```text
课时定位
教学目标
教学重难点
教学准备
教学过程：活动步骤 + 教师话术 + 学生活动 + 小结 + 【设计意图】
评价设计
板书 / 大屏结构
附：review ledger 保存说明
```

P3 不删除课堂事件链，只改变默认教师阅读层的组织方式。
