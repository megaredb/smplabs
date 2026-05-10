from __future__ import annotations

from http import HTTPStatus
from typing import Annotated  # TYPE_CHECKING можна прибрати

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps.transaction import get_transaction_service

from app.schemas.transaction import (
    TransactionId,
    TransactionResponse,
    TransactionCreate,
)

from app.services.transaction_service import TransactionService

transactions_router = APIRouter()


@transactions_router.get("/{transaction_id}")
async def get_transaction(
    transaction_id: TransactionId,
    transaction_service: Annotated[
        TransactionService, Depends(get_transaction_service)
    ],
) -> TransactionResponse:
    transaction = await transaction_service.get_transaction(transaction_id)

    if not transaction:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Transaction not found"
        )

    return TransactionResponse.model_validate(transaction)


@transactions_router.post("/", status_code=HTTPStatus.CREATED)
async def create_transaction(
    transaction: TransactionCreate,
    transaction_service: Annotated[
        TransactionService, Depends(get_transaction_service)
    ],
) -> None:
    try:
        await transaction_service.add_transaction(transaction)
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e


""""
@transactions_router.get("/")
async def get_transactions(
    transaction_service: Annotated[
        TransactionService, Depends(get_transaction_service)
    ],
    offset: int = 0,
    limit: int = 10,
) -> list[TransactionResponse]:
    transactions = await transaction_service.get_transactions(offset, limit)
    return [TransactionResponse.model_validate(t) for t in transactions]
"""


@transactions_router.delete("/{transaction_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_transaction(
    transaction_id: TransactionId,
    transaction_service: Annotated[
        TransactionService, Depends(get_transaction_service)
    ],
) -> None:
    transaction = await transaction_service.get_transaction(transaction_id)

    if not transaction:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Transaction not found"
        )

    await transaction_service.remove_transaction(transaction_id)
