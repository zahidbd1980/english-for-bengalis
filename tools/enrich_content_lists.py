#!/usr/bin/env python3
"""Fill underfilled vocab/spelling lists from vocabulary.json bank; add exam lists."""
from __future__ import annotations

import json
import re
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from cefr_policy import keep_word, list_cefr_label  # noqa: E402
VOCAB = ROOT / "data" / "vocabulary.json"
VLISTS = ROOT / "data" / "vocabulary-lists.json"
SLISTS = ROOT / "data" / "spelling-lists.json"

# Map list id -> (categories to pull, max size; None = all available)
THEMATIC_FILL = {
    "home-vocab": (["home"], None),
    "office-vocab": (["office"], None),
    "outdoor-nature": (["outdoor", "nature"], None),
    "food-health": (["food", "health"], None),
    "travel-shopping": (["travel", "shopping"], None),
    "education-study": (["education"], 200),
    "import-verbs": (["verbs"], None),
    "technology-digital": (["technology"], None),
    "daily-conversation": (["daily"], None),
    "ielts-academic-core": (["ielts", "education"], 250),
    "ielts-environment-society": (["nature", "outdoor", "health"], 200),
    "ielts-education-tech": (["education", "technology"], 200),
    "ielts-speaking-topics": (["home", "travel", "daily", "food", "office", "health"], 300),
}

# New exam-oriented lists built from bank categories/tags
NEW_LISTS = [
    {
        "id": "toefl-academic-core",
        "title": "TOEFL Academic Core",
        "title_bn": "TOEFL একাডেমিক কোর",
        "description": "Campus & academic English useful for TOEFL Reading/Listening (unofficial).",
        "description_bn": "TOEFL Reading/Listening-এর জন্য ক্যাম্পাস ও একাডেমিক শব্দ (অনঅফিসিয়াল)।",
        "cefr": "B1–C1",
        "categories": ["education", "ielts"],
        "tag_any": ["academic", "study", "ielts"],
        "max": 400,
    },
    {
        "id": "pte-academic-core",
        "title": "PTE Academic Core",
        "title_bn": "PTE একাডেমিক কোর",
        "description": "High-value academic & workplace words for PTE (unofficial).",
        "description_bn": "PTE-এর জন্য একাডেমিক ও অফিস শব্দ (অনঅফিসিয়াল)।",
        "cefr": "B1–C1",
        "categories": ["education", "office", "ielts"],
        "tag_any": ["academic", "work", "ielts"],
        "max": 400,
    },
    {
        "id": "ielts-reading-academic",
        "title": "IELTS Reading · Academic",
        "title_bn": "IELTS রিডিং · একাডেমিক",
        "description": "Passage-style academic vocabulary for IELTS Reading (unofficial).",
        "description_bn": "IELTS Reading প্যাসেজের মতো একাডেমিক শব্দ (অনঅফিসিয়াল)।",
        "cefr": "B2–C1",
        "categories": ["education", "ielts", "nature", "health", "technology"],
        "tag_any": ["academic", "ielts"],
        "max": 500,
    },
    {
        "id": "ielts-writing-task2",
        "title": "IELTS Writing Task 2",
        "title_bn": "IELTS রাইটিং টাস্ক ২",
        "description": "Opinion/discussion essay vocabulary (unofficial practice set).",
        "description_bn": "Opinion/discussion essay-এর শব্দভাণ্ডার (অনঅফিসিয়াল)।",
        "cefr": "B1–C1",
        "categories": ["education", "office", "ielts", "health", "technology"],
        "tag_any": ["academic", "formal", "ielts"],
        "max": 350,
    },
    {
        "id": "toefl-campus-life",
        "title": "TOEFL Campus Life",
        "title_bn": "TOEFL ক্যাম্পাস লাইফ",
        "description": "Dorm, library, registration, campus services vocabulary (unofficial).",
        "description_bn": "ডরম, লাইব্রেরি, রেজিস্ট্রেশন, ক্যাম্পাস সার্ভিস শব্দ (অনঅফিসিয়াল)।",
        "cefr": "B1–B2",
        "categories": ["education", "daily", "home", "food"],
        "tag_any": ["study", "daily"],
        "max": 250,
    },
    {
        "id": "pte-speaking-writing",
        "title": "PTE Speaking & Writing",
        "title_bn": "PTE স্পিকিং ও রাইটিং",
        "description": "Describe-image / essay friendly words for PTE (unofficial).",
        "description_bn": "PTE Describe Image ও essay-এর শব্দ (অনঅফিসিয়াল)।",
        "cefr": "B1–C1",
        "categories": ["education", "nature", "technology", "office", "health"],
        "tag_any": ["academic", "formal"],
        "max": 300,
    },
    {
        "id": "exam-collocations",
        "title": "Exam Collocations",
        "title_bn": "এক্সাম কলোকেশন",
        "description": "Work/study/health collocation-heavy words for IELTS/TOEFL/PTE.",
        "description_bn": "IELTS/TOEFL/PTE-এর জন্য কাজ/পড়া/স্বাস্থ্য কলোকেশন।",
        "cefr": "B1–B2",
        "categories": ["office", "education", "health"],
        "tag_any": ["work", "study", "health", "academic"],
        "max": 250,
    },
]

# Extra linker lemmas to pull into ielts-writing-linkers if present in bank
LINKER_WORDS = {
    "however", "therefore", "moreover", "furthermore", "nevertheless",
    "consequently", "meanwhile", "although", "whereas", "despite",
    "instead", "similarly", "likewise", "otherwise", "hence",
    "thus", "additionally", "conversely", "nonetheless", "accordingly",
    "specifically", "particularly", "notably", "overall", "finally",
    "firstly", "secondly", "thirdly", "in addition", "for example",
    "for instance", "in contrast", "on the other hand", "as a result",
    "in conclusion", "to summarise", "to summarize", "in summary",
}

# Spelling: grow toward targets from bank words not already present
SPELLING_GROW = {
    "common-misspellings": {"max": 800, "prefer_cats": None},
    "ielts-style": {"max": 600, "prefer_cats": ["ielts", "education"]},
    "everyday-hard": {"max": 400, "prefer_cats": ["daily", "office", "travel"]},
}


def slug_id(word: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", word.strip().lower()).strip("-")
    return f"vocab:{s}" if s else ""


def load_bank():
    bank = json.loads(VOCAB.read_text(encoding="utf-8"))
    by_cat: dict[str, list] = {}
    by_id = {}
    for w in bank:
        wid = w.get("id") or slug_id(w.get("word", ""))
        by_id[wid] = w
        cat = (w.get("category") or "").strip().lower()
        by_cat.setdefault(cat, []).append(w)
    return bank, by_id, by_cat


def ordered_unique_ids(words: list, max_n: int | None = None) -> list[str]:
    seen = set()
    out = []
    for w in words:
        if not keep_word(w):
            continue
        wid = w.get("id")
        if not wid or wid in seen:
            continue
        seen.add(wid)
        out.append(wid)
        if max_n is not None and len(out) >= max_n:
            break
    return out


def fill_thematic(lists: list, by_cat: dict, by_id: dict) -> dict:
    report = {}
    for L in lists:
        lid = L.get("id")
        if lid not in THEMATIC_FILL:
            continue
        cats, max_n = THEMATIC_FILL[lid]
        pool = []
        for c in cats:
            pool.extend(by_cat.get(c, []))
        existing = [wid for wid in (L.get("word_ids") or []) if keep_word(by_id.get(wid))]
        seen = set(existing)
        for w in pool:
            if not keep_word(w):
                continue
            wid = w.get("id")
            if wid and wid not in seen:
                existing.append(wid)
                seen.add(wid)
                if max_n is not None and len(existing) >= max_n:
                    break
        if max_n is not None:
            existing = existing[:max_n]
        before = len(L.get("word_ids") or [])
        L["word_ids"] = existing
        report[lid] = (before, len(existing))
    return report


def upsert_list(lists: list, entry: dict) -> None:
    for i, L in enumerate(lists):
        if L.get("id") == entry["id"]:
            lists[i] = entry
            return
    lists.append(entry)


def build_new_lists(lists: list, bank: list, by_cat: dict) -> dict:
    report = {}
    for spec in NEW_LISTS:
        pool = []
        for c in spec["categories"]:
            pool.extend(by_cat.get(c, []))
        tag_any = set(spec.get("tag_any") or [])
        # prefer tagged, then rest of category pool
        tagged = []
        rest = []
        for w in pool:
            tags = set(w.get("tags") or [])
            if tag_any and tags & tag_any:
                tagged.append(w)
            else:
                rest.append(w)
        # also pull tagged from whole bank
        for w in bank:
            tags = set(w.get("tags") or [])
            if tag_any and tags & tag_any and w not in tagged and w not in rest:
                tagged.append(w)
        ordered = tagged + rest
        ids = ordered_unique_ids(ordered, spec["max"])
        entry = {
            "id": spec["id"],
            "title": spec["title"],
            "title_bn": spec["title_bn"],
            "description": spec["description"],
            "description_bn": spec["description_bn"],
            "cefr": spec["cefr"],
            "word_ids": ids,
        }
        upsert_list(lists, entry)
        report[spec["id"]] = len(ids)
    return report


def ensure_exam_categories(meta: dict) -> None:
    cats = meta.get("categories") or []
    want = [
        {"id": "toefl", "label": "TOEFL", "label_bn": "টোয়েফল"},
        {"id": "pte", "label": "PTE", "label_bn": "পিটিই"},
        {"id": "exams", "label": "Exams", "label_bn": "পরীক্ষা"},
    ]
    have = {c.get("id") for c in cats}
    for c in want:
        if c["id"] not in have:
            cats.append(c)
    meta["categories"] = cats


def fill_writing_linkers(lists: list, bank: list) -> tuple[int, int]:
    by_word = {(w.get("word") or "").strip().lower(): w for w in bank}
    for L in lists:
        if L.get("id") != "ielts-writing-linkers":
            continue
        existing = list(L.get("word_ids") or [])
        seen = set(existing)
        before = len(existing)
        for lemma in sorted(LINKER_WORDS):
            w = by_word.get(lemma.lower())
            if not w or not keep_word(w):
                continue
            wid = w.get("id")
            if wid and wid not in seen:
                existing.append(wid)
                seen.add(wid)
        L["word_ids"] = existing
        return before, len(existing)
    return 0, 0


def grow_spelling(meta: dict, bank: list, by_cat: dict) -> dict:
    report = {}
    lists = meta.get("lists") or []
    bank_words = []
    for w in bank:
        word = (w.get("word") or "").strip()
        if word and " " not in word and len(word) >= 4:
            bank_words.append((word, (w.get("category") or "").lower()))

    for L in lists:
        lid = L.get("id")
        if lid not in SPELLING_GROW:
            continue
        cfg = SPELLING_GROW[lid]
        max_n = cfg["max"]
        prefer = set(cfg["prefer_cats"] or [])
        existing = list(L.get("words") or [])
        seen = {x.strip().lower() for x in existing}
        candidates = []
        if prefer:
            for word, cat in bank_words:
                if cat in prefer:
                    candidates.append(word)
            for word, cat in bank_words:
                if cat not in prefer:
                    candidates.append(word)
        else:
            candidates = [w for w, _ in sorted(bank_words, key=lambda t: (-len(t[0]), t[0]))]

        before = len(existing)
        for word in candidates:
            key = word.lower()
            if key in seen:
                continue
            existing.append(word)
            seen.add(key)
            if len(existing) >= max_n:
                break
        L["words"] = existing
        L["target_size"] = max(L.get("target_size") or 0, len(existing))
        report[lid] = (before, len(existing))

    # New exam spelling packs from category pools
    new_spell = [
        {
            "id": "toefl-spellings",
            "title": "TOEFL Spellings",
            "title_bn": "TOEFL বানান",
            "description": "Academic & campus spellings for TOEFL practice (unofficial).",
            "description_bn": "TOEFL অনুশীলনের একাডেমিক বানান (অনঅফিসিয়াল)।",
            "cats": ["education", "ielts", "office"],
            "max": 400,
        },
        {
            "id": "pte-spellings",
            "title": "PTE Spellings",
            "title_bn": "PTE বানান",
            "description": "Write-from-dictation friendly spellings for PTE (unofficial).",
            "description_bn": "PTE Write From Dictation-এর বানান (অনঅফিসিয়াল)।",
            "cats": ["education", "office", "technology", "health"],
            "max": 400,
        },
        {
            "id": "ielts-writing-spellings",
            "title": "IELTS Writing Spellings",
            "title_bn": "IELTS রাইটিং বানান",
            "description": "Essay vocabulary spellings for IELTS Writing (unofficial).",
            "description_bn": "IELTS Writing essay শব্দের বানান (অনঅফিসিয়াল)।",
            "cats": ["education", "ielts", "nature", "health"],
            "max": 350,
        },
    ]
    for spec in new_spell:
        words = []
        seen = set()
        for c in spec["cats"]:
            for w in by_cat.get(c, []):
                word = (w.get("word") or "").strip()
                key = word.lower()
                if not word or " " in word or key in seen:
                    continue
                seen.add(key)
                words.append(word)
                if len(words) >= spec["max"]:
                    break
            if len(words) >= spec["max"]:
                break
        entry = {
            "id": spec["id"],
            "title": spec["title"],
            "title_bn": spec["title_bn"],
            "description": spec["description"],
            "description_bn": spec["description_bn"],
            "target_size": len(words),
            "words": words,
        }
        upsert_list(lists, entry)
        report[spec["id"]] = (0, len(words))

    meta["lists"] = lists
    return report


def main() -> None:
    bank, by_id, by_cat = load_bank()
    vmeta = json.loads(VLISTS.read_text(encoding="utf-8"))
    lists = vmeta.get("lists") or []

    thematic = fill_thematic(lists, by_cat, by_id)
    linkers = fill_writing_linkers(lists, bank)
    new_counts = build_new_lists(lists, bank, by_cat)
    ensure_exam_categories(vmeta)
    for L in lists:
        L["cefr"] = list_cefr_label(L.get("cefr"))
    vmeta["lists"] = lists
    VLISTS.write_text(json.dumps(vmeta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    smeta = json.loads(SLISTS.read_text(encoding="utf-8"))
    spelling = grow_spelling(smeta, bank, by_cat)
    SLISTS.write_text(json.dumps(smeta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("=== Thematic vocab filled ===")
    for k, (a, b) in sorted(thematic.items()):
        print(f"  {k}: {a} -> {b}")
    print("=== Linkers ===")
    print(f"  ielts-writing-linkers: {linkers[0]} -> {linkers[1]}")
    print("=== New exam lists ===")
    for k, n in new_counts.items():
        print(f"  {k}: {n}")
    print("=== Spelling grown ===")
    for k, (a, b) in spelling.items():
        print(f"  {k}: {a} -> {b}")
    print("bank size", len(bank))


if __name__ == "__main__":
    main()
