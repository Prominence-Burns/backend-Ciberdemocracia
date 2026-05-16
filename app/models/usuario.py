import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre = Column(String, nullable=False)
    rol = Column(String, nullable=False)             # funcionario, auditor, admin
    casilla_id = Column(String, ForeignKey("casillas.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)