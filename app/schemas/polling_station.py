from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PollingStationCreate(BaseModel):
    district: str
    section: str
    state: str
    municipality: str

class PollingStationOut(BaseModel):
    id: str
    district: str
    section: str
    state: str
    municipality: str
    created_at: datetime

    model_config = {"from_attributes": True}