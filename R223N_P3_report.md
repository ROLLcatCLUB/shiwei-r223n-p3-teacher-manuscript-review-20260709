# R223N-P3 教师文稿文法对齐报告

```text
stage_id=1013R_R223N_P3_TEACHER_MANUSCRIPT_GRAMMAR_ALIGNMENT
source_stage_id=1013R_R223N_P2_TEACHER_LANGUAGE_HUMANIZATION_AND_LABEL_DETECHNICALIZATION
standard_id=GOLDEN_CLASSROOM_EVENT_EXPANSION_STANDARD_V0.1_LOCK_CANDIDATE
status=teacher_manuscript_grammar_alignment_report
preview_only=true
teacher_confirmed=false
formal_apply_allowed=false
R97B / UI / runtime / prompt / model / db = untouched
```

## 一、当前判断

```text
R223N-P2 = PASS_LANGUAGE_HUMANIZATION_BUT_MANUSCRIPT_GRAMMAR_NOT_YET_PASS
R223N-P3 = TEACHER_MANUSCRIPT_GRAMMAR_ALIGNED
formal_ui = blocked
R97B / UI / runtime / prompt / model / db = untouched
```

## 二、对齐结果

```text
p2_visible_label_count_in_default=0
backend_term_count_in_default=0
component_name_count_in_default=0
design_intent_count=5
teacher_talk_signal=True
student_activity_signal=True
screen_sheet_assessment_signal=True
```

## 三、内容说明

- 默认教师稿新增课时定位、教学目标、重难点、准备、单课结构、评价设计和板书 / 大屏结构；
- 教学过程不再重复 P2 的固定标题，而是按活动步骤组织；
- 学生可能反应、教师追问、补救策略、投屏示范、学习单记录和评价证据没有删除；
- 组件名默认退到 review ledger，正文只保留对应课堂动作；
- 本包仍然只是静态内容产物，不授权正式 UI 或 runtime。

## 四、浏览器 smoke

```text
url=http://127.0.0.1:8907/R223N_P3_teacher_manuscript_draft_v4.html
h1=《有趣的纸印》教师文稿版 v4
h2_count=10
h3_count=4
h4_count=7
table_count=3
design_intent_blocks=4
has_p2_labels=false
has_backend_terms=false
has_component_names=false
has_teacher_talk=true
has_assessment=true
horizontal_overflow=false
screenshot=R223N_P3_teacher_manuscript_draft_v4_screenshot.png
smoke_result=R223N_P3_browser_smoke_result.json
```
