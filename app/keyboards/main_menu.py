from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📚 Kitoblar"),
                KeyboardButton(text="🤖 AI yordamchi"),
            ],
            [
                KeyboardButton(text="📊 Natijalar"),
                KeyboardButton(text="ℹ️ Ma'lumot"),
            ],
        ],
        resize_keyboard=True,
        input_field_placeholder="Bo'limni tanlang...",
    )