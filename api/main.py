from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from api.database import engine, Base, get_db
from api import models
from api.routers import projects, sprints, tasks
from api.github_client import get_repo_activity_summary
from agents.engineering_agent import run_engineering_agent
from api.database import SessionLocal
from agents.risk_agent import extract_risk_features

Base.metadata.create_all(bind=engine)

app = FastAPI(title="EngiPilot API", version="0.1.0")

app.include_router(projects.router)
app.include_router(sprints.router)
app.include_router(tasks.router)

@app.get("/")
def root():
    return {"status": "EngiPilot API is running"}

@app.get("/health/db")
def check_db_connection(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"database": "connected"}
    except Exception as e:
        return {"database": "error", "detail": str(e)}

@app.get("/github/activity")
def github_activity():
    return get_repo_activity_summary()

@app.get("/agents/engineering/{project_id}")
def engineering_agent_endpoint(project_id: int):
    db = SessionLocal()
    try:
        result = run_engineering_agent(project_id, db)
        return result
    finally:
        db.close()

@app.get("/agents/risk/features/{project_id}")
def risk_features_endpoint(project_id: int):
    db = SessionLocal()
    try:
        return extract_risk_features(project_id, db)
    finally:
        db.close()