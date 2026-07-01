import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN

from app.database.db import create_database, close_database

from app.handlers.start import router as start_router
from app.handlers.books import router as books_router
from app.handlers.book import router as book_router
from app.handlers.test import router as test_router
from app.handlers.results import router as results_router
from app.handlers.admin.panel import router as admin_panel_router
from app.handlers.admin.books import router as admin_books_router

async def main():

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    await create_database()

    from aiogram.client.default import DefaultBotProperties
    from aiogram.enums import ParseMode

    bot = Bot(
        BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
        ),
    )

    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(books_router)
    dp.include_router(book_router)
    dp.include_router(test_router)
    dp.include_router(results_router)
    dp.include_router(admin_panel_router)
    dp.include_router(admin_books_router)

    try:
        print("✅ Bot ishga tushdi...")
        await dp.start_polling(bot)

    finally:
        await close_database()


if __name__ == "__main__":
    asyncio.run(main())