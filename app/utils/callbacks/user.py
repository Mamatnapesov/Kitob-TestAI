from aiogram.filters.callback_data import CallbackData


class BookCallback(CallbackData, prefix="book"):
    id: int


class TestCountCallback(CallbackData, prefix="test_count"):
    book_id: int
    count: int