# Root homepage design fix (Featured Post full body)

## Problem
Indie theme `FeaturedPost1` was set to **snippet mode**.  
Root URL showed a truncated “Welcome” card (“Keep reading”), not the designed `index.html` landing.

## Fix in `themeCode.txt`
- Featured Post renders **full** `<data:post.body/>` (Welcome HTML)
- Hide title / byline / “Keep reading” on homepage featured
- CSS: `.efb-featured-full` for full-width landing

## You must apply theme in Blogger
API cannot paste theme safely from here every time — apply once:

1. Blogger → **Theme** → **Backup** (save copy)
2. **Theme** → **Edit HTML**
3. Select all → replace with project file **`themeCode.txt`**
4. **Save theme**
5. Hard refresh: https://englishforbengalis.blogspot.com/

## Still true
- Home = **root URL only** (no `/p/home.html` Page)
- Landing content = Welcome post body (`index.html` via `--upload-welcome`)
