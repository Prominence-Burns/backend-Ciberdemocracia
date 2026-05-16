from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ActaCreate(BaseModel):
    casilla_id: str
    image_url: Optional[str] = None
    boletas_recibidas: Optional[int] = None
    boletas_sobrantes: Optional[int] = None
    personas_votaron: Optional[int] = None
    rep_partido_fuera_lista: Optional[int] = None
    boletas_en_urna: Optional[int] = None
    boletas_contadas: Optional[int] = None
    candidatos_no_registrados: Optional[int] = None
    votos_nulos: Optional[int] = None
    total_votos: Optional[int] = None
    boletas_procesadas: Optional[int] = None
    boletas_revision_humana: Optional[int] = None
    criterio_1: Optional[bool] = None
    criterio_2: Optional[bool] = None
    criterio_3: Optional[bool] = None
    criterio_4: Optional[bool] = None
    acta_consistente: Optional[bool] = None
    tipo_error: Optional[str] = None
    incidentes_presentes: bool = False
    descripcion_incidentes: Optional[str] = None
    hojas_incidentes: int = 0
    hash_boletas: Optional[str] = None
    validation_status: Optional[str] = None

class ActaOut(ActaCreate):
    id: str
    created_at: datetime
    model_config = {"from_attributes": True}