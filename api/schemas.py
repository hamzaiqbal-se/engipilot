from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ---------- Project Schemas ----------
class ProjectCreate(BaseModel):
    name: str
    technology: str
    deadline: Optional[datetime] = None
    status: Optional[str] = "active"

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    technology: Optional[str] = None
    deadline: Optional[datetime] = None
    status: Optional[str] = None

class ProjectResponse(BaseModel):
    id: int
    name: str
    technology: str
    start_date: Optional[datetime]
    deadline: Optional[datetime]
    status: str

    class Config:
        from_attributes = True


# ---------- Sprint Schemas ----------
class SprintCreate(BaseModel):
    project_id: int
    sprint_number: int
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    goal: Optional[str] = None

class SprintResponse(BaseModel):
    id: int
    project_id: int
    sprint_number: int
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    goal: Optional[str]

    class Config:
        from_attributes = True


# ---------- Task Schemas ----------
class TaskCreate(BaseModel):
    sprint_id: int
    assignee_id: Optional[int] = None
    title: str
    status: Optional[str] = "todo"
    priority: Optional[str] = "medium"

class TaskUpdate(BaseModel):
    assignee_id: Optional[int] = None
    title: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None

class TaskResponse(BaseModel):
    id: int
    sprint_id: int
    assignee_id: Optional[int]
    title: str
    status: str
    priority: str

    class Config:
        from_attributes = True