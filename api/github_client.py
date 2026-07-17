import os
import requests
from dotenv import load_dotenv
import logging

logger = logging.getLogger("engipilot")
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
DEFAULT_GITHUB_REPO = os.getenv("GITHUB_REPO")  # fallback agar project ka apna repo na ho

BASE_URL = "https://api.github.com"
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}


def get_recent_commits(repo: str = None, limit: int = 10):
    """Fetch recent commits from the given repo (or default repo if none specified)."""
    repo = repo or DEFAULT_GITHUB_REPO
    url = f"{BASE_URL}/repos/{repo}/commits"
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


def get_pull_requests(repo: str = None, state: str = "all", limit: int = 10):
    """Fetch pull requests from the given repo (or default repo if none specified)."""
    repo = repo or DEFAULT_GITHUB_REPO
    url = f"{BASE_URL}/repos/{repo}/pulls"
    response = requests.get(url, headers=HEADERS, params={"state": state, "per_page": limit})
    response.raise_for_status()

    prs = []
    for pr in response.json():
        prs.append({
            "number": pr["number"],
            "title": pr["title"],
            "state": pr["state"],
            "created_at": pr["created_at"],
            "updated_at": pr["updated_at"],
            "merged_at": pr["merged_at"],
            "draft": pr.get("draft", False),
        })
    return prs


def get_repo_activity_summary(repo: str = None):
    """Combine commits + PRs into one summary for the given repo."""
    commits = get_recent_commits(repo=repo)
    prs = get_pull_requests(repo=repo)
    logger.info(f"Fetched GitHub activity for repo={repo or DEFAULT_GITHUB_REPO}: {len(commits)} commits, {len(prs)} PRs")

    return {
        "total_recent_commits": len(commits),
        "total_recent_prs": len(prs),
        "open_prs": len([p for p in prs if p["state"] == "open"]),
        "merged_prs": len([p for p in prs if p["merged_at"] is not None]),
        "commits": commits,
        "pull_requests": prs,
    }