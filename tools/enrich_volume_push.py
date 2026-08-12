# Volume push toward §68: vocab, mistakes→50, phrasals→50, spoken lines
import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"


def load(n):
    return json.loads((DATA / n).read_text(encoding="utf-8"))


def save(n, o):
    (DATA / n).write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def merge(existing, news):
    seen = {x["id"] for x in existing}
    a = 0
    for it in news:
        if it["id"] in seen:
            continue
        existing.append(it)
        seen.add(it["id"])
        a += 1
    return a


def V(word, en, bn, pos, level, cat, ex, exb, syn=None, ant=None, fam=None):
    d = {
        "id": "vocab:" + word.lower().replace(" ", "-").replace("'", ""),
        "word": word,
        "meaning_en": en,
        "meaning_bn": bn,
        "part_of_speech": pos,
        "cefr_level": level,
        "category": cat,
        "example": ex,
        "example_bn": exb,
        "synonyms": syn or [],
        "antonyms": ant or [],
    }
    if fam:
        d["word_family"] = fam
    return d


F = lambda *rows: [{"word": w, "pos": p, "meaning_bn": bn} for w, p, bn in rows]

NEW_VOCAB = [
    V("arrive", "to reach a place", "পৌঁছানো", "verb", "A1", "travel", "What time do you arrive?", "আপনি কখন পৌঁছাবেন?", ["reach"], ["leave"], F(("arrival", "noun", "আগমন"))),
    V("leave", "to go away from a place", "ছেড়ে যাওয়া", "verb", "A1", "travel", "I leave home at 8.", "আমি ৮টায় বাড়ি থেকে বের হই।", ["depart"], ["arrive"]),
    V("busy", "having a lot to do", "ব্যস্ত", "adjective", "A1", "daily", "I am busy today.", "আজ আমি ব্যস্ত।", ["occupied"], ["free"], F(("busily", "adverb", "ব্যস্তভাবে"))),
    V("early", "before the usual time", "তাড়াতাড়ি", "adjective/adverb", "A1", "daily", "Come early tomorrow.", "কাল তাড়াতাড়ি আসুন।", [], ["late"]),
    V("late", "after the usual time", "দেরি", "adjective/adverb", "A1", "daily", "Sorry I am late.", "দুঃখিত, আমি দেরি করেছি।", [], ["early"]),
    V("hungry", "wanting food", "ক্ষুধার্ত", "adjective", "A1", "food", "I am hungry.", "আমি ক্ষুধার্ত।", [], [], F(("hunger", "noun", "ক্ষুধা"))),
    V("thirsty", "wanting a drink", "তৃষ্ণার্ত", "adjective", "A1", "food", "She is thirsty.", "সে তৃষ্ণার্ত।", [], [], F(("thirst", "noun", "তৃষ্ণা"))),
    V("tired", "needing rest", "ক্লান্ত", "adjective", "A1", "daily", "I feel tired after work.", "কাজের পর ক্লান্ত লাগে।", ["exhausted"], ["energetic"]),
    V("happy", "feeling pleasure", "খুশি", "adjective", "A1", "daily", "I am happy to help.", "সাহায্য করতে পেরে খুশি।", ["glad"], ["sad"], F(("happiness", "noun", "সুখ"), ("happily", "adverb", "খুশিতে"))),
    V("sad", "unhappy", "দুঃখিত", "adjective", "A1", "daily", "He looks sad.", "সে দুঃখিত দেখাচ্ছে।", ["unhappy"], ["happy"]),
    V("angry", "feeling strong dislike", "রাগান্বিত", "adjective", "A1", "daily", "Don't be angry.", "রাগ করবেন না।", ["annoyed"], ["calm"], F(("anger", "noun", "রাগ"))),
    V("afraid", "feeling fear", "ভীত", "adjective", "A1", "daily", "I am afraid of dogs.", "আমি কুকুরকে ভয় পাই।", ["scared"], ["brave"]),
    V("careful", "paying attention to avoid mistakes", "সতর্ক", "adjective", "A2", "daily", "Be careful on the road.", "রাস্তায় সতর্ক থাকুন।", ["cautious"], ["careless"], F(("carefully", "adverb", "সতর্কভাবে"), ("care", "noun/verb", "যত্ন"))),
    V("dangerous", "likely to cause harm", "বিপজ্জনক", "adjective", "A2", "daily", "This road is dangerous.", "এই রাস্তা বিপজ্জনক।", ["risky"], ["safe"], F(("danger", "noun", "বিপদ"))),
    V("safe", "not in danger", "নিরাপদ", "adjective", "A2", "daily", "Is it safe to drink?", "পান করা কি নিরাপদ?", ["secure"], ["dangerous"], F(("safely", "adverb", "নিরাপদে"), ("safety", "noun", "নিরাপত্তা"))),
    V("important", "having great meaning", "গুরুত্বপূর্ণ", "adjective", "A1", "daily", "This is an important meeting.", "এটি একটি গুরুত্বপূর্ণ মিটিং।", ["significant"], ["unimportant"], F(("importance", "noun", "গুরুত্ব"))),
    V("difficult", "not easy", "কঠিন", "adjective", "A1", "education", "This question is difficult.", "এই প্রশ্নটা কঠিন।", ["hard"], ["easy"], F(("difficulty", "noun", "কঠিনতা"))),
    V("easy", "not difficult", "সহজ", "adjective", "A1", "education", "English can be easy with practice.", "অনুশীলনে ইংরেজি সহজ হতে পারে।", ["simple"], ["difficult"], F(("easily", "adverb", "সহজে"))),
    V("interesting", "holding your attention", "মজার / আকর্ষণীয়", "adjective", "A1", "daily", "This book is interesting.", "এই বইটা আকর্ষণীয়।", ["engaging"], ["boring"], F(("interest", "noun", "আগ্রহ"), ("interested", "adjective", "আগ্রহী"))),
    V("boring", "not interesting", "একঘেয়ে", "adjective", "A2", "daily", "The lecture was boring.", "লেকচারটা একঘেয়ে ছিল।", ["dull"], ["interesting"]),
    V("beautiful", "very attractive", "সুন্দর", "adjective", "A1", "daily", "What a beautiful day!", "কী সুন্দর দিন!", ["pretty"], ["ugly"], F(("beauty", "noun", "সৌন্দর্য"), ("beautifully", "adverb", "সুন্দরভাবে"))),
    V("strong", "having power", "শক্তিশালী", "adjective", "A1", "health", "He is strong.", "সে শক্তিশালী।", ["powerful"], ["weak"], F(("strength", "noun", "শক্তি"), ("strongly", "adverb", "জোরে"))),
    V("weak", "not strong", "দুর্বল", "adjective", "A2", "health", "I feel weak today.", "আজ দুর্বল লাগছে।", ["frail"], ["strong"]),
    V("quick", "fast", "দ্রুত", "adjective", "A1", "daily", "That was a quick answer.", "সেটা দ্রুত উত্তর ছিল।", ["fast"], ["slow"], F(("quickly", "adverb", "দ্রুত"))),
    V("slow", "not fast", "ধীর", "adjective", "A1", "daily", "Please speak slowly.", "ধীরে কথা বলুন।", [], ["quick"], F(("slowly", "adverb", "ধীরে"))),
    V("loud", "making a lot of sound", "জোরে / উচ্চশব্দ", "adjective", "A2", "daily", "The music is too loud.", "মিউজিকটা খুব জোরে।", ["noisy"], ["quiet"], F(("loudly", "adverb", "জোরে"))),
    V("quiet", "with little noise", "শান্ত", "adjective", "A1", "daily", "Please be quiet.", "অনুগ্রহ করে চুপ থাকুন।", ["silent"], ["loud"], F(("quietly", "adverb", "চুপিচুপি"))),
    V("clean", "not dirty", "পরিষ্কার", "adjective/verb", "A1", "home", "Keep your room clean.", "রুম পরিষ্কার রাখুন।", [], ["dirty"], F(("cleanliness", "noun", "পরিচ্ছন্নতা"))),
    V("dirty", "not clean", "নোংরা", "adjective", "A1", "home", "Don't wear dirty clothes.", "নোংরা কাপড় পরবেন না।", [], ["clean"]),
    V("empty", "with nothing inside", "খালি", "adjective", "A1", "daily", "The bottle is empty.", "বোতলটা খালি।", [], ["full"]),
    V("full", "containing as much as possible", "ভর্তি", "adjective", "A1", "daily", "The bus is full.", "বাসটা ভর্তি।", [], ["empty"]),
    V("open", "not closed; to make open", "খোলা / খোলা", "adjective/verb", "A1", "daily", "The shop is open.", "দোকান খোলা আছে।", [], ["closed"], F(("opening", "noun", "উদ্বোধন"))),
    V("closed", "not open", "বন্ধ", "adjective", "A1", "daily", "The bank is closed today.", "আজ ব্যাংক বন্ধ।", [], ["open"]),
    V("heavy", "weighing a lot", "ভারী", "adjective", "A1", "daily", "This bag is heavy.", "এই ব্যাগটা ভারী।", [], ["light"]),
    V("light", "not heavy; not dark", "হালকা / আলো", "adjective/noun", "A1", "daily", "This bag is light.", "এই ব্যাগটা হালকা।", [], ["heavy"]),
    V("weather", "conditions of the air", "আবহাওয়া", "noun", "A1", "nature", "The weather is hot today.", "আজ আবহাওয়া গরম।", ["climate"], []),
    V("sunny", "with a lot of sun", "রৌদ্রোজ্জ্বল", "adjective", "A1", "nature", "It is sunny today.", "আজ রোদ আছে।", [], ["cloudy"]),
    V("rainy", "with a lot of rain", "বৃষ্টির", "adjective", "A1", "nature", "It is a rainy day.", "আজ বৃষ্টির দিন।", [], ["dry"], F(("rain", "noun/verb", "বৃষ্টি"))),
    V("cloudy", "with many clouds", "মেঘলা", "adjective", "A1", "nature", "The sky is cloudy.", "আকাশ মেঘলা।", [], ["sunny"]),
    V("windy", "with a lot of wind", "ঝোড়ো", "adjective", "A2", "nature", "It is windy outside.", "বাইরে ঝোড়ো হাওয়া।", [], []),
    V("hot", "having a high temperature", "গরম", "adjective", "A1", "daily", "The tea is hot.", "চা গরম।", ["warm"], ["cold"]),
    V("cold", "having a low temperature", "ঠান্ডা", "adjective", "A1", "daily", "I feel cold.", "আমার ঠান্ডা লাগছে।", ["cool"], ["hot"]),
    V("warm", "quite hot in a pleasant way", "উষ্ণ", "adjective", "A1", "daily", "The room is warm.", "রুমটা উষ্ণ।", [], ["cool"]),
    V("buy", "to get something by paying", "কেনা", "verb", "A1", "shopping", "I want to buy a shirt.", "আমি একটা শার্ট কিনতে চাই।", ["purchase"], ["sell"], F(("buyer", "noun", "ক্রেতা"))),
    V("sell", "to give something for money", "বিক্রি করা", "verb", "A1", "shopping", "They sell fresh fruit.", "তারা তাজা ফল বিক্রি করে।", [], ["buy"], F(("seller", "noun", "বিক্রেতা"), ("sale", "noun", "বিক্রি"))),
    V("pay", "to give money for something", "টাকা দেওয়া", "verb", "A1", "shopping", "How would you like to pay?", "আপনি কীভাবে টাকা দেবেন?", [], [], F(("payment", "noun", "পরিশোধ"))),
    V("cost", "the price of something", "দাম / খরচ", "verb/noun", "A1", "shopping", "How much does it cost?", "এটার দাম কত?", ["price"], []),
    V("cheap", "low in price", "সস্তা", "adjective", "A1", "shopping", "This phone is cheap.", "এই ফোনটা সস্তা।", ["inexpensive"], ["expensive"], F(("cheaply", "adverb", "সস্তায়"))),
    V("expensive", "costing a lot", "দামি", "adjective", "A1", "shopping", "That watch is expensive.", "ঐ ঘড়িটা দামি।", ["costly"], ["cheap"], F(("expense", "noun", "খরচ"))),
    V("order", "to ask for food/goods", "অর্ডার করা", "verb/noun", "A2", "food", "I would like to order tea.", "আমি চা অর্ডার করতে চাই।", [], []),
    V("menu", "list of food in a restaurant", "মেনু", "noun", "A1", "food", "Can I see the menu?", "মেনুটা দেখতে পারি?", [], []),
    V("bill", "paper that shows money to pay", "বিল", "noun", "A2", "food", "Can I have the bill, please?", "বিলটা দেবেন?", ["check"], []),
    V("taste", "the flavour of food", "স্বাদ / স্বাদ নেওয়া", "noun/verb", "A2", "food", "This curry tastes good.", "এই তরকারির স্বাদ ভালো।", ["flavour"], []),
    V("fresh", "recently made or produced", "তাজা", "adjective", "A1", "food", "Buy fresh vegetables.", "তাজা সবজি কিনুন।", [], ["stale"]),
    V("sweet", "tasting like sugar", "মিষ্টি", "adjective", "A1", "food", "I like sweet tea.", "আমি মিষ্টি চা পছন্দ করি।", [], ["bitter"]),
    V("spicy", "with strong hot flavour", "ঝাল", "adjective", "A2", "food", "Is the food spicy?", "খাবার কি ঝাল?", [], []),
    V("hospital", "place for medical treatment", "হাসপাতাল", "noun", "A1", "health", "She works in a hospital.", "সে হাসপাতালে কাজ করে।", [], []),
    V("medicine", "substance to treat illness", "ওষুধ", "noun", "A1", "health", "Take this medicine twice a day.", "এই ওষুধ দিনে দুবার খান।", ["drug"], []),
    V("pain", "unpleasant physical feeling", "ব্যথা", "noun", "A2", "health", "I have pain in my back.", "আমার পিঠে ব্যথা।", ["ache"], [], F(("painful", "adjective", "ব্যথাদায়ক"))),
    V("fever", "high body temperature from illness", "জ্বর", "noun", "A2", "health", "He has a fever.", "তার জ্বর আছে।", [], []),
    V("cough", "to force air from the throat", "কাশি / কাশি দেওয়া", "noun/verb", "A2", "health", "I have a bad cough.", "আমার খারাপ কাশি আছে।", [], []),
    V("appointment", "arranged meeting time", "অ্যাপয়েন্টমেন্ট", "noun", "A2", "office", "I have a doctor's appointment.", "আমার ডাক্তারের অ্যাপয়েন্টমেন্ট আছে।", ["booking"], [], F(("appoint", "verb", "নিয়োগ করা"))),
    V("message", "information sent to someone", "বার্তা", "noun", "A1", "technology", "I sent you a message.", "আমি তোমাকে মেসেজ পাঠিয়েছি।", ["note"], []),
    V("call", "to phone someone", "ফোন করা", "verb/noun", "A1", "technology", "Please call me later.", "পরে আমাকে ফোন করুন।", ["phone"], []),
    V("internet", "global computer network", "ইন্টারনেট", "noun", "A1", "technology", "Do you have internet at home?", "বাড়িতে ইন্টারনেট আছে?", ["web"], []),
    V("password", "secret word for access", "পাসওয়ার্ড", "noun", "A2", "technology", "Don't share your password.", "পাসওয়ার্ড শেয়ার করবেন না।", [], []),
    V("download", "to copy a file from the internet", "ডাউনলোড করা", "verb/noun", "A2", "technology", "Download the app first.", "আগে অ্যাপ ডাউনলোড করুন।", [], ["upload"]),
    V("upload", "to send a file to the internet", "আপলোড করা", "verb/noun", "A2", "technology", "Upload your photo here.", "এখানে ছবি আপলোড করুন।", [], ["download"]),
    V("screen", "the display of a device", "স্ক্রিন", "noun", "A2", "technology", "Look at the screen.", "স্ক্রিনের দিকে তাকান।", ["display"], []),
    V("office", "place where people work at desks", "অফিস", "noun", "A1", "office", "I work in an office.", "আমি অফিসে কাজ করি।", ["workplace"], []),
    V("meeting", "people gathering to discuss", "মিটিং", "noun", "A1", "office", "We have a meeting at 10.", "১০টায় আমাদের মিটিং আছে।", ["conference"], [], F(("meet", "verb", "সাক্ষাৎ করা"))),
    V("email", "electronic message", "ইমেইল", "noun/verb", "A1", "office", "Please send me an email.", "আমাকে ইমেইল পাঠান।", [], []),
    V("salary", "money paid for work", "বেতন", "noun", "A2", "office", "What is your salary?", "আপনার বেতন কত?", ["pay"], [], F(("salaried", "adjective", "বেতনভুক্ত"))),
    V("boss", "person in charge at work", "বস", "noun", "A2", "office", "My boss is kind.", "আমার বস দয়ালু।", ["manager"], []),
    V("team", "group working together", "টিম", "noun", "A1", "office", "We are a strong team.", "আমরা একটি শক্তিশালী টিম।", ["group"], []),
    V("travel", "to go from one place to another", "ভ্রমণ করা", "verb/noun", "A1", "travel", "I love to travel.", "আমি ভ্রমণ করতে ভালোবাসি।", ["journey"], [], F(("traveller", "noun", "পর্যটক"))),
    V("ticket", "paper for travel or entry", "টিকেট", "noun", "A1", "travel", "I bought a train ticket.", "আমি ট্রেনের টিকেট কিনেছি।", [], []),
    V("passport", "official travel document", "পাসপোর্ট", "noun", "A2", "travel", "Don't forget your passport.", "পাসপোর্ট ভুলবেন না।", [], []),
    V("airport", "place for planes", "বিমানবন্দর", "noun", "A1", "travel", "We are at the airport.", "আমরা বিমানবন্দরে আছি।", [], []),
    V("hotel", "place to stay when travelling", "হোটেল", "noun", "A1", "travel", "We stayed in a hotel.", "আমরা হোটেলে ছিলাম।", [], []),
    V("map", "drawing of an area", "মানচিত্র", "noun", "A1", "travel", "Look at the map.", "মানচিত্র দেখুন।", [], []),
    V("street", "road in a town", "রাস্তা", "noun", "A1", "outdoor", "I live on this street.", "আমি এই রাস্তায় থাকি।", ["road"], []),
    V("bridge", "structure over a river/road", "সেতু", "noun", "A2", "outdoor", "Cross the bridge.", "সেতু পার হোন।", [], []),
    V("park", "public green area", "পার্ক", "noun", "A1", "outdoor", "Children play in the park.", "শিশুরা পার্কে খেলে।", [], []),
    V("city", "large town", "শহর", "noun", "A1", "outdoor", "Dhaka is a big city.", "ঢাকা একটি বড় শহর।", ["town"], ["village"], F(("urban", "adjective", "শহুরে"))),
    V("village", "small country place", "গ্রাম", "noun", "A1", "outdoor", "My grandparents live in a village.", "দাদা-দাদি গ্রামে থাকেন।", [], ["city"], F(("rural", "adjective", "গ্রামীণ"))),
    V("neighbour", "person living nearby", "প্রতিবেশী", "noun", "A2", "home", "Our neighbour is friendly.", "আমাদের প্রতিবেশী বন্ধুসুলভ।", [], [], F(("neighbourhood", "noun", "পাড়া"))),
    V("kitchen", "room for cooking", "রান্নাঘর", "noun", "A1", "home", "She is in the kitchen.", "সে রান্নাঘরে আছে।", [], []),
    V("bedroom", "room for sleeping", "শোবার ঘর", "noun", "A1", "home", "My bedroom is small.", "আমার বেডরুম ছোট।", [], []),
    V("bathroom", "room with a bath/toilet", "বাথরুম", "noun", "A1", "home", "Where is the bathroom?", "বাথরুম কোথায়?", [], []),
    V("furniture", "tables, chairs, beds etc.", "আসবাবপত্র", "noun", "A2", "home", "We need new furniture.", "আমাদের নতুন আসবাব দরকার।", [], [], F(("furnish", "verb", "সাজানো"))),
    V("rent", "money paid to live in a place", "ভাড়া", "noun/verb", "A2", "home", "How much is the rent?", "ভাড়া কত?", [], []),
    V("exam", "formal test", "পরীক্ষা", "noun", "A1", "education", "I have an exam tomorrow.", "কাল আমার পরীক্ষা আছে।", ["test"], []),
    V("homework", "school work at home", "বাড়ির কাজ", "noun", "A1", "education", "Do your homework.", "হোমওয়ার্ক করো।", [], []),
    V("lesson", "period of learning", "লেসন / পাঠ", "noun", "A1", "education", "Today's lesson is about articles.", "আজকের লেসন article নিয়ে।", ["class"], []),
    V("dictionary", "book of word meanings", "অভিধান", "noun", "A1", "education", "Look it up in the dictionary.", "অভিধানে দেখুন।", [], []),
    V("library", "place with books to borrow", "লাইব্রেরি", "noun", "A1", "education", "I study in the library.", "আমি লাইব্রেরিতে পড়ি।", [], []),
    V("university", "higher education institution", "বিশ্ববিদ্যালয়", "noun", "A2", "education", "She goes to university.", "সে বিশ্ববিদ্যালয়ে যায়।", ["college"], []),
    V("knowledge", "what you know", "জ্ঞান", "noun", "A2", "education", "Knowledge is power.", "জ্ঞানই শক্তি।", [], [], F(("know", "verb", "জানা"), ("knowledgeable", "adjective", "জ্ঞানী"))),
    V("memory", "ability to remember", "স্মৃতি", "noun", "A2", "education", "I have a good memory.", "আমার স্মৃতিশক্তি ভালো।", [], [], F(("memorise", "verb", "মুখস্থ করা"), ("memorable", "adjective", "স্মরণীয়"))),
    V("mistake", "something wrong", "ভুল", "noun", "A1", "education", "Don't worry about small mistakes.", "ছোট ভুল নিয়ে চিন্তা করবেন না।", ["error"], [], F(("mistaken", "adjective", "ভুল ধারণার"))),
    V("answer", "response to a question", "উত্তর", "noun/verb", "A1", "education", "Write your answer here.", "এখানে উত্তর লিখুন।", ["reply"], ["question"]),
    V("question", "something you ask", "প্রশ্ন", "noun", "A1", "education", "Any questions?", "কোনো প্রশ্ন আছে?", [], ["answer"]),
    V("success", "achievement of a goal", "সাফল্য", "noun", "A2", "education", "Hard work leads to success.", "কঠোর পরিশ্রম সাফল্য আনে।", ["achievement"], ["failure"], F(("succeed", "verb", "সফল হওয়া"), ("successful", "adjective", "সফল"), ("successfully", "adverb", "সফলভাবে"))),
    V("failure", "lack of success", "ব্যর্থতা", "noun", "B1", "education", "Failure can teach us.", "ব্যর্থতা আমাদের শেখাতে পারে।", [], ["success"], F(("fail", "verb", "ফেল করা"))),
    V("future", "time that will come", "ভবিষ্যৎ", "noun", "A1", "daily", "Think about your future.", "ভবিষ্যৎ নিয়ে ভাবুন।", [], ["past"]),
    V("past", "time before now", "অতীত", "noun/adjective", "A1", "daily", "In the past, people wrote letters.", "অতীতে মানুষ চিঠি লিখত।", [], ["future"]),
    V("promise", "to say you will do something", "প্রতিশ্রুতি / প্রতিশ্রুতি দেওয়া", "noun/verb", "A2", "daily", "I promise to help you.", "আমি সাহায্য করার প্রতিশ্রুতি দিচ্ছি।", [], []),
    V("invite", "to ask someone to come", "নিমন্ত্রণ করা", "verb", "A2", "daily", "I invited my friends.", "আমি বন্ধুদের নিমন্ত্রণ করেছি।", [], [], F(("invitation", "noun", "নিমন্ত্রণ"))),
    V("visit", "to go and see a place/person", "বেড়াতে যাওয়া", "verb/noun", "A1", "travel", "We visited our uncle.", "আমরা চাচার বাড়ি গিয়েছিলাম।", [], [], F(("visitor", "noun", "দর্শনার্থী"))),
    V("enjoy", "to get pleasure from", "উপভোগ করা", "verb", "A1", "daily", "I enjoy reading.", "আমি পড়তে উপভোগ করি।", ["like"], [], F(("enjoyment", "noun", "আনন্দ"), ("enjoyable", "adjective", "উপভোগ্য"))),
    V("hope", "to want something to happen", "আশা করা", "verb/noun", "A1", "daily", "I hope you feel better.", "আশা করি আপনি ভালো বোধ করবেন।", ["wish"], [], F(("hopeful", "adjective", "আশাবাদী"))),
    V("worry", "to feel anxious", "চিন্তা করা", "verb/noun", "A2", "daily", "Don't worry.", "চিন্তা করবেন না।", ["stress"], [], F(("worried", "adjective", "চিন্তিত"))),
    V("decide", "to make a choice", "সিদ্ধান্ত নেওয়া", "verb", "A2", "daily", "I decided to learn English.", "আমি ইংরেজি শেখার সিদ্ধান্ত নিয়েছি।", ["choose"], [], F(("decision", "noun", "সিদ্ধান্ত"))),
    V("change", "to become different", "বদলানো / পরিবর্তন", "verb/noun", "A1", "daily", "I want to change my habits.", "আমি অভ্যাস বদলাতে চাই।", ["alter"], [], F(("changeable", "adjective", "পরিবর্তনশীল"))),
    V("help", "to make it easier for someone", "সাহায্য করা", "verb/noun", "A1", "daily", "Can you help me?", "আমাকে সাহায্য করতে পারেন?", ["assist"], [], F(("helpful", "adjective", "সহায়ক"), ("helper", "noun", "সাহায্যকারী"))),
    V("thank", "to express gratitude", "ধন্যবাদ জানানো", "verb", "A1", "daily", "Thank you for your help.", "সাহায্যের জন্য ধন্যবাদ।", [], [], F(("thanks", "noun", "ধন্যবাদ"), ("thankful", "adjective", "কৃতজ্ঞ"))),
    V("sorry", "feeling regret", "দুঃখিত", "adjective", "A1", "daily", "I am sorry for the delay.", "দেরির জন্য দুঃখিত।", ["apologetic"], []),
    V("welcome", "friendly greeting when someone arrives", "স্বাগতম", "noun/verb/adjective", "A1", "daily", "Welcome to our class!", "আমাদের ক্লাসে স্বাগতম!", [], []),
]

vocab = load("vocabulary.json")
# skip if word already exists by normalized word
have = {x["word"].lower() for x in vocab}
added_v = 0
for it in NEW_VOCAB:
    if it["word"].lower() in have:
        continue
    vocab.append(it)
    have.add(it["word"].lower())
    added_v += 1
save("vocabulary.json", vocab)
print("vocab added", added_v, "total", len(vocab))

NEW_M = [
    dict(id="mistake:go-to-home-again", incorrect="I will go to home now.", correct="I will go home now.", bangla_tip="go home — to লাগে না।", category="prepositions", explanation="go home (no to)"),
    dict(id="mistake:explain-me", incorrect="Please explain me this.", correct="Please explain this to me.", bangla_tip="explain something to someone।", category="grammar", explanation="explain X to Y"),
    dict(id="mistake:suggest-me", incorrect="Can you suggest me a book?", correct="Can you suggest a book to me?", bangla_tip="suggest something to someone নিরাপদ।", category="grammar", explanation="suggest something (to someone)"),
    dict(id="mistake:congratulate-for", incorrect="I congratulate you for your success.", correct="I congratulate you on your success.", bangla_tip="congratulate on।", category="prepositions", explanation="congratulate someone on something"),
    dict(id="mistake:afraid-from", incorrect="I am afraid from spiders.", correct="I am afraid of spiders.", bangla_tip="afraid of।", category="prepositions", explanation="afraid of"),
    dict(id="mistake:similar-with", incorrect="Your idea is similar with mine.", correct="Your idea is similar to mine.", bangla_tip="similar to।", category="prepositions", explanation="similar to"),
    dict(id="mistake:different-than-bn", incorrect="This is different than that. (careful formal)", correct="This is different from that.", bangla_tip="পরীক্ষায় different from নিরাপদ।", category="prepositions", explanation="prefer different from in careful English"),
    dict(id="mistake:enjoy-to", incorrect="I enjoy to swim.", correct="I enjoy swimming.", bangla_tip="enjoy-এর পরে verb-ing।", category="grammar", explanation="enjoy + -ing"),
    dict(id="mistake:look-forward-to-ing", incorrect="I look forward to meet you.", correct="I look forward to meeting you.", bangla_tip="look forward to + -ing।", category="grammar", explanation="look forward to + gerund"),
    dict(id="mistake:used-to-do-now", incorrect="I am used to wake up early.", correct="I am used to waking up early.", bangla_tip="be used to + -ing (অভ্যস্ত)।", category="grammar", explanation="be used to + -ing"),
]
mistakes = load("common-mistakes.json")
print("mistakes added", merge(mistakes, NEW_M), "total", len(mistakes))
save("common-mistakes.json", mistakes)

NEW_PV = [
    dict(id="pv:break-down", phrase="break down", meaning_en="stop working; become very upset", meaning_bn="নষ্ট হয়ে যাওয়া; ভেঙে পড়া", example="My bike broke down.", example_bn="আমার সাইকেল নষ্ট হয়ে গেছে।", cefr_level="B1"),
    dict(id="pv:break-up", phrase="break up", meaning_en="end a relationship", meaning_bn="সম্পর্ক ভাঙা", example="They broke up last year.", example_bn="তারা গত বছর আলাদা হয়ে গেছে।", cefr_level="B1"),
    dict(id="pv:catch-up", phrase="catch up", meaning_en="reach the same level; talk after a long time", meaning_bn="তাল মেলানো; খোঁজখবর নেওয়া", example="Let's catch up soon.", example_bn="শীঘ্রই কথা বলে খোঁজখবর নেই।", cefr_level="B1"),
    dict(id="pv:cut-down-on", phrase="cut down on", meaning_en="reduce", meaning_bn="কমানো", example="I am cutting down on sugar.", example_bn="আমি চিনি কমাচ্ছি।", cefr_level="B1"),
    dict(id="pv:end-up", phrase="end up", meaning_en="finally be in a situation", meaning_bn="শেষমেশ এমন হওয়া", example="We ended up at home.", example_bn="শেষমেশ আমরা বাড়িতেই এসেছি।", cefr_level="B1"),
    dict(id="pv:figure-out", phrase="figure out", meaning_en="understand / solve", meaning_bn="বুঝে নেওয়া / সমাধান করা", example="I can't figure out this problem.", example_bn="এই সমস্যা বুঝতে পারছি না।", cefr_level="B1"),
    dict(id="pv:get-back", phrase="get back", meaning_en="return", meaning_bn="ফিরে আসা", example="When did you get back?", example_bn="কখন ফিরে এলে?", cefr_level="A2"),
    dict(id="pv:get-over", phrase="get over", meaning_en="recover from", meaning_bn="কাটিয়ে ওঠা", example="She got over the flu.", example_bn="সে ফ্লু কাটিয়ে উঠেছে।", cefr_level="B1"),
    dict(id="pv:give-away", phrase="give away", meaning_en="give free; reveal a secret", meaning_bn="বিনামূল্যে দেওয়া; গোপন কথা ফাঁস", example="Don't give away the ending.", example_bn="শেষটা ফাঁস করবেন না।", cefr_level="B1"),
    dict(id="pv:go-back", phrase="go back", meaning_en="return to a place", meaning_bn="ফিরে যাওয়া", example="I will go back tomorrow.", example_bn="কাল ফিরে যাব।", cefr_level="A1"),
    dict(id="pv:grow-up", phrase="grow up", meaning_en="become an adult", meaning_bn="বড় হওয়া", example="I grew up in Dhaka.", example_bn="আমি ঢাকায় বড় হয়েছি।", cefr_level="A2"),
    dict(id="pv:hold-on", phrase="hold on", meaning_en="wait", meaning_bn="অপেক্ষা করা", example="Hold on a minute.", example_bn="এক মিনিট অপেক্ষা করুন।", cefr_level="A2"),
    dict(id="pv:look-up", phrase="look up", meaning_en="search for information", meaning_bn="খুঁজে দেখা (অভিধান/অনলাইন)", example="Look up the word in a dictionary.", example_bn="অভিধানে শব্দটা দেখুন।", cefr_level="A2"),
    dict(id="pv:put-on", phrase="put on", meaning_en="wear clothes", meaning_bn="পরা", example="Put on your jacket.", example_bn="জ্যাকেট পরুন।", cefr_level="A1"),
    dict(id="pv:take-out", phrase="take out", meaning_en="remove; buy food to eat elsewhere", meaning_bn="বের করা; পার্সেল খাবার", example="Let's take out pizza.", example_bn="চলো পিজা পার্সেল নিই।", cefr_level="A2"),
    dict(id="pv:throw-away", phrase="throw away", meaning_en="put in the bin", meaning_bn="ফেলে দেওয়া", example="Don't throw away paper.", example_bn="কাগজ ফেলবেন না।", cefr_level="A2"),
    dict(id="pv:try-on", phrase="try on", meaning_en="put on clothes to see if they fit", meaning_bn="পরে দেখা", example="Can I try this on?", example_bn="এটা পরে দেখতে পারি?", cefr_level="A2"),
    dict(id="pv:turn-up", phrase="turn up", meaning_en="appear; increase volume", meaning_bn="হাজির হওয়া; ভলিউম বাড়ানো", example="He turned up late.", example_bn="সে দেরি করে এসেছে।", cefr_level="B1"),
    dict(id="pv:wake-up", phrase="wake up", meaning_en="stop sleeping", meaning_bn="ঘুম ভাঙা", example="I wake up at 6.", example_bn="আমি ৬টায় ঘুম ভাঙি।", cefr_level="A1"),
    dict(id="pv:write-down", phrase="write down", meaning_en="record in writing", meaning_bn="লিখে রাখা", example="Write down the address.", example_bn="ঠিকানা লিখে রাখুন।", cefr_level="A2"),
]
pv = load("phrasal-verbs.json")
print("pv added", merge(pv, NEW_PV), "total", len(pv))
save("phrasal-verbs.json", pv)

NEW_SP = [
    {
        "id": "spoken:weather-1",
        "title": "Talking about weather",
        "level": "A1",
        "lines": [
            {"en": "How is the weather today?", "bn": "আজ আবহাওয়া কেমন?"},
            {"en": "It's sunny and hot.", "bn": "রোদ আর গরম।"},
            {"en": "It might rain later.", "bn": "পরে বৃষ্টি হতে পারে।"},
            {"en": "Don't forget your umbrella.", "bn": "ছাতা ভুলবেন না।"},
            {"en": "Thanks for the reminder.", "bn": "মনে করিয়ে দেওয়ার জন্য ধন্যবাদ।"},
        ],
    },
    {
        "id": "spoken:market-1",
        "title": "At the market",
        "level": "A2",
        "lines": [
            {"en": "How much are the bananas?", "bn": "কলা কত করে?"},
            {"en": "They are 80 taka a dozen.", "bn": "ডজন ৮০ টাকা।"},
            {"en": "Can you give me a discount?", "bn": "একটু কম দেবেন?"},
            {"en": "Okay, 70 taka.", "bn": "ঠিক আছে, ৭০ টাকা।"},
            {"en": "Please give me two dozen.", "bn": "দুই ডজন দেন।"},
        ],
    },
    {
        "id": "spoken:bus-1",
        "title": "On the bus",
        "level": "A2",
        "lines": [
            {"en": "Does this bus go to Gulshan?", "bn": "এই বাস গুলশান যায়?"},
            {"en": "Yes, get off at the next stop.", "bn": "হ্যাঁ, পরের স্টপে নামবেন।"},
            {"en": "How long will it take?", "bn": "কতক্ষণ লাগবে?"},
            {"en": "About twenty minutes.", "bn": "প্রায় বিশ মিনিট।"},
            {"en": "Thank you very much.", "bn": "অনেক ধন্যবাদ।"},
        ],
    },
    {
        "id": "spoken:friend-1",
        "title": "Making plans with a friend",
        "level": "A2",
        "lines": [
            {"en": "Are you free this evening?", "bn": "আজ সন্ধ্যায় খালি আছো?"},
            {"en": "Yes, what do you want to do?", "bn": "হ্যাঁ, কী করতে চাও?"},
            {"en": "Let's watch a film.", "bn": "চলো একটা সিনেমা দেখি।"},
            {"en": "Good idea. What time?", "bn": "ভালো আইডিয়া। কখন?"},
            {"en": "How about 7 pm?", "bn": "সন্ধ্যা ৭টা কেমন?"},
            {"en": "Perfect. See you then.", "bn": "পারফেক্ট। তখন দেখা হবে।"},
        ],
    },
    {
        "id": "spoken:hotel-1",
        "title": "At a hotel",
        "level": "B1",
        "lines": [
            {"en": "I have a reservation under Rahman.", "bn": "রাহমান নামে আমার রিজার্ভেশন আছে।"},
            {"en": "May I see your ID, please?", "bn": "আইডি দেখতে পারি?"},
            {"en": "Here you are.", "bn": "এই যে।"},
            {"en": "Your room is on the third floor.", "bn": "আপনার রুম তৃতীয় তলায়।"},
            {"en": "What time is breakfast?", "bn": "ব্রেকফাস্ট কখন?"},
            {"en": "From 7 to 10 in the morning.", "bn": "সকাল ৭টা থেকে ১০টা।"},
        ],
    },
    {
        "id": "spoken:office-1",
        "title": "At the office",
        "level": "B1",
        "lines": [
            {"en": "Could you send me the report today?", "bn": "আজ রিপোর্টটা পাঠাতে পারবেন?"},
            {"en": "Yes, I will email it by 5 pm.", "bn": "হ্যাঁ, বিকেল ৫টার মধ্যে ইমেইল করব।"},
            {"en": "Is the meeting still on?", "bn": "মিটিং কি আছে?"},
            {"en": "It has been put off until tomorrow.", "bn": "কাল পর্যন্ত স্থগিত হয়েছে।"},
            {"en": "Okay, thanks for letting me know.", "bn": "ঠিক আছে, জানানোর জন্য ধন্যবাদ।"},
        ],
    },
]
spoken = load("spoken.json")
print("spoken added", merge(spoken, NEW_SP), "total dialogues", len(spoken), "lines", sum(len(x["lines"]) for x in spoken))
save("spoken.json", spoken)

print("DONE volume push")
