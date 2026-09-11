@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo [1/4] Installing build dependencies...
python -m pip install -r requirements.txt
python -m pip install pyinstaller
if errorlevel 1 (
    echo pip install failed.
    exit /b 1
)

echo [2/4] Stopping running app (if any)...
taskkill /F /IM CharacterWordCloud.exe >nul 2>&1
ping -n 2 127.0.0.1 >nul

echo [3/4] Cleaning previous build...
if exist build rd /s /q build
if exist dist rd /s /q dist
if exist build goto :clean_fail
if exist dist goto :clean_fail
goto :build

:clean_fail
echo.
echo Clean failed: dist/build is locked.
echo Close CharacterWordCloud.exe and any Explorer window under dist, then retry.
exit /b 1

:build
echo [4/4] Building with PyInstaller...
python -m PyInstaller cwc.spec --noconfirm --clean
if errorlevel 1 (
    echo Build failed.
    exit /b 1
)

echo.
echo Done: dist\CharacterWordCloud\CharacterWordCloud.exe
echo Open that folder manually when needed; do not leave it open during the next build.
