from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CasillaCreate(BaseModel):
    casilla_id: str
    entidad_federativa: str
    municipio_o_delegacion: str
    distrito: str
    seccion: str
    tipo_casilla: str
    tipo_eleccion: str
    proceso_electoral: str

class CasillaOut(CasillaCreate):
    id: str
    created_at: datetime
    model_config = {"from_attributes": True}