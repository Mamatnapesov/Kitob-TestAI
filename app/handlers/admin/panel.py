from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from config import ADMINS
from app.keyboards.admin import admin_menu_keyboard

router = Router()


def is_admin(user_id: int) -> bool:
    return user_id in ADMINS


@router.message(Command("admin"))
async def admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("⛔ Siz admin emassiz.")
        return

    await message.answer(
        "⚙️ Admin panel",
        reply_markup=admin_menu_keyboard()
    )


@router.message(F.text == "⚙️ Admin panel")
async def admin_panel_button(message: Message):
    if not is_admin(message.from_user.id):
        return

    await message.answer(
        "⚙️ Admin panel",
        reply_markup=admin_menu_keyboard()
    )
@router.message(F.text == "⬅️ Admin panel")
async def back_admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        return

    await message.answer(
        "⚙️ Admin panel",
        reply_markup=admin_menu_keyboard()
    )