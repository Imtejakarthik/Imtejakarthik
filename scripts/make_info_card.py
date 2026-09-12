from pathlib import Path
from html import escape

OUT = Path("info-card.svg")

ROWS = [
    ("Role", "Full-stack developer & AI enthusiast"),
    ("Focus", "System design, automation, web apps"),
    ("Stack", "Next.js, React, TypeScript, Node, Python"),
    ("Cloud", "AWS, GCP, Azure, Docker, Kubernetes"),
    ("Mode", "Building useful things with purpose"),
]


def main():
    row_svg = []
    for index, (key, value) in enumerate(ROWS):
        y = 72 + index * 28
        delay = 0.15 + index * 0.16
        row_svg.append(
            f'<g class="row" style="animation-delay:{delay:.2f}s">'
            f'<text class="key" x="34" y="{y}">{escape(key)}</text>'
            f'<text class="value" x="122" y="{y}">{escape(value)}</text>'
            "</g>"
        )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="860" height="230" viewBox="0 0 860 230" role="img" aria-label="Animated profile info card for Imteja Karthik">
  <style>
    .frame {{ fill: #1a1b27; stroke: #30365f; stroke-width: 1; }}
    .dot-red {{ fill: #ff5f57; }} .dot-yellow {{ fill: #ffbd2e; }} .dot-green {{ fill: #28c840; }}
    .prompt {{ fill: #7dd3fc; font: 700 18px 'Cascadia Code', Consolas, monospace; }}
    .key {{ fill: #c084fc; font: 700 15px 'Cascadia Code', Consolas, monospace; }}
    .value {{ fill: #f5f7ff; font: 500 15px 'Segoe UI', Ubuntu, sans-serif; }}
    .row {{ opacity: 0; transform: translateX(-12px); animation: typein .5s cubic-bezier(.2,.8,.2,1) forwards; }}
    .cursor {{ animation: blink 1s steps(2, start) infinite; }}
    @keyframes typein {{ to {{ opacity: 1; transform: translateX(0); }} }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{ .row {{ animation: none; opacity: 1; transform: none; }} .cursor {{ animation: none; }} }}
  </style>
  <rect class="frame" x="1" y="1" width="858" height="228" rx="10"/>
  <circle class="dot-red" cx="28" cy="26" r="6"/>
  <circle class="dot-yellow" cx="48" cy="26" r="6"/>
  <circle class="dot-green" cx="68" cy="26" r="6"/>
  <text class="prompt" x="34" y="50">imteja@profile ~ $ whoami<tspan class="cursor">_</tspan></text>
  {''.join(row_svg)}
</svg>
"""
    OUT.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
