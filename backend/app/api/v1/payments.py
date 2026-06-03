import logging
from typing import TYPE_CHECKING, Annotated

import stripe
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel

from app.api.deps.unit_of_work import get_uow
from app.core.users import possible_user
from app.schemas.transaction import TransactionCreate
from app.schemas.campaign import CampaignUpdate
from app.services.payment_service import PaymentService

if TYPE_CHECKING:
    from app.interfaces.unit_of_work import IUnitOfWork
    from app.schemas.user import UserDB

logger = logging.getLogger(__name__)

payments_router = APIRouter(prefix="/payments", tags=["payments"])


class CheckoutRequest(BaseModel):
    campaign_id: int
    amount: float


class CheckoutResponse(BaseModel):
    url: str


@payments_router.post("/create-checkout-session", response_model=CheckoutResponse)
async def create_checkout_session(
    checkout_req: CheckoutRequest,
    possible_user: Annotated[UserDB | None, Depends(possible_user)] = None,
) -> CheckoutResponse:
    payment_service = PaymentService()
    donor_id = possible_user.id if possible_user else None

    try:
        checkout_url = await payment_service.create_checkout_session(
            campaign_id=checkout_req.campaign_id,
            amount=checkout_req.amount,
            donor_id=donor_id,
        )
        return CheckoutResponse(url=checkout_url)
    except Exception as e:
        logger.exception("Failed to create checkout session")
        raise HTTPException(status_code=400, detail=str(e))


@payments_router.post("/webhook")
async def stripe_webhook(
    request: Request,
    uow: Annotated[IUnitOfWork, Depends(get_uow)],
):
    payment_service = PaymentService()
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        if not sig_header:
            raise stripe.SignatureVerificationError("Missing signature header", sig_header)
        event = payment_service.construct_event(payload.decode("utf-8"), sig_header)
    except ValueError as e:
        # Invalid payload
        logger.exception(f"Invalid payload: {e}")
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.SignatureVerificationError as e:
        # Invalid signature
        logger.exception(f"Invalid signature: {e}")
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Handle the event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        metadata = session.metadata or {}
        campaign_id_str = metadata.get("campaign_id") if isinstance(metadata, dict) else getattr(metadata, "campaign_id", None)
        donor_id_str = metadata.get("donor_id") if isinstance(metadata, dict) else getattr(metadata, "donor_id", None)
        amount_total = session.amount_total or 0  # in cents

        if not campaign_id_str:
            logger.error("Missing campaign_id in webhook metadata")
            return Response(status_code=200)

        campaign_id = int(campaign_id_str)
        donor_id = int(donor_id_str) if donor_id_str else None
        amount = amount_total / 100.0

        # Record the transaction using UOW
        transaction_data = TransactionCreate(
            campaign_id=campaign_id,
            donor_id=donor_id,
            amount=amount,
            comment="Paid via Stripe",
        )

        try:
            await uow.transactions.add_one(transaction_data)

            # Update campaign total amount
            campaign = await uow.campaigns.get_by_id(campaign_id)
            if campaign:
                await uow.campaigns.update_current_amount(campaign_id, amount)

            await uow.commit()
            logger.info(f"Transaction recorded for campaign {campaign_id}")
        except Exception:
            await uow.rollback()
            logger.exception("Failed to save transaction from webhook")
            raise HTTPException(status_code=500, detail="Database error")

    return Response(status_code=200)
