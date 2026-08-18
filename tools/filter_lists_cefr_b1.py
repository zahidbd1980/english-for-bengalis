# -*- coding: utf-8 -*-
"""Remove A1/A2 items from vocabulary + verb-form lists. Audience is B1+."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from cefr_policy import (  # noqa: E402
    BEGINNER_ONLY_LIST_IDS,
    filter_list_ids,
    keep_word,
    list_cefr_label,
)

VOCAB = ROOT / "data" / "vocabulary.json"
VERBS = ROOT / "data" / "verb-forms.json"
VLISTS = ROOT / "data" / "vocabulary-lists.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def index_entries(rows: list) -> dict:
    return {row.get("id"): row for row in rows if row.get("id")}


def filter_ids(ids: list, lookup: dict) -> list[str]:
    return filter_list_ids(ids, lookup)


def refill_from_bank(kept: list[str], lookup: dict, bank: list, max_n: int | None = None) -> list[str]:
    """If a list shrank, add more B1+ items from the same categories as remaining words."""
    if max_n is None:
        max_n = max(40, len(kept))
    cats = set()
    for wid in kept:
        entry = lookup.get(wid) or {}
        cat = (entry.get("category") or "").strip().lower()
        if cat:
            cats.add(cat)
    seen = set(kept)
    extra = []
    for w in bank:
        wid = w.get("id")
        if not wid or wid in seen:
            continue
        if not keep_word(w):
            continue
        cat = (w.get("category") or "").strip().lower()
        if cats and cat not in cats:
            continue
        extra.append(wid)
        seen.add(wid)
        if len(kept) + len(extra) >= max_n:
            break
    return kept + extra


def main() -> None:
    vocab = load(VOCAB)
    verbs = load(VERBS)
    meta = load(VLISTS)
    lookup = {}
    lookup.update(index_entries(vocab))
    lookup.update(index_entries(verbs))

    reports = []
    kept_lists = []
    for L in meta.get("lists") or []:
        lid = str(L.get("id") or "")
        before = list(L.get("word_ids") or [])
        if lid in BEGINNER_ONLY_LIST_IDS:
            reports.append((lid, len(before), 0, "dropped"))
            continue
        kept = filter_ids(before, lookup)
        is_verb_list = any(str(i).startswith("verb:") for i in before) or lid.startswith(
            ("vf-", "verb-forms")
        )
        if not is_verb_list and len(kept) < max(20, int(len(before) * 0.45)):
            kept = refill_from_bank(kept, lookup, vocab, max_n=max(len(before), 40))
        if not kept:
            reports.append((lid, len(before), 0, "empty"))
            continue
        L["word_ids"] = kept
        L["cefr"] = list_cefr_label(L.get("cefr"))
        kept_lists.append(L)
        reports.append((lid, len(before), len(kept), "ok"))

    meta["lists"] = kept_lists
    save(VLISTS, meta)
    print("id\tbefore\tafter\tnote")
    for row in reports:
        lid, b, a, note = row
        flag = " !" if a < 10 else ""
        print(f"{lid}\t{b}\t{a}{flag}\t{note}")


if __name__ == "__main__":
    main()
