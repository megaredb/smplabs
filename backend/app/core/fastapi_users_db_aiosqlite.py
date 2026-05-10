from typing import Any, Generic

import aiosqlite
from fastapi_users.db import BaseUserDatabase
from fastapi_users.models import ID, OAP, UOAP, UP


class AioSqliteUserDatabase(BaseUserDatabase[UP, ID], Generic[UP, ID]):  # noqa: UP046
    """Database adapter for aiosqlite (raw SQL, no ORM).

    :param user_table: Name of the users table.
    :param oauth_table: Name of the OAuth accounts table (optional).
    :param user_model: Pydantic model class for the user.
    :param db: An open aiosqlite.Connection instance.
    """

    def __init__(
        self,
        user_model: type[UP],
        db: aiosqlite.Connection,
        user_table: str = "user",
        oauth_table: str = "oauth_account",
    ) -> None:
        self.user_model = user_model
        self.db = db
        self.user_table = user_table
        self.oauth_table = oauth_table
        self.db.row_factory = aiosqlite.Row

    def _row_to_user(self, row: aiosqlite.Row) -> UP:
        """Convert a DB row to the user model."""
        return self.user_model(**dict(row))

    async def _get_user_by_query(self, query: str, params: tuple) -> UP | None:
        async with self.db.execute(query, params) as cursor:
            row = await cursor.fetchone()
        if row is None:
            return None
        return self._row_to_user(row)

    async def get(self, id: ID) -> UP | None:
        """Get a single user by id."""
        query = f"SELECT * FROM {self.user_table} WHERE id = ?"  # noqa: S608
        return await self._get_user_by_query(query, (str(id),))

    async def get_by_email(self, email: str) -> UP | None:
        query = f"SELECT * FROM {self.user_table} WHERE lower(email) = lower(?)"  # noqa: S608
        return await self._get_user_by_query(query, (email,))

    async def get_by_oauth_account(self, oauth: str, account_id: str) -> UP | None:
        """Get a user by OAuth provider + remote account id."""
        query = (
            f"SELECT u.* FROM {self.user_table} u "  # noqa: S608
            f"JOIN {self.oauth_table} oa ON oa.user_id = u.id "
            f"WHERE oa.oauth_name = ? AND oa.account_id = ?"
        )
        return await self._get_user_by_query(query, (oauth, account_id))

    async def create(self, create_dict: dict[str, Any]) -> UP:
        """Insert a new user row and return the created user."""
        columns = ", ".join(create_dict.keys())
        placeholders = ", ".join("?" for _ in create_dict)
        values = tuple(
            str(v) if not isinstance(v, (int, float, bool, type(None))) else v
            for v in create_dict.values()
        )
        async with self.db.cursor() as cursor:
            query = (
                f"INSERT INTO {self.user_table} ({columns}) VALUES ({placeholders}) "  # noqa: S608
                f"RETURNING id"
            )
            await cursor.execute(query, values)
            new_user_id = await cursor.fetchone()

            if not new_user_id:
                msg = "User was not created"
                raise ValueError(msg)
            new_user_id: ID = new_user_id[0]

        await self.db.commit()

        user = await self.get(new_user_id)

        if user is None:
            msg = "User was not created"
            raise ValueError(msg)

        return user

    async def update(self, user: UP, update_dict: dict[str, Any]) -> UP:
        """Update an existing user row."""
        if not update_dict:
            return user

        set_clause = ", ".join(f"{k} = ?" for k in update_dict)
        values = tuple(
            str(v) if not isinstance(v, (int, float, bool, type(None))) else v
            for v in update_dict.values()
        )
        query = f"UPDATE {self.user_table} SET {set_clause} WHERE id = ?"  # noqa: S608
        await self.db.execute(query, (*values, str(user.id)))
        await self.db.commit()

        updated = await self.get(user.id)
        if updated is None:
            msg = "User disappeared after update"
            raise ValueError(msg)
        return updated

    async def delete(self, user: UP) -> None:
        """Delete a user row."""
        query = f"DELETE FROM {self.user_table} WHERE id = ?"  # noqa: S608
        await self.db.execute(query, (str(user.id),))
        await self.db.commit()

    async def add_oauth_account(
        self: AioSqliteUserDatabase[UOAP, ID],
        user: UOAP,
        create_dict: dict[str, Any],
    ) -> UOAP:
        """Insert an OAuth account row linked to the user."""
        create_dict["user_id"] = str(user.id)
        columns = ", ".join(create_dict.keys())
        placeholders = ", ".join("?" for _ in create_dict)
        values = tuple(create_dict.values())

        query = f"INSERT INTO {self.oauth_table} ({columns}) VALUES ({placeholders})"  # noqa: S608
        await self.db.execute(query, values)
        await self.db.commit()

        updated = await self.get(user.id)
        if updated is None:
            raise ValueError
        return updated

    async def update_oauth_account(
        self: AioSqliteUserDatabase[UOAP, ID],
        user: UOAP,
        oauth_account: OAP,
        update_dict: dict[str, Any],
    ) -> UOAP:
        """Update an existing OAuth account row."""
        if not update_dict:
            return user

        set_clause = ", ".join(f"{k} = ?" for k in update_dict)
        values = tuple(update_dict.values())

        query = (
            f"UPDATE {self.oauth_table} "  # noqa: S608
            f"SET {set_clause} "
            f"WHERE oauth_name = ? AND account_id = ?"
        )
        await self.db.execute(
            query,
            (*values, oauth_account.oauth_name, oauth_account.account_id),
        )
        await self.db.commit()

        updated = await self.get(user.id)
        if updated is None:
            raise ValueError
        return updated  # type: ignore[return-value]
