# Append IELTS vocabulary + target lists (does not wipe existing bank)
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from cefr_policy import keep_word  # noqa: E402

DATA = ROOT / "data"

IELTS_WORDS = [
  # Academic core (Writing/Reading)
  dict(id="vocab:analyse", word="analyse", meaning_en="to examine something in detail", meaning_bn="বিশ্লেষণ করা", part_of_speech="verb", cefr_level="B1", category="ielts", example="The report analyses the main causes of traffic.", example_bn="রিপোর্টটি যানজটের মূল কারণ বিশ্লেষণ করে।", synonyms=["examine", "study"], antonyms=[]),
  dict(id="vocab:significant", word="significant", meaning_en="important or large enough to notice", meaning_bn="উল্লেখযোগ্য / গুরুত্বপূর্ণ", part_of_speech="adjective", cefr_level="B1", category="ielts", example="There was a significant increase in online learning.", example_bn="অনলাইন লার্নিংয়ে উল্লেখযোগ্য বৃদ্ধি হয়েছিল।", synonyms=["important", "notable"], antonyms=["minor"]),
  dict(id="vocab:benefit", word="benefit", meaning_en="an advantage or useful result", meaning_bn="উপকার / সুবিধা", part_of_speech="noun/verb", cefr_level="B1", category="ielts", example="Exercise has many health benefits.", example_bn="ব্যায়ামের অনেক স্বাস্থ্য উপকার আছে।", synonyms=["advantage", "gain"], antonyms=["drawback"]),
  dict(id="vocab:drawback", word="drawback", meaning_en="a disadvantage", meaning_bn="অসুবিধা / দুর্বলতা", part_of_speech="noun", cefr_level="B1", category="ielts", example="One drawback of city life is pollution.", example_bn="শহরের জীবনের এক অসুবিধা হলো দূষণ।", synonyms=["disadvantage", "downside"], antonyms=["benefit"]),
  dict(id="vocab:evidence", word="evidence", meaning_en="facts or information that support a claim", meaning_bn="প্রমাণ", part_of_speech="noun", cefr_level="B1", category="ielts", example="There is strong evidence that reading improves vocabulary.", example_bn="পড়া শব্দভাণ্ডার বাড়ায়—এর শক্তিশালী প্রমাণ আছে।", synonyms=["proof", "data"], antonyms=[]),
  dict(id="vocab:approach", word="approach", meaning_en="a way of dealing with something", meaning_bn="পদ্ধতি / দৃষ্টিভঙ্গি", part_of_speech="noun/verb", cefr_level="B1", category="ielts", example="A practical approach helps learners improve faster.", example_bn="ব্যবহারিক পদ্ধতি শিক্ষার্থীদের দ্রুত উন্নতিতে সাহায্য করে।", synonyms=["method", "strategy"], antonyms=[]),
  dict(id="vocab:impact", word="impact", meaning_en="a strong effect or influence", meaning_bn="প্রভাব", part_of_speech="noun/verb", cefr_level="B1", category="ielts", example="Social media has a big impact on young people.", example_bn="সোশ্যাল মিডিয়ার তরুণদের ওপর বড় প্রভাব আছে।", synonyms=["effect", "influence"], antonyms=[]),
  dict(id="vocab:issue", word="issue", meaning_en="an important topic or problem", meaning_bn="ইস্যু / সমস্যা / বিষয়", part_of_speech="noun", cefr_level="B1", category="ielts", example="Climate change is a global issue.", example_bn="জলবায়ু পরিবর্তন একটি বৈশ্বিক ইস্যু।", synonyms=["problem", "matter"], antonyms=[]),
  dict(id="vocab:solution", word="solution", meaning_en="a way to solve a problem", meaning_bn="সমাধান", part_of_speech="noun", cefr_level="A2", category="ielts", example="Public transport is one solution to traffic problems.", example_bn="যানজটের এক সমাধান হলো পাবলিক ট্রান্সপোর্ট।", synonyms=["answer", "remedy"], antonyms=[]),
  dict(id="vocab:trend", word="trend", meaning_en="a general direction of change", meaning_bn="প্রবণতা / ট্রেন্ড", part_of_speech="noun", cefr_level="B1", category="ielts", example="The chart shows an upward trend in sales.", example_bn="চার্টে বিক্রয়ের ঊর্ধ্বমুখী প্রবণতা দেখা যায়।", synonyms=["pattern", "tendency"], antonyms=[]),
  dict(id="vocab:proportion", word="proportion", meaning_en="a part of a whole; relative amount", meaning_bn="অনুপাত / অংশ", part_of_speech="noun", cefr_level="B1", category="ielts", example="A large proportion of students study online.", example_bn="বড় অনুপাতের শিক্ষার্থী অনলাইনে পড়ে।", synonyms=["percentage", "share"], antonyms=[]),
  dict(id="vocab:compare", word="compare", meaning_en="to look at similarities and differences", meaning_bn="তুলনা করা", part_of_speech="verb", cefr_level="B1", category="ielts", example="Compare the two graphs carefully.", example_bn="দুই গ্রাফ সাবধানে তুলনা করুন।", synonyms=["contrast"], antonyms=[]),
  dict(id="vocab:contrast", word="contrast", meaning_en="a clear difference between two things", meaning_bn="বৈসাদৃশ্য / পার্থক্য", part_of_speech="noun/verb", cefr_level="B1", category="ielts", example="In contrast, rural areas have cleaner air.", example_bn="বিপরীতে, গ্রামীণ এলাকায় বাতাস পরিষ্কার।", synonyms=["difference"], antonyms=["similarity"]),
  dict(id="vocab:conclude", word="conclude", meaning_en="to decide or finish after considering facts", meaning_bn="সিদ্ধান্তে পৌঁছানো / শেষ করা", part_of_speech="verb", cefr_level="B1", category="ielts", example="I conclude that practice is essential.", example_bn="আমি সিদ্ধান্তে পৌঁছাই যে অনুশীলন অপরিহার্য।", synonyms=["decide", "summarise"], antonyms=[]),
  dict(id="vocab:overall", word="overall", meaning_en="in general; considering everything", meaning_bn="মোটের ওপর / সামগ্রিকভাবে", part_of_speech="adverb/adjective", cefr_level="B1", category="ielts", example="Overall, the benefits outweigh the drawbacks.", example_bn="মোটের ওপর, উপকার অসুবিধার চেয়ে বেশি।", synonyms=["generally", "mainly"], antonyms=[]),

  # Linking / essay language
  dict(id="vocab:therefore", word="therefore", meaning_en="for that reason", meaning_bn="অতএব / তাই", part_of_speech="adverb", cefr_level="B1", category="ielts", example="The roads were flooded; therefore, schools closed.", example_bn="রাস্তা ডুবেছিল; অতএব স্কুল বন্ধ ছিল।", synonyms=["so", "thus"], antonyms=[]),
  dict(id="vocab:however", word="however", meaning_en="but; used to introduce a contrasting idea", meaning_bn="তবে / যাই হোক", part_of_speech="adverb", cefr_level="B1", category="ielts", example="The idea is good; however, it is expensive.", example_bn="আইডিয়া ভালো; তবে এটি ব্যয়বহুল।", synonyms=["but", "nevertheless"], antonyms=[]),
  dict(id="vocab:furthermore", word="furthermore", meaning_en="in addition; also", meaning_bn="অধিকন্তু / তাছাড়া", part_of_speech="adverb", cefr_level="B2", category="ielts", example="Furthermore, free courses help poor students.", example_bn="অধিকন্তু, ফ্রি কোর্স দরিদ্র শিক্ষার্থীদের সাহায্য করে।", synonyms=["moreover", "also"], antonyms=[]),
  dict(id="vocab:although", word="although", meaning_en="even though", meaning_bn="যদিও", part_of_speech="conjunction", cefr_level="B1", category="ielts", example="Although it was raining, they went out.", example_bn="যদিও বৃষ্টি হচ্ছিল, তারা বাইরে গিয়েছিল।", synonyms=["though", "even though"], antonyms=[]),
  dict(id="vocab:whereas", word="whereas", meaning_en="used to show contrast between two facts", meaning_bn="যেখানে / অন্যদিকে", part_of_speech="conjunction", cefr_level="B2", category="ielts", example="City life is busy, whereas village life is calm.", example_bn="শহরের জীবন ব্যস্ত, অন্যদিকে গ্রামের জীবন শান্ত।", synonyms=["while", "but"], antonyms=[]),
  dict(id="vocab:consequently", word="consequently", meaning_en="as a result", meaning_bn="ফলস্বরূপ", part_of_speech="adverb", cefr_level="B2", category="ielts", example="He did not revise; consequently, he failed.", example_bn="সে রিভিশন করেনি; ফলস্বরূপ সে ফেল করেছে।", synonyms=["therefore", "as a result"], antonyms=[]),
  dict(id="vocab:argue", word="argue", meaning_en="to give reasons for or against something", meaning_bn="যুক্তি দেওয়া / তর্ক করা", part_of_speech="verb", cefr_level="B1", category="ielts", example="Some people argue that exams are unfair.", example_bn="কিছু লোক যুক্তি দেয় পরীক্ষা অন্যায্য।", synonyms=["claim", "reason"], antonyms=[]),
  dict(id="vocab:opinion", word="opinion", meaning_en="what someone thinks or believes", meaning_bn="মতামত", part_of_speech="noun", cefr_level="A2", category="ielts", example="In my opinion, education should be free.", example_bn="আমার মতে, শিক্ষা বিনামূল্যে হওয়া উচিত।", synonyms=["view", "belief"], antonyms=[]),
  dict(id="vocab:advantage", word="advantage", meaning_en="a good or useful feature", meaning_bn="সুবিধা", part_of_speech="noun", cefr_level="A2", category="ielts", example="One advantage of buses is low cost.", example_bn="বাসের এক সুবিধা হলো কম খরচ।", synonyms=["benefit", "plus"], antonyms=["disadvantage"]),
  dict(id="vocab:disadvantage", word="disadvantage", meaning_en="a bad feature or problem", meaning_bn="অসুবিধা", part_of_speech="noun", cefr_level="A2", category="ielts", example="A disadvantage of cars is air pollution.", example_bn="গাড়ির এক অসুবিধা হলো বায়ু দূষণ।", synonyms=["drawback", "downside"], antonyms=["advantage"]),

  # Environment & society (common Task 2)
  dict(id="vocab:environment", word="environment", meaning_en="the natural world around us", meaning_bn="পরিবেশ", part_of_speech="noun", cefr_level="A2", category="ielts", example="We must protect the environment.", example_bn="আমাদের পরিবেশ রক্ষা করতে হবে।", synonyms=["nature", "surroundings"], antonyms=[]),
  dict(id="vocab:pollution", word="pollution", meaning_en="dirty air, water, or land from human activity", meaning_bn="দূষণ", part_of_speech="noun", cefr_level="B1", category="ielts", example="Air pollution is serious in big cities.", example_bn="বড় শহরে বায়ু দূষণ গুরুতর।", synonyms=["contamination"], antonyms=["purity"]),
  dict(id="vocab:sustainable", word="sustainable", meaning_en="able to continue without harming the future", meaning_bn="টেকসই", part_of_speech="adjective", cefr_level="B2", category="ielts", example="Cities need sustainable transport systems.", example_bn="শহরগুলোর টেকসই পরিবহন ব্যবস্থা দরকার।", synonyms=["eco-friendly", "long-term"], antonyms=["unsustainable"]),
  dict(id="vocab:recycle", word="recycle", meaning_en="to process used materials so they can be used again", meaning_bn="রিসাইকেল করা / পুনঃব্যবহারযোগ্য করা", part_of_speech="verb", cefr_level="A2", category="ielts", example="People should recycle plastic bottles.", example_bn="মানুষের প্লাস্টিক বোতল রিসাইকেল করা উচিত।", synonyms=["reuse"], antonyms=["waste"]),
  dict(id="vocab:urban", word="urban", meaning_en="related to a city", meaning_bn="শহুরে / নগর", part_of_speech="adjective", cefr_level="B1", category="ielts", example="Urban areas often have better hospitals.", example_bn="শহুরে এলাকায় প্রায়ই ভালো হাসপাতাল থাকে।", synonyms=["city"], antonyms=["rural"]),
  dict(id="vocab:rural", word="rural", meaning_en="related to the countryside", meaning_bn="গ্রামীণ", part_of_speech="adjective", cefr_level="B1", category="ielts", example="Rural communities need better internet.", example_bn="গ্রামীণ সমাজের ভালো ইন্টারনেট দরকার।", synonyms=["countryside"], antonyms=["urban"]),
  dict(id="vocab:poverty", word="poverty", meaning_en="the state of being very poor", meaning_bn="দারিদ্র্য", part_of_speech="noun", cefr_level="B1", category="ielts", example="Education can help reduce poverty.", example_bn="শিক্ষা দারিদ্র্য কমাতে সাহায্য করতে পারে।", synonyms=["hardship"], antonyms=["wealth"]),
  dict(id="vocab:equality", word="equality", meaning_en="the state of being equal", meaning_bn="সমান অধিকার / সমতা", part_of_speech="noun", cefr_level="B1", category="ielts", example="Gender equality is important in workplaces.", example_bn="কর্মক্ষেত্রে জেন্ডার সমতা গুরুত্বপূর্ণ।", synonyms=["fairness"], antonyms=["inequality"]),
  dict(id="vocab:community", word="community", meaning_en="a group of people living in the same area", meaning_bn="সম্প্রদায় / কমিউনিটি", part_of_speech="noun", cefr_level="A2", category="ielts", example="The local community organised a clean-up.", example_bn="স্থানীয় কমিউনিটি পরিষ্কার অভিযান করেছে।", synonyms=["society", "neighbourhood"], antonyms=[]),
  dict(id="vocab:government", word="government", meaning_en="the group of people who control a country", meaning_bn="সরকার", part_of_speech="noun", cefr_level="A2", category="ielts", example="The government should invest in public transport.", example_bn="সরকারের পাবলিক ট্রান্সপোর্টে বিনিয়োগ করা উচিত।", synonyms=["authorities", "state"], antonyms=[]),

  # Education / work / technology themes
  dict(id="vocab:academic", word="academic", meaning_en="related to education and study", meaning_bn="একাডেমিক / শিক্ষাসংক্রান্ত", part_of_speech="adjective", cefr_level="B1", category="ielts", example="She needs strong academic English for university.", example_bn="বিশ্ববিদ্যালয়ের জন্য তার শক্তিশালী একাডেমিক ইংরেজি দরকার।", synonyms=["educational", "scholarly"], antonyms=[]),
  dict(id="vocab:research", word="research", meaning_en="careful study to find new information", meaning_bn="গবেষণা", part_of_speech="noun/verb", cefr_level="B1", category="ielts", example="Recent research supports this idea.", example_bn="সাম্প্রতিক গবেষণা এই ধারণাকে সমর্থন করে।", synonyms=["study", "investigation"], antonyms=[]),
  dict(id="vocab:skill", word="skill", meaning_en="the ability to do something well", meaning_bn="দক্ষতা / স্কিল", part_of_speech="noun", cefr_level="A2", category="ielts", example="Communication skills help in interviews.", example_bn="ইন্টারভিউতে কমিউনিকেশন স্কিল সাহায্য করে।", synonyms=["ability", "expertise"], antonyms=[]),
  dict(id="vocab:career", word="career", meaning_en="a job or profession over a long time", meaning_bn="ক্যারিয়ার / পেশাজীবন", part_of_speech="noun", cefr_level="B1", category="ielts", example="She wants a career in nursing.", example_bn="সে নার্সিংয়ে ক্যারিয়ার করতে চায়।", synonyms=["profession", "occupation"], antonyms=[]),
  dict(id="vocab:innovation", word="innovation", meaning_en="a new idea, method, or product", meaning_bn="উদ্ভাবন", part_of_speech="noun", cefr_level="B2", category="ielts", example="Innovation can improve public services.", example_bn="উদ্ভাবন পাবলিক সার্ভিস উন্নত করতে পারে।", synonyms=["invention", "advance"], antonyms=[]),
  dict(id="vocab:digital", word="digital", meaning_en="using computer technology", meaning_bn="ডিজিটাল", part_of_speech="adjective", cefr_level="A2", category="ielts", example="Digital tools make learning easier.", example_bn="ডিজিটাল টুল শেখাকে সহজ করে।", synonyms=["online", "electronic"], antonyms=["analogue"]),
  dict(id="vocab:access", word="access", meaning_en="the ability or right to use something", meaning_bn="প্রবেশাধিকার / অ্যাক্সেস", part_of_speech="noun/verb", cefr_level="B1", category="ielts", example="Not all students have access to the internet.", example_bn="সব শিক্ষার্থীর ইন্টারনেট অ্যাক্সেস নেই।", synonyms=["entry", "availability"], antonyms=[]),
  dict(id="vocab:efficient", word="efficient", meaning_en="working well without wasting time or resources", meaning_bn="দক্ষ / কার্যকর", part_of_speech="adjective", cefr_level="B1", category="ielts", example="An efficient system saves money.", example_bn="একটি দক্ষ সিস্টেম টাকা বাঁচায়।", synonyms=["effective", "productive"], antonyms=["inefficient"]),
  dict(id="vocab:essential", word="essential", meaning_en="completely necessary", meaning_bn="অপরিহার্য / জরুরি", part_of_speech="adjective", cefr_level="B1", category="ielts", example="Clean water is essential for health.", example_bn="স্বাস্থ্যের জন্য পরিষ্কার পানি অপরিহার্য।", synonyms=["necessary", "vital"], antonyms=["optional"]),
  dict(id="vocab:challenge", word="challenge", meaning_en="a difficult task or problem", meaning_bn="চ্যালেঞ্জ / কঠিন সমস্যা", part_of_speech="noun/verb", cefr_level="B1", category="ielts", example="Finding a job can be a challenge.", example_bn="চাকরি খোঁজা একটি চ্যালেঞ্জ হতে পারে।", synonyms=["difficulty", "obstacle"], antonyms=[]),
]

# Speaking-friendly IELTS topics (everyday but exam useful)
SPEAKING = [
  dict(id="vocab:hobby", word="hobby", meaning_en="an activity you do for enjoyment", meaning_bn="শখ / হবি", part_of_speech="noun", cefr_level="A2", category="ielts", example="My hobby is reading novels.", example_bn="আমার হবি উপন্যাস পড়া।", synonyms=["pastime", "interest"], antonyms=[]),
  dict(id="vocab:neighbourhood", word="neighbourhood", meaning_en="the area around where you live", meaning_bn="পাড়া / এলাকা", part_of_speech="noun", cefr_level="A2", category="ielts", example="My neighbourhood is quiet and friendly.", example_bn="আমার পাড়া শান্ত ও বন্ধুসুলভ।", synonyms=["area", "locality"], antonyms=[]),
  dict(id="vocab:celebrate", word="celebrate", meaning_en="to do something enjoyable for a special event", meaning_bn="উদযাপন করা", part_of_speech="verb", cefr_level="A2", category="ielts", example="We celebrate Pohela Boishakh every year.", example_bn="আমরা প্রতিবছর পহেলা বৈশাখ উদযাপন করি।", synonyms=["mark", "observe"], antonyms=[]),
  dict(id="vocab:prefer", word="prefer", meaning_en="to like one thing more than another", meaning_bn="বেশি পছন্দ করা", part_of_speech="verb", cefr_level="A2", category="ielts", example="I prefer tea to coffee.", example_bn="কফির চেয়ে চা বেশি পছন্দ করি।", synonyms=["favour"], antonyms=[]),
  dict(id="vocab:describe", word="describe", meaning_en="to say what something or someone is like", meaning_bn="বর্ণনা করা", part_of_speech="verb", cefr_level="A2", category="ielts", example="Describe a place you like to visit.", example_bn="এমন এক জায়গার বর্ণনা দাও যেখানে যেতে ভালো লাগে।", synonyms=["explain", "portray"], antonyms=[]),
]

ALL_NEW = IELTS_WORDS + SPEAKING

vocab_path = DATA / "vocabulary.json"
lists_path = DATA / "vocabulary-lists.json"

bank = json.loads(vocab_path.read_text(encoding="utf-8"))
if isinstance(bank, dict):
    words = bank.get("words", [])
else:
    words = bank

existing = {w["id"] for w in words}
added = 0
for w in ALL_NEW:
    # prefer already exists pollution/compare/prefer/describe if present — skip duplicate ids
    if w["id"] in existing:
        continue
    # also skip if same word already in bank under different id
    if any(x.get("word", "").lower() == w["word"].lower() for x in words):
        # still allow if we want ielts category copy? skip to avoid dup cards
        continue
    words.append(w)
    existing.add(w["id"])
    added += 1

# ensure pollution/environment etc that might already exist get referenced in lists by finding ids
def find_id(word):
    for x in words:
        if x.get("word", "").lower() == word.lower():
            return x["id"]
    return None

vocab_path.write_text(json.dumps(words, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

meta = json.loads(lists_path.read_text(encoding="utf-8"))
cats = meta.get("categories", [])
if not any(c["id"] == "ielts" for c in cats):
    cats.append({"id": "ielts", "label": "IELTS", "label_bn": "আইইএলটিএস"})
meta["categories"] = cats

def ids(*words_or_ids):
    out = []
    for item in words_or_ids:
        fid = item if item.startswith("vocab:") else find_id(item)
        if not fid:
            continue
        entry = next((w for w in words if w.get("id") == fid), None)
        if not keep_word(entry):
            continue
        out.append(fid)
    # unique preserve order
    seen = set()
    uniq = []
    for i in out:
        if i not in seen:
            seen.add(i)
            uniq.append(i)
    return uniq

NEW_LISTS = [
  {
    "id": "ielts-academic-core",
    "title": "IELTS Academic Core",
    "title_bn": "IELTS একাডেমিক মূল শব্দ",
    "description": "High-value words for Reading/Writing (analyse, evidence, impact…). Unofficial practice.",
    "description_bn": "রিডিং/রাইটিংয়ের জরুরি শব্দ। অনঅফিসিয়াল প্র্যাকটিস।",
    "word_ids": ids(
      "analyse", "significant", "benefit", "drawback", "evidence", "approach", "impact",
      "issue", "solution", "trend", "proportion", "compare", "contrast", "conclude", "overall",
      "research", "academic", "essential", "efficient", "challenge"
    ),
  },
  {
    "id": "ielts-writing-linkers",
    "title": "IELTS Writing Linkers",
    "title_bn": "IELTS রাইটিং সংযোগকারী শব্দ",
    "description": "Linking words for Task 2 essays: however, therefore, although…",
    "description_bn": "Task 2 রচনার জন্য linking words।",
    "word_ids": ids(
      "therefore", "however", "furthermore", "although", "whereas", "consequently",
      "argue", "opinion", "advantage", "disadvantage", "overall", "conclude", "contrast"
    ),
  },
  {
    "id": "ielts-environment-society",
    "title": "IELTS Environment & Society",
    "title_bn": "IELTS পরিবেশ ও সমাজ",
    "description": "Common essay themes: pollution, urban/rural, poverty, equality.",
    "description_bn": "প্রবন্ধের সাধারণ থিম: দূষণ, শহর-গ্রাম, দারিদ্র্য, সমতা।",
    "word_ids": ids(
      "environment", "pollution", "sustainable", "recycle", "urban", "rural",
      "poverty", "equality", "community", "government", "issue", "solution", "impact", "benefit"
    ),
  },
  {
    "id": "ielts-education-tech",
    "title": "IELTS Education & Technology",
    "title_bn": "IELTS শিক্ষা ও প্রযুক্তি",
    "description": "Study and tech vocabulary for essays and speaking.",
    "description_bn": "পড়াশোনা ও প্রযুক্তি বিষয়ক শব্দ।",
    "word_ids": ids(
      "academic", "research", "skill", "career", "innovation", "digital", "access",
      "efficient", "essential", "opportunity", "improve", "explain", "education"
    ),
  },
  {
    "id": "ielts-speaking-topics",
    "title": "IELTS Speaking Topics",
    "title_bn": "IELTS স্পিকিং টপিক",
    "description": "Useful words for Part 1–2: hobby, neighbourhood, prefer, describe…",
    "description_bn": "Part 1–2 এর জন্য দরকারি শব্দ।",
    "word_ids": ids(
      "hobby", "neighbourhood", "celebrate", "prefer", "describe", "opinion",
      "family", "journey", "weather", "neighbour", "polite", "confident"
    ),
  },
]

lists = meta.get("lists", [])
# remove old ielts lists if re-run
lists = [L for L in lists if not str(L.get("id", "")).startswith("ielts-")]
lists.extend(NEW_LISTS)
meta["lists"] = lists
lists_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print("added_words", added, "total_words", len(words))
for L in NEW_LISTS:
    print(L["id"], len(L["word_ids"]))
