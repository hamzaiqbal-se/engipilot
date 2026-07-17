from sqlalchemy.orm import Session
from api import models
import logging
from datetime import datetime, timedelta


logger = logging.getLogger("engipilot")

PRIORITY_WEIGHTS = {"high": 5, "medium": 2, "low": 1}


def run_planning_agent(project_id: int, db: Session, risk_data: dict = None) -> dict:
    """
    Planning Agent:
    - Ranks pending tasks by priority and status
    - Suggests a sprint goal
    - Uses Risk Agent's delay_risk (if provided) to adjust feasibility recommendation
    - Suggests a timeline adjustment based on current velocity
    Returns a dict matching the 'planning_data' schema field.
    """

    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        return {"error": f"Project with id {project_id} not found"}

    pending_tasks = (
        db.query(models.Task)
        .join(models.Sprint)
        .filter(models.Sprint.project_id == project_id)
        .filter(models.Task.status != "done")
        .all()
    )

    def task_score(task):
        status_boost = 10 if task.status == "in_progress" else 0
        priority_score = PRIORITY_WEIGHTS.get(task.priority, 1)
        blocked_penalty = -2 if task.status == "blocked" else 0
        return status_boost + priority_score + blocked_penalty

    ranked = sorted(pending_tasks, key=task_score, reverse=True)

    ranked_tasks = [
        {
            "id": t.id,
            "title": t.title,
            "status": t.status,
            "priority": t.priority,
            "recommended_action": (
                "Resolve blocker first" if t.status == "blocked"
                else "Continue and finish" if t.status == "in_progress"
                else "Start next"
            ),
        }
        for t in ranked
    ]

    delay_risk = risk_data.get("delay_risk") if risk_data else None

    if delay_risk is None:
        feasibility = "Unknown — Risk Agent data not available"
        suggested_sprint_goal = "Complete highest-priority pending tasks"
    elif delay_risk >= 0.7:
        feasibility = "At Risk — recommend reducing sprint scope"
        suggested_sprint_goal = "Focus only on unblocking critical tasks; defer new work"
    elif delay_risk >= 0.4:
        feasibility = "Needs Attention — proceed with caution"
        suggested_sprint_goal = "Prioritize unblocking tasks before starting new ones"
    else:
        feasibility = "On Track — current scope is feasible"
        suggested_sprint_goal = "Continue current sprint plan as scheduled"

    # --- Timeline adjustment ---
    features = risk_data.get("features_used", {}) if risk_data else {}
    timeline_adjustment = calculate_timeline_adjustment(project, features)

    result = {
        "project_id": project_id,
        "ranked_tasks": ranked_tasks,
        "pending_task_count": len(ranked_tasks),
        "suggested_sprint_goal": suggested_sprint_goal,
        "feasibility": feasibility,
        "delay_risk_considered": delay_risk,
        "timeline_adjustment": timeline_adjustment,
    }

    logger.info(f"Planning Agent run for project_id={project_id}: feasibility={feasibility}, pending_tasks={len(ranked_tasks)}")
    return result

def calculate_timeline_adjustment(project, features: dict) -> dict:
    """
    Suggests a revised deadline based on current velocity and remaining work.
    Compares it against the original deadline to flag risk of delay.
    """

    velocity = features.get("velocity", 0)
    total_tasks = features.get("total_tasks", 0)
    done_tasks = features.get("done_tasks", 0)
    remaining_tasks = total_tasks - done_tasks

    if velocity <= 0 or remaining_tasks <= 0:
        return {
            "original_deadline": project.deadline.isoformat() if project.deadline else None,
            "suggested_deadline": None,
            "estimated_days_remaining": None,
            "adjustment_message": (
                "No remaining tasks." if remaining_tasks <= 0
                else "Insufficient velocity data to estimate a timeline."
            ),
            "is_at_risk": False,
        }

    estimated_days_remaining = round(remaining_tasks / velocity, 1)
    suggested_deadline = datetime.now() + timedelta(days=estimated_days_remaining)

    original_deadline = project.deadline
    is_at_risk = False
    adjustment_message = "Current pace supports the original deadline."

    if original_deadline:
        original_deadline_naive = original_deadline.replace(tzinfo=None)
        if suggested_deadline > original_deadline_naive:
            is_at_risk = True
            days_over = (suggested_deadline - original_deadline_naive).days
            adjustment_message = f"At current pace, completion is projected {days_over} day(s) past the original deadline."
    else:
        adjustment_message = "No original deadline set — estimate based on current pace only."

    return {
        "original_deadline": original_deadline.isoformat() if original_deadline else None,
        "suggested_deadline": suggested_deadline.isoformat(),
        "estimated_days_remaining": estimated_days_remaining,
        "adjustment_message": adjustment_message,
        "is_at_risk": is_at_risk,
    }