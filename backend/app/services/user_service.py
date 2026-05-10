from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.interfaces.unit_of_work import IUnitOfWork
    from app.schemas.user import UserCreate, UserId
    from app.schemas.user import UserDB as User


class UserService:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def add_user(self, user: UserCreate) -> None:
        await self.uow.users.add_one(user)

    async def get_users(self, limit: int, offset: int) -> list[User]:
        return await self.uow.users.get_many(limit, offset)

    async def get_user(self, user_id: UserId) -> User | None:
        return await self.uow.users.get_by_id(user_id)

    async def remove_user(self, user_id: UserId) -> None:
        await self.uow.users.remove_by_id(user_id)
