from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.interfaces.unit_of_work import IUnitOfWork
    from app.schemas.transaction import Transaction, TransactionCreate, TransactionId


class TransactionService:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def add_transaction(self, transaction: TransactionCreate) -> None:
        # 1. Отримуємо дані збору з бази
        campaign = await self.uow.campaigns.get_by_id(transaction.campaign_id)
        if not campaign:
            msg = "Збір не знайдено"
            raise ValueError(msg)

        # 2. Перевірка дати: чи не закінчився час
        if campaign.end_date:
            now = (
                datetime.now(UTC)
                if campaign.end_date.tzinfo
                else datetime.now()
            )
            if now > campaign.end_date:
                msg = "Час збору вже минув, донати не приймаються."
                raise ValueError(msg)

        # 3. Перевірка суми: щоб не перевищити ціль
        remaining = campaign.target_amount - campaign.current_amount
        if transaction.amount > remaining:
            msg = f"Сума перевищує залишок. Максимум можна задонатити {remaining} ₴"
            raise ValueError(
                msg
            )

        # 4. Якщо перевірки пройдені, записуємо транзакцію
        await self.uow.transactions.add_one(transaction)
        await self.uow.campaigns.update_current_amount(
            transaction.campaign_id, transaction.amount
        )

    async def get_transaction(
        self, transaction_id: TransactionId
    ) -> Transaction | None:
        return await self.uow.transactions.get_by_id(transaction_id)

    async def remove_transaction(self, transaction_id: TransactionId) -> None:
        await self.uow.transactions.remove_by_id(transaction_id)

    async def get_transactions_by_donor(
        self, donor_id: int, offset: int = 0, limit: int = 50
    ) -> list[Transaction]:
        return await self.uow.transactions.get_by_donor_id(donor_id, limit, offset)
