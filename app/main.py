from fastapi import FastAPI, Depends, HTTPException
from app import db, crud, schemas
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

app = FastAPI(title="FlatZ resident engagemnt", version ="0.1.0")

@app.on_event("startup")
async def startup():
    # call the create db
    await db.init_db()

@app.post("/activity", response_model=schemas.ActivityOut)
async def post_activity(payload: schemas.ActivityCreate, session: AsyncSession = Depends(db.get_session)):
    obj = await crud.create_activity(session, payload)
    return obj

@app.get("/score/{user_id}", response_model=schemas.ScoreOut)
async def get_score(user_id: int, session: AsyncSession = Depends(db.get_session)):
    rec = await crud.compute_score(session, user_id)
    return {"user_id": rec["user_id"], "score": rec["score"], "last_activity": rec["last_activity"]}

@app.get("/leaderboard", response_model=list[schemas.LeaderboardEntry])
async def get_leaderboard(session: AsyncSession = Depends(db.get_session)):
    lb = await crud.top_n_users(session, n=10)
    return lb




