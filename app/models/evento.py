import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON
from app.database import Base

class Evento(Base):
    __tablename__ = "eventos"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    entidad_tipo = Column(String, nullable=False)   # boleta, acta, resultado...
    entidad_id = Column(String, nullable=False)
    tipo_evento = Column(String, nullable=False)    # boleta_escaneada, voto_detectado...
    usuario_id = Column(String, ForeignKey("usuarios.id"), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    detalles = Column(JSON, nullable=True)
    hash = Column(String, nullable=True)