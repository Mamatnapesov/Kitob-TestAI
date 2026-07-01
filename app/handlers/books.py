from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from app.keyboards.books import (
    books_keyboard,
    test_count_keyboard,
)
from app.services.book_service import BookService
from app.services.test_service import TestService
from app.utils.callbacks import BookCallback

router = Router()


@router.message(F.text == "📚 Kitoblar")
async def books_handler(message: Message):

    books = await BookService.get_books()

    if not books:
        await message.answer(
            "📚 Hozircha kitoblar mavjud emas."
        )
        return

    await message.answer(
        text="📚 Kitobni tanlang:",
        reply_markup=await books_keyboard(books),
    )


@router.callback_query(BookCallback.filter())
async def book_handler(
    callback: CallbackQuery,
    callback_data: BookCallback,
):

    await callback.answer()

    book = await BookService.get_book(
        callback_data.id
    )

    if not book:
        await callback.message.edit_text(
            "❌ Kitob topilmadi."
        )
        return

    tests_count = await TestService.count_tests(
        book.id
    )

    text = (
        f"📖 <b>{book.name}</b>\n\n"
        f"✍️ Muallif: {book.author}\n"
        f"📝 Testlar soni: {tests_count}\n\n"
        "📊 Nechta test ishlamoqchisiz?"
    )

    await callback.message.edit_text(
        text=text,
        reply_markup=await test_count_keyboard(
            book.id
        ),
        parse_mode="HTML",
    )