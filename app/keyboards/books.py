from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.models import Book
from app.utils.callbacks import BookCallback
from app.utils.callbacks import TestCountCallback


async def books_keyboard(
    books: list[Book],
):
    builder = InlineKeyboardBuilder()

    for book in books:
        builder.button(
            text=book.name,
            callback_data=BookCallback(
                id=book.id,
            ),
        )

    builder.adjust(1)

    return builder.as_markup()


async def test_count_keyboard(
    book_id: int,
):
    builder = InlineKeyboardBuilder()

    builder.button(
        text="20 ta",
        callback_data=TestCountCallback(
            book_id=book_id,
            count=20,
        ),
    )

    builder.button(
        text="40 ta",
        callback_data=TestCountCallback(
            book_id=book_id,
            count=40,
        ),
    )

    builder.button(
        text="60 ta",
        callback_data=TestCountCallback(
            book_id=book_id,
            count=60,
        ),
    )

    builder.button(
        text="80 ta",
        callback_data=TestCountCallback(
            book_id=book_id,
            count=80,
        ),
    )

    builder.button(
        text="📚 Hammasi",
        callback_data=TestCountCallback(
            book_id=book_id,
            count=0,
        ),
    )

    builder.button(
        text="⬅️ Orqaga",
        callback_data="books",
    )

    builder.adjust(2, 2, 1, 1)

    return builder.as_markup()