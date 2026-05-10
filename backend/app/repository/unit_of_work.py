from typing import TYPE_CHECKING, Self

from app.interfaces.unit_of_work import IUnitOfWork
from app.repository.campaign_repo import CampaignRepository
from app.repository.transaction_repo import TransactionRepository
from app.repository.user_repo import UserRepository

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable
    from types import TracebackType

    import aiosqlite


class UnitOfWork(IUnitOfWork):
    def __init__(
        self, connection_factory: Callable[[], Awaitable[aiosqlite.Connection]]
    ) -> None:
        self._connection_factory = connection_factory
        self._connection: aiosqlite.Connection | None = None

    @property
    def connection(self) -> aiosqlite.Connection:
        if not self._connection:
            msg = "Connection is not initialized"
            raise RuntimeError(msg)
        return self._connection

    async def __aenter__(self) -> Self:
        self._connection = await self._connection_factory()

        self.users = UserRepository(self.connection)
        self.transactions = TransactionRepository(self.connection)
        self.campaigns = CampaignRepository(self.connection)

        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if not self._connection:
            return
        try:
            if exc_type is None:
                await self.commit()
            else:
                await self.rollback()
        finally:
            await self._connection.close()

    async def commit(self) -> None:
        if self._connection:
            await self._connection.commit()

    async def rollback(self) -> None:
        if self._connection:
            await self._connection.rollback()
