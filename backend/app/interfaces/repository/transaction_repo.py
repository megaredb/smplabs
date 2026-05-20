from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from app.schemas.user import UserId

if TYPE_CHECKING:
    from app.schemas.transaction import Transaction, TransactionCreate, TransactionId


class ITransactionRepository(ABC):
    @abstractmethod
    async def add_one(self, data: TransactionCreate) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, transaction_id: TransactionId) -> Transaction | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_donor_id(
        self, donor_id: UserId, limit: int, offset: int
    ) -> list[Transaction]:
        raise NotImplementedError

    @abstractmethod
    async def remove_by_id(self, transaction_id: TransactionId) -> None:
        raise NotImplementedError
