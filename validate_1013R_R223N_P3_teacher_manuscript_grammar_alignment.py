from __future__ import annotations

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
