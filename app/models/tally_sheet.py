import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON
from app.database import Base

class TallySheet(Base):
    __tablename__ = "tally_sheets"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    polling_station_id = Column(String, ForeignKey("polling_stations.id"), nullable=False)
    image_url = Column(String, nullable=False)
    extracted_text = Column(JSON, nullable=True)       # JSONB en PostgreSQL, JSON en SQLite
    validation_status = Column(String, nullable=True)
    total_votes = Column(Integer, nullable=True)
    null_votes = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)