from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    name: str
    flat_no: str
    block: str
    email: str


class UserCreate(UserBase):
    joined_date: datetime


class UserOut(UserBase):
    id: int
    joined_date: datetime

    class Config:
        orm_mode = True



class ActivityBase(BaseModel):
    user_id: int
    feature_name: str
    activity_type: str


class ActivityCreate(ActivityBase):
    timestamp: Optional[datetime] = None


class ActivityOut(ActivityBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True

class ScoreOut(BaseModel):
    user_id: int
    score: float
    last_activity: Optional[datetime] = None

class LeaderboardEntry(BaseModel):
    user_id: int
    score: float

class InsightOut(BaseModel):
    user_id: int
    insight: str

class ChatRequest(BaseModel):
    user_id: int
    message: str
    conversation_id: Optional[int] = None
