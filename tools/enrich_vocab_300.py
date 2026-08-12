# -*- coding: utf-8 -*-
import json
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "data" / "vocabulary.json"
v = json.loads(p.read_text(encoding="utf-8"))
have = {x["word"].lower() for x in v}
print("before", len(v))

# Fix any stub entries from failed one-liner
fixed = []
for item in v:
    if item.get("meaning_bn") == item.get("word") or not item.get("meaning_bn"):
        # drop bad stubs; re-add clean below
        if item["word"].lower() in {"reliable", "urgent", "temporary", "permanent", "frequent", "rare", "obvious", "complex", "simple", "flexible"} and item.get("phonetic") == "":
            continue
    fixed.append(item)
v = fixed
have = {x["word"].lower() for x in v}

extras = [
  {
    "id": "v327",
    "word": "reliable",
    "phonetic": "/rɪˈlaɪəbl/",
    "pos": "adj",
    "cefr": "B1",
    "meaning_en": "can be trusted",
    "meaning_bn": "নির্ভরযোগ্য",
    "example": "He is a reliable friend.",
    "example_bn": "সে একজন নির্ভরযোগ্য বন্ধু।",
    "tags": ["daily"],
    "synonyms": ["trustworthy"],
    "antonyms": ["unreliable"],
  },
  {
    "id": "v328",
    "word": "urgent",
    "phonetic": "/ˈɜːdʒənt/",
    "pos": "adj",
    "cefr": "B1",
    "meaning_en": "needing quick action",
    "meaning_bn": "জরুরি",
    "example": "This is an urgent message.",
    "example_bn": "এটি একটি জরুরি বার্তা।",
    "tags": ["work"],
    "synonyms": ["pressing"],
    "antonyms": [],
  },
]

added = 0
for w in extras:
    if w["word"].lower() in have:
        continue
    v.append(w)
    have.add(w["word"].lower())
    added += 1
    if len(v) >= 300:
        break

p.write_text(json.dumps(v, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("added", added, "total", len(v))
