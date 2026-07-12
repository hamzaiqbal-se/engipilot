import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.database import Base
from api import models
from agents.planning_agent import run_planning_agent


@pytest.fixture
def test_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestSession = sessionmaker(bind=engine)
    db = TestSession()
    yield db
    db.close()


@pytest.fixture
def sample_project_with_tasks(test_db):
    project = models.Project(name="Planning Test", technology="AI/ML", status="active")
    test_db.add(project)
    test_db.commit()
    test_db.refresh(project)

    sprint = models.Sprint(project_id=project.id, sprint_number=1, goal="Test sprint")
    test_db.add(sprint)
    test_db.commit()
    test_db.refresh(sprint)

    tasks = [
        models.Task(sprint_id=sprint.id, title="Done task", status="done", priority="high"),
        models.Task(sprint_id=sprint.id, title="In progress task", status="in_progress", priority="medium"),
        models.Task(sprint_id=sprint.id, title="Blocked task", status="blocked", priority="high"),
        models.Task(sprint_id=sprint.id, title="Todo task", status="todo", priority="low"),
    ]
    test_db.add_all(tasks)
    test_db.commit()

    return project


def test_planning_agent_ranks_tasks_correctly(sample_project_with_tasks, test_db):
    result = run_planning_agent(sample_project_with_tasks.id, test_db, risk_data={"delay_risk": 0.3})

    assert result["pending_task_count"] == 3  # done task excluded
    assert result["feasibility"] == "On Track — current scope is feasible"

    # in_progress task should be ranked first
    assert result["ranked_tasks"][0]["status"] == "in_progress"


def test_planning_agent_flags_high_risk(sample_project_with_tasks, test_db):
    result = run_planning_agent(sample_project_with_tasks.id, test_db, risk_data={"delay_risk": 0.85})
    assert "At Risk" in result["feasibility"]


def test_planning_agent_handles_missing_project(test_db):
    result = run_planning_agent(9999, test_db)
    assert "error" in result