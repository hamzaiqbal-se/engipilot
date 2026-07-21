import pytest
from agents.qa_agent import run_qa_agent


def test_qa_agent_returns_valid_structure(monkeypatch):
    """QA Agent should return a properly structured result, using fake PR data."""

    def fake_pull_requests(repo=None, state="open", limit=20):
        return [
            {
                "number": 1,
                "title": "Old PR",
                "state": "open",
                "created_at": "2026-06-01T00:00:00Z",
                "updated_at": "2026-06-02T00:00:00Z",
                "merged_at": None,
                "draft": False,
            },
            {
                "number": 2,
                "title": "Draft PR",
                "state": "open",
                "created_at": "2026-07-10T00:00:00Z",
                "updated_at": "2026-07-10T00:00:00Z",
                "merged_at": None,
                "draft": True,
            },
        ]

    monkeypatch.setattr("agents.qa_agent.get_pull_requests", fake_pull_requests)

    result = run_qa_agent()

    assert result["total_open_prs"] == 2
    assert result["review_priority_queue"][0]["number"] == 1
    assert result["review_priority_queue"][0]["urgency_label"] == "High"
    assert result["review_priority_queue"][1]["urgency_label"] == "Low (Draft)"


def test_qa_agent_handles_api_failure(monkeypatch):
    def fake_failure(repo=None, state="open", limit=20):
        raise Exception("GitHub API unreachable")

    monkeypatch.setattr("agents.qa_agent.get_pull_requests", fake_failure)

    result = run_qa_agent()
    assert "error" in result