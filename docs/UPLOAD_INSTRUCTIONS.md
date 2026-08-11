# সাইট আপলোড ও ব্যবহার গাইড  
## English for Bengalis — MVP

**তারিখ:** 11 August 2026  
**প্রজেক্ট ফোল্ডার:** `English_Learning_Platform`

এই ডকুমেন্টে আছে:
1. লোকালে সাইট চালানো  
2. কোন ফাইল কী কাজ করে  
3. Blogger-এ আপলোড করার ধাপ  
4. GitHub Pages দিয়ে JS/CSS হোস্ট করা (প্রস্তাবিত)  
5. মেনু ও পেজ সেটআপ  
6. সাধারণ সমস্যা ও সমাধান  

---

## ১) আগে লোকালে টেস্ট করুন (জরুরি)

JSON ডেটা `fetch` দিয়ে লোড হয়। তাই ফাইল ডাবল‑ক্লিক (`file://`) করলে অনেক ব্রাউজারে কুইজ/লিস্ট কাজ নাও করতে পারে।

### Windows PowerShell এ সহজ সার্ভার

প্রজেক্ট ফোল্ডারে গিয়ে:

```powershell
cd H:\project\English_Learning_Platform
python -m http.server 8080
```

তারপর ব্রাউজারে খুলুন:

`http://localhost:8080/`

বন্ধ করতে টার্মিনালে `Ctrl + C`।

Python না থাকলে Node দিয়ে:

```powershell
npx --yes serve -l 8080
```

### যা চেক করবেন

- [ ] হোমপেজ খুলছে  
- [ ] Vocabulary / Grammar লিস্ট আসছে  
- [ ] Quiz উত্তর দিলে স্কোর হচ্ছে  
- [ ] My Progress আপডেট হচ্ছে  
- [ ] Settings → Export JSON কাজ করছে  

---

## ২) ফাইল ম্যাপ — কোনটা কী

```text
English_Learning_Platform/
├── index.html              ← হোমপেজ
├── pages/                  ← সব টুল ও হাব পেজ
│   ├── learn.html
│   ├── practice.html
│   ├── vocabulary.html
│   ├── grammar.html
│   ├── phrasal-verbs.html
│   ├── spelling.html
│   ├── spoken-english.html
│   ├── common-mistakes.html
│   ├── quizzes.html
│   ├── flashcards.html
│   ├── daily-challenge.html
│   ├── translation-lab.html
│   ├── my-progress.html
│   ├── level-test.html
│   ├── settings.html
│   ├── ielts.html
│   ├── about.html
│   ├── contact.html
│   ├── privacy.html
│   ├── terms.html
│   └── disclaimer.html
├── css/learning.css        ← ডিজাইন
├── js/                     ← লার্নিং ইঞ্জিন
│   ├── storage.js
│   ├── progress.js
│   ├── quiz-engine.js
│   ├── daily-challenge.js
│   └── app.js
├── data/                   ← কন্টেন্ট JSON
│   ├── vocabulary.json
│   ├── phrasal-verbs.json
│   ├── spelling.json
│   ├── grammar.json
│   ├── common-mistakes.json
│   ├── quizzes.json
│   └── spoken.json
├── docs/
│   └── UPLOAD_INSTRUCTIONS.md   ← এই ফাইল
└── Bengali_Speaker_English_Learning_Platform_Master_Plan.md
```

### আপলোড ভাগ করে ভাবুন

| অংশ | ফাইল | কোথায় রাখবেন |
|---|---|---|
| লার্নিং ইঞ্জিন + ডেটা | `css/`, `js/`, `data/` | **GitHub Pages / Netlify / Cloudflare Pages** (প্রস্তাবিত) |
| পাঠযোগ্য পেজ | `index.html`, `pages/*.html` | প্রথমে একই হোস্টে পুরো সাইট; পরে চাইলে Blogger পেজে কন্টেন্ট কপি |
| প্ল্যান ডক | `*.md` | আপলোড লাগবে না (নিজের জন্য) |

> **সবচেয়ে সহজ পথ (শুরুতে):** পুরো ফোল্ডার GitHub Pages-এ পাবলিশ করুন। Blogger পরে SEO আর্টিকেলের জন্য ব্যবহার করুন।

---

## ৩) সবচেয়ে সহজ আপলোড: GitHub Pages (পুরো সাইট)

Blogger-এ টুকরো টুকরো না করে আগে পুরো MVP লাইভ করতে চাইলে এটি বেস্ট।

### ধাপ

1. GitHub-এ নতুন রিপোজিটরি তৈরি করুন (উদাহরণ: `english-for-bengalis`)  
2. সব প্রজেক্ট ফাইল আপলোড / push করুন  
3. **Settings → Pages → Branch: `main` → folder: `/ (root)` → Save**  
4. কিছু মিনিট পর সাইট পাবেন:  
   `https://YOUR_USERNAME.github.io/english-for-bengalis/`  

### কাস্টম ডোমেইন (ঐচ্ছিক)

Pages সেটিংসে Custom domain দিন (যেমন `englishforbengalis.com`)।  
**সতর্কতা:** ডোমেইন বদলালে localStorage আলাদা হয়ে যেতে পারে — আগে Settings থেকে **Export** করুন।

### এই পদ্ধতিতে কোন ফাইল আপলোড?

**সব** — `index.html`, `pages/`, `css/`, `js/`, `data/`।  
`.md` ডক চাইলে বাদ দিতে পারেন।

---

## ৪) Blogger-এ রাখতে চাইলে (হাইব্রিড পদ্ধতি)

প্ল্যান অনুযায়ী Blogger = SEO/লেসন, আর JS ইঞ্জিন বাইরে হোস্ট।

### ধাপ A — ইঞ্জিন হোস্ট করুন

1. `css/`, `js/`, `data/` GitHub Pages-এ পাবলিশ করুন  
2. পাবলিক URL নোট করুন, যেমন:  
   `https://YOUR_USERNAME.github.io/english-for-bengalis/js/app.js`

### ধাপ B — Blogger থিম

1. [blogger.com](https://www.blogger.com) → আপনার ব্লগ  
2. **Theme → Edit HTML**  
3. `</head>` এর আগে CSS যোগ করুন:

```html
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;700&family=Noto+Sans+Bengali:wght@400;600;700&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="https://YOUR_USERNAME.github.io/english-for-bengalis/css/learning.css" />
```

4. `</body>` এর আগে স্ক্রিপ্ট:

```html
<script src="https://YOUR_USERNAME.github.io/english-for-bengalis/js/storage.js"></script>
<script src="https://YOUR_USERNAME.github.io/english-for-bengalis/js/progress.js"></script>
<script src="https://YOUR_USERNAME.github.io/english-for-bengalis/js/quiz-engine.js"></script>
<script src="https://YOUR_USERNAME.github.io/english-for-bengalis/js/daily-challenge.js"></script>
<script src="https://YOUR_USERNAME.github.io/english-for-bengalis/js/app.js"></script>
```

5. Save

### ধাপ C — Blogger Pages তৈরি

**Pages → New page** দিয়ে তৈরি করুন (নাম মিলিয়ে):

| Blogger Page নাম | সোর্স থেকে কপি করবেন |
|---|---|
| Learn | `pages/learn.html` এর `<main>...</main>` অংশ |
| Practice | `pages/practice.html` |
| Vocabulary | `pages/vocabulary.html` |
| Grammar | `pages/grammar.html` |
| … | একইভাবে অন্যান্য পেজ |
| My Progress | `pages/my-progress.html` |
| Privacy / Terms / Disclaimer | সংশ্লিষ্ট HTML |

**কীভাবে কপি করবেন**

1. সংশ্লিষ্ট HTML ফাইল খুলুন  
2. শুধু `<main id="main" ...> ... </main>` এর ভিতরের কন্টেন্ট কপি করুন  
3. Blogger পেজ এডিটরে **HTML view** এ পেস্ট করুন  
4. স্ক্রিপ্ট পাথ ঠিক করুন:  
   - `../js/...` → পূর্ণ GitHub URL  
   - `../css/...` → থিমে থাকলে বাদ দিতে পারেন  
   - `EFBApp.loadJSON(...)` কাজ করতে `data-root` ও asset URL ঠিক রাখুন  

> **সহজ বিকল্প:** Blogger পেজে শুধু বাটন/লিংক রাখুন যা GitHub Pages সাইটের টুল পেজে নিয়ে যায়। SEO আর্টিকেল Blogger-এ, ইন্টারঅ্যাকটিভ টুল GitHub Pages-এ।

### ধাপ D — মেনু

Blogger → **Layout** বা Pages সেটিংস থেকে মেনু:

1. Learn  
2. Practice  
3. Progress  
4. Level Test  
5. IELTS  
6. About / Contact  

প্ল্যানের বিস্তারিত মেনু: Master Plan §126।

### ধাপ E — পোস্ট (লেসন/SEO)

নতুন শিক্ষণ আর্টিকেল = **Post** (Page নয়)।  
লেবেল দিন: `grammar`, `a2`, `lesson`, `common-mistakes` ইত্যাদি।

---

## ৫) কোন ফাইল Blogger-এ সরাসরি আপলোড হয় না?

Blogger সাধারণত আলাদা করে `js/` বা `json/` ফোল্ডার হোস্ট করে না যেমনটা GitHub করে।

তাই:

- ❌ শুধু Blogger Media-তে সব JS রেখে পূর্ণ অ্যাপ আশা করবেন না  
- ✅ JS/CSS/JSON → GitHub Pages / Netlify  
- ✅ লেসন টেক্সট / SEO পোস্ট → Blogger  

---

## ৬) Netlify দিয়ে আপলোড (বিকল্প)

1. [netlify.com](https://www.netlify.com) এ সাইন আপ  
2. **Add new site → Deploy manually**  
3. পুরো `English_Learning_Platform` ফোল্ডার ড্র্যাগ‑ড্রপ  
4. লাইভ লিংক পাবেন  

এটিও GitHub Pages-এর মতো সহজ।

---

## ৭) আপলোড চেকলিস্ট

### GitHub Pages / Netlify

- [ ] `index.html` রুটে আছে  
- [ ] `css/learning.css` লোড হচ্ছে (View Source / Network)  
- [ ] `data/vocabulary.json` ব্রাউজারে খুলে JSON দেখা যাচ্ছে  
- [ ] Quiz কাজ করছে  
- [ ] মোবাইলে মেনু খুলছে  

### Blogger হাইব্রিড

- [ ] বাইরের CSS/JS URL HTTPS  
- [ ] Privacy / Terms / Disclaimer পেজ আছে  
- [ ] IELTS disclaimer আছে  
- [ ] মেনু লিংক ভাঙা নয়  
- [ ] Contact-এ নিজের ইমেইল বসানো  

---

## ৮) কন্টেন্ট বাড়ানো হলে কী আপলোড?

| কাজ | কোন ফাইল এডিট | কোথায় আপলোড |
|---|---|---|
| নতুন শব্দ | `data/vocabulary.json` | GitHub/Netlify আবার deploy |
| নতুন কুইজ | `data/quizzes.json` | একই |
| নতুন গ্রামার টপিক | `data/grammar.json` (+ চাইলে নতুন HTML সেকশন) | একই |
| ডিজাইন বদল | `css/learning.css` | একই |
| নতুন টুল পেজ | `pages/new-page.html` + `js/app.js` মেনু | একই |
| SEO আর্টিকেল | — | Blogger **Post** |

প্রতিবার JSON বদলালে হোস্টিং এ **Redeploy / push** করতে হবে।

---

## ৯) সাধারণ সমস্যা

### “Data load error” / লিস্ট খালি

- `file://` দিয়ে খুলেছেন → লোকাল সার্ভার ব্যবহার করুন  
- GitHub Pages-এ পাথ ভুল → রিপো নামসহ ফোল্ডার স্ট্রাকচার চেক করুন  

### প্রোগ্রেস উধাও

- ব্রাউজার ডেটা ক্লিয়ার করেছেন  
- অন্য ব্রাউজার/ফোন ব্যবহার করছেন  
- blogspot → কাস্টম ডোমেইন বদলেছেন  

**সমাধান:** Settings → Export রাখুন; নতুন জায়গায় Import করুন।

### Blogger-এ স্ক্রিপ্ট কাজ করছে না

- HTTP মিক্সড কন্টেন্ট — সব URL `https://` হতে হবে  
- থিম এডিটরে ট্যাগ কেটে গেছে কিনা দেখুন  

---

## ১০) CMD দিয়ে সরাসরি Blogger আপলোড (নতুন)

হ্যাঁ, Windows CMD/BAT দিয়ে Blogger-এ পেজ ও পোস্ট পাঠানো যায়।

1. পড়ুন: [`docs/BLOGGER_CMD_UPLOAD.md`](BLOGGER_CMD_UPLOAD.md)  
2. Google OAuth `tools/client_secret.json` সেট করুন  
3. ডাবল‑ক্লিক: `tools\upload-to-blogger.bat`  

টার্গেট ব্লগ: https://englishforbengalis.blogspot.com/

---

## ১১) এখন আপনার করণীয় (সংক্ষেপ)

1. লোকালে `python -m http.server 8080` চালিয়ে টেস্ট  
2. **Blogger CMD আপলোড** (`upload-to-blogger.bat`) অথবা GitHub Pages  
3. Contact পেজে নিজের ইমেইল দিন  
4. কুইজের জন্য `css/js/data` GitHub Pages-এ রেখে `asset_base_url` সেট করুন  
5. কন্টেন্ট বাড়াতে `data/*.json` এডিট করে আবার deploy / BAT  

---

## ১১) সাহায্যকারী লিংক

- Blogger: https://www.blogger.com  
- আপনার সাইট: https://englishforbengalis.blogspot.com/  
- CMD আপলোড গাইড: [`BLOGGER_CMD_UPLOAD.md`](BLOGGER_CMD_UPLOAD.md)  
- GitHub Pages ডক: https://docs.github.com/pages  
- মাস্টার প্ল্যান: `Bengali_Speaker_English_Learning_Platform_Master_Plan.md`  

---

**মনে রাখবেন:**  
`UPLOAD_INSTRUCTIONS.md` ও Master Plan সাইট ভিজিটরের জন্য আপলোড করা লাগে না — শুধু `html/css/js/data` লাগে।  
BAT স্ক্রিপ্ট Blogger-এ **HTML পেজ/পোস্ট** পাঠায়; `css/js/data` ফাইল হোস্ট করতে GitHub Pages লাগে।
