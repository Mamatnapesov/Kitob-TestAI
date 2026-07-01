import asyncio
import json
from pathlib import Path

from app.services.book_service import BookService
from app.services.test_service import TestService

TESTS_DIR = Path("data/tests")


async def main():

    books = await BookService.get_books()

    books_map = {
        book.name.lower(): book
        for book in books
    }

    for file in TESTS_DIR.glob("*.json"):

        book_name = file.stem.replace("_", " ").lower()

        book = books_map.get(book_name)

        if not book:
            print(f"❌ Kitob topilmadi: {book_name}")
            continue

        with open(file, "r", encoding="utf-8") as f:
            tests = json.load(f)

        added = 0

        for test in tests:

            await TestService.create_test(
                book_id=book.id,
                question=test["question"],
                option_a=test["option_a"],
                option_b=test["option_b"],
                option_c=test["option_c"],
                option_d=test["option_d"],
                correct=test["correct"],
                difficulty=test.get("difficulty", "easy"),
            )

            added += 1

        print(f"✅ {book.name}: {added} ta test qo'shildi.")

    print("\n🎉 Barcha testlar bazaga yuklandi.")


if __name__ == "__main__":
    asyncio.run(main())