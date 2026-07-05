Bolt AutoClicker
================

A simple Windows autoclicker inspired by the classic GT Auto Clicker layout.

Features
--------
- Repeat forever or repeat a specific number of times.
- Mouse mode with left, right, or middle button.
- Single-click or double-click for mouse mode.
- Keyboard mode for sending one key repeatedly.
- Interval controls for hours, minutes, seconds, and milliseconds.
- Fastest possible mode.
- Current cursor position mode or fixed X/Y position mode.
- Start, Stop, and Off buttons.
- Save Settings, Reset Settings, and Change Hotkeys buttons.
- Global hotkeys. Defaults are F1 start, F2 stop, F3 toggle.
- No GitHub auto-updater.

Run From Source
---------------
python .\bolt_autoclicker.py

Build One EXE Like CodeHub
--------------------------
AppUpdater.bat

The release file will be:
BoltAutoClicker.exe

Publish Source To GitHub Repo
-----------------------------
Github.bat

Publish GitHub Release EXE
--------------------------
Github Release.bat

Expected repo folder:
F:\Github\repos\codex\bolt-autoclicker

Notes
-----
Settings save beside the app as bolt_settings.json. When compiled as one EXE,
the JSON file will be created next to BoltAutoClicker.exe.
