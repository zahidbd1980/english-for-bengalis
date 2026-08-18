# -*- coding: utf-8 -*-
"""Content batch 2: Task1 expand, collocations, speaking Part1, academic verbs, listening traps."""
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


def E(
    word: str,
    meaning_en: str,
    meaning_bn: str,
    *,
    pos: str = "noun",
    cefr: str = "B1",
    category: str = "ielts",
    example: str = "",
    example_bn: str = "",
    tags: list[str] | None = None,
    synonyms: list[str] | None = None,
) -> dict:
    return {
        "id": slug_id(word),
        "word": word,
        "phonetic": "",
        "meaning_en": meaning_en,
        "meaning_bn": meaning_bn,
        "part_of_speech": pos,
        "cefr_level": cefr if cefr in CEFR else "B1",
        "category": category,
        "example": example or f"Learners should practise the word '{word}'.",
        "example_bn": example_bn or f"'{word}' শব্দটি অনুশীলন করুন।",
        "synonyms": synonyms or [],
        "antonyms": [],
        "word_family": [],
        "tags": tags or ["ielts"],
    }


TASK1 = [
    E("decline", "to become smaller or weaker", "হ্রাস / কমতি", pos="verb/noun", cefr="B1",
      example="There was a steady decline in coal use.", example_bn="কয়লা ব্যবহারে স্থির হ্রাস হয়েছিল।",
      tags=["ielts", "writing", "task1"], synonyms=["fall", "decrease"]),
    E("drop", "to fall to a lower level", "কমে যাওয়া / পতন", pos="verb/noun", cefr="A2",
      example="Prices dropped by 10% in May.", example_bn="মে মাসে দাম ১০% কমেছে।",
      tags=["ielts", "writing", "task1"]),
    E("grow", "to become larger", "বাড়া / বৃদ্ধি পাওয়া", pos="verb", cefr="A2", category="daily",
      example="The number of users grew rapidly.", example_bn="ইউজারের সংখ্যা দ্রুত বেড়েছে।",
      tags=["ielts", "writing", "task1"]),
    E("climb", "to go up (numbers/levels)", "উপরে ওঠা", pos="verb", cefr="B1",
      example="Unemployment climbed to 8%.", example_bn="বেকারত্ব ৮%-এ উঠেছে।",
      tags=["ielts", "writing", "task1"]),
    E("dip", "a small temporary fall", "সামান্য পতন", pos="verb/noun", cefr="B2",
      example="Sales dipped slightly in winter.", example_bn="শীতকালে বিক্রি সামান্য কমেছিল।",
      tags=["ielts", "writing", "task1"]),
    E("surge", "a sudden large increase", "হঠাৎ তীব্র বৃদ্ধি", pos="verb/noun", cefr="B2",
      example="There was a surge in online orders.", example_bn="অনলাইন অর্ডারে হঠাৎ তীব্র বৃদ্ধি হয়েছিল।",
      tags=["ielts", "writing", "task1"]),
    E("plummet", "to fall very quickly and far", "খাড়াভাবে পড়ে যাওয়া", pos="verb", cefr="C1",
      example="Tourist arrivals plummeted in 2020.", example_bn="২০২০-এ পর্যটক আগমন খাড়াভাবে পড়েছে।",
      tags=["ielts", "writing", "task1"]),
    E("recover", "to return to a normal level", "ঘুরে দাঁড়ানো / পুনরুদ্ধার", pos="verb", cefr="B1", category="health",
      example="Exports recovered after the crisis.", example_bn="সঙ্কটের পর রপ্তানি ঘুরে দাঁড়িয়েছে।",
      tags=["ielts", "writing", "task1"]),
    E("overtake", "to become larger than something else", "ছাড়িয়ে যাওয়া", pos="verb", cefr="B2",
      example="Renewables overtook coal in 2018.", example_bn="২০১৮-এ নবায়নযোগ্য জ্বালানি কয়লাকে ছাড়িয়ে গেছে।",
      tags=["ielts", "writing", "task1"]),
    E("constitute", "to make up / form a part", "গঠন করা / অংশ হওয়া", pos="verb", cefr="B2",
      example="Women constituted 55% of graduates.", example_bn="গ্র্যাজুয়েটদের ৫৫% ছিলেন নারী।",
      tags=["ielts", "writing", "task1"]),
    E("comprise", "to consist of", "নিয়ে গঠিত", pos="verb", cefr="B2",
      example="The chart comprises five age groups.", example_bn="চার্টটি পাঁচটি বয়সগোষ্ঠী নিয়ে গঠিত।",
      tags=["ielts", "writing", "task1"]),
    E("majority", "more than half", "সংখ্যাগরিষ্ঠ অংশ", pos="noun", cefr="B1", category="education",
      example="The majority preferred buses.", example_bn="সংখ্যাগরিষ্ঠ অংশ বাস পছন্দ করেছিল।",
      tags=["ielts", "writing", "task1"]),
    E("minority", "a smaller part of a group", "সংখ্যালঘু অংশ", pos="noun", cefr="B1", category="education",
      example="Only a minority chose taxis.", example_bn="শুধু সংখ্যালঘু অংশ ট্যাক্সি বেছে নিয়েছে।",
      tags=["ielts", "writing", "task1"]),
    E("category", "a group of things with shared features", "বিভাগ / শ্রেণি", pos="noun", cefr="B1", category="education",
      example="The largest category was students.", example_bn="সবচেয়ে বড় বিভাগ ছিল শিক্ষার্থী।",
      tags=["ielts", "writing", "task1"]),
    E("trend", "a general direction of change", "ধারা / প্রবণতা", pos="noun", cefr="B1",
      example="The overall trend is upward.", example_bn="সামগ্রিক ধারা ঊর্ধ্বমুখী।",
      tags=["ielts", "writing", "task1"]),
    E("figure", "a number in a chart or table", "সংখ্যা / ফিগার", pos="noun", cefr="B1", category="education",
      example="The figure for 2016 was higher.", example_bn="২০১৬-এর ফিগার বেশি ছিল।",
      tags=["ielts", "writing", "task1"]),
    E("period", "a length of time", "সময়কাল", pos="noun", cefr="A2", category="daily",
      example="During this period, sales doubled.", example_bn="এই সময়কালে বিক্রি দ্বিগুণ হয়েছে।",
      tags=["ielts", "writing", "task1"]),
    E("roughly", "approximately", "প্রায় / মোটামুটি", pos="adverb", cefr="B1",
      example="Roughly one third used bicycles.", example_bn="মোটামুটি এক-তৃতীয়াংশ সাইকেল ব্যবহার করেছিল।",
      tags=["ielts", "writing", "task1"]),
    E("slightly", "a little", "সামান্য", pos="adverb", cefr="A2", category="daily",
      example="Numbers rose slightly in July.", example_bn="জুলাইয়ে সংখ্যা সামান্য বেড়েছে।",
      tags=["ielts", "writing", "task1"]),
    E("dramatically", "very suddenly and strongly", "নাটকীয়ভাবে / তীব্রভাবে", pos="adverb", cefr="B2",
      example="Demand fell dramatically after 2019.", example_bn="২০১৯-এর পর চাহিদা তীব্রভাবে কমেছে।",
      tags=["ielts", "writing", "task1"]),
    E("considerably", "by a large amount", "উল্লেখযোগ্য পরিমাণে", pos="adverb", cefr="B2",
      example="Costs rose considerably.", example_bn="খরচ উল্লেখযোগ্য পরিমাণে বেড়েছে।",
      tags=["ielts", "writing", "task1"]),
    E("moderate", "average in amount; not extreme", "মাঝারি / পরিমিত", pos="adjective", cefr="B1",
      example="There was a moderate increase.", example_bn="মাঝারি বৃদ্ধি হয়েছিল।",
      tags=["ielts", "writing", "task1"]),
    E("noticeable", "easy to see or notice", "লক্ষণীয়", pos="adjective", cefr="B1",
      example="A noticeable gap appeared after 2010.", example_bn="২০১০-এর পর লক্ষণীয় ফারাক দেখা যায়।",
      tags=["ielts", "writing", "task1"]),
    E("compared with", "used when showing difference", "তুলনায়", pos="phrase", cefr="B1",
      example="Compared with 2000, usage is higher.", example_bn="২০০০-এর তুলনায় ব্যবহার বেশি।",
      tags=["ielts", "writing", "task1"]),
    E("in comparison", "when comparing two things", "তুলনা করলে", pos="phrase", cefr="B1",
      example="In comparison, rural figures were lower.", example_bn="তুলনা করলে গ্রামীণ সংখ্যা কম ছিল।",
      tags=["ielts", "writing", "task1"]),
    E("the same as", "equal to", "একই / সমান", pos="phrase", cefr="A2", category="daily",
      example="The 2012 figure was the same as 2011.", example_bn="২০১২-এর সংখ্যা ২০১১-এর সমান ছিল।",
      tags=["ielts", "writing", "task1"]),
    E("twice as high", "two times larger", "দ্বিগুণ উঁচু/বেশি", pos="phrase", cefr="B1",
      example="Male wages were twice as high.", example_bn="পুরুষদের মজুরি দ্বিগুণ বেশি ছিল।",
      tags=["ielts", "writing", "task1"]),
    E("a threefold increase", "becoming three times larger", "তিন গুণ বৃদ্ধি", pos="phrase", cefr="B2",
      example="There was a threefold increase in users.", example_bn="ইউজারে তিন গুণ বৃদ্ধি হয়েছিল।",
      tags=["ielts", "writing", "task1"]),
]

COLLOC = [
    E("do homework", "to complete school tasks at home", "বাড়ির কাজ করা", pos="phrase", cefr="A1", category="education",
      example="Children should do homework every day.", example_bn="বাচ্চাদের প্রতিদিন বাড়ির কাজ করা উচিত।",
      tags=["ielts", "collocation"]),
    E("do business", "to buy/sell or trade", "ব্যবসা করা", pos="phrase", cefr="B1", category="office",
      example="Many firms do business online.", example_bn="অনেক প্রতিষ্ঠান অনলাইনে ব্যবসা করে।",
      tags=["ielts", "collocation"]),
    E("make a mistake", "to do something wrong", "ভুল করা", pos="phrase", cefr="A2", category="daily",
      example="It is normal to make a mistake while learning.", example_bn="শেখার সময় ভুল করা স্বাভাবিক।",
      tags=["ielts", "collocation"]),
    E("make sense", "to be logical or understandable", "যুক্তিসংগত হওয়া / বোঝা যায়", pos="phrase", cefr="B1", category="daily",
      example="Your argument makes sense.", example_bn="তোমার যুক্তি বোঝা যায়।",
      tags=["ielts", "collocation", "writing"]),
    E("take responsibility", "to accept duty for something", "দায়িত্ব নেওয়া", pos="phrase", cefr="B1", category="office",
      example="Leaders must take responsibility for results.", example_bn="ফলাফলের জন্য নেতাদের দায়িত্ব নিতে হবে।",
      tags=["ielts", "collocation", "writing"]),
    E("take advantage of", "to use an opportunity", "সুযোগ কাজে লাগানো", pos="phrase", cefr="B1", category="daily",
      example="Students should take advantage of free libraries.", example_bn="শিক্ষার্থীদের ফ্রি লাইব্রেরির সুযোগ কাজে লাগানো উচিত।",
      tags=["ielts", "collocation"]),
    E("have difficulty", "to find something hard", "অসুবিধা হওয়া", pos="phrase", cefr="B1", category="education",
      example="Many learners have difficulty with articles.", example_bn="অনেক শিক্ষার্থীর article-এ অসুবিধা হয়।",
      tags=["ielts", "collocation"]),
    E("have access to", "to be able to use something", "ব্যবহারের সুযোগ থাকা", pos="phrase", cefr="B1", category="education",
      example="Not all villages have access to broadband.", example_bn="সব গ্রামে ব্রডব্যান্ড ব্যবহারের সুযোগ নেই।",
      tags=["ielts", "collocation", "writing"]),
    E("give priority to", "to treat as more important", "অগ্রাধিকার দেওয়া", pos="phrase", cefr="B2", category="office",
      example="Governments should give priority to health.", example_bn="সরকারের স্বাস্থ্যকে অগ্রাধিকার দেওয়া উচিত।",
      tags=["ielts", "collocation", "writing"]),
    E("put pressure on", "to try to force someone to act", "চাপ দেওয়া", pos="phrase", cefr="B2", category="ielts",
      example="Parents may put pressure on children to score high.", example_bn="উচ্চ স্কোরের জন্য অভিভাবকরা চাপ দিতে পারেন।",
      tags=["ielts", "collocation", "writing"]),
    E("come to an agreement", "to agree after discussion", "একমত হওয়া", pos="phrase", cefr="B2", category="office",
      example="The two sides came to an agreement.", example_bn="দুই পক্ষ একমত হয়েছে।",
      tags=["ielts", "collocation"]),
    E("keep in mind", "to remember while deciding", "মনে রাখা", pos="phrase", cefr="B1", category="daily",
      example="Keep in mind the word limit.", example_bn="শব্দসীমা মনে রাখুন।",
      tags=["ielts", "collocation"]),
    E("lead to", "to cause a result", "ফলাফল হিসেবে ঘটানো", pos="phrase", cefr="B1", category="ielts",
      example="Poor diet can lead to health problems.", example_bn="খারাপ খাবার স্বাস্থ্যসমস্যা ঘটাতে পারে।",
      tags=["ielts", "collocation", "writing"]),
    E("result in", "to cause something to happen", "পরিণতিতে ঘটা", pos="phrase", cefr="B2", category="ielts",
      example="Heavy rain resulted in floods.", example_bn="ভারী বৃষ্টির পরিণতিতে বন্যা হয়েছে।",
      tags=["ielts", "collocation", "writing"]),
    E("depend on", "to be affected by", "নির্ভর করা", pos="phrase", cefr="A2", category="daily",
      example="Success depends on consistent practice.", example_bn="সাফল্য নিয়মিত অনুশীলনের ওপর নির্ভর করে।",
      tags=["ielts", "collocation"]),
    E("focus on", "to give attention to", "মনোযোগ দেওয়া", pos="phrase", cefr="A2", category="education",
      example="Focus on Task 2 first.", example_bn="আগে Task 2-এ মনোযোগ দিন।",
      tags=["ielts", "collocation"]),
    E("based on", "using something as the foundation", "ভিত্তি করে", pos="phrase", cefr="B1", category="education",
      example="The essay is based on recent research.", example_bn="রচনাটি সাম্প্রতিক গবেষণার ভিত্তিতে।",
      tags=["ielts", "collocation", "writing"]),
    E("in favour of", "supporting something (UK)", "পক্ষে", pos="phrase", cefr="B1", category="ielts",
      example="Many voters are in favour of reform.", example_bn="অনেক ভোটার সংস্কারের পক্ষে।",
      tags=["ielts", "collocation", "writing"]),
    E("in favor of", "supporting something (US)", "পক্ষে", pos="phrase", cefr="B1", category="ielts",
      example="The committee voted in favor of the plan.", example_bn="কমিটি পরিকল্পনার পক্ষে ভোট দিয়েছে।",
      tags=["toefl", "collocation"]),
    E("on average", "as a typical amount", "গড়ে", pos="phrase", cefr="B1", category="ielts",
      example="On average, students study two hours a day.", example_bn="গড়ে শিক্ষার্থীরা দিনে দুই ঘণ্টা পড়ে।",
      tags=["ielts", "collocation", "task1"]),
]

SPEAKING = [
    E("hometown", "the town where you grew up", "নিজ শহর / জন্মস্থান", pos="noun", cefr="A2", category="daily",
      example="My hometown is quiet but friendly.", example_bn="আমার নিজ শহর শান্ত কিন্তু বন্ধুসুলভ।",
      tags=["ielts", "speaking"]),
    E("neighbourhood", "the area around your home (UK)", "পাড়া / এলাকা", pos="noun", cefr="B1", category="home",
      example="My neighbourhood has many parks.", example_bn="আমার পাড়ায় অনেক পার্ক আছে।",
      tags=["ielts", "speaking"]),
    E("neighborhood", "the area around your home (US)", "পাড়া / এলাকা", pos="noun", cefr="B1", category="home",
      example="This neighborhood is safe at night.", example_bn="এই পাড়া রাতে নিরাপদ।",
      tags=["toefl", "speaking"]),
    E("commute", "regular travel to work or study", "নিয়মিত যাতায়াত", pos="verb/noun", cefr="B1", category="travel",
      example="I commute by bus every morning.", example_bn="আমি প্রতি সকালে বাসে যাতায়াত করি।",
      tags=["ielts", "speaking", "toefl"]),
    E("hobby", "an activity done for pleasure", "শখ", pos="noun", cefr="A1", category="daily",
      example="My hobby is reading short stories.", example_bn="আমার শখ ছোটগল্প পড়া।",
      tags=["ielts", "speaking"]),
    E("pastime", "something you do for enjoyment", "অবসরের কাজ", pos="noun", cefr="B1", category="daily",
      example="Gardening is a popular pastime.", example_bn="বাগান করা জনপ্রিয় অবসরের কাজ।",
      tags=["ielts", "speaking"]),
    E("leisure", "free time", "অবসর সময়", pos="noun", cefr="B1", category="daily",
      example="I spend my leisure time with family.", example_bn="অবসর সময় পরিবারের সঙ্গে কাটাই।",
      tags=["ielts", "speaking"]),
    E("outdoors", "outside in the open air", "বাইরে খোলা জায়গায়", pos="adverb", cefr="A2", category="outdoor",
      example="I prefer spending weekends outdoors.", example_bn="উইকএন্ড বাইরে কাটাতে পছন্দ করি।",
      tags=["ielts", "speaking"]),
    E("cuisine", "a style of cooking", "রান্নার ধরন / খাবারের সংস্কৃতি", pos="noun", cefr="B1", category="food",
      example="Bengali cuisine uses lots of fish.", example_bn="বাঙালি খাবারে মাছ বেশি ব্যবহৃত হয়।",
      tags=["ielts", "speaking"]),
    E("spicy", "having a strong hot flavour", "ঝাল / মশলাদার", pos="adjective", cefr="A2", category="food",
      example="I like spicy food, but not every day.", example_bn="ঝাল খাবার পছন্দ করি, কিন্তু প্রতিদিন নয়।",
      tags=["ielts", "speaking"]),
    E("colleague", "a person you work with", "সহকর্মী", pos="noun", cefr="A2", category="office",
      example="I often have lunch with my colleagues.", example_bn="প্রায়ই সহকর্মীদের সঙ্গে লাঞ্চ করি।",
      tags=["ielts", "speaking", "toefl"]),
    E("shift", "a period of work time", "শিফট / কাজের পালা", pos="noun", cefr="B1", category="office",
      example="She works the night shift at the hospital.", example_bn="সে হাসপাতালে নাইট শিফটে কাজ করে।",
      tags=["ielts", "speaking"]),
    E("deadline", "the time by which work must finish", "শেষ সময়সীমা", pos="noun", cefr="B1", category="office",
      example="Meeting deadlines is stressful.", example_bn="ডেডলাইন মানা চাপের।",
      tags=["ielts", "speaking", "toefl"]),
    E("major", "main subject at university (US)", "মেজর / মূল বিষয়", pos="noun", cefr="B1", category="education",
      example="My major is computer science.", example_bn="আমার মেজর কম্পিউটার সায়েন্স।",
      tags=["toefl", "speaking"]),
    E("campus", "university grounds and buildings", "ক্যাম্পাস", pos="noun", cefr="A2", category="education",
      example="The campus has a large library.", example_bn="ক্যাম্পাসে বড় লাইব্রেরি আছে।",
      tags=["toefl", "speaking", "ielts"]),
    E("assignment", "a piece of academic work", "অ্যাসাইনমেন্ট / নির্ধারিত কাজ", pos="noun", cefr="B1", category="education",
      example="I have two assignments this week.", example_bn="এই সপ্তাহে দুইটি অ্যাসাইনমেন্ট আছে।",
      tags=["ielts", "speaking", "toefl"]),
    E("semester", "half of an academic year", "সেমিস্টার", pos="noun", cefr="B1", category="education",
      example="Exams are at the end of the semester.", example_bn="সেমিস্টার শেষে পরীক্ষা হয়।",
      tags=["toefl", "speaking"]),
    E("routine", "a regular way of doing things", "রুটিন / নিয়মিত অভ্যাস", pos="noun", cefr="A2", category="daily",
      example="My morning routine starts at 6 a.m.", example_bn="আমার সকালের রুটিন সকাল ৬টায় শুরু।",
      tags=["ielts", "speaking"]),
    E("prefer", "to like one thing more than another", "বেশি পছন্দ করা", pos="verb", cefr="A1", category="daily",
      example="I prefer tea to coffee.", example_bn="কফির চেয়ে চা বেশি পছন্দ করি।",
      tags=["ielts", "speaking"]),
    E("rarely", "not often", "কদাচিৎ", pos="adverb", cefr="B1", category="daily",
      example="I rarely watch TV on weekdays.", example_bn="কর্মদিবসে কদাচিৎ টিভি দেখি।",
      tags=["ielts", "speaking"]),
    E("occasionally", "sometimes but not often", "মাঝে মাঝে", pos="adverb", cefr="B1", category="daily",
      example="I occasionally cook for friends.", example_bn="মাঝে মাঝে বন্ধুদের জন্য রান্না করি।",
      tags=["ielts", "speaking"]),
    E("memorable", "worth remembering", "স্মরণীয়", pos="adjective", cefr="B1", category="daily",
      example="My most memorable trip was to Cox's Bazar.", example_bn="সবচেয়ে স্মরণীয় ভ্রমণ ছিল কক্সবাজারে।",
      tags=["ielts", "speaking"]),
    E("convenient", "easy and suitable", "সুবিধাজনক", pos="adjective", cefr="B1", category="daily",
      example="Online banking is convenient.", example_bn="অনলাইন ব্যাংকিং সুবিধাজনক।",
      tags=["ielts", "speaking"]),
    E("affordable", "not too expensive", "সাশ্রয়ী", pos="adjective", cefr="B1", category="shopping",
      example="Public transport should be affordable.", example_bn="গণপরিবহন সাশ্রয়ী হওয়া উচিত।",
      tags=["ielts", "speaking", "writing"]),
    E("crowded", "full of people", "ভিড়পূর্ণ", pos="adjective", cefr="A2", category="travel",
      example="The bus is crowded in the morning.", example_bn="সকালে বাস ভিড়পূর্ণ থাকে।",
      tags=["ielts", "speaking"]),
    E("polluted", "dirty because of chemicals/waste", "দূষিত", pos="adjective", cefr="B1", category="nature",
      example="Some rivers are heavily polluted.", example_bn="কিছু নদী মারাত্মকভাবে দূষিত।",
      tags=["ielts", "speaking", "writing"]),
    E("get along with", "to have a friendly relationship", "মিলমিশ থাকা", pos="phrase", cefr="B1", category="daily",
      example="I get along with my classmates.", example_bn="সহপাঠীদের সঙ্গে মিলমিশ আছে।",
      tags=["ielts", "speaking"]),
    E("look forward to", "to feel happy about a future event", "অপেক্ষায় থাকা / আগ্রহে থাকা", pos="phrase", cefr="B1", category="daily",
      example="I look forward to the weekend.", example_bn="উইকএন্ডের অপেক্ষায় থাকি।",
      tags=["ielts", "speaking"]),
    E("in my free time", "when I am not working/studying", "অবসর সময়ে", pos="phrase", cefr="A2", category="daily",
      example="In my free time I listen to podcasts.", example_bn="অবসর সময়ে পডকাস্ট শুনি।",
      tags=["ielts", "speaking"]),
    E("on a daily basis", "every day", "প্রতিদিন ভিত্তিতে", pos="phrase", cefr="B1", category="daily",
      example="I practise English on a daily basis.", example_bn="প্রতিদিন ভিত্তিতে ইংরেজি অনুশীলন করি।",
      tags=["ielts", "speaking"]),
]

ACADEMIC = [
    E("analyse", "to examine carefully (UK)", "বিশ্লেষণ করা", pos="verb", cefr="B2", category="education",
      example="Researchers analyse the survey data.", example_bn="গবেষকরা জরিপের তথ্য বিশ্লেষণ করেন।",
      tags=["ielts", "toefl", "pte", "academic"], synonyms=["examine"]),
    E("analyze", "to examine carefully (US)", "বিশ্লেষণ করা", pos="verb", cefr="B2", category="education",
      example="Students analyze the author's argument.", example_bn="শিক্ষার্থীরা লেখকের যুক্তি বিশ্লেষণ করে।",
      tags=["toefl", "academic"]),
    E("imply", "to suggest without saying directly", "ইঙ্গিত করা", pos="verb", cefr="B2", category="education",
      example="The results imply a need for reform.", example_bn="ফলাফল সংস্কারের প্রয়োজন ইঙ্গিত করে।",
      tags=["ielts", "toefl", "academic"]),
    E("infer", "to conclude from evidence", "অনুমান করে সিদ্ধান্ত নেওয়া", pos="verb", cefr="B2", category="education",
      example="Readers can infer the author's attitude.", example_bn="পাঠক লেখকের মনোভাব অনুমান করতে পারেন।",
      tags=["toefl", "ielts", "academic"]),
    E("cite", "to mention as evidence", "উদ্ধৃত করা", pos="verb", cefr="B2", category="education",
      example="Always cite reliable sources.", example_bn="সবসময় নির্ভরযোগ্য সূত্র উদ্ধৃত করুন।",
      tags=["toefl", "pte", "academic"]),
    E("refute", "to prove a statement is wrong", "খণ্ডন করা", pos="verb", cefr="C1", category="education",
      example="The study refutes the old theory.", example_bn="গবেষণাটি পুরনো তত্ত্ব খণ্ডন করে।",
      tags=["toefl", "ielts", "academic"]),
    E("assert", "to state firmly", "জোর দিয়ে বলা", pos="verb", cefr="B2", category="education",
      example="The author asserts that climate policy is urgent.", example_bn="লেখক জোর দিয়ে বলেন জলবায়ু নীতি জরুরি।",
      tags=["ielts", "toefl", "academic"]),
    E("evaluate", "to judge the value or quality", "মূল্যায়ন করা", pos="verb", cefr="B2", category="education",
      example="Teachers evaluate student essays carefully.", example_bn="শিক্ষকরা শিক্ষার্থীর রচনা সাবধানে মূল্যায়ন করেন।",
      tags=["ielts", "toefl", "pte", "academic"]),
    E("summarise", "to give the main points briefly (UK)", "সংক্ষেপ করা", pos="verb", cefr="B1", category="education",
      example="Summarise the paragraph in one sentence.", example_bn="অনুচ্ছেদটি এক বাক্যে সংক্ষেপ করুন।",
      tags=["ielts", "pte", "academic"]),
    E("summarize", "to give the main points briefly (US)", "সংক্ষেপ করা", pos="verb", cefr="B1", category="education",
      example="Summarize the lecture in your notes.", example_bn="লেকচার নোটের মধ্যে সংক্ষেপ করুন।",
      tags=["toefl", "academic"]),
    E("highlight", "to emphasise an important point", "গুরুত্ব দিয়ে তুলে ধরা", pos="verb", cefr="B1", category="education",
      example="The report highlights funding gaps.", example_bn="রিপোর্ট অর্থায়নের ঘাটতি তুলে ধরে।",
      tags=["ielts", "toefl", "academic"]),
    E("demonstrate", "to show clearly", "প্রদর্শন করা / দেখানো", pos="verb", cefr="B2", category="education",
      example="The graph demonstrates a clear rise.", example_bn="গ্রাফ স্পষ্ট বৃদ্ধি দেখায়।",
      tags=["ielts", "toefl", "pte", "academic"]),
    E("illustrate", "to explain with an example", "উদাহরণ দিয়ে বোঝানো", pos="verb", cefr="B2", category="education",
      example="This case illustrates the problem.", example_bn="এই কেস সমস্যাটি উদাহরণ দিয়ে বোঝায়।",
      tags=["ielts", "toefl", "academic"]),
    E("indicate", "to show or point to", "নির্দেশ করা / ইঙ্গিত দেওয়া", pos="verb", cefr="B1", category="education",
      example="The data indicate higher demand.", example_bn="তথ্য উচ্চ চাহিদা নির্দেশ করে।",
      tags=["ielts", "toefl", "academic"]),
    E("suggest", "to put forward an idea", "প্রস্তাব করা / ইঙ্গিত করা", pos="verb", cefr="A2", category="daily",
      example="Experts suggest limiting screen time.", example_bn="বিশেষজ্ঞরা স্ক্রিন টাইম সীমিত করার প্রস্তাব করেন।",
      tags=["ielts", "toefl", "academic"]),
    E("argue", "to give reasons for a view", "যুক্তি দেওয়া", pos="verb", cefr="B1", category="ielts",
      example="Some people argue that cities are safer.", example_bn="কেউ কেউ যুক্তি দেন যে শহর নিরাপদ।",
      tags=["ielts", "writing", "academic"]),
    E("claim", "to say something is true", "দাবি করা", pos="verb/noun", cefr="B1", category="ielts",
      example="The article claims that pollution fell.", example_bn="নিবন্ধটি দাবি করে দূষণ কমেছে।",
      tags=["ielts", "toefl", "academic"]),
    E("hypothesis", "an idea to be tested", "হাইপোথিসিস / অনুমান", pos="noun", cefr="B2", category="education",
      example="The hypothesis was later confirmed.", example_bn="হাইপোথিসিসটি পরে নিশ্চিত হয়েছিল।",
      tags=["toefl", "pte", "academic"]),
    E("methodology", "a system of methods used in study", "পদ্ধতিবিজ্ঞান / মেথডলজি", pos="noun", cefr="C1", category="education",
      example="The methodology section explains the sample.", example_bn="মেথডলজি অংশে নমুনা ব্যাখ্যা করা হয়েছে।",
      tags=["toefl", "pte", "academic"]),
    E("perspective", "a way of thinking about something", "দৃষ্টিভঙ্গি", pos="noun", cefr="B2", category="education",
      example="The passage presents a historical perspective.", example_bn="প্যাসেজটি ঐতিহাসিক দৃষ্টিভঙ্গি উপস্থাপন করে।",
      tags=["ielts", "toefl", "academic"]),
    E("assumption", "something accepted as true without proof", "অনুমান / ধরে নেওয়া বিষয়", pos="noun", cefr="B2", category="education",
      example="The argument rests on a weak assumption.", example_bn="যুক্তিটি দুর্বল অনুমানের ওপর দাঁড়িয়ে।",
      tags=["toefl", "ielts", "academic"]),
    E("valid", "logically acceptable", "যৌক্তিকভাবে গ্রহণযোগ্য", pos="adjective", cefr="B2", category="education",
      example="Is this a valid conclusion?", example_bn="এটি কি যৌক্তিক সিদ্ধান্ত?",
      tags=["toefl", "ielts", "academic"]),
    E("reliable", "able to be trusted", "নির্ভরযোগ্য", pos="adjective", cefr="B1", category="education",
      example="Use reliable academic sources.", example_bn="নির্ভরযোগ্য একাডেমিক সূত্র ব্যবহার করুন।",
      tags=["ielts", "toefl", "pte", "academic"]),
    E("relevant", "connected to the topic", "প্রাসঙ্গিক", pos="adjective", cefr="B1", category="education",
      example="Include only relevant examples.", example_bn="শুধু প্রাসঙ্গিক উদাহরণ রাখুন।",
      tags=["ielts", "toefl", "pte", "academic"]),
    E("controversial", "causing public disagreement", "বিতর্কিত", pos="adjective", cefr="B2", category="ielts",
      example="It remains a controversial issue.", example_bn="এটি এখনও বিতর্কিত বিষয়।",
      tags=["ielts", "writing", "academic"]),
]

LISTENING_TRAPS = [
    E("accommodation", "a place to live or stay", "বাসস্থান / থাকার জায়গা", pos="noun", cefr="B1", category="home",
      example="Student accommodation is near campus.", example_bn="স্টুডেন্ট অ্যাকোমোডেশন ক্যাম্পাসের কাছে।",
      tags=["ielts", "listening", "spelling"]),
    E("necessary", "needed; essential", "প্রয়োজনীয়", pos="adjective", cefr="A2", category="daily",
      example="A passport is necessary for travel.", example_bn="ভ্রমণের জন্য পাসপোর্ট প্রয়োজনীয়।",
      tags=["ielts", "listening", "spelling"]),
    E("environment", "the natural world around us", "পরিবেশ", pos="noun", cefr="B1", category="nature",
      example="Protecting the environment matters.", example_bn="পরিবেশ রক্ষা গুরুত্বপূর্ণ।",
      tags=["ielts", "listening", "spelling"]),
    E("government", "the group that runs a country", "সরকার", pos="noun", cefr="A2", category="ielts",
      example="The government announced new rules.", example_bn="সরকার নতুন নিয়ম ঘোষণা করেছে।",
      tags=["ielts", "listening", "spelling"]),
    E("forty", "the number 40", "চল্লিশ", pos="number", cefr="A1", category="daily",
      example="The meeting starts at forty minutes past nine.", example_bn="মিটিং সাড়ে নয়টায় শুরু (৯:৪০)।",
      tags=["ielts", "listening", "spelling"]),
    E("twelfth", "12th in order", "দ্বাদশ", pos="adjective", cefr="A2", category="daily",
      example="Her birthday is on the twelfth of May.", example_bn="তার জন্মদিন ১২ মে।",
      tags=["ielts", "listening", "spelling"]),
    E("eighth", "8th in order", "অষ্টম", pos="adjective", cefr="A2", category="daily",
      example="Take the eighth turning on the left.", example_bn="বাঁ দিকে অষ্টম মোড় নিন।",
      tags=["ielts", "listening", "spelling"]),
    E("questionnaire", "a set of written questions", "প্রশ্নপত্র / প্রশ্নমালা", pos="noun", cefr="B1", category="education",
      example="Please complete the questionnaire.", example_bn="প্রশ্নপত্রটি পূরণ করুন।",
      tags=["ielts", "listening", "spelling"]),
    E("temperature", "how hot or cold something is", "তাপমাত্রা", pos="noun", cefr="A2", category="health",
      example="Check the temperature twice a day.", example_bn="দিনে দুবার তাপমাত্রা চেক করুন।",
      tags=["ielts", "listening", "spelling"]),
    E("pharmacy", "a shop that sells medicines", "ফার্মেসি / ওষুধের দোকান", pos="noun", cefr="A2", category="health",
      example="There is a pharmacy opposite the station.", example_bn="স্টেশনের উল্টোদিকে একটি ফার্মেসি আছে।",
      tags=["ielts", "listening", "spelling"]),
    E("appointment", "a planned meeting", "অ্যাপয়েন্টমেন্ট / নির্ধারিত সাক্ষাৎ", pos="noun", cefr="A2", category="health",
      example="I have a dentist appointment at 3 p.m.", example_bn="বিকেল ৩টায় ডেন্টিস্ট অ্যাপয়েন্টমেন্ট আছে।",
      tags=["ielts", "listening", "spelling"]),
    E("available", "able to be used or obtained", "পাওয়া যায় / খালি আছে", pos="adjective", cefr="A2", category="daily",
      example="Rooms are available from Monday.", example_bn="সোমবার থেকে রুম পাওয়া যাবে।",
      tags=["ielts", "listening", "spelling"]),
    E("immediately", "at once; without delay", "অবিলম্বে", pos="adverb", cefr="B1", category="daily",
      example="Please call immediately if you are late.", example_bn="দেরি হলে অবিলম্বে ফোন করুন।",
      tags=["ielts", "listening", "spelling"]),
    E("restaurant", "a place that serves meals", "রেস্তোরাঁ", pos="noun", cefr="A1", category="food",
      example="The restaurant opens at noon.", example_bn="রেস্তোরাঁ দুপুরে খোলে।",
      tags=["ielts", "listening", "spelling"]),
    E("Wednesday", "the day after Tuesday", "বুধবার", pos="noun", cefr="A1", category="daily",
      example="Classes start on Wednesday.", example_bn="ক্লাস বুধবার শুরু।",
      tags=["ielts", "listening", "spelling"]),
    E("February", "the second month of the year", "ফেব্রুয়ারি", pos="noun", cefr="A1", category="daily",
      example="The course begins in February.", example_bn="কোর্স ফেব্রুয়ারিতে শুরু।",
      tags=["ielts", "listening", "spelling"]),
    E("library", "a place with books to borrow", "লাইব্রেরি", pos="noun", cefr="A1", category="education",
      example="Return books to the library desk.", example_bn="বই লাইব্রেরি ডেস্কে জমা দিন।",
      tags=["ielts", "listening", "spelling"]),
    E("address", "details of where someone lives", "ঠিকানা", pos="noun", cefr="A1", category="daily",
      example="Write your full address clearly.", example_bn="সম্পূর্ণ ঠিকানা স্পষ্ট করে লিখুন।",
      tags=["ielts", "listening", "spelling"]),
    E("postcode", "letters/numbers for a postal area (UK)", "পোস্টকোড", pos="noun", cefr="A2", category="travel",
      example="What is your postcode?", example_bn="আপনার পোস্টকোড কী?",
      tags=["ielts", "listening", "spelling"]),
    E("receipt", "a written proof of payment", "রসিদ", pos="noun", cefr="A2", category="shopping",
      example="Keep the receipt for refunds.", example_bn="রিফান্ডের জন্য রসিদ রাখুন।",
      tags=["ielts", "listening", "spelling"]),
    E("luggage", "bags you take when travelling", "লাগেজ / মালপত্র", pos="noun", cefr="A2", category="travel",
      example="Heavy luggage must be checked in.", example_bn="ভারী লাগেজ চেক-ইন করতে হবে।",
      tags=["ielts", "listening", "spelling"]),
    E("queue", "a line of people waiting (UK)", "লাইন / কিউ", pos="noun", cefr="A2", category="daily",
      example="Please join the queue at desk B.", example_bn="B ডেস্কে লাইনে দাঁড়ান।",
      tags=["ielts", "listening", "spelling"]),
    E("schedule", "a plan of times for events", "সময়সূচি", pos="noun", cefr="A2", category="travel",
      example="Check the train schedule online.", example_bn="অনলাইনে ট্রেনের সময়সূচি দেখুন।",
      tags=["ielts", "listening", "spelling"]),
    E("cancellation", "the act of stopping a planned event", "বাতিলকরণ", pos="noun", cefr="B1", category="travel",
      example="There was a flight cancellation.", example_bn="ফ্লাইট বাতিল হয়েছিল।",
      tags=["ielts", "listening", "spelling"]),
    E("registration", "the act of recording details officially", "নিবন্ধন", pos="noun", cefr="B1", category="education",
      example="Registration opens at 9 a.m.", example_bn="নিবন্ধন সকাল ৯টায় খোলে।",
      tags=["ielts", "listening", "spelling", "toefl"]),
]

PHRASALS = [
    E("bring about", "to cause something to happen", "ঘটানো / সৃষ্টি করা", pos="phrasal verb", cefr="B2", category="ielts",
      example="The reform brought about major changes.", example_bn="সংস্কার বড় পরিবর্তন এনেছে।",
      tags=["ielts", "phrasal", "writing"]),
    E("carry out", "to do or complete a task", "সম্পাদন করা", pos="phrasal verb", cefr="B1", category="office",
      example="Scientists carried out an experiment.", example_bn="বিজ্ঞানীরা একটি পরীক্ষা সম্পাদন করেছেন।",
      tags=["ielts", "phrasal", "toefl"]),
    E("look into", "to investigate", "তদন্ত করা / খতিয়ে দেখা", pos="phrasal verb", cefr="B1", category="office",
      example="The team will look into the complaint.", example_bn="টিম অভিযোগ খতিয়ে দেখবে।",
      tags=["ielts", "phrasal"]),
    E("point out", "to draw attention to", "ইঙ্গিত করে বলা", pos="phrasal verb", cefr="B1", category="education",
      example="The tutor pointed out three errors.", example_bn="টিউটর তিনটি ভুল দেখিয়ে দিয়েছেন।",
      tags=["ielts", "phrasal", "toefl"]),
    E("set up", "to establish or arrange", "প্রতিষ্ঠা / সাজানো", pos="phrasal verb", cefr="B1", category="office",
      example="They set up a community clinic.", example_bn="তারা একটি কমিউনিটি ক্লিনিক প্রতিষ্ঠা করেছে।",
      tags=["ielts", "phrasal"]),
    E("cut down on", "to reduce", "কমিয়ে আনা", pos="phrasal verb", cefr="B1", category="health",
      example="Cut down on sugar for better health.", example_bn="স্বাস্থ্যের জন্য চিনি কমিয়ে আনুন।",
      tags=["ielts", "phrasal", "speaking"]),
    E("work out", "to find a solution; to exercise", "সমাধান বের করা / ব্যায়াম করা", pos="phrasal verb", cefr="B1", category="daily",
      example="We need to work out a timetable.", example_bn="আমাদের একটি সময়সূচি বের করতে হবে।",
      tags=["ielts", "phrasal", "speaking"]),
    E("run out of", "to have no more of something", "ফুরিয়ে যাওয়া", pos="phrasal verb", cefr="A2", category="daily",
      example="The printer ran out of ink.", example_bn="প্রিন্টারের কালি ফুরিয়ে গেছে।",
      tags=["ielts", "phrasal", "speaking"]),
    E("put off", "to delay", "পিছিয়ে দেওয়া", pos="phrasal verb", cefr="B1", category="daily",
      example="Don't put off studying until midnight.", example_bn="পড়াশোনা মধ্যরাত পর্যন্ত পিছিয়ে দেবেন না।",
      tags=["ielts", "phrasal", "speaking"]),
    E("figure out", "to understand after thinking", "বুঝে ওঠা", pos="phrasal verb", cefr="B1", category="daily",
      example="I finally figured out the question type.", example_bn="অবশেষে প্রশ্নের ধরন বুঝে উঠেছি।",
      tags=["toefl", "phrasal", "speaking"]),
    E("come up with", "to think of an idea", "আইডিয়া বের করা", pos="phrasal verb", cefr="B1", category="education",
      example="Students came up with creative solutions.", example_bn="শিক্ষার্থীরা সৃজনশীল সমাধান বের করেছে।",
      tags=["ielts", "phrasal", "toefl"]),
    E("end up", "to finally be in a situation", "শেষ পর্যন্ত হয়ে যাওয়া", pos="phrasal verb", cefr="B1", category="daily",
      example="Without a plan, you may end up wasting time.", example_bn="পরিকল্পনা ছাড়া শেষ পর্যন্ত সময় নষ্ট হতে পারে।",
      tags=["ielts", "phrasal", "speaking"]),
]


LIST_SPECS = [
    ("ielts-task1-graphs", "IELTS Writing Task 1 · Graphs", "IELTS রাইটিং টাস্ক ১ · গ্রাফ",
     "Trend and comparison language for charts (unofficial).", "চার্টের ট্রেন্ড ও তুলনার ভাষা (অনঅফিসিয়াল)।", "A2–B2", TASK1),
    ("exam-collocations-core", "Exam Collocations Core", "এক্সাম কলোকেশন কোর",
     "High-frequency collocations for IELTS/TOEFL/PTE (unofficial).", "IELTS/TOEFL/PTE কলোকেশন (অনঅফিসিয়াল)।", "B1–C1", COLLOC),
    ("ielts-speaking-part1", "IELTS Speaking Part 1", "IELTS স্পিকিং পার্ট ১",
     "Hometown, hobbies, work/study micro-vocab (unofficial).", "হোমটাউন, শখ, পড়া/কাজের মাইক্রো-ভোকাব (অনঅফিসিয়াল)।", "A2–B1", SPEAKING),
    ("academic-reading-verbs", "Academic Reading Verbs", "একাডেমিক রিডিং ভার্ব",
     "Analyse/infer/cite-style verbs for IELTS/TOEFL/PTE (unofficial).", "IELTS/TOEFL/PTE রিডিং ভার্ব (অনঅফিসিয়াল)।", "B2–C1", ACADEMIC),
    ("ielts-listening-spelling-traps", "IELTS Listening Spelling Traps", "IELTS লিসেনিং বানান ফাঁদ",
     "Form-filling words that cost marks if misspelled (unofficial).", "ফর্ম-ফিলিংয়ে বানান ভুলে নম্বর কাটে (অনঅফিসিয়াল)।", "A1–B1", LISTENING_TRAPS),
    ("exam-phrasal-verbs", "Exam Phrasal Verbs", "এক্সাম ফ্রেজাল ভার্ব",
     "High-value phrasal verbs for essays and speaking (unofficial).", "Essay ও speaking-এর ফ্রেজাল ভার্ব (অনঅফিসিয়াল)।", "B1–B2", PHRASALS),
]


def merge_vocab(incoming: list[dict]) -> tuple[int, int]:
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


def resolve_ids(entries: list[dict]) -> list[str]:
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


def upsert_list(meta: dict, list_id: str, title: str, title_bn: str, desc: str, desc_bn: str, cefr: str, word_ids: list[str]) -> None:
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
    entry_obj = {
        "id": list_id,
        "title": title,
        "title_bn": title_bn,
        "description": desc,
        "description_bn": desc_bn,
        "cefr": list_cefr_label(cefr),
        "word_ids": existing,
    }
    for i, L in enumerate(lists):
        if L.get("id") == list_id:
            lists[i] = entry_obj
            meta["lists"] = lists
            return
    lists.append(entry_obj)
    meta["lists"] = lists


def upsert_spelling(list_id: str, title: str, title_bn: str, words: list[str]) -> None:
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
                key = w.lower()
                if key not in seen and " " not in w:
                    clean.append(w)
                    seen.add(key)
            break
    entry_obj = {
        "id": list_id,
        "title": title,
        "title_bn": title_bn,
        "description": "Spelling practice for exam forms (unofficial).",
        "description_bn": "এক্সাম ফর্মের বানান অনুশীলন (অনঅফিসিয়াল)।",
        "target_size": len(clean),
        "words": clean,
    }
    for i, L in enumerate(lists):
        if L.get("id") == list_id:
            lists[i] = entry_obj
            meta["lists"] = lists
            SLISTS.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            return
    lists.append(entry_obj)
    meta["lists"] = lists
    SLISTS.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    all_entries = TASK1 + COLLOC + SPEAKING + ACADEMIC + LISTENING_TRAPS + PHRASALS
    added, updated = merge_vocab(all_entries)
    vmeta = json.loads(VLISTS.read_text(encoding="utf-8"))
    for list_id, title, title_bn, desc, desc_bn, cefr, entries in LIST_SPECS:
        upsert_list(vmeta, list_id, title, title_bn, desc, desc_bn, cefr, resolve_ids(entries))
        print(list_id, len(resolve_ids(entries)))
    VLISTS.write_text(json.dumps(vmeta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    upsert_spelling(
        "ielts-listening-form-traps",
        "IELTS Listening Form Traps",
        "IELTS লিসেনিং ফর্ম ফাঁদ",
        [e["word"] for e in LISTENING_TRAPS],
    )
    upsert_spelling(
        "ielts-task1-spellings",
        "IELTS Task 1 Spellings",
        "IELTS টাস্ক ১ বানান",
        [e["word"] for e in TASK1],
    )
    bank = json.loads(VOCAB.read_text(encoding="utf-8"))
    print("added", added, "updated", updated, "bank", len(bank))


if __name__ == "__main__":
    main()
