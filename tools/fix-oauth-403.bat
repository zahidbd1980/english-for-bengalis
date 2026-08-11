@echo off
setlocal EnableExtensions
cd /d "%~dp0\.."

echo ============================================
echo  FIX: OAuth 403 access_denied / Test users
echo ============================================
echo.
echo Your Google Cloud project_id:
echo   cobalt-mantis-272505
echo.
echo Your tester email MUST be added:
echo   zahidbd1980@gmail.com
echo.
echo Opening the correct Audience / Test users page...
start "" "https://console.cloud.google.com/auth/audience?project=cobalt-mantis-272505"
echo.
echo ON THAT PAGE DO THIS:
echo   1. Publishing status = Testing  (NOT In production)
echo   2. Click "+ Add users" under Test users
echo   3. Add: zahidbd1980@gmail.com
echo   4. Save
echo.
echo Also open Branding/consent if needed:
start "" "https://console.cloud.google.com/auth/overview?project=cobalt-mantis-272505"
echo.
pause

echo.
echo Optional: open old consent screen path too...
start "" "https://console.cloud.google.com/apis/credentials/consent?project=cobalt-mantis-272505"
echo.
echo After Save, wait 1-2 minutes.
echo Then use Chrome Incognito, login ONLY as zahidbd1980@gmail.com
echo.
pause

echo.
echo Running auth again...
if exist "tools\token.json" del "tools\token.json"
python -m pip install -r tools\requirements-blogger.txt >nul
python tools\blogger_upload.py --auth
if errorlevel 1 (
  echo.
  echo Still failed. Check:
  echo  - Test user saved under project cobalt-mantis-272505
  echo  - Incognito only with zahidbd1980@gmail.com
  echo  - Advanced - Go to app - Allow
  pause
  exit /b 1
)

echo.
echo AUTH OK. Upload pages now? 
set /p GO=Type y to upload: 
if /i "%GO%"=="y" (
  python tools\blogger_upload.py --upload-welcome
  python tools\blogger_upload.py --upload-pages
)

echo.
echo Done or stopped.
pause
endlocal
