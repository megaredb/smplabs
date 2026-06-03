from stripe import StripeClient
from app.core.config import settings

def main():
    client = StripeClient(settings.STRIPE_SECRET_KEY)
    try:
        session = client.v1.checkout.sessions.create(
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

main()
