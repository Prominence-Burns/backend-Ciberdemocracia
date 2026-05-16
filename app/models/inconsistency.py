import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from app.database import Base

class Inconsistency(Base):
    __tablename__ = "inconsistencies"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    ballot_id = Column(String, ForeignKey("ballots.id"), nullable=False)
    inconsistency_type = Column(String, nullable=False)
    severity = Column(String, nullable=False)      # low, medium, high
    resolved = Column(Boolean, default=False)
    resolution_notes = Column(String, nullable=True)
    resolved_by = Column(String, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)