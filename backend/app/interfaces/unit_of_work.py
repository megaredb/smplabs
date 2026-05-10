from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from types import TracebackType

    from app.interfaces.repository.campaign_repo import ICampaignRepository
    from app.interfaces.repository.transaction_repo import ITransactionRepository
    from app.interfaces.repository.user_repo import IUserRepository


class IUnitOfWork(ABC):
    users: IUserRepository
    campaigns: ICampaignRepository
    transactions: ITransactionRepository

    @abstractmethod
    async def __aenter__(self) -> Self:
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError
