from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageOps


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "assets" / "mouse_source.png"
ICO_OUT = ROOT / "assets" / "bolt_autoclicker.ico"
PNG_OUT = ROOT / "assets" / "bolt_autoclicker_logo.png"


def make_background(size: int) -> Image.Image:
    base = Image.new("RGBA", (size, size), "#1455d9")
    top = Image.new("RGBA", (size, size), "#2fb7ff")
    mask = Image.linear_gradient("L").resize((size, size)).transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    base.alpha_composite(Image.composite(top, Image.new("RGBA", (size, size), "#0c2f7a"), mask))

    inset = max(2, size // 18)
    frame = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    frame_mask = Image.new("L", (size, size), 0)
    inner = Image.new("L", (size - inset * 2, size - inset * 2), 255)
    frame_mask.paste(inner, (inset, inset))
    frame_mask = frame_mask.filter(ImageFilter.GaussianBlur(max(1, size // 80)))
    frame_color = Image.new("RGBA", (size, size), "#dff6ff")
    frame.alpha_composite(frame_color, (0, 0))
    base = Image.composite(frame, base, frame_mask)
    return base


def mouse_layer(size: int) -> Image.Image:
    source = Image.open(SOURCE).convert("RGBA")
    gray = ImageOps.grayscale(source)
    outline_mask = Image.eval(gray, lambda p: 255 if p < 90 else 0).filter(ImageFilter.MaxFilter(5))

    bbox = outline_mask.getbbox()
    if not bbox:
        return Image.new("RGBA", (size, size), (0, 0, 0, 0))

    alpha = filled_pointer_mask(outline_mask.crop(bbox))
    target = int(size * 0.68)
    alpha.thumbnail((target, target), Image.Resampling.LANCZOS)

    outline = Image.new("RGBA", alpha.size, "#111111")
    outline.putalpha(alpha.filter(ImageFilter.MaxFilter(5)))
    fill = Image.new("RGBA", alpha.size, "#ffffff")
    fill.putalpha(alpha)

    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    x = (size - alpha.width) // 2
    y = (size - alpha.height) // 2 + size // 24
    layer.alpha_composite(outline, (x, y))
    layer.alpha_composite(fill, (x, y))

    click = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(click)
    tip_x = x + int(alpha.width * 0.54)
    tip_y = y + int(alpha.height * 0.04)
    for radius, opacity in ((int(size * 0.12), 180), (int(size * 0.18), 95)):
        draw.ellipse(
            (tip_x - radius, tip_y - radius, tip_x + radius, tip_y + radius),
            outline=(255, 255, 255, opacity),
            width=max(2, size // 42),
        )
    dot_radius = max(2, size // 34)
    draw.ellipse(
        (tip_x - dot_radius, tip_y - dot_radius, tip_x + dot_radius, tip_y + dot_radius),
        fill="#ffffff",
        outline="#071a3d",
        width=max(1, size // 96),
    )
    layer.alpha_composite(click)
    return layer


def filled_pointer_mask(outline: Image.Image) -> Image.Image:
    outline = outline.convert("L")
    w, h = outline.size
    blocked = outline.load()
    outside = Image.new("L", (w, h), 0)
    outside_px = outside.load()
    stack = []
    for x in range(w):
        stack.extend([(x, 0), (x, h - 1)])
    for y in range(h):
        stack.extend([(0, y), (w - 1, y)])
    while stack:
        x, y = stack.pop()
        if x < 0 or y < 0 or x >= w or y >= h:
            continue
        if outside_px[x, y] or blocked[x, y] > 0:
            continue
        outside_px[x, y] = 255
        stack.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])
    return ImageOps.invert(outside).filter(ImageFilter.MaxFilter(3))


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
