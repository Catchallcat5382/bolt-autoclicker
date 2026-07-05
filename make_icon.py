from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageOps


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "assets" / "mouse_source.png"
ICO_OUT = ROOT / "assets" / "bolt_autoclicker.ico"
PNG_OUT = ROOT / "assets" / "bolt_autoclicker_logo.png"


def make_background(size: int) -> Image.Image:
    base = Image.new("RGBA", (size, size), "#b7812f")
    top = Image.new("RGBA", (size, size), "#d5b06a")
    mask = Image.linear_gradient("L").resize((size, size)).transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    base.alpha_composite(Image.composite(top, Image.new("RGBA", (size, size), "#7a5520"), mask))

    inset = max(2, size // 18)
    frame = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    frame_mask = Image.new("L", (size, size), 0)
    inner = Image.new("L", (size - inset * 2, size - inset * 2), 255)
    frame_mask.paste(inner, (inset, inset))
    frame_mask = frame_mask.filter(ImageFilter.GaussianBlur(max(1, size // 80)))
    frame_color = Image.new("RGBA", (size, size), "#f3dfad")
    frame.alpha_composite(frame_color, (0, 0))
    base = Image.composite(frame, base, frame_mask)
    return base


def mouse_layer(size: int) -> Image.Image:
    source = Image.open(SOURCE).convert("RGBA")
    gray = ImageOps.grayscale(source)
    alpha_from_dark = Image.eval(gray, lambda p: 255 if p < 200 else 0)
    alpha_from_source = source.getchannel("A")
    alpha = Image.composite(alpha_from_dark, alpha_from_source, alpha_from_source)
    alpha = alpha.filter(ImageFilter.GaussianBlur(max(0.4, size / 256)))

    bbox = alpha.getbbox()
    if not bbox:
        return Image.new("RGBA", (size, size), (0, 0, 0, 0))

    alpha = alpha.crop(bbox)
    target = int(size * 0.72)
    alpha.thumbnail((target, target), Image.Resampling.LANCZOS)

    outline = Image.new("RGBA", alpha.size, "#111111")
    outline.putalpha(alpha.filter(ImageFilter.MaxFilter(5)))
    fill = Image.new("RGBA", alpha.size, "#ffffff")
    fill.putalpha(alpha)

    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    x = (size - alpha.width) // 2
    y = (size - alpha.height) // 2 - size // 30
    layer.alpha_composite(outline, (x, y))
    layer.alpha_composite(fill, (x, y))

    click = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(click)
    dot_size = max(4, size // 10)
    x0 = int(size * 0.66)
    y0 = int(size * 0.66)
    draw.ellipse((x0, y0, x0 + dot_size, y0 + dot_size), fill="#2f80ed", outline="#0b3f85", width=max(1, size // 80))
    layer.alpha_composite(click)
    return layer


def compose(size: int) -> Image.Image:
    image = make_background(size)
    image.alpha_composite(mouse_layer(size))
    return image


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"Missing source logo: {SOURCE}")
    large = compose(512)
    large.save(PNG_OUT)
    icons = [compose(size) for size in (16, 24, 32, 48, 64, 128, 256)]
    icons[-1].save(ICO_OUT, sizes=[(icon.width, icon.height) for icon in icons], append_images=icons[:-1])
    print(ICO_OUT)
    print(PNG_OUT)


if __name__ == "__main__":
    main()
