from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.database.db import SessionLocal
from app.database.models import User


class UserRepository:

    @staticmethod
    async def get_by_telegram_id(
        telegram_id: int,
    ) -> User | None:

        async with SessionLocal() as session:

            return await session.scalar(
                select(User).where(
                    User.telegram_id == telegram_id
                )
            )

    @staticmethod
    async def create(
        telegram_id: int,
        full_name: str,
        username: str | None,
    ) -> User:

        async with SessionLocal() as session:

            try:

                user = User(
                    telegram_id=telegram_id,
                    full_name=full_name,
                    username=username,
                )

                session.add(user)

                await session.commit()

                await session.refresh(user)

                return user

            except SQLAlchemyError:

                await session.rollback()

                raise

    @staticmethod
    async def get_or_create(
        telegram_id: int,
        full_name: str,
        username: str | None,
    ) -> User:

        user = await UserRepository.get_by_telegram_id(
            telegram_id
        )

        if user:
            return user

        return await UserRepository.create(
            telegram_id,
            full_name,
            username,
        )