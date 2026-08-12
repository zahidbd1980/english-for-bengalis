# -*- coding: utf-8 -*-
import json
from pathlib import Path

vp = Path(__file__).resolve().parents[1] / "data" / "vocabulary.json"
vocab = json.loads(vp.read_text(encoding="utf-8"))
have = {v["word"].lower() for v in vocab}
extra = [
  {"id":"v301","word":"patient","phonetic":"/ˈpeɪʃnt/","pos":"adj/noun","cefr":"A2","meaning_en":"able to wait calmly / sick person","meaning_bn":"ধৈর্যশীল / রোগী","example":"Be patient.","example_bn":"ধৈর্য ধরুন।","tags":["health"],"synonyms":[],"antonyms":["impatient"]},
  {"id":"v302","word":"nervous","phonetic":"/ˈnɜːvəs/","pos":"adj","cefr":"A2","meaning_en":"worried or anxious","meaning_bn":"নার্ভাস / উদ্বিগ্ন","example":"I feel nervous before exams.","example_bn":"পরীক্ষার আগে নার্ভাস লাগে।","tags":["daily"],"synonyms":["anxious"],"antonyms":["calm"]},
  {"id":"v303","word":"confident","phonetic":"/ˈkɒnfɪdənt/","pos":"adj","cefr":"B1","meaning_en":"sure of yourself","meaning_bn":"আত্মবিশ্বাসী","example":"She is confident.","example_bn":"সে আত্মবিশ্বাসী।","tags":["daily"],"synonyms":["sure"],"antonyms":["insecure"],"word_family":[{"form":"confidence","pos":"noun","bn":"আত্মবিশ্বাস"}]},
  {"id":"v304","word":"curious","phonetic":"/ˈkjʊəriəs/","pos":"adj","cefr":"B1","meaning_en":"wanting to know more","meaning_bn":"কৌতূহলী","example":"Children are curious.","example_bn":"শিশুরা কৌতূহলী।","tags":["daily"],"synonyms":["inquisitive"],"antonyms":[]},
  {"id":"v305","word":"honest","phonetic":"/ˈɒnɪst/","pos":"adj","cefr":"A2","meaning_en":"truthful","meaning_bn":"সৎ","example":"Be honest with me.","example_bn":"আমার সাথে সৎ থাকুন।","tags":["daily"],"synonyms":["truthful"],"antonyms":["dishonest"],"word_family":[{"form":"honesty","pos":"noun","bn":"সততা"}]},
  {"id":"v306","word":"polite","phonetic":"/pəˈlaɪt/","pos":"adj","cefr":"A2","meaning_en":"having good manners","meaning_bn":"ভদ্র","example":"Please be polite.","example_bn":"দয়া করে ভদ্র থাকুন।","tags":["daily"],"synonyms":["courteous"],"antonyms":["rude"]},
  {"id":"v307","word":"rude","phonetic":"/ruːd/","pos":"adj","cefr":"A2","meaning_en":"not polite","meaning_bn":"অভদ্র","example":"That comment was rude.","example_bn":"সেই মন্তব্য অভদ্র ছিল।","tags":["daily"],"synonyms":["impolite"],"antonyms":["polite"]},
  {"id":"v308","word":"brave","phonetic":"/breɪv/","pos":"adj","cefr":"A2","meaning_en":"ready to face danger","meaning_bn":"সাহসী","example":"Firefighters are brave.","example_bn":"ফায়ারফাইটাররা সাহসী।","tags":["daily"],"synonyms":["courageous"],"antonyms":["cowardly"]},
  {"id":"v309","word":"clever","phonetic":"/ˈklevər/","pos":"adj","cefr":"A2","meaning_en":"intelligent","meaning_bn":"চতুর / বুদ্ধিমান","example":"That was a clever idea.","example_bn":"সেটি চতুর ধারণা ছিল।","tags":["daily"],"synonyms":["smart"],"antonyms":["stupid"]},
  {"id":"v310","word":"lazy","phonetic":"/ˈleɪzi/","pos":"adj","cefr":"A2","meaning_en":"not willing to work","meaning_bn":"অলস","example":"Don't be lazy.","example_bn":"অলস হয়ো না।","tags":["daily"],"synonyms":[],"antonyms":["hardworking"]},
  {"id":"v311","word":"careful","phonetic":"/ˈkeəfl/","pos":"adj","cefr":"A2","meaning_en":"paying attention to avoid mistakes","meaning_bn":"সাবধান","example":"Be careful crossing the road.","example_bn":"রাস্তা পার হওয়ার সময় সাবধান।","tags":["daily"],"synonyms":["cautious"],"antonyms":["careless"]},
  {"id":"v312","word":"careless","phonetic":"/ˈkeələs/","pos":"adj","cefr":"A2","meaning_en":"not careful","meaning_bn":"অসাবধান","example":"A careless mistake.","example_bn":"একটি অসাবধান ভুল।","tags":["daily"],"synonyms":["sloppy"],"antonyms":["careful"]},
  {"id":"v313","word":"useful","phonetic":"/ˈjuːsfl/","pos":"adj","cefr":"A1","meaning_en":"helpful","meaning_bn":"দরকারি","example":"This app is useful.","example_bn":"এই অ্যাপ দরকারি।","tags":["daily"],"synonyms":["helpful"],"antonyms":["useless"]},
  {"id":"v314","word":"useless","phonetic":"/ˈjuːsləs/","pos":"adj","cefr":"A2","meaning_en":"not useful","meaning_bn":"অকেজো","example":"The broken phone is useless.","example_bn":"ভাঙা ফোন অকেজো।","tags":["daily"],"synonyms":[],"antonyms":["useful"]},
  {"id":"v315","word":"possible","phonetic":"/ˈpɒsəbl/","pos":"adj","cefr":"A2","meaning_en":"able to be done","meaning_bn":"সম্ভব","example":"Is it possible?","example_bn":"এটা সম্ভব কি?","tags":["daily"],"synonyms":["feasible"],"antonyms":["impossible"],"word_family":[{"form":"possibility","pos":"noun","bn":"সম্ভাবনা"}]},
  {"id":"v316","word":"impossible","phonetic":"/ɪmˈpɒsəbl/","pos":"adj","cefr":"A2","meaning_en":"not possible","meaning_bn":"অসম্ভব","example":"Nothing is impossible.","example_bn":"কিছুই অসম্ভব নয়।","tags":["daily"],"synonyms":[],"antonyms":["possible"]},
  {"id":"v317","word":"necessary","phonetic":"/ˈnesəsəri/","pos":"adj","cefr":"A2","meaning_en":"needed","meaning_bn":"প্রয়োজনীয়","example":"Sleep is necessary.","example_bn":"ঘুম প্রয়োজনীয়।","tags":["daily"],"synonyms":["needed"],"antonyms":["unnecessary"]},
  {"id":"v318","word":"popular","phonetic":"/ˈpɒpjələr/","pos":"adj","cefr":"A2","meaning_en":"liked by many people","meaning_bn":"জনপ্রিয়","example":"This song is popular.","example_bn":"এই গান জনপ্রিয়।","tags":["daily"],"synonyms":["well-known"],"antonyms":["unpopular"]},
  {"id":"v319","word":"modern","phonetic":"/ˈmɒdn/","pos":"adj","cefr":"A2","meaning_en":"of the present time","meaning_bn":"আধুনিক","example":"Modern technology helps us.","example_bn":"আধুনিক প্রযুক্তি সাহায্য করে।","tags":["academic"],"synonyms":["contemporary"],"antonyms":["old-fashioned"]},
  {"id":"v320","word":"traditional","phonetic":"/trəˈdɪʃənl/","pos":"adj","cefr":"B1","meaning_en":"following old customs","meaning_bn":"ঐতিহ্যবাহী","example":"Traditional food is tasty.","example_bn":"ঐতিহ্যবাহী খাবার সুস্বাদু।","tags":["culture"],"synonyms":["customary"],"antonyms":["modern"],"word_family":[{"form":"tradition","pos":"noun","bn":"ঐতিহ্য"}]},
  {"id":"v321","word":"foreign","phonetic":"/ˈfɒrən/","pos":"adj","cefr":"A2","meaning_en":"from another country","meaning_bn":"বিদেশি","example":"He speaks a foreign language.","example_bn":"সে একটি বিদেশি ভাষা বলে।","tags":["daily"],"synonyms":[],"antonyms":["local"]},
  {"id":"v322","word":"local","phonetic":"/ˈləʊkl/","pos":"adj/noun","cefr":"A2","meaning_en":"from this area","meaning_bn":"স্থানীয়","example":"Buy local products.","example_bn":"স্থানীয় পণ্য কিনুন।","tags":["daily"],"synonyms":[],"antonyms":["foreign"]},
  {"id":"v323","word":"public","phonetic":"/ˈpʌblɪk/","pos":"adj/noun","cefr":"A2","meaning_en":"for everyone","meaning_bn":"প্রকাশ্য / জনসাধারণ","example":"Public transport is cheap.","example_bn":"পাবলিক ট্রান্সপোর্ট সস্তা।","tags":["daily"],"synonyms":[],"antonyms":["private"]},
  {"id":"v324","word":"private","phonetic":"/ˈpraɪvət/","pos":"adj","cefr":"A2","meaning_en":"for one person or group only","meaning_bn":"ব্যক্তিগত","example":"This is a private message.","example_bn":"এটি ব্যক্তিগত বার্তা।","tags":["daily"],"synonyms":[],"antonyms":["public"]},
  {"id":"v325","word":"similar","phonetic":"/ˈsɪmələr/","pos":"adj","cefr":"A2","meaning_en":"almost the same","meaning_bn":"অনুরূপ","example":"The two words are similar.","example_bn":"দুটি শব্দ অনুরূপ।","tags":["academic"],"synonyms":["alike"],"antonyms":["different"]},
  {"id":"v326","word":"different","phonetic":"/ˈdɪfrənt/","pos":"adj","cefr":"A1","meaning_en":"not the same","meaning_bn":"আলাদা","example":"We have different opinions.","example_bn":"আমাদের আলাদা মতামত।","tags":["daily"],"synonyms":["distinct"],"antonyms":["same","similar"]},
]
added = 0
for w in extra:
    if w["word"].lower() in have:
        continue
    w.setdefault("synonyms", [])
    w.setdefault("antonyms", [])
    w.setdefault("tags", [])
    vocab.append(w)
    have.add(w["word"].lower())
    added += 1
vp.write_text(json.dumps(vocab, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("added", added, "total", len(vocab))
