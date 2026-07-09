from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from PIL import JpegImagePlugin  # noqa: F401 - registers PIL's PDF image writer.


OUT_DIR = Path(__file__).resolve().parent
RNG = np.random.default_rng(15674)


def clipped_normal(mean, sd, size, low, high):
    values = RNG.normal(mean, sd, size)
    return np.clip(values, low, high)


def sample_matched_points():
    """Create a point cloud with denser matched points near the Z/reference plane."""
    # Sparse baseline points throughout the tissue volume.
    n_background = 2500
    x_bg = RNG.uniform(0.08, 0.88, n_background)
    y_bg = RNG.uniform(0.08, 0.92, n_background)

    # Strong matched-point enrichment around the reference Z plane.
    z_y = 0.64
    n_z_band = 2600
    x_band = RNG.uniform(0.08, 0.88, n_z_band)
    y_band = clipped_normal(z_y, 0.018, n_z_band, 0.08, 0.92)

    # Local tissue-like dense regions that make the denser sampling look organic.
    clusters = [
        (0.30, 0.18, 0.13, 0.035, 850),
        (0.58, 0.56, 0.08, 0.07, 700),
        (0.68, 0.49, 0.08, 0.06, 550),
        (0.40, 0.83, 0.05, 0.045, 420),
        (0.50, 0.69, 0.05, 0.035, 350),
    ]

    x_clusters = []
    y_clusters = []
    for cx, cy, sx, sy, count in clusters:
        x_clusters.append(clipped_normal(cx, sx, count, 0.08, 0.88))
        y_clusters.append(clipped_normal(cy, sy, count, 0.08, 0.92))

    x = np.concatenate([x_bg, x_band, *x_clusters])
    y = np.concatenate([y_bg, y_band, *y_clusters])

    density_weight = np.exp(-((y - z_y) / 0.055) ** 2)
    alpha = 0.16 + 0.34 * density_weight
    size = 3.5 + 5.5 * density_weight
    return x, y, alpha, size, z_y


def draw_panel():
    x, y, alpha, size, z_y = sample_matched_points()

    width, height = 1530, 2400
    margin = 20
    image = Image.new("RGB", (width, height), "white")
    overlay = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")

    def to_pixel(px, py):
        return int(px * width), int(py * height)

    def ellipse(cx, cy, radius, color, opacity):
        px, py = to_pixel(cx, cy)
        r = max(1, int(radius))
        rgba = (*color, int(255 * opacity))
        draw.ellipse((px - r, py - r, px + r, py + r), fill=rgba)

    teal = (37, 109, 134)
    pale_teal = (119, 174, 190)
    dark_teal = (23, 101, 127)

    # Faint tissue silhouette, then the matched points on top.
    for px, py, point_size in zip(x, y, size):
        ellipse(px, py, point_size * 0.9, pale_teal, 0.035)
    for px, py, point_alpha, point_size in zip(x, y, alpha, size):
        ellipse(px, py, point_size * 0.48, teal, point_alpha)

    # A compressed dense Z/reference layer emphasizes where matching is strongest.
    xs = np.linspace(0.06, 0.91, 420)
    wave = z_y + 0.0035 * np.sin(np.linspace(0, 10 * np.pi, xs.size))
    wave_points = [to_pixel(px, py) for px, py in zip(xs, wave)]
    draw.line(wave_points, fill=(*dark_teal, 148), width=8, joint="curve")
    for px, py in zip(RNG.uniform(0.07, 0.90, 800), clipped_normal(z_y, 0.007, 800, 0.08, 0.92)):
        ellipse(px, py, 3.2, dark_teal, 0.23)

    # Light boundary noise suggests lower confidence away from the dense tissue band.
    edge_x = np.concatenate([
        RNG.uniform(0.04, 0.09, 220),
        RNG.uniform(0.88, 0.94, 220),
    ])
    edge_y = RNG.uniform(0.09, 0.90, edge_x.size)
    for px, py in zip(edge_x, edge_y):
        ellipse(px, py, 2.4, teal, 0.10)

    image = Image.alpha_composite(image.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(image, "RGBA")

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 190)
    except OSError:
        font = ImageFont.load_default()
    z_px, z_py = to_pixel(0.90, z_y + 0.01)
    draw.text((z_px, z_py - 105), "Z", fill=(0, 0, 0, 255), font=font)
    draw.line([to_pixel(0.91, 0.96), to_pixel(0.70, 1.05)], fill=(0, 0, 0, 255), width=9)

    image = image.crop((margin, margin, width - margin, height - margin))

    png_path = OUT_DIR / "matched_points_density_z.png"
    pdf_path = OUT_DIR / "matched_points_density_z.pdf"
    image.convert("RGB").save(png_path, dpi=(600, 600))
    image.convert("RGB").save(pdf_path, resolution=600)
    return png_path, pdf_path


if __name__ == "__main__":
    for path in draw_panel():
        print(path)
