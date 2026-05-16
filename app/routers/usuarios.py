from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioOut
from typing import List

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.post("/", response_model=UsuarioOut)
def crear(data: UsuarioCreate, db: Session = Depends(get_db)):
    record = Usuario(**data.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.get("/", response_model=List[UsuarioOut])
def listar(db: Session = Depends(get_db)):
    return db.query(Usuario).all()

@router.get("/{id}", response_model=UsuarioOut)
def obtener(id: str, db: Session = Depends(get_db)):
    record = db.query(Usuario).filter(Usuario.id == id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return record

@router.delete("/{id}")
def eliminar(id: str, db: Session = Depends(get_db)):
    record = db.query(Usuario).filter(Usuario.id == id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(record)
    db.commit()
    return {"mensaje": "Usuario eliminado correctamente"}