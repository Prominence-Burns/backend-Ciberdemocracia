import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey
from app.database import Base

class Ballot(Base):
    __tablename__ = "ballots"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    polling_station_id = Column(String, ForeignKey("polling_stations.id"), nullable=False)
    image_url = Column(String, nullable=False)
    detected_vote = Column(String, nullable=True)
    confidence_score = Column(Float, nullable=True)
    reviewed_by_human = Column(Boolean, default=False)
    final_classification = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)