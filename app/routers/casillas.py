from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.casilla import Casilla
from app.schemas.casilla import CasillaCreate, CasillaOut
from typing import List

router = APIRouter(prefix="/casillas", tags=["Casillas"])

@router.post("/", response_model=CasillaOut)
def crear(data: CasillaCreate, db: Session = Depends(get_db)):
    record = Casilla(**data.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.get("/", response_model=List[CasillaOut])
def listar(db: Session = Depends(get_db)):
    return db.query(Casilla).all()

@router.get("/{id}", response_model=CasillaOut)
def obtener(id: str, db: Session = Depends(get_db)):
    record = db.query(Casilla).filter(Casilla.id == id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Casilla no encontrada")
    return record

@router.delete("/{id}")
def eliminar(id: str, db: Session = Depends(get_db)):
    record = db.query(Casilla).filter(Casilla.id == id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Casilla no encontrada")
    db.delete(record)
    db.commit()
    return {"mensaje": "Casilla eliminada correctamente"}