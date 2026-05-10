from typing import TYPE_CHECKING

import aiosqlite

from app.interfaces.repository.user_repo import IUserRepository
from app.schemas.user import UserDB as UserSchema
from app.schemas.user import UserId

if TYPE_CHECKING:
    from app.schemas.user import UserCreate


class UserRepository(IUserRepository):
    def __init__(self, connection: aiosqlite.Connection) -> None:
        self.connection = connection

    async def add_one(self, data: UserCreate) -> None:
        query = """
            INSERT INTO users (name, email, password_hash, role)
            VALUES (?, ?, ?, ?)
        """
        try:
            await self.connection.execute(
                query, (data.name, data.email, data.password, data.role)
            )
        except aiosqlite.IntegrityError as exc:
            msg = "User with this email already exists"
            raise ValueError(msg) from exc

    async def get_by_id(self, user_id: UserId) -> UserSchema | None:
        query = """
            SELECT id, name, email, password_hash, role, created_at
            FROM users
            WHERE id = ?
        """
        async with self.connection.execute(query, (user_id,)) as cursor:
            row = await cursor.fetchone()

        if not row:
            return None

        return UserSchema(
            id=row[0],
            name=row[1],
            email=row[2],
            hashed_password=row[3],
            role=row[4],
            created_at=row[5],
        )

    async def get_many(self, limit: int, offset: int) -> list[UserSchema]:
        query = """
            SELECT id, name, email, password_hash, role, created_at
            FROM users
            LIMIT ? OFFSET ?
        """

        async with self.connection.execute(query, (limit, offset)) as cursor:
            row = await cursor.fetchmany()

        if not row:
            return []

        return list(map(UserSchema.model_validate, row))

    async def remove_by_id(self, user_id: UserId) -> None:
        query = "DELETE FROM users WHERE id = ?"
        await self.connection.execute(query, (user_id,))
