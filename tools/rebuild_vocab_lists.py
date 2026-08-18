# -*- coding: utf-8 -*-
"""Audit + rebuild effective vocabulary target lists from bank.

Audience is B1+. Never put A1/A2 words on study lists.
Does not wipe exam/verb lists that were added by other importers.
"""
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from cefr_policy import BEGINNER_ONLY_LIST_IDS, keep_word, list_cefr_label  # noqa: E402

VP = ROOT / "data" / "vocabulary.json"
LP = ROOT / "data" / "vocabulary-lists.json"

# Map messy categories onto UI filter categories
CAT_MAP = {
    "academic": "ielts",
    "work": "office",
    "study": "education",
    "formal": "office",
    "culture": "daily",
    "general": "daily",
}


def load():
    vocab = json.loads(VP.read_text(encoding="utf-8"))
    meta = json.loads(LP.read_text(encoding="utf-8"))
    return vocab, meta


def normalize_bank(vocab):
    changed = 0
    for w in vocab:
        c = w.get("category") or "daily"
        if c in CAT_MAP:
            w["category"] = CAT_MAP[c]
            changed += 1
        w.setdefault("synonyms", [])
        w.setdefault("antonyms", [])
        w.setdefault("word_family", [])
        if "cefr_level" not in w and w.get("cefr"):
            w["cefr_level"] = w.pop("cefr")
        if "part_of_speech" not in w and w.get("pos"):
            w["part_of_speech"] = w.pop("pos")
    return changed


def pick(by_id, words):
    out = []
    for w in words:
        key = w if w.startswith("vocab:") else f"vocab:{w}"
        # also try slug from raw word
        if key not in by_id:
            slug = "vocab:" + w.lower().replace(" ", "-")
            key = slug if slug in by_id else None
        if key and key in by_id and key not in out:
            out.append(key)
    return out


def by_category(vocab, cat, limit=None, cefr=None):
    rows = [w for w in vocab if w.get("category") == cat and keep_word(w)]
    if cefr:
        rows = [w for w in rows if w.get("cefr_level") in cefr]
    rows = sorted(rows, key=lambda x: (x.get("cefr_level") or "", x.get("word") or ""))
    ids = [w["id"] for w in rows]
    return ids[:limit] if limit else ids


def by_cefr(vocab, levels, limit=None, exclude=None):
    exclude = set(exclude or [])
    rows = [w for w in vocab if w.get("cefr_level") in levels and keep_word(w) and w["id"] not in exclude]
    rows = sorted(rows, key=lambda x: (x.get("category") or "", x.get("word") or ""))
    ids = [w["id"] for w in rows]
    return ids[:limit] if limit else ids


def with_antonyms(vocab, limit=40):
    rows = [w for w in vocab if w.get("antonyms") and keep_word(w)]
    rows = sorted(rows, key=lambda x: (-len(x.get("antonyms") or []), x.get("word") or ""))
    return [w["id"] for w in rows[:limit]]


def with_family(vocab, limit=40):
    rows = [w for w in vocab if w.get("word_family") and keep_word(w)]
    rows = sorted(rows, key=lambda x: (-len(x.get("word_family") or []), x.get("word") or ""))
    return [w["id"] for w in rows[:limit]]


def rebuild_lists(vocab):
    by_id = {w["id"]: w for w in vocab}
    words = {w["word"].lower(): w["id"] for w in vocab}

    def ids_from_words(names):
        out = []
        for n in names:
            wid = words.get(n.lower())
            if wid and wid not in out and keep_word(by_id.get(wid)):
                out.append(wid)
        return out

    # Curated high-value spoken/daily cores (B1+ only if in bank)
    b1_power = ids_from_words(
        [
            "achieve", "develop", "require", "consider", "realize", "recognize", "reduce",
            "provide", "prevent", "suffer", "recover", "affect", "effect", "benefit",
            "advantage", "disadvantage", "solution", "condition", "quality", "quantity",
            "value", "profit", "budget", "expense", "income", "encourage", "forbid",
            "perform", "produce", "reliable", "urgent", "curious", "traditional",
            "analyse", "significant", "evidence", "approach", "impact", "issue", "trend",
            "proportion", "research", "essential", "efficient", "sustainable", "urban",
            "rural", "poverty", "equality", "community", "government", "innovation",
        ]
    )

    lists = [
        {
            "id": "target-b1-power",
            "title": "B1 Power Words",
            "title_bn": "B1 পাওয়ার ওয়ার্ডস",
            "description": "High-value words for work, study, and confident speaking.",
            "description_bn": "কাজ, পড়াশোনা ও আত্মবিশ্বাসী কথার শব্দ।",
            "cefr": "B1",
            "word_ids": b1_power,
        },
        {
            "id": "import-verbs",
            "title": "Important Verbs",
            "title_bn": "গুরুত্বপূর্ণ ক্রিয়া",
            "description": "High-frequency action verbs for speaking and writing.",
            "description_bn": "কথা ও লেখার জরুরি action verbs।",
            "cefr": "B1",
            "word_ids": [
                w["id"]
                for w in vocab
                if "verb" in str(w.get("part_of_speech") or "").lower() and keep_word(w)
            ][:45],
        },
        {
            "id": "soft-skills-adjectives",
            "title": "Soft Skills · Adjectives",
            "title_bn": "সফট স্কিল · বিশেষণ",
            "description": "Describe people and feelings: polite, confident, careful…",
            "description_bn": "মানুষ ও অনুভূতি বর্ণনা: ভদ্র, আত্মবিশ্বাসী, সাবধান…",
            "cefr": "B1",
            "word_ids": ids_from_words(
                [
                    "polite", "rude", "confident", "nervous", "honest", "brave", "clever",
                    "lazy", "careful", "careless", "patient", "curious", "useful", "useless",
                    "possible", "impossible", "necessary", "popular", "modern", "traditional",
                    "reliable", "urgent", "similar", "different", "healthy", "busy", "early",
                    "late", "clean", "dirty", "cheap", "expensive", "delicious", "spicy",
                ]
            ),
        },
        {
            "id": "office-vocab",
            "title": "Office & Work",
            "title_bn": "অফিস ও কাজ",
            "description": "Meetings, email, deadlines, salary, tasks.",
            "description_bn": "মিটিং, ইমেইল, ডেডলাইন, বেতন, কাজ।",
            "cefr": "B1",
            "word_ids": sorted(
                set(by_category(vocab, "office") + ids_from_words(
                    ["salary", "income", "budget", "expense", "profit", "loss", "goal", "task", "report", "manager"]
                ))
            ),
        },
        {
            "id": "home-vocab",
            "title": "Home & Family",
            "title_bn": "বাড়ি ও পরিবার",
            "description": "Rooms, cleaning, neighbours, family life.",
            "description_bn": "ঘর, পরিষ্কার, প্রতিবেশী, পারিবারিক জীবন।",
            "cefr": "B1–C1",
            "word_ids": by_category(vocab, "home"),
        },
        {
            "id": "outdoor-nature",
            "title": "Outdoor & Nature",
            "title_bn": "বাইরে ও প্রকৃতি",
            "description": "Park, weather, river, pollution, environment.",
            "description_bn": "পার্ক, আবহাওয়া, নদী, দূষণ, পরিবেশ।",
            "cefr": "B1–C1",
            "word_ids": sorted(set(by_category(vocab, "outdoor") + by_category(vocab, "nature") + ids_from_words(["pollution", "environment", "weather", "traffic"]))),
        },
        {
            "id": "food-health",
            "title": "Food & Health",
            "title_bn": "খাবার ও স্বাস্থ্য",
            "description": "Meals, taste, doctor, exercise, recovery.",
            "description_bn": "খাবার, স্বাদ, ডাক্তার, ব্যায়াম, সুস্থতা।",
            "cefr": "B1–C1",
            "word_ids": sorted(set(by_category(vocab, "food") + by_category(vocab, "health"))),
        },
        {
            "id": "travel-shopping",
            "title": "Travel & Shopping",
            "title_bn": "ভ্রমণ ও কেনাকাটা",
            "description": "Tickets, airport, price, discount, customers.",
            "description_bn": "টিকিট, এয়ারপোর্ট, দাম, ছাড়।",
            "cefr": "B1–C1",
            "word_ids": sorted(set(by_category(vocab, "travel") + by_category(vocab, "shopping"))),
        },
        {
            "id": "education-study",
            "title": "Education & Study",
            "title_bn": "শিক্ষা ও পড়াশোনা",
            "description": "School, skills, homework, improve, succeed.",
            "description_bn": "স্কুল, দক্ষতা, হোমওয়ার্ক, উন্নতি, সফলতা।",
            "cefr": "B1–C1",
            "word_ids": by_category(vocab, "education"),
        },
        {
            "id": "technology-digital",
            "title": "Technology & Digital",
            "title_bn": "প্রযুক্তি ও ডিজিটাল",
            "description": "Email, download, digital tools, access.",
            "description_bn": "ইমেইল, ডাউনলোড, ডিজিটাল টুল।",
            "cefr": "B1",
            "word_ids": by_category(vocab, "technology"),
        },
        {
            "id": "daily-conversation",
            "title": "Daily Conversation",
            "title_bn": "দৈনন্দিন কথোপকথন",
            "description": "Everyday words you need in shops, home, and chat.",
            "description_bn": "দোকান, বাড়ি ও চ্যাটে দরকারি শব্দ।",
            "cefr": "B1–C1",
            "word_ids": by_cefr([w for w in vocab if w.get("category") == "daily"], ["B1", "B2", "C1", "C2"], limit=80),
        },
        {
            "id": "opposites-pack",
            "title": "Opposites Pack",
            "title_bn": "বিপরীত শব্দ প্যাক",
            "description": "Learn faster with antonym pairs (cheap/expensive, early/late).",
            "description_bn": "antonym জোড়ায় শিখুন — দ্রুত মনে থাকে।",
            "cefr": "B1–C1",
            "word_ids": with_antonyms(vocab, 50),
        },
        {
            "id": "word-family-pack",
            "title": "Word Family Pack",
            "title_bn": "শব্দ পরিবার প্যাক",
            "description": "Root + related forms (improve → improvement, decide → decision).",
            "description_bn": "মূল শব্দ + পরিবার — IELTS/লেখার জন্য জরুরি।",
            "cefr": "B1",
            "word_ids": with_family(vocab, 45),
        },
        {
            "id": "ielts-academic-core",
            "title": "IELTS Academic Core",
            "title_bn": "IELTS একাডেমিক মূল শব্দ",
            "description": "High-value Reading/Writing words. Unofficial practice.",
            "description_bn": "রিডিং/রাইটিংয়ের জরুরি শব্দ। অনঅফিসিয়াল।",
            "cefr": "B1–B2",
            "word_ids": ids_from_words(
                [
                    "analyse", "significant", "benefit", "drawback", "evidence", "approach",
                    "impact", "issue", "solution", "trend", "proportion", "compare", "contrast",
                    "conclude", "overall", "research", "academic", "essential", "efficient",
                    "challenge", "achieve", "develop", "consider", "require", "affect", "effect",
                    "advantage", "disadvantage", "quality", "value",
                ]
            ),
        },
        {
            "id": "ielts-writing-linkers",
            "title": "IELTS Writing Linkers",
            "title_bn": "IELTS রাইটিং লিংকার",
            "description": "Linking words for Task 2: however, therefore, although…",
            "description_bn": "Task 2 রচনার সংযোগকারী শব্দ।",
            "cefr": "B1–B2",
            "word_ids": ids_from_words(
                [
                    "therefore", "however", "furthermore", "although", "whereas", "consequently",
                    "argue", "opinion", "advantage", "disadvantage", "overall", "conclude",
                    "contrast", "compare", "result", "cause", "purpose",
                ]
            ),
        },
        {
            "id": "ielts-environment-society",
            "title": "IELTS Environment & Society",
            "title_bn": "IELTS পরিবেশ ও সমাজ",
            "description": "Essay themes: pollution, urban/rural, poverty, equality.",
            "description_bn": "প্রবন্ধ থিম: দূষণ, শহর-গ্রাম, দারিদ্র্য, সমতা।",
            "cefr": "B1",
            "word_ids": ids_from_words(
                [
                    "environment", "pollution", "sustainable", "recycle", "urban", "rural",
                    "poverty", "equality", "community", "government", "issue", "solution",
                    "impact", "benefit", "protect", "prevent", "public", "local", "condition",
                    "quality",
                ]
            ),
        },
        {
            "id": "ielts-education-tech",
            "title": "IELTS Education & Technology",
            "title_bn": "IELTS শিক্ষা ও প্রযুক্তি",
            "description": "Study and tech vocabulary for essays and speaking.",
            "description_bn": "পড়াশোনা ও প্রযুক্তি বিষয়ক শব্দ।",
            "cefr": "B1",
            "word_ids": sorted(
                set(by_category(vocab, "education") + by_category(vocab, "technology") + ids_from_words(
                    ["skill", "career", "innovation", "digital", "access", "efficient", "essential", "opportunity", "improve", "research", "academic"]
                ))
            ),
        },
        {
            "id": "ielts-speaking-topics",
            "title": "IELTS Speaking Topics",
            "title_bn": "IELTS স্পিকিং টপিক",
            "description": "Useful words for Part 1–2: hobby, neighbourhood, prefer, describe…",
            "description_bn": "Part 1–2 এর জন্য দরকারি শব্দ।",
            "cefr": "B1",
            "word_ids": ids_from_words(
                [
                    "hobby", "neighbourhood", "celebrate", "prefer", "describe", "opinion",
                    "family", "journey", "weather", "neighbour", "polite", "confident",
                    "agree", "discuss", "mention", "explain", "remember", "forget", "busy",
                    "local", "traditional", "modern", "popular", "opportunity", "challenge",
                ]
            ),
        },
        {
            "id": "false-friends-bn",
            "title": "Bangla Speakers · Careful Words",
            "title_bn": "বাংলাভাষীদের সাবধান শব্দ",
            "description": "Words often mixed up: borrow/lend, affect/effect, accept/except patterns.",
            "description_bn": "যেসব শব্দে বাংলাভাষীরা প্রায়ই গুলিয়ে ফেলেন।",
            "cefr": "B1",
            "word_ids": ids_from_words(
                [
                    "borrow", "lend", "affect", "effect", "accept", "except", "advise", "advice",
                    "practice", "prefer", "suggest", "discuss", "agree", "allow", "reach",
                    "arrive", "leave", "remember", "forget", "interesting", "interested",
                ]
            ),
        },
    ]

    # Drop empty / validate
    clean = []
    for L in lists:
        ids = [i for i in L["word_ids"] if i in by_id and keep_word(by_id[i])]
        # unique preserve order
        seen = set()
        uniq = []
        for i in ids:
            if i not in seen:
                seen.add(i)
                uniq.append(i)
        L["word_ids"] = uniq
        L["cefr"] = list_cefr_label(L.get("cefr"))
        if len(uniq) >= 6:
            clean.append(L)
    return clean


def merge_lists(existing: list, rebuilt: list) -> list:
    by_rebuilt = {L["id"]: L for L in rebuilt}
    merged = []
    seen = set()
    for L in existing or []:
        lid = L.get("id")
        if not lid or lid in BEGINNER_ONLY_LIST_IDS:
            continue
        if lid in by_rebuilt:
            merged.append(by_rebuilt[lid])
        else:
            merged.append(L)
        seen.add(lid)
    for L in rebuilt:
        if L["id"] not in seen:
            merged.append(L)
    return merged


def main():
    vocab, meta = load()
    changed = normalize_bank(vocab)
    lists = merge_lists(meta.get("lists") or [], rebuild_lists(vocab))

    # Keep categories UI list, ensure needed cats exist
    cats = meta.get("categories") or []
    have = {c["id"] for c in cats}
    for needed in [
        ("daily", "Daily", "দৈনন্দিন"),
        ("ielts", "IELTS", "আইইএলটিএস"),
        ("education", "Education", "শিক্ষা"),
    ]:
        if needed[0] not in have:
            cats.append({"id": needed[0], "label": needed[1], "label_bn": needed[2]})

    meta["categories"] = cats
    meta["lists"] = lists

    VP.write_text(json.dumps(vocab, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    LP.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    covered = set(i for L in lists for i in L["word_ids"])
    print("bank", len(vocab), "category fixes", changed)
    print("lists", len(lists))
    for L in lists:
        print(f"  {L['id']}: {len(L['word_ids'])}")
    print("unique words in lists", len(covered), "/", len(vocab))
    print("cat counts", Counter(w.get("category") for w in vocab).most_common())


if __name__ == "__main__":
    main()
