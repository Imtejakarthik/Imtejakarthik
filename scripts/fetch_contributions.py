import json
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USERNAME = "Imtejakarthik"
OUT = Path("data/contributions.json")


def parse_count(label):
    if not label:
        return 0
    first = label.split(" contribution", 1)[0].replace(",", "")
    try:
        return int(first)
    except ValueError:
        return 0


def streaks(days):
    counts = {day["date"]: day["count"] for day in days}
    today = date.today()

    current = 0
    cursor = today
    while counts.get(cursor.isoformat(), 0) > 0:
        current += 1
        cursor -= timedelta(days=1)

    longest = 0
    run = 0
    for item in sorted(days, key=lambda d: d["date"]):
        if item["count"] > 0:
            run += 1
            longest = max(longest, run)
        else:
            run = 0
    return current, longest


def main():
    url = f"https://github.com/users/{USERNAME}/contributions"
    html = requests.get(url, timeout=30, headers={"User-Agent": "profile-readme-generator"}).text
    soup = BeautifulSoup(html, "html.parser")

    tooltips = {tip.get("for"): tip.get_text(" ", strip=True) for tip in soup.select("tool-tip[for]")}

    days = []
    for cell in soup.select("td.ContributionCalendar-day[data-date]"):
        day = cell.get("data-date")
        label = cell.get("aria-label") or tooltips.get(cell.get("id"), "")
        count = parse_count(label)
        level = int(cell.get("data-level") or min(4, count))
        days.append({"date": day, "count": count, "level": level})

    unique = {item["date"]: item for item in days}
    days = [unique[key] for key in sorted(unique)]
    total = sum(day["count"] for day in days)
    current, longest = streaks(days)
    best = max(days, key=lambda d: d["count"], default={"date": "", "count": 0})

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(
            {
                "username": USERNAME,
                "generated_at": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
                "total": total,
                "current_streak": current,
                "longest_streak": longest,
                "best_day": best,
                "days": days[-371:],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
