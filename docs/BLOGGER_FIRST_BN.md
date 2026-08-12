# Blogger প্রথম — GitHub Pages শুধু asset

## Home কোথায়? (সহজ উত্তর)

**হ্যাঁ — আপনি ঠিক বলেছেন।**

User যখন address bar-এ লিখবে:

`https://englishforbengalis.blogspot.com/`

তখন যা খুলবে **সেটাই Home**। Blogger-এ এটাকে **blog homepage** বলে (`blog.homepageUrl`).

**আলাদা “Home” নামের Page (`/p/home.html`) home নয়** — এটা শুধু একটা static page, URL আলাদা। সাধারণত **দরকার নেই**।

## Blogger-এ ৩ ধরনের URL

| ধরন | উদাহরণ | কী |
|------|--------|-----|
| **Home (blog index)** | `englishforbengalis.blogspot.com/` | Address bar URL = এটাই home |
| **Static Page** | `/p/learn.html`, `/p/vocabulary.html` | Learn, Vocabulary ইত্যাদি |
| **Blog Post** | `/2026/08/welcome-...html` | Welcome post, future articles |

Menu-র **“Home”** লিংক theme-এ সাধারণত `englishforbengalis.blogspot.com/` — সেটা সঠিক।

## আমাদের home-এ কী দেখাবে?

আপনার Indie theme-এ homepage-এ **Featured Post** widget আছে।  
আমরা **Welcome post**-এ `index.html` landing content upload করি — সেটা featured হলে visitor root URL-এ landing দেখে।

নিচে theme অনুযায়ী আরও post list থাকতে পারে (Welcome post list-এ duplicate না দেখানোর logic theme-এ আছে).

## GitHub Pages কেন?

| জায়গা | URL | কাজ |
|--------|-----|-----|
| **Blogger** | https://englishforbengalis.blogspot.com/ | Learners এখানে |
| **GitHub Pages** | zahidbd1980.github.io/english-for-bengalis/ | css, js, data JSON (CDN) |

## প্রতিবার update

1. `git push` — assets
2. `tools\upload-to-blogger.bat` — Welcome post + Pages (Home Page upload **না**)

## Optional (শুধু যদি চান)

Blogger Settings → Search preferences → Custom redirects:

- From: `/`
- To: `/p/some-landing.html`
- Permanent 301

এটা root URL থেকে static page-এ redirect — **default দরকার নেই** যদি Featured Welcome post ঠিকমতো দেখায়।

## Dashboard cleanup

যদি “Home” নামে Page (`/p/home.html`) তৈরি হয়ে গেছে — **Pages → Home → Delete** করতে পারেন। Menu-তে Home রাখুন blog root (`/`) লিংকে।

`upload-welcome` এখন দেখতে পারলে সেই leftover Home Page-কে **latest `index.html` দিয়ে sync** করে দেয় (যাতে menu ভুল URL-এ গেলেও পুরনো landing না দেখায়)। তবু canonical home = **root URL + Featured Welcome**।
