from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from typing import List

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserOut)
def create(data: UserCreate, db: Session = Depends(get_db)):
    record = User(**data.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.get("/", response_model=List[UserOut])
def get_all(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.get("/{id}", response_model=UserOut)
def get_one(id: str, db: Session = Depends(get_db)):
    record = db.query(User).filter(User.id == id).first()
    if not record:
        raise HTTPException(status_code=404, detail="No encontrado")
    return record

@router.delete("/{id}")
def delete(id: str, db: Session = Depends(get_db)):
    record = db.query(User).filter(User.id == id).first()
    if not record:
        raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(record)
    db.commit()
    return {"message": "Eliminado correctamente"}