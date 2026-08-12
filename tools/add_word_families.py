# Attach word_family (POS forms) to vocabulary entries where useful.
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "vocabulary.json"

# Related forms only (headword itself is skipped when applying / rendering).
# Each item: word, pos, meaning_bn
F = lambda *rows: [{"word": w, "pos": p, "meaning_bn": bn} for w, p, bn in rows]

FAMILIES = {
    "improve": F(
        ("improvement", "noun", "উন্নতি / উন্নয়ন"),
        ("improved", "adjective", "উন্নত"),
    ),
    "practice": F(
        ("practise", "verb", "অনুশীলন করা (UK)"),
        ("practical", "adjective", "ব্যবহারিক"),
        ("practically", "adverb", "প্রায় / ব্যবহারিকভাবে"),
    ),
    "confident": F(
        ("confidence", "noun", "আত্মবিশ্বাস"),
        ("confidently", "adverb", "আত্মবিশ্বাসের সাথে"),
    ),
    "appointment": F(("appoint", "verb", "নিয়োগ করা / নির্ধারণ করা"),),
    "recommend": F(
        ("recommendation", "noun", "সুপারিশ"),
        ("recommended", "adjective", "সুপারিশকৃত"),
    ),
    "polite": F(
        ("politeness", "noun", "ভদ্রতা"),
        ("politely", "adverb", "ভদ্রভাবে"),
        ("impolite", "adjective", "অভদ্র"),
    ),
    "necessary": F(
        ("necessity", "noun", "প্রয়োজনীয়তা"),
        ("necessarily", "adverb", "অবশ্যই / প্রয়োজনীয়ভাবে"),
        ("unnecessary", "adjective", "অপ্রয়োজনীয়"),
    ),
    "opportunity": F(("opportune", "adjective", "উপযুক্ত সময়ের"),),
    "explain": F(
        ("explanation", "noun", "ব্যাখ্যা"),
        ("explanatory", "adjective", "ব্যাখ্যামূলক"),
    ),
    "available": F(
        ("availability", "noun", "সহজলভ্যতা"),
        ("unavailable", "adjective", "অপ্রাপ্য"),
    ),
    "hungry": F(("hunger", "noun", "ক্ষুধা"),),
    "thirsty": F(("thirst", "noun", "তৃষ্ণা"),),
    "borrow": F(("borrower", "noun", "ধার নেওয়া ব্যক্তি"),),
    "lend": F(("lender", "noun", "ধারদাতা"),),
    "busy": F(("busily", "adverb", "ব্যস্তভাবে"),),
    "early": F(("earliness", "noun", "আগাম / অকালতা"),),
    "late": F(
        ("lateness", "noun", "দেরি"),
        ("lately", "adverb", "সম্প্রতি"),
    ),
    "forget": F(
        ("forgetful", "adjective", "ভুলুকে"),
        ("forgetfulness", "noun", "ভুলুকতা"),
    ),
    "remember": F(
        ("memory", "noun", "স্মৃতি"),
        ("memorable", "adjective", "স্মরণীয়"),
    ),
    "arrive": F(("arrival", "noun", "আগমন"),),
    "leave": F(("departure", "noun", "প্রস্থান"),),
    "clean": F(
        ("cleanliness", "noun", "পরিচ্ছন্নতা"),
        ("cleaner", "noun", "পরিচ্ছন্নতাকারী"),
        ("cleanly", "adverb", "পরিচ্ছন্নভাবে"),
    ),
    "dirty": F(("dirt", "noun", "ময়লা"),),
    "neighbour": F(("neighbourhood", "noun", "পাড়া / এলাকা"), ("neighbouring", "adjective", "পার্শ্ববর্তী")),
    "furniture": F(("furnish", "verb", "আসবাব দিয়ে সাজানো"),),
    "rent": F(("rental", "noun/adjective", "ভাড়া সংক্রান্ত"), ("renter", "noun", "ভাড়াটে")),
    "meeting": F(("meet", "verb", "সাক্ষাৎ করা"),),
    "schedule": F(("scheduled", "adjective", "নির্ধারিত"),),
    "salary": F(("salaried", "adjective", "বেতনভুক্ত"),),
    "report": F(("reporter", "noun", "প্রতিবেদক"),),
    "manager": F(("manage", "verb", "পরিচালনা করা"), ("management", "noun", "ব্যবস্থাপনা")),
    "pollution": F(
        ("pollute", "verb", "দূষিত করা"),
        ("polluted", "adjective", "দূষিত"),
        ("pollutant", "noun", "দূষক পদার্থ"),
    ),
    "delicious": F(("deliciously", "adverb", "সুস্বাদুভাবে"),),
    "vegetable": F(("vegetarian", "noun/adjective", "নিরামিষভোজী"),),
    "direction": F(
        ("direct", "verb/adjective", "নির্দেশ করা / সরাসরি"),
        ("directly", "adverb", "সরাসরি"),
        ("director", "noun", "পরিচালক"),
    ),
    "healthy": F(
        ("health", "noun", "স্বাস্থ্য"),
        ("unhealthy", "adjective", "অস্বাস্থ্যকর"),
    ),
    "student": F(("study", "verb/noun", "পড়াশোনা করা / অধ্যয়ন"),),
    "teacher": F(("teach", "verb", "শেখানো"), ("teaching", "noun", "শিক্ষাদান")),
    "begin": F(
        ("beginning", "noun", "শুরু"),
        ("beginner", "noun", "শিক্ষানবিশ"),
    ),
    "finish": F(("finished", "adjective", "শেষ / সম্পন্ন"),),
    "choose": F(
        ("choice", "noun", "পছন্দ / বাছাই"),
        ("chosen", "adjective", "নির্বাচিত"),
    ),
    "decide": F(
        ("decision", "noun", "সিদ্ধান্ত"),
        ("decisive", "adjective", "দৃঢ়সংকল্প"),
    ),
    "prefer": F(
        ("preference", "noun", "পছন্দ / অগ্রাধিকার"),
        ("preferable", "adjective", "অধিক পছন্দনীয়"),
        ("preferably", "adverb", "অধিকতর ভালো হয় যদি"),
    ),
    "suggest": F(
        ("suggestion", "noun", "পরামর্শ"),
        ("suggested", "adjective", "প্রস্তাবিত"),
    ),
    "accept": F(
        ("acceptance", "noun", "গ্রহণ"),
        ("acceptable", "adjective", "গ্রহণযোগ্য"),
        ("unacceptable", "adjective", "অগ্রহণযোগ্য"),
    ),
    "refuse": F(
        ("refusal", "noun", "প্রত্যাখ্যান"),
        ("refused", "adjective", "প্রত্যাখ্যাত"),
    ),
    "compare": F(
        ("comparison", "noun", "তুলনা"),
        ("comparative", "adjective", "তুলনামূলক"),
        ("comparatively", "adverb", "তুলনামূলকভাবে"),
    ),
    "describe": F(
        ("description", "noun", "বর্ণনা"),
        ("descriptive", "adjective", "বর্ণনামূলক"),
    ),
    "prepare": F(
        ("preparation", "noun", "প্রস্তুতি"),
        ("prepared", "adjective", "প্রস্তুত"),
    ),
    "solve": F(
        ("solution", "noun", "সমাধান"),
        ("solvable", "adjective", "সমাধানযোগ্য"),
    ),
    "notice": F(("noticeable", "adjective", "লক্ষণীয়"),),
    "avoid": F(
        ("avoidance", "noun", "এড়িয়ে চলা"),
        ("avoidable", "adjective", "এড়ানো যায় এমন"),
    ),
    "price": F(("pricey", "adjective", "দামি"), ("priced", "adjective", "মূল্য নির্ধারিত")),
    "cheap": F(("cheaply", "adverb", "সস্তায়"), ("cheapness", "noun", "সস্তাভাব")),
    "expensive": F(("expense", "noun", "খরচ"),),
    "customer": F(("customise", "verb", "কাস্টমাইজ করা"), ("custom", "noun", "প্রথা / কাস্টম")),
    "analyse": F(
        ("analysis", "noun", "বিশ্লেষণ"),
        ("analyst", "noun", "বিশ্লেষক"),
        ("analytical", "adjective", "বিশ্লেষণাত্মক"),
    ),
    "significant": F(
        ("significance", "noun", "গুরুত্ব / তাৎপর্য"),
        ("significantly", "adverb", "উল্লেখযোগ্যভাবে"),
        ("insignificant", "adjective", "তুচ্ছ / অগুরুত্বপূর্ণ"),
    ),
    "benefit": F(
        ("beneficial", "adjective", "উপকারী"),
        ("beneficiary", "noun", "উপকারভোগী"),
    ),
    "evidence": F(("evident", "adjective", "স্পষ্ট / প্রতীয়মান"), ("evidently", "adverb", "স্পষ্টতই")),
    "approach": F(("approachable", "adjective", "সহজে কাছে যাওয়া যায় এমন"),),
    "impact": F(("impactful", "adjective", "প্রভাবশালী"),),
    "issue": F(("issuing", "noun/verb", "জারি করা"),),
    "solution": F(("solve", "verb", "সমাধান করা"), ("solvable", "adjective", "সমাধানযোগ্য")),
    "trend": F(("trendy", "adjective", "ফ্যাশনেবল / চলতি"),),
    "proportion": F(
        ("proportional", "adjective", "আনুপাতিক"),
        ("proportionately", "adverb", "আনুপাতিকভাবে"),
    ),
    "contrast": F(("contrasting", "adjective", "বৈসাদৃশ্যপূর্ণ"),),
    "conclude": F(
        ("conclusion", "noun", "উপসংহার / সিদ্ধান্ত"),
        ("conclusive", "adjective", "চূড়ান্ত / নিশ্চিত"),
    ),
    "argue": F(
        ("argument", "noun", "যুক্তি / তর্ক"),
        ("argumentative", "adjective", "তর্কপ্রিয়"),
    ),
    "opinion": F(("opinionated", "adjective", "একগুঁয়ে মতামতের"),),
    "advantage": F(
        ("advantageous", "adjective", "সুবিধাজনক"),
        ("disadvantage", "noun", "অসুবিধা"),
    ),
    "disadvantage": F(
        ("disadvantaged", "adjective", "সুবিধাবঞ্চিত"),
        ("advantage", "noun", "সুবিধা"),
    ),
    "environment": F(
        ("environmental", "adjective", "পরিবেশগত"),
        ("environmentally", "adverb", "পরিবেশগতভাবে"),
    ),
    "sustainable": F(
        ("sustain", "verb", "টিকিয়ে রাখা"),
        ("sustainability", "noun", "টেকসইতা"),
        ("unsustainable", "adjective", "অটেকসই"),
    ),
    "recycle": F(
        ("recycling", "noun", "রিসাইক্লিং"),
        ("recyclable", "adjective", "রিসাইকেলযোগ্য"),
    ),
    "urban": F(("urbanisation", "noun", "নগরায়ণ"),),
    "rural": F(("rurality", "noun", "গ্রামীণ বৈশিষ্ট্য"),),
    "poverty": F(("poor", "adjective", "দরিদ্র"), ("impoverished", "adjective", "দারিদ্র্যপীড়িত")),
    "equality": F(
        ("equal", "adjective", "সমান"),
        ("equally", "adverb", "সমানভাবে"),
        ("unequal", "adjective", "অসমান"),
    ),
    "community": F(("communal", "adjective", "সাম্প্রদায়িক / যৌথ"),),
    "government": F(
        ("govern", "verb", "শাসন করা"),
        ("governmental", "adjective", "সরকারি"),
    ),
    "academic": F(
        ("academy", "noun", "একাডেমি"),
        ("academically", "adverb", "একাডেমিকভাবে"),
    ),
    "research": F(("researcher", "noun", "গবেষক"),),
    "skill": F(
        ("skilled", "adjective", "দক্ষ"),
        ("skilful", "adjective", "দক্ষ / কুশলী"),
        ("unskilled", "adjective", "অদক্ষ"),
    ),
    "career": F(("careerist", "noun", "ক্যারিয়ারমুখী ব্যক্তি"),),
    "innovation": F(
        ("innovate", "verb", "উদ্ভাবন করা"),
        ("innovative", "adjective", "উদ্ভাবনী"),
        ("innovator", "noun", "উদ্ভাবক"),
    ),
    "digital": F(("digitally", "adverb", "ডিজিটালভাবে"), ("digitise", "verb", "ডিজিটাইজ করা")),
    "access": F(
        ("accessible", "adjective", "সহজলভ্য / প্রবেশযোগ্য"),
        ("accessibility", "noun", "প্রবেশযোগ্যতা"),
        ("inaccessible", "adjective", "দুর্লভ / অপ্রবেশযোগ্য"),
    ),
    "efficient": F(
        ("efficiency", "noun", "দক্ষতা"),
        ("efficiently", "adverb", "দক্ষভাবে"),
        ("inefficient", "adjective", "অদক্ষ"),
    ),
    "essential": F(
        ("essentially", "adverb", "মূলত"),
        ("essence", "noun", "সারকথা / সারাংশ"),
    ),
    "challenge": F(
        ("challenging", "adjective", "চ্যালেঞ্জিং / কঠিন"),
        ("challenger", "noun", "প্রতিদ্বন্দ্বী"),
    ),
    "celebrate": F(
        ("celebration", "noun", "উদযাপন"),
        ("celebratory", "adjective", "উৎসবমুখর"),
    ),
}


def main():
    bank = json.loads(PATH.read_text(encoding="utf-8"))
    assert isinstance(bank, list)
    updated = 0
    for w in bank:
        key = str(w.get("word", "")).strip().lower()
        fam = FAMILIES.get(key)
        if not fam:
            if "word_family" in w:
                del w["word_family"]
            continue
        # do not duplicate the headword inside family
        head = key
        cleaned = []
        seen = set()
        for item in fam:
            ww = str(item["word"]).strip()
            nk = ww.lower()
            if nk == head or nk in seen:
                continue
            seen.add(nk)
            cleaned.append(
                {
                    "word": ww,
                    "pos": item["pos"],
                    "meaning_bn": item["meaning_bn"],
                }
            )
        if cleaned:
            w["word_family"] = cleaned
            updated += 1
        elif "word_family" in w:
            del w["word_family"]

    PATH.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with_f = sum(1 for x in bank if x.get("word_family"))
    print(f"updated {updated}; with_family {with_f}; total {len(bank)}")


if __name__ == "__main__":
    main()
