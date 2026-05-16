import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey
from app.database import Base

class Boleta(Base):
    __tablename__ = "boletas"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    casilla_id = Column(String, ForeignKey("casillas.id"), nullable=False)
    image_url = Column(String, nullable=False)
    voto_detectado = Column(String, nullable=True)        # SHH, PAN, NULO...
    confianza_ia = Column(Float, nullable=True)           # 0.0 - 1.0
    revision_humana = Column(Boolean, default=False)
    clasificacion_final = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)