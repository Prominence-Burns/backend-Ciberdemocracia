import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from app.database import Base

class Result(Base):
    __tablename__ = "results"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    polling_station_id = Column(String, ForeignKey("polling_stations.id"), nullable=False)
    party = Column(String, nullable=False)
    vote_count = Column(Integer, default=0)
    source = Column(String, nullable=True)         # ai, human, mixed
    created_at = Column(DateTime, default=datetime.utcnow)