import asyncio

from app.services.book_service import BookService


BOOKS = [
    ("Shum bola", "G'afur G'ulom"),
    ("Oq kema", "Chingiz Aytmatov"),
    ("Jamila", "Chingiz Aytmatov"),
    ("Sudxo'rning o'limi", "Sadriddin Ayniy"),
    ("Mumu", "Ivan Turgenev"),
    ("Alkimyogar", "Paulo Coelho"),
    ("Sariq devni minib", "Xudoyberdi To'xtaboyev"),
    ("Robinzon Kruzo", "Daniel Defo"),
    ("Bolalik", "Oybek"),
    ("Qobusnoma", "Kaykovus"),
    ("Boy ota va kambag'al ota", "Robert Kiyosaki"),
    ("Do'stlar orttirish va odamlarga ta'sir o'tkazish xususida", "Dale Carnegie"),
]


async def main():

    for name, author in BOOKS:

        await BookService.create_book(
            name=name,
            author=author,
        )

    print("✅ Kitoblar bazaga qo'shildi.")


if __name__ == "__main__":
    asyncio.run(main())