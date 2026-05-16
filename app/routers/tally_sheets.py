from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.tally_sheet import TallySheet
from app.schemas.tally_sheet import TallySheetCreate, TallySheetOut
from typing import List

router = APIRouter(prefix="/tally-sheets", tags=["Tally Sheets"])

@router.post("/", response_model=TallySheetOut)
def create(data: TallySheetCreate, db: Session = Depends(get_db)):
    record = TallySheet(**data.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@router.get("/", response_model=List[TallySheetOut])
def get_all(db: Session = Depends(get_db)):
    return db.query(TallySheet).all()

@router.get("/{id}", response_model=TallySheetOut)
def get_one(id: str, db: Session = Depends(get_db)):
    record = db.query(TallySheet).filter(TallySheet.id == id).first()
    if not record:
        raise HTTPException(status_code=404, detail="No encontrado")
    return record

@router.delete("/{id}")
def delete(id: str, db: Session = Depends(get_db)):
    record = db.query(TallySheet).filter(TallySheet.id == id).first()
    if not record:
        raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(record)
    db.commit()
    return {"message": "Eliminado correctamente"}