import json
from datetime import UTC, datetime
from pathlib import Path

import requests

USERNAME = "Imtejakarthik"
OUT = Path("data/repos.json")


def main():
    response = requests.get(
        f"https://api.github.com/users/{USERNAME}/repos?per_page=100&sort=updated",
        timeout=30,
        headers={"User-Agent": "profile-readme-generator"},
    )
    response.raise_for_status()
    repos = []
    for repo in response.json():
        if repo["fork"] or repo["name"] == USERNAME:
            continue
        repos.append(
            {
                "name": repo["name"],
                "description": repo["description"] or "",
                "language": repo["language"] or "Other",
                "url": repo["html_url"],
                "stars": repo["stargazers_count"],
                "updated_at": repo["pushed_at"] or repo["updated_at"],
            }
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps({"username": USERNAME, "generated_at": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"), "repos": repos}, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
