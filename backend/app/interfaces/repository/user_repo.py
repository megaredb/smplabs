from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.user import UserCreate, UserDB, UserId


class IUserRepository(ABC):
    @abstractmethod
    async def add_one(self, data: UserCreate) -> None:
        """Add new user.

        :raises ValueError: If user with this email already exists
        :param data: UserCreate
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, user_id: UserId) -> UserDB | None:
        raise NotImplementedError

    @abstractmethod
    async def get_many(self, limit: int, offset: int) -> list[UserDB]:
        raise NotImplementedError

    @abstractmethod
    async def remove_by_id(self, user_id: UserId) -> None:
        raise NotImplementedError
