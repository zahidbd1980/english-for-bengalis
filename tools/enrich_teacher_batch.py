# Teacher enrichment batch — USP + volume toward §68 (12 Aug 2026)
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def save(name, obj):
    (DATA / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def merge_by_id(existing, new_items):
    seen = {x["id"] for x in existing}
    added = 0
    for it in new_items:
        if it["id"] in seen:
            continue
        existing.append(it)
        seen.add(it["id"])
        added += 1
    return added


# --- Translation Lab ---
TRANSLATION = [
    {"id": "tl:improve", "item_id": "vocab:improve", "skill": "translate", "type": "type", "question": "আমি আমার ইংরেজি উন্নত করতে চাই।", "question_bn": "ইংরেজিতে লিখুন:", "answer": "I want to improve my English.", "answers": ["I want to improve my English"], "explanation": "want to + verb", "topic": "goals"},
    {"id": "tl:learning", "item_id": "grammar:present-continuous", "skill": "translate", "type": "type", "question": "আমি ইংরেজি শিখছি।", "question_bn": "ইংরেজিতে লিখুন:", "answer": "I am learning English.", "explanation": "am + -ing", "topic": "tense"},
    {"id": "tl:agree", "item_id": "mistake:i-am-agree", "skill": "translate", "type": "type", "question": "আমি একমত।", "question_bn": "ইংরেজিতে লিখুন (I am agree নয়):", "answer": "I agree.", "explanation": "no am before agree", "topic": "mistakes"},
    {"id": "tl:give-up", "item_id": "pv:give-up", "skill": "translate", "type": "type", "question": "চেষ্টা ছেড়ে দিও না।", "question_bn": "ইংরেজিতে লিখুন:", "answer": "Don't give up.", "answers": ["Do not give up.", "Don't give up"], "explanation": "give up", "topic": "phrasal"},
    {"id": "tl:light", "item_id": "mistake:open-light", "skill": "translate", "type": "type", "question": "লাইটটা জ্বালাও।", "question_bn": "ইংরেজিতে লিখুন:", "answer": "Turn on the light.", "answers": ["Please turn on the light.", "Turn the light on.", "Please turn the light on."], "explanation": "Not open the light", "topic": "mistakes"},
    {"id": "tl:available", "item_id": "vocab:available", "skill": "translate", "type": "type", "question": "আপনি কি কাল খালি আছেন?", "question_bn": "ইংরেজিতে লিখুন:", "answer": "Are you available tomorrow?", "explanation": "available = free", "topic": "daily"},
    {"id": "tl:student", "item_id": "mistake:i-am-student", "skill": "translate", "type": "type", "question": "আমি একজন শিক্ষার্থী।", "question_bn": "ইংরেজিতে লিখুন:", "answer": "I am a student.", "explanation": "a + singular noun", "topic": "articles"},
    {"id": "tl:homework", "item_id": "mistake:make-homework", "skill": "translate", "type": "type", "question": "আমি হোমওয়ার্ক করি।", "question_bn": "ইংরেজিতে লিখুন:", "answer": "I do my homework.", "explanation": "do homework", "topic": "mistakes"},
    {"id": "tl:good-at", "item_id": "mistake:good-in-english", "skill": "translate", "type": "type", "question": "সে ইংরেজিতে ভালো।", "question_bn": "ইংরেজিতে লিখুন:", "answer": "She is good at English.", "answers": ["He is good at English.", "She is good at English"], "explanation": "good at", "topic": "prepositions"},
    {"id": "tl:interested", "item_id": "mistake:interested-on", "skill": "translate", "type": "type", "question": "আমি সঙ্গীতে আগ্রহী।", "question_bn": "ইংরেজিতে লিখুন:", "answer": "I am interested in music.", "explanation": "interested in", "topic": "prepositions"},
    {"id": "tl:depend", "item_id": "mistake:depend-of", "skill": "translate", "type": "type", "question": "এটা আবহাওয়ার উপর নির্ভর করে।", "question_bn": "ইংরেজিতে লিখুন:", "answer": "It depends on the weather.", "explanation": "depend on", "topic": "prepositions"},
    {"id": "tl:reach", "item_id": "mistake:reach-to", "skill": "translate", "type": "type", "question": "আমরা দুপুরে ঢাকা পৌঁছেছি।", "question_bn": "ইংরেজিতে লিখুন:", "answer": "We reached Dhaka at noon.", "explanation": "reach + place (no to)", "topic": "prepositions"},
    {"id": "tl:look-after", "item_id": "pv:look-after", "skill": "translate", "type": "type", "question": "সে তার ভাইয়ের দেখাশোনা করে।", "question_bn": "ইংরেজিতে লিখুন:", "answer": "She looks after her brother.", "answers": ["She looks after her little brother."], "explanation": "look after", "topic": "phrasal"},
    {"id": "tl:find-out", "item_id": "pv:find-out", "skill": "translate", "type": "type", "question": "আমাকে সময়টা জেনে নিতে হবে।", "question_bn": "ইংরেজিতে লিখুন:", "answer": "I need to find out the time.", "answers": ["I need to find out the train time."], "explanation": "find out", "topic": "phrasal"},
    {"id": "tl:get-up", "item_id": "pv:get-up", "skill": "translate", "type": "type", "question": "আমি সকাল ছয়টায় উঠি।", "question_bn": "ইংরেজিতে লিখুন:", "answer": "I get up at six.", "answers": ["I get up at 6.", "I get up at 6 every morning.", "I get up at six every morning."], "explanation": "get up", "topic": "phrasal"},
    {"id": "tl:nice-meet", "item_id": "spoken:greeting-1", "skill": "translate", "type": "type", "question": "আপনার সাথে দেখা হয়ে ভালো লাগল।", "question_bn": "ইংরেজিতে লিখুন:", "answer": "Nice to meet you.", "explanation": "greeting", "topic": "spoken"},
    {"id": "tl:how-much", "item_id": "spoken:shopping-1", "skill": "translate", "type": "type", "question": "এটার দাম কত?", "question_bn": "ইংরেজিতে লিখুন:", "answer": "How much is this?", "answers": ["Excuse me, how much is this?"], "explanation": "shopping", "topic": "spoken"},
    {"id": "tl:tell-me", "item_id": "mistake:tell-to-me", "skill": "translate", "type": "type", "question": "আমাকে সত্যটা বলুন।", "question_bn": "ইংরেজিতে লিখুন:", "answer": "Please tell me the truth.", "answers": ["Tell me the truth."], "explanation": "tell me (no to)", "topic": "mistakes"},
    {"id": "tl:discuss", "item_id": "mistake:discuss-about", "skill": "translate", "type": "type", "question": "আমরা পরিকল্পনা নিয়ে আলোচনা করেছি।", "question_bn": "ইংরেজিতে লিখুন:", "answer": "We discussed the plan.", "explanation": "discuss (no about)", "topic": "mistakes"},
    {"id": "tl:return", "item_id": "mistake:return-back", "skill": "translate", "type": "type", "question": "ফর্মটা ফেরত দিন।", "question_bn": "ইংরেজিতে লিখুন:", "answer": "Please return the form.", "explanation": "return (no back)", "topic": "mistakes"},
    {"id": "tl:for-years", "item_id": "mistake:since-for", "skill": "translate", "type": "type", "question": "আমি এখানে পাঁচ বছর ধরে থাকি।", "question_bn": "ইংরেজিতে লিখুন:", "answer": "I have lived here for five years.", "answers": ["I have lived here for 5 years."], "explanation": "for + duration", "topic": "tense"},
    {"id": "tl:prefer", "item_id": "vocab:prefer", "skill": "translate", "type": "type", "question": "কফির চেয়ে চা বেশি পছন্দ করি।", "question_bn": "ইংরেজিতে লিখুন:", "answer": "I prefer tea to coffee.", "explanation": "prefer A to B", "topic": "daily"},
    {"id": "tl:deadline", "item_id": "vocab:deadline", "skill": "translate", "type": "type", "question": "প্রজেক্টের ডেডলাইন শুক্রবার।", "question_bn": "ইংরেজিতে লিখুন:", "answer": "The project deadline is Friday.", "explanation": "deadline", "topic": "work"},
    {"id": "tl:recommend", "item_id": "vocab:recommend", "skill": "translate", "type": "type", "question": "একটি ভালো বই সুপারিশ করতে পারেন?", "question_bn": "ইংরেজিতে লিখুন:", "answer": "Can you recommend a good book?", "answers": ["Can you recommend a good book to me?"], "explanation": "recommend", "topic": "daily"},
    {"id": "tl:enter", "item_id": "mistake:enter-into", "skill": "translate", "type": "type", "question": "রুমটাতে ঢুকুন।", "question_bn": "ইংরেজিতে লিখুন:", "answer": "Please enter the room.", "answers": ["Enter the room."], "explanation": "enter + place", "topic": "prepositions"},
    {"id": "tl:belong", "item_id": "mistake:belong-to", "skill": "translate", "type": "type", "question": "এই বইটা আমার।", "question_bn": "ইংরেজিতে লিখুন:", "answer": "This book belongs to me.", "explanation": "belongs to", "topic": "mistakes"},
    {"id": "tl:one-of", "item_id": "mistake:one-of-the-student", "skill": "translate", "type": "type", "question": "সে সেরা শিক্ষার্থীদের একজন।", "question_bn": "ইংরেজিতে লিখুন:", "answer": "He is one of the best students.", "answers": ["She is one of the best students."], "explanation": "one of the + plural", "topic": "grammar"},
    {"id": "tl:said-told", "item_id": "mistake:said-me", "skill": "translate", "type": "type", "question": "সে আমাকে খবরটা বলল।", "question_bn": "ইংরেজিতে লিখুন:", "answer": "He told me the news.", "answers": ["She told me the news."], "explanation": "tell someone", "topic": "mistakes"},
    {"id": "tl:put-off", "item_id": "pv:put-off", "skill": "translate", "type": "type", "question": "আমরা মিটিং স্থগিত করেছি।", "question_bn": "ইংরেজিতে লিখুন:", "answer": "We put off the meeting.", "answers": ["We put off the meeting until Monday."], "explanation": "put off = postpone", "topic": "phrasal"},
    {"id": "tl:run-out", "item_id": "pv:run-out-of", "skill": "translate", "type": "type", "question": "আমাদের দুধ শেষ হয়ে গেছে।", "question_bn": "ইংরেজিতে লিখুন:", "answer": "We have run out of milk.", "answers": ["We've run out of milk."], "explanation": "run out of", "topic": "phrasal"},
    {"id": "tl:take-off", "item_id": "pv:take-off", "skill": "translate", "type": "type", "question": "জুতো খুলুন।", "question_bn": "ইংরেজিতে লিখুন:", "answer": "Please take off your shoes.", "answers": ["Take off your shoes."], "explanation": "take off", "topic": "phrasal"},
    {"id": "tl:look-for", "item_id": "pv:look-for", "skill": "translate", "type": "type", "question": "আমি আমার চাবি খুঁজছি।", "question_bn": "ইংরেজিতে লিখুন:", "answer": "I am looking for my keys.", "answers": ["I'm looking for my keys."], "explanation": "look for", "topic": "phrasal"},
    {"id": "tl:station", "item_id": "spoken:directions-1", "skill": "translate", "type": "type", "question": "স্টেশনে কীভাবে যাব?", "question_bn": "ইংরেজিতে লিখুন:", "answer": "How do I get to the station?", "answers": ["Excuse me, how do I get to the station?"], "explanation": "directions", "topic": "spoken"},
    {"id": "tl:call-back", "item_id": "spoken:phone-1", "skill": "translate", "type": "type", "question": "তাকে বলবেন আমাকে ফোন করতে।", "question_bn": "ইংরেজিতে লিখুন:", "answer": "Please ask him to call me back.", "explanation": "phone English", "topic": "spoken"},
    {"id": "tl:experience", "item_id": "spoken:interview-1", "skill": "translate", "type": "type", "question": "সেলসে আমার দুই বছরের অভিজ্ঞতা আছে।", "question_bn": "ইংরেজিতে লিখুন:", "answer": "I have two years of experience in sales.", "explanation": "interview", "topic": "spoken"},
    {"id": "tl:polite", "item_id": "vocab:polite", "skill": "translate", "type": "type", "question": "কাস্টমারদের সাথে ভদ্র থাকুন।", "question_bn": "ইংরেজিতে লিখুন:", "answer": "Please be polite to customers.", "explanation": "polite", "topic": "work"},
    {"id": "tl:necessary", "item_id": "vocab:necessary", "skill": "translate", "type": "type", "question": "এটা প্রয়োজনীয়।", "question_bn": "ইংরেজিতে লিখুন:", "answer": "It is necessary.", "answers": ["This is necessary.", "It's necessary."], "explanation": "necessary", "topic": "daily"},
    {"id": "tl:explain", "item_id": "vocab:explain", "skill": "translate", "type": "type", "question": "দয়া করে এটা ব্যাখ্যা করুন।", "question_bn": "ইংরেজিতে লিখুন:", "answer": "Please explain this.", "answers": ["Can you explain this, please?"], "explanation": "explain", "topic": "daily"},
    {"id": "tl:celebrate", "item_id": "vocab:celebrate", "skill": "translate", "type": "type", "question": "আমরা প্রতিবছর পহেলা বৈশাখ উদযাপন করি।", "question_bn": "ইংরেজিতে লিখুন:", "answer": "We celebrate Pohela Boishakh every year.", "explanation": "celebrate", "topic": "culture"},
    {"id": "tl:environment", "item_id": "vocab:environment", "skill": "translate", "type": "type", "question": "আমাদের পরিবেশ রক্ষা করতে হবে।", "question_bn": "ইংরেজিতে লিখুন:", "answer": "We must protect the environment.", "explanation": "environment", "topic": "ielts"},
]

save("translation-lab.json", TRANSLATION)
print("translation-lab", len(TRANSLATION))

# --- Common mistakes expansion ---
NEW_MISTAKES = [
    dict(id="mistake:listen-music", incorrect="I listen music every day.", correct="I listen to music every day.", bangla_tip="listen-এর পরে to লাগে (listen to music)।", category="prepositions", explanation="listen to + noun"),
    dict(id="mistake:marry-with", incorrect="She married with a doctor.", correct="She married a doctor.", bangla_tip="marry-এর পরে with লাগে না।", category="prepositions", explanation="marry someone (no with)"),
    dict(id="mistake:ask-to-him", incorrect="I asked to him a question.", correct="I asked him a question.", bangla_tip="ask someone — মাঝে to লাগে না।", category="grammar", explanation="ask someone something"),
    dict(id="mistake:go-to-home", incorrect="I go to home after class.", correct="I go home after class.", bangla_tip="home-এর আগে to সাধারণত লাগে না (go home)।", category="prepositions", explanation="go home / arrive home (no to)"),
    dict(id="mistake:despite-of", incorrect="Despite of the rain, we went out.", correct="Despite the rain, we went out.", bangla_tip="despite-এর পরে of লাগে না।", category="grammar", explanation="despite + noun (no of)"),
    dict(id="mistake:although-but", incorrect="Although it was late, but he came.", correct="Although it was late, he came.", bangla_tip="although ও but একসাথে ব্যবহার করবেন না।", category="grammar", explanation="Although … , … (no but)"),
    dict(id="mistake:very-much-like", incorrect="I very much like tea.", correct="I like tea very much.", bangla_tip="very much সাধারণত বাক্যের শেষে বসে।", category="word-choice", explanation="like … very much"),
    dict(id="mistake:people-is", incorrect="People is waiting outside.", correct="People are waiting outside.", bangla_tip="people = plural → are।", category="grammar", explanation="people takes plural verb"),
    dict(id="mistake:informations", incorrect="I need some informations.", correct="I need some information.", bangla_tip="information অগণনীয় — s লাগে না।", category="word-choice", explanation="information is uncountable"),
    dict(id="mistake:advices", incorrect="He gave me many advices.", correct="He gave me a lot of advice.", bangla_tip="advice অগণনীয়; এক পরামর্শ = a piece of advice।", category="word-choice", explanation="advice is uncountable"),
    dict(id="mistake:borrow-me", incorrect="Can you borrow me your pen?", correct="Can you lend me your pen?", bangla_tip="কাউকে ধার দেওয়া = lend; নিজে নেওয়া = borrow।", category="word-choice", explanation="lend to someone; borrow from someone"),
    dict(id="mistake:close-the-light", incorrect="Please close the light.", correct="Please turn off the light.", bangla_tip="লাইট বন্ধ = turn off; close নয়।", category="direct-translation", explanation="turn off the light"),
    dict(id="mistake:take-a-bath-hair", incorrect="I wash my hair in the bath every day. (when meaning showering head)", correct="I wash my hair every day.", bangla_tip="চুল ধোয়া = wash my hair; take a bath = গোসল।", category="word-choice", explanation="wash hair vs take a bath"),
    dict(id="mistake:wait-for", incorrect="I waited you for an hour.", correct="I waited for you for an hour.", bangla_tip="wait-এর পরে for লাগে।", category="prepositions", explanation="wait for someone"),
    dict(id="mistake:reply-back", incorrect="Please reply back soon.", correct="Please reply soon.", bangla_tip="reply-এর মানেই জবাব — back বাড়তি।", category="word-choice", explanation="reply (no back)"),
    dict(id="mistake:cope-up", incorrect="I cannot cope up with stress.", correct="I cannot cope with stress.", bangla_tip="cope with — up লাগে না।", category="word-choice", explanation="cope with"),
    dict(id="mistake:comprise-of", incorrect="The team comprises of 10 members.", correct="The team comprises 10 members.", bangla_tip="comprise-এর পরে of লাগে না (formal)।", category="grammar", explanation="comprise + object (or be comprised of)"),
    dict(id="mistake:request-for", incorrect="I request for your help.", correct="I request your help.", bangla_tip="request + object; for সাধারণত লাগে না।", category="prepositions", explanation="request something"),
    dict(id="mistake:same-like", incorrect="Your bag is same like mine.", correct="Your bag is the same as mine.", bangla_tip="the same as ব্যবহার করুন।", category="word-choice", explanation="the same as"),
    dict(id="mistake:discuss-with-about", incorrect="We discussed with him about money.", correct="We discussed money with him.", bangla_tip="discuss something with someone।", category="grammar", explanation="discuss X with Y"),
    dict(id="mistake:go-to-abroad", incorrect="She went to abroad last year.", correct="She went abroad last year.", bangla_tip="abroad-এর আগে to লাগে না।", category="prepositions", explanation="go abroad"),
    dict(id="mistake:take-care-for", incorrect="Please take care for yourself.", correct="Please take care of yourself.", bangla_tip="take care of।", category="prepositions", explanation="take care of"),
    dict(id="mistake:married-since", incorrect="They are married since 2018.", correct="They have been married since 2018.", bangla_tip="since-এর সাথে often present perfect।", category="grammar", explanation="have been + since"),
]

mistakes = load("common-mistakes.json")
print("mistakes added", merge_by_id(mistakes, NEW_MISTAKES), "total", len(mistakes))
save("common-mistakes.json", mistakes)

# --- Phrasals ---
NEW_PV = [
    dict(id="pv:bring-up", phrase="bring up", meaning_en="mention a topic; raise a child", meaning_bn="প্রসঙ্গ তোলা; সন্তান লালন-পালন", example="Don't bring up politics at dinner.", example_bn="ডিনারে রাজনীতির প্রসঙ্গ তুলবেন না।", cefr_level="B1"),
    dict(id="pv:call-off", phrase="call off", meaning_en="cancel", meaning_bn="বাতিল করা", example="They called off the match.", example_bn="তারা ম্যাচ বাতিল করেছে।", cefr_level="B1"),
    dict(id="pv:carry-on", phrase="carry on", meaning_en="continue", meaning_bn="চালিয়ে যাওয়া", example="Please carry on with your work.", example_bn="আপনার কাজ চালিয়ে যান।", cefr_level="A2"),
    dict(id="pv:check-in", phrase="check in", meaning_en="register at a hotel/airport", meaning_bn="চেক-ইন করা", example="We checked in at 2 pm.", example_bn="আমরা দুপুর ২টায় চেক-ইন করেছি।", cefr_level="A2"),
    dict(id="pv:check-out", phrase="check out", meaning_en="leave a hotel; look at", meaning_bn="চেক-আউট; দেখে নেওয়া", example="Check out this new app.", example_bn="এই নতুন অ্যাপটা দেখে নিন।", cefr_level="A2"),
    dict(id="pv:come-up-with", phrase="come up with", meaning_en="think of an idea", meaning_bn="আইডিয়া বের করা", example="She came up with a good plan.", example_bn="সে একটা ভালো পরিকল্পনা বের করেছে।", cefr_level="B1"),
    dict(id="pv:drop-off", phrase="drop off", meaning_en="leave someone somewhere by car", meaning_bn="গাড়ি থেকে নামিয়ে দেওয়া", example="Can you drop me off at school?", example_bn="আমাকে স্কুলে নামিয়ে দিতে পারবেন?", cefr_level="A2"),
    dict(id="pv:fill-in", phrase="fill in", meaning_en="complete a form", meaning_bn="ফর্ম পূরণ করা", example="Please fill in this form.", example_bn="এই ফর্মটা পূরণ করুন।", cefr_level="A2"),
    dict(id="pv:get-along", phrase="get along", meaning_en="have a good relationship", meaning_bn="মিলমিশ থাকা", example="I get along with my colleagues.", example_bn="সহকর্মীদের সাথে আমার মিলমিশ আছে।", cefr_level="B1"),
    dict(id="pv:give-in", phrase="give in", meaning_en="stop resisting; agree after pressure", meaning_bn="নতি স্বীকার করা", example="He finally gave in.", example_bn="অবশেষে সে নতি স্বীকার করেছে।", cefr_level="B1"),
    dict(id="pv:go-on", phrase="go on", meaning_en="continue; happen", meaning_bn="চলতে থাকা", example="Please go on.", example_bn="অনুগ্রহ করে চালিয়ে যান।", cefr_level="A2"),
    dict(id="pv:hang-out", phrase="hang out", meaning_en="spend time relaxing", meaning_bn="সময় কাটানো / ঘোরাঘুরি", example="We hang out on Fridays.", example_bn="শুক্রবারে আমরা একসাথে সময় কাটাই।", cefr_level="A2"),
    dict(id="pv:keep-up", phrase="keep up", meaning_en="continue at the same level", meaning_bn="তাল মিলিয়ে চলা", example="Keep up the good work.", example_bn="ভালো কাজ চালিয়ে যান।", cefr_level="B1"),
    dict(id="pv:look-forward-to", phrase="look forward to", meaning_en="feel happy about a future event", meaning_bn="অপেক্ষায় থাকা / আগ্রহে থাকা", example="I look forward to meeting you.", example_bn="আপনার সাথে দেখার অপেক্ষায় আছি।", cefr_level="B1"),
    dict(id="pv:make-up", phrase="make up", meaning_en="invent; become friends again", meaning_bn="বানিয়ে বলা; মিটমাট করা", example="Don't make up stories.", example_bn="গল্প বানিয়ে বলবেন না।", cefr_level="B1"),
    dict(id="pv:pass-away", phrase="pass away", meaning_en="die (polite)", meaning_bn="মারা যাওয়া (ভদ্র)", example="His grandfather passed away.", example_bn="তার দাদা মারা গেছেন।", cefr_level="B1"),
    dict(id="pv:set-up", phrase="set up", meaning_en="arrange; start a business", meaning_bn="সেটআপ করা / প্রতিষ্ঠা করা", example="They set up a new shop.", example_bn="তারা নতুন দোকান প্রতিষ্ঠা করেছে।", cefr_level="A2"),
    dict(id="pv:show-up", phrase="show up", meaning_en="arrive", meaning_bn="হাজির হওয়া", example="He didn't show up.", example_bn="সে হাজির হয়নি।", cefr_level="A2"),
    dict(id="pv:take-care-of", phrase="take care of", meaning_en="look after", meaning_bn="যত্ন নেওয়া", example="Take care of your health.", example_bn="নিজের স্বাস্থ্যের যত্ন নিন।", cefr_level="A2"),
    dict(id="pv:work-out", phrase="work out", meaning_en="exercise; find a solution", meaning_bn="ব্যায়াম করা; সমাধান খোঁজা", example="I work out three times a week.", example_bn="আমি সপ্তাহে তিনবার ব্যায়াম করি।", cefr_level="A2"),
]

pv = load("phrasal-verbs.json")
print("phrasals added", merge_by_id(pv, NEW_PV), "total", len(pv))
save("phrasal-verbs.json", pv)

# --- Spoken ---
spoken = load("spoken.json")
NEW_SPOKEN = [
    {
        "id": "spoken:doctor-1",
        "title": "At the doctor's",
        "level": "A2",
        "lines": [
            {"en": "I have a headache and a fever.", "bn": "আমার মাথাব্যথা ও জ্বর আছে।"},
            {"en": "How long have you felt like this?", "bn": "কতদিন ধরে এমন লাগছে?"},
            {"en": "Since yesterday evening.", "bn": "গতকাল সন্ধ্যা থেকে।"},
            {"en": "Take this medicine twice a day.", "bn": "এই ওষুধ দিনে দুবার খান।"},
        ],
    },
    {
        "id": "spoken:restaurant-1",
        "title": "Ordering food",
        "level": "A2",
        "lines": [
            {"en": "Could I see the menu, please?", "bn": "মেনুটা দেখতে পারি?"},
            {"en": "I'd like chicken biryani, please.", "bn": "এক প্লেট চিকেন বিরিয়ানি দেবেন।"},
            {"en": "Is it spicy?", "bn": "এটা কি ঝাল?"},
            {"en": "The bill, please.", "bn": "বিলটা দেন।"},
        ],
    },
    {
        "id": "spoken:classroom-1",
        "title": "In the classroom",
        "level": "A1",
        "lines": [
            {"en": "May I come in?", "bn": "আমি কি ভিতরে আসতে পারি?"},
            {"en": "Sorry I'm late.", "bn": "দুঃখিত, আমি দেরি করেছি।"},
            {"en": "Can you repeat that, please?", "bn": "আবার বলবেন কি?"},
            {"en": "I don't understand this word.", "bn": "এই শব্দটা বুঝতে পারছি না।"},
        ],
    },
    {
        "id": "spoken:bank-1",
        "title": "At the bank",
        "level": "B1",
        "lines": [
            {"en": "I'd like to open a savings account.", "bn": "আমি একটি সেভিংস অ্যাকাউন্ট খুলতে চাই।"},
            {"en": "Do you have your NID with you?", "bn": "আপনার কাছে NID আছে?"},
            {"en": "Yes, here it is.", "bn": "হ্যাঁ, এই যে।"},
            {"en": "Please fill in this form.", "bn": "এই ফর্মটা পূরণ করুন।"},
        ],
    },
]
print("spoken added", merge_by_id(spoken, NEW_SPOKEN), "total", len(spoken))
save("spoken.json", spoken)

# --- Quizzes: append from translation + mistakes + phrasals ---
quizzes = load("quizzes.json")
q_ids = {q["id"] for q in quizzes}
qi = 100


def add_q(obj):
    global qi
    while f"q{qi}" in q_ids:
        qi += 1
    obj = dict(obj)
    obj["id"] = f"q{qi}"
    q_ids.add(obj["id"])
    quizzes.append(obj)
    qi += 1


for m in NEW_MISTAKES[:12]:
    add_q(
        {
            "type": "mcq",
            "skill": "mistakes",
            "item_id": m["id"],
            "question": "Choose the correct sentence:",
            "question_bn": "সঠিক বাক্য বেছে নিন:",
            "options": [m["correct"], m["incorrect"], "Both are fine.", "Neither is correct."],
            "answer": m["correct"],
            "explanation": m.get("bangla_tip") or m.get("explanation", ""),
        }
    )

for p in NEW_PV[:10]:
    wrongs = ["stop forever", "forget quickly", "sleep early"]
    add_q(
        {
            "type": "mcq",
            "skill": "phrasal",
            "item_id": p["id"],
            "question": f'"{p["phrase"]}" means:',
            "question_bn": f'"{p["phrase"]}" মানে?',
            "options": [p["meaning_en"], wrongs[0], wrongs[1], wrongs[2]],
            "answer": p["meaning_en"],
            "explanation": p["meaning_bn"],
        }
    )

for t in TRANSLATION[:15]:
    add_q(
        {
            "type": "type",
            "skill": "translate",
            "item_id": t.get("item_id") or t["id"],
            "question": t["question"],
            "question_bn": t.get("question_bn", "ইংরেজিতে লিখুন:"),
            "answer": t["answer"],
            "answers": t.get("answers") or [t["answer"]],
            "explanation": t.get("explanation", ""),
        }
    )

print("quizzes total", len(quizzes))
save("quizzes.json", quizzes)

print("DONE enrichment batch")
