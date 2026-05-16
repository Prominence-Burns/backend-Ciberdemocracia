from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ResultadoCreate(BaseModel):
    acta_id: str
    partido_o_coalicion: str
    partido_id: str = Field(alias="id")   # "id" en JSON → "partido_id" en BD
    votos: int = 0
    es_coalicion: bool = False
    partidos_coalicion: Optional[List[str]] = None

    model_config = {"populate_by_name": True}

class ResultadoOut(BaseModel):
    id: str
    acta_id: str
    partido_o_coalicion: str
    partido_id: str
    votos: int
    es_coalicion: bool
    partidos_coalicion: Optional[List[str]]
    created_at: datetime
    model_config = {"from_attributes": True}