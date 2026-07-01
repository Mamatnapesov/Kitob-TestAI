from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.filters.admin import AdminFilter
from app.keyboards.admin import (
    admin_keyboard,
    books_admin_keyboard,
    tests_admin_keyboard,
)
from app.services.book_service import BookService
from app.states.admin import AddBookState
from aiogram.types import CallbackQuery
from app.utils.callbacks import DeleteBookCallback
router = Router()


@router.message(
    Command("admin"),
    AdminFilter(),
)
async def admin_panel(
    message: Message,
):
    await message.answer(
        "⚙️ <b>Admin panel</b>\n\nKerakli bo'limni tanlang.",
        reply_markup=admin_keyboard(),
        parse_mode="HTML",
    )


@router.message(
    AdminFilter(),
    F.text == "📚 Kitob boshqaruvi",
)
async def books_menu(
    message: Message,
):
    await message.answer(
        "📚 <b>Kitob boshqaruvi</b>\n\nKerakli amalni tanlang.",
        reply_markup=books_admin_keyboard(),
        parse_mode="HTML",
    )


@router.message(
    AdminFilter(),
    F.text == "📝 Test boshqaruvi",
)
async def tests_menu(
    message: Message,
):
    await message.answer(
        "📝 <b>Test boshqaruvi</b>\n\nKerakli amalni tanlang.",
        reply_markup=tests_admin_keyboard(),
        parse_mode="HTML",
    )


@router.message(
    AdminFilter(),
    F.text == "⬅️ Admin panel",
)
async def back_admin(
    message: Message,
):
    await message.answer(
        "⚙️ <b>Admin panel</b>",
        reply_markup=admin_keyboard(),
        parse_mode="HTML",
    )


@router.message(
    AdminFilter(),
    F.text == "➕ Kitob qo'shish",
)
async def add_book_start(
    message: Message,
    state: FSMContext,
):
    await state.clear()

    await state.set_state(
        AddBookState.name,
    )

    await message.answer(
        "📚 Kitob nomini yuboring."
    )
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def skip_cover_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="⏭ O'tkazib yuborish",
                )
            ]
        ],
        resize_keyboard=True,
    )


@router.message(
    AdminFilter(),
    AddBookState.name,
)
async def add_book_name(
    message: Message,
    state: FSMContext,
):
    await state.update_data(
        name=message.text.strip(),
    )

    await state.set_state(
        AddBookState.author,
    )

    await message.answer(
        "✍️ Muallifni kiriting."
    )


@router.message(
    AdminFilter(),
    AddBookState.author,
)
async def add_book_author(
    message: Message,
    state: FSMContext,
):
    await state.update_data(
        author=message.text.strip(),
    )

    await state.set_state(
        AddBookState.cover,
    )

    await message.answer(
        "🖼 Muqova rasmini yuboring.\n\nYoki pastdagi tugmani bosing.",
        reply_markup=skip_cover_keyboard(),
    )


@router.message(
    AdminFilter(),
    AddBookState.cover,
    F.text == "⏭ O'tkazib yuborish",
)
async def add_book_without_cover(
    message: Message,
    state: FSMContext,
):
    data = await state.get_data()

    await BookService.create_book(
        name=data["name"],
        author=data["author"],
        cover="",
    )

    await state.clear()

    await message.answer(
        "✅ Kitob muvaffaqiyatli qo'shildi.",
        reply_markup=books_admin_keyboard(),
    )


@router.message(
    AdminFilter(),
    AddBookState.cover,
    F.photo,
)
async def add_book_with_cover(
    message: Message,
    state: FSMContext,
):
    data = await state.get_data()

    photo = message.photo[-1].file_id

    await BookService.create_book(
        name=data["name"],
        author=data["author"],
        cover=photo,
    )

    await state.clear()

    await message.answer(
        "✅ Kitob muvaffaqiyatli qo'shildi.",
        reply_markup=books_admin_keyboard(),
    )


@router.message(
    AdminFilter(),
    AddBookState.cover,
)
async def invalid_cover(
    message: Message,
):
    await message.answer(
        "❌ Muqova rasmini yuboring yoki \"⏭ O'tkazib yuborish\" tugmasini bosing."
    )
@router.callback_query(DeleteBookCallback.filter())
async def delete_book(
    callback: CallbackQuery,
    callback_data: DeleteBookCallback,
):
    await callback.answer()

    success = await BookService.deactivate_book(
        callback_data.id,
    )

    if success:
        await callback.message.edit_text(
            "✅ Kitob muvaffaqiyatli o'chirildi."
        )
    else:
        await callback.message.edit_text(
            "❌ Kitob topilmadi."
        )
