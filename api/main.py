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
from agents.risk_agent import run_risk_agent
from orchestrator.graph import run_orchestrator
from agents.planning_agent import run_planning_agent
from agents.risk_agent import run_risk_agent
from agents.qa_agent import run_qa_agent
from shared.vector_store import add_document, search_documents
from agents.documentation_agent import index_project_documents, run_documentation_agent
from agents.reporting_agent import run_reporting_agent
from agents.engineering_agent import run_engineering_agent
from agents.risk_agent import run_risk_agent
from agents.planning_agent import run_planning_agent
from agents.qa_agent import run_qa_agent


app = FastAPI(title="EngiPilot API", version="0.1.0")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/agents/risk/{project_id}")
def risk_agent_endpoint(project_id: int):
    db = SessionLocal()
    try:
        return run_risk_agent(project_id, db)
    finally:
        db.close()

@app.get("/orchestrator/run/{project_id}")
def orchestrator_endpoint(project_id: int):
    db = SessionLocal()
    try:
        result = run_orchestrator(project_id, db)
        return result
    finally:
        db.close()

@app.get("/agents/planning/{project_id}")
def planning_agent_endpoint(project_id: int):
    db = SessionLocal()
    try:
        risk_result = run_risk_agent(project_id, db)
        return run_planning_agent(project_id, db, risk_data=risk_result)
    finally:
        db.close()

@app.get("/agents/qa")
def qa_agent_endpoint():
    return run_qa_agent()

@app.post("/rag/add")
def rag_add_document(doc_id: str, text: str):
    add_document(doc_id, text)
    return {"status": "added", "doc_id": doc_id}

@app.get("/rag/search")
def rag_search(query: str):
    results = search_documents(query)
    return results

@app.post("/agents/documentation/index")
def documentation_index_endpoint():
    return index_project_documents()

@app.get("/agents/documentation/query")
def documentation_query_endpoint(query: str):
    return run_documentation_agent(query)

@app.get("/agents/reporting/{project_id}")
def reporting_agent_endpoint(project_id: int):
    db = SessionLocal()
    try:
        engineering_result = run_engineering_agent(project_id, db)
        risk_result = run_risk_agent(project_id, db)
        planning_result = run_planning_agent(project_id, db, risk_data=risk_result)
        qa_result = run_qa_agent()

        state = {
            "project_id": project_id,
            "engineering_data": engineering_result,
            "risk_data": risk_result,
            "planning_data": planning_result,
            "qa_data": qa_result,
        }
        return run_reporting_agent(state)
    finally:
        db.close()