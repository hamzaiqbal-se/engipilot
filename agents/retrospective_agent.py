import os
import json
from shared.gemini_client import generate_text
import logging

logger = logging.getLogger("engipilot")


def generate_sprint_retrospective(state: dict) -> dict:
    """
    Sprint Retrospective Generator:
    - Combines Reporting, Risk, and Documentation agent outputs
    - Uses Gemini (via the shared fallback-aware client) to generate a
      structured retrospective: what went well, what didn't, and action items.
    """

    engineering_data = state.get("engineering_data", {})
    risk_data = state.get("risk_data", {})
    planning_data = state.get("planning_data", {})
    report_output = state.get("report_output", {})

    prompt = f"""You are generating a sprint retrospective for a software engineering team.
Based ONLY on the data below, produce a JSON object with exactly these keys:
"went_well": a list of 2-3 short bullet points (strings) about what went well this sprint,
"went_wrong": a list of 2-3 short bullet points about what didn't go well,
"action_items": a list of 2-3 short, actionable next steps.

Do not invent facts not present in the data. Keep each bullet point under 15 words.
Return ONLY valid JSON, no markdown formatting, no explanation.

Engineering Data: {engineering_data}
Risk Data: {risk_data}
Planning Data: {planning_data}
Existing Report: {report_output.get("report", "")}
"""

    try:
        raw_text = generate_text(prompt)
    except Exception as e:
        logger.info(f"Retrospective generation failed — {e}")
        return {
            "went_well": [],
            "went_wrong": [],
            "action_items": [],
            "error": str(e),
        }

    try:
        if raw_text.startswith("```"):
            raw_text = raw_text.strip("`")
            if raw_text.startswith("json"):
                raw_text = raw_text[4:].strip()

        parsed = json.loads(raw_text)
    except json.JSONDecodeError as e:
        logger.info(f"Retrospective: failed to parse JSON — {e}")
        return {
            "went_well": [],
            "went_wrong": [],
            "action_items": [],
            "error": "Could not parse retrospective output.",
        }

    result = {
        "went_well": parsed.get("went_well", []),
        "went_wrong": parsed.get("went_wrong", []),
        "action_items": parsed.get("action_items", []),
    }

    logger.info(f"Sprint retrospective generated for project_id={state.get('project_id')}")
    return result