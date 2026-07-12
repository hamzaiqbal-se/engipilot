from sqlalchemy.orm import Session
from api import models
import logging

logger = logging.getLogger("engipilot")

PRIORITY_WEIGHTS = {"high": 3, "medium": 2, "low": 1}


def run_planning_agent(project_id: int, db: Session, risk_data: dict = None) -> dict:
    """
    Planning Agent:
    - Ranks pending tasks by priority and status
    - Suggests a sprint goal
    - Uses Risk Agent's delay_risk (if provided) to adjust feasibility recommendation
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

    # --- Rank tasks: in_progress tasks first (finish what's started), then by priority weight ---
    def task_score(task):
        status_boost = 10 if task.status == "in_progress" else 0
        priority_score = PRIORITY_WEIGHTS.get(task.priority, 1)
        blocked_penalty = -5 if task.status == "blocked" else 0
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

    # --- Feasibility check using Risk Agent's delay_risk ---
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

    result = {
        "project_id": project_id,
        "ranked_tasks": ranked_tasks,
        "pending_task_count": len(ranked_tasks),
        "suggested_sprint_goal": suggested_sprint_goal,
        "feasibility": feasibility,
        "delay_risk_considered": delay_risk,
    }

    logger.info(f"Planning Agent run for project_id={project_id}: feasibility={feasibility}, pending_tasks={len(ranked_tasks)}")
    return result