import pytest
from agents.reporting_agent import run_reporting_agent


def test_reporting_agent_generates_report(monkeypatch):
    """Reporting Agent should synthesize a report from aggregated agent data."""

    def fake_generate_text(prompt):
        return "The project is 50% complete with one blocked task. Delay risk is moderate."

    monkeypatch.setattr("agents.reporting_agent.generate_text", fake_generate_text)

    fake_state = {
        "project_id": 1,
        "engineering_data": {"progress_percentage": 50},
        "risk_data": {"delay_risk": 0.5},
        "planning_data": {"feasibility": "Needs Attention"},
        "qa_data": {"total_open_prs": 0},
    }

    result = run_reporting_agent(fake_state)

    assert result["project_id"] == 1
    assert "50" in result["report"]
    assert result["based_on"]["progress_percentage"] == 50


def test_reporting_agent_handles_llm_failure(monkeypatch):
    def fake_generate_text_raises(prompt):
        raise Exception("API unreachable")

    monkeypatch.setattr("agents.reporting_agent.generate_text", fake_generate_text_raises)

    result = run_reporting_agent({"project_id": 1})
    assert "error" in result