from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter


SRC = Path("pathologists-3d-screen-icon-v2.png")
OUT = Path("pathologists-3d-screen-icon-v2-transparent-v3.png")
PREVIEW = Path("pathologists-3d-screen-icon-v2-transparent-v3-preview.png")


def is_background_candidate(rgb: np.ndarray) -> np.ndarray:
    rgb16 = rgb.astype(np.int16)
    min_channel = rgb16.min(axis=2)
    spread = rgb16.max(axis=2) - min_channel
    very_light = min_channel >= 236
    light_neutral = (min_channel >= 218) & (spread <= 34)
    return very_light | light_neutral


def flood_outer_background(candidate: np.ndarray) -> np.ndarray:
    h, w = candidate.shape
    seen = np.zeros((h, w), dtype=bool)
    q: deque[tuple[int, int]] = deque()

    def push(y: int, x: int) -> None:
        if 0 <= y < h and 0 <= x < w and candidate[y, x] and not seen[y, x]:
            seen[y, x] = True
            q.append((y, x))

    # Seed from top and side edges. Avoid the bottom edge, where white coats
    # can be open to the canvas in generated icon art.
    for x in range(w):
        push(0, x)
    for y in range(h):
        push(y, 0)
        push(y, w - 1)

    while q:
        y, x = q.popleft()
        push(y - 1, x)
        push(y + 1, x)
        push(y, x - 1)
        push(y, x + 1)

    return seen


def main() -> None:
    image = Image.open(SRC).convert("RGBA")
    arr = np.array(image)
    background = flood_outer_background(is_background_candidate(arr[:, :, :3]))

    alpha = np.full(background.shape, 255, dtype=np.uint8)
    alpha[background] = 0

    alpha_img = Image.fromarray(alpha, "L").filter(ImageFilter.GaussianBlur(0.35))
    out = image.copy()
    out.putalpha(alpha_img)
    out.save(OUT)

    preview_bg = Image.new("RGBA", out.size, "#d9e7f2")
    preview_bg.alpha_composite(out)
    preview_bg.convert("RGB").save(PREVIEW)


if __name__ == "__main__":
    main()
