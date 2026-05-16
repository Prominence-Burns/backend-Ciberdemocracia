import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    nombre = Column(String, nullable=True)
    rol = Column(String, nullable=False)             
    # valores válidos:
    # presidente_de_casilla
    # primer_escrutador
    # segundo_escrutador
    # tercer_escrutador
    # primer_secretario
    # segundo_secretario
    # auditor
    # admin
    casilla_id = Column(String, ForeignKey("casillas.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    password_hash = Column(String, nullable=True)  
    clave_de_elector = Column(String, nullable=True, unique=True)  
