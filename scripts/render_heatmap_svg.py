import json
from datetime import date, datetime, timedelta
from html import escape
from pathlib import Path

DATA = Path("data/contributions.json")
OUT = Path("contrib-heatmap.svg")
PALETTE = ["#1a1b27", "#173d3f", "#255e6f", "#4f7fcf", "#8a63d2", "#c084fc"]


def main():
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    days = {item["date"]: item for item in payload["days"]}
    today = date.today()
    start = today - timedelta(days=370)
    start -= timedelta(days=(start.weekday() + 1) % 7)

    cells = []
    for i in range(371):
        current = start + timedelta(days=i)
        week = i // 7
        dow = (current.weekday() + 1) % 7
        item = days.get(current.isoformat(), {"count": 0, "level": 0})
        level = max(0, min(5, int(item.get("level", 0))))
        x = 28 + week * 15
        y = 54 + dow * 15
        delay = (week + dow) * 0.018
        label = f"{item['count']} contributions on {current.strftime('%b %d, %Y')}"
        cells.append(
            f'<rect class="cell" x="{x}" y="{y}" width="11" height="11" rx="3" '
            f'fill="{PALETTE[level]}" style="animation-delay:{delay:.3f}s">'
            f"<title>{escape(label)}</title></rect>"
        )

    footer = (
        f"{payload['total']:,} contributions in the last year | "
        f"Current streak {payload['current_streak']} | "
        f"Longest streak {payload['longest_streak']}"
    )
    best = payload.get("best_day", {})
    best_text = ""
    if best.get("date"):
        best_text = f"Best day: {best['count']} on {datetime.strptime(best['date'], '%Y-%m-%d').strftime('%b %d')}"

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="860" height="190" viewBox="0 0 860 190" role="img" aria-label="Animated GitHub contribution heatmap for Imteja Karthik">
  <style>
    .frame {{ fill: #1a1b27; stroke: #30365f; stroke-width: 1; }}
    .title {{ fill: #f5f7ff; font: 700 18px 'Segoe UI', Ubuntu, sans-serif; }}
    .muted {{ fill: #9aa7c7; font: 500 12px 'Segoe UI', Ubuntu, sans-serif; }}
    .cell {{ opacity: 0; transform: translateY(12px) scale(.82); transform-box: fill-box; transform-origin: center; animation: reveal .55s cubic-bezier(.2,.8,.2,1) forwards; }}
    .legend {{ font: 500 11px 'Segoe UI', Ubuntu, sans-serif; fill: #9aa7c7; }}
    @keyframes reveal {{ to {{ opacity: 1; transform: translateY(0) scale(1); }} }}
    @media (prefers-reduced-motion: reduce) {{ .cell {{ animation: none; opacity: 1; transform: none; }} }}
  </style>
  <rect class="frame" x="1" y="1" width="858" height="188" rx="10"/>
  <text class="title" x="28" y="32">Imtejakarthik@github ~ $ ./contributions.sh</text>
  <text class="muted" x="28" y="170">{escape(footer)}</text>
  <text class="muted" x="610" y="170">{escape(best_text)}</text>
  {''.join(cells)}
  <text class="legend" x="728" y="32">Less</text>
  <rect x="760" y="23" width="10" height="10" rx="2" fill="{PALETTE[0]}"/>
  <rect x="776" y="23" width="10" height="10" rx="2" fill="{PALETTE[1]}"/>
  <rect x="792" y="23" width="10" height="10" rx="2" fill="{PALETTE[2]}"/>
  <rect x="808" y="23" width="10" height="10" rx="2" fill="{PALETTE[3]}"/>
  <rect x="824" y="23" width="10" height="10" rx="2" fill="{PALETTE[5]}"/>
  <text class="legend" x="840" y="32">More</text>
</svg>
"""
    OUT.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
