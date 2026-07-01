import time

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.keyboards.tests import (
    answer_keyboard,
    finish_keyboard,
)
from app.services.exam_service import ExamService
from app.services.result_service import ResultService
from app.services.user_service import UserService
from app.states.exam import ExamState
from app.utils.callbacks import TestCountCallback
from app.keyboards.books import books_keyboard
from app.services.book_service import BookService

router = Router()


async def show_question(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:

    data = await state.get_data()

    tests = data["tests"]
    current = data["current"]

    test = tests[current]

    text = (
        f"📚 Savol {current + 1}/{len(tests)}\n\n"
        f"{test['question']}\n\n"
        f"🅰 {test['option_a']}\n"
        f"🅱 {test['option_b']}\n"
        f"🇨 {test['option_c']}\n"
        f"🇩 {test['option_d']}"
    )

    await callback.message.edit_text(
        text=text,
        reply_markup=answer_keyboard(),
    )


@router.callback_query(TestCountCallback.filter())
async def start_exam(
    callback: CallbackQuery,
    callback_data: TestCountCallback,
    state: FSMContext,
):

    await callback.answer()

    tests = await ExamService.prepare_exam(
        book_id=callback_data.book_id,
        count=callback_data.count,
    )

    if not tests:
        await callback.message.edit_text(
            "❌ Ushbu kitob uchun testlar topilmadi."
        )
        return

    await state.set_state(
        ExamState.solving
    )

    await state.update_data(
        book_id=callback_data.book_id,
        tests=tests,
        current=0,
        correct=0,
        wrong=0,
        total=len(tests),
        started_at=time.time(),
    )

    await show_question(
        callback,
        state,
    )
@router.callback_query(
    ExamState.solving,
    F.data.startswith("answer:")
)
async def answer_handler(
    callback: CallbackQuery,
    state: FSMContext,
):

    await callback.answer()

    answer = callback.data.split(":")[1].upper()

    data = await state.get_data()

    tests = data["tests"]
    current = data["current"]
    correct = data["correct"]
    wrong = data["wrong"]

    test = tests[current]

    if ExamService.is_correct(
        answer=answer,
        correct=test["correct"],
    ):
        correct += 1
    else:
        wrong += 1

    current += 1

    if current >= len(tests):

        spent_time = int(
            time.time() - data["started_at"]
        )

        percent = ExamService.calculate_percent(
            total=len(tests),
            correct=correct,
        )

        user = await UserService.get_or_create_user(
            telegram_id=callback.from_user.id,
            full_name=callback.from_user.full_name,
            username=callback.from_user.username,
        )

        await ResultService.save_result(
            user_id=user.id,
            book_id=data["book_id"],
            total=len(tests),
            correct=correct,
            wrong=wrong,
            percent=percent,
            spent_time=spent_time,
        )

        minutes = spent_time // 60
        seconds = spent_time % 60

        text = (
            "🎉 <b>Test yakunlandi!</b>\n\n"
            f"📚 Jami savollar: {len(tests)}\n"
            f"✅ To'g'ri: {correct}\n"
            f"❌ Noto'g'ri: {wrong}\n"
            f"📈 Natija: <b>{percent}%</b>\n"
            f"⏱ Vaqt: {minutes:02d}:{seconds:02d}"
        )

        await state.clear()

        await callback.message.edit_text(
            text=text,
            reply_markup=finish_keyboard(
                data["book_id"]
            ),
            parse_mode="HTML",
        )

        return

    await state.update_data(
        current=current,
        correct=correct,
        wrong=wrong,
    )

    await show_question(
        callback,
        state,
    )
@router.callback_query(F.data.startswith("restart:"))
async def restart_exam(
    callback: CallbackQuery,
    state: FSMContext,
):
    await callback.answer()

    book_id = int(callback.data.split(":")[1])

    data = await state.get_data()

    # Avvalgi test sonini saqlab qolamiz
    count = data.get("total", 40)

    tests = await ExamService.prepare_exam(
        book_id=book_id,
        count=count,
    )

    if not tests:
        await callback.message.edit_text(
            "❌ Testlar topilmadi."
        )
        return

    await state.set_state(ExamState.solving)

    await state.update_data(
        book_id=book_id,
        tests=tests,
        current=0,
        correct=0,
        wrong=0,
        total=len(tests),
        started_at=time.time(),
    )

    await show_question(
        callback,
        state,
    )

@router.callback_query(F.data == "books")
async def back_to_books(
    callback: CallbackQuery,
    state: FSMContext,
):
    await callback.answer()

    await state.clear()

    books = await BookService.get_books()

    if not books:
        await callback.message.edit_text(
            "📚 Hozircha kitoblar mavjud emas."
        )
        return

    await callback.message.edit_text(
        text="📚 Kitobni tanlang:",
        reply_markup=await books_keyboard(books),
    )