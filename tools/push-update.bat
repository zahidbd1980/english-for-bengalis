@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0\.."
echo Push update to GitHub (repo must already exist)...
echo.

where git >nul 2>&1
if errorlevel 1 (
  echo [ERROR] Git not found.
  pause
  exit /b 1
)

git add -A
git status --short
git diff --cached --quiet
if errorlevel 1 (
  set "MSG=Update site"
  set /p MSG=Commit message [Update site]: 
  if "!MSG!"=="" set "MSG=Update site"
  git commit -m "!MSG!"
  if errorlevel 1 (
    echo [ERROR] commit failed
    pause
    exit /b 1
  )
) else (
  echo No changes to commit.
)

git push
if errorlevel 1 (
  echo [ERROR] Push failed. Run deploy-github-pages.bat first, or check remote.
  pause
  exit /b 1
)

echo.
echo Push OK. GitHub Pages will update in a minute.
pause
endlocal
