import asyncio
import stripe
from app.core.config import settings

async def main():
    try:
        client = stripe.StripeClient(
            settings.STRIPE_SECRET_KEY, 
            http_client=stripe.AIOHTTPClient()
        )
        session = await client.v1.checkout.sessions.create_async(
            params={
                "payment_method_types": ["card"],
                "line_items": [{"price_data": {"currency": "uah", "product_data": {"name": "test"}, "unit_amount": 1000}, "quantity": 1}],
                "mode": "payment",
                "success_url": "http://localhost/success",
                "cancel_url": "http://localhost/cancel",
            }
        )
        print("Success:", session.url)
    except Exception as e:
        print("Error:", repr(e))

asyncio.run(main())
