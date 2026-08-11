@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0\.."

echo ============================================
echo  Deploy to GitHub Pages
echo  English for Bengalis MVP
echo ============================================
echo.
echo This script will push the project to GitHub Pages.
echo Need: GitHub account + Git installed.
echo Git download: https://git-scm.com/download/win
echo.

where git >nul 2>&1
if errorlevel 1 (
  echo [ERROR] Git not found.
  echo Install from https://git-scm.com/download/win
  pause
  exit /b 1
)

where gh >nul 2>&1
set "HAS_GH=0"
if not errorlevel 1 set "HAS_GH=1"

set "GH_USER="
set /p GH_USER=Enter GitHub username: 
if "!GH_USER!"=="" (
  echo [ERROR] Username cannot be empty.
  pause
  exit /b 1
)

set "REPO_NAME="
set /p REPO_NAME=Enter repository name [english-for-bengalis]: 
if "!REPO_NAME!"=="" set "REPO_NAME=english-for-bengalis"

set "PAGES_URL=https://!GH_USER!.github.io/!REPO_NAME!"
echo.
echo Pages URL will be: !PAGES_URL!/
echo.

if not exist ".git" (
  echo [1] git init...
  git init
  git branch -M main
) else (
  echo [1] .git already exists
)

echo.
echo [2] Staging files + commit...
git add -A
git status --short

git diff --cached --quiet
if errorlevel 1 (
  git commit -m "Deploy English for Bengalis MVP to GitHub Pages"
) else (
  echo No new changes to commit. Continuing...
)

echo.
echo [3] Remote / Push...

if "!HAS_GH!"=="1" (
  echo GitHub CLI found.
  gh auth status >nul 2>&1
  if errorlevel 1 (
    echo Login required...
    gh auth login
  )

  gh repo view "!GH_USER!/!REPO_NAME!" >nul 2>&1
  if errorlevel 1 (
    echo Creating repo: !GH_USER!/!REPO_NAME!
    gh repo create "!GH_USER!/!REPO_NAME!" --public --source=. --remote=origin --push
    if errorlevel 1 (
      echo [ERROR] gh repo create failed.
      pause
      exit /b 1
    )
  ) else (
    echo Repo exists. Pushing to origin...
    git remote remove origin >nul 2>&1
    git remote add origin "https://github.com/!GH_USER!/!REPO_NAME!.git"
    git push -u origin main
    if errorlevel 1 (
      echo [ERROR] git push failed.
      pause
      exit /b 1
    )
  )

  echo.
  echo [4] Enabling GitHub Pages on main branch root...
  gh api -X POST "repos/!GH_USER!/!REPO_NAME!/pages" -f "build_type=legacy" -f "source[branch]=main" -f "source[path]=/" >nul 2>&1
  if errorlevel 1 (
    gh api -X PUT "repos/!GH_USER!/!REPO_NAME!/pages" -f "build_type=legacy" -f "source[branch]=main" -f "source[path]=/" >nul 2>&1
  )
  echo Pages enable request sent.
) else (
  echo.
  echo GitHub CLI ^(gh^) not found. Manual steps:
  echo   1. Create public repo: https://github.com/new  name=!REPO_NAME!
  echo   2. Run these commands:
  echo      git remote remove origin
  echo      git remote add origin https://github.com/!GH_USER!/!REPO_NAME!.git
  echo      git push -u origin main
  echo   3. GitHub - Settings - Pages - Branch main - Folder /root - Save
  echo.
  set "MANUAL="
  set /p MANUAL=Did you create repo and push already? ^(y/n^): 
  if /i not "!MANUAL!"=="y" (
    echo Run this BAT again after push.
    pause
    exit /b 0
  )
)

echo.
echo [5] Writing asset_base_url into blogger_config.json...
where python >nul 2>&1
if errorlevel 1 (
  echo [WARN] Python not found. Set manually in tools\blogger_config.json
  echo   "asset_base_url": "!PAGES_URL!"
) else (
  python tools\set_pages_url.py --user "!GH_USER!" --repo "!REPO_NAME!" --write-config
  if errorlevel 1 (
    echo [WARN] Could not update config. Set manually:
    echo   "asset_base_url": "!PAGES_URL!"
  )
)

echo.
echo ============================================
echo  DONE
echo ============================================
echo  Site (wait 1-2 minutes): !PAGES_URL!/
echo.
echo  Next for Blogger quizzes:
echo    tools\upload-to-blogger.bat
echo.
echo  GitHub repo:
echo    https://github.com/!GH_USER!/!REPO_NAME!
echo ============================================
pause
endlocal
