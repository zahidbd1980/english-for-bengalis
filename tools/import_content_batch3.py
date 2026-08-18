# -*- coding: utf-8 -*-
"""Content batch 3: AWL starter, paraphrase pairs, false friends, reading themes."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from cefr_policy import is_beginner_cefr, list_cefr_label  # noqa: E402

VOCAB = ROOT / "data" / "vocabulary.json"
VLISTS = ROOT / "data" / "vocabulary-lists.json"
SLISTS = ROOT / "data" / "spelling-lists.json"
CEFR = {"A1", "A2", "B1", "B2", "C1", "C2"}


def slug_id(word: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", word.strip().lower()).strip("-")
    return f"vocab:{s or 'word'}"


def E(word, meaning_en, meaning_bn, *, pos="noun", cefr="B2", category="education",
      example="", example_bn="", tags=None, synonyms=None):
    return {
        "id": slug_id(word),
        "word": word,
        "phonetic": "",
        "meaning_en": meaning_en,
        "meaning_bn": meaning_bn,
        "part_of_speech": pos,
        "cefr_level": cefr if cefr in CEFR else "B2",
        "category": category,
        "example": example or f"Academic texts often use the word '{word}'.",
        "example_bn": example_bn or f"একাডেমিক লেখায় '{word}' প্রায়ই দেখা যায়।",
        "synonyms": synonyms or [],
        "antonyms": [],
        "word_family": [],
        "tags": tags or ["awl", "academic", "ielts"],
    }


# AWL Sublist-style high-frequency starters (curated BN)
AWL = [
    E("approach", "a way of dealing with something", "পদ্ধতি / দৃষ্টিভঙ্গি", pos="noun/verb", cefr="B1",
      example="A new approach may help weak students.", example_bn="নতুন পদ্ধতি দুর্বল শিক্ষার্থীদের সাহায্য করতে পারে।",
      synonyms=["method", "way"]),
    E("area", "a particular subject or space", "ক্ষেত্র / এলাকা", pos="noun", cefr="A2",
      example="She works in the area of public health.", example_bn="সে পাবলিক হেলথ ক্ষেত্রে কাজ করে।"),
    E("assess", "to judge the quality or amount", "মূল্যায়ন করা", pos="verb", cefr="B2",
      example="Teachers assess writing with clear criteria.", example_bn="শিক্ষকরা স্পষ্ট মানদণ্ডে রাইটিং মূল্যায়ন করেন।",
      synonyms=["evaluate", "judge"]),
    E("assume", "to accept as true without proof", "ধরে নেওয়া", pos="verb", cefr="B1",
      example="Do not assume the reader knows the context.", example_bn="পাঠক কনটেক্সট জানে ধরে নেবেন না।"),
    E("authority", "the power to make decisions; an expert", "কর্তৃপক্ষ / কর্তৃত্ব", pos="noun", cefr="B1",
      example="Local authorities manage city transport.", example_bn="স্থানীয় কর্তৃপক্ষ শহরের পরিবহন পরিচালনা করে।"),
    E("available", "able to be used or obtained", "পাওয়া যায় / লভ্য", pos="adjective", cefr="A2", category="daily",
      example="Grants are available for low-income students.", example_bn="কম আয়ের শিক্ষার্থীদের জন্য অনুদান পাওয়া যায়।"),
    E("benefit", "an advantage", "উপকার / সুবিধা", pos="noun/verb", cefr="A2",
      example="Exercise has many health benefits.", example_bn="ব্যায়ামের অনেক স্বাস্থ্য উপকার আছে।"),
    E("concept", "an idea or principle", "ধারণা / কনসেপ্ট", pos="noun", cefr="B1",
      example="The concept of fairness is central to law.", example_bn="ন্যায়বিচারের ধারণা আইনের কেন্দ্রে।"),
    E("consist", "to be made up of", "গঠিত হওয়া", pos="verb", cefr="B1",
      example="The course consists of lectures and labs.", example_bn="কোর্সটি লেকচার ও ল্যাব নিয়ে গঠিত।"),
    E("constitute", "to form or make up", "গঠন করা", pos="verb", cefr="B2",
      example="Women constitute half of the workforce.", example_bn="কর্মক্ষেত্রের অর্ধেক নারী।"),
    E("context", "the situation in which something happens", "প্রসঙ্গ / কনটেক্সট", pos="noun", cefr="B1",
      example="Always explain new words in context.", example_bn="নতুন শব্দ সবসময় প্রসঙ্গে ব্যাখ্যা করুন।"),
    E("contract", "a legal agreement", "চুক্তি", pos="noun/verb", cefr="B1", category="office",
      example="They signed a one-year contract.", example_bn="তারা এক বছরের চুক্তি সই করেছে।"),
    E("create", "to make something new", "তৈরি করা", pos="verb", cefr="A1", category="daily",
      example="Good policy can create more jobs.", example_bn="ভালো নীতি আরও কর্মসংস্থান তৈরি করতে পারে।"),
    E("data", "facts or information", "তথ্য / ডেটা", pos="noun", cefr="A2",
      example="The data support the main claim.", example_bn="তথ্য মূল দাবিকে সমর্থন করে।"),
    E("define", "to explain the meaning of a word", "সংজ্ঞায়িত করা", pos="verb", cefr="B1",
      example="Please define the key terms clearly.", example_bn="মূল শব্দগুলো স্পষ্টভাবে সংজ্ঞায়িত করুন।"),
    E("derive", "to get something from a source", "উদ্ভূত হওয়া / পাওয়া", pos="verb", cefr="B2",
      example="Many English words derive from Latin.", example_bn="অনেক ইংরেজি শব্দ ল্যাটিন থেকে এসেছে।"),
    E("distribute", "to give out to many people", "বিতরণ করা", pos="verb", cefr="B1",
      example="NGOs distribute food after floods.", example_bn="বন্যার পর এনজিওরা খাবার বিতরণ করে।"),
    E("economy", "the system of money and trade", "অর্থনীতি", pos="noun", cefr="B1",
      example="Tourism supports the local economy.", example_bn="পর্যটন স্থানীয় অর্থনীতিকে সহায়তা করে।"),
    E("environment", "the natural world; surroundings", "পরিবেশ", pos="noun", cefr="B1", category="nature",
      example="Factories can damage the environment.", example_bn="কারখানা পরিবেশের ক্ষতি করতে পারে।"),
    E("establish", "to start or create permanently", "প্রতিষ্ঠা করা", pos="verb", cefr="B2",
      example="The university established a research centre.", example_bn="বিশ্ববিদ্যালয় একটি গবেষণা কেন্দ্র প্রতিষ্ঠা করেছে।"),
    E("estimate", "to roughly calculate", "আনুমানিক হিসাব করা", pos="verb/noun", cefr="B1",
      example="Experts estimate the cost at $2 million.", example_bn="বিশেষজ্ঞরা খরচ প্রায় ২০ লাখ ডলার অনুমান করেন।"),
    E("evident", "clear; easy to see", "স্পষ্ট / প্রমাণিত", pos="adjective", cefr="B2",
      example="It is evident that demand is rising.", example_bn="স্পষ্ট যে চাহিদা বাড়ছে।"),
    E("export", "to sell goods to another country", "রপ্তানি", pos="noun/verb", cefr="B1", category="office",
      example="Bangladesh exports garments worldwide.", example_bn="বাংলাদেশ বিশ্বব্যাপী পোশাক রপ্তানি করে।"),
    E("factor", "something that influences a result", "কারণ / উপাদান", pos="noun", cefr="B1",
      example="Cost is a key factor in this decision.", example_bn="এই সিদ্ধান্তে খরচ একটি মূল কারণ।"),
    E("finance", "the management of money", "অর্থায়ন / ফাইন্যান্স", pos="noun/verb", cefr="B1", category="office",
      example="Students need finance for tuition fees.", example_bn="টিউশন ফির জন্য শিক্ষার্থীদের অর্থায়ন লাগে।"),
    E("formula", "a method or set of rules", "সূত্র / ফর্মুলা", pos="noun", cefr="B1",
      example="There is no single formula for success.", example_bn="সাফল্যের একক সূত্র নেই।"),
    E("function", "the purpose of something", "কার্য / ফাংশন", pos="noun/verb", cefr="B1",
      example="The main function of schools is education.", example_bn="স্কুলের মূল কার্য শিক্ষা।"),
    E("identify", "to recognise or name", "শনাক্ত করা", pos="verb", cefr="B1",
      example="Identify the writer's main argument.", example_bn="লেখকের মূল যুক্তি শনাক্ত করুন।"),
    E("income", "money received regularly", "আয়", pos="noun", cefr="A2", category="office",
      example="Higher education can raise lifetime income.", example_bn="উচ্চ শিক্ষা জীবনব্যাপী আয় বাড়াতে পারে।"),
    E("indicate", "to show or suggest", "নির্দেশ করা", pos="verb", cefr="B1",
      example="Surveys indicate growing concern.", example_bn="জরিপ বাড়তে থাকা উদ্বেগ নির্দেশ করে।"),
    E("individual", "a single person", "ব্যক্তি", pos="noun/adjective", cefr="A2",
      example="Each individual has different needs.", example_bn="প্রত্যেক ব্যক্তির চাহিদা আলাদা।"),
    E("interpret", "to explain the meaning", "ব্যাখ্যা করা", pos="verb", cefr="B2",
      example="Students must interpret the graph carefully.", example_bn="শিক্ষার্থীদের গ্রাফ সাবধানে ব্যাখ্যা করতে হবে।"),
    E("involve", "to include as a necessary part", "জড়িত করা / অন্তর্ভুক্ত করা", pos="verb", cefr="B1",
      example="The project involves three departments.", example_bn="প্রকল্পে তিনটি বিভাগ জড়িত।"),
    E("issue", "an important topic; a problem", "ইস্যু / সমস্যা", pos="noun", cefr="B1",
      example="Housing is a major urban issue.", example_bn="আবাসন একটি বড় নগর সমস্যা।"),
    E("labour", "work; workers as a group (UK)", "শ্রম / শ্রমিক", pos="noun", cefr="B1", category="office",
      example="Cheap labour attracted foreign factories.", example_bn="সস্তা শ্রম বিদেশি কারখানা আকর্ষণ করেছিল।"),
    E("legal", "connected with the law", "আইনি", pos="adjective", cefr="B1", category="office",
      example="There are legal limits on working hours.", example_bn="কর্মঘণ্টার আইনি সীমা আছে।"),
    E("legislate", "to make laws", "আইন প্রণয়ন করা", pos="verb", cefr="C1",
      example="Parliaments legislate on tax policy.", example_bn="পার্লামেন্ট কর নীতিতে আইন প্রণয়ন করে।"),
    E("major", "important; main", "প্রধান / বড়", pos="adjective", cefr="A2",
      example="Traffic is a major problem in Dhaka.", example_bn="ঢাকায় ট্রাফিক একটি প্রধান সমস্যা।"),
    E("method", "a way of doing something", "পদ্ধতি", pos="noun", cefr="A2",
      example="This method saves time.", example_bn="এই পদ্ধতি সময় বাঁচায়।"),
    E("occur", "to happen", "ঘটা", pos="verb", cefr="B1",
      example="Floods often occur during monsoon.", example_bn="বন্যা প্রায়ই বর্ষায় ঘটে।"),
    E("percent", "in each hundred", "শতাংশ", pos="noun", cefr="A2",
      example="About 30 percent prefer trains.", example_bn="প্রায় ৩০ শতাংশ ট্রেন পছন্দ করে।"),
    E("period", "a length of time", "সময়কাল", pos="noun", cefr="A2", category="daily",
      example="During this period sales doubled.", example_bn="এই সময়কালে বিক্রি দ্বিগুণ হয়েছে।"),
    E("policy", "a plan of action by a government/org", "নীতি", pos="noun", cefr="B1",
      example="Education policy affects every family.", example_bn="শিক্ষা নীতি প্রতিটি পরিবারকে প্রভাবিত করে।"),
    E("principle", "a basic rule or belief", "নীতি / মূলনীতি", pos="noun", cefr="B2",
      example="Equality is a core principle of democracy.", example_bn="সমতা গণতন্ত্রের মূলনীতি।"),
    E("proceed", "to continue", "এগিয়ে যাওয়া", pos="verb", cefr="B2",
      example="Please proceed to the next question.", example_bn="পরের প্রশ্নে এগিয়ে যান।"),
    E("process", "a series of actions", "প্রক্রিয়া", pos="noun/verb", cefr="B1",
      example="Learning is a long process.", example_bn="শেখা একটি দীর্ঘ প্রক্রিয়া।"),
    E("require", "to need", "প্রয়োজন হওয়া", pos="verb", cefr="A2",
      example="The job requires strong writing skills.", example_bn="চাকরিতে শক্তিশালী রাইটিং দক্ষতা প্রয়োজন।"),
    E("research", "careful study to find facts", "গবেষণা", pos="noun/verb", cefr="A2",
      example="More research is needed on air quality.", example_bn="বায়ুর মান নিয়ে আরও গবেষণা দরকার।"),
    E("respond", "to reply or react", "প্রতিক্রিয়া জানানো", pos="verb", cefr="A2", category="daily",
      example="Governments must respond to emergencies.", example_bn="জরুরি অবস্থায় সরকারকে প্রতিক্রিয়া জানাতে হবে।"),
    E("role", "the function of a person or thing", "ভূমিকা", pos="noun", cefr="A2",
      example="Parents play a key role in education.", example_bn="শিক্ষায় অভিভাবকদের মূল ভূমিকা আছে।"),
    E("section", "a part of a whole", "অংশ / সেকশন", pos="noun", cefr="A2",
      example="Read section 2 carefully.", example_bn="সেকশন ২ সাবধানে পড়ুন।"),
    E("sector", "a part of the economy", "খাত / সেক্টর", pos="noun", cefr="B2", category="office",
      example="The health sector needs more nurses.", example_bn="স্বাস্থ্য খাতে আরও নার্স দরকার।"),
    E("significant", "important or large enough to notice", "উল্লেখযোগ্য", pos="adjective", cefr="B2",
      example="There was a significant rise in fees.", example_bn="ফি-তে উল্লেখযোগ্য বৃদ্ধি হয়েছিল।"),
    E("similar", "almost the same", "সদৃশ / একই রকম", pos="adjective", cefr="A1", category="daily",
      example="The two charts show similar patterns.", example_bn="দুই চার্টে একই রকম ধরন দেখা যায়।"),
    E("source", "the place something comes from", "উৎস", pos="noun", cefr="B1",
      example="Cite every source in your essay.", example_bn="Essay-এ প্রতিটি উৎস উল্লেখ করুন।"),
    E("specific", "particular; exact", "নির্দিষ্ট", pos="adjective", cefr="B1",
      example="Give a specific example from your city.", example_bn="আপনার শহর থেকে একটি নির্দিষ্ট উদাহরণ দিন।"),
    E("structure", "the way parts are organised", "কাঠামো", pos="noun/verb", cefr="B1",
      example="A clear structure improves essays.", example_bn="স্পষ্ট কাঠামো essay উন্নত করে।"),
    E("theory", "an idea that explains something", "তত্ত্ব", pos="noun", cefr="B1",
      example="The theory was later tested in labs.", example_bn="তত্ত্বটি পরে ল্যাবে পরীক্ষা করা হয়েছিল।"),
    E("vary", "to be different in different cases", "ভিন্ন হওয়া / পরিবর্তিত হওয়া", pos="verb", cefr="B1",
      example="Opinions vary across age groups.", example_bn="বয়সগোষ্ঠীতে মতামত ভিন্ন।"),
]

# Paraphrase anchors (exam synonym practice) — store as useful academic synonyms
PARA = [
    E("important", "of great value or influence", "গুরুত্বপূর্ণ", pos="adjective", cefr="A1", category="daily",
      example="Education is important for development.", example_bn="উন্নয়নের জন্য শিক্ষা গুরুত্বপূর্ণ।",
      tags=["paraphrase", "ielts"], synonyms=["crucial", "significant", "vital"]),
    E("crucial", "extremely important", "অত্যন্ত গুরুত্বপূর্ণ", pos="adjective", cefr="B2",
      example="Clean water is crucial for public health.", example_bn="জনস্বাস্থ্যের জন্য বিশুদ্ধ পানি অত্যন্ত গুরুত্বপূর্ণ।",
      tags=["paraphrase", "ielts"], synonyms=["vital", "essential"]),
    E("essential", "absolutely necessary", "অপরিহার্য", pos="adjective", cefr="B1",
      example="Sleep is essential for memory.", example_bn="মেমোরির জন্য ঘুম অপরিহার্য।",
      tags=["paraphrase", "ielts"]),
    E("show", "to make something visible or clear", "দেখানো", pos="verb", cefr="A1", category="daily",
      example="The chart shows a clear rise.", example_bn="চার্ট স্পষ্ট বৃদ্ধি দেখায়।",
      tags=["paraphrase", "ielts"], synonyms=["illustrate", "demonstrate", "indicate"]),
    E("improve", "to make better", "উন্নত করা", pos="verb", cefr="A2",
      example="Practice helps improve fluency.", example_bn="অনুশীলন ফ্লুয়েন্সি উন্নত করে।",
      tags=["paraphrase", "ielts"], synonyms=["enhance", "boost", "develop"]),
    E("enhance", "to improve the quality of something", "উন্নীত করা / বাড়ানো", pos="verb", cefr="B2",
      example="Training can enhance workplace skills.", example_bn="প্রশিক্ষণ কর্মক্ষেত্রের দক্ষতা বাড়াতে পারে।",
      tags=["paraphrase", "ielts", "pte"]),
    E("reduce", "to make smaller", "কমানো", pos="verb", cefr="A2", category="daily",
      example="Cycling can reduce traffic congestion.", example_bn="সাইকেল চালানো ট্রাফিক জট কমাতে পারে।",
      tags=["paraphrase", "ielts"], synonyms=["decrease", "cut", "lower"]),
    E("increase", "to become larger", "বাড়ানো / বৃদ্ধি", pos="verb/noun", cefr="A2",
      example="Cities need to increase green space.", example_bn="শহরে সবুজ স্থান বাড়াতে হবে।",
      tags=["paraphrase", "ielts"], synonyms=["rise", "grow", "expand"]),
    E("problem", "a difficult situation", "সমস্যা", pos="noun", cefr="A1", category="daily",
      example="Air pollution is a serious problem.", example_bn="বায়ুদূষণ একটি গুরুতর সমস্যা।",
      tags=["paraphrase", "ielts"], synonyms=["issue", "challenge", "difficulty"]),
    E("challenge", "a difficult task", "চ্যালেঞ্জ / কঠিন কাজ", pos="noun", cefr="B1",
      example="Finding affordable housing is a challenge.", example_bn="সাশ্রয়ী আবাসন খোঁজা একটি চ্যালেঞ্জ।",
      tags=["paraphrase", "ielts"]),
    E("advantage", "a good or useful feature", "সুবিধা", pos="noun", cefr="A2",
      example="One advantage of buses is low cost.", example_bn="বাসের একটি সুবিধা কম খরচ।",
      tags=["paraphrase", "ielts"], synonyms=["benefit", "merit", "plus"]),
    E("disadvantage", "a negative feature", "অসুবিধা", pos="noun", cefr="A2",
      example="A disadvantage of cars is pollution.", example_bn="গাড়ির একটি অসুবিধা দূষণ।",
      tags=["paraphrase", "ielts"], synonyms=["drawback", "downside"]),
    E("drawback", "a disadvantage", "অসুবিধা / নেতিবাচক দিক", pos="noun", cefr="B2",
      example="The main drawback is high tuition fees.", example_bn="মূল অসুবিধা উচ্চ টিউশন ফি।",
      tags=["paraphrase", "ielts"]),
    E("people", "human beings in general", "মানুষ", pos="noun", cefr="A1", category="daily",
      example="Many people work from home now.", example_bn="এখন অনেকে বাড়ি থেকে কাজ করেন।",
      tags=["paraphrase", "ielts"], synonyms=["individuals", "citizens", "residents"]),
    E("citizen", "a member of a country/city", "নাগরিক", pos="noun", cefr="B1",
      example="Citizens expect better public services.", example_bn="নাগরিকরা ভালো পাবলিক সার্ভিস আশা করেন।",
      tags=["paraphrase", "ielts"]),
    E("help", "to make it easier for someone", "সাহায্য করা", pos="verb/noun", cefr="A1", category="daily",
      example="Mentors help new students settle in.", example_bn="মেন্টররা নতুন শিক্ষার্থীদের মানিয়ে নিতে সাহায্য করেন।",
      tags=["paraphrase", "ielts"], synonyms=["assist", "support", "aid"]),
    E("assist", "to help", "সহায়তা করা", pos="verb", cefr="B1", category="office",
      example="Volunteers assist elderly patients.", example_bn="স্বেচ্ছাসেবকরা বয়স্ক রোগীদের সহায়তা করেন।",
      tags=["paraphrase", "ielts", "toefl"]),
    E("cause", "to make something happen", "কারণ হওয়া / ঘটানো", pos="verb/noun", cefr="A2",
      example="Heavy rain can cause floods.", example_bn="ভারী বৃষ্টি বন্যা ঘটাতে পারে।",
      tags=["paraphrase", "ielts"], synonyms=["lead to", "result in", "trigger"]),
    E("because", "for the reason that", "কারণ", pos="conjunction", cefr="A1", category="daily",
      example="I stayed home because I was ill.", example_bn="অসুস্থ থাকায় বাড়িতে ছিলাম।",
      tags=["paraphrase", "ielts"], synonyms=["since", "as", "due to"]),
    E("due to", "because of", "এর কারণে", pos="phrase", cefr="B1",
      example="Classes were cancelled due to the storm.", example_bn="ঝড়ের কারণে ক্লাস বাতিল হয়েছিল।",
      tags=["paraphrase", "ielts"]),
    E("many", "a large number of", "অনেক", pos="determiner", cefr="A1", category="daily",
      example="Many students prefer online classes.", example_bn="অনেক শিক্ষার্থী অনলাইন ক্লাস পছন্দ করে।",
      tags=["paraphrase", "ielts"], synonyms=["numerous", "a large number of", "plenty of"]),
    E("numerous", "very many", "অসংখ্য / প্রচুর", pos="adjective", cefr="B2",
      example="There are numerous reasons for migration.", example_bn="মাইগ্রেশনের অসংখ্য কারণ আছে।",
      tags=["paraphrase", "ielts"]),
    E("get", "to obtain or receive", "পাওয়া", pos="verb", cefr="A1", category="daily",
      example="Students get feedback after each test.", example_bn="প্রতি পরীক্ষার পর শিক্ষার্থীরা ফিডব্যাক পায়।",
      tags=["paraphrase", "ielts"], synonyms=["obtain", "receive", "gain"]),
    E("obtain", "to get something", "অর্জন করা / পাওয়া", pos="verb", cefr="B2",
      example="Applicants must obtain a visa first.", example_bn="আবেদনকারীদের আগে ভিসা পেতে হবে।",
      tags=["paraphrase", "ielts", "toefl"]),
    E("think", "to have an opinion", "ভাবা / মনে করা", pos="verb", cefr="A1", category="daily",
      example="Some people think cities are safer.", example_bn="কেউ কেউ মনে করেন শহর নিরাপদ।",
      tags=["paraphrase", "ielts"], synonyms=["believe", "argue", "consider"]),
    E("believe", "to accept as true", "বিশ্বাস করা", pos="verb", cefr="A1", category="daily",
      example="I believe practice builds confidence.", example_bn="আমি বিশ্বাস করি অনুশীলন আত্মবিশ্বাস বাড়ায়।",
      tags=["paraphrase", "ielts"]),
    E("good", "of high quality; positive", "ভালো", pos="adjective", cefr="A1", category="daily",
      example="A good argument needs evidence.", example_bn="ভালো যুক্তির প্রমাণ লাগে।",
      tags=["paraphrase", "ielts"], synonyms=["effective", "beneficial", "positive"]),
    E("effective", "producing the result you want", "কার্যকর", pos="adjective", cefr="B1",
      example="Clear feedback is effective for learners.", example_bn="স্পষ্ট ফিডব্যাক শিক্ষার্থীদের জন্য কার্যকর।",
      tags=["paraphrase", "ielts", "pte"]),
    E("bad", "of low quality; negative", "খারাপ", pos="adjective", cefr="A1", category="daily",
      example="Bad diet affects concentration.", example_bn="খারাপ খাবার মনোযোগে প্রভাব ফেলে।",
      tags=["paraphrase", "ielts"], synonyms=["harmful", "negative", "poor"]),
    E("harmful", "causing damage", "ক্ষতিকর", pos="adjective", cefr="B1", category="health",
      example="Smog is harmful to children.", example_bn="ধোঁয়াশা শিশুদের জন্য ক্ষতিকর।",
      tags=["paraphrase", "ielts"]),
]

FALSE = [
    E("actually", "in fact (NOT 'currently')", "আসলে (বাংলা 'আসলে'; ≠ 'এখন')", pos="adverb", cefr="B1", category="daily",
      example="Actually, the train is on time.", example_bn="আসলে ট্রেন সময়মতো আছে।",
      tags=["false-friend", "bn"]),
    E("eventually", "in the end; finally (NOT 'possibly')", "শেষ পর্যন্ত (অর্থ 'সম্ভবত' নয়)", pos="adverb", cefr="B1", category="daily",
      example="Eventually, she passed the exam.", example_bn="শেষ পর্যন্ত সে পরীক্ষায় পাস করেছে।",
      tags=["false-friend", "bn"]),
    E("sympathetic", "showing care for someone's feelings (NOT 'nice/likable')", "সহানুভূতিশীল (শুধু 'ভদ্র' নয়)", pos="adjective", cefr="B2", category="daily",
      example="The nurse was sympathetic to the patient.", example_bn="নার্স রোগীর প্রতি সহানুভূতিশীল ছিলেন।",
      tags=["false-friend", "bn"]),
    E("sensible", "practical and wise (NOT 'sensitive')", "বিচক্ষণ / বুদ্ধিমান (sensitive নয়)", pos="adjective", cefr="B1", category="daily",
      example="It is sensible to revise every day.", example_bn="প্রতিদিন রিভিশন করা বিচক্ষণ।",
      tags=["false-friend", "bn"]),
    E("sensitive", "easily affected; needing care", "সংবেদনশীল", pos="adjective", cefr="B1", category="daily",
      example="This is a sensitive political issue.", example_bn="এটি একটি সংবেদনশীল রাজনৈতিক ইস্যু।",
      tags=["false-friend", "bn"]),
    E("interesting", "holding your attention (NOT only 'important')", "মজার / আকর্ষণীয়", pos="adjective", cefr="A1", category="daily",
      example="The documentary was interesting.", example_bn="ডকুমেন্টারিটি আকর্ষণীয় ছিল।",
      tags=["false-friend", "bn"]),
    E("interested", "wanting to know more", "আগ্রহী", pos="adjective", cefr="A1", category="daily",
      example="I am interested in public speaking.", example_bn="আমি পাবলিক স্পিকিংয়ে আগ্রহী।",
      tags=["false-friend", "bn"]),
    E("library", "place for books (NOT bookshop)", "লাইব্রেরি (বইয়ের দোকান নয়)", pos="noun", cefr="A1", category="education",
      example="Borrow novels from the library.", example_bn="লাইব্রেরি থেকে উপন্যাস ধার নিন।",
      tags=["false-friend", "bn"]),
    E("college", "higher education institution (sense differs by country)", "কলেজ / উচ্চশিক্ষা প্রতিষ্ঠান", pos="noun", cefr="A2", category="education",
      example="She starts college next autumn.", example_bn="সে আগামী শরতে কলেজ শুরু করবে।",
      tags=["false-friend", "bn"]),
    E("faculty", "teaching staff / department (NOT only 'ability')", "ফ্যাকাল্টি / বিভাগ (শুধু 'দক্ষতা' নয়)", pos="noun", cefr="B2", category="education",
      example="The science faculty published new research.", example_bn="সায়েন্স ফ্যাকাল্টি নতুন গবেষণা প্রকাশ করেছে।",
      tags=["false-friend", "bn"]),
    E("fabric", "cloth material (NOT building structure)", "কাপড়ের উপাদান (ভবনের কাঠামো নয়)", pos="noun", cefr="B1", category="shopping",
      example="This fabric is soft and durable.", example_bn="এই কাপড় নরম ও টেকসই।",
      tags=["false-friend", "bn"]),
    E("novel", "a long story book; new/original", "উপন্যাস / নতুন ধরনের", pos="noun/adjective", cefr="B1", category="education",
      example="She wrote a novel about migration.", example_bn="সে মাইগ্রেশন নিয়ে একটি উপন্যাস লিখেছে।",
      tags=["false-friend", "bn"]),
    E("lecture", "an academic talk (NOT 'reading a book')", "লেকচার / ক্লাস বক্তৃতা", pos="noun", cefr="A2", category="education",
      example="The lecture starts at 10 a.m.", example_bn="লেকচার সকাল ১০টায় শুরু।",
      tags=["false-friend", "bn"]),
    E("prescription", "doctor's written order for medicine", "প্রেসক্রিপশন / ওষুধের নির্দেশ", pos="noun", cefr="B1", category="health",
      example="Take this prescription to the pharmacy.", example_bn="এই প্রেসক্রিপশন ফার্মেসিতে দিন।",
      tags=["false-friend", "bn"]),
    E("recipe", "instructions for cooking (NOT medical)", "রান্নার রেসিপি (ওষুধ নয়)", pos="noun", cefr="A2", category="food",
      example="This recipe needs only five ingredients.", example_bn="এই রেসিপিতে মাত্র পাঁচটি উপকরণ লাগে।",
      tags=["false-friend", "bn"]),
]

THEME = [
    E("urbanisation", "growth of cities (UK)", "নগরায়ণ", pos="noun", cefr="B2", category="nature",
      example="Rapid urbanisation increases housing demand.", example_bn="দ্রুত নগরায়ণ আবাসনের চাহিদা বাড়ায়।",
      tags=["ielts", "reading", "theme"]),
    E("urbanization", "growth of cities (US)", "নগরায়ণ", pos="noun", cefr="B2", category="nature",
      example="Urbanization can strain public transport.", example_bn="নগরায়ণ গণপরিবহনে চাপ ফেলতে পারে।",
      tags=["toefl", "reading", "theme"]),
    E("infrastructure", "basic systems like roads and power", "অবকাঠামো", pos="noun", cefr="B2", category="office",
      example="Cities need better infrastructure.", example_bn="শহরে ভালো অবকাঠামো দরকার।",
      tags=["ielts", "reading", "theme"]),
    E("congestion", "too much traffic in one place", "যানজট", pos="noun", cefr="B2", category="travel",
      example="Congestion wastes commuting time.", example_bn="যানজট যাতায়াতের সময় নষ্ট করে।",
      tags=["ielts", "reading", "theme"]),
    E("emissions", "gases released into the air", "নির্গমন / এমিশন", pos="noun", cefr="B2", category="nature",
      example="Transport emissions harm air quality.", example_bn="পরিবহন এমিশন বায়ুর মান নষ্ট করে।",
      tags=["ielts", "reading", "theme"]),
    E("renewable", "able to be replaced naturally", "নবায়নযোগ্য", pos="adjective", cefr="B2", category="nature",
      example="Renewable energy includes solar power.", example_bn="নবায়নযোগ্য জ্বালানিতে সোলার পাওয়ার আছে।",
      tags=["ielts", "reading", "theme"]),
    E("sustainable", "able to continue without harming the future", "টেকসই", pos="adjective", cefr="B2", category="nature",
      example="Cities need sustainable transport plans.", example_bn="শহরে টেকসই পরিবহন পরিকল্পনা লাগে।",
      tags=["ielts", "reading", "theme"]),
    E("biodiversity", "variety of living things", "জীববৈচিত্র্য", pos="noun", cefr="C1", category="nature",
      example="Forests protect biodiversity.", example_bn="বন জীববৈচিত্র্য রক্ষা করে।",
      tags=["ielts", "reading", "theme"]),
    E("deforestation", "clearing forests", "বন উজাড়", pos="noun", cefr="B2", category="nature",
      example="Deforestation increases flood risk.", example_bn="বন উজাড় বন্যার ঝুঁকি বাড়ায়।",
      tags=["ielts", "reading", "theme"]),
    E("climate change", "long-term shift in weather patterns", "জলবায়ু পরিবর্তন", pos="phrase", cefr="B1", category="nature",
      example="Climate change affects farmers worldwide.", example_bn="জলবায়ু পরিবর্তন বিশ্বজুড়ে কৃষকদের প্রভাবিত করে।",
      tags=["ielts", "reading", "theme"]),
    E("public health", "health of the whole population", "জনস্বাস্থ্য", pos="phrase", cefr="B1", category="health",
      example="Vaccination protects public health.", example_bn="টিকাদান জনস্বাস্থ্য রক্ষা করে।",
      tags=["ielts", "reading", "theme"]),
    E("life expectancy", "average years a person is expected to live", "গড় আয়ু", pos="phrase", cefr="B2", category="health",
      example="Life expectancy has risen in many countries.", example_bn="অনেক দেশে গড় আয়ু বেড়েছে।",
      tags=["ielts", "reading", "theme"]),
    E("obesity", "the state of being very overweight", "স্থূলতা", pos="noun", cefr="B2", category="health",
      example="Obesity is linked to poor diet.", example_bn="স্থূলতা খারাপ খাদ্যাভ্যাসের সঙ্গে যুক্ত।",
      tags=["ielts", "reading", "theme"]),
    E("nutrition", "food needed for health", "পুষ্টি", pos="noun", cefr="B1", category="health",
      example="School meals improve child nutrition.", example_bn="স্কুল মিল শিশুদের পুষ্টি উন্নত করে।",
      tags=["ielts", "reading", "theme"]),
    E("migration", "movement of people to a new place", "অভিবাসন / মাইগ্রেশন", pos="noun", cefr="B1", category="travel",
      example="Migration can fill labour shortages.", example_bn="মাইগ্রেশন শ্রমিক ঘাটতি পূরণ করতে পারে।",
      tags=["ielts", "reading", "theme"]),
    E("refugee", "a person forced to leave their country", "শরণার্থী", pos="noun", cefr="B1", category="travel",
      example="Refugees need safe housing and schools.", example_bn="শরণার্থীদের নিরাপদ আবাসন ও স্কুল লাগে।",
      tags=["ielts", "reading", "theme"]),
    E("inequality", "unfair difference between groups", "অসমতা", pos="noun", cefr="B2", category="education",
      example="Education can reduce inequality.", example_bn="শিক্ষা অসমতা কমাতে পারে।",
      tags=["ielts", "reading", "theme"]),
    E("affordable housing", "homes people can pay for", "সাশ্রয়ী আবাসন", pos="phrase", cefr="B1", category="home",
      example="Cities lack affordable housing.", example_bn="শহরে সাশ্রয়ী আবাসনের অভাব।",
      tags=["ielts", "reading", "theme"]),
    E("remote work", "working from outside the office", "রিমোট ওয়ার্ক", pos="phrase", cefr="B1", category="office",
      example="Remote work changed commuting patterns.", example_bn="রিমোট ওয়ার্ক যাতায়াতের ধরন বদলেছে।",
      tags=["ielts", "reading", "theme"]),
    E("digital literacy", "ability to use digital tools well", "ডিজিটাল সাক্ষরতা", pos="phrase", cefr="B1", category="technology",
      example="Schools must teach digital literacy.", example_bn="স্কুলগুলোকে ডিজিটাল সাক্ষরতা শেখাতে হবে।",
      tags=["ielts", "reading", "theme"]),
]

LIST_SPECS = [
    ("awl-starter", "Academic Word List · Starter", "একাডেমিক ওয়ার্ড লিস্ট · স্টার্টার",
     "High-frequency AWL-style words for IELTS/TOEFL/PTE (unofficial).", "AWL-স্টাইল উচ্চ-ফ্রিকোয়েন্সি শব্দ (অনঅফিসিয়াল)।", "B1–C1", AWL),
    ("paraphrase-synonyms", "Paraphrase Synonyms", "প্যারাফ্রেজ সমার্থক শব্দ",
     "Swap common words for exam-ready synonyms (unofficial).", "সাধারণ শব্দের exam-ready সমার্থক (অনঅফিসিয়াল)।", "A2–B2", PARA),
    ("false-friends-bn", "False Friends (BN)", "ফলস ফ্রেন্ডস (বাংলা)",
     "English words Bengali learners often misread.", "বাংলা ভাষাভাষীরা যেসব শব্দ ভুল বোঝেন।", "A2–B2", FALSE),
    ("reading-theme-pack", "Reading Theme Pack", "রিডিং থিম প্যাক",
     "Climate, cities, health, migration themes (unofficial).", "জলবায়ু, নগর, স্বাস্থ্য, মাইগ্রেশন থিম (অনঅফিসিয়াল)।", "B1–C1", THEME),
]


def merge_vocab(incoming):
    bank = json.loads(VOCAB.read_text(encoding="utf-8"))
    by_id = {w["id"]: i for i, w in enumerate(bank)}
    by_word = {w["word"].lower(): i for i, w in enumerate(bank)}
    added = updated = 0
    for e in incoming:
        if not e.get("word"):
            continue
        if e["id"] in by_id:
            i = by_id[e["id"]]
            old = bank[i]
            bank[i] = {**old, **e, "tags": sorted(set((old.get("tags") or []) + (e.get("tags") or [])))}
            updated += 1
        elif e["word"].lower() in by_word:
            i = by_word[e["word"].lower()]
            old = bank[i]
            bank[i] = {**old, **{k: v for k, v in e.items() if k != "id"}, "id": old["id"],
                       "tags": sorted(set((old.get("tags") or []) + (e.get("tags") or [])))}
            updated += 1
        else:
            bank.append(e)
            by_id[e["id"]] = len(bank) - 1
            by_word[e["word"].lower()] = len(bank) - 1
            added += 1
    VOCAB.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return added, updated


def resolve_ids(entries):
    bank = json.loads(VOCAB.read_text(encoding="utf-8"))
    by_word = {w["word"].lower(): w["id"] for w in bank}
    out, seen = [], set()
    for e in entries:
        if is_beginner_cefr(e.get("cefr_level")):
            continue
        wid = by_word.get(e["word"].lower(), e["id"])
        if wid not in seen:
            seen.add(wid)
            out.append(wid)
    return out


def upsert_list(meta, list_id, title, title_bn, desc, desc_bn, cefr, word_ids):
    lists = meta.get("lists") or []
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
    obj = {"id": list_id, "title": title, "title_bn": title_bn, "description": desc,
           "description_bn": desc_bn, "cefr": list_cefr_label(cefr), "word_ids": existing}
    for i, L in enumerate(lists):
        if L.get("id") == list_id:
            lists[i] = obj
            meta["lists"] = lists
            return
    lists.append(obj)
    meta["lists"] = lists


def upsert_spelling(list_id, title, title_bn, words):
    meta = json.loads(SLISTS.read_text(encoding="utf-8"))
    lists = meta.get("lists") or []
    clean, seen = [], set()
    for w in words:
        w = w.strip()
        if not w or " " in w:
            continue
        key = w.lower()
        if key in seen:
            continue
        seen.add(key)
        clean.append(w)
    for L in lists:
        if L.get("id") == list_id:
            for w in L.get("words") or []:
                if w.lower() not in seen and " " not in w:
                    clean.append(w)
                    seen.add(w.lower())
            break
    obj = {"id": list_id, "title": title, "title_bn": title_bn,
           "description": "Academic spelling practice (unofficial).",
           "description_bn": "একাডেমিক বানান অনুশীলন (অনঅফিসিয়াল)।",
           "target_size": len(clean), "words": clean}
    for i, L in enumerate(lists):
        if L.get("id") == list_id:
            lists[i] = obj
            meta["lists"] = lists
            SLISTS.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            return
    lists.append(obj)
    meta["lists"] = lists
    SLISTS.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    all_e = AWL + PARA + FALSE + THEME
    added, updated = merge_vocab(all_e)
    vmeta = json.loads(VLISTS.read_text(encoding="utf-8"))
    for list_id, title, title_bn, desc, desc_bn, cefr, entries in LIST_SPECS:
        ids = resolve_ids(entries)
        upsert_list(vmeta, list_id, title, title_bn, desc, desc_bn, cefr, ids)
        print(list_id, len(ids))
    VLISTS.write_text(json.dumps(vmeta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    upsert_spelling("awl-starter-spellings", "AWL Starter Spellings", "AWL স্টার্টার বানান",
                    [e["word"] for e in AWL])
    bank = json.loads(VOCAB.read_text(encoding="utf-8"))
    print("added", added, "updated", updated, "bank", len(bank))


if __name__ == "__main__":
    main()
