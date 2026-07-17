from api.github_client import get_pull_requests
from datetime import datetime
import logging

logger = logging.getLogger("engipilot")


def run_qa_agent(repo: str = None) -> dict:
    """
    QA Agent: fetches open pull requests for the given repo and scores review priority.
    """
    try:
        prs = get_pull_requests(repo=repo, state="open", limit=20)
    except Exception as e:
        logger.info(f"QA Agent: failed to fetch PRs — {e}")
        return {"error": str(e)}

    scored_prs = []
    for pr in prs:
        created_dt = datetime.fromisoformat(pr["created_at"].replace("Z", "+00:00"))
        age_days = (datetime.now(created_dt.tzinfo) - created_dt).days

        # --- Priority scoring: older PRs get higher urgency, drafts get lower priority ---
        if pr["draft"]:
            urgency_score = 0
            urgency_label = "Low (Draft)"
        elif age_days >= 7:
            urgency_score = 3
            urgency_label = "High"
        elif age_days >= 3:
            urgency_score = 2
            urgency_label = "Medium"
        else:
            urgency_score = 1
            urgency_label = "Low"

        scored_prs.append({
            "number": pr["number"],
            "title": pr["title"],
            "age_days": age_days,
            "urgency_score": urgency_score,
            "urgency_label": urgency_label,
            "is_draft": pr["draft"],
        })

    ranked_prs = sorted(scored_prs, key=lambda p: p["urgency_score"], reverse=True)

    result = {
        "total_open_prs": len(ranked_prs),
        "review_priority_queue": ranked_prs,
        "high_priority_count": len([p for p in ranked_prs if p["urgency_label"] == "High"]),
    }

    logger.info(f"QA Agent run: {len(ranked_prs)} open PRs scored, {result['high_priority_count']} high priority")
    return result