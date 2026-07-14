import pytest
from agents.documentation_agent import run_documentation_agent


def test_documentation_agent_returns_answer(monkeypatch):
    """Documentation Agent should retrieve context and generate a grounded answer."""

    def fake_search(query, n_results=3):
        return {
            "ids": [["doc1"]],
            "documents": [["EngiPilot uses XGBoost models for risk prediction."]],
        }

    class FakeResponse:
        text = "EngiPilot uses XGBoost models to predict risk."

    class FakeModel:
        def generate_content(self, prompt):
            return FakeResponse()

    monkeypatch.setattr("agents.documentation_agent.search_documents", fake_search)
    monkeypatch.setattr(
        "agents.documentation_agent.genai.GenerativeModel", lambda name: FakeModel()
    )

    result = run_documentation_agent("What models does the Risk Agent use?")

    assert result["query"] == "What models does the Risk Agent use?"
    assert "XGBoost" in result["answer"]
    assert result["sources"] == ["doc1"]


def test_documentation_agent_handles_no_results(monkeypatch):
    def fake_search(query, n_results=3):
        return {"ids": [[]], "documents": [[]]}

    monkeypatch.setattr("agents.documentation_agent.search_documents", fake_search)

    result = run_documentation_agent("Unrelated query")
    assert result["sources"] == []
    assert "No relevant documentation" in result["answer"]