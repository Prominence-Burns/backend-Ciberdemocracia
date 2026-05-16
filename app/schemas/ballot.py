from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BallotCreate(BaseModel):
    polling_station_id: str
    image_url: str
    detected_vote: Optional[str] = None
    confidence_score: Optional[float] = None
    reviewed_by_human: bool = False
    final_classification: Optional[str] = None

class BallotOut(BaseModel):
    id: str
    polling_station_id: str
    image_url: str
    detected_vote: Optional[str]
    confidence_score: Optional[float]
    reviewed_by_human: bool
    final_classification: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}