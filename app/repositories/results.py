from sqlalchemy import desc
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.database.db import SessionLocal
from app.database.models import Result


class ResultRepository:

    @staticmethod
    async def create(
        user_id: int,
        book_id: int,
        total: int,
        correct: int,
        wrong: int,
        percent: float,
        spent_time: int,
    ) -> Result:

        async with SessionLocal() as session:

            try:

                result = Result(
                    user_id=user_id,
                    book_id=book_id,
                    total=total,
                    correct=correct,
                    wrong=wrong,
                    percent=percent,
                    spent_time=spent_time,
                )

                session.add(result)

                await session.commit()

                await session.refresh(result)

                return result

            except SQLAlchemyError:

                await session.rollback()

                raise

    @staticmethod
    async def get_user_results(
        user_id: int,
    ) -> list[Result]:

        async with SessionLocal() as session:

            result = await session.execute(
                select(Result)
                .where(Result.user_id == user_id)
                .order_by(desc(Result.created_at))
            )

            return list(result.scalars().all())

    @staticmethod
    async def get_best_result(
        user_id: int,
    ) -> Result | None:

        async with SessionLocal() as session:

            return await session.scalar(
                select(Result)
                .where(Result.user_id == user_id)
                .order_by(desc(Result.percent))
            )