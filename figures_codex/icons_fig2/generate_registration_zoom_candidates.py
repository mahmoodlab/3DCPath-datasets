from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


BASE_DIR = Path(__file__).resolve().parent
INPUT = BASE_DIR / "registration_zoom_outputs" / "registration_zoom_comparison.png"
OUTPUT_DIR = BASE_DIR / "registration_zoom_outputs" / "zoom_region_candidates"

# Bounding boxes for the full-size panels in registration_zoom_comparison.png.
# Format: (left, upper, right, lower)
GLOBAL_PANEL = (18, 420, 2357, 1599)
ELASTIC_PANEL = (2720, 420, 5059, 1599)

# Candidate ROIs are defined in normalized panel coordinates:
# (label, center_x, center_y, width_fraction, height_fraction)
ROIS = [
    ("A", 0.58, 0.58, 0.50, 0.68),
    ("B", 0.23, 0.60, 0.50, 0.68),
    ("C", 0.50, 0.30, 0.50, 0.68),
    ("D", 0.77, 0.48, 0.50, 0.68),
    ("E", 0.47, 0.79, 0.50, 0.68),
    ("F", 0.17, 0.33, 0.50, 0.68),
]


def roi_box(panel, cx, cy, wf, hf):
    left, upper, right, lower = panel
    width = right - left
    height = lower - upper
    crop_w = int(width * wf)
    crop_h = int(height * hf)
    center_x = left + int(width * cx)
    center_y = upper + int(height * cy)
    x0 = max(left, min(right - crop_w, center_x - crop_w // 2))
    y0 = max(upper, min(lower - crop_h, center_y - crop_h // 2))
    return (x0, y0, x0 + crop_w, y0 + crop_h)


def crop_pair(image, roi):
    _, cx, cy, wf, hf = roi
    return (
        image.crop(roi_box(GLOBAL_PANEL, cx, cy, wf, hf)),
        image.crop(roi_box(ELASTIC_PANEL, cx, cy, wf, hf)),
    )


def font(size):
    for candidate in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def resize_to_width(image, width):
    height = round(image.height * width / image.width)
    return image.resize((width, height), Image.Resampling.LANCZOS)


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


def compose_pair(before, after, label, crop_width=920):
    title_font = font(38)
    roi_font = font(36)
    before = resize_to_width(before, crop_width)
    after = resize_to_width(after, crop_width)

    gutter = 70
    top = 88
    bottom = 34
    left_label = 150
    width = left_label + crop_width * 2 + gutter
    height = top + max(before.height, after.height) + bottom

    canvas = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(canvas)
    draw_centered(
        draw,
        (left_label, 8, left_label + crop_width, top - 8),
        "Before elastic registration",
        (20, 20, 20),
        title_font,
    )
    draw_centered(
        draw,
        (left_label + crop_width + gutter, 8, width, top - 8),
        "After elastic registration",
        (20, 20, 20),
        title_font,
    )
    draw.text((16, top + before.height / 2 - 28), f"ROI {label}", fill=(20, 20, 20), font=roi_font)
    canvas.paste(before, (left_label, top))
    canvas.paste(after, (left_label + crop_width + gutter, top))
    return canvas


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    image = Image.open(INPUT).convert("RGB")

    pairs = [(roi[0], *crop_pair(image, roi)) for roi in ROIS]

    rows = [compose_pair(before, after, label) for label, before, after in pairs]
    row_gap = 34
    contact_width = max(row.width for row in rows)
    contact_height = sum(row.height for row in rows) + row_gap * (len(rows) - 1)
    contact = Image.new("RGB", (contact_width, contact_height), "white")
    y = 0
    for row in rows:
        contact.paste(row, ((contact_width - row.width) // 2, y))
        y += row.height + row_gap

    contact_png = OUTPUT_DIR / "registration_zoom_region_candidates_contact_sheet.png"
    contact_pdf = OUTPUT_DIR / "registration_zoom_region_candidates_contact_sheet.pdf"
    contact.save(contact_png, dpi=(300, 300))
    contact.save(contact_pdf, "PDF", resolution=300)

    separate_pages = []
    for row, (label, _, _) in zip(rows, pairs):
        row.save(
            OUTPUT_DIR / f"registration_zoom_region_candidate_{label}.png",
            dpi=(300, 300),
        )
        separate_pages.append(row)
    separate_pages[0].save(
        OUTPUT_DIR / "registration_zoom_region_candidates_separate.pdf",
        "PDF",
        save_all=True,
        append_images=separate_pages[1:],
        resolution=300,
    )


if __name__ == "__main__":
    main()
