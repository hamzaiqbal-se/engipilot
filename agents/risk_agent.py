from sqlalchemy.orm import Session
from api import models
from datetime import datetime
import logging

logger = logging.getLogger("engipilot")


def extract_risk_features(project_id: int, db: Session) -> dict:
    """
    Extracts ML-ready features for a project, to be used by the
    Risk Agent's prediction model (trained in the next step).
    """

    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        return {"error": f"Project with id {project_id} not found"}

    tasks = (
        db.query(models.Task)
        .join(models.Sprint)
        .filter(models.Sprint.project_id == project_id)
        .all()
    )

    total_tasks = len(tasks)
    done_tasks = len([t for t in tasks if t.status == "done"])
    blocked_tasks = len([t for t in tasks if t.status == "blocked"])
    in_progress_tasks = len([t for t in tasks if t.status == "in_progress"])

    completion_rate = round(done_tasks / total_tasks, 3) if total_tasks > 0 else 0.0
    blocked_ratio = round(blocked_tasks / total_tasks, 3) if total_tasks > 0 else 0.0

    # --- Velocity: tasks completed per day since project start ---
    days_elapsed = max((datetime.now() - project.start_date.replace(tzinfo=None)).days, 1)
    velocity = round(done_tasks / days_elapsed, 3)

    # --- Deadline proximity (negative = overdue) ---
    days_to_deadline = None
    if project.deadline:
        days_to_deadline = (project.deadline.replace(tzinfo=None) - datetime.now()).days

    # --- Team workload signal ---
    assignee_ids = list({t.assignee_id for t in tasks if t.assignee_id is not None})
    team_members = (
        db.query(models.TeamMember)
        .filter(models.TeamMember.id.in_(assignee_ids))
        .all()
        if assignee_ids else []
    )

    if team_members:
        workload_ratios = [
            (m.current_workload / m.capacity_hours) if m.capacity_hours > 0 else 0
            for m in team_members
        ]
        avg_workload_ratio = round(sum(workload_ratios) / len(workload_ratios), 3)
    else:
        avg_workload_ratio = 0.0

    features = {
        "project_id": project_id,
        "total_tasks": total_tasks,
        "done_tasks": done_tasks,
        "blocked_tasks": blocked_tasks,
        "in_progress_tasks": in_progress_tasks,
        "completion_rate": completion_rate,
        "blocked_ratio": blocked_ratio,
        "velocity": velocity,
        "days_elapsed": days_elapsed,
        "days_to_deadline": days_to_deadline,
        "avg_workload_ratio": avg_workload_ratio,
    }

    logger.info(f"Extracted risk features for project_id={project_id}: {features}")
    return features