from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ActaCreate(BaseModel):
    casilla_id: str
    image_url: Optional[str] = None

    # bloque_1
    boletas_recibidas: Optional[int] = None
    BS: Optional[int] = None
    PV: Optional[int] = None
    RPPV: Optional[int] = None
    SV: Optional[int] = None
    BSU: Optional[int] = None

    # bloque_2
    CNR: Optional[int] = None
    VN: Optional[int] = None
    RV: Optional[int] = None

    # consistencia
    criterio_1_pv_rppv_sv: Optional[bool] = None
    criterio_2_sv_bsu: Optional[bool] = None
    criterio_3_bsu_rv: Optional[bool] = None
    criterio_4_sum_vi_rv: Optional[bool] = None
    acta_consistente: Optional[bool] = None
    tipo_error: Optional[str] = None

    # incidentes
    se_presentaron: bool = False
    descripcion: Optional[str] = None
    hojas_de_incidentes: int = 0

    # raíz
    boletas_procesadas: Optional[int] = None
    boletas_revision_humana: Optional[int] = None
    hash_boletas: Optional[str] = None
    validation_status: Optional[str] = None

class ActaOut(ActaCreate):
    id: str
    created_at: datetime
    model_config = {"from_attributes": True}