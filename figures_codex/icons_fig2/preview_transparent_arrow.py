from pathlib import Path

import numpy as np
from PIL import Image


BASE_DIR = Path(__file__).resolve().parent
SOURCE = BASE_DIR / "dark_gray_gradient_arrow.png"
OUTPUT = BASE_DIR / "dark_gray_gradient_arrow_preview.png"


def main():
    arrow = Image.open(SOURCE).convert("RGBA")
    width, height = arrow.size
    tile = 24
    yy, xx = np.mgrid[:height, :width]
    checks = ((xx // tile + yy // tile) % 2).astype(np.uint8)
    bg = np.where(checks[..., None] == 0, 238, 205).astype(np.uint8)
    bg = np.repeat(bg, 3, axis=2)
    preview = Image.fromarray(bg, "RGB").convert("RGBA")
    preview.alpha_composite(arrow)
    preview.convert("RGB").save(OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    main()
