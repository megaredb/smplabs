from typing import TYPE_CHECKING, Annotated

from fastapi import Depends

from app.api.deps.unit_of_work import get_uow
from app.core.database import get_db_connection_with_context
from app.core.fastapi_users_db_aiosqlite import AioSqliteUserDatabase
from app.schemas.user import UserDB
from app.services.user_service import UserService

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    import aiosqlite

    from app.interfaces.unit_of_work import IUnitOfWork


def get_user_service(
    uow: Annotated[IUnitOfWork, Depends(get_uow)],
) -> UserService:
    return UserService(uow)


async def get_user_db(
    db: Annotated[aiosqlite.Connection, Depends(get_db_connection_with_context)],
) -> AsyncGenerator[AioSqliteUserDatabase]:
    yield AioSqliteUserDatabase(UserDB, db, user_table="users")
