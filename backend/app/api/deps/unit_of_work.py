from typing import TYPE_CHECKING

from app.core.database import get_db_connection
from app.repository.unit_of_work import UnitOfWork

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from app.interfaces.unit_of_work import IUnitOfWork


async def get_uow() -> AsyncGenerator[IUnitOfWork]:
    uow = UnitOfWork(get_db_connection)
    async with uow:
        yield uow
