from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class TallySheetCreate(BaseModel):
    polling_station_id: str
    image_url: str
    extracted_text: Optional[Any] = None
    validation_status: Optional[str] = None
    total_votes: Optional[int] = None
    null_votes: Optional[int] = None

class TallySheetOut(BaseModel):
    id: str
    polling_station_id: str
    image_url: str
    extracted_text: Optional[Any]
    validation_status: Optional[str]
    total_votes: Optional[int]
    null_votes: Optional[int]
    created_at: datetime

    model_config = {"from_attributes": True}