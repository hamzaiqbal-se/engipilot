from sqlalchemy.orm import Session
from shared.gemini_client import generate_text
import logging

logger = logging.getLogger("engipilot")


def run_reporting_agent(state: dict) -> dict:
    """
    Reporting Agent:
    - Takes the aggregated state from other agents (engineering_data, risk_data,
      planning_data, qa_data) and generates a natural-language report using Gemini.
    Returns a dict matching the 'report_output' schema field.
    """

    engineering_data = state.get("engineering_data", {})
    risk_data = state.get("risk_data", {})
    planning_data = state.get("planning_data", {})
    qa_data = state.get("qa_data", {})

    prompt = f"""You are an engineering reporting assistant. Write a concise, professional
project status report (4-6 sentences) for a project manager, based on the following data.
Do not invent numbers not present in the data. Be direct and actionable.

Engineering Progress: {engineering_data}
Risk Assessment: {risk_data}
Planning Recommendation: {planning_data}
QA / Review Queue: {qa_data}

Write the report now:"""

    try:
        report_text = generate_text(prompt)
    except Exception as e:
        logger.info(f"Reporting Agent: Gemini generation failed — {e}")
        return {"error": f"LLM generation failed: {str(e)}"}

    result = {
        "project_id": state.get("project_id"),
        "report": report_text,
        "based_on": {
            "progress_percentage": engineering_data.get("progress_percentage"),
            "delay_risk": risk_data.get("delay_risk"),
            "feasibility": planning_data.get("feasibility"),
            "open_prs": qa_data.get("total_open_prs"),
        },
    }

    logger.info(f"Reporting Agent generated report for project_id={state.get('project_id')}")
    return result