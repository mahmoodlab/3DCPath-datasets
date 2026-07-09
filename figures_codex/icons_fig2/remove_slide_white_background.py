from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image


BASE_DIR = Path(__file__).resolve().parent
SOURCES = [
    "microscope_slides_he_tissue.png",
    "microscope_slides_he_tissue_v2.png",
    "microscope_slides_sectioned_tissue.png",
]


def connected_light_background(rgb):
    arr = np.asarray(rgb, dtype=np.int16)
    maxc = arr.max(axis=2)
    minc = arr.min(axis=2)

    # The exterior is near white or very pale gray; the slide glass/tissue edges
    # are less bright or more saturated, so they stop the flood fill.
    light = (minc > 232) & ((maxc - minc) < 18)
    height, width = light.shape
    visited = np.zeros_like(light, dtype=bool)
    queue = deque()

    for x in range(width):
        if light[0, x]:
            queue.append((0, x))
        if light[height - 1, x]:
            queue.append((height - 1, x))
    for y in range(height):
        if light[y, 0]:
            queue.append((y, 0))
        if light[y, width - 1]:
            queue.append((y, width - 1))

    while queue:
        y, x = queue.popleft()
        if visited[y, x] or not light[y, x]:
            continue
        visited[y, x] = True
        for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
            if 0 <= ny < height and 0 <= nx < width and not visited[ny, nx]:
                queue.append((ny, nx))

    return visited, minc


def remove_background(path):
    image = Image.open(path).convert("RGB")
    arr = np.asarray(image).copy()
    background, minc = connected_light_background(image)

    alpha = np.full(background.shape, 255, dtype=np.uint8)

    # Fade only the connected exterior background; this preserves anti-aliased
    # edges and soft shadows without leaving a white rectangle.
    transparent = background & (minc > 244)
    fade = background & ~transparent
    alpha[transparent] = 0
    alpha[fade] = np.clip((244 - minc[fade]) * 10, 18, 150).astype(np.uint8)

    rgba = np.dstack([arr, alpha])
    out = Image.fromarray(rgba, "RGBA")
    out_path = path.with_name(f"{path.stem}_transparent.png")
    out.save(out_path)
    save_checker_preview(out, out_path.with_name(f"{path.stem}_transparent_preview.png"))
    return out_path


def save_checker_preview(image, out_path):
    width, height = image.size
    tile = 32
    yy, xx = np.mgrid[:height, :width]
    checks = ((xx // tile + yy // tile) % 2).astype(np.uint8)
    bg = np.where(checks[..., None] == 0, 238, 205).astype(np.uint8)
    bg = np.repeat(bg, 3, axis=2)
    preview = Image.fromarray(bg, "RGB").convert("RGBA")
    preview.alpha_composite(image)
    preview.convert("RGB").save(out_path)


def main():
    for name in SOURCES:
        out_path = remove_background(BASE_DIR / name)
        print(out_path)


if __name__ == "__main__":
    main()
