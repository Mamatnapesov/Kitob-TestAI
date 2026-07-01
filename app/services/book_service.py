from app.database.models import Book
from app.repositories.books import BookRepository


class BookService:

    @staticmethod
    async def create_book(
        name: str,
        author: str,
        cover: str = "",
    ) -> Book:
        return await BookRepository.create(
            name=name,
            author=author,
            cover=cover,
        )

    @staticmethod
    async def get_book(book_id: int) -> Book | None:
        return await BookRepository.get(book_id)

    @staticmethod
    async def get_books() -> list[Book]:
        return await BookRepository.get_all()

    @staticmethod
    async def deactivate_book(book_id: int) -> bool:
        return await BookRepository.deactivate(book_id)

    @staticmethod
    async def update_cover(
        book_id: int,
        cover: str,
    ) -> bool:
        return await BookRepository.update_cover(
            book_id=book_id,
            cover=cover,
        )