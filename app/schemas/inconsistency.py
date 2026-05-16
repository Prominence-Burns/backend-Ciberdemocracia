from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class InconsistencyCreate(BaseModel):
    ballot_id: str
    inconsistency_type: str
    severity: str  # low, medium, high
    resolved: bool = False
    resolution_notes: Optional[str] = None
    resolved_by: Optional[str] = None

class InconsistencyOut(BaseModel):
    id: str
    ballot_id: str
    inconsistency_type: str
    severity: str
    resolved: bool
    resolution_notes: Optional[str]
    resolved_by: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}