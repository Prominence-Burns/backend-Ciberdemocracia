from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.acta import Acta
from app.schemas.acta import ActaCreate, ActaOut
from typing import List

router = APIRouter(prefix="/actas", tags=["Actas"])

@router.post("/", response_model=ActaOut)
def crear(data: ActaCreate, db: Session = Depends(get_db)):
    record = Acta(**data.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.get("/", response_model=List[ActaOut])
def listar(db: Session = Depends(get_db)):
    return db.query(Acta).all()

@router.get("/{id}", response_model=ActaOut)
def obtener(id: str, db: Session = Depends(get_db)):
    record = db.query(Acta).filter(Acta.id == id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Acta no encontrada")
    return record

@router.delete("/{id}")
def eliminar(id: str, db: Session = Depends(get_db)):
    record = db.query(Acta).filter(Acta.id == id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Acta no encontrada")
    db.delete(record)
    db.commit()
    return {"mensaje": "Acta eliminada correctamente"}