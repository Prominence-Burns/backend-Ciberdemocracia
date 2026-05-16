from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.resultado import Resultado
from app.schemas.resultado import ResultadoCreate, ResultadoOut
from typing import List

router = APIRouter(prefix="/resultados", tags=["Resultados"])

@router.post("/", response_model=ResultadoOut)
def crear(data: ResultadoCreate, db: Session = Depends(get_db)):
    record = Resultado(**data.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.get("/", response_model=List[ResultadoOut])
def listar(db: Session = Depends(get_db)):
    return db.query(Resultado).all()

@router.get("/{id}", response_model=ResultadoOut)
def obtener(id: str, db: Session = Depends(get_db)):
    record = db.query(Resultado).filter(Resultado.id == id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Resultado no encontrado")
    return record