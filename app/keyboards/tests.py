from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def finish_keyboard(book_id: int):

    builder = InlineKeyboardBuilder()

    builder.button(
        text="🔄 Qayta ishlash",
        callback_data=f"restart:{book_id}"
    )

    builder.button(
        text="📚 Kitoblar",
        callback_data="books"
    )

    builder.adjust(1)

    return builder.as_markup()
def answer_keyboard():

    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text="🅰️ A",
            callback_data="answer:A"
        ),
        InlineKeyboardButton(
            text="🅱️ B",
            callback_data="answer:B"
        ),
    )

    builder.row(
        InlineKeyboardButton(
            text="🇨 C",
            callback_data="answer:C"
        ),
        InlineKeyboardButton(
            text="🇩 D",
            callback_data="answer:D"
        ),
    )

    return builder.as_markup()
