from html import escape
from pathlib import Path

OUT = Path("info-card.svg")

ROWS = [
    ("Name", "Imteja Karthik G"),
    ("Role", "Full-stack developer + AI builder"),
    ("Focus", "Automation, products, systems"),
    ("Stack", "Next.js, React, TS, Node, Python"),
    ("Cloud", "AWS, GCP, Azure, Docker, K8s"),
    ("Ship", "Useful tools with clean UX"),
]

ASCII = [
    "IIII  M   M  TTTTT  EEEEE  JJJJJ   AAAAA",
    " II   MM MM    T    E        J     A   A",
    " II   M M M    T    EEEE     J     AAAAA",
    " II   M   M    T    E        J     A   A",
    "IIII  M   M    T    EEEEE  JJJ     A   A",
]


def main():
    row_svg = []
    for index, (key, value) in enumerate(ROWS):
        y = 82 + index * 28
        delay = 0.15 + index * 0.16
        row_svg.append(
            f'<g class="row" style="animation-delay:{delay:.2f}s">'
            f'<text class="key" x="424" y="{y}">{escape(key)}</text>'
            f'<text class="value" x="510" y="{y}">{escape(value)}</text>'
            "</g>"
        )

    ascii_svg = []
    for index, line in enumerate(ASCII):
        delay = 0.2 + index * 0.16
        ascii_svg.append(
            f'<text class="ascii row" x="38" y="{92 + index * 25}" style="animation-delay:{delay:.2f}s">{escape(line)}</text>'
        )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="820" height="270" viewBox="0 0 820 270" role="img" aria-label="Animated terminal profile card for Imteja Karthik">
  <style>
    .frame {{ fill: #0d1117; stroke: #30365f; stroke-width: 1; }}
    .glow {{ fill: none; stroke: #58a6ff; stroke-opacity: .28; stroke-width: 2; }}
    .split {{ stroke: #30365f; stroke-width: 1; }}
    .dot-red {{ fill: #ff5f57; }} .dot-yellow {{ fill: #ffbd2e; }} .dot-green {{ fill: #28c840; }}
    .prompt {{ fill: #7dd3fc; font: 700 17px 'Cascadia Code', Consolas, monospace; }}
    .ascii {{ fill: #c084fc; font: 800 17px 'Cascadia Code', Consolas, monospace; letter-spacing: 0; }}
    .key {{ fill: #7dd3fc; font: 700 14px 'Cascadia Code', Consolas, monospace; }}
    .value {{ fill: #f5f7ff; font: 500 14px 'Segoe UI', Ubuntu, sans-serif; }}
    .caption {{ fill: #9aa7c7; font: 600 12px 'Segoe UI', Ubuntu, sans-serif; }}
    .pill {{ fill: #161b22; stroke: #30365f; stroke-width: 1; }}
    .pilltext {{ fill: #f5f7ff; font: 700 12px 'Segoe UI', Ubuntu, sans-serif; }}
    .row {{ opacity: 0; transform: translateY(10px); animation: typein .5s cubic-bezier(.2,.8,.2,1) forwards; }}
    .cursor {{ animation: blink 1s steps(2, start) infinite; }}
    @keyframes typein {{ to {{ opacity: 1; transform: translateY(0); }} }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{ .row {{ animation: none; opacity: 1; transform: none; }} .cursor {{ animation: none; }} }}
  </style>
  <rect class="frame" x="1" y="1" width="818" height="268" rx="14"/>
  <rect class="glow" x="11" y="11" width="798" height="248" rx="10"/>
  <circle class="dot-red" cx="28" cy="26" r="6"/>
  <circle class="dot-yellow" cx="48" cy="26" r="6"/>
  <circle class="dot-green" cx="68" cy="26" r="6"/>
  <text class="prompt" x="34" y="52">imteja@github ~ $ ./profile.sh<tspan class="cursor">_</tspan></text>
  <line class="split" x1="394" y1="72" x2="394" y2="214"/>
  {''.join(ascii_svg)}
  {''.join(row_svg)}
  <rect class="pill" x="38" y="225" width="108" height="26" rx="13"/>
  <rect class="pill" x="156" y="225" width="122" height="26" rx="13"/>
  <rect class="pill" x="288" y="225" width="92" height="26" rx="13"/>
  <text class="pilltext" x="61" y="242">AI Tools</text>
  <text class="pilltext" x="178" y="242">Web Apps</text>
  <text class="pilltext" x="312" y="242">Cloud</text>
  <text class="caption" x="424" y="236">Open to building fast, useful software that feels good to use.</text>
</svg>
"""
    OUT.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
