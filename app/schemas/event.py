from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class EventCreate(BaseModel):
    entity_type: str
    entity_id: str
    event_type: str  # ballot_scanned, vote_detected, inconsistency_detected...
    user_id: Optional[str] = None
    details: Optional[Any] = None
    hash: Optional[str] = None

class EventOut(BaseModel):
    id: str
    entity_type: str
    entity_id: str
    event_type: str
    user_id: Optional[str]
    timestamp: datetime
    details: Optional[Any]
    hash: Optional[str]

    model_config = {"from_attributes": True}