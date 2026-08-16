# Blogger Theme apply (high-contrast education chrome)

File: **`themeCode.txt`**  
Backup first: Blogger → Theme → Backup

## What this theme fixes

Screenshot problem: **white title + white menu on light beige** (unreadable).

New shell:
1. Indie stock photo / tall dark hero **removed**
2. **White sticky header** + dark teal brand text (readable)
3. Nav links: muted gray → teal wash on select/hover
4. Soft cream page background + soft green/warm light
5. Content cards with border + light shadow
6. Homepage Featured Post still renders full `index.html` landing

## How to paste

1. Blogger → **Theme** → **Backup**
2. **Theme** → **Edit HTML**
3. Select all → Delete
4. Open project file **`themeCode.txt`** → Copy all
5. Paste → **Save theme**
6. Hard refresh: https://englishforbengalis.blogspot.com/

If save errors: try `themeCode-SAFE.txt`, or restore backup and send the error.

## Optional polish in Blogger

- **Theme → Customize → Blog title**: shorten to `English for Bengalis` (cleaner header)
- **Layout → PageList**: keep Home, Learn, Practice, Quizzes, Daily Challenge, Progress, etc.

## After CSS-only deploy (no theme paste yet)

CDN `learning.css` also forces dark title/nav + hides `.bg-photo`, so contrast improves even before theme paste. Theme paste still required for fonts/variables and a permanent clean shell.
