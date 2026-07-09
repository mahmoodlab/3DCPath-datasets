from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


OUT = Path(__file__).with_name("interpolation_schematic_no_text.png")
W, H = 1800, 1000
SCALE = 3


def rgba(hex_color: str, alpha: int) -> tuple[int, int, int, int]:
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def local_to_quad(u: float, v: float, quad: list[tuple[float, float]]) -> tuple[float, float]:
    tl, tr, br, bl = quad
    top = (lerp(tl[0], tr[0], u), lerp(tl[1], tr[1], u))
    bottom = (lerp(bl[0], br[0], u), lerp(bl[1], br[1], u))
    return (lerp(top[0], bottom[0], v), lerp(top[1], bottom[1], v))


def offset_quad(quad: list[tuple[float, float]], dx: float, dy: float) -> list[tuple[float, float]]:
    return [(x + dx, y + dy) for x, y in quad]


def draw_poly(
    draw: ImageDraw.ImageDraw,
    points: list[tuple[float, float]],
    fill: tuple[int, int, int, int] | None = None,
    outline: tuple[int, int, int, int] | None = None,
    width: int = 1,
) -> None:
    p = [(round(x), round(y)) for x, y in points]
    draw.polygon(p, fill=fill)
    if outline and width:
        draw.line(p + [p[0]], fill=outline, width=width, joint="curve")


def tissue_boundary(cx: float, cy: float, rx: float, ry: float, phase: float, lobed: bool) -> list[tuple[float, float]]:
    pts = []
    for i in range(150):
        a = 2 * math.pi * i / 150.0
        wobble = 1.0
        if lobed:
            wobble += 0.17 * math.sin(2.1 * a + phase) + 0.07 * math.sin(5.0 * a - phase)
        x = cx + rx * wobble * math.cos(a)
        y = cy + ry * (1.0 + 0.10 * math.cos(3.0 * a + phase)) * math.sin(a)
        pts.append((x, y))
    return pts


def draw_tissue(
    im: Image.Image,
    quad: list[tuple[float, float]],
    slide_w: float,
    slide_h: float,
    cx: float,
    cy: float,
    rx: float,
    ry: float,
    phase: float,
    seed: int,
    lobed: bool = True,
) -> None:
    rng = random.Random(seed)
    local_poly = tissue_boundary(cx, cy, rx, ry, phase, lobed)
    canvas_poly = [local_to_quad(x / slide_w, y / slide_h, quad) for x, y in local_poly]

    overlay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")
    draw_poly(draw, canvas_poly, fill=rgba("#efbfd9", 224), outline=rgba("#cf5fa4", 170), width=4 * SCALE)

    # Gland-like pale spaces.
    for j in range(15):
        a = rng.uniform(0, 2 * math.pi)
        rr = math.sqrt(rng.random()) * 0.78
        x = cx + math.cos(a) * rx * rr
        y = cy + math.sin(a) * ry * rr * 0.8
        if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 > 0.85:
            continue
        px, py = local_to_quad(x / slide_w, y / slide_h, quad)
        r1 = rng.uniform(10, 22) * SCALE
        r2 = rng.uniform(4, 9) * SCALE
        draw.ellipse((px - r1, py - r2, px + r1, py + r2), fill=rgba("#fff4fb", 178), outline=rgba("#d98fc5", 100), width=2 * SCALE)

    # Nuclei and stromal speckles.
    for _ in range(700):
        a = rng.uniform(0, 2 * math.pi)
        rr = math.sqrt(rng.random()) * 0.95
        x = cx + math.cos(a) * rx * rr
        y = cy + math.sin(a) * ry * rr
        if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 > 1.0:
            continue
        px, py = local_to_quad(x / slide_w, y / slide_h, quad)
        rad = rng.uniform(1.2, 2.5) * SCALE
        color = rng.choice([rgba("#6d3a91", 190), rgba("#8b4faa", 165), rgba("#b35aa1", 145)])
        draw.ellipse((px - rad, py - rad * 0.65, px + rad, py + rad * 0.65), fill=color)

    im.alpha_composite(overlay)


def slide_quad(x: float, y: float, w: float = 545, h: float = 120, skew: float = 92) -> list[tuple[float, float]]:
    return [(x, y + skew * 0.18), (x + w, y), (x + w + skew, y + h), (x + skew, y + h + skew * 0.18)]


def draw_slide(
    im: Image.Image,
    x: float,
    y: float,
    tissue: dict[str, float],
    seed: int,
    w: float = 545 * SCALE,
    h: float = 120 * SCALE,
    skew: float = 92 * SCALE,
) -> None:
    q = slide_quad(x, y, w, h, skew)
    draw = ImageDraw.Draw(im, "RGBA")

    shadow = Image.new("RGBA", im.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow, "RGBA")
    draw_poly(sd, offset_quad(q, 10 * SCALE, 14 * SCALE), fill=(30, 55, 75, 48))
    shadow = shadow.filter(ImageFilter.GaussianBlur(7 * SCALE))
    im.alpha_composite(shadow)

    draw_poly(draw, q, fill=rgba("#f4fbff", 158), outline=rgba("#2b5f91", 215), width=4 * SCALE)

    lip = [
        local_to_quad(0.0, 0.86, q),
        local_to_quad(1.0, 0.86, q),
        local_to_quad(1.0, 1.0, q),
        local_to_quad(0.0, 1.0, q),
    ]
    draw_poly(draw, lip, fill=rgba("#2d6b9d", 72), outline=rgba("#234f76", 130), width=2 * SCALE)

    cap = [
        local_to_quad(0.0, 0.0, q),
        local_to_quad(0.27, 0.0, q),
        local_to_quad(0.27, 1.0, q),
        local_to_quad(0.0, 1.0, q),
    ]
    draw_poly(draw, cap, fill=rgba("#aeb9c3", 166), outline=rgba("#2a3741", 138), width=3 * SCALE)

    highlight = [
        local_to_quad(0.36, 0.03, q),
        local_to_quad(0.96, 0.03, q),
        local_to_quad(0.78, 0.56, q),
        local_to_quad(0.45, 0.32, q),
    ]
    draw_poly(draw, highlight, fill=rgba("#ffffff", 70))

    inset = [
        local_to_quad(0.015, 0.09, q),
        local_to_quad(0.985, 0.09, q),
        local_to_quad(0.985, 0.88, q),
        local_to_quad(0.015, 0.88, q),
    ]
    draw.line([(round(a), round(b)) for a, b in inset + [inset[0]]], fill=rgba("#6fa0c8", 125), width=2 * SCALE)

    draw_tissue(
        im,
        q,
        w,
        h,
        tissue["cx"] * SCALE,
        tissue["cy"] * SCALE,
        tissue["rx"] * SCALE,
        tissue["ry"] * SCALE,
        tissue["phase"],
        seed,
        bool(tissue.get("lobed", 1)),
    )


def make_figure() -> Image.Image:
    im = Image.new("RGBA", (W * SCALE, H * SCALE), (255, 255, 255, 255))

    # Input: observed sections aligned to matching output rows.
    input_sections = [
        (95, 115, {"cx": 365, "cy": 58, "rx": 54, "ry": 31, "phase": 0.0, "lobed": 0}),
        (95, 375, {"cx": 376, "cy": 63, "rx": 126, "ry": 37, "phase": 0.8, "lobed": 1}),
        (95, 765, {"cx": 360, "cy": 62, "rx": 47, "ry": 27, "phase": 1.5, "lobed": 0}),
    ]
    for i, (x, y, tissue) in enumerate(input_sections):
        draw_slide(im, x * SCALE, y * SCALE, tissue, seed=100 + i)

    # Output: observed sections plus extra interpolated shapes in between.
    output_sections = [
        (995, 115, {"cx": 365, "cy": 58, "rx": 54, "ry": 31, "phase": 0.0, "lobed": 0}),
        (970, 245, {"cx": 371, "cy": 61, "rx": 88, "ry": 32, "phase": 0.4, "lobed": 1}),
        (990, 375, {"cx": 376, "cy": 63, "rx": 126, "ry": 37, "phase": 0.8, "lobed": 1}),
        (1010, 505, {"cx": 380, "cy": 63, "rx": 110, "ry": 35, "phase": 1.2, "lobed": 1}),
        (990, 635, {"cx": 372, "cy": 62, "rx": 78, "ry": 31, "phase": 1.6, "lobed": 1}),
        (1015, 765, {"cx": 360, "cy": 62, "rx": 47, "ry": 27, "phase": 1.5, "lobed": 0}),
    ]
    for i, (x, y, tissue) in enumerate(output_sections):
        draw_slide(im, x * SCALE, y * SCALE, tissue, seed=200 + i)

    # Subtle reconstruction cue without text.
    draw = ImageDraw.Draw(im, "RGBA")
    arrow = [
        (810 * SCALE, 500 * SCALE),
        (888 * SCALE, 500 * SCALE),
        (888 * SCALE, 460 * SCALE),
        (960 * SCALE, 540 * SCALE),
        (888 * SCALE, 620 * SCALE),
        (888 * SCALE, 580 * SCALE),
        (810 * SCALE, 580 * SCALE),
    ]
    draw.polygon(arrow, fill=rgba("#111111", 205))

    return im.resize((W, H), Image.Resampling.LANCZOS).convert("RGB")


if __name__ == "__main__":
    fig = make_figure()
    fig.save(OUT, quality=95)
    print(OUT)
