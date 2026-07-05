from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
EXTRA = ROOT / "extra"
LOGO_PNG = ASSETS / "bolt_autoclicker_logo.png"
HEADER_BMP = ASSETS / "bolt_autoclicker_header.bmp"
ASSET_ICO = ASSETS / "bolt_autoclicker.ico"
EXTRA_ICO = EXTRA / "bolt_autoclicker.ico"


def make_header_bitmap() -> None:
    if not LOGO_PNG.exists():
        raise SystemExit(f"Missing logo image: {LOGO_PNG}")

    image = Image.open(LOGO_PNG).convert("RGB")
    image.thumbnail((64, 64), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (64, 64), (232, 232, 232))
    x = (64 - image.width) // 2
    y = (64 - image.height) // 2
    canvas.paste(image, (x, y))
    canvas.save(HEADER_BMP)


def make_taskbar_icon() -> None:
    if not LOGO_PNG.exists():
        raise SystemExit(f"Missing logo image: {LOGO_PNG}")

    EXTRA.mkdir(exist_ok=True)
    image = Image.open(LOGO_PNG).convert("RGBA")
    icon_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    image.save(EXTRA_ICO, format="ICO", sizes=icon_sizes)
    shutil.copy2(EXTRA_ICO, ASSET_ICO)


def main() -> None:
    make_header_bitmap()
    make_taskbar_icon()
    print(HEADER_BMP)
    print(EXTRA_ICO)


if __name__ == "__main__":
    main()
