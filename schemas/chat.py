from pydantic import BaseModel
from typing import List
from datetime import datetime

class MessageRequest(BaseModel):
    conversation_id: int
    prompt: str

class MessageResponse(BaseModel):
    conversation_id: int
    response: str

class MessageResponse(BaseModel):
    conversation_id: int
    content: str
    timestamp: datetime


class MessageOut(BaseModel):
    id: int
    conversation_id: int
    sender: str
    content: str
    timestamp: datetime

    class Config:
        from_attributes = True  

class ConversationOut(BaseModel):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
