from contextlib import asynccontextmanager
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app.configs import settings
from app.db.models.base import Base

async_engine = create_async_engine(settings.db_uri)
Session = scoped_session(sessionmaker(bind=create_engine(settings.db_uri_sync)))
Async_session = sessionmaker(class_=AsyncSession, bind=async_engine)


@asynccontextmanager
async def create_session(**kwargs: Any) -> AsyncSession:
    async with Async_session(**kwargs) as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def create_db() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await async_engine.dispose()


async def clear_db() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
