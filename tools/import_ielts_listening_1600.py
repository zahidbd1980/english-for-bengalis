# -*- coding: utf-8 -*-
"""Import IELTS Listening 1600 words -> vocab bank + vocab list + spelling list."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "various words lists" / "ielts-listening-1600-words.json"
VOCAB = ROOT / "data" / "vocabulary.json"
VLISTS = ROOT / "data" / "vocabulary-lists.json"
SLISTS = ROOT / "data" / "spelling-lists.json"

CEFR = {"A1", "A2", "B1", "B2", "C1", "C2"}
CAT_OK = {
    "home", "office", "outdoor", "nature", "food", "travel", "health",
    "education", "verbs", "shopping", "technology", "daily", "ielts",
}
CAT_MAP = {
    "academic": "ielts",
    "work": "office",
    "study": "education",
    "formal": "office",
    "culture": "daily",
    "general": "daily",
}


def slug_id(word: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", word.strip().lower()).strip("-")
    return f"vocab:{s or 'word'}"


def normalize_entry(raw: dict) -> dict:
    word = str(raw.get("word") or "").strip()
    eid = str(raw.get("id") or "").strip() or slug_id(word)
    if not eid.startswith("vocab:"):
        eid = slug_id(word)

    cat = str(raw.get("category") or "ielts").strip().lower()
    cat = CAT_MAP.get(cat, cat)
    if cat not in CAT_OK:
        cat = "ielts"

    cefr = str(raw.get("cefr_level") or "A2").strip().upper()
    if cefr not in CEFR:
        cefr = "A2"

    fam = []
    for f in raw.get("word_family") or []:
        if not isinstance(f, dict):
            continue
        fw = f.get("word") or f.get("form")
        pos = f.get("pos") or f.get("part_of_speech") or "noun"
        bn = f.get("meaning_bn") or f.get("bn") or ""
        if fw and bn:
            fam.append({"word": str(fw).strip(), "pos": str(pos).strip(), "meaning_bn": str(bn).strip()})
    fam = fam[:4]

    syn = [str(x).strip() for x in (raw.get("synonyms") or []) if str(x).strip()][:3]
    ant = [str(x).strip() for x in (raw.get("antonyms") or []) if str(x).strip()][:3]
    tags = list(raw.get("tags") or [])
    if "ielts" not in tags:
        tags.append("ielts")
    if "listening" not in tags:
        tags.append("listening")

    return {
        "id": eid,
        "word": word,
        "phonetic": raw.get("phonetic") or "",
        "meaning_en": str(raw.get("meaning_en") or "").strip() or word,
        "meaning_bn": str(raw.get("meaning_bn") or "").strip() or word,
        "part_of_speech": str(raw.get("part_of_speech") or "noun").strip() or "noun",
        "cefr_level": cefr,
        "category": cat,
        "example": str(raw.get("example") or "").strip() or f"I learned the word '{word}'.",
        "example_bn": str(raw.get("example_bn") or "").strip() or f"আমি '{word}' শব্দটি শিখেছি।",
        "synonyms": syn,
        "antonyms": ant,
        "word_family": fam,
        "tags": tags,
    }


def merge_vocab(incoming: list[dict]) -> tuple[int, int, list[str]]:
    bank = json.loads(VOCAB.read_text(encoding="utf-8"))
    by_id = {w["id"]: i for i, w in enumerate(bank)}
    by_word = {w["word"].lower(): i for i, w in enumerate(bank)}
    added = updated = 0
    ids = []
    for raw in incoming:
        e = normalize_entry(raw)
        if not e["word"]:
            continue
        ids.append(e["id"])
        if e["id"] in by_id:
            i = by_id[e["id"]]
            cur = bank[i]
            for k, v in e.items():
                if k in ("synonyms", "antonyms", "word_family", "tags"):
                    if v:
                        cur[k] = v
                elif v not in ("", None):
                    cur[k] = v
            bank[i] = cur
            updated += 1
        elif e["word"].lower() in by_word:
            i = by_word[e["word"].lower()]
            # keep existing id; still enrich
            cur = bank[i]
            ids[-1] = cur["id"]
            for k, v in e.items():
                if k == "id":
                    continue
                if k in ("synonyms", "antonyms", "word_family", "tags"):
                    if v:
                        cur[k] = v
                elif v not in ("", None):
                    cur[k] = v
            bank[i] = cur
            updated += 1
        else:
            if not e.get("phonetic"):
                e.pop("phonetic", None)
            bank.append(e)
            by_id[e["id"]] = len(bank) - 1
            by_word[e["word"].lower()] = len(bank) - 1
            added += 1
    VOCAB.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # unique preserve order
    seen = set()
    uniq = []
    for i in ids:
        if i not in seen:
            seen.add(i)
            uniq.append(i)
    return added, updated, uniq


def upsert_vocab_list(word_ids: list[str]) -> None:
    meta = json.loads(VLISTS.read_text(encoding="utf-8"))
    lists = meta.get("lists") or []
    entry = {
        "id": "ielts-listening-1600",
        "title": "IELTS Listening · 1600 Words",
        "title_bn": "IELTS লিসেনিং · ১৬০০ শব্দ",
        "description": "High-frequency IELTS Listening spellings/vocabulary (unofficial practice).",
        "description_bn": "IELTS Listening-এ বহুল ব্যবহৃত শব্দ ও বানান (অনঅফিসিয়াল প্র্যাকটিস)।",
        "cefr": "A1–B2",
        "word_ids": word_ids,
    }
    replaced = False
    for i, L in enumerate(lists):
        if L.get("id") == entry["id"]:
            lists[i] = entry
            replaced = True
            break
    if not replaced:
        lists.append(entry)
    # ensure ielts category exists
    cats = meta.get("categories") or []
    if not any(c.get("id") == "ielts" for c in cats):
        cats.append({"id": "ielts", "label": "IELTS", "label_bn": "আইইএলটিএস"})
    meta["categories"] = cats
    meta["lists"] = lists
    VLISTS.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def upsert_spelling_list(words: list[str]) -> None:
    meta = json.loads(SLISTS.read_text(encoding="utf-8"))
    lists = meta.get("lists") or []
    # unique case-insensitive preserve order
    seen = set()
    clean = []
    for w in words:
        n = w.strip().lower()
        if not n or n in seen:
            continue
        seen.add(n)
        clean.append(w.strip())
    entry = {
        "id": "ielts-listening-1600",
        "title": "IELTS Listening · 1600 Spellings",
        "title_bn": "IELTS লিসেনিং · ১৬০০ বানান",
        "description": "Listen & type high-frequency IELTS Listening words (unofficial).",
        "description_bn": "IELTS Listening-এর বহুল ব্যবহৃত শব্দ শুনে লেখো (অনঅফিসিয়াল)।",
        "target_size": len(clean),
        "words": clean,
    }
    replaced = False
    for i, L in enumerate(lists):
        if L.get("id") == entry["id"]:
            lists[i] = entry
            replaced = True
            break
    if not replaced:
        lists.append(entry)
    meta["lists"] = lists
    SLISTS.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"Missing source: {SRC}")
    incoming = json.loads(SRC.read_text(encoding="utf-8"))
    if not isinstance(incoming, list):
        raise SystemExit("Source must be a JSON array")

    added, updated, word_ids = merge_vocab(incoming)
    words = []
    # map ids back to display words from final bank
    bank = json.loads(VOCAB.read_text(encoding="utf-8"))
    by_id = {w["id"]: w["word"] for w in bank}
    for wid in word_ids:
        if wid in by_id:
            words.append(by_id[wid])

    upsert_vocab_list(word_ids)
    upsert_spelling_list(words)

    print("source", len(incoming))
    print("vocab added", added, "updated", updated, "bank", len(bank))
    print("vocab list word_ids", len(word_ids))
    print("spelling list words", len(words))


if __name__ == "__main__":
    main()
