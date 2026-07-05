@echo off
setlocal
color 0A
title Bolt AutoClicker Updater
cd /d "%~dp0"

set "PYTHON_EXE=python"
python --version >nul 2>&1
if errorlevel 1 (
    if exist "C:\Users\ilans\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" (
        set "PYTHON_EXE=C:\Users\ilans\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
    )
)

echo [Bolt AutoClicker] checking source tree...
echo [Bolt AutoClicker] installing/updating build requirements...
"%PYTHON_EXE%" -m pip install -r "%~dp0requirements.txt"
if errorlevel 1 (
    echo [Bolt AutoClicker] requirement install failed.
    pause
    exit /b 1
)

echo [Bolt AutoClicker] building single-file executable...
powershell.exe -ExecutionPolicy Bypass -File "%~dp0build.ps1"
if errorlevel 1 (
    echo [Bolt AutoClicker] build failed.
    pause
    exit /b 1
)

echo [Bolt AutoClicker] updating local copy...
copy /y "%~dp0build_out\dist\BoltAutoClicker.exe" "%~dp0BoltAutoClicker.exe" >nul

if exist "F:\Auto Hotkey\Python\Apps" (
    echo [Bolt AutoClicker] updating Apps copy...
    copy /y "%~dp0build_out\dist\BoltAutoClicker.exe" "F:\Auto Hotkey\Python\Apps\BoltAutoClicker.exe" >nul
)

echo [Bolt AutoClicker] done.
exit /b 0
