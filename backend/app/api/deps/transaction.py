from typing import Annotated

from fastapi import Depends

from app.api.deps.unit_of_work import get_uow
from app.interfaces.unit_of_work import IUnitOfWork  # noqa: TC001
from app.services.transaction_service import TransactionService


def get_transaction_service(
    uow: Annotated[IUnitOfWork, Depends(get_uow)],
) -> TransactionService:
    return TransactionService(uow)
