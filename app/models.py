from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship
from app.db import Base


def utc_now():
    """Return timezone-aware UTC datetime (for defaults)."""
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    flat_no = Column(String, nullable=False)
    block = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    joined_date = Column(DateTime(timezone=True), default=utc_now)

    activities = relationship("Activity", back_populates="user")


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    feature_name = Column(String, nullable=False)
    activity_type = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), default=utc_now)

    user = relationship("User", back_populates="activities")


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    role = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
