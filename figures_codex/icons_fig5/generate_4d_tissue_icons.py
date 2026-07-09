from pathlib import Path
import random
import subprocess


OUT = Path(__file__).resolve().parent
W, H = 1200, 420


def poly(points, **attrs):
    attr = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    return f"<polygon points=\"{pts}\" {attr}/>"


def line(x1, y1, x2, y2, **attrs):
    attr = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" {attr}/>'


def path(d, **attrs):
    attr = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    return f'<path d="{d}" {attr}/>'


def text(x, y, s, size=34, weight=600, fill="#222", anchor="middle"):
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
        f'font-family="Arial, Helvetica, sans-serif" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}">{s}</text>'
    )


def arrow_marker(color, marker_id):
    return (
        f'<marker id="{marker_id}" viewBox="0 0 10 10" refX="8" refY="5" '
        f'markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{color}"/></marker>'
    )


def defs():
    return f"""
    <defs>
      {arrow_marker("#5d6168", "arrow_gray")}
      {arrow_marker("#e41f2d", "arrow_red")}
      {arrow_marker("#1874bd", "arrow_blue")}
      {arrow_marker("#49a24d", "arrow_green")}
      <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
        <feDropShadow dx="0" dy="6" stdDeviation="5" flood-color="#000" flood-opacity="0.16"/>
      </filter>
      <linearGradient id="faceFront" x1="0" x2="1" y1="0" y2="1">
        <stop offset="0%" stop-color="#20c5d2"/>
        <stop offset="45%" stop-color="#43d69a"/>
        <stop offset="100%" stop-color="#9ce35c"/>
      </linearGradient>
      <linearGradient id="faceTop" x1="0" x2="1" y1="0" y2="1">
        <stop offset="0%" stop-color="#6ee8e9"/>
        <stop offset="100%" stop-color="#eaa0d8"/>
      </linearGradient>
      <linearGradient id="faceSide" x1="0" x2="1" y1="0" y2="1">
        <stop offset="0%" stop-color="#36b9be"/>
        <stop offset="100%" stop-color="#8aca46"/>
      </linearGradient>
      <radialGradient id="lesionPink" cx="48%" cy="45%" r="52%">
        <stop offset="0%" stop-color="#ff7db9" stop-opacity="0.95"/>
        <stop offset="62%" stop-color="#f3a1d1" stop-opacity="0.72"/>
        <stop offset="100%" stop-color="#f3a1d1" stop-opacity="0"/>
      </radialGradient>
    </defs>
    """


def texture_for_face(clip_id, x, y, w, h, seed, lesion=0.55):
    rng = random.Random(seed)
    parts = [f'<g clip-path="url(#{clip_id})" opacity="0.95">']
    parts.append(f'<rect x="{x-120}" y="{y-120}" width="{w+240}" height="{h+240}" fill="url(#faceFront)"/>')
    cx = x + w * (0.32 + 0.12 * rng.random())
    cy = y + h * (0.28 + 0.2 * rng.random())
    rx = w * (0.22 + 0.08 * rng.random()) * lesion
    ry = h * (0.20 + 0.06 * rng.random()) * lesion
    parts.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="url(#lesionPink)"/>')
    for _ in range(42):
        px = x + rng.random() * w
        py = y + rng.random() * h
        r = rng.uniform(2.0, 5.8)
        color = rng.choice(["#f5f32f", "#1ac7ff", "#00a783", "#bdf35c", "#ee7db4", "#ffffff"])
        opacity = rng.uniform(0.45, 0.88)
        parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r:.1f}" fill="{color}" opacity="{opacity:.2f}"/>')
    for _ in range(18):
        x1 = x + rng.random() * w
        y1 = y + rng.random() * h
        x2 = x1 + rng.uniform(-30, 46)
        y2 = y1 + rng.uniform(-16, 26)
        color = rng.choice(["#f1ef33", "#16bdd8", "#70e25f", "#f49ac8"])
        parts.append(line(x1, y1, x2, y2, stroke=color, stroke_width=rng.uniform(2.0, 4.5), stroke_linecap="round", opacity="0.72"))
    parts.append("</g>")
    return "\n".join(parts)


def cube(x, y, size, depth, clip_prefix, seed=1, opacity=1, lesion=0.65):
    top = [(x, y), (x + depth, y - depth * 0.52), (x + size + depth, y - depth * 0.52), (x + size, y)]
    front = [(x, y), (x + size, y), (x + size, y + size), (x, y + size)]
    side = [(x + size, y), (x + size + depth, y - depth * 0.52), (x + size + depth, y + size - depth * 0.52), (x + size, y + size)]
    top_id, front_id, side_id = f"{clip_prefix}_top", f"{clip_prefix}_front", f"{clip_prefix}_side"
    parts = [f'<g filter="url(#softShadow)" opacity="{opacity}">']
    parts.extend([
        f'<clipPath id="{top_id}">{poly(top)}</clipPath>',
        f'<clipPath id="{front_id}">{poly(front)}</clipPath>',
        f'<clipPath id="{side_id}">{poly(side)}</clipPath>',
        poly(top, fill="url(#faceTop)", stroke="#8e979d", stroke_width="3", stroke_linejoin="round"),
        poly(side, fill="url(#faceSide)", stroke="#8e979d", stroke_width="3", stroke_linejoin="round"),
        poly(front, fill="url(#faceFront)", stroke="#8e979d", stroke_width="3", stroke_linejoin="round"),
        texture_for_face(top_id, x, y - depth * 0.55, size + depth, depth + 18, seed + 10, lesion * 0.78),
        texture_for_face(side_id, x + size, y - depth * 0.55, depth + 20, size + 24, seed + 20, lesion * 0.5),
        texture_for_face(front_id, x, y, size, size, seed + 30, lesion),
    ])
    parts.extend([
        poly(top, fill="none", stroke="#879198", stroke_width="3", stroke_linejoin="round"),
        poly(side, fill="none", stroke="#879198", stroke_width="3", stroke_linejoin="round"),
        poly(front, fill="none", stroke="#879198", stroke_width="3", stroke_linejoin="round"),
        line(x + size, y, x + size, y + size, stroke="#777f86", stroke_width="3"),
        line(x + size, y, x + size + depth, y - depth * 0.52, stroke="#777f86", stroke_width="3"),
        "</g>",
    ])
    return "\n".join(parts)


def axes(x, y, scale=1.0):
    return "\n".join([
        line(x, y, x + 150 * scale, y, stroke="#e41f2d", stroke_width="7", marker_end="url(#arrow_red)"),
        line(x, y, x - 78 * scale, y + 58 * scale, stroke="#1874bd", stroke_width="7", marker_end="url(#arrow_blue)"),
        line(x, y, x, y - 145 * scale, stroke="#49a24d", stroke_width="7", marker_end="url(#arrow_green)"),
        text(x + 174 * scale, y + 21 * scale, "X", 46 * scale, 700, "#e41f2d"),
        text(x - 92 * scale, y + 74 * scale, "Y", 46 * scale, 700, "#1874bd"),
        text(x - 21 * scale, y - 159 * scale, "Z", 46 * scale, 700, "#49a24d"),
    ])


def base_svg(body):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">\n'
        '<rect width="100%" height="100%" fill="#fffdf7"/>\n'
        f'{defs()}\n{body}\n</svg>\n'
    )


def variant_one():
    body = [
        text(605, 58, "3D + Time", 54, 500),
        text(605, 108, "Temporal axis", 32, 600, "#30343a"),
        axes(112, 330, 0.82),
        path("M 245 275 C 390 155, 570 148, 768 116 C 885 96, 996 91, 1090 77",
             fill="none", stroke="#626870", stroke_width="4.5", stroke_dasharray="9 12",
             stroke_linecap="round", marker_end="url(#arrow_gray)"),
        cube(210, 238, 100, 42, "v1_c0", 10, 0.50, 0.55),
        cube(263, 221, 110, 46, "v1_c1", 20, 0.72, 0.7),
        cube(345, 186, 125, 52, "v1_c2", 30, 1.0, 0.85),
        cube(573, 135, 122, 52, "v1_c3", 40, 1.0, 0.68),
        cube(876, 96, 120, 54, "v1_c4", 50, 1.0, 0.45),
        text(261, 378, "t0", 24, 700, "#4a4f55"),
        text(630, 332, "t1", 24, 700, "#4a4f55"),
        text(934, 290, "t2", 24, 700, "#4a4f55"),
    ]
    return base_svg("\n".join(body))


def variant_two():
    body = [
        text(96, 60, "4D tissue evolution", 38, 700, "#222", "start"),
        axes(92, 333, 0.7),
        path("M 205 300 C 365 205, 515 246, 665 174 S 960 108, 1095 92",
             fill="none", stroke="#5b6068", stroke_width="6", stroke_dasharray="2 16",
             stroke_linecap="round", marker_end="url(#arrow_gray)"),
        text(1002, 62, "time", 30, 700, "#5b6068"),
        cube(205, 236, 96, 40, "v2_c0", 100, 1.0, 0.9),
        cube(430, 205, 112, 48, "v2_c1", 110, 1.0, 0.72),
        cube(666, 154, 124, 52, "v2_c2", 120, 1.0, 0.58),
        cube(910, 114, 112, 48, "v2_c3", 130, 1.0, 0.35),
        text(252, 370, "baseline", 23, 700, "#4a4f55"),
        text(486, 346, "growth", 23, 700, "#4a4f55"),
        text(724, 304, "remodeling", 23, 700, "#4a4f55"),
        text(969, 271, "response", 23, 700, "#4a4f55"),
    ]
    return base_svg("\n".join(body))


def variant_three():
    body = [
        path("M 130 84 L 1080 84", fill="none", stroke="#60666d", stroke_width="5",
             stroke_linecap="round", marker_end="url(#arrow_gray)"),
        text(605, 51, "Temporal axis", 30, 700, "#333"),
        axes(102, 332, 0.68),
    ]
    for i, x in enumerate([205, 414, 624, 834]):
        body.append(line(x + 67, 88, x + 67, 151, stroke="#aeb5ba", stroke_width="3", stroke_dasharray="5 8"))
        body.append(cube(x, 165 - i * 12, 112, 46, f"v3_c{i}", 200 + i * 12, 1.0, 0.95 - i * 0.18))
        body.append(text(x + 55, 365 - i * 12, f"T{i}", 24, 700, "#4a4f55"))
    body.append(text(1080, 52, "3D + time", 30, 700, "#222", "end"))
    return base_svg("\n".join(body))


def variant_four():
    body = [
        text(82, 60, "3D tissue images over time", 36, 700, "#222", "start"),
        path("M 165 305 C 352 174, 548 271, 744 151 C 855 84, 990 85, 1100 128",
             fill="none", stroke="#596069", stroke_width="5.5", stroke_dasharray="10 12",
             stroke_linecap="round", marker_end="url(#arrow_gray)"),
        axes(90, 335, 0.62),
        cube(188, 240, 88, 38, "v4_c0", 310, 0.42, 0.75),
        cube(236, 218, 96, 40, "v4_c1", 320, 0.66, 0.82),
        cube(308, 183, 108, 45, "v4_c2", 330, 1.0, 0.95),
        cube(558, 167, 116, 50, "v4_c3", 340, 1.0, 0.7),
        cube(870, 111, 126, 54, "v4_c4", 350, 1.0, 0.42),
        text(358, 354, "serial 3D volumes", 24, 700, "#4a4f55"),
        text(917, 292, "later state", 24, 700, "#4a4f55"),
    ]
    return base_svg("\n".join(body))


def main():
    variants = {
        "temporal_4d_tissue_v1.svg": variant_one(),
        "temporal_4d_tissue_v2.svg": variant_two(),
        "temporal_4d_tissue_v3.svg": variant_three(),
        "temporal_4d_tissue_v4.svg": variant_four(),
    }
    for name, svg in variants.items():
        svg_path = OUT / name
        svg_path.write_text(svg)
        png_path = svg_path.with_suffix(".png")
        subprocess.run(
            ["rsvg-convert", str(svg_path), "-w", str(W), "-h", str(H), "-o", str(png_path)],
            check=True,
        )


if __name__ == "__main__":
    main()
