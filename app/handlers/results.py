from aiogram import F, Router
from aiogram.types import Message

from app.services.book_service import BookService
from app.services.result_service import ResultService
from app.services.user_service import UserService

router = Router()


@router.message(F.text == "📊 Natijalar")
async def results_handler(message: Message):

    user = await UserService.get_user(
        telegram_id=message.from_user.id,
    )

    if not user:
        await message.answer(
            "📊 Siz hali birorta ham test ishlamagansiz."
        )
        return

    results = await ResultService.get_results(
        user.id
    )

    if not results:
        await message.answer(
            "📊 Siz hali birorta ham test ishlamagansiz."
        )
        return

    best = await ResultService.get_best_result(
        user.id
    )

    average = round(
        sum(result.percent for result in results)
        / len(results),
        1,
    )

    text = (
        "📊 <b>Sizning natijalaringiz</b>\n\n"
        f"📝 Jami ishlangan testlar: <b>{len(results)}</b>\n"
        f"🥇 Eng yaxshi natija: <b>{best.percent}%</b>\n"
        f"📈 O'rtacha natija: <b>{average}%</b>\n\n"
        "<b>Oxirgi 5 ta natija:</b>\n\n"
    )

    for result in results[:5]:

        book = await BookService.get_book(
            result.book_id
        )

        book_name = (
            book.name
            if book
            else "Noma'lum kitob"
        )

        minutes = result.spent_time // 60
        seconds = result.spent_time % 60

        text += (
            f"📚 <b>{book_name}</b>\n"
            f"✅ {result.correct}/{result.total}\n"
            f"📈 {result.percent}%\n"
            f"⏱ {minutes}:{seconds:02d}\n"
            f"📅 {result.created_at.strftime('%d.%m.%Y %H:%M')}\n\n"
        )

    await message.answer(
        text,
        parse_mode="HTML",
    )