import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")

BASE_URL = "https://api.github.com"
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}


def get_recent_commits(limit: int = 10):
    """Fetch recent commits from the repo."""
    url = f"{BASE_URL}/repos/{GITHUB_REPO}/commits"
    response = requests.get(url, headers=HEADERS, params={"per_page": limit})
    response.raise_for_status()

    commits = []
    for c in response.json():
        commits.append({
            "sha": c["sha"][:7],
            "message": c["commit"]["message"],
            "author": c["commit"]["author"]["name"],
            "date": c["commit"]["author"]["date"],
        })
    return commits


def get_pull_requests(state: str = "all", limit: int = 10):
    """Fetch pull requests (open, closed, or all)."""
    url = f"{BASE_URL}/repos/{GITHUB_REPO}/pulls"
    response = requests.get(url, headers=HEADERS, params={"state": state, "per_page": limit})
    response.raise_for_status()

    prs = []
    for pr in response.json():
        prs.append({
            "number": pr["number"],
            "title": pr["title"],
            "state": pr["state"],
            "created_at": pr["created_at"],
            "merged_at": pr["merged_at"],
        })
    return prs


def get_repo_activity_summary():
    """Combine commits + PRs into one summary — this is what the Engineering Agent will consume."""
    commits = get_recent_commits()
    prs = get_pull_requests()

    return {
        "total_recent_commits": len(commits),
        "total_recent_prs": len(prs),
        "open_prs": len([p for p in prs if p["state"] == "open"]),
        "merged_prs": len([p for p in prs if p["merged_at"] is not None]),
        "commits": commits,
        "pull_requests": prs,
    }