# connecting to db and managing sessions

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# will set this later on
DATABASE_URL = ""

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
# (make echo true to run sql in console)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


Base = declarative_base()
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session

@app.post("/users")
async def create_user(user: UserSchema, session: AsyncSession = Depends(get_session)):
    session.add(User(**user.dict()))
    await session.commit()

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_db())

