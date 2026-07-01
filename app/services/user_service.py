from app.database.models import User
from app.repositories.users import UserRepository


class UserService:

    @staticmethod
    async def get_user(
        telegram_id: int,
    ) -> User | None:
        return await UserRepository.get_by_telegram_id(
            telegram_id
        )

    @staticmethod
    async def create_user(
        telegram_id: int,
        full_name: str,
        username: str | None,
    ) -> User:

        return await UserRepository.create(
            telegram_id=telegram_id,
            full_name=full_name,
            username=username,
        )

    @staticmethod
    async def get_or_create_user(
        telegram_id: int,
        full_name: str,
        username: str | None,
    ) -> User:

        return await UserRepository.get_or_create(
            telegram_id=telegram_id,
            full_name=full_name,
            username=username,
        )