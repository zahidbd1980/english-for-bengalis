# -*- coding: utf-8 -*-
"""Import curated IELTS/TOEFL/PTE writing pack into vocab bank + lists + spelling.

Packs:
  - Writing linkers / discourse markers
  - Task 1 graph & trend language
  - High-frequency exam collocations (single-word anchors + short phrases)
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VOCAB = ROOT / "data" / "vocabulary.json"
VLISTS = ROOT / "data" / "vocabulary-lists.json"
SLISTS = ROOT / "data" / "spelling-lists.json"

CEFR = {"A1", "A2", "B1", "B2", "C1", "C2"}


def slug_id(word: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", word.strip().lower()).strip("-")
    return f"vocab:{s or 'word'}"


def entry(
    word: str,
    meaning_en: str,
    meaning_bn: str,
    *,
    pos: str = "adverb",
    cefr: str = "B2",
    category: str = "ielts",
    example: str = "",
    example_bn: str = "",
    tags: list[str] | None = None,
    synonyms: list[str] | None = None,
) -> dict:
    ex = example or f"Students should use '{word}' carefully in essays."
    ex_bn = example_bn or f"Essay-এ '{word}' সাবধানে ব্যবহার করুন।"
    return {
        "id": slug_id(word),
        "word": word,
        "phonetic": "",
        "meaning_en": meaning_en,
        "meaning_bn": meaning_bn,
        "part_of_speech": pos,
        "cefr_level": cefr if cefr in CEFR else "B2",
        "category": category,
        "example": ex,
        "example_bn": ex_bn,
        "synonyms": synonyms or [],
        "antonyms": [],
        "word_family": [],
        "tags": tags or ["ielts", "writing"],
    }


# --- curated content ---
LINKERS = [
    entry("moreover", "in addition; used to add a stronger point", "অধিকন্তু / তাছাড়াও",
          example="Moreover, online classes save travel time.",
          example_bn="অধিকন্তু, অনলাইন ক্লাস যাতায়াতের সময় বাঁচায়।",
          synonyms=["furthermore", "additionally"]),
    entry("furthermore", "in addition; also", "অধিকন্তু / আরও বলা যায়",
          example="Furthermore, public transport reduces pollution.",
          example_bn="অধিকন্তু, গণপরিবহন দূষণ কমায়।"),
    entry("additionally", "as an extra point", "অতিরিক্তভাবে / সেই সঙ্গে",
          example="Additionally, libraries offer free internet access.",
          example_bn="অতিরিক্তভাবে, লাইব্রেরিতে ফ্রি ইন্টারনেট থাকে।"),
    entry("nevertheless", "in spite of that; however", "তবুও / তারপরও",
          example="The course is difficult; nevertheless, many finish it.",
          example_bn="কোর্সটি কঠিন; তবুও অনেকে শেষ করেন।",
          synonyms=["nonetheless", "however"]),
    entry("nonetheless", "in spite of what has just been said", "তা সত্ত্বেও / তবুও",
          example="It rains often; nonetheless, tourism is strong.",
          example_bn="প্রায়ই বৃষ্টি হয়; তা সত্ত্বেও পর্যটন শক্তিশালী।"),
    entry("meanwhile", "at the same time", "এই সময়ে / ইতোমধ্যে",
          pos="adverb", cefr="B1",
          example="Parents work; meanwhile, children attend school.",
          example_bn="বাবা-মা কাজ করেন; এই সময়ে সন্তানেরা স্কুলে যায়।"),
    entry("consequently", "as a result", "ফলস্বরূপ / এর ফলে",
          example="Factories closed; consequently, unemployment rose.",
          example_bn="কারখানা বন্ধ হয়েছিল; ফলস্বরূপ বেকারত্ব বেড়েছিল।",
          synonyms=["therefore", "thus"]),
    entry("hence", "for this reason", "এজন্য / অতএব",
          example="Demand fell; hence prices dropped.",
          example_bn="চাহিদা কমেছে; এজন্য দাম কমেছে।"),
    entry("thus", "in this way; therefore", "এভাবে / অতএব",
          example="She practised daily; thus her band score improved.",
          example_bn="সে প্রতিদিন অনুশীলন করেছিল; এভাবে ব্যান্ড স্কোর বেড়েছিল।"),
    entry("accordingly", "in a way that is suitable; therefore", "সেই অনুযায়ী / তদনুসারে",
          example="Rules changed; schools acted accordingly.",
          example_bn="নিয়ম বদলেছে; স্কুলগুলো সেই অনুযায়ী কাজ করেছে।"),
    entry("conversely", "in the opposite way", "উল্টোদিকে / বিপরীতে",
          example="City life is busy; conversely, villages are quieter.",
          example_bn="শহরের জীবন ব্যস্ত; উল্টোদিকে গ্রাম শান্ত।"),
    entry("similarly", "in a similar way", "একইভাবে",
          cefr="B1",
          example="Similarly, recycled paper can protect forests.",
          example_bn="একইভাবে, রিসাইকেল কাগজ বন রক্ষা করতে পারে।"),
    entry("likewise", "in the same way; also", "তেমনি / একইভাবে",
          example="Teachers need training; likewise, parents need guidance.",
          example_bn="শিক্ষকদের প্রশিক্ষণ লাগে; তেমনি অভিভাবকদের গাইডলাইন লাগে।"),
    entry("specifically", "in a detailed or exact way", "বিশেষভাবে / স্পষ্ট করে",
          example="Specifically, Task 2 needs a clear opinion.",
          example_bn="বিশেষভাবে, Task 2-এ স্পষ্ট মতামত লাগে।"),
    entry("particularly", "especially", "বিশেষ করে",
          cefr="B1",
          example="Air pollution is particularly severe in winter.",
          example_bn="শীতকালে বায়ুদূষণ বিশেষ করে তীব্র।"),
    entry("notably", "especially; in a way worth mentioning", "উল্লেখযোগ্যভাবে",
          example="Notably, women joined the workforce in large numbers.",
          example_bn="উল্লেখযোগ্যভাবে, নারীরা বড় সংখ্যায় কর্মক্ষেত্রে যোগ দিয়েছেন।"),
    entry("overall", "in general; considering everything", "মোটের উপর / সামগ্রিকভাবে",
          cefr="B1", pos="adverb",
          example="Overall, the advantages outweigh the drawbacks.",
          example_bn="মোটের উপর, সুবিধা অসুবিধার চেয়ে বেশি।"),
    entry("finally", "used to introduce the last point", "সবশেষে",
          cefr="A2",
          example="Finally, governments should invest in education.",
          example_bn="সবশেষে, সরকারের শিক্ষায় বিনিয়োগ করা উচিত।"),
    entry("firstly", "used to introduce the first point", "প্রথমত",
          cefr="B1",
          example="Firstly, public transport must be affordable.",
          example_bn="প্রথমত, গণপরিবহন সাশ্রয়ী হতে হবে।"),
    entry("secondly", "used to introduce the second point", "দ্বিতীয়ত",
          cefr="B1",
          example="Secondly, roads need better maintenance.",
          example_bn="দ্বিতীয়ত, রাস্তার রক্ষণাবেক্ষণ ভালো করতে হবে।"),
    entry("thirdly", "used to introduce the third point", "তৃতীয়ত",
          cefr="B1",
          example="Thirdly, citizens should follow traffic rules.",
          example_bn="তৃতীয়ত, নাগরিকদের ট্রাফিক নিয়ম মানতে হবে।"),
    entry("despite", "without being affected by", "সত্ত্বেও",
          pos="preposition", cefr="B1",
          example="Despite the cost, many people study abroad.",
          example_bn="খরচ সত্ত্বেও অনেকে বিদেশে পড়েন।"),
    entry("instead", "as an alternative", "পরিবর্তে",
          cefr="A2",
          example="Instead of memorising, practise with examples.",
          example_bn="মুখস্থ করার পরিবর্তে উদাহরণ দিয়ে অনুশীলন করুন।"),
    entry("otherwise", "if not; or else", "না হলে / অন্যথায়",
          cefr="B1",
          example="Submit on time; otherwise you may lose marks.",
          example_bn="সময়মতো জমা দিন; না হলে নম্বর কাটা যেতে পারে।"),
    entry("whereas", "used to contrast two facts", "যেখানে / অন্যদিকে",
          pos="conjunction", cefr="B2",
          example="Some prefer cities, whereas others like villages.",
          example_bn="কেউ শহর পছন্দ করেন, অন্যদিকে কেউ গ্রাম পছন্দ করেন।"),
    entry("although", "even though", "যদিও",
          pos="conjunction", cefr="B1",
          example="Although online learning is flexible, it needs discipline.",
          example_bn="যদিও অনলাইন লার্নিং নমনীয়, এতে শৃঙ্খলা লাগে।"),
    entry("however", "but; used to introduce contrast", "তবে / যাই হোক",
          cefr="B1",
          example="The plan looks good; however, funding is limited.",
          example_bn="পরিকল্পনা ভালো দেখায়; তবে অর্থায়ন সীমিত।"),
    entry("therefore", "for that reason", "অতএব / তাই",
          cefr="B1",
          example="Traffic increased; therefore commute times rose.",
          example_bn="ট্রাফিক বেড়েছে; অতএব যাতায়াতের সময় বেড়েছে।"),
    entry("in addition", "as well as what was said", "এছাড়াও",
          pos="phrase", cefr="B1",
          example="In addition, free clinics help poor families.",
          example_bn="এছাড়াও, ফ্রি ক্লিনিক দরিদ্র পরিবারকে সাহায্য করে।"),
    entry("for example", "used to introduce an example", "উদাহরণস্বরূপ",
          pos="phrase", cefr="A2",
          example="For example, cycling reduces carbon emissions.",
          example_bn="উদাহরণস্বরূপ, সাইকেল চালানো কার্বন নির্গমন কমায়।"),
    entry("for instance", "as an example", "যেমন / উদাহরণ হিসেবে",
          pos="phrase", cefr="B1",
          example="For instance, Singapore taxes cars heavily.",
          example_bn="যেমন, সিঙ্গাপুর গাড়ির ওপর ভারী ট্যাক্স নেয়।"),
    entry("in contrast", "used to show a clear difference", "বিপরীতে",
          pos="phrase", cefr="B2",
          example="In contrast, rural schools often lack labs.",
          example_bn="বিপরীতে, গ্রামীণ স্কুলে প্রায়ই ল্যাব থাকে না।"),
    entry("on the other hand", "used to present the opposite view", "অন্যদিকে",
          pos="phrase", cefr="B1",
          example="On the other hand, private schools may be expensive.",
          example_bn="অন্যদিকে, প্রাইভেট স্কুল ব্যয়বহুল হতে পারে।"),
    entry("as a result", "because of something", "এর ফলে",
          pos="phrase", cefr="B1",
          example="As a result, more students chose online courses.",
          example_bn="এর ফলে আরও শিক্ষার্থী অনলাইন কোর্স বেছে নিয়েছে।"),
    entry("in conclusion", "used to end an essay", "পরিশেষে / উপসংহারে",
          pos="phrase", cefr="B1",
          example="In conclusion, balanced policies are needed.",
          example_bn="পরিশেষে, ভারসাম্যপূর্ণ নীতি দরকার।"),
    entry("to summarise", "to give the main points briefly (UK)", "সংক্ষেপে বলতে গেলে",
          pos="phrase", cefr="B2",
          example="To summarise, education and health should come first.",
          example_bn="সংক্ষেপে বলতে গেলে, শিক্ষা ও স্বাস্থ্য আগে আসা উচিত।"),
    entry("to summarize", "to give the main points briefly (US)", "সংক্ষেপে বলতে গেলে",
          pos="phrase", cefr="B2",
          example="To summarize, both sides have valid points.",
          example_bn="সংক্ষেপে বলতে গেলে, দুই পক্ষেরই যুক্তি আছে।"),
    entry("in summary", "briefly stating the main points", "সারকথায়",
          pos="phrase", cefr="B1",
          example="In summary, investment in skills creates jobs.",
          example_bn="সারকথায়, দক্ষতায় বিনিয়োগ কর্মসংস্থান তৈরি করে।"),
    entry("that said", "despite what has just been said", "তা বলেও / তবে এ কথাও ঠিক",
          pos="phrase", cefr="B2",
          example="Online learning is useful; that said, labs still matter.",
          example_bn="অনলাইন লার্নিং উপকারী; তা বলেও ল্যাব এখনও গুরুত্বপূর্ণ।"),
    entry("by contrast", "used when comparing opposite things", "তুলনায় / বিপরীতে",
          pos="phrase", cefr="B2",
          example="By contrast, older adults prefer face-to-face care.",
          example_bn="তুলনায়, বয়স্করা সরাসরি সেবা পছন্দ করেন।"),
]

TASK1 = [
    entry("increase", "to become larger in number or amount", "বৃদ্ধি পাওয়া / বাড়ানো",
          pos="verb", cefr="A2", category="education",
          example="Sales increased from 20 to 45 units.",
          example_bn="বিক্রি ২০ থেকে ৪৫ ইউনিটে বৃদ্ধি পেয়েছে।",
          tags=["ielts", "writing", "task1"], synonyms=["rise", "grow"]),
    entry("decrease", "to become smaller", "কমে যাওয়া / হ্রাস",
          pos="verb", cefr="A2", category="education",
          example="Unemployment decreased slightly in 2019.",
          example_bn="২০১৯-এ বেকারত্ব সামান্য কমেছে।",
          tags=["ielts", "writing", "task1"], synonyms=["fall", "decline"]),
    entry("rise", "to go up", "ওঠা / বৃদ্ধি",
          pos="verb/noun", cefr="A2", category="education",
          example="There was a sharp rise in fuel prices.",
          example_bn="জ্বালানির দামে তীব্র বৃদ্ধি হয়েছিল।",
          tags=["ielts", "writing", "task1"]),
    entry("fall", "to go down", "পতন / কমে যাওয়া",
          pos="verb/noun", cefr="A2", category="education",
          example="Visitor numbers fell after the pandemic.",
          example_bn="মহামারীর পর পর্যটকের সংখ্যা কমেছে।",
          tags=["ielts", "writing", "task1"]),
    entry("fluctuate", "to rise and fall irregularly", "উঠানামা করা",
          pos="verb", cefr="B2", category="ielts",
          example="Temperatures fluctuated throughout the year.",
          example_bn="সারা বছর তাপমাত্রা উঠানামা করেছে।",
          tags=["ielts", "writing", "task1"]),
    entry("peak", "to reach the highest point", "সর্বোচ্চ বিন্দুতে পৌঁছানো",
          pos="verb/noun", cefr="B1", category="ielts",
          example="Demand peaked in December.",
          example_bn="ডিসেম্বরে চাহিদা সর্বোচ্চ হয়েছিল।",
          tags=["ielts", "writing", "task1"]),
    entry("plunge", "to fall suddenly and steeply", "হঠাৎ তীব্রভাবে পড়ে যাওয়া",
          pos="verb", cefr="B2", category="ielts",
          example="Share prices plunged after the announcement.",
          example_bn="ঘোষণার পর শেয়ারের দাম হঠাৎ তীব্রভাবে পড়েছে।",
          tags=["ielts", "writing", "task1"]),
    entry("soar", "to rise very quickly", "দ্রুত বেড়ে যাওয়া",
          pos="verb", cefr="B2", category="ielts",
          example="Online enrolment soared during lockdown.",
          example_bn="লকডাউনে অনলাইন ভর্তি দ্রুত বেড়েছে।",
          tags=["ielts", "writing", "task1"]),
    entry("stabilize", "to become steady (US spelling)", "স্থিতিশীল হওয়া",
          pos="verb", cefr="B2", category="ielts",
          example="Inflation stabilized after new policies.",
          example_bn="নতুন নীতির পর মুদ্রাস্ফীতি স্থিতিশীল হয়েছে।",
          tags=["ielts", "writing", "task1"]),
    entry("stabilise", "to become steady (UK spelling)", "স্থিতিশীল হওয়া",
          pos="verb", cefr="B2", category="ielts",
          example="The figure stabilised at around 30%.",
          example_bn="সংখ্যা প্রায় ৩০%-এ স্থিতিশীল হয়েছে।",
          tags=["ielts", "writing", "task1"]),
    entry("gradual", "happening slowly over time", "ধীরে ধীরে / ক্রমশ",
          pos="adjective", cefr="B1", category="ielts",
          example="There was a gradual decline in coal use.",
          example_bn="কয়লা ব্যবহারে ধীরে ধীরে হ্রাস হয়েছিল।",
          tags=["ielts", "writing", "task1"]),
    entry("sharp", "sudden and strong (of a change)", "তীব্র / হঠাৎ বড়",
          pos="adjective", cefr="B1", category="ielts",
          example="The chart shows a sharp increase in 2015.",
          example_bn="চার্টে ২০১৫-এ তীব্র বৃদ্ধি দেখা যায়।",
          tags=["ielts", "writing", "task1"]),
    entry("steady", "regular and continuous", "স্থির / নিয়মিত",
          pos="adjective", cefr="B1", category="ielts",
          example="Exports showed a steady rise for five years.",
          example_bn="পাঁচ বছর ধরে রপ্তানিতে স্থির বৃদ্ধি ছিল।",
          tags=["ielts", "writing", "task1"]),
    entry("significant", "large or important enough to notice", "উল্লেখযোগ্য",
          pos="adjective", cefr="B2", category="ielts",
          example="A significant proportion preferred trains.",
          example_bn="উল্লেখযোগ্য অংশ ট্রেন পছন্দ করেছিল।",
          tags=["ielts", "writing", "task1"]),
    entry("proportion", "a part of a whole", "অনুপাত / অংশ",
          pos="noun", cefr="B1", category="education",
          example="The proportion of remote workers grew.",
          example_bn="রিমোট কর্মীর অনুপাত বেড়েছে।",
          tags=["ielts", "writing", "task1"]),
    entry("approximately", "about; not exact", "প্রায়",
          pos="adverb", cefr="B1", category="ielts",
          example="Approximately 40% chose public transport.",
          example_bn="প্রায় ৪০% গণপরিবহন বেছে নিয়েছে।",
          tags=["ielts", "writing", "task1"]),
    entry("respectively", "in the order already mentioned", "যথাক্রমে",
          pos="adverb", cefr="B2", category="ielts",
          example="Men and women scored 6.5 and 7.0 respectively.",
          example_bn="পুরুষ ও নারী যথাক্রমে ৬.৫ ও ৭.০ পেয়েছেন।",
          tags=["ielts", "writing", "task1"]),
    entry("outnumber", "to be more in number than", "সংখ্যায় বেশি হওয়া",
          pos="verb", cefr="B2", category="ielts",
          example="Cyclists outnumbered drivers in the city centre.",
          example_bn="সিটি সেন্টারে সাইকেল আরোহী গাড়িচালকের চেয়ে বেশি ছিল।",
          tags=["ielts", "writing", "task1"]),
    entry("account for", "to be the reason for a part of something", "অংশ হিসেবে থাকা / ব্যাখ্যা করা",
          pos="phrase", cefr="B2", category="ielts",
          example="Renewables accounted for 25% of electricity.",
          example_bn="নবায়নযোগ্য জ্বালানি বিদ্যুতের ২৫% ছিল।",
          tags=["ielts", "writing", "task1"]),
    entry("remain stable", "to stay at a similar level", "স্থিতিশীল থাকা",
          pos="phrase", cefr="B1", category="ielts",
          example="Oil production remained stable after 2018.",
          example_bn="২০১৮-এর পর তেল উৎপাদন স্থিতিশীল ছিল।",
          tags=["ielts", "writing", "task1"]),
    entry("reach a peak", "to arrive at the highest point", "সর্বোচ্চ পর্যায়ে পৌঁছানো",
          pos="phrase", cefr="B1", category="ielts",
          example="Tourism reached a peak in 2017.",
          example_bn="২০১৭-এ পর্যটন সর্বোচ্চ পর্যায়ে পৌঁছেছিল।",
          tags=["ielts", "writing", "task1"]),
    entry("hit a low", "to reach the lowest point", "সর্বনিম্ন পর্যায়ে নামা",
          pos="phrase", cefr="B2", category="ielts",
          example="Attendance hit a low in January.",
          example_bn="জানুয়ারিতে উপস্থিতি সর্বনিম্ন পর্যায়ে নেমেছিল।",
          tags=["ielts", "writing", "task1"]),
]

COLLOCATIONS = [
    entry("make progress", "to improve or advance", "অগ্রগতি করা",
          pos="phrase", cefr="B1", category="education",
          example="Regular feedback helps students make progress.",
          example_bn="নিয়মিত ফিডব্যাক শিক্ষার্থীদের অগ্রগতি করতে সাহায্য করে।",
          tags=["ielts", "collocation", "writing"]),
    entry("make a decision", "to choose what to do", "সিদ্ধান্ত নেওয়া",
          pos="phrase", cefr="A2", category="daily",
          example="Governments must make a decision about funding.",
          example_bn="অর্থায়ন নিয়ে সরকারকে সিদ্ধান্ত নিতে হবে।",
          tags=["ielts", "collocation"]),
    entry("make an effort", "to try hard", "চেষ্টা করা",
          pos="phrase", cefr="B1", category="education",
          example="Learners should make an effort to speak daily.",
          example_bn="শেখার জন্য প্রতিদিন কথা বলার চেষ্টা করা উচিত।",
          tags=["ielts", "collocation"]),
    entry("do research", "to study a subject carefully", "গবেষণা করা",
          pos="phrase", cefr="B1", category="education",
          example="Scientists do research on climate change.",
          example_bn="বিজ্ঞানীরা জলবায়ু পরিবর্তন নিয়ে গবেষণা করেন।",
          tags=["ielts", "collocation", "toefl", "pte"]),
    entry("take into account", "to consider something", "বিবেচনায় নেওয়া",
          pos="phrase", cefr="B2", category="ielts",
          example="Planners must take into account local needs.",
          example_bn="পরিকল্পনাকারীদের স্থানীয় চাহিদা বিবেচনায় নিতে হবে।",
          tags=["ielts", "collocation", "writing"]),
    entry("take part in", "to join an activity", "অংশ নেওয়া",
          pos="phrase", cefr="A2", category="daily",
          example="Many adults take part in evening classes.",
          example_bn="অনেক প্রাপ্তবয়স্ক সন্ধ্যার ক্লাসে অংশ নেন।",
          tags=["ielts", "collocation"]),
    entry("pay attention", "to listen or watch carefully", "মনোযোগ দেওয়া",
          pos="phrase", cefr="A2", category="education",
          example="Pay attention to keywords in Listening.",
          example_bn="Listening-এ কীওয়ার্ডে মনোযোগ দিন।",
          tags=["ielts", "collocation"]),
    entry("play a role", "to have an effect or function", "ভূমিকা রাখা",
          pos="phrase", cefr="B1", category="ielts",
          example="Teachers play a role in student motivation.",
          example_bn="শিক্ষার্থীর মোটিভেশনে শিক্ষকদের ভূমিকা আছে।",
          tags=["ielts", "collocation", "writing"]),
    entry("have an impact on", "to affect something", "প্রভাব ফেলা",
          pos="phrase", cefr="B1", category="ielts",
          example="Social media has an impact on teenagers.",
          example_bn="সোশ্যাল মিডিয়া কিশোরদের ওপর প্রভাব ফেলে।",
          tags=["ielts", "collocation", "writing"]),
    entry("raise awareness", "to make people know about an issue", "সচেতনতা বাড়ানো",
          pos="phrase", cefr="B2", category="ielts",
          example="Campaigns raise awareness about recycling.",
          example_bn="ক্যাম্পেইন রিসাইক্লিং নিয়ে সচেতনতা বাড়ায়।",
          tags=["ielts", "collocation", "writing"]),
    entry("meet the needs", "to provide what is required", "চাহিদা পূরণ করা",
          pos="phrase", cefr="B2", category="office",
          example="Public hospitals must meet the needs of all citizens.",
          example_bn="সরকারি হাসপাতালকে সব নাগরিকের চাহিদা পূরণ করতে হবে।",
          tags=["ielts", "collocation"]),
    entry("provide access to", "to make something available", "প্রবেশাধিকার দেওয়া",
          pos="phrase", cefr="B2", category="education",
          example="Libraries provide access to reliable information.",
          example_bn="লাইব্রেরি নির্ভরযোগ্য তথ্যের প্রবেশাধিকার দেয়।",
          tags=["ielts", "collocation", "toefl"]),
    entry("pose a threat", "to create a danger", "হুমকি সৃষ্টি করা",
          pos="phrase", cefr="B2", category="ielts",
          example="Plastic waste poses a threat to oceans.",
          example_bn="প্লাস্টিক বর্জ্য সমুদ্রের জন্য হুমকি সৃষ্টি করে।",
          tags=["ielts", "collocation", "writing"]),
    entry("draw a conclusion", "to decide something after thinking", "সিদ্ধান্তে আসা",
          pos="phrase", cefr="B2", category="education",
          example="Readers should draw a conclusion from the evidence.",
          example_bn="প্রমাণ দেখে পাঠকদের সিদ্ধান্তে আসা উচিত।",
          tags=["ielts", "collocation", "toefl", "pte"]),
    entry("reach a consensus", "to agree as a group", "ঐকমত্যে পৌঁছানো",
          pos="phrase", cefr="C1", category="office",
          example="Experts rarely reach a consensus quickly.",
          example_bn="বিশেষজ্ঞরা দ্রুত ঐকমত্যে পৌঁছান না।",
          tags=["ielts", "collocation", "writing"]),
    entry("address the issue", "to deal with a problem", "সমস্যা মোকাবিলা করা",
          pos="phrase", cefr="B2", category="ielts",
          example="Policies must address the issue of housing.",
          example_bn="নীতির আবাসন সমস্যা মোকাবিলা করা উচিত।",
          tags=["ielts", "collocation", "writing"]),
    entry("highly likely", "very probable", "অত্যন্ত সম্ভাব্য",
          pos="phrase", cefr="B2", category="ielts",
          example="It is highly likely that demand will grow.",
          example_bn="চাহিদা বাড়বে—এটি অত্যন্ত সম্ভাব্য।",
          tags=["ielts", "collocation", "pte"]),
    entry("widely believed", "accepted by many people", "ব্যাপকভাবে বিশ্বাস করা হয়",
          pos="phrase", cefr="B2", category="ielts",
          example="It is widely believed that exercise improves mood.",
          example_bn="ব্যাপকভাবে বিশ্বাস করা হয় যে ব্যায়াম মুড ভালো করে।",
          tags=["ielts", "collocation", "writing"]),
    entry("key factor", "an important cause or element", "মূল কারণ / গুরুত্বপূর্ণ উপাদান",
          pos="phrase", cefr="B1", category="ielts",
          example="Cost is a key factor in choosing a university.",
          example_bn="বিশ্ববিদ্যালয় বেছে নেওয়ার মূল কারণ খরচ।",
          tags=["ielts", "collocation"]),
    entry("growing concern", "an increasing worry", "বাড়তে থাকা উদ্বেগ",
          pos="phrase", cefr="B2", category="ielts",
          example="There is growing concern about screen time.",
          example_bn="স্ক্রিন টাইম নিয়ে বাড়তে থাকা উদ্বেগ আছে।",
          tags=["ielts", "collocation", "writing"]),
]


def merge_vocab(incoming: list[dict]) -> tuple[int, int, list[str]]:
    bank = json.loads(VOCAB.read_text(encoding="utf-8"))
    by_id = {w["id"]: i for i, w in enumerate(bank)}
    by_word = {w["word"].lower(): i for i, w in enumerate(bank)}
    added = updated = 0
    ids: list[str] = []
    for e in incoming:
        if not e.get("word"):
            continue
        ids.append(e["id"])
        if e["id"] in by_id:
            i = by_id[e["id"]]
            old = bank[i]
            # preserve richer existing fields when new is empty
            for k in ("meaning_bn", "meaning_en", "example", "example_bn"):
                if not e.get(k) and old.get(k):
                    e[k] = old[k]
            bank[i] = {**old, **e, "tags": sorted(set((old.get("tags") or []) + (e.get("tags") or [])))}
            updated += 1
        elif e["word"].lower() in by_word:
            i = by_word[e["word"].lower()]
            old = bank[i]
            e["id"] = old["id"]
            ids[-1] = old["id"]
            bank[i] = {**old, **e, "id": old["id"],
                       "tags": sorted(set((old.get("tags") or []) + (e.get("tags") or [])))}
            by_id[old["id"]] = i
            updated += 1
        else:
            bank.append(e)
            by_id[e["id"]] = len(bank) - 1
            by_word[e["word"].lower()] = len(bank) - 1
            added += 1
    VOCAB.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # dedupe ids preserving order
    seen = set()
    uniq = []
    for i in ids:
        if i not in seen:
            seen.add(i)
            uniq.append(i)
    return added, updated, uniq


def upsert_vocab_list(list_id: str, meta: dict, word_ids: list[str]) -> None:
    lists = meta.get("lists") or []
    titles = {
        "ielts-writing-linkers": (
            "IELTS Writing Linkers",
            "IELTS রাইটিং লিংকার",
            "Discourse markers for Task 2 essays (unofficial).",
            "Task 2 essay-এর discourse marker (অনঅফিসিয়াল)।",
            "B1–C1",
        ),
        "ielts-task1-graphs": (
            "IELTS Writing Task 1 · Graphs",
            "IELTS রাইটিং টাস্ক ১ · গ্রাফ",
            "Trend and comparison language for charts (unofficial).",
            "চার্টের ট্রেন্ড ও তুলনার ভাষা (অনঅফিসিয়াল)।",
            "A2–B2",
        ),
        "exam-collocations-core": (
            "Exam Collocations Core",
            "এক্সাম কলোকেশন কোর",
            "High-frequency collocations for IELTS/TOEFL/PTE (unofficial).",
            "IELTS/TOEFL/PTE-এর বহুল ব্যবহৃত কলোকেশন (অনঅফিসিয়াল)।",
            "B1–C1",
        ),
    }
    title, title_bn, desc, desc_bn, cefr = titles[list_id]
    # keep existing ids first
    existing = []
    for L in lists:
        if L.get("id") == list_id:
            existing = list(L.get("word_ids") or [])
            break
    seen = set(existing)
    for wid in word_ids:
        if wid not in seen:
            existing.append(wid)
            seen.add(wid)
    entry_obj = {
        "id": list_id,
        "title": title,
        "title_bn": title_bn,
        "description": desc,
        "description_bn": desc_bn,
        "cefr": cefr,
        "word_ids": existing,
    }
    replaced = False
    for i, L in enumerate(lists):
        if L.get("id") == list_id:
            lists[i] = entry_obj
            replaced = True
            break
    if not replaced:
        lists.append(entry_obj)
    meta["lists"] = lists


def upsert_spelling(words: list[str], list_id: str, title: str, title_bn: str) -> None:
    meta = json.loads(SLISTS.read_text(encoding="utf-8"))
    lists = meta.get("lists") or []
    clean = []
    seen = set()
    for w in words:
        w = w.strip()
        if not w or " " in w:
            continue
        key = w.lower()
        if key in seen:
            continue
        seen.add(key)
        clean.append(w)
    entry_obj = {
        "id": list_id,
        "title": title,
        "title_bn": title_bn,
        "description": "Spell key writing vocabulary (unofficial).",
        "description_bn": "রাইটিং শব্দের বানান অনুশীলন (অনঅফিসিয়াল)।",
        "target_size": len(clean),
        "words": clean,
    }
    replaced = False
    for i, L in enumerate(lists):
        if L.get("id") == list_id:
            # merge with existing
            old = list(L.get("words") or [])
            for w in old:
                key = w.lower()
                if key not in seen and " " not in w:
                    clean.insert(0, w)
                    seen.add(key)
            entry_obj["words"] = clean
            entry_obj["target_size"] = len(clean)
            lists[i] = entry_obj
            replaced = True
            break
    if not replaced:
        lists.append(entry_obj)
    meta["lists"] = lists
    SLISTS.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    linkers = LINKERS
    task1 = TASK1
    colloc = COLLOCATIONS
    all_entries = linkers + task1 + colloc

    added, updated, _ = merge_vocab(all_entries)
    linker_ids = [e["id"] for e in linkers]
    task1_ids = [e["id"] for e in task1]
    colloc_ids = [e["id"] for e in colloc]
    # resolve ids after merge (word-based remaps)
    bank = json.loads(VOCAB.read_text(encoding="utf-8"))
    by_word = {w["word"].lower(): w["id"] for w in bank}

    def resolve(entries: list[dict]) -> list[str]:
        out = []
        seen = set()
        for e in entries:
            wid = by_word.get(e["word"].lower(), e["id"])
            if wid not in seen:
                seen.add(wid)
                out.append(wid)
        return out

    vmeta = json.loads(VLISTS.read_text(encoding="utf-8"))
    upsert_vocab_list("ielts-writing-linkers", vmeta, resolve(linkers))
    upsert_vocab_list("ielts-task1-graphs", vmeta, resolve(task1))
    upsert_vocab_list("exam-collocations-core", vmeta, resolve(colloc))
    VLISTS.write_text(json.dumps(vmeta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    spell_words = [e["word"] for e in linkers + task1 if " " not in e["word"]]
    upsert_spelling(
        spell_words,
        "ielts-writing-markers",
        "IELTS Writing Markers",
        "IELTS রাইটিং মার্কার",
    )

    print("bank added", added, "updated", updated, "total", len(bank))
    print("linkers", len(resolve(linkers)))
    print("task1", len(resolve(task1)))
    print("collocations", len(resolve(colloc)))


if __name__ == "__main__":
    main()
