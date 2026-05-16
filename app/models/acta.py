import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, JSON
from app.database import Base

class Acta(Base):
    __tablename__ = "actas"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    casilla_id = Column(String, ForeignKey("casillas.id"), nullable=False)
    image_url = Column(String, nullable=True)

    # Bloque 1 — Control de boletas
    boletas_recibidas = Column(Integer, nullable=True)   # BR: 95
    boletas_sobrantes = Column(Integer, nullable=True)   # BS: 50
    personas_votaron = Column(Integer, nullable=True)    # PV: 45
    rep_partido_fuera_lista = Column(Integer, nullable=True)  # RPPV: 0
    boletas_en_urna = Column(Integer, nullable=True)     # SV = PV + RPPV
    boletas_contadas = Column(Integer, nullable=True)    # BSU: 45

    # Bloque 2 — Totales
    candidatos_no_registrados = Column(Integer, nullable=True)  # CNR: 0
    votos_nulos = Column(Integer, nullable=True)         # VN: 0
    total_votos = Column(Integer, nullable=True)         # RV: 45
    boletas_procesadas = Column(Integer, nullable=True)
    boletas_revision_humana = Column(Integer, nullable=True)

    # Consistencia
    criterio_1 = Column(Boolean, nullable=True)          # PV + RPPV = SV
    criterio_2 = Column(Boolean, nullable=True)          # SV = BSU
    criterio_3 = Column(Boolean, nullable=True)          # BSU = RV
    criterio_4 = Column(Boolean, nullable=True)          # Σvotos = RV
    acta_consistente = Column(Boolean, nullable=True)
    tipo_error = Column(String, nullable=True)

    # Incidentes
    incidentes_presentes = Column(Boolean, default=False)
    descripcion_incidentes = Column(String, nullable=True)
    hojas_incidentes = Column(Integer, default=0)

    # Integridad
    hash_boletas = Column(String, nullable=True)

    validation_status = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)