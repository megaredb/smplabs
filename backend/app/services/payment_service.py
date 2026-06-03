import stripe

from app.core.config import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

from stripe import StripeClient


class PaymentService:
    def __init__(self) -> None:
        self.client = StripeClient(settings.STRIPE_SECRET_KEY)

    async def create_checkout_session(
        self, campaign_id: int, amount: float, donor_id: int | None
    ) -> str:
        """Creates a Stripe Checkout Session for a donation.
        Returns the checkout URL.
        """
        # Convert amount to cents (assuming amount is in USD/UAH, e.g. 10.50 -> 1050)
        amount_in_cents = int(amount * 100)

        session = await self.client.v1.checkout.sessions.create_async(
            params={
                "payment_method_types": ["card"],
                "line_items": [
                    {
                        "price_data": {
                            "currency": "uah",
                            "product_data": {
                                "name": f"Donation to Campaign #{campaign_id}",
                            },
                            "unit_amount": amount_in_cents,
                        },
                        "quantity": 1,
                    }
                ],
                "mode": "payment",
                "success_url": f"{settings.FRONTEND_HOST}/campaigns/{campaign_id}?payment=success",
                "cancel_url": f"{settings.FRONTEND_HOST}/campaigns/{campaign_id}?payment=cancel",
                "metadata": {
                    "campaign_id": str(campaign_id),
                    "donor_id": str(donor_id) if donor_id else "",
                },
            }
        )

        return session.url

    def construct_event(self, payload: str, sig_header: str) -> stripe.Event:
        """Validates the Stripe webhook signature and returns the Event."""
        return stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
