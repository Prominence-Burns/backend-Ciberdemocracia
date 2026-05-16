from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UsuarioCreate(BaseModel):
    nombre: str
    rol: str
    casilla_id: Optional[str] = None

class UsuarioOut(UsuarioCreate):
    id: str
    created_at: datetime
    model_config = {"from_attributes": True}