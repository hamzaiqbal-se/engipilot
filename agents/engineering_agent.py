from sqlalchemy.orm import Session
from api import models
from api.github_client import get_repo_activity_summary
from datetime import datetime, timedelta


INACTIVITY_THRESHOLD_DAYS = 7


def run_engineering_agent(project_id: int, db: Session) -> dict:
    """
    Engineering Agent:
    - Calculates progress % from task completion
    - Detects blocked tasks
    - Flags inactive projects based on GitHub activity
    Returns a dict matching the 'engineering_data' schema field.
    """

    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        return {"error": f"Project with id {project_id} not found"}

    # --- 1. Progress % calculation ---
    all_tasks = (
        db.query(models.Task)
        .join(models.Sprint)
        .filter(models.Sprint.project_id == project_id)
        .all()
    )

    total_tasks = len(all_tasks)
    done_tasks = len([t for t in all_tasks if t.status == "done"])
    progress_percentage = round((done_tasks / total_tasks) * 100, 2) if total_tasks > 0 else 0.0

    # --- 2. Blocked task detection ---
    blocked_tasks = [
        {"id": t.id, "title": t.title, "priority": t.priority}
        for t in all_tasks if t.status == "blocked"
    ]

    # --- 3. Inactive project detection (via GitHub activity) ---
    is_inactive = False
    last_commit_date = None
    try:
        github_activity = get_repo_activity_summary()
        commits = github_activity.get("commits", [])
        if commits:
            last_commit_date = commits[0]["date"]  # most recent commit
            last_commit_dt = datetime.fromisoformat(last_commit_date.replace("Z", "+00:00"))
            days_since_last_commit = (datetime.now(last_commit_dt.tzinfo) - last_commit_dt).days
            is_inactive = days_since_last_commit > INACTIVITY_THRESHOLD_DAYS
        else:
            is_inactive = True  # no commits at all
    except Exception as e:
        github_activity = {"error": str(e)}

    # --- Final output matching engineering_data schema field ---
    return {
        "project_id": project_id,
        "project_name": project.name,
        "progress_percentage": progress_percentage,
        "total_tasks": total_tasks,
        "done_tasks": done_tasks,
        "blocked_tasks": blocked_tasks,
        "blocked_task_count": len(blocked_tasks),
        "is_inactive": is_inactive,
        "last_commit_date": last_commit_date,
        "github_activity_summary": {
            "total_recent_commits": github_activity.get("total_recent_commits", 0),
            "open_prs": github_activity.get("open_prs", 0),
            "merged_prs": github_activity.get("merged_prs", 0),
        } if isinstance(github_activity, dict) and "error" not in github_activity else None,
    }