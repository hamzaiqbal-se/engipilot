from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database import get_db
from api import models, schemas

router = APIRouter(prefix="/sprints", tags=["Sprints"])


@router.post("/", response_model=schemas.SprintResponse)
def create_sprint(sprint: schemas.SprintCreate, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == sprint.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    new_sprint = models.Sprint(**sprint.dict())
    db.add(new_sprint)
    db.commit()
    db.refresh(new_sprint)
    return new_sprint


@router.get("/", response_model=list[schemas.SprintResponse])
def get_all_sprints(db: Session = Depends(get_db)):
    return db.query(models.Sprint).all()


@router.get("/{sprint_id}", response_model=schemas.SprintResponse)
def get_sprint(sprint_id: int, db: Session = Depends(get_db)):
    sprint = db.query(models.Sprint).filter(models.Sprint.id == sprint_id).first()
    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")
    return sprint


@router.delete("/{sprint_id}")
def delete_sprint(sprint_id: int, db: Session = Depends(get_db)):
    sprint = db.query(models.Sprint).filter(models.Sprint.id == sprint_id).first()
    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")

    db.delete(sprint)
    db.commit()
    return {"detail": "Sprint deleted successfully"}