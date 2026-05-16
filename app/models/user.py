import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)  # funcionario, auditor, admin
    polling_station_id = Column(String, ForeignKey("polling_stations.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)