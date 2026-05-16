from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ResultadoCreate(BaseModel):
    acta_id: str
    partido_o_coalicion: str
    partido_id: str
    votos: int = 0
    es_coalicion: bool = False
    partidos_coalicion: Optional[List[str]] = None

class ResultadoOut(ResultadoCreate):
    id: str
    created_at: datetime
    model_config = {"from_attributes": True}