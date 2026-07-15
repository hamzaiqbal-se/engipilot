from sqlalchemy.orm import Session
from api import models
from shared.notifications import send_slack_notification
from datetime import datetime
import logging

logger = logging.getLogger("engipilot")

DELAY_RISK_THRESHOLD = 0.7


def log_automation_event(db: Session, event_type: str, project_id: int, details: str):
    """Saves a structured automation event to the agent_logs table."""
    log_entry = models.AgentLog(
        agent_name="automation_agent",
        action=event_type,
        input_summary=f"project_id={project_id}",
        output_summary=details,
    )
    db.add(log_entry)
    db.commit()
    logger.info(f"Automation event logged: {event_type} for project_id={project_id}")


def run_automation_checks(state: dict, db: Session) -> dict:
    """
    Runs automation triggers based on the orchestrator's final state:
    - Notifies (Slack + log) when a project is At Risk (high delay_risk)
    - Logs blocked task detection
    - Logs inactive project detection
    Returns a summary of which triggers fired.
    """

    project_id = state.get("project_id")
    engineering_data = state.get("engineering_data", {})
    risk_data = state.get("risk_data", {})

    triggers_fired = []

    # --- Trigger 1: High delay risk -> notify PM ---
    delay_risk = risk_data.get("delay_risk")
    if delay_risk is not None and delay_risk >= DELAY_RISK_THRESHOLD:
        message = f"⚠️ *At Risk Alert* — Project {project_id} has a delay risk of {delay_risk:.2f}. Immediate PM attention recommended."
        log_automation_event(db, "high_risk_notification", project_id, message)
        send_slack_notification(message)
        triggers_fired.append("high_risk_notification")

    # --- Trigger 2: Blocked tasks detected ---
    blocked_count = engineering_data.get("blocked_task_count", 0)
    if blocked_count > 0:
        message = f"🚧 *Blocked Tasks Detected* — Project {project_id} has {blocked_count} blocked task(s)."
        log_automation_event(db, "blocked_tasks_detected", project_id, message)
        send_slack_notification(message)
        triggers_fired.append("blocked_tasks_detected")

    # --- Trigger 3: Inactive project detected ---
    is_inactive = engineering_data.get("is_inactive", False)
    if is_inactive:
        message = f"💤 *Inactive Project Alert* — Project {project_id} shows no recent GitHub activity."
        log_automation_event(db, "inactive_project_detected", project_id, message)
        send_slack_notification(message)
        triggers_fired.append("inactive_project_detected")

    result = {
        "project_id": project_id,
        "triggers_fired": triggers_fired,
        "trigger_count": len(triggers_fired),
    }

    logger.info(f"Automation checks completed for project_id={project_id}: {triggers_fired}")
    return result