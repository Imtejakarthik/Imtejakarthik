from html import escape
from pathlib import Path

OUT = Path("info-card.svg")
ROWS = [
    ("Name", "Imteja Karthik G"),
    ("Role", "CSE student specializing in AI / ML"),
    ("Work", "ML projects, web apps, automation"),
    ("Stack", "Python, TypeScript, React, Next.js"),
    ("Focus", "Healthcare ML, data science, agents"),
    ("Status", "Building practical, useful systems"),
]


def main():
    rows = []
    for index, (key, value) in enumerate(ROWS):
        y = 80 + index * 31
        rows.append(
            f'<g class="row" style="animation-delay:{0.14 + index * 0.12:.2f}s">'
            f'<text class="key" x="34" y="{y}">{escape(key)}</text>'
            f'<text class="value" x="130" y="{y}">{escape(value)}</text></g>'
        )
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="490" height="500" viewBox="0 0 490 500" role="img" aria-label="Neofetch style info card for Imteja Karthik">
  <style>
    .frame {{ fill:#0d1117; stroke:#30365f; stroke-width:1; }}
    .dot1 {{ fill:#ff5f57; }} .dot2 {{ fill:#ffbd2e; }} .dot3 {{ fill:#28c840; }}
    .prompt {{ fill:#7dd3fc; font:700 17px 'Cascadia Code', Consolas, monospace; }}
    .key {{ fill:#c084fc; font:800 15px 'Cascadia Code', Consolas, monospace; }}
    .value {{ fill:#f5f7ff; font:600 15px 'Segoe UI', Ubuntu, sans-serif; }}
    .row {{ opacity:0; transform:translateX(-10px); animation:line .5s cubic-bezier(.16,1,.3,1) forwards; }}
    .cursor {{ animation:blink 1s steps(2,start) infinite; }}
    @keyframes line {{ to {{ opacity:1; transform:translateX(0); }} }}
    @keyframes blink {{ 50% {{ opacity:0; }} }}
    @media (prefers-reduced-motion: reduce) {{ .row,.cursor {{ animation:none; opacity:1; transform:none; }} }}
  </style>
  <rect class="frame" x="1" y="1" width="488" height="498" rx="14"/>
  <circle class="dot1" cx="26" cy="28" r="6"/><circle class="dot2" cx="47" cy="28" r="6"/><circle class="dot3" cx="68" cy="28" r="6"/>
  <text class="prompt" x="34" y="55">teja@github ~ $ neofetch<tspan class="cursor">_</tspan></text>
  {''.join(rows)}
  <text class="value" x="34" y="312">Highlights</text>
  <text class="key" x="34" y="346">▸</text><text class="value" x="58" y="346">Healthcare prediction systems</text>
  <text class="key" x="34" y="377">▸</text><text class="value" x="58" y="377">NLP and LLM experiments</text>
  <text class="key" x="34" y="408">▸</text><text class="value" x="58" y="408">Full-stack product interfaces</text>
  <text class="key" x="34" y="439">▸</text><text class="value" x="58" y="439">Automation and developer tools</text>
</svg>
"""
    OUT.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
