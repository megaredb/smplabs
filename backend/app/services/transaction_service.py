from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.interfaces.unit_of_work import IUnitOfWork
    from app.schemas.transaction import Transaction, TransactionCreate, TransactionId


class TransactionService:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def add_transaction(self, transaction: TransactionCreate) -> None:
        await self.uow.transactions.add_one(transaction)

    async def get_transaction(
        self, transaction_id: TransactionId
    ) -> Transaction | None:
        return await self.uow.transactions.get_by_id(transaction_id)

    async def remove_transaction(self, transaction_id: TransactionId) -> None:
        await self.uow.transactions.remove_by_id(transaction_id)
