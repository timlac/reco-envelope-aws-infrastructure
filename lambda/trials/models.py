from typing import Dict, Any, Optional
from pydantic import BaseModel
import datetime
from zoneinfo import ZoneInfo


class TrialItemModel(BaseModel):
    retrieved: int
    retrieved_at: Optional[str] = None
    participant_id: Optional[str] = None
    administrator_id: Optional[str] = None
    data: Dict[str, Any] = {}


class TrialModel(BaseModel):
    trial_id: str
    created_at: str
    trial_items: list[TrialItemModel]

    def __init__(self, **data):
        if 'created_at' not in data:
            data['created_at'] = str(datetime.datetime.now(ZoneInfo("Europe/Berlin")).isoformat())
        super().__init__(**data)
