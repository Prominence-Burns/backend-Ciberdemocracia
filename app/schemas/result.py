from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ResultCreate(BaseModel):
    polling_station_id: str
    party: str
    vote_count: int = 0
    source: Optional[str] = None  # ai, human, mixed

class ResultOut(BaseModel):
    id: str
    polling_station_id: str
    party: str
    vote_count: int
    source: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}