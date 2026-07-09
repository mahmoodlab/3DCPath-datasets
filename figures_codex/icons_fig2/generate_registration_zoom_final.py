from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "registration_zoom_outputs"

GLOBAL_SOURCE = OUTPUT_DIR / "generated_red_box_overlay_colormap_inset.png"
ELASTIC_CONTEXT_SOURCE = OUTPUT_DIR / "generated_after_elastic_overlay_colormap_inset.png"
ELASTIC_REDUCED_LUMEN_SOURCE = OUTPUT_DIR / "generated_after_elastic_overlay_colormap_inset_v2.png"


def font(size):
    for candidate in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def draw_centered(draw, box, text, fill, used_font):
    x0, y0, x1, y1 = box
    bbox = draw.textbbox((0, 0), text, font=used_font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    draw.text(
        (x0 + (x1 - x0 - text_w) / 2, y0 + (y1 - y0 - text_h) / 2),
        text,
        fill=fill,
        font=used_font,
    )


def save_png_and_pdf(image, stem):
    rgb = image.convert("RGB")
    rgb.save(OUTPUT_DIR / f"{stem}.png", dpi=(300, 300))
    rgb.save(OUTPUT_DIR / f"{stem}.pdf", "PDF", resolution=300)


def elastic_panel_with_recovered_context():
    context = Image.open(ELASTIC_CONTEXT_SOURCE).convert("RGB")
    reduced_lumen = Image.open(ELASTIC_REDUCED_LUMEN_SOURCE).convert("RGB")
    if context.size != reduced_lumen.size:
        reduced_lumen = reduced_lumen.resize(context.size, Image.Resampling.LANCZOS)

    width, height = context.size
    mask = Image.new("L", (width, height), 0)
    pixels = mask.load()

    # Recover only the upper-left tissue context from the full-context elastic render.
    # The arrowed lumen boundary stays from the reduced-lumen elastic render.
    solid_x = int(width * 0.30)
    fade_x = int(width * 0.48)
    solid_y = int(height * 0.16)
    fade_y = int(height * 0.31)
    for y in range(fade_y):
        for x in range(fade_x):
            x_alpha = 1.0 if x <= solid_x else 1.0 - (x - solid_x) / max(1, fade_x - solid_x)
            y_alpha = 1.0 if y <= solid_y else 1.0 - (y - solid_y) / max(1, fade_y - solid_y)
            pixels[x, y] = int(255 * max(0.0, min(x_alpha, y_alpha)))

    elastic = Image.composite(context, reduced_lumen, mask)
    return reduce_arrowed_green_band(elastic)


def reduce_arrowed_green_band(image):
    arr = np.asarray(image.convert("RGB"), dtype=np.float32)
    height, width = arr.shape[:2]
    yy, xx = np.mgrid[:height, :width]

    # Localize the correction to the tissue-in-lumen region highlighted by the arrow.
    cx, cy = width * 0.40, height * 0.47
    rx, ry = width * 0.16, height * 0.28
    region = ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 < 1.0

    red = arr[..., 0]
    green = arr[..., 1]
    blue = arr[..., 2]
    green_dominant = (green > red * 1.06) & (green > blue * 1.06)
    visible_green = green_dominant & (green - np.maximum(red, blue) > 9)
    target = region & visible_green

    overlap_gray = (red + green + blue) / 3.0
    arr[..., 0][target] = np.maximum(red[target], overlap_gray[target] * 1.08)
    arr[..., 1][target] = green[target] * 0.76 + overlap_gray[target] * 0.24
    arr[..., 2][target] = np.maximum(blue[target], overlap_gray[target] * 1.04)

    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")


def comparison_image(global_panel, elastic_panel):
    title_font = font(46)
    panel_w, panel_h = global_panel.size
    gutter = 90
    top = 82
    margin = 18
    canvas_w = margin * 2 + panel_w * 2 + gutter
    canvas_h = margin + top + panel_h
    canvas = Image.new("RGB", (canvas_w, canvas_h), "white")
    draw = ImageDraw.Draw(canvas)

    left_x = margin
    right_x = margin + panel_w + gutter
    draw_centered(
        draw,
        (left_x, margin, left_x + panel_w, margin + top - 10),
        "Global registration zoom",
        (0, 0, 0),
        title_font,
    )
    draw_centered(
        draw,
        (right_x, margin, right_x + panel_w, margin + top - 10),
        "Elastic registration zoom",
        (0, 0, 0),
        title_font,
    )
    canvas.paste(global_panel, (left_x, margin + top))
    canvas.paste(elastic_panel, (right_x, margin + top))
    return canvas


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    global_panel = Image.open(GLOBAL_SOURCE).convert("RGB")
    elastic_panel = elastic_panel_with_recovered_context()

    if global_panel.size != elastic_panel.size:
        elastic_panel = elastic_panel.resize(global_panel.size, Image.Resampling.LANCZOS)

    save_png_and_pdf(global_panel, "global_registration_zoom")
    save_png_and_pdf(elastic_panel, "elastic_registration_zoom")
    save_png_and_pdf(
        comparison_image(global_panel, elastic_panel),
        "registration_zoom_comparison",
    )

    print(f"Saved registration zoom figures to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
