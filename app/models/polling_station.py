import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from app.database import Base

class PollingStation(Base):
    __tablename__ = "polling_stations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    district = Column(String, nullable=False)
    section = Column(String, nullable=False)
    state = Column(String, nullable=False)
    municipality = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)