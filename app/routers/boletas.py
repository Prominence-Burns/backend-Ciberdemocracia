from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.boleta import Boleta
from app.schemas.boleta import BoletaCreate, BoletaOut
from typing import List

router = APIRouter(prefix="/boletas", tags=["Boletas"])

@router.post("/", response_model=BoletaOut)
def crear(data: BoletaCreate, db: Session = Depends(get_db)):
    record = Boleta(**data.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.get("/", response_model=List[BoletaOut])
def listar(db: Session = Depends(get_db)):
    return db.query(Boleta).all()

@router.get("/{id}", response_model=BoletaOut)
def obtener(id: str, db: Session = Depends(get_db)):
    record = db.query(Boleta).filter(Boleta.id == id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Boleta no encontrada")
    return record

@router.delete("/{id}")
def eliminar(id: str, db: Session = Depends(get_db)):
    record = db.query(Boleta).filter(Boleta.id == id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Boleta no encontrada")
    db.delete(record)
    db.commit()
    return {"mensaje": "Boleta eliminada correctamente"}