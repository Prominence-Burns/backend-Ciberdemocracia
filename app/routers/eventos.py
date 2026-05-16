from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.evento import Evento
from app.schemas.evento import EventoCreate, EventoOut
from typing import List

router = APIRouter(prefix="/eventos", tags=["Eventos"])

@router.post("/", response_model=EventoOut)
def crear(data: EventoCreate, db: Session = Depends(get_db)):
    record = Evento(**data.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.get("/", response_model=List[EventoOut])
def listar(db: Session = Depends(get_db)):
    return db.query(Evento).all()

@router.get("/{id}", response_model=EventoOut)
def obtener(id: str, db: Session = Depends(get_db)):
    record = db.query(Evento).filter(Evento.id == id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return record