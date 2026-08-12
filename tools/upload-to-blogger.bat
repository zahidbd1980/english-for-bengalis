@echo off
setlocal EnableExtensions
cd /d "%~dp0\.."

echo ============================================
echo  English for Bengalis - Blogger Upload
echo  Target: https://englishforbengalis.blogspot.com/
echo ============================================
echo.

where python >nul 2>&1
if errorlevel 1 (
  echo [ERROR] Python not found.
  echo Install from https://www.python.org/downloads/
  echo Enable: Add Python to PATH
  pause
  exit /b 1
)

echo [1/4] Installing Python packages...
python -m pip install -r tools\requirements-blogger.txt
if errorlevel 1 (
  echo [ERROR] pip install failed
  pause
  exit /b 1
)

if not exist "tools\client_secret.json" (
  echo.
  echo [ERROR] Missing tools\client_secret.json
  echo.
  echo Setup steps:
  echo   1. Read docs\BLOGGER_CMD_UPLOAD.md
  echo   2. Create Google OAuth Desktop client JSON
  echo   3. Save it as tools\client_secret.json
  echo.
  pause
  exit /b 1
)

echo.
echo [2/4] Google login (browser opens first time)...
python tools\blogger_upload.py --auth
if errorlevel 1 (
  echo [ERROR] Auth failed
  pause
  exit /b 1
)

echo.
echo [3/4] Uploading welcome post (Blogger homepage featured)...
python tools\blogger_upload.py --upload-welcome
if errorlevel 1 (
  echo [ERROR] Welcome post failed
  pause
  exit /b 1
)

echo.
echo [4/4] Uploading / updating Pages (includes Home landing)...
python tools\blogger_upload.py --upload-pages
if errorlevel 1 (
  echo [ERROR] Pages upload failed
  pause
  exit /b 1
)

echo.
echo ============================================
echo  DONE - Blogger site updated
echo  Live: https://englishforbengalis.blogspot.com/
echo  Home page: https://englishforbengalis.blogspot.com/p/home.html
echo.
echo  Workflow reminder:
echo   1. Edit code in this project
echo   2. git push  (updates GitHub Pages assets)
echo   3. Run this bat again  (updates Blogger pages)
echo.
echo  GitHub Pages is ONLY for css/js/data CDN.
echo ============================================
pause
endlocal
