# Generate enriched vocabulary.json + vocabulary-lists.json
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

# Accurate A1–B1 bank for Bengali learners
WORDS = [
  # --- keep/enrich existing ---
  dict(id="vocab:improve", word="improve", meaning_en="to make better", meaning_bn="উন্নত করা / উন্নতি সাধন করা", part_of_speech="verb", cefr_level="A2", category="education", example="I want to improve my English.", example_bn="আমি আমার ইংরেজি উন্নত করতে চাই।", synonyms=["enhance", "develop"], antonyms=["worsen"]),
  dict(id="vocab:practice", word="practice", meaning_en="regular training to get better (US spelling; UK verb often practise)", meaning_bn="অনুশীলন (noun) / অনুশীলন করা (verb)", part_of_speech="verb/noun", cefr_level="A1", category="education", example="Practice speaking every day.", example_bn="প্রতিদিন স্পিকিং অনুশীলন করুন।", synonyms=["rehearse", "train"], antonyms=[]),
  dict(id="vocab:confident", word="confident", meaning_en="sure of yourself", meaning_bn="আত্মবিশ্বাসী", part_of_speech="adjective", cefr_level="A2", category="office", example="She feels confident in interviews.", example_bn="সে ইন্টারভিউতে আত্মবিশ্বাসী বোধ করে।", synonyms=["assured", "self-assured"], antonyms=["nervous", "shy"]),
  dict(id="vocab:appointment", word="appointment", meaning_en="a planned meeting", meaning_bn="অ্যাপয়েন্টমেন্ট / নির্ধারিত সাক্ষাৎ", part_of_speech="noun", cefr_level="A2", category="office", example="I have a doctor's appointment at 4 pm.", example_bn="বিকেল ৪টায় আমার ডাক্তারের অ্যাপয়েন্টমেন্ট আছে।", synonyms=["meeting", "booking"], antonyms=[]),
  dict(id="vocab:recommend", word="recommend", meaning_en="to suggest something as good", meaning_bn="সুপারিশ করা", part_of_speech="verb", cefr_level="B1", category="daily", example="Can you recommend a good book?", example_bn="আপনি কি একটি ভালো বই সুপারিশ করতে পারেন?", synonyms=["suggest", "advise"], antonyms=["discourage"]),
  dict(id="vocab:deadline", word="deadline", meaning_en="the latest time to finish something", meaning_bn="শেষ সময়সীমা", part_of_speech="noun", cefr_level="B1", category="office", example="The project deadline is Friday.", example_bn="প্রজেক্টের ডেডলাইন শুক্রবার।", synonyms=["due date", "time limit"], antonyms=[]),
  dict(id="vocab:polite", word="polite", meaning_en="having good manners", meaning_bn="বিনয়ী / ভদ্র", part_of_speech="adjective", cefr_level="A2", category="daily", example="Please be polite to customers.", example_bn="অনুগ্রহ করে কাস্টমারদের সাথে ভদ্র থাকুন।", synonyms=["courteous", "respectful"], antonyms=["rude"]),
  dict(id="vocab:journey", word="journey", meaning_en="travel from one place to another", meaning_bn="যাত্রা", part_of_speech="noun", cefr_level="A2", category="travel", example="It was a long journey by bus.", example_bn="বাস করে লম্বা যাত্রা ছিল।", synonyms=["trip", "voyage"], antonyms=[]),
  dict(id="vocab:necessary", word="necessary", meaning_en="needed", meaning_bn="প্রয়োজনীয়", part_of_speech="adjective", cefr_level="A2", category="daily", example="Is a passport necessary?", example_bn="পাসপোর্ট কি প্রয়োজনীয়?", synonyms=["essential", "required"], antonyms=["unnecessary", "optional"]),
  dict(id="vocab:opportunity", word="opportunity", meaning_en="a chance to do something", meaning_bn="সুযোগ", part_of_speech="noun", cefr_level="B1", category="office", example="This job is a great opportunity.", example_bn="এই চাকরিটি একটি বড় সুযোগ।", synonyms=["chance", "opening"], antonyms=[]),
  dict(id="vocab:explain", word="explain", meaning_en="to make something clear", meaning_bn="ব্যাখ্যা করা", part_of_speech="verb", cefr_level="A2", category="education", example="Can you explain this grammar rule?", example_bn="আপনি কি এই গ্রামার রুল ব্যাখ্যা করতে পারেন?", synonyms=["clarify", "describe"], antonyms=["confuse"]),
  dict(id="vocab:available", word="available", meaning_en="free to use or free to meet", meaning_bn="উপলব্ধ; (সময়) ফাঁকা", part_of_speech="adjective", cefr_level="A2", category="office", example="Are you available tomorrow?", example_bn="আপনি কি কাল খালি আছেন?", synonyms=["free", "open"], antonyms=["busy", "unavailable"]),
  dict(id="vocab:family", word="family", meaning_en="parents, children, and relatives as a group", meaning_bn="পরিবার", part_of_speech="noun", cefr_level="A1", category="home", example="My family lives in Chittagong.", example_bn="আমার পরিবার চট্টগ্রামে থাকে।", synonyms=["relatives", "household"], antonyms=[]),
  dict(id="vocab:yesterday", word="yesterday", meaning_en="the day before today", meaning_bn="গতকাল", part_of_speech="adverb/noun", cefr_level="A1", category="daily", example="I met her yesterday.", example_bn="আমি তাকে গতকাল দেখেছিলাম।", synonyms=[], antonyms=["tomorrow"]),
  dict(id="vocab:tomorrow", word="tomorrow", meaning_en="the day after today", meaning_bn="আগামীকাল", part_of_speech="adverb/noun", cefr_level="A1", category="daily", example="We will start tomorrow.", example_bn="আমরা আগামীকাল শুরু করব।", synonyms=[], antonyms=["yesterday"]),
  dict(id="vocab:hungry", word="hungry", meaning_en="wanting food", meaning_bn="ক্ষুধার্ত", part_of_speech="adjective", cefr_level="A1", category="food", example="I am hungry after class.", example_bn="ক্লাসের পর আমি ক্ষুধার্ত।", synonyms=["starving"], antonyms=["full"]),
  dict(id="vocab:thirsty", word="thirsty", meaning_en="wanting a drink", meaning_bn="তৃষ্ণার্ত", part_of_speech="adjective", cefr_level="A1", category="food", example="She is thirsty; she needs water.", example_bn="সে তৃষ্ণার্ত; তার পানি দরকার।", synonyms=[], antonyms=[]),
  dict(id="vocab:station", word="station", meaning_en="a place where trains or buses stop", meaning_bn="স্টেশন", part_of_speech="noun", cefr_level="A1", category="travel", example="Meet me at the bus station.", example_bn="বাস স্টেশনে আমার সাথে দেখা করো।", synonyms=["terminal", "stop"], antonyms=[]),
  dict(id="vocab:ticket", word="ticket", meaning_en="a pass that lets you travel or enter", meaning_bn="টিকিট", part_of_speech="noun", cefr_level="A1", category="travel", example="I bought a train ticket.", example_bn="আমি একটা ট্রেনের টিকিট কিনেছি।", synonyms=["pass", "fare"], antonyms=[]),
  dict(id="vocab:medicine", word="medicine", meaning_en="something you take to treat illness", meaning_bn="ওষুধ", part_of_speech="noun", cefr_level="A2", category="health", example="Take this medicine twice a day.", example_bn="এই ওষুধ দিনে দুবার খান।", synonyms=["medication", "drug"], antonyms=[]),
  dict(id="vocab:borrow", word="borrow", meaning_en="to take something briefly and return it", meaning_bn="ধার নেওয়া", part_of_speech="verb", cefr_level="A2", category="verbs", example="Can I borrow your pen?", example_bn="আমি কি তোমার কলমটা ধার নিতে পারি?", synonyms=[], antonyms=["lend"]),
  dict(id="vocab:lend", word="lend", meaning_en="to give something briefly to someone", meaning_bn="ধার দেওয়া", part_of_speech="verb", cefr_level="A2", category="verbs", example="Please lend me your book.", example_bn="অনুগ্রহ করে আমাকে তোমার বইটা ধার দাও।", synonyms=["loan"], antonyms=["borrow"]),
  dict(id="vocab:busy", word="busy", meaning_en="having a lot to do", meaning_bn="ব্যস্ত", part_of_speech="adjective", cefr_level="A1", category="office", example="Sorry, I am busy today.", example_bn="দুঃখিত, আজ আমি ব্যস্ত।", synonyms=["occupied"], antonyms=["free", "available"]),
  dict(id="vocab:early", word="early", meaning_en="before the usual time", meaning_bn="তাড়াতাড়ি / আগে", part_of_speech="adjective/adverb", cefr_level="A1", category="daily", example="Please come early tomorrow.", example_bn="কাল অনুগ্রহ করে তাড়াতাড়ি এসো।", synonyms=[], antonyms=["late"]),
  dict(id="vocab:late", word="late", meaning_en="after the usual time", meaning_bn="দেরি / বিলম্বে", part_of_speech="adjective/adverb", cefr_level="A1", category="daily", example="The bus was late.", example_bn="বাসটা দেরি করেছিল।", synonyms=["delayed"], antonyms=["early"]),
  dict(id="vocab:forget", word="forget", meaning_en="to not remember", meaning_bn="ভুলে যাওয়া", part_of_speech="verb", cefr_level="A1", category="verbs", example="Don't forget your homework.", example_bn="তোমার হোমওয়ার্ক ভুলো না।", synonyms=[], antonyms=["remember"]),
  dict(id="vocab:remember", word="remember", meaning_en="to keep something in your mind", meaning_bn="মনে রাখা", part_of_speech="verb", cefr_level="A1", category="verbs", example="I remember your name.", example_bn="আমি তোমার নাম মনে রেখেছি।", synonyms=["recall"], antonyms=["forget"]),
  dict(id="vocab:arrive", word="arrive", meaning_en="to reach a place", meaning_bn="পৌঁছানো", part_of_speech="verb", cefr_level="A2", category="travel", example="We arrived at the station at 9.", example_bn="আমরা ৯টায় স্টেশনে পৌঁছালাম।", synonyms=["reach", "get to"], antonyms=["leave", "depart"]),
  dict(id="vocab:leave", word="leave", meaning_en="to go away from a place", meaning_bn="ছেড়ে যাওয়া / বের হওয়া", part_of_speech="verb", cefr_level="A1", category="travel", example="I leave home at 7 am.", example_bn="আমি সকাল ৭টায় বাড়ি থেকে বের হই।", synonyms=["depart", "go"], antonyms=["arrive", "stay"]),

  # --- home ---
  dict(id="vocab:kitchen", word="kitchen", meaning_en="the room where you cook", meaning_bn="রান্নাঘর", part_of_speech="noun", cefr_level="A1", category="home", example="Mum is in the kitchen.", example_bn="মা রান্নাঘরে আছেন।", synonyms=[], antonyms=[]),
  dict(id="vocab:bedroom", word="bedroom", meaning_en="a room for sleeping", meaning_bn="শোবার ঘর", part_of_speech="noun", cefr_level="A1", category="home", example="My bedroom is upstairs.", example_bn="আমার শোবার ঘর উপরতলায়।", synonyms=[], antonyms=[]),
  dict(id="vocab:clean", word="clean", meaning_en="not dirty; to remove dirt", meaning_bn="পরিষ্কার; পরিষ্কার করা", part_of_speech="adjective/verb", cefr_level="A1", category="home", example="Please clean the table.", example_bn="অনুগ্রহ করে টেবিলটা পরিষ্কার করো।", synonyms=["tidy", "wash"], antonyms=["dirty"]),
  dict(id="vocab:dirty", word="dirty", meaning_en="not clean", meaning_bn="নোংরা / ময়লা", part_of_speech="adjective", cefr_level="A1", category="home", example="These clothes are dirty.", example_bn="এই কাপড়গুলো নোংরা।", synonyms=["messy"], antonyms=["clean"]),
  dict(id="vocab:neighbour", word="neighbour", meaning_en="a person living near you", meaning_bn="প্রতিবেশী", part_of_speech="noun", cefr_level="A1", category="home", example="Our neighbour is very kind.", example_bn="আমাদের প্রতিবেশী খুব দয়ালু।", synonyms=["resident"], antonyms=[]),
  dict(id="vocab:furniture", word="furniture", meaning_en="tables, chairs, beds, etc.", meaning_bn="আসবাবপত্র", part_of_speech="noun", cefr_level="A2", category="home", example="We bought new furniture.", example_bn="আমরা নতুন আসবাব কিনেছি।", synonyms=[], antonyms=[]),
  dict(id="vocab:rent", word="rent", meaning_en="money paid to live in a house; to pay for temporary use", meaning_bn="ভাড়া; ভাড়া নেওয়া", part_of_speech="noun/verb", cefr_level="A2", category="home", example="How much is the rent?", example_bn="ভাড়া কত?", synonyms=["hire"], antonyms=[]),

  # --- office ---
  dict(id="vocab:meeting", word="meeting", meaning_en="people gathering to discuss work", meaning_bn="মিটিং / সভা", part_of_speech="noun", cefr_level="A2", category="office", example="The meeting starts at 10.", example_bn="মিটিং ১০টায় শুরু।", synonyms=["discussion", "conference"], antonyms=[]),
  dict(id="vocab:email", word="email", meaning_en="an electronic message", meaning_bn="ইমেইল", part_of_speech="noun/verb", cefr_level="A1", category="office", example="Please send me an email.", example_bn="অনুগ্রহ করে আমাকে ইমেইল পাঠান।", synonyms=["message"], antonyms=[]),
  dict(id="vocab:schedule", word="schedule", meaning_en="a plan of times for work or events", meaning_bn="সময়সূচি", part_of_speech="noun/verb", cefr_level="A2", category="office", example="Check the schedule for today.", example_bn="আজকের সময়সূচি দেখুন।", synonyms=["timetable", "agenda"], antonyms=[]),
  dict(id="vocab:salary", word="salary", meaning_en="money you earn from a job each month", meaning_bn="বেতন", part_of_speech="noun", cefr_level="A2", category="office", example="His salary increased this year.", example_bn="এই বছর তার বেতন বেড়েছে।", synonyms=["pay", "wage"], antonyms=[]),
  dict(id="vocab:colleague", word="colleague", meaning_en="a person you work with", meaning_bn="সহকর্মী", part_of_speech="noun", cefr_level="A2", category="office", example="My colleague helped me.", example_bn="আমার সহকর্মী আমাকে সাহায্য করেছে।", synonyms=["coworker"], antonyms=[]),
  dict(id="vocab:report", word="report", meaning_en="a written description of work or facts", meaning_bn="রিপোর্ট / বিবরণী", part_of_speech="noun/verb", cefr_level="B1", category="office", example="I finished the sales report.", example_bn="আমি সেলস রিপোর্ট শেষ করেছি।", synonyms=["document", "summary"], antonyms=[]),
  dict(id="vocab:manager", word="manager", meaning_en="a person who controls a team or shop", meaning_bn="ম্যানেজার / ব্যবস্থাপক", part_of_speech="noun", cefr_level="A2", category="office", example="Speak to the manager, please.", example_bn="অনুগ্রহ করে ম্যানেজারের সাথে কথা বলুন।", synonyms=["boss", "supervisor"], antonyms=[]),
  dict(id="vocab:task", word="task", meaning_en="a piece of work to do", meaning_bn="কাজ / অ্যাসাইনমেন্ট", part_of_speech="noun", cefr_level="A2", category="office", example="This task will take one hour.", example_bn="এই কাজটিতে এক ঘণ্টা লাগবে।", synonyms=["job", "duty"], antonyms=[]),

  # --- outdoor / nature ---
  dict(id="vocab:park", word="park", meaning_en="a public green area for walking and rest", meaning_bn="পার্ক", part_of_speech="noun", cefr_level="A1", category="outdoor", example="Children play in the park.", example_bn="শিশুরা পার্কে খেলে।", synonyms=["garden"], antonyms=[]),
  dict(id="vocab:bridge", word="bridge", meaning_en="a structure that crosses a river or road", meaning_bn="সেতু", part_of_speech="noun", cefr_level="A2", category="outdoor", example="Cross the bridge carefully.", example_bn="সাবধানে সেতু পার হও।", synonyms=[], antonyms=[]),
  dict(id="vocab:traffic", word="traffic", meaning_en="cars and buses on the road", meaning_bn="ট্রাফিক / যানজট", part_of_speech="noun", cefr_level="A2", category="outdoor", example="Traffic is heavy in the morning.", example_bn="সকালে ট্রাফিক খুব বেশি।", synonyms=[], antonyms=[]),
  dict(id="vocab:river", word="river", meaning_en="a large natural flow of water", meaning_bn="নদী", part_of_speech="noun", cefr_level="A1", category="nature", example="The Padma is a wide river.", example_bn="পদ্মা একটি প্রশস্ত নদী।", synonyms=["stream"], antonyms=[]),
  dict(id="vocab:forest", word="forest", meaning_en="a large area with many trees", meaning_bn="বন", part_of_speech="noun", cefr_level="A2", category="nature", example="We walked through the forest.", example_bn="আমরা বনের ভিতর দিয়ে হেঁটেছি।", synonyms=["woods"], antonyms=["desert"]),
  dict(id="vocab:mountain", word="mountain", meaning_en="a very high hill", meaning_bn="পর্বত / পাহাড়", part_of_speech="noun", cefr_level="A1", category="nature", example="They climbed the mountain.", example_bn="তারা পাহাড়ে উঠেছিল।", synonyms=["hill", "peak"], antonyms=[]),
  dict(id="vocab:weather", word="weather", meaning_en="conditions like rain, sun, wind", meaning_bn="আবহাওয়া", part_of_speech="noun", cefr_level="A1", category="nature", example="The weather is hot today.", example_bn="আজ আবহাওয়া গরম।", synonyms=["climate"], antonyms=[]),
  dict(id="vocab:rain", word="rain", meaning_en="water falling from clouds", meaning_bn="বৃষ্টি", part_of_speech="noun/verb", cefr_level="A1", category="nature", example="It will rain this evening.", example_bn="আজ সন্ধ্যায় বৃষ্টি হবে।", synonyms=["shower"], antonyms=["drought"]),
  dict(id="vocab:sunny", word="sunny", meaning_en="bright with sunshine", meaning_bn="রৌদ্রোজ্জ্বল", part_of_speech="adjective", cefr_level="A1", category="nature", example="It is a sunny morning.", example_bn="আজ রৌদ্রোজ্জ্বল সকাল।", synonyms=["bright"], antonyms=["cloudy", "rainy"]),
  dict(id="vocab:pollution", word="pollution", meaning_en="dirty air, water, or land from human activity", meaning_bn="দূষণ", part_of_speech="noun", cefr_level="B1", category="nature", example="Air pollution is a big problem.", example_bn="বায়ু দূষণ একটি বড় সমস্যা।", synonyms=["contamination"], antonyms=["purity"]),

  # --- food ---
  dict(id="vocab:breakfast", word="breakfast", meaning_en="the first meal of the day", meaning_bn="নাস্তা / সকালের খাবার", part_of_speech="noun", cefr_level="A1", category="food", example="I eat breakfast at 8.", example_bn="আমি ৮টায় নাস্তা করি।", synonyms=[], antonyms=[]),
  dict(id="vocab:lunch", word="lunch", meaning_en="the midday meal", meaning_bn="দুপুরের খাবার", part_of_speech="noun", cefr_level="A1", category="food", example="Let's have lunch together.", example_bn="চলো একসাথে লাঞ্চ করি।", synonyms=[], antonyms=[]),
  dict(id="vocab:dinner", word="dinner", meaning_en="the main evening meal", meaning_bn="রাতের খাবার", part_of_speech="noun", cefr_level="A1", category="food", example="Dinner is ready.", example_bn="ডিনার রেডি।", synonyms=["supper"], antonyms=[]),
  dict(id="vocab:delicious", word="delicious", meaning_en="very tasty", meaning_bn="খুব সুস্বাদু", part_of_speech="adjective", cefr_level="A2", category="food", example="This curry is delicious.", example_bn="এই তরকারি খুব সুস্বাদু।", synonyms=["tasty", "yummy"], antonyms=["tasteless"]),
  dict(id="vocab:vegetable", word="vegetable", meaning_en="a plant used as food", meaning_bn="সবজি", part_of_speech="noun", cefr_level="A1", category="food", example="Eat more vegetables.", example_bn="আরও সবজি খান।", synonyms=["greens"], antonyms=[]),
  dict(id="vocab:spicy", word="spicy", meaning_en="hot in taste from chilli", meaning_bn="ঝাল / মশলাদার", part_of_speech="adjective", cefr_level="A2", category="food", example="Bengali food can be spicy.", example_bn="বাঙালি খাবার ঝাল হতে পারে।", synonyms=["hot"], antonyms=["mild"]),

  # --- travel ---
  dict(id="vocab:passport", word="passport", meaning_en="an official document for foreign travel", meaning_bn="পাসপোর্ট", part_of_speech="noun", cefr_level="A2", category="travel", example="Keep your passport safe.", example_bn="পাসপোর্ট নিরাপদে রাখুন।", synonyms=[], antonyms=[]),
  dict(id="vocab:airport", word="airport", meaning_en="a place where planes take off and land", meaning_bn="বিমানবন্দর", part_of_speech="noun", cefr_level="A1", category="travel", example="We reached the airport early.", example_bn="আমরা তাড়াতাড়ি এয়ারপোর্টে পৌঁছালাম।", synonyms=[], antonyms=[]),
  dict(id="vocab:luggage", word="luggage", meaning_en="bags you take when travelling", meaning_bn="মালপত্র / লাগেজ", part_of_speech="noun", cefr_level="A2", category="travel", example="My luggage is heavy.", example_bn="আমার লাগেজ ভারী।", synonyms=["baggage", "bags"], antonyms=[]),
  dict(id="vocab:direction", word="direction", meaning_en="the way to go somewhere", meaning_bn="দিক / পথনির্দেশ", part_of_speech="noun", cefr_level="A2", category="travel", example="Can you give me directions?", example_bn="আমাকে পথ বলে দিতে পারবেন?", synonyms=["route", "way"], antonyms=[]),

  # --- health ---
  dict(id="vocab:doctor", word="doctor", meaning_en="a person who treats sick people", meaning_bn="ডাক্তার", part_of_speech="noun", cefr_level="A1", category="health", example="I need to see a doctor.", example_bn="আমাকে ডাক্তার দেখাতে হবে।", synonyms=["physician"], antonyms=[]),
  dict(id="vocab:hospital", word="hospital", meaning_en="a place where sick people are treated", meaning_bn="হাসপাতাল", part_of_speech="noun", cefr_level="A1", category="health", example="She works in a hospital.", example_bn="সে হাসপাতালে কাজ করে।", synonyms=["clinic"], antonyms=[]),
  dict(id="vocab:fever", word="fever", meaning_en="high body temperature from illness", meaning_bn="জ্বর", part_of_speech="noun", cefr_level="A2", category="health", example="He has a high fever.", example_bn="তার হাই ফিভার।", synonyms=[], antonyms=[]),
  dict(id="vocab:healthy", word="healthy", meaning_en="in good health", meaning_bn="সুস্থ / স্বাস্থ্যকর", part_of_speech="adjective", cefr_level="A1", category="health", example="Exercise keeps you healthy.", example_bn="ব্যায়াম আপনাকে সুস্থ রাখে।", synonyms=["fit", "well"], antonyms=["ill", "unhealthy"]),
  dict(id="vocab:exercise", word="exercise", meaning_en="physical activity to stay fit", meaning_bn="ব্যায়াম", part_of_speech="noun/verb", cefr_level="A2", category="health", example="I exercise every morning.", example_bn="আমি প্রতিদিন সকালে ব্যায়াম করি।", synonyms=["workout"], antonyms=[]),

  # --- education ---
  dict(id="vocab:student", word="student", meaning_en="a person who is learning", meaning_bn="শিক্ষার্থী / ছাত্র-ছাত্রী", part_of_speech="noun", cefr_level="A1", category="education", example="I am a student.", example_bn="আমি একজন শিক্ষার্থী।", synonyms=["learner", "pupil"], antonyms=[]),
  dict(id="vocab:teacher", word="teacher", meaning_en="a person who teaches", meaning_bn="শিক্ষক / শিক্ষিকা", part_of_speech="noun", cefr_level="A1", category="education", example="Our teacher is patient.", example_bn="আমাদের শিক্ষক ধৈর্যশীল।", synonyms=["tutor", "instructor"], antonyms=[]),
  dict(id="vocab:homework", word="homework", meaning_en="school work done at home", meaning_bn="হোমওয়ার্ক / বাড়ির কাজ", part_of_speech="noun", cefr_level="A1", category="education", example="I do my homework after dinner.", example_bn="ডিনারের পর আমি হোমওয়ার্ক করি।", synonyms=["assignment"], antonyms=[]),
  dict(id="vocab:exam", word="exam", meaning_en="a formal test of knowledge", meaning_bn="পরীক্ষা", part_of_speech="noun", cefr_level="A2", category="education", example="The exam is next week.", example_bn="পরের সপ্তাহে পরীক্ষা।", synonyms=["test"], antonyms=[]),
  dict(id="vocab:dictionary", word="dictionary", meaning_en="a book or app of word meanings", meaning_bn="অভিধান", part_of_speech="noun", cefr_level="A2", category="education", example="Look up the word in a dictionary.", example_bn="অভিধানে শব্দটা দেখো।", synonyms=["lexicon"], antonyms=[]),

  # --- core verbs (import verbs focus) ---
  dict(id="vocab:begin", word="begin", meaning_en="to start", meaning_bn="শুরু করা", part_of_speech="verb", cefr_level="A1", category="verbs", example="Let's begin the lesson.", example_bn="চলো লেসন শুরু করি।", synonyms=["start", "commence"], antonyms=["end", "finish"]),
  dict(id="vocab:finish", word="finish", meaning_en="to complete something", meaning_bn="শেষ করা", part_of_speech="verb", cefr_level="A1", category="verbs", example="I finished my work.", example_bn="আমি কাজ শেষ করেছি।", synonyms=["complete", "end"], antonyms=["begin", "start"]),
  dict(id="vocab:choose", word="choose", meaning_en="to pick one option", meaning_bn="বাছাই করা / বেছে নেওয়া", part_of_speech="verb", cefr_level="A1", category="verbs", example="Choose the correct answer.", example_bn="সঠিক উত্তর বেছে নাও।", synonyms=["select", "pick"], antonyms=[]),
  dict(id="vocab:decide", word="decide", meaning_en="to choose after thinking", meaning_bn="সিদ্ধান্ত নেওয়া", part_of_speech="verb", cefr_level="A2", category="verbs", example="We decided to stay home.", example_bn="আমরা বাড়িতে থাকার সিদ্ধান্ত নিলাম।", synonyms=["determine"], antonyms=["hesitate"]),
  dict(id="vocab:prefer", word="prefer", meaning_en="to like one thing more than another", meaning_bn="বেশি পছন্দ করা", part_of_speech="verb", cefr_level="A2", category="verbs", example="I prefer tea to coffee.", example_bn="কফির চেয়ে চা বেশি পছন্দ করি।", synonyms=["favour"], antonyms=[]),
  dict(id="vocab:suggest", word="suggest", meaning_en="to offer an idea", meaning_bn="পরামর্শ দেওয়া / প্রস্তাব করা", part_of_speech="verb", cefr_level="A2", category="verbs", example="I suggest we leave early.", example_bn="আমি পরামর্শ দিই আমরা তাড়াতাড়ি যাই।", synonyms=["recommend", "propose"], antonyms=[]),
  dict(id="vocab:accept", word="accept", meaning_en="to say yes to an offer", meaning_bn="গ্রহণ করা", part_of_speech="verb", cefr_level="A2", category="verbs", example="She accepted the job offer.", example_bn="সে চাকরির অফার গ্রহণ করেছে।", synonyms=["agree to"], antonyms=["reject", "refuse"]),
  dict(id="vocab:refuse", word="refuse", meaning_en="to say no", meaning_bn="প্রত্যাখ্যান করা / না বলা", part_of_speech="verb", cefr_level="A2", category="verbs", example="He refused to help.", example_bn="সে সাহায্য করতে রাজি হয়নি।", synonyms=["decline", "reject"], antonyms=["accept"]),
  dict(id="vocab:compare", word="compare", meaning_en="to look at similarities and differences", meaning_bn="তুলনা করা", part_of_speech="verb", cefr_level="B1", category="verbs", example="Compare these two sentences.", example_bn="এই দুই বাক্য তুলনা করো।", synonyms=["contrast"], antonyms=[]),
  dict(id="vocab:describe", word="describe", meaning_en="to say what something is like", meaning_bn="বর্ণনা করা", part_of_speech="verb", cefr_level="A2", category="verbs", example="Describe your hometown.", example_bn="তোমার শহরের বর্ণনা দাও।", synonyms=["explain", "portray"], antonyms=[]),
  dict(id="vocab:prepare", word="prepare", meaning_en="to get ready", meaning_bn="প্রস্তুত করা / তৈরি হওয়া", part_of_speech="verb", cefr_level="A2", category="verbs", example="Prepare for the interview.", example_bn="ইন্টারভিউয়ের জন্য প্রস্তুত হও।", synonyms=["ready", "arrange"], antonyms=[]),
  dict(id="vocab:solve", word="solve", meaning_en="to find an answer to a problem", meaning_bn="সমাধান করা", part_of_speech="verb", cefr_level="A2", category="verbs", example="Can you solve this problem?", example_bn="এই সমস্যা সমাধান করতে পারবে?", synonyms=["resolve", "fix"], antonyms=[]),
  dict(id="vocab:notice", word="notice", meaning_en="to see or become aware of something", meaning_bn="লক্ষ্য করা", part_of_speech="verb", cefr_level="A2", category="verbs", example="Did you notice the sign?", example_bn="সাইনবোর্ডটা লক্ষ্য করেছ?", synonyms=["observe", "spot"], antonyms=["ignore"]),
  dict(id="vocab:avoid", word="avoid", meaning_en="to stay away from something", meaning_bn="এড়িয়ে চলা", part_of_speech="verb", cefr_level="B1", category="verbs", example="Avoid junk food.", example_bn="জাঙ্ক ফুড এড়িয়ে চলো।", synonyms=["keep away from"], antonyms=["face", "seek"]),

  # --- shopping / daily extras ---
  dict(id="vocab:price", word="price", meaning_en="how much something costs", meaning_bn="দাম / মূল্য", part_of_speech="noun", cefr_level="A1", category="shopping", example="What is the price of this shirt?", example_bn="এই শার্টের দাম কত?", synonyms=["cost", "rate"], antonyms=[]),
  dict(id="vocab:cheap", word="cheap", meaning_en="low in price", meaning_bn="সস্তা", part_of_speech="adjective", cefr_level="A1", category="shopping", example="These shoes are cheap.", example_bn="এই জুতোগুলো সস্তা।", synonyms=["inexpensive"], antonyms=["expensive"]),
  dict(id="vocab:expensive", word="expensive", meaning_en="costing a lot of money", meaning_bn="দামি / ব্যয়বহুল", part_of_speech="adjective", cefr_level="A1", category="shopping", example="That phone is expensive.", example_bn="ওই ফোনটা দামি।", synonyms=["costly"], antonyms=["cheap"]),
  dict(id="vocab:customer", word="customer", meaning_en="a person who buys something", meaning_bn="ক্রেতা / কাস্টমার", part_of_speech="noun", cefr_level="A2", category="shopping", example="The customer asked for a receipt.", example_bn="কাস্টমার রসিদ চেয়েছে।", synonyms=["buyer", "client"], antonyms=["seller"]),
  dict(id="vocab:discount", word="discount", meaning_en="a reduction in price", meaning_bn="ছাড় / ডিসকাউন্ট", part_of_speech="noun", cefr_level="A2", category="shopping", example="There is a 20% discount today.", example_bn="আজ ২০% ছাড় আছে।", synonyms=["reduction", "offer"], antonyms=[]),

  # --- technology ---
  dict(id="vocab:password", word="password", meaning_en="a secret word to open an account", meaning_bn="পাসওয়ার্ড", part_of_speech="noun", cefr_level="A2", category="technology", example="Never share your password.", example_bn="পাসওয়ার্ড কখনো শেয়ার করো না।", synonyms=["passcode"], antonyms=[]),
  dict(id="vocab:download", word="download", meaning_en="to copy a file from the internet to your device", meaning_bn="ডাউনলোড করা", part_of_speech="verb/noun", cefr_level="A2", category="technology", example="Download the app first.", example_bn="আগে অ্যাপটা ডাউনলোড করো।", synonyms=[], antonyms=["upload"]),
  dict(id="vocab:upload", word="upload", meaning_en="to send a file from your device to the internet", meaning_bn="আপলোড করা", part_of_speech="verb/noun", cefr_level="A2", category="technology", example="Upload your photo here.", example_bn="এখানে তোমার ছবি আপলোড করো।", synonyms=[], antonyms=["download"]),
  dict(id="vocab:website", word="website", meaning_en="a set of pages on the internet", meaning_bn="ওয়েবসাইট", part_of_speech="noun", cefr_level="A2", category="technology", example="Visit our website for lessons.", example_bn="লেসনের জন্য আমাদের ওয়েবসাইট দেখুন।", synonyms=["site", "webpage"], antonyms=[]),
]

CATEGORIES = [
  ("all", "All", "সব"),
  ("home", "Home", "বাড়ি"),
  ("office", "Office", "অফিস"),
  ("outdoor", "Outdoor", "বাইরে"),
  ("nature", "Nature", "প্রকৃতি"),
  ("food", "Food", "খাবার"),
  ("travel", "Travel", "ভ্রমণ"),
  ("health", "Health", "স্বাস্থ্য"),
  ("education", "Education", "শিক্ষা"),
  ("verbs", "Import Verbs", "গুরুত্বপূর্ণ ক্রিয়া"),
  ("shopping", "Shopping", "কেনাকাটা"),
  ("technology", "Technology", "প্রযুক্তি"),
  ("daily", "Daily", "দৈনন্দিন"),
]

def by_cat(*cats):
  return [w["id"] for w in WORDS if w["category"] in cats]

def by_ids(*ids):
  return list(ids)

LISTS = [
  {
    "id": "target-a1-core",
    "title": "A1 Core Target",
    "title_bn": "A1 মূল টার্গেট লিস্ট",
    "description": "Survival words every beginner should know first.",
    "description_bn": "শুরুতেই জানা দরকার এমন প্রয়োজনীয় শব্দ।",
    "word_ids": [w["id"] for w in WORDS if w["cefr_level"] == "A1"][:40],
  },
  {
    "id": "import-verbs",
    "title": "Important Verbs",
    "title_bn": "গুরুত্বপূর্ণ ক্রিয়াপদ",
    "description": "High-frequency action verbs for speaking and writing.",
    "description_bn": "কথা ও লেখার জন্য জরুরি action verbs।",
    "word_ids": by_cat("verbs"),
  },
  {
    "id": "office-vocab",
    "title": "Office Vocabulary",
    "title_bn": "অফিস ভোকাবুলারি",
    "description": "Meetings, email, deadlines, colleagues.",
    "description_bn": "মিটিং, ইমেইল, ডেডলাইন, সহকর্মী।",
    "word_ids": by_cat("office"),
  },
  {
    "id": "home-vocab",
    "title": "Home Vocabulary",
    "title_bn": "বাড়ির শব্দ",
    "description": "Rooms, cleaning, neighbours, rent.",
    "description_bn": "ঘর, পরিষ্কার, প্রতিবেশী, ভাড়া।",
    "word_ids": by_cat("home"),
  },
  {
    "id": "outdoor-nature",
    "title": "Outdoor & Nature",
    "title_bn": "বাইরে ও প্রকৃতি",
    "description": "Park, traffic, weather, river, pollution.",
    "description_bn": "পার্ক, ট্রাফিক, আবহাওয়া, নদী, দূষণ।",
    "word_ids": by_cat("outdoor", "nature"),
  },
  {
    "id": "food-health",
    "title": "Food & Health",
    "title_bn": "খাবার ও স্বাস্থ্য",
    "description": "Meals, taste, doctor, exercise.",
    "description_bn": "খাবার, স্বাদ, ডাক্তার, ব্যায়াম।",
    "word_ids": by_cat("food", "health"),
  },
  {
    "id": "travel-shopping",
    "title": "Travel & Shopping",
    "title_bn": "ভ্রমণ ও কেনাকাটা",
    "description": "Tickets, airport, price, discount.",
    "description_bn": "টিকিট, এয়ারপোর্ট, দাম, ছাড়।",
    "word_ids": by_cat("travel", "shopping"),
  },
  {
    "id": "opposites-pack",
    "title": "Opposites Pack",
    "title_bn": "বিপরীত শব্দ প্যাক",
    "description": "Words that come with useful antonyms.",
    "description_bn": "যেসব শব্দের সাথে antonym শেখা সহজ।",
    "word_ids": [w["id"] for w in WORDS if w.get("antonyms")],
  },
]

# ensure unique ids
ids = [w["id"] for w in WORDS]
assert len(ids) == len(set(ids)), "duplicate ids"

(DATA / "vocabulary.json").write_text(
  json.dumps(WORDS, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
(DATA / "vocabulary-lists.json").write_text(
  json.dumps({"categories": [{"id": a, "label": b, "label_bn": c} for a,b,c in CATEGORIES], "lists": LISTS}, ensure_ascii=False, indent=2) + "\n",
  encoding="utf-8",
)
print("words", len(WORDS))
print("lists", len(LISTS))
for L in LISTS:
  print(" ", L["id"], len(L["word_ids"]))
