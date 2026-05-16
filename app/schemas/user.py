from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    role: str  # funcionario, auditor, admin
    polling_station_id: Optional[str] = None

class UserOut(BaseModel):
    id: str
    name: str
    role: str
    polling_station_id: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}