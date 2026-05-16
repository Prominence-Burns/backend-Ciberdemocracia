from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.inconsistencia import Inconsistencia
from app.schemas.inconsistencia import InconsistenciaCreate, InconsistenciaOut
from typing import List

router = APIRouter(prefix="/inconsistencias", tags=["Inconsistencias"])

@router.post("/", response_model=InconsistenciaOut)
def crear(data: InconsistenciaCreate, db: Session = Depends(get_db)):
    record = Inconsistencia(**data.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.get("/", response_model=List[InconsistenciaOut])
def listar(db: Session = Depends(get_db)):
    return db.query(Inconsistencia).all()

@router.get("/{id}", response_model=InconsistenciaOut)
def obtener(id: str, db: Session = Depends(get_db)):
    record = db.query(Inconsistencia).filter(Inconsistencia.id == id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Inconsistencia no encontrada")
    return record