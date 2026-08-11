# client_secret.json — সহজ সেটআপ (৫ ধাপ)

আপনার ব্লগ: https://englishforbengalis.blogspot.com/  
লাইভ টুল সাইট: https://zahidbd1980.github.io/english-for-bengalis/

`client_secret` এখনো নেই — নিচের ধাপ একবার করলেই হবে।

---

## সবচেয়ে সহজ উপায়

ডাবল‑ক্লিক করুন:

```text
tools\setup-blogger-secret.bat
```

এটা ধাপে ধাপে ব্রাউজার খুলে দেবে। শেষে JSON ফাইল `tools` ফোল্ডারে রাখবেন।

---

## ম্যানুয়াল ধাপ (একই কাজ)

### ১) Google Cloud প্রজেক্ট
1. খুলুন: https://console.cloud.google.com/  
2. যে Gmail দিয়ে Blogger চলে, **সেই অ্যাকাউন্ট** দিয়ে লগইন  
3. উপরের প্রজেক্ট সিলেক্টর → **New Project**  
4. নাম: `EnglishForBengalis` → Create  

### ২) Blogger API চালু
1. খুলুন: https://console.cloud.google.com/apis/library/blogger.googleapis.com  
2. **Enable** চাপুন  

### ৩) OAuth consent screen
1. খুলুন: https://console.cloud.google.com/apis/credentials/consent  
2. User type: **External** → Create  
3. App name: `English for Bengalis`  
4. User support email + Developer contact = আপনার Gmail  
5. Save  
6. **Test users** → Add users → আপনার Gmail যোগ করুন  
7. Save  

### ৪) Desktop OAuth client
1. খুলুন: https://console.cloud.google.com/apis/credentials  
2. **+ Create Credentials** → **OAuth client ID**  
3. Application type: **Desktop app**  
4. Name: `EFB Uploader` → Create  
5. **Download JSON** চাপুন  

### ৫) ফাইল রাখুন
ডাউনলোড করা ফাইলের নাম বদলে রাখুন:

```text
H:\project\English_Learning_Platform\tools\client_secret.json
```

নাম ঠিক এমনই হতে হবে।

---

## তারপর আপলোড

```text
tools\upload-to-blogger.bat
```

1. প্রথমবার ব্রাউজার খুলবে → Google অ্যাকাউন্ট সিলেক্ট  
2. “Google hasn’t verified this app” দেখলে: **Advanced** → **Go to English for Bengalis (unsafe)**  
3. Allow / Continue  
4. স্ক্রিপ্ট Pages + Welcome post আপলোড করবে  

শেষে Blogger → **Pages** থেকে মেনুতে পেজ যোগ করুন।

---

## আটকে গেলে

| সমস্যা | করণীয় |
|---|---|
| client_secret.json নেই | উপরের ধাপ ৪–৫ |
| Access blocked | Test user এ নিজের Gmail যোগ করুন |
| Wrong account | Blogger যে Gmail, সেই দিয়ে Allow করুন |
| Quiz Blogger-এ নষ্ট | `asset_base_url` আগে থেকেই ঠিক আছে (GitHub Pages) |

সেটআপ শেষ হলে বলুন — আমি চেক করে বলব পরের ধাপ।
