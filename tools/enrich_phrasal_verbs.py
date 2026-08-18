# -*- coding: utf-8 -*-
"""Build B1+ phrasal-verb bank + study lists. Bank may keep A1/A2; lists do not."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from cefr_policy import keep_word, list_cefr_label  # noqa: E402

PV = ROOT / "data" / "phrasal-verbs.json"
VOCAB = ROOT / "data" / "vocabulary.json"
PLISTS = ROOT / "data" / "phrasal-lists.json"

CEFR_OK = {"A1", "A2", "B1", "B2", "C1", "C2"}
PARTICLES = {
    "up", "off", "out", "on", "in", "down", "over", "through", "after", "for",
    "into", "with", "about", "forward", "back", "away", "around", "along",
    "across", "apart", "aside", "by", "of", "to", "upon", "under", "ahead",
    "behind", "round", "together",
}
VERB_HINTS = {
    "look", "get", "give", "put", "take", "come", "go", "bring", "call", "carry",
    "set", "turn", "run", "make", "break", "hold", "keep", "cut", "fall", "work",
    "stand", "pick", "find", "fill", "hand", "drop", "wind", "live", "sort",
    "rule", "phase", "wipe", "wear", "use", "talk", "think", "catch", "account",
    "lay", "end", "figure", "point", "zero", "sum", "do", "pass", "pull", "push",
    "show", "shut", "sit", "speak", "spell", "split", "spread", "stick", "switch",
    "throw", "try", "wake", "warm", "watch", "write", "back", "blow", "build",
    "burn", "check", "clear", "close", "count", "cover", "deal", "draw", "dress",
    "eat", "face", "fit", "grow", "hang", "head", "help", "hit", "kick", "knock",
    "leave", "let", "lock", "log", "mix", "move", "opt", "pay", "plan", "play",
    "plug", "print", "read", "rely", "send", "settle", "sign", "slow", "speed",
    "start", "stay", "step", "stop", "tear", "tell", "tie", "track", "trade",
    "wait", "walk", "wash", "weigh", "win", "wish", "zoom", "add", "ask", "beat",
    "boil", "bump", "calm", "cheer", "chip", "clean", "come", "cool", "cross",
}

# Object can sit between verb and particle
SEPARABLE = {
    "bring up", "call off", "carry out", "fill in", "give up", "hand in",
    "pick up", "put off", "put on", "put out", "set up", "take off", "take on",
    "take over", "throw away", "try on", "turn down", "turn off", "turn on",
    "turn up", "work out", "write down", "figure out", "point out", "sort out",
    "make up", "hold up", "let down", "let out", "put away", "put down",
    "put forward", "take out", "take up", "tear up", "think over", "try out",
    "wake up", "warm up", "wear out", "wipe out", "cut off", "cut down",
    "blow up", "break down", "break off", "bring about", "bring forward",
    "call up", "clear up", "close down", "do up", "drop off", "fill out",
    "find out", "give away", "give back", "give out", "keep up", "lay off",
    "leave out", "look up", "make out", "pass on", "pay back", "print out",
    "put through", "send off", "shut down", "switch off", "switch on",
    "take away", "talk over", "throw out", "use up", "write off",
    "draw up", "fill in", "fill out", "jot down", "note down", "pass on",
    "phase out", "print out", "put together", "roll out", "scale back",
    "scale up", "send out", "step up", "type up", "wrap up", "write up",
    "call back", "file away", "iron out",
}

INTRANSITIVE = {
    "get up", "get by", "get ahead", "come in", "come along", "come round",
    "go on", "go out", "go ahead", "grow up", "show up", "turn up", "break down",
    "catch on", "drop out", "end up", "fall behind", "give in", "hang out",
    "pass away", "set off", "set out", "sit down", "stand up", "wake up",
    "work out", "carry on", "come over", "get on", "go back", "move on",
    "slow down", "speed up", "stay up", "take off", "turn out", "wind down",
    "clock in", "clock out", "log in", "kick off", "step down", "opt out",
}

# Used for Work & Office list even if category is daily/education
WORK_PHRASES = {
    "back up", "bring forward", "call back", "call off", "carry out",
    "catch up", "catch up on", "clock in", "clock out", "deal with",
    "draw up", "fill in", "fill out", "follow up", "get ahead", "get through",
    "go over", "go through", "hand in", "hold on", "iron out", "jot down",
    "kick off", "lay off", "log in", "log out", "look into", "look up",
    "note down", "pass on", "phase out", "print out", "put forward",
    "put off", "put through", "put together", "report back", "roll out",
    "scale back", "scale up", "send out", "set aside", "set up", "shut down",
    "sign off", "sort out", "stand in", "step down", "step in", "step up",
    "take on", "take over", "take up", "talk over", "turn down", "type up",
    "wrap up", "write up", "file away", "opt out", "bring up", "cut back on",
}


def slug_id(phrase: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", phrase.strip().lower()).strip("-")
    return f"pv:{s or 'phrase'}"


def particle_of(phrase: str) -> str:
    parts = phrase.strip().lower().split()
    if len(parts) < 2:
        return ""
    return " ".join(parts[1:])


def guess_type(phrase: str) -> str:
    p = phrase.strip().lower()
    if p in INTRANSITIVE and p not in SEPARABLE:
        return "intransitive"
    if p in SEPARABLE:
        return "separable"
    return "inseparable"


def pattern_of(phrase: str, ptype: str) -> str:
    parts = phrase.strip().split()
    verb = parts[0] if parts else phrase
    rest = " ".join(parts[1:]) if len(parts) > 1 else ""
    if ptype == "separable":
        return f"{verb} sth {rest}  /  {verb} {rest} sth"
    if ptype == "intransitive":
        return f"{verb} {rest}"
    return f"{verb} {rest} sth/sb"


def entry(
    phrase: str,
    meaning_en: str,
    meaning_bn: str,
    *,
    example: str = "",
    example_bn: str = "",
    cefr: str = "B1",
    category: str = "daily",
    ptype: str | None = None,
    extra_en: str = "",
    extra_bn: str = "",
) -> dict:
    phrase = phrase.strip()
    ptype = ptype or guess_type(phrase)
    return {
        "id": slug_id(phrase),
        "phrase": phrase,
        "meaning_en": meaning_en,
        "meaning_bn": meaning_bn,
        "example": example or f"Learners should practise '{phrase}'.",
        "example_bn": example_bn or f"'{phrase}' অনুশীলন করুন।",
        "cefr_level": cefr if cefr in CEFR_OK else "B1",
        "category": category,
        "type": ptype,
        "particle": particle_of(phrase),
        "pattern": pattern_of(phrase, ptype),
        "extra_example": extra_en,
        "extra_example_bn": extra_bn,
    }


EXTRA = [
    entry("account for", "to explain the reason for", "ব্যাখ্যা করা / কারণ দেওয়া",
          example="Tourism accounts for many local jobs.", example_bn="পর্যটন স্থানীয় অনেক চাকরির কারণ।",
          cefr="B2", category="ielts", ptype="inseparable"),
    entry("back up", "to support; to make a copy", "সমর্থন করা / ব্যাকআপ নেওয়া",
          example="Please back up your files tonight.", example_bn="আজ রাতে ফাইল ব্যাকআপ নিন।",
          cefr="B1", category="office", ptype="separable"),
    entry("break down", "to stop working; to analyse into parts", "ভেঙে পড়া / ভাগ করে বোঝা",
          example="The bus broke down on the highway.", example_bn="হাইওয়েতে বাস ভেঙে পড়েছে।",
          cefr="B1", category="daily", ptype="intransitive"),
    entry("break into", "to enter by force; to start suddenly", "জোর করে ঢোকা",
          example="Thieves broke into the office.", example_bn="চোরেরা অফিসে জোর করে ঢুকেছে।",
          cefr="B1", category="daily", ptype="inseparable"),
    entry("bring about", "to cause something to happen", "ঘটানো / সৃষ্টি করা",
          example="The reform brought about real change.", example_bn="সংস্কার সত্যিকারের পরিবর্তন এনেছে।",
          cefr="B2", category="ielts", ptype="separable"),
    entry("bring forward", "to move something to an earlier time", "এগিয়ে আনা",
          example="They brought the deadline forward.", example_bn="তারা ডেডলাইন এগিয়ে এনেছে।",
          cefr="B2", category="office", ptype="separable"),
    entry("bring up", "to mention a topic; to raise a child", "প্রসঙ্গ তোলা; সন্তান লালন-পালন",
          example="Don't bring up politics at dinner.", example_bn="ডিনারে রাজনীতির প্রসঙ্গ তুলবেন না।",
          cefr="B1", category="daily", ptype="separable"),
    entry("call off", "to cancel", "বাতিল করা",
          example="They called off the match.", example_bn="তারা ম্যাচ বাতিল করেছে।",
          cefr="B1", category="daily", ptype="separable"),
    entry("carry on", "to continue", "চালিয়ে যাওয়া",
          example="Carry on speaking until the examiner stops you.", example_bn="পরীক্ষক না থামানো পর্যন্ত কথা চালিয়ে যান।",
          cefr="B1", category="education", ptype="intransitive"),
    entry("carry out", "to do or complete a task", "সম্পাদন করা",
          example="Scientists carried out a national survey.", example_bn="বিজ্ঞানীরা জাতীয় জরিপ করেছেন।",
          cefr="B1", category="office", ptype="separable"),
    entry("catch up on", "to do something delayed", "পিছিয়ে পড়া কাজ শেষ করা",
          example="I need to catch up on emails.", example_bn="ইমেইলের কাজ শেষ করতে হবে।",
          cefr="B1", category="office", ptype="inseparable"),
    entry("catch on", "to become popular; to understand", "জনপ্রিয় হওয়া / বুঝতে পারা",
          example="The idea quickly caught on.", example_bn="আইডিয়াটা দ্রুত জনপ্রিয় হয়ে যায়।",
          cefr="B2", category="daily", ptype="intransitive"),
    entry("check in", "to register at a hotel or airport", "চেক-ইন করা",
          example="We checked in two hours before the flight.", example_bn="ফ্লাইটের দুই ঘণ্টা আগে চেক-ইন করেছি।",
          cefr="B1", category="travel", ptype="intransitive"),
    entry("check out", "to leave a hotel; to look at something", "চেক-আউট করা / দেখে নেওয়া",
          example="Check out the graph in paragraph two.", example_bn="দ্বিতীয় অনুচ্ছেদের গ্রাফ দেখে নিন।",
          cefr="B1", category="travel", ptype="separable"),
    entry("come across", "to find by chance", "হঠাৎ পেয়ে যাওয়া",
          example="I came across a useful article.", example_bn="একটি দরকারি আর্টিকেল হঠাৎ পেয়েছি।",
          cefr="B1", category="daily", ptype="inseparable"),
    entry("come down to", "to be the most important point", "মূল কথা দাঁড়ায়",
          example="The debate comes down to cost.", example_bn="বিতর্কের মূল কথা খরচ।",
          cefr="B2", category="ielts", ptype="inseparable"),
    entry("come up with", "to think of an idea", "আইডিয়া বের করা",
          example="She came up with a better title.", example_bn="সে আরও ভালো একটি শিরোনাম বের করেছে।",
          cefr="B1", category="education", ptype="inseparable"),
    entry("count on", "to rely on", "ভরসা করা",
          example="You can count on your study partner.", example_bn="স্টাডি পার্টনারের ওপর ভরসা করতে পারো।",
          cefr="B1", category="daily", ptype="inseparable"),
    entry("cut back on", "to reduce", "কমিয়ে আনা",
          example="Hospitals must cut back on waste.", example_bn="হাসপাতালকে অপচয় কমাতে হবে।",
          cefr="B1", category="health", ptype="inseparable"),
    entry("cut down on", "to reduce (especially food or smoking)", "কমিয়ে আনা",
          example="He cut down on sugar last year.", example_bn="সে গত বছর চিনি কমিয়েছে।",
          cefr="B1", category="health", ptype="inseparable"),
    entry("cut off", "to stop a supply; to isolate", "বিচ্ছিন্ন করা",
          example="The storm cut off electricity.", example_bn="ঝড়ে বিদ্যুৎ বিচ্ছিন্ন হয়ে গেল।",
          cefr="B1", category="daily", ptype="separable"),
    entry("deal with", "to handle a problem or person", "মোকাবিলা করা",
          example="Teachers deal with mixed-ability classes.", example_bn="শিক্ষকরা মিশ্র সক্ষমতার ক্লাস সামলান।",
          cefr="B1", category="office", ptype="inseparable"),
    entry("do away with", "to abolish or remove", "তুলে দেওয়া / বাতিল করা",
          example="Some cities did away with plastic bags.", example_bn="কিছু শহর প্লাস্টিক ব্যাগ তুলে দিয়েছে।",
          cefr="B2", category="ielts", ptype="inseparable"),
    entry("drop out", "to leave a course before finishing", "মাঝপথে ছেড়ে দেওয়া",
          example="High fees make students drop out.", example_bn="উচ্চ ফিতে শিক্ষার্থীরা মাঝপথে ছাড়ে।",
          cefr="B1", category="education", ptype="intransitive"),
    entry("end up", "to finally be in a situation", "শেষ পর্যন্ত হয়ে যাওয়া",
          example="We ended up taking the bus.", example_bn="শেষ পর্যন্ত আমরা বাসেই গেলাম।",
          cefr="B1", category="daily", ptype="intransitive"),
    entry("fall behind", "to fail to keep up", "পিছিয়ে পড়া",
          example="Students fall behind without practice.", example_bn="অনুশীলন ছাড়া শিক্ষার্থী পিছিয়ে পড়ে।",
          cefr="B1", category="education", ptype="intransitive"),
    entry("figure out", "to understand after thinking", "বুঝে ওঠা",
          example="I cannot figure out this graph.", example_bn="এই গ্রাফ বুঝে উঠতে পারছি না।",
          cefr="B1", category="education", ptype="separable"),
    entry("fill in", "to complete a form", "ফর্ম পূরণ করা",
          example="Fill in your passport number carefully.", example_bn="পাসপোর্ট নম্বর সাবধানে পূরণ করুন।",
          cefr="B1", category="daily", ptype="separable"),
    entry("get across", "to communicate an idea successfully", "বুঝিয়ে বলা",
          example="Use examples to get your point across.", example_bn="পয়েন্ট বোঝাতে উদাহরণ দিন।",
          cefr="B2", category="education", ptype="separable"),
    entry("get along with", "to have a friendly relationship", "মিলিয়ে চলা",
          example="She gets along with her classmates.", example_bn="সে সহপাঠীদের সঙ্গে মিলিয়ে চলে।",
          cefr="B1", category="daily", ptype="inseparable"),
    entry("get away with", "to avoid punishment", "রক্ষা পাওয়া / ধরা না পড়া",
          example="Companies should not get away with pollution.", example_bn="কোম্পানি দূষণ করে রক্ষা পাবে না।",
          cefr="B2", category="ielts", ptype="inseparable"),
    entry("get by", "to manage with difficulty", "কষ্টে চালিয়ে যাওয়া",
          example="We can get by with one laptop.", example_bn="একটা ল্যাপটপ দিয়েই চালানো যাবে।",
          cefr="B2", category="daily", ptype="intransitive"),
    entry("get over", "to recover from", "কাটিয়ে ওঠা",
          example="It took weeks to get over the flu.", example_bn="ফ্লু কাটাতে কয়েক সপ্তাহ লেগেছে।",
          cefr="B1", category="health", ptype="inseparable"),
    entry("get rid of", "to remove or throw away", "মুক্ত হওয়া / ফেলে দেওয়া",
          example="Get rid of unused apps.", example_bn="অব্যবহৃত অ্যাপ ফেলে দিন।",
          cefr="B1", category="daily", ptype="inseparable"),
    entry("give in", "to stop resisting; to submit", "হার মেনে নেওয়া / জমা দেওয়া",
          example="Don't give in to exam panic.", example_bn="পরীক্ষার আতঙ্কে হার মানবেন না।",
          cefr="B1", category="daily", ptype="intransitive"),
    entry("give rise to", "to cause", "সৃষ্টি করা",
          example="Urban growth gives rise to congestion.", example_bn="নগর বৃদ্ধি যানজট সৃষ্টি করে।",
          cefr="B2", category="ielts", ptype="inseparable"),
    entry("give up", "to stop trying; to quit a habit", "চেষ্টা ছেড়ে দেওয়া",
          example="Don't give up after one mock test.", example_bn="এক মক টেস্টের পর চেষ্টা ছাড়বেন না।",
          cefr="B1", category="daily", ptype="separable"),
    entry("go along with", "to agree with or support", "সাথে একমত হওয়া",
          example="I cannot go along with that plan.", example_bn="সেই পরিকল্পনার সাথে একমত হতে পারি না।",
          cefr="B1", category="daily", ptype="inseparable"),
    entry("go through", "to experience; to examine carefully", "অতিক্রম করা / খতিয়ে দেখা",
          example="Go through the essay before you submit.", example_bn="জমা দেওয়ার আগে রচনা খতিয়ে দেখুন।",
          cefr="B1", category="education", ptype="inseparable"),
    entry("hand in", "to submit work", "জমা দেওয়া",
          example="Hand in the assignment by Friday.", example_bn="শুক্রবারের মধ্যে অ্যাসাইনমেন্ট জমা দিন।",
          cefr="B1", category="education", ptype="separable"),
    entry("hold on to", "to keep", "ধরে রাখা",
          example="Hold on to your boarding pass.", example_bn="বোর্ডিং পাস ধরে রাখুন।",
          cefr="B1", category="travel", ptype="inseparable"),
    entry("keep up with", "to stay informed or at the same speed", "তাল মিলিয়ে চলা",
          example="It is hard to keep up with new research.", example_bn="নতুন গবেষণার তাল মিলানো কঠিন।",
          cefr="B1", category="education", ptype="inseparable"),
    entry("lay off", "to stop employing someone because there is no work", "ছাঁটাই করা",
          example="The factory laid off 200 workers.", example_bn="কারখানা ২০০ শ্রমিক ছাঁটাই করেছে।",
          cefr="B2", category="office", ptype="separable"),
    entry("leave out", "to omit", "বাদ দেওয়া",
          example="Don't leave out counter-arguments.", example_bn="কাউন্টার-আর্গুমেন্ট বাদ দেবেন না।",
          cefr="B1", category="education", ptype="separable"),
    entry("live up to", "to be as good as expected", "প্রত্যাশা পূরণ করা",
          example="The course lived up to its reviews.", example_bn="কোর্সটি রিভিউ অনুযায়ী প্রত্যাশা পূরণ করেছে।",
          cefr="B2", category="daily", ptype="inseparable"),
    entry("look after", "to take care of", "দেখাশোনা করা",
          example="Nurses look after patients overnight.", example_bn="নার্সরা রাতে রোগীদের দেখাশোনা করেন।",
          cefr="B1", category="daily", ptype="inseparable"),
    entry("look down on", "to think you are better than someone", "হেয় করা",
          example="Do not look down on vocational jobs.", example_bn="ভোকেশনাল চাকরি হেয় করবেন না।",
          cefr="B2", category="daily", ptype="inseparable"),
    entry("look forward to", "to feel pleased about a future event", "অপেক্ষায় থাকা",
          example="I look forward to the speaking test.", example_bn="স্পিকিং টেস্টের অপেক্ষায় আছি।",
          cefr="B1", category="daily", ptype="inseparable"),
    entry("look into", "to investigate", "তদন্ত করা / খতিয়ে দেখা",
          example="The council will look into the complaints.", example_bn="কাউন্সিল অভিযোগ খতিয়ে দেখবে।",
          cefr="B1", category="office", ptype="inseparable"),
    entry("look up to", "to admire someone", "আদর্শ মনে করা",
          example="Many students look up to their teachers.", example_bn="অনেক শিক্ষার্থী শিক্ষকদের আদর্শ মনে করে।",
          cefr="B1", category="daily", ptype="inseparable"),
    entry("make do with", "to manage with something that is not ideal", "যা আছে তা দিয়ে চালানো",
          example="We made do with a small kitchen.", example_bn="ছোট রান্নাঘর দিয়েই চালিয়েছি।",
          cefr="B2", category="daily", ptype="inseparable"),
    entry("make up for", "to compensate", "ক্ষতিপূরণ করা",
          example="Extra classes made up for lost time.", example_bn="বাড়তি ক্লাস হারানো সময় পুষিয়ে দিয়েছে।",
          cefr="B2", category="education", ptype="inseparable"),
    entry("make up", "to invent; to become friends again", "বানিয়ে বলা / মিটমাট করা",
          example="Don't make up evidence in essays.", example_bn="রচনায় প্রমাণ বানিয়ে লিখবেন না।",
          cefr="B1", category="education", ptype="separable"),
    entry("opt for", "to choose", "বেছে নেওয়া",
          example="Many candidates opt for Academic IELTS.", example_bn="অনেকে একাডেমিক আইইএলটিএস বেছে নেন।",
          cefr="B2", category="education", ptype="inseparable"),
    entry("pass away", "to die (polite)", "মারা যাওয়া (ভদ্র)",
          example="Her grandfather passed away last year.", example_bn="গত বছর তার দাদা মারা গেছেন।",
          cefr="B1", category="daily", ptype="intransitive"),
    entry("phase out", "to stop using something gradually", "ধীরে ধীরে বন্ধ করা",
          example="The government will phase out coal plants.", example_bn="সরকার কয়লা প্লান্ট ধীরে ধীরে বন্ধ করবে।",
          cefr="B2", category="ielts", ptype="separable"),
    entry("point out", "to draw attention to", "ইঙ্গিত করে বলা",
          example="The tutor pointed out two grammar slips.", example_bn="টিউটর দুটি গ্রামার ভুল দেখিয়ে দিয়েছেন।",
          cefr="B1", category="education", ptype="separable"),
    entry("put down to", "to believe something is caused by", "কারণ হিসেবে ধরা",
          example="They put the delay down to weather.", example_bn="তারা দেরিকে আবহাওয়ার কারণ ধরেছে।",
          cefr="B2", category="ielts", ptype="inseparable"),
    entry("put forward", "to suggest an idea", "প্রস্তাব করা",
          example="The report puts forward three options.", example_bn="রিপোর্ট তিনটি অপশন প্রস্তাব করে।",
          cefr="B2", category="ielts", ptype="separable"),
    entry("put off", "to postpone", "পিছিয়ে দেওয়া",
          example="Don't put off revision until the night before.", example_bn="আগের রাত পর্যন্ত রিভিশন পিছাবেন না।",
          cefr="B1", category="daily", ptype="separable"),
    entry("put up with", "to tolerate", "সহ্য করা",
          example="Residents put up with noise from the road.", example_bn="বাসিন্দারা রাস্তার শব্দ সহ্য করেন।",
          cefr="B2", category="daily", ptype="inseparable"),
    entry("rely on", "to depend on", "নির্ভর করা",
          example="Do not rely on last-minute luck.", example_bn="শেষ মুহূর্তের ভাগ্যের ওপর নির্ভর করবেন না।",
          cefr="B1", category="daily", ptype="inseparable"),
    entry("rule out", "to decide that something is not possible", "বাদ দেওয়া",
          example="Doctors ruled out a heart attack.", example_bn="ডাক্তাররা হার্ট অ্যাটাক বাদ দিয়েছেন।",
          cefr="B2", category="health", ptype="separable"),
    entry("run into", "to meet by chance; to face a problem", "হঠাৎ দেখা / সমস্যায় পড়া",
          example="The project ran into funding problems.", example_bn="প্রজেক্ট অর্থায়নের সমস্যায় পড়েছে।",
          cefr="B1", category="office", ptype="inseparable"),
    entry("run out of", "to have no more of something", "ফুরিয়ে যাওয়া",
          example="We have run out of printer ink.", example_bn="প্রিন্টারের কালি ফুরিয়ে গেছে।",
          cefr="B1", category="daily", ptype="inseparable"),
    entry("set out", "to start; to explain in an organised way", "যাত্রা শুরু / সাজিয়ে বলা",
          example="The essay sets out the main arguments.", example_bn="রচনা মূল যুক্তিগুলো সাজিয়ে বলে।",
          cefr="B2", category="ielts", ptype="intransitive"),
    entry("set up", "to establish or arrange", "প্রতিষ্ঠা / সাজানো",
          example="They set up a community clinic.", example_bn="তারা একটি কমিউনিটি ক্লিনিক প্রতিষ্ঠা করেছে।",
          cefr="B1", category="office", ptype="separable"),
    entry("show up", "to arrive; to appear", "হাজির হওয়া",
          example="Half the class showed up late.", example_bn="ক্লাসের অর্ধেক দেরিতে হাজির।",
          cefr="B1", category="daily", ptype="intransitive"),
    entry("sort out", "to solve or organise", "সমাধান করা / গুছিয়ে ফেলা",
          example="We need to sort out the timetable.", example_bn="সময়সূচি গুছিয়ে ফেলতে হবে।",
          cefr="B1", category="office", ptype="separable"),
    entry("stand for", "to represent; to support", "প্রতিনিধিত্ব করা / সমর্থন করা",
          example="UNICEF stands for children's rights.", example_bn="ইউনিসেফ শিশু অধিকারের পক্ষে দাঁড়ায়।",
          cefr="B1", category="ielts", ptype="inseparable"),
    entry("stand up for", "to defend a person or idea", "পক্ষে দাঁড়ানো",
          example="Stand up for your classmates.", example_bn="সহপাঠীদের পক্ষে দাঁড়ান।",
          cefr="B1", category="daily", ptype="inseparable"),
    entry("sum up", "to summarise", "সংক্ষেপে বলা",
          example="The last paragraph sums up the argument.", example_bn="শেষ অনুচ্ছেদ যুক্তি সংক্ষেপে বলে।",
          cefr="B1", category="education", ptype="separable"),
    entry("take after", "to resemble a parent or relative", "চেহারায়/স্বভাবে মিলে যাওয়া",
          example="She takes after her mother.", example_bn="সে মায়ের মতো।",
          cefr="B1", category="daily", ptype="inseparable"),
    entry("take on", "to accept a responsibility or challenge", "দায়িত্ব নেওয়া",
          example="Don't take on too many courses at once.", example_bn="একসঙ্গে বেশি কোর্স নেবেন না।",
          cefr="B1", category="office", ptype="separable"),
    entry("take over", "to gain control of something", "দায়িত্ব নেওয়া",
          example="A new manager took over the team.", example_bn="নতুন ম্যানেজার দলের দায়িত্ব নিয়েছে।",
          cefr="B1", category="office", ptype="separable"),
    entry("take up", "to start a hobby or activity", "নতুন করে শুরু করা",
          example="He took up cycling last winter.", example_bn="গত শীতে সে সাইক্লিং শুরু করেছে।",
          cefr="B1", category="daily", ptype="separable"),
    entry("talk over", "to discuss thoroughly", "আলোচনা করা",
          example="Talk the essay plan over with a friend.", example_bn="বন্ধুর সঙ্গে রচনার পরিকল্পনা আলোচনা করুন।",
          cefr="B1", category="education", ptype="separable"),
    entry("think through", "to consider all the results of a plan", "ভালভাবে ভেবে দেখা",
          example="Think through the disadvantages first.", example_bn="আগে অসুবিধাগুলো ভালভাবে ভাবুন।",
          cefr="B2", category="education", ptype="separable"),
    entry("turn down", "to refuse an offer", "প্রত্যাখ্যান করা",
          example="She turned down the job abroad.", example_bn="সে বিদেশের চাকরি প্রত্যাখ্যান করেছে।",
          cefr="B1", category="office", ptype="separable"),
    entry("turn into", "to become", "পরিণত হওয়া",
          example="A small leak can turn into mould.", example_bn="ছোট লিক মাউল্ডে পরিণত হতে পারে।",
          cefr="B1", category="daily", ptype="inseparable"),
    entry("turn out", "to happen in a particular way; to attend", "পরিণত হওয়া / হাজির হওয়া",
          example="The experiment turned out well.", example_bn="পরীক্ষাটি ভালো পরিণত হয়েছে।",
          cefr="B1", category="daily", ptype="intransitive"),
    entry("use up", "to finish a supply", "শেষ করে ফেলা",
          example="Do not use up all the printer ink.", example_bn="প্রিন্টারের কালি শেষ করে ফেলবেন না।",
          cefr="B1", category="daily", ptype="separable"),
    entry("wear off", "to gradually disappear", "ধীরে ধীরে কমে যাওয়া",
          example="The painkiller wore off after two hours.", example_bn="দুই ঘণ্টা পর ব্যথানাশক কমে গেল।",
          cefr="B2", category="health", ptype="intransitive"),
    entry("wind down", "to relax after work or study", "ধীরে ধীরে শান্ত হওয়া",
          example="I wind down by walking after class.", example_bn="ক্লাসের পর হেঁটে আমি শান্ত হই।",
          cefr="B1", category="daily", ptype="intransitive"),
    entry("wipe out", "to destroy completely", "নিশ্চিহ্ন করা",
          example="Floods can wipe out a harvest.", example_bn="বন্যা ফসল নিশ্চিহ্ন করতে পারে।",
          cefr="B2", category="ielts", ptype="separable"),
    entry("work on", "to spend time improving something", "কাজ চালিয়ে যাওয়া",
          example="Work on pronunciation every day.", example_bn="প্রতিদিন উচ্চারণে কাজ করুন।",
          cefr="B1", category="education", ptype="inseparable"),
    entry("work out", "to find a solution; to exercise", "সমাধান বের করা / ব্যায়াম করা",
          example="They worked out a cheaper timetable.", example_bn="তারা সস্তা একটি সময়সূচি বের করেছে।",
          cefr="B1", category="daily", ptype="separable"),
    entry("zero in on", "to focus closely on", "লক্ষ্য স্থির করা",
          example="The study zeroes in on teenage readers.", example_bn="গবেষণা কিশোর পাঠকদের ওপর লক্ষ্য রাখে।",
          cefr="B2", category="education", ptype="inseparable"),
    entry("add up", "to make sense; to total", "যুক্তিযুক্ত হওয়া / যোগ হওয়া",
          example="The figures do not add up.", example_bn="সংখ্যাগুলো মিলছে না।",
          cefr="B2", category="ielts", ptype="intransitive"),
    entry("blow over", "to pass without serious damage", "থিতিয়ে যাওয়া",
          example="The scandal will blow over.", example_bn="স্ক্যান্ডাল থিতিয়ে যাবে।",
          cefr="B2", category="daily", ptype="intransitive"),
    entry("boil down to", "to be the essential point", "মূল কথা দাঁড়ায়",
          example="The issue boils down to funding.", example_bn="সমস্যার মূল কথা অর্থায়ন।",
          cefr="B2", category="ielts", ptype="inseparable"),
    entry("build up", "to increase gradually", "ধীরে ধীরে বাড়ানো",
          example="Practice builds up confidence.", example_bn="অনুশীলন আত্মবিশ্বাস বাড়ায়।",
          cefr="B1", category="education", ptype="separable"),
    entry("call for", "to require or publicly ask for", "দাবি করা / প্রয়োজন হওয়া",
          example="The report calls for stricter rules.", example_bn="রিপোর্ট কঠোর নিয়মের দাবি করে।",
          cefr="B2", category="ielts", ptype="inseparable"),
    entry("come up", "to be mentioned; to happen", "উঠে আসা / ঘটা",
          example="This topic comes up in Part 3.", example_bn="এই টপিক পার্ট ৩-এ উঠে আসে।",
          cefr="B1", category="daily", ptype="intransitive"),
    entry("cut out", "to stop eating or doing something", "বাদ দেওয়া",
          example="He cut out junk food before the exam.", example_bn="পরীক্ষার আগে সে জাঙ্ক ফুড বাদ দিয়েছে।",
          cefr="B1", category="health", ptype="separable"),
    entry("face up to", "to accept and deal with a difficult fact", "সামনে দাঁড়ানো / মেনে নেওয়া",
          example="Face up to your weak modules.", example_bn="দুর্বল মডিউলগুলোর সামনে দাঁড়ান।",
          cefr="B2", category="education", ptype="inseparable"),
    entry("follow up", "to take further action after something", "ফলোআপ করা",
          example="Follow up the email with a call.", example_bn="ইমেইলের পর ফোন করে ফলোআপ করুন।",
          cefr="B1", category="office", ptype="separable"),
    entry("go over", "to review", "রিভিশন করা / আবার দেখা",
          example="Go over the linking words tonight.", example_bn="আজ রাতে লিংকিং ওয়ার্ড আবার দেখুন।",
          cefr="B1", category="education", ptype="inseparable"),
    entry("keep on", "to continue", "লেগে থাকা",
          example="Keep on practising even after a low score.", example_bn="কম স্কোরের পরেও অনুশীলন চালিয়ে যান।",
          cefr="B1", category="daily", ptype="intransitive"),
    entry("let down", "to disappoint", "হতাশ করা",
          example="The weak conclusion let the essay down.", example_bn="দুর্বল উপসংহার রচনাকে হতাশ করেছে।",
          cefr="B2", category="daily", ptype="separable"),
    entry("look over", "to examine quickly", "চোখ বুলিয়ে দেখা",
          example="Look over the question twice.", example_bn="প্রশ্ন দুবার চোখ বুলিয়ে দেখুন।",
          cefr="B1", category="education", ptype="separable"),
    entry("move on", "to start something new", "এগিয়ে যাওয়া",
          example="Move on to the next question if you are stuck.", example_bn="আটকে গেলে পরের প্রশ্নে যান।",
          cefr="B1", category="daily", ptype="intransitive"),
    entry("narrow down", "to reduce a list of options", "কমিয়ে নির্দিষ্ট করা",
          example="Narrow down the essay to one clear view.", example_bn="রচনাকে এক স্পষ্ট মতে নামিয়ে আনুন।",
          cefr="B2", category="education", ptype="separable"),
    entry("pay off", "to bring a good result; to finish paying a debt", "কাজ দেওয়া / শোধ করা",
          example="Daily reading pays off in IELTS Reading.", example_bn="প্রতিদিন পড়া রিডিংয়ে কাজ দেয়।",
          cefr="B1", category="education", ptype="intransitive"),
    entry("pick up", "to collect; to learn informally; to improve", "তুলে নেওয়া / অনানুষ্ঠানিকভাবে শেখা",
          example="You pick up collocations by reading.", example_bn="পড়লে কলোকেশন আপনাআপনি শেখা যায়।",
          cefr="B1", category="daily", ptype="separable"),
    entry("put across", "to communicate an idea clearly", "পরিষ্কার করে বোঝানো",
          example="Put your opinion across in the first paragraph.", example_bn="প্রথম অনুচ্ছেদে মতামত পরিষ্কার করুন।",
          cefr="B2", category="education", ptype="separable"),
    entry("set aside", "to save for a purpose; to ignore temporarily", "আলাদা করে রাখা",
          example="Set aside 20 minutes for speaking.", example_bn="স্পিকিংয়ের জন্য ২০ মিনিট আলাদা রাখুন।",
          cefr="B2", category="daily", ptype="separable"),
    entry("slow down", "to go more slowly", "ধীর করা",
          example="Slow down when you read the question.", example_bn="প্রশ্ন পড়ার সময় ধীরে যান।",
          cefr="B1", category="daily", ptype="intransitive"),
    entry("spell out", "to explain in detail", "বিস্তারিত বলা",
          example="Spell out what the graph shows.", example_bn="গ্রাফ কী দেখায় তা বিস্তারিত বলুন।",
          cefr="B2", category="ielts", ptype="separable"),
    entry("stand out", "to be clearly better or different", "আলাদাভাবে চোখে পড়া",
          example="Precise examples help your essay stand out.", example_bn="নির্দিষ্ট উদাহরণ রচনাকে আলাদা করে।",
          cefr="B2", category="education", ptype="intransitive"),
    entry("stick to", "to continue with a plan", "লেগে থাকা",
          example="Stick to your essay structure.", example_bn="রচনার স্ট্রাকচারে লেগে থাকুন।",
          cefr="B1", category="education", ptype="inseparable"),
    entry("take off", "to leave the ground; to become successful; to remove clothes", "উড্ডয়ন / সফল হওয়া / খুলে ফেলা",
          example="Her YouTube channel took off last year.", example_bn="গত বছর তার ইউটিউব চ্যানেল সফল হয়েছে।",
          cefr="B1", category="daily", ptype="intransitive"),
    entry("talk into", "to persuade someone to do something", "রাজি করানো",
          example="She talked me into joining the debate club.", example_bn="সে আমাকে বিতর্ক ক্লাবে যোগ দিতে রাজি করিয়েছে।",
          cefr="B2", category="daily", ptype="inseparable"),
    entry("turn up", "to arrive; to increase volume", "হাজির হওয়া / বাড়ানো",
          example="He turned up ten minutes early.", example_bn="সে দশ মিনিট আগে হাজির হয়েছে।",
          cefr="B1", category="daily", ptype="intransitive"),
    entry("watch out for", "to be careful about", "সাবধান থাকা",
          example="Watch out for spelling traps in Listening.", example_bn="লিসেনিংয়ের বানান ফাঁদে সাবধান।",
          cefr="B1", category="education", ptype="inseparable"),
    entry("weigh up", "to consider the good and bad points", "তুলনা করে বিচার করা",
          example="Weigh up both views before you decide.", example_bn="সিদ্ধান্তের আগে দুই মত তুলনা করুন।",
          cefr="B2", category="ielts", ptype="separable"),
    entry("clock in", "to record the time you start work", "কাজ শুরুর সময় রেকর্ড করা",
          example="Staff clock in at nine.", example_bn="স্টাফ নয়টায় ক্লক-ইন করে।",
          cefr="B1", category="office", ptype="intransitive"),
    entry("clock out", "to record the time you finish work", "কাজ শেষের সময় রেকর্ড করা",
          example="Please clock out before you leave.", example_bn="যাওয়ার আগে ক্লক-আউট করুন।",
          cefr="B1", category="office", ptype="intransitive"),
    entry("draw up", "to prepare a document or plan", "খসড়া তৈরি করা",
          example="Legal drew up a new contract.", example_bn="লিগ্যাল নতুন চুক্তির খসড়া করেছে।",
          cefr="B2", category="office", ptype="separable"),
    entry("fill in", "to complete a form; to substitute temporarily", "ফর্ম পূরণ / সাময়িক দায়িত্ব নেওয়া",
          example="Fill in the leave form today.", example_bn="আজই ছুটির ফর্ম পূরণ করুন।",
          cefr="B1", category="office", ptype="separable"),
    entry("fill out", "to complete a form", "ফর্ম পূরণ করা",
          example="Fill out the timesheet every Friday.", example_bn="প্রতি শুক্রবার টাইমশিট পূরণ করুন।",
          cefr="B1", category="office", ptype="separable"),
    entry("get ahead", "to make progress in a career", "ক্যারিয়ারে এগিয়ে যাওয়া",
          example="Clear writing helps you get ahead at work.", example_bn="পরিষ্কার লেখা কাজে এগিয়ে দেয়।",
          cefr="B2", category="office", ptype="intransitive"),
    entry("iron out", "to solve small problems in a plan", "ছোট সমস্যা মিটিয়ে নেওয়া",
          example="Let's iron out the budget issues first.", example_bn="আগে বাজেটের সমস্যা মিটিয়ে নিই।",
          cefr="B2", category="office", ptype="separable"),
    entry("jot down", "to write a short note quickly", "তাড়াতাড়ি নোট করা",
          example="Jot down the action points.", example_bn="অ্যাকশন পয়েন্টগুলো নোট করুন।",
          cefr="B1", category="office", ptype="separable"),
    entry("kick off", "to start a meeting or project", "শুরু করা",
          example="We'll kick off the meeting at ten.", example_bn="দশটায় মিটিং শুরু করব।",
          cefr="B2", category="office", ptype="intransitive"),
    entry("lay off", "to stop employing someone because work is short", "ছাঁটাই করা",
          example="The factory laid off fifty workers.", example_bn="কারখানা পঞ্চাশ জনকে ছাঁটাই করেছে।",
          cefr="B2", category="office", ptype="separable"),
    entry("log in", "to start using a computer system", "লগইন করা",
          example="Log in before you open the shared folder.", example_bn="শেয়ার্ড ফোল্ডার খোলার আগে লগইন করুন।",
          cefr="B1", category="office", ptype="intransitive"),
    entry("log out", "to end a computer session", "লগআউট করা",
          example="Log out when you leave the desk.", example_bn="ডেস্ক ছেড়ে যাওয়ার সময় লগআউট করুন।",
          cefr="B1", category="office", ptype="intransitive"),
    entry("note down", "to write something so you remember it", "লিখে রাখা",
          example="Note down the client's number.", example_bn="ক্লায়েন্টের নম্বর লিখে রাখুন।",
          cefr="B1", category="office", ptype="separable"),
    entry("opt out", "to choose not to take part", "না করার সিদ্ধান্ত নেওয়া",
          example="You can opt out of the mailing list.", example_bn="মেইলিং লিস্ট থেকে বেরিয়ে যেতে পারেন।",
          cefr="B2", category="office", ptype="intransitive"),
    entry("pass on", "to give information to someone else", "পৌঁছে দেওয়া",
          example="Please pass on the agenda.", example_bn="অ্যাজেন্ডা পৌঁছে দিন।",
          cefr="B1", category="office", ptype="separable"),
    entry("phase out", "to stop using something gradually", "ধীরে ধীরে বন্ধ করা",
          example="The office is phasing out paper forms.", example_bn="অফিস কাগজের ফর্ম ধীরে ধীরে বন্ধ করছে।",
          cefr="B2", category="office", ptype="separable"),
    entry("print out", "to print a document", "প্রিন্ট করে নেওয়া",
          example="Print out the invoice for accounts.", example_bn="অ্যাকাউন্টসের জন্য ইনভয়েস প্রিন্ট করুন।",
          cefr="B1", category="office", ptype="separable"),
    entry("put together", "to assemble or prepare", "জড়ো করা / তৈরি করা",
          example="Put together a one-page brief.", example_bn="এক পাতার ব্রিফ তৈরি করুন।",
          cefr="B1", category="office", ptype="separable"),
    entry("report back", "to return with information", "রিপোর্ট করে জানানো",
          example="Report back after the client call.", example_bn="ক্লায়েন্ট কলের পর জানিয়ে দিন।",
          cefr="B1", category="office", ptype="intransitive"),
    entry("roll out", "to introduce a product or system widely", "চালু করা / ছড়িয়ে দেওয়া",
          example="HR rolled out the new policy.", example_bn="এইচআর নতুন নীতি চালু করেছে।",
          cefr="B2", category="office", ptype="separable"),
    entry("scale up", "to increase the size of a business or project", "বড় করা",
          example="They scaled up the pilot project.", example_bn="তারা পাইলট প্রজেক্ট বড় করেছে।",
          cefr="B2", category="office", ptype="separable"),
    entry("scale back", "to reduce the size of a plan", "কমিয়ে আনা",
          example="We had to scale back hiring.", example_bn="নিয়োগ কমাতে হয়েছে।",
          cefr="B2", category="office", ptype="separable"),
    entry("send out", "to distribute to many people", "পাঠিয়ে দেওয়া",
          example="Send out the minutes by 5 p.m.", example_bn="পাঁচটার মধ্যে মিনিটস পাঠান।",
          cefr="B1", category="office", ptype="separable"),
    entry("shut down", "to close a system or business", "বন্ধ করা",
          example="Shut down the unused accounts.", example_bn="অব্যবহৃত অ্যাকাউন্টগুলো বন্ধ করুন।",
          cefr="B1", category="office", ptype="separable"),
    entry("sign off", "to give final approval; to end a message", "অনুমোদন দেওয়া / শেষ করা",
          example="The manager signed off the budget.", example_bn="ম্যানেজার বাজেট অনুমোদন দিয়েছেন।",
          cefr="B2", category="office", ptype="intransitive"),
    entry("stand in", "to replace someone temporarily", "কাউকে সাময়িকভাবে বদলি করা",
          example="Can you stand in for me at the briefing?", example_bn="ব্রিফিংয়ে কি আমার জায়গায় দাঁড়াতে পারবেন?",
          cefr="B2", category="office", ptype="intransitive"),
    entry("step down", "to leave an important job", "পদ ছাড়া",
          example="The director stepped down last month.", example_bn="গত মাসে ডিরেক্টর পদ ছেড়েছেন।",
          cefr="B2", category="office", ptype="intransitive"),
    entry("step in", "to become involved to help", "এগিয়ে এসে সাহায্য করা",
          example="HR stepped in to settle the dispute.", example_bn="বিরোধ মেটাতে এইচআর এগিয়ে এসেছে।",
          cefr="B2", category="office", ptype="intransitive"),
    entry("step up", "to increase effort or take more responsibility", "বাড়ানো / এগিয়ে আসা",
          example="We need to step up customer support.", example_bn="কাস্টমার সাপোর্ট বাড়াতে হবে।",
          cefr="B2", category="office", ptype="separable"),
    entry("take on", "to accept work or hire someone", "দায়িত্ব নেওয়া / নিয়োগ করা",
          example="The team took on two extra projects.", example_bn="টিম অতিরিক্ত দুটি প্রজেক্ট নিয়েছে।",
          cefr="B1", category="office", ptype="separable"),
    entry("talk over", "to discuss carefully", "আলোচনা করে দেখা",
          example="Let's talk over the proposal.", example_bn="প্রস্তাবটা আলোচনা করে দেখি।",
          cefr="B1", category="office", ptype="separable"),
    entry("type up", "to type a finished version of notes", "টাইপ করে তৈরি করা",
          example="Type up the interview notes.", example_bn="ইন্টারভিউ নোট টাইপ করুন।",
          cefr="B1", category="office", ptype="separable"),
    entry("wrap up", "to finish a meeting or task", "শেষ করা",
          example="We'll wrap up in five minutes.", example_bn="পাঁচ মিনিটে শেষ করব।",
          cefr="B1", category="office", ptype="separable"),
    entry("write up", "to write a full report from notes", "রিপোর্ট লিখে ফেলা",
          example="Write up the findings by Monday.", example_bn="সোমবারের মধ্যে ফাইন্ডিংস লিখে ফেলুন।",
          cefr="B1", category="office", ptype="separable"),
    entry("call back", "to return a phone call", "ফোন ফেরত দেওয়া",
          example="I'll call you back after the meeting.", example_bn="মিটিংয়ের পর ফোন করব।",
          cefr="B1", category="office", ptype="separable"),
    entry("file away", "to store documents for later", "ফাইল করে রাখা",
          example="File away the signed copies.", example_bn="স্বাক্ষরিত কপিগুলো ফাইল করে রাখুন।",
          cefr="B2", category="office", ptype="separable"),
    entry("fall behind", "to fail to keep up with work or a schedule", "পিছিয়ে পড়া",
          example="Don't fall behind on the deadline.", example_bn="ডেডলাইনে পিছিয়ে পড়বেন না।",
          cefr="B1", category="office", ptype="intransitive"),
]


def is_phrasal_vocab(w: dict) -> bool:
    pos = str(w.get("part_of_speech") or "").lower()
    tags = " ".join(w.get("tags") or []).lower()
    word = str(w.get("word") or "").strip()
    if "phrasal" in pos or "phrasal" in tags:
        return True
    parts = word.lower().split()
    if len(parts) < 2 or len(parts) > 4:
        return False
    if parts[0] not in VERB_HINTS:
        return False
    return any(p in PARTICLES for p in parts[1:])


def from_vocab(w: dict) -> dict:
    phrase = str(w.get("word") or "").strip()
    e = entry(
        phrase,
        str(w.get("meaning_en") or phrase),
        str(w.get("meaning_bn") or phrase),
        example=str(w.get("example") or ""),
        example_bn=str(w.get("example_bn") or ""),
        cefr=str(w.get("cefr_level") or w.get("cefr") or "B1"),
        category=str(w.get("category") or "daily"),
    )
    return e


def merge(bank: list, incoming: list[dict]) -> tuple[int, int]:
    by_id = {x["id"]: i for i, x in enumerate(bank)}
    by_phrase = {(x.get("phrase") or "").strip().lower(): x["id"] for x in bank}
    added = updated = 0
    for e in incoming:
        phrase = (e.get("phrase") or "").strip().lower()
        if not phrase:
            continue
        if e["id"] in by_id:
            i = by_id[e["id"]]
            cur = bank[i]
            for k, v in e.items():
                if k == "id":
                    continue
                if v not in ("", None, []):
                    cur[k] = v
            bank[i] = cur
            updated += 1
        elif phrase in by_phrase:
            i = by_id[by_phrase[phrase]]
            cur = bank[i]
            for k, v in e.items():
                if k == "id":
                    continue
                if v not in ("", None, []):
                    cur[k] = v
            bank[i] = cur
            updated += 1
        else:
            bank.append(e)
            by_id[e["id"]] = len(bank) - 1
            by_phrase[phrase] = e["id"]
            added += 1
    return added, updated


def normalize_existing(row: dict) -> dict:
    phrase = str(row.get("phrase") or "").strip()
    ptype = row.get("type") or guess_type(phrase)
    out = dict(row)
    out["id"] = out.get("id") or slug_id(phrase)
    out["cefr_level"] = str(out.get("cefr_level") or "B1")
    out["category"] = out.get("category") or "daily"
    out["type"] = ptype
    out["particle"] = out.get("particle") or particle_of(phrase)
    out["pattern"] = out.get("pattern") or pattern_of(phrase, ptype)
    out.setdefault("extra_example", "")
    out.setdefault("extra_example_bn", "")
    return out


def list_entry(lid, title, title_bn, desc, desc_bn, cefr, ids):
    return {
        "id": lid,
        "title": title,
        "title_bn": title_bn,
        "description": desc,
        "description_bn": desc_bn,
        "cefr": list_cefr_label(cefr),
        "word_ids": ids,
    }


def main() -> None:
    bank = [normalize_existing(x) for x in json.loads(PV.read_text(encoding="utf-8"))]
    vocab = json.loads(VOCAB.read_text(encoding="utf-8"))
    from_v = [from_vocab(w) for w in vocab if keep_word(w) and is_phrasal_vocab(w)]
    a1, u1 = merge(bank, from_v)
    a2, u2 = merge(bank, EXTRA)

    lookup = {x["id"]: x for x in bank}
    b1_ids = [x["id"] for x in bank if keep_word(x)]

    def pick(pred, limit=80):
        out = []
        for x in bank:
            if not keep_word(x):
                continue
            if pred(x) and x["id"] not in out:
                out.append(x["id"])
            if len(out) >= limit:
                break
        return out

    def is_work(x: dict) -> bool:
        if x.get("category") in ("office", "work"):
            return True
        return (x.get("phrase") or "").strip().lower() in WORK_PHRASES

    lists = [
        list_entry(
            "pv-daily",
            "Everyday Intermediate Phrasals",
            "দৈনন্দিন ইন্টারমিডিয়েট ফ্রেজাল",
            "B1+ phrasal verbs for real conversations.",
            "আসল কথোপকথনের B1+ ফ্রেজাল ভার্ব।",
            "B1–B2",
            pick(lambda x: x.get("category") == "daily", 80),
        ),
        list_entry(
            "pv-work",
            "Work & Office Phrasals",
            "কাজ ও অফিস ফ্রেজাল",
            "Meetings, email, hiring, deadlines.",
            "মিটিং, ইমেইল, নিয়োগ, ডেডলাইন।",
            "B1–C1",
            pick(is_work, 80),
        ),
        list_entry(
            "pv-study",
            "Study & Exam Phrasals",
            "পড়াশোনা ও এক্সাম ফ্রেজাল",
            "Revision, essays, tutorials, research.",
            "রিভিশন, রচনা, টিউটোরিয়াল, গবেষণা।",
            "B1–C1",
            pick(lambda x: x.get("category") in ("education", "ielts"), 80),
        ),
        list_entry(
            "pv-ielts-speaking",
            "IELTS Speaking Phrasals",
            "IELTS স্পিকিং ফ্রেজাল",
            "Natural phrasals for Part 1–3 (unofficial).",
            "পার্ট ১–৩-এর স্বাভাবিক ফ্রেজাল (অনঅফিসিয়াল)।",
            "B1–B2",
            pick(lambda x: x.get("category") in ("daily", "education", "travel", "health"), 80),
        ),
        list_entry(
            "pv-ielts-writing",
            "IELTS Writing Phrasals",
            "IELTS রাইটিং ফ্রেজাল",
            "Cause, change, and argument phrasals (unofficial).",
            "কারণ, পরিবর্তন ও যুক্তির ফ্রেজাল (অনঅফিসিয়াল)।",
            "B1–C1",
            pick(lambda x: x.get("category") in ("ielts", "education", "office"), 80),
        ),
        list_entry(
            "pv-separable",
            "Separable Phrasals",
            "সেপারেবল ফ্রেজাল",
            "Object can go between verb and particle: turn it off.",
            "অবজেক্ট মাঝে বসতে পারে: turn it off.",
            "B1–C1",
            pick(lambda x: x.get("type") == "separable", 80),
        ),
        list_entry(
            "pv-inseparable",
            "Inseparable Phrasals",
            "ইনসেপারেবল ফ্রেজাল",
            "Keep the particle next to the verb: look after her.",
            "পার্টিকেল ভার্বের পাশেই রাখুন: look after her.",
            "B1–C1",
            pick(lambda x: x.get("type") in ("inseparable", "intransitive"), 80),
        ),
        list_entry(
            "pv-master",
            "Phrasal Verbs Master List",
            "ফ্রেজাল ভার্ব মাস্টার লিস্ট",
            "All B1+ phrasal verbs in the bank.",
            "ব্যাংকের সব B1+ ফ্রেজাল ভার্ব।",
            "B1–C1",
            b1_ids,
        ),
    ]

    PV.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    PLISTS.write_text(json.dumps({"lists": lists}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"phrasal-verbs.json: {len(bank)} (vocab +{a1}/{u1}, extra +{a2}/{u2})")
    print(f"B1+ {len(b1_ids)}")
    for L in lists:
        print(f"  {L['id']}: {len(L['word_ids'])}")


if __name__ == "__main__":
    main()
