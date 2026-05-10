from __future__ import annotations

from typing import TYPE_CHECKING

from app.interfaces.repository.transaction_repo import ITransactionRepository
from app.schemas.transaction import Transaction as TransactionSchema

if TYPE_CHECKING:
    import aiosqlite

    from app.schemas.transaction import TransactionCreate, TransactionId


class TransactionRepository(ITransactionRepository):
    def __init__(self, connection: aiosqlite.Connection) -> None:
        self.connection = connection

    async def add_one(self, data: TransactionCreate) -> None:
        query = """
        INSERT INTO transactions (campaign_id, donor_id, amount, comment)
        VALUES (?, ?, ?, ?)
        """
        await self.connection.execute(
            query, (data.campaign_id, data.donor_id, data.amount, data.comment)
        )

    async def get_by_id(
        self, transaction_id: TransactionId
    ) -> TransactionSchema | None:
        query = """
        SELECT id, campaign_id, donor_id, amount, comment, created_at
        FROM transactions
        WHERE id = ?
        """
        async with self.connection.execute(query, (transaction_id,)) as cursor:
            row = await cursor.fetchone()

        if not row:
            return None

        return TransactionSchema(
            id=row[0],
            campaign_id=row[1],
            donor_id=row[2],
            amount=row[3],
            comment=row[4],
            created_at=row[5],
        )

    async def remove_by_id(self, transaction_id: TransactionId) -> None:
        query = """
        DELETE FROM transactions
        WHERE id = ?
        """
        await self.connection.execute(query, (transaction_id,))
