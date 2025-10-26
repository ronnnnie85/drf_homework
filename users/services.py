import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_product(name: str, description: str | None = None) -> dict:
    """Создаёт продукт в Stripe"""
    return stripe.Product.create(name=name, description=description or "")


def create_price(product_id: str, unit_amount: int, currency: str) -> dict:
    """Создаёт цену в Stripe"""
    return stripe.Price.create(
        product=product_id,
        unit_amount=unit_amount,   # сумма в копейках
        currency=currency,
    )


def create_checkout_session(price_id: str, success_url: str, cancel_url: str) -> dict:
    """Создаёт Checkout Session и возвращает сессию"""
    return stripe.checkout.Session.create(
        mode="payment",
        line_items=[{"price": price_id, "quantity": 1}],
        success_url=success_url,
        cancel_url=cancel_url,
    )
