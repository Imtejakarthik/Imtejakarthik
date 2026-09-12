from html import escape
from pathlib import Path

from PIL import Image

SOURCE = Path("source-prepped.png")
OUT = Path("teja-ascii.svg")
RAMP = " .`:-=+*cs#%@"
COLS = 74
ROWS = 45


def main():
    image = Image.open(SOURCE).convert("L")
    image = image.resize((COLS, ROWS))
    lines = []
    for y in range(ROWS):
        chars = []
        for x in range(COLS):
            value = 255 - image.getpixel((x, y))
            chars.append(RAMP[min(len(RAMP) - 1, value * len(RAMP) // 256)])
        lines.append("".join(chars).rstrip())

    text_rows = []
    for index, line in enumerate(lines):
        y = 30 + index * 10
        duration = 0.34
        begin = index * 0.028
        text_rows.append(
            f'<g clip-path="url(#row-{index})">'
            f'<text class="ascii" x="18" y="{y}">{escape(line)}</text>'
            f'</g><clipPath id="row-{index}">'
            f'<rect x="18" y="{y - 9}" width="0" height="11">'
            f'<animate attributeName="width" from="0" to="345" dur="{duration}s" begin="{begin:.3f}s" fill="freeze"/>'
            f'</rect></clipPath>'
        )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="370" height="500" viewBox="0 0 370 500" role="img" aria-label="Animated ASCII portrait of Imteja Karthik">
  <style>
    .frame {{ fill:#0d1117; stroke:#30365f; stroke-width:1; }}
    .ascii {{ fill:#c9d1d9; font:700 9px 'Cascadia Code', Consolas, monospace; letter-spacing:0; }}
  </style>
  <rect class="frame" x="1" y="1" width="368" height="498" rx="14"/>
  {''.join(text_rows)}
</svg>
"""
    OUT.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
