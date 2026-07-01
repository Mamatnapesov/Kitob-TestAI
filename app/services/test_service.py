from app.database.models import Test
from app.repositories.books import BookRepository
from app.repositories.tests import TestRepository


class TestService:

    @staticmethod
    async def create_test(
        book_id: int,
        question: str,
        option_a: str,
        option_b: str,
        option_c: str,
        option_d: str,
        correct: str,
        difficulty: str = "easy",
    ) -> Test:

        book = await BookRepository.get(book_id)

        if not book:
            raise ValueError("Book not found.")

        return await TestRepository.create(
            book_id=book_id,
            question=question,
            option_a=option_a,
            option_b=option_b,
            option_c=option_c,
            option_d=option_d,
            correct=correct,
            difficulty=difficulty,
        )

    @staticmethod
    async def get_test(
        test_id: int,
    ) -> Test | None:

        return await TestRepository.get(test_id)

    @staticmethod
    async def get_tests(
        book_id: int,
    ) -> list[Test]:

        return await TestRepository.get_all(book_id)

    @staticmethod
    async def get_random_tests(
        book_id: int,
        limit: int = 20,
    ) -> list[Test]:

        return await TestRepository.get_random(
            book_id=book_id,
            limit=limit,
        )

    @staticmethod
    async def count_tests(
        book_id: int,
    ) -> int:

        return await TestRepository.count(book_id)

    @staticmethod
    async def check_answer(
        test_id: int,
        answer: str,
    ) -> bool:

        return await TestRepository.check_answer(
            test_id=test_id,
            answer=answer,
        )

    @staticmethod
    async def deactivate_test(
        test_id: int,
    ) -> bool:

        return await TestRepository.deactivate(test_id)