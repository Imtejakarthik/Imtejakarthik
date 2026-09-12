import json
from collections import Counter
from html import escape
from pathlib import Path

DATA = Path("data/repos.json")
OUT = Path("projects-terminal.svg")

PROJECTS = [
    ("AI / LLM", "#c084fc", [
        ("PhilosopherMind_UltimateLLM", "Custom emotionally intelligent LLM concept"),
        ("Keyboard-Auto-Suggestion-NLP-Project", "NLP next-word suggestion system"),
        ("anti-ai-agent-genrator", "Modular AI agent automation platform"),
        ("llm-automations", "TypeScript LLM workflow experiments"),
    ]),
    ("Healthcare ML", "#39d353", [
        ("Heart-Disease-Prediction-", "Clinical heart disease prediction"),
        ("advance-brain-tumor-segmentation", "Deep learning medical image segmentation"),
        ("Live-Human-Emotion-Classification", "Live emotion classification experiment"),
        ("smart_sock_iot", "IoT diabetic foot ulcer monitoring concept"),
    ]),
    ("Data / Analytics", "#58a6ff", [
        ("market-regime", "RL trading agent with market regime detection"),
        ("CO2-EMSSION", "Vehicle carbon emission predictive analysis"),
        ("scholarship-eligibility-analyzer", "Local scholarship recommendation app"),
        ("ekkocare", "Real-time analysis notebook project"),
    ]),
    ("Web / Product UI", "#ffbd2e", [
        ("campusnext", "Next.js event management app"),
        ("jv_mahal_website", "Next.js website project"),
        ("lora", "TypeScript web app"),
        ("maptip", "EJS web project"),
    ]),
    ("Automation / Tools", "#f778ba", [
        ("dvader", "JavaScript developer tooling project"),
        ("flowise-aii", "Docker Flowise AI setup"),
        ("https-sever", "Shell HTTPS server experiment"),
        ("PYTHON", "Python practice and utility scripts"),
    ]),
]


def main():
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    repos = {repo["name"]: repo for repo in payload["repos"]}
    langs = Counter(repo["language"] for repo in payload["repos"])
    total = len(payload["repos"])

    cards = []
    for field_index, (field, color, names) in enumerate(PROJECTS):
        x = 26 + (field_index % 2) * 404
        y = 80 + (field_index // 2) * 162
        rows = []
        for row_index, (name, fallback) in enumerate(names):
            repo = repos.get(name, {})
            desc = repo.get("description") or fallback
            lang = repo.get("language", "Other")
            rows.append(
                f'<text class="repo" x="{x + 22}" y="{y + 58 + row_index * 25}">{escape(name)}</text>'
                f'<text class="meta" x="{x + 254}" y="{y + 58 + row_index * 25}">{escape(lang)}</text>'
                f'<title>{escape(desc)}</title>'
            )
        delay = 0.08 + field_index * 0.12
        cards.append(
            f'<g class="card" style="animation-delay:{delay:.2f}s">'
            f'<rect x="{x}" y="{y}" width="382" height="136" rx="10" fill="#161b22" stroke="#30365f"/>'
            f'<rect x="{x}" y="{y}" width="382" height="34" rx="10" fill="{color}" opacity=".16"/>'
            f'<text class="field" x="{x + 18}" y="{y + 23}" fill="{color}">{escape(field)}</text>'
            f'{"".join(rows)}</g>'
        )

    top_langs = ", ".join(f"{name} {count}" for name, count in langs.most_common(4))
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="860" height="590" viewBox="0 0 860 590" role="img" aria-label="Real projects grouped by field for Imteja Karthik">
  <style>
    .frame {{ fill:#0d1117; stroke:#30365f; stroke-width:1; }}
    .title {{ fill:#f5f7ff; font:800 22px 'Segoe UI', Ubuntu, sans-serif; }}
    .prompt {{ fill:#7dd3fc; font:700 15px 'Cascadia Code', Consolas, monospace; }}
    .muted {{ fill:#9aa7c7; font:500 13px 'Segoe UI', Ubuntu, sans-serif; }}
    .field {{ font:800 15px 'Segoe UI', Ubuntu, sans-serif; }}
    .repo {{ fill:#f5f7ff; font:700 13px 'Cascadia Code', Consolas, monospace; }}
    .meta {{ fill:#9aa7c7; font:600 12px 'Segoe UI', Ubuntu, sans-serif; }}
    .card {{ opacity:0; transform:translateY(14px); animation:rise .55s cubic-bezier(.16,1,.3,1) forwards; }}
    @keyframes rise {{ to {{ opacity:1; transform:translateY(0); }} }}
    @media (prefers-reduced-motion: reduce) {{ .card {{ animation:none; opacity:1; transform:none; }} }}
  </style>
  <rect class="frame" x="1" y="1" width="858" height="588" rx="14"/>
  <text class="prompt" x="26" y="34">imteja@github ~ $ ls projects --group=field</text>
  <text class="title" x="26" y="62">Real Projects</text>
  <text class="muted" x="174" y="62">{total} public source repos | {escape(top_langs)}</text>
  {''.join(cards)}
</svg>
"""
    OUT.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
