@echo off
setlocal EnableExtensions
cd /d "%~dp0\.."
echo Draft mode upload (items created as drafts)...
python -m pip install -r tools\requirements-blogger.txt
if errorlevel 1 (
  echo [ERROR] pip install failed
  pause
  exit /b 1
)
if not exist "tools\client_secret.json" (
  echo [ERROR] Missing tools\client_secret.json
  pause
  exit /b 1
)
python tools\blogger_upload.py --auth
if errorlevel 1 goto :fail
python tools\blogger_upload.py --upload-welcome --draft
if errorlevel 1 goto :fail
python tools\blogger_upload.py --upload-pages --draft
if errorlevel 1 goto :fail
echo.
echo Drafts created. Publish them from Blogger Dashboard.
pause
endlocal
exit /b 0

:fail
echo [ERROR] Upload failed
pause
endlocal
exit /b 1
