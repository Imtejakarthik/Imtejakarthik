import json
from html import escape
from pathlib import Path

OUT = Path("projects-terminal.svg")
DATA = Path("data/repos.json")

FIELDS = [
    ("AI / LLM", "#c084fc", ["PhilosopherMind_UltimateLLM", "Keyboard-Auto-Suggestion-NLP-Project", "anti-ai-agent-genrator", "llm-automations"]),
    ("Healthcare ML", "#39d353", ["Heart-Disease-Prediction-", "advance-brain-tumor-segmentation", "Live-Human-Emotion-Classification", "smart_sock_iot"]),
    ("Data Science", "#58a6ff", ["market-regime", "CO2-EMSSION", "scholarship-eligibility-analyzer", "ekkocare"]),
    ("Web Apps", "#ffbd2e", ["campusnext", "jv_mahal_website", "lora", "maptip"]),
    ("Automation", "#f778ba", ["dvader", "flowise-aii", "https-sever", "PYTHON"]),
]

LABELS = {
    "PhilosopherMind_UltimateLLM": "PhilosopherMind Ultimate",
    "Keyboard-Auto-Suggestion-NLP-Project": "Keyboard NLP Suggestion",
    "anti-ai-agent-genrator": "AI Agent Automation",
    "Heart-Disease-Prediction-": "Heart Disease Prediction",
    "advance-brain-tumor-segmentation": "Brain Tumor Segmentation",
    "Live-Human-Emotion-Classification": "Emotion Classification",
    "CO2-EMSSION": "CO2 Emission Analysis",
    "scholarship-eligibility-analyzer": "Scholarship Analyzer",
    "jv_mahal_website": "JV Mahal Website",
    "https-sever": "HTTPS Server",
}


def main():
    repos = {repo["name"]: repo for repo in json.loads(DATA.read_text(encoding="utf-8"))["repos"]}
    cards = []
    for i, (title, color, names) in enumerate(FIELDS):
        x = 26 + (i % 2) * 404
        y = 76 + (i // 2) * 150
        lines = []
        for j, name in enumerate(names):
            repo = repos.get(name, {"language": "Other", "description": ""})
            lines.append(
                f'<text class="repo" x="{x + 20}" y="{y + 58 + j * 23}">{escape(LABELS.get(name, name))}</text>'
                f'<text class="lang" x="{x + 270}" y="{y + 58 + j * 23}">{escape(repo["language"][:16])}</text>'
            )
        cards.append(
            f'<g class="card" style="animation-delay:{0.08 + i * .1:.2f}s"><rect x="{x}" y="{y}" width="382" height="126" rx="10" fill="#161b22" stroke="#30365f"/>'
            f'<text class="field" x="{x + 20}" y="{y + 28}" fill="{color}">{escape(title)}</text>{"".join(lines)}</g>'
        )
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="860" height="470" viewBox="0 0 860 470" role="img" aria-label="Real projects grouped by field">
  <style>
    .frame {{ fill:#0d1117; stroke:#30365f; stroke-width:1; }}
    .prompt {{ fill:#7dd3fc; font:700 15px 'Cascadia Code', Consolas, monospace; }}
    .field {{ font:800 15px 'Segoe UI', Ubuntu, sans-serif; }}
    .repo {{ fill:#f5f7ff; font:700 12px 'Cascadia Code', Consolas, monospace; }}
    .lang {{ fill:#9aa7c7; font:600 11px 'Segoe UI', Ubuntu, sans-serif; }}
    .card {{ opacity:0; transform:translateY(12px); animation:rise .45s cubic-bezier(.16,1,.3,1) forwards; }}
    @keyframes rise {{ to {{ opacity:1; transform:translateY(0); }} }}
    @media (prefers-reduced-motion: reduce) {{ .card {{ animation:none; opacity:1; transform:none; }} }}
  </style>
  <rect class="frame" x="1" y="1" width="858" height="468" rx="14"/>
  <text class="prompt" x="26" y="38">teja@github ~ $ ls projects --group=field</text>
  {''.join(cards)}
</svg>
"""
    OUT.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
