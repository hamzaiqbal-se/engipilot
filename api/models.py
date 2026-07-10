from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from api.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    technology = Column(String, nullable=False)   # e.g. "AI/ML", "MERN", "Laravel"
    start_date = Column(DateTime, server_default=func.now())
    deadline = Column(DateTime, nullable=True)
    status = Column(String, default="active")      # active, completed, at_risk, blocked

    sprints = relationship("Sprint", back_populates="project", cascade="all, delete")


class TeamMember(Base):
    __tablename__ = "team_members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)           # e.g. "AI Engineer", "Mentor"
    capacity_hours = Column(Float, default=40.0)     # weekly capacity
    current_workload = Column(Float, default=0.0)    # hours currently assigned

    tasks = relationship("Task", back_populates="assignee")


class Sprint(Base):
    __tablename__ = "sprints"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    sprint_number = Column(Integer, nullable=False)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    goal = Column(Text, nullable=True)

    project = relationship("Project", back_populates="sprints")
    tasks = relationship("Task", back_populates="sprint", cascade="all, delete")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    sprint_id = Column(Integer, ForeignKey("sprints.id"), nullable=False)
    assignee_id = Column(Integer, ForeignKey("team_members.id"), nullable=True)
    title = Column(String, nullable=False)
    status = Column(String, default="todo")          # todo, in_progress, blocked, done
    priority = Column(String, default="medium")       # low, medium, high
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    sprint = relationship("Sprint", back_populates="tasks")
    assignee = relationship("TeamMember", back_populates="tasks")


class AgentLog(Base):
    __tablename__ = "agent_logs"

    id = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String, nullable=False)
    action = Column(String, nullable=False)
    input_summary = Column(Text, nullable=True)
    output_summary = Column(Text, nullable=True)
    timestamp = Column(DateTime, server_default=func.now())


class RiskPrediction(Base):
    __tablename__ = "risk_predictions"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    delay_risk = Column(Float, nullable=True)
    burnout_risk = Column(Float, nullable=True)
    completion_forecast = Column(String, nullable=True)
    predicted_at = Column(DateTime, server_default=func.now())