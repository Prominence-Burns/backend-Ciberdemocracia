from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class EventoCreate(BaseModel):
    entidad_tipo: str
    entidad_id: str
    tipo_evento: str
    usuario_id: Optional[str] = None
    detalles: Optional[Any] = None
    hash: Optional[str] = None

class EventoOut(EventoCreate):
    id: str
    timestamp: datetime
    model_config = {"from_attributes": True}