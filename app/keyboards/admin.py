from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from app.utils.callbacks.admin import (
    EditBookCallback,
    DeleteBookCallback,
    EditTestCallback,
    DeleteTestCallback,
)


# ==========================
# Asosiy admin panel
# ==========================

def admin_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📚 Kitob boshqaruvi"),
                KeyboardButton(text="📝 Test boshqaruvi"),
            ],
            [
                KeyboardButton(text="📊 Statistika"),
                KeyboardButton(text="👥 Foydalanuvchilar"),
            ],
            [
                KeyboardButton(text="📢 Xabar yuborish"),
            ],
            [
                KeyboardButton(text="⬅️ Orqaga"),
            ],
        ],
        resize_keyboard=True,
    )


# ==========================
# Kitoblar menyusi
# ==========================

def books_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="➕ Kitob qo'shish"),
                KeyboardButton(text="📋 Kitoblar"),
            ],
            [
                KeyboardButton(text="✏️ Kitobni tahrirlash"),
                KeyboardButton(text="🗑 Kitobni o'chirish"),
            ],
            [
                KeyboardButton(text="⬅️ Admin panel"),
            ],
        ],
        resize_keyboard=True,
    )


# ==========================
# Testlar menyusi
# ==========================

def tests_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="➕ Test qo'shish"),
            ],
            [
                KeyboardButton(text="📥 JSON import"),
                KeyboardButton(text="📄 Word import"),
            ],
            [
                KeyboardButton(text="📊 Excel import"),
            ],
            [
                KeyboardButton(text="📋 Testlar"),
            ],
            [
                KeyboardButton(text="⬅️ Admin panel"),
            ],
        ],
        resize_keyboard=True,
    )


# ==========================
# Kitob amallari
# ==========================

def book_actions_keyboard(book_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✏️ Tahrirlash",
                    callback_data=EditBookCallback(id=book_id).pack(),
                ),
                InlineKeyboardButton(
                    text="🗑 O'chirish",
                    callback_data=DeleteBookCallback(id=book_id).pack(),
                ),
            ]
        ]
    )


# ==========================
# Test amallari
# ==========================

def test_actions_keyboard(test_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✏️ Tahrirlash",
                    callback_data=EditTestCallback(id=test_id).pack(),
                ),
                InlineKeyboardButton(
                    text="🗑 O'chirish",
                    callback_data=DeleteTestCallback(id=test_id).pack(),
                ),
            ]
        ]
    )