from sqlalchemy.future import select
from sqlalchemy import desc
from app import models, schemas
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

POINTS_PER_ACTIVITY = 10
async def create_user(session: AsyncSession, payload: schemas.UserCreate):
    user = models.User(**payload.dict())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user(session: AsyncSession, user_id: int):
    result = await session.execute(select(models.User).where(models.User.id == user_id))
    return result.scalars().first()

async def create_activity(session: AsyncSession, payload: schemas.ActivityCreate):
    activity = models.Activity(**payload.dict())
    session.add(activity)
    await session.commit()
    await session.refresh(activity)
    return activity


async def get_recent_activities(session: AsyncSession, user_id: int, days: int = 30):
    cutoff = datetime.utcnow() - timedelta(days=days)
    result = await session.execute(
        select(models.Activity)
        .where(models.Activity.user_id == user_id)
        .where(models.Activity.timestamp >= cutoff)
    )
    return result.scalars().all()

async def compute_score(session: AsyncSession, user_id: int):
    activities = await get_recent_activities(session, user_id)
    score = len(activities) * 10  # each activity = 10 points
    last_activity = activities[-1].timestamp if activities else None

    # 10% decay if last activity older than 7 days
    if last_activity and (datetime.utcnow() - last_activity).days > 7:
        score *= 0.9

    return {"user_id": user_id, "score": score, "last_activity": last_activity}


async def top_n_users(session: AsyncSession, n: int = 10):
    result = await session.execute(select(models.User.id))
    users = result.scalars().all()

    scores = []
    for uid in users:
        rec = await compute_score(session, uid)
        scores.append(rec)

    scores.sort(key=lambda x: x["score"], reverse=True)
    return scores[:n]




# conversation helpers for chat (optional)
async def add_conversation_message(db: AsyncSession, user_id: int, role: str, message: str):
    conv = models.Conversation(user_id=user_id, role=role, message=message)
    db.add(conv)
    await db.commit()
    await db.refresh(conv)
    return conv

async def get_conversation_history(db: AsyncSession, user_id: int, limit:int=20):
    q = select(models.Conversation).where(models.Conversation.user_id==user_id).order_by(models.Conversation.created_at.desc()).limit(limit)
    res = await db.execute(q)
    return list(reversed(res.scalars().all()))
