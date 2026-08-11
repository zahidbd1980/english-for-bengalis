@echo off
setlocal EnableExtensions
cd /d "%~dp0\.."

echo ============================================
echo  Blogger setup helper - client_secret.json
echo ============================================
echo.
echo Your blog: https://englishforbengalis.blogspot.com/
echo.
echo Follow these steps IN ORDER.
echo Use the SAME Google account that owns the Blogger blog.
echo.

echo [STEP 1] Opening Google Cloud Console...
start "" "https://console.cloud.google.com/"
echo   - Create or select a project (example name: EnglishForBengalis)
echo.
pause

echo.
echo [STEP 2] Opening Blogger API enable page...
start "" "https://console.cloud.google.com/apis/library/blogger.googleapis.com"
echo   - Click ENABLE
echo.
pause

echo.
echo [STEP 3] Opening OAuth consent screen...
start "" "https://console.cloud.google.com/apis/credentials/consent"
echo   - User type: External
echo   - App name: English for Bengalis
echo   - Add your email as developer + Test user
echo   - Save
echo.
pause

echo.
echo [STEP 4] Opening Credentials page...
start "" "https://console.cloud.google.com/apis/credentials"
echo   - Create Credentials - OAuth client ID
echo   - Application type: Desktop app
echo   - Name: EFB Uploader
echo   - Create - then DOWNLOAD JSON
echo.
pause

echo.
echo [STEP 5] Save the downloaded JSON file here:
echo   %cd%\tools\client_secret.json
echo.
echo IMPORTANT:
echo   - Rename/move the downloaded file to exactly: client_secret.json
echo   - Put it inside the tools folder
echo.
echo Opening tools folder now...
explorer "%cd%\tools"
echo.
pause

if exist "tools\client_secret.json" (
  echo.
  echo FOUND tools\client_secret.json
  echo.
  echo Next: run tools\upload-to-blogger.bat
  echo First time a browser will ask Google permission - click Allow.
  echo.
  set /p RUNNOW=Run upload now? (y/n): 
  if /i "%RUNNOW%"=="y" (
    call tools\upload-to-blogger.bat
  ) else (
    echo OK. Run upload-to-blogger.bat when ready.
    pause
  )
) else (
  echo.
  echo Still missing: tools\client_secret.json
  echo After you save the file, run this helper again OR run upload-to-blogger.bat
  pause
)

endlocal
