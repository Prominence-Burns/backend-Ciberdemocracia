import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, JSON
from app.database import Base

class Acta(Base):
    __tablename__ = "actas"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    casilla_id = Column(String, ForeignKey("casillas.id"), nullable=False)
    image_url = Column(String, nullable=True)

    # bloque_1
    boletas_recibidas = Column(Integer, nullable=True)
    BS = Column(Integer, nullable=True)
    PV = Column(Integer, nullable=True)
    RPPV = Column(Integer, nullable=True)
    SV = Column(Integer, nullable=True)
    BSU = Column(Integer, nullable=True)

    # bloque_2
    CNR = Column(Integer, nullable=True)
    VN = Column(Integer, nullable=True)
    RV = Column(Integer, nullable=True)

    # consistencia
    criterio_1_pv_rppv_sv = Column(Boolean, nullable=True)
    criterio_2_sv_bsu = Column(Boolean, nullable=True)
    criterio_3_bsu_rv = Column(Boolean, nullable=True)
    criterio_4_sum_vi_rv = Column(Boolean, nullable=True)
    acta_consistente = Column(Boolean, nullable=True)
    tipo_error = Column(String, nullable=True)

    # incidentes
    se_presentaron = Column(Boolean, default=False)
    descripcion = Column(String, nullable=True)
    hojas_de_incidentes = Column(Integer, default=0)

    # raíz del JSON
    boletas_procesadas = Column(Integer, nullable=True)
    boletas_revision_humana = Column(Integer, nullable=True)
    hash_boletas = Column(String, nullable=True)

    validation_status = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)