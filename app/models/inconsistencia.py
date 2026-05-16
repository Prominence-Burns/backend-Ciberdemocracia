import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from app.database import Base

class Inconsistencia(Base):
    __tablename__ = "inconsistencias"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    boleta_id = Column(String, ForeignKey("boletas.id"), nullable=False)
    tipo_inconsistencia = Column(String, nullable=False)
    severidad = Column(String, nullable=False)       # baja, media, alta
    resuelta = Column(Boolean, default=False)
    notas_resolucion = Column(String, nullable=True)
    resuelta_por = Column(String, ForeignKey("usuarios.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)