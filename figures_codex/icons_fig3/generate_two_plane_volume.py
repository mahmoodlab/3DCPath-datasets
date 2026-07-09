from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


OUT = Path(__file__).with_name("two_plane_volume_schematic.png")
W, H = 760, 980
SCALE = 3


def rgba(hex_color: str, alpha: int) -> tuple[int, int, int, int]:
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def scaled(points: list[tuple[float, float]]) -> list[tuple[int, int]]:
    return [(round(x * SCALE), round(y * SCALE)) for x, y in points]


def draw_tissue(draw: ImageDraw.ImageDraw) -> None:
    lobes = [
        [(120, 255), (190, 210), (305, 255), (418, 350), (565, 420), (690, 575),
         (715, 705), (630, 800), (455, 795), (300, 700), (185, 585), (85, 430)],
        [(80, 395), (180, 330), (325, 355), (480, 440), (610, 560), (665, 710),
         (590, 815), (420, 820), (250, 730), (105, 620), (35, 500)],
        [(90, 570), (210, 500), (390, 520), (535, 615), (605, 745), (545, 850),
         (390, 855), (230, 790), (100, 690)],
        [(170, 735), (270, 700), (370, 740), (405, 830), (355, 920), (260, 955),
         (185, 890)],
    ]
    for i, pts in enumerate(lobes):
        fill = rgba("#d89a94", 118 - i * 8)
        outline = rgba("#c85f66", 128)
        draw.polygon(scaled(pts), fill=fill)
        draw.line(scaled(pts + [pts[0]]), fill=outline, width=5 * SCALE, joint="curve")

    inner = [
        [(92, 438), (175, 388), (300, 386), (420, 435), (525, 540), (615, 665),
         (615, 742), (525, 765), (380, 725), (238, 633), (125, 535)],
        [(85, 710), (190, 665), (295, 680), (345, 750), (292, 820), (165, 805)],
    ]
    for pts in inner:
        draw.line(scaled(pts), fill=rgba("#c85f66", 95), width=4 * SCALE, joint="curve")

    highlights = [
        (150, 410, 176, 535),
        (160, 670, 215, 690),
        (455, 675, 515, 705),
    ]
    for x0, y0, x1, y1 in highlights:
        draw.rounded_rectangle(
            (x0 * SCALE, y0 * SCALE, x1 * SCALE, y1 * SCALE),
            radius=14 * SCALE,
            fill=rgba("#ffffff", 76),
        )


def draw_plane(draw: ImageDraw.ImageDraw, x: int) -> None:
    y0, y1 = 70 * SCALE, 910 * SCALE
    for dx, color, width in [
        (-7, rgba("#191919", 235), 4),
        (-2, rgba("#f4f4f4", 235), 3),
        (4, rgba("#191919", 235), 4),
    ]:
        draw.line((x * SCALE + dx * SCALE, y0, x * SCALE + dx * SCALE, y1), fill=color, width=width * SCALE)
    draw.line((x * SCALE - 11 * SCALE, y0, x * SCALE + 9 * SCALE, y0), fill=rgba("#888888", 180), width=2 * SCALE)
    draw.line((x * SCALE - 11 * SCALE, y1, x * SCALE + 9 * SCALE, y1), fill=rgba("#888888", 180), width=2 * SCALE)


def make_figure() -> Image.Image:
    im = Image.new("RGBA", (W * SCALE, H * SCALE), (255, 255, 255, 255))

    tissue = Image.new("RGBA", im.size, (0, 0, 0, 0))
    draw_tissue(ImageDraw.Draw(tissue, "RGBA"))
    tissue = tissue.filter(ImageFilter.GaussianBlur(0.45 * SCALE))
    im.alpha_composite(tissue)

    draw = ImageDraw.Draw(im, "RGBA")
    draw_plane(draw, 285)
    draw_plane(draw, 475)

    return im.resize((W, H), Image.Resampling.LANCZOS).convert("RGB")


if __name__ == "__main__":
    fig = make_figure()
    fig.save(OUT, quality=95)
    print(OUT)
