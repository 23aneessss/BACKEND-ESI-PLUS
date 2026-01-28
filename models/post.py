from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from typing import Optional

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    content = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)
    #updated_at: Optional[datetime] = None
    # updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
