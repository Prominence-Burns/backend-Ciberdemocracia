from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.polling_station import PollingStation
from app.schemas.polling_station import PollingStationCreate, PollingStationOut
from typing import List

router = APIRouter(prefix="/polling-stations", tags=["Polling Stations"])

@router.post("/", response_model=PollingStationOut)
def create(data: PollingStationCreate, db: Session = Depends(get_db)):
    record = PollingStation(**data.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.get("/", response_model=List[PollingStationOut])
def get_all(db: Session = Depends(get_db)):
    return db.query(PollingStation).all()

@router.get("/{id}", response_model=PollingStationOut)
def get_one(id: str, db: Session = Depends(get_db)):
    record = db.query(PollingStation).filter(PollingStation.id == id).first()
    if not record:
        raise HTTPException(status_code=404, detail="No encontrado")
    return record

@router.delete("/{id}")
def delete(id: str, db: Session = Depends(get_db)):
    record = db.query(PollingStation).filter(PollingStation.id == id).first()
    if not record:
        raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(record)
    db.commit()
    return {"message": "Eliminado correctamente"}