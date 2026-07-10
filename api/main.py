from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from api.database import engine, Base, get_db

# Creates tables if they don't exist yet
Base.metadata.create_all(bind=engine)

app = FastAPI(title="EngiPilot API", version="0.1.0")

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