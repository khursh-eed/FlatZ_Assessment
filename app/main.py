from fastapi import FastAPI,HTTPException,Depends
from app import db, crud, schemas
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

app = FastAPI()

# @app.get("/homepage")
# def homepage():
#     print("Home page it is")
#     return {'message':'Home page it is'}

# print("Working")

@app.on_event("startup")
async def startup():
    #create db
    await db.init_db()

@app.post("/users", response_model=schemas.UserOut)
async def create_user(payload: schemas.UserCreate, session: AsyncSession = Depends(db.get_session)):
    user = await crud.create_user(session, payload)
    return user

@app.get("/users/{user_id}", response_model=schemas.UserOut)
async def get_user(user_id: int, session: AsyncSession = Depends(db.get_session)):
    user = await crud.get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/activity", response_model=schemas.ActivityOut)
async def post_activity(payload: schemas.ActivityCreate, session: AsyncSession = Depends(db.get_session)):
    act = await crud.create_activity(session, payload)
    return act

@app.get("/score/{user_id}", response_model=schemas.ScoreOut)
async def get_score(user_id: int, session: AsyncSession = Depends(db.get_session)):
    rec = await crud.compute_score(session, user_id)
    return rec

@app.get("/leaderboard", response_model=list[schemas.LeaderboardEntry])
async def get_leaderboard(session: AsyncSession = Depends(db.get_session)):
    lb = await crud.top_n_users(session, n=10)
    return lb