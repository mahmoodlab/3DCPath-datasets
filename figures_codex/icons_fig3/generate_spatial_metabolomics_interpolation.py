from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


OUT = Path(__file__).with_name("spatial_metabolomics_interpolation.png")
W, H = 1500, 900
SCALE = 3
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size * SCALE)


def rgba(hex_color: str, alpha: int = 255) -> tuple[int, int, int, int]:
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def interp(a: tuple[float, ...], b: tuple[float, ...], t: float) -> tuple[float, ...]:
    return tuple(lerp(x, y, t) for x, y in zip(a, b))


def heat_color(v: float) -> tuple[int, int, int, int]:
    stops = [
        (0.00, (44, 16, 100)),
        (0.24, (103, 24, 119)),
        (0.48, (190, 44, 95)),
        (0.72, (235, 97, 63)),
        (1.00, (248, 211, 85)),
    ]
    for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
        if p0 <= v <= p1:
            t = (v - p0) / (p1 - p0)
            return (
                int(lerp(c0[0], c1[0], t)),
                int(lerp(c0[1], c1[1], t)),
                int(lerp(c0[2], c1[2], t)),
                255,
            )
    return (*stops[-1][1], 255)


def tissue_polygon(cx: float, cy: float, rx: float, ry: float, phase: float, tilt: float) -> list[tuple[float, float]]:
    pts = []
    ct, st = math.cos(tilt), math.sin(tilt)
    for i in range(180):
        a = 2 * math.pi * i / 180.0
        wobble = 1.0 + 0.18 * math.sin(2.0 * a + phase) + 0.09 * math.sin(5.0 * a - 0.6 * phase)
        x = rx * wobble * math.cos(a)
        y = ry * (1.0 + 0.08 * math.cos(3.0 * a + phase)) * wobble * math.sin(a)
        pts.append((cx + x * ct - y * st, cy + x * st + y * ct))
    return pts


def draw_heatmap_tissue(
    im: Image.Image,
    spec: tuple[float, float, float, float, float, float],
    seed: int,
    interpolated: bool = False,
) -> None:
    cx, cy, rx, ry, phase, tilt = [v * SCALE for v in spec[:4]] + [spec[4], spec[5]]
    rng = random.Random(seed)
    poly = tissue_polygon(cx, cy, rx, ry, phase, tilt)

    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).polygon([(int(x), int(y)) for x, y in poly], fill=255)
    md = ImageDraw.Draw(mask)

    # A small satellite lobe helps make section shape changes easier to read.
    sat_x = cx - rx * 0.62 * math.cos(tilt) + ry * 0.08 * math.sin(tilt)
    sat_y = cy - rx * 0.62 * math.sin(tilt) - ry * 0.08 * math.cos(tilt)
    md.ellipse(
        (sat_x - rx * 0.34, sat_y - ry * 0.55, sat_x + rx * 0.28, sat_y + ry * 0.48),
        fill=255,
    )
    mask = mask.filter(ImageFilter.GaussianBlur(1.2 * SCALE))

    pix = layer.load()
    mask_pix = mask.load()
    min_x = max(0, int(cx - rx * 1.45))
    max_x = min(im.size[0], int(cx + rx * 1.45))
    min_y = max(0, int(cy - ry * 1.45))
    max_y = min(im.size[1], int(cy + ry * 1.45))
    for y in range(min_y, max_y, 2 * SCALE):
        for x in range(min_x, max_x, 2 * SCALE):
            a = mask_pix[x, y]
            if a < 18:
                continue
            nx = (x - cx) / max(rx, 1)
            ny = (y - cy) / max(ry, 1)
            field = (
                0.48
                + 0.27 * math.sin(2.8 * nx + phase)
                + 0.19 * math.cos(3.3 * ny - phase)
                + 0.10 * rng.uniform(-1, 1)
            )
            field = max(0.0, min(1.0, field))
            col = heat_color(field)
            rad = rng.uniform(2.3, 4.8) * SCALE
            ImageDraw.Draw(layer, "RGBA").ellipse(
                (x - rad, y - rad, x + rad, y + rad),
                fill=(col[0], col[1], col[2], min(235, a + 70)),
            )

    layer.putalpha(mask)
    im.alpha_composite(layer)

    edge = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ed = ImageDraw.Draw(edge, "RGBA")
    ed.line(poly + [poly[0]], fill=rgba("#8e256f", 150), width=2 * SCALE)
    im.alpha_composite(edge)


def draw_arrow(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    x *= SCALE
    y *= SCALE
    bars = [44, 68, 54, 40, 32, 40, 54, 68]
    for i, h in enumerate(bars):
        bx = x + i * 18 * SCALE
        draw.rounded_rectangle(
            (bx, y - h * SCALE / 2, bx + 9 * SCALE, y + h * SCALE / 2),
            radius=3 * SCALE,
            fill=rgba("#adadb2", 220),
        )


def label(
    im: Image.Image,
    draw: ImageDraw.ImageDraw,
    text: str,
    x: int,
    y: int,
    fnt: ImageFont.FreeTypeFont,
    rotate: bool = False,
) -> None:
    if not rotate:
        draw.text((x * SCALE, y * SCALE), text, fill=rgba("#111111"), font=fnt)
        return
    bbox = draw.textbbox((0, 0), text, font=fnt)
    tile = Image.new("RGBA", (bbox[2] + 20 * SCALE, bbox[3] + 20 * SCALE), (0, 0, 0, 0))
    td = ImageDraw.Draw(tile)
    td.text((10 * SCALE, 2 * SCALE), text, fill=rgba("#111111"), font=fnt)
    tile = tile.rotate(90, expand=True, resample=Image.Resampling.BICUBIC)
    im.alpha_composite(tile, (x * SCALE, y * SCALE))


def make_figure() -> Image.Image:
    base = Image.new("RGBA", (W * SCALE, H * SCALE), (255, 255, 255, 255))
    draw = ImageDraw.Draw(base, "RGBA")
    title_font = font(BOLD, 42)
    z_font = font(FONT, 34)
    z_small = font(FONT, 27)

    label(base, draw, "Spatial metabolomics", 118, 34, title_font)

    z1 = (238, 250, 108, 42, 0.35, -0.02)
    z3 = (238, 450, 92, 54, 1.45, -0.01)
    z5 = (238, 650, 45, 31, 2.15, 0.03)
    z2 = interp(z1, z3, 0.5)
    z4 = interp(z3, z5, 0.5)

    left_specs = [(1, z1), (3, z3), (5, z5)]
    for z, spec in left_specs:
        label(base, draw, f"Z={z}", 38, int(spec[1]) - 64, z_font, rotate=True)
        draw_heatmap_tissue(base, spec, seed=10 + z)

    draw_arrow(draw, 460, 450)

    # Right panel: measured Z=1,3,5 are copied from the left-side templates.
    # Z=2 and Z=4 are slight morphs between the neighboring measured sections.
    right_specs = [
        (1, (925, 170, z1[2], z1[3], z1[4], z1[5]), False, 11),
        (2, (925, 310, z2[2] * 1.03, z2[3] * 0.98, z2[4] + 0.18, z2[5]), True, 22),
        (3, (925, 450, z3[2], z3[3], z3[4], z3[5]), False, 13),
        (4, (925, 590, z4[2] * 0.97, z4[3] * 1.02, z4[4] - 0.14, z4[5]), True, 24),
        (5, (925, 730, z5[2], z5[3], z5[4], z5[5]), False, 15),
    ]

    for z, spec, interpolated, seed in right_specs:
        label(base, draw, f"Z={z}", 730, int(spec[1]) - 48, z_small, rotate=True)
        draw_heatmap_tissue(base, spec, seed=seed, interpolated=interpolated)

    return base.resize((W, H), Image.Resampling.LANCZOS).convert("RGB")


if __name__ == "__main__":
    fig = make_figure()
    fig.save(OUT, quality=95)
    print(OUT)
