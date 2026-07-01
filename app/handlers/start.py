from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.keyboards.main_menu import main_menu_keyboard

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):

    text = (
        f"Assalomu alaykum, {message.from_user.full_name}! 👋\n\n"
        "Kitob-Test AI botiga xush kelibsiz.\n\n"
        "Kerakli bo'limni tanlang."
    )

    await message.answer(
        text=text,
        reply_markup=main_menu_keyboard(),
    )