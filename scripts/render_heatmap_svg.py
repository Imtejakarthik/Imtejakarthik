import json
from datetime import date, datetime, timedelta
from html import escape
from pathlib import Path

DATA = Path("data/contributions.json")
OUT = Path("contrib-heatmap.svg")
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]


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
        delay = (week + dow) * 0.017
        cells.append(
            f'<rect class="cell" x="{28 + week * 15}" y="{54 + dow * 15}" width="11" height="11" rx="3" fill="{PALETTE[level]}" style="animation-delay:{delay:.3f}s">'
            f"<title>{escape(str(item['count']))} contributions on {current.strftime('%b %d, %Y')}</title></rect>"
        )
    best = payload.get("best_day", {})
    best_text = ""
    if best.get("date"):
        best_text = f"Best day: {best['count']} on {datetime.strptime(best['date'], '%Y-%m-%d').strftime('%b %d')}"
    footer = f"{payload['total']:,} contributions | Current streak {payload['current_streak']} | Longest streak {payload['longest_streak']}"
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="860" height="190" viewBox="0 0 860 190" role="img" aria-label="Animated GitHub contribution heatmap">
  <style>
    .frame {{ fill:#0d1117; stroke:#30365f; stroke-width:1; }}
    .title {{ fill:#f5f7ff; font:700 18px 'Segoe UI', Ubuntu, sans-serif; }}
    .muted {{ fill:#9aa7c7; font:600 12px 'Segoe UI', Ubuntu, sans-serif; }}
    .cell {{ opacity:0; transform:translateY(10px) scale(.86); transform-box:fill-box; transform-origin:center; animation:reveal .5s cubic-bezier(.16,1,.3,1) forwards; }}
    @keyframes reveal {{ to {{ opacity:1; transform:translateY(0) scale(1); }} }}
    @media (prefers-reduced-motion: reduce) {{ .cell {{ animation:none; opacity:1; transform:none; }} }}
  </style>
  <rect class="frame" x="1" y="1" width="858" height="188" rx="14"/>
  <text class="title" x="28" y="32">imteja@github ~ $ ./contributions.sh</text>
  {''.join(cells)}
  <text class="muted" x="28" y="170">{escape(footer)}</text>
  <text class="muted" x="640" y="170">{escape(best_text)}</text>
</svg>
"""
    OUT.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
