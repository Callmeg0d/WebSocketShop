from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

DATABASE_URL = settings.DATABASE_URL
DATABASE_PARAMS = {}


# Создание асинхронного движка
engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)
# Создание движка (небольших транзакций)
async_session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
