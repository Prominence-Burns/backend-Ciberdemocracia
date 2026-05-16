import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from app.database import Base

class Casilla(Base):
    __tablename__ = "casillas"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    casilla_id = Column(String, nullable=False, unique=True)  # DEMO-001-001-B
    entidad_federativa = Column(String, nullable=False)
    municipio_o_delegacion = Column(String, nullable=False)
    distrito = Column(String, nullable=False)
    seccion = Column(String, nullable=False)
    tipo_casilla = Column(String, nullable=False)             # basica, contigua...
    tipo_eleccion = Column(String, nullable=False)            # diputacion_mr...
    proceso_electoral = Column(String, nullable=False)        # 2023-2024
    created_at = Column(DateTime, default=datetime.utcnow)