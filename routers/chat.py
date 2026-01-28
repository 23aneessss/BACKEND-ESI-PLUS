import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv

from database import SessionLocal
from models.convai import Message, Conversation
from schemas.chat import MessageRequest, MessageResponse, MessageOut

api = os.getenv("API_KEY")
genai.configure(api_key="api")
model = genai.GenerativeModel("gemini-1.5-flash")

router = APIRouter(
    prefix="/chat",
    tags=["chatbot"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/conversations", response_model=dict)
def create_conversation(db: db_dependency):
    conversation = Conversation(created_at=datetime.utcnow())
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return {"conversation_id": conversation.id}

@router.post("/message", response_model=MessageResponse)
def chat_with_gemini(input: MessageRequest, db: db_dependency):
    past_messages = db.query(Message).filter(
        Message.conversation_id == input.conversation_id
    ).order_by(Message.timestamp).all()

    history = [
        {"role": msg.sender, "parts": [msg.content]} for msg in past_messages
    ]

    chat = model.start_chat(history=history)

    response = chat.send_message(input.prompt)

    user_msg = Message(
        conversation_id=input.conversation_id,
        sender="user",
        content=input.prompt,
        timestamp=datetime.utcnow()
    )
    db.add(user_msg)

    ai_msg = Message(
        conversation_id=input.conversation_id,
        sender="model",
        content=response.text,
        timestamp=datetime.utcnow()
    )
    db.add(ai_msg)

    db.commit()
    db.refresh(ai_msg)

    return ai_msg

@router.get("/messages/{conversation_id}", response_model=list[MessageOut])
def get_messages(conversation_id: int, db: db_dependency):
    messages = db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.timestamp).all()
    return messages
