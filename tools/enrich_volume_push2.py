# -*- coding: utf-8 -*-
"""Second volume push: vocab ~300, spoken ~100 lines."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MORE = [
  {"id":"v225","word":"accept","phonetic":"/əkˈsept/","pos":"verb","cefr":"A2","meaning_en":"to take something offered","meaning_bn":"গ্রহণ করা","example":"I accept your invitation.","example_bn":"আমি আপনার আমন্ত্রণ গ্রহণ করি।","tags":["daily"],"synonyms":["receive"],"antonyms":["refuse"],"word_family":[{"form":"acceptance","pos":"noun","bn":"গ্রহণ"},{"form":"acceptable","pos":"adj","bn":"গ্রহণযোগ্য"}]},
  {"id":"v226","word":"refuse","phonetic":"/rɪˈfjuːz/","pos":"verb","cefr":"A2","meaning_en":"to say no","meaning_bn":"প্রত্যাখ্যান করা","example":"She refused the offer.","example_bn":"সে অফার প্রত্যাখ্যান করেছে।","tags":["daily"],"synonyms":["decline"],"antonyms":["accept"]},
  {"id":"v227","word":"agree","phonetic":"/əˈɡriː/","pos":"verb","cefr":"A1","meaning_en":"to have the same opinion","meaning_bn":"একমত হওয়া","example":"I agree with you.","example_bn":"আমি আপনার সাথে একমত।","tags":["daily"],"synonyms":["consent"],"antonyms":["disagree"],"word_family":[{"form":"agreement","pos":"noun","bn":"চুক্তি/মতৈক্য"},{"form":"disagree","pos":"verb","bn":"অসম্মত হওয়া"}]},
  {"id":"v228","word":"decide","phonetic":"/dɪˈsaɪd/","pos":"verb","cefr":"A2","meaning_en":"to choose after thinking","meaning_bn":"সিদ্ধান্ত নেওয়া","example":"We decided to stay.","example_bn":"আমরা থাকার সিদ্ধান্ত নিয়েছি।","tags":["daily"],"synonyms":["choose"],"antonyms":[],"word_family":[{"form":"decision","pos":"noun","bn":"সিদ্ধান্ত"},{"form":"decisive","pos":"adj","bn":"দৃঢ়সংকল্প"}]},
  {"id":"v229","word":"prefer","phonetic":"/prɪˈfɜːr/","pos":"verb","cefr":"A2","meaning_en":"to like more","meaning_bn":"পছন্দ করা (তুলনায়)","example":"I prefer tea to coffee.","example_bn":"কফির চেয়ে চা পছন্দ করি।","tags":["daily"],"synonyms":["favor"],"antonyms":[],"word_family":[{"form":"preference","pos":"noun","bn":"পছন্দ"}]},
  {"id":"v230","word":"suggest","phonetic":"/səˈdʒest/","pos":"verb","cefr":"A2","meaning_en":"to put forward an idea","meaning_bn":"পরামর্শ দেওয়া","example":"I suggest we leave early.","example_bn":"আমি পরামর্শ দিই আমরা তাড়াতাড়ি যাই।","tags":["daily"],"synonyms":["recommend"],"antonyms":[],"word_family":[{"form":"suggestion","pos":"noun","bn":"পরামর্শ"}]},
  {"id":"v231","word":"explain","phonetic":"/ɪkˈspleɪn/","pos":"verb","cefr":"A2","meaning_en":"to make clear","meaning_bn":"ব্যাখ্যা করা","example":"Can you explain this?","example_bn":"এটা ব্যাখ্যা করতে পারবেন?","tags":["study"],"synonyms":["clarify"],"antonyms":[],"word_family":[{"form":"explanation","pos":"noun","bn":"ব্যাখ্যা"}]},
  {"id":"v232","word":"describe","phonetic":"/dɪˈskraɪb/","pos":"verb","cefr":"A2","meaning_en":"to say what something is like","meaning_bn":"বর্ণনা করা","example":"Describe your city.","example_bn":"আপনার শহর বর্ণনা করুন।","tags":["study"],"synonyms":["portray"],"antonyms":[],"word_family":[{"form":"description","pos":"noun","bn":"বর্ণনা"}]},
  {"id":"v233","word":"discuss","phonetic":"/dɪˈskʌs/","pos":"verb","cefr":"A2","meaning_en":"to talk about something","meaning_bn":"আলোচনা করা","example":"We discussed the plan.","example_bn":"আমরা পরিকল্পনা নিয়ে আলোচনা করেছি।","tags":["work"],"synonyms":["talk over"],"antonyms":[],"word_family":[{"form":"discussion","pos":"noun","bn":"আলোচনা"}]},
  {"id":"v234","word":"mention","phonetic":"/ˈmenʃn/","pos":"verb","cefr":"A2","meaning_en":"to speak about briefly","meaning_bn":"উল্লেখ করা","example":"He mentioned your name.","example_bn":"সে আপনার নাম উল্লেখ করেছে।","tags":["daily"],"synonyms":["refer to"],"antonyms":[]},
  {"id":"v235","word":"promise","phonetic":"/ˈprɒmɪs/","pos":"verb/noun","cefr":"A2","meaning_en":"to say you will do something","meaning_bn":"প্রতিশ্রুতি / প্রতিশ্রুতি দেওয়া","example":"I promise to help.","example_bn":"আমি সাহায্য করার প্রতিশ্রুতি দিচ্ছি।","tags":["daily"],"synonyms":["vow"],"antonyms":[]},
  {"id":"v236","word":"allow","phonetic":"/əˈlaʊ/","pos":"verb","cefr":"A2","meaning_en":"to let someone do something","meaning_bn":"অনুমতি দেওয়া","example":"Parents allow children to play.","example_bn":"বাবা-মা শিশুদের খেলতে অনুমতি দেন।","tags":["daily"],"synonyms":["permit"],"antonyms":["forbid"],"word_family":[{"form":"permission","pos":"noun","bn":"অনুমতি"}]},
  {"id":"v237","word":"forbid","phonetic":"/fəˈbɪd/","pos":"verb","cefr":"B1","meaning_en":"to not allow","meaning_bn":"নিষেধ করা","example":"Smoking is forbidden here.","example_bn":"এখানে ধূমপান নিষিদ্ধ।","tags":["formal"],"synonyms":["ban"],"antonyms":["allow"]},
  {"id":"v238","word":"encourage","phonetic":"/ɪnˈkʌrɪdʒ/","pos":"verb","cefr":"B1","meaning_en":"to give support or confidence","meaning_bn":"উৎসাহ দেওয়া","example":"Teachers encourage students.","example_bn":"শিক্ষকরা শিক্ষার্থীদের উৎসাহ দেন।","tags":["study"],"synonyms":["motivate"],"antonyms":["discourage"],"word_family":[{"form":"encouragement","pos":"noun","bn":"উৎসাহ"}]},
  {"id":"v239","word":"improve","phonetic":"/ɪmˈpruːv/","pos":"verb","cefr":"A2","meaning_en":"to get better","meaning_bn":"উন্নতি করা","example":"Your English is improving.","example_bn":"আপনার ইংরেজি উন্নতি করছে।","tags":["study"],"synonyms":["get better"],"antonyms":["worsen"],"word_family":[{"form":"improvement","pos":"noun","bn":"উন্নতি"}]},
  {"id":"v240","word":"develop","phonetic":"/dɪˈveləp/","pos":"verb","cefr":"B1","meaning_en":"to grow or create","meaning_bn":"বিকাশ করা","example":"Cities develop quickly.","example_bn":"শহরগুলো দ্রুত বিকাশ লাভ করে।","tags":["academic"],"synonyms":["grow"],"antonyms":[],"word_family":[{"form":"development","pos":"noun","bn":"উন্নয়ন"}]},
  {"id":"v241","word":"increase","phonetic":"/ɪnˈkriːs/","pos":"verb/noun","cefr":"A2","meaning_en":"to become larger","meaning_bn":"বৃদ্ধি পাওয়া / বৃদ্ধি","example":"Prices increased.","example_bn":"দাম বেড়েছে।","tags":["academic"],"synonyms":["rise"],"antonyms":["decrease"]},
  {"id":"v242","word":"decrease","phonetic":"/dɪˈkriːs/","pos":"verb/noun","cefr":"B1","meaning_en":"to become smaller","meaning_bn":"কমে যাওয়া / হ্রাস","example":"The number decreased.","example_bn":"সংখ্যা কমেছে।","tags":["academic"],"synonyms":["reduce"],"antonyms":["increase"]},
  {"id":"v243","word":"reduce","phonetic":"/rɪˈdjuːs/","pos":"verb","cefr":"B1","meaning_en":"to make smaller","meaning_bn":"কমানো","example":"We should reduce waste.","example_bn":"আমাদের বর্জ্য কমানো উচিত।","tags":["academic"],"synonyms":["lower"],"antonyms":["increase"],"word_family":[{"form":"reduction","pos":"noun","bn":"হ্রাস"}]},
  {"id":"v244","word":"include","phonetic":"/ɪnˈkluːd/","pos":"verb","cefr":"A2","meaning_en":"to contain as part","meaning_bn":"অন্তর্ভুক্ত করা","example":"The price includes tax.","example_bn":"দামে ট্যাক্স অন্তর্ভুক্ত।","tags":["daily"],"synonyms":["contain"],"antonyms":["exclude"],"word_family":[{"form":"including","pos":"prep","bn":"সহ"}]},
  {"id":"v245","word":"exclude","phonetic":"/ɪkˈskluːd/","pos":"verb","cefr":"B1","meaning_en":"to leave out","meaning_bn":"বাদ দেওয়া","example":"Do not exclude anyone.","example_bn":"কাউকে বাদ দিবেন না।","tags":["formal"],"synonyms":["omit"],"antonyms":["include"]},
  {"id":"v246","word":"provide","phonetic":"/prəˈvaɪd/","pos":"verb","cefr":"B1","meaning_en":"to give something needed","meaning_bn":"সরবরাহ করা","example":"The school provides books.","example_bn":"স্কুল বই সরবরাহ করে।","tags":["work"],"synonyms":["supply"],"antonyms":[],"word_family":[{"form":"provider","pos":"noun","bn":"সরবরাহকারী"}]},
  {"id":"v247","word":"require","phonetic":"/rɪˈkwaɪər/","pos":"verb","cefr":"B1","meaning_en":"to need","meaning_bn":"প্রয়োজন হওয়া","example":"This job requires experience.","example_bn":"এই চাকরিতে অভিজ্ঞতা প্রয়োজন।","tags":["work"],"synonyms":["need"],"antonyms":[],"word_family":[{"form":"requirement","pos":"noun","bn":"প্রয়োজনীয়তা"}]},
  {"id":"v248","word":"consider","phonetic":"/kənˈsɪdər/","pos":"verb","cefr":"B1","meaning_en":"to think carefully about","meaning_bn":"বিবেচনা করা","example":"Consider all options.","example_bn":"সব অপশন বিবেচনা করুন।","tags":["academic"],"synonyms":["think about"],"antonyms":[],"word_family":[{"form":"consideration","pos":"noun","bn":"বিবেচনা"}]},
  {"id":"v249","word":"expect","phonetic":"/ɪkˈspekt/","pos":"verb","cefr":"A2","meaning_en":"to think something will happen","meaning_bn":"আশা করা / প্রত্যাশা করা","example":"I expect good news.","example_bn":"আমি ভালো খবর আশা করি।","tags":["daily"],"synonyms":["anticipate"],"antonyms":[],"word_family":[{"form":"expectation","pos":"noun","bn":"প্রত্যাশা"}]},
  {"id":"v250","word":"realize","phonetic":"/ˈrɪəlaɪz/","pos":"verb","cefr":"B1","meaning_en":"to understand clearly","meaning_bn":"উপলব্ধি করা","example":"I realized my mistake.","example_bn":"আমি আমার ভুল উপলব্ধি করেছি।","tags":["daily"],"synonyms":["understand"],"antonyms":[],"word_family":[{"form":"realization","pos":"noun","bn":"উপলব্ধি"}]},
  {"id":"v251","word":"recognize","phonetic":"/ˈrekəɡnaɪz/","pos":"verb","cefr":"B1","meaning_en":"to know someone or something again","meaning_bn":"চেনা / স্বীকৃতি দেওয়া","example":"I recognized her voice.","example_bn":"আমি তার কণ্ঠ চেনেছি।","tags":["daily"],"synonyms":["identify"],"antonyms":[],"word_family":[{"form":"recognition","pos":"noun","bn":"স্বীকৃতি"}]},
  {"id":"v252","word":"remember","phonetic":"/rɪˈmembər/","pos":"verb","cefr":"A1","meaning_en":"to keep in mind","meaning_bn":"মনে রাখা","example":"I remember your name.","example_bn":"আমি আপনার নাম মনে রাখি।","tags":["daily"],"synonyms":["recall"],"antonyms":["forget"]},
  {"id":"v253","word":"forget","phonetic":"/fərˈɡet/","pos":"verb","cefr":"A1","meaning_en":"to not remember","meaning_bn":"ভুলে যাওয়া","example":"Don't forget your keys.","example_bn":"চাবি ভুলবেন না।","tags":["daily"],"synonyms":[],"antonyms":["remember"]},
  {"id":"v254","word":"imagine","phonetic":"/ɪˈmædʒɪn/","pos":"verb","cefr":"A2","meaning_en":"to form a picture in the mind","meaning_bn":"কল্পনা করা","example":"Imagine a better future.","example_bn":"একটি ভালো ভবিষ্যৎ কল্পনা করুন।","tags":["daily"],"synonyms":["picture"],"antonyms":[],"word_family":[{"form":"imagination","pos":"noun","bn":"কল্পনা"}]},
  {"id":"v255","word":"notice","phonetic":"/ˈnəʊtɪs/","pos":"verb/noun","cefr":"A2","meaning_en":"to see or become aware","meaning_bn":"লক্ষ্য করা / নোটিশ","example":"Did you notice the sign?","example_bn":"আপনি সাইন লক্ষ্য করেছেন?","tags":["daily"],"synonyms":["observe"],"antonyms":[]},
  {"id":"v256","word":"appear","phonetic":"/əˈpɪər/","pos":"verb","cefr":"A2","meaning_en":"to become visible / seem","meaning_bn":"দেখা যাওয়া / মনে হওয়া","example":"He appeared suddenly.","example_bn":"সে হঠাৎ দেখা দিল।","tags":["daily"],"synonyms":["seem"],"antonyms":["disappear"],"word_family":[{"form":"appearance","pos":"noun","bn":"চেহারা/উপস্থিতি"}]},
  {"id":"v257","word":"disappear","phonetic":"/ˌdɪsəˈpɪər/","pos":"verb","cefr":"A2","meaning_en":"to go out of sight","meaning_bn":"অদৃশ্য হয়ে যাওয়া","example":"The sun disappeared.","example_bn":"সূর্য অদৃশ্য হয়ে গেল।","tags":["daily"],"synonyms":["vanish"],"antonyms":["appear"]},
  {"id":"v258","word":"remain","phonetic":"/rɪˈmeɪn/","pos":"verb","cefr":"B1","meaning_en":"to stay","meaning_bn":"থাকা / অবশিষ্ট থাকা","example":"Please remain seated.","example_bn":"দয়া করে বসে থাকুন।","tags":["formal"],"synonyms":["stay"],"antonyms":[]},
  {"id":"v259","word":"continue","phonetic":"/kənˈtɪnjuː/","pos":"verb","cefr":"A2","meaning_en":"to keep doing","meaning_bn":"চালিয়ে যাওয়া","example":"Please continue.","example_bn":"দয়া করে চালিয়ে যান।","tags":["daily"],"synonyms":["keep on"],"antonyms":["stop"],"word_family":[{"form":"continuous","pos":"adj","bn":"অবিচ্ছিন্ন"}]},
  {"id":"v260","word":"complete","phonetic":"/kəmˈpliːt/","pos":"verb/adj","cefr":"A2","meaning_en":"to finish / whole","meaning_bn":"সম্পূর্ণ করা / সম্পূর্ণ","example":"Complete the form.","example_bn":"ফর্মটি পূরণ করুন।","tags":["daily"],"synonyms":["finish"],"antonyms":["incomplete"],"word_family":[{"form":"completion","pos":"noun","bn":"সম্পন্নতা"}]},
  {"id":"v261","word":"achieve","phonetic":"/əˈtʃiːv/","pos":"verb","cefr":"B1","meaning_en":"to succeed in doing","meaning_bn":"অর্জন করা","example":"She achieved her goal.","example_bn":"সে তার লক্ষ্য অর্জন করেছে।","tags":["academic"],"synonyms":["accomplish"],"antonyms":[],"word_family":[{"form":"achievement","pos":"noun","bn":"অর্জন"}]},
  {"id":"v262","word":"fail","phonetic":"/feɪl/","pos":"verb","cefr":"A2","meaning_en":"to not succeed","meaning_bn":"ব্যর্থ হওয়া","example":"He failed the test.","example_bn":"সে টেস্টে ব্যর্থ হয়েছে।","tags":["study"],"synonyms":[],"antonyms":["succeed"],"word_family":[{"form":"failure","pos":"noun","bn":"ব্যর্থতা"}]},
  {"id":"v263","word":"succeed","phonetic":"/səkˈsiːd/","pos":"verb","cefr":"A2","meaning_en":"to achieve what you want","meaning_bn":"সফল হওয়া","example":"Hard work helps you succeed.","example_bn":"কঠোর পরিশ্রম সফল হতে সাহায্য করে।","tags":["study"],"synonyms":["thrive"],"antonyms":["fail"],"word_family":[{"form":"success","pos":"noun","bn":"সফলতা"},{"form":"successful","pos":"adj","bn":"সফল"}]},
  {"id":"v264","word":"prepare","phonetic":"/prɪˈpeər/","pos":"verb","cefr":"A2","meaning_en":"to get ready","meaning_bn":"প্রস্তুতি নেওয়া","example":"Prepare for the exam.","example_bn":"পরীক্ষার জন্য প্রস্তুতি নিন।","tags":["study"],"synonyms":["get ready"],"antonyms":[],"word_family":[{"form":"preparation","pos":"noun","bn":"প্রস্তুতি"}]},
  {"id":"v265","word":"practice","phonetic":"/ˈpræktɪs/","pos":"verb/noun","cefr":"A1","meaning_en":"to do something repeatedly to improve","meaning_bn":"অনুশীলন করা / অনুশীলন","example":"Practice English every day.","example_bn":"প্রতিদিন ইংরেজি অনুশীলন করুন।","tags":["study"],"synonyms":["train"],"antonyms":[]},
  {"id":"v266","word":"perform","phonetic":"/pərˈfɔːrm/","pos":"verb","cefr":"B1","meaning_en":"to do a task or act","meaning_bn":"সম্পাদন করা / পরিবেশন করা","example":"They performed well.","example_bn":"তারা ভালো করেছে।","tags":["work"],"synonyms":["carry out"],"antonyms":[],"word_family":[{"form":"performance","pos":"noun","bn":"পারফরম্যান্স"}]},
  {"id":"v267","word":"produce","phonetic":"/prəˈdjuːs/","pos":"verb","cefr":"B1","meaning_en":"to make or create","meaning_bn":"উৎপাদন করা","example":"Farms produce rice.","example_bn":"খামার ধান উৎপাদন করে।","tags":["academic"],"synonyms":["make"],"antonyms":[],"word_family":[{"form":"product","pos":"noun","bn":"পণ্য"},{"form":"production","pos":"noun","bn":"উৎপাদন"}]},
  {"id":"v268","word":"create","phonetic":"/kriˈeɪt/","pos":"verb","cefr":"A2","meaning_en":"to make something new","meaning_bn":"তৈরি করা","example":"Artists create beauty.","example_bn":"শিল্পীরা সৌন্দর্য তৈরি করেন।","tags":["daily"],"synonyms":["make"],"antonyms":[],"word_family":[{"form":"creation","pos":"noun","bn":"সৃষ্টি"},{"form":"creative","pos":"adj","bn":"সৃজনশীল"}]},
  {"id":"v269","word":"protect","phonetic":"/prəˈtekt/","pos":"verb","cefr":"A2","meaning_en":"to keep safe","meaning_bn":"রক্ষা করা","example":"Wear a helmet to protect your head.","example_bn":"মাথা রক্ষায় হেলমেট পরুন।","tags":["daily"],"synonyms":["guard"],"antonyms":[],"word_family":[{"form":"protection","pos":"noun","bn":"সুরক্ষা"}]},
  {"id":"v270","word":"prevent","phonetic":"/prɪˈvent/","pos":"verb","cefr":"B1","meaning_en":"to stop something from happening","meaning_bn":"প্রতিরোধ করা","example":"Exercise can prevent illness.","example_bn":"ব্যায়াম অসুস্থতা প্রতিরোধ করতে পারে।","tags":["health"],"synonyms":["stop"],"antonyms":[],"word_family":[{"form":"prevention","pos":"noun","bn":"প্রতিরোধ"}]},
  {"id":"v271","word":"suffer","phonetic":"/ˈsʌfər/","pos":"verb","cefr":"B1","meaning_en":"to experience pain or difficulty","meaning_bn":"ভোগা / কষ্ট পাওয়া","example":"Many people suffer from allergies.","example_bn":"অনেকে অ্যালার্জিতে ভোগেন।","tags":["health"],"synonyms":["endure"],"antonyms":[]},
  {"id":"v272","word":"recover","phonetic":"/rɪˈkʌvər/","pos":"verb","cefr":"B1","meaning_en":"to get better after illness","meaning_bn":"সুস্থ হয়ে ওঠা","example":"She recovered quickly.","example_bn":"সে দ্রুত সুস্থ হয়ে উঠেছে।","tags":["health"],"synonyms":["heal"],"antonyms":[],"word_family":[{"form":"recovery","pos":"noun","bn":"সুস্থতা ফিরে পাওয়া"}]},
  {"id":"v273","word":"treat","phonetic":"/triːt/","pos":"verb","cefr":"B1","meaning_en":"to give medical care / behave toward","meaning_bn":"চিকিৎসা করা / আচরণ করা","example":"Doctors treat patients.","example_bn":"ডাক্তাররা রোগীদের চিকিৎসা করেন।","tags":["health"],"synonyms":["care for"],"antonyms":[],"word_family":[{"form":"treatment","pos":"noun","bn":"চিকিৎসা"}]},
  {"id":"v274","word":"affect","phonetic":"/əˈfekt/","pos":"verb","cefr":"B1","meaning_en":"to influence","meaning_bn":"প্রভাবিত করা","example":"Rain affects traffic.","example_bn":"বৃষ্টি ট্রাফিককে প্রভাবিত করে।","tags":["academic"],"synonyms":["influence"],"antonyms":[]},
  {"id":"v275","word":"effect","phonetic":"/ɪˈfekt/","pos":"noun","cefr":"B1","meaning_en":"a result","meaning_bn":"প্রভাব / ফলাফল","example":"What is the effect of pollution?","example_bn":"দূষণের প্রভাব কী?","tags":["academic"],"synonyms":["result"],"antonyms":[]},
  {"id":"v276","word":"cause","phonetic":"/kɔːz/","pos":"verb/noun","cefr":"A2","meaning_en":"to make happen / reason","meaning_bn":"কারণ হওয়া / কারণ","example":"What caused the accident?","example_bn":"দুর্ঘটনার কারণ কী ছিল?","tags":["daily"],"synonyms":["reason"],"antonyms":[]},
  {"id":"v277","word":"result","phonetic":"/rɪˈzʌlt/","pos":"noun/verb","cefr":"A2","meaning_en":"outcome","meaning_bn":"ফলাফল","example":"The result was good.","example_bn":"ফলাফল ভালো ছিল।","tags":["study"],"synonyms":["outcome"],"antonyms":[]},
  {"id":"v278","word":"benefit","phonetic":"/ˈbenɪfɪt/","pos":"noun/verb","cefr":"B1","meaning_en":"an advantage","meaning_bn":"সুবিধা / উপকার","example":"Exercise has many benefits.","example_bn":"ব্যায়ামের অনেক উপকার আছে।","tags":["academic"],"synonyms":["advantage"],"antonyms":["harm"]},
  {"id":"v279","word":"advantage","phonetic":"/ədˈvɑːntɪdʒ/","pos":"noun","cefr":"B1","meaning_en":"something helpful","meaning_bn":"সুবিধা","example":"Speaking English is an advantage.","example_bn":"ইংরেজি বলা একটি সুবিধা।","tags":["academic"],"synonyms":["benefit"],"antonyms":["disadvantage"]},
  {"id":"v280","word":"disadvantage","phonetic":"/ˌdɪsədˈvɑːntɪdʒ/","pos":"noun","cefr":"B1","meaning_en":"something unhelpful","meaning_bn":"অসুবিধা","example":"One disadvantage is cost.","example_bn":"একটি অসুবিধা হলো খরচ।","tags":["academic"],"synonyms":["drawback"],"antonyms":["advantage"]},
  {"id":"v281","word":"purpose","phonetic":"/ˈpɜːpəs/","pos":"noun","cefr":"A2","meaning_en":"the reason for something","meaning_bn":"উদ্দেশ্য","example":"What is the purpose of this meeting?","example_bn":"এই মিটিংয়ের উদ্দেশ্য কী?","tags":["work"],"synonyms":["aim"],"antonyms":[]},
  {"id":"v282","word":"goal","phonetic":"/ɡəʊl/","pos":"noun","cefr":"A2","meaning_en":"something you want to achieve","meaning_bn":"লক্ষ্য","example":"My goal is Band 7.","example_bn":"আমার লক্ষ্য ব্যান্ড ৭।","tags":["study"],"synonyms":["aim","target"],"antonyms":[]},
  {"id":"v283","word":"opportunity","phonetic":"/ˌɒpəˈtjuːnəti/","pos":"noun","cefr":"B1","meaning_en":"a chance to do something","meaning_bn":"সুযোগ","example":"This is a great opportunity.","example_bn":"এটি একটি দুর্দান্ত সুযোগ।","tags":["work"],"synonyms":["chance"],"antonyms":[]},
  {"id":"v284","word":"challenge","phonetic":"/ˈtʃælɪndʒ/","pos":"noun/verb","cefr":"B1","meaning_en":"something difficult","meaning_bn":"চ্যালেঞ্জ","example":"Learning a language is a challenge.","example_bn":"ভাষা শেখা একটি চ্যালেঞ্জ।","tags":["study"],"synonyms":["difficulty"],"antonyms":[]},
  {"id":"v285","word":"solution","phonetic":"/səˈluːʃn/","pos":"noun","cefr":"B1","meaning_en":"an answer to a problem","meaning_bn":"সমাধান","example":"We need a solution.","example_bn":"আমাদের একটি সমাধান দরকার।","tags":["academic"],"synonyms":["answer"],"antonyms":[],"word_family":[{"form":"solve","pos":"verb","bn":"সমাধান করা"}]},
  {"id":"v286","word":"problem","phonetic":"/ˈprɒbləm/","pos":"noun","cefr":"A1","meaning_en":"something difficult to deal with","meaning_bn":"সমস্যা","example":"We have a small problem.","example_bn":"আমাদের একটি ছোট সমস্যা আছে।","tags":["daily"],"synonyms":["issue"],"antonyms":[]},
  {"id":"v287","word":"situation","phonetic":"/ˌsɪtʃuˈeɪʃn/","pos":"noun","cefr":"A2","meaning_en":"the way things are","meaning_bn":"পরিস্থিতি","example":"The situation is under control.","example_bn":"পরিস্থিতি নিয়ন্ত্রণে আছে।","tags":["daily"],"synonyms":["circumstance"],"antonyms":[]},
  {"id":"v288","word":"condition","phonetic":"/kənˈdɪʃn/","pos":"noun","cefr":"B1","meaning_en":"state of something","meaning_bn":"অবস্থা / শর্ত","example":"The road is in bad condition.","example_bn":"রাস্তার অবস্থা খারাপ।","tags":["daily"],"synonyms":["state"],"antonyms":[]},
  {"id":"v289","word":"quality","phonetic":"/ˈkwɒləti/","pos":"noun","cefr":"B1","meaning_en":"how good something is","meaning_bn":"গুণমান","example":"High quality products last longer.","example_bn":"উচ্চ গুণমানের পণ্য বেশিদিন টিকে।","tags":["work"],"synonyms":["standard"],"antonyms":[]},
  {"id":"v290","word":"quantity","phonetic":"/ˈkwɒntəti/","pos":"noun","cefr":"B1","meaning_en":"amount","meaning_bn":"পরিমাণ","example":"Buy a large quantity.","example_bn":"বড় পরিমাণে কিনুন।","tags":["academic"],"synonyms":["amount"],"antonyms":[]},
  {"id":"v291","word":"amount","phonetic":"/əˈmaʊnt/","pos":"noun","cefr":"A2","meaning_en":"a quantity of something","meaning_bn":"পরিমাণ","example":"A large amount of money.","example_bn":"প্রচুর পরিমাণ টাকা।","tags":["daily"],"synonyms":["quantity"],"antonyms":[]},
  {"id":"v292","word":"value","phonetic":"/ˈvæljuː/","pos":"noun/verb","cefr":"B1","meaning_en":"worth","meaning_bn":"মূল্য","example":"Education has great value.","example_bn":"শিক্ষার বড় মূল্য আছে।","tags":["academic"],"synonyms":["worth"],"antonyms":[]},
  {"id":"v293","word":"price","phonetic":"/praɪs/","pos":"noun","cefr":"A1","meaning_en":"how much something costs","meaning_bn":"দাম","example":"What is the price?","example_bn":"দাম কত?","tags":["shopping"],"synonyms":["cost"],"antonyms":[]},
  {"id":"v294","word":"cost","phonetic":"/kɒst/","pos":"noun/verb","cefr":"A1","meaning_en":"the amount you pay","meaning_bn":"খরচ / খরচ হওয়া","example":"It costs too much.","example_bn":"এর খরচ অনেক।","tags":["shopping"],"synonyms":["price"],"antonyms":[]},
  {"id":"v295","word":"profit","phonetic":"/ˈprɒfɪt/","pos":"noun","cefr":"B1","meaning_en":"money gained in business","meaning_bn":"লাভ","example":"The company made a profit.","example_bn":"কোম্পানি লাভ করেছে।","tags":["work"],"synonyms":["gain"],"antonyms":["loss"]},
  {"id":"v296","word":"loss","phonetic":"/lɒs/","pos":"noun","cefr":"A2","meaning_en":"something lost","meaning_bn":"ক্ষতি / হারানো","example":"They suffered a loss.","example_bn":"তারা ক্ষতির সম্মুখীন হয়েছে।","tags":["work"],"synonyms":[],"antonyms":["profit","gain"]},
  {"id":"v297","word":"budget","phonetic":"/ˈbʌdʒɪt/","pos":"noun","cefr":"B1","meaning_en":"a plan for spending money","meaning_bn":"বাজেট","example":"We have a tight budget.","example_bn":"আমাদের বাজেট সীমিত।","tags":["work"],"synonyms":[],"antonyms":[]},
  {"id":"v298","word":"expense","phonetic":"/ɪkˈspens/","pos":"noun","cefr":"B1","meaning_en":"money spent","meaning_bn":"খরচ","example":"Travel expenses are high.","example_bn":"ভ্রমণ খরচ বেশি।","tags":["work"],"synonyms":["cost"],"antonyms":[]},
  {"id":"v299","word":"income","phonetic":"/ˈɪnkʌm/","pos":"noun","cefr":"B1","meaning_en":"money received","meaning_bn":"আয়","example":"His income increased.","example_bn":"তার আয় বেড়েছে।","tags":["work"],"synonyms":["earnings"],"antonyms":[]},
  {"id":"v300","word":"salary","phonetic":"/ˈsæləri/","pos":"noun","cefr":"A2","meaning_en":"regular pay from a job","meaning_bn":"বেতন","example":"What is your salary?","example_bn":"আপনার বেতন কত?","tags":["work"],"synonyms":["pay","wage"],"antonyms":[]},
]

NEW_SP = [
  {"id":"sp16","title":"At the pharmacy","title_bn":"ফার্মেসিতে","cefr":"A2","scenario":"Buying medicine","lines":[
    {"speaker":"You","en":"I have a headache. Do you have something for it?","bn":"আমার মাথাব্যথা। এর জন্য কিছু আছে?"},
    {"speaker":"Pharmacist","en":"Yes. Take this twice a day after meals.","bn":"হ্যাঁ। দিনে দুবার খাবারের পর নিন।"},
    {"speaker":"You","en":"How much is it?","bn":"এর দাম কত?"},
    {"speaker":"Pharmacist","en":"One hundred twenty taka.","bn":"একশো বিশ টাকা।"},
    {"speaker":"You","en":"Thank you.","bn":"ধন্যবাদ।"},
  ]},
  {"id":"sp17","title":"Asking for directions","title_bn":"রাস্তা জিজ্ঞাসা","cefr":"A2","scenario":"Finding a place","lines":[
    {"speaker":"You","en":"Excuse me, where is the nearest metro station?","bn":"মাফ করবেন, নিকটতম মেট্রো স্টেশন কোথায়?"},
    {"speaker":"Local","en":"Go straight and turn left at the traffic light.","bn":"সোজা যান এবং ট্রাফিক লাইটে বামে ঘুরুন।"},
    {"speaker":"You","en":"Is it far?","bn":"দূরে কি?"},
    {"speaker":"Local","en":"About five minutes on foot.","bn":"পায়ে হেঁটে প্রায় পাঁচ মিনিট।"},
    {"speaker":"You","en":"Thanks a lot!","bn":"অনেক ধন্যবাদ!"},
  ]},
  {"id":"sp18","title":"At a restaurant","title_bn":"রেস্টুরেন্টে","cefr":"A2","scenario":"Ordering food","lines":[
    {"speaker":"Waiter","en":"Are you ready to order?","bn":"অর্ডার দিতে প্রস্তুত?"},
    {"speaker":"You","en":"Yes. I'll have chicken biryani, please.","bn":"হ্যাঁ। আমি চিকেন বিরিয়ানি নেব।"},
    {"speaker":"Waiter","en":"Anything to drink?","bn":"কিছু পানীয়?"},
    {"speaker":"You","en":"A soft drink, please.","bn":"একটা সফট ড্রিংক দিন।"},
    {"speaker":"Waiter","en":"It will be ready in fifteen minutes.","bn":"পনেরো মিনিটে রেডি হবে।"},
  ]},
  {"id":"sp19","title":"Making an appointment","title_bn":"অ্যাপয়েন্টমেন্ট","cefr":"B1","scenario":"Doctor booking","lines":[
    {"speaker":"You","en":"I'd like to make an appointment with Dr. Rahman.","bn":"ডা. রহমানের সাথে অ্যাপয়েন্টমেন্ট চাই।"},
    {"speaker":"Reception","en":"Is Thursday morning okay?","bn":"বৃহস্পতিবার সকাল ঠিক আছে?"},
    {"speaker":"You","en":"Yes, around ten o'clock.","bn":"হ্যাঁ, প্রায় দশটার দিকে।"},
    {"speaker":"Reception","en":"You're booked for 10:15. Please bring your ID.","bn":"আপনি ১০:১৫-এ বুক হয়েছেন। আইডি নিয়ে আসবেন।"},
  ]},
  {"id":"sp20","title":"Complaining politely","title_bn":"ভদ্রভাবে অভিযোগ","cefr":"B1","scenario":"Hotel room issue","lines":[
    {"speaker":"You","en":"Excuse me. There is a problem with my room.","bn":"মাফ করবেন। আমার রুমে সমস্যা আছে।"},
    {"speaker":"Staff","en":"I'm sorry to hear that. What's wrong?","bn":"দুঃখিত। কী সমস্যা?"},
    {"speaker":"You","en":"The air conditioner is not working.","bn":"এয়ার কন্ডিশনার কাজ করছে না।"},
    {"speaker":"Staff","en":"We'll send someone immediately.","bn":"আমরা এখনই কাউকে পাঠাব।"},
    {"speaker":"You","en":"Thank you for your help.","bn":"সাহায্যের জন্য ধন্যবাদ।"},
  ]},
  {"id":"sp21","title":"Small talk at work","title_bn":"অফিসে ছোট কথা","cefr":"B1","scenario":"Colleague chat","lines":[
    {"speaker":"Colleague","en":"How was your weekend?","bn":"উইকেন্ড কেমন কাটল?"},
    {"speaker":"You","en":"It was good. I visited my family. What about you?","bn":"ভালো ছিল। পরিবারের সাথে দেখা করেছি। আপনি?"},
    {"speaker":"Colleague","en":"I stayed home and rested.","bn":"বাড়িতে থেকে বিশ্রাম নিয়েছি।"},
    {"speaker":"You","en":"Sounds nice. Ready for the meeting?","bn":"ভালো শুনতে। মিটিংয়ের জন্য প্রস্তুত?"},
  ]},
  {"id":"sp22","title":"Paying a bill","title_bn":"বিল পরিশোধ","cefr":"A2","scenario":"Checkout","lines":[
    {"speaker":"Cashier","en":"Your total is eight hundred taka.","bn":"মোট আটশো টাকা।"},
    {"speaker":"You","en":"Can I pay by card?","bn":"কার্ডে দিতে পারি?"},
    {"speaker":"Cashier","en":"Yes, of course. Please tap your card.","bn":"হ্যাঁ অবশ্যই। কার্ড ট্যাপ করুন।"},
    {"speaker":"You","en":"Done. Could I have a receipt?","bn":"হয়ে গেছে। রসিদ দেবেন?"},
    {"speaker":"Cashier","en":"Here you are. Have a nice day!","bn":"নিন। ভালো দিন কাটুক!"},
  ]},
]


def main():
    vp = ROOT / "data" / "vocabulary.json"
    vocab = json.loads(vp.read_text(encoding="utf-8"))
    have = {v["word"].lower() for v in vocab}
    added = 0
    for w in MORE:
        if w["word"].lower() in have:
            continue
        w.setdefault("synonyms", [])
        w.setdefault("antonyms", [])
        w.setdefault("tags", [])
        vocab.append(w)
        have.add(w["word"].lower())
        added += 1
    vp.write_text(json.dumps(vocab, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("vocab added", added, "total", len(vocab))

    sp = ROOT / "data" / "spoken.json"
    spoken = json.loads(sp.read_text(encoding="utf-8"))
    ids = {x["id"] for x in spoken}
    for d in NEW_SP:
        if d["id"] not in ids:
            spoken.append(d)
            ids.add(d["id"])
    sp.write_text(json.dumps(spoken, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("spoken", len(spoken), "lines", sum(len(x["lines"]) for x in spoken))


if __name__ == "__main__":
    main()
