# Blogger প্রথম — GitHub Pages শুধু asset

## Home কোথায়? (লক করা সিদ্ধান্ত)

**Home = root URL only.**

`https://englishforbengalis.blogspot.com/`

ওয়েব ইন্ডাস্ট্রিতে homepage মানেই এটা।  
**“Home” নামের Blogger Page (`/p/home.html`) দরকার নেই — রাখা যাবে না।**

| ধরন | URL | Home? |
|------|-----|-------|
| **Blog homepage (root)** | `englishforbengalis.blogspot.com/` | ✅ **এটাই Home** |
| Static Page | `/p/learn.html`, `/p/vocabulary.html` | ❌ |
| Welcome post | `/2026/08/welcome-...` | Featured content for root |
| Page titled “Home” | `/p/home.html` | ❌ **Forbidden / auto-deleted** |

Menu-র **Home** লিংক = blog root `/` (কখনো `/p/home.html` নয়)।

## Root-এ কী দেখাবে?

Theme-এর **Featured Post** = Welcome post — এবং সেটা **full body** দেখাতে হবে (snippet/excerpt নয়)।  
`themeCode.txt`-এ এটা লক করা আছে; Blogger-এ Theme HTML paste করতে হবে (`docs/HOME_ROOT_DESIGN_FIX.md`)।

## GitHub Pages কেন?

| জায়গা | URL | কাজ |
|--------|-----|-----|
| **Blogger** | https://englishforbengalis.blogspot.com/ | Learners এখানে |
| **GitHub Pages** | zahidbd1980.github.io/english-for-bengalis/ | css, js, data JSON (CDN) |

## প্রতিবার update

1. `git push` — assets  
2. `tools\upload-to-blogger.bat` — Welcome + Pages  

Home fix (যদি আবার `/p/home.html` দেখা যায়):

```text
python tools/blogger_upload.py --fix-home
```

এটা leftover Home Page **মুছে** দেয় + Welcome refresh করে।

## Dashboard

Pages তালিকায় “Home” দেখলে Delete — অথবা উপরের `--fix-home` চালান।  
Config-এ কখনো `"title": "Home"` যোগ করবেন না।
