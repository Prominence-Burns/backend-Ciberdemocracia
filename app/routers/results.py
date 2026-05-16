from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.result import Result
from app.schemas.result import ResultCreate, ResultOut
from typing import List

router = APIRouter(prefix="/results", tags=["Results"])

@router.post("/", response_model=ResultOut)
def create(data: ResultCreate, db: Session = Depends(get_db)):
    record = Result(**data.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.get("/", response_model=List[ResultOut])
def get_all(db: Session = Depends(get_db)):
    return db.query(Result).all()

@router.get("/{id}", response_model=ResultOut)
def get_one(id: str, db: Session = Depends(get_db)):
    record = db.query(Result).filter(Result.id == id).first()
    if not record:
        raise HTTPException(status_code=404, detail="No encontrado")
    return record