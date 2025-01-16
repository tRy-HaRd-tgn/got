from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from redis.asyncio import Redis
from app.config import settings

DATABASE_URL = settings.DATABASE_URL
DATABASE_PARAMS = {}

engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)


class Base(DeclarativeBase):
    pass
