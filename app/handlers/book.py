from aiogram import Router
from aiogram.types import CallbackQuery

from app.services.book_service import BookService
from app.services.test_service import TestService
from app.keyboards.books import test_count_keyboard
from app.utils.callbacks import BookCallback

router = Router()


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
        reply_markup=await test_count_keyboard(book.id),
        parse_mode="HTML",
    )