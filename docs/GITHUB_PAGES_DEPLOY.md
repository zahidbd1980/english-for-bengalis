# GitHub Pages Deploy (BAT)

> Note: All `.bat` files use **English/ASCII only**. Bangla text inside BAT breaks Windows CMD encoding (causes errors like `'xit' is not recognized`).

## One click

```text
tools\deploy-github-pages.bat
```

What it does:
1. Checks Git  
2. Asks GitHub username + repo name (**do not leave username empty**)  
3. Commit + push (`gh` CLI creates repo + enables Pages if installed)  
4. Sets `asset_base_url` in `tools/blogger_config.json`  

Site URL: `https://YOUR_USER.github.io/REPO_NAME/`

## Later updates

```text
tools\push-update.bat
```

## Blogger + Pages together

1. `deploy-github-pages.bat` first  
2. Then `upload-to-blogger.bat`  

## Requirements

- Git: https://git-scm.com/download/win  
- Recommended: GitHub CLI https://cli.github.com/  
- Python (for `set_pages_url.py`)  

Blogger guide: `docs/BLOGGER_CMD_UPLOAD.md`
