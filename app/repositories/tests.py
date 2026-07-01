from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError

from app.database.db import SessionLocal
from app.database.models import Test


class TestRepository:

    @staticmethod
    async def create(
        book_id: int,
        question: str,
        option_a: str,
        option_b: str,
        option_c: str,
        option_d: str,
        correct: str,
        difficulty: str = "easy",
    ) -> Test:

        async with SessionLocal() as session:
            try:
                test = Test(
                    book_id=book_id,
                    question=question,
                    option_a=option_a,
                    option_b=option_b,
                    option_c=option_c,
                    option_d=option_d,
                    correct=correct.upper(),
                    difficulty=difficulty,
                )

                session.add(test)

                await session.commit()
                await session.refresh(test)

                return test

            except SQLAlchemyError:
                await session.rollback()
                raise

    @staticmethod
    async def get(test_id: int) -> Test | None:

        async with SessionLocal() as session:

            return await session.scalar(
                select(Test).where(
                    Test.id == test_id,
                    Test.is_active.is_(True),
                )
            )

    @staticmethod
    async def get_all(book_id: int) -> list[Test]:

        async with SessionLocal() as session:

            result = await session.execute(
                select(Test)
                .where(
                    Test.book_id == book_id,
                    Test.is_active.is_(True),
                )
                .order_by(Test.id)
            )

            return list(result.scalars().all())

    @staticmethod
    async def get_random(
        book_id: int,
        limit: int,
    ) -> list[Test]:

        async with SessionLocal() as session:

            result = await session.execute(
                select(Test)
                .where(
                    Test.book_id == book_id,
                    Test.is_active.is_(True),
                )
                .order_by(func.random())
                .limit(limit)
            )

            return list(result.scalars().all())

    @staticmethod
    async def count(book_id: int) -> int:

        async with SessionLocal() as session:

            result = await session.scalar(
                select(func.count(Test.id)).where(
                    Test.book_id == book_id,
                    Test.is_active.is_(True),
                )
            )

            return result or 0

    @staticmethod
    async def update(
        test_id: int,
        **kwargs,
    ) -> bool:

        async with SessionLocal() as session:
            try:

                test = await session.get(Test, test_id)

                if not test:
                    return False

                for key, value in kwargs.items():
                    if hasattr(test, key):
                        setattr(test, key, value)

                await session.commit()

                return True

            except SQLAlchemyError:
                await session.rollback()
                raise

    @staticmethod
    async def deactivate(
        test_id: int,
    ) -> bool:

        async with SessionLocal() as session:
            try:

                test = await session.get(Test, test_id)

                if not test:
                    return False

                test.is_active = False

                await session.commit()

                return True

            except SQLAlchemyError:
                await session.rollback()
                raise

    @staticmethod
    async def delete(
        test_id: int,
    ) -> bool:

        async with SessionLocal() as session:
            try:

                test = await session.get(Test, test_id)

                if not test:
                    return False

                await session.delete(test)

                await session.commit()

                return True

            except SQLAlchemyError:
                await session.rollback()
                raise
@staticmethod
async def get_all_admin() -> list[Test]:

    async with SessionLocal() as session:

        result = await session.execute(
            select(Test)
            .where(Test.is_active.is_(True))
            .order_by(Test.book_id, Test.id)
        )

        return list(result.scalars().all())