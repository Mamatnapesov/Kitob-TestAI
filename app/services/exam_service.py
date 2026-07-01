import random

from app.database.models import Test
from app.services.test_service import TestService


class ExamService:

    @staticmethod
    async def prepare_exam(
        book_id: int,
        count: int,
    ) -> list[dict]:

        tests = await TestService.get_tests(book_id)

        if not tests:
            return []

        if count == 0 or count >= len(tests):
            selected = tests.copy()
            random.shuffle(selected)
        else:
            selected = random.sample(
                tests,
                count,
            )

        return [
            {
                "id": test.id,
                "question": test.question,
                "option_a": test.option_a,
                "option_b": test.option_b,
                "option_c": test.option_c,
                "option_d": test.option_d,
                "correct": test.correct,
            }
            for test in selected
        ]

    @staticmethod
    def calculate_percent(
        total: int,
        correct: int,
    ) -> float:

        if total == 0:
            return 0.0

        return round(
            correct * 100 / total,
            1,
        )

    @staticmethod
    def is_correct(
        answer: str,
        correct: str,
    ) -> bool:

        return (
            answer.upper()
            ==
            correct.upper()
        )