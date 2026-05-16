from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.inconsistency import Inconsistency
from app.schemas.inconsistency import InconsistencyCreate, InconsistencyOut
from typing import List

router = APIRouter(prefix="/inconsistencies", tags=["Inconsistencies"])

@router.post("/", response_model=InconsistencyOut)
def create(data: InconsistencyCreate, db: Session = Depends(get_db)):
    record = Inconsistency(**data.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.get("/", response_model=List[InconsistencyOut])
def get_all(db: Session = Depends(get_db)):
    return db.query(Inconsistency).all()

@router.get("/{id}", response_model=InconsistencyOut)
def get_one(id: str, db: Session = Depends(get_db)):
    record = db.query(Inconsistency).filter(Inconsistency.id == id).first()
    if not record:
        raise HTTPException(status_code=404, detail="No encontrado")
    return record