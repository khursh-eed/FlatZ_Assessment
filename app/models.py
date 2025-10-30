from sqlalchemy import Column, Integer, String, DateTime, func, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression
from app.db import Base
import datetime

class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    feature_name = Column(String, index=True)
    timestamp = Column(DateTime, default=func.now(), index=True)

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    role = Column(String)  
    message = Column(Text)
    created_at = Column(DateTime, default=func.now())
