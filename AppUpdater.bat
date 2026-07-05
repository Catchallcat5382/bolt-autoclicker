@echo off
setlocal EnableExtensions
color 0A
title Bolt AutoClicker Updater
cd /d "%~dp0"

set "PYTHON_EXE=python"
set "APP_EXE=BoltAutoClicker.exe"
set "NEW_EXE=BoltAutoClicker_new.exe"
set "BUILD_PS1=build.ps1"

echo ==========================================================
echo              BOLT AUTOCLICKER APP UPDATER
echo ==========================================================
echo.

if not exist "bolt_autoclicker.py" (
    echo [FAIL] Missing bolt_autoclicker.py
    pause
    exit /b 1
)

if not exist "assets\bolt_autoclicker.ico" if not exist "extra\bolt_autoclicker.ico" (
    echo [FAIL] Missing icon file. Expected assets\bolt_autoclicker.ico or extra\bolt_autoclicker.ico
    pause
    exit /b 1
)

if not exist "%BUILD_PS1%" (
    echo [FAIL] Missing build.ps1
    pause
    exit /b 1
)

echo [CLEAN] Closing old app...
taskkill /f /im "%APP_EXE%" >nul 2>&1
timeout /t 1 /nobreak >nul

echo [CLEAN] Removing old build files...
rmdir /s /q "build" >nul 2>&1
rmdir /s /q "dist" >nul 2>&1
rmdir /s /q "build_out" >nul 2>&1
del /f /q "BoltAutoClicker.spec" >nul 2>&1
del /f /q "BoltAutoClicker_new.spec" >nul 2>&1
del /f /q "%NEW_EXE%" >nul 2>&1

echo.
echo [REQ] Installing requirements...
if exist "requirements.txt" (
    "%PYTHON_EXE%" -m pip install -r "requirements.txt"
    if errorlevel 1 goto fail
)

echo.
echo [REQ] Making sure PyInstaller is installed...
"%PYTHON_EXE%" -m pip install pyinstaller
if errorlevel 1 goto fail

echo.
echo [BUILD] Running build.ps1...
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0%BUILD_PS1%"
if errorlevel 1 goto fail

if not exist "%NEW_EXE%" (
    echo [FAIL] New exe was not created:
    echo %CD%\%NEW_EXE%
    pause
    exit /b 1
)

echo.
echo [UPDATE] Replacing exact main exe...
del /f /q "%APP_EXE%" >nul 2>&1

if exist "%APP_EXE%" (
    echo [FAIL] Old exe is still locked.
    pause
    exit /b 1
)

move /y "%NEW_EXE%" "%APP_EXE%" >nul
if errorlevel 1 goto fail

if exist "F:\Auto Hotkey\Python\Apps" (
    echo [UPDATE] Copying to Apps folder...
    copy /y "%APP_EXE%" "F:\Auto Hotkey\Python\Apps\BoltAutoClicker.exe" >nul
)

echo.
echo [DONE] Updated:
dir "%APP_EXE%"

echo.
echo [RUN] Opening exact rebuilt exe...
start "" "%CD%\%APP_EXE%"

timeout /t 1 /nobreak >nul
exit /b 0

:fail
echo.
echo [FAIL] AppUpdater failed.
pause
exit /b 1
