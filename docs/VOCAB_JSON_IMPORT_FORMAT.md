# Vocabulary JSON Import Format

এই ডকুমেন্টে **English for Bengalis** সাইটে শব্দ/লিস্ট যোগ করার অফিসিয়াল JSON ফরম্যাট আছে।

সাইটে দুই ধরনের ইমপোর্ট আছে:

| ধরন | ফাইল | কাজ |
|---|---|---|
| **Word bank** | `data/vocabulary.json` (বা patch JSON) | পুরো শব্দ কার্ড (অর্থ, উদাহরণ, word family) |
| **Target list** | `data/vocabulary-lists.json` | টার্গেট স্টাডি লিস্ট (`word_ids` দিয়ে) |
| **Browser custom** | Vocabulary পেজে `.txt` আপলোড | এখন শুধু plain text (প্রতি লাইনে এক শব্দ) — পূর্ণ JSON নয় |

---

## 1) Word bank — একক শব্দের JSON অবজেক্ট

প্রতিটি শব্দ একটি object। পুরো ফাইল সাধারণত **array of objects**।

### Required fields

| Field | Type | Example | Notes |
|---|---|---|---|
| `id` | string | `"vocab:improve"` | সবসময় `vocab:` + slug |
| `word` | string | `"improve"` | মূল ইংরেজি শব্দ |
| `meaning_en` | string | `"to make better"` | ইংরেজি অর্থ |
| `meaning_bn` | string | `"উন্নত করা"` | বাংলা অর্থ |
| `part_of_speech` | string | `"verb"` | দেখুন নিচের POS তালিকা |
| `cefr_level` | string | `"A2"` | `A1` `A2` `B1` `B2` `C1` `C2` |
| `category` | string | `"education"` | দেখুন নিচের category তালিকা |
| `example` | string | `"I want to improve my English."` | ইংরেজি উদাহরণ বাক্য |
| `example_bn` | string | `"আমি আমার ইংরেজি উন্নত করতে চাই।"` | বাংলা উদাহরণ |

### Optional but recommended

| Field | Type | Example |
|---|---|---|
| `phonetic` | string | `"/ɪmˈpruːv/"` |
| `synonyms` | string[] | `["enhance", "develop"]` (max ~3) |
| `antonyms` | string[] | `["worsen"]` (max ~3) |
| `word_family` | object[] | নিচের ফরম্যাট |
| `tags` | string[] | `["study", "ielts"]` (ঐচ্ছিক) |

### `word_family` item format

```json
{
  "word": "improvement",
  "pos": "noun",
  "meaning_bn": "উন্নতি"
}
```

> কিছু পুরনো ডেটায় `form` ফিল্ডও দেখা যেতে পারে; নতুন ইমপোর্টে **`word` + `pos` + `meaning_bn`** ব্যবহার করুন।

### Allowed `part_of_speech`

`noun`, `verb`, `adjective`, `adverb`, `preposition`, `conjunction`, `pronoun`,  
অথবা কম্পোজিট: `verb/noun`, `adj/noun` ইত্যাদি।

### Allowed `category` (UI ফিল্টার)

`home`, `office`, `outdoor`, `nature`, `food`, `travel`, `health`, `education`,  
`verbs`, `shopping`, `technology`, `daily`, `ielts`

---

## 2) Word bank — পূর্ণ উদাহরণ (১টা শব্দ)

```json
{
  "id": "vocab:deadline",
  "word": "deadline",
  "phonetic": "/ˈdedlaɪn/",
  "meaning_en": "the latest time something must be finished",
  "meaning_bn": "শেষ সময়সীমা / ডেডলাইন",
  "part_of_speech": "noun",
  "cefr_level": "B1",
  "category": "office",
  "example": "The deadline is Friday.",
  "example_bn": "ডেডলাইন শুক্রবার।",
  "synonyms": ["time limit"],
  "antonyms": [],
  "word_family": []
}
```

---

## 3) Word bank — প্যাচ/ইমপোর্ট ফাইল (অনেক শব্দ)

ফাইলটি অবশ্যই **JSON array** হবে:

```json
[
  {
    "id": "vocab:deadline",
    "word": "deadline",
    "meaning_en": "the latest time something must be finished",
    "meaning_bn": "শেষ সময়সীমা",
    "part_of_speech": "noun",
    "cefr_level": "B1",
    "category": "office",
    "example": "The deadline is Friday.",
    "example_bn": "ডেডলাইন শুক্রবার।",
    "synonyms": ["time limit"],
    "antonyms": [],
    "word_family": []
  },
  {
    "id": "vocab:colleague",
    "word": "colleague",
    "meaning_en": "a person you work with",
    "meaning_bn": "সহকর্মী",
    "part_of_speech": "noun",
    "cefr_level": "A2",
    "category": "office",
    "example": "My colleague helped me.",
    "example_bn": "আমার সহকর্মী আমাকে সাহায্য করেছে।",
    "synonyms": ["coworker"],
    "antonyms": [],
    "word_family": []
  }
]
```

### Repo-তে মার্জ করার কমান্ড

```bash
# ফরম্যাট চেক
python tools/merge_vocab.py --check

# JSON patch মার্জ
python tools/merge_vocab.py --from data/my_vocab_patch.json

# CSV থেকেও যায় (টেমপ্লেট: data/vocab_import_template.csv)
python tools/merge_vocab.py --from data/vocab_import_template.csv
```

মার্জ রুল:
- একই `id` থাকলে আপডেট
- না থাকলে নতুন শব্দ যোগ
- তারপর `git push` → GitHub Pages CDN আপডেট

---

## 4) Target list JSON (স্টাডি লিস্ট)

টার্গেট লিস্ট শব্দের পূর্ণ ডেটা রাখে না — শুধু **`word_ids`** রাখে (ব্যাংকের `id`)।

### List object format

```json
{
  "id": "office-vocab",
  "title": "Office & Work",
  "title_bn": "অফিস ও কাজ",
  "description": "Meetings, email, deadlines, salary, tasks.",
  "description_bn": "মিটিং, ইমেইল, ডেডলাইন, বেতন, কাজ।",
  "cefr": "B1–C1",
  "word_ids": [
    "vocab:deadline",
    "vocab:colleague",
    "vocab:meeting",
    "vocab:email",
    "vocab:salary"
  ]
}
```

### পুরো `vocabulary-lists.json` স্কিমা

```json
{
  "categories": [
    { "id": "office", "label": "Office", "label_bn": "অফিস" }
  ],
  "lists": [
    {
      "id": "my-custom-list",
      "title": "My Custom List",
      "title_bn": "আমার কাস্টম লিস্ট",
      "description": "Short English description",
      "description_bn": "সংক্ষিপ্ত বাংলা বর্ণনা",
      "cefr": "B1",
      "word_ids": ["vocab:improve", "vocab:practice"]
    }
  ]
}
```

### গুরুত্বপূর্ণ নিয়ম

1. প্রতিটি `word_ids` আইটেম অবশ্যই `vocabulary.json`-এ থাকতে হবে  
2. `id` ইউনিক রাখুন (`my-team-week-3` স্টাইল)  
3. খালি লিস্ট (`word_ids: []`) এড়াবেন  
4. **লিস্টে A1/A2 রাখবেন না** — ভিজিটর intermediate–advanced। শুধু B1+ (`keep_word` / `tools/cefr_policy.py`)  
5. ব্যাংকে (`vocabulary.json`) A1/A2 থাকতে পারে; টার্গেট লিস্টে নয়  

---

## 5) ID বানানোর নিয়ম

```text
vocab: + lowercase-slug
```

উদাহরণ:

| word | id |
|---|---|
| improve | `vocab:improve` |
| living room | `vocab:living-room` |
| neighbour | `vocab:neighbour` |

স্ক্রিপ্ট দিয়েও বানানো যায়:

```python
# tools/merge_vocab.py → slug_id("living room") → "vocab:living-room"
```

---

## 6) Browser Vocabulary পেজে এখন কী ইমপোর্ট হয়

Vocabulary পেজের **Custom list** এখন:

- `.txt` ফাইল / textarea
- প্রতি লাইনে একটি শব্দ  
  অথবা `word — meaning` / `word: meaning`

উদাহরণ `.txt`:

```text
deadline
colleague
improve
practice — অনুশীলন করা
```

> ব্রাউজারে পূর্ণ JSON কার্ড আপলোড এখনো সাপোর্টেড নয়। পূর্ণ কার্ড যোগ করতে উপরের **Word bank JSON + `merge_vocab.py`** ব্যবহার করুন।

---

## 7) দ্রুত চেকলিস্ট (পাঠানোর আগে)

- [ ] JSON valid (array/object ঠিক আছে)
- [ ] সব required ফিল্ড ভরা
- [ ] `id` সব `vocab:...`
- [ ] `cefr_level` বৈধ
- [ ] `category` UI তালিকার মধ্যে
- [ ] `example` ও `example_bn` দুটোই আছে
- [ ] Target list হলে `word_ids` ব্যাংকে মিলে

---

## 8) মিনিমাল টেমপ্লেট (কপি করে ব্যবহার করুন)

```json
[
  {
    "id": "vocab:your-word",
    "word": "your-word",
    "meaning_en": "English meaning",
    "meaning_bn": "বাংলা অর্থ",
    "part_of_speech": "noun",
    "cefr_level": "A2",
    "category": "daily",
    "example": "Write one English example sentence.",
    "example_bn": "একটি বাংলা উদাহরণ বাক্য লিখুন।",
    "synonyms": [],
    "antonyms": [],
    "word_family": []
  }
]
```

সংরক্ষণ করুন যেমন: `data/my_vocab_patch.json` → তারপর:

```bash
python tools/merge_vocab.py --from data/my_vocab_patch.json
```
