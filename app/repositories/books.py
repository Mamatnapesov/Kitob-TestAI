from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.database.db import SessionLocal
from app.database.models import Book


class BookRepository:

    @staticmethod
    async def create(
        name: str,
        author: str,
        description: str,
        cover: str = "",
    ) -> Book:

        async with SessionLocal() as session:
            try:
                exists = await session.scalar(
                    select(Book).where(Book.name == name)
                )

                if exists:
                    return exists

                book = Book(
                    name=name,
                    author=author,
                    description=description,
                    cover=cover,
                )

                session.add(book)

                await session.commit()
                await session.refresh(book)

                return book

            except SQLAlchemyError:
                await session.rollback()
                raise

    @staticmethod
    async def get(book_id: int) -> Book | None:

        async with SessionLocal() as session:
            return await session.scalar(
                select(Book).where(
                    Book.id == book_id,
                    Book.is_active.is_(True)
                )
            )

    @staticmethod
    async def get_all() -> list[Book]:

        async with SessionLocal() as session:
            result = await session.execute(
                select(Book)
                .where(Book.is_active.is_(True))
                .order_by(Book.id)
            )

            return list(result.scalars().all())

    @staticmethod
    async def update(
        book_id: int,
        name: str,
        author: str,
        description: str,
    ) -> bool:

        async with SessionLocal() as session:
            try:
                book = await session.get(Book, book_id)

                if not book:
                    return False

                book.name = name
                book.author = author
                book.description = description

                await session.commit()

                return True

            except SQLAlchemyError:
                await session.rollback()
                raise

    @staticmethod
    async def update_cover(
        book_id: int,
        cover: str,
    ) -> bool:

        async with SessionLocal() as session:
            try:
                book = await session.get(Book, book_id)

                if not book:
                    return False

                book.cover = cover

                await session.commit()

                return True

            except SQLAlchemyError:
                await session.rollback()
                raise

    @staticmethod
    async def deactivate(book_id: int) -> bool:

        async with SessionLocal() as session:
            try:
                book = await session.get(Book, book_id)

                if not book:
                    return False

                book.is_active = False

                await session.commit()

                return True

            except SQLAlchemyError:
                await session.rollback()
                raise

    @staticmethod
    async def update(
            book_id: int,
            name: str,
            author: str,
            description: str,
    ) -> bool:

        async with SessionLocal() as session:
            try:

                book = await session.get(Book, book_id)

                if not book:
                    return False

                book.name = name
                book.author = author
                book.description = description

                await session.commit()

                return True

            except SQLAlchemyError:
                await session.rollback()
                raise