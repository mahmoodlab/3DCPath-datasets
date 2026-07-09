from pathlib import Path
import subprocess


OUT = Path(__file__).resolve().parent
SIZE = 360


def svg_wrap(body):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{SIZE}" height="{SIZE}" viewBox="0 0 {SIZE} {SIZE}">
  <defs>
    <style>
      .line {{ fill: none; stroke: #3a3a3a; stroke-width: 9; stroke-linecap: round; stroke-linejoin: round; }}
      .thin {{ fill: none; stroke: #3a3a3a; stroke-width: 6; stroke-linecap: round; stroke-linejoin: round; }}
      .blue {{ fill: none; stroke: #176fb8; stroke-width: 9; stroke-linecap: round; stroke-linejoin: round; }}
      .green {{ fill: none; stroke: #4b8239; stroke-width: 10; stroke-linecap: round; stroke-linejoin: round; }}
      .red {{ fill: none; stroke: #c63a49; stroke-width: 10; stroke-linecap: round; stroke-linejoin: round; }}
      .grayfill {{ fill: #f4f5f6; stroke: #3a3a3a; stroke-width: 8; }}
      .bluefill {{ fill: #dcecf8; stroke: #176fb8; stroke-width: 8; }}
      .greenfill {{ fill: #dbead6; stroke: #4b8239; stroke-width: 8; }}
      .redfill {{ fill: #f5d5da; stroke: #c63a49; stroke-width: 8; }}
      .text {{ font-family: Arial, Helvetica, sans-serif; font-weight: 700; fill: #242424; }}
      .muted {{ fill: #6f7478; }}
    </style>
    <marker id="arrowBlue" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#176fb8"/>
    </marker>
    <marker id="arrowDark" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#3a3a3a"/>
    </marker>
  </defs>
{body}
</svg>
"""


def risk_clock():
    body = """
  <circle class="grayfill" cx="180" cy="180" r="118"/>
  <path class="thin" d="M180 78 V100 M180 260 V282 M78 180 H100 M260 180 H282"/>
  <path class="line" d="M180 180 V116"/>
  <path class="line" d="M180 180 L224 224"/>
  <path class="blue" d="M100 232 C127 210, 143 216, 163 184 C184 151, 210 154, 244 112"/>
  <circle cx="244" cy="112" r="13" fill="#c63a49"/>
  <text class="text" x="180" y="338" text-anchor="middle" font-size="50">5Y</text>
"""
    return svg_wrap(body)


def survival_curve():
    body = """
  <path class="line" d="M74 284 H290"/>
  <path class="line" d="M74 284 V70"/>
  <path class="blue" d="M94 98 H142 V137 H188 V180 H234 V228 H279"/>
  <path class="thin" d="M247 284 V228"/>
  <text class="text muted" x="247" y="324" text-anchor="middle" font-size="39">5Y</text>
  <circle cx="279" cy="228" r="13" fill="#c63a49"/>
  <path class="green" d="M110 255 C142 252, 162 247, 194 236"/>
"""
    return svg_wrap(body)


def calendar_outcome():
    body = """
  <rect class="grayfill" x="67" y="78" width="226" height="220" rx="28"/>
  <path class="line" d="M67 133 H293"/>
  <path class="line" d="M124 55 V101 M236 55 V101"/>
  <text class="text" x="180" y="218" text-anchor="middle" font-size="74">5Y</text>
  <path class="green" d="M127 254 L161 287 L233 209"/>
  <circle cx="262" cy="94" r="15" fill="#c63a49"/>
"""
    return svg_wrap(body)


def prognostic_gauge():
    body = """
  <path class="grayfill" d="M65 234 A115 115 0 0 1 295 234 L254 234 A74 74 0 0 0 106 234 Z"/>
  <path class="green" d="M86 232 A94 94 0 0 1 134 150"/>
  <path class="blue" d="M142 144 A94 94 0 0 1 217 144"/>
  <path class="red" d="M226 150 A94 94 0 0 1 274 232"/>
  <path class="line" d="M180 230 L235 162"/>
  <circle cx="180" cy="230" r="16" fill="#3a3a3a"/>
  <text class="text" x="180" y="312" text-anchor="middle" font-size="44">Risk</text>
  <text class="text muted" x="180" y="67" text-anchor="middle" font-size="42">5Y</text>
"""
    return svg_wrap(body)


def outcome_wheel():
    body = """
  <circle class="grayfill" cx="180" cy="180" r="94"/>
  <path class="line" d="M180 180 V116"/>
  <path class="line" d="M180 180 L224 218"/>
  <path class="thin" d="M263 111 C289 149, 292 198, 267 238" marker-end="url(#arrowDark)"/>
  <path class="thin" d="M97 249 C68 213, 63 165, 85 122" marker-end="url(#arrowDark)"/>
  <circle class="redfill" cx="112" cy="73" r="28"/>
  <path class="red" d="M101 73 H123"/>
  <path class="red" d="M112 62 V84"/>
  <circle class="greenfill" cx="284" cy="86" r="28"/>
  <path class="green" d="M270 87 L280 98 L299 76"/>
  <circle class="bluefill" cx="84" cy="296" r="28"/>
  <path class="blue" d="M69 296 H99"/>
  <path class="blue" d="M84 281 V311"/>
  <text class="text" x="180" y="338" text-anchor="middle" font-size="45">5Y</text>
"""
    return svg_wrap(body)


def km_prediction():
    body = """
  <text class="text" x="184" y="40" text-anchor="middle" font-size="29">Clinical outcome</text>
  <path class="line" d="M77 286 H313"/>
  <path class="line" d="M77 286 V68"/>
  <text class="text muted" x="195" y="344" text-anchor="middle" font-size="38">Time</text>
  <text class="text muted" x="27" y="184" text-anchor="middle" font-size="30" transform="rotate(-90 27 184)">Survival</text>
  <path class="blue" d="M95 91 H123 V111 H164 V132 H219 V151 H276 V168 H303"/>
  <path class="red" d="M95 91 H110 V110 H119 V128 H136 V146 H158 V165 H184 V184 H199 V202 H213 V220 H228 V238 H241 V256 H288 V273 H303"/>
  <path class="thin" d="M299 158 V178 M289 264 V282"/>
  <rect x="91" y="218" width="132" height="54" rx="10" fill="#ffffff" fill-opacity="0.82"/>
  <path class="red" d="M105 236 H126"/>
  <text class="text" x="137" y="244" text-anchor="start" font-size="22">High risk</text>
  <path class="blue" d="M105 259 H126"/>
  <text class="text" x="137" y="267" text-anchor="start" font-size="22">Low risk</text>
"""
    return svg_wrap(body)


def main():
    icons = {
        "five_year_prediction_risk_clock.svg": risk_clock(),
        "five_year_prediction_survival_curve.svg": survival_curve(),
        "five_year_prediction_calendar.svg": calendar_outcome(),
        "five_year_prediction_gauge.svg": prognostic_gauge(),
        "five_year_prediction_outcome_wheel.svg": outcome_wheel(),
        "five_year_prediction_km_icon.svg": km_prediction(),
    }
    pngs = []
    for name, svg in icons.items():
        svg_path = OUT / name
        png_path = svg_path.with_suffix(".png")
        svg_path.write_text(svg)
        subprocess.run(["rsvg-convert", str(svg_path), "-w", str(SIZE), "-h", str(SIZE), "-o", str(png_path)], check=True)
        pngs.append(str(png_path))
    subprocess.run(["convert", *pngs, "-background", "white", "+append", str(OUT / "five_year_prediction_icons_contact_sheet.png")], check=True)


if __name__ == "__main__":
    main()
