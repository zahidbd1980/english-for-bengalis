# -*- coding: utf-8 -*-
"""Simulate progress tracking integrity (no browser)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    vocab = json.loads((ROOT / "data" / "vocabulary.json").read_text(encoding="utf-8"))
    quizzes = json.loads((ROOT / "data" / "quizzes.json").read_text(encoding="utf-8"))
    migrate = json.loads((ROOT / "data" / "progress_id_migrate.json").read_text(encoding="utf-8"))
    grammar = json.loads((ROOT / "data" / "grammar.json").read_text(encoding="utf-8"))

    # 1) Schema / id integrity
    bad_id = [w["id"] for w in vocab if not str(w["id"]).startswith("vocab:")]
    bad_schema = [
        w["id"]
        for w in vocab
        if not w.get("cefr_level") or not w.get("part_of_speech") or not w.get("category")
    ]
    assert not bad_id, bad_id[:5]
    assert not bad_schema, bad_schema[:5]
    assert len(vocab) == 300
    assert len(migrate) == 76

    by_id = {w["id"]: w for w in vocab}

    # 2) Simulate user learning 5 words via markSeen + quiz recordResult
    STATUS = {"SEEN": 1, "PRACTICED": 3, "MASTERED": 5}
    items = {}

    def ensure(item_id):
        if item_id not in items:
            items[item_id] = {
                "status": 0,
                "mastery_score": 0,
                "attempts": 0,
                "correct_count": 0,
                "wrong_count": 0,
                "productive_correct": 0,
                "reps": 0,
                "recent": [],
            }
        return items[item_id]

    def mark_seen(item_id):
        it = ensure(item_id)
        if it["mastery_score"] < 10:
            it["mastery_score"] = 10
        if it["status"] == 0:
            it["status"] = STATUS["SEEN"]

    def record_result(item_id, correct, fmt="mcq"):
        it = ensure(item_id)
        it["attempts"] += 1
        it["recent"].append(correct)
        if correct:
            it["correct_count"] += 1
            gain = 12 if fmt == "type" else 8
            if fmt in ("type", "translate"):
                it["productive_correct"] += 1
            it["mastery_score"] = min(100, it["mastery_score"] + gain)
            if it["status"] < STATUS["PRACTICED"]:
                it["status"] = STATUS["PRACTICED"]
            it["reps"] += 1
        else:
            it["wrong_count"] += 1
            it["mastery_score"] = max(0, it["mastery_score"] - 15)

    sample = [w["id"] for w in vocab[:5]]
    for vid in sample:
        mark_seen(vid)
    # flashcard know
    record_result(sample[0], True, "mcq")
    record_result(sample[0], True, "mcq")
    # quiz type
    q_vocab = [q for q in quizzes if q.get("skill") == "vocabulary" and q.get("item_id") in by_id]
    assert q_vocab, "no vocabulary quizzes with matching item_id"
    record_result(q_vocab[0]["item_id"], True, "mcq")

    started = sum(1 for w in vocab if items.get(w["id"], {}).get("status", 0) > 0)
    practiced = sum(1 for w in vocab if items.get(w["id"], {}).get("status", 0) >= 3)
    assert started >= 5, started
    assert practiced >= 1, practiced

    # 3) Grammar topic ids match deep-links
    g_ids = {g["id"] for g in grammar}
    g_quizzes = [q for q in quizzes if q.get("skill") == "grammar"]
    linked = [q for q in g_quizzes if q.get("item_id") in g_ids]
    assert linked, "grammar quizzes should use grammar:* item_ids"

    # 4) Migration remaps legacy keys into countable ids
    legacy_state = {"v227": {"status": 1, "mastery_score": 10}}
    mapped = {}
    for old, val in legacy_state.items():
        mapped[migrate.get(old, old)] = val
    assert "vocab:agree" in mapped
    assert mapped["vocab:agree"]["status"] == 1
    assert "vocab:agree" in by_id

    target = 2000
    print("OK progress integrity")
    print("  vocab bank", len(vocab))
    print("  simulated started", started, "practiced", practiced)
    print("  vocab quizzes matched", len(q_vocab))
    print("  grammar quizzes linked", len(linked), "/", len(g_quizzes))
    print("  personal target example", f"{started}/{target}")


if __name__ == "__main__":
    main()
