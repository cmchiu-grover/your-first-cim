from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NotificationCreate(BaseModel):
    title: str
    message: str
    event_type: str

class NotificationOut(BaseModel):
    id: int
    title: str
    message: str
    event_type: str
    created_at: datetime
    is_read: Optional[bool] = False
