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
    image = image.resize((64, 64), Image.Resampling.LANCZOS)
    image.save(HEADER_BMP)


def make_taskbar_icon() -> None:
    EXTRA.mkdir(exist_ok=True)
    if EXTRA_ICO.exists():
        if ASSET_ICO.exists():
            return
        shutil.copy2(EXTRA_ICO, ASSET_ICO)
        return

    if ASSET_ICO.exists():
        shutil.copy2(ASSET_ICO, EXTRA_ICO)
        return

    raise SystemExit(f"Missing taskbar icon: {EXTRA_ICO} or {ASSET_ICO}")


def main() -> None:
    make_header_bitmap()
    make_taskbar_icon()
    print(HEADER_BMP)
    print(EXTRA_ICO)


if __name__ == "__main__":
    main()
