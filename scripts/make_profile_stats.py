import json
from html import escape
from pathlib import Path

OUT = Path("profile-stats.svg")

FIELDS = [
    ("AI / LLM", "PhilosopherMind Ultimate, Keyboard Auto Suggestion, agent automation"),
    ("Healthcare ML", "Heart disease prediction, brain tumor segmentation, emotion classification"),
    ("Data Science", "Market regime RL, carbon emission prediction, scholarship analyzer"),
    ("Web Apps", "CampusNext, JV Mahal website, portfolio and TypeScript projects"),
    ("Automation", "dvader, llm-automations, flowise-aii, HTTPS server"),
    ("IoT", "Smart Sock diabetic foot ulcer detection system"),
]

LANGS = [
    ("TypeScript", 13, "#58a6ff"),
    ("Jupyter Notebook", 9, "#c084fc"),
    ("Python", 6, "#39d353"),
    ("JavaScript", 1, "#f778ba"),
    ("EJS / Shell / Java", 3, "#ffbd2e"),
]


def main():
    total = sum(count for _, count, _ in LANGS)
    bars = []
    x = 34
    for name, count, color in LANGS:
        width = round(690 * count / total)
        bars.append(f'<rect x="{x}" y="72" width="{width}" height="13" rx="6" fill="{color}"><title>{escape(name)}: {count} repos</title></rect>')
        x += width + 4

    lang_rows = []
    for index, (name, count, color) in enumerate(LANGS):
        y = 118 + index * 25
        lang_rows.append(
            f'<circle cx="48" cy="{y - 4}" r="5" fill="{color}"/>'
            f'<text class="value" x="64" y="{y}">{escape(name)}</text>'
            f'<text class="muted" x="252" y="{y}">{count} repos</text>'
        )

    field_rows = []
    for index, (name, detail) in enumerate(FIELDS):
        y = 118 + index * 25
        field_rows.append(
            f'<text class="key" x="380" y="{y}">{escape(name)}</text>'
            f'<text class="value" x="520" y="{y}">{escape(detail)}</text>'
        )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="860" height="292" viewBox="0 0 860 292" role="img" aria-label="GitHub profile summary for Imteja Karthik">
  <style>
    .frame {{ fill: #0d1117; stroke: #30365f; stroke-width: 1; }}
    .title {{ fill: #f5f7ff; font: 700 18px 'Segoe UI', Ubuntu, sans-serif; }}
    .label {{ fill: #7dd3fc; font: 700 13px 'Cascadia Code', Consolas, monospace; }}
    .key {{ fill: #c084fc; font: 700 13px 'Segoe UI', Ubuntu, sans-serif; }}
    .value {{ fill: #f5f7ff; font: 500 13px 'Segoe UI', Ubuntu, sans-serif; }}
    .muted {{ fill: #9aa7c7; font: 500 12px 'Segoe UI', Ubuntu, sans-serif; }}
  </style>
  <rect class="frame" x="1" y="1" width="858" height="290" rx="14"/>
  <text class="title" x="34" y="38">Real GitHub Work Summary</text>
  <text class="muted" x="34" y="58">36 public source repositories grouped from the Imtejakarthik account</text>
  {''.join(bars)}
  <text class="label" x="34" y="102">languages</text>
  <text class="label" x="380" y="102">fields</text>
  {''.join(lang_rows)}
  {''.join(field_rows)}
</svg>
"""
    OUT.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
