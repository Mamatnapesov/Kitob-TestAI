from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import ADMINS
from app.states.admin import AddBookState
from app.repositories.books import BookRepository
from app.keyboards.admin import (
    books_menu_keyboard,
    book_actions_keyboard,
)
from aiogram.types import CallbackQuery

from app.utils.callbacks.admin import DeleteBookCallback
router = Router()


def is_admin(user_id: int) -> bool:
    return user_id in ADMINS


# ==========================
# BOOK MENU
# ==========================

@router.message(F.text == "📚 Kitob boshqaruvi")
async def books_menu(message: Message):
    if not is_admin(message.from_user.id):
        return

    await message.answer(
        "📚 Kitob boshqaruvi",
        reply_markup=books_menu_keyboard()
    )


# ==========================
# ADD BOOK
# ==========================

@router.message(F.text == "➕ Kitob qo'shish")
async def add_book(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return

    await state.clear()
    await state.set_state(AddBookState.name)

    await message.answer(
        "📚 Kitob nomini kiriting:"
    )


@router.message(AddBookState.name)
async def get_name(message: Message, state: FSMContext):

    if not message.text:
        return

    await state.update_data(
        name=message.text.strip()
    )

    await state.set_state(AddBookState.author)

    await message.answer(
        "✍️ Muallifni kiriting:"
    )


@router.message(AddBookState.author)
async def get_author(message: Message, state: FSMContext):

    if not message.text:
        return

    await state.update_data(
        author=message.text.strip()
    )

    await state.set_state(AddBookState.description)

    await message.answer(
        "📝 Tavsifni kiriting:"
    )


@router.message(AddBookState.description)
async def get_description(message: Message, state: FSMContext):

    if not message.text:
        return

    await state.update_data(
        description=message.text.strip()
    )

    await state.set_state(AddBookState.cover)

    await message.answer(
        "🖼 Kitob rasmini yuboring.\n\n"
        "Yoki /skip yuboring."
    )


# ==========================
# SKIP COVER
# ==========================

@router.message(Command("skip"), AddBookState.cover)
async def skip_cover(message: Message, state: FSMContext):

    data = await state.get_data()

    await BookRepository.create(
        name=data["name"],
        author=data["author"],
        description=data["description"],
        cover="",
    )

    await state.clear()

    await message.answer(
        "✅ Kitob muvaffaqiyatli qo'shildi.",
        reply_markup=books_menu_keyboard()
    )
@router.message(AddBookState.cover, F.photo)
async def get_cover(message: Message, state: FSMContext):

    data = await state.get_data()

    photo = message.photo[-1].file_id

    await BookRepository.create(
        name=data["name"],
        author=data["author"],
        description=data["description"],
        cover=photo,
    )

    await state.clear()

    await message.answer(
        "✅ Kitob muvaffaqiyatli qo'shildi.",
        reply_markup=books_menu_keyboard(),
    )
@router.message(AddBookState.cover)
async def invalid_cover(message: Message):
    await message.answer(
        "🖼 Iltimos, rasm yuboring yoki /skip yozing."
    )
@router.message(F.text == "📋 Kitoblar")
async def books_list(message: Message):

    if not is_admin(message.from_user.id):
        return

    books = await BookRepository.get_all()

    if not books:
        await message.answer("📚 Hozircha kitoblar mavjud emas.")
        return

    for book in books:

        text = (
            f"📚 <b>{book.name}</b>\n\n"
            f"✍️ Muallif: {book.author}\n\n"
            f"📝 {book.description}"
        )

        if book.cover:
            await message.answer_photo(
                photo=book.cover,
                caption=text,
                reply_markup=book_actions_keyboard(book.id),
            )
        else:
            await message.answer(
                text,
                reply_markup=book_actions_keyboard(book.id),
            )

@router.callback_query(DeleteBookCallback.filter())
async def delete_book(
    callback: CallbackQuery,
    callback_data: DeleteBookCallback,
):
    if not is_admin(callback.from_user.id):
        await callback.answer("Ruxsat yo'q.", show_alert=True)
        return

    success = await BookRepository.deactivate(
        callback_data.id
    )

    if not success:
        await callback.answer(
            "❌ Kitob topilmadi.",
            show_alert=True,
        )
        return

    await callback.message.edit_text(
        "✅ Kitob muvaffaqiyatli o'chirildi."
    )

    await callback.answer()