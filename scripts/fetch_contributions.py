import json
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USERNAME = "Imtejakarthik"
OUT = Path("data/contributions.json")


def parse_count(label):
    first = (label or "").split(" contribution", 1)[0].replace(",", "")
    return 0 if first == "No" else int(first or 0)


def main():
    html = requests.get(
        f"https://github.com/users/{USERNAME}/contributions",
        timeout=30,
        headers={"User-Agent": "profile-readme-generator"},
    ).text
    soup = BeautifulSoup(html, "html.parser")
    tooltips = {tip.get("for"): tip.get_text(" ", strip=True) for tip in soup.select("tool-tip[for]")}
    days = []
    for cell in soup.select("td.ContributionCalendar-day[data-date]"):
        label = tooltips.get(cell.get("id"), "")
        days.append(
            {
                "date": cell["data-date"],
                "count": parse_count(label),
                "level": int(cell.get("data-level") or 0),
            }
        )

    today = date.today()
    counts = {d["date"]: d["count"] for d in days}
    current = 0
    cursor = today
    while counts.get(cursor.isoformat(), 0) > 0:
        current += 1
        cursor -= timedelta(days=1)

    longest = run = 0
    for day in sorted(days, key=lambda item: item["date"]):
        run = run + 1 if day["count"] else 0
        longest = max(longest, run)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(
            {
                "username": USERNAME,
                "generated_at": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
                "total": sum(d["count"] for d in days),
                "current_streak": current,
                "longest_streak": longest,
                "best_day": max(days, key=lambda d: d["count"], default={"date": "", "count": 0}),
                "days": days[-371:],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
