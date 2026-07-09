from pathlib import Path
import random
import subprocess


OUT = Path(__file__).resolve().parent
W, H = 900, 380


def attrs(**kwargs):
    return " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in kwargs.items())


def line(x1, y1, x2, y2, **kw):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" {attrs(**kw)}/>'


def poly(points, **kw):
    pts = " ".join(f"{x},{y}" for x, y in points)
    return f'<polygon points="{pts}" {attrs(**kw)}/>'


def text(x, y, s, size=36, weight=600, fill="#111", anchor="middle"):
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
        f'font-family="Arial, Helvetica, sans-serif" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}">{s}</text>'
    )


def defs():
    return """
    <defs>
      <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5"
              markerWidth="8" markerHeight="8" orient="auto-start-reverse">
        <path d="M 0 0 L 10 5 L 0 10 z" fill="#166fb8"/>
      </marker>
      <filter id="shadow" x="-20%" y="-20%" width="140%" height="150%">
        <feDropShadow dx="0" dy="8" stdDeviation="7" flood-color="#000" flood-opacity="0.22"/>
      </filter>
      <linearGradient id="frontGray" x1="0" x2="1" y1="0" y2="1">
        <stop offset="0%" stop-color="#e8e8e8"/>
        <stop offset="45%" stop-color="#9f9f9f"/>
        <stop offset="100%" stop-color="#3e3e3e"/>
      </linearGradient>
      <linearGradient id="topGray" x1="0" x2="1" y1="0" y2="1">
        <stop offset="0%" stop-color="#f6f6f6"/>
        <stop offset="100%" stop-color="#6e6e6e"/>
      </linearGradient>
      <linearGradient id="sideGray" x1="0" x2="1" y1="0" y2="1">
        <stop offset="0%" stop-color="#b5b5b5"/>
        <stop offset="100%" stop-color="#4d4d4d"/>
      </linearGradient>
      <radialGradient id="tumor" cx="45%" cy="40%" r="58%">
        <stop offset="0%" stop-color="#ff74be"/>
        <stop offset="55%" stop-color="#d91773"/>
        <stop offset="100%" stop-color="#821047"/>
      </radialGradient>
    </defs>
    """


def texture(clip_id, x, y, w, h, seed, dark=False):
    rng = random.Random(seed)
    parts = [f'<g clip-path="url(#{clip_id})">']
    for _ in range(34):
        cx = x + rng.random() * w
        cy = y + rng.random() * h
        rx = rng.uniform(12, 38)
        ry = rng.uniform(4, 14)
        rot = rng.uniform(-35, 35)
        fill = rng.choice(["#1f1f1f", "#3c3c3c", "#686868", "#cfcfcf", "#eeeeee"])
        op = rng.uniform(0.28, 0.72) if not dark else rng.uniform(0.35, 0.78)
        parts.append(
            f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" '
            f'transform="rotate({rot:.1f} {cx:.1f} {cy:.1f})" fill="{fill}" opacity="{op:.2f}"/>'
        )
    for _ in range(42):
        x1 = x + rng.random() * w
        y1 = y + rng.random() * h
        x2 = x1 + rng.uniform(-45, 45)
        y2 = y1 + rng.uniform(-20, 22)
        parts.append(line(f"{x1:.1f}", f"{y1:.1f}", f"{x2:.1f}", f"{y2:.1f}",
                          stroke="#f4f4f4", stroke_width=f"{rng.uniform(1.1, 2.6):.1f}",
                          opacity=f"{rng.uniform(0.28, 0.55):.2f}", stroke_linecap="round"))
    parts.append("</g>")
    return "\n".join(parts)


def tissue_block(present):
    x, y, w, h, d = 88, 116, 260, 128, 72
    top = [(x, y), (x + d, y - 42), (x + w + d, y - 42), (x + w, y)]
    front = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    side = [(x + w, y), (x + w + d, y - 42), (x + w + d, y + h - 42), (x + w, y + h)]
    parts = [
        '<g filter="url(#shadow)">',
        '<clipPath id="topClip">' + poly(top) + '</clipPath>',
        '<clipPath id="frontClip">' + poly(front) + '</clipPath>',
        '<clipPath id="sideClip">' + poly(side) + '</clipPath>',
        poly(top, fill="url(#topGray)", stroke="#161616", stroke_width="5", stroke_linejoin="round"),
        poly(side, fill="url(#sideGray)", stroke="#161616", stroke_width="5", stroke_linejoin="round"),
        poly(front, fill="url(#frontGray)", stroke="#161616", stroke_width="5", stroke_linejoin="round"),
        texture("topClip", x, y - 44, w + d, 54, 20),
        texture("sideClip", x + w, y - 44, d + 18, h + 24, 30, True),
        texture("frontClip", x, y, w, h, 40, True),
    ]
    if present:
        parts.extend([
            '<g clip-path="url(#frontClip)">',
            '<ellipse cx="219" cy="178" rx="42" ry="25" fill="url(#tumor)" opacity="0.96"/>',
            '<circle cx="184" cy="187" r="11" fill="#ff84c9" opacity="0.9"/>',
            '<circle cx="257" cy="169" r="9" fill="#a30959" opacity="0.95"/>',
            '</g>',
            '<g clip-path="url(#topClip)" opacity="0.86">',
            '<ellipse cx="240" cy="101" rx="32" ry="11" fill="#db1a78"/>',
            '</g>',
        ])
    parts.extend([
        poly(top, fill="none", stroke="#151515", stroke_width="5", stroke_linejoin="round"),
        poly(side, fill="none", stroke="#151515", stroke_width="5", stroke_linejoin="round"),
        poly(front, fill="none", stroke="#151515", stroke_width="5", stroke_linejoin="round"),
        "</g>",
    ])
    return "\n".join(parts)


def finding_glyph(present):
    if present:
        fill, stroke = "#d7196f", "#9b0f4d"
        return "\n".join([
            f'<circle cx="776" cy="226" r="25" fill="{fill}" stroke="{stroke}" stroke-width="5"/>',
            '<circle cx="759" cy="213" r="6" fill="#ff9fd1" opacity="0.95"/>',
            '<circle cx="788" cy="239" r="6" fill="#7b0d42" opacity="0.85"/>',
            line(808, 251, 829, 270, stroke=stroke, stroke_width="6", stroke_linecap="round"),
            f'<circle cx="837" cy="276" r="13" fill="{fill}" stroke="{stroke}" stroke-width="4"/>',
        ])
    return "\n".join([
        '<circle cx="778" cy="226" r="25" fill="none" stroke="#8c8c8c" stroke-width="5"/>',
        line(758, 246, 798, 206, stroke="#8c8c8c", stroke_width="6", stroke_linecap="round"),
        line(810, 251, 831, 270, stroke="#8c8c8c", stroke_width="6", stroke_linecap="round"),
        '<circle cx="838" cy="276" r="13" fill="none" stroke="#8c8c8c" stroke-width="4"/>',
    ])


def icon(present):
    status = "present" if present else "absent"
    accent = "#d7196f" if present else "#8c8c8c"
    body = [
        tissue_block(present),
        line(392, 176, 498, 176, stroke="#166fb8", stroke_width="8", marker_end="url(#arrow)", stroke_linecap="round"),
        f'<rect x="520" y="82" width="324" height="216" rx="28" fill="#ffffff" fill-opacity="0.96" '
        f'stroke="{accent}" stroke-width="5"/>',
        text(646, 141, "Micrometastasis", 32, 700),
        text(646, 198, status, 40, 700, accent),
        finding_glyph(present),
    ]
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">\n'
        f'{defs()}\n' + "\n".join(body) + "\n</svg>\n"
    )


def main():
    files = {
        "micrometastasis_present_icon.svg": icon(True),
        "micrometastasis_absent_icon.svg": icon(False),
    }
    for name, svg in files.items():
        svg_path = OUT / name
        svg_path.write_text(svg)
        subprocess.run(
            ["rsvg-convert", str(svg_path), "-w", str(W), "-h", str(H), "-o", str(svg_path.with_suffix(".png"))],
            check=True,
        )
    subprocess.run(
        [
            "convert",
            str(OUT / "micrometastasis_present_icon.png"),
            str(OUT / "micrometastasis_absent_icon.png"),
            "-background",
            "white",
            "+append",
            str(OUT / "micrometastasis_icons_contact_sheet.png"),
        ],
        check=True,
    )


if __name__ == "__main__":
    main()
