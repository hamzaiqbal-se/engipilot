from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from api.database import engine, Base, get_db
from api import models
from api.routers import projects, sprints, tasks
from api.github_client import get_repo_activity_summary

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