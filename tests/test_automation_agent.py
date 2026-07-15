import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.database import Base
from agents.automation_agent import run_automation_checks


@pytest.fixture
def test_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestSession = sessionmaker(bind=engine)
    db = TestSession()
    yield db
    db.close()


def test_automation_fires_high_risk_trigger(test_db, monkeypatch):
    monkeypatch.setattr("agents.automation_agent.send_slack_notification", lambda msg: True)

    fake_state = {
        "project_id": 1,
        "engineering_data": {"blocked_task_count": 0, "is_inactive": False},
        "risk_data": {"delay_risk": 0.85},
    }

    result = run_automation_checks(fake_state, test_db)

    assert "high_risk_notification" in result["triggers_fired"]
    assert result["trigger_count"] == 1


def test_automation_fires_multiple_triggers(test_db, monkeypatch):
    monkeypatch.setattr("agents.automation_agent.send_slack_notification", lambda msg: True)

    fake_state = {
        "project_id": 2,
        "engineering_data": {"blocked_task_count": 3, "is_inactive": True},
        "risk_data": {"delay_risk": 0.9},
    }

    result = run_automation_checks(fake_state, test_db)

    assert set(result["triggers_fired"]) == {
        "high_risk_notification",
        "blocked_tasks_detected",
        "inactive_project_detected",
    }
    assert result["trigger_count"] == 3


def test_automation_no_triggers_when_healthy(test_db, monkeypatch):
    monkeypatch.setattr("agents.automation_agent.send_slack_notification", lambda msg: True)

    fake_state = {
        "project_id": 3,
        "engineering_data": {"blocked_task_count": 0, "is_inactive": False},
        "risk_data": {"delay_risk": 0.2},
    }

    result = run_automation_checks(fake_state, test_db)

    assert result["triggers_fired"] == []
    assert result["trigger_count"] == 0