import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.database import Base
from api import models
from agents.risk_agent import run_risk_agent


@pytest.fixture
def test_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestSession = sessionmaker(bind=engine)
    db = TestSession()
    yield db
    db.close()


@pytest.fixture
def sample_project(test_db):
    project = models.Project(name="Risk Test Project", technology="AI/ML", status="active")
    test_db.add(project)
    test_db.commit()
    test_db.refresh(project)

    sprint = models.Sprint(project_id=project.id, sprint_number=1, goal="Test sprint")
    test_db.add(sprint)
    test_db.commit()
    test_db.refresh(sprint)

    tasks = [
        models.Task(sprint_id=sprint.id, title="Task 1", status="done", priority="high"),
        models.Task(sprint_id=sprint.id, title="Task 2", status="blocked", priority="medium"),
    ]
    test_db.add_all(tasks)
    test_db.commit()

    return project


def test_risk_agent_returns_valid_predictions(sample_project, test_db):
    result = run_risk_agent(sample_project.id, test_db)

    assert result["project_id"] == sample_project.id
    assert 0.0 <= result["delay_risk"] <= 1.0
    assert 0.0 <= result["burnout_risk"] <= 1.0
    assert result["completion_forecast"] in ["On Track", "Needs Attention", "At Risk"]


def test_risk_agent_handles_missing_project(test_db):
    result = run_risk_agent(9999, test_db)
    assert "error" in result