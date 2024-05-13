from typing import Dict, Any, Optional
from pydantic import BaseModel
import datetime
from zoneinfo import ZoneInfo


class GroupListItemModel(BaseModel):
    retrieved: int
    retrieved_at: Optional[str] = None
    data: Dict[str, Any] = {}


class GroupListModel(BaseModel):
    group_list_id: str
    created_at: str
    group_list_items: list[GroupListItemModel]

    def __init__(self, **data):
        if 'created_at' not in data:
            data['created_at'] = str(datetime.datetime.now(ZoneInfo("Europe/Berlin")).isoformat())
        super().__init__(**data)
