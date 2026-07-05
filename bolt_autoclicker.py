from __future__ import annotations

import ctypes
import json
import sys
import threading
import time
from ctypes import wintypes
from dataclasses import asdict, dataclass
from pathlib import Path


APP_NAME = "Bolt AutoClicker"
SETTINGS_FILE = "bolt_settings.json"
ASSETS_FOLDER = "assets"
EXTRA_FOLDER = "extra"
APP_ICO_FILE = "bolt_autoclicker.ico"
APP_LOGO_PNG_FILE = "bolt_autoclicker_logo.png"
APP_HEADER_BMP_FILE = "bolt_autoclicker_header.bmp"
APP_AUMID = "Bolt.AutoClicker.App"

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
kernel32 = ctypes.windll.kernel32
shell32 = ctypes.windll.shell32
LRESULT = wintypes.LPARAM

def MAKEINTRESOURCEW(resource_id: int) -> wintypes.LPCWSTR:
    return ctypes.cast(ctypes.c_void_p(resource_id), wintypes.LPCWSTR)

user32.DefWindowProcW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
user32.DefWindowProcW.restype = LRESULT
user32.CreateWindowExW.argtypes = [
    wintypes.DWORD,
    wintypes.LPCWSTR,
    wintypes.LPCWSTR,
    wintypes.DWORD,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    wintypes.HWND,
    wintypes.HMENU,
    wintypes.HINSTANCE,
    wintypes.LPVOID,
]
user32.CreateWindowExW.restype = wintypes.HWND
user32.RegisterClassExW.argtypes = [ctypes.c_void_p]
user32.RegisterClassExW.restype = wintypes.ATOM
shell32.SetCurrentProcessExplicitAppUserModelID.argtypes = [wintypes.LPCWSTR]
shell32.SetCurrentProcessExplicitAppUserModelID.restype = ctypes.c_long
kernel32.GetModuleHandleW.argtypes = [wintypes.LPCWSTR]
kernel32.GetModuleHandleW.restype = wintypes.HINSTANCE
user32.SendMessageW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
user32.SendMessageW.restype = LRESULT
user32.LoadCursorW.argtypes = [wintypes.HINSTANCE, wintypes.LPCWSTR]
user32.LoadCursorW.restype = wintypes.HANDLE
user32.LoadIconW.argtypes = [wintypes.HINSTANCE, wintypes.LPCWSTR]
user32.LoadIconW.restype = wintypes.HANDLE
user32.DestroyWindow.argtypes = [wintypes.HWND]
user32.DestroyWindow.restype = wintypes.BOOL
user32.LoadImageW.argtypes = [wintypes.HINSTANCE, wintypes.LPCWSTR, wintypes.UINT, ctypes.c_int, ctypes.c_int, wintypes.UINT]
user32.LoadImageW.restype = wintypes.HANDLE
user32.SetWindowPos.argtypes = [wintypes.HWND, wintypes.HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, wintypes.UINT]
user32.SetWindowPos.restype = wintypes.BOOL
user32.GetClientRect.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.RECT)]
user32.GetClientRect.restype = wintypes.BOOL
user32.SetScrollInfo.argtypes = [wintypes.HWND, ctypes.c_int, ctypes.c_void_p, wintypes.BOOL]
user32.SetScrollInfo.restype = ctypes.c_int
user32.RegisterHotKey.argtypes = [wintypes.HWND, ctypes.c_int, wintypes.UINT, wintypes.UINT]
user32.UnregisterHotKey.argtypes = [wintypes.HWND, ctypes.c_int]
gdi32.SetBkMode.argtypes = [wintypes.HDC, ctypes.c_int]
gdi32.SetTextColor.argtypes = [wintypes.HDC, wintypes.COLORREF]

WM_DESTROY = 0x0002
WM_COMMAND = 0x0111
WM_CTLCOLORSTATIC = 0x0138
WM_HOTKEY = 0x0312
WM_SIZE = 0x0005
WM_VSCROLL = 0x0115
WM_MOUSEWHEEL = 0x020A
WM_SETFONT = 0x0030
WM_SETICON = 0x0080
WM_CLOSE = 0x0010
BM_SETCHECK = 0x00F1
BM_GETCHECK = 0x00F0
BST_CHECKED = 1
CB_ADDSTRING = 0x0143
CB_SETCURSEL = 0x014E
CB_GETCURSEL = 0x0147
CB_GETLBTEXT = 0x0148
CB_GETLBTEXTLEN = 0x0149
ES_NUMBER = 0x2000
WS_OVERLAPPED = 0x00000000
WS_CAPTION = 0x00C00000
WS_SYSMENU = 0x00080000
WS_MINIMIZEBOX = 0x00020000
WS_THICKFRAME = 0x00040000
WS_MAXIMIZEBOX = 0x00010000
WS_VSCROLL = 0x00200000
WS_EX_DLGMODALFRAME = 0x00000001
WS_VISIBLE = 0x10000000
WS_CHILD = 0x40000000
WS_TABSTOP = 0x00010000
WS_GROUP = 0x00020000
WS_BORDER = 0x00800000
BS_PUSHBUTTON = 0x00000000
BS_DEFPUSHBUTTON = 0x00000001
BS_AUTORADIOBUTTON = 0x00000009
BS_AUTOCHECKBOX = 0x00000003
BS_GROUPBOX = 0x00000007
CBS_DROPDOWNLIST = 0x0003
SS_LEFT = 0x00000000
SS_CENTERIMAGE = 0x00000200
SS_ICON = 0x00000003
SS_BITMAP = 0x0000000E
STM_SETICON = 0x0170
STM_SETIMAGE = 0x0172
IMAGE_BITMAP = 0
IMAGE_ICON = 1
LR_LOADFROMFILE = 0x0010
LR_DEFAULTSIZE = 0x0040
SWP_NOZORDER = 0x0004
SWP_NOACTIVATE = 0x0010
SB_VERT = 1
SB_LINEUP = 0
SB_LINEDOWN = 1
SB_PAGEUP = 2
SB_PAGEDOWN = 3
SB_THUMBPOSITION = 4
SB_THUMBTRACK = 5
SIF_RANGE = 0x0001
SIF_PAGE = 0x0002
SIF_POS = 0x0004
SIF_ALL = SIF_RANGE | SIF_PAGE | SIF_POS
ICON_SMALL = 0
ICON_BIG = 1
COLOR_WINDOW = 5
BG_COLORREF = 0xE8E8E8
TEXT_COLORREF = 0x222222
WARN_COLORREF = 0x0000CC
CONTENT_HEIGHT = 675
IDI_APPLICATION = 32512
MODIFIERS = {"ALT": 0x0001, "CTRL": 0x0002, "SHIFT": 0x0004, "WIN": 0x0008}

VK_CODES = {
    "BACKSPACE": 0x08,
    "TAB": 0x09,
    "ENTER": 0x0D,
    "SHIFT": 0x10,
    "CTRL": 0x11,
    "ALT": 0x12,
    "PAUSE": 0x13,
    "CAPSLOCK": 0x14,
    "ESC": 0x1B,
    "SPACE": 0x20,
    "PAGEUP": 0x21,
    "PAGEDOWN": 0x22,
    "END": 0x23,
    "HOME": 0x24,
    "LEFT": 0x25,
    "UP": 0x26,
    "RIGHT": 0x27,
    "DOWN": 0x28,
    "INSERT": 0x2D,
    "DELETE": 0x2E,
}
for index in range(10):
    VK_CODES[f"NUMPAD{index}"] = 0x60 + index

for index in range(1, 25):
    VK_CODES[f"F{index}"] = 0x6F + index
for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
    VK_CODES[char] = ord(char)


def app_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent




def bundle_dir() -> Path:
    """PyInstaller extraction folder when bundled, otherwise the script folder."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    return app_dir()


def assets_candidates() -> list[Path]:
    """Search both beside the exe/script and inside a PyInstaller bundle."""
    seen: list[Path] = []
    for base in (app_dir(), bundle_dir()):
        candidate = base / ASSETS_FOLDER
        if candidate not in seen:
            seen.append(candidate)
    return seen


def assets_dir() -> Path:
    """Finished icon/logo assets live here. No make_icon.py, no source image required."""
    return assets_candidates()[0]


def asset_path(filename: str) -> Path | None:
    search_roots = []

    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        search_roots.append(Path(sys._MEIPASS))

    search_roots.append(app_dir())

    for root in search_roots:
        candidate = root / ASSETS_FOLDER / filename
        if candidate.exists():
            return candidate

    return None


def extra_asset_path(filename: str) -> Path | None:
    search_roots = []

    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        search_roots.append(Path(sys._MEIPASS))

    search_roots.append(app_dir())

    for root in search_roots:
        candidate = root / EXTRA_FOLDER / filename
        if candidate.exists():
            return candidate

    return None


class SCROLLINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.UINT),
        ("fMask", wintypes.UINT),
        ("nMin", ctypes.c_int),
        ("nMax", ctypes.c_int),
        ("nPage", wintypes.UINT),
        ("nPos", ctypes.c_int),
        ("nTrackPos", ctypes.c_int),
    ]

def normalize_key_name(value: str) -> str:
    value = value.strip().upper().replace(" ", "")
    aliases = {
        "ESCAPE": "ESC",
        "RETURN": "ENTER",
        "PGUP": "PAGEUP",
        "PGDN": "PAGEDOWN",
        "DEL": "DELETE",
        "INS": "INSERT",
        "CONTROL": "CTRL",
    }
    return aliases.get(value, value)


def parse_hotkey(text: str) -> tuple[int, int] | None:
    parts = [normalize_key_name(part) for part in text.split("+") if part.strip()]
    if not parts:
        return None
    modifiers = 0
    key = None
    for part in parts:
        if part in MODIFIERS:
            modifiers |= MODIFIERS[part]
        else:
            key = part
    if key is None or key not in VK_CODES:
        return None
    return modifiers, VK_CODES[key]


@dataclass
class Settings:
    hours: int = 0
    minutes: int = 0
    seconds: int = 0
    milliseconds: int = 100
    fastest: bool = False
    repeat_mode: str = "forever"
    repeat_count: int = 100
    action_type: str = "mouse"
    mouse_button: str = "left"
    click_count: str = "single"
    key_name: str = "SPACE"
    position_mode: str = "current"
    x: int = 0
    y: int = 0
    start_hotkey: str = "F1"
    stop_hotkey: str = "F2"
    toggle_hotkey: str = "F3"
    exit_hotkey: str = "NUMPAD5"


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


class MSG(ctypes.Structure):
    _fields_ = [
        ("hwnd", wintypes.HWND),
        ("message", wintypes.UINT),
        ("wParam", wintypes.WPARAM),
        ("lParam", wintypes.LPARAM),
        ("time", wintypes.DWORD),
        ("pt", POINT),
    ]


class WNDCLASSEX(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.UINT),
        ("style", wintypes.UINT),
        ("lpfnWndProc", ctypes.c_void_p),
        ("cbClsExtra", ctypes.c_int),
        ("cbWndExtra", ctypes.c_int),
        ("hInstance", wintypes.HINSTANCE),
        ("hIcon", wintypes.HANDLE),
        ("hCursor", wintypes.HANDLE),
        ("hbrBackground", wintypes.HANDLE),
        ("lpszMenuName", wintypes.LPCWSTR),
        ("lpszClassName", wintypes.LPCWSTR),
        ("hIconSm", wintypes.HANDLE),
    ]


user32.RegisterClassExW.argtypes = [ctypes.POINTER(WNDCLASSEX)]
user32.RegisterClassExW.restype = wintypes.ATOM


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
    ]


class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
    ]


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong), ("wParamL", ctypes.c_short), ("wParamH", ctypes.c_ushort)]


class INPUT_UNION(ctypes.Union):
    _fields_ = [("mi", MOUSEINPUT), ("ki", KEYBDINPUT), ("hi", HARDWAREINPUT)]


class INPUT(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("union", INPUT_UNION)]


class WinInput:
    INPUT_MOUSE = 0
    INPUT_KEYBOARD = 1
    KEYEVENTF_KEYUP = 0x0002
    MOUSEEVENTF_LEFTDOWN = 0x0002
    MOUSEEVENTF_LEFTUP = 0x0004
    MOUSEEVENTF_RIGHTDOWN = 0x0008
    MOUSEEVENTF_RIGHTUP = 0x0010
    MOUSEEVENTF_MIDDLEDOWN = 0x0020
    MOUSEEVENTF_MIDDLEUP = 0x0040
    BUTTON_FLAGS = {
        "left": (MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP),
        "right": (MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP),
        "middle": (MOUSEEVENTF_MIDDLEDOWN, MOUSEEVENTF_MIDDLEUP),
    }

    def get_position(self) -> tuple[int, int]:
        point = POINT()
        user32.GetCursorPos(ctypes.byref(point))
        return point.x, point.y

    def set_position(self, x: int, y: int) -> None:
        user32.SetCursorPos(int(x), int(y))

    def click(self, button: str, times: int) -> None:
        down, up = self.BUTTON_FLAGS[button]
        for _ in range(times):
            self._mouse_event(down)
            self._mouse_event(up)

    def key_press(self, key_name: str) -> None:
        vk = VK_CODES.get(normalize_key_name(key_name))
        if vk is None:
            return
        self._keyboard_event(vk, 0)
        self._keyboard_event(vk, self.KEYEVENTF_KEYUP)

    def _mouse_event(self, flags: int) -> None:
        inp = INPUT(type=self.INPUT_MOUSE, union=INPUT_UNION(mi=MOUSEINPUT(0, 0, 0, flags, 0, None)))
        user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT))

    def _keyboard_event(self, vk: int, flags: int) -> None:
        inp = INPUT(type=self.INPUT_KEYBOARD, union=INPUT_UNION(ki=KEYBDINPUT(vk, 0, flags, 0, None)))
        user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT))


class NativeApp:
    def __init__(self) -> None:
        self.set_app_user_model_id()
        self.instance = kernel32.GetModuleHandleW(None)
        self.class_name = "BoltAutoClickerWindow"
        self.settings_path = app_dir() / SETTINGS_FILE
        self.settings = self.load_settings()
        self.input = WinInput()
        self.stop_event = threading.Event()
        self.worker: threading.Thread | None = None
        self.controls: dict[str, wintypes.HWND] = {}
        self.child_layout: dict[int, tuple[int, int, int, int]] = {}
        self.warning_labels: set[int] = set()
        self.scroll_y = 0
        self.hotkey_controls: dict[str, wintypes.HWND] = {}
        self.hotkey_hwnd: wintypes.HWND | None = None
        self.wndproc_ref = ctypes.WINFUNCTYPE(LRESULT, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)(self.wndproc)
        self.font = gdi32.CreateFontW(18, 0, 0, 0, 400, 0, 0, 0, 1, 0, 0, 0, 0, "Segoe UI")
        self.bold_font = gdi32.CreateFontW(25, 0, 0, 0, 700, 0, 0, 0, 1, 0, 0, 0, 0, "Segoe UI")
        self.bg_brush = gdi32.CreateSolidBrush(BG_COLORREF)
        self.app_icon = self.load_app_icon(64)
        self.app_icon_small = self.load_app_icon(16)
        self.register_class()
        self.hwnd = self.create_window()
        self.build_controls()
        self.update_scrollbar()
        self.apply_settings(self.settings)
        self.register_hotkeys()
        self.set_status("Ready.")

    def set_app_user_model_id(self) -> None:
        # Makes Windows group this app correctly on the taskbar and helps it use this app's icon.
        try:
            shell32.SetCurrentProcessExplicitAppUserModelID(APP_AUMID)
        except Exception:
            pass

    def register_class(self) -> None:
        wc = WNDCLASSEX()
        wc.cbSize = ctypes.sizeof(WNDCLASSEX)
        wc.lpfnWndProc = ctypes.cast(self.wndproc_ref, ctypes.c_void_p)
        wc.hInstance = self.instance
        wc.hIcon = self.app_icon or user32.LoadIconW(None, MAKEINTRESOURCEW(IDI_APPLICATION))
        wc.hIconSm = self.app_icon_small or self.app_icon or user32.LoadIconW(None, MAKEINTRESOURCEW(IDI_APPLICATION))
        wc.hCursor = user32.LoadCursorW(None, wintypes.LPCWSTR(32512))
        wc.hbrBackground = self.bg_brush
        wc.lpszClassName = self.class_name
        atom = user32.RegisterClassExW(ctypes.byref(wc))
        if not atom:
            # If the class already exists from a very fast relaunch, continue instead of crashing.
            pass

    def load_app_icon(self, size: int) -> wintypes.HANDLE | None:
        # First load the embedded PyInstaller EXE icon.
        # MAKEINTRESOURCEW is required here. Passing ctypes.c_wchar_p(1) can fail.
        for resource_id in (1, 101, 32512):
            handle = user32.LoadImageW(
                self.instance,
                MAKEINTRESOURCEW(resource_id),
                IMAGE_ICON,
                size,
                size,
                LR_DEFAULTSIZE if size <= 0 else 0,
            )
            if handle:
                return handle

            handle = user32.LoadIconW(self.instance, MAKEINTRESOURCEW(resource_id))
            if handle:
                return handle

        # Fallback to the bundled/external icon. Prefer extra\ for the taskbar/window icon.
        icon = extra_asset_path(APP_ICO_FILE) or asset_path(APP_ICO_FILE)
        if icon is None:
            return None

        for cx, cy in ((size, size), (64, 64), (48, 48), (32, 32), (16, 16), (0, 0)):
            handle = user32.LoadImageW(
                None,
                str(icon),
                IMAGE_ICON,
                cx,
                cy,
                LR_LOADFROMFILE | (LR_DEFAULTSIZE if cx == 0 else 0),
            )
            if handle:
                return handle

        return None

    def load_header_bitmap(self) -> wintypes.HANDLE | None:
        bitmap = asset_path(APP_HEADER_BMP_FILE)
        if bitmap is None:
            return None
        return user32.LoadImageW(None, str(bitmap), IMAGE_BITMAP, 64, 64, LR_LOADFROMFILE)

    def create_window(self) -> wintypes.HWND:
        style = WS_OVERLAPPED | WS_CAPTION | WS_SYSMENU | WS_MINIMIZEBOX | WS_THICKFRAME | WS_MAXIMIZEBOX | WS_VSCROLL
        hwnd = user32.CreateWindowExW(0, self.class_name, APP_NAME, style | WS_VISIBLE, 180, 120, 620, 600, None, None, self.instance, None)
        if not hwnd:
            raise ctypes.WinError()
        if self.app_icon:
            user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG, self.app_icon)
        if self.app_icon_small:
            user32.SendMessageW(hwnd, WM_SETICON, ICON_SMALL, self.app_icon_small)
        return hwnd

    def build_controls(self) -> None:
        self.logo_box = self.create("STATIC", "", WS_CHILD | WS_VISIBLE | SS_BITMAP, 20, 12, 64, 64)
        header_bitmap = self.load_header_bitmap()
        if header_bitmap:
            user32.SendMessageW(self.logo_box, STM_SETIMAGE, IMAGE_BITMAP, header_bitmap)
        else:
            logo_icon = self.load_app_icon(48)
            if logo_icon:
                user32.SendMessageW(self.logo_box, STM_SETICON, logo_icon, 0)

        # Moved title/description to the right so they do not crowd the logo.
        self.label("Bolt AutoClicker", 104, 16, 300, 30, bold=True)
        self.label("Compact Windows autoclicker with saved hotkeys.", 106, 48, 380, 22)
        self.button("exit_app", "Exit", 500, 22, 70, 30)

        self.group("Click interval", 18, 82, 550, 106)
        for index, (name, text) in enumerate((("hours", "Hours"), ("minutes", "Minutes"), ("seconds", "Seconds"), ("milliseconds", "Milliseconds"))):
            x = 36 + index * 128
            self.label(text, x, 106, 105, 20)
            self.edit(name, x, 130, 90, 26, number=True)
        self.check("fastest", "As fast as possible", 36, 158, 195, 22)
        warning = self.label("Warning: sub-millisecond / fastest timing may be limited by Windows scheduling and hardware.", 36, 178, 500, 20)
        self.warning_labels.add(int(warning))

        self.group("Click repeat", 18, 204, 550, 78)
        self.radio("repeat_forever", "Repeat until stopped", 36, 228, 195, 22)
        self.radio("repeat_count_mode", "Repeat this many times", 36, 256, 195, 22)
        self.edit("repeat_count", 238, 254, 100, 26, number=True)

        self.group("Action", 18, 298, 550, 82)
        self.radio("action_mouse", "Mouse click", 36, 322, 128, 22)
        self.radio("action_key", "Keyboard key", 36, 352, 128, 22)
        self.label("Button", 176, 322, 52, 22)
        self.combo("mouse_button", 232, 320, 94, 120, ["left", "right", "middle"])
        self.label("Clicks", 342, 322, 48, 22)
        self.combo("click_count", 394, 320, 98, 120, ["single", "double"])
        self.label("Key", 176, 352, 38, 22)
        self.edit("key_name", 232, 350, 112, 26)

        self.group("Click position", 18, 396, 550, 84)
        self.radio("position_current", "Current cursor position", 36, 420, 205, 22)
        self.radio("position_fixed", "Fixed position", 36, 450, 122, 22)
        self.label("X", 166, 450, 18, 22)
        self.edit("x", 188, 448, 72, 26, number=True)
        self.label("Y", 270, 450, 18, 22)
        self.edit("y", 292, 448, 72, 26, number=True)
        self.button("pick_position", "Use Current Position", 382, 446, 166, 30)

        self.button("start", "Start", 18, 500, 176, 34, default=True)
        self.button("stop", "Stop", 206, 500, 176, 34)
        self.button("toggle", "Toggle", 394, 500, 174, 34)

        self.button("save", "Save Settings", 18, 548, 176, 32)
        self.button("reset", "Reset Settings", 206, 548, 176, 32)
        self.button("hotkeys", "Change Hotkeys", 394, 548, 174, 32)

        self.controls["status"] = self.label("", 18, 600, 550, 22)

    def label(self, text: str, x: int, y: int, w: int, h: int, bold: bool = False) -> wintypes.HWND:
        hwnd = self.create("STATIC", text, WS_CHILD | WS_VISIBLE | SS_LEFT | SS_CENTERIMAGE, x, y, w, h)
        user32.SendMessageW(hwnd, WM_SETFONT, self.bold_font if bold else self.font, True)
        return hwnd

    def group(self, text: str, x: int, y: int, w: int, h: int) -> wintypes.HWND:
        # Native group boxes can look faint, so WS_BORDER gives the boxes a clearer outline.
        hwnd = self.create("BUTTON", text, WS_CHILD | WS_VISIBLE | BS_GROUPBOX | WS_BORDER, x, y, w, h)
        user32.SendMessageW(hwnd, WM_SETFONT, self.font, True)
        return hwnd

    def button(self, name: str, text: str, x: int, y: int, w: int, h: int, default: bool = False) -> None:
        # Do not use BS_DEFPUSHBUTTON; it makes Start/F1 look permanently highlighted.
        style = WS_CHILD | WS_VISIBLE | WS_TABSTOP | BS_PUSHBUTTON
        self.controls[name] = self.create("BUTTON", text, style, x, y, w, h)
        user32.SendMessageW(self.controls[name], WM_SETFONT, self.font, True)

    def radio(self, name: str, text: str, x: int, y: int, w: int, h: int) -> None:
        self.controls[name] = self.create("BUTTON", text, WS_CHILD | WS_VISIBLE | WS_TABSTOP | BS_AUTORADIOBUTTON, x, y, w, h)
        user32.SendMessageW(self.controls[name], WM_SETFONT, self.font, True)

    def check(self, name: str, text: str, x: int, y: int, w: int, h: int) -> None:
        self.controls[name] = self.create("BUTTON", text, WS_CHILD | WS_VISIBLE | WS_TABSTOP | BS_AUTOCHECKBOX, x, y, w, h)
        user32.SendMessageW(self.controls[name], WM_SETFONT, self.font, True)

    def edit(self, name: str, x: int, y: int, w: int, h: int, number: bool = False) -> None:
        style = WS_CHILD | WS_VISIBLE | WS_TABSTOP | WS_BORDER | 0x00000080 | (ES_NUMBER if number else 0)
        self.controls[name] = self.create("EDIT", "", style, x, y, w, h)
        user32.SendMessageW(self.controls[name], WM_SETFONT, self.font, True)

    def combo(self, name: str, x: int, y: int, w: int, h: int, values: list[str]) -> None:
        hwnd = self.create("COMBOBOX", "", WS_CHILD | WS_VISIBLE | WS_TABSTOP | WS_BORDER | CBS_DROPDOWNLIST, x, y, w, h)
        self.controls[name] = hwnd
        user32.SendMessageW(hwnd, WM_SETFONT, self.font, True)
        for value in values:
            text = ctypes.c_wchar_p(value)
            user32.SendMessageW(hwnd, CB_ADDSTRING, 0, ctypes.cast(text, ctypes.c_void_p).value)

    def create(self, cls: str, text: str, style: int, x: int, y: int, w: int, h: int) -> wintypes.HWND:
        return self.create_in(self.hwnd, cls, text, style, x, y, w, h)

    def create_in(self, parent: wintypes.HWND, cls: str, text: str, style: int, x: int, y: int, w: int, h: int) -> wintypes.HWND:
        hwnd = user32.CreateWindowExW(0, cls, text, style, x, y - (self.scroll_y if parent == self.hwnd else 0), w, h, parent, None, self.instance, None)
        if parent == self.hwnd and hwnd:
            self.child_layout[int(hwnd)] = (x, y, w, h)
        return hwnd

    def client_height(self) -> int:
        rect = wintypes.RECT()
        if not user32.GetClientRect(self.hwnd, ctypes.byref(rect)):
            return 0
        return max(0, rect.bottom - rect.top)

    def update_scrollbar(self) -> None:
        if not hasattr(self, "hwnd"):
            return
        height = self.client_height()
        max_scroll = self.max_scroll()
        self.scroll_y = min(max(self.scroll_y, 0), max_scroll)
        info = SCROLLINFO()
        info.cbSize = ctypes.sizeof(SCROLLINFO)
        info.fMask = SIF_ALL
        info.nMin = 0
        info.nMax = CONTENT_HEIGHT
        info.nPage = max(1, height)
        info.nPos = self.scroll_y
        user32.SetScrollInfo(self.hwnd, SB_VERT, ctypes.byref(info), True)
        self.apply_scroll()

    def max_scroll(self) -> int:
        return max(0, CONTENT_HEIGHT - self.client_height())

    def scroll_to(self, value: int) -> None:
        new_value = min(max(value, 0), self.max_scroll())
        if new_value == self.scroll_y:
            return
        self.scroll_y = new_value
        self.update_scrollbar()

    def handle_vscroll(self, wparam: int) -> None:
        code = wparam & 0xFFFF
        thumb = (wparam >> 16) & 0xFFFF
        if thumb >= 0x8000:
            thumb -= 0x10000

        if code == SB_LINEUP:
            self.scroll_to(self.scroll_y - 24)
        elif code == SB_LINEDOWN:
            self.scroll_to(self.scroll_y + 24)
        elif code == SB_PAGEUP:
            self.scroll_to(self.scroll_y - max(60, self.client_height() - 40))
        elif code == SB_PAGEDOWN:
            self.scroll_to(self.scroll_y + max(60, self.client_height() - 40))
        elif code in (SB_THUMBTRACK, SB_THUMBPOSITION):
            self.scroll_to(thumb)

    def handle_mousewheel(self, wparam: int) -> None:
        delta = (wparam >> 16) & 0xFFFF
        if delta >= 0x8000:
            delta -= 0x10000
        self.scroll_to(self.scroll_y - int(delta / 120) * 54)

    def apply_scroll(self) -> None:
        for hwnd_value, (x, y, w, h) in self.child_layout.items():
            user32.SetWindowPos(wintypes.HWND(hwnd_value), None, x, y - self.scroll_y, w, h, SWP_NOZORDER | SWP_NOACTIVATE)

    def load_settings(self) -> Settings:
        if not self.settings_path.exists():
            return Settings()
        try:
            data = json.loads(self.settings_path.read_text(encoding="utf-8"))
            defaults = asdict(Settings())
            defaults.update({key: data[key] for key in defaults.keys() & data.keys()})
            return Settings(**defaults)
        except (OSError, json.JSONDecodeError, TypeError, ValueError):
            return Settings()

    def apply_settings(self, s: Settings) -> None:
        for name in ("hours", "minutes", "seconds", "milliseconds", "repeat_count", "key_name", "x", "y"):
            self.set_text(name, str(getattr(s, name)))
        self.set_combo("mouse_button", s.mouse_button)
        self.set_combo("click_count", s.click_count)
        self.set_check("fastest", s.fastest)
        self.set_radio("repeat_forever" if s.repeat_mode == "forever" else "repeat_count_mode")
        self.set_radio("action_mouse" if s.action_type == "mouse" else "action_key")
        self.set_radio("position_current" if s.position_mode == "current" else "position_fixed")
        self.refresh_hotkey_buttons()

    def current_settings(self) -> Settings:
        s = self.settings
        return Settings(
            hours=self.get_int("hours"),
            minutes=self.get_int("minutes"),
            seconds=self.get_int("seconds"),
            milliseconds=self.get_int("milliseconds"),
            fastest=self.get_check("fastest"),
            repeat_mode="forever" if self.get_check("repeat_forever") else "count",
            repeat_count=max(1, self.get_int("repeat_count")),
            action_type="mouse" if self.get_check("action_mouse") else "key",
            mouse_button=self.get_combo("mouse_button"),
            click_count=self.get_combo("click_count"),
            key_name=normalize_key_name(self.get_text("key_name") or "SPACE"),
            position_mode="current" if self.get_check("position_current") else "fixed",
            x=self.get_int("x"),
            y=self.get_int("y"),
            start_hotkey=s.start_hotkey,
            stop_hotkey=s.stop_hotkey,
            toggle_hotkey=s.toggle_hotkey,
            exit_hotkey=s.exit_hotkey,
        )

    def start(self) -> None:
        if self.worker and self.worker.is_alive() and not self.stop_event.is_set():
            self.set_status("Already running.")
            return
        settings = self.current_settings()
        if settings.action_type == "key" and normalize_key_name(settings.key_name) not in VK_CODES:
            self.message(f"Unknown key: {settings.key_name}")
            return
        self.stop_event.clear()
        self.worker = threading.Thread(target=self.click_loop, args=(settings,), daemon=True)
        self.worker.start()
        self.set_status("Running.")

    def stop(self) -> None:
        self.stop_event.set()
        self.set_status("Stopped.")

    def toggle(self) -> None:
        if self.worker and self.worker.is_alive() and not self.stop_event.is_set():
            self.stop()
        else:
            self.start()

    def save_settings(self) -> None:
        self.settings = self.current_settings()
        self.settings_path.write_text(json.dumps(asdict(self.settings), indent=2), encoding="utf-8")
        self.register_hotkeys()
        self.refresh_hotkey_buttons()
        self.set_status("Settings saved.")

    def reset_settings(self) -> None:
        self.stop()
        self.settings = Settings()
        self.apply_settings(self.settings)
        self.save_settings()
        self.set_status("Settings reset.")

    def change_hotkeys(self) -> None:
        if self.hotkey_hwnd:
            user32.SetForegroundWindow(self.hotkey_hwnd)
            return
        style = WS_OVERLAPPED | WS_CAPTION | WS_SYSMENU
        self.hotkey_hwnd = user32.CreateWindowExW(
            WS_EX_DLGMODALFRAME,
            self.class_name,
            "Change Hotkeys",
            style | WS_VISIBLE,
            260,
            180,
            350,
            245,
            self.hwnd,
            None,
            self.instance,
            None,
        )
        self.hotkey_controls.clear()
        rows = [
            ("Start hotkey", "hk_start", self.settings.start_hotkey, 18),
            ("Stop hotkey", "hk_stop", self.settings.stop_hotkey, 55),
            ("Toggle hotkey", "hk_toggle", self.settings.toggle_hotkey, 92),
            ("Exit app hotkey", "hk_exit", self.settings.exit_hotkey, 129),
        ]
        for label, name, value, y in rows:
            lbl = self.create_in(self.hotkey_hwnd, "STATIC", label, WS_CHILD | WS_VISIBLE | SS_LEFT | SS_CENTERIMAGE, 18, y, 105, 22)
            user32.SendMessageW(lbl, WM_SETFONT, self.font, True)
            edit = self.create_in(self.hotkey_hwnd, "EDIT", value, WS_CHILD | WS_VISIBLE | WS_TABSTOP | 0x00000080, 130, y, 145, 24)
            user32.SendMessageW(edit, WM_SETFONT, self.font, True)
            self.hotkey_controls[name] = edit
        tip = self.create_in(self.hotkey_hwnd, "STATIC", "Examples: F1, CTRL+F1, ALT+S, NUMPAD5", WS_CHILD | WS_VISIBLE | SS_LEFT, 18, 160, 300, 20)
        user32.SendMessageW(tip, WM_SETFONT, self.font, True)
        self.hotkey_button("hk_save", "Save", 62, 188, 100, 28)
        self.hotkey_button("hk_cancel", "Cancel", 182, 188, 100, 28)

    def hotkey_button(self, name: str, text: str, x: int, y: int, w: int, h: int) -> None:
        hwnd = self.create_in(self.hotkey_hwnd, "BUTTON", text, WS_CHILD | WS_VISIBLE | WS_TABSTOP | BS_PUSHBUTTON, x, y, w, h)
        user32.SendMessageW(hwnd, WM_SETFONT, self.font, True)
        self.hotkey_controls[name] = hwnd

    def save_hotkeys_from_dialog(self) -> None:
        values = {
            "start_hotkey": self.get_window_text(self.hotkey_controls["hk_start"]).strip().upper(),
            "stop_hotkey": self.get_window_text(self.hotkey_controls["hk_stop"]).strip().upper(),
            "toggle_hotkey": self.get_window_text(self.hotkey_controls["hk_toggle"]).strip().upper(),
            "exit_hotkey": self.get_window_text(self.hotkey_controls["hk_exit"]).strip().upper(),
        }
        for value in values.values():
            if parse_hotkey(value) is None:
                self.message(f"Invalid hotkey: {value}")
                return
        self.settings.start_hotkey = values["start_hotkey"]
        self.settings.stop_hotkey = values["stop_hotkey"]
        self.settings.toggle_hotkey = values["toggle_hotkey"]
        self.settings.exit_hotkey = values["exit_hotkey"]
        self.save_settings()
        user32.DestroyWindow(self.hotkey_hwnd)

    def use_current_position(self) -> None:
        x, y = self.input.get_position()
        self.set_text("x", str(x))
        self.set_text("y", str(y))
        self.set_radio("position_fixed")
        self.set_status(f"Fixed position set to {x}, {y}.")

    def exit_app(self) -> None:
        self.stop()
        self.unregister_hotkeys()
        user32.DestroyWindow(self.hwnd)

    def click_loop(self, settings: Settings) -> None:
        interval = self.interval_seconds(settings)
        max_runs = None if settings.repeat_mode == "forever" else max(1, int(settings.repeat_count))
        runs = 0
        while not self.stop_event.is_set() and (max_runs is None or runs < max_runs):
            if settings.position_mode == "fixed":
                self.input.set_position(settings.x, settings.y)
            if settings.action_type == "mouse":
                self.input.click(settings.mouse_button, 2 if settings.click_count == "double" else 1)
            else:
                self.input.key_press(settings.key_name)
            runs += 1
            self.stop_event.wait(0.001 if interval <= 0 else interval)
        self.set_status("Finished." if not self.stop_event.is_set() else "Stopped.")

    def interval_seconds(self, s: Settings) -> float:
        if s.fastest:
            return 0.0
        return max((s.hours * 3600) + (s.minutes * 60) + s.seconds + (s.milliseconds / 1000), 0.001)

    def register_hotkeys(self) -> None:
        self.unregister_hotkeys()
        for hotkey_id, text in (
            (1, self.settings.start_hotkey),
            (2, self.settings.stop_hotkey),
            (3, self.settings.toggle_hotkey),
            (4, self.settings.exit_hotkey),
        ):
            parsed = parse_hotkey(text)
            if parsed:
                modifiers, vk = parsed
                user32.RegisterHotKey(self.hwnd, hotkey_id, modifiers, vk)

    def unregister_hotkeys(self) -> None:
        for hotkey_id in (1, 2, 3, 4):
            user32.UnregisterHotKey(self.hwnd, hotkey_id)

    def refresh_hotkey_buttons(self) -> None:
        self.set_text("start", f"Start ({self.settings.start_hotkey})")
        self.set_text("stop", f"Stop ({self.settings.stop_hotkey})")
        self.set_text("toggle", f"Toggle ({self.settings.toggle_hotkey})")
        self.set_status(f"Ready. Start: {self.settings.start_hotkey}  Stop: {self.settings.stop_hotkey}  Toggle: {self.settings.toggle_hotkey}  Exit: {self.settings.exit_hotkey}")

    def wndproc(self, hwnd: wintypes.HWND, msg: int, wparam: int, lparam: int) -> int:
        if msg == WM_COMMAND:
            source = wintypes.HWND(lparam).value
            for name, control in self.controls.items():
                if control == source:
                    self.dispatch(name)
                    break
            for name, control in self.hotkey_controls.items():
                if control == source:
                    if name == "hk_save":
                        self.save_hotkeys_from_dialog()
                    elif name == "hk_cancel":
                        user32.DestroyWindow(self.hotkey_hwnd)
                    break
        elif msg == WM_HOTKEY:
            if wparam == 1:
                self.start()
            elif wparam == 2:
                self.stop()
            elif wparam == 3:
                self.toggle()
            elif wparam == 4:
                self.exit_app()
        elif msg == WM_SIZE:
            if hasattr(self, "hwnd"):
                self.update_scrollbar()
        elif msg == WM_VSCROLL:
            self.handle_vscroll(int(wparam))
            return 0
        elif msg == WM_MOUSEWHEEL:
            self.handle_mousewheel(int(wparam))
            return 0
        elif msg == WM_CTLCOLORSTATIC:
            gdi32.SetBkMode(wparam, 1)
            if int(lparam) in self.warning_labels:
                gdi32.SetTextColor(wparam, WARN_COLORREF)
            else:
                gdi32.SetTextColor(wparam, TEXT_COLORREF)
            return self.bg_brush
        elif msg == WM_CLOSE:
            self.exit_app()
            return 0
        elif msg == WM_DESTROY:
            if hwnd == self.hotkey_hwnd:
                self.hotkey_hwnd = None
                self.hotkey_controls.clear()
                return 0
            self.stop()
            self.unregister_hotkeys()
            user32.PostQuitMessage(0)
            return 0
        return user32.DefWindowProcW(hwnd, msg, wparam, lparam)

    def dispatch(self, name: str) -> None:
        actions = {
            "start": self.start,
            "stop": self.stop,
            "toggle": self.toggle,
            "save": self.save_settings,
            "reset": self.reset_settings,
            "hotkeys": self.change_hotkeys,
            "pick_position": self.use_current_position,
            "exit_app": self.exit_app,
        }
        if name in actions:
            actions[name]()

    def run(self) -> None:
        msg = MSG()
        while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))

    def get_text(self, name: str) -> str:
        return self.get_window_text(self.controls[name])

    def get_window_text(self, hwnd: wintypes.HWND) -> str:
        length = user32.GetWindowTextLengthW(hwnd)
        buf = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buf, length + 1)
        return buf.value

    def set_text(self, name: str, text: str) -> None:
        user32.SetWindowTextW(self.controls[name], text)

    def get_int(self, name: str) -> int:
        try:
            return int(self.get_text(name) or "0")
        except ValueError:
            return 0

    def set_check(self, name: str, value: bool) -> None:
        user32.SendMessageW(self.controls[name], BM_SETCHECK, BST_CHECKED if value else 0, 0)

    def get_check(self, name: str) -> bool:
        return user32.SendMessageW(self.controls[name], BM_GETCHECK, 0, 0) == BST_CHECKED

    def set_radio(self, name: str) -> None:
        groups = [
            ("repeat_forever", "repeat_count_mode"),
            ("action_mouse", "action_key"),
            ("position_current", "position_fixed"),
        ]
        for group in groups:
            if name in group:
                for item in group:
                    self.set_check(item, item == name)
                return

    def set_combo(self, name: str, value: str) -> None:
        values = {"mouse_button": ["left", "right", "middle"], "click_count": ["single", "double"]}[name]
        index = values.index(value) if value in values else 0
        user32.SendMessageW(self.controls[name], CB_SETCURSEL, index, 0)

    def get_combo(self, name: str) -> str:
        hwnd = self.controls[name]
        index = user32.SendMessageW(hwnd, CB_GETCURSEL, 0, 0)
        if index < 0:
            return ""
        length = user32.SendMessageW(hwnd, CB_GETLBTEXTLEN, index, 0)
        buf = ctypes.create_unicode_buffer(length + 1)
        user32.SendMessageW(hwnd, CB_GETLBTEXT, index, ctypes.addressof(buf))
        return buf.value

    def set_status(self, text: str) -> None:
        if "status" in self.controls:
            self.set_text("status", text)

    def message(self, text: str) -> None:
        user32.MessageBoxW(self.hwnd, text, APP_NAME, 0x00000040)


def main() -> None:
    if sys.platform != "win32":
        raise SystemExit("Bolt AutoClicker is built for Windows.")
    NativeApp().run()


if __name__ == "__main__":
    main()
