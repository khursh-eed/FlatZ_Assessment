from pydantic import BaseModel
from typing import Optional, List
import datetime

class ActivityCreate(BaseModel):
    user_id: int
    feature_name: str
    timestamp: Optional[datetime.datetime] = None

class ActivityOut(BaseModel):
    id: int
    user_id: int
    feature_name: str
    timestamp: datetime.datetime
    class Config:
        orm_mode = True

class ScoreOut(BaseModel):
    user_id: int
    score: float
    last_activity: Optional[datetime.datetime] = None

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
