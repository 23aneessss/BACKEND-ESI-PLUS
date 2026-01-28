from pydantic import BaseModel
from datetime import datetime

class TodoCreate(BaseModel):
    title: str
    content: str
    due_date: datetime | None = None

class TodoOut(BaseModel):
    id: int
    title: str
    content: str
    is_done: bool
    due_date: datetime | None
    created_at: datetime

    class Config:
        orm_mode = True