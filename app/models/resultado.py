import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, JSON
from app.database import Base

class Resultado(Base):
    __tablename__ = "resultados"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    acta_id = Column(String, ForeignKey("actas.id"), nullable=False)
    partido_o_coalicion = Column(String, nullable=False)
    partido_id = Column(String, nullable=False)        # viene como "id" en el JSON
    votos = Column(Integer, default=0)
    es_coalicion = Column(Boolean, default=False)
    partidos_coalicion = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)