# Blogger প্রথম — GitHub Pages শুধু asset

## আপনার সাইট কোথায়?

| জায়গা | URL | কাজ |
|--------|-----|-----|
| **Blogger (মূল সাইট)** | https://englishforbengalis.blogspot.com/ | Learners এখানে আসে |
| **GitHub Pages (CDN)** | https://zahidbd1980.github.io/english-for-bengalis/ | css, js, data JSON |

Blogger পেজে quiz/vocabulary/spelling কাজ করে কারণ HTML Blogger-এ, কিন্তু `learning.css`, `app.js`, `vocabulary.json` GitHub Pages থেকে লোড হয়।

## প্রতিবার improvement-এর পর

1. `git push` — GitHub Pages asset আপডেট (১–২ মিনিট)
2. `tools\upload-to-blogger.bat` — Blogger Pages + Welcome post আপডেট

## Home page Blogger-এ

- **Welcome post** = blog homepage (`/`) এ featured landing (index.html থেকে)
- **Home Page** = `/p/home.html` — পূর্ণ landing সরাসরি লিংক

Theme-এ menu-র Home লিংক `/p/home.html` করতে চাইলে: Layout → Pages widget → Home URL বদলান।

## মনে রাখুন

যেকোনো UI, content, SEO improvement **Blogger visitor-দের জন্যই** — GitHub শুধু backend CDN।
