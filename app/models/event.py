import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON
from app.database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    entity_type = Column(String, nullable=False)   # ballot, tally_sheet, result...
    entity_id = Column(String, nullable=False)
    event_type = Column(String, nullable=False)    # ballot_scanned, vote_detected...
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    details = Column(JSON, nullable=True)
    hash = Column(String, nullable=True)