from http import HTTPStatus
from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps.transaction import get_transaction_service
from app.core.users import current_user
from app.schemas.transaction import (
    TransactionCreate,
    TransactionId,
    TransactionResponse,
)

if TYPE_CHECKING:
    from app.schemas.user import UserDB
    from app.services.transaction_service import TransactionService

transactions_router = APIRouter()


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


@transactions_router.get("/my")
async def get_my_transactions(
    _current_user: Annotated[UserDB, Depends(current_user)],
    transaction_service: Annotated[
        TransactionService, Depends(get_transaction_service)
    ],
    offset: int = 0,
    limit: int = 10,
) -> list[TransactionResponse]:
    transactions = await transaction_service.get_transactions_by_donor(
        _current_user.id, offset, limit
    )
    return [TransactionResponse.model_validate(t) for t in transactions]


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


from fastapi.responses import HTMLResponse

from app.services.invoice_service import InvoiceService


@transactions_router.get("/{transaction_id}/invoice", response_class=HTMLResponse)
async def get_invoice(
    transaction_id: TransactionId,
    _current_user: Annotated[UserDB, Depends(current_user)],
    transaction_service: Annotated[
        TransactionService, Depends(get_transaction_service)
    ],
):
    """Get the HTML invoice for a specific transaction."""
    transaction = await transaction_service.get_transaction(transaction_id)
    if not transaction:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Transaction not found")

    if transaction.donor_id != _current_user.id and not _current_user.is_superuser:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Not authorized to view this invoice")

    invoice_service = InvoiceService()
    return invoice_service.generate_html_invoice(TransactionResponse.model_validate(transaction), donor_name=_current_user.name)
