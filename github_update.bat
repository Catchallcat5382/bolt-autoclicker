@echo off
setlocal EnableExtensions
color 0A
title Bolt AutoClicker GitHub Updater
cd /d "%~dp0"

echo ==========================================================
echo              BOLT AUTOCLICKER GITHUB UPDATER
echo ==========================================================
echo.

git --version >nul 2>&1
if errorlevel 1 (
    echo [FAIL] Git is not installed or not on PATH.
    pause
    exit /b 1
)

if not exist ".git" (
    echo [FAIL] This folder is not a Git repository.
    pause
    exit /b 1
)

echo [GITIGNORE] Writing personal publish ignore rules...
(
echo # Python
echo __pycache__/
echo *.pyc
echo *.py[cod]
echo.
echo # Build folders
echo build/
echo build_out/
echo dist/
echo *.spec
echo BoltAutoClicker.spec
echo BoltAutoClicker.exe
echo.
echo # Runtime settings/logs
echo bolt_settings.json
echo publish_log.txt
echo *.log
echo .env
echo.
echo # Personal-only scripts/folders
echo Github.bat
echo "Github Release.bat"
echo github_update.bat
echo releases/
echo.
echo # Windows junk
echo Thumbs.db
echo Desktop.ini
echo *.lnk
) > ".gitignore"

echo [CLEAN] Removing local-only files from the repo worktree...
for %%F in (
    "README.txt"
    "Github.bat"
    "Github Release.bat"
    "publish_log.txt"
    "BoltAutoClicker.spec"
    "BoltAutoClicker.exe"
) do (
    del /f /q "%%~F" >nul 2>&1
)

for %%D in (
    "build"
    "build_out"
    "dist"
    "__pycache__"
    "releases"
) do (
    rmdir /s /q "%%~D" >nul 2>&1
)

git rm -r --cached build build_out dist __pycache__ releases README.txt BoltAutoClicker.exe BoltAutoClicker.spec Github.bat "Github Release.bat" publish_log.txt >nul 2>&1

echo [GIT] Staging files...
git add -A

echo.
echo [GIT] Pending changes:
git status --short
echo.

git diff --cached --quiet
if not errorlevel 1 (
    echo [DONE] Nothing to commit.
    timeout /t 2 /nobreak >nul
    exit /b 0
)

set /p MSG=Commit message: 
if "%MSG%"=="" set "MSG=Bolt AutoClicker update"

echo [GIT] Committing...
git commit -m "%MSG%"
if errorlevel 1 (
    echo [FAIL] Commit failed.
    pause
    exit /b 1
)

echo [GIT] Pushing to origin/main...
git push origin main
if errorlevel 1 (
    echo [FAIL] Push failed.
    pause
    exit /b 1
)

echo.
echo [DONE] GitHub updated successfully.
timeout /t 2 /nobreak >nul
exit /b 0