from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.event import Event
from app.schemas.event import EventCreate, EventOut
from typing import List

router = APIRouter(prefix="/events", tags=["Events"])

@router.post("/", response_model=EventOut)
def create(data: EventCreate, db: Session = Depends(get_db)):
    record = Event(**data.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.get("/", response_model=List[EventOut])
def get_all(db: Session = Depends(get_db)):
    return db.query(Event).all()

@router.get("/{id}", response_model=EventOut)
def get_one(id: str, db: Session = Depends(get_db)):
    record = db.query(Event).filter(Event.id == id).first()
    if not record:
        raise HTTPException(status_code=404, detail="No encontrado")
    return record