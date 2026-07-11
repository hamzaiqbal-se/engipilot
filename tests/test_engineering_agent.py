import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.database import Base
from api import models
from agents.engineering_agent import run_engineering_agent


@pytest.fixture
def test_db():
    """Creates a fresh in-memory SQLite database for each test."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestSession = sessionmaker(bind=engine)
    db = TestSession()
    yield db
    db.close()


@pytest.fixture
def sample_project(test_db):
    """Creates a project with one sprint and two tasks (one done, one blocked)."""
    project = models.Project(name="Test Project", technology="AI/ML", status="active")
    test_db.add(project)
    test_db.commit()
    test_db.refresh(project)

    sprint = models.Sprint(project_id=project.id, sprint_number=1, goal="Test sprint")
    test_db.add(sprint)
    test_db.commit()
    test_db.refresh(sprint)

    task1 = models.Task(sprint_id=sprint.id, title="Task 1", status="done", priority="high")
    task2 = models.Task(sprint_id=sprint.id, title="Task 2", status="blocked", priority="medium")
    test_db.add_all([task1, task2])
    test_db.commit()

    return project


def test_engineering_agent_returns_correct_structure(sample_project, test_db, monkeypatch):
    """Engineering Agent should return a dict matching the engineering_data schema."""

    # Avoid a real GitHub API call during testing
    def fake_github_activity():
        return {
            "total_recent_commits": 5,
            "total_recent_prs": 2,
            "open_prs": 1,
            "merged_prs": 1,
            "commits": [{"date": "2026-07-11T00:00:00Z"}],
            "pull_requests": [],
        }

    monkeypatch.setattr(
        "agents.engineering_agent.get_repo_activity_summary", fake_github_activity
    )

    result = run_engineering_agent(sample_project.id, test_db)

    assert result["project_id"] == sample_project.id
    assert result["total_tasks"] == 2
    assert result["done_tasks"] == 1
    assert result["blocked_task_count"] == 1
    assert result["progress_percentage"] == 50.0
    assert "is_inactive" in result


def test_engineering_agent_handles_missing_project(test_db):
    """Should return an error dict when project doesn't exist."""
    result = run_engineering_agent(9999, test_db)
    assert "error" in result