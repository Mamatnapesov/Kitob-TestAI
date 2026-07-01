from app.database.models import Result
from app.repositories.results import ResultRepository


class ResultService:

    @staticmethod
    async def save_result(
        user_id: int,
        book_id: int,
        total: int,
        correct: int,
        wrong: int,
        percent: float,
        spent_time: int,
    ) -> Result:

        return await ResultRepository.create(
            user_id=user_id,
            book_id=book_id,
            total=total,
            correct=correct,
            wrong=wrong,
            percent=percent,
            spent_time=spent_time,
        )

    @staticmethod
    async def get_results(
        user_id: int,
    ) -> list[Result]:

        return await ResultRepository.get_user_results(
            user_id
        )

    @staticmethod
    async def get_best_result(
        user_id: int,
    ) -> Result | None:

        return await ResultRepository.get_best_result(
            user_id
        )