from sqlalchemy.future import select
from sqlalchemy import desc
from app import models, schemas
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

POINTS_PER_ACTIVITY = 10

async def create_activity(db: AsyncSession, activity: schemas.ActivityCreate):
    obj = models.Activity(
        user_id=activity.user_id,
        feature_name=activity.feature_name,
        timestamp=activity.timestamp or datetime.utcnow()
    )
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

async def get_recent_activities(db: AsyncSession, user_id: int, days: int = 30):
    cutoff = datetime.utcnow() - timedelta(days=days)
    q = select(models.Activity).where(models.Activity.user_id == user_id).where(models.Activity.timestamp >= cutoff).order_by(models.Activity.timestamp.desc())
    res = await db.execute(q)
    return res.scalars().all()

async def get_all_activities(db: AsyncSession, user_id: int):
    q = select(models.Activity).where(models.Activity.user_id == user_id).order_by(models.Activity.timestamp.desc())
    res = await db.execute(q)
    return res.scalars().all()

async def get_last_activity(db: AsyncSession, user_id: int):
    q = select(models.Activity).where(models.Activity.user_id == user_id).order_by(models.Activity.timestamp.desc()).limit(1)
    res = await db.execute(q)
    return res.scalars().first()

async def compute_score(db: AsyncSession, user_id: int):

    # get all activites and count their points (10 per ac)
    activities = await get_all_activities(db, user_id)
    total = len(activities) * POINTS_PER_ACTIVITY
    
    last = await get_last_activity(db, user_id)
    last_ts = last.timestamp if last else None

    # apply decay if inactive > 7 days
    decay_applied = False
    if last_ts:
        from datetime import datetime, timedelta
        if datetime.utcnow() - last_ts > timedelta(days=7):
            total = total * 0.9  # 10% decay
            decay_applied = True

    return {
        "user_id": user_id,
        "score": float(total),
        "last_activity": last_ts,
        "decay_applied": decay_applied
    }

async def top_n_users(db: AsyncSession, n: int = 10):
    #  compute scores for all distinct user_ids, then sort
    q = select(models.Activity.user_id).distinct()
    res = await db.execute(q)
    user_ids = [r for (r,) in res.all()]

    leaderboard = []
    for uid in user_ids:
        rec = await compute_score(db, uid)
        leaderboard.append({"user_id": uid, "score": rec["score"]})
    leaderboard.sort(key=lambda x: x["score"], reverse=True)
    return leaderboard[:n]

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
