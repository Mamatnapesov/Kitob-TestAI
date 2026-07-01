from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from sqlalchemy.orm import DeclarativeBase

from config import DATABASE_URL


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass


engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)


SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Return database session.
    """

    async with SessionLocal() as session:
        yield session


async def create_database() -> None:
    """
    Create all database tables.
    """

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_database() -> None:
    """
    Drop all database tables.
    """

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def close_database() -> None:
    """
    Close database engine.
    """

    await engine.dispose()