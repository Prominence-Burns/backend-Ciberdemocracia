from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BoletaCreate(BaseModel):
    casilla_id: str
    image_url: str
    voto_detectado: Optional[str] = None
    confianza_ia: Optional[float] = None
    revision_humana: bool = False
    clasificacion_final: Optional[str] = None

class BoletaOut(BoletaCreate):
    id: str
    created_at: datetime
    model_config = {"from_attributes": True}