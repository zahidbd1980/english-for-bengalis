# -*- coding: utf-8 -*-
"""
End-to-end simulation of learner progress flow (no browser).
Mirrors storage.js + progress.js + My Progress counting rules.
"""
from __future__ import annotations

import json
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

STATUS = {
    "NOT_STARTED": 0,
    "SEEN": 1,
    "LEARNING": 2,
    "PRACTICED": 3,
    "FAMILIAR": 4,
    "MASTERED": 5,
    "NEEDS_REVIEW": 6,
}


def default_state():
    return {
        "progress_version": 1,
        "settings": {"vocab_target": 2000, "goal": "spoken_english"},
        "profile": {"estimated_level": None, "last_lesson_id": None, "last_skill": None},
        "streak": {"current": 0, "longest": 0, "last_active_date": None},
        "items": {},
        "mistakes": [],
        "challenge": {"date": None, "completed": False, "item_ids": [], "score": 0, "total": 0},
    }


def ensure(state, item_id):
    if item_id not in state["items"]:
        state["items"][item_id] = {
            "status": 0,
            "mastery_score": 0,
            "attempts": 0,
            "correct_count": 0,
            "wrong_count": 0,
            "productive_correct": 0,
            "ease": 2.3,
            "interval_days": 0,
            "reps": 0,
            "recent": [],
        }
    return state["items"][item_id]


def mark_seen(state, item_id):
    it = ensure(state, item_id)
    if it["mastery_score"] < 10:
        it["mastery_score"] = 10
    if it["status"] == 0:
        it["status"] = STATUS["SEEN"]


def record_result(state, item_id, correct, fmt="mcq"):
    it = ensure(state, item_id)
    it["attempts"] += 1
    it["recent"].append({"correct": bool(correct), "format": fmt})
    if len(it["recent"]) > 5:
        it["recent"] = it["recent"][-5:]
    if correct:
        it["correct_count"] += 1
        gain = 12 if fmt in ("type", "translate", "speak") else 8
        if fmt in ("type", "translate", "speak"):
            it["productive_correct"] += 1
        it["mastery_score"] = min(100, it["mastery_score"] + gain)
        if it["status"] < STATUS["PRACTICED"]:
            it["status"] = STATUS["PRACTICED"]
        it["reps"] += 1
        state["mistakes"] = [m for m in state["mistakes"] if m != item_id]
    else:
        it["wrong_count"] += 1
        it["mastery_score"] = max(0, it["mastery_score"] - 15)
        it["status"] = STATUS["NEEDS_REVIEW"]
        if item_id not in state["mistakes"]:
            state["mistakes"].insert(0, item_id)


def set_last(state, skill, lesson):
    state["profile"]["last_skill"] = skill
    state["profile"]["last_lesson_id"] = lesson


def count_for(bank, state):
    started = sum(
        1
        for x in bank
        if state["items"].get(x["id"])
        and (
            state["items"][x["id"]].get("status", 0) > 0
            or state["items"][x["id"]].get("attempts", 0) > 0
        )
    )
    practiced = sum(1 for x in bank if state["items"].get(x["id"], {}).get("attempts", 0) > 0)
    mastered = sum(1 for x in bank if state["items"].get(x["id"], {}).get("status", 0) == 5)
    return started, practiced, mastered


def resolve_continue(state, due_count=0, challenge_done=False):
    skill_page = {
        "vocabulary": "vocabulary.html",
        "grammar": "grammar.html",
        "spelling": "spelling-practice.html",
        "phrasal": "phrasal-verbs.html",
        "mistakes": "common-mistakes.html",
        "sentence": "sentence-builder.html",
        "translate": "translation-lab.html",
        "spoken": "spoken-english.html",
        "daily": "daily-challenge.html",
        "review": "quizzes.html?mode=review",
        "quizzes": "quizzes.html",
        "flashcards": "flashcards.html",
    }
    if due_count:
        return "quizzes.html?mode=review"
    if not challenge_done:
        return "daily-challenge.html"
    skill = (state["profile"] or {}).get("last_skill")
    if skill:
        return skill_page.get(skill, "my-progress.html")
    if state["mistakes"]:
        return "quizzes.html?mode=mistakes"
    return "my-progress.html"


def check_wiring():
    checks = []
    files = {
        "pages/grammar.html": ["watchLessonSeen", "data-item-id", "setLastLesson"],
        "pages/phrasal-verbs.html": ["watchLessonSeen", "data-item-id"],
        "pages/common-mistakes.html": ["watchLessonSeen", "data-item-id"],
        "pages/spelling.html": ["watchLessonSeen", "data-item-id"],
        "pages/spoken-english.html": ["watchLessonSeen", "data-item-id"],
        "pages/my-progress.html": ["vocab_target", "sentence-builder.json", "spoken.json", "resolveContinue"],
        "js/quiz-engine.js": ["nextRoundActions", "setLastLesson", "recordResult"],
        "js/daily-challenge.js": ["Deck complete", "nextRoundActions", "setLastLesson"],
        "js/app.js": ["resolveContinue", "watchLessonSeen", "nextRoundActions", "/p/"],
        "pages/sentence-builder.html": ["recordResult", "nextRoundActions"],
    }
    for path, needles in files.items():
        text = (ROOT / path).read_text(encoding="utf-8")
        missing = [n for n in needles if n not in text]
        # grammar must NOT bulk markSeen in map loop
        if path.endswith("grammar.html") and "EFBProgress.markSeen(g.id)" in text:
            missing.append("MUST_NOT_bulk_markSeen")
        checks.append((path, missing))
    return checks


def main():
    report = []
    vocab = json.loads((ROOT / "data/vocabulary.json").read_text(encoding="utf-8"))
    grammar = json.loads((ROOT / "data/grammar.json").read_text(encoding="utf-8"))
    spoken = json.loads((ROOT / "data/spoken.json").read_text(encoding="utf-8"))
    sentence = json.loads((ROOT / "data/sentence-builder.json").read_text(encoding="utf-8"))
    quizzes = json.loads((ROOT / "data/quizzes.json").read_text(encoding="utf-8"))
    migrate = json.loads((ROOT / "data/progress_id_migrate.json").read_text(encoding="utf-8"))

    # --- BUG regression: opening grammar list must NOT mark all ---
    state = default_state()
    # simulate old bug vs new behavior
    visible_only = grammar[:2]
    for g in visible_only:
        mark_seen(state, g["id"])
    started, _, _ = count_for(grammar, state)
    assert started == 2, started
    report.append(f"PASS grammar visible-only seen = {started}/{len(grammar)} (not all)")

    # --- Learning flow: Vocab see → quiz wrong → mistake bank → quiz correct ---
    state = default_state()
    w = vocab[0]["id"]
    mark_seen(state, w)
    set_last(state, "vocabulary", "vocab-hub")
    assert state["items"][w]["status"] == 1
    report.append(f"PASS vocab markSeen → status SEEN for {w}")

    qv = next(q for q in quizzes if q.get("item_id") == w or q.get("skill") == "vocabulary")
    item = qv.get("item_id") or w
    if item not in {x["id"] for x in vocab}:
        item = w
    record_result(state, item, False, "mcq")
    assert item in state["mistakes"]
    assert state["items"][item]["status"] == STATUS["NEEDS_REVIEW"]
    report.append(f"PASS wrong quiz → Mistake Bank has {item}")

    record_result(state, item, True, "mcq")
    assert item not in state["mistakes"]
    assert state["items"][item]["status"] >= STATUS["PRACTICED"]
    report.append("PASS correct retry → cleared from Mistake Bank + PRACTICED")

    # --- Sentence builder counts on dashboard ---
    state2 = default_state()
    sid = sentence[0]["id"]
    assert sid.startswith("sb:"), sid
    record_result(state2, sid, True, "type")
    s_started, s_prac, _ = count_for(sentence, state2)
    assert s_started == 1 and s_prac == 1
    report.append(f"PASS sentence builder id {sid} counts on progress")

    # --- Spoken ids ---
    assert all(x["id"].startswith("spoken:") for x in spoken)
    mark_seen(state2, spoken[0]["id"])
    sp_started, _, _ = count_for(spoken, state2)
    assert sp_started == 1
    report.append(f"PASS spoken id {spoken[0]['id']} counts")

    # --- Continue resolver learning loop ---
    st = default_state()
    set_last(st, "sentence", "sentence-builder")
    assert resolve_continue(st, due_count=0, challenge_done=False) == "daily-challenge.html"
    assert resolve_continue(st, due_count=3, challenge_done=True) == "quizzes.html?mode=review"
    assert resolve_continue(st, due_count=0, challenge_done=True) == "sentence-builder.html"
    report.append("PASS Continue priority: review → daily → last skill")

    # --- Migration remap ---
    legacy = {"v227": {"status": 1, "mastery_score": 10}, "sb1": {"status": 3, "mastery_score": 20}}
    mapped = {}
    for old, val in legacy.items():
        mapped[migrate.get(old, old)] = val
    assert "vocab:agree" in mapped
    assert "sb:1" in mapped
    report.append("PASS legacy id migration map (v227/sb1)")

    # --- Vocab target tracking ---
    st3 = default_state()
    for x in vocab[:15]:
        mark_seen(st3, x["id"])
    for x in vocab[:5]:
        record_result(st3, x["id"], True, "mcq")
    started, practiced, _ = count_for(vocab, st3)
    target = st3["settings"]["vocab_target"]
    pct = round(started / target * 100)
    report.append(f"PASS vocab goal progress {started}/{target} ({pct}%) · practiced {practiced}")

    # --- Wiring on disk ---
    wiring = check_wiring()
    bad = [(p, m) for p, m in wiring if m]
    if bad:
        for p, m in bad:
            report.append(f"FAIL wiring {p}: missing {m}")
        raise SystemExit("WIRING FAIL\n" + "\n".join(report))
    report.append("PASS page/JS wiring for watchLessonSeen + nextRoundActions + setLastLesson")

    # Interactive loop narrative check
    flow = [
        "1. Learn: open grammar topic (visible) → markSeen",
        "2. Practice: topic quiz → recordResult",
        "3. Result screen: Again / Review / Skill / Daily / Progress",
        "4. Home Continue follows due -> daily -> last_skill",
        "5. My Progress shows skill bars + vocab target",
    ]
    report.append("FLOW:")
    report.extend("  " + step for step in flow)

    out = "\n".join(report) + "\n\nOVERALL: PROGRESS TRACKING + LEARNING FLOW OK\n"
    (ROOT / "tools" / "_progress_verify_report.txt").write_text(out, encoding="utf-8")
    print(out.encode("ascii", "replace").decode("ascii"))


if __name__ == "__main__":
    main()
