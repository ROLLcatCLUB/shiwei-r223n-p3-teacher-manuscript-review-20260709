from __future__ import annotations

import html
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RENDER_ROOT = ROOT.parent
CHAIN_PATH = RENDER_ROOT / "1013R_R223N_CROSS_SAMPLE_CLASSROOM_EVENT_EXPANSION_VALIDATION" / "R223N_classroom_event_expansion_chain.json"
P2_PATH = RENDER_ROOT / "1013R_R223N_P2_TEACHER_LANGUAGE_HUMANIZATION_AND_LABEL_DETECHNICALIZATION" / "R223N_P2_teacher_default_reading_draft_v3.md"
STAGE_ID = "1013R_R223N_P3_TEACHER_MANUSCRIPT_GRAMMAR_ALIGNMENT"
SOURCE_STAGE_ID = "1013R_R223N_P2_TEACHER_LANGUAGE_HUMANIZATION_AND_LABEL_DETECHNICALIZATION"
STANDARD_ID = "GOLDEN_CLASSROOM_EVENT_EXPANSION_STANDARD_V0.1_LOCK_CANDIDATE"


P2_VISIBLE_LABELS = [
    "这一环节要解决什么",
    "上课时可以这样展开",
    "如果学生卡住",
    "留下什么，再往哪走",
    "大屏、学习单和评价怎么跟上",
]

BACKEND_TERMS = [
    "event_id",
    "teaching_responsibility",
    "student_problem",
    "task_release",
    "expected_student_responses",
    "likely_misconceptions",
    "teacher_follow_up",
    "teacher_rescue_strategy",
    "component_trigger",
    "screen_trigger",
    "learning_sheet_trigger",
    "evidence_trigger",
]

COMPONENT_NAMES = [
    "比一比",
    "材料盲盒",
    "技法拆解",
    "圈一圈",
    "中途看一看",
    "作品画廊",
]


def load_chain() -> dict:
    return json.loads(CHAIN_PATH.read_text(encoding="utf-8"))


def md_table(headers: list[str], rows: list[list[str]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        out.append("| " + " | ".join(str(cell).replace("\n", "<br>") for cell in row) + " |")
    return "\n".join(out)


def first(items: list[str], default: str = "") -> str:
    return items[0] if items else default


def second(items: list[str], default: str = "") -> str:
    return items[1] if len(items) > 1 else default


def short(text: str, limit: int = 52) -> str:
    text = str(text).strip()
    return text if len(text) <= limit else text[: limit - 1] + "…"


def render_meta(status: str) -> str:
    return f"""```text
stage_id={STAGE_ID}
source_stage_id={SOURCE_STAGE_ID}
standard_id={STANDARD_ID}
status={status}
preview_only=true
teacher_confirmed=false
formal_apply_allowed=false
R97B / UI / runtime / prompt / model / db = untouched
```"""


def build_grammar_analysis() -> str:
    rows = [
        ["单元总表", "把主题、学科、年级、大观念、基本问题、目标、学情和重难点放在一张总览里", "教师先知道这节课从哪里来，不被细节淹没"],
        ["单元评价方案", "表现性任务和评价要点单列", "评价不是课后附加，而是从任务开始就有方向"],
        ["单元结构表", "阶段、学习任务、小问题、学习活动、学习评价并列呈现", "让阶段责任和活动关系先被压清楚"],
        ["单元结构图", "用图表达四阶段关系", "帮助教师快速抓住整体推进，不把单课孤立出来"],
        ["教学过程摘要", "按阶段写活动名和简要过程", "先看流程骨架，再进入具体课堂"],
        ["具体教学过程", "活动名、教师话术、学生活动、小结、设计意图、素材和学习单", "正文承担上课过程，不承担完整后端 ledger"],
        ["【设计意图】", "把推理链压成教师能接受的一小段理由", "解释为什么这样教，但不把控制点逐项外露"],
        ["图片 / 学习单 / 评价表", "素材、记录和评价单独承担证据角色", "让视觉材料和学习证据有位置，不挤进正文"],
    ]
    return f"""# R223N-P3 Gold Manuscript Grammar Analysis

{render_meta("gold_manuscript_grammar_analysis")}

## 一、判断

《我为文具代言》的价值不在于简单“表格多”或“正文长”，而在于它形成了稳定的教师文稿秩序：先总览，再结构，再流程，再细节，再评价。每一种形态都有角色，表格负责总览，结构图负责关系，正文负责上课过程，【设计意图】负责解释为什么，图片和学习单负责素材证据，评价表负责学习证据。

## 二、Gold Grammar

{md_table(["文稿部件", "承担的角色", "对 R223N-P3 的启发"], rows)}

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
"""


def build_rendering_rules() -> str:
    rows = [
        ["teaching_responsibility", "环节导语或【设计意图】", "不作为固定字段标题反复出现"],
        ["student_problem", "设计意图中的问题意识，或正文中的教师提醒", "只露出教师需要抓住的教学风险"],
        ["task_release", "教师话术", "直接写成“教师：……”"],
        ["expected_student_responses", "学生活动和学生可能回答", "自然嵌入，不列完整清单"],
        ["likely_misconceptions_or_failures", "“若学生……”的课堂调控句", "只保留高频偏差"],
        ["teacher_follow_up_questions", "教师追问", "写进正文，不另做追问矩阵"],
        ["teacher_rescue_strategy", "教师调整 / 小支架", "在学生卡住处自然补入"],
        ["screen_trigger", "大屏可出示……", "只写和本环节相关的 1 句"],
        ["component_trigger", "课堂动作", "默认稿不写组件名，转成两图对比、摸猜、步骤拆解、圈画等动作"],
        ["learning_sheet_trigger", "学习单记录", "写成学生留下什么记录"],
        ["evidence_trigger", "评价证据", "进入环节收束或评价设计"],
        ["transition_chain", "过渡语", "帮助教师知道下一步为何自然发生"],
    ]
    return f"""# R223N-P3 Event To Manuscript Rendering Rules

{render_meta("event_to_manuscript_rules")}

## 一、核心原则

P3 不把课堂事件字段直接铺给老师。后端字段仍完整留在 review ledger，教师默认稿只看文稿结果。事件链进入教师稿时，需要被转译为：活动步骤、教师话术、学生活动、课堂调控、小结、【设计意图】、素材和评价证据。

## 二、字段转译表

{md_table(["后端字段", "教师稿位置", "渲染规则"], rows)}

## 三、默认稿与审核稿分层

- 默认教师稿：连续教案文稿，不显示完整 event_id、组件矩阵和控制点矩阵。
- 审核视图：保留 event_id、组件触发、screen_trigger、learning_sheet_trigger、evidence_trigger 和 source_anchor。
- 评价视图：只抽取“可观察证据”和“学习单记录”，不把全部推理链塞入正文。

## 四、禁止

- 不把 R223N-P2 的固定标题继续作为每个环节主结构；
- 不把组件名作为工具清单显示在教师稿；
- 不把大屏、学习单、评价证据堆成卡片墙；
- 不把《我为文具代言》的文具内容迁移到《有趣的纸印》。
"""


def build_overview_tables(events: list[dict]) -> str:
    structure_rows = [
        ["第一段", "入场与纸材观察", "纸材和印法碰在一起会留下什么痕迹？", "走进版画车间坊；纸材肌理观察", "入场观察句；纸材预测句"],
        ["第二段", "纸材改造与第一次试印", "纸怎样变出新的可印肌理？", "制造新肌理；第一次转印", "改造小样；试印记录"],
        ["第三段", "印法比较与作品完成", "不同印法怎样改变印痕效果？", "干印 / 湿印 / 油印比较；完成纸印作品", "同版对照；作品取舍说明"],
        ["第四段", "展评与车间收束", "怎样用证据说明自己的纸印作品？", "作品与试印记录一起展评", "作品 + 试印证据归档"],
    ]
    return f"""## 一、课时定位

| 项目 | 内容 |
| --- | --- |
| 课题 | 《有趣的纸印》 |
| 课型 | 材料 / 技法 / 印痕探究 |
| 核心理解 | 印痕是版画的独特语言；纸材、改造方法和印法都会改变画面效果。 |
| 本课任务 | 走进“版画车间坊”，通过纸材观察、肌理制造、试印比较和作品展评，完成一件能说明纸材和印法效果的纸印作品。 |
| 学习证据 | 纸材预测、改造小样、试印记录、同版印法对照、作品说明与展评记录。 |

## 二、教学目标

1. 能观察不同纸材的厚薄、软硬、粗糙、光滑和凹凸肌理，并尝试预测它们可能留下的印痕。
2. 能用揉、撕、折、拼贴等方法制造纸的新肌理，并通过一次或多次试印验证纸材和印法对印痕的影响。
3. 能选择合适纸材和印法完成小幅纸印作品，并用纸材、印法、印痕等词语说明自己的发现。
4. 能在展示中带着试印记录评价作品，形成用证据说话的版画学习习惯。

## 三、教学重难点

**重点。** 引导学生从“纸不一样”进一步看到“纸材、肌理和印法会留下不同印痕”，并能通过试印记录表达发现。

**难点。** 学生容易把纸印课做成普通纸手工或漂亮图案制作。本课要帮助他们把注意力落到印痕证据上：哪里清楚、哪里模糊、为什么会这样、下一次怎样调整。

## 四、教学准备

- 教师准备：普通绘画作品与纸印作品对比图、纸材观察词库、几种纸材小样、改造方法示范小样、同版不同印法对照图、展示句式。
- 学生准备：不同纸材、剪刀或安全刻划工具、颜料或油墨、滚筒或替代刷具、试印纸、清洁材料。
- 学习单：入场观察、纸材预测、改造方法、试印记录、印法比较、作品取舍和展评归档。
- 替代方案：如油墨或滚筒不足，可先使用拓印、单色试印或局部小样试印保底。

## 五、单课结构

{md_table(["阶段", "学习任务", "小问题", "课堂活动", "学习证据"], structure_rows)}
"""


def event_by_id(events: list[dict], suffix: str) -> dict:
    for event in events:
        if event["event_id"].endswith(suffix):
            return event
    raise KeyError(suffix)


def process_text(events: list[dict]) -> str:
    e1 = event_by_id(events, "task_entry")
    e2 = event_by_id(events, "material_texture_observation")
    e3 = event_by_id(events, "texture_making")
    e4 = event_by_id(events, "first_print_trial")
    e5 = event_by_id(events, "print_method_comparison")
    e6 = event_by_id(events, "artwork_creation_with_print_marks")
    e7 = event_by_id(events, "gallery_reflection")

    return f"""## 六、教学过程

### （一）入场与观察：从“纸作品”走向“印痕”

#### 1. 看一看：发现纸印痕迹

教师先出示一张普通绘画作品和一张纸印痕迹明显的作品，请学生不急着评价好不好看，而是找一找：哪一张更像“印”出来的？它和画出来的线条有什么不同？

教师：“今天我们不是只做一张纸作品，而是进入一个小小的版画车间。纸材和印法碰在一起，会留下什么样的印痕？这就是我们今天要一起找的秘密。”

学生可能会说纸有厚薄、软硬、粗糙、光滑，也可能想到印章、拓印、压印等生活经验。若学生只说“这张好看”“颜色不一样”，教师可以把局部放大，请他们圈出重复、压印、留白或边缘痕迹，再追问：“这个痕迹像是画出来的，还是材料压出来的？”这样把注意力从图案喜好拉回印痕观察。

小结时，教师把“版画车间坊”说清楚：这里不是普通展板，而是作品和试验证据一起展示的空间。学生先在学习单上写一句：“我发现印痕和画线不同的地方是……”作为入场记录。

#### 2. 摸一摸：纸材肌理观察

每组选择三种纸，先不急着上色。教师请学生摸一摸、看一看，也可以斜着照一照，猜一猜哪张纸最可能留下明显肌理。

学生通常会先说“这张纸硬”“这张纸粗”“这张纸好看”。如果他们只按颜色或大小分类，教师可以拿两张颜色接近但肌理不同的纸，让学生闭眼摸一摸，再问：“看不见颜色以后，你还能怎么分？”这时再给出粗糙、细密、凸起、凹下、吸水、光滑、柔软、硬挺等词语，帮助学生把感觉说出来。

这一活动结束前，每组只选一张最想试印的纸，并写下预测：“我选择的纸材是……我预测它会留下……印痕，因为……”有了预测，后面的试印就不是随便尝试，而是在验证自己的判断。

【设计意图】本段先把学生从“做纸作品”的经验拉到“观察印痕”的任务上。通过作品对比、局部圈画和纸材触摸，学生知道本课关注的不是纸好不好看，而是纸材和印法怎样留下可以观察、可以记录、可以说明的痕迹。

大屏可出示画出来 / 印出来对比图、纸材观察词库和预测句式。评价重点看学生能否说出一个印痕观察点，并能用肌理词说明纸材预测。

### （二）改造与试印：让纸留下新的痕迹

#### 1. 变一变：制造纸的新肌理

教师把任务缩小：“请你只选一种方法改造纸，可以刻、剪、撕、揉、卷、折或拼贴。改造后先不追求像什么，而要看看它会不会留下新的肌理。”

学生可能会剪出复杂造型，或把拼贴做得很厚。教师不急着否定，而是请他们用手指给同伴看：“你改造出来的肌理在哪里？这块地方印出来可能是线、点，还是一片灰？”如果全班开始偏向手工装饰，教师暂停半分钟，展示一张简单但肌理清楚的小样，提醒大家：今天先要印得清楚，再考虑造型丰富。

每组保留一个改造小样，并在学习单上写：“我用……方法让纸出现了……肌理。”这个记录会成为下一步试印时判断成败的依据。

#### 2. 试一试：第一次转印

教师示范少量上色、均匀压印、慢慢揭纸三步，只做小块试印，不要求马上完成作品。教师提醒：“印完先不要说好不好看，先找哪里清楚，哪里模糊，和纸材、用力、颜料有什么关系。”

学生第一次试印时，常会出现颜料太多、太少或用力不均。若大面积糊印，教师可以立即拿一块小版现场示范：“颜料少一点，压力均一点，揭纸慢一点。”随后允许每组补一次小试印。若学生只盯着图案是否完整，教师追问：“你圈出的地方为什么最清楚？它和刚才的纸材预测一致吗？”

学生在试印纸上圈出最清楚或最有层次的一处，并写一句调整计划：“第一次试印最清楚的地方是……我想调整……”这样，下一次比较印法时，学生就有了可追踪的证据。

【设计意图】这一段把“纸材观察”推进到“印痕验证”。学生不只是做材料小样，而是在学习用试印结果修正判断。教师通过小样示范、暂停调整和圈画记录，帮助学生形成版画课最重要的习惯：边试、边看、边改。

大屏只放改造方法图、少量上色 / 均匀压印 / 慢揭纸三步和清楚 / 糊印对比。评价重点看学生是否保留改造小样和试印记录，并能说出一次调整理由。

### （三）比较与成作：把试验发现变成作品

#### 1. 看差异：干印、湿印与油印

在学生已有一次试印经验后，教师出示同一块版在不同印法下的效果。教师不急着讲术语，而是先问：“哪一种边缘更清楚？哪一种灰层更丰富？哪一种更适合你想要的画面？”

学生可能只记住干印、湿印、油印这些名称，却说不出差异。教师可以先遮住术语，只展示两张试印效果，请学生指出最大的不同，再把他们说出的清晰、模糊、灰层、浓淡对应到印法名称。每组只比较两种方法，避免一次展开过多术语。

学生完成一组同版不同印法对照，并写下选择理由：“我比较了……和……，我选择……，因为它让印痕……”这样进入作品阶段时，他们不是把所有方法都用上，而是带着理由选择。

#### 2. 做一做：用印痕完成作品

教师提出作品要求：“现在完成一幅小作品。你至少要保留一个自己满意的印痕，并说明它来自哪种纸材或印法。”学生根据前面的纸材预测、改造小样和印法对照，选择一到两种方法进入作品。

制作中，学生可能想把所有试过的材料都印上去，导致画面没有重点。教师可以请他们用手遮住部分区域，选择最想保留的一处印痕，再围绕它减少或调整其他痕迹。若学生为了完整图案覆盖掉了最有特色的痕迹，教师追问：“这幅作品最想让大家看到的印痕是哪一处？”

作品完成前，学生在学习单上补一句：“我最满意的印痕是……它来自……我保留它是因为……”这句话帮助他们把作品从“做完”推进到“能说明”。

【设计意图】本段让学生理解印法不是名称记忆，而是画面选择。通过同版对照和一主一辅的画面提示，学生把前面的材料试验转化为作品取舍，知道好作品不一定是痕迹最多，而是能看出纸材、印法和画面效果的关系。

大屏可出示同版不同印法对照图、一主一辅画面提示和印痕过多 / 重点清楚作品对比。评价重点看学生能否说明自己选择的纸材和印法，以及作品中至少一处有来源、有理由的印痕。

### （四）展评与收束：用证据介绍纸印作品

#### 1. 说一说：印痕展评与车间收束

展评时，教师要求每组同时带一件作品和一张试印记录上来。介绍时必须说清三件事：用了什么纸材，试了什么印法，留下了什么印痕。

学生容易把展评说成“我觉得它漂亮”“我喜欢这个颜色”。教师可以把评价改成找证据：“请你找一处最能说明纸材特点的印痕，先说证据，再贴星。”如果学生忘记带试印记录，教师提醒他们回到桌面找一张能说明调整过程的小样或记录，而不是只拿成品。

教师可给出展示句式：“我用了……纸，采用……印法，印出了……效果。同伴建议我……”学生完成介绍后，把作品和试印记录一起归档到“版画车间坊”。

【设计意图】最后一段把展示从“谁更漂亮”转为“谁能用证据说明作品”。作品、试印记录和学习单一起出现，说明学生不是只完成了一张纸印，而是经历了观察、预测、改造、试印、比较、取舍和表达的完整学习过程。

大屏可出示展示句式、纸材 / 印法 / 印痕 / 画面四类评价词和证据归档提醒。评价重点看学生是否能带着证据介绍作品，并能听取同伴建议继续调整。
"""


def build_evaluation_and_screen() -> str:
    rows = [
        ["入场观察", "能说出印痕和画线的一个不同", "学习单入场记录 / 口头说明"],
        ["纸材观察", "能用肌理词说明纸材预测", "纸材预测句"],
        ["纸材改造", "能说明自己用了什么方法制造肌理", "改造小样 + 方法记录"],
        ["第一次试印", "能圈出一处清楚或有层次的印痕，并提出调整", "试印记录"],
        ["印法比较", "能比较两种印法带来的效果差异", "同版对照记录"],
        ["作品完成", "作品中有一处能说明来源的印痕", "作品说明句"],
        ["展评收束", "能带着作品和试印证据进行介绍", "作品 + 试印记录归档"],
    ]
    return f"""## 七、评价设计

{md_table(["学习环节", "观察重点", "证据来源"], rows)}

本课评价不只看作品是否漂亮，更看学生是否能说清“纸材、印法和印痕效果”的关系。教师可以优先收集三类证据：纸材预测、试印调整、作品说明。只要学生能用证据解释一处印痕，就说明他们已经从普通纸手工进入了版画语言的学习。

## 八、板书 / 大屏结构

```text
有趣的纸印

纸材：厚薄 / 软硬 / 粗糙 / 光滑 / 凹凸
方法：刻、剪、撕、揉、卷、折、拼贴
试印：少量上色 - 均匀压印 - 慢慢揭纸
比较：清楚 / 模糊 / 灰层 / 肌理 / 边缘
表达：我用了……纸，采用……印法，印出了……效果
```

## 九、确认门

本稿仍为 preview-only。它只是把 R223N-P2 的课堂事件内容转译为教师文稿版，不写入正式备课本，不修改 R97B，不新增正式 UI，不接 runtime、provider/model、prompt 或数据库。
"""


def build_teacher_manuscript(chain: dict) -> str:
    events = chain["events"]
    return f"""# 《有趣的纸印》教师文稿版 v4

{render_meta("teacher_manuscript_grammar_aligned_draft")}

## 阅读说明

P3 不继续把课堂事件 ledger 直接排成教师稿，而是按成熟教案文稿的组织方式重新渲染：先看课时定位、目标、重难点和准备，再进入教学过程。学生可能反应、教师追问、补救策略、大屏、学习单和评价证据仍然保留，但被写进活动步骤、教师话术、学生活动、小结和【设计意图】中。完整控制点另见 review ledger。

{build_overview_tables(events)}

{process_text(events)}

{build_evaluation_and_screen()}
"""


def build_review_ledger_note(chain: dict) -> str:
    rows = []
    for event in chain["events"]:
        comp = event.get("component_trigger", {})
        screen = event.get("screen_trigger", {})
        sheet = event.get("learning_sheet_trigger", {})
        evidence = event.get("evidence_trigger", {})
        rows.append([
            event["event_id"],
            event["event_name"],
            comp.get("component_name", ""),
            screen.get("content", ""),
            sheet.get("field", ""),
            evidence.get("minimum_evidence", ""),
        ])
    return f"""# R223N-P3 Review Ledger Preservation Note

{render_meta("review_ledger_preservation_note")}

## 一、分层原则

P3 默认教师稿不显示完整 event_id、组件触发矩阵和控制点矩阵，但这些信息没有被删除。它们继续作为 review ledger 和后续大屏、学习单、评价证据生成的依据。

## 二、Ledger 保留摘要

{md_table(["event_id", "事件", "组件触发（审核层）", "大屏触发", "学习单字段", "最小证据"], rows)}

## 三、边界

默认稿可以把组件转成课堂动作，例如“两图对比”“摸猜材料”“步骤拆解”“圈画印痕”。审核层仍保留组件名和 component_id，供后续系统检查；正式 UI、R97B、runtime 和数据库仍然不接入。
"""


def build_before_after(p2_md: str, p3_md: str) -> str:
    p2_label_count = sum(p2_md.count(x) for x in P2_VISIBLE_LABELS)
    p3_label_count = sum(p3_md.count(x) for x in P2_VISIBLE_LABELS)
    p2_design = p2_md.count("【设计意图】")
    p3_design = p3_md.count("【设计意图】")
    rows = [
        ["默认结构", "课堂事件结构的人话版", "教师文稿文法稿", "从 event ledger 直排转为教案文稿"],
        ["P2 固定标题数量", str(p2_label_count), str(p3_label_count), "默认稿不再重复 P2 标题"],
        ["【设计意图】数量", str(p2_design), str(p3_design), "用教师熟悉的方式承载推理"],
        ["组件呈现", "部分保留组件名", "默认稿转成课堂动作，组件名退到 ledger", "避免工具货架感"],
        ["教学过程", "每个事件按同一结构展开", "按教学段落组织活动、话术、学生动作、小结", "更像成熟教案"],
        ["review ledger", "另有结构但默认稿仍像 ledger", "另文件保留完整触发摘要", "深度未丢"],
    ]
    return f"""# R223N-P3 Before / After Compare With P2

{render_meta("before_after_compare_with_p2")}

{md_table(["项目", "R223N-P2", "R223N-P3", "判断"], rows)}

## 结论

P2 解决的是字段去技术化，P3 解决的是教师文稿文法对齐。P3 没有删除课堂事件链，而是把事件内容分配到教师话术、学生活动、课堂调控、小结、【设计意图】、学习单和评价设计中。
"""


def build_report(p2_md: str, p3_md: str) -> str:
    label_count = sum(p3_md.count(x) for x in P2_VISIBLE_LABELS)
    backend_count = sum(p3_md.count(x) for x in BACKEND_TERMS)
    component_count = sum(p3_md.count(x) for x in COMPONENT_NAMES)
    return f"""# R223N-P3 教师文稿文法对齐报告

{render_meta("teacher_manuscript_grammar_alignment_report")}

## 一、当前判断

```text
R223N-P2 = PASS_LANGUAGE_HUMANIZATION_BUT_MANUSCRIPT_GRAMMAR_NOT_YET_PASS
R223N-P3 = TEACHER_MANUSCRIPT_GRAMMAR_ALIGNED
formal_ui = blocked
R97B / UI / runtime / prompt / model / db = untouched
```

## 二、对齐结果

```text
p2_visible_label_count_in_default={label_count}
backend_term_count_in_default={backend_count}
component_name_count_in_default={component_count}
design_intent_count={p3_md.count("【设计意图】")}
teacher_talk_signal={"教师：" in p3_md}
student_activity_signal={"学生" in p3_md}
screen_sheet_assessment_signal={"大屏" in p3_md and "学习单" in p3_md and "评价" in p3_md}
```

## 三、内容说明

- 默认教师稿新增课时定位、教学目标、重难点、准备、单课结构、评价设计和板书 / 大屏结构；
- 教学过程不再重复 P2 的固定标题，而是按活动步骤组织；
- 学生可能反应、教师追问、补救策略、投屏示范、学习单记录和评价证据没有删除；
- 组件名默认退到 review ledger，正文只保留对应课堂动作；
- 本包仍然只是静态内容产物，不授权正式 UI 或 runtime。
"""


def build_readme() -> str:
    return f"""# R223N-P3 Teacher Manuscript Grammar Alignment Review

{render_meta("review_package")}

## Open first

1. `R223N_P3_teacher_manuscript_draft_v4.html`
2. `R223N_P3_teacher_manuscript_draft_v4.md`
3. `R223N_P3_before_after_compare_with_P2.md`
4. `R223N_P3_review_ledger_preservation_note.md`

## Review question

Does P3 make the default teacher draft read like a mature lesson manuscript rather than a humanized backend event ledger, while preserving classroom event depth and review traceability?

## Boundaries

No R97B change, no formal UI, no frontend/backend change, no runtime/provider/model/prompt/db connection, no lesson body writeback, no formal apply.
"""


def md_to_html(md: str, title: str) -> str:
    lines = md.splitlines()
    out: list[str] = []
    in_code = False
    table_buf: list[str] = []

    def flush_table() -> None:
        nonlocal table_buf
        if not table_buf:
            return
        rows = []
        for row in table_buf:
            cells = [c.strip() for c in row.strip().strip("|").split("|")]
            rows.append(cells)
        if len(rows) >= 2:
            out.append("<table>")
            for i, cells in enumerate(rows):
                if i == 1 and all(set(c) <= {"-"} for c in cells):
                    continue
                tag = "th" if i == 0 else "td"
                out.append("<tr>" + "".join(f"<{tag}>{html.escape(c)}</{tag}>" for c in cells) + "</tr>")
            out.append("</table>")
        table_buf = []

    for raw in lines:
        line = raw.rstrip()
        if line.startswith("```"):
            flush_table()
            if in_code:
                out.append("</pre>")
            else:
                out.append("<pre>")
            in_code = not in_code
            continue
        if in_code:
            out.append(html.escape(line) + "\n")
            continue
        if line.startswith("|") and line.endswith("|"):
            table_buf.append(line)
            continue
        flush_table()
        if not line:
            continue
        if line.startswith("# "):
            out.append(f"<h1>{html.escape(line[2:])}</h1>")
        elif line.startswith("## "):
            out.append(f"<h2>{html.escape(line[3:])}</h2>")
        elif line.startswith("### "):
            out.append(f"<h3>{html.escape(line[4:])}</h3>")
        elif line.startswith("#### "):
            out.append(f"<h4>{html.escape(line[5:])}</h4>")
        elif line.startswith("【设计意图】"):
            out.append(f"<p class='intent'><strong>【设计意图】</strong>{html.escape(line[len('【设计意图】'):])}</p>")
        elif line.startswith("- "):
            out.append(f"<p class='bullet'>• {html.escape(line[2:])}</p>")
        elif re.match(r"^\d+\.", line):
            out.append(f"<p class='numbered'>{html.escape(line)}</p>")
        else:
            text = html.escape(line)
            text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
            out.append(f"<p>{text}</p>")
    flush_table()

    css = """
body { margin: 0; background: #f3f5f2; color: #1f2b27; font-family: "Microsoft YaHei", "Noto Sans SC", Arial, sans-serif; }
.page { width: min(980px, calc(100vw - 64px)); margin: 32px auto 56px; background: #fffef9; padding: 56px 64px; box-shadow: 0 12px 36px rgba(24,52,44,.10); border: 1px solid #dfe8df; }
h1 { text-align: center; font-size: 30px; margin: 0 0 28px; letter-spacing: 0; }
h2 { font-size: 22px; margin: 34px 0 16px; padding-top: 18px; border-top: 1px solid #dce7df; color: #176b5f; }
h3 { font-size: 20px; margin: 30px 0 14px; color: #20342e; }
h4 { font-size: 17px; margin: 20px 0 8px; color: #122922; }
p { font-size: 15px; line-height: 1.9; margin: 9px 0; }
.intent { border-left: 4px solid #2f8d7d; background: #f4fbf8; padding: 12px 16px; margin: 15px 0; }
.bullet, .numbered { margin-left: 1em; }
table { width: 100%; border-collapse: collapse; margin: 14px 0 22px; font-size: 14px; }
th, td { border: 1px solid #bdccc4; padding: 10px 12px; vertical-align: top; line-height: 1.65; }
th { background: #eef7f3; }
pre { background: #f6f7f4; border: 1px solid #d7dfd8; padding: 14px; white-space: pre-wrap; word-break: break-word; font-size: 13px; line-height: 1.6; }
@media (max-width: 760px) { .page { width: auto; margin: 0; padding: 28px 20px 40px; border: none; box-shadow: none; } h1 { font-size: 24px; } }
"""
    return f"<!doctype html><html lang='zh-CN'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'><title>{html.escape(title)}</title><style>{css}</style></head><body><main class='page'>{''.join(out)}</main></body></html>"


REQUIRED = [
    "R223N_P3_gold_manuscript_grammar_analysis.md",
    "R223N_P3_event_to_manuscript_rendering_rules.md",
    "R223N_P3_teacher_manuscript_draft_v4.md",
    "R223N_P3_teacher_manuscript_draft_v4.html",
    "R223N_P3_review_ledger_preservation_note.md",
    "R223N_P3_before_after_compare_with_P2.md",
    "R223N_P3_report.md",
    "validate_1013R_R223N_P3_teacher_manuscript_grammar_alignment.py",
    "PACKAGE_MANIFEST.json",
    "README_FOR_GPT_REVIEW.md",
]


VALIDATOR = r'''from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

REQUIRED = [
    "R223N_P3_gold_manuscript_grammar_analysis.md",
    "R223N_P3_event_to_manuscript_rendering_rules.md",
    "R223N_P3_teacher_manuscript_draft_v4.md",
    "R223N_P3_teacher_manuscript_draft_v4.html",
    "R223N_P3_review_ledger_preservation_note.md",
    "R223N_P3_before_after_compare_with_P2.md",
    "R223N_P3_report.md",
    "validate_1013R_R223N_P3_teacher_manuscript_grammar_alignment.py",
    "PACKAGE_MANIFEST.json",
    "README_FOR_GPT_REVIEW.md",
]

P2_VISIBLE_LABELS = [
    "这一环节要解决什么",
    "上课时可以这样展开",
    "如果学生卡住",
    "留下什么，再往哪走",
    "大屏、学习单和评价怎么跟上",
]

BACKEND_TERMS = [
    "event_id",
    "teaching_responsibility",
    "student_problem",
    "task_release",
    "expected_student_responses",
    "likely_misconceptions",
    "teacher_follow_up",
    "teacher_rescue_strategy",
    "component_trigger",
    "screen_trigger",
    "learning_sheet_trigger",
    "evidence_trigger",
]

COMPONENT_NAMES = ["比一比", "材料盲盒", "技法拆解", "圈一圈", "中途看一看", "作品画廊"]
BOUNDARY_FALSE = [
    "formal_ui_changed",
    "r97b_changed",
    "frontend_backend_changed",
    "runtime_connected",
    "provider_model_connected",
    "prompt_changed",
    "database_changed",
    "formal_apply_allowed",
]


def clean_code(md: str) -> str:
    return re.sub(r"```.*?```", "", md, flags=re.S)


def check(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def main() -> int:
    failures: list[str] = []
    check_count = 0
    for name in REQUIRED:
        check_count += 1
        check((ROOT / name).exists(), f"missing {name}", failures)

    md = (ROOT / "R223N_P3_teacher_manuscript_draft_v4.md").read_text(encoding="utf-8")
    html = (ROOT / "R223N_P3_teacher_manuscript_draft_v4.html").read_text(encoding="utf-8")
    ledger = (ROOT / "R223N_P3_review_ledger_preservation_note.md").read_text(encoding="utf-8")
    rules = (ROOT / "R223N_P3_event_to_manuscript_rendering_rules.md").read_text(encoding="utf-8")
    compare = (ROOT / "R223N_P3_before_after_compare_with_P2.md").read_text(encoding="utf-8")
    manifest = json.loads((ROOT / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
    body = clean_code(md)

    label_count = sum(body.count(x) for x in P2_VISIBLE_LABELS)
    backend_count = sum(body.count(x) for x in BACKEND_TERMS)
    component_count = sum(body.count(x) for x in COMPONENT_NAMES)

    checks = [
        (md.count("### （") == 4, "expected 4 manuscript process stages"),
        (md.count("#### ") >= 7, "expected at least 7 activity steps"),
        (md.count("【设计意图】") >= 4, "expected design intent blocks"),
        ("## 七、评价设计" in md and "## 八、板书 / 大屏结构" in md, "evaluation or screen structure missing"),
        ("教师：" in md, "teacher talk signal missing"),
        ("学生" in md and "学习单" in md and "评价" in md and "大屏" in md, "student/sheet/assessment/screen signals missing"),
        (label_count == 0, f"P2 visible labels remain in default draft: {label_count}"),
        (backend_count == 0, f"backend terms leaked into default draft: {backend_count}"),
        (component_count == 0, f"component names leaked into default draft: {component_count}"),
        ("event_id" in ledger and "组件触发" in ledger and "最小证据" in ledger, "review ledger preservation is incomplete"),
        ("teaching_responsibility" in rules and "教师稿位置" in rules, "rendering rules missing field mapping"),
        ("P2 是结构化人话稿" in compare or "P2 解决的是字段去技术化" in compare, "before/after contrast missing"),
        ("<table>" in html and "class='intent'" in html, "html lacks manuscript rendering"),
    ]
    for condition, message in checks:
        check_count += 1
        check(condition, message, failures)

    boundary = manifest.get("boundary", {})
    for key in BOUNDARY_FALSE:
        check_count += 1
        check(boundary.get(key) is False, f"boundary {key} must be false", failures)

    check_count += 1
    check(manifest.get("preview_only") is True, "preview_only must be true", failures)

    result = {
        "passed": not failures,
        "check_count": check_count,
        "failed": len(failures),
        "failures": failures,
        "p2_visible_label_count_in_default": label_count,
        "backend_term_count_in_default": backend_count,
        "component_name_count_in_default": component_count,
        "design_intent_count": md.count("【设计意图】"),
        "activity_step_count": md.count("#### "),
    }
    (ROOT / "validate_1013R_R223N_P3_teacher_manuscript_grammar_alignment_result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
'''


def write(name: str, content: str) -> None:
    (ROOT / name).write_text(content, encoding="utf-8")


def main() -> int:
    chain = load_chain()
    p2_md = P2_PATH.read_text(encoding="utf-8")
    p3_md = build_teacher_manuscript(chain)

    write("R223N_P3_gold_manuscript_grammar_analysis.md", build_grammar_analysis())
    write("R223N_P3_event_to_manuscript_rendering_rules.md", build_rendering_rules())
    write("R223N_P3_teacher_manuscript_draft_v4.md", p3_md)
    write("R223N_P3_teacher_manuscript_draft_v4.html", md_to_html(p3_md, "R223N-P3 有趣的纸印教师文稿版 v4"))
    write("R223N_P3_review_ledger_preservation_note.md", build_review_ledger_note(chain))
    write("R223N_P3_before_after_compare_with_P2.md", build_before_after(p2_md, p3_md))
    write("R223N_P3_report.md", build_report(p2_md, p3_md))
    write("validate_1013R_R223N_P3_teacher_manuscript_grammar_alignment.py", VALIDATOR)

    manifest = {
        "stage_id": STAGE_ID,
        "source_stage_id": SOURCE_STAGE_ID,
        "standard_id": STANDARD_ID,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "preview_only": True,
        "change_type": "teacher_manuscript_grammar_alignment_only",
        "source_sample": "有趣的纸印",
        "gold_grammar_reference": "我为文具代言 manuscript organization screenshots and prior R223M standard",
        "outputs": REQUIRED + ["validate_1013R_R223N_P3_teacher_manuscript_grammar_alignment_result.json"],
        "boundary": {
            "formal_ui_changed": False,
            "r97b_changed": False,
            "frontend_backend_changed": False,
            "runtime_connected": False,
            "provider_model_connected": False,
            "prompt_changed": False,
            "database_changed": False,
            "formal_apply_allowed": False,
        },
    }
    write("PACKAGE_MANIFEST.json", json.dumps(manifest, ensure_ascii=False, indent=2))
    write("README_FOR_GPT_REVIEW.md", build_readme())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
