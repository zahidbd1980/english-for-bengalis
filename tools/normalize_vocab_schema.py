# -*- coding: utf-8 -*-
"""Normalize vocabulary bank IDs/schema so progress tracking matches quizzes."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VP = ROOT / "data" / "vocabulary.json"
MIG = ROOT / "data" / "progress_id_migrate.json"

TAG_TO_CAT = {
    "daily": "daily",
    "study": "study",
    "work": "work",
    "health": "health",
    "shopping": "shopping",
    "academic": "academic",
    "formal": "formal",
    "culture": "culture",
}


def slug_word(word: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (word or "").lower().strip())
    return s.strip("-") or "word"


def normalize_entry(w: dict, migrate: dict) -> dict:
    old_id = str(w.get("id") or "")
    word = w.get("word") or ""
    new_id = old_id if old_id.startswith("vocab:") else f"vocab:{slug_word(word)}"
    if old_id and old_id != new_id:
        migrate[old_id] = new_id

    out = dict(w)
    out["id"] = new_id
    # Canonical teacher schema fields
    if "cefr_level" not in out and "cefr" in out:
        out["cefr_level"] = out.pop("cefr")
    elif "cefr" in out and "cefr_level" in out:
        out.pop("cefr", None)

    if "part_of_speech" not in out and "pos" in out:
        out["part_of_speech"] = out.pop("pos")
    elif "pos" in out and "part_of_speech" in out:
        out.pop("pos", None)

    if not out.get("category"):
        tags = out.get("tags") or []
        cat = "general"
        for t in tags:
            if t in TAG_TO_CAT:
                cat = TAG_TO_CAT[t]
                break
        out["category"] = cat

    out.setdefault("synonyms", [])
    out.setdefault("antonyms", [])
    out.setdefault("word_family", [])
    # Keep phonetic/tags if present; harmless extras
    return out


def main():
    vocab = json.loads(VP.read_text(encoding="utf-8"))
    migrate = {}
    fixed = [normalize_entry(w, migrate) for w in vocab]

    # Ensure unique ids
    seen = set()
    for w in fixed:
        if w["id"] in seen:
            raise SystemExit(f"duplicate id after normalize: {w['id']}")
        seen.add(w["id"])

    VP.write_text(json.dumps(fixed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    MIG.write_text(json.dumps(migrate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("vocab", len(fixed))
    print("migrated ids", len(migrate))
    print("still non-prefixed", sum(1 for w in fixed if not w["id"].startswith("vocab:")))
    print("missing category", sum(1 for w in fixed if not w.get("category")))
    print("missing cefr_level", sum(1 for w in fixed if not w.get("cefr_level")))
    print("missing pos", sum(1 for w in fixed if not w.get("part_of_speech")))


if __name__ == "__main__":
    main()
