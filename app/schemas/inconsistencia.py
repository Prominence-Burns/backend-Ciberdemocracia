from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class InconsistenciaCreate(BaseModel):
    boleta_id: str
    tipo_inconsistencia: str
    severidad: str
    resuelta: bool = False
    notas_resolucion: Optional[str] = None
    resuelta_por: Optional[str] = None

class InconsistenciaOut(InconsistenciaCreate):
    id: str
    created_at: datetime
    model_config = {"from_attributes": True}