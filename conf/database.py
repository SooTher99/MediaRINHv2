from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from conf.settings import settings


class Base(DeclarativeBase):
    ...

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session

