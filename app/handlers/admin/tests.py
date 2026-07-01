from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import ADMINS

from app.states.admin import AddTestState
from app.repositories.books import BookRepository
from app.keyboards.admin import tests_menu_keyboard
from app.repositories.tests import TestRepository
from app.keyboards.admin import test_actions_keyboard
from aiogram.types import CallbackQuery
from app.utils.callbacks.admin import DeleteTestCallback

router = Router()


def is_admin(user_id: int) -> bool:
    return user_id in ADMINS


# ==========================
# TEST MENU
# ==========================

@router.message(F.text == "📝 Test boshqaruvi")
async def tests_menu(message: Message):
    if not is_admin(message.from_user.id):
        return

    await message.answer(
        "📝 Test boshqaruvi",
        reply_markup=tests_menu_keyboard()
    )


# ==========================
# ADD TEST
# ==========================

@router.message(F.text == "➕ Test qo'shish")
async def add_test(message: Message, state: FSMContext):

    if not is_admin(message.from_user.id):
        return

    books = await BookRepository.get_all()

    if not books:
        await message.answer(
            "❌ Avval kitob qo'shing."
        )
        return

    text = "📚 Kitob ID sini kiriting:\n\n"

    for book in books:
        text += f"{book.id}. {book.name}\n"

    await state.clear()
    await state.set_state(AddTestState.book)

    await message.answer(text)


@router.message(AddTestState.book)
async def get_book(message: Message, state: FSMContext):

    if not message.text.isdigit():
        await message.answer("❌ ID kiriting.")
        return

    book = await BookRepository.get(
        int(message.text)
    )

    if not book:
        await message.answer(
            "❌ Kitob topilmadi."
        )
        return

    await state.update_data(
        book=book.id
    )

    await state.set_state(
        AddTestState.question
    )

    await message.answer(
        "❓ Savolni kiriting:"
    )


@router.message(AddTestState.question)
async def get_question(
    message: Message,
    state: FSMContext,
):

    await state.update_data(
        question=message.text.strip()
    )

    await state.set_state(
        AddTestState.option_a
    )

    await message.answer(
        "🇦 A variant:"
    )


@router.message(AddTestState.option_a)
async def get_option_a(
    message: Message,
    state: FSMContext,
):

    await state.update_data(
        option_a=message.text.strip()
    )

    await state.set_state(
        AddTestState.option_b
    )

    await message.answer(
        "🇧 B variant:"
    )
@router.message(AddTestState.option_b)
async def get_option_b(message: Message, state: FSMContext):

    await state.update_data(
        option_b=message.text.strip()
    )

    await state.set_state(AddTestState.option_c)

    await message.answer(
        "🇨 C variant:"
    )
@router.message(AddTestState.option_c)
async def get_option_c(message: Message, state: FSMContext):

    await state.update_data(
        option_c=message.text.strip()
    )

    await state.set_state(AddTestState.option_d)

    await message.answer(
        "🇩 D variant:"
    )

@router.message(AddTestState.option_d)
async def get_option_d(message: Message, state: FSMContext):

    await state.update_data(
        option_d=message.text.strip()
    )

    await state.set_state(AddTestState.correct)

    await message.answer(
        "✅ To'g'ri javobni kiriting (A, B, C yoki D):"
    )

@router.message(AddTestState.correct)
async def get_correct(message: Message, state: FSMContext):

    correct = message.text.strip().upper()

    if correct not in ("A", "B", "C", "D"):
        await message.answer(
            "❌ Faqat A, B, C yoki D kiriting."
        )
        return

    await state.update_data(
        correct=correct
    )

    await state.set_state(AddTestState.difficulty)

    await message.answer(
        "📊 Qiyinlik darajasini kiriting:\n\n"
        "easy\n"
        "medium\n"
        "hard"
    )

@router.message(AddTestState.difficulty)
async def save_test(message: Message, state: FSMContext):

    difficulty = message.text.strip().lower()

    if difficulty not in ("easy", "medium", "hard"):
        difficulty = "easy"

    data = await state.get_data()

    await TestRepository.create(
        book_id=data["book"],
        question=data["question"],
        option_a=data["option_a"],
        option_b=data["option_b"],
        option_c=data["option_c"],
        option_d=data["option_d"],
        correct=data["correct"],
        difficulty=difficulty,
    )

    await state.clear()

    await message.answer(
        "✅ Test muvaffaqiyatli qo'shildi.",
        reply_markup=tests_menu_keyboard(),
    )

@router.message(F.text == "📋 Testlar")
async def tests_list(message: Message):

    if not is_admin(message.from_user.id):
        return

    tests = await TestRepository.get_all_admin()

    if not tests:
        await message.answer("📋 Hozircha testlar mavjud emas.")
        return

    current_book = None

    for test in tests:

        if current_book != test.book_id:
            current_book = test.book_id

            book = await BookRepository.get(test.book_id)

            if book:
                await message.answer(
                    f"📚 <b>{book.name}</b>"
                )

        text = (
            f"🆔 {test.id}\n\n"
            f"❓ {test.question}\n\n"
            f"🇦 {test.option_a}\n"
            f"🇧 {test.option_b}\n"
            f"🇨 {test.option_c}\n"
            f"🇩 {test.option_d}\n\n"
            f"✅ Javob: <b>{test.correct}</b>\n"
            f"📊 Daraja: <b>{test.difficulty}</b>"
        )

        await message.answer(
            text,
            reply_markup=test_actions_keyboard(test.id),
        )

@router.callback_query(DeleteTestCallback.filter())
async def delete_test(
    callback: CallbackQuery,
    callback_data: DeleteTestCallback,
):
    if not is_admin(callback.from_user.id):
        await callback.answer(
            "Ruxsat yo'q.",
            show_alert=True,
        )
        return

    success = await TestRepository.deactivate(
        callback_data.id
    )

    if not success:
        await callback.answer(
            "❌ Test topilmadi.",
            show_alert=True,
        )
        return

    await callback.message.edit_text(
        "✅ Test o'chirildi."
    )

    await callback.answer()