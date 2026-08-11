@echo off
setlocal EnableExtensions
cd /d "%~dp0\.."
echo Listing Blogger pages/posts...
python tools\blogger_upload.py --list
pause
endlocal
