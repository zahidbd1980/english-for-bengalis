# Blogger CMD আপলোড গাইড (Python + BAT)

আপনার সাইট: https://englishforbengalis.blogspot.com/

হ্যাঁ — CMD দিয়ে Blogger-এ পেজ/পোস্ট পাবলিশ করা যায়। এটা **অফিসিয়াল Blogger API v3** ব্যবহার করে (ফাইল FTP নয়)।

---

## গুরুত্বপূর্ণ সত্য (আগে পড়ুন)

| কাজ | CMD দিয়ে সম্ভব? |
|---|---|
| About / Learn / Quiz **পেজের HTML** পাবলিশ | ✅ হ্যাঁ (`upload-to-blogger.bat`) |
| Welcome **পোস্ট** পাবলিশ | ✅ হ্যাঁ |
| `css/`, `js/`, `data/` ফাইল Blogger সার্ভারে আপলোড | ❌ না (Blogger ফাইল হোস্ট নয়) |
| কুইজ/JSON কাজ করানো | ✅ আলাদাভাবে GitHub Pages-এ `css/js/data` রেখে `asset_base_url` সেট করুন |

অর্থাৎ: **BAT = Blogger-এ কন্টেন্ট পাঠায়**।  
**ইন্টারঅ্যাকটিভ ইঞ্জিন** চাইলে GitHub Pages লিংক `blogger_config.json`-এ দিতে হবে।

---

## একবারের সেটআপ (৩০–৪০ মিনিট)

### A) Python

1. https://www.python.org/downloads/  
2. ইন্সটলে **Add python.exe to PATH** টিক দিন  
3. CMD খুলে চেক:

```bat
python --version
```

### B) Google Cloud OAuth (একবার)

1. https://console.cloud.google.com/ এ যান (যে Google অ্যাকাউন্টে Blogger আছে)  
2. নতুন প্রজেক্ট তৈরি (নাম: `EnglishForBengalis`)  
3. **APIs & Services → Library** → খুঁজুন **Blogger API v3** → **Enable**  
4. **APIs & Services → OAuth consent screen**  
   - User type: **External** (ব্যক্তিগত অ্যাকাউন্ট হলে)  
   - App name: English for Bengalis  
   - নিজের ইমেইল দিন → Save  
   - Test users এ নিজের Gmail যোগ করুন  
5. **Credentials → Create Credentials → OAuth client ID**  
   - Application type: **Desktop app**  
   - Create → **Download JSON**  
6. ডাউনলোড করা ফাইল কপি করে রাখুন:

```text
H:\project\English_Learning_Platform\tools\client_secret.json
```

> নাম ঠিক এমনই হতে হবে: `client_secret.json`

### C) (ঐচ্ছিক কিন্তু কুইজের জন্য দরকার) GitHub Pages

1. পুরো প্রজেক্ট GitHub-এ পুশ করুন  
2. Pages চালু করুন  
3. `tools\blogger_config.json` খুলে লিখুন:

```json
"asset_base_url": "https://YOUR_USERNAME.github.io/REPO_NAME"
```

শেষে `/` দেবেন না।

---

## Blogger + Pages একসাথে (সুপারিশ)

```bat
tools\deploy-github-pages.bat
tools\upload-to-blogger.bat
```

আগে Pages, পরে Blogger — তাহলে কুইজের `asset_base_url` ঠিক থাকে।


### উপায় ২ — CMD

```bat
cd /d H:\project\English_Learning_Platform
tools\upload-to-blogger.bat
```

অথবা:

```bat
cd /d H:\project\English_Learning_Platform
python -m pip install -r tools\requirements-blogger.txt
python tools\blogger_upload.py --auth
python tools\blogger_upload.py --upload-welcome
python tools\blogger_upload.py --upload-pages
```

### আগে Draft হিসেবে পাঠাতে চাইলে

```text
tools\upload-to-blogger-DRAFT.bat
```

তারপর Blogger Dashboard থেকে Publish।

### কী আছে দেখতে

```text
tools\list-blogger.bat
```

---

## আপলোডের পর Blogger-এ যা করবেন

1. https://www.blogger.com → আপনার ব্লগ  
2. **Pages** → পেজগুলো দেখা যাচ্ছে কিনা চেক  
3. **Layout / Pages gadget** বা থিম মেনুতে যোগ করুন: Learn, Practice, Progress…  
4. হোমপেজে Welcome পোস্ট দেখা যাবে  
5. কুইজ না খুললে `asset_base_url` সেট করে BAT আবার চালান  

সাইট: https://englishforbengalis.blogspot.com/

---

## ফাইল তালিকা

| ফাইল | কাজ |
|---|---|
| `tools/upload-to-blogger.bat` | এক ক্লিকে আপলোড |
| `tools/upload-to-blogger-DRAFT.bat` | Draft মোড |
| `tools/list-blogger.bat` | পেজ/পোস্ট লিস্ট |
| `tools/blogger_upload.py` | আসল আপলোড স্ক্রিপ্ট |
| `tools/blogger_config.json` | কোন পেজ যাবে + asset URL |
| `tools/client_secret.json` | আপনি রাখবেন (গোপন) |
| `tools/token.json` | লগইনের পর অটো তৈরি |

---

## সমস্যা হলে

### `client_secret.json নেই`
উপরের Google Cloud ধাপ শেষ করে JSON রাখুন।

### Access blocked / app not verified
Consent screen এ **Testing** মোড + Test user হিসেবে নিজের Gmail যোগ করুন। Continuে গিয়ে Advanced → Go to app।

### Quiz কাজ করে না
`asset_base_url` খালি আছে। GitHub Pages সেট করে আবার `--upload-pages` চালান।

### 403 / Blog not found
যে Google অ্যাকাউন্টে ব্লগ আছে, সেই অ্যাকাউন্ট দিয়ে `--auth` করুন।  
`blogger_config.json` এ URL: `https://englishforbengalis.blogspot.com/`

---

## নিরাপত্তা

- `client_secret.json` ও `token.json` **কখনো GitHub-এ পাবলিক পুশ করবেন না**  
- প্রজেক্টে `.gitignore` এ এগুলো বাদ দেওয়া আছে  

---

## রেফারেন্স

- [Blogger API — Using the API](https://developers.google.com/blogger/docs/3.0/using)  
- [Pages: insert](https://developers.google.com/blogger/docs/3.0/reference/pages/insert)
