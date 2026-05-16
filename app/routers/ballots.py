from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.ballot import Ballot
from app.schemas.ballot import BallotCreate, BallotOut
from typing import List

router = APIRouter(prefix="/ballots", tags=["Ballots"])

@router.post("/", response_model=BallotOut)
def create(data: BallotCreate, db: Session = Depends(get_db)):
    record = Ballot(**data.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.get("/", response_model=List[BallotOut])
def get_all(db: Session = Depends(get_db)):
    return db.query(Ballot).all()

@router.get("/{id}", response_model=BallotOut)
def get_one(id: str, db: Session = Depends(get_db)):
    record = db.query(Ballot).filter(Ballot.id == id).first()
    if not record:
        raise HTTPException(status_code=404, detail="No encontrado")
    return record

@router.delete("/{id}")
def delete(id: str, db: Session = Depends(get_db)):
    record = db.query(Ballot).filter(Ballot.id == id).first()
    if not record:
        raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(record)
    db.commit()
    return {"message": "Eliminado correctamente"}